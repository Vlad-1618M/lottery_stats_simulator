#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from pathlib import Path
from rich.console import Console
from collections import defaultdict
from typing import List, Union, Generator

sys.path.append(str(Path(__file__).resolve().parents[1]))
from run_search import frequency_maps
from run_search import use_rarest_sequence
from injectors import runtime_perf as perf

colored = Console()

# __________ compare input sequence to draw results:
def compare_sequence_to_draws(input_sequence: List[int], game: str, sequence_key: str, records: List[dict], match_type: str = "exact", debug: bool = False,) -> List[dict]:
    matches = []
    input_set = set(input_sequence)
    job_pointer = "[bold]→[/bold] "
    pointer = "\t[bold magenta]→[/bold magenta] "
    _decorator_under = "\n"+"[dim]_[/dim]" * 95
    _decorator_equal = "\n"+"[dim]=[/dim]" * 95
    if debug:
        colored.print(f"{_decorator_equal}")
        colored.print("\n[bold blue]\t\t--- [bold white]DEBUG RUNTIME TRACE START[/bold white] --- [/bold blue]")
        colored.print(f"\nGame type [bold cyan]{game.upper()}[/bold cyan] [bold green]+[/bold green] [bold yellow]{sequence_key.upper()}[/bold yellow] records key:{_decorator_under}")

    for idx, record in enumerate(records):
        record_game = record.get("game", None)
        selection = record.get("selection", {})

        # Log record-level debug
        if debug:
            colored.print(f"{pointer}[dim]Record:[/dim] # [bold magenta]{idx}[/bold magenta]\t[dim]Record Type[/dim]: [bold orange1]{record_game}[/bold orange1]")
            colored.print(f"{pointer}[bold white]Selection[/bold white]:\t{selection}")

        if record_game != game:
            if debug:
                colored.print(f"{pointer}[bold red]Skipping[/bold red]:\t[dim]wrong game type[/dim]: [bold red]{record_game}[/bold red]:\n")
            continue

        drawn = selection.get(sequence_key)
        if not drawn:
            if debug:
                colored.print(f"[yellow]No drawn numbers for key '{sequence_key}'[/yellow]")
            continue

        try:
            drawn = list(map(int, drawn))
        except Exception as cast_error:
            colored.print(f"\n\t[bold red]Cast to int failed:[/bold red] {drawn} — {cast_error}\n")
            continue

        if debug:
            colored.print(f"{_decorator_equal}")
            colored.print(f"[dim]Compare:[/dim] Drawn Set: {job_pointer} [bold green]{drawn}[/bold green] | [dim]Target Seqence[/dim] [bold orange1]{input_sequence}[/bold orange1]")

        if match_type == "exact":
            if sorted(drawn) == sorted(input_sequence):
                colored.print("[bold green]EXACT MATCH FOUND[/bold green]")
                matches.append(record)

        elif match_type == "partial":
            overlap = input_set.intersection(set(drawn))
            if debug:
                colored.print(f"Overlap: [bold cyan]{sorted(overlap)}[/bold cyan]")
            if overlap:
                matches.append({
                    "draw": drawn,
                    "overlap": sorted(list(overlap)),
                    "draw_date": record.get("draw_date", record.get("date", "unknown")),
                    "match_count": len(overlap)
                })
    if debug:
        colored.print(f"{_decorator_equal}")
        colored.print(f"\n[bold blue]\t\t--- [bold white]DEBUG RUNTIME TRACE END[/bold white] --- [/bold blue]{_decorator_equal}")
    return matches


# @perf.timeit
# ________ load draw records from all jsons | inject 'game' and 'selection' keys:
def get_records(base_dir=None) -> List[str]:
    if base_dir is None:
        base_dir = Path(__file__).resolve().parents[1]
    return [str(records_path.absolute()) for records_path in (base_dir / "lotto_draw_results").glob("**/*.json")]

# @perf.timeit
def iter_json_catalogs(json_paths: List[Union[str, Path]], details: bool = False) -> Generator[dict, None, None]:
    for path in map(Path, json_paths):
        if details:
            colored.print(f"\n[dim]Reading Path[/dim] [bold]Record[/bold]:\t[dim]-->[/dim] [bold cyan]{path.parent}[/bold cyan]")
        try:
            with path.open("r", encoding="utf-8") as record_file:
                try:
                    data = json.load(record_file)
                    if isinstance(data, list):
                        if details:
                            colored.print(f"\t[dim]Game[/dim] Records:\t[dim]-->[/dim] [bold green]{len(data)}[/bold green] in [bold yellow]{path.name}[/bold yellow]\n\t"+"[bold blue]_[/bold blue]" * 95)
                        game_tag = path.stem.lower().split("_")[0]
                        for record in data:
                            record["game"] = game_tag
                            record["selection"] = {
                                "primary_numbers": record.get("primary_numbers", []),
                                "mega": [record.get("megaball") or record.get("powerball")] if record.get("megaball") or record.get("powerball") else []
                            }
                            yield record
                    else:
                        yield data  # ___ incase json data is not a list:
                except json.JSONDecodeError:
                    colored.print(f"[red] JSON decode error:[/red] {path.name} — fallback to line-by-line")
                    record_file.seek(0)
                    for idx, line in enumerate(record_file, start=1):
                        try:
                            yield json.loads(line)
                        except Exception as line_read_error:
                            colored.print(f"[red]Failed line {idx} in {path.name}:[/red] {line_read_error}")
        except Exception as file_read_error:
            colored.print(f"[red]Failed to open file:[/red] {path} — {file_read_error}")


