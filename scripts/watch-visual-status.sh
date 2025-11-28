#!/bin/bash
# WATCH VISUAL STATUS
# 
# Continuously updates ALL visual status displays
# Keeps status always visible and current in Cursor for ALL users
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo " Watching visual status (updates every 30 seconds)"
echo "   Visual files:"
echo "     - drift-visual-status.md"
echo "     - DRIFT_STATUS_VISUAL.md"
echo "     - .drift-status.txt"
echo "   Keep these files open in Cursor for always-visible status!"
echo "   Press Ctrl+C to stop"
echo ""

while true; do
  cd "$WORKSPACE_ROOT"
  ./scripts/update-all-visual-status.sh
  sleep 30
done

