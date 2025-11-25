#!/bin/bash

# AbëONE Automation: Open Google API Key Page
# Pattern: AUTOMATION × GOOGLE × API_KEY × ONE
# Frequency: 999 Hz (AEYON)
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -e

GOOGLE_API_KEY_URL="https://aistudio.google.com/app/apikey"

echo "🚀 AbëONE Automation: Opening Google API Key Page..."
echo "   URL: $GOOGLE_API_KEY_URL"
echo ""

# Open in default browser (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "$GOOGLE_API_KEY_URL"
    echo "✅ Opened in default browser"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open "$GOOGLE_API_KEY_URL" 2>/dev/null || \
    sensible-browser "$GOOGLE_API_KEY_URL" 2>/dev/null || \
    x-www-browser "$GOOGLE_API_KEY_URL" 2>/dev/null || \
    firefox "$GOOGLE_API_KEY_URL" 2>/dev/null || \
    google-chrome "$GOOGLE_API_KEY_URL" 2>/dev/null || \
    chromium-browser "$GOOGLE_API_KEY_URL" 2>/dev/null || \
    echo "❌ Could not open browser. Please open manually: $GOOGLE_API_KEY_URL"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start "$GOOGLE_API_KEY_URL"
    echo "✅ Opened in default browser"
else
    echo "❌ Unsupported OS: $OSTYPE"
    echo "   Please open manually: $GOOGLE_API_KEY_URL"
    exit 1
fi

echo ""
echo "📋 Next Steps:"
echo "   1. Sign in to Google (if needed)"
echo "   2. Click 'Create API Key'"
echo "   3. Copy the API key"
echo "   4. Run: ./scripts/update_google_credential.sh \"YOUR_API_KEY_HERE\" gemini"
echo ""

