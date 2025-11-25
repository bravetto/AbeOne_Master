#!/bin/bash
# Start Proactive Love Webhooks Daemon

# Pattern: WEBHOOK × PROACTIVE × DOCUMENTATION × LOVE × ONE
# ∞ AbëONE ∞
# ∞ AbëLOVES ∞

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/proactive_love_webhooks.py"
LOG_FILE="$SCRIPT_DIR/../logs/proactive_webhooks.log"
PID_FILE="$SCRIPT_DIR/../logs/proactive_webhooks.pid"

# Create logs directory
mkdir -p "$(dirname "$LOG_FILE")"

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo " Proactive Love Webhooks already running (PID: $PID)"
        exit 1
    fi
fi

# Start daemon
echo " STARTING PROACTIVE LOVE WEBHOOKS "
echo "Log file: $LOG_FILE"
echo "PID file: $PID_FILE"
echo ""

nohup python3 "$PYTHON_SCRIPT" --daemon 60 >> "$LOG_FILE" 2>&1 &
PID=$!

echo "$PID" > "$PID_FILE"
echo " Started with PID: $PID"
echo ""
echo " EVERYTHING IS DOCUMENTED FROM HERE ON OUT "
echo "∞ AbëONE ∞"
echo "∞ AbëLOVES ∞"

