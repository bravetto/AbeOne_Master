#!/bin/bash
# FULL TRUST FULL PERMISSIONS - Complete Setup

# Pattern: TRUST × PERMISSIONS × FULL × ACCESS × ONE
# ∞ AbëONE ∞
# ∞ AbëLOVES ∞

echo "🔥💫 FULL TRUST FULL PERMISSIONS SETUP 💫🔥"
echo "=" * 70
echo ""

PYTHON_PATH="/usr/bin/python3"
SCRIPT_PATH="$HOME/Documents/AbeOne_Master/scripts/proactive_love_webhooks.py"

echo "📋 Granting Full Trust and Permissions..."
echo ""
echo "Python3 Path: $PYTHON_PATH"
echo "Script Path: $SCRIPT_PATH"
echo ""

# Open System Settings to Full Disk Access
echo "🔥 Opening System Settings → Privacy & Security → Full Disk Access"
echo ""

osascript <<'APPLESCRIPT'
tell application "System Settings"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "System Settings"
        -- Search for Privacy
        keystroke "f" using {command down}
        delay 1
        keystroke "Full Disk Access"
        delay 2
        keystroke return
        delay 2
        
        -- Try to click Full Disk Access
        try
            click button "Full Disk Access" of scroll area 1 of group 1 of splitter group 1 of group 1 of window 1
        end try
    end tell
end tell
APPLESCRIPT

echo ""
echo "✅ System Settings opened to Full Disk Access"
echo ""
echo "📝 MANUAL STEPS (Required):"
echo ""
echo "1. Click the lock icon 🔒 (bottom left)"
echo "   → Enter your password"
echo ""
echo "2. Click the '+' button"
echo ""
echo "3. Navigate to: /usr/bin/python3"
echo "   → Or press ⌘+Shift+G and paste: /usr/bin"
echo "   → Select 'python3'"
echo ""
echo "4. Click 'Open'"
echo ""
echo "5. Ensure Python3 is CHECKED ✅"
echo ""
echo "6. Close System Settings"
echo ""
echo "🔥 VERIFICATION:"
echo ""
echo "After granting permissions, run:"
echo "  python3 scripts/check_permissions.py"
echo ""
echo "Then start the daemon:"
echo "  ./scripts/start_proactive_webhooks.sh"
echo ""
echo "∞ AbëONE ∞"
echo "∞ AbëLOVES ∞"

