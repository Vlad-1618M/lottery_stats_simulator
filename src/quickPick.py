#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import json
import datetime
import unicodedata
from time import sleep
from pathlib import Path
from rich.table import Table
from rich.panel import Panel
from unidecode import unidecode
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))
import math_modules.prime_sequence_check as nitup
import glob_args

colored = Console()


def normalize_name(name):
    if not name:
        return ""
    name = unidecode(name)
    return unicodedata.normalize("NFKC", name).casefold().strip()


PLAYERS = {Path(entrant).stem: Path(entrant) for entrant in glob_args.entrant_catalog(records_dir="catalog")}
NAME_LOOKUP = {normalize_name(name): name for name in PLAYERS.keys()}
PLAYER_INDEX = {idx: name for idx, name in enumerate(PLAYERS.keys(), start=1)}


def get_random_selection(config: dict, seed=None) -> dict:
    result = {}
    for key, (count, min_val, max_val) in config.items():
        full_set, primes, _ = nitup.get_primes_from_random(count, min_val, max_val, seed)
        result[key] = full_set
        result[f"primes_in_{key}"] = primes
    return result


def save_selection(name: str, game: str, numbers: dict):
    timestamp = datetime.datetime.now().isoformat()
    data = {"timestamp": timestamp, "game": game, "selection": numbers}

    artifact_path = PLAYERS.get(name)
    if artifact_path is None:
        colored.print(f"[red]No artifact path found for {name}[/red]")
        return

    existing = []
    if artifact_path.exists():
        try:
            with artifact_path.open("r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            existing = []

    existing.append(data)

    artifact = json.dumps(existing, indent=4, ensure_ascii=False)
    json_cleanup = re.sub(r'(\s*)(\[[\d,\s]+?\])', lambda m: m.group(1) + m.group(2).replace("\n", "").replace(" ", ""), artifact)

    with artifact_path.open("w", encoding="utf-8") as clean_artifact:
        clean_artifact.write(json_cleanup)


def main():
    auto_mode, run_all, all_names, seed, single_game = glob_args.parse_quick_pick_args()
    total_players = len(PLAYER_INDEX)

    columns = next((cols for limit, cols in [(100, 2), (500, 4), (1000, 6), (1500, 8), (2000, 10)] if total_players <= limit), 16)
    rows = (total_players + columns - 1) // columns
    colored.print(f"\n[bold cyan]Available players ({total_players} total):[/bold cyan]\n")
    sorted_players = sorted(PLAYER_INDEX.items(), key=lambda x: (x[1].lower(), x[0]))
    max_name_length = max(len(name) for _, name in sorted_players) + 2

    indexed_players = list(enumerate(sorted_players, start=1))
    grid = [[] for _ in range(rows)]

    for idx, ((number, name)) in indexed_players:
        row = (idx - 1) % rows
        grid[row].append(f"[dim]{idx:<4}.[/dim] [green]{name:<{max_name_length}}[/green]")

    # Skip row prompts for automation or batch modes
    interactive_display = not (auto_mode or all_names or run_all)

    if interactive_display:
        try:
            row_limit = int(input("How many grid rows to display at once? (e.g., 10): ").strip())
        except ValueError:
            row_limit = 10
        total_chunks = (len(grid) + row_limit - 1) // row_limit
        current_chunk = 0

        while current_chunk < total_chunks:
            start = current_chunk * row_limit
            end = start + row_limit
            chunk = grid[start:end]

            for row_items in chunk:
                if row_items:
                    colored.print(" ".join(row_items))

            current_chunk += 1

            if current_chunk < total_chunks:
                cont = input("Show next rows? (y/n): ").strip().lower()
                if cont != "y":
                    break
    else:
        for row_items in grid:
            if row_items:
                colored.print(" ".join(row_items))

    if all_names and auto_mode:
        selected_names = list(PLAYERS.keys())
    else:
        default_name = NAME_LOOKUP.get(normalize_name("ghost"), "ghost")
        default_stem = PLAYERS.get(default_name, Path("ghost.json")).stem

        chosen_raw = input(f"\nEnter player name (default = {default_stem}): ").strip()
        chosen_norm = normalize_name(chosen_raw)
        chosen_key = NAME_LOOKUP.get(chosen_norm, default_name)

        if chosen_key not in PLAYERS:
            colored.print(f"[red]No entry found for '{chosen_raw}' — using default '{default_stem}'[/red]")
            chosen_key = default_name

        selected_names = [chosen_key]

    player_records_summary = {name: 0 for name in selected_names}

    for chosen in selected_names:
        player_game_list = [single_game] if single_game else list(glob_args.GAMES) if (run_all or auto_mode) else []

        if not player_game_list:
            colored.print(f"[red]No game specified for {chosen}. Use --game or --run-all.[/red]")
            continue

        for game in player_game_list:
            config = glob_args.GAMES[game]
            attempt = 0
            max_attempts = 30

            while attempt < max_attempts:
                attempt += 1
                colored.print(f"\n[bold cyan]{'[AUTO]' if auto_mode else ''}\t[magenta]{game.upper():<19}[/magenta][/bold cyan] [underline yellow]QuikPick[/underline yellow]: [white]Attempt[/white] [bold green]{attempt}[/bold green] of {max_attempts}")
                numbers = get_random_selection(config, seed)

                for key, val in numbers.items():
                    label = key.replace("_", " ").capitalize()
                    joined_vals = ", ".join(map(str, val)) if isinstance(val, (list, tuple)) else str(val)
                    colored.print(f"\t[yellow]{label:<19}[/yellow]| [white]{joined_vals}[/white]")

                if auto_mode:
                    save_selection(chosen, game, numbers)
                    player_records_summary[chosen] += 1
                    colored.print(f"\t[underline dim]saved to[/underline dim] [bold]\t-> [/bold][green]{Path(*PLAYERS[chosen].parts[-3:])}[/green]")
                    break

                while True:
                    ask = "\t[bright_red]Accept current set[/bright_red] ? "
                    yes = "[bright_green]y[/bright_green] [dim]= yes[/dim] | "
                    no = "[bright_red]n[/bright_red] [dim]= skip[/dim] | "
                    try_again = "[bright_cyan]r[/bright_cyan] [dim]= retry[/dim] "

                    colored.print(f"{ask} {yes} {no} {try_again} ")
                    confirm = input().strip().lower()

                    if confirm == 'y':
                        save_selection(chosen, game, numbers)
                        player_records_summary[chosen] += 1
                        attempt = max_attempts
                        break
                    elif confirm == 'n':
                        attempt = max_attempts
                        break
                    elif confirm == 'r':
                        break
                    else:
                        colored.print(f"\t[bright_white]{confirm}[/bright_white] is [bright_red]invalid input[/bright_red]")

    total_records = sum(player_records_summary.values())
    # colored.print(Panel(f"[bold green]{total_records} total game record(s) saved.[/bold green]", title="Summary", width=80))

    summary_table = Table(title="\nLottery Game Records:", width=170, show_lines=True)
    summary_table.add_column("Player Name", justify="left", style="cyan", no_wrap=True)
    summary_table.add_column("Records File", justify="left", style="yellow")
    summary_table.add_column("Records Path", justify="left", style="dim")
    summary_table.add_column("Games Saved", justify="center", style="magenta")

    for name, count in player_records_summary.items():
        record_file = PLAYERS[name].name
        record_path = Path(*PLAYERS[name].parts[-3:])
        summary_table.add_row(name, record_file, str(record_path), str(count))

    colored.print(summary_table)
    # total_records = sum(player_records_summary.values())
    colored.print(Panel(f"[bold green]{total_records} total game record(s) saved.[/bold green]", title="Summary", width=80))

def _debug_gen_more_data(limit=10):
    counter = 0
    while counter < limit:
        colored.print(f"\n[bright_blue][[orange1]JOB[/orange1]:][/bright_blue]\t[dim]{sys.argv[0]}[/dim] init call:\t[dim]Init Count[/dim]: [bright_yellow]{counter}[/bright_yellow]")
        counter += 1
        sleep(1)
        colored.print(f"[bright_blue][[orange1]JOB[/bright_blue]:]\t{main()}\t\t\t\t[bright_magenta]run[/bright_magenta] count: [bright_green]{counter}[/bright_green]")


if __name__ == "__main__":
    # _debug_gen_more_data(limit=2)
    main()
