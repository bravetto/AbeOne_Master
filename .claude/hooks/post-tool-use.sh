#!/bin/bash
# Post-Tool Use Hook
# Executes after Claude uses a tool

TOOL_NAME="$1"
EXIT_CODE="$2"
echo "✅ Post-tool: $TOOL_NAME (exit: $EXIT_CODE)"

# Log tool usage
echo "$(date -Iseconds) | $TOOL_NAME | $EXIT_CODE" >> .claude/tool-usage.log 2>/dev/null || true

