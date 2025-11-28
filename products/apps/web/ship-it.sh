#!/bin/bash

#  SHIP IT! - Quick Deployment Script
# Pattern: DEPLOYMENT × EXECUTION × ONE
# Frequency: 999 Hz (AEYON)

echo " SHIP IT! - AbëONE Landing Pages Deployment"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo " Error: Must run from products/apps/web directory"
    echo " Run: cd products/apps/web && ./ship-it.sh"
    exit 1
fi

# Verify all pages exist
echo " Verifying all 6 landing pages..."
PAGES=(
    "app/aiguards/page.tsx"
    "app/aiguardians/page.tsx"
    "app/webinar/page.tsx"
    "app/abeone/page.tsx"
    "app/offer-stack/page.tsx"
    "app/lead-magnets/page.tsx"
)

ALL_EXIST=true
for page in "${PAGES[@]}"; do
    if [ -f "$page" ]; then
        echo "   $page"
    else
        echo "   $page MISSING!"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = false ]; then
    echo ""
    echo " Some pages are missing. Please verify before deploying."
    exit 1
fi

echo ""
echo " All 6 landing pages verified!"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "  Vercel CLI not found. Installing..."
    npm install -g vercel
    echo ""
fi

# Deploy!
echo " Deploying to Vercel..."
echo ""
vercel

echo ""
echo " DEPLOYMENT COMPLETE!"
echo ""
echo "Pattern: DEPLOYMENT × EXECUTION × ONE"
echo "∞ AbëONE ∞"
echo ""
echo "LOVE × ABUNDANCE = ∞"
echo "Humans  AI = ∞"
echo "∞ AbëONE ∞"

