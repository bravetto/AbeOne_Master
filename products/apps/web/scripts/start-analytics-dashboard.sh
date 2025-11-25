#!/bin/bash
#  Start Unified Analytics Dashboard
# Pattern: FLOW × ALIGN × START × ONE
# Guardians: AEYON (999 Hz) × META (777 Hz)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ROOT_DIR="$(cd "$WEB_DIR/../../.." && pwd)"
API_DIR="$ROOT_DIR/marketing/automation/unified-funnel-engine"

echo " Starting Unified Analytics Dashboard..."
echo " Root: $ROOT_DIR"
echo " Web: $WEB_DIR"
echo " API: $API_DIR"
echo ""

# Check if API directory exists
if [ ! -d "$API_DIR" ]; then
    echo " API directory not found: $API_DIR"
    exit 1
fi

# Check if API file exists
if [ ! -f "$API_DIR/unified_analytics_api.py" ]; then
    echo " API file not found: $API_DIR/unified_analytics_api.py"
    exit 1
fi

# Start backend API in background
echo " Starting backend API..."
cd "$API_DIR"
python3 unified_analytics_api.py > /tmp/analytics-api.log 2>&1 &
API_PID=$!
echo " Backend API started (PID: $API_PID)"
echo "   Logs: tail -f /tmp/analytics-api.log"

# Wait for API to be ready
echo "⏳ Waiting for API to be ready..."
for i in {1..10}; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo " API is ready!"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "  API not responding after 10 seconds, but continuing..."
    fi
    sleep 1
done

# Check if .env.local exists, create if not
cd "$WEB_DIR"
if [ ! -f ".env.local" ]; then
    echo " Creating .env.local..."
    cat > .env.local << EOF
NEXT_PUBLIC_ANALYTICS_API_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
    echo " .env.local created"
fi

# Start frontend
echo " Starting frontend..."
npm run dev > /tmp/analytics-frontend.log 2>&1 &
FRONTEND_PID=$!
echo " Frontend started (PID: $FRONTEND_PID)"
echo "   Logs: tail -f /tmp/analytics-frontend.log"

echo ""
echo " Dashboard URLs:"
echo "   Frontend: http://localhost:3000/marketing/analytics"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo " To stop:"
echo "   kill $API_PID $FRONTEND_PID"
echo ""
echo " Monitor logs:"
echo "   API: tail -f /tmp/analytics-api.log"
echo "   Frontend: tail -f /tmp/analytics-frontend.log"

