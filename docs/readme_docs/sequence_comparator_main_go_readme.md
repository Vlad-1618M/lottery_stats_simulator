# Lotto Sequence Comparator (Go)

### A tool for comparing data int sequence using lottery number selections stored in bulk JSON catalogs. <br> Designed to extract an *exact* and *partial* matches, exports HTML report:
---
## Features:
>- Compares:<br>
    - `MegaMillions`:&nbsp;&nbsp;&nbsp;- ***multi-state*** lottery game:<br>
    - `Powerball`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - ***multi-state*** lottery game:<br>
    - `Lucky-Day`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - ***IL State*** lottery game:<br>
    - `Lotto`: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - ***IL State*** lottery game:<br>
    - `Pick3`: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - ***IL State*** lottery game:<br>
    - `Pick4`: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - ***IL State*** lottery game:<br><br>
>- Allows:<br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `match` all numbers or `ignore` bonus (***`Mega/Power`***) using args:<br><br>
>- Supports:<br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `concurrency` for handling high data count:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `colorized` cli unicode and `rtl` vs `ltr` reads plus cleaned oputput columns: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `Multilingual` filenames works with all scripts/locales: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `HTML` reports args based auto-opens in browser: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; run time `stats` & `benchmarks`:<br>
---
### Setup:
>- Prereqs:<br>
>- Go 1.18+ https://go.dev/dl <br>
>- Test Data in `catalog/` folder (as `.json` files per spec below) <br><br>

#### If new clone:
```bash
    go mod tidy   # .... download deps | run from repo root (e.g) --> lotto_simulator/ 
    go run src_for_go/main.go --help # .... see cli args / flags:
```
>- Command-Line Flags: <br>
```bash
go run src_for_go/main.go --games=powerball --depth=6
go run src_for_go/main.go --games=megamillion --depth=5 --drop-mega
go run src_for_go/main.go --games=powerball,megamillion --depth=5 --drop-mega --drop-power
go run src_for_go/main.go --games=lotto --depth=6
go run src_for_go/main.go --games=powerball --depth=6 --html --open-html
go run src_for_go/main.go --summary-only
```
``` txt
| Flag             | Type   | Default               | Description                                                                  |
| ---------------- | ------ | --------------------- | ---------------------------------------------------------------------------- |
| `--games`        | string | powerball,megamillion | Comma-separated games: powerball, megamillion, lotto, luckyday, pick3, pick4 |
| `--depth`        | int    | 5                     | Number of primary numbers to match (max for game)                            |
| `--drop-mega`    | bool   | false                 | Ignore Mega number in MegaMillions                                           |
| `--drop-power`   | bool   | false                 | Ignore Power number in Powerball                                             |
| `--force-mega`   | bool   | false                 | Require bonus (Mega/Power) match for exact                                   |
| `--include-mega` | bool   | false                 | Include bonus in pool for partial/depth matches                              |
| `--html`         | bool   | false                 | Generate HTML report                                                         |
| `--open-html`    | bool   | false                 | (With `--html`) open report in browser                                       |
| `--summary-only` | bool   | false                 | Print only summary, skip per-match lines                                     |
```

### NOTEs on Test Data & Data Structure:
>- The [python code](../src/quickPick.py) will generate enough fresh data: see [python src](../src) for more info:
>- The [Data Sets](../July-2025/catalog/) are in `catalog` path under each of its parent ( tagged by the e.g [timestampt](../July-2025/)) <br>
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
>- Each json record should be a list of records: for example: <br>
```json
[
    {
        "timestamp": "2025-07-29T11:04:59.509028",
        "game": "megamillion",
        "selection": {
            "primary": [64,1,69,41,29],
            "primes_in_primary": [41,29],
            "mega": [2],
            "primes_in_mega": [2]
        }
    },
    {
        "timestamp": "2025-07-29T11:04:59.510453",
        "game": "powerball",
        "selection": {
            "primary": [36,16,50,54,26],
            "primes_in_primary": [],
            "power": [25],
            "primes_in_power": []
        }
    },
    {
        "timestamp": "2025-07-29T11:04:59.512705",
        "game": "lotto",
        "selection": {
            "primary": [34,37,40,41,26,31],
            "primes_in_primary": [37,41,31]
        }
    },
    {
        "timestamp": "2025-07-29T11:04:59.515696",
        "game": "luckyday",
        "selection": {
            "primary": [4,41,13,15,27],
            "primes_in_primary": [41,13]
        }
    },
    {
        "timestamp": "2025-07-29T11:04:59.520478",
        "game": "pick3",
        "selection": {
            "primary": [0,1,7],
            "primes_in_primary": [7]
        }
    },
    {
        "timestamp": "2025-07-29T11:04:59.523302",
        "game": "pick4",
        "selection": {
            "primary": [0,2,5,7],
            "primes_in_primary": [2,5,7]
        }
    },
```
---

