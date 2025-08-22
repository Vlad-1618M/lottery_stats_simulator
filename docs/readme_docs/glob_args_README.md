# Global Arguments Config:
[glob_args.py](/src/glob_args.py) script provides utility functions for parsing CLI arguments and managing lottery-related scripts for player's records catalog: <br>
- Supports: 
>- interactive player selection: 
>- game execution arguments: 
>- .yml configuration loading:

### Features:

- Parses CLI arguments for game execution and player record selection:
- Displays a paginated catalog of player `json` file artifacts:
- Integrates with info about `Sieve of Eratosthenes` explanation through [why.py](/injectors/why.py) script:
- Loads game configurations from [players.ymll](/injectors/players.yml) config:

## Dependencies:
- Written on Python 3.13.1
- [rich](https://pypi.org/project/rich/) 
- [pyyaml](https://pypi.org/project/PyYAML/)
- [logger_main.py](/logger/logger_main.py)
- [constants.py](/injectors/constants.py)
- [why.py](/injectors/why.py)
- see [requirements.txt](/deps/requirements.txt) for more info on versions:


### CLI Examples & Command Description:
- Script is an essential module designed to parse arguments for other scripts:
- But also can list player records, show arguments as tables, retrive algo info on itsown:
```bash
python3 src/glob_args.py
```
>- parse_quick_pick_args()
```python
if __name__ == "__main__":
    parse_quick_pick_args()
```
![parse_quick_pick_args()](/docs/png_docs/glob_args_example_call_image_1.png)

#### Show Sieve of Eratosthenes algo explanation: 
>- why.info_statement(explain_primes=True)
```python
if __name__ == "__main__":
    why.info_statement(explain_primes=True)
```
![why.info_statement](/docs/png_docs/glob_args_example_call_image_2.png)

#### Select player record by index:
>- show_table_help_args() 
```python
if __name__ == "__main__":
    show_table_help_args()
```
![show_table_help_args()](/docs/png_docs/glob_args_example_call_image_3.png)

#### List player records interactively:
>- entrant_catalog(records_dir="players")
```python
if __name__ == "__main__":
    [print(f"- count:{idx:>5}:\t{Path(name).name}") for idx, name in enumerate(entrant_catalog(records_dir="players"), start=1)]
```
![entrant_catalog(records_dir="players"](/docs/png_docs/glob_args_example_call_image_4.png)

- For debugging purposes some of function calls are kept in main and commented out: 
```python
if __name__ == "__main__":
    pass
    # why.info_statement(explain_primes=True)
    # parse_quick_pick_args()
    # show_table_help_args()
    # [print(f"- count:{idx:>5}:\t{Path(name).name}") for idx, name in enumerate(entrant_catalog(records_dir="catalog"), start=1)]
    # print(entrant_catalog(records_dir="players"))
    # [print(f"- count:{idx:>5}:\t{Path(name).name}") for idx, name in enumerate(entrant_catalog(records_dir="players"), start=1)]
``` 

### Functions Description:
- `entrant_catalog(records_dir: str)`
- Loads [players.yml](/injectors/players.yml) | generates json paths for each palyer: 
```python
def entrant_catalog(records_dir: str):
    all_artifacts = []
    stamp = datetime.now().strftime("%B-%Y")
    storage = Path(__file__).resolve().parents[1] / stamp / records_dir
    _ini = Path(__file__).resolve().parents[1] / "injectors"
    get_cfg = [cfg for cfg in _ini.iterdir() if cfg.is_file() and cfg.suffix == ".yml"]
    
    for cfg_file in get_cfg:
        with cfg_file.open("r", encoding="utf-8") as entrant:
            data = yaml.safe_load(entrant)
            names = data.get("name", [])
            storage.mkdir(parents=True, exist_ok=True)

            for name in names:
                json_path = storage / f"{name}.json"
                all_artifacts.append(str(json_path))

    return all_artifacts
```
- `get_available_players():`
- Returns a list of tuples with player labels and json file paths:
```python
def get_available_players() -> list[tuple[str, Path]]:
    """Returns a list of tuples: (display label, path to .json file)"""
    parent = Path(__file__).resolve().parents[1]
    all_jsons = parent.glob("*/catalog/*.json")

    players = []
    for artifact in all_jsons:
        if artifact.is_file():
            month_dir = artifact.parent.parent.name  # e.g., June-2025
            display = f"{artifact.stem:<10} {month_dir:>20}"
            players.append((display, artifact))

    return sorted(players, key=lambda call: call[0].lower())
```
- `show_table_help_args()`
- Displays paginated catalog of player records for selection by index values:
```python
def show_table_help_args():
    players = get_available_players()
    if not players:
        console.print("[red]Empty Catalog or Nothing Found[/red]")
        return

    per_page = 50
    total = len(players)
    page = 0

    while True:
        start = page * per_page
        end = min(start + per_page, total)
        chunk = players[start:end]
        chunk = players[start:end]

        listed = "\n".join(f"[dim]{item + 1:<5}[/dim] {label:>19}" for item, (label, _) in enumerate(chunk, start=start))

        help_msg = (
            f"\n[yellow]--name-index[/yellow] [bold]int[/bold] [dim]= select JSON record by index[/dim]\n"
            f"Call Example: [dim]->[/dim] [green]{sys.argv[0]} [bright_yellow]--name-index {start + 1}[/bright_yellow][/green]\n\n"
            f"[bright_yellow]Current Catalog[/bright_yellow]:\n"
            f"[bright_green]Available Player Records[/bright_green]: [bold]\n\n{listed}[/bold]")

        console.print(Panel(help_msg, title="Records Catalog Help", width=60))
        console.print(
            f"\n[bright_cyan]Enter[/bright_cyan] [dim]index[/dim] [bright_cyan]number[/bright_cyan] to select or press "
            f"[bold][[/bold][bright_magenta]Enter[/bright_magenta][bold]][/bold] to show next {per_page}, "
            f"[bright_red]q[/bright_red] to quit:")
        response = input().strip().lower()

        if response.isdigit():
            selected_index = int(response)
            if 1 <= selected_index <= total:
                sys.argv.extend(["--name-index", str(selected_index)])
                return
            else:
                console.print(f"[red]Index out of range (1 to {total})[/red]")
                try_again = input("Try again? (y/N): ").strip().lower()
                if try_again != "y":
                    break
        elif response == "q":
            break
        else:
            if end >= total:
                console.print("[yellow]Reached end of catalog.[/yellow]")
                break
            page += 1
```
- `parse_table_args()`
- parses cli arguments for selecting json records by index: module used in [user_records.py](/src/user_records.py) 
```python
def parse_table_args():
    args = sys.argv[1:]

    options = {
        "json_path": None,
        "translit": False,
        "csv": False,
        "md": False
    }

    players = get_available_players()

    if not args or "--name-index" not in args:
        show_table_help_args()
        return options

    try:
        index_pos = args.index("--name-index") + 1
        selected_index = int(args[index_pos]) - 1

        if not (0 <= selected_index < len(players)):
            console.print(f"[red]Invalid index: {selected_index + 1}[/red]")
            return options

        options["json_path"] = players[selected_index][1]

    except (IndexError, ValueError):
        console.print("[red]Error: '--name-index' must be followed by a valid number[/red]")
        return options

    options["translit"] = "--translit" in args
    options["csv"] = "--csv" in args
    options["md"] = "--md" in args

    return options
```
- `parse_quick_pick_args()`
- parses cli arguments for game execution (e.g., `--game`, `--seed`) module used in [quickPick.py](/src/quickPick.py) 

```python
def parse_quick_pick_args():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        why.info_statement(explain_primes=False)

    if "--sieve" in args:
        sieve_args = ["--algo"]
        if "--lang" in args:
            try:
                idx = args.index("--lang")
                lang_val = args[idx + 1]
                sieve_args.extend(["--lang", lang_val])
            except IndexError:
                console.print("[red]Missing language code after --lang[/red]")
                sys.exit(1)

        if "--langs" in args:
            sieve_args.append("--langs")

        if not sieve_args:
            sieve_args.append("--algo")

        why.external_calls(sieve_args)
        sys.exit(0)

    auto_mode = "--auto" in args
    run_all = "--run-all" in args
    all_names = "--all-names" in args
    seed = None
    game = None

    if "--seed" in args:
        try:
            seed_pos = args.index("--seed")
            seed = int(args[seed_pos + 1])
        except (ValueError, IndexError):
            log_it.error("--seed requires an integer value")
            why.info_statement(explain_primes=False)

    if "--game" in args:
        try:
            game_pos = args.index("--game")
            game = args[game_pos + 1].lower()
            if game not in GAMES:
                log_it.error(f"Unknown game '{game}'. Available games: {', '.join(GAMES.keys())}")
                why.info_statement(explain_primes=False)
        except IndexError:
            log_it.error("--game requires a name")
            why.info_statement(explain_primes=False)

    return auto_mode, run_all, all_names, seed, game
```

### Notes:
- Player records are expected in ***month_year/catalog/*** --- (e.g., `/lotto_simulator/August-2025/catalog/` ***dynamic behaviour***):
- since artifact dir is auto created hence ***dynamic behaviour*** therefore ignored -- see `.gitignore` config: 
```python
    for cfg_file in get_cfg:
        with cfg_file.open("r", encoding="utf-8") as entrant:
            data = yaml.safe_load(entrant)
            names = data.get("name", [])
            storage.mkdir(parents=True, exist_ok=True)
```
```bash
# local:
.logs
lotto_draw_results
lotto_screenshots
lottery_catalog
/build/gotools/go_compiled
html_reports
Aug-*
June-*
July-*
August-*
```
- `--name-index` option allows selecting records from the catalog by index value name association:
- game configurations loaded by [constants.py](/injectors/constants.py) `.yml` files in [players.yml](/injectors/players.yml)

### License:
- See LICENSE in the repository root for licensing details: