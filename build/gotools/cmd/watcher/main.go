// cmd/watcher/main.go
package main

import (
	"os"
	"sync"

	"gotools/internal/config"
	"gotools/internal/reporter"
	"gotools/internal/watcher"
)

/*
Main is the entry point of the filesystem watcher application.

Responsibilities:
- Load configuration from cfg.yml using the config module.
- For each directory to watch, assign a color and print a startup message via the reporter module.
- Start a concurrent watcher for each directory using the watcher module.
- Wait for all watcher goroutines to complete using sync.WaitGroup.

The application is modular and can be easily extended or debugged by modifying the respective internal packages.
*/
func main() {
	cfg, err := config.Load("cfg.yml")
	if err != nil {
		reporter.PrintError("Failed to load config: %v", err)
		os.Exit(1)
	}

	var wg sync.WaitGroup
	for i, dir := range cfg.WatchDirs {
		color := reporter.GetColor(i)
		reporter.PrintInfo("Watching: %s", dir)
		wg.Add(1)
		go watcher.WatchDirectory(dir, color, &wg)
	}

	wg.Wait()
}
