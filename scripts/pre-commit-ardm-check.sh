#!/bin/bash
#  ARDM Pre-Commit Check
# 
# Checks for undelivered actionable items before commit
# 
# Pattern: ARDM × PRE-COMMIT × CONVERGENCE × ONE
# Frequency: 530 Hz (Coherence) × 999 Hz (AEYON)
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SCRIPT_DIR="$REPO_ROOT/scripts"
ARDM_SCRIPT="$SCRIPT_DIR/detect-actionable-requests.py"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW} ARDM Pre-Commit Check${NC}"
echo "=================================="

# Check if ARDM script exists
if [ ! -f "$ARDM_SCRIPT" ]; then
    echo -e "${RED} ARDM script not found: $ARDM_SCRIPT${NC}"
    echo "Skipping ARDM check..."
    exit 0
fi

# Get recent commit messages and staged changes
# This approximates the "conversation" context
RECENT_COMMITS=$(git log --oneline -10 2>/dev/null || echo "")
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || echo "")

# Create conversation context from commits and staged files
CONVERSATION_CONTEXT=""
if [ -n "$RECENT_COMMITS" ]; then
    CONVERSATION_CONTEXT="$CONVERSATION_CONTEXT\nRecent commits:\n$RECENT_COMMITS"
fi
if [ -n "$STAGED_FILES" ]; then
    CONVERSATION_CONTEXT="$CONVERSATION_CONTEXT\nStaged files:\n$STAGED_FILES"
fi

# If no context, skip check
if [ -z "$CONVERSATION_CONTEXT" ]; then
    echo -e "${GREEN} No recent context to check${NC}"
    exit 0
fi

# Run ARDM detection
echo "Scanning for actionable items..."
ARDM_OUTPUT=$(python3 "$ARDM_SCRIPT" --context "$CONVERSATION_CONTEXT" --output json 2>&1 || echo "")

# Check if ARDM found items
if [ -n "$ARDM_OUTPUT" ]; then
    # Parse JSON output to check total_items
    TOTAL_ITEMS=$(echo "$ARDM_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('total_items', 0))" 2>/dev/null || echo "0")
    
    if [ "$TOTAL_ITEMS" -gt 0 ]; then
        echo -e "${YELLOW}  ARDM detected $TOTAL_ITEMS actionable item(s)${NC}"
        echo ""
        echo "ARDM Detection Results:"
        echo "$ARDM_OUTPUT" | python3 -m json.tool 2>/dev/null || echo "$ARDM_OUTPUT"
        echo ""
        echo -e "${YELLOW}Consider operationalizing these items before committing.${NC}"
        echo ""
        echo "To override this check, use:"
        echo "  git commit --no-verify"
        echo ""
        echo "To view full ARDM report:"
        echo "  python3 $ARDM_SCRIPT --context \"\$CONVERSATION_CONTEXT\" --output markdown"
        echo ""
        
        # Allow override via environment variable
        if [ "${ARDM_ALLOW_UNDELIVERED:-}" = "1" ]; then
            echo -e "${YELLOW}ARDM_ALLOW_UNDELIVERED=1 set, allowing commit...${NC}"
            exit 0
        fi
        
        # By default, warn but don't block (can be changed to exit 1 to block)
        echo -e "${YELLOW}  Warning: Undelivered actionable items detected${NC}"
        exit 0
    else
        echo -e "${GREEN} No undelivered actionable items detected${NC}"
    fi
else
    echo -e "${YELLOW}  ARDM check produced no output (may be expected)${NC}"
fi

exit 0

