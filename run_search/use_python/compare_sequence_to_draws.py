#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import argparse
from pathlib import Path
from rich.console import Console
from collections import defaultdict
from typing import List, Union, Generator, Optional

sys.path.append(str(Path(__file__).resolve().parents[2]))
from injectors import runtime_perf as perf
import use_rarest_sequence
import frequency_maps

colored = Console()

# _____ Compare Logic:
def compare_sequence_to_draws(
        input_sequence: List[int], game: str, sequence_key: str, records: List[dict], match_type: str = "exact", debug: bool = False,) -> List[dict]:
    matches = []
    input_set = set(input_sequence)
    job_pointer = "[bold]→[/bold] "
    pointer = "\t[bold magenta]→[/bold magenta] "
    _decorator_under = "\n" + "[dim]_[/dim]" * 95
    _decorator_equal = "\n" + "[dim]=[/dim]" * 95

    if debug:
        colored.print(f"{_decorator_equal}")
        colored.print("\n[bold blue]\t\t--- [bold white]DEBUG RUNTIME TRACE START[/bold white] --- [/bold blue]")
        colored.print(f"\nGame type [bold cyan]{game.upper()}[/bold cyan] [bold green]+[/bold green] [bold yellow]{sequence_key.upper()}[/bold yellow] records key:{_decorator_under}")

    for idx, record in enumerate(records):
        record_game = record.get("game", None)
        selection = record.get("selection", {})

        if debug:
            colored.print(f"{pointer}[dim]Record:[/dim] # [bold magenta]{idx}[/bold magenta]\t[dim]Record Type[/dim]: [bold orange1]{record_game}[/bold orange1]")

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
            colored.print(f"[dim]Compare:[/dim] Drawn Set: {job_pointer} [bold green]{drawn}[/bold green] | [dim]Target Sequence[/dim] [bold orange1]{input_sequence}[/bold orange1]")

        if match_type == "exact":
            if sorted(drawn) == sorted(input_sequence):
                if debug:
                    colored.print("[bold green]EXACT MATCH FOUND[/bold green]")
                matches.append({
                    "draw": drawn,
                    "overlap": drawn[:],
                    "draw_date": record.get("draw_date", record.get("date", "unknown")),
                    "match_count": len(drawn)
                })

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

    if match_type == "partial":
        matches.sort(key=lambda x: x.get("match_count", 0), reverse=True)

    if debug:
        colored.print(f"{_decorator_equal}")
        colored.print(f"\n[bold blue]\t\t--- [bold white]DEBUG RUNTIME TRACE END[/bold white] --- [/bold blue]{_decorator_equal}")
    return matches


# _______ results draws loader:
def get_records(base_dir=None) -> List[str]:
    if base_dir is None:
        base_dir = Path(__file__).resolve().parents[2]
    # __ using Path.glob() in retunr call | personal hack :0) 
    # __ sinse glob got 'graceful degradation' logic | helps to retunr [] list in case one of the data dirs is yet to be created: 
    return [
        str(_path.absolute()) for _path in (base_dir / "lotto_draw_results").glob("**/*.json")] \
            + [str(_path.absolute()) for _path in Path("./historical_lotto_draw_results").glob("*.json")]


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
                            colored.print(f"\t[dim]Game[/dim] Records:\t[dim]-->[/dim] [bold green]{len(data)}[/bold green] in [bold yellow]{path.name}[/bold yellow]\n\t" + "[bold blue]_[/bold blue]" * 95)
                        game_tag = path.stem.lower().split("_")[0]
                        for record in data:
                            # ____ normalized keys injections for draw files:
                            record["game"] = game_tag
                            
                            # Handle both formats of primary_numbers
                            primary_nums = record.get("primary_numbers", [])
                            if primary_nums and isinstance(primary_nums[0], str) and "," in primary_nums[0]:
                                primary_nums = [num.strip() for num in primary_nums[0].split(",")]
                            record["selection"] = {
                                "primary_numbers": primary_nums,  # Use the processed primary numbers
                                "mega": [record.get("megaball") or record.get("powerball")] if record.get("megaball") or record.get("powerball") else []}
                            yield record
                    else:
                        yield data
                except json.JSONDecodeError:
                    colored.print(f"[red] JSON decode error:[/red] {path.name} — fallback to line-by-line")
                    record_file.seek(0)
                    for idx, line in enumerate(record_file, start=1):
                        try:
                            record = json.loads(line)
                            # Apply the same format handling for line-by-line reading
                            primary_nums = record.get("primary_numbers", [])
                            if primary_nums and isinstance(primary_nums[0], str) and "," in primary_nums[0]:
                                record["primary_numbers"] = [num.strip() for num in primary_nums[0].split(",")]
                            yield record
                        except Exception as line_read_error:
                            colored.print(f"[red]Failed line {idx} in {path.name}:[/red] {line_read_error}")
        except Exception as file_read_error:
            colored.print(f"[red]Failed to open file:[/red] {path} — {file_read_error}")


