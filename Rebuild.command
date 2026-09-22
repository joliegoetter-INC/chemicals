#!/bin/zsh
# Double-click me in Finder. Picks up edits made in Chemical_Inventory.xlsx, re-checks hazards, rebuilds the workbook and inventory.html.
cd "$(dirname "$0")"
echo "Close Chemical_Inventory.xlsx in Excel first if it is open.\n"
python3 tools/build_inventory.py readings Chemical_Inventory.xlsx && python3 tools/build_html.py && echo "\nDone. You can close this window."
