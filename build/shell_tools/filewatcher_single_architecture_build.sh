#!/bin/bash

# ─────────────────────────────────────────────────────────────────────────────
# Terminal colors
YELLOW='\033[93m'
GREEN='\033[92m'
MAGENTA='\033[95m'
_off='\033[0m'

# ─────────────────────────────────────────────────────────────────────────────
# ___ Args with defaults
ARCH=${1:-amd64}   # defaults to amd64
OS=${2:-linux}     # defaults to linux

# ─────────────────────────────────────────────────────────────────────────────
# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
TIMESTAMP=$(date +%Y_%m_%d_%H%M%S)
BASE_DIR="$REPO_ROOT/build/gotools/go_compiled"
OUTPUT_NAME="go_watcher"
[[ "$OS" == "windows" ]] && OUTPUT_NAME="go_watcher.exe"
OUTPUT_PATH="$BASE_DIR/$OS-$ARCH/$OUTPUT_NAME"
LOG_FILE="$BASE_DIR/build_summary_${OS}_${ARCH}_${TIMESTAMP}.log"

mkdir -p "$(dirname "$OUTPUT_PATH")"

# ─────────────────────────────────────────────────────────────────────────────
job_echo() {
  echo -e "${YELLOW}[${GREEN}JOB${YELLOW}]${_off}: ${MAGENTA}-->${_off} $1"
  }

# ─────────────────────────────────────────────────────────────────────────────
job_echo "Building Go watcher binary for: OS=${GREEN}${OS}${_off}, ARCH=${GREEN}${ARCH}\t${_off}--> ${MAGENTA}$(basename ${OUTPUT_PATH})${_off}"
job_echo "Log file: ${MAGENTA}$(basename ${LOG_FILE})${_off}"

cd "$REPO_ROOT/build/gotools" || exit 1

{
  echo -e "\n\tBuild started at $(date):"
  echo -e "\tGOOS=$OS GOARCH=$ARCH go build -trimpath -o $OUTPUT_PATH ./cmd/watcher"
  GOOS=$OS GOARCH=$ARCH go build -trimpath -o "$OUTPUT_PATH" ./cmd/watcher
  echo -e "\tBuild ended at $(date)\n"
} 2>&1 | tee "$LOG_FILE"

# ___ post build check:
if [[ -f "$OUTPUT_PATH" ]]; then
  job_echo "Build successful: $(basename "$OUTPUT_PATH")"
  ls -alh "$(dirname "$OUTPUT_PATH")"
else
  job_echo "Build failed: See log: $LOG_FILE"
fi

# ___ tree context:
echo -e "\n${GREEN}Directory Tree:${_off}"
tree "$BASE_DIR"
