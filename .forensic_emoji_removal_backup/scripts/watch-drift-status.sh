#!/bin/bash
# WATCH DRIFT STATUS
# 
# Continuously updates .drift-status.txt with current drift guardian status
# Keeps status always visible in Cursor
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "🛡️  Watching drift status (updates every 30 seconds)"
echo "   Status file: .drift-status.txt"
echo "   Press Ctrl+C to stop"
echo ""

while true; do
  cd "$WORKSPACE_ROOT"
  node scripts/update-drift-status.js
  sleep 30
done

