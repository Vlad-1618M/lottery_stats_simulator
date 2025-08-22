#!/bin/bash

green="\033[1;32m"
cyan="\033[1;36m"
red="\033[0;31m"
yellow="\033[1;33m"
white="\033[1;37m"
off="\033[0m"

# ... decorators:
decorator_init="echo -e ${white}"$(printf '.%.0s' {1..40})"${off}"
decorator_done="echo -e ${white}"$(printf '=%.0s' {1..68})"${off}"
in_file_decorator="$(printf '_%.0s' {1..72})"

# ... setup:
SCRIPT_PATH="$(realpath "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
STATIC_DIR="$SCRIPT_DIR"
OUTPUT_DIR="$STATIC_DIR/crontab_logs"
OUTPUT_FILE="$OUTPUT_DIR/crontab_$TIMESTAMP.txt"

mkdir -p "$OUTPUT_DIR"

if crontab -l > /dev/null 2>&1; then
    echo -e "\n[ INFO ]:\tCrontab Schedule found for user: $USER" > "$OUTPUT_FILE"
    echo -e "$in_file_decorator" >> "$OUTPUT_FILE"
    crontab -l >> "$OUTPUT_FILE"
    echo -e "\n${yellow}[${green} SUCCESS ${yellow}]${off} Crontab Schedule${cyan}:\t-->${yellow} $(basename $OUTPUT_FILE)"
    echo -e "$in_file_decorator" >> "$OUTPUT_FILE"
else
    echo -e "\n[ WARNING ]:\tNo crontab found for user: $USER" > "$OUTPUT_FILE"
    echo -e "\n${yellow}[${cyan} INFO ${yellow}]:${red} Empty ${off}or ${red}non-existent ${off}cron schedule:\n\t  See Logs${cyan}: -->${yellow} $(basename $OUTPUT_FILE)"
    cat "$OUTPUT_FILE"
fi
$decorator_done
