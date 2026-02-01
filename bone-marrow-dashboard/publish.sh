#!/bin/bash
# Publish dashboard to GitHub Pages
#
# Usage: ./publish.sh [data_file] [period]
# Example: ./publish.sh data/bm_cases_2025_01.csv "January 2025"

set -e

DATA_FILE="${1:-data/bm_cases_2024_12.csv}"
PERIOD="${2:-$(date -d 'last month' '+%B %Y' 2>/dev/null || date -v-1m '+%B %Y')}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Publishing dashboard..."
echo "  Data: $DATA_FILE"
echo "  Period: $PERIOD"

# Generate dashboard
python3 "$SCRIPT_DIR/src/generate_dashboard.py" \
    --data "$SCRIPT_DIR/$DATA_FILE" \
    --template "$SCRIPT_DIR/templates/dashboard.html" \
    --output "$REPO_ROOT/docs/index.html" \
    --period "$PERIOD"

echo ""
echo "Dashboard updated at: $REPO_ROOT/docs/index.html"
echo ""
echo "To publish, run:"
echo "  git add docs/index.html"
echo "  git commit -m 'Update dashboard for $PERIOD'"
echo "  git push"
