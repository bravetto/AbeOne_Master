#!/bin/bash

echo ""
echo " ABëDESK RESONANCE DASHBOARD LAUNCHER "
echo ""
echo "Pattern: AEYON × DASHBOARD × VISUALIZATION × ONE"
echo "Status:  LAUNCHING "
echo "∞ AbëONE ∞"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo " Installing dependencies..."
    npm install
    echo ""
fi

echo " Starting AbëDESK development server..."
echo ""
echo " Dashboard will be available at:"
echo "   http://localhost:3000/resonance"
echo ""
echo " Press Ctrl+C to stop"
echo ""

npm run dev
