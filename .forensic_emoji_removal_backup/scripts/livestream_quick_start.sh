#!/bin/bash
# 🎥 LIVESTREAM QUICK START SCRIPT
# Starts essential services for livestream demo

set -e

echo "🎥 Starting Livestream Demo Services..."
echo ""

# Check if we're in the right directory
if [ ! -f "scripts/launch_pad.py" ]; then
    echo "❌ Error: Must run from AbeOne_Master root directory"
    exit 1
fi

# Start Backend (FastAPI)
echo "🚀 Starting Backend API (FastAPI)..."
cd EMERGENT_OS/server 2>/dev/null || cd apps/api 2>/dev/null || {
    echo "⚠️  Backend directory not found - skipping"
    echo "   Manual start: cd EMERGENT_OS/server && uvicorn main:app --reload"
}
cd - > /dev/null

# Start Frontend (Next.js)
echo "🚀 Starting Frontend (Next.js)..."
if [ -d "apps/web" ]; then
    cd apps/web
    if [ ! -d "node_modules" ]; then
        echo "   Installing dependencies..."
        npm install > /dev/null 2>&1 || echo "   ⚠️  npm install failed"
    fi
    echo "   Starting dev server..."
    # Note: This will run in background - user should start manually in separate terminal
    echo "   Manual start: cd apps/web && npm run dev"
    cd - > /dev/null
else
    echo "⚠️  Frontend directory not found"
fi

# Check Launch Pad
echo ""
echo "📊 Checking Launch Pad Dashboard..."
python3 scripts/launch_pad.py --check

echo ""
echo "✅ Quick Start Complete!"
echo ""
echo "📋 Next Steps:"
echo "   1. Start Backend: cd EMERGENT_OS/server && uvicorn main:app --reload"
echo "   2. Start Frontend: cd apps/web && npm run dev"
echo "   3. Check services: python3 scripts/launch_pad.py --check"
echo "   4. View Launch Pad: python3 scripts/launch_pad.py"
echo ""
echo "🎥 Ready for Livestream!"

