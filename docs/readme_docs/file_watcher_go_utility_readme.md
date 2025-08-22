# File Watcher Go Utility:
The [File Watcher Go Utility](lotto_simulator/build/gotools/) is a modular Go application desinged to monitor specified directories for filesystem events:<br> 
- create: 
- write: 
- remove:
- logs changes with colored terminal output:
- writes logs to ***fs_watcher.log*** 
- Detects FS content changes in files:
- Reports metadata for binary files: 
- Tracks directory statistics: 
- Supports concurrent directory watching: 
- Designed to be ***sidecar*** deployed by [monitor.Dockerfile](/build/sidecar/monitor.Dockerfile) for lightweight execution:

## Features:
- Monitors multiple directories concurrently, specified in [cfg.yml](/build/gotools/cfg.yml)
- Detects filesystem events (****create****, ****write****, ***remove***) using [fsnotify](https://pkg.go.dev/github.com/fsnotify/fsnotify)
- Logs events with ***ANSI-colored*** terminal output as well as to ***fs_watcher.log***
- Displays ***diffs*** for text file changes (***new***, ***appended***, or ***modified***)
- Tracks file metadata (***size***, ***type***, ***modification*** time) + directory statistics (***file*** count and ***type***)
- Ignores ***binary***/unsupported file types (e.g., ***.png***, ***.exe***) for diffing by logging metadata instead:
- Supports Docker deployment with an Alpine-based container:
- Uunit tests for reliability inlcuded:

## Dependencies:
- Go 1.21+ [go install](https://go.dev/doc/install)
- External Go modules:
    - [gopkg.in/yaml.v3](https://pkg.go.dev/gopkg.in/yaml.v3?utm_source=godoc) for parsing [cfg.yml](/build/gotools/cfg.yml)
    - [github.com/fsnotify/fsnotify](https://github.com/fsnotify/fsnotify) for filesystem event monitoring:


### Internal packages: - in ***[repo](/build/gotools/internal/)***
>- [internal/config](/build/gotools/internal/config/)
>- [internal/diff](/build/gotools/internal/diff/)
>- [internal/reporter](/build/gotools/internal/reporter/)
>- [internal/tracker](/build/gotools/internal/tracker/)
>- [internal/watcher](/build/gotools/internal/watcher/)
>- Configuration file: - ***[cfg.yml](/build/gotools/cfg.yml)***

### Installation:
>- Clone the Repository:
>   - git clone ???? T.B.D
>   - cd [gotools](/build/gotools/)
>   - Install Golang: 
>       - ensure [Go 1.21+](https://go.dev/doc/install) is installed: 
>        - you can use/refer to [install_go.sh](/build/shell_tools/install_go.sh) script to make it easier for clund ***VMs*** or ***Docker*** containers:
>   - Install Dependencies:
>       - `go mod tidy` - will fetche [gopkg.in/yaml.v3]([gopkg.in/yaml.v3](https://pkg.go.dev/gopkg.in/yaml.v3?utm_source=godoc)) and [github.com/fsnotify/fsnotify]([github.com/fsnotify/fsnotify](https://github.com/fsnotify/fsnotify)) repos:
>       - [NOTE](https://www.reddit.com/r/golang/comments/x722i0/go_install_vs_go_mod_tidy_vs_go_get/): - ***What is the different between*** [go mod](https://go.dev/ref/mod) and [go mod tidy](https://go.dev/ref/mod#go-mod-tidy) ***download*** ?

### File Watcher Utility: How To:
[File Watcher](lotto_simulator/build/gotools/) utility ***as implemented in this repository*** is designed to be shipped and executed from a [sidecar](/build/sidecar/monitor.Dockerfile) as a stand-alone container:<br>
It is built as a [compiled binary](/build/shell_tools/filewatcher_compiler_architecture.sh) and supports multiple architectures:<br>
That said, it can also be run outside the container, assuming the [cfg.yml](/build/gotools/cfg.yml) file is properly configured with the correct watch paths:<br>
- NOTE: Basic knowledge of Go is recommended, particularly the differences between running source code (***`go run`***) or executing ***`compiled binaries`*** in various environments:
    - Reads [cfg.yml](/build/gotools/cfg.yml) to determine which directories to monitor: <br>
    - Logs events to both ***terminal*** and ***fs_watcher.log*** file:
    - In containerized environment such as this one:
        - If call as (***`go run`***): - executes from [/gotools/cmd/watcher/main.go](/build/gotools/cmd/watcher/main.go) directory:
        - If call as (***`compiled binary`***) - can be invoked from anywhere, as long as the [gotools](/build/gotools/) directory is present in the system's path:

### CLI Examples & Command Description:
- files structure in ***`gotools`*** dir path:
```bash
tree .
.
|-- cfg.yml
|-- cmd
|   `-- watcher
|       `-- main.go
|-- go.mod
|-- go.sum
`-- internal
    |-- config
    |   |-- config.go
    |   `-- config_test.go
    |-- diff
    |   |-- diff.go
    |   `-- diff_test.go
    |-- reporter
    |   |-- fs_watcher.log
    |   |-- reporter.go
    |   `-- reporter_test.go
    |-- tracker
    |   |-- filemeta.go
    |   |-- tracker.go
    |   `-- tracker_test.go
    `-- watcher
        |-- watcher.go
```

- ***`go run cmd/watcher/main.go`*** - as code:
```bash
cd build/gotools/
go run cmd/watcher/main.go
```

![go run](/docs/png_docs/filewatcher_gorun_image_1.png)


- ***`go run cmd/watcher/main.go`*** - as binary: [mp4](/docs/mp4/go_watcher_as_code.mov_2x.mp4)
```bash
cd build/gotools/
go build -o go_watcher cmd/watcher/main.go
./go_watcher
```
- call example ***compiled*** binary:

![go binary](/docs/png_docs/go_watcher_complied_image.png)

- call example ***fs_watcher*** logs:

![go binary logs](/docs/png_docs/fs_watcher_logs.png)

### Multi Architecture Support | Sidecar + Composer: 
Since this repo is containerized, most common OS environments should be supported out of the box:<br>
However, if the repo is cloned to a system other than macOS or Linux, the multi-architecture support should help:<br>
- The [filewatcher_compiler_architecture.sh](/build/shell_tools/filewatcher_compiler_architecture.sh) designed to support the following OS architectures:
    >- linux - amd64
    >- darwin - arm64
    >- windows - 386
    >- windows - win32

```bash
cd build/gotools/
../shell_tools/filewatcher_compiler_architecture.sh
```
- ***filewatcher_compiler_architecture.sh*** run example:

![multi-architecture](/docs/png_docs/go_compiled.png)

- [mp4 -> filewatcher_compiler_architecture.sh](/docs/mp4/go_watcher_run_example_2x.mp4) to the [sidecar](/build/sidecar/monitor.Dockerfile) container runtime with [docker-compose](/build/orchestrators/docker-compose.yml)

---

- go test run: 
- ***`go test ./internal/...`*** Runs internal packages unit tests:
- ***`go test -cover`*** Generate test coverage report:
```bash
go test ./internal/... -cover -covermode=atomic -coverprofile=coverage.out -failfast
go tool cover -html=coverage.out -o coverage.html
```
- ***go unit tests*** run example:

![go test](/docs/png_docs/go_tests.png)

### Docker Deployment Only | ***NO docker-composer:***
- Sidecar or [monitor.Dockerfile](/build/sidecar/monitor.Dockerfile) builds a lightweight Alpine-based image:
- Copies the compiled binary (go_watcher) or dynamically selects the latest binary from [build/gotools](/build/gotools/)/go_compiled dir path:
- Copies cfg.yml to /side_monitor/cfg.yml.
- Runs the binary as the entrypoint.

### Build ***`stand-along`*** Sidecar Docker Container:
- Step 1: - get compiled binary:
    - Run [filewatcher_single_architecture_build.sh](/build/shell_tools/filewatcher_single_architecture_build.sh) shell script for a single ARCH binary compiled engine:
```bash
./build/shell_tools/filewatcher_single_architecture_build.sh
```

- Step 2: - Create shared `Docker network`:
```bash
docker network create lotto_network
```
- Docker netwrok check: 
```bash
docker network inspect lotto_network
[
    {
        "Name": "lotto_network",
        "Id": "1d9be4d2acb4f7eedb7064bd53ef4da5d3868f1b1bb54119b778a351ca974990",
        "Created": "2025-08-19T17:40:43.977806919Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv4": true,
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "XXXX/X",
                    "Gateway": "XXXX"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {
            "com.docker.network.enable_ipv4": "true",
            "com.docker.network.enable_ipv6": "false"
        },
        "Labels": {}
    }
]

```
- Step 3: - Build the `watcher-sidecar` [image](/build/sidecar/monitor.Dockerfile)
```bash
docker build -t watcher-sidecar -f build/sidecar/monitor.Dockerfile  .
```
>- Run sidecar container — needs:
>- * Explicit network setup:
>- * Volume mount:
>- * if inspect or reuse the container is needed,  drop the `--rm` flag:
- Run sidecar container with `--dit`
```bash
docker run -dit --name watcher_sidecar --network lotto_network -v lotto_data:/lotto watcher-sidecar
```
- or with `--rm`
```bash
docker run --rm --name watcher_sidecar --network lotto_network -v lotto_data:/lotto watcher-sidecar
```
>- `-dit` instead of `--rm` allows interactive or background runs:
>- `--rm` not recommended if you want persistent observation or volume inspections:

- Step 4: - Build the data collector `lotto` [container](/build/amd64/ubu_amd64_playwright.Dockerfile) 
    ___****- check your OS architecture prior to this step:****___
    - [arm64](/build/amd64/ubu_amd64_playwright.Dockerfile)
    - [amd64](/build/amd64/ubu_amd64_playwright.Dockerfile)

```bash
docker build -t lotto --progress=plain -f build/arm64/ubu_arm64_playwright.Dockerfile .
```
- Step 5:
- Run ***`lotto`*** container image as ***`container_lotto`*** + shared ***`lotto_network`*** and shell in session: 
```bash
docker run -it --name container_lotto --network lotto_network -v lotto_data:/lotto lotto bash
```

[watcher mp4 demo](/docs/mp4/sidecar_stand_along_watcher_build_demo_2x.mp4)

---
## Glang Components / Package Description:

- [main()](/build/gotools/cmd/watcher/main.go) - Loads [cfg.yml](/build/gotools/cfg.yml) | starts concurrent watchers for each directory | waits for completion:

    ```go
    // cmd/watcher/main.go
    package main

    import (
        "os"
        "sync"

        "gotools/internal/config"
        "gotools/internal/reporter"
        "gotools/internal/watcher"
    )
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

    ```

- Config [internal/config](/build/gotools/internal/config/config.go) 
    - list of directories to monitor:
    - Reads and parses [cfg.yml](/build/gotools/cfg.yml) into a Config struct:
        ```go
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

        ```

- [DiffText](/build/gotools/internal/diff/diff.go) 
    - Compares file content: 
    - Returns `diff` for new or appended or full content if modified:

        ```go
        package diff

        func DiffText(oldText, newText string) (bool, string) {
            if oldText == newText {
                return false, ""
            }

            // If old is empty (new file), show full content
            if oldText == "" {
                return true, newText
            }

            // If new text is longer → appended
            if len(newText) > len(oldText) {
                return true, newText[len(oldText):]
            }

            // Fallback: full content
            return true, newText
        }
        ```


- [reporter](/build/gotools/internal/reporter/) 
    - ***func PrintInfo*** - Logs informational messages with yellow color to terminal and fs_watcher.log:
        ```go
        func PrintInfo(format string, a ...interface{}) {
            msg := fmt.Sprintf(format, a...)
            fmt.Printf("%s[INFO]%s %s%s\n", yellow, reset, msg, reset)
            log.Printf("[INFO] %s\n", msg)
        }
        ```
    - ***func PrintError*** - Logs error messages | colors to terminal and fs_watcher.log:
        ```go
        func PrintError(format string, a ...interface{}) {
            msg := fmt.Sprintf(format, a...)
            fmt.Printf("%s[ERROR]%s %s%s\n", red, reset, msg, reset)
            log.Printf("[ERROR] %s\n", msg)
        }
        ```
    - ***func PrintIdle*** - Logs idle messages after 10 seconds of inactivity

        ```go
        func PrintIdle(dir string) {
            msg := fmt.Sprintf("No activity in %s", dir)
            fmt.Printf("%s[IDLE] %sNo activity in %s%s%s\n", gray, gray, dir, reset, reset)
            log.Printf("[IDLE] %s", msg)
        }
        ```

    - ***func LogOnly***  - Logs to fs_watcher.log without terminal output (e.g., for binary files):

        ```go
        func LogOnly(format string, a ...interface{}) {
            msg := fmt.Sprintf(format, a...)
            log.Printf("[LOG] %s\n", msg)
        }
        ```
- [tracker](/build/gotools/internal/tracker/) 
    - [filemeta.go](/build/gotools/internal/tracker/filemeta.go) - holding file metadata (***`size`, `modification time`, `file type`***):
    - ***func AnalyzeFile*** - Retrieves file metadata:

        ```go
        func AnalyzeFile(path string) (*FileMeta, error) {
            info, err := os.Stat(path)
            if err != nil {
                return nil, err
            }

            fileType := DetectFileType(path)
            return &FileMeta{
                Size:    info.Size(),
                ModTime: info.ModTime().Unix(),
                Type:    fileType,
            }, nil
        }
        ```
    - ***func DetectFileType*** - directory stats:

        ```go
        func DetectFileType(path string) string {
        base := filepath.Base(path)
        if !strings.Contains(base, ".") || strings.HasPrefix(base, ".") && !strings.Contains(base[1:], ".") {
            return "unknown"
        }

        ext := strings.ToLower(filepath.Ext(base))
        if ext == "" {
            return "unknown"
        }
        return ext[1:] // remove dot
        }
        ```
    - [tracker.go](/build/gotools/internal/tracker/tracker.go)
        - ***type DirStats struct*** - Struct holding directory stats (***`file count`, `types`***)

            ```go
            type DirStats struct {
                FileCount int
                FileTypes map[string]int
            }
            ```
        - ***func AnalyzeDir*** - Scans directory recursively, collecting file count and type distribution:

            ```go
            func AnalyzeDir(dirPath string) (*DirStats, error) {
                stats := &DirStats{
                    FileCount: 0,
                    FileTypes: make(map[string]int),
                }

                err := filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
                    if err != nil {
                        return err
                    }
                    if !info.IsDir() {
                        stats.FileCount++
                        
                        fileType := DetectFileType(path)
                        stats.FileTypes[fileType]++
                    }
                    return nil
                })

                if err != nil {
                    return nil, err
                }

                return stats, nil
            }
            
            ```
    - [watcher.go](/build/gotools/internal/watcher/watcher.go)
        - ***func WatchDirectory*** - Monitors directory for filesystem events, logs changes, handles diffs:
        
        ```go
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

        ```

- Configuration: [cfg.yml](/build/gotools/cfg.yml) file specifies directories to monitor:

    ```yml
    watch_dirs:
    - /lotto
    ```

    - Paths must be absolute or relative to the container’s filesystem when using Docker:
    - Directories must exist:

--- 
## Performance Considerations:
>- ***Concurrency:*** 
>   - The utility uses goroutines to monitor multiple directories concurrently, scaling well for small-to-medium directory counts. 
>   - However, each `fsnotify.Watcher` consumes system resources (`e.g.`, inotify watches on Linux), so monitoring many directories may hit system limits (`e.g.`, fs.inotify.max_user_watches). Increase limits by `sysctl` if needed:

>- ***Event Processing***: 
>   - The `fsnotify` loop in WatchDirectory processes events in real-time but includes a 1-second sleep in the default case to reduce CPU usage. 
>   - High event rates (`e.g.`, frequent file writes) may queue events, causing some delays:

>- ***File Content Reading:*** 
>   - Reading entire files for diffing (os.ReadFile) is memory-intensive for large text files. 
>   - The snapshots map stores file contents in memory, which could grow significantly for many or large files. 
>   - Consider limiting diffing to smaller files or using streaming for large files.

>- ***Logging Overhead:*** 
>   - Dual logging (terminal and fs_watcher.log) for most events may slow performance on disk-bound systems. 
>   - The LogOnly function for binary files reduces terminal output, optimizing high-frequency events.

>- ***Directory Scanning:*** 
>   - AnalyzeDir recursively scans directories, which is efficient for small trees but may be slow for directories with thousands of files. 
>   - Caching directory stats could improve performance for repeated scans.

>- ***Docker Efficiency:*** 
>   - The Alpine-based container minimizes resource usage, but volume mounts for watched directories should avoid network filesystems, as fsnotify performs poorly with them:

>- ***Idle Detection:*** 
>   - Idle messages are logged after 10 seconds of inactivity, which may be frequent for quiet directories. 
>   - Adjust the idleDuration threshold in [watcher.go](/build/gotools/internal/watcher/watcher.go) (`e.g`., to 30 seconds) to reduce logging overhead:

### Optimization Tips:
- Limit the number of watched directories in [cfg.yml](/build/gotools/cfg.yml) to avoid exhausting inotify watches.
- Use SSDs for fs_watcher.log to reduce disk I/O latency.
- For large files, modify DiffText to stream content instead of loading it entirely into memory:
- Monitor memory usage of the snapshots map and consider pruning old entries for long-running processes:


### Notes:
- Test Coverage:  
    - coverage.html, config, diff, and tracker have 100% coverage, but [main.go](/build/gotools/cmd/watcher/main.go) (`0%`) aso as [watcher.go](/build/gotools/internal/watcher/watcher.go) (`0%`) lacks coverage due to their runtime nature: 
    - `T.B.D` - might need to add integration tests later: 
<!-- Commented Code: Alternative implementations in diff, tracker, and reporter are commented out, likely for experimentation. The active versions are simpler and more robust (e.g., DiffText avoids line-based splitting). -->
- Binary Files: Extensions `.png`, `.exe`, `.zip` are logged to fs_watcher.log without diffs to optimize performance:
- Docker Binary Selection: - [monitor.Dockerfile](/build/sidecar/monitor.Dockerfile) dynamically selects the latest AMD64 binary, which is robust but assumes binaries are in `go_compiled`/`amd64`/ run [filewatcher_single_architecture_build.sh](/build/shell_tools/filewatcher_single_architecture_build.sh) script to ensure binaries exists during CI/CD:
- Log File: fs_watcher.log is written to the project root (or /side_monitor/ in Docker)
- Platform Compatibility: Tested on Linux Docker Alpine image and macOS: Windows wil fail unless Windows is. host machine and may require adjusting cfg.yml paths and fsnotify behavior:

#### Troubleshooting:
- Error: "Failed to load config": Ensure cfg.yml exists and is valid YAML.
- Error: "Failed to watch directory": Verify directory paths in cfg.yml are accessible.
- No events logged: Check if fsnotify supports the filesystem (e.g., avoid network-mounted drives).
- High memory usage: Monitor the snapshots map size and consider limiting diffing to smaller files.
- Inotify errors: Increase fs.inotify.max_user_watches on Linux if watching many directories.

### License:
- See LICENSE in the repository root for licensing details: