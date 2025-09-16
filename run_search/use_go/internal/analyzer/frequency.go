package analyzer

// GameFrequencies stores both raw counts and file origins per game.
type GameFrequencies struct {
	Primary      map[int]int              `json:"primary_freq"`
	Bonus        map[int]int              `json:"bonus_freq,omitempty"`
	TotalPrimary int                      `json:"total_primary"`
	TotalBonus   int                      `json:"total_bonus,omitempty"`
	FileOrigins  map[int]map[string]int   `json:"file_origins,omitempty"`
	BonusOrigins map[int]map[string]int   `json:"bonus_origins,omitempty"`
}

// BuildFrequencies aggregates frequency counts per game across sequences.
func BuildFrequencies(seqs []Sequence) map[string]GameFrequencies {
	res := make(map[string]GameFrequencies)

	for _, s := range seqs {
		gf, ok := res[s.Game]
		if !ok {
			gf = GameFrequencies{
				Primary:      make(map[int]int),
				Bonus:        make(map[int]int),
				FileOrigins:  make(map[int]map[string]int),
				BonusOrigins: make(map[int]map[string]int),
			}
		}

		// Count primary numbers
		for _, v := range s.Primary {
			gf.Primary[v]++
			gf.TotalPrimary++

			if gf.FileOrigins[v] == nil {
				gf.FileOrigins[v] = make(map[string]int)
			}
			gf.FileOrigins[v][s.Filename]++
		}

		// Count bonus number (if present)
		if s.Bonus != 0 {
			gf.Bonus[s.Bonus]++
			gf.TotalBonus++

			if gf.BonusOrigins[s.Bonus] == nil {
				gf.BonusOrigins[s.Bonus] = make(map[string]int)
			}
			gf.BonusOrigins[s.Bonus][s.Filename]++
		}

		res[s.Game] = gf
	}
	return res
}

// package analyzer

// // GameFrequencies stores both raw counts and totals for each game.
// type GameFrequencies struct {
// 	Primary      map[int]int `json:"primary_freq"`
// 	Bonus        map[int]int `json:"bonus_freq,omitempty"`
// 	TotalPrimary int         `json:"total_primary"`
// 	TotalBonus   int         `json:"total_bonus,omitempty"`
// }

// // BuildFrequencies aggregates frequency counts per game across sequences.
// func BuildFrequencies(seqs []Sequence) map[string]GameFrequencies {
// 	res := make(map[string]GameFrequencies)

// 	for _, s := range seqs {
// 		gf, ok := res[s.Game]
// 		if !ok {
// 			gf = GameFrequencies{
// 				Primary: make(map[int]int),
// 				Bonus:   make(map[int]int),
// 			}
// 		}

// 		// Count primary numbers
// 		for _, v := range s.Primary {
// 			gf.Primary[v]++
// 			gf.TotalPrimary++
// 		}

// 		// Count bonus number (if present)
// 		if s.Bonus != 0 {
// 			gf.Bonus[s.Bonus]++
// 			gf.TotalBonus++
// 		}

// 		res[s.Game] = gf
// 	}
// 	return res
// }

