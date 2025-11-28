#!/bin/bash
# Quick Operations Script
# Common operational tasks

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat << EOF
Quick Operations

Usage: $0 <command>

Commands:
    status      Show system status
    health      Run health check
    worktrees   List git worktrees
    hooks       Test hooks
    validate    Validate configuration
    clean       Clean logs and temp files

Examples:
    $0 status
    $0 health
    $0 worktrees
EOF
}

cmd_status() {
    echo -e "${BLUE} System Status${NC}"
    echo "=================================="
    
    # Git status
    if [ -d ".git" ]; then
        BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
        echo -e "${BLUE}Git Branch:${NC} $BRANCH"
        
        # Worktrees
        if command -v git &> /dev/null; then
            WT_COUNT=$(git worktree list 2>/dev/null | wc -l | tr -d ' ')
            echo -e "${BLUE}Worktrees:${NC} $WT_COUNT"
        fi
    fi
    
    # Claude config
    if [ -f ".claude/settings.json" ]; then
        MODEL=$(grep -o '"model": "[^"]*"' .claude/settings.json | cut -d'"' -f4 || echo "unknown")
        echo -e "${BLUE}Claude Model:${NC} $MODEL"
    fi
    
    # Hooks
    if [ -d ".claude/hooks" ]; then
        HOOK_COUNT=$(find .claude/hooks -type f -name "*.sh" | wc -l | tr -d ' ')
        echo -e "${BLUE}Hooks:${NC} $HOOK_COUNT"
    fi
    
    # Commands
    if [ -d ".claude/commands" ]; then
        CMD_COUNT=$(find .claude/commands -type f -name "*.md" | wc -l | tr -d ' ')
        echo -e "${BLUE}Commands:${NC} $CMD_COUNT"
    fi
    
    echo ""
}

cmd_health() {
    if [ -f "scripts/health-check.sh" ]; then
        ./scripts/health-check.sh
    else
        echo -e "${YELLOW}  Health check script not found${NC}"
    fi
}

cmd_worktrees() {
    if [ -f "scripts/git-worktree-manager.sh" ]; then
        ./scripts/git-worktree-manager.sh list
    else
        echo -e "${YELLOW}  Worktree manager not found${NC}"
    fi
}

cmd_hooks() {
    echo -e "${BLUE} Testing Hooks${NC}"
    echo "=================================="
    
    for hook in .claude/hooks/*.sh; do
        if [ -f "$hook" ] && [ -x "$hook" ]; then
            HOOK_NAME=$(basename "$hook")
            echo -e "${BLUE}Testing: $HOOK_NAME${NC}"
            "$hook" "test" "0" > /dev/null 2>&1 && echo -e "${GREEN} Passed${NC}" || echo -e "${YELLOW}  Warning${NC}"
        fi
    done
    echo ""
}

cmd_validate() {
    echo -e "${BLUE} Validating Configuration${NC}"
    echo "=================================="
    
    # Validate JSON files
    if command -v python3 &> /dev/null; then
        for json_file in .claude/*.json; do
            if [ -f "$json_file" ]; then
                if python3 -m json.tool "$json_file" > /dev/null 2>&1; then
                    echo -e "${GREEN} $(basename $json_file)${NC}"
                else
                    echo -e "${YELLOW}  $(basename $json_file) - Invalid JSON${NC}"
                fi
            fi
        done
    fi
    echo ""
}

cmd_clean() {
    echo -e "${BLUE} Cleaning Logs${NC}"
    echo "=================================="
    
    # Clean log files (keep structure)
    if [ -f ".claude/tool-usage.log" ]; then
        > .claude/tool-usage.log
        echo -e "${GREEN} Cleared tool-usage.log${NC}"
    fi
    
    if [ -f ".claude/session.log" ]; then
        > .claude/session.log
        echo -e "${GREEN} Cleared session.log${NC}"
    fi
    
    # Clean temp files
    find .claude/logs -type f -name "*.tmp" -delete 2>/dev/null && echo -e "${GREEN} Cleared temp files${NC}" || true
    
    echo ""
}

# Main dispatcher
main() {
    if [ $# -eq 0 ]; then
        usage
        exit 1
    fi
    
    case "$1" in
        status)
            cmd_status
            ;;
        health)
            cmd_health
            ;;
        worktrees)
            cmd_worktrees
            ;;
        hooks)
            cmd_hooks
            ;;
        validate)
            cmd_validate
            ;;
        clean)
            cmd_clean
            ;;
        *)
            echo -e "${RED}Unknown command: $1${NC}"
            usage
            exit 1
            ;;
    esac
}

main "$@"

