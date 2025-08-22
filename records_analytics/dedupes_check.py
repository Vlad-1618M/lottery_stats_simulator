#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import psutil
import hashlib
import unicodedata
from time import sleep
from pathlib import Path
from rich.table import Table
from unidecode import unidecode
from collections import Counter
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src import glob_args

colored = Console()
process = psutil.Process()


def normalize_name(name, transliterate=True):
    if not name:
        return ""
    if transliterate:
        name = unidecode(name)
    return unicodedata.normalize("NFKC", name).casefold().strip()


def hash_name(name, digest_size=8):
    return hashlib.blake2b(name.encode('utf-8'), digest_size=digest_size).hexdigest()


def check_duplicates(players, name_lookup, use_set=False, use_loop=False, use_counter=False, use_hash=False, digest_size=8, transliterate=True, slow=False):
    summary = {
        'SET': 0,
        'LOOP': 0,
        'COUNTER': 0,
        'HASH': 0
    }

    # ___ variant 1: | Set Intersection:
    if use_set:
        normalized_players = {normalize_name(name, transliterate): name for name in players.keys()}
        duplicates = set(name_lookup.keys()) & set(normalized_players.keys())
        for idx, match in enumerate(duplicates, start=1):
            colored.print(f"[blue]{idx:<4}[/blue][red][[yellow]SET:[/yellow]][/red] Duplicate: [bold_yellow]{match}[/bold_yellow] -> [bold_yellow]{normalized_players[match]}[/bold_yellow]")
            summary['SET'] += 1
            if slow:
                sleep(slow)

    # ___ variant 2: | brute loop:
    if use_loop:
        normalized_list = [normalize_name(name, transliterate) for name in players.keys()]
        for idx, (norm_name, original) in enumerate(name_lookup.items(), start=1):
            if norm_name in normalized_list:
                colored.print(f"[blue]{idx:<4}[/blue][red][[yellow]LOOP:[/yellow]][/red] Duplicate: [bold_yellow]{norm_name}[/bold_yellow] -> [bold_yellow]{original}[/bold_yellow]")
                summary['LOOP'] += 1
                if slow:
                    sleep(slow)

    # ___ variant 3: | frequency counter:
    if use_counter:
        all_normalized = [normalize_name(name, transliterate) for name in players.keys()]
        counts = Counter(all_normalized)
        idx = 0
        for name, count in counts.items():
            if count > 1:
                idx += 1
                colored.print(f"[blue]{idx:<4}[/blue][red][[yellow]COUNTER:[/yellow]][/red] Duplicate: [bold_yellow]{name}[/bold_yellow] appears [bold_yellow]{count}[/bold_yellow] times")
                summary['COUNTER'] += 1
                if slow:
                    sleep(slow)

    # ___ variant 4: | hash_based dedup:
    if use_hash:
        hash_map = {}
        for name in players.keys():
            norm = normalize_name(name, transliterate=False)  # strict normalization only, no translit
            hashed = hash_name(norm, digest_size=digest_size)
            # print(f"ORIGINAL: {name} | NORM: {norm} | HASH: {hashed}")
            hash_map.setdefault(hashed, []).append(name)

        idx = 0
        for hashed_val, name_list in hash_map.items():
            if len(name_list) > 1:
                idx += 1
                names_str = " | ".join([f"[bold_yellow]{n}[/bold_yellow]" for n in name_list])
                colored.print(f"[blue]{idx:<4}[/blue][red][[yellow]HASH:[/yellow]][/red] Duplicate Hash: [bold_yellow]{hashed_val}[/bold_yellow] -> {names_str}")
                summary['HASH'] += 1
                if slow:
                    sleep(slow)

    table = Table(title="\nDeduplication Summary:", show_lines=True, border_style="pink1", title_justify="left")
    table.add_column("Method", style="bright_yellow", justify="left")
    table.add_column("Duplicates Found", style="green", justify="right")

    for method, count in summary.items():
        table.add_row(method, str(count))

    colored.print(table)
    # [print(f"{idx:<4}, -> {tag}") for idx, tag in enumerate(hash_map.items(), start=1) if idx <= 10]


if __name__ == "__main__":
    PLAYERS = {Path(entrant).stem: Path(entrant) for entrant in glob_args.entrant_catalog(records_dir="catalog")}
    NAME_LOOKUP = {normalize_name(name): name for name in PLAYERS.keys()}
    check_duplicates(PLAYERS, NAME_LOOKUP, use_set=True, use_loop=True, use_counter=True, use_hash=True, digest_size=8, transliterate=False, slow=False)

    # check_duplicates(
    #     PLAYERS,
    #     NAME_LOOKUP,
    #     use_set=True,
    #     use_loop=True,
    #     use_counter=True,
    #     use_hash=True,
    #     digest_size=8,          # ____ hashed digest size [8, 16, etc.]
    #     transliterate=False,    # ____ transliteration switch | global setting:
    #     slow=False              # ____ sleep | in case of visual to process the stdout:
    # )
