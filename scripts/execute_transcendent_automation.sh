#!/bin/bash
#  TRANSCENDENT AUTOMATION EXECUTOR
# Wrapper script that uses transcendent capabilities

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo " TRANSCENDENT AUTOMATION ENGINE"
echo "============================================================"
echo ""

# Check if transcendent engine exists
if [ -f "$SCRIPT_DIR/transcendent_automation_engine.py" ]; then
    echo " Using Transcendent Automation Engine"
    echo ""
    python3 "$SCRIPT_DIR/transcendent_automation_engine.py" "$@"
else
    echo "  Transcendent engine not found, using standard Playwright"
    echo ""
    python3 "$SCRIPT_DIR/automate_cloudflare_pages_playwright.py" "$@"
fi

