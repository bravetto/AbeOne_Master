#!/bin/bash
# Quick script to kill process on port 8000

PORT=8000
PID=$(lsof -ti:$PORT)

if [ -z "$PID" ]; then
    echo "✅ Port $PORT is free"
else
    echo "🔪 Killing process $PID on port $PORT..."
    kill -9 $PID
    echo "✅ Port $PORT is now free"
fi