- Output Example: <br>
```bash
go run src_for_go/main.go --games=powerball,megamillion,lotto,luckyday --depth=6
```
![](../docs/go_call_mixed_search.png)
---
- Output Example: <br>
```bash
go run src_for_go/main.go --games=powerball --depth=6
go run src_for_go/main.go --games=powerball --depth=6 --drop-power
go run src_for_go/main.go --games=megamillion --depth=5 --drop-mega
```
![](../docs/go_call_single_runs.png)

- Output Example HTML Report:
```bash
go run src_for_go/main.go --games=megamillion,powerball,lotto --drop-mega --html --open-html
```
![](../docs/go_call_html_flag.png)

- If `--open-html` is passed, report will open in sys default browser | unless headless (`e`.`g` `docker` or cloud `linux` instance: <br>

![](../docs/go_call_html_view.png)

***
# GO Functions: | Code Walkthrough:
>- main()<br>
>- Entrypoint. 
>- Parses CLI flags, validates arguments, loads all JSONs, collects all Sequence entries, runs comparison, prints summary, optionally writes and opens HTML.

`findCatalogJSON()`:
Adds the path to any file that contains /catalog/ and ends with .json.

Returns a slice of string paths.
>- Purpose: - Recursively scans the current directory for all JSON files under any /catalog/ subdirectory and returns their file paths.
>- Logic: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `filepath.Walk`, appends path if `/catalog/` in path and ends with `.json` <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Walks the file tree starting at `cwd`: <br> 
```go
func findCatalogJSON() ([]string, error) {
	var paths []string
	err := filepath.Walk(".", func(path string, info os.FileInfo, err error) error {
		if strings.Contains(path, "/catalog/") && strings.HasSuffix(path, ".json") {
			paths = append(paths, path)
		}
		return nil
	})
	return paths, err
}
```

### func `loadSequences(path string, ch, wg, selectedGames)`:
>- Purpose: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Reads a JSON file, extracts all valid lottery selections for selected game types, and writes them as Sequence structs to a channel (for concurrent loading): 
>- Logic: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Reads the file content: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Parses the content as a list of Record: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; For each record matching the selected games: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Extracts the sorted primary numbers and bonus (Mega or Power) if present: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Appends a Sequence to the output slice: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Sends the results on a channel: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; For each record: if game is wanted, extracts & sorts primary, sets bonus (Mega/Power), pushes Sequence: <br>
```go
func loadSequences(path string, ch chan<- []Sequence, wg *sync.WaitGroup, selectedGames map[string]bool) {
	defer wg.Done()

	file, err := os.ReadFile(path)
	if err != nil {
		fmt.Printf("[ERROR] Reading %s: %v\n", path, err)
		return
	}
	var records []Record
	if err := json.Unmarshal(file, &records); err != nil {
		fmt.Printf("[ERROR] Parsing %s: %v\n", path, err)
		return
	}
	filename := filepath.Base(path)
	var result []Sequence

	for _, rec := range records {
		if !selectedGames[rec.Game] {
			continue
		}
		primary := append([]int{}, rec.Selection.Primary...)
		sort.Ints(primary)
		var bonus int
		switch rec.Game {
		case "megamillion":
			if len(rec.Selection.Mega) == 1 {
				bonus = rec.Selection.Mega[0]
			}
		case "powerball":
			if len(rec.Selection.Power) == 1 {
				bonus = rec.Selection.Power[0]
			}
		}
		result = append(result, Sequence{
			Game:     rec.Game,
			Primary:  primary,
			Bonus:    bonus,
			Filename: filename,
		})
	}
	ch <- result
}
```
### func `compareSequences(all, gameFlags, ...)`
>- Purpose: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Compares every pair of Sequence records to identify exact and partial matches according to game-specific logic and CLI flags: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Gathers all match statistics and timing info:<br>
>- Logic: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Loops over all unique pairs: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Skips pairs not from the same game: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Applies the matching logic (drop bonus, require bonus, include bonus, or full set): <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Increments counters and records match details for display: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; If should be counted, prints result (with color/columns) and adds to matchesList: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Benchmarks time; returns total/partial/exact stats, plus time taken: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Returns counts and duration: <br>
```go
func compareSequences(allSequences []Sequence, gameFlags map[string]int, matchDepth int,
	dropMega, dropPower, forceMega, includeMega, summaryOnly bool,) (exactCount, partialCount, total int, matches []MatchEntry, hours, minutes, seconds, millis int,) {
	total = len(allSequences)
	start := time.Now()
	exactCount, partialCount = 0, 0
	var matchesList []MatchEntry

	for idxA := 0; idxA < len(allSequences); idxA++ {
		sequenceA := allSequences[idxA]
		for idxB := idxA + 1; idxB < len(allSequences); idxB++ {
			sequenceB := allSequences[idxB]

			// Only compare sequences from the same game
			if sequenceA.Game != sequenceB.Game {
				continue
			}

			gameMax := gameFlags[sequenceA.Game]
			// Both primary selections must be the expected length for the game
			if len(sequenceA.Primary) != gameMax || len(sequenceB.Primary) != gameMax {
				continue
			}

			primaryOverlap := countOverlap(sequenceA.Primary, sequenceB.Primary)
			bonusA, bonusB := sequenceA.Bonus, sequenceB.Bonus
			bonusMatched := (bonusA != 0 && bonusA == bonusB)

			isExact := false
			var percent float64

			entry := MatchEntry{
				FileA:         sequenceA.Filename,
				FileB:         sequenceB.Filename,
				Game:          sequenceA.Game,
				PrimaryMatched: primaryOverlap,
				BonusMatched:   bonusMatched,
				TotalPrimary:   gameMax,
				PrimaryA:       sequenceA.Primary,
				PrimaryB:       sequenceB.Primary,
				BonusA:         bonusA,
				BonusB:         bonusB,
			}

			// --- Game-specific matching logic ---
			switch {
			case (sequenceA.Game == "megamillion" && dropMega) || (sequenceA.Game == "powerball" && dropPower):
				if primaryOverlap == matchDepth {
					isExact = setsEqual(sequenceA.Primary, sequenceB.Primary)
					percent = float64(primaryOverlap) / float64(gameMax) * 100
				}
			case (sequenceA.Game == "megamillion" && forceMega) || (sequenceA.Game == "powerball" && forceMega):
				if primaryOverlap == gameMax && bonusMatched {
					isExact = setsEqual(sequenceA.Primary, sequenceB.Primary)
					num := primaryOverlap
					den := gameMax
					if bonusMatched {
						num++
					}
					den++
					percent = float64(num) / float64(den) * 100
				}
			case (sequenceA.Game == "megamillion" && includeMega) || (sequenceA.Game == "powerball" && includeMega):
				aval := append([]int{}, sequenceA.Primary...)
				bval := append([]int{}, sequenceB.Primary...)
				if sequenceA.Bonus != 0 {
					aval = append(aval, sequenceA.Bonus)
				}
				if sequenceB.Bonus != 0 {
					bval = append(bval, sequenceB.Bonus)
				}
				sort.Ints(aval)
				sort.Ints(bval)
				overlap := countOverlap(aval, bval)
				if overlap == matchDepth {
					isExact = setsEqual(aval, bval)
					percent = float64(overlap) / float64(len(aval)) * 100
				}
			case sequenceA.Game == "megamillion" || sequenceA.Game == "powerball":
				if primaryOverlap == gameMax && bonusMatched {
					isExact = setsEqual(sequenceA.Primary, sequenceB.Primary)
					num := primaryOverlap
					den := gameMax
					if bonusMatched {
						num++
					}
					den++
					percent = float64(num) / float64(den) * 100
				}
			default:
				if primaryOverlap == matchDepth {
					isExact = setsEqual(sequenceA.Primary, sequenceB.Primary)
					percent = float64(primaryOverlap) / float64(gameMax) * 100
				}
			}

			entry.Exact = isExact
			entry.Percent = percent

			// Decide if this match should be shown/reported
			shouldShow := false
			if (sequenceA.Game == "megamillion" && dropMega && primaryOverlap == matchDepth) ||
				(sequenceA.Game == "powerball" && dropPower && primaryOverlap == matchDepth) ||
				((sequenceA.Game == "megamillion" || sequenceA.Game == "powerball") && forceMega && primaryOverlap == gameMax && bonusMatched) ||
				((sequenceA.Game == "megamillion" || sequenceA.Game == "powerball") && includeMega && countOverlap(append(sequenceA.Primary, sequenceA.Bonus), append(sequenceB.Primary, sequenceB.Bonus)) == matchDepth) ||
				((sequenceA.Game == "megamillion" || sequenceA.Game == "powerball") && !dropMega && !dropPower && !forceMega && !includeMega && primaryOverlap == gameMax && bonusMatched) ||
				((sequenceA.Game != "megamillion" && sequenceA.Game != "powerball") && primaryOverlap == matchDepth) {
				shouldShow = true
			}

			// Print or store the match as needed
			if shouldShow {
				matchesList = append(matchesList, entry)
				if isExact {
					exactCount++
					if !summaryOnly {
						fmt.Printf("%s   %s == %s (primary+bonus)\t\t[Primary: %s | %s]   [Bonus: %s | %s]   (%s)\n",
							green("[EXACT]"),
							white(padRight(sequenceA.Filename, 20)),
							white(padRight(sequenceB.Filename, 20)),
							magenta(padRight(formatSlice(sequenceA.Primary), 20)),
							magenta(padRight(formatSlice(sequenceB.Primary), 20)),
							yellow(padRight(bonusString(sequenceA.Bonus), 9)),
							yellow(padRight(bonusString(sequenceB.Bonus), 6)),
							cyan(fmt.Sprintf("%.1f%%", percent)),
						)
					}
				} else {
					partialCount++
					if !summaryOnly {
						fmt.Printf("%s %s <> %s (primary+bonus)   [Primary: %s | %s]   [Bonus: %s | %s]   (%s)\n",
							yellow("[PARTIAL]"),
							dim(padRight(sequenceA.Filename, 20)),
							dim(padRight(sequenceB.Filename, 20)),
							magenta(padRight(formatSlice(sequenceA.Primary), 22)),
							magenta(padRight(formatSlice(sequenceB.Primary), 22)),
							yellow(padRight(bonusString(sequenceA.Bonus), 5)),
							yellow(padRight(bonusString(sequenceB.Bonus), 5)),
							cyan(fmt.Sprintf("%.1f%%", percent)),
						)
					}
				}
			}
		}
	}

	duration := time.Since(start)
	hours = int(duration.Hours())
	minutes = int(duration.Minutes()) % 60
	seconds = int(duration.Seconds()) % 60
	millis = int(duration.Milliseconds()) % 1000
	return exactCount, partialCount, total, matchesList, hours, minutes, seconds, millis
}
```
### func `padRight(s, width)`
>- Purpose: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Pads a string with spaces on the right, for clean column alignment, handling multi-byte characters: Unicode, RTL, etc. <br>
>- Logic: <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; runs with `runewidth.StringWidth` from `github.com/mattn/go-runewidth`
>- Note: <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  keeps CLI columns neat, even for multi-byte or right-to-left filenames.
```go
func padRight(s string, width int) string {
    words := runewidth.StringWidth(s)
    if words >= width {
        return s
    }
    return s + strings.Repeat(" ", width-words)
}
```
### func `bonusString()`
>- Purpose: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Formats a slice of integers as a space-separated string, or `-` if empty: <br>
```go
func bonusString(bonus int) string {
	if bonus == 0 { return "-" }
	return fmt.Sprintf("%d", bonus)
}
```
### func `formatSlice(s []int)`
>- Purpose: Pretty-print `int` slice as space-separated string, or `"-"` if empty.
```go
func formatSlice(s []int) string {
	if len(s) == 0 {
		return "-"
	}
	var sb strings.Builder
	for i, v := range s {
		if i > 0 {
			sb.WriteString(" ")
		}
		sb.WriteString(fmt.Sprintf("%d", v))
	}
	return sb.String()
}
```
### func `setsEqual(a, b []int)`
>- Purpose: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Checks if two slices of integers are exactly equal as an element/idx, order matters: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `True` if slices are of the same length and all elements are identical in order: <br>
```go
func setsEqual(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}
```
### func `countOverlap(a, b []int)`
>- Purpose: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Counts how many elements `two slices` of integers have in common (regardless of order, no repeats):

```go
func countOverlap(a, b []int) int {
	set := make(map[int]struct{}, len(a))
	for _, v := range a {
		set[v] = struct{}{}
	}
	overlap := 0
	for _, v := range b {
		if _, ok := set[v]; ok {
			overlap++
		}
	}
	return overlap
}
```
### func `writeHTMLReport(path, matches)`
>- Purpose: Write results table as HTML file - up to 1000 matches:
>- Logic: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Runs with `Go’s html/template` with included [css config](../src_for_go/assets/style.css):
```go
func writeHTMLReport(path string, matches []MatchEntry) {
	const maxEntries = 1000
	trimmed := matches
	if len(matches) > maxEntries {
		trimmed = matches[:maxEntries]
	}
	tmpl := template.Must(template.New("report").Parse(`
<html>
<head>
	<title>Match Report</title>
	<link rel="stylesheet" type="text/css" href="../src_for_go/assets/style.css">
</head>
<body>
	<h2>Sequence Match Report</h2>
	<p>Showing {{len .Matches}} matches (capped to 1000 max).</p>
	<table>
	<tr>
		<th>Game</th><th>File A</th><th>File B</th>
		<th>Primary A</th><th>Primary B</th>
		<th>Bonus A</th><th>Bonus B</th>
		<th>Primary Matched</th><th>Bonus Matched</th><th>%</th><th>Exact?</th>
	</tr>
	{{range .Matches}}
	<tr>
		<td>{{.Game}}</td><td>{{.FileA}}</td><td>{{.FileB}}</td>
		<td>{{printf "%v" .PrimaryA}}</td><td>{{printf "%v" .PrimaryB}}</td>
		<td>{{.BonusA}}</td><td>{{.BonusB}}</td>
		<td>{{.PrimaryMatched}}</td><td>{{.BonusMatched}}</td>
		<td>{{printf "%.1f" .Percent}}</td><td>{{.Exact}}</td>
	</tr>
	{{end}}
	</table>
</body>
</html>`))
	buf := new(bytes.Buffer)
	tmpl.Execute(buf, struct {
		Matches []MatchEntry
	}{Matches: trimmed})

	_ = os.WriteFile(path, buf.Bytes(), 0644)
}
```
### func `openInBrowser(path)`
>- Purpose: Opens file in browser (macOS, Linux, Windows), prints debug info.
>- Logic: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if mac: runs open path: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if linux: runs xdg-open path: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; On windows: uses rundll32 ... path: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Prints URL for manual open if fails: <br>
```go
func openInBrowser(path string) {
	url := "file://" + filepath.ToSlash(path)
	var cmd *exec.Cmd

	switch runtime.GOOS {
	case "darwin":
		fmt.Printf("[DEBUG] Running: open %s\n", path)
		cmd = exec.Command("open", path)
	case "linux":
		fmt.Printf("[DEBUG] Running: xdg-open %s\n", path)
		cmd = exec.Command("xdg-open", path)
	case "windows":
		fmt.Printf("[DEBUG] Running: rundll32 url.dll,FileProtocolHandler %s\n", path)
		cmd = exec.Command("rundll32", "url.dll,FileProtocolHandler", path)
	default:
		color.Yellow("[WARN] OS not supported for browser auto-open.")
		return
	}
	if err := cmd.Start(); err != nil {
		color.Yellow("[WARN] Could not open browser: %v", err)
		fmt.Println("... html can be opened manually using sys default browsers:")
		fmt.Println(url)
	}
}
```
### func `printFlagSummary(games, depth, dropMega, ...)`
>- Purpose: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The main entry point of the Lotto Sequence Comparison app. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Handles CLI argument parsing, orchestrates data loading, triggers the matching and statistics logic, and manages output/reporting. <br>
>- Logic: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Parse CLI Flags: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Game types (`--games`) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Match depth (`--depth`) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Output/reporting options (`--html`, `--open-html`) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Matching logic flags (`--drop-mega`, `--drop-power`,` --force-mega`, `--include-mega`, `--summary-only`) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Validate Input/Flags: <br>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Ensures only one special matching mode is enabled at a time. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Validates game names and depth. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Warns for unused or redundant options. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Collect File Paths: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Scans for JSON catalog files under the expected directory. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Load and Filter Sequences: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Loads relevant records in parallel (using goroutines and channels). <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Filters by the user’s game selection. <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Compare All Sequences: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Runs matching logic (compareSequences) to find exact/partial matches and compute statistics. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Print Summary and Stats: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Displays colored statistics (exact, partial, total, benchmark time). <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Generate HTML Report (optional): <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; If requested, saves match data to an HTML file and optionally opens it in the browser.
Key Functions Called in main: <br>
>- `findCatalogJSON()` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   Finds all JSON catalog files in the expected location: <br>
>- `loadSequences()` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Loads (and filters) all lottery pick sequences from data files in parallel: <br>
>- `compareSequences()` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Compares every pair of sequences, finds exact and partial matches, computes stats: <br>
>- `printFlagSummary()` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Prints a summary of chosen CLI options and game logic: <br>
>- `writeHTMLReport()` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Generates an HTML file of the match results: <br>
>- `openInBrowser()` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Opens the HTML report using the system’s default browser: <br>

``` go
func printFlagSummary(games map[string]bool, depth int, dropMega, dropPower, forceMega, includeMega bool) {
	var desc string
	if len(games) == 1 {
		for g := range games {
			if g == "megamillion" && dropMega {
				desc = "primary only (ignore Mega)"
			} else if g == "powerball" && dropPower {
				desc = "primary only (ignore Power)"
			}
		}
	}
	if desc == "" {
		if (dropMega && dropPower) || (dropMega && len(games) > 1) || (dropPower && len(games) > 1) {
			desc = "primary only (ignore bonus)"
		}
	}
	if desc == "" && forceMega {
		desc = "require bonus match"
	}
	if desc == "" && includeMega {
		desc = "include bonus in match pool"
	}
	if desc == "" {
		desc = "default matching"
	}
	color.Yellow("[INFO] Games: %v | Depth: %d | Flags: %s", keysFromMap(games), depth, desc)
}
```

### func `main()`
>- Purpose:
>- Logic: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>

```go
func main() {
    // --- 1. CLI Flags and Usage ---
    gamesFlag := flag.String("games", "powerball,megamillion", "Comma-separated list of games to include")
    depthFlag := flag.Int("depth", 5, "Match depth threshold for primary numbers")
    htmlFlag := flag.Bool("html", false, "Generate HTML report")
    openHTMLFlag := flag.Bool("open-html", false, "Open HTML report in browser after generation")
    dropMega := flag.Bool("drop-mega", false, "Ignore Mega number (MegaMillions bonus)")
    dropPower := flag.Bool("drop-power", false, "Ignore Power number (Powerball bonus)")
    forceMega := flag.Bool("force-mega", false, "Bonus ball must match (primary+bonus)")
    includeMega := flag.Bool("include-mega", false, "Include bonus in set for depth match")
    summaryOnly := flag.Bool("summary-only", false, "Summary stats only")

    flag.Parse()

    // --- 2. Validate Flags/Inputs ---
    bonusFlags := 0
    if *dropMega     { bonusFlags++ }
    if *dropPower    { bonusFlags++ }
    if *forceMega    { bonusFlags++ }
    if *includeMega  { bonusFlags++ }
    if bonusFlags > 1 {
        color.Red("[ERROR] Only one of --drop-mega, --drop-power, --force-mega, or --include-mega allowed")
        os.Exit(1)
    }
    if *openHTMLFlag && !*htmlFlag {
        color.Yellow("[WARN] --open-html flag requires --html flag. Ignoring.")
    }

    // --- 3. Parse & Validate Games List ---
    selected := make(map[string]bool)
    for _, g := range strings.Split(*gamesFlag, ",") {
        g = strings.ToLower(strings.TrimSpace(g))
        if _, ok := gameLimits[g]; !ok {
            color.Red("Invalid game '%s', allowed: %v", g, keys(gameLimits))
            os.Exit(1)
        }
        selected[g] = true
    }
    if *depthFlag < 1 {
        color.Red("depth must be >= 1")
        os.Exit(1)
    }

    // --- 4. Warn for Redundant or Unused Flags ---
    for game := range selected {
        if (game == "megamillion" || game == "powerball") && *forceMega && *depthFlag == gameLimits[game]+1 {
            color.Yellow("[WARN] --force-mega has no effect for depth=%d (full match requires bonus anyway)", *depthFlag)
        }
    }
    if *dropMega && !selected["megamillion"] {
        color.Yellow("[WARN] --drop-mega has no effect for games: %v", keysFromMap(selected))
    }
    if *dropPower && !selected["powerball"] {
        color.Yellow("[WARN] --drop-power has no effect for games: %v", keysFromMap(selected))
    }

    // --- 5. Locate and Validate Data Files ---
    paths, _ := findCatalogJSON()
    if len(paths) == 0 {
        color.Red("[ERROR] No JSON files found under catalog/*")
        os.Exit(1)
    }
    color.Magenta("[INFO] Found %d JSON files", len(paths))

    printFlagSummary(selected, *depthFlag, *dropMega, *dropPower, *forceMega, *includeMega)

    // --- 6. Load and Filter Sequences in Parallel ---
    var wg sync.WaitGroup
    ch := make(chan []Sequence, len(paths))
    for _, p := range paths {
        wg.Add(1)
        go loadSequences(p, ch, &wg, selected)
    }
    wg.Wait()
    close(ch)

    var all []Sequence
    for s := range ch {
        all = append(all, s...)
    }

    // --- 7. Compare Sequences and Gather Stats ---
    exact, partial, total, matches, h, m, s, ms :=
        compareSequences(all, gameLimits, *depthFlag, *dropMega, *dropPower, *forceMega, *includeMega, *summaryOnly,)

    // --- 8. Print Summary ---
    fmt.Println()
    fmt.Println(magenta("Stats:"))
    fmt.Println(hiWhite(strings.Repeat("-", 45)))
    fmt.Printf("%s   %s = %s\n", green("[EXACT\t ]"), bold("exact match"), green(fmt.Sprintf("%-6d", exact)))
    fmt.Printf("%s   %s ≥ %-2d = %s\n", yellow("[PARTIAL ]"), bold("partial match"), *depthFlag, hiMagenta(fmt.Sprintf("%-6d", partial)))
    fmt.Printf("%s   %s = %s\n", bold("[TOTAL\t ]"), blue("total sequences"), cyan(fmt.Sprintf("%-6d", total)))
    fmt.Printf("%s   %s\n", bold("[BENCH\t ]"), bold(fmt.Sprintf("Compared in %02dh: %02dm: %02ds. %03dms", h, m, s, ms)))
    fmt.Println()

    // --- 9. HTML Reporting (if requested) ---
    if *htmlFlag {
        reportDir := "html_reports"
        if _, err := os.Stat(reportDir); os.IsNotExist(err) {
            _ = os.MkdirAll(reportDir, 0755)
        }
        timestamp := time.Now().Format("2006-01-02_15-04-05")
        reportPath := filepath.Join(reportDir, fmt.Sprintf("go_report_%s.html", timestamp))
        writeHTMLReport(reportPath, matches)
        if *openHTMLFlag {
            openInBrowser(reportPath)
        }
        color.Cyan("\tHTML report written to %s", reportPath)
    }
}

```
##  Utility Functions: <br>
### func `keys()`
>- Purpose: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Returns all keys from a map as a slice: <br>
``` go
func keys(m map[string]int) []string {
	var k []string
	for key := range m {
		k = append(k, key)
	}
	return k
}
```

### func `printFlagSummary()`
>- Purpose: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Prints a human-readable summary of active flags and options: <br>
``` go
func printFlagSummary(games map[string]bool, depth int, dropMega, dropPower, forceMega, includeMega bool) {
	var desc string
	if len(games) == 1 {
		for g := range games {
			if g == "megamillion" && dropMega {
				desc = "primary only (ignore Mega)"
			} else if g == "powerball" && dropPower {
				desc = "primary only (ignore Power)"
			}
		}
	}
	if desc == "" {
		if (dropMega && dropPower) || (dropMega && len(games) > 1) || (dropPower && len(games) > 1) {
			desc = "primary only (ignore bonus)"
		}
	}
	if desc == "" && forceMega {
		desc = "require bonus match"
	}
	if desc == "" && includeMega {
		desc = "include bonus in match pool"
	}
	if desc == "" {
		desc = "default matching"
	}
	color.Yellow("[INFO] Games: %v | Depth: %d | Flags: %s", keysFromMap(games), depth, desc)
}
```

### func `keysFromMap()`
>- Purpose: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Same as keys(), but for map[string]bool: <br>
``` go
func keysFromMap(m map[string]bool) []string {
	var res []string
	for k := range m {
		res = append(res, k)
	}
	return res
}
```

### func `init()`
>- Purpose: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Customizes the CLI help output: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; When runs the `binary with` no arguments or with -h/--help, function helps with user-friendly usage instructions plus example command invocations.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `usageExamples` help users quickly learn how to use advanced features: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ... bonus drop flags, summary modes, and HTML reporting: <br>

```go
func init() {
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "Usage of %s:\n", os.Args[0])
		flag.PrintDefaults()
		fmt.Fprintln(flag.CommandLine.Output(), usageExamples)
	}
}
```

>- Imports and Data Types: <br>
```go 
import (
    "bytes"             // Buffer for HTML/template rendering
    "encoding/json"     // Reading and parsing JSON lotto records
    "flag"              // Command-line argument parsing
    "fmt"               // Formatted I/O (e.g., Printf)
    "html/template"     // Generates HTML reports
    "os"                // File operations, environment, exiting, etc.
    "os/exec"           // For opening HTML reports in the browser
    "path/filepath"     // Path manipulation (platform-independent)
    "runtime"           // OS detection (for browser launching)
    "sort"              // Sorting slices (numbers for matching)
    "strings"           // String operations (e.g., Split, Trim)
    "sync"              // Goroutine synchronization (WaitGroup)
    "time"              // Benchmarking, timestamps, formatting

    // Third-party:
    "github.com/fatih/color"         // Terminal colored output
    "github.com/mattn/go-runewidth"  // Correct alignment for Unicode filenames
)
```
>- Core Data Types: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Selection: Represents a single lotto ticket selection: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Primary: The main drawn numbers (array of integers): <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Mega: (optional) MegaMillions bonus ball, if present: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Power: (optional) Powerball bonus number, if present: <br>
```go
type Selection struct {
    Primary []int `json:"primary"`
    Mega    []int `json:"mega,omitempty"`
    Power   []int `json:"power,omitempty"`
}

```
>- Records <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Represents a single ticket record (one item in a .json file). <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Timestamp: When the ticket was generated or played. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Game: The game type (e.g., "powerball"). <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Selection: The actual picked numbers, including bonus if present. <br>
```go
type Record struct {
    Timestamp string    `json:"timestamp"`
    Game      string    `json:"game"`
    Selection Selection `json:"selection"`
}
```
>- Sequence: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; An internal, normalized representation used for matching logic. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Game: Game name. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Primary: Main numbers (sorted for comparison). <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Bonus: Bonus number if present, otherwise 0. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Filename: The filename where the record was found (for reporting). <br>
```go
type Sequence struct {
    Game     string
    Primary  []int
    Bonus    int // 0 if not present
    Filename string
}
```
>- MatchEntry: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Captures information about a pair of tickets that match (either exact or partial): <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; FileA, FileB: Names of files where the matched tickets were found: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Game: Game name: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PrimaryMatched: How many primary numbers overlap: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BonusMatched: Whether bonus number matched: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TotalPrimary: Total possible primary numbers (depends on game): <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Exact: Is this an exact match: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PrimaryA, PrimaryB: The main number sets for both tickets: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BonusA, BonusB: Bonus numbers for both: <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Percent: Percent match (used for partials/visualization): <br> 

```go
type MatchEntry struct {
    FileA, FileB, Game string
    PrimaryMatched     int
    BonusMatched       bool
    TotalPrimary       int
    Exact              bool
    PrimaryA, PrimaryB []int
    BonusA, BonusB     int
    Percent            float64
}
```
>- gameLimits: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A global constant mapping game names to the number of primary balls needed for a full valid ticket: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This ensures all matching and validation logic always uses the right ticket length for each game type: <br>
```go
var gameLimits = map[string]int{
    "megamillion": 5,
    "powerball":   5,
    "lotto":       6,
    "luckyday":    5,
    "pick3":       3,
    "pick4":       4,
}
```
___

<!-- ```go
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br> -->
