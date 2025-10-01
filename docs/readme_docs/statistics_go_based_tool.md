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
    - ___Why do it | Necessity___: 
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
    - ___Why do it | Necessity___:
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
    - ___Why do it | Necessity___:
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
    - ___Why do it | Necessity___:
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
    - ___Why do it | Necessity___:
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
    - ___Why do it | Necessity___:
        - Different lottery games have different rules. Centralizing these constraints ensures consistent processing and prevents invalid combinations:

    - Example:
        ```bash
        ./analyze --games=megamillion,powerball --print-all
        Strategic Suggestions
        ```
        ```bash
        ./analyze --games=lotto --suggest=10 --strategy=mixed --avoid-latest=5
        Export Results
        ```
        ```bash
        ./analyze --games=powerball --export-dir=reports --export-json=analysis.json
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