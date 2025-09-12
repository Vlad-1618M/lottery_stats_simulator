package analyzer

import (
	"fmt"
	"sort"
	"strings"
	"time"
)

// ________ OriginEntry: tracks unique sequences across all catalog files:
type OriginEntry struct {
	Game      string   `json:"game"`
	Primary   []int    `json:"primary"`
	Bonus     int      `json:"bonus"`
	Count     int      `json:"count"`
	FirstSeen string   `json:"first_seen,omitempty"`
	LastSeen  string   `json:"last_seen,omitempty"`
	Files     []string `json:"files"`
}

// ________ TrackOrigins: indexes all unique combinations of game + primary + bonus:
func TrackOrigins(sequences []Sequence) map[string]*OriginEntry {
	originMap := make(map[string]*OriginEntry)

	for _, seq := range sequences {
		key := makeKey(seq.Game, seq.Primary, seq.Bonus)

		if entry, exists := originMap[key]; exists {
			entry.Count++
			if !containsStr(entry.Files, seq.Filename) {
				entry.Files = append(entry.Files, seq.Filename)
			}
			entry.LastSeen = maxTime(entry.LastSeen, seq.Timestamp)
		} else {
			originMap[key] = &OriginEntry{
				Game:      seq.Game,
				Primary:   append([]int{}, seq.Primary...), // defensive copy
				Bonus:     seq.Bonus,
				Count:     1,
				FirstSeen: seq.Timestamp,
				LastSeen:  seq.Timestamp,
				Files:     []string{seq.Filename},
			}
		}
	}

	return originMap
}

// ________ UniqToSlice: converts map of origin entries to sorted slice:
func UniqToSlice(originMap map[string]*OriginEntry) []OriginEntry {
	uniqueList := make([]OriginEntry, 0, len(originMap))

	for _, entry := range originMap {
		uniqueList = append(uniqueList, *entry)
	}

	sort.SliceStable(uniqueList, func(i, j int) bool {
		if uniqueList[i].Game != uniqueList[j].Game {
			return uniqueList[i].Game < uniqueList[j].Game
		}
		if uniqueList[i].Count != uniqueList[j].Count {
			return uniqueList[i].Count < uniqueList[j].Count
		}
		return joinInts(uniqueList[i].Primary) < joinInts(uniqueList[j].Primary)
	})

	return uniqueList
}

// ________ makeKey: generates unique string key for game + primary numbers + bonus:
func makeKey(game string, primary []int, bonus int) string {
	var builder strings.Builder

	builder.WriteString(game)
	builder.WriteString("|")

	for i, num := range primary {
		if i > 0 {
			builder.WriteByte(',')
		}
		builder.WriteString(fmt.Sprintf("%d", num))
	}

	builder.WriteString("|")
	builder.WriteString(fmt.Sprintf("%d", bonus))

	return builder.String()
}

// ________ containsStr: checks if string exists in a slice:
func containsStr(list []string, target string) bool {
	for _, value := range list {
		if value == target {
			return true
		}
	}
	return false
}

// ________ maxTime: returns the later of two RFC3339 timestamps:
func maxTime(a, b string) string {
	timeA, errA := time.Parse(time.RFC3339, a)
	timeB, errB := time.Parse(time.RFC3339, b)

	if errA == nil && errB == nil {
		if timeB.After(timeA) {
			return b
		}
		return a
	}

	// ________ lexicographical go back condition:
	if b > a {
		return b
	}
	return a
}

// ________  joinInts: converts list of integers to a comma-separated string:
func joinInts(numbers []int) string {
	var builder strings.Builder

	for i, n := range numbers {
		if i > 0 {
			builder.WriteByte(',')
		}
		builder.WriteString(fmt.Sprintf("%d", n))
	}

	return builder.String()
}
