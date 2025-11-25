#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
while IFS= read -r df; do
    if ! grep -q "^FROM" "$df"; then
        echo "❌ Invalid Dockerfile (must start with FROM): $df"
        FAILURES=$((FAILURES + 1))
    else
        echo "✅ Valid Dockerfile: $df"
    fi
    if ! grep -q "RUN.*--no-cache" "$df"; then
        echo "⚠️  Warning: Dockerfile may use cache: $df"
    fi
done < <(find "$REPO_ROOT" -name "Dockerfile" -type f)
exit $FAILURES
