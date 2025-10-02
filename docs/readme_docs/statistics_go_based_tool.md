# Statistics Simulator:

## GO based data analytics tool overview: 
- This Go based simulator was designed to analyze historical lottery data and generate strategic gameplay suggestions:
- It processes both catalog-style records (user selections) and historical draw data to provide frequency analysis, unique sequence tracking, and data-driven number suggestions:
- This [tool](/run_search/use_go/) represents some ideas or an attempt on how to: 
    - create sophisticated approach to lottery data analysis combining statistical rigor/accuracy with practical usability for both casual players and or serious analysts or algo based data processing:

## Project Structure:
```text
    ├── cmd/analyze/main.go          # Application entry point
    ├── go.mod                       # Go module dependencies
    ├── go.sum                       # Dependency checksums
    └── internal/
        ├── analyzer/                # Core analysis logic
        │   ├── constants.go         # Game configuration
        │   ├── frequency.go         # Frequency counting
        │   ├── loader.go            # Data loading and parsing
        │   ├── suggest.go           # Suggestion generation
        │   ├── time_utils.go        # Time parsing utilities
        │   └── unique.go            # Unique sequence tracking
        ├── cli/root.go              # Command-line interface
        └── output/writer.go         # JSON export functionality
```
---
### Core Components:
***__Command Line Interface__***:
* [root.go](/run_search/use_go/internal/cli/root.go) - provides command-line interface options for configuring stats with analysis:
    * ***Helps With***:
        - game selections (e.g. megamillion, powerball, lotto):
        - multiple output formats (console, .json, .html):
        - suggestion strategies (rarest, mixed):
        - filtering options (avoid recent draws by ***__x__*** count):
        - colorized terminal output:
    - ___Necessity___: 
        - Without this CLI layer, users would need to interact directly with Go code:
        - The CLI abstracts complexity and provides intuitive configuration options for non-technical users:
---

2. ***___Data Loading System___***:
    * [loader.go](/run_search/use_go/internal/analyzer/loader.go) - handles multiple data formats and sources as an unified interface for lottery data processing:
    * ***__Supported Formats:__***:
        - Catalog Format: User selection records with timestamps
        - Historical Format: Official draw results with draw dates
    * ***Helps With***:
        - `FindCatalogJSON()`: Recursively discovers .json files in repo fs structure:
        - `LoadSequences()`: Parses and normalizes both data formats into unified sequence objects:
        - `normalizeGameName()`: Standardizes game name variations:
    - ___Necessity___:
        - Lottery data comes from multiple sources with different formats: 
        - This system ensures consistent processing regardless of data origin, making this tool adaptable to various data collection methods:

---
3. ***___Frequency Analysis___***:
    * [frequency.go](/run_search/use_go/internal/analyzer/frequency.go) - calculates how often each number appears in historical data, providing the foundation for statistical analysis:
    * __***Data Structure***__:
        ```go
            type GameFrequencies struct {
                Primary      map[int]int            // Count of primary numbers
                Bonus        map[int]int            // Count of bonus numbers
                TotalPrimary int                    // Total primary draws
                TotalBonus   int                    // Total bonus draws
                FileOrigins  map[int]map[string]int // Which files contributed numbers
                BonusOrigins map[int]map[string]int // Bonus number file origins
            }
        ```
    - ___Necessity___:
        - Frequency analysis identifies ***__`hot`__*** and ***__`cold`__*** number values, enabling data-driven strategies rather than random selection: 
        - and the file origin tracking helps understand data distribution across sources:

