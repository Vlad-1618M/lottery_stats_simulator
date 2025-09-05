#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from pathlib import Path
from rich.console import Console
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple, Union

sys.path.append(str(Path(__file__).resolve().parents[1]))
from run_search import use_rarest_sequence
from injectors import runtime_perf as perf

colored = Console()

# Map raw filename stems to normalized game names
GAME_NAME_ALIASES = {
    "megamillions": "megamillion",
    "powerball": "powerball",
    "lotto": "lotto",
    "pick3": "pick3",
    "pick4": "pick4",
    "luckydaylotto": "luckyday",
}

# Canonical supported game names (values of the alias map)
SUPPORTED_GAMES = sorted(set(GAME_NAME_ALIASES.values()))

# ___________________________________
def iter_json_catalogs_with_trace(json_paths: List[Union[str, Path]]):
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
                                record["selection"] = {
                                    "primary": list(map(int, record.get("primary_numbers", []))),
                                    "mega": [int(record["mega"])] if record.get("mega") not in [None, "N/A"] else [],
                                    "power": [int(record["powerball"])] if record.get("powerball") not in [None, "N/A"] else []
                                }
                            yield record, path.name, line_no

                except json.JSONDecodeError as json_err:
                    colored.print(f"[red]Failed to parse JSON in {path.name}[/red]: {json_err}")
        except Exception as e:
            colored.print(f"[red]Failed to open {path}[/red]: {e}")

# ___________________________________
def build_augmented_frequency_map(json_paths: List[Union[str, Path]]):
    frequency_map = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
    origin_trace = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    for record, file_name, line_number in iter_json_catalogs_with_trace(json_paths):
        game = record.get("game")
        selection = record.get("selection", {})

        if not game or not selection:
            continue

        for seq_name, nums in selection.items():
            if not isinstance(nums, list):
                continue
            for idx, val in enumerate(nums):
                try:
                    val_int = int(val)
                    frequency_map[game][seq_name][idx][val_int] += 1
                    origin_trace[game][seq_name][idx][val_int].append((file_name, line_number))
                except ValueError:
                    continue

    return frequency_map, origin_trace

# ___________________________________
def generate_unique_gameplay_sequence(
    frequency_map: Dict[str, Dict[str, Dict[int, Counter]]],
    origin_trace: Dict[str, Dict[str, Dict[int, Dict[int, List[Tuple[str, int]]]]]],
    game: str,
    sequence_key: str = "primary",
    debug: bool = False
) -> Tuple[List[int], Dict[int, Tuple[int, int, str]], List[int]]:
    raw_sequence = use_rarest_sequence.construct_rarest_sequence(
        frequency_map, game=game, sequence_key=sequence_key, debug=debug
    )

    game_map = frequency_map[game][sequence_key]
    trace_map = origin_trace[game][sequence_key]

    seen = set()
    final_sequence = []
    origin = {}
    dropped = []

    for idx, val in enumerate(raw_sequence):
        freq = game_map.get(idx, {}).get(val, 0)
        source_list = trace_map.get(idx, {}).get(val, [])
        source_str = f"{source_list[0][0]}:{source_list[0][1]}" if source_list else "unknown"

        if val in seen:
            dropped.append(val)
            continue

        seen.add(val)
        final_sequence.append(val)
        origin[idx] = (val, freq, source_str)

    return final_sequence, origin, dropped

# ___________________________________
def display_suggestions(
    freq_map: Dict[str, Dict[str, Dict[int, Counter]]],
    origin_trace: Dict[str, Dict[str, Dict[int, Dict[int, List[Tuple[str, int]]]]]],
    games: Optional[List[str]] = None
):
    #  Use canonical normalized game keys
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
        if game not in freq_map:
            colored.print(f"[red]Skipping {game} — no data[/red]")
            continue

        for key in seq_keys.get(game, ["primary"]):
            if key not in freq_map[game]:
                continue

            try:
                picks, trace, dropped = generate_unique_gameplay_sequence(freq_map, origin_trace, game=game, sequence_key=key, debug=False)
                header = f"{game.upper()} — {key.upper()} Picks"
                colored.rule(f"[bold cyan]{header}[/bold cyan]")
                colored.print(f"[green]Sequence:[/green] [bold yellow]{picks}[/bold yellow]")

                for idx, (val, freq, source) in trace.items():
                    colored.print(
                        f"  [dim]index[/dim] [bold]{idx:<2}[/bold] → "
                        f"[white]{val}[/white]  (freq: {freq}, from: [dim]{source}[/dim])"
                    )

                if dropped:
                    colored.print(f"\n[yellow]⚠ Duplicates dropped:[/yellow] [red]{dropped}[/red]")

                colored.print("\n")

            except Exception as err:
                colored.print(f"[red]Error processing {game}:{key} →[/red] {err}")

