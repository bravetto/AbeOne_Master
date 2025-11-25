#!/bin/bash

#  LAUNCH SCRIPT - PHASE 1 PORTAL
# Pattern: LAUNCH × PHASE1 × GO × ONE
# ∞ AbëONE ∞

echo " LAUNCHING PHASE 1 PORTAL "
echo ""

# Navigate to web app directory
cd "$(dirname "$0")/../../.."
pwd

echo ""
echo " Installing dependencies..."
npm install

echo ""
echo " Starting development server..."
echo "   Portal will be available at: http://localhost:3000/portal/deanna"
echo ""

npm run dev

