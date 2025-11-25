#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
WARNINGS=0
find "$REPO_ROOT" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) -not -path "*/.git/*" | while read -r f; do
    lines=$(grep -n "^[[:space:]]*#[[:space:]]*[a-zA-Z]" "$f" 2>/dev/null | wc -l)
    [ "$lines" -gt 10 ] && echo "Warning: Many commented lines in $f"
done
exit 0
