# Playwright Dockerfiles (AMD64 & ARM64):
The [amd64_playwright](/build/amd64/ubu_amd64_playwright.Dockerfile) and [arm64_playwright](/build/arm64/ubu_arm64_playwright.Dockerfile) Dockerfiles provide containerized environments for running Playwright with Ubuntu and Python 3.13 support:
- Base: 
    - Both are built on `Ubuntu 22.04` where `Python 3.13` and pre-installed `Playwright` browsers configured for the runtime: 
    - Compatibility Note: 
        - Since the official Playwright base image [mcr.playwright](https://mcr.microsoft.com/en-us/artifact/mar/playwright/python/tags) only supports Ubuntu and Python 3.10, a custom multi-layer approach is used to merge system and runtime dependencies into a single container:
    - Use Case:
        - Works well for web scraping, browser automation, or other Playwright-driven tasks — with additional tools and fonts included for enhanced runtime support:
    - Architecture-Specific Differences: 
        - Both Dockerfiles are nearly identical, differing only in platform architecture (`AMD64` vs. `ARM64`) and minor dependency adjustments:

## Features:
- Multi-stage build: 
    - Installs [Playwright](https://github.com/microsoft/playwright-python) browsers (chromium, firefox, webkit) from [mcr.microsoft.com/playwright/python:v1.52.0-jammy](https://github.com/microsoft/playwright-python/blob/main/utils/docker/Dockerfile.jammy) and sets up a runtime environment:
    - Installs Python 3.13 with [deadsnakes/ppa](https://github.com/deadsnakes) for 'off rails' Python support:
    - Includes runtime tools: 
        - [bat](https://github.com/sharkdp/bat)
        - [make](https://github.com/ubuntu/ubuntu-make)
        - [shellcheck](https://github.com/koalaman/shellcheck)
        - [jq](https://jqlang.org/)
        - [tree](http://www.linuxguide.it/command_line/linux-manpage/do.php?file=tree)
        - [vim](https://vimhelp.org/)
        - [iputils-ping](https://packages.debian.org/sid/iputils-ping)
        - [cron](https://man7.org/linux/man-pages/man8/cron.8.html)
        - [netcat-openbsd](https://packages.debian.org/sid/netcat-openbsd)
    - Provides fonts (`fonts-liberation`, `fonts-dejavu`, `fonts-unifont`) for browser rendering:
    - Copies project files to `/lotto` workdir and installs Python dependencies from [requirements.txt](/deps/requirements.txt)
    - [entrypoint.sh](/build/shell_tools/entrypoint.sh) script designed for container startup:
    - Sets environment variables for Playwright (PLAYWRIGHT_BROWSERS_PATH), Python (PYTHONPATH), and Go (PATH):
    - Supports both [AMD64](/build/amd64/ubu_amd64_playwright.Dockerfile) and [ARM64](/build/arm64/ubu_arm64_playwright.Dockerfile) architectures:

## Dependencies:
- Docker 20.10+ (docker install):
- written and tested on ***`Docker version 28.3.2`***
- Project files:
    - [Python dependencies](/deps/requirements.txt)
    - [entrypoint.sh](/build/shell_tools/entrypoint.sh) shell script:
    - `lotto_simulator` - repository root as build context:
- mcr.microsoft.com/playwright/python:v1.52.0-jammy External base images:
- Playwright Version 1.52.0
- ubuntu:22.04

## Installation:
- Clone the Repository:
```bash
git clone git@github.com:Vlad-1618M/lottery_stats_simulator.git
```
- cd lottery_stats_simulator"
```bash
cd lottery_stats_simulator
```
- Check your sys architecure:
    ```bash
    uname -a
    ```
- Run Dockerfile:
    - [amd64_playwright](/build/amd64/ubu_amd64_playwright.Dockerfile)
        ```bash
        docker build -t lotto_amd64 -f build/amd64/ubu_amd64_playwright.Dockerfile .
        ```
    - [arm64_playwright](/build/arm64/ubu_arm64_playwright.Dockerfile)
        ```bash
        docker build -t lotto_arm64 -f build/arm64/ubu_arm64_playwright.Dockerfile .
        ```
- Container Access: 
    - in shell: 
        ```bash
        docker run -it lotto_arm64 bash
        ```
    - in shell + full host to container access: 
        ```bash
        docker run -it -v $(pwd):/lotto lotto_arm64 bash
        ```
    - in shell + data dir volume mount: all work is stored in data dir path: 
        -   NOTE: This enables file sharing between host and container:
        ```bash
        docker run -it -v $(pwd)/data:/lotto lotto_arm64 bash
        ```
        or
        ```bash
        docker run -it --rm -v $(pwd)/data:/lotto --name lotto_dev lotto_arm64 bash
        ```
    - Run in Detached Mode:
        - `tail -f /dev/null` is to keep container running for later debug or dev work:
        ```bash
        docker run -d --name lotto_job -v $(pwd)/data:/lotto/data lotto_arm64 tail -f /dev/null
        ```
        ```bash
        docker run -d --name lotto_arm64 tail -f /dev/null
        ```

- Cleanup:
    ```bash
    docker stop lotto_job && docker rm lotto_job
    docker rmi lotto_amd64
    docker system prune -af
    ```

## Notes:
- Platform Selection: 
    - For ***AMD64*** systems (`e.g`., ***Intel***/***AMD CPUs***) use [ubu_amd64_playwright.Dockerfile](/build/amd64/ubu_amd64_playwright.Dockerfile)  
    - For ***ARM64*** systems (`e.g`., ***Apple Mx***/, ***Raspberry Pi***) [ubu_arm64_playwright.Dockerfile](/build/arm64/ubu_arm64_playwright.Dockerfile) 
- [Entrypoint](/build/shell_tools/entrypoint.sh) is a DEMO for this repository’s capabilities:
    - Container executes [entrypoint.sh](/build/shell_tools/entrypoint.sh) has startup logic for runnign the following code sequnce:
        >- Sieve of Eratosthenes Calculation Method Explained: --> [quickPick.py](/src/quickPick.py) "***--sieve***"
        >- Sieve of Eratosthenes Calculation Method Explained in Spanish: --> [quickPick.py](/src/quickPick.py "***--sieve --lang es***"
        >- Collect Recent Lottery Draw Results + Screenshots: --> [get_lotto_results.py](/src/get_lotto_results.py) "***--shots***"
        >- Create Player's Catalog | All Users JSON datasets: --> [quickPick.py](/src/quickPick.py) "***--auto --all-names***"
        >- Lotto Sequence Analytics Scripts: 
        >   - [collect_statistics.py](/src/collect_statistics.py) "***--list***"
        >   - [collect_statistics.py](/src/collect_statistics.py) "***---games megamillion powerball --save-html***"
        >- Show Existing Catalog Details:
        >   - [catalog_manager.py](/src/records_analytics/catalog_manager.py) "***--items***"
        >   - [catalog_manager.py](/src/records_analytics/catalog_manager.py) "***--show-ids***"
        >   - [catalog_manager.py](/src/records_analytics/catalog_manager.py) "***--show-details***"
        >- Installing Golang pkgs: --> [install_go.sh](/build/shell_tools/install_go.sh)
        >   - Run Lotto Sequence Comparator for mixed game pool: [main.go](/src_for_go/main.go) "***--games powerball,megamillion,lotto --html***"
        >   - Run Lotto Sequence Comparator for megamillion + html report: --> [main.go](/src_for_go/main.go) "***--games megamillion --html***"
        >   - Run Lotto Sequence Comparator for megamillion - mega values + html report: --> [main.go](/src_for_go/main.go) "***--games megamillion --drop-mega --html***"
        >   - Run Lotto Sequence Comparator for megamillion - altered sequence depth + html report: --> [main.go](/src_for_go/main.go) "***--games megamillion --depth 4 --html***"
        >   - Run Lotto Sequence Comparator for powerball + html report: --> [main.go](/src_for_go/main.go) "***--games powerball --html***"
        >   - Run Lotto Sequence Comparator for powerball - powerball values + html report: --> [main.go](/src_for_go/main.go) "***--games powerball --drop-power --html***"
        >   - Run Lotto Sequence Comparator for powerball - altered sequence depth + html report: --> [main.go](/src_for_go/main.go) "***--games powerball --depth 4 --html***"
        >   - Run Lotto Sequence Comparator for lotto + html report: --> [main.go](/src_for_go/main.go) "***--games lotto --html***"
        >   - Run Lotto Sequence Comparator for lotto - altered sequence depth + html report: --> [main.go](/src_for_go/main.go) "***--games lotto --depth 6 --html***"
        >- Pull draw results from ***`lotto_draw_results`*** dir with `.jq` lib for nicer print/output:

___
- Volume Mounts: Mount a host directory (`e.g.`, $(pwd)/data) to /lotto/data for persistent data storage:
- Performance Considerations:
    - Multi-Stage Build: 
        - The multi-stage build minimizes the final image size by copying only Playwright browsers from the first stage, reducing disk usage:
    - Package Installation: 
        - ***`--no-install-recommends`*** plus cleaning ***`/var/lib/apt/lists/*`*** reduces image size and build time:
- Playwright Browsers: 
        - Pre-installing browsers: (`chromium`, `firefox`, `webkit`) avoids runtime installation, improving startup performance but increasing image size:
- Python Dependencies: 
        - ***`--no-cache-dir`*** flag for ***`pip install`*** prevents caching, reducing image size, could be slower on rebuilds if dependencies changes frequently:

- Resource Usage: 
        - Playwright browsers are memory-intensive: Be aware of Docker settings on your host machine, check toi be sure if container has sufficient RAM allowed (`e.g`., 4GB+) for concurrent browser instances:

- * Resource Allocation Example:<br>
![dokcer_engine](/docs/png_docs/dockerengine_settings.png)
----

### Potential Optimization Thoughts: T.B.D:
* Fonts:
    - Fonts are for proper rendering but add minor overhead: 
    - MIght need to revist or remove unused fonts `fonts-unifont` if not needed or go by case specific:
* If short on Resources: 
    - Run containers with ***`--memory`*** and ***`--cpus`*** flags to limit resource usage (`e.g.`, ***docker run --memory=4g --cpus=2***):
    - For ***`ARM64`***: best to test performance on target hardware: 
        - Emulation on AMD64 hosts may degrade performance:

### Troubleshooting:
- Error: "Cannot find ***`/lotto/entrypoint.sh`***": Check if [build/shell_tools/entrypoint.sh](/build/shell_tools/entrypoint.sh) exists in build context:
- Error: ***"`pip install failed`"***: Verify [deps/requirements.txt](/deps/requirements.txt) is valid and or accessible:
- Browser failures: Check ***`PLAYWRIGHT_BROWSERS_PATH=/ms-playwright`*** is set and browsers are copied correctly from the first stage:
- ***ARM64*** issues: 
    - On AMD64 hosts: - enable Docker’s `QEMU` emulation (****`docker run --platform linux/arm64`****) or build on native `ARM64` hardware:

### License:
- See LICENSE in the repository root for licensing details:

___
