# #!/usr/bin/env python
# # -*- config: utf-8 -*-

import sys
import argparse
from pathlib import Path
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))

from records_analytics.statistics import main as filtered_stats
from injectors.html_utils import save_html_report

colored = Console()
SRC = Path(__file__).resolve().parents[1]

AVAILABLE_GAMES = ["megamillion", "powerball", "lotto", "luckyday", "pick3", "pick4"]
MIN_SEQ_MAP = {"lotto": 6, "megamillion": 5, "powerball": 5, "luckyday": 5, "pick3": 3, "pick4": 4}


# _____ help msg | handle errors:
class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)
        return ', '.join(action.option_strings)


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        help_text = self.format_help()
        colored.print(f"\n[bright_magenta]{help_text}[/bright_magenta]")
        colored.print(f"\n[bright_cyan][[bright_red]ERROR[/bright_red]][/bright_cyan]: [bold]{message}[/bold]\n")
        sys.exit(2)

    def print_help(self, file=None):
        help_text = self.format_help()
        colored.print(f"[bright_cyan]{help_text}[/bright_cyan]")


# _____ core logic | see 'records_analytics.statistics.py' for details:
def collector(games, user_seq=None, logs=False, console=colored, max_exact=10, max_partial=3, save_all_to_html=False):
    catalog_dirs = list(SRC.glob("*/catalog"))
    catalog_path = Path(*catalog_dirs) if catalog_dirs else Path("unknown")

    for game in games:
        required_seq = MIN_SEQ_MAP.get(game, 5)
        actual_seq = user_seq if user_seq is not None else required_seq

        if actual_seq < required_seq:
            warning = (
                f"\n[orange1][[bright_red]Heads Up[/bright_red]][/orange1] [bold]Accuracy May Be Degraded[/bold]: "
                f"[bright_green]{game}[/bright_green] recommends a minimum sequence of "
                f"[bright_magenta]{required_seq}[/bright_magenta], but [bright_red]{actual_seq}[/bright_red] was provided.\n"
            )
            console.print(warning)

        job_msg = (
            f"\n[bright_green][JOB][/bright_green]:\t[bold] ->[/bold] Processing [bright_magenta]{game.upper()}[/bright_magenta] game records "
            f"in [cyan]{catalog_path.parent.name}/{catalog_path.name}[/cyan] sequence depth [bright_magenta] ->[/bright_magenta] [bold]{actual_seq}[/bold]\n"
        )
        console.print(job_msg)
        filtered_stats(main_depth_level=1, minimum_sequence=actual_seq, games=game, logs=logs, console=console, max_exact=max_exact, max_partial=max_partial, save_all_to_html=save_all_to_html,)


# _____ entrypoint
if __name__ == "__main__":
    parser = CustomArgumentParser(description="Analyze lotto game sequence statistics:", formatter_class=CustomHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run all supported games.")
    group.add_argument("--games", nargs="+", choices=AVAILABLE_GAMES, metavar="GAME", help=("Run one or more specific games.\n\tExamples:\n\t  --games lotto\n\t  --games megamillion powerball pick4"))
    group.add_argument("--list", action="store_true", help="List all supported games with their required minimum sequence.")
    parser.add_argument("--min-sequence", type=int, help=("Override default minimum sequence.\n\tUse cautiously — lower values may reduce match accuracy.\n\tIf not provided, the default is used per game:"))
    parser.add_argument("--logs", action="store_true", help="Show detailed loading logs for each file and batch.")
    parser.add_argument("--save-html", action="store_true", help="Save the report output as a styled HTML file in 'html_reports/' and open it.")
    parser.add_argument("--max-exact", type=int, default=10, help="Max exact matches to show in terminal.")
    parser.add_argument("--max-partial", type=int, default=3, help="Max partial matches to show in terminal.")
    args = parser.parse_args()

    if args.list:
        colored.print("\n[bright_green]Available games and recommended minimum sequences:[/bright_green]\n")
        for g in AVAILABLE_GAMES:
            colored.print(f"  - [cyan]{g:<12}[/cyan] → [magenta]min_sequence = {MIN_SEQ_MAP[g]}[/magenta]")
        sys.exit(0)

    selected_games = AVAILABLE_GAMES if args.all else args.games

    if args.save_html:
        save_html_report(collector, selected_games, user_seq=args.min_sequence, logs=args.logs, open_browser=True, max_exact=args.max_exact, max_partial=args.max_partial,)
    else:
        collector(selected_games, user_seq=args.min_sequence, logs=args.logs, max_exact=args.max_exact, max_partial=args.max_partial,)
