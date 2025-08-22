#!/usr/bin/env python
# -*- config: utf-8 -*-
# mypy: ignore-errors

import argparse
from rich.text import Text
from rich.panel import Panel
from rich.console import Console

colored = Console()

EXAMPLE_GAME_TYPE = "powerball"
EXAMPLE_GAME = "megamillion"
EXAMPLE_NAME = "Χρήστος"

# def extended_epilog_help(name: str = "Zagreb", game_type: str = "powerball"):
def extended_epilog_help():
    _decor = "¬"*40
    cli_help = [
        # f"{_decor}{_decor:>59}\n"
        f"{_decor} CLI EXAMPLE CALLS {_decor}\n\n"
        f"--name {EXAMPLE_NAME} \t\t\t\t--> Print all entries from {EXAMPLE_NAME}.json",
        f"--name {EXAMPLE_NAME} --keys timestamp game \t--> Extract only 'timestamp' and 'game' fields from each entry",
        f"--name {EXAMPLE_NAME} --filter game {EXAMPLE_GAME_TYPE} \t--> Only include entries where 'game' == '{EXAMPLE_GAME_TYPE}'",
        f"--name {EXAMPLE_NAME} --keys {EXAMPLE_GAME_TYPE} \t\t--> (auto-inferred) Filter by game='{EXAMPLE_GAME_TYPE}' — same as --filter game {EXAMPLE_GAME_TYPE}",
        f"--name {EXAMPLE_NAME} --keys timestamp \t\t--> Extract only the timestamp from each entry\n",
        f"--name {EXAMPLE_NAME} --keys timestamp primary power --filter game {EXAMPLE_GAME_TYPE} \t--> Filter by game='{EXAMPLE_GAME_TYPE}' and extract specific fields\n",
        "Note:",
        "\t• Keys searched in both top-level and 'selection' block",
        f"\t• Auto-fallback: values like '{EXAMPLE_GAME_TYPE}' or '{EXAMPLE_GAME}' used alone in --keys will be treated as filters"
    ]

    _epilog = "\n".join(cli_help)
    parser = argparse.ArgumentParser(description="Query values from JSON game records.", epilog=_epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--name", required=True, help=f"Base name of the JSON file (e.g., {EXAMPLE_GAME_TYPE} for {EXAMPLE_GAME_TYPE}.json)")
    parser.add_argument("--keys", nargs="*", help="Fields to extract (e.g., timestamp game primary mega)")
    parser.add_argument("--filter", nargs=2, metavar=("key", "value"), help="Filter records where key equals value")
    return parser


def extended_epilog_rich_panle_help(name=EXAMPLE_NAME, game=EXAMPLE_GAME):
    # _decor = "¬"*83
    _decor = "¬"*133
    help_msg = Text()

    help_msg.append(f"\n--name {name}\t\t\t\t\t", style="bright_yellow")
    help_msg.append(f"Print all entries from {name}.json:\n", style="bright_cyan")

    help_msg.append(f"--name {name} --keys timestamp\t\t\t", style="bright_yellow")
    help_msg.append("Extract only the timestamp from each entry:\n", style="bright_cyan")

    help_msg.append(f"--name {name} --keys {game}\t\t", style="bright_yellow")
    help_msg.append(f"[auto-inferred] Filter by game={game}:\n", style="bright_cyan")

    help_msg.append(f"--name {name} --keys timestamp game:\t\t", style="bright_yellow")
    help_msg.append("Extract only 'timestamp' and 'game' key pair value fields:\n", style="bright_cyan")

    help_msg.append(f"--name {name} --filter game {game}\t", style="bright_yellow")
    help_msg.append(f"Only include entries where 'game' == {game}:\n", style="bright_cyan")

    help_msg.append(f"--name {name} --keys timestamp primary power --filter game {game}\t", style="bright_yellow")
    help_msg.append(f"Filter by game='{game}' and extract specific fields\n", style="bright_cyan")

    help_msg.append(f"{_decor}", style="dim")
    help_msg.append("\nNote:\n", style="bright_magenta")

    help_msg.append("\t• Keys searched in both top-level and 'selection' block:\n", style="bright_orange1")
    help_msg.append(f"\t• Auto-fallback: values like {game} or megamillion used in --keys will be treated as filters\n", style="bright_orange1")
    return Panel(help_msg, title="[bright_magenta]CLI Examples Calls[/bright_magenta]", border_style="white", width=140)

    # return Panel(help_msg, title="[bold cyan]Examples & Usage[/bold cyan]", border_style="yellow", width=140)
    # return Panel(help_msg, title="[bright_magenta]CLI Examples Calls[/bright_magenta]", border_style="orange1", width=140)
    # return Panel(help_msg, title="[bright_magenta]CLI Examples Calls[/bright_magenta]", border_style="underline", width=140)
    # return Panel(help_msg, title="[bright_magenta]CLI Examples Calls[/bright_magenta]", border_style="green", width=140)


if __name__ == "__main__":
    pass
