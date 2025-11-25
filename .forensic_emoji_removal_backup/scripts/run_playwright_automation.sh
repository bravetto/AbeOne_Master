#!/bin/bash
# 🎭 RUN PLAYWRIGHT AUTOMATION
# Simple wrapper to run Playwright automation

set -e

echo "🎭 PLAYWRIGHT AUTOMATION"
echo "============================================================"
echo ""

# Check if Playwright is available
if ! python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    echo "❌ Playwright not installed"
    echo ""
    echo "💡 Install Playwright:"
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "   pip install playwright"
    else
        echo "   pip3 install playwright"
    fi
    echo "   playwright install chromium"
    exit 1
fi

echo "✅ Playwright ready"
echo ""

# Run automation
echo "🚀 Starting automation..."
echo "   Browser will open - ensure you're logged into Cloudflare"
echo ""

python3 scripts/automate_cloudflare_pages_playwright.py "$@"

echo ""
echo "✅ Automation complete!"

