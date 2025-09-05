#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import orjson
from time import time
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Union, Generator, Optional

from rich.console import Console
sys.path.append(str(Path(__file__).resolve().parents[1]))
from injectors import runtime_perf as perf, str_formatter

colored = Console()

DEFAULT_RARE_THRESHOLD = {"megamillion": 5, "powerball": 5, "lotto": 3, "pick3": 1, "pick4": 1}
GAMES_SEQUENCE_LIMITS = {"megamillion": 70, "powerball": 69, "lotto": 52, "pick3": 10, "pick4": 10}
LOAD_SET_LIMITS = {"megamillion": 5, "powerball": 5, "lotto": 6, "pick3": 3}

pointer = "[bold green] → [/bold green] "
_decorator_under = "\t" + "[dim]_[/dim]" * 65
_decorator_equal = "\n" + "[dim]=[/dim]" * 95


def get_records(base_dir=None) -> List[str]:
    if base_dir is None:
        base_dir = Path(__file__).resolve().parents[1]
    return [str(path.absolute()) for path in Path(base_dir).glob("*/catalog/*.json")]


def iter_json_catalogs(json_paths: List[Union[str, Path]]) -> Generator[dict, None, None]:
    for path in map(Path, json_paths):
        with path.open("r", encoding="utf-8") as current_file:
            try:
                data = json.load(current_file)
                if isinstance(data, list):
                    yield from data
                else:
                    yield data
            except json.JSONDecodeError:
                current_file.seek(0)
                for line in current_file:
                    if line.strip():
                        yield json.loads(line)


