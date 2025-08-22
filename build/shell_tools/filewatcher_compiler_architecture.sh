#!/bin/bash

YELLOW='\033[93m'
GREEN='\033[92m'
MAGENTA='\033[95m'
RED='\033[91m'
_off='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

TIMESTAMP=$(date +%Y_%m_%d_%H%M%S)
OUTPUT_BASE="go_watcher_${TIMESTAMP}"
BASE_DIR="$REPO_ROOT/build/gotools/go_compiled"
LOG_FILE="$BASE_DIR/build_summary_${TIMESTAMP}.log"

mkdir -p "$BASE_DIR"

job() {
  echo -e "${YELLOW}[${GREEN}JOB${YELLOW}]${_off}: ${MAGENTA}-->${_off} $1"
  echo "[JOB] --> $1" >> "$LOG_FILE"
}

build_binary() {
  local os="$1"
  local arch="$2"
  local suffix="$3"
  local binary_size

  local out_dir="${BASE_DIR}/${OUTPUT_BASE}_${suffix}"
  mkdir -p "$out_dir"

  local out_file="go_watcher"
  [ "$os" == "windows" ] && out_file="go_watcher.exe"

  # job "Building for OS=${os}, ARCH=${arch} → $out_dir/$out_file"
  job "\t${MAGENTA}OS=${GREEN}${os}${_off}: ARCH=${GREEN}${arch}${_off}: ${MAGENTA}$(dirname $out_dir)${_off}/${GREEN}$(basename $out_file)${_off}"

  # subshell call - to contain temporary environment changes without leaving any mess behind:
  (cd "$REPO_ROOT/build/gotools" && GOOS="$os" GOARCH="$arch" go build -o "$out_dir/$out_file" ./cmd/watcher/main.go) # <-- run compiler in shubshell for safety:

  # shellcheck disable=SC2181
  if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${_off} Build failed for OS=${os} ARCH=${arch}. Check above logs." | tee -a "$LOG_FILE"
  else
    local binary_path="$out_dir/$out_file"
    binary_size=$(stat -f%z "$binary_path" 2>/dev/null || stat -c%s "$binary_path")

    job "\tBinary created: $(realpath "$binary_path") (Size: ${binary_size} bytes)"
    # job "\t${GREEN}Binary created: ${MAGENTA}$(realpath "$binary_path")\t${YELLOW}(Size: ${binary_size} bytes)${_off}"
    job "\t${GREEN}Binary created: ${MAGENTA}$(basename "$binary_path")\t${YELLOW}(Size: ${binary_size} bytes)${_off}\n"

    echo "[RESULT] ${binary_path} Size: ${binary_size} bytes" >> "$LOG_FILE"
  fi
}

build_binary "linux" "amd64" "amd64"
build_binary "darwin" "arm64" "arm64"
build_binary "windows" "386" "win32"

job "Starting Docker Compose..."
cd "$REPO_ROOT" && docker-compose -f build/orchestrators/docker-compose.yml up --build 

# ___________________________________________________________________________________________________________________
# (cd "$REPO_ROOT" && docker-compose -f build/orchestrators/docker-compose.yml up --build >> "$LOG_FILE" 2>&1)
# (cd "$REPO_ROOT" && docker-compose -f build/orchestrators/docker-compose.yml up --build 2>&1 | tee -a "$LOG_FILE")
