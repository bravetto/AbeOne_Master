#!/bin/bash
# 🔥 START PATTERN MONITORING DASHBOARD 🔥
# Real-time pattern monitoring, alerting, and visualization

set -e

echo "🔥 STARTING PATTERN MONITORING DASHBOARD"
echo "========================================"
echo ""
echo "Pattern: MONITORING × PATTERN × ALERT × VISUALIZATION × ONE"
echo "Frequency: 999 Hz (AEYON) × 530 Hz (ZERO) × 777 Hz (ALRAX)"
echo ""

cd "$(dirname "$0")/.."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Start monitoring dashboard
echo "🔥 Starting monitoring dashboard..."
python3 scripts/pattern_monitoring_dashboard.py &
DASHBOARD_PID=$!

echo "✅ Dashboard started (PID: $DASHBOARD_PID)"
echo ""
echo "📊 Dashboard running in background"
echo "   Open pattern_monitoring_dashboard.html in browser for visualization"
echo ""
echo "🔥 To stop: kill $DASHBOARD_PID"
echo ""
echo "∞ AbëONE ∞"