@perf.timeit
def build_frequency_maps(
        json_paths: List[Union[str, Path]], max_index_per_game: Dict[str, int] = None, 
        debug: bool = False, throttle: int = 100, export_path: Optional[Union[str, Path]] = None) -> Dict[str, Dict[str, Dict[int, Counter]]]:
    """ Build vertical frequency maps per index for numeric sequences:
        frequency_map[game][sequence_name][index][value] -> count """
    
    frequency_map: Dict[str, Dict[str, Dict[int, Counter]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
    progress_counter = 0
    last_debug = time()

    for record in iter_json_catalogs(json_paths):
        game = record.get("game")
        selection = record.get("selection", {})
        if not game or not selection:
            continue

        limit = max_index_per_game.get(game) if max_index_per_game else None
        for seq_name, nums in selection.items():
            if not isinstance(nums, list):
                continue
            for idx, val in enumerate(nums):
                if limit is not None and idx >= limit:
                    break
                frequency_map[game][seq_name][idx][val] += 1
        progress_counter += 1


        # ___ throttled progress line: every N records or >=3s since last print:
        if debug and (progress_counter % max(1, throttle) == 0 or time() - last_debug > 3):
            games_count = len(frequency_map)
            seq_count = sum(len(seq_map) for seq_map in frequency_map.values())
            colored.print(
                f"{pointer}[dim]processed[/dim] [bold yellow]{progress_counter:>5}[/bold yellow] "
                f"[dim]records[/dim] [bold red]|[/bold red] "
                f"{games_count} games [dim]*[/dim] [bold green]{seq_count}[/bold green] sequences")
            last_debug = time()

    # ___ build debug/export stats if true:
    debug_stats: Dict[str, Dict[str, Dict[int, dict]]] = {}
    if debug or export_path:
        for game, sequences in frequency_map.items():
            if debug:
                colored.rule(f"\n[bold]GAME TYPE:[/bold] [bold magenta]{game.upper()}[/bold magenta]", align="center")
            debug_stats[game] = {}

            for seq_name, idx_map in sequences.items():
                if debug:
                    colored.print(f"\n\t[bold green]Sequence:[/bold green] [bold]{seq_name.upper()}[/bold]")
                debug_stats[game][seq_name] = {}

                for idx, counter in idx_map.items():
                    top = counter.most_common(3)
                    bottom = sorted(counter.items(), key=lambda key_values: (key_values[1], key_values[0]))[:3]
                    unique_values = len(counter)
                    total = sum(counter.values())

                    if debug:
                        top_str  = str_formatter.format_key_pairs(top)
                        rare_str = str_formatter.format_key_pairs(bottom)
                        pipe_decorator_line = str_formatter.format_key_pairs(bottom)
                        
                        # choose a common width so columns line up (tweak min width as you like)
                        width = max(len(top_str), 10, len(rare_str), 35)

                        colored.print(
                            f"\t[dim]{game:12}[/dim] • [bright_cyan]{seq_name:<18}[/bright_cyan] idx [bold]{idx}[/bold] → "
                            f"count: [green]{total:>7}[/green], "
                            f"unique: {unique_values:>3} | "
                            f"[yellow]Top:[/yellow] {top_str:>{width}} "
                            f"[bold] {pipe_decorator_line:<35} | [/bold] [bold red]Rare[/bold red]: {rare_str}"
                        )

                    debug_stats[game][seq_name][idx] = {"top": top, "rarest": bottom, "unique_values": unique_values, "total_counts": total}

    
    # __ write to .json | optional
    if export_path:
        export_path = Path(export_path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        # with open(export_path, "wb") as out:
        #     for game, seq_map in debug_stats.items():
        #         for seq_name, idx_map in seq_map.items():
        #             for idx, stats in idx_map.items():
        #                 record = {
        #                     "game": game,
        #                     "sequence": seq_name,
        #                     "index": idx,
        #                     **stats,}
        #                 out.write(orjson.dumps(record, option=orjson.OPT_APPEND_NEWLINE))

        with open(export_path, "w", encoding="utf-8") as file_write:
            json.dump(debug_stats, file_write, indent=4)
        
        if debug:
            colored.print(f"\n... [bold green]wrote debug stats to:[/bold green] {pointer} {export_path.absolute()}")
    

    # ___  summary:
    if debug:
        colored.rule("[bold yellow]Mapped Frequency Summary[/bold yellow]")
        for game, sequences in frequency_map.items():
            for seq_name, idx_map in sequences.items():
                colored.print(f"{_decorator_under}")
                colored.print(f"\n\t[bright_white]GAME TYPE[/bright_white]:{pointer}[bold italic]{game.upper()}[/bold italic] | [bright_white]Sequence Key[/bright_white]:{pointer}[bold yellow italic]{seq_name.upper()}[/bold yellow italic]\n")
                
                for idx, counter in idx_map.items():
                    top = counter.most_common(3)
                    total = sum(counter.values())

                    top_str = str_formatter.format_key_pairs(top)
                    width = max(35, len(top_str))

                    colored.print(
                        f"\t[dim]Index[/dim]: "
                        f"[bold yellow]{idx:<2}[/bold yellow] "
                        f"[bright_white]→[/bright_white][dim]top[/dim]: "
                        f"[bold green]{top_str:>{width}}[/bold green] "
                        f"[bold red]|[/bold red] total [green]{total:>7}[/green]"
                    )
    return frequency_map


@perf.timeit
def main(dev_debug_path="./_dev_debug/vertical_freq_summary.json", show_runtime: bool = False,):
    # ruff: noqa: E731
    jsons = get_records()    
    
    if show_runtime:
        debug_frequency_map = build_frequency_maps(jsons, max_index_per_game=LOAD_SET_LIMITS, debug=show_runtime, throttle=100, export_path=dev_debug_path)
        return debug_frequency_map 

    raw_frequency_map = build_frequency_maps(jsons, max_index_per_game=LOAD_SET_LIMITS, debug=show_runtime, throttle=100)
    [colored.print(idx, runtime, _decorator_equal) for idx, runtime in enumerate(raw_frequency_map.items(), start=1)]
    show_games_data = lambda fm: [colored.print(f"{item:<2} {pointer} {game:<11} {len(seq_map)} sequences") for item, (game, seq_map) in enumerate(fm.items(), start=1)] 
    show_games_data(raw_frequency_map)


if __name__ == "__main__":
    main(show_runtime=True)
    # main()
