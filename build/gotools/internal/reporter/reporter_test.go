package reporter

import "testing"

func TestGetColor(t *testing.T) {
	tests := []struct {
		index    int
		expected string
	}{
		{0, colors[0]},
		{1, colors[1]},
		{2, colors[2]},
		{3, colors[3]},
		{4, colors[0]}, // Test wrapping around
		{5, colors[1]},
	}

	for _, tt := range tests {
		if GetColor(tt.index) != tt.expected {
			t.Errorf("GetColor(%d) = %q; want %q", tt.index, GetColor(tt.index), tt.expected)
		}
	}
}

func TestColorGetters(t *testing.T) {
	if Yellow() != yellow {
		t.Errorf("Yellow() = %q; want %q", Yellow(), yellow)
	}
	if Green() != green {
		t.Errorf("Green() = %q; want %q", Green(), green)
	}
	if Gray() != gray {
		t.Errorf("Gray() = %q; want %q", Gray(), gray)
	}
	if Red() != red {
		t.Errorf("Red() = %q; want %q", Red(), red)
	}
	if Reset() != reset {
		t.Errorf("Reset() = %q; want %q", Reset(), reset)
	}
}
