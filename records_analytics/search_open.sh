#!/bin/bash

LOTTO=("فِردوس.json" "Putri.json" "Sherice.json" "Leonard.json" "Cristian.json" "Liam.json" "Nonhlanhla.json" "Dolors.json" "Moussa.json" "Aria.json") 
POWERBALL=("曾丽.json" "מיכאל.json" "נועה.json" "Benoît.json" "Manuia.json" "Kimberly.json")
MEGAMILLION=("Peppermintos.json" "Putri.json" "Ciara.json" "Alessandro.json" "بهرام.json" "淑惠.json" "Гулнора.json" "Araya.json" "Conakry.json" "翔.json" "Драган.json")

workdir="July-2025/catalog"

# ___ get absolute workdir path | exit if not valid:
abs_workdir=$(realpath "$workdir" 2>/dev/null)
if [ -z "$abs_workdir" ]; then
echo "Error: Directory does not exist: $workdir"
    exit 1
fi

# Search for each JSON file
# for json in "${POWERBALL[@]}"; do
# for json in "${LOTTO[@]}"; do
for json in "${MEGAMILLION[@]}"; do
    file=$(find "$abs_workdir" -name "$json" -print -quit 2>/dev/null)
    if [ -n "$file" ]; then
        echo -e "Found:\t--> $file"
        open "$file"            # macOS
        # xdg-open "$file"      # Linux
        # start "$file"         # Windows (Git Bash)
    else
        echo "Not found: $json"
    fi
done

###############################################################################################################################################

# while IFS= read -r file; do
#     abs_path=$(realpath "$file")
#     echo "Opening: $abs_path"
#     xdg-open "$abs_path"    # Linux
#     # open "$abs_path"      # macOS
#     # start "$abs_path"     # Windows (Git Bash)
# done < <(find catalog/ -type f -name "file.json")
                  
