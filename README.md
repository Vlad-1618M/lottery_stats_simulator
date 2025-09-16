# Simulator for benchmarking algorithms using dynamic integer datasets:
**This Simulator** is a modular toolkit designed to run algorithms across large integer datatypes as set sequences, using lottery games as a realistic and structured primary data source. <br>
Repo generates, manages, and analyzes large collections of simulated player records, with multilingual support, statistical analysis, and sequence-matching engines for data processing:<br>

Equipped with Go-based engine for analyzing, comparing, and benchmarking large sets of lottery game data (`Lotto`, `Mega Million`, `Powerball`)<br>
Reads player ticket (`.json`) files, compares all possible pairs for "`exact`" and "`partial`" matches:<br> 
Supports terminal and HTML reports/records stats:

> **Features**:
> - Multi-lingual filename and number set support:
> - Unicode/RTL-safe alignment for all terminal outputs:
> - Flexible matching: primary only, primary+bonus, partial match stats:
> - Custom CLI flags for game logic, depth, and reporting:
> - Probability and odds notes and details:

---

## Table of Contents:
- [Overview:](#overview)
- [How Code Works](#how-the-code-works)
- [Combination vs. Permutation](#combination-vs-permutation)
- [Core Features](#core-features)
- [Repository Structure](#repository-structure)
- [Data Sources](#data-sources)
- [Math Modules](#math-modules)
- [Go ReadMe](#go)
- [Python ReadMe](#python)
- [Automation & Orchestration](#automation--orchestration)
- [Docker Builds](#docker-builds)
- [Documentation by Module](#documentation-by-module)
- [Lotto Math Formulas](#lotto-math-formulas)
- [License](/LICENSE)

---

## Overview:
The idea behind **Simulator** was to create realistic, high-volume, test-ready datasets:<br> 
Lottery game rules and sequences were adapted, as they provide a core data structure and support naturally evolving data flows:
> - Large numerical combinations.
> - Diverse selection rules per game.
> - Easily simulated real-world scenarios.

To make the simulations as lifelike as possible, the repo creates `.json`s datasets of *player profiles* — each representing a lottery participant with unique name and history of game selections and its outcomes:<br>
The [player](/injectors/players.yml) data and [game](/globs/games.yml) limits are defined in relativly large `.yml` configuration files enabling quick customization and realistic first name user diversity:

## How the Code Works:
- **Reads** all player ticket `.json`s under `catalog/` path:
- Each `.json` contains one or more ticket entries, each with primary and bonus numbers, `e.g.`, `Mega` or `Power` game entries:
- All primary numbers are ***sorted*** before comparison: - (order does ***not*** matter in standard lottery games)
- The code performs **pairwise comparison** of every ticket set against every other ticket set for each selected game:
- Reports are output with **Unicode/locale-safe alignment** using [`runewidth`](https://github.com/mattn/go-runewidth) for visual formatting:
---

## Combination vs. Permutation:
**Lottery games are about combinations, NOT permutations**
- *Combination*: Order does **not** matter. `[5, 10, 22, 31, 36, 42]` = `[10, 5, 22, 36, 42, 31]`
- *Permutation*: Order matters. Not used in lottery matching, so, ***`different story` and perhaps some fun code to write later***: 


## Core Features:
- [**High-Volume Data Simulation**](/src/quickPick.py): - Generates thousands of unique player records with name localization:
- [**Configurable Game Rules**](/globs/games.yml): - Define primary/secondary draws, number ranges, and game variants:
- [**Hybrid Processing**](/src_for_go/main.go): Go-based sequence matching + [Python-based](/src/collect_statistics.py) simulation and analytics:
- [**Mathematical Enhancements**](/math_modules/number_generator.py): Optional [prime-number](/math_modules/prime_sequence_check.py)-focused selections, randomizers and [quick-pick](/src/quickPick.py) logic:
- [**Multilingual Support**](/injectors/render_translit.py): Using [`deep_translator`](https://pypi.org/project/deep-translator/) for name/game translations and localized reporting:
- [**Automated Runs**](/auto_jobs/cron_schedule_check.sh): CRON-based execution scripts for unattended data generation and analysis:
- [**Dockerized Environment**](/build/): Build targets for [AMD64](/build/amd/amd_setup.Dockerfile), [ARM64](/build/arm64/), [sidecar](/build/sidecar/monitor.Dockerfile) monitoring and [orchestrated](/build/orchestrators/docker-compose.yml) composer:

---

## Repository Structure:

| directory:        |             description:                                                                                              |
|-------------------|-----------------------------------------------------------------------------------------------------------------------|
| [CROn auto jobs](/auto_jobs/)                 | ***Automated job schedules, shell scripts & notes:***                                     |
|                                               | [cron_schedule_check.sh](/auto_jobs/cron_schedule_check.sh)                               |
|                                               | [run.sh](/auto_jobs/run.sh)                                                               |
| [build Docker](/build/)                       | ***Docker OS Architecture Configurations:***                                              |
|                                               | [amd64](/build/amd64/ubu_amd64_playwright.Dockerfile)                                     |
|                                               | [arm64](/build/arm64/ubu_arm64_playwright.Dockerfile)                                     |
| [build go watcher](/build/gotools/)           | ***Golang file system watcher utility:***                                                 |
|                                               | [gotools](/build/gotools/)                                                                |
|                                               | [cfg.yml](/build/gotools/cfg.yml)                                                         |
|                                               | [cmd](/build/gotools/cmd/)                                                                |
|                                               | [watcher](/build/gotools/cmd/watcher/)                                                    |
|                                               | [main.go](/build/gotools/cmd/watcher/main.go/)                                            |
|                                               | [coverage.html](/build/gotools/coverage.html)                                             |
|                                               | [coverage.out](/build/gotools/coverage.out)                                               |
|                                               | [fs_watcher.log](/build/gotools/fs_watcher.log)                                           |
|                                               | [go.mod](/build/gotools/go.mod)                                                           |
|                                               | [go.sum](/build/gotools/go.sum)                                                           |
|                                               | [internal](/build/gotools/internal/)                                                      |
|                                               | [config](/build/gotools/internal/config/)                                                 |
|                                               | [config.go](/build/gotools/internal/config/config.go)                                     |
|                                               | [config_test.go](/build/gotools/internal/config/config_test.go)                           |
|                                               | [diff](/build/gotools/internal/diff/)                                                     |
|                                               | [diff.go](/build/gotools/internal/diff/diff.go)                                           |
|                                               | [diff_test.go](/build/gotools/internal/diff/diff_test.go)                                 |
|                                               | [reporter](/build/gotools/internal/reporter/)                                             |
|                                               | [reporter.go](/build/gotools/internal/reporter/reporter.go)                               |
|                                               | [reporter_test.go](/build/gotools/internal/reporter/reporter_test.go)                     |
|                                               | [tracker](/build/gotools/internal/tracker/)                                               |
|                                               | [filemeta.go](/build/gotools/internal/tracker/filemeta.go)                                |
|                                               | [tracker.go](/build/gotools/internal/tracker/tracker.go)                                  |
|                                               | [tracker_test.go](/build/gotools/internal/tracker/tracker_test.go)                        |
|                                               | [watcher](/build/gotools/internal/watcher/)                                               |
|                                               | [watcher.go](/build/gotools/internal/watcher/watcher.go)                                  |
| [build composer](/build/orchestrators/)       | ***Orchestrator:***                                                                       |
|                                               | [Docker Compose](/build/orchestrators/docker-compose.yml)                                 |
| [build shell tools](/build/shell_tools/)      | ***Pipeline shell scripts:***                                                             |
|                                               | [shell_tools](/build/shell_tools/)                                                        |
|                                               | [go auto arch compiler](/build/shell_tools/filewatcher_compiler_architecture.sh)          |
|                                               | [go arch compiler](/build/shell_tools/filewatcher_single_architecture_build.sh)           |
|                                               | [entrypoint.sh](/build/shell_tools/entrypoint.sh)                                         |
|                                               | [install_go.sh](/build/shell_tools/install_go.sh)                                         |
| [Sidecar GO Container](/build/sidecar/)       | ***Dedicated go utility runtime container:***                                             |
|                                               | [sidecar](/build/sidecar/monitor.Dockerfile)                                              |
| [Python Dependencies](/deps/)                 | ***Python's Requirements config:***                                                       |
|                                               | [requirements](/deps/requirements.txt)                                                    |
| [Repo Docs](/docs/)                           | ***Readme docs, refs & screenshots:***                                                    |
|                                               | [.md/.png/.mp4 - files](/docs/)                                                           |
| [Code Thoughts/Research](/experemental/)      | ***Experimental Python based scripts & prototypes:***                                     |
|                                               |`cruft` / `T.B.R` [cli by subprocess & cProfile](/experemental/cli_tools.py)               |
|                                               |`T.B.R` [algo animations](/experemental/statistics_simulator_by_matplotlib.py)             |
|                                               |`cruft` / `T.B.R` [Figlet ASCII ideas](/experemental/themed_decorator.py)                  |
|                                               |`T.B.R` [sequentially read str sets by vertical index](/experemental/vertical_reader.py)   |
| [Global CFG](/globs/)                         | ***Core game configuration limits:***                                                     |
|                                               |[games.yml](/globs/games.yml)                                                              |
| [Injected Modules](/injectors/)               |***Set of cfgs and modules:***                                                             |
|                                               |[constants.py](/injectors/constants.py) track num limits `used in` -> [glob_args.py](/src/glob_args.py)                                        |
|                                               |[epilogs.py](/injectors/epilogs.py) cli + gfx `used i`n -> [catalog_manager.py](/records_analytics/catalog_manager.py)                         |
|                                               |[html_utils.py](/injectors/html_utils.py) keep rich.console output for htmls `used in` -> [collect_statistics.py](/src/collect_statistics.py)  |
|                                               |[ilinois.py](/injectors/ilinois.py) headers, selector's paths and urls cfg `used in` -> [get_lotto_results.py](/src/get_lotto_results.py)      |
|                                               |[players.yml](/injectors/players.yml) user / player names config `used in` -> [glob_args.py](/src/glob_args.py)                                |
|                                               |[render_translit.py](/injectors/render_translit.py) GoogleTranslator API `used in` -> [user_records.py](/src/user_records.py) and [sieve_eratosthenes_algo_prime_numbers.py](/math_modules/sieve_eratosthenes_algo_prime_numbers.py) |
|                                               |[theme.css](/injectors/theme.css) theme assets for html reports:                                                                                                           |
|                                               |[why.py](/injectors/why.py) `sys.argv` cli info and args help msgs `used in` -> [glob_args.py](/src/glob_args.py)                                                          |
| [Logger](/logger/)                            | ***Log Module***:                                                                                                                                                         |
|                                               |[logger_main.py](/logger/logger_main.py)                                                                                                                                   |
| [Math Modules](/math_modules/)                |***Core mathematical sequence generators:***                                                                                                                               |
|                                               |[number_generator.py](/math_modules/number_generator.py) `used in` -> [quickPick.py](/src/quickPick.py)                                                                    |
|                                               |[payout.py](/math_modules/payout.py) lump sum vs nnuity payout with tax withholdings `standalong script`                                                                   |
|                                               |[prime_sequence_check.py](/math_modules/prime_sequence_check.py) `used in` -> [quickPick.py](/src/quickPick.py)                                                            |
|                                               |[sieve_eratosthenes_algo_prime_numbers.py](/math_modules/sieve_eratosthenes_algo_prime_numbers.py) `used in` -> [number_generator.py](/math_modules/number_generator.py)   |
| [Game Records](/records_analytics/)           | ***Data analytics, statistics, and deduplication checks:***                                                       |
|                                               |[catalog_manager.py](/records_analytics/catalog_manager.py) process existing `.json` records `standalong script`   |
|                                               |`cruft`[dedupes_check.py](/records_analytics/dedupes_check.py) check for duplicates in [players.yml](/injectors/players.yml) `standalong script` may not be applicable if full config is used `T.B.R`  |
|                                               |[search_open.sh](/records_analytics/search_open.sh) help script to search for `_.json` names for data debug analysis `standalong script`                                                               |
|                                               |[statistics.py](/records_analytics/statistics.py) data statistics module `used in` -> in args based [collect_statistics.py](/src/collect_statistics.py)                                                |
| [Python Main Source](/src/)                           | ***Python Main Source plus Lotto Statistics & Sequence Match Engine modules:***                                                                                                                       |
|                                               |[collect_statistics.py](/src/collect_statistics.py) cli based module designed to run sequential data matche statistics across all user records `depends` on [statistics.py](/records_analytics/statistics.py)  |
|                                               |[get_lotto_results.py](/src/get_lotto_results.py) Lotto Scraper module designed to collect latest winning numbers from official lottery source `depends` on [ilinois.py](/injectors/ilinois.py)                |
|                                               |[glob_args.py](/src/glob_args.py) global cli argsv configuration module designed to help with parse quickPick and table args, loads entrant user catalog `depends` on [constants.py](/injectors/constants.py)  |
|                                               |[quickPick.py](/src/quickPick.py) cli module designed to simulate lotto quick pick play, prime number force injections options, game run for single/all users configured in [players.yml](/injectors/players.yml) `depends` on [prime_sequence_check.py](/math_modules/prime_sequence_check.py) and [glob_args.py](/src/glob_args.py) |
|                                               |[user_records.py](/src/user_records.py) input based module designed to collect user data with language AutoTranslator API `depends` on [render_translit.py](/injectors/render_translit.py) [glob_args.py](/src/glob_args.py) |
| [Golang Main Source](/src_for_go/)            |***Lotto Statistics & Sequence Match Engine written in Golang:***  |
|                                               |[style.css](/src_for_go/assets/style.css) for html report exports: |
|                                               |[main.go](/src_for_go/main.go) main module see [main_go_readme.md](/src_for_go/main_go_readme.md) |
| [Repo Root](/)                                |***Root level file and configurations:***                          |
|                                               |[LICENSE](/LICENSE)                                                |
|                                               |[Makefile](/Makefile)                                              |
|                                               |[pyproject.toml](/pyproject.toml)                                  |
|                                               |[Main README](/README.md)                                          |
|                                               |[setup.cfg](/setup.cfg)                                            |
|---------------------------------

## Documentation by Module:
### Data Sources:
 - [Players Configuration](/injectors/players.yml):
 - [Games Configuration](/globs/games.yml):


### Math Modules:
- [Number Generator](/docs/readme_docs/number_generator_README.md)
- [Lottery Payout Calculator](/docs/readme_docs/lottery_payout_calculator_README.md)
- [Sieve of Eratosthenes](/docs/readme_docs/Sieve_of_Eratosthenes_README.md)

### Go:
- [Sequence Comparator](/docs/readme_docs/sequence_comparator_main_go_readme.md)
- [File Watcher](/docs/readme_docs/file_watcher_go_utility_readme.md)

### Python:
- [Glob Args](/docs/readme_docs/glob_args_README.md)
- [Quick Pick](/docs/readme_docs/quickPick_README.md)
- [User Records](/docs/readme_docs/user_records_README.md)
- [Collect Statistics](/docs/readme_docs/collect_statistics_README.md)
- [Get Lotto Draw Results](/docs/readme_docs/get_lotto_results_README.md)
- [Pull Historical Lotto Draw Results](/docs/readme_docs/historical_lotto_data_readme.md)

## Automation / Docker Builds:
- [Dockerfiles](/docs/readme_docs/playwright_based_dockerfile_builds_reademe.md)
- [Orchestration](/docs/readme_docs/orchestration_plus_sidecar_reademe.md)

---
* ***GitHub did not like my `.mp4` uploads***:
* YouTube: ***https://www.youtube.com/@Vlad-1618.M/playlists***

    ![youtube](/docs/png_docs/youtube_ref.png)

## Downloads Only: - mp4 Demos:
- [Orchestration Setup](/docs/mp4/docker_compose_setup_example_2x.mp4)
- [Sidecar Setup](/docs/mp4/sidecar_stand_along_watcher_build_demo_2x.mp4)
- [Entrypoint Build](/docs/mp4/demo_entrypoint_build_2x.mp4)
- [Entrypoint Runtime](/docs/mp4/entrypoint_runtime_demo_start_2x.mp4)
- [FS Watcher Run as code](/docs/mp4/go_watcher_as_code.mov_2x.mp4)
- [FS Watcher Binary Auto run](/docs/mp4/go_watcher_run_example_2x.mp4)

---

## Lotto Math Formulas:
> General Lottery Odds Formula:
>   - For a game where you pick `k` numbers from a set of `n` total balls:
- **Number of possible combinations:**

```math
C(n, k) = \frac{n!}{k!(n-k)!}
```

- Where:
- * `n!` = n factorial (e.g., 5! = 5×4×3×2×1 = 120)
- * `C(n, k)` = "n choose k" = number of unique combinations

> **Probability of matching all k numbers:**

```math
P(\text{match}) = \frac{1}{C(n, k)}
```

> **Including a separate bonus ball:**
If the game has a bonus (e.g., Mega or Power), and there are `b` bonus numbers:

```math
\text{Odds} = C(n, k) \times b
```

---
## Lotto Example (Pick 6 from 49, no bonus):

```math
C(49, 6) = \frac{49!}{6!(49-6)!} = 13,983,816
```

> - Odds of exact match:

```math
\frac{1}{13,983,816}
```

---

## Mega Millions Example (Pick 5 from 70 + Mega Ball from 25):

```math
C(70, 5) = \frac{70!}{5!(70-5)!} = 12,103,014
```

> - Total combinations (with Mega Ball):

```math
12,103,014 \times 25 = 302,575,350
```

> - Odds of exact match:

```math
\frac{1}{302,575,350}
```

---

## Powerball Example (Pick 5 from 69 + Powerball from 26):

```math
C(69, 5) = \frac{69!}{5!(69-5)!} = 11,238,513
```

> - Total combinations (with Powerball):

```math
11,238,513 \times 26 = 292,201,338
```

> - Odds of exact match:

```math
\frac{1}{292,201,338}
```
___
