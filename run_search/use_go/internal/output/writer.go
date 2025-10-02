package output

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

// ________ FindRepoRoot: located rep root --> "lottery_stats_simulator" directory:
func FindRepoRoot() (string, error) {
	dir, err := os.Getwd()
	if err != nil {
		return "", err
	}
	for {
		if filepath.Base(dir) == "lottery_stats_simulator" {
			return filepath.Abs(dir)
		}
		parent := filepath.Dir(dir)
		if parent == dir {
			return "", fmt.Errorf("repository root not found")
		}
		dir = parent
	}
}

// ________ Suggestion: should match --> analyzer.Suggestion exactly:
type Suggestion struct {
	Game    string   `json:"game"`
	Values  []int    `json:"values"`
	Source  string   `json:"source"`
	Index   int      `json:"index"`
	Trace   []string `json:"trace,omitempty"`
}

// ________ MarshalJSON: customizes .json output | keeps values key pairs inline:
func (s Suggestion) MarshalJSON() ([]byte, error) {
	// ________ control .json structure -->  map:
	type Alias Suggestion // ________ avoid infinite recursion:
	aux := struct {
		Alias
		Values string `json:"values"` // ________ override values as string:
	}{
		Alias: Alias(s),
	}

	// ________ convert values key pairs to  str: --> (e.g., [7,19,21,45,49])
	valuesBytes, err := json.Marshal(s.Values)
	if err != nil {
		return nil, fmt.Errorf("marshaling values: %w", err)
	}
	aux.Values = string(valuesBytes)

	return json.Marshal(aux)
}

// ________ WriteJSON: exports analysis results to a timestamped .json file:
func WriteJSON(
	suggestions []Suggestion,
	summary map[string]int,
	sourcePath, exportDir, exportName string,
) error {
	// ________ find repo root path:
	repoRoot, err := FindRepoRoot()
	if err != nil {
		return fmt.Errorf("finding repository root: %w", err)
	}

	// ________ use repoRoot unless exportDir is absolute:
	outputDir := exportDir
	if !filepath.IsAbs(exportDir) {
		outputDir = filepath.Join(repoRoot, exportDir)
	}
	fullPath := filepath.Join(outputDir, exportName)

	err = os.MkdirAll(outputDir, 0755)
	if err != nil {
		return fmt.Errorf("creating export dir: %w", err)
	}

	f, err := os.Create(fullPath)
	if err != nil {
		return fmt.Errorf("creating export file: %w", err)
	}
	defer f.Close()

	enc := json.NewEncoder(f)
	enc.SetIndent("", "  ") // ________ restore indentation for readable .json:

	payload := map[string]interface{}{
		"summary":     summary,
		"suggestions": suggestions,
		"timestamp":   time.Now().Format(time.RFC3339),
		"source_path": sourcePath,
	}

	if err := enc.Encode(payload); err != nil {
		return fmt.Errorf("encoding json: %w", err)
	}

	return nil
}