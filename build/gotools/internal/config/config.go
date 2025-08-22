// internal/config/config.go
package config

import (
	"os"

	"gopkg.in/yaml.v3"
)

// Config holds the list of directories to watch.
type Config struct {
	WatchDirs []string `yaml:"watch_dirs"`
}

// Load reads and parses the YAML configuration file.
func Load(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, err
	}
	return &cfg, nil
}
