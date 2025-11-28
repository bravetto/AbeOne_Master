#!/bin/bash
#  SETUP PLAYWRIGHT FOR AUTOMATION
# Installs Playwright and Chromium browser

set -e

echo " SETTING UP PLAYWRIGHT..."
echo "============================================================"
echo ""

# Check if in venv
if [ -n "$VIRTUAL_ENV" ]; then
    echo " Virtual environment detected: $VIRTUAL_ENV"
else
    echo "  Not in virtual environment"
    echo "   Consider: source .venv/bin/activate"
fi

echo ""
echo " Installing Playwright..."
pip install playwright

echo ""
echo " Installing Chromium browser..."
playwright install chromium

echo ""
echo " Playwright setup complete!"
echo ""
echo " Usage:"
echo "   python3 scripts/automate_cloudflare_pages_playwright.py"
echo ""