---
4. ***___Suggestion Engine___***:
    * [suggest.go](/run_search/use_go/internal/analyzer/suggest.go) - generates lottery number suggestions based on statistical analysis and configurable strategies:
    * ***__Strategies__***:
        - ___rarest___: - Prioritizes least frequently drawn numbers:
        - ___mixed___: - Alternates between rare and moderately frequent numbers:
    * ***___Advanced Features___***:
        - Avoids recently drawn numbers (configurable window):
        - Ensures unique combinations not in historical data:
        - Game-specific rules (bonus numbers for certain games):
    - ___Necessity___:
        - Manual number selection suffers from cognitive bias, resulting in constant repetition of the same numbers - ***leading `us` to pick the `same numbers` repeatedly***: 
        - The engine offers data-driven, impartial suggestions designed to achieve two goals: ___`refine`___ strategic moves for the next play and ___`counteract`___ the cognitive biases our brain is constantly using to trick us:

---
5. ***___Unique Sequence Tracking___***: 
    * [unique.go](/run_search/use_go/internal/analyzer/unique.go) - identifies and catalogs all unique number combinations across dataset:
    * ***Helps With***:
        - Tracks first/last appearance dates:
        - Counts occurrence frequency:
        - Maps sequences to source files for data origins:
        - Chronological sorting:
    - ___Necessity___:
        - Understanding sequence uniqueness helps avoid commonly played combinations and identifies patterns in draw history:

---
6. ***___Configuration System___***:
    * [constants.go](/run_search/use_go/internal/analyzer/constants.go) - centralizes game-specific rules and constraints:
    - Game Limits:
        - ___Mega Millions___: 5 primary + 1 bonus:
        - ___Powerball___: 5 primary + 1 bonus:
        - ___Lotto___: 6 primary numbers:
        - ___Lucky Day___: 5 primary numbers:
        - ___Pick 3___: 3 primary numbers:
        - ___Pick 4___: 4 primary numbers:
    - ___Necessity___:
        - Different lottery games have different rules. Centralizing these constraints ensures consistent processing and prevents invalid combinations:

## Call Examples:  - [/cmd/analyze/main.go](/run_search/use_go/cmd/analyze/main.go)

___--help___