def data_load(show_loaded_count=False, see_details=False):
    count = 0
    records = []
    paths = get_records()
    
    for idx, record in enumerate(iter_json_catalogs(paths, details=see_details), start=1):
        records.append(record)
        if show_loaded_count:
            colored.print(f"\t[bold red]{idx:<3}[/bold red] {json.dumps(record, ensure_ascii=False)}")
        count += 1
    colored.print(f"\n[bold]Total Records Load[/bold]: [bold green]{count}[/bold green]\n" + "[dim]=[/dim]" * 25)
    unique_games = set(read.get("game") for read in records)
    colored.print(f"[bold cyan]Games found:[/bold cyan] {sorted(unique_games)}")
    return records

def show_matches_grouped(overlaps: List[dict]):
    grouped = defaultdict(list)
    for match in overlaps:
        grouped[match["match_count"]].append(match)

    for count in sorted(grouped.keys(), reverse=True):
        colored.print(f"\n[bold magenta]{count} number match(es)[/bold magenta] → {len(grouped[count])} draw(s):")
        for match in grouped[count]:
            # colored.print(f"  → {str(match['draw']).split("[")[1].split("]")[0]:<20} | [dim italic]Overlap:[/dim italic] [yellow]{match['overlap']}[/yellow]\t| Date: [green]{match['draw_date']:>10}[/green]")
            colored.print(f"  → {', '.join(map(str, match['draw'])):<20} | [dim italic]Overlap:[/dim italic] [yellow]{', '.join(map(str, match['overlap']))}[/yellow]\t| Date: [green]{match['draw_date']:>10}[/green]")


# ________ cli args orchestration logic:
GAME_PRIMARY_COUNTS = {
    "powerball": 5,
    "megamillion": 5,
    "lotto": 6,
    "pick3": 3,
    "pick4": 4,
}

DRAW_PRIMARY_KEY = "primary_numbers"   # ____ draw files normalized here:
DRAW_BONUS_KEY   = "mega"              # ____ one-number list to handle 'bonus' values in game ruls e.g., megaball/powerball:

def parse_csv_ints(s: str) -> List[int]:
    return [int(x.strip()) for x in s.split(",") if x.strip() != ""]

def run_one(game: str, match_depth: str, records: List[dict], primary_seq: List[int], bonus_seq: Optional[int], key_override: Optional[str], debug: bool,):
    """Run comparison for one game (primary; and bonus if provided)."""
    seq_key = key_override or DRAW_PRIMARY_KEY
    colored.rule(f"[bold yellow]{game.upper()} • {seq_key} • {match_depth.upper()}[/bold yellow]")
    overlaps = compare_sequence_to_draws(input_sequence=primary_seq, game=game, sequence_key=seq_key, records=records, match_type=match_depth, debug=debug,)
    show_matches_grouped(overlaps)
    colored.print(f"\n[bold green]{len(overlaps)}[/bold green] results matched around {sorted(primary_seq)} sequence data.\n")

    # ___ If bonus vlaue is provided | compare it as well:
    if bonus_seq is not None:
        colored.rule(f"[bold yellow]{game.upper()} • {DRAW_BONUS_KEY} (bonus) • {match_depth.upper()}[/bold yellow]")
        bonus_overlaps = compare_sequence_to_draws(input_sequence=[bonus_seq], game=game, sequence_key=DRAW_BONUS_KEY, records=records, match_type=match_depth, debug=debug,)
        show_matches_grouped(bonus_overlaps)
        colored.print(f"\n[bold green]{len(bonus_overlaps)}[/bold green] results matched around bonus [{bonus_seq}] data.\n")