# ___________________________________
@perf.timeit
def main():
    base_dir = Path(__file__).resolve().parents[1]
    draw_paths = list((base_dir / "lotto_draw_results").glob("**/*.json"))
    freq_map, origin_trace = build_augmented_frequency_map(draw_paths)
    display_suggestions(freq_map, origin_trace)

    # Optional: Debug summary of games and keys
    colored.rule("[bold yellow]DEBUG: Loaded Games from Frequency Map[/bold yellow]")
    for game in freq_map:
        keys = list(freq_map[game].keys())
        colored.print(f"[cyan]{game}[/cyan] → keys: {keys}")

if __name__ == "__main__":
    main()


# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import sys
# from pathlib import Path
# from collections import Counter
# from rich.console import Console
# from typing import Dict, List, Optional, Tuple

# sys.path.append(str(Path(__file__).resolve().parents[1]))
# from run_search import frequency_maps
# from run_search import use_rarest_sequence

# colored = Console()

# # ________ Generate a unique gameplay suggestion per game:
# def generate_unique_gameplay_sequence(
#         frequency_map: Dict[str, Dict[str, Dict[int, Counter]]],
#         game: str, sequence_key: str = "primary", debug: bool = False) -> Tuple[List[int], Dict[int, Tuple[int, int]], List[int]]:
#     """ Returns:
#             - final_sequence: List[int] - deduplicated picks
#             - origin_trace: Dict[index, (value, frequency)]
#             - dropped_duplicates: List[int] """
    
#     raw_sequence = use_rarest_sequence.construct_rarest_sequence(frequency_map, game=game, sequence_key=sequence_key, debug=debug)
#     game_map = frequency_map[game][sequence_key]

#     seen = set()
#     final_sequence = []
#     origin_trace = {}
#     dropped_duplicates = []

#     for idx, val in enumerate(raw_sequence):
#         freq = game_map.get(idx, {}).get(val, 0)
#         if val in seen:
#             dropped_duplicates.append(val)
#             continue
#         seen.add(val)
#         final_sequence.append(val)
#         origin_trace[idx] = (val, freq)

#     return final_sequence, origin_trace, dropped_duplicates


# # ________ Pretty display logic:
# def display_gameplay_suggestions(
#     frequency_map: Dict[str, Dict[str, Dict[int, Counter]]],
#     supported_games: Optional[List[str]] = None,
#     sequence_key: str = "primary"
# ):
#     supported_games = supported_games or ["powerball", "megamillion", "lotto", "pick3", "pick4"]

#     for game in supported_games:
#         if game not in frequency_map or sequence_key not in frequency_map[game]:
#             colored.print(f"[yellow]Skipping[/yellow] → [red]{game.upper()}[/red] has no data for key '{sequence_key}'")
#             continue

#         try:
#             picks, trace, dropped = generate_unique_gameplay_sequence(
#                 frequency_map, game=game, sequence_key=sequence_key, debug=False
#             )

#             colored.rule(f"[bold white]{game.upper()}[/bold white] → [bold green]Suggested Gameplay Pick[/bold green]")
#             colored.print(f"[cyan]Sequence:[/cyan] [bold magenta]{picks}[/bold magenta]\n")

#             for idx, (val, freq) in trace.items():
#                 colored.print(
#                     f"  • [dim]From index[/dim] [bold yellow]{idx:<2}[/bold yellow] "
#                     f"→ value: [bold]{val}[/bold] (freq: {freq})"
#                 )

#             if dropped:
#                 colored.print(
#                     f"\n[bold red]Duplicates dropped[/bold red]: {dropped}"
#                 )

#             colored.print("[dim]─[/dim]" * 90)

#         except Exception as err:
#             colored.print(f"[red]Failed to generate pick for {game}[/red]: {err}")


# # ________ CLI Entrypoint:
# def main():
#     jsons = frequency_maps.get_records()
#     freq_map = frequency_maps.build_frequency_maps(jsons, max_index_per_game=frequency_maps.LOAD_SET_LIMITS, debug=False)

#     display_gameplay_suggestions(freq_map)


# if __name__ == "__main__":
#     main()
