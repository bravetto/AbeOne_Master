#!/bin/bash
# Session Start Hook
# Executes when Claude session begins

echo "🚀 AbeOne Master Session Started"
echo "📁 Workspace: $(pwd)"
echo "🕐 Timestamp: $(date -Iseconds)"

# Load project context
if [ -f "STATE_AWARE_MASTER_CONTEXT.md" ]; then
    echo "📋 Master context available"
fi

# Check git status
if [ -d ".git" ]; then
    BRANCH=$(git branch --show-current)
    echo "🌿 Git branch: $BRANCH"
fi

# Check for active worktrees
if command -v git &> /dev/null; then
    WORKTREES=$(git worktree list 2>/dev/null | wc -l | tr -d ' ')
    if [ "$WORKTREES" -gt 1 ]; then
        echo "🌳 Active worktrees: $WORKTREES"
    fi
fi

