#!/usr/bin/env python
# -*- config: utf-8 -*-
# mypy: ignore-errors

import sys
import json
import argparse
from pathlib import Path
from rich.table import Table
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))
from records_analytics import catalog_manager 
from experemental import cli_tools

colored = Console()

def records_catalog_increase(limit, out=False):
    counter = 0
    while counter < limit:
        colored.print(f"{sys.argv[0]}\tinit call:\tInit Count: {counter}\n{catalog_manager.caller_trace()}")
        counter += 1
        cli_tools.cli("python3", "quickPick.py", "--auto", "--all-names", live_output=out)

def items_records_view():
    json_files = catalog_manager.find_all_json_paths()
    if not json_files:
        colored.print("[bright_yellow][WARN][/bright_yellow] No JSON files found.")
        return
    
    error_table = Table(title="\nBroken JSON Records", width=50, show_lines=False, title_justify="left")
    # error_table = Table(title="\nBroken JSON Records:\n", title_justify="left", width=55, show_lines=False, show_edge=False, show_footer=False, show_header=False)
    error_table.add_column("Index", justify="left", style="red")
    error_table.add_column("Error", justify="left", style="yellow")
    error_table.add_column("File Name", justify="left", style="cyan")

    for idx, json_path in enumerate(sorted(json_files, key=lambda _: Path(_).stat().st_mtime), start=1):
        data = catalog_manager.load_json(json_path, idx, error_table)
        if data is None:
            continue
        colored.print(f"[dim][CATALOG ][/dim]: Loaded [bold yellow]{len(data)}[/bold yellow] items from: [bright_cyan]{Path(json_path).name:>6}[/bright_cyan]")

    if error_table.row_count > 0:
        colored.print(error_table)


def records_catalog_view(details=False):
    catalog = catalog_manager.find_all_json_paths()
    results = []
    if not catalog:
        colored.print("[yellow][WARN][/yellow] No JSON files found.")
        return results

    for idx, catalog_name in enumerate(sorted(catalog, key=lambda _: Path(_).stat().st_mtime), start=1):
        path_object = Path(catalog_name)
        try:
            with path_object.open("r", encoding="utf-8") as reader:
                read_catalog_details = json.load(reader)
                results.append((path_object.name, read_catalog_details))
                colored.print(f"[Game Record Catalog ID: {idx}] ➜ [bold cyan]{path_object.name}[/bold cyan]")
                if details:
                    colored.print(read_catalog_details)

        except json.JSONDecodeError as json_struct_error:
            colored.print(f"[bright_red][ERROR {idx}][/bright_red] Invalid JSON in: [bold red]{path_object.name}[/bold red]")
            colored.print(f"[dim]{json_struct_error}[/dim]")
        except Exception as messed_up_json:
            colored.print(f"[red][FAIL][/red] Could not process file: [cyan]{path_object.name}[/cyan] — {str(messed_up_json)}")

    return results

def game_records():
    enable_args = argparse.ArgumentParser(description="Catalog Records Viewer:")
    enable_args.add_argument('--items', action='store_true', help='Show catalog items (e.g., recorded game count) records:')
    enable_args.add_argument('--show-details', action='store_true', help='Show catalog itmes details (e.g., See key-pair values) records:')
    enable_args.add_argument('--show-ids', action='store_true', help='Show catalog ids + names of each record:')
    args = enable_args.parse_args()
    
    _any = False
    
    if args.items:
        items_records_view()
        _any = True
    
    if args.show_details:
        records_catalog_view(details=True)
        _any = True
    
    if args.show_ids:
        records_catalog_view(details=False)
        _any = True
        
    if not _any:
        colored.print(
            f"[bold red]No[/bold red] view option selected for: [bold red]-->[/bold red] "
            f"{catalog_manager.caller_trace()}\n\t\t\t\t"
            f" Run [bold yellow]`--help`[/bold yellow] to see available [bold]cli[/bold] flags:\n")


def main_logic():
    records_catalog_increase(limit=1, out=True)
    game_records()

if __name__ == "__main__":
    main_logic()

