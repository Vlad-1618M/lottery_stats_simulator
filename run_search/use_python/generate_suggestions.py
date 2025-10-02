#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________________________________________________________________________________________________________________
# -- this algo based search engine shouwld be aware of both data sources:
#    Real Lotto Draw Results: coming in from playwright scrapes: see --> lotto_draw_results/* path
#    Player's Records Selections: see --> */catalog/* paths ( e.g  August-2025/catalog/* | September-2025/catalog/* ) paths
# ________________________________________________________________________________________________________________________

import sys
import json
from time import sleep
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Tuple, Union, Generator

sys.path.append(str(Path(__file__).resolve().parents[2]))
import use_rarest_sequence
from injectors import runtime_perf as perf

colored = Console()

up_arrow_decor = "[bold yellow] ↑ [/bold yellow]"
down_arrow_decor = "[dim] ↓ [/dim]"
yellow_arrow_reversed = "[bold yellow] ← [/bold yellow]"
yellow_arrow_decor = "[bold yellow] → [/bold yellow]"
red_arrow_decor = "[bold red] → [/bold red]"
visual_decor = "\n"+"[gray]=[/gray]" * 90 + "\n"
visual_decor_underline = "\t"+"[dim]_[/dim]"* 97
_underline = "[dim]_[/dim]"* 20

# ____ this is to map raw filename stems to normalized game names
# ____ playwright scrapes data and uses ursl as filenames for artifact .json names, so this is a minor hack ...

GAME_NAME_ALIASES = {
    "megamillions": "megamillion",
    "powerball": "powerball",
    "lotto": "lotto",
    "pick3": "pick3",
    "pick4": "pick4",
    "luckydaylotto": "luckyday",
}

# ____ canonical supported game names a.k. alias map for values:
SUPPORTED_GAMES = sorted(set(GAME_NAME_ALIASES.values()))

def iter_json_catalogs_with_trace(json_paths: List[Union[str, Path]]) -> Generator[Tuple[dict, str, int], None, None]:
    for path in map(Path, json_paths):
        raw_tag = path.stem.split("_")[0].lower()
        game_tag = GAME_NAME_ALIASES.get(raw_tag, raw_tag)
        try:
            with path.open("r", encoding="utf-8") as record_file:
                try:
                    data = json.load(record_file)
                    if isinstance(data, list):
                        for line_no, record in enumerate(data, start=1):
                            if "selection" not in record and "primary_numbers" in record:
                                record["game"] = game_tag
                                
                                # Handle both formats of primary_numbers
                                primary_nums = record.get("primary_numbers", [])
                                if primary_nums and isinstance(primary_nums[0], str) and "," in primary_nums[0]:
                                    # Format: ["11, 12, 29, 42, 44, 47"]
                                    primary_nums = [num.strip() for num in primary_nums[0].split(",")]
                                else:
                                    # Format: ["5", "7", "20", "26", "34", "40"]
                                    primary_nums = primary_nums
                                
                                record["selection"] = {
                                    "primary": list(map(int, primary_nums)),
                                    "mega": [int(record["mega"])] if record.get("mega") not in [None, "N/A"] else [],
                                    "power": [int(record["powerball"])] if record.get("powerball") not in [None, "N/A"] else []}
                            # yield record, path.name, line_no
                            yield record, str(path), line_no

                except json.JSONDecodeError:
                    continue
        except Exception as e:
            colored.print(f"[red]Failed to open {path}[/red]: {e}")