```bash
    cd run_search/use_go
    go run ./cmd/analyze/main.go --help
    Analyze lottery catalog results and generate gameplay suggestions

    Usage:
    analyze [flags]

    Flags:
        --avoid-latest int      Avoid numbers seen in last K draws
        --catalog-root string   Root directory to search for catalog JSON files (default ".")
        --export-dir string     Directory to write analysis output (default "analytics")
        --export-json string    Output JSON file name (default: timestamped)
        --games strings         Comma-separated list of games to analyze (default: all)
    -h, --help                  help for analyze
        --html                  Also export HTML report
        --no-color              Disable colored terminal output
        --print-all             Print all results (frequencies, uniques, suggestions)
        --print-freq            Print frequency tables with percentages
        --print-suggestions     Print suggestions
        --print-uniques         Print unique sequences
        --strategy string       Suggestion strategy: rarest | mixed (default "rarest")
        --suggest int           Number of suggested sequences per game (default 5)

```
---
___--games=megamillion,powerball --print-suggestions___
```bash
    cd run_search/use_go
    go run ./cmd/analyze/main.go --games=megamillion,powerball --print-suggestions
    Exporting results to: /lottery_stats_simulator/analytics/analysis_20251001_212644.json
    Loaded sequences: 2656
    Frequency map built for: 2 game(s)
    Found unique sequence entries: 2656

    [SUGGESTIONS]
    - POWERBALL → [13   26   60   65   68  ] +31 (rarest)
    - POWERBALL → [13   26   46   60   68  ] +31 (rarest)
    - POWERBALL → [13   26   46   66   68  ] +31 (rarest)
    - POWERBALL → [26   46   49   66   68  ] +31 (rarest)
    - POWERBALL → [46   49   51   66   68  ] +31 (rarest)
    - MEGAMILLION → [71   72   73   74   75  ] +23 (rarest)
    - MEGAMILLION → [67   72   73   74   75  ] +23 (rarest)
    - MEGAMILLION → [65   67   73   74   75  ] +23 (rarest)
    - MEGAMILLION → [36   65   67   73   74  ] +23 (rarest)
    - MEGAMILLION → [36   55   65   67   73  ] +23 (rarest)
    Generated: 5 suggestions for powerball
    Generated: 5 suggestions for megamillion
```
---
```json
 ──────┬─────────────────────────────────────────────────────
       │ File: ../../analytics/analysis_20251001_210539.json
 ──────┼─────────────────────────────────────────────────────
   1   │ {
   2   │   "source_path": "/lottery_stats_simulator/",
   3   │   "suggestions": [
   4   │     {
   5   │       "game": "megamillion",
   6   │       "source": "rarest",
   7   │       "index": 0,
   8   │       "values": "[71,72,73,74,75]"
   9   │     },
  10   │     {
  11   │       "game": "megamillion",
  12   │       "source": "rarest",
  13   │       "index": 1,
  14   │       "values": "[67,72,73,74,75]"
  15   │     },
  16   │     {
  17   │       "game": "megamillion",
  18   │       "source": "rarest",
  19   │       "index": 2,
  20   │       "values": "[65,67,73,74,75]"
  21   │     },
  22   │     {
  23   │       "game": "megamillion",
  24   │       "source": "rarest",
  25   │       "index": 3,
  26   │       "values": "[36,65,67,73,74]"
  27   │     },
  28   │     {
  29   │       "game": "megamillion",
  30   │       "source": "rarest",
  31   │       "index": 4,
  32   │       "values": "[36,55,65,67,73]"
  33   │     },
  34   │     {
  35   │       "game": "powerball",
  36   │       "source": "rarest",
  37   │       "index": 5,
  38   │       "values": "[13,26,60,65,68]"
  39   │     },
  40   │     {
```
---
___--games=megamillion,powerball,lotto --strategy mixed --print-suggestions___
```bash
cd run_search/use_go
go run ./cmd/analyze/main.go --games=megamillion,powerball,lotto --strategy mixed --print-suggestions
Exporting results to: lottery_stats_simulator/analytics/analysis_20251001_213802.json
Loaded sequences: 4487
Frequency map built for: 3 game(s)
Found unique sequence entries: 4487

[SUGGESTIONS]
  - MEGAMILLION → [15   45   71   72   75  ] +23 (mixed)
  - MEGAMILLION → [15   27   72   74   75  ] +21 (mixed)
  - MEGAMILLION → [15   27   73   74   75  ] +16 (mixed)
  - MEGAMILLION → [27   39   67   73   74  ] +20 (mixed)
  - MEGAMILLION → [27   39   65   67   73  ] +17 (mixed)
  - POWERBALL → [9    13   30   60   65  ] +31 (mixed)
  - POWERBALL → [13   26   30   60   63  ] +32 (mixed)
  - POWERBALL → [13   26   30   63   68  ] +30 (mixed)
  - POWERBALL → [1    26   46   63   68  ] +34 (mixed)
  - POWERBALL → [1    46   63   66   68  ] +28 (mixed)
  - LOTTO → [9    22   27   40   51   52  ] +0  (mixed)
  - LOTTO → [9    22   27   35   40   51  ] +0  (mixed)
  - LOTTO → [5    9    22   35   40   42  ] +0  (mixed)
  - LOTTO → [1    5    22   35   40   42  ] +0  (mixed)
  - LOTTO → [1    5    22   42   48   50  ] +0  (mixed)
Generated: 5 suggestions for megamillion
Generated: 5 suggestions for powerball
Generated: 5 suggestions for lotto
```
---
___--games=megamillion --print-uniques --print-suggestions --suggest 30___
```bash
cd run_search/use_go
go run ./cmd/analyze/main.go --games=megamillion --print-uniques --print-suggestions --suggest 30
Exporting results to: /lottery_stats_simulator/analytics/analysis_20251001_214444.json
Loaded sequences: 1221
Frequency map built for: 1 game(s)
Found unique sequence entries: 1221

[UNIQUES] Total unique sequences: 1221

[SUGGESTIONS]
  - MEGAMILLION → [71   72   73   74   75  ] +23 (rarest)
  - MEGAMILLION → [67   72   73   74   75  ] +23 (rarest)
  - MEGAMILLION → [65   67   73   74   75  ] +23 (rarest)
  - MEGAMILLION → [36   65   67   73   74  ] +23 (rarest)
  - MEGAMILLION → [36   55   65   67   73  ] +23 (rarest)
  - MEGAMILLION → [23   36   55   65   67  ] +23 (rarest)
  - MEGAMILLION → [23   36   55   60   65  ] +23 (rarest)
  - MEGAMILLION → [23   36   55   60   63  ] +23 (rarest)
  - MEGAMILLION → [5    23   55   60   63  ] +23 (rarest)
  - MEGAMILLION → [5    23   32   60   63  ] +23 (rarest)
  - MEGAMILLION → [5    9    32   60   63  ] +23 (rarest)
  - MEGAMILLION → [5    9    32   47   63  ] +23 (rarest)
  - MEGAMILLION → [1    5    9    32   47  ] +23 (rarest)
  - MEGAMILLION → [1    9    32   47   51  ] +23 (rarest)
  - MEGAMILLION → [1    9    12   47   51  ] +23 (rarest)
  - MEGAMILLION → [1    12   34   47   51  ] +23 (rarest)
  - MEGAMILLION → [1    12   34   49   51  ] +23 (rarest)
  - MEGAMILLION → [12   34   49   50   51  ] +23 (rarest)
  - MEGAMILLION → [12   34   49   50   70  ] +23 (rarest)
  - MEGAMILLION → [13   34   49   50   70  ] +23 (rarest)
  - MEGAMILLION → [13   21   49   50   70  ] +23 (rarest)
  - MEGAMILLION → [13   21   50   54   70  ] +23 (rarest)
  - MEGAMILLION → [13   21   54   57   70  ] +23 (rarest)
  - MEGAMILLION → [13   21   54   57   61  ] +23 (rarest)
  - MEGAMILLION → [21   48   54   57   61  ] +23 (rarest)
  - MEGAMILLION → [48   52   54   57   61  ] +23 (rarest)
  - MEGAMILLION → [48   52   57   59   61  ] +23 (rarest)
  - MEGAMILLION → [4    48   52   59   61  ] +23 (rarest)
  - MEGAMILLION → [4    40   48   52   59  ] +23 (rarest)
  - MEGAMILLION → [4    40   52   59   68  ] +23 (rarest)
Generated: 30 suggestions for megamillion
```
---
### Design Philosophy:
1. ___Data Agnosticism:___ - System processes multiple data formats without requiring data transformation, making it adaptable to various data collection methodologies:
2. ___Statistical Foundation:___ - All suggestions are based on actual historical data analysis rather than random generation or ay othre random superstition noise:
3. ___Configurable Strategies___ - Multiple suggestion strategies accommodate different playing philosophies while maintaining statistical validity:
4. ___Comprehensive Tracking___ - The system maintains detailed provenance information, allowing users to understand where suggestions originate and how they're calculated:

### Technical Implementation:
* Data Flow:
    - ___Discovery___: - Find .json files in repository structure:
    - ___Loading___: Parse and normalize into unified Sequence format:
    - ___Analysis___: Calculate frequencies and unique sequences:
    - ___Generation___: Create suggestions based on strategy:
    - ___Output___: Show results and export to .json:

* Error Handling:
    - Graceful handling of malformed data files:
    - Ok error messages for configuration issues:
    - Re-init back behaviors for missing data:

* Performance Considerations:
    - Efficient memory usage for large datasets:
    - Optimized sorting and searching algorithms:
    - Streaming output for large result sets:

---