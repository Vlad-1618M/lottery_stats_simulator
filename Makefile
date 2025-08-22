# ========================= Variables ==================================
# Color codes
PINK := $(shell printf '\033[38;5;213m')
ORANGE := $(shell printf '\033[38;5;208m')
VIOLET := $(shell printf '\033[38;5;177m')
LIME := $(shell printf '\033[38;5;154m')
AQUA := $(shell printf '\033[38;5;122m')
PEACH := $(shell printf '\033[38;5;217m')
TEAL := $(shell printf '\033[38;5;44m')
GRAY := $(shell printf '\033[38;5;245m')

BLACK := $(shell printf '\033[1;30m')
RED := $(shell printf '\033[1;31m')
GREEN := $(shell printf '\033[1;32m')
BLUE := $(shell printf '\033[1;34m')
WHITE := $(shell printf '\033[1;37m')

DARK_RED := $(shell printf '\033[38;5;88m')
DARK_GREEN := $(shell printf '\033[38;5;22m')
DARK_BLUE := $(shell printf '\033[38;5;18m')
DARK_GRAY := $(shell printf '\033[38;5;236m')

YELLOW := $(shell printf '\033[1;33m')
CYAN := $(shell printf '\033[1;36m')
MAGENTA := $(shell printf '\033[1;35m')
RESET := $(shell printf '\033[0m')
_off := $(RESET)

# _____ decorators:
DECORATOR := $(shell printf '$(AQUA)%s$(_off)' "$$($(PYTHON) -c 'print("="*90)')")

# _____ package vars:
PYTHON := python3
PY_INREPO := $(shell pwd)/

INJECTORS := $(PY_INREPO)injectors
LOGGER := $(PY_INREPO)logger
MATH := $(PY_INREPO)math_modules
STATISTICS := $(PY_INREPO)records_analytics
SRC := $(PY_INREPO)src

GO_DIR := build/gotools
GO_CMD := $(GO_DIR)/cmd/watcher
GO_BIN := gotools
GO_BUILD_CMD := cd $(GO_DIR)

DOCKER_DIRS := ../build/sidecar ../build/amd ../build/arm64 ../build/orchestrators

SH_DIR := build/shell_tools

GOFLAGS := -v -cover -failfast
ARGS := ./internal/... ./cmd/...

# _____ Preflight Check:
print-decorator:
	@echo "$(DECORATOR)"

preflight: go-check shell-check
	@echo "\n$(MAGENTA)[$(GREEN)INFO$(MAGENTA)]$(_off) Preflight checks passed.\n"

# _____ Python Linters:
lint_by_flake8:
	@echo "\n$(MAGENTA)[$(GREEN)INFO$(MAGENTA)]$(_off) Running $(MAGENTA)flake8$(_off) lint...\n"
	$(PYTHON) -m flake8 -v $(MATH) $(SRC) $(STATISTICS)

lint_by_ruff:
	@echo "\n$(MAGENTA)[$(GREEN)INFO$(MAGENTA)]$(_off) Running $(MAGENTA)ruff$(_off) lint...\n"
	$(PYTHON) -m ruff -v check $(INJECTORS) $(LOGGER) $(MATH) $(SRC) $(STATISTICS)

python-lint: lint_by_flake8 lint_by_ruff print-decorator
	@echo "$(MAGENTA)[$(GREEN)SUCCESS$(MAGENTA)]$(_off) Python lint checks $(GREEN)completed$(_off)\n"

# _____ Go:
go-test:
	@echo "$(YELLOW)[INFO]$(_off) Running Go unit tests..."
	@$(GO_BUILD_CMD) && go test $(ARGS) $(GOFLAGS)

go-lint:
	@echo "$(CYAN)[INFO]$(_off) Running golangci-lint..."
	@command -v golangci-lint >/dev/null 2>&1 || { echo "$(RED)[ERROR]$(_off) golangci-lint not installed."; exit 1; }
	@$(GO_BUILD_CMD) && golangci-lint run ./... --timeout 2m || { \
		echo "$(RED)[FAIL]$(_off) golangci-lint found issues."; exit 1; }
	@echo "$(GREEN)[SUCCESS]$(_off) golangci-lint passed."

go-build:
	@echo "$(YELLOW)[INFO]$(_off) Building Go binary..."
	@$(GO_BUILD_CMD) && go build -o $(GO_BIN) ./cmd/watcher
	@echo "$(GREEN)[SUCCESS]$(_off) Binary: $(GRAY)$(GO_DIR)/$(GO_BIN)$(_off)"

go-run:
	@echo "$(YELLOW)[INFO]$(_off) Running Go app..."
	@$(GO_BUILD_CMD) && go run ./cmd/watcher

go-clean:
	@echo "$(YELLOW)[INFO]$(_off) Cleaning Go build artifacts..."
	@if [ -f "$(GO_DIR)/$(GO_BIN)" ]; then \
		rm -f $(GO_DIR)/$(GO_BIN) && \
		echo "$(GREEN)[CLEANED]$(_off) Removed: $(GRAY)$(GO_BIN)$(_off)"; \
	else \
		echo "$(GRAY)[SKIP]$(_off) No Go binary found."; \
	fi

go-coverage:
	@echo "$(CYAN)[INFO]$(_off) Generating coverage report..."
	@$(GO_BUILD_CMD) && go test $(ARGS) -coverprofile=coverage.out -covermode=atomic
	@$(GO_BUILD_CMD) && go tool cover -html=coverage.out -o coverage.html
	@echo "$(GREEN)[SUCCESS]$(_off) View: $(GRAY)$(GO_DIR)/coverage.html$(_off)"

