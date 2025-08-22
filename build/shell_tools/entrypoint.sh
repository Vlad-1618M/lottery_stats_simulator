#!/bin/bash

# POSIX-compatible color setup:
RED=$(printf '\033[31m')
GREEN=$(printf '\033[32m')
YELLOW=$(printf '\033[33m')
MAGENTA=$(printf '\033[35m')
CYAN=$(printf '\033[36m')
BLUE=$(printf '\033[34m')
off=$(printf '\033[0m')

generate_decorator() {
  printf '%s\n' "${YELLOW}$(printf '%63s' '' | tr ' ' '_')${off}"
}

job() {
  _type=$1
  _msg=$2
  _timestamp=$(date +"%T")

  case "$_type" in
    job)    _prefix="${YELLOW}[${GREEN}JOB  ${YELLOW}]${off}" ;;
    call)   _prefix="${YELLOW}[${GREEN}CALL ${YELLOW}]${off}" ;;
    error)  _prefix="${YELLOW}[${RED}ERROR${YELLOW}]${off}" ;;
    skip)   _prefix="${YELLOW}[${MAGENTA}SKIP ${YELLOW}]${off}" ;;
    debug)  _prefix="${YELLOW}[${CYAN}DEBUG${YELLOW}]${off}" ;;
    warn)   _prefix="${YELLOW}[${YELLOW}WARN ${YELLOW}]${off}" ;;
    docker) _prefix="${YELLOW}[${BLUE}DOCKER${YELLOW}]${off}" ;;
    *)      _prefix="${YELLOW}[${_type}]${off}" ;;
  esac

  printf '%s\n' "[${_timestamp}] ${_prefix}: ${MAGENTA}->${off} ${_msg}"
}

installed_playwright_deps() {
  if command -v playwright >/dev/null 2>&1; then
    job debug "Checking installed Playwright system dependencies..."

    # ____ get deps from dry-run call:
    local deps
    deps=$(playwright install-deps --dry-run 2>/dev/null | grep -oP '(?<=apt-get install -y --no-install-recommends ).*')

    if [ -z "$deps" ]; then
      job warn "Could not extract dependency list from playwright"
      return
    fi

    # get list to arrays
    read -ra dep_array <<< "$deps"

    for pkg in "${dep_array[@]}"; do
      if dpkg -s "$pkg" &>/dev/null; then
        echo -e "  ${GREEN}${pkg}${off}"
      else
        echo -e "  ${YELLOW}${pkg} (missing)${off}"
      fi
    done
  else
    job error "playwright CLI not found — skipping system dependency check"
  fi
}


deps_check() {
  job debug "System PATH:"
  echo "$PATH" | tr ':' '\n' | sed "s/^/${CYAN}  /" | sed "s/$/${off}/"

  job debug " Python info:"
  PYTHON_BIN=$(command -v python || command -v python3)
  if [ -n "$PYTHON_BIN" ]; then
    PYTHON_VERSION=$($PYTHON_BIN --version 2>&1)
    job debug " Path: ${CYAN}${PYTHON_BIN}${off}"
    job debug " Version: ${CYAN}${PYTHON_VERSION}${off}"
  else
    job error "Python not found!"
  fi

  job debug " Golang info:"
  if command -v go >/dev/null 2>&1; then
    GO_BIN=$(command -v go)
    GO_VERSION=$(go version)
    job debug " Path: ${CYAN}${GO_BIN}${off}"
    job debug " Version: ${CYAN}${GO_VERSION}${off}"
  else
    job error "Go not found!"
  fi
  installed_playwright_deps
}


check_docker() {
  if grep -q '/docker/' /proc/1/cgroup 2>/dev/null; then
    job docker "Running inside Docker container"
    _cpus=$(nproc 2>/dev/null || echo "?")
    _mem=$(awk '/MemTotal/ {printf "%.1fGB", $2/1024/1024}' /proc/meminfo 2>/dev/null || echo "?")
    job docker "Resources: ${_cpus} CPUs, ${_mem} memory"

    if mount | grep -q '/lotto'; then
      job docker "Volume mounted: /lotto"
    else
      job warn "Volume /lotto not mounted"
    fi
  fi
}

run_python() {
  _script_path=$1
  shift
  _args=("$@")  # Save all remaining args as an array

  if [ -f "$_script_path" ]; then
    job call "Running ${_script_path##*/} with args: ${_args[*]}"
    "$PYTHON_BIN" "$_script_path" "${_args[@]}" || {
      job error "${_script_path##*/} failed!"
      exit 1
    }
  else
    job skip "${_script_path##*/} not found"
  fi
}