# @perf.timeit
def data_load(show_loaded_count=False, see_details=False):
    records = []
    paths = get_records()
    count = 0
    for idx, record in enumerate(iter_json_catalogs(paths, details=see_details), start=1):
        records.append(record)
        if show_loaded_count:
            # for draw_keys, draw_values in record.items():
            #     out = f"[bold]{draw_keys}[/bold] [bold magenta]{draw_values}[/bold magenta]"
            colored.print(f"\t[bold red]{idx:<3}[/bold red] {json.dumps(record, ensure_ascii=False)}")
        count += 1
    colored.print(f"\n[bold]Total Records Load[/bold]: [bold green]{count}[/bold green]\n" + "[dim]=[/dim]" * 25)
    unique_games = set(read.get("game") for read in records)
    colored.print(f"[bold cyan]Games found:[/bold cyan] {sorted(unique_games)}")
    return records


# ______________ group numbers overlapped matches:
def show_matches_grouped(overlaps: List[dict]):
    grouped = defaultdict(list)
    for match in overlaps:
        grouped[match["match_count"]].append(match)

    for count in sorted(grouped.keys(), reverse=True):
        colored.print(f"\n[bold magenta]{count} number match(es)[/bold magenta] → {len(grouped[count])} draw(s):")
        for match in grouped[count]:
            colored.print(f"  → {match['draw']} | Overlap: [yellow]{match['overlap']}[/yellow] | Date: [green]{match['draw_date']}[/green]")

@perf.timeit
# ________ main logic:
def main(game: str, keys: str, match_depth: str = "partial", debug=False):
    """ game        : str  — e.g. 'powerball'
        keys        : str  — e.g. 'primary'
        match_depth : str  — 'partial' or 'exact' """

    match_depth = match_depth.lower().strip()
    if match_depth not in {"partial", "exact"}:
        raise ValueError("match_depth must be 'partial' or 'exact'")

    # records = data_load(show_loaded_count=False, see_details=False)
    # records = data_load(show_loaded_count=False, see_details=True)
    records = data_load(show_loaded_count=True, see_details=True)

    json_paths = frequency_maps.get_records()
    freq_map = frequency_maps.build_frequency_maps(json_paths)
    rarest_seq = use_rarest_sequence.construct_rarest_sequence(freq_map, game=game)
    colored.print(f"\n[bold]RARE SEQUENCE[/bold] → [cyan]{rarest_seq}[/cyan]")
    if debug:
        overlaps = compare_sequence_to_draws(input_sequence=rarest_seq, game=game, sequence_key=keys, records=records, match_type=match_depth, debug=True)
    overlaps = compare_sequence_to_draws(input_sequence=rarest_seq, game=game, sequence_key=keys, records=records, match_type=match_depth, debug=False)
    show_matches_grouped(overlaps=overlaps)
    # colored.print(f"\n[bold green]Matched {len(overlaps)} times with real results.[/bold green]\n")
    # colored.print(f"\n[bold green]{len(overlaps)}[/bold green] results matched around {rarest_seq} sequence data:\n")
    colored.print(f"[bold green]{len(overlaps)}[/bold green] results matched around {sorted(rarest_seq)} sequence data:\n")


if __name__ == "__main__":
    # main(game="powerball", keys="primary", match_depth="partial")
    # main(game="megamillion", keys="primary", match_depth="partial")
    # main(game="megamillion", keys="primary_numbers", match_depth="partial")
    
    
    main(game="powerball", keys="primary_numbers", match_depth="partial", debug=True)
    # main(game="powerball", keys="primary_numbers", match_depth="exact", debug=True)
    # main(game="megamillion", keys="primary_numbers", match_depth="partial")
    # main(game="megamillion", keys="primary_numbers", match_depth="exact")
    # main(game="lotto", keys="primary_numbers", match_depth="partial")
    # main(game="lotto", keys="primary_numbers", match_depth="exact")
