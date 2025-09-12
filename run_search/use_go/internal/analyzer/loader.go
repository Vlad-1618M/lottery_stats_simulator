package analyzer

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

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

type Sequence struct {
	Game      string
	Primary   []int
	Bonus     int
	Filename  string
	Timestamp string
}

func FindCatalogJSON(root string) ([]string, error) {
	root = filepath.Clean(root)
	var paths []string
	err := filepath.WalkDir(root, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return nil
		}
		if d.IsDir() {
			return nil
		}
		// ________  use .jsons only in or under "catalog/" dir / subdir:
		if strings.HasSuffix(strings.ToLower(path), ".json") &&
			strings.Contains(path, string(os.PathSeparator)+"catalog"+string(os.PathSeparator)) {
			paths = append(paths, path)
		}
		return nil
	})
	return paths, err
}

// ________  LoadSequences: parses draw records into normalized Sequence structs:
func LoadSequences(paths []string, selectedGames map[string]bool) ([]Sequence, error) {
	var all []Sequence
	for _, p := range paths {
		raw, err := os.ReadFile(p)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[WARN] read %s: %v\n", p, err)
			continue
		}
		var recs []Record
		if err := json.Unmarshal(raw, &recs); err != nil {
			fmt.Fprintf(os.Stderr, "[WARN] parse %s: %v\n", p, err)
			continue
		}
		base := filepath.Base(p)
		for _, r := range recs {
			g := strings.ToLower(strings.TrimSpace(r.Game))
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
	}
	return all, nil
}
