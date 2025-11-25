#!/bin/bash
# 🚀💥⚡ ABËDESKS APP LAUNCHER ⚡💥🚀

echo "🚀💥⚡ ABËDESKS APP LAUNCHER ⚡💥🚀"
echo "============================================================"

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

# Start the app
echo "🚀 Starting AbëDESKs App..."
echo "🌐 Server will start on available port (check output above)"
echo "============================================================"
echo ""

python3 app.py

