#!/bin/bash

# ─── Colors (optional, can be removed) ─────────────────────────────────────────
white="\033[1;37m"
off="\033[0m"

# ─── Setup Static Paths ───────────────────────────────────────────────────────
SCRIPT_PATH="$(realpath "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
LOG_DIR="$SCRIPT_DIR/crontab_job_logs"
PY_SCRIPT="$SCRIPT_DIR/../src/get_lotto_results.py"

mkdir -p "$LOG_DIR"

# ─── Determine Time and Day ───────────────────────────────────────────────────
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
hour=$(date +%H)
minute=$(date +%M)
dow=$(date +%u)  # 1 = Monday ... 7 = Sunday

# ─── Define Log File ──────────────────────────────────────────────────────────
log_file="$LOG_DIR/lucky_lotto_cron.log"

# ─── Optional Force Run ───────────────────────────────────────────────────────
force="$1"

# ─── Append Header with Time Marker ───────────────────────────────────────────
{
    echo -e "\n============================================\n"
    echo -e "[ CRON ]:\t-> Job triggered at: $timestamp"
    echo -e "User:\t\t-> $USER"
    echo -e "Force:\t\t-> ${force:-none}"
} >> "$log_file"

# ─── Force Dispatch Logic ─────────────────────────────────────────────────────
if [[ "$force" == "--force-powerball" ]]; then
    echo -e "\n[TEST]:\t--> Force-running Powerball draw..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots powerball >> "$log_file" 2>&1
    exit 0
elif [[ "$force" == "--force-megamillions" ]]; then
    echo -e "\n[TEST]:\t--> Force-running Mega Millions draw..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots megamillions >> "$log_file" 2>&1
    exit 0
elif [[ "$force" == "--force-lotto" ]]; then
    echo -e "\n[TEST]:\t--> Force-running Lotto draw..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots lotto >> "$log_file" 2>&1
    exit 0
elif [[ "$force" == "--force-luckyday" ]]; then
    echo -e "\n[TEST]:\t--> Force-running Lucky Day draw..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots luckyday >> "$log_file" 2>&1
    exit 0
elif [[ "$force" == "--force-all" ]]; then
    echo -e "\n[TEST]:\t--> Force-running all draws..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots >> "$log_file" 2>&1
    exit 0
fi

# ─── Scheduled Game Dispatch Logic ────────────────────────────────────────────
if [[ "$hour" == "19" && "$minute" == "59" && "$dow" =~ ^(1|3|6)$ ]]; then
    echo -e "\n[INFO]:\t--> Running Powerball draw..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots powerball >> "$log_file" 2>&1
elif [[ "$hour" == "20" && "$minute" == "00" && "$dow" =~ ^(2|5)$ ]]; then
    echo -e "\n[INFO]:\t--> Running Mega Millions draw..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots megamillions >> "$log_file" 2>&1
elif [[ "$hour" == "19" && "$minute" == "22" && "$dow" =~ ^(1|4|6)$ ]]; then
    echo -e "\n[INFO]:\t--> Running Lotto draw..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots lotto >> "$log_file" 2>&1
elif [[ "$hour" == "10" && "$minute" == "40" ]]; then
    echo -e "\n[INFO]:\t--> Running Pick3/4 & Lucky Day (midday)..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots pick3 >> "$log_file" 2>&1
    python3 "$PY_SCRIPT" --shots pick4 >> "$log_file" 2>&1
    python3 "$PY_SCRIPT" --shots luckyday >> "$log_file" 2>&1
elif [[ "$hour" == "19" && "$minute" == "22" ]]; then
    echo -e "\n[INFO]:\t--> Running Pick3/4 & Lucky Day (evening)..." >> "$log_file"
    python3 "$PY_SCRIPT" --shots pick3 >> "$log_file" 2>&1
    python3 "$PY_SCRIPT" --shots pick4 >> "$log_file" 2>&1
    python3 "$PY_SCRIPT" --shots luckyday >> "$log_file" 2>&1
else
    echo -e "\n[WARNING]:\t--> No matching draw condition met." >> "$log_file"
fi


# NOTES: 
# ./auto_jobs/run.sh --force-powerball
# ./auto_jobs/run.sh --force-powerball
# ./auto_jobs/run.sh --force-megamillions
# ./auto_jobs/run.sh --force-all

# cron
# 59 19 * * 1,3,6 /path/to/run.sh
