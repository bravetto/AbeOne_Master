#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
find "$REPO_ROOT" -path "*/helm/*" -name "values.yaml" -o -path "*/helm/*" -name "Chart.yaml" | while read -r f; do
    [ -f "$f" ] || continue
    dir=$(dirname "$f")
    helm lint "$dir" >/dev/null 2>&1 || { echo "Helm lint failed: $dir"; ((FAILURES++)); }
done
exit $FAILURES
