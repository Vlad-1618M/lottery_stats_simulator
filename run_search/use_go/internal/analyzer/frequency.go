package analyzer

type GameFrequencies struct {
	Primary map[int]int `json:"primary_freq"`
	Bonus   map[int]int `json:"bonus_freq,omitempty"`
}

// ________ BuildFrequencies: returns frequency tables per game:
func BuildFrequencies(seqs []Sequence) map[string]GameFrequencies {
	res := make(map[string]GameFrequencies)
	for _, s := range seqs {
		gf := res[s.Game]
		if gf.Primary == nil {
			gf.Primary = make(map[int]int)
		}
		for _, v := range s.Primary {
			gf.Primary[v]++
		}
		if s.Bonus != 0 {
			if gf.Bonus == nil {
				gf.Bonus = make(map[int]int)
			}
			gf.Bonus[s.Bonus]++
		}
		res[s.Game] = gf
	}
	return res
}
