#!/bin/bash

#  Portal Run Script 
# 
# Pattern: RUN × PORTAL × NOW × ONE
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -e

echo " Starting Portal..."
echo ""

# Navigate to web directory
cd "$(dirname "$0")"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo " Installing dependencies..."
  npm install
fi

# Check if jspdf is installed
if ! npm list jspdf > /dev/null 2>&1; then
  echo " Installing jspdf..."
  npm install jspdf
fi

# Start development server
echo " Starting development server..."
echo ""
echo " Portal will be available at: http://localhost:3000/portal/deanna"
echo " Mobile view: Open DevTools → Toggle device toolbar"
echo ""
echo "Press Ctrl+C to stop"
echo ""

npm run dev

