#!/bin/bash
#  BRAVETTO PRE-PUSH HOOK - Danny Rules Enforcement
# Guardian: AbëONE | Pattern: PREFLIGHT × ENFORCEMENT × DANNY × ONE

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SCRIPT_DIR="$REPO_ROOT/scripts"

# Run comprehensive preflight checks before push
if [ -f "$SCRIPT_DIR/bravetto_preflight.sh" ]; then
    "$SCRIPT_DIR/bravetto_preflight.sh" || {
        echo " Pre-push checks failed. Fix issues before pushing."
        exit 1
    }
fi

exit 0

