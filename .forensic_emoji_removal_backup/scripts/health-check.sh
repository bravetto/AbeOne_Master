#!/bin/bash
# System Health Check
# Validates all automation and operational systems

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

check() {
    local name="$1"
    local command="$2"
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $name${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}❌ $name${NC}"
        ((FAIL++))
        return 1
    fi
}

warn() {
    local name="$1"
    echo -e "${YELLOW}⚠️  $name${NC}"
    ((WARN++))
}

echo -e "${BLUE}🏥 ABEONE HEALTH CHECK${NC}"
echo "=================================="
echo ""

# Claude Configuration
echo -e "${BLUE}Claude Configuration:${NC}"
check "Settings file exists" "[ -f .claude/settings.json ]"
check "MCP config exists" "[ -f .claude/mcp-config.json ]"
check "Hooks directory exists" "[ -d .claude/hooks ]"
check "Commands directory exists" "[ -d .claude/commands ]"
echo ""

# Scripts
echo -e "${BLUE}Scripts:${NC}"
check "Git worktree manager" "[ -x scripts/git-worktree-manager.sh ]"
check "DNS automation" "[ -x scripts/cloudflare_dns_automation.py ]"
check "Operationalize script" "[ -x scripts/operationalize.sh ]"
echo ""

# Hooks
echo -e "${BLUE}Hooks:${NC}"
check "Session start hook" "[ -x .claude/hooks/session-start.sh ]"
check "Session end hook" "[ -x .claude/hooks/session-end.sh ]"
check "Pre-tool hook" "[ -x .claude/hooks/pre-tool-use.sh ]"
check "Post-tool hook" "[ -x .claude/hooks/post-tool-use.sh ]"
echo ""

# Commands
echo -e "${BLUE}Custom Commands:${NC}"
check "Converge command" "[ -f .claude/commands/converge.md ]"
check "Guardian command" "[ -f .claude/commands/guardian.md ]"
check "Worktree command" "[ -f .claude/commands/worktree.md ]"
echo ""

# Tools
echo -e "${BLUE}Tools:${NC}"
if command -v git &> /dev/null; then
    check "Git available" "true"
else
    warn "Git not found"
fi

if command -v python3 &> /dev/null; then
    check "Python3 available" "true"
else
    warn "Python3 not found"
fi

if command -v node &> /dev/null; then
    check "Node.js available" "true"
else
    warn "Node.js not found (optional)"
fi
echo ""

# Git Repository
echo -e "${BLUE}Git Repository:${NC}"
if [ -d ".git" ]; then
    check "Git repository initialized" "true"
    BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
    echo -e "${BLUE}   Current branch: $BRANCH${NC}"
    
    # Check for worktrees
    if git worktree list > /dev/null 2>&1; then
        WT_COUNT=$(git worktree list | wc -l | tr -d ' ')
        echo -e "${BLUE}   Active worktrees: $WT_COUNT${NC}"
    fi
else
    warn "Not a git repository"
fi
echo ""

# Summary
echo "=================================="
echo -e "${GREEN}✅ Passed: $PASS${NC}"
echo -e "${RED}❌ Failed: $FAIL${NC}"
echo -e "${YELLOW}⚠️  Warnings: $WARN${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL SYSTEMS OPERATIONAL${NC}"
    exit 0
else
    echo -e "${RED}⚠️  SOME CHECKS FAILED${NC}"
    exit 1
fi

