#!/bin/bash

# AbëONE Server Opener
# Opens the server in your default browser
# LOVE = LIFE = ONE

SERVER_URL="http://localhost:3000"
API_URL="${SERVER_URL}/api/llm/chat"

echo "∞ AbëONE Server Opener ∞"
echo "========================"
echo ""

# Check if server is running
if ! lsof -ti:3000 > /dev/null 2>&1; then
    echo "❌ Server not running on port 3000"
    echo ""
    echo "Start the server with:"
    echo "  npm run dev"
    exit 1
fi

echo "✅ Server is running!"
echo ""
echo "Opening in browser..."
echo ""

# Detect OS and open browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$SERVER_URL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$SERVER_URL" 2>/dev/null || sensible-browser "$SERVER_URL" 2>/dev/null || echo "Please open: $SERVER_URL"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    start "$SERVER_URL"
else
    echo "Please open: $SERVER_URL"
fi

echo ""
echo "Frontend: $SERVER_URL"
echo "API:     $API_URL"
echo ""
echo "LOVE = LIFE = ONE"
echo "∞ AbëONE ∞"

