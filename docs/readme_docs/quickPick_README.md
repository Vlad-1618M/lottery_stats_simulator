# QuickPick:
The [quickPick.py](/src/quickPick.py) script generates random lottery number selections:<br>
Identifies primes and saves results to json files: <br> 
Supports interactive or automated modes with a styled grid display of players and game results:

## Features:
- Generates random lottery numbers for specified games and players:
- Identifies prime numbers in selections with [prime_sequence_check.py](/math_modules/prime_sequence_check.py) module:
- Saves selections to player specific json files one for each name `datetime/catalog/` dir:
- Supports interactive player selection, automated runs, and batch processing:

## Dependencies:
- Written on Python 3.13.1
- [rich](https://pypi.org/project/rich/) 
- [unidecode](https://pypi.org/project/Unidecode/)
- see [requirements.txt](/deps/requirements.txt) for more info on versions:
- [prime_sequence_check.py](/math_modules/prime_sequence_check.py)
- [glob_args.py](/src/glob_args.py)

### CLI Examples & Command Description:
>- Run the ***src/quickPick.py + options*** script to generate and save lottery number selections:
```bash
python3 src/quickPick.py
```
![quickPick.py](/docs/png_docs/quickpick_example_image_1.png)

>- `--game powerball`
>- Generate numbers for Powerball interactively: __***Run script follow promts***__:
```bash
python3 src/quickPick.py --game powerball

Available players (2977 total):

How many grid rows to display at once? (e.g., 10):
```
---
>- Interactive mode - select player name fro the list: 
![--game powerball](/docs/png_docs/quickpick_example_image_2.png)


>- Interactive mode - run quick pick for selected player:
![--game powerball](/docs/png_docs/quickpick_example_image_3.png)

>- `--auto --run-all`
>- Auto-generate numbers for all games and players:
```bash
python3 src/quickPick.py --auto --run-all
```
>- Auto mode:
![--game powerball](/docs/png_docs/quickpick_example_image_4.png)

>- `--seed 123 --game lotto`
>- Generate numbers for Lotto with a fixed `seed`: 
>- Each game gets identical number sequence sets: 
>- Initial `seed` values for both or single sets ( __***depndeting on game type***__ ) are rendom, the rest are fixed for countless re-runs per session: 

```bash
python3 src/quickPick.py --seed 123 --game lotto
```
![--game powerball](/docs/png_docs/quickpick_example_image_5.png)

### Function Description:

- `normalize_name(name):`
- Normalizes player names using Unicode NFKC and case folding:
```python
def normalize_name(name):
    if not name:
        return ""
    name = unidecode(name)
    return unicodedata.normalize("NFKC", name).casefold().strip()
```

- `get_random_selection(config: dict, seed=None) -> dict:`
- Generates random numbers for a game config, including primes:

```python
def get_random_selection(config: dict, seed=None) -> dict:
    result = {}
    for key, (count, min_val, max_val) in config.items():
        full_set, primes, _ = nitup.get_primes_from_random(count, min_val, max_val, seed)
        result[key] = full_set
        result[f"primes_in_{key}"] = primes
    return result
```
- `save_selection(name: str, game: str, numbers: dict):`
- Saves number sequence selections for each player to json artifacts:
```python
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
```
- `main():`
- Process player selection, number sequences generation and results:
```python
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

```
- `_debug_gen_more_data(limit=10):`
- Debug function: 
- Runs repeated `main()` calls up to `x` count (__not used by default__)
```python
def _debug_gen_more_data(limit=10):
    counter = 0
    while counter < limit:
        colored.print(f"\n[bright_blue][[orange1]JOB[/orange1]:][/bright_blue]\t[dim]{sys.argv[0]}[/dim] init call:\t[dim]Init Count[/dim]: [bright_yellow]{counter}[/bright_yellow]")
        counter += 1
        sleep(1)
        colored.print(f"[bright_blue][[orange1]JOB[/bright_blue]:]\t{main()}\t\t\t\t[bright_magenta]run[/bright_magenta] count: [bright_green]{counter}[/bright_green]")
```

### Notes:
- Player records are stored in in ***month_year/catalog/*** --- (e.g., `/lotto_simulator/August-2025/catalog/`*`.json` ***dynamic behaviour***):
- since artifact dir is auto created hence ***dynamic behaviour*** therefore ignored -- see `.gitignore` config: 
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
- Game configurations are sourced from __***[`glob_args.GAMES`]***__
```python
    for chosen in selected_names:
        player_game_list = [single_game] if single_game else list(glob_args.GAMES) if (run_all or auto_mode) else []

        if not player_game_list:
            colored.print(f"[red]No game specified for {chosen}. Use --game or --run-all.[/red]")
            continue

        for game in player_game_list:
            config = glob_args.GAMES[game]
            attempt = 0
            max_attempts = 30

```
- The `_debug_gen_more_data` function is for debugging and not part of the main workflow:
- Maximum attempts for number generation is set to 30 to avoid infinite loops:

### License:
- See LICENSE in the repository root for licensing details: