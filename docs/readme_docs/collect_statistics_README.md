# Collect Statistics:
[collect_statistics.py](/src/collect_statistics.py) script analyzes lottery game sequence statistics:<br>
Processing game records from a catalog directory:<br> 
Supports multiple games (`e.g`., `Powerball`, `MegaMillion`):<br>
Generates reports with `exact` and `partial` matches:<br>
Keep results in `html` optionall:

### Features:
- Processes lottery game records for specified games or all supported games:
- Validates sequence lengths against game-specific minimums:
- Supports detailed logging and HTML report generation:
- Customizable CLI for selecting games, sequence lengths, and output options:

#### Dependencies:
- Python 3.11
- [rich](https://pypi.org/project/rich/) see [requirements.txt](/deps/requirements.txt)
- works as cli plugin to [statistics.py](/records_analytics/statistics.py) module:
- [html_utils.py](/injectors/html_utils.py)
- Catalog directory see `.gitignore` and [quickPick.py](/src/quickPick.py) `save_selection(name: str, game: str, numbers: dict):` function:
- Wont work unless [quickPick.py](/src/quickPick.py) has been called first to generate data sets:
```bash
python3 src/quickPick.py --auto --all-names
```
---

#### CLI Examples & Command Description:
- Run the script to analyze game statistics or list supported games:
```bash
python3 src/collect_statistics.py

usage: collect_statistics.py [-h] (--all | --games GAME [GAME ...] | --list) [--min-sequence MIN_SEQUENCE] [--logs] [--save-html] [--max-exact MAX_EXACT] [--max-partial MAX_PARTIAL]

Analyze lotto game sequence statistics:

options:
  -h, --help      show this help message and exit
  --all           Run all supported games.
  --games         Run one or more specific games. Examples: --games lotto --games megamillion powerball pick4
  --list          List all supported games with their required minimum sequence.
  --min-sequence  Override default minimum sequence. Use cautiously — lower values may reduce match accuracy. If not provided, the default is used per game:
  --logs          Show detailed loading logs for each file and batch.
  --save-html     Save the report output as a styled HTML file in 'html_reports/' and open it.
  --max-exact     Max exact matches to show in terminal.
  --max-partial   Max partial matches to show in terminal.


[ERROR]: one of the arguments --all --games --list is required
```
- `--list`
- List supported games and minimum sequences:
```bash
python3 src/collect_statistics.py --list

Available games and recommended minimum sequences:

  - megamillion  → min_sequence = 5
  - powerball    → min_sequence = 5
  - lotto        → min_sequence = 6
  - luckyday     → min_sequence = 5
  - pick3        → min_sequence = 3
  - pick4        → min_sequence = 4

```
- `--all`
- Analyze all supported games:
```bash
python3 src/collect_statistics.py --all

[JOB]:   -> Processing MEGAMILLION game records in August-2025/catalog sequence depth  -> 5


        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:23:01,947
        MODULE-SRC:       -> statistics: -> Line # 120
        MESSAGE:     -> Starting sequence comparison:

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:23:01,947
        MODULE-SRC:       -> statistics: -> Line # 121
        MESSAGE:     -> Total JSON files: 2977

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:23:01,947
        MODULE-SRC:       -> statistics: -> Line # 122
        MESSAGE:     -> Total file pairs to compare: 4429776

  Comparing sequences... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Pairs: 4429776/4429776 Exact: 0 Partial: 167837 0:00:33 0:00:00 Runtime:100%
```
![collect_statistics.py --all](/docs/png_docs/collect_stats_all_flag_image_1.png)
---
![collect_statistics.py --all](/docs/png_docs/collect_stats_all_flag_image_2.png)
---
![collect_statistics.py --all](/docs/png_docs/collect_stats_all_flag_image_3.png)

- `--games powerball megamillion`
- Specific game sets: `e.g` ***> 1*** <br>
```bash
python3 src/collect_statistics.py --games powerball megamillion

[JOB]:   -> Processing POWERBALL game records in August-2025/catalog sequence depth  -> 5


        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:33:55,037
        MODULE-SRC:       -> statistics: -> Line # 120
        MESSAGE:     -> Starting sequence comparison:

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:33:55,037
        MODULE-SRC:       -> statistics: -> Line # 121
        MESSAGE:     -> Total JSON files: 2977

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:33:55,037
        MODULE-SRC:       -> statistics: -> Line # 122
        MESSAGE:     -> Total file pairs to compare: 4429776

  Comparing sequences... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Pairs: 4429776/4429776 Exact: 0 Partial: 172322 0:00:33 0:00:00 Runtime:100%

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:34:28,354
        MODULE-SRC:       -> statistics: -> Line # 170
        MESSAGE:     ->  → Total sequences in file1: 17778656

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:34:28,355
        MODULE-SRC:       -> statistics: -> Line # 171
        MESSAGE:     ->  → Total sequences in file2: 17775616

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:34:28,355
        MODULE-SRC:       -> statistics: -> Line # 172
        MESSAGE:     ->  → Avg sequences per file: 4

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:34:28,355
        MODULE-SRC:       -> statistics: -> Line # 173
        MESSAGE:     ->  → Total sequence comparisons: 71341413

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:34:28,355
        MODULE-SRC:       -> statistics: -> Line # 174
        MESSAGE:     ->  ✓ Exact matches found: 0

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:34:28,355
        MODULE-SRC:       -> statistics: -> Line # 175
        MESSAGE:     ->  ✓ Partial matches found: 172322
                                                                                                                                                                          
Sequence Match Summary:                                                                                                                                                   
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Match Type              ┃      Count ┃ Details                                                                                                                         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Partial Matches         │     172322 │ Isabelle.json ↔ Aatos.json                                                                                                      │
│                         │            │ POWERBALL: in .json key name: primary → POWERBALL: in .json key name: primary                                                   │
│                         │            │                 • Match: 40% • Values: [8, 28]                                                                                  │
│                         │            │                                                                                                                                 │
│                         │            │ Isabelle.json ↔ Borislav.json                                                                                                   │
│                         │            │ POWERBALL: in .json key name: primary → POWERBALL: in .json key name: primary                                                   │
│                         │            │                 • Match: 40% • Values: [17, 28]                                                                                 │
│                         │            │                                                                                                                                 │
│                         │            │ Isabelle.json ↔ Икона.json                                                                                                      │
│                         │            │ POWERBALL: in .json key name: primary → POWERBALL: in .json key name: primary                                                   │
│                         │            │                 • Match: 40% • Values: [8, 47]                                                                                  │
│                         │            │                                                                                                                                 │
├─────────────────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                         │            │ + 172319 more partial matches: run → display_matches(view=(True, True) to see details:                                          │
└─────────────────────────┴────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
- `--games lotto --min-sequence 4 --save-html`
- Analyze Lotto with custom sequence length write it to HTML report:
```bash
python3 src/collect_statistics.py --games lotto --min-sequence 4 --save-html

[Heads Up] Accuracy May Be Degraded: lotto recommends a minimum sequence of 6, but 4 was provided.


[JOB]:   -> Processing LOTTO game records in August-2025/catalog sequence depth  -> 4


        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:40:16,508
        MODULE-SRC:       -> statistics: -> Line # 120
        MESSAGE:     -> Starting sequence comparison:

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:40:16,508
        MODULE-SRC:       -> statistics: -> Line # 121
        MESSAGE:     -> Total JSON files: 2977

        LOG-LEVEL:        -> INFO:
        Time-Date:        -> 2025-08-13 23:40:16,508
        MODULE-SRC:       -> statistics: -> Line # 122
        MESSAGE:     -> Total file pairs to compare: 4429776

⠼ Comparing sequences... ━━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━ Pairs: 2924614/4429776 Exact: 5 Partial: 54708 0:00:26 0:00:14 Runtime: 66%
```
- html file css [sequence_stats_2025-08-13_23-40-15.html](/docs/html_report_sample/sequence_stats_2025-08-13_23-40-15.html) example: 

![--save-html](/docs/png_docs/html_example_image_1.png)
---
![--save-html](/docs/png_docs/html_example_image_2.png)
---

#### Functions:
- class CustomHelpFormatter(argparse.HelpFormatter):
>- Argparse help class for cleaner display:
```python
class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)
        return ', '.join(action.option_strings)
```

- class CustomArgumentParser(argparse.ArgumentParser):
>- Extends argparse for colored help and error messages print:
```python
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        help_text = self.format_help()
        colored.print(f"\n[bright_magenta]{help_text}[/bright_magenta]")
        colored.print(f"\n[bright_cyan][[bright_red]ERROR[/bright_red]][/bright_cyan]: [bold]{message}[/bold]\n")
        sys.exit(2)

    def print_help(self, file=None):
        help_text = self.format_help()
        colored.print(f"[bright_cyan]{help_text}[/bright_cyan]")
```
- collector(games, user_seq=None, logs=False, console=colored, max_exact=10, max_partial=3, save_all_to_html=False):
>- Game records processor: 
>- validates sequence lengths:
>- generates statistics:
```python
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

```

- main()
>- Parses CLI args:
>- Runs analysis:
```python
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
```

### Notes:
- Supported Lotto Games: 
>- MegaMillion
>- Powerball 
>- Lotto 
>- Lucky Day
>- Pick 3 
>- Pick 4
>- The script looks for a catalog/ directory in the parent directory’s subfolders (e.g., <parent>/lottery_catalog/catalog/).
- Tryes to use `--min-sequence` cautiously since in some casesd if values below the recommended minimum were used, the results may reduce accuracy:
- html reports kept in `html_reports/` if `--save-html` falg was provided:
---
### License:
- See LICENSE in the repository root for licensing details: