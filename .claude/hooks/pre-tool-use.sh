#!/bin/bash
# Pre-Tool Use Hook
# Executes before Claude uses a tool

TOOL_NAME="$1"
echo "🔧 Pre-tool: $TOOL_NAME"

# Safety checks for destructive operations
case "$TOOL_NAME" in
    *delete*|*remove*|*rm*)
        echo "⚠️  Destructive operation detected"
        ;;
esac

