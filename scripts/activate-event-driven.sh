#!/bin/bash
# ACTIVATE EVENT-DRIVEN ORGANISM
# 
# Activates the event-driven synchronization system
# 
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "ACTIVATING EVENT-DRIVEN ORGANISM"
echo "===================================="
echo ""

# Step 1: Install Git Hooks
echo "[1/3] Installing Git Hooks..."
chmod +x "$WORKSPACE_ROOT/.git/hooks/pre-commit" 2>/dev/null
chmod +x "$WORKSPACE_ROOT/.git/hooks/pre-push" 2>/dev/null

if [ -f "$WORKSPACE_ROOT/.git/hooks/pre-commit" ] && [ -x "$WORKSPACE_ROOT/.git/hooks/pre-commit" ]; then
  echo "   [OK] pre-commit hook active"
else
  echo "   [WARN] pre-commit hook not found - run: ./scripts/install-git-hooks.sh"
fi

if [ -f "$WORKSPACE_ROOT/.git/hooks/pre-push" ] && [ -x "$WORKSPACE_ROOT/.git/hooks/pre-push" ]; then
  echo "   [OK] pre-push hook active"
else
  echo "   [WARN] pre-push hook not found - run: ./scripts/install-git-hooks.sh"
fi

echo ""

# Step 2: Initial pulse to sync everything
echo "[2/3] Running initial pulse..."
cd "$WORKSPACE_ROOT"
node scripts/pulse.js

echo ""
echo "[3/3] Optional: Start boundary watcher"
echo "   Run: node scripts/boundary-watcher-native.js"
echo "   (or: node scripts/boundary-watcher.js if chokidar is installed)"
echo ""

echo "[OK] EVENT-DRIVEN ORGANISM ACTIVATED"
echo ""
echo "Usage:"
echo "  - Git commits/pushes will auto-update source of truth"
echo "  - Run 'node scripts/pulse.js' anytime for manual sync"
echo "  - Start boundary-watcher for real-time file watching (optional)"
echo ""

