#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import json
from pathlib import Path
from rich.table import Table
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))
from injectors.render_translit import AutoTranslator as disenchant
from src import glob_args

# from experemental import themed_decorator as thought
colored = Console()


def get_table(fs_name, drop_english=None, get_csv=False, get_md=False):
    with fs_name.open("r", encoding="utf-8") as f:
        search_in = [json.load(f)]

    if not search_in[0]:
        colored.print(f"[red]✘ No data found in:[/red] {fs_name}")
        return

    # _______ collect all unique selection keys from all entries:
    selection_keys = set()
    for entry in search_in[0]:
        selection_keys.update(entry["selection"].keys())

    # _______ initialize translator only if drop_english is provided:
    no_english = None
    translated_keys = {}
    from_language = "English"
    to_language = None

    if drop_english:
        no_english = disenchant(language=drop_english)
        to_language = drop_english
        translated_keys = {
            key: no_english.translate(key.replace("_", " ").capitalize())
            for key in sorted(selection_keys)
        }

    # _______ define static labels and title:
    default_labels = {
        "title": "Games Table 🤔",
        "date": "Date:",
        "game": "Played Game:"
    }

    args_in_use = {_kyes: _value for _kyes, _value in ARGS.items() if _value and _kyes not in {"json_path"}}

    if no_english:
        default_labels = {_kyes: no_english.translate(_value).upper() for _kyes, _value in default_labels.items()}
        translated_args = {no_english.translate(_kyes): no_english.translate(str(_value)) if isinstance(_value, (bool, str)) else _value for _kyes, _value in args_in_use.items()}
    else:
        translated_args = args_in_use

    # _______ Format title:
    short_path = Path(*fs_name.parts[-3:]).as_posix()
    table_title = f"[bold] {short_path.upper():<40} [/bold] [bold yellow]{default_labels['title']}[/bold yellow]"

    table = Table(title=table_title, show_lines=True)
    table.add_column(default_labels["date"], justify="center", style="cyan", no_wrap=True)
    table.add_column(default_labels["game"], justify="center", style="magenta", no_wrap=True)

    for key in sorted(selection_keys):
        label = translated_keys.get(key, key).upper()
        table.add_column(label, justify="left", style="green")

    all_rows = []
    headers = [default_labels["date"], default_labels["game"]] + [translated_keys.get(k, k) for k in sorted(selection_keys)]

    for data in search_in[0]:
        when = data["timestamp"].split("T")[0]
        game_type = data["game"]
        selections = data["selection"]

        row = [when, game_type]
        for key in sorted(selection_keys):
            numbers = selections.get(key, [])
            row.append(" ".join(map(str, numbers)))

        table.add_row(*row)
        all_rows.append(row)

    colored.print("\n", table, end="\n\n")

    # _______ show additional args used:
    if translated_args:
        colored.print("\n[bold cyan]Used Arg-Options:[/bold cyan]")
        for key, value in translated_args.items():
            colored.print(f"\t[green]{key}[/green]: [yellow]{value}[/yellow]")
        if drop_english and to_language:
            colored.print(f"[dim]Translated From:[/dim] [blue]{from_language}[/blue] → [bold magenta]{to_language.upper()}[/bold magenta]")
        colored.rule(f"\n[dim]{cool}[/dim]", style="dim", characters="-")

    # _______ output to CSV and Markdown:
    lang_suffix = f"_{drop_english}" if drop_english else ""
    catalog_dir = Path(__file__).resolve().parents[1] / "lottery_catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)

    basename = fs_name.stem

    if get_csv:
        csv_out = catalog_dir / f"{basename}{lang_suffix}.csv"
        with csv_out.open("w", newline='', encoding="utf-8") as catalog:
            writer = csv.writer(catalog)
            writer.writerow(headers)
            writer.writerows(all_rows)

    if get_md:
        md_out = catalog_dir / f"{basename}{lang_suffix}.md"
        with md_out.open("w", encoding="utf-8") as catalog:
            catalog.write(f"# {default_labels['title']}\n\n")
            catalog.write("| " + " | ".join(headers) + " |\n")
            catalog.write("|" + "---|" * len(headers) + "\n")
            for row in all_rows:
                catalog.write("| " + " | ".join(row) + " |\n")

def main(player=None, language_catalog=False, csv_file=False, md_file=False):
    colored.rule(f"[dim]Processing {thumbsUp}[/dim]")
    if not player:
        return
    # # ____ check if a valid language was provided trhough --translit
    # translit = None
    # if language_catalog and isinstance(language_catalog, str):
    #     translit = language_catalog.lower()
    # if not translit:

    if language_catalog:
        colored.print("\n[bold]Available Languages:[/bold]\n")
        google_language_catalog = disenchant.available_languages(as_dict=True)

        for code, name in google_language_catalog.items():
            colored.print(f"[bold cyan]{name:<8}[/bold cyan][yellow] <- [/yellow][dim]{code:>21}[/dim]")

        colored.print("\nIn what [bold yellow]language[/bold yellow] ?")
        colored.print("[bold green]Both accepted [/bold green] — the [dim]language name[/dim] or its [bold cyan]abbreviation code[/bold cyan]:")
        translit = input(" >> ? ").strip().lower()

        language_selector = (
            translit if translit in google_language_catalog
            else next((code for code, name in google_language_catalog.items() if name.lower() == translit), None)
        )

        if language_selector:
            get_table(fs_name=player, drop_english=language_selector, get_csv=csv_file, get_md=md_file)
        else:
            colored.print(f"[red] Invalid language input: '{translit}'[/red]")
    else:
        get_table(fs_name=player, get_csv=csv_file, get_md=md_file)


if __name__ == "__main__":
    thumbsUp = "👍🏻"
    cool = "😎"
    thinking = "🤔"

    ARGS = glob_args.parse_table_args()
    # main(player=ARGS.get("json_path"), language_catalog=ARGS.get("translit", True), csv_file=ARGS.get("csv", False), md_file=ARGS.get("md", False))
    main(player=ARGS.get("json_path"), language_catalog=ARGS.get("translit", False), csv_file=ARGS.get("csv", False), md_file=ARGS.get("md", False))
    
    # main(
    #     player=ARGS.get("json_path"),
    #     language_catalog=ARGS.get("translit", False), 
    #     csv_file=ARGS.get("csv", False),
    #     md_file=ARGS.get("md", False)
    # )
