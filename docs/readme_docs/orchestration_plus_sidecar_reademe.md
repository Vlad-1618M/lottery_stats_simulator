# Lotto Simulator Orchestration:
- [Docker Compose](/build/orchestrators/docker-compose.yml) orchestrates the following services:
    - [File Watcher Go Utility](/docs/readme_docs/file_watcher_go_utility_readme.md)
    - [Data Collector](/docs/readme_docs/playwright_based_dockerfile_builds_reademe.md)
- [Sidecar](/build/sidecar/monitor.Dockerfile) 
    - lightweight Alpine-based container for the - [File Watcher Go Utility](/docs/readme_docs/file_watcher_go_utility_readme.md) service, monitoring filesystem changes in shared directories:
 
## Features:
- [Docker Compose](/build/orchestrators/docker-compose.yml) orchestrator:
    - Orchestrates [Data Collector](/docs/readme_docs/playwright_based_dockerfile_builds_reademe.md) and [File Watcher Go Utility](/docs/readme_docs/file_watcher_go_utility_readme.md)
    - Shares a lotto_data volume path for data persistence between services:
    - Sets up lotto_network for service communication:
    - Configured to wait for [File Watcher Go Utility](/docs/readme_docs/file_watcher_go_utility_readme.md) start after the main reopo container - [Data Collector](/docs/readme_docs/playwright_based_dockerfile_builds_reademe.md) is build compelted:


