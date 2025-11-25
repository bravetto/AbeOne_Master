#!/bin/bash
# Session End Hook
# Executes when Claude session ends

echo "✅ AbeOne Master Session Ended"
echo "🕐 Timestamp: $(date -Iseconds)"

# Log session summary if available
if [ -f ".claude/session.log" ]; then
    echo "📝 Session log available"
fi

