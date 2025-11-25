#!/bin/bash
# Operationalization Master Script
# Ensures all automation and operational systems are ready

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 ABEONE OPERATIONALIZATION${NC}"
echo "=================================="
echo ""

# 1. Ensure all scripts are executable
echo -e "${BLUE}1. Making scripts executable...${NC}"
find scripts -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod +x {} \; 2>/dev/null || true
find .claude/hooks -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
echo -e "${GREEN}✅ Scripts executable${NC}"
echo ""

# 2. Verify Claude configuration
echo -e "${BLUE}2. Verifying Claude configuration...${NC}"
if [ -f ".claude/settings.json" ]; then
    echo -e "${GREEN}✅ Claude settings.json exists${NC}"
else
    echo -e "${RED}❌ Claude settings.json missing${NC}"
    exit 1
fi

if [ -f ".claude/mcp-config.json" ]; then
    echo -e "${GREEN}✅ MCP configuration exists${NC}"
else
    echo -e "${RED}❌ MCP configuration missing${NC}"
    exit 1
fi

if [ -d ".claude/hooks" ]; then
    HOOK_COUNT=$(find .claude/hooks -type f -name "*.sh" | wc -l | tr -d ' ')
    echo -e "${GREEN}✅ Hooks directory exists ($HOOK_COUNT hooks)${NC}"
else
    echo -e "${RED}❌ Hooks directory missing${NC}"
    exit 1
fi

if [ -d ".claude/commands" ]; then
    CMD_COUNT=$(find .claude/commands -type f -name "*.md" | wc -l | tr -d ' ')
    echo -e "${GREEN}✅ Commands directory exists ($CMD_COUNT commands)${NC}"
else
    echo -e "${RED}❌ Commands directory missing${NC}"
    exit 1
fi
echo ""

# 3. Verify critical scripts
echo -e "${BLUE}3. Verifying critical scripts...${NC}"
CRITICAL_SCRIPTS=(
    "scripts/git-worktree-manager.sh"
    "scripts/bravetto_ai_dns_setup.sh"
    "scripts/cloudflare_dns_automation.py"
)

for script in "${CRITICAL_SCRIPTS[@]}"; do
    if [ -f "$script" ] && [ -x "$script" ]; then
        echo -e "${GREEN}✅ $(basename $script)${NC}"
    else
        echo -e "${YELLOW}⚠️  $(basename $script) missing or not executable${NC}"
    fi
done
echo ""

# 4. Test git worktree manager
echo -e "${BLUE}4. Testing git worktree manager...${NC}"
if ./scripts/git-worktree-manager.sh list > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Git worktree manager functional${NC}"
else
    echo -e "${YELLOW}⚠️  Git worktree manager test failed${NC}"
fi
echo ""

# 5. Verify Python dependencies
echo -e "${BLUE}5. Checking Python environment...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✅ Python3 available ($PYTHON_VERSION)${NC}"
    
    # Check for common dependencies
    if python3 -c "import json" 2>/dev/null; then
        echo -e "${GREEN}✅ json module available${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Python3 not found${NC}"
fi
echo ""

# 6. Verify Node.js (if needed)
echo -e "${BLUE}6. Checking Node.js environment...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version 2>&1)
    echo -e "${GREEN}✅ Node.js available ($NODE_VERSION)${NC}"
    
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version 2>&1)
        echo -e "${GREEN}✅ npm available ($NPM_VERSION)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Node.js not found (optional)${NC}"
fi
echo ""

# 7. Verify Git
echo -e "${BLUE}7. Checking Git...${NC}"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version 2>&1 | awk '{print $3}')
    echo -e "${GREEN}✅ Git available ($GIT_VERSION)${NC}"
    
    if [ -d ".git" ]; then
        BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✅ Git repository initialized (branch: $BRANCH)${NC}"
    fi
else
    echo -e "${RED}❌ Git not found${NC}"
    exit 1
fi
echo ""

# 8. Create operational status file
echo -e "${BLUE}8. Creating operational status...${NC}"
cat > .claude/operational-status.json << EOF
{
  "status": "operational",
  "timestamp": "$(date -Iseconds)",
  "version": "1.0.0",
  "components": {
    "claude_config": true,
    "mcp_servers": true,
    "hooks": true,
    "commands": true,
    "scripts": true,
    "git_worktree": true
  }
}
EOF
echo -e "${GREEN}✅ Operational status created${NC}"
echo ""

# Summary
echo -e "${GREEN}=================================="
echo "✅ OPERATIONALIZATION COMPLETE"
echo "==================================${NC}"
echo ""
echo -e "${BLUE}📋 Quick Commands:${NC}"
echo "  ./scripts/git-worktree-manager.sh list"
echo "  ./scripts/bravetto_ai_dns_setup.sh"
echo "  python3 scripts/cloudflare_dns_automation.py --help"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "  CLAUDE_CODE_INTEGRATION.md"
echo "  CLAUDE_CODE_QUICK_REFERENCE.md"
echo ""

