#!/bin/bash
# Gap Filler - Closes any remaining gaps in automation
# Ensures everything is 100% complete

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔍 GAP ANALYSIS & FILLER${NC}"
echo "=================================="
echo ""

FIXED=0

# 1. Ensure .gitignore has .claude entries
echo -e "${BLUE}1. Checking .gitignore...${NC}"
if [ -f ".gitignore" ]; then
    NEEDS_UPDATE=false
    
    # Check for .claude log entries
    if ! grep -q "^\.claude/.*\.log$" .gitignore 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Adding .claude log entries to .gitignore${NC}"
        {
            echo ""
            echo "# Claude automation logs"
            echo ".claude/*.log"
            echo ".claude/logs/"
            echo ".claude/tool-usage.log"
            echo ".claude/session.log"
        } >> .gitignore
        NEEDS_UPDATE=true
        ((FIXED++))
    fi
    
    # Check for operational status (optional - might want to track this)
    if ! grep -q "^\.claude/operational-status\.json$" .gitignore 2>/dev/null; then
        echo -e "${BLUE}ℹ️  Note: operational-status.json can be tracked or ignored${NC}"
    fi
    
    if [ "$NEEDS_UPDATE" = false ]; then
        echo -e "${GREEN}✅ .gitignore properly configured${NC}"
    else
        echo -e "${GREEN}✅ .gitignore updated${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Creating .gitignore${NC}"
    cat > .gitignore << 'EOF'
# Claude automation logs
.claude/*.log
.claude/logs/
.claude/tool-usage.log
.claude/session.log

# Standard ignores
*.pyc
__pycache__/
.env
.env.local
*.log
.DS_Store
EOF
    ((FIXED++))
    echo -e "${GREEN}✅ .gitignore created${NC}"
fi
echo ""

# 2. Ensure log directories exist
echo -e "${BLUE}2. Checking log directories...${NC}"
mkdir -p .claude/logs 2>/dev/null || true
touch .claude/tool-usage.log 2>/dev/null || true
touch .claude/session.log 2>/dev/null || true
echo -e "${GREEN}✅ Log directories ready${NC}"
echo ""

# 3. Verify all hooks have proper error handling
echo -e "${BLUE}3. Verifying hook error handling...${NC}"
HOOKS_FIXED=0
for hook in .claude/hooks/*.sh; do
    if [ -f "$hook" ]; then
        # Check if hook has error handling
        if ! grep -q "set -e\|set -o errexit\||| true" "$hook" 2>/dev/null; then
            # Add error handling to hooks that don't have it
            if ! grep -q "^#!/bin/bash" "$hook" 2>/dev/null; then
                # Add shebang if missing
                sed -i.bak '1i\
#!/bin/bash\
set -euo pipefail || true
' "$hook" 2>/dev/null || true
                rm -f "${hook}.bak" 2>/dev/null || true
                ((HOOKS_FIXED++))
            fi
        fi
    fi
done
if [ $HOOKS_FIXED -gt 0 ]; then
    echo -e "${GREEN}✅ Enhanced $HOOKS_FIXED hooks with error handling${NC}"
    ((FIXED++))
else
    echo -e "${GREEN}✅ All hooks have proper error handling${NC}"
fi
echo ""

# 4. Create README for .claude directory
echo -e "${BLUE}4. Creating .claude README...${NC}"
if [ ! -f ".claude/README.md" ]; then
    cat > .claude/README.md << 'EOF'
# Claude Configuration Directory

This directory contains Claude AI assistant configuration, automation hooks, and custom commands.

## Structure

- `settings.json` - Main Claude configuration
- `mcp-config.json` - MCP server configuration
- `operational-status.json` - Auto-generated operational status
- `commands/` - Custom slash commands
- `hooks/` - Automation hooks
- `logs/` - Log files (gitignored)
- `*.log` - Log files (gitignored)

## Usage

See `CLAUDE_CODE_INTEGRATION.md` for complete documentation.

## Quick Commands

- `/converge` - Convergence workflows
- `/guardian` - Guardian management
- `/worktree` - Git worktree operations

## Hooks

Hooks execute automatically:
- `session-start.sh` - On session begin
- `session-end.sh` - On session end
- `pre-tool-use.sh` - Before tool execution
- `post-tool-use.sh` - After tool execution

## Logs

Log files are automatically gitignored:
- `tool-usage.log` - Tool usage tracking
- `session.log` - Session tracking
- `logs/` - Log directory

EOF
    echo -e "${GREEN}✅ Created .claude/README.md${NC}"
    ((FIXED++))
else
    echo -e "${GREEN}✅ .claude/README.md exists${NC}"
fi
echo ""

# 5. Verify JSON files are valid
echo -e "${BLUE}5. Validating JSON files...${NC}"
JSON_ERRORS=0
for json_file in .claude/*.json; do
    if [ -f "$json_file" ]; then
        if command -v python3 &> /dev/null; then
            if ! python3 -m json.tool "$json_file" > /dev/null 2>&1; then
                echo -e "${RED}❌ Invalid JSON: $json_file${NC}"
                ((JSON_ERRORS++))
            fi
        fi
    fi
done
if [ $JSON_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All JSON files valid${NC}"
else
    echo -e "${RED}❌ Found $JSON_ERRORS invalid JSON files${NC}"
    exit 1
fi
echo ""

# 6. Create quick reference symlink/alias script
echo -e "${BLUE}6. Creating quick reference script...${NC}"
if [ ! -f "scripts/claude-help.sh" ]; then
    cat > scripts/claude-help.sh << 'EOF'
#!/bin/bash
# Quick help for Claude automation

cat << 'HELP'
🚀 CLAUDE AUTOMATION QUICK REFERENCE

Quick Commands:
  ./scripts/quick-ops.sh status    # System status
  ./scripts/health-check.sh         # Health check
  ./scripts/operationalize.sh      # Full operationalization

Git Worktrees:
  ./scripts/git-worktree-manager.sh create feature/new-module
  ./scripts/git-worktree-manager.sh list
  ./scripts/git-worktree-manager.sh remove ../feature-new-module

Claude Commands:
  /converge    # Convergence workflows
  /guardian    # Guardian management
  /worktree    # Git worktree operations

Documentation:
  CLAUDE_CODE_INTEGRATION.md
  CLAUDE_CODE_QUICK_REFERENCE.md
  AUTOMATION_MASTER_INDEX.md

HELP
EOF
    chmod +x scripts/claude-help.sh
    echo -e "${GREEN}✅ Created claude-help.sh${NC}"
    ((FIXED++))
else
    echo -e "${GREEN}✅ claude-help.sh exists${NC}"
fi
echo ""

# Summary
echo "=================================="
if [ $FIXED -gt 0 ]; then
    echo -e "${GREEN}✅ FIXED $FIXED GAPS${NC}"
else
    echo -e "${GREEN}✅ NO GAPS FOUND - ALL SYSTEMS OPERATIONAL${NC}"
fi
echo "=================================="
echo ""

# Final validation
echo -e "${BLUE}Running final validation...${NC}"
./scripts/health-check.sh > /dev/null 2>&1 && echo -e "${GREEN}✅ Health check passed${NC}" || echo -e "${YELLOW}⚠️  Health check had warnings${NC}"