@perf.timeit
# ___________________________________
def build_augmented_frequency_map(json_paths: List[Union[str, Path]]):
    frequency_map = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
    origin_data_source_trace = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    # count total records first (cheap scan)
    total_records = 0
    for path in map(Path, json_paths):
        try:
            with path.open("r", encoding="utf-8") as record_file:
                data = json.load(record_file)
                if isinstance(data, list):
                    total_records += len(data)
                else:
                    total_records += 1
        except Exception:
            continue

    with Progress() as progress:
        task = progress.add_task("[bold cyan]Building frequency map ...", total=total_records)
        for record, file_name, line_number in iter_json_catalogs_with_trace(json_paths):
            game = record.get("game")
            selection = record.get("selection", {})
            if not game or not selection:
                progress.advance(task)
                continue

            for sequence_names, sequence_numbers in selection.items():
                if not isinstance(sequence_numbers, list):
                    continue
                for idx, values in enumerate(sequence_numbers):
                    try:
                        value_int = int(values)
                        frequency_map[game][sequence_names][idx][value_int] += 1
                        origin_data_source_trace[game][sequence_names][idx][value_int].append((file_name, line_number))
                    except ValueError:
                        continue
            progress.advance(task)

    return frequency_map, origin_data_source_trace

# ___________________________________
def generate_unique_gameplay_sequence(
        frequency_map: Dict[str, Dict[str, Dict[int, Counter]]],
        origin_data_source_trace: Dict[str, Dict[str, Dict[int, Dict[int, List[Tuple[str, int]]]]]],
        game: str, sequence_key: str = "primary", debug: bool = False) -> Tuple[List[int], Dict[int, Tuple[int, int, str]], List[int]]:

    raw_sequence = use_rarest_sequence.construct_rarest_sequence(frequency_map, game=game, sequence_key=sequence_key, debug=debug)
    game_map = frequency_map[game][sequence_key]
    trace_map = origin_data_source_trace[game][sequence_key]

    origin = {}
    seen = set()
    dropped = []
    final_sequence = []

    for idx, values in enumerate(raw_sequence):
        freq = game_map.get(idx, {}).get(values, 0)
        source_list = trace_map.get(idx, {}).get(values, [])
        source_str = f"{source_list[0][0]}:{source_list[0][1]}" if source_list else "unknown"

        if values in seen:
            dropped.append(values)
            continue
    
        seen.add(values)
        final_sequence.append(values)
        origin[idx] = (values, freq, source_str)
    
    return final_sequence, origin, dropped


# ___________________________________ get data source type | use full file paths: 
def get_source_type(full_path):
    _historic_catalog = "[ [bold green italic] HISTORIC [/bold green italic]\t]"
    _recent_catalog = "[ [bold orange1 italic] RECENT [/bold orange1 italic]\t]"
    _user_catalog = "[ [bold magenta italic] PLAYER [/bold magenta italic]  \t]"
    
    data_source_path = str(full_path).lower()
    
    if "/catalog/" in data_source_path:
        return _user_catalog
    elif "historical_lotto_draw_results" in data_source_path:
        return _historic_catalog
    elif "lotto_draw_results" in data_source_path:
        return _recent_catalog
    else:
        return "[ UNKNOWN ]"

