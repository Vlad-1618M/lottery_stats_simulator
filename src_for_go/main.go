// main.go
package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"html/template"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"sort"
	"strings"
	"sync"
	"time"

	"github.com/fatih/color"
	"github.com/mattn/go-runewidth"
)

// =====================================================================================================================================
type Selection struct {
	Primary []int `json:"primary"`
	Mega    []int `json:"mega,omitempty"`
	Power   []int `json:"power,omitempty"`
}

// =====================================================================================================================================
type Record struct {
	Timestamp string    `json:"timestamp"`
	Game      string    `json:"game"`
	Selection Selection `json:"selection"`
}

// =====================================================================================================================================
type Sequence struct {
	Game     string
	Primary  []int
	Bonus    int // 0 if not present
	Filename string
}

// =====================================================================================================================================
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

// =====================================================================================================================================
var gameLimits = map[string]int{
	"megamillion": 5,
	"powerball":   5,
	"lotto":       6,
	"luckyday":    5,
	"pick3":       3,
	"pick4":       4,
}

// =====================================================================================================================================
var usageExamples = `
CLI Examples:
  	--games=powerball --depth=5 --drop-power         	--> Match Powerball ignoring the Power number (bonus)
  	--games=megamillion --depth=5 --drop-mega        	--> Match MegaMillions ignoring the Mega number (bonus)
  	--games=powerball,megamillion --depth=5 --drop-mega --drop-power --> Both flags allowed together (bonus ignored for both games)
  	--games=megamillion --depth=6                    	--> Strict: match 5+1 (all primary + mega)
  	--games=lotto --depth=6                          	--> Lotto is always single set, no bonus logic:
	--html                								--> Save match results to HTML
  	--html --open-html    								--> Save AND open HTML report in browser
  	--summary-only                                   	--> Show only summary:
`

// =====================================================================================================================================
var (
	green      = color.New(color.FgGreen).SprintFunc()
    yellow     = color.New(color.FgYellow).SprintFunc()
    magenta    = color.New(color.FgMagenta).SprintFunc()
    cyan       = color.New(color.FgCyan).SprintFunc()
    white      = color.New(color.FgWhite).SprintFunc()
    red        = color.New(color.FgRed).SprintFunc()
    blue       = color.New(color.FgBlue).SprintFunc()
    black      = color.New(color.FgBlack).SprintFunc()
    hiRed      = color.New(color.FgHiRed).SprintFunc()
    hiGreen    = color.New(color.FgHiGreen).SprintFunc()
    hiYellow   = color.New(color.FgHiYellow).SprintFunc()
    hiBlue     = color.New(color.FgHiBlue).SprintFunc()
    hiMagenta  = color.New(color.FgHiMagenta).SprintFunc()
    hiCyan     = color.New(color.FgHiCyan).SprintFunc()
    hiWhite    = color.New(color.FgHiWhite).SprintFunc()
    hiBlack    = color.New(color.FgHiBlack).SprintFunc()
    dim        = color.New(color.Faint).SprintFunc()
    bold       = color.New(color.Bold).SprintFunc()
    italic     = color.New(color.Italic).SprintFunc()
    underline  = color.New(color.Underline).SprintFunc()
    inverse    = color.New(color.ReverseVideo).SprintFunc()
)
// _____________________________________________________________________________________________________________________________________

func padRight(s string, width int) string {
    words := runewidth.StringWidth(s)
    if words >= width {
        return s
    }
    return s + strings.Repeat(" ", width-words)
}

// _____________________________________________________________________________________________________________________________________
func init() {
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "Usage of %s:\n", os.Args[0])
		flag.PrintDefaults()
		fmt.Fprintln(flag.CommandLine.Output(), usageExamples)
	}
}

// _____________________________________________________________________________________________________________________________________
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

// _____________________________________________________________________________________________________________________________________
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

// _____________________________________________________________________________________________________________________________________
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

// _____________________________________________________________________________________________________________________________________
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

// _____________________________________________________________________________________________________________________________________
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

// _____________________________________________________________________________________________________________________________________
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

// _____________________________________________________________________________________________________________________________________
func bonusString(bonus int) string {
	if bonus == 0 {
		return "-"
	}
	return fmt.Sprintf("%d", bonus)
}

// _____________________________________________________________________________________________________________________________________
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

// _____________________________________________________________________________________________________________________________________
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

// _____________________________________________________________________________________________________________________________________
func keys(m map[string]int) []string {
	var k []string
	for key := range m {
		k = append(k, key)
	}
	return k
}

// _____________________________________________________________________________________________________________________________________
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


// _____________________________________________________________________________________________________________________________________
func keysFromMap(m map[string]bool) []string {
	var res []string
	for k := range m {
		res = append(res, k)
	}
	return res
}


// _____________________________________________________________________________________________________________________________________
func main() {
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

	bonusFlags := 0
	if *dropMega {
		bonusFlags++
	}
	if *dropPower {
		bonusFlags++
	}
	if *forceMega {
		bonusFlags++
	}
	if *includeMega {
		bonusFlags++
	}
	if bonusFlags > 1 {
		color.Red("[ERROR] Only one of --drop-mega, --drop-power, --force-mega, or --include-mega allowed")
		os.Exit(1)
	}
	
	if *openHTMLFlag && !*htmlFlag {
		color.Yellow("[WARN] --open-html flag requires --html flag. Ignoring.")
	}

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

	// Warn user if forceMega is redundant with depth=max+1
	for game := range selected {
		if (game == "megamillion" || game == "powerball") && *forceMega && *depthFlag == gameLimits[game]+1 {
			color.Yellow("[WARN] --force-mega has no effect for depth=%d (full match requires bonus anyway)", *depthFlag)
		}
	}
	// Warn if drop-mega or drop-power set for a game not present
	if *dropMega && !selected["megamillion"] {
		color.Yellow("[WARN] --drop-mega has no effect for games: %v", keysFromMap(selected))
	}
	if *dropPower && !selected["powerball"] {
		color.Yellow("[WARN] --drop-power has no effect for games: %v", keysFromMap(selected))
	}

	paths, _ := findCatalogJSON()
	if len(paths) == 0 {
		color.Red("[ERROR] No JSON files found under catalog/*")
		os.Exit(1)
	}
	color.Magenta("[INFO] Found %d JSON files", len(paths))

	printFlagSummary(selected, *depthFlag, *dropMega, *dropPower, *forceMega, *includeMega)

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

	exact, partial, total, matches, h, m, s, ms := compareSequences(all, gameLimits, *depthFlag, *dropMega, *dropPower, *forceMega, *includeMega, *summaryOnly,)
	
	fmt.Println()
	fmt.Println(magenta("Stats:"))
	fmt.Println(hiWhite(strings.Repeat("-", 45)))
	fmt.Printf("%s   %s = %s\n", green("[EXACT\t ]"), bold("exact match"), green(fmt.Sprintf("%-6d", exact)))
	fmt.Printf("%s   %s ≥ %-2d = %s\n", yellow("[PARTIAL ]"), bold("partial match"), *depthFlag, hiMagenta(fmt.Sprintf("%-6d", partial)))
	fmt.Printf("%s   %s = %s\n", bold("[TOTAL\t ]"), blue("total sequences"), cyan(fmt.Sprintf("%-6d", total)))
	fmt.Printf("%s   %s\n", bold("[BENCH\t ]"), bold(fmt.Sprintf("Compared in %02dh: %02dm: %02ds. %03dms", h, m, s, ms)))
	fmt.Println()

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
