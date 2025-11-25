#!/bin/bash
# SETUP VISUAL STATUS FOR ALL
# 
# Makes drift protection visually visible in Cursor for ALL users
# Creates visual displays, badges, and always-visible status
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║  🎨 SETTING UP VISUAL STATUS FOR ALL 🎨                        ║"
echo "║  Making drift protection visible in Cursor                      ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Create visual status file
echo "📦 Step 1: Creating visual status display..."
./scripts/create-visual-status.sh
echo "   ✅ Visual status file created: drift-visual-status.md"
echo ""

# Step 2: Update status files
echo "📦 Step 2: Updating status files..."
node scripts/update-drift-status.js
echo "   ✅ Status files updated"
echo ""

# Step 3: Create workspace settings
echo "📦 Step 3: Configuring Cursor workspace..."
mkdir -p "$WORKSPACE_ROOT/.vscode"

# Create settings if they don't exist or update them
if [ ! -f "$WORKSPACE_ROOT/.vscode/settings.json" ]; then
    cat > "$WORKSPACE_ROOT/.vscode/settings.json" << 'EOF'
{
  "files.associations": {
    ".drift-status.txt": "plaintext",
    ".drift-status.json": "json",
    "drift-visual-status.md": "markdown"
  },
  "files.watcherExclude": {
    "**/.drift-status.txt": false,
    "**/.drift-status.json": false,
    "**/drift-visual-status.md": false
  },
  "workbench.startupEditor": "none",
  "workbench.editor.enablePreview": false
}
EOF
    echo "   ✅ Workspace settings created"
else
    echo "   ✅ Workspace settings already exist"
fi
echo ""

# Step 4: Create README for visual setup
echo "📦 Step 4: Creating visual setup guide..."
cat > "$WORKSPACE_ROOT/VISUAL_SETUP_GUIDE.md" << 'EOF'
# 🎨 VISUAL STATUS SETUP GUIDE

**For**: All users who want visual drift protection status in Cursor

---

## 🚀 QUICK SETUP (One Time)

### Method 1: Visual Status File (Recommended)

1. **Open** `drift-visual-status.md` in Cursor
2. **Pin the tab** (right-click → Pin)
3. **Run watch script**:
   ```bash
   ./scripts/watch-visual-status.sh
   ```
4. **Status updates automatically** every 30 seconds!

### Method 2: HTML Dashboard

1. **Open** `drift-status-dashboard.html` in Cursor
2. **Right-click** → "Open Preview" or use browser preview
3. **Auto-refreshes** every 30 seconds!

### Method 3: Status Badge

1. **Open** `drift-status-badge.html` in Cursor
2. **Keep it open** in a small window
3. **Always visible** status badge!

---

## 📋 FILES TO KEEP OPEN

### For Always-Visible Status:

1. **`drift-visual-status.md`** - Visual markdown status (recommended)
2. **`drift-status-dashboard.html`** - Full HTML dashboard
3. **`drift-status-badge.html`** - Compact status badge
4. **`.drift-status.txt`** - Simple text status

**Choose one or more** - pin them for always-visible status!

---

## 🎯 RECOMMENDED SETUP

### Best Practice:

1. **Open** `drift-visual-status.md` in Cursor
2. **Pin the tab** (right-click → Pin)
3. **Split editor** to show status alongside code
4. **Run watch script**:
   ```bash
   ./scripts/watch-visual-status.sh
   ```

**Result**: Status always visible, updates automatically!

---

## 💡 TIPS

- **Pin tabs**: Keep status files pinned for easy access
- **Split view**: Show status alongside your code
- **Watch script**: Auto-updates keep status current
- **Multiple views**: Use different files for different needs

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**: ✅ **VISUAL STATUS READY**

EOF
echo "   ✅ Visual setup guide created"
echo ""

# Step 5: Initial visual status creation
echo "📦 Step 5: Creating initial visual status..."
./scripts/create-visual-status.sh
echo "   ✅ Initial visual status created"
echo ""

# Summary
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║  ✨ VISUAL STATUS SETUP COMPLETE ✨                              ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎨 VISUAL FILES CREATED:"
echo ""
echo "   1. drift-visual-status.md          - Visual markdown status"
echo "   2. drift-status-dashboard.html     - Full HTML dashboard"
echo "   3. drift-status-badge.html          - Compact status badge"
echo "   4. VISUAL_SETUP_GUIDE.md           - Setup guide"
echo ""
echo "🚀 QUICK START:"
echo ""
echo "   1. Open drift-visual-status.md in Cursor"
echo "   2. Pin the tab (right-click → Pin)"
echo "   3. Run: ./scripts/watch-visual-status.sh"
echo "   4. Status updates automatically every 30 seconds!"
echo ""
echo "✨ Visual status is now available for ALL users!"
echo ""

