#!/usr/bin/env python
# -*- config: utf-8 -*-
# mypy: ignore-errors

import os
import sys
import json
import shlex
import inspect
from pathlib import Path
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


def main_call(use_rich=False):
    if use_rich and ("--help" in sys.argv or "-h" in sys.argv):
        colored.print("\n", epilogs.extended_epilog_rich_panle_help())
        sys.exit(0)

    parser = epilogs.extended_epilog_help()
    args = parser.parse_args()
    result = get_values_by_keys(args.name, keys=args.keys, filter_by=tuple(args.filter) if args.filter else None)
    
    details = {"name": args.name, "keys": args.keys if args.keys else None, "filter": args.filter if args.filter else None}
    # details = {"name": args.name}
    # if args.keys:
    #     details["keys"] = args.keys
    # if args.filter:
    #     details["filter"] = args.filter

    if result:
        detail_str = ", ".join(f"{_keys}='{_values}'" for _keys, _values in details.items())
        colored.print(f"\n[bold green]✓[/bold green] [bold cyan]{args.name}[/bold cyan].json got total of [bold yellow]{len(result)}[/bold yellow] [bold magenta]{detail_str}[/bold magenta] records:\n" + "[dim]_[/dim]" * 185)
        # colored.print(f"\n[bold green]✓[/bold green] [bold cyan]{args.name}[/bold cyan].json got total of [bold yellow]{len(result)}[/bold yellow] [bold magenta]{detail_str.split("name=")[-1].split("keys=")[-1]}[/bold magenta] records:\n" + "[dim]_[/dim]" * 185)
        for idx, entry in enumerate(result, start=1):
            colored.print(f"[bold]{idx:>4}[/bold]. {entry}")
    else:
        colored.print(f"\n[bright_red]Records Not found[/bright_red] - [bold]failed[/bold] to process:\t[bold magenta]{args.name}[/bold magenta].json file:\n" + "[dim]=[/dim]" * 90)


if __name__ == "__main__":
    main_call(use_rich=True)
