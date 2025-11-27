#!/bin/bash
# Share Shiny Happy People App - Create Public Tunnel
# Pattern: UNITY × LOVE × JOY × CONNECTION × ONE
# ∞ AbëONE ∞

echo "∞ AbëONE ∞"
echo "Creating public tunnel for Shiny Happy People..."
echo ""

# Check if cloudflared is available
if ! command -v cloudflared &> /dev/null; then
    echo "⚠ cloudflared not found. Installing..."
    brew install cloudflared
fi

# Check if app is running
if ! curl -s http://localhost:53009/ > /dev/null 2>&1; then
    echo "⚠ App not running on localhost:53009"
    echo "Please start the app first:"
    echo "  cd abeone_app && flutter run -d chrome"
    exit 1
fi

echo "✓ App is running on localhost:53009"
echo ""
echo "Creating public tunnel..."
echo "This will give you a public URL like: https://xxxx-xxxx.trycloudflare.com"
echo ""
echo "Press Ctrl+C to stop the tunnel when done sharing."
echo ""

# Create tunnel
cloudflared tunnel --url http://localhost:53009

