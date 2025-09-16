package analyzer

import (
	"fmt"
	"sort"
	"strings"
)

type Suggestion struct {
	Game     string `json:"game"`
	Primary  []int  `json:"primary"`
	Bonus    int    `json:"bonus,omitempty"`
	Strategy string `json:"strategy"`
	Notes    string `json:"notes,omitempty"`
}

// GenerateSuggestions creates nPerGame unique sequences per game,
// using either "rarest" or "mixed" strategy.
func GenerateSuggestions(
	history []Sequence,
	games map[string]bool,
	limits map[string]int,
	frequencies map[string]GameFrequencies,
	avoidKDraws int,
	strategy string,
	nPerGame int,
) ([]Suggestion, map[string]int) {
	historyIndex := make(map[string]bool)
	for _, s := range history {
		historyIndex[makeKey(s.Game, s.Primary, s.Bonus)] = true
	}

	// Avoid values from last K draws (if requested)
	recentValues := map[string]map[int]bool{}
	if avoidKDraws > 0 {
		recentValues = buildRecentWindows(history, avoidKDraws)
	}

	useMixed := strings.ToLower(strategy) == "mixed"
	result := []Suggestion{}
	perGameCount := make(map[string]int)

	for game := range games {
		limit := limits[game]
		freqPrimary := sortByFrequencyAsc(frequencies[game].Primary)
		freqBonus := sortByFrequencyAsc(frequencies[game].Bonus)
		recent := recentValues[game]

		genCount := 0
		primaryIndex := 0
		bonusIndex := 0

		for genCount < nPerGame {
			primaryPick := pickPrimary(freqPrimary[primaryIndex:], limit, recent, useMixed)
			if len(primaryPick) < limit {
				break
			}

			bonus := 0
			if requiresBonus(game) && len(freqBonus) > 0 {
				if useMixed && bonusIndex < len(freqBonus) {
					bonus = freqBonus[bonusIndex].Number
					bonusIndex++
				} else {
					bonus = freqBonus[0].Number
				}
				// Avoid recent bonus
				if recent != nil && recent[bonus] {
					for _, fb := range freqBonus {
						if !recent[fb.Number] {
							bonus = fb.Number
							break
						}
					}
				}
			}

			key := makeKey(game, primaryPick, bonus)
			if historyIndex[key] {
				primaryIndex++
				if primaryIndex >= len(freqPrimary) {
					break
				}
				continue
			}

			note := ""
			if avoidKDraws > 0 {
				note = fmt.Sprintf("avoided last %d draws", avoidKDraws)
			}

			result = append(result, Suggestion{
				Game:     game,
				Primary:  primaryPick,
				Bonus:    bonus,
				Strategy: strategy,
				Notes:    note,
			})
			historyIndex[key] = true
			perGameCount[game]++
			genCount++
			primaryIndex++
		}
	}

	return result, perGameCount
}

// freqPair stores a number and its frequency count.
type freqPair struct {
	Number int
	Count  int
}

// sortByFrequencyAsc orders numbers from rarest to most frequent.
func sortByFrequencyAsc(freq map[int]int) []freqPair {
	out := make([]freqPair, 0, len(freq))
	for num, count := range freq {
		out = append(out, freqPair{Number: num, Count: count})
	}
	sort.SliceStable(out, func(i, j int) bool {
		if out[i].Count != out[j].Count {
			return out[i].Count < out[j].Count
		}
		return out[i].Number < out[j].Number
	})
	return out
}

// requiresBonus checks if a game type includes a bonus number.
func requiresBonus(game string) bool {
	return game == "megamillion" || game == "powerball"
}

// pickPrimary selects primary numbers according to strategy.
func pickPrimary(pairs []freqPair, count int, banned map[int]bool, useMixed bool) []int {
	result := []int{}
	i := 0
	j := len(pairs) / 2

	for len(result) < count && (i < len(pairs) || j < len(pairs)) {
		var candidate freqPair
		if useMixed && len(result)%2 == 1 && j < len(pairs) {
			candidate = pairs[j]
			j++
		} else if i < len(pairs) {
			candidate = pairs[i]
			i++
		} else {
			break
		}
		if banned != nil && banned[candidate.Number] {
			continue
		}
		if containsInt(result, candidate.Number) {
			continue
		}
		result = append(result, candidate.Number)
	}

	sort.Ints(result)
	return result
}

func containsInt(slice []int, target int) bool {
	for _, v := range slice {
		if v == target {
			return true
		}
	}
	return false
}

// buildRecentWindows collects numbers from the last K draws per game.
func buildRecentWindows(sequences []Sequence, k int) map[string]map[int]bool {
	gameMap := make(map[string][]Sequence)
	for _, s := range sequences {
		gameMap[s.Game] = append(gameMap[s.Game], s)
	}

	out := make(map[string]map[int]bool)
	for game, draws := range gameMap {
		sort.SliceStable(draws, func(i, j int) bool {
			ti := parseTime(draws[i].Timestamp)
			tj := parseTime(draws[j].Timestamp)
			return ti.After(tj)
		})

		if k > len(draws) {
			k = len(draws)
		}
		recent := make(map[int]bool)
		for i := 0; i < k; i++ {
			for _, n := range draws[i].Primary {
				recent[n] = true
			}
			if draws[i].Bonus != 0 {
				recent[draws[i].Bonus] = true
			}
		}
		out[game] = recent
	}
	return out
}
