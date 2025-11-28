#!/bin/bash
# 🚀💥⚡ ABËDESKS APP LAUNCHER ⚡💥🚀
# Fixed for port conflicts

echo "🚀💥⚡ ABËDESKS APP LAUNCHER ⚡💥🚀"
echo "============================================================"

# Kill any existing Flask processes on common ports
echo "🧹 Cleaning up any existing processes..."
pkill -f "flask run" 2>/dev/null
pkill -f "app.py" 2>/dev/null
sleep 1

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip3 install flask markdown
fi

# Check if markdown is installed
if ! python3 -c "import markdown" 2>/dev/null; then
    echo "📦 Installing markdown..."
    pip3 install markdown
fi

# Navigate to app directory
cd "$(dirname "$0")"

# Start the app (it will auto-detect available port)
echo "🚀 Starting AbëDESKs App..."
echo "🌐 Server will auto-detect available port"
echo "💎 Check terminal output for the URL"
echo "============================================================"
echo ""

python3 app.py

