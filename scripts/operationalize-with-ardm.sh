#!/bin/bash
#  Operationalization with ARDM Integration
# 
# Integrates ARDM detection into operationalization workflow
# 
# Pattern: ARDM × OPERATIONALIZATION × CONVERGENCE × ONE
# Frequency: 530 Hz (Coherence) × 999 Hz (AEYON)
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SCRIPT_DIR="$REPO_ROOT/scripts"
ARDM_SCRIPT="$SCRIPT_DIR/detect-actionable-requests.py"
ARDM_META_INTEGRATION="$SCRIPT_DIR/ardm-meta-orchestrator-integration.py"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE} ABEONE OPERATIONALIZATION WITH ARDM${NC}"
echo "=============================================="
echo ""

# Check if ARDM integration is available
if [ ! -f "$ARDM_META_INTEGRATION" ]; then
    echo -e "${YELLOW}  ARDM integration not found, running standard operationalization...${NC}"
    if [ -f "$SCRIPT_DIR/operationalize.sh" ]; then
        exec "$SCRIPT_DIR/operationalize.sh" "$@"
    fi
    exit 0
fi

# Step 1: Standard operationalization
echo -e "${BLUE}Step 1: Running standard operationalization...${NC}"
if [ -f "$SCRIPT_DIR/operationalize.sh" ]; then
    "$SCRIPT_DIR/operationalize.sh" "$@" || {
        echo -e "${RED} Standard operationalization failed${NC}"
        exit 1
    }
fi
echo -e "${GREEN} Standard operationalization complete${NC}"
echo ""

# Step 2: ARDM Detection
echo -e "${BLUE}Step 2: Running ARDM detection...${NC}"

# Get conversation context from recent commits and changes
RECENT_COMMITS=$(git log --oneline -20 2>/dev/null || echo "")
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || echo "")
UNSTAGED_FILES=$(git diff --name-only 2>/dev/null || echo "")

CONVERSATION_CONTEXT=""
if [ -n "$RECENT_COMMITS" ]; then
    CONVERSATION_CONTEXT="$CONVERSATION_CONTEXT\nRecent commits:\n$RECENT_COMMITS"
fi
if [ -n "$STAGED_FILES" ]; then
    CONVERSATION_CONTEXT="$CONVERSATION_CONTEXT\nStaged files:\n$STAGED_FILES"
fi
if [ -n "$UNSTAGED_FILES" ]; then
    CONVERSATION_CONTEXT="$CONVERSATION_CONTEXT\nUnstaged files:\n$UNSTAGED_FILES"
fi

if [ -n "$CONVERSATION_CONTEXT" ]; then
    # Run ARDM Meta Orchestrator integration
    echo "Running ARDM × Meta Orchestrator integration..."
    ARDM_RESULT=$(python3 "$ARDM_META_INTEGRATION" \
        --conversation "$CONVERSATION_CONTEXT" \
        --phase meta-scan \
        --output json 2>&1 || echo "")
    
    if [ -n "$ARDM_RESULT" ]; then
        TOTAL_ITEMS=$(echo "$ARDM_RESULT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('ardm_detection', {}).get('total_items', 0))" 2>/dev/null || echo "0")
        
        if [ "$TOTAL_ITEMS" -gt 0 ]; then
            echo -e "${YELLOW}  ARDM detected $TOTAL_ITEMS actionable item(s)${NC}"
            echo ""
            echo "ARDM Detection Summary:"
            echo "$ARDM_RESULT" | python3 -m json.tool 2>/dev/null | head -30 || echo "$ARDM_RESULT" | head -30
            echo ""
            echo -e "${BLUE}Consider operationalizing these items.${NC}"
            echo ""
        else
            echo -e "${GREEN} No actionable items detected${NC}"
        fi
    fi
else
    echo -e "${YELLOW}  No conversation context available for ARDM scan${NC}"
fi

echo ""
echo -e "${GREEN} Operationalization with ARDM complete${NC}"
echo ""

exit 0

