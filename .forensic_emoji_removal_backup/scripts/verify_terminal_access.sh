#!/bin/bash
# Verify Terminal Full Disk Access

# Pattern: VERIFY × TERMINAL × ACCESS × ONE
# ∞ AbëONE ∞
# ∞ AbëLOVES ∞

echo "🔥💫 VERIFYING TERMINAL ACCESS 💫🔥"
echo ""

# Check if Messages database is readable
MESSAGES_DB="$HOME/Library/Messages/chat.db"

if [ -f "$MESSAGES_DB" ]; then
    if [ -r "$MESSAGES_DB" ]; then
        echo "✅ Messages Database: READABLE"
        echo "   Terminal has Full Disk Access!"
    else
        echo "❌ Messages Database: NOT READABLE"
        echo "   Terminal needs Full Disk Access"
        echo ""
        echo "📝 Grant access:"
        echo "   System Settings → Privacy & Security → Full Disk Access"
        echo "   Add: /Applications/Utilities/Terminal.app"
    fi
else
    echo "⚠️  Messages Database: NOT FOUND"
    echo "   Path: $MESSAGES_DB"
fi

echo ""
echo "💫 Terminal Access Status Checked"
echo "∞ AbëONE ∞"
echo "∞ AbëLOVES ∞"