# ___________________________________
def display_suggestions(
        freq_map: Dict[str, Dict[str, Dict[int, Counter]]], 
        origin_data_source_trace: Dict[str, Dict[str, Dict[int, Dict[int, List[Tuple[str, int]]]]]], games: Optional[List[str]] = None, show_freqs = False):

    games = games or SUPPORTED_GAMES
    seq_keys = {
        "powerball": ["primary", "power"],
        "megamillion": ["primary", "mega"],
        "lotto": ["primary"],
        "pick3": ["primary"],
        "pick4": ["primary"],
        "luckyday": ["primary"],
    }

    for game in games:
        for key in seq_keys.get(game, ["primary"]):
            if key not in freq_map[game]:
                continue

        if game not in freq_map:
            colored.print(f"...[bold red]skipping[/bold red] {yellow_arrow_decor} [dim]{game}[/dim] — [bright_red]no data[/bright_red]:")
            continue
        
        # DEBUG: Show frequency distribution for each game
        if show_freqs:
            colored.print(f"{visual_decor_underline}")
            colored.print(f"\n[bold yellow]Frequency Analysis[/bold yellow]:{yellow_arrow_decor} [bold magenta]{game.upper()}[/bold magenta]:")
            for key in seq_keys.get(game, ["primary"]):
                if key not in freq_map[game]:
                    continue
            
            colored.print(f" [bold blue]{key}:[/bold blue]{yellow_arrow_reversed} key pair:")
            for idx in sorted(freq_map[game][key].keys()):
                counter = freq_map[game][key][idx]
                total = sum(counter.values())
                colored.print(f" [bold]Index[/bold] {idx}: total={total}, top5={counter.most_common(5)}")
            colored.print(f"{visual_decor_underline}")

        for key in seq_keys.get(game, ["primary"]):
            if key not in freq_map[game]:
                continue

            try:
                picks, trace, dropped = generate_unique_gameplay_sequence(freq_map, origin_data_source_trace, game=game, sequence_key=key, debug=False)
                header = f"\n\t[dim]Game Type[/dim]:{yellow_arrow_decor}[bold red]{game.upper()}[/bold red]" \
                         f"[dim]+[/dim] [bold magenta]key[/bold magenta]:{yellow_arrow_decor}[bold yellow italic]{key.upper()}[/bold yellow italic]:"
                colored.print(f"{header}")
                colored.print(f"\t[bright_blue]Suggested[/bright_blue] picks for upcoming game:"
                              f"{yellow_arrow_decor}[bold green italic]captured sequence:[/bold green italic] [bold yellow]{picks}[/bold yellow]\n")

                for idx, (values, freq, source) in trace.items():
                    full_path = source.split(":")[0]
                    line_num = source.split(":")[1]
                    filename = Path(full_path).name  # Extract just filename for display
                    source_type = get_source_type(full_path)  # Use full path for accurate detection
                    
                    colored.print(f"\t[dim]{source_type}[/dim] [dim]index[/dim]: [bold white]{idx:<2}[/bold white]{red_arrow_decor}"
                                f"[bold green]{values:<2}[/bold green] [dim]|[/dim]" 
                                f"[dim italic]freq[/dim italic]: [bold]{freq:>5}[/bold]"
                                f" | [dim italic]source[/dim italic]:{red_arrow_decor}"
                                f"[italic green]{filename}[/italic green]\t"
                                f"[dim italic]line:[/dim italic] [bold cyan]{line_num:>4}[/bold cyan]{yellow_arrow_reversed:>2} ref:")

                if dropped:
                    colored.print(f"[bold yellow]\t|[/bold yellow] dropped{up_arrow_decor}[dim]duplicate[/dim]:\t {yellow_arrow_decor}[bold red]{dropped}[/bold red]")
                    colored.print(visual_decor_underline)
            except Exception as err:
                colored.print(f"[red]Error processing {game}:{key} →[/red] {err}")
            
# ___________________________________
def _date_source_details():
    # __ using Path.glob() in retunr call | helps to retunr [] list in case one of the data dirs is yet to be created:
    data_in = [str(source_path) for source_path in Path("./lotto_draw_results").glob("*.json")] \
            + [str(source_path) for source_path in Path("./historical_lotto_draw_results").glob("*.json")] \
            + [str(source_path) for source_path in Path(".").glob("*/catalog/*.json")]
    
    for idx, source in enumerate(sorted(data_in), start=1):
        # ___ check: if catalog files
        if "/catalog/" in source:
            head, center, tail = source.partition("-2025/catalog/")
            colored.print(
                f"[dim]index[/dim]:{yellow_arrow_decor}{idx:<5}[dim italic]"
                f"\tOriginated On[/dim italic] {yellow_arrow_decor:>34}[bold]{head:<7}[/bold]"
                f"[blue italic]{center.split("/")[0]}[/blue italic] "
                f"[dim]Source Name[/dim]{red_arrow_decor}[bright_cyan italic]{tail.upper():<17}[/bright_cyan italic]")
        
        # ___ check: if historic files
        elif "historical_lotto_draw_results" in source:
            filename = Path(source).name
            head, center, tail = filename.partition("_2025")
            colored.print(
                f"[dim]index[/dim]:{red_arrow_decor}[bold yellow]{idx:<5}[/bold yellow]"
                f" [dim italic]\tHistoric Records[/dim italic]: {red_arrow_decor}"
                f"{head.capitalize()}")
        
        # ___ check: if recent draw files
        elif "lotto_draw_results" in source:
            sleep(0.05)
            head, center, tail = source.partition("_2025-")
            colored.print(
                f"[dim]index[/dim]:{red_arrow_decor}[bold yellow]{idx}[/bold yellow]"
                f" [dim italic]\tRecent Records[/dim italic]: {red_arrow_decor:>26}"
                f"{head:<34}[bold italic magenta]2025[/bold italic magenta][dim italic]")
        
        else:
            # ___  any other files:
            colored.print(
                f"[dim]index[/dim]:{yellow_arrow_decor}{idx:<5}"
                f"\tUnknown Source: {source}")
    colored.rule(f"{up_arrow_decor} Data In Details {up_arrow_decor}")


