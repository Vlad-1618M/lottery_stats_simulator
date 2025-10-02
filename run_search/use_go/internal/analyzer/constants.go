package analyzer

// ________ DefaultGameLimits CFG: defines how many numbers each game requires:
// ________ Used for frequency analysis and suggestion generation:
var DefaultGameLimits = map[string]int{
	"megamillion": 5,
	"powerball":   5,
	"lotto":       6,
	"luckyday":    5,
	"pick3":       3,
	"pick4":       4,
}