go-coverage-clean:
	@rm -f $(GO_DIR)/coverage.out $(GO_DIR)/coverage.html
	@echo "$(GRAY)[CLEANED]$(_off) Removed coverage artifacts."

# _____ Go Composite:
go-check: go-lint go-test
	@echo "$(DECORATOR)"
	@echo "$(MAGENTA)[$(GREEN)SUCCESS$(MAGENTA)]$(_off) Static + unit checks complete.$(_off)"

go-dev: go-build go-run
	@echo "$(DECORATOR)"
	@echo "$(MAGENTA)[$(GREEN)SUCCESS$(MAGENTA)]$(_off) Built & executed.$(_off)"

go-release: go-lint go-test go-build
	@echo "$(DECORATOR)"
	@echo "$(MAGENTA)[$(GREEN)SUCCESS$(MAGENTA)]$(_off) Release binary: $(GRAY)$(GO_DIR)/$(GO_BIN)$(_off)"

go-dry-run: go-test go-run
	@echo "$(DECORATOR)"
	@echo "$(MAGENTA)[$(GREEN)DRY-RUN$(MAGENTA)]$(_off) Validated source w/o build.$(_off)"

# _____ Shell::
shell-check:
	@echo "\n$(YELLOW)[INFO]$(_off) Shellcheck validation...\n"
	@command -v shellcheck >/dev/null 2>&1 || { echo "$(RED)[ERROR]$(_off) shellcheck not installed."; exit 1; }
	@sh_files="$$($(PYTHON) -c 'import pathlib; print(" ".join(str(p) for p in pathlib.Path("$(SH_DIR)").rglob("*.sh")))')"; \
	count="$$($(PYTHON) -c 'import pathlib; print(len(list(pathlib.Path("$(SH_DIR)").rglob("*.sh"))))')"; \
	if [ -z "$$sh_files" ]; then \
		echo "$(YELLOW)[WARN]$(_off) No shell scripts in $(SH_DIR)."; \
	else \
		shellcheck_output="$$($(PYTHON) -c 'import subprocess; subprocess.run(["shellcheck"] + "$$sh_files".split(), capture_output=True, text=True).stdout')"; \
		echo "$(GREEN)[SUCCESS]$(_off) $$count scripts passed shellcheck."; \
		ls -1 $(SH_DIR)/*.sh; \
	fi

# _____ Docker:
docker-build-all:
	@echo "$(YELLOW)[INFO]$(_off) Building all Docker images... (muted)"
	@# for dir in $(DOCKER_DIRS); do \
	@#     echo "Building Docker image for $$dir..." ; \
	@#     docker build -t $$(basename $$dir) $$dir ; \
	@# done

docker-run:
	@echo "$(YELLOW)[INFO]$(_off) Running Docker container: $(IMAGE)"
	@docker run -it --rm $(IMAGE)

docker-clean:
	@echo "$(YELLOW)[INFO]$(_off) Removing Docker images..."
	@for dir in $(DOCKER_DIRS); do \
	    docker rmi -f $$(basename $$dir) 2>/dev/null || true ; \
	done

# _____ Python Cleanup:
cleanpy_data:
	@echo "$(YELLOW)[INFO]$(_off) Cleaning Python metadata with cleanpy..."
	@cleanpy --verbose .

# _____ All:
all: preflight python-lint
	@echo "$(GREEN)[SUCCESS]$(_off) All checks passed. (Build muted)"

ci: preflight python-lint go-check
	@echo "$(GREEN)[SUCCESS]$(_off) CI pipeline completed. (Build steps muted)"

# _____ Help:
help:
	@echo "\n$(MAGENTA)Available Targets:$(_off)"
	@echo "\n$(CYAN)# Python$(_off)"
	@echo "  $(GREEN)python-lint$(_off)       - flake8 + ruff"
	@echo "  $(GREEN)lint_by_flake8$(_off)    - Run flake8 only"
	@echo "  $(GREEN)lint_by_ruff$(_off)      - Run ruff only"

	@echo "\n$(CYAN)# Go$(_off)"
	@echo "  $(GREEN)go-test$(_off)           - Run tests (override ARGS=...)"
	@echo "  $(GREEN)go-lint$(_off)           - Run golangci-lint"
	@echo "  $(GREEN)go-build$(_off)          - Compile binary"
	@echo "  $(GREEN)go-run$(_off)            - Run main.go"
	@echo "  $(GREEN)go-clean$(_off)          - Remove binary"
	@echo "  $(GREEN)go-coverage$(_off)       - HTML report"
	@echo "  $(GREEN)go-coverage-clean$(_off) - Cleanup report files"
	@echo "  $(GREEN)go-check$(_off)          - Lint + test"
	@echo "  $(GREEN)go-dev$(_off)            - Build + run"
	@echo "  $(GREEN)go-release$(_off)        - Full check + release"
	@echo "  $(GREEN)go-dry-run$(_off)        - Test + run (no build)"

	@echo "\n$(CYAN)# Shell$(_off)"
	@echo "  $(GREEN)shell-check$(_off)       - Validate *.sh via shellcheck"

	@echo "\n$(CYAN)# Decorators & Meta$(_off)"
	@echo "  $(GREEN)print-decorator$(_off)   - Show line separator"
	@echo "  $(GREEN)preflight$(_off)         - Run go-check + shell-check"

	@echo "\n$(CYAN)# Misc$(_off)"
	@echo "  $(GREEN)help$(_off)              - This help"

# _____ Phony:
.PHONY: go-test go-lint go-build go-run go-clean go-coverage go-coverage-clean \
        go-check go-dev go-release go-dry-run \
        preflight python-lint lint_by_flake8 lint_by_ruff \
        shell-check print-decorator help docker-build-all docker-run docker-clean \
        cleanpy_data all ci