## Monitor -  [Sidecar](/build/sidecar/monitor.Dockerfile) Dockerfile:
- Builds a minimal Alpine-based container for the Go file watcher utility:
- Copies a precompiled go_watcher [binary](/build/shell_tools/filewatcher_single_architecture_build.sh) and [cfg.yml](/build/gotools/cfg.yml):
- Dynamically selects the latest AMD64 binary from build/gotools/go_compiled/*amd64/:
- Monitors directories (e.g., /`lotto`, /`root`) paths specified in [cfg.yml](/build/gotools/cfg.yml) for filesystem events: 
- For more info: 
    -   see [sidecar_stand_along_watcher_build_demo.mp4](/docs/mp4/sidecar_stand_along_watcher_build_demo_2x.mp4)
    -   see [go_watcher_run_example.mp4](/docs/mp4/go_watcher_run_example_2x.mp4)


## Dependencies
- Docker Compose:
    - Docker Compose 2.+ [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
        - written and tested on ***`Docker Compose version v2.38.2-desktop.1`***
    - Build context: 
        - [lotto_simulator repo](????) root
    - Files: 
        - [build/arm64/ubu_arm64_playwright.Dockerfile](/build/arm64/ubu_arm64_playwright.Dockerfile)
        - [build/amd64/ubu_amd64_playwright.Dockerfile](/build/amd64/ubu_amd64_playwright.Dockerfile)
        - [sidecar monitor](/build/sidecar/monitor.Dockerfile) 
        - [build/gotools/cfg.yml](/build/gotools/cfg.yml)
        - build/gotools/go_compiled/*amd64/go_watcher: 
            - see [compiler_architecture](/build/shell_tools/filewatcher_compiler_architecture.sh) 
            - see [single_architecture](/build/shell_tools/filewatcher_single_architecture_build.sh)

- Docker:
    - Docker 20.+ [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/):
        - written and tested on ***`Docker version 28.3.2`***
    - Files: 
    - [build/gotools/cfg.yml](/build/gotools/cfg.yml)
    - build/gotools/go_compiled/*amd64/go_watcher 
        - see [compiler_architecture](/build/shell_tools/filewatcher_compiler_architecture.sh) 
        - see [single_architecture](/build/shell_tools/filewatcher_single_architecture_build.sh)
    - Base image: ***`alpine:latest`***


## Installation:
- Clone the Repository:
```bash
git clone git@github.com:Vlad-1618M/lottery_stats_simulator.git
```
- cd lotto_simulator"
```bash
cd lottery_stats_simulator
```
- Check your sys architecure:
    ```bash
    uname -a
    ```
- Repo Files Exist Check:
    - [build/arm64/ubu_arm64_playwright.Dockerfile](/build/arm64/ubu_arm64_playwright.Dockerfile)
    - [build/amd64/ubu_amd64_playwright.Dockerfile](/build/amd64/ubu_amd64_playwright.Dockerfile)
    - [sidecar monitor](/build/sidecar/monitor.Dockerfile)
    - [build/gotools/cfg.yml](/build/gotools/cfg.yml)
    - compiled go_watcher binary:
        - see [file_watcher_go_utility_readme.md](/docs/readme_docs/file_watcher_go_utility_readme.md)
        - see [filewatcher_compiler_architecture.sh](/build/shell_tools/filewatcher_compiler_architecture.sh) 
        - see [filewatcher_single_architecture_build.sh](/build/shell_tools/filewatcher_single_architecture_build.sh)


## Build Refs:
- run orchestrated services using [Docker Compose](/build/orchestrators/docker-compose.yml)
    - see [go_watcher_run_example.mp4](/docs/mp4/go_watcher_run_example_2x.mp4)
- or build [sidecar monitor](/build/sidecar/monitor.Dockerfile) container independently
    - see [sidecar_stand_along_watcher_build_demo.mp4](/docs/mp4/sidecar_stand_along_watcher_build_demo_2x.mp4)

## Docker Compose CLI Examples:
- get go binaries into ***`build/gotools/go_compiled/`*** dir:
```bash
./build/shell_tools/filewatcher_single_architecture_build.sh
```
- Build and start both [Data Collector](/docs/readme_docs/playwright_based_dockerfile_builds_reademe.md) and [File Watcher Go Utility](/docs/readme_docs/file_watcher_go_utility_readme.md) services.
```bash
docker-compose -f build/orchestrators/docker-compose.yml up --build 
```
>- mp4 example:
[docker_compose_setup](/docs/mp4/docker_compose_setup_example.mp4)

![runtime_example](/docs/png_docs/docker_compose_runtime_example.png)

- if needed - run in detached mode:
```bash
docker-compose -f build/orchestrators/docker-compose.yml up -d
```
Stop. Remove services and networks:
```bash
docker-compose -f build/orchestrators/docker-compose.yml down
[+] Running 3/3
 ✔ Container watcher_sidecar            Removed
 ✔ Container container_lotto            Removed
 ✔ Network orchestrators_lotto_network  Removed
```

----

## Monitor Dockerfile CLI Examples:

- get go binaries into ***`build/gotools/go_compiled/`*** dir:
```bash
./build/shell_tools/filewatcher_single_architecture_build.sh
```
Build the - [File Watcher Go Utility](/docs/readme_docs/file_watcher_go_utility_readme.md) [container](/build/sidecar/monitor.Dockerfile):
```bash
docker build -t watcher_sidecar -f build/sidecar/monitor.Dockerfile .
```
![sidecar_setup](/docs/png_docs/sidecar_setup_example.png)

### Performance Considerations:

* Docker Compose:
    - Service Dependency: 
        - `depends_on` in [docker-compose.yml](/build/orchestrators/docker-compose.yml) checks `watcher_sidecar` starts after `repo_container`:
    - Network Overhead: 
        - `lotto_network` is a bridge network, sufficient for small-scale setups: 
        - enything more or high-traffic - may need different/optimized to scale network settings:


* Monitor Dockerfile:
    - Alpine Base: 
        - `alpine:latest` image minimizes container size (~5MB base + binary), reducing startup time and resource usage:
    - Binary Selection: 
        - Dynamic selection of the latest AMD64 binary adds build-time overhead but helps with automation flexibility: 
        - If faster builds needed - hardcoed paths for each binary:
    - Filesystem Watching: 
        - `fsnotify` is used in go binary (`go_watcher`) which is nice tohave, but may hit `inotify limits` if on some headless Linux for many directories: 
        - Increase `fs.inotify.max_user_watches` if needed:
            - T.B.C
            ```go 
            package main
            import (
                "fmt"
                "os"
                "strconv"
                "strings"

                "gotools/internal/config"
                "gotools/internal/reporter"
                "gotools/internal/watcher"
                "sync"
            )

            func checkInotifyLimit() error {
                data, err := os.ReadFile("/proc/sys/fs/inotify/max_user_watches")
                if err != nil {
                    return fmt.Errorf("failed to read inotify limit: %v", err)
                }
                limit, err := strconv.Atoi(strings.TrimSpace(string(data)))
                if err != nil {
                    return fmt.Errorf("failed to parse inotify limit: %v", err)
                }
                // ____ change based on expected directory count:
                if limit < 8192 {
                    reporter.PrintError("Inotify watch limit (%d) is low. Consider increasing via: sudo sysctl -w fs.inotify.max_user_watches=524288", limit)
                }
                return nil
            }

            func main() {
                // ___ inotify limit check prior to  watchers start:
                if err := checkInotifyLimit(); err != nil {
                    reporter.PrintError("Inotify check failed: %v", err)
                }

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

### Optimization THoughts for any unknown infras + envs:
>   - Health checks in [docker-compose.yml](/build/orchestrators/docker-compose.yml) for `repo_container`may help to check for `watcher_sidecar` start only when ready:
>   - Docker’s `--cpus` and `--memory` flags to limit resource usage (e.g., `docker-compose up --build --memory=2g`).
>   - Understand your OS resourses before you go crazy on directories in [cfg.yml](/build/gotools/cfg.yml) to watchfor: `fsnotify` overhead will not like it: 
>   - Cache Docker layers by reusing images (`docker-compose up --no-build`) unles you do what I do `docker system prune -af --volumes` :0)



### Notes:

- Docker Compose:
    - `repo_container` service uses [ubu_arm64_playwright.Dockerfile](/build/arm64/ubu_arm64_playwright.Dockerfile) sinse this was build on macOS [docker-compose.yml](/build/orchestrators/docker-compose.yml) assums `ARM64` hardware: 
    - If youare on pure Linux `AMD64` -  update [docker-compose.yml](/build/orchestrators/docker-compose.yml) with [ubu_amd64_playwright.Dockerfile](/build/amd64/ubu_amd64_playwright.Dockerfile)
    - `lotto_data` volume persists data across container restarts but requires proper host directory mapping: if youare on Windows - use `Posix` paths:


- Monitor Dockerfile:
    - Assumes a precompiled `go_watcher` binary: Make sure binaries generated during CI/CD or amy other runs: 
        - see [docker_compose_setup](/docs/mp4/docker_compose_setup_example_2x.mp4)
        - see [filewatcher_compiler_architecture.sh](/build/shell_tools/filewatcher_compiler_architecture.sh) 
        - see [filewatcher_single_architecture_build.sh](/build/shell_tools/filewatcher_single_architecture_build.sh)


- Platform Compatibility: 
    - docker-compose.yml assumes ARM64 for `repo_container`. 
    * If short on Resources: 
        - Run containers with ***`--memory`*** and ***`--cpus`*** flags to limit resource usage (`e.g.`, ***docker run --memory=4g --cpus=2***):
        - For ***`ARM64`***: best to test performance on target hardware: 
            - Emulation on AMD64 hosts may degrade performance:
    - Log File: gets write permissions when mounted:

- * Resource Allocation Example:<br>
![dokcer_engine](/docs/png_docs/dockerengine_settings.png)

### Troubleshooting:
- Error: "`Cannot find go_watcher`": check build context for `build/gotools/go_compiled/*amd64/go_watcher`:
- Error: "`Cannot access /lotto`": check if `lotto_data volume` is correctly mounted and directories exist:
- Service startup issues: checks resource limists and [docker-compose.yml](/build/orchestrators/docker-compose.yml) for any race conditions around who goes first (`e.g.`, `repo_container` is ready before `watcher_sidecar`) starts:
- Inotify errors: Increase fs.inotify.max_user_watches on Linux if `watcher_sidecar` reports watch limits:

### License:
- See LICENSE in the repository root for licensing details.