run_go() {
  local _script_path=$1
  shift
  local _args=("$@")

  if command -v go >/dev/null 2>&1; then
    job call "Running ${_script_path##*/} with args: ${_args[*]}"
    
    go run "$_script_path" "${_args[@]}" || {
      job error "${_script_path##*/} failed!"
      exit 1
    }
  else
    job error "Go interpreter not found. Skipping ${_script_path##*/}"
    exit 1
  fi
}

# ____________________________________________________________________________
py_main(){
  PYTHON_BIN=$(command -v python || command -v python3)
  if [ -z "$PYTHON_BIN" ]; then
    job error "No valid Python interpreter found:"
    exit 1
  fi
  generate_decorator
  job "PYTHON Sieve Method" "Sieve of Eratosthenes Calculation Method:"
  run_python "src/quickPick.py" "--sieve"
  job "PYTHON Sieve Method" "Sieve of Eratosthenes Calculation Method in Spanish:"
  run_python "src/quickPick.py" "--sieve" "--lang" "es"
  # job "PYTHON Sieve Method" "Sieve of Eratosthenes Calculation Method in Chinese(traditional):"
  # run_python "src/quickPick.py" "--sieve" "--lang" "zh-TW"
  # job "PYTHON Sieve Method" "Sieve of Eratosthenes Calculation Method in Hindi:"
  # run_python "src/quickPick.py" "--sieve" "--lang" "hi"
  # job "PYTHON Sieve Method" "Sieve of Eratosthenes Calculation Method in Hebrew:"
  # run_python "src/quickPick.py" "--sieve" "--lang" "iw"
  # job "PYTHON Sieve Method" "Sieve of Eratosthenes Calculation Method in Arabic:"
  # run_python "src/quickPick.py" "--sieve" "--lang" "ar"
  # job "PYTHON Sieve Method" "Sieve of Eratosthenes Calculation Method in Russian:"
  # run_python "src/quickPick.py" "--sieve" "--lang" "ru"
  # job "PYTHON Sieve Method" "Sieve of Eratosthenes Calculation Method in Armenian:"
  # run_python "src/quickPick.py" "--sieve" "--lang" "hy"
  # job "PYTHON Sieve Method" "Sieve of Eratosthenes Calculation Method in Japanese:"
  # run_python "src/quickPick.py" "--sieve" "--lang" "ja"

  generate_decorator
  job "PYTHON Collect" "Collect Recent Draw Results + Screenshots:"
  run_python "/lotto/src/get_lotto_results.py" "--shots"
  generate_decorator
  job "PYTHON Catalog" "Create Player's Catalog | All Users JSON datasets:"
  run_python "/lotto/src/quickPick.py" "--auto" "--all-names"
  generate_decorator
  job "PYTHON Analytics" "Lotto Sequence Analytics Scripts:"
  run_python "/lotto/src/collect_statistics.py" "--list"
  run_python "/lotto/src/collect_statistics.py" "--games" "megamillion" "powerball" "--save-html"
  generate_decorator
  job "PYTHON Catalogs" "Show Existing Catalog Details:"
  run_python "/lotto/records_analytics/catalog_manager.py" "--items"
  run_python "/lotto/records_analytics/catalog_manager.py" "--show-ids"
  run_python "/lotto/records_analytics/catalog_manager.py" "--show-details"
  generate_decorator  
}

go_main(){
  job "GO Install" "Installing GO Sequence Comparator Script Engine | install_go.sh:"
  job GOLANG "Installing GO | install_go.sh"
  eval /lotto/build/shell_tools/install_go.sh
  
  generate_decorator
  job "GO RUN MIXed" "Lotto Sequence Comparator Scripts:"
  run_go "src_for_go/main.go" "--games" "powerball,megamillion,lotto" "--html"
  
  job "GO RUN Megamillion" "Lotto Sequence Comparator Scripts:"
  run_go "src_for_go/main.go" "--games" "megamillion" "--html"
  run_go "src_for_go/main.go" "--games" "megamillion" "--drop-mega" "--html"
  run_go "src_for_go/main.go" "--games" "megamillion" "--depth" "4" "--html"
  generate_decorator

  job "GO RUN Powerball" "Lotto Sequence Comparator Scripts:"
  run_go "src_for_go/main.go" "--games" "powerball" "--html"
  run_go "src_for_go/main.go" "--games" "powerball" "--drop-power" "--html"
  run_go "src_for_go/main.go" "--games" "powerball" "--depth" "4" "--html"
  
  generate_decorator
  job "GO RUN Lotto" "Lotto Sequence Comparator Scripts:"
  run_go "src_for_go/main.go" "--games" "lotto" "--html"
  run_go "src_for_go/main.go" "--games" "lotto" "--depth" "6" "--html"
}

