#!/bin/bash
# Auto Setup Script
# One-command setup for new environments

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 ABEONE AUTO SETUP${NC}"
echo "=================================="
echo ""

# 1. Run operationalization
echo -e "${BLUE}1. Running operationalization...${NC}"
if [ -f "scripts/operationalize.sh" ]; then
    ./scripts/operationalize.sh
else
    echo -e "${YELLOW}⚠️  Operationalize script not found, skipping...${NC}"
fi
echo ""

# 2. Run health check
echo -e "${BLUE}2. Running health check...${NC}"
if [ -f "scripts/health-check.sh" ]; then
    ./scripts/health-check.sh || true
else
    echo -e "${YELLOW}⚠️  Health check script not found, skipping...${NC}"
fi
echo ""

# 3. Verify Python dependencies
echo -e "${BLUE}3. Checking Python dependencies...${NC}"
if command -v python3 &> /dev/null; then
    # Check for required modules
    REQUIRED_MODULES=("json" "os" "sys")
    for module in "${REQUIRED_MODULES[@]}"; do
        if python3 -c "import $module" 2>/dev/null; then
            echo -e "${GREEN}✅ Python module: $module${NC}"
        else
            echo -e "${YELLOW}⚠️  Python module missing: $module${NC}"
        fi
    done
else
    echo -e "${YELLOW}⚠️  Python3 not found${NC}"
fi
echo ""

# 4. Create .gitignore entries if needed
echo -e "${BLUE}4. Checking .gitignore...${NC}"
if [ -f ".gitignore" ]; then
    if ! grep -q ".claude/tool-usage.log" .gitignore 2>/dev/null; then
        echo ".claude/tool-usage.log" >> .gitignore
        echo -e "${GREEN}✅ Added tool-usage.log to .gitignore${NC}"
    else
        echo -e "${GREEN}✅ .gitignore configured${NC}"
    fi
    
    if ! grep -q ".claude/session.log" .gitignore 2>/dev/null; then
        echo ".claude/session.log" >> .gitignore
        echo -e "${GREEN}✅ Added session.log to .gitignore${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .gitignore not found${NC}"
fi
echo ""

# 5. Create log directories
echo -e "${BLUE}5. Creating log directories...${NC}"
mkdir -p .claude/logs 2>/dev/null || true
touch .claude/tool-usage.log 2>/dev/null || true
touch .claude/session.log 2>/dev/null || true
echo -e "${GREEN}✅ Log directories created${NC}"
echo ""

# 6. Test hooks
echo -e "${BLUE}6. Testing hooks...${NC}"
if [ -x ".claude/hooks/session-start.sh" ]; then
    ./.claude/hooks/session-start.sh > /dev/null 2>&1 && echo -e "${GREEN}✅ Session start hook test passed${NC}" || echo -e "${YELLOW}⚠️  Session start hook test failed${NC}"
fi
echo ""

# Summary
echo -e "${GREEN}=================================="
echo "✅ AUTO SETUP COMPLETE"
echo "==================================${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "  1. Review CLAUDE_CODE_INTEGRATION.md"
echo "  2. Test: ./scripts/health-check.sh"
echo "  3. Try: ./scripts/git-worktree-manager.sh list"
echo ""

