# Statistics Simulator - Python based Analysis Tool:

## Overview:
- In addition to [GO based data analytics tool](/docs/readme_docs/statistics_go_based_tool.md), this Python engine provides interactive data analysis and visualization as an enhancement capability to an overall algo based [scripts](/run_search/):
- Unlike the Go version, which handles batch processing and structured reports, the Python engine is built for exploratory data analysis, dynamic comparisons, and trying out various sequences in real-time:

## Project Structure:
```text
run_search/use_python/
├── compare_sequence_to_draws.py    # Sequence comparison against historical draws:
├── frequency_maps.py               # Vertical index/position frequency analysis:
├── generate_suggestions.py         # Suggestion generation with data provenance:
└── use_rarest_sequence.py          # Core rarest sequence algorithm:
```
---
### Core Components:

1. ***___Sequence Comparison Engine___***: 
* [compare_sequence_to_draws.py](/run_search/use_python/compare_sequence_to_draws.py) - compares target number sequences against historical lottery draws to find matches and overlaps:
    * ***Helps With***:
        - Dual matching strategies: - Exact sequence matching and partial overlap detection:
        - Multi-game support: - Powerball, Mega Millions, Lotto, e.t.c:
        - Bonus number analysis: - Separate comparison for bonus numbers, **_e.g. `powerball`, `mega`_**:
        - [Rich](https://rich.readthedocs.io/en/latest/introduction.html) visual output: - Color-coded results with grouping by match count:
        - Input: - Manual sequences or auto-generated rarest sequences:
        - Core Algorithm:
            ```python
            def compare_sequence_to_draws(input_sequence: List[int], game: str, sequence_key: str, records: List[dict], match_type: str = "exact", debug: bool = False,) -> List[dict]:
                # Exact matching: sorted(drawn) == sorted(input_sequence)
                # Partial matching: input_set.intersection(set(drawn))
            ```
        - ___Necessity___: 
            - Retunrs data on how suggested numbers have performed historically: 
            - Helps understand some practical implications of how others have played, strategies if any:  

---
2. **___Vertical Frequency Analysis___**:
* [frequency_maps.py](/run_search/use_python/frequency_maps.py) - analyzes number of index-based frequencies by specific positions in sequences:
    - Key Points: 
        - Unlike traditional frequency counting which treats all positions equally, this one, analyzes each position separately:
            ```bash
                  ⬇ Position 0 frequency distribution:
                ["4",  "17", "27", "34", "69"] 
                
                        ⬇  Position 1 frequency distribution:             
                ["1",  "8",  "31", "56", "67"]

                              ⬇  Position 2 frequency distribution:
                ["2",  "6",  "8",  "14", "49"]
                
                e.t.c ...
                ["12", "27", "42", "59", "65"]
                ["18", "27", "29", "33", "70"]
                ["17", "30", "34", "63", "67"]
                ["14", "21", "25", "49", "52"]
                ["22", "41", "42", "59", "69"]
                ["11", "43", "54", "55", "63"]
                ["6",  "10", "24", "35", "43"]
            ```
    - Data Structure:
        ```python
            def build_frequency_maps(
                json_paths: List[Union[str, Path]], max_index_per_game: Dict[str, int] = None, 
                debug: bool = False, throttle: int = 100, export_path: Optional[Union[str, Path]] = None) -> Dict[str, Dict[str, Dict[int, Counter]]]:
            """ Build vertical frequency maps per index for numeric sequences:
                frequency_map[game][sequence_name][index][value] -> count """
            
            frequency_map: Dict[str, Dict[str, Dict[int, Counter]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
            progress_counter = 0
            last_debug = time()
            ....
        ```
        ```shell
            # Example: frequency_map["powerball"]["primary"][0][5] = 47
        ```
    - Advanced Features:
        - Throttled progress reporting: Real-time processing feedback:
        - Export capabilities: JSON output for external analysis:
        - Top/rare identification: Shows most and least frequent numbers per position:
        - Game-specific limits: Respects different game formats:
    - ___Necessity___:
        - Unlike ___`aggregate`___ analysis algos, the ___`positional`___ frequency analysis gest key patterns and helps with the question like, ___`which numbers appear most often in each specific drawing position`___:

---
3. **___Suggestions___**: 
    * [generate_suggestions.py](/run_search/use_python/generate_suggestions.py) - generates number suggestions while tracking an exact data source origin (**_e.g. `historic`, `recent`, `users catalog`_**):
        - Key Features:
            - Data source tracking: - knows where the suggested numbers came from: ___user catalogs___, ___recent draws___, or ___historical data___:
            - Duplicate elimination: - keeps sequences unique:
            - Multi-source integration: - combines ___`user data`___ with official ___`draw results`___:
            - Output: - Shows file names and line numbers for each suggested number:

        - Data Source Classification:
            - Player Catalogs: - User's personal number selections:
            - Recent Draws: - Latest official lottery results:
            - Historical Data: - Long-term draw archives:
    
    - ___Necessity___:
        - Transparency in suggestion generation helps to understand why specific numbers were recommended:


---
4. **__Rarest Sequence Algorithm__**: 
    * [use_rarest_sequence.py](/run_search/use_python/use_rarest_sequence.py) - the core "`rarest numbers`" strategy by selecting least-frequent numbers at each sequence position:
        - Algorithm / Logic:
            ```python
                def construct_rarest_sequence(frequency_map: Dict[str, Dict[str, Dict[int, Counter]]], 
                            game: str, sequence_key: str = "primary", count: Optional[int] = None, debug: bool = False,) -> List[int]:
                        """ Build a sequence choosing the least-frequent number at each index.
                            frequency_map: game -> sequence_key -> index -> Counter(number -> freq) """
                # ___ validate game & sequence_key exists:
                if game not in frequency_map:
                    raise KeyError(f"Game '{game}' not found in frequency_map keys: {list(frequency_map.keys())}")
                if sequence_key not in frequency_map[game]:
                    raise KeyError(f"sequence_key '{sequence_key}' not in frequency_map['{game}'] keys: {list(frequency_map[game].keys())}")

                game_map: Dict[int, Counter] = frequency_map[game][sequence_key]
                ....
            ```
            >- For each position index:
                >   - Find all numbers that have appeared in that position
                >   - Select the number with lowest frequency count
                >   - Break ties by choosing smaller number
            
            ```python
                for idx in range(count):
                    counter = game_map.get(idx)
                    if not counter or not any(counter.values()):
                    # if not counter or sum(counter.values()) == 0:
                        raise ValueError(f"No frequency data for index {idx} in game='{game}', sequence_key='{sequence_key}'.")

                    # ___ coerce keys to int (in case they were stored as strings)
                    norm_items = []
                    for key_int, _value in counter.items():
                        try:
                            keys = int(key_int)
                        except (TypeError, ValueError):
                            # ___ skip for any non-numeric values such as 'N/A'
                            continue
                        norm_items.append((keys, _value))

                    if not norm_items:
                        raise ValueError(f"All entries at index {idx} are non-numeric for game='{game}', key='{sequence_key}'.")

                    # ___ choose rarest with deterministic tie-break: (freq asc, number asc)
                    rare_value, rare_freq = min(norm_items, key=lambda key_value: (key_value[1], key_value[0]))
                    result.append(rare_value)
                    ..... 
                ```
        - Characteristics:
            - Position-aware:   - meaning it analyzes the frequency of numbers based on where they appear in the sequence:
            - Deterministic:    - Same input always produces same output:
            - Validation:       - Error checking for data quality:
        
        - ___Necessity___:
            - Offers a mathematically grounded alternative to random selection. 
            - Operates on the hypothesis that numbers drawn less frequently may be due for an appearance, hence somewhat reasoned strategy instead of pure chance:
            <!-- - Operates on the hypothesis that less-frequently drawn numbers may be due for appearance: -->

---

### Data Integration Architecture:
* Multi-Source Data Loading:
    - The Python engine integrates three distinct data sources:
        - User Catalogs: __`*/catalog/*.json`__
        - Personal number selection history:
            - Timestamped user preferences: 
            - Format: ___`{"game": "powerball", "selection": {"primary": [1,2,3,4,5], "power": [6]}}`___
        ---
        - Recent Draws: ___`/lotto_draw_results/`___
            - Automatically scraped current results:
            - Latest winning combinations:
            - Real-time data integration:
        ---
        - Historical Archives: __`/historical_lotto_draw_results/`__
            - Long-term statistical base:
            - Decades of draw results:
            - Foundation for frequency analysis:
        ---
        - Normalization Pipeline:
            >- Handles multiple JSON formats
            >- Normalizes game names (megamillions → megamillion)
            >- Standardizes number formats ("11, 12, 29" → [11, 12, 29])
        
            ```python
                def iter_json_catalogs_with_trace(json_paths: List[Union[str, Path]]) -> Generator[Tuple[dict, str, int], None, None]:
                    for path in map(Path, json_paths):
                        raw_tag = path.stem.split("_")[0].lower()
                        game_tag = GAME_NAME_ALIASES.get(raw_tag, raw_tag)
                        try:
                            with path.open("r", encoding="utf-8") as record_file:
                                try:
                                    data = json.load(record_file)
                                    if isinstance(data, list):
                                        for line_no, record in enumerate(data, start=1):
                                            if "selection" not in record and "primary_numbers" in record:
                                                record["game"] = game_tag
                                                
                                                # Handle both formats of primary_numbers
                                                primary_nums = record.get("primary_numbers", [])
                                                if primary_nums and isinstance(primary_nums[0], str) and "," in primary_nums[0]:
                                                    # Format: ["11, 12, 29, 42, 44, 47"]
                                                    primary_nums = [num.strip() for num in primary_nums[0].split(",")]
                                                else:
                                                    # Format: ["5", "7", "20", "26", "34", "40"]
                                                    primary_nums = primary_nums
                                                
                                                record["selection"] = {
                                                    "primary": list(map(int, primary_nums)),
                                                    "mega": [int(record["mega"])] if record.get("mega") not in [None, "N/A"] else [],
                                                    "power": [int(record["powerball"])] if record.get("powerball") not in [None, "N/A"] else []}
                                            # yield record, path.name, line_no
                                            yield record, str(path), line_no

                                except json.JSONDecodeError:
                                    continue
                        except Exception as e:
                            colored.print(f"[red]Failed to open {path}[/red]: {e}")
            ```

---
## Examples:
> - [compare_sequence_to_draws.py](/run_search/use_python/compare_sequence_to_draws.py)
```bash
    python run_search/use_python/compare_sequence_to_draws.py --help
    usage: compare_sequence_to_draws.py [-h] [-g {powerball,megamillion,lotto,pick3,pick4}] [-k KEY] [-m {partial,exact}] [--manual MANUAL] [--bonus BONUS] [--all-games] [--both-depths] [--debug] [--details] [--show-loaded]

    Compare a target number sequence (rarest or manual) against historical draw results:

    options:
    -h, --help            show this help message and exit
    -g, --game {powerball,megamillion,lotto,pick3,pick4}
    -k, --key KEY         Draw selection key to compare: --> (default: primary_numbers)
    -m, --match {partial,exact}
    --manual MANUAL       Comma-separated alternative primary numbers to compare: --> (e.g., '7,12,30,40,69')
    --bonus BONUS         Bonus number for Mega/Power: (single int value)
    --all-games           Run across all supported games:
    --both-depths         Run both partial and exact matching:
    --debug
    --details             Verbose draw file loading logs:
    --show-loaded         Print every parsed draw record as .jsons:
```
```bash
    python run_search/use_python/compare_sequence_to_draws.py --game=powerball --manual="7,12,30,40,69" --bonus=25
```
> - ![compare_sequence_to_draws](/docs/png_docs/compare_sequence_to_draws.py.png)


```bash
    python run_search/use_python/compare_sequence_to_draws.py -g lotto --details

    Reading Path Record:    --> /lotto/historical_lotto_draw_results
            Game Records:   --> 1410 in powerball_history_20251001_1647_abea.json
            _______________________________________________________________________________________________

    Total Records Load: 1410
    =========================
    Games found: ['powerball']

    ===============================================================================================
    [PERF STATS] for      build_frequency_maps | completed in: 0m  0.28s (0.2752 sec)


    RAREST (catalog) for LOTTO → [17, 25, 28, 33, 3, 3]

    LOTTO • primary_numbers • PARTIAL ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

    0 results matched around [3, 3, 17, 25, 28, 33] sequence data.

    ===============================================================================================
    [PERF STATS] for                      main | completed in: 0m  0.29s (0.2907 sec)
```

```bash
    python run_search/use_python/compare_sequence_to_draws.py -g powerball --details

    Reading Path Record:    --> /lotto/historical_lotto_draw_results
            Game Records:   --> 1410 in powerball_history_20251001_1647_abea.json
            _______________________________________________________________________________________________

    Total Records Load: 1410
    =========================
    Games found: ['powerball']

    ===============================================================================================
    [PERF STATS] for      build_frequency_maps | completed in: 0m  0.31s (0.3098 sec)


    RAREST (catalog) for POWERBALL → [25, 63, 32, 1, 2]

    POWERBALL • primary_numbers • PARTIAL ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

    3 number match(es) → 2 draw(s):
    → 21, 25, 32, 63, 67   | Overlap: 25, 32, 63  | Date: Apr 21, 2021
    → 1, 5, 25, 63, 67     | Overlap: 1, 25, 63   | Date: Oct 16, 2019

    2 number match(es) → 63 draw(s):
    → 2, 18, 19, 25, 35    | Overlap: 2, 25       | Date: Jul 23, 2025
    → 1, 2, 3, 57, 59      | Overlap: 1, 2        | Date: Apr 30, 2025
    → 7, 25, 37, 39, 63    | Overlap: 25, 63      | Date: Apr 19, 2025
    → 2, 4, 16, 23, 63     | Overlap: 2, 63       | Date: Mar 8, 2025
    → 1, 23, 25, 28, 61    | Overlap: 1, 25       | Date: Dec 4, 2024
    → 21, 22, 25, 32, 38   | Overlap: 25, 32      | Date: Nov 16, 2024
    → 1, 25, 57, 62, 64    | Overlap: 1, 25       | Date: Oct 21, 2024
    → 25, 32, 43, 53, 66   | Overlap: 25, 32      | Date: Oct 9, 2024
    → 1, 2, 21, 37, 43     | Overlap: 1, 2        | Date: Oct 2, 2024
    → 1, 2, 15, 23, 28     | Overlap: 1, 2        | Date: Aug 19, 2024
    → 1, 2, 27, 30, 67     | Overlap: 1, 2        | Date: Feb 5, 2024

```
---
> - [generate_suggestions.py](/run_search/use_python/generate_suggestions.py)

```bash
    python run_search/use_python/generate_suggestions.py

    Data to be injected in frequency map:  ↓ 
        0 files:  ←  recent lottery draws:
        1 files:  ←  lottery draws history:
    2977 files:  ←  user data catalog:

    Building frequency map ... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

    ===============================================================================================
    [PERF STATS] for build_augmented_frequency_map | completed in: 0m  0.69s (0.6858 sec)

    Built scaled Frequency Map: detected game count: 6 of game types: ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

            Game Type: → LOTTO+ key: → PRIMARY:
            Suggested picks for upcoming game: → captured sequence: [17, 25, 28, 33, 3]

            [  PLAYER       ] index: 0  → 17 |freq:     1 | source: → MX.json       line:   15 ←  ref:
            [  PLAYER       ] index: 1  → 25 |freq:     1 | source: → גילי.json     line:    3 ←  ref:
            [  PLAYER       ] index: 2  → 28 |freq:     1 | source: → Nadezhda.json line:   21 ←  ref:
            [  PLAYER       ] index: 3  → 33 |freq:     1 | source: → Facundo.json  line:    9 ←  ref:
            [  PLAYER       ] index: 4  → 3  |freq:     1 | source: → Irmak.json    line:    3 ←  ref:
            | dropped ↑ duplicate:    → [3]
            _________________________________________________________________________________________________

            Game Type: → LUCKYDAY+ key: → PRIMARY:
            Suggested picks for upcoming game: → captured sequence: [21, 28, 29, 2, 35]

            [  PLAYER       ] index: 0  → 21 |freq:     1 | source: → Bandar Seri Begawan.json      line:   22 ←  ref:
            [  PLAYER       ] index: 1  → 28 |freq:     1 | source: → Шахриёр.json  line:    4 ←  ref:
            [  PLAYER       ] index: 2  → 29 |freq:     4 | source: → Шахриёр.json  line:    4 ←  ref:
            [  PLAYER       ] index: 3  → 2  |freq:     1 | source: → Yacouba.json  line:   22 ←  ref:
            [  PLAYER       ] index: 4  → 35 |freq:     1 | source: → پرنیا.json    line:    4 ←  ref:

            Game Type: → MEGAMILLION+ key: → PRIMARY:
            Suggested picks for upcoming game: → captured sequence: [28, 31, 32, 1, 4]

            [  PLAYER       ] index: 0  → 28 |freq:     1 | source: → Andrés.json   line:    1 ←  ref:
            [  PLAYER       ] index: 1  → 31 |freq:     1 | source: → Лена.json     line:   25 ←  ref:
            [  PLAYER       ] index: 2  → 32 |freq:     2 | source: → Жељко.json    line:    1 ←  ref:
            [  PLAYER       ] index: 3  → 1  |freq:     1 | source: → Gil.json      line:   13 ←  ref:
            [  PLAYER       ] index: 4  → 4  |freq:     1 | source: → Adwoa.json    line:    7 ←  ref:

            Game Type: → MEGAMILLION+ key: → MEGA:
            Suggested picks for upcoming game: → captured sequence: [11]

            [  PLAYER       ] index: 0  → 11 |freq:   478 | source: → Constanza.json        line:   19 ←  ref:

            Game Type: → PICK3+ key: → PRIMARY:
            Suggested picks for upcoming game: → captured sequence: [5, 8, 0]

            [  PLAYER       ] index: 0  → 5  |freq:    94 | source: → Tarawa.json   line:   11 ←  ref:
            [  PLAYER       ] index: 1  → 8  |freq:   333 | source: → نعمت.json     line:   17 ←  ref:
            [  PLAYER       ] index: 2  → 0  |freq:    62 | source: → Bank.json     line:   11 ←  ref:

            Game Type: → PICK4+ key: → PRIMARY:
            Suggested picks for upcoming game: → captured sequence: [4, 6, 8, 0]

            [  PLAYER       ] index: 0  → 4  |freq:    62 | source: → طلال.json     line:   12 ←  ref:
            [  PLAYER       ] index: 1  → 6  |freq:    14 | source: → Александра.json       line:   18 ←  ref:
            [  PLAYER       ] index: 2  → 8  |freq:    52 | source: → Vasco.json    line:    6 ←  ref:
            [  PLAYER       ] index: 3  → 0  |freq:   187 | source: → نعمت.json     line:   18 ←  ref:

            Game Type: → POWERBALL+ key: → PRIMARY:
            Suggested picks for upcoming game: → captured sequence: [61, 63, 65, 1, 2]

            [  PLAYER       ] index: 0  → 61 |freq:     1 | source: → أسرول.json    line:   20 ←  ref:
            [  PLAYER       ] index: 1  → 63 |freq:     1 | source: → Jack.json     line:    8 ←  ref:
            [  HISTORIC     ] index: 2  → 65 |freq:     4 | source: → powerball_history_20251001_1647_abea.json     line:  263 ←  ref:
            [  PLAYER       ] index: 3  → 1  |freq:     1 | source: → Stanisław.json        line:    2 ←  ref:
            [  PLAYER       ] index: 4  → 2  |freq:     1 | source: → Niamh.json    line:   20 ←  ref:

            Game Type: → POWERBALL+ key: → POWER:
            Suggested picks for upcoming game: → captured sequence: [30]

            [  HISTORIC     ] index: 0  → 30 |freq:     3 | source: → powerball_history_20251001_1647_abea.json     line: 1301 ←  ref:

    Frequency Map - Data Check:
    ↓  ↓  ↓  ↓  ↓  ↓ 
    powerball    →  keys: ['primary', 'power', 'primes_in_primary', 'primes_in_power']
    megamillion  →  keys: ['primary', 'primes_in_primary', 'mega', 'primes_in_mega']
    lotto        →  keys: ['primary', 'primes_in_primary']
    luckyday     →  keys: ['primary', 'primes_in_primary']
    pick3        →  keys: ['primary', 'primes_in_primary']
    pick4        →  keys: ['primary', 'primes_in_primary']

    ===============================================================================================
    [PERF STATS] for                      main | completed in: 0m  0.75s (0.7483 sec)
```
> - ![generate_suggestions](/docs/png_docs/generate_suggestions.py.png)
---

> - [frequency_maps.py](/run_search/use_python/frequency_maps.py)
```bash
    pytho3 run_search/use_python/frequency_maps.py
    ...
    →  processed 76100 records | 6 games * 16 sequences
    →  processed 76200 records | 6 games * 16 sequences
    
    GAME TYPE: MEGAMILLION ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

            Sequence: PRIMARY
            megamillion  • primary            idx 0 → count:   12714, unique:  63 | Top:        (64,954), (32,858), (65,789)  (28,1), (29,1), (57,1)              |  Rare: (28,1), (29,1), (57,1)
            megamillion  • primary            idx 1 → count:   12714, unique:  68 | Top:          (6,416), (7,400), (39,397)  (31,1), (28,4), (30,5)              |  Rare: (31,1), (28,4), (30,5)
            megamillion  • primary            idx 2 → count:   12714, unique:  69 | Top:        (46,390), (13,357), (48,356)  (32,2), (62,2), (65,3)              |  Rare: (32,2), (62,2), (65,3)
            megamillion  • primary            idx 3 → count:   12714, unique:  66 | Top:        (55,421), (23,417), (53,416)  (1,1), (2,1), (34,2)                |  Rare: (1,1), (2,1), (34,2)
            megamillion  • primary            idx 4 → count:   12714, unique:  59 | Top:        (31,889), (63,863), (62,791)  (4,1), (68,1), (5,2)                |  Rare: (4,1), (68,1), (5,2)

            Sequence: PRIMES_IN_PRIMARY
            megamillion  • primes_in_primary  idx 0 → count:   10285, unique:  19 | Top:          (2,908), (3,812), (67,790)  (31,278), (61,306), (29,324)        |  Rare: (31,278), (61,306), (29,324)
            megamillion  • primes_in_primary  idx 1 → count:    5306, unique:  19 | Top:        (29,413), (61,403), (23,398)  (2,4), (3,75), (67,84)              |  Rare: (2,4), (3,75), (67,84)
            megamillion  • primes_in_primary  idx 2 → count:    1523, unique:  18 | Top:        (29,196), (31,191), (61,186)  (2,1), (67,1), (37,10)              |  Rare: (2,1), (67,1), (37,10)
            megamillion  • primes_in_primary  idx 3 → count:     199, unique:  13 | Top:           (31,42), (29,34), (61,28)  (41,2), (43,2), (11,3)              |  Rare: (41,2), (43,2), (11,3)
            megamillion  • primes_in_primary  idx 4 → count:      12, unique:   5 | Top:              (31,5), (29,2), (53,2)  (23,1), (29,2), (53,2)              |  Rare: (23,1), (29,2), (53,2)

            Sequence: MEGA
            megamillion  • mega               idx 0 → count:   12714, unique:  25 | Top:         (3,553), (18,546), (22,528)  (11,478), (12,481), (13,485)        |  Rare: (11,478), (12,481), (13,485)

            Sequence: PRIMES_IN_MEGA
            megamillion  • primes_in_mega     idx 0 → count:    4558, unique:   9 | Top:         (3,553), (23,519), (19,510)  (11,478), (13,485), (17,501)        |  Rare: (11,478), (13,485), (17,501)
    
    ... wrote debug stats to:  →   /lotto/_dev_debug/vertical_freq_summary.json
    
    Mapped Frequency Summary ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

            GAME TYPE: →  MEGAMILLION | Sequence Key: →  PRIMARY

            Index: 0  →top:        (64,954), (32,858), (65,789) | total   12714
            Index: 1  →top:          (6,416), (7,400), (39,397) | total   12714
            Index: 2  →top:        (46,390), (13,357), (48,356) | total   12714
            Index: 3  →top:        (55,421), (23,417), (53,416) | total   12714
            Index: 4  →top:        (31,889), (63,863), (62,791) | total   12714
            _________________________________________________________________

            GAME TYPE: →  MEGAMILLION | Sequence Key: →  PRIMES_IN_PRIMARY

            Index: 0  →top:          (2,908), (3,812), (67,790) | total   10285
            Index: 1  →top:        (29,413), (61,403), (23,398) | total    5306
            Index: 2  →top:        (29,196), (31,191), (61,186) | total    1523
            Index: 3  →top:           (31,42), (29,34), (61,28) | total     199
            Index: 4  →top:              (31,5), (29,2), (53,2) | total      12
            _________________________________________________________________

            GAME TYPE: →  MEGAMILLION | Sequence Key: →  MEGA

            Index: 0  →top:         (3,553), (18,546), (22,528) | total   12714
            _________________________________________________________________

            GAME TYPE: →  MEGAMILLION | Sequence Key: →  PRIMES_IN_MEGA

            Index: 0  →top:         (3,553), (23,519), (19,510) | total    4558

    ===============================================================================================
    [PERF STATS] for                      main | completed in: 0m  0.61s (0.6139 sec)
```
> - ![requency_maps](/docs/png_docs/frequency_map.py.png)
---

> - [use_rarest_sequence.py](/run_search/use_python/use_rarest_sequence.py)
```bash
    root@30dfcf682933:/lotto# python run_search/use_python/use_rarest_sequence.py 
    ===============================================================================================
    [PERF STATS] for      build_frequency_maps | completed in: 0m  0.31s (0.3102 sec)

                    idx 0 → pick    25  (freq=1    ): candidates: [(25, 1), (28, 1), (30, 1), (61, 1), (22, 2)]
                    idx 1 → pick    63  (freq=1    ): candidates: [(63, 1), (30, 4), (28, 6), (61, 6), (29, 7)]
                    idx 2 → pick    32  (freq=2    ): candidates: [(32, 2), (62, 3), (65, 3), (31, 4), (63, 4)]
                    idx 3 → pick    1   (freq=1    ): candidates: [(1, 1), (33, 1), (34, 2), (67, 3), (66, 4)]
                    idx 4 → pick    2   (freq=1    ): candidates: [(2, 1), (37, 1), (39, 1), (5, 2), (36, 2)]

    POWERBALL       → rarest sequence: [25, 63, 32, 1, 2] in Key: PRIMARY
                    idx 0 → pick    31  (freq=255  ): candidates: [(31, 255), (29, 269), (61, 289), (23, 362), (59, 365)]
                    idx 1 → pick    2   (freq=1    ): candidates: [(2, 1), (3, 63), (67, 84), (5, 164), (37, 173)]
                    idx 2 → pick    3   (freq=1    ): candidates: [(3, 1), (67, 1), (5, 10), (37, 13), (7, 15)]
                    idx 3 → pick    11  (freq=1    ): candidates: [(11, 1), (41, 1), (43, 1), (7, 2), (17, 7)]
                    idx 4 → pick    11  (freq=1    ): candidates: [(11, 1), (17, 1), (29, 1), (53, 1), (59, 1)]

    POWERBALL       → rarest sequence: [31, 2, 3, 11, 11] in Key: PRIMES_IN_PRIMARY
                    idx 0 → pick    13  (freq=450  ): candidates: [(13, 450), (11, 454), (24, 463), (21, 464), (17, 467)]

    POWERBALL       → rarest sequence: [13] in Key: POWER
                    idx 0 → pick    13  (freq=450  ): candidates: [(13, 450), (11, 454), (17, 467), (19, 477), (7, 488)]

    POWERBALL       → rarest sequence: [13] in Key: PRIMES_IN_POWER
                    idx 0 → pick    28  (freq=1    ): candidates: [(28, 1), (29, 1), (57, 1), (61, 1), (23, 2)]
                    idx 1 → pick    31  (freq=1    ): candidates: [(31, 1), (28, 4), (30, 5), (57, 6), (61, 7)]
                    idx 2 → pick    32  (freq=2    ): candidates: [(32, 2), (62, 2), (65, 3), (64, 4), (31, 6)]
                    idx 3 → pick    1   (freq=1    ): candidates: [(1, 1), (2, 1), (34, 2), (3, 5), (35, 5)]
                    idx 4 → pick    4   (freq=1    ): candidates: [(4, 1), (68, 1), (5, 2), (36, 2), (69, 2)]

    MEGAMILLION     → rarest sequence: [28, 31, 32, 1, 4] in Key: PRIMARY
                    idx 0 → pick    31  (freq=278  ): candidates: [(31, 278), (61, 306), (29, 324), (59, 333), (23, 363)]
                    idx 1 → pick    2   (freq=4    ): candidates: [(2, 4), (3, 75), (67, 84), (5, 149), (37, 178)]
                    idx 2 → pick    2   (freq=1    ): candidates: [(2, 1), (67, 1), (37, 10), (7, 12), (5, 13)]
                    idx 3 → pick    41  (freq=2    ): candidates: [(41, 2), (43, 2), (11, 3), (13, 3), (47, 6)]
                    idx 4 → pick    23  (freq=1    ): candidates: [(23, 1), (29, 2), (53, 2), (59, 2), (31, 5)]

    MEGAMILLION     → rarest sequence: [31, 2, 2, 41, 23] in Key: PRIMES_IN_PRIMARY
                    idx 0 → pick    11  (freq=478  ): candidates: [(11, 478), (12, 481), (13, 485), (21, 491), (10, 497)]

    MEGAMILLION     → rarest sequence: [11] in Key: MEGA
                    idx 0 → pick    11  (freq=478  ): candidates: [(11, 478), (13, 485), (17, 501), (2, 502), (5, 504)]

    MEGAMILLION     → rarest sequence: [11] in Key: PRIMES_IN_MEGA
                    idx 0 → pick    17  (freq=1    ): candidates: [(17, 1), (23, 1), (49, 2), (18, 3), (48, 4)]
                    idx 1 → pick    25  (freq=1    ): candidates: [(25, 1), (24, 2), (22, 5), (21, 6), (19, 10)]
                    idx 2 → pick    28  (freq=1    ): candidates: [(28, 1), (27, 4), (26, 10), (1, 14), (25, 16)]
                    idx 3 → pick    33  (freq=1    ): candidates: [(33, 1), (1, 2), (2, 2), (34, 3), (29, 11)]
                    idx 4 → pick    3   (freq=1    ): candidates: [(3, 1), (4, 1), (34, 1), (36, 2), (37, 2)]
                    idx 5 → pick    3   (freq=1    ): candidates: [(3, 1), (34, 1), (37, 1), (38, 1), (8, 3)]

    LOTTO           → rarest sequence: [17, 25, 28, 33, 3, 3] in Key: PRIMARY
                    idx 0 → pick    31  (freq=271  ): candidates: [(31, 271), (29, 302), (23, 329), (19, 396), (17, 433)]
                    idx 1 → pick    2   (freq=2    ): candidates: [(2, 2), (3, 156), (37, 314), (5, 335), (7, 515)]
                    idx 2 → pick    3   (freq=1    ): candidates: [(3, 1), (37, 13), (5, 27), (7, 63), (41, 102)]
                    idx 3 → pick    7   (freq=1    ): candidates: [(7, 1), (41, 12), (11, 18), (43, 26), (13, 39)]
                    idx 4 → pick    13  (freq=1    ): candidates: [(13, 1), (11, 2), (47, 2), (17, 3), (43, 3)]
                    idx 5 → pick    13  (freq=1    ): candidates: [(13, 1), (23, 1), (29, 2), (31, 2)]

    LOTTO           → rarest sequence: [31, 2, 3, 7, 13, 13] in Key: PRIMES_IN_PRIMARY

    ===============================================================================================
    [PERF STATS] for                      main | completed in: 0m  0.34s (0.3368 sec)
    root@30dfcf682933:/lotto# 
```
> - ![use_rarest_sequence](/docs/png_docs/use_rarest_sequence.py.png)

---

## Features:
* Debug and Trace Capabilities:
    - Runtime tracing:      - Step-by-step execution visibility:
    - Data provenance:      - Full traceability from suggestion back to source records:
    - Progress tracking:    - Real-time processing updates for larger datasets:

* Visual Output:
    - Color-coded results:  - for visual comprehension:
    - Grouped displays:     - Logical organization of match results:
    - Hierarchical views:   - Drill-down capability from summary to details:

* Performance Optimizations:
    - Generator-based loading:  - To manage RAM efficientcy if large file processing is true:
    - Progress throttling:      - Balanced data stream to reduce performance impact:
    - Selective debugging:      - more of a control over verbosity:

## Comparison with Go Version:
* Python Advantages:
    - Interactive use / exploration: - Immediate data retunr and its visualization:
    - Data Matching:                 - Multiple comparison strategies in real-time:
    - Output:                        - Colorized, formatted terminal displays:
    - Prototyping:                   - Easier algorithm experimentation and research:
---
* Go Advantages:
    - Robust:                       - Clear typing and error handling:
    - Performance:                  - Better memory management if large datasets:
    - Structured output:            - Consistent .json export formats:
    - CLI:                          - cli interface makes it simpler to use:

* Positional Frequency Analysis:
    - The key takeaway in the Python engine is that, ___treating each position in a lottery sequence as an independent distribution___: 
    - Which reveals that:
        - Some numbers appear more frequently in certain positions:
        - Positional `hot` and `cold` numbers can differ from overall frequencies:
        - Game-specific patterns may emerge in position preferences:

* Data Stream Tracking:
    - Every suggested number carries metadata about its origin:
    - Source file and line number:
    - Data source type (`user`, `recent`, `historical`)
    - Frequency context within its position:

* Multi-strategy Comparison:
- Supports both conservative (rarest numbers) and balanced (mixed frequency) approaches, allowing users to compare different strategic philosophies:
---

### This Python engine was written to help with the interactive, exploratory interface that data analysts need for developing and testing sequences and strategies _`in this case`_ - using organic data produced by state lottery games and its rules: <br> While the [Go version](/docs/readme_docs/statistics_go_based_tool.md) provides the production-grade batch processing for regular use at scale:

