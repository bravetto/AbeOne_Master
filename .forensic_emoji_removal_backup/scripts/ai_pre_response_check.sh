#!/bin/bash
# AI Pre-Response Checklist Runner
# Ensures memory files are checked before responding

MEMORY_DIR="/Users/michaelmataluni/Documents/AbeOne_Master/docs/reference"
RELATIONSHIP_MEMORY="$MEMORY_DIR/AI_RELATIONSHIP_MEMORY.md"
GUARDRAILS="$MEMORY_DIR/AI_GUARDRAILS_USER_PREFERENCES.md"
CHECKLIST="$MEMORY_DIR/AI_PRE_RESPONSE_CHECKLIST.md"

echo "🔍 AI PRE-RESPONSE CHECKLIST"
echo "=============================="
echo ""

# Check if files exist
if [ ! -f "$RELATIONSHIP_MEMORY" ]; then
    echo "❌ Missing: AI_RELATIONSHIP_MEMORY.md"
else
    echo "✅ Found: AI_RELATIONSHIP_MEMORY.md"
fi

if [ ! -f "$GUARDRAILS" ]; then
    echo "❌ Missing: AI_GUARDRAILS_USER_PREFERENCES.md"
else
    echo "✅ Found: AI_GUARDRAILS_USER_PREFERENCES.md"
fi

if [ ! -f "$CHECKLIST" ]; then
    echo "❌ Missing: AI_PRE_RESPONSE_CHECKLIST.md"
else
    echo "✅ Found: AI_PRE_RESPONSE_CHECKLIST.md"
fi

echo ""
echo "📋 REMINDER: Read these files before responding"
echo "  1. $RELATIONSHIP_MEMORY"
echo "  2. $GUARDRAILS"
echo "  3. $CHECKLIST"
echo ""
echo "Pattern: CHECKLIST × MEMORY × RELATIONSHIP × ONE"
echo "∞ AbëONE ∞"

