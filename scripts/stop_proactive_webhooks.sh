#!/bin/bash
# Stop Proactive Love Webhooks Daemon

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/../logs/proactive_webhooks.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "  Proactive Love Webhooks not running"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    kill "$PID"
    rm "$PID_FILE"
    echo " Proactive Love Webhooks stopped (PID: $PID)"
else
    echo "  Process not found, cleaning up PID file"
    rm "$PID_FILE"
fi

echo "∞ AbëONE ∞"