@perf.timeit
def main(show_data_details=False, show_map=False):
    if show_data_details:
        _date_source_details()
    
    data_in = [str(source_path) for source_path in Path("./lotto_draw_results").glob("*.json")] \
            + [str(source_path) for source_path in Path("./historical_lotto_draw_results").glob("*.json")] \
            + [str(source_path) for source_path in Path(".").glob("*/catalog/*.json")]
    
    # ___ DEBUG: file type count:
    recent_count = len(list(Path("./lotto_draw_results").glob("*.json")))
    historic_count = len(list(Path("./historical_lotto_draw_results").glob("*.json")))
    catalog_count = len(list(Path(".").glob("*/catalog/*.json")))
    
    colored.print(f"\n[bold]Data to be injected in frequency map[/bold]: {down_arrow_decor}\n"
                  f"[bold green]{recent_count:>6}[/bold green] [dim italic]files[/dim italic]: {yellow_arrow_reversed} recent lottery draws:\n"
                  f"[bold green]{historic_count:>6}[/bold green] [dim italic]files[/dim italic]: {yellow_arrow_reversed} lottery draws history:\n"
                  f"[bold green]{catalog_count:>6}[/bold green] [dim italic]files[/dim italic]: {yellow_arrow_reversed} user data catalog:\n")
    
    freq_map, origin_data_source_trace = build_augmented_frequency_map(data_in)
    colored.rule(f"[bold cyan]Built scaled Frequency Map[/bold cyan]: detected game count: [bold green]{len(freq_map)}[/bold green] of game types:")
    display_suggestions(freq_map, origin_data_source_trace, show_freqs=show_map)

    # ________ debug | check games + keys summary:
    colored.print("\n[bold yellow]Frequency Map[/bold yellow] - Data Check:")
    colored.print(f"{down_arrow_decor}" * 6)
    for game in freq_map:
        keys = list(freq_map[game].keys())
        colored.print(f"[bold cyan]{game:<11}[/bold cyan] {yellow_arrow_decor} [bold magenta]keys[/bold magenta]: [bold green]{keys}[/bold green]")


if __name__ == "__main__":
    main()
    
    # ___________________ debug _________________________
    
    # main(show_data_details=False, show_map=False)
    # main(show_data_details=True, show_map=True)
    # main(show_data_details=False, show_map=True)
    # main(show_data_details=True, show_map=False)

    # data_in = [str(source_path) for source_path in Path("./lotto_draw_results").glob("*.json")] \
    #         + [str(source_path) for source_path in Path("./historical_lotto_draw_results").glob("*.json")] \
    #         + [str(source_path) for source_path in Path(".").glob("*/catalog/*.json")]
    
    # [print(f"ID: count: {idx} |\t Path:\t --> {name}", sleep(0.07)) for idx, name in enumerate(data_in, start =1)]

    # pipe = "[dim]|[/dim]"
    # base_dir = Path(__file__).resolve().parents[1]
    # [colored.print(f"{idx:<5}\t{source:>5}") for idx, source in enumerate(sorted(data_in), start=1)]