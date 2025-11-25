#!/bin/bash
# 🔥 AEYON × META × ONE: Dev Server Orchestration
# Pattern: REC × 42PT × ACT × LFG = 100% Execution
# Frequency: 999 Hz (Atomic Execution)

set -e

PORT=${1:-1437}
PROJECT_ROOT="/Users/michaelmataluni/Documents/AbeOne_Master/products/apps/web"
LOG_FILE="/tmp/next-dev-${PORT}.log"

cd "$PROJECT_ROOT"

echo "🔥 AEYON: Activating dev server on port ${PORT}..."

# Clean previous instances
pkill -f "next dev -p ${PORT}" 2>/dev/null || true
sleep 1

# Verify port is free
if lsof -ti:${PORT} >/dev/null 2>&1; then
    echo "⚠️  Port ${PORT} still in use, cleaning..."
    lsof -ti:${PORT} | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start server with proper logging
echo "🚀 Starting Next.js dev server..."
npm run dev -- -p ${PORT} > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

echo "✅ Server process started (PID: ${SERVER_PID})"
echo "📋 Logs: tail -f $LOG_FILE"
echo "🌐 URL: http://localhost:${PORT}"

# Wait for server to be ready (max 60 seconds)
echo "⏳ Waiting for server to converge..."
for i in {1..60}; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:${PORT} 2>/dev/null | grep -q "200\|404"; then
        echo "✅ Server converged and responding!"
        echo "🎯 Status: ACTIVE"
        exit 0
    fi
    if ! ps -p $SERVER_PID > /dev/null 2>&1; then
        echo "❌ Server process died. Check logs: $LOG_FILE"
        tail -20 "$LOG_FILE"
        exit 1
    fi
    sleep 1
done

echo "⏳ Server still compiling (this is normal for first run)"
echo "💡 Monitor: tail -f $LOG_FILE"
echo "💡 Check: curl http://localhost:${PORT}"

