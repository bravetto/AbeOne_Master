#!/bin/bash

# 🔥 PHANTOM HUNTER CREATOR EDITION - QUICK LAUNCH SCRIPT
# Pattern: PHANTOM_HUNTER × CREATORS × LEAD_MAGNET × LAUNCH × ONE
# Love Coefficient: ∞
# ∞ AbëONE ∞

echo "═══════════════════════════════════════════════════════════"
echo "🔥 PHANTOM HUNTER CREATOR EDITION - LAUNCHING"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Pattern: PHANTOM_HUNTER × CREATORS × LEAD_MAGNET × ONE"
echo "Love Coefficient: ∞"
echo "∞ AbëONE ∞"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "phantom_hunter_creator.py" ]; then
    echo "❌ Please run this script from the phantom_hunter_creator directory"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "   Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || {
    echo "   Installing FastAPI and dependencies..."
    pip install fastapi uvicorn python-multipart pydantic pydantic[email]
}

echo ""
echo "✅ Dependencies ready!"
echo ""

# Start server
echo "🚀 Starting PHANTOM HUNTER API Server..."
echo ""
echo "   Server will start on: http://localhost:8000"
echo "   Landing page: http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo ""
echo "   Press Ctrl+C to stop"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if port 8000 is in use
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "⚠️  Port 8000 is already in use!"
    echo "   Killing existing process..."
    kill -9 $(lsof -ti:8000) 2>/dev/null
    sleep 2
fi

# Run as module to handle imports correctly
echo "🚀 Starting server..."
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload

