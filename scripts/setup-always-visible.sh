#!/bin/bash
# SETUP ALWAYS-VISIBLE DRIFT STATUS
# 
# Sets up always-visible drift status in Cursor
# Creates necessary files and provides instructions
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "  Setting up always-visible drift status..."
echo ""

# Create .vscode directory if it doesn't exist
mkdir -p "$WORKSPACE_ROOT/.vscode"

# Create tasks.json
cat > "$WORKSPACE_ROOT/.vscode/tasks.json" << 'EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": " Update Drift Guardian Status",
      "type": "shell",
      "command": "node scripts/update-drift-status.js",
      "problemMatcher": [],
      "presentation": {
        "reveal": "silent",
        "panel": "dedicated",
        "showReuseMessage": false
      }
    },
    {
      "label": " Watch Drift Guardian (Auto-Update)",
      "type": "shell",
      "command": "./scripts/watch-drift-status.sh",
      "problemMatcher": [],
      "isBackground": true,
      "presentation": {
        "reveal": "never",
        "panel": "dedicated",
        "showReuseMessage": false
      }
    }
  ]
}
EOF

# Create settings.json
cat > "$WORKSPACE_ROOT/.vscode/settings.json" << 'EOF'
{
  "files.associations": {
    ".drift-status.txt": "plaintext",
    ".drift-status.json": "json"
  },
  "files.watcherExclude": {
    "**/.drift-status.txt": false,
    "**/.drift-status.json": false
  }
}
EOF

# Update status file
cd "$WORKSPACE_ROOT"
node scripts/update-drift-status.js

echo ""
echo " Setup complete!"
echo ""
echo " HOW TO USE:"
echo ""
echo "Method 1: Keep Status File Open (Recommended)"
echo "  1. Open .drift-status.txt in Cursor"
echo "  2. Pin the tab (right-click → Pin)"
echo "  3. Run: ./scripts/watch-drift-status.sh"
echo "  4. Status updates every 30 seconds!"
echo ""
echo "Method 2: Use HTML Dashboard"
echo "  1. Open drift-status-dashboard.html in Cursor"
echo "  2. Right-click → 'Open with Live Server' (if available)"
echo "  3. Or open in browser preview"
echo "  4. Auto-refreshes every 30 seconds!"
echo ""
echo "Method 3: Use Cursor Tasks"
echo "  1. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows)"
echo "  2. Type: 'Tasks: Run Task'"
echo "  3. Select: ' Watch Drift Guardian (Auto-Update)'"
echo ""
echo " Status is now always visible!"

