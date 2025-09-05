#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from collections import Counter
from rich.console import Console
from typing import List, Dict, Optional

sys.path.append(str(Path(__file__).resolve().parents[1]))
from run_search import frequency_maps
from injectors import runtime_perf as perf, str_formatter
colored = Console()

def construct_rarest_sequence(
        frequency_map: Dict[str, Dict[str, Dict[int, Counter]]], 
        game: str, sequence_key: str = "primary", count: Optional[int] = None, debug: bool = False,) -> List[int]:
    """ Build a sequence choosing the least-frequent number at each index.
        frequency_map: game -> sequence_key -> index -> Counter(number -> freq) """
    
    # ___ validate game & sequence_key exists:
    if game not in frequency_map:
        raise KeyError(f"Game '{game}' not found in frequency_map keys: {list(frequency_map.keys())}")
    if sequence_key not in frequency_map[game]:
        raise KeyError(f"sequence_key '{sequence_key}' not in frequency_map['{game}'] keys: {list(frequency_map[game].keys())}")

    game_map: Dict[int, Counter] = frequency_map[game][sequence_key]

    # ___ derive count from available indices if not provided:
    if count is None:
        count = (max(game_map.keys()) + 1) if game_map else 0
    result: List[int] = []

    for idx in range(count):
        counter = game_map.get(idx)
        if not counter or not any(counter.values()):
        # if not counter or sum(counter.values()) == 0:
            raise ValueError(f"No frequency data for index {idx} in game='{game}', sequence_key='{sequence_key}'.")

        # ___ coerce keys to int (in case they were stored as strings)
        norm_items = []
        for key_int, _value in counter.items():
            try:
                keys = int(key_int)
            except (TypeError, ValueError):
                # ___ skip for any non-numeric values such as 'N/A'
                continue
            norm_items.append((keys, _value))

        if not norm_items:
            raise ValueError(f"All entries at index {idx} are non-numeric for game='{game}', key='{sequence_key}'.")

        # ___ choose rarest with deterministic tie-break: (freq asc, number asc)
        rare_value, rare_freq = min(norm_items, key=lambda key_value: (key_value[1], key_value[0]))
        result.append(rare_value)

        if debug:
            # ___ show top few rare candidates (up to 5):
            preview = sorted(norm_items, key=lambda key_value: (key_value[1], key_value[0]))[:5]
            colored.print(f"\t\t[dim]idx {idx}[/dim] → pick [bold]\t{rare_value:<3}[/bold] (freq={rare_freq:<5}): candidates: {preview}")
    return result


def main():
    state_games = ["powerball", "megamillion", "lotto"]
    jsons = frequency_maps.get_records()
    map_frequencies = frequency_maps.build_frequency_maps(jsons, max_index_per_game=frequency_maps.LOAD_SET_LIMITS, debug=False)
    
    for game in state_games:
        valid_keys = map_frequencies.get(game, {}).keys()
        for key in valid_keys:
            try:
                rarest_seq = construct_rarest_sequence(
                    map_frequencies,
                    game=game,
                    sequence_key=key,
                    debug=True)
                # colored.print("[dim]_[/dim]" * 110)
                colored.print(f"\n[bold green]{game.upper():<13}[/bold green]\t→ rarest sequence: [bright_red]{rarest_seq}[/bright_red] in Key: [bold magenta]{key.upper():>3}[/bold magenta]")
            except Exception as e:
                colored.print(f":warning: Skipping [bold red]{game:<7}[/bold red] → {e}")

if __name__ == "__main__":
    main()
