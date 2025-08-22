// internal/watcher/watcher.go
package watcher

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"gotools/internal/diff"
	"gotools/internal/reporter"
	"gotools/internal/tracker"

	"github.com/fsnotify/fsnotify"
)

// WatchDirectory sets up and manages filesystem event watching for a specific directory and its subdirectories.
func WatchDirectory(dir string, color string, wg *sync.WaitGroup) {
	defer wg.Done()

	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		reporter.PrintError("Failed to create watcher: %v", err)
		return
	}
	defer watcher.Close()

	addDirectoryRecursive := func(path string) {
		filepath.Walk(path, func(walkPath string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if info.IsDir() {
				if err := watcher.Add(walkPath); err != nil {
					reporter.PrintError("Failed to watch directory: %s", walkPath)
				}
			}
			return nil
		})
	}

	addDirectoryRecursive(dir)

	snapshots := make(map[string]string)
	lastActivity := time.Now()

	logOnlyExtensions := map[string]bool{
		"pyc": true, "swp": true,
		"png": true, "jpg": true, "jpeg": true, "gif": true,
		"bmp": true, "webp": true, "svg": true, "exe": true,
		"bin": true, "dll": true, "so": true, "zip": true,
		"gz": true, "tar": true, "7z": true,
	}

	for {
		select {
		case event, ok := <-watcher.Events:
			if !ok {
				return
			}
			lastActivity = time.Now()
			timestamp := time.Now().Format("2006-01-02 15:04:05")

			reporter.PrintRaw(fmt.Sprintf("%s[%s] [%s]%s %s on: -> %s%s",
				reporter.Gray(), timestamp, event.Op.String(), reporter.Reset(),
				reporter.Yellow(), event.Name, reporter.Reset()))

			if event.Op&fsnotify.Create == fsnotify.Create {
				info, err := os.Stat(event.Name)
				if err == nil && info.IsDir() {
					addDirectoryRecursive(event.Name)
				}
			}

			if event.Op&fsnotify.Write == fsnotify.Write || event.Op&fsnotify.Create == fsnotify.Create {
				meta, err := tracker.AnalyzeFile(event.Name)
				if err == nil {
					ext := strings.ToLower(meta.Type)
					if logOnlyExtensions[ext] || ext == "" {
						reporter.LogOnly("File updated (binary or unsupported type): %s", event.Name)
					} else {
						content, err := os.ReadFile(event.Name)
						if err == nil {
							old := snapshots[event.Name]
							newContent := string(content)

							changed, diffChunk := diff.DiffText(old, newContent)
							if changed {
								var catColor string
								if old == "" {
									catColor = reporter.Yellow()
								} else if len(newContent) > len(old) {
									catColor = reporter.Green()
								} else {
									catColor = reporter.Reset()
								}

								fileName := filepath.Base(event.Name)
								formatted := fmt.Sprintf("%s%s--- Change Detected%s [%s%s%s] %ssize: %d bytes%s ---%s\n%s%s%s",
									reporter.Gray(), reporter.Red(), reporter.Reset(),
									reporter.Green(), fileName, reporter.Reset(),
									reporter.Gray(), meta.Size, reporter.Reset(),
									reporter.Reset(),
									catColor, diffChunk, reporter.Reset())

								reporter.PrintRaw(formatted)
								snapshots[event.Name] = newContent
							}
						}
					}
				}
			}

			if event.Op&fsnotify.Remove == fsnotify.Remove {
				delete(snapshots, event.Name)
				reporter.PrintInfo("--- File Removed: %s", event.Name)
			}

		case err, ok := <-watcher.Errors:
			if !ok {
				return
			}
			reporter.PrintError("Watcher error: %v", err)

		default:
			idleDuration := time.Since(lastActivity)
			if idleDuration > 10*time.Second {
				idleMinutes := int(idleDuration.Minutes())
				idleSeconds := int(idleDuration.Seconds()) % 60
				msg := fmt.Sprintf("%s[IDLE]%s No activity for %d min %d sec in %s%s",
					reporter.Gray(), reporter.Reset(),
					idleMinutes, idleSeconds,
					dir, reporter.Reset())
				reporter.PrintRaw(msg)
				lastActivity = time.Now()
			}

			time.Sleep(1 * time.Second)
		}
	}
}
