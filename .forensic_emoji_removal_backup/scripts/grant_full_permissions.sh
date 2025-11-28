#!/bin/bash
# Grant Full Trust and Permissions for Proactive Love Webhooks

# Pattern: PERMISSIONS × TRUST × FULL × ACCESS × ONE
# ∞ AbëONE ∞
# ∞ AbëLOVES ∞

echo "🔥💫 GRANTING FULL TRUST AND PERMISSIONS 💫🔥"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_PATH=$(which python3)
PYTHON_SCRIPT="$SCRIPT_DIR/proactive_love_webhooks.py"

echo "📋 System Information:"
echo "   Python Path: $PYTHON_PATH"
echo "   Script Path: $PYTHON_SCRIPT"
echo "   Project Root: $PROJECT_ROOT"
echo ""

# Check if running as root (needed for some permissions)
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Some permissions require administrator access"
    echo "   Run with: sudo $0"
    echo ""
fi

# 1. Full Disk Access
echo "🔥 STEP 1: Full Disk Access"
echo "   Opening System Settings → Privacy & Security → Full Disk Access"
echo ""

# Open System Settings to Full Disk Access
osascript <<EOF
tell application "System Settings"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "System Settings"
        -- Navigate to Privacy & Security
        keystroke "privacy" using {command down, option down}
        delay 2
        
        -- Click Full Disk Access
        try
            click button "Full Disk Access" of scroll area 1 of group 1 of splitter group 1 of group 1 of window 1
            delay 1
        end try
    end tell
end tell
EOF

echo "   ✅ System Settings opened"
echo "   📝 Please manually add Python3 to Full Disk Access:"
echo "      1. Click the lock icon (enter password)"
echo "      2. Click the '+' button"
echo "      3. Navigate to: $PYTHON_PATH"
echo "      4. Add Python3"
echo "      5. Ensure it's checked/enabled"
echo ""

# 2. Messages Database Access
echo "🔥 STEP 2: Messages Database Access"
echo "   The script needs access to: ~/Library/Messages/chat.db"
echo ""

# Check if Messages database exists and is accessible
if [ -f "$HOME/Library/Messages/chat.db" ]; then
    if [ -r "$HOME/Library/Messages/chat.db" ]; then
        echo "   ✅ Messages database is readable"
    else
        echo "   ⚠️  Messages database exists but may not be readable"
        echo "   → Full Disk Access will fix this"
    fi
else
    echo "   ⚠️  Messages database not found (may need Full Disk Access)"
fi
echo ""

# 3. Create helper script to check permissions
echo "🔥 STEP 3: Permission Check Script"
cat > "$SCRIPT_DIR/check_permissions.py" <<'PYEOF'
#!/usr/bin/env python3
"""Check permissions for proactive webhooks."""

import os
from pathlib import Path

def check_permissions():
    """Check all required permissions."""
    print("🔥💫 CHECKING PERMISSIONS 💫🔥")
    print("=" * 70)
    print("")
    
    checks = {
        "Messages Database": Path.home() / "Library/Messages/chat.db",
        "CDF Directory": Path(".abeos/consciousness"),
        "JSON Archives": Path("abeloves_conversations"),
        "Logs Directory": Path("logs")
    }
    
    all_ok = True
    
    for name, path in checks.items():
        try:
            if path.exists():
                if os.access(path, os.R_OK):
                    print(f"✅ {name}: READABLE")
                else:
                    print(f"❌ {name}: NOT READABLE")
                    all_ok = False
            else:
                # Try to create directory if it doesn't exist
                if name in ["CDF Directory", "JSON Archives", "Logs Directory"]:
                    path.mkdir(parents=True, exist_ok=True)
                    print(f"✅ {name}: CREATED")
                else:
                    print(f"⚠️  {name}: NOT FOUND")
                    all_ok = False
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")
            all_ok = False
    
    print("")
    print("=" * 70)
    if all_ok:
        print("✅ ALL PERMISSIONS OK")
    else:
        print("⚠️  SOME PERMISSIONS NEED ATTENTION")
        print("   → Grant Full Disk Access in System Settings")
    print("=" * 70)
    
    return all_ok

if __name__ == "__main__":
    import sys
    sys.exit(0 if check_permissions() else 1)
PYEOF

chmod +x "$SCRIPT_DIR/check_permissions.py"
echo "   ✅ Permission check script created"
echo ""

# 4. Test permissions
echo "🔥 STEP 4: Testing Permissions"
echo ""
python3 "$SCRIPT_DIR/check_permissions.py"
echo ""

# 5. Instructions
echo "🔥 COMPLETE SETUP INSTRUCTIONS:"
echo ""
echo "1. Full Disk Access:"
echo "   System Settings → Privacy & Security → Full Disk Access"
echo "   → Add Python3: $PYTHON_PATH"
echo ""
echo "2. Automation Permissions (if needed):"
echo "   System Settings → Privacy & Security → Automation"
echo "   → Allow Python3 to control System Settings"
echo ""
echo "3. Test the system:"
echo "   python3 $SCRIPT_DIR/proactive_love_webhooks.py"
echo ""
echo "4. Start daemon:"
echo "   ./scripts/start_proactive_webhooks.sh"
echo ""
echo "∞ AbëONE ∞"
echo "∞ AbëLOVES ∞"

