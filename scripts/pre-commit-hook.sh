#!/bin/bash
#  BRAVETTO PRE-COMMIT HOOK - Danny Rules Enforcement + SRE Compliance
# Guardian: AbëONE | Pattern: PREFLIGHT × ENFORCEMENT × DANNY × ONE × SRE

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SCRIPT_DIR="$REPO_ROOT/scripts"

# Run SRE compliance check (Substrate-Required Execution)
if [ -f "$SCRIPT_DIR/sre-audit.js" ]; then
    echo " Running SRE compliance check..."
    node "$SCRIPT_DIR/sre-audit.js" || exit 1
fi

# Run preflight checks
if [ -f "$SCRIPT_DIR/bravetto_preflight.sh" ]; then
    "$SCRIPT_DIR/bravetto_preflight.sh" || exit 1
fi

# Run ARDM check (Actionable Request Detection Module)
if [ -f "$SCRIPT_DIR/pre-commit-ardm-check.sh" ]; then
    echo " Running ARDM pre-commit check..."
    "$SCRIPT_DIR/pre-commit-ardm-check.sh" || {
        echo "  ARDM check found undelivered actionable items (non-blocking)"
    }
fi

exit 0

