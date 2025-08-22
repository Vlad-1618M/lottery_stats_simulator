#!/usr/bin/env python
# -*- config: utf-8 -*-
# mypy: ignore-errors

import os
import sys
import json
import shlex
import inspect
import argparse
from time import sleep
from pathlib import Path
from rich.table import Table
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))
from injectors import epilogs

colored = Console()

def caller_trace():
    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)
    
    function_trace = info.function
    code_line = info.lineno
    trace_file = ' '.join(map(shlex.quote, (os.path.basename(sys.executable), os.path.basename(sys.argv[0]))))
    return f"[dim]{trace_file}[/dim] --> [bold magenta]{function_trace}()[/bold magenta] code line: #[bold yellow]{code_line}[/bold yellow]"

def find_all_json_paths(base_dir=None) -> list[str]:
    if base_dir is None:
        base_dir = Path(__file__).resolve().parents[1]
    json_paths = list(base_dir.glob("*/catalog/*.json"))
    return [str(path.absolute()) for path in json_paths]


def load_json(path: str, idx: int, error_table):
    path_object = Path(path)

    if path_object.stat().st_size == 0:
        error_table.add_row(f"[dim]{idx}[/dim]", "[bold cyan]Empty[/bold cyan]\tJSON", f"[bold red]{path_object.name}[/bold red]")
        return None

    try:
        with path_object.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        error_table.add_row(f"[dim]{idx}[/dim]", "[bold red]Invalid[/bold red] JSON", f"[bold red]{path_object.name}[/bold red]")
        return None
    except Exception as read_error:
        error_table.add_row(f"[dim]{idx}[/dim]", f"[yellow]{str(read_error)}[/yellow]", f"[bold red]{path_object.name}[/bold red]")
        return None


def items_records_view():
    json_files = find_all_json_paths()
    if not json_files:
        colored.print("[bright_yellow][WARN][/bright_yellow] No JSON files found.")
        return
    
    error_table = Table(title="\nBroken JSON Records", width=50, show_lines=False, title_justify="left")
    # error_table = Table(title="\nBroken JSON Records:\n", title_justify="left", width=55, show_lines=False, show_edge=False, show_footer=False, show_header=False)
    error_table.add_column("Index", justify="left", style="red")
    error_table.add_column("Error", justify="left", style="yellow")
    error_table.add_column("File Name", justify="left", style="cyan")

    for idx, json_path in enumerate(sorted(json_files, key=lambda _: Path(_).stat().st_mtime), start=1):
        data = load_json(json_path, idx, error_table)
        if data is None:
            continue
        colored.print(f"[dim][CATALOG ][/dim]: Loaded [bold yellow]{len(data)}[/bold yellow] items from: [bright_cyan]{Path(json_path).name:>6}[/bright_cyan]")

    if error_table.row_count > 0:
        # colored.print(Panel(error_table, title="Summary of Errors", width=110))
        colored.print(error_table)


def records_catalog_view(details=False):
    catalog = find_all_json_paths()
    if not catalog:
        colored.print("[yellow][WARN][/yellow] No JSON files found.")
        return

    for idx, catalog_name in enumerate(sorted(catalog, key=lambda _: Path(_).stat().st_mtime), start=1):
        path_object = Path(catalog_name)
        try:
            with path_object.open("r", encoding="utf-8") as reader:
                read_catalog_details = json.load(reader)
                colored.print(f"[Game Rcord Catalog ID: {idx}] ➜ [bold cyan]{path_object.name}[/bold cyan]")
                if details:
                    sleep(0.09)
                    colored.print(read_catalog_details)

        except json.JSONDecodeError as json_struct_error:
            colored.print(f"[bright_red][ERROR {idx}][/bright_red] Invalid JSON in: [bold red]{path_object.name}[/bold red]")
            colored.print(f"[dim]{json_struct_error}[/dim]")
        except Exception as messed_up_json:
            colored.print(f"[red][FAIL][/red] Could not process file: [cyan]{path_object.name}[/cyan] — {str(messed_up_json)}")
    

def get_values_by_keys(name: str, keys: list[str] = None, filter_by: tuple = None, directory: Path = None) -> list[dict] | None:
    game_values = {"powerball", "megamillion", "lotto", "luckyday", "pick3", "pick4"}
    
    if directory is None:
        directory = Path(__file__).resolve().parents[1]

    for json_path in find_all_json_paths(directory):
        path_object = Path(json_path)
        if path_object.stem != name:
            continue

        try:
            with path_object.open("r", encoding="utf-8") as file_ready:
                records = json.load(file_ready)
                if not isinstance(records, list):
                    colored.print(f"[red] Unexpected format in:[/red] {path_object.name}")
                    return None

                filtered_records = []

                # ____ auto-infer | incase if a filter values was accidentally passed in as --keys:
                filter_inferred = None
                if not filter_by and keys:
                    for key_object in keys:
                        if key_object.lower() in game_values:
                            filter_inferred = ("game", key_object)
                            keys = None  # ___ don't treat it as a valid key:
                            break

                for entry in records:
                    # ___ apply filter:
                    if filter_by:
                        filtered_key, filtered_value = filter_by
                        if entry.get(filtered_key) != filtered_value and entry.get("selection", {}).get(filtered_key) != filtered_value:
                            continue
                    elif filter_inferred:
                        filtered_key, filtered_value = filter_inferred
                        if entry.get(filtered_key) != filtered_value:
                            continue

                    # ___ extract values:
                    if not keys:
                        filtered_records.append(entry)
                        continue

                    result = {}
                    for key_object in keys:
                        if key_object in entry:
                            result[key_object] = entry[key_object]
                        elif key_object in entry.get("selection", {}):
                            result[key_object] = entry["selection"][key_object]
                        else:
                            result[key_object] = ""
                    filtered_records.append(result)

                return filtered_records if filtered_records else [{"warning": "No records matched."}]

        except json.JSONDecodeError:
            colored.print(f"[red]✗ Invalid JSON:[/red] [bold]{path_object.name}[/bold]")
        except Exception as err:
            colored.print(f"[red]✗ Error loading:[/red] {path_object.name} — {err}")
    return None


# def game_records(items_count=False, show_catalog_details=False,  show_catalog_Ids=False):
#     if items_count:
#         items_records_view()
#     if  show_catalog_details:
#         return records_catalog_view(details=True)
#     if show_catalog_Ids:
#         return records_catalog_view(details=False)
#     else:
#         return []


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
            f"{caller_trace()}\n\t\t\t\t"
            f" Run [bold yellow]`--help`[/bold yellow] to see available [bold]cli[/bold] flags:\n"
        )

def main_call(use_rich=False):
    if use_rich:
        if "--help" in sys.argv or "-h" in sys.argv:
            print("\n")
            colored.print(epilogs.extended_epilog_rich_panle_help())
            sys.exit(0)

    parser = epilogs.extended_epilog_help()
    args = parser.parse_args()
    result = get_values_by_keys(args.name, keys=args.keys, filter_by=tuple(args.filter) if args.filter else None)

    if result:
        colored.print(f"[bright_green]✓ Extracted {len(result)} record(s) from:[/bright_green] [cyan]{args.name}.json[/cyan]")
        for idx, entry in enumerate(result, start=1):
            colored.print(f"[bold]{idx}[/bold]. {entry}")
    else:
        colored.print("[bright_red] No records found or failed to process file:[/bright_red]")


if __name__ == "__main__":
    game_records()
    # main_call(use_rich=True)