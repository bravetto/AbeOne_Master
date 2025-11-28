#!/bin/bash
# TRIGGER VISUAL STATUS UPDATE
# 
# Lightweight trigger for DRIFT_STATUS_VISUAL.md updates
# Runs silently in background, non-blocking
# Called automatically on chat interactions
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Run update in background (non-blocking)
cd "$WORKSPACE_ROOT"
./scripts/update-all-visual-status.sh > /dev/null 2>&1 &

