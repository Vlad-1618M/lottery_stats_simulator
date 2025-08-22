package config

import (
	"os"
	"testing"
)

func TestLoadYmlNotFound(t *testing.T) {
	_, err := Load("nonexistent.yml")
	if err == nil {
		t.Error("Expected error for missing file, got nil")
	}
}

func TestYmlLoad(t *testing.T) {
	const testFile = "test_config.yml"

	yamlContent := "watch_dirs:\n  - /tmp\n"
	err := os.WriteFile(testFile, []byte(yamlContent), 0644)
	if err != nil {
		t.Fatalf("Failed to create test YAML file: %v", err)
	}
	defer os.Remove(testFile)

	cfg, err := Load(testFile)
	if err != nil {
		t.Fatalf("Load() returned an error: %v", err)
	}

	if len(cfg.WatchDirs) != 1 || cfg.WatchDirs[0] != "/tmp" {
		t.Errorf("Expected WatchDirs to contain \"/tmp\", got: %+v", cfg.WatchDirs)
	}
}

func TestLoadInvalidYAML(t *testing.T) {
	const testFile = "invalid_config.yml"
	badContent := "not: [valid: yaml"

	err := os.WriteFile(testFile, []byte(badContent), 0644)
	if err != nil {
		t.Fatalf("Failed to create invalid YAML: %v", err)
	}
	defer os.Remove(testFile)

	_, err = Load(testFile)
	if err == nil {
		t.Error("Expected YAML unmarshal error, got nil")
	}
}