filter_draw_results(){
  local record="/lotto/lotto_draw_results"
  local mega="megamillions"
  local power="powerball"
  local lotto="lotto"
  # local zz="sleep 0.3"
  job "Show ${mega}" "Draw Results: ${record}/${mega}*.json"
  jq -r '.[] | "date: \(.draw_date),\t primary: \(.primary_numbers | join(",\t")), mega: \(.powerball)"' ${record}/${mega}*.json | batcat --language json
  ${zz}
  job "Show ${power}" "Draw Results: ${record}/${power}*.json" 
  jq -r '.[] | "date: \(.draw_date), primary: \(.primary_numbers | join(",\t")), powerball: \(.powerball)"' ${record}/${power}*.json | batcat --language json
  ${zz}
  job "Show ${lotto}" "Draw Results: ${record}/${lotto}*.json"
  jq -r '.[] | "date: \(.draw_date), primary: \(.primary_numbers | join(",\t")),"' ${record}/${lotto}*.json | batcat --language json
  # batcat /lotto/lotto_draw_results/${mega}*.json
  # batcat /lotto/lotto_draw_results/${power}*.json
  # batcat /lotto/lotto_draw_results/${lotto}*.json
}

main() {
  # check_docker
  generate_decorator
  deps_check
  
  # # ____ Run Python Scripts:
  py_main "$@"
  
  # # ____ Run Golang Scripts:
  go_main "$@"
  generate_decorator
  filter_draw_results
  generate_decorator
  tree /lotto/lotto_draw_results
  tree /lotto/lotto_screenshots
  tree /lotto/html_reports
  generate_decorator
  job job "All jobs completed:"
}

# ____________________________________________________________________________
main "$@"


# ____________________ DEBUG NOTES ________________________________________________________
# batcat /lotto/lotto_draw_results/powerbal*.json | grep '"primary_numbers"' | grep '"powerball"' 
# batcat /lotto/lotto_draw_results/powerbal*.json | grep -A 2 '"primary_numbers"' | grep '"powerball"' 
# batcat /lotto/lotto_draw_results/powerbal*.json | egrep 'primary_numbers|powerball'
# batcat /lotto/lotto_draw_results/powerbal*.json | egrep --color=always 'primary_numbers|powerball'
# go_main "$@"
# py_main "$@"
# tail -f /dev/null



# deps_check() {
#   job debug "System PATH:"
#   echo "$PATH" | tr ':' '\n' | sed "s/^/${CYAN}  /" | sed "s/$/${off}/"

#   job debug " Python info:"
#   PYTHON_BIN=$(command -v python || command -v python3)
#   if [ -n "$PYTHON_BIN" ]; then
#     PYTHON_VERSION=$($PYTHON_BIN --version 2>&1)
#     job debug " Path: ${CYAN}${PYTHON_BIN}${off}"
#     job debug " Version: ${CYAN}${PYTHON_VERSION}${off}"

#     job debug " Python packages:"
#     $PYTHON_BIN -m pip list | grep -E 'playwright|pip|setuptools|wheel' || job warn "No known packages found"
#   else
#     job error "Python not found!"
#   fi

#   job debug " Golang info:"
#   if command -v go >/dev/null 2>&1; then
#     GO_BIN=$(command -v go)
#     GO_VERSION=$(go version)
#     job debug " Path: ${CYAN}${GO_BIN}${off}"
#     job debug " Version: ${CYAN}${GO_VERSION}${off}"
#   else
#     job error "Go not found!"
#   fi

#   job debug " CLI tools:"
#   for tool in jq batcat curl tree shellcheck make; do
#     if command -v "$tool" >/dev/null 2>&1; then
#       TOOL_PATH=$(command -v "$tool")
#       TOOL_VER=$("$tool" --version 2>/dev/null | head -n1)
#       job debug " ${tool}: ${CYAN}${TOOL_PATH}${off} (${TOOL_VER})"
#     else
#       job warn " ${tool} not installed"
#     fi
#   done

#   job debug " Playwright dependencies (system-level):"
#   if command -v playwright >/dev/null 2>&1; then
#     playwright install-deps --dry-run || job warn "Could not validate playwright deps"
#   else
#     job error "playwright CLI not found!"
#   fi
# }



# debug_info() {
#   job debug "System PATH:"
#   echo "$PATH" | tr ':' '\n' | sed "s/^/${CYAN}  /" | sed "s/$/${off}/"

#   job debug " Python info:"
#   PYTHON_BIN=$(command -v python || command -v python3)

#   if [ -n "$PYTHON_BIN" ]; then
#     PYTHON_VERSION=$($PYTHON_BIN --version 2>&1)
#     job debug " Path: ${CYAN}${PYTHON_BIN}${off}"
#     job debug " Version: ${CYAN}${PYTHON_VERSION}${off}"
#   else
#     job error "Python not found!"
#   fi
# }