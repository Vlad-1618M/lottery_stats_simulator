package analyzer

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"

	"lottery_stats_simulator/run_search/go/internal/output"
)

// Catalog-style record
type Selection struct {
	Primary []int `json:"primary"`
	Mega    []int `json:"mega,omitempty"`
	Power   []int `json:"power,omitempty"`
}

type Record struct {
	Timestamp string    `json:"timestamp"`
	Game      string    `json:"game"`
	Selection Selection `json:"selection"`
}

// Historical draw record
type DrawRecord struct {
	DrawDate       string   `json:"draw_date"`
	PrimaryNumbers []string `json:"primary_numbers"`
	Mega           string   `json:"mega,omitempty"`
	Powerball      string   `json:"powerball,omitempty"`
}

// Normalized sequence
type Sequence struct {
	Game      string
	Primary   []int
	Bonus     int
	Filename  string
	Timestamp string
}

// normalizeGameName maps aliases/variants to consistent keys
func normalizeGameName(name string) string {
	n := strings.ToLower(strings.TrimSpace(name))
	switch n {
	case "megamillions", "mega_millions", "mm":
		return "megamillion"
	case "powerball", "pb":
		return "powerball"
	case "lotto":
		return "lotto"
	case "luckyday", "luckydaylotto":
		return "luckyday"
	case "pick3":
		return "pick3"
	case "pick4":
		return "pick4"
	}
	return n
}

// FindCatalogJSON returns all .json files under root (file, dir, or repo root)
func FindCatalogJSON(root string) ([]string, error) {
	root = filepath.Clean(root)

	// If root is explicitly a file, just return it
	info, err := os.Stat(root)
	if err == nil && !info.IsDir() {
		if strings.HasSuffix(strings.ToLower(root), ".json") {
			return []string{root}, nil
		}
		return nil, fmt.Errorf("not a .json file: %s", root)
	}

	// If root == "." → treat as repo root and search known dirs
	if root == "." {
		repoRoot, err := output.FindRepoRoot()
		if err != nil {
			return nil, fmt.Errorf("failed to find repository root: %w", err)
		}

		subdirs := []string{
			"catalog",
			"historical_lotto_draw_results",
			"lotto_draw_results",
		}

		var allPaths []string
		for _, sub := range subdirs {
			start := filepath.Join(repoRoot, sub)
			if _, err := os.Stat(start); os.IsNotExist(err) {
				continue // skip missing dirs
			}
			filepath.WalkDir(start, func(path string, d os.DirEntry, err error) error {
				if err == nil && !d.IsDir() && strings.HasSuffix(strings.ToLower(path), ".json") {
					allPaths = append(allPaths, path)
				}
				return nil
			})
		}
		return allPaths, nil
	}

	// Otherwise: user gave a directory → walk it
	var paths []string
	err = filepath.WalkDir(root, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return nil
		}
		if !d.IsDir() && strings.HasSuffix(strings.ToLower(path), ".json") {
			paths = append(paths, path)
		}
		return nil
	})
	return paths, err
}

// LoadSequences parses both catalog and historical draw records
func LoadSequences(paths []string, selectedGames map[string]bool) ([]Sequence, error) {
	var all []Sequence

	for _, p := range paths {
		raw, err := os.ReadFile(p)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[WARN] read %s: %v\n", p, err)
			continue
		}

		base := filepath.Base(p)

		// --- Try catalog format ---
		var recs []Record
		if err := json.Unmarshal(raw, &recs); err == nil && len(recs) > 0 && recs[0].Game != "" {
			for _, r := range recs {
				g := normalizeGameName(r.Game)
				if !selectedGames[g] {
					continue
				}

				prim := append([]int{}, r.Selection.Primary...)
				sort.Ints(prim)

				bonus := 0
				switch g {
				case "megamillion":
					if len(r.Selection.Mega) == 1 {
						bonus = r.Selection.Mega[0]
					}
				case "powerball":
					if len(r.Selection.Power) == 1 {
						bonus = r.Selection.Power[0]
					}
				}

				all = append(all, Sequence{
					Game:      g,
					Primary:   prim,
					Bonus:     bonus,
					Filename:  base,
					Timestamp: r.Timestamp,
				})
			}
			continue
		}

		// --- Try historical format ---
		var draws []DrawRecord
		if err := json.Unmarshal(raw, &draws); err == nil && len(draws) > 0 {
			// Guess game from filename (before first "_")
			g := normalizeGameName(strings.Split(strings.ToLower(base), "_")[0])
			if !selectedGames[g] {
				continue
			}
			for _, r := range draws {
				var prim []int
				for _, s := range r.PrimaryNumbers {
					for _, chunk := range strings.Split(s, ",") {
						chunk = strings.TrimSpace(chunk)
						if n, err := strconv.Atoi(chunk); err == nil {
							prim = append(prim, n)
						}
					}
				}
				sort.Ints(prim)

				bonus := 0
				if r.Mega != "" {
					bonus, _ = strconv.Atoi(r.Mega)
				} else if r.Powerball != "" {
					bonus, _ = strconv.Atoi(r.Powerball)
				}

				all = append(all, Sequence{
					Game:      g,
					Primary:   prim,
					Bonus:     bonus,
					Filename:  base,
					Timestamp: r.DrawDate,
				})
			}
		}
	}
	return all, nil
}