def build_rarest_from_catalog(game: str) -> List[int]:
    """Use player catalog frequency map to compute rarest sequence for the chosen game."""
    json_paths = frequency_maps.get_records()
    freq_map = frequency_maps.build_frequency_maps(json_paths, max_index_per_game=frequency_maps.LOAD_SET_LIMITS, debug=False,)
    rarest_seq = use_rarest_sequence.construct_rarest_sequence(freq_map, game=game, sequence_key="primary", debug=False,) # ___ catalogs use 'primary' for main line:
    return rarest_seq

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare a target number sequence (rarest or manual) against historical draw results:")
    parser.add_argument("-g", "--game", choices=["powerball", "megamillion", "lotto", "pick3", "pick4"], default="powerball")
    parser.add_argument("-k", "--key", default=None, help="Draw selection key to compare: --> (default: primary_numbers)")
    parser.add_argument("-m", "--match", choices=["partial", "exact"], default="partial")
    parser.add_argument("--manual", help="Comma-separated alternative primary numbers to compare: --> (e.g., '7,12,30,40,69')")
    parser.add_argument("--bonus", type=int, help="Bonus number for Mega/Power: (single int value)")
    parser.add_argument("--all-games", action="store_true", help="Run across all supported games:")
    parser.add_argument("--both-depths", action="store_true", help="Run both partial and exact matching:")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--details", action="store_true", help="Verbose draw file loading logs:")
    parser.add_argument("--show-loaded", action="store_true", help="Print every parsed draw record as .jsons:")
    return parser.parse_args()

@perf.timeit
def main():
    args = parse_args()
    # ___ buffer cotrol | load all normalized draw records (in-memory)
    records = data_load(show_loaded_count=args.show_loaded, see_details=args.details)
    
    # __ figureout which games and match depths to run:
    games = ["powerball", "megamillion", "lotto", "pick3", "pick4"] if args.all_games else [args.game]
    depths = ["partial", "exact"] if args.both_depths else [args.match]

    # ___  primary sequence target selections | manual or rarest from catalog:
    primary_seq_by_game = {}
    bonus_by_game = {}

    for the_game in games:
        if args.manual:
            prim = parse_csv_ints(args.manual)
            expected = GAME_PRIMARY_COUNTS.get(the_game, 5)
            if len(prim) != expected:
                colored.print(f"[red]Manual sequence length {len(prim)} does not match expected {expected} for {the_game}[/red]")
                continue
            primary_seq_by_game[the_game] = prim
            bonus_by_game[the_game] = args.bonus
        else:
            # ___ build rarest sequence from user catalogs:
            try:
                rarest = build_rarest_from_catalog(the_game)
                primary_seq_by_game[the_game] = rarest
                bonus_by_game[the_game] = args.bonus  # ____ optional | can be omitted or derived separately:
                colored.print(f"\n[bold]RAREST (catalog) for {the_game.upper()}[/bold] → [cyan]{rarest}[/cyan]\n")
            except Exception as failed_to_build_rarest_sequence:
                colored.print(f"[red]Could not build rarest sequence for {the_game}:[/red] {failed_to_build_rarest_sequence}")
                continue

    # ___ run comparisons:
    for _game in games:
        prim = primary_seq_by_game.get(_game)
        if not prim:
            continue
        for how_deep in depths:
            # __ in case of `key_override=args.key` | if None, defaults to DRAW_PRIMARY_KEY:
            run_one(game=_game, match_depth=how_deep, records=records, primary_seq=prim, bonus_seq=bonus_by_game.get(_game), key_override=args.key, debug=args.debug,)


if __name__ == "__main__":
    main()

# _____________________________ NOTES _______________________________________________

# === No args (defaults): rarest (from catalogs) vs draws for Powerball, partial: ===
# --> python compare_sequence_to_draws.py

# === Manual sequence (Powerball primary 5 nums) + Mega/Power bonus:  ===
# --> python compare_sequence_to_draws.py --manual "7,12,30,40,69" --bonus 17

# === Exact matching: ===
# --> python compare_sequence_to_draws.py -m exact

#  === Run both depths:  ===
# --> python compare_sequence_to_draws.py --both-depths


#  === All games: ===
# --> python compare_sequence_to_draws.py --all-games

#  === Specific draw key (if you ever change injected schema): ===
# --> python compare_sequence_to_draws.py -k primary_numbers


# === Verbose debug & load details:  ===
# --> python compare_sequence_to_draws.py --debug --details --show-loaded


# keeps both schemas aligned:
#   CatalogsL (user picks) → rarity uses "primary" | e.g --> Path(base_dir).glob("*/catalog/*.json")]
#   Draws (historical) → comparison uses "primary_numbers" (and "mega" for bonus) as injected: | e.g -->  (base_dir / "lotto_draw_results").glob("**/*.json")]
