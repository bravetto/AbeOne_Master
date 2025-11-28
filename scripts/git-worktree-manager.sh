#!/bin/bash
# Git Worktree Manager
# Automated worktree management for parallel feature development

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
WORKTREE_BASE_DIR="${WORKTREE_BASE_DIR:-..}"
MAIN_BRANCH="${MAIN_BRANCH:-main}"

usage() {
    cat << EOF
Git Worktree Manager

Usage: $0 <command> [options]

Commands:
    create <branch-name> [path]    Create new worktree with branch
    list                            List all worktrees
    remove <path>                   Remove worktree
    switch <path>                   Switch to worktree directory
    cleanup                         Remove stale worktrees

Examples:
    $0 create feature/new-module
    $0 create feat/auth ../feat-auth
    $0 list
    $0 remove ../feature-new-module
    $0 switch ../feature-new-module
    $0 cleanup

Environment Variables:
    WORKTREE_BASE_DIR    Base directory for worktrees (default: ..)
    MAIN_BRANCH          Main branch name (default: main)
EOF
}

create_worktree() {
    local branch_name="$1"
    local worktree_path="${2:-${WORKTREE_BASE_DIR}/${branch_name//\//-}}"
    
    # Validate branch name
    if [[ ! "$branch_name" =~ ^[a-z]+(/[a-z-]+)+$ ]]; then
        echo -e "${RED} Invalid branch name format. Use: type/description${NC}"
        echo "   Example: feat/user-auth, fix/login-bug"
        exit 1
    fi
    
    # Check if worktree path exists
    if [ -d "$worktree_path" ]; then
        echo -e "${RED} Directory already exists: $worktree_path${NC}"
        exit 1
    fi
    
    # Check if branch already exists
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        echo -e "${YELLOW}  Branch '$branch_name' already exists${NC}"
        read -p "Create worktree from existing branch? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
        BASE_BRANCH="$branch_name"
    else
        BASE_BRANCH="$MAIN_BRANCH"
    fi
    
    echo -e "${BLUE} Creating worktree...${NC}"
    echo "   Branch: $branch_name"
    echo "   Path: $worktree_path"
    echo "   Base: $BASE_BRANCH"
    
    # Create worktree
    if git worktree add "$worktree_path" -b "$branch_name" "$BASE_BRANCH"; then
        echo -e "${GREEN} Worktree created successfully${NC}"
        echo -e "${BLUE} Switch to worktree:${NC}"
        echo "   cd $worktree_path"
        echo ""
        echo -e "${BLUE} Or use:${NC}"
        echo "   $0 switch $worktree_path"
    else
        echo -e "${RED} Failed to create worktree${NC}"
        exit 1
    fi
}

list_worktrees() {
    echo -e "${BLUE} Active Worktrees:${NC}"
    echo ""
    git worktree list
    echo ""
    
    # Count worktrees
    local count=$(git worktree list | wc -l | tr -d ' ')
    echo -e "${GREEN}Total: $count worktree(s)${NC}"
}

remove_worktree() {
    local worktree_path="$1"
    
    if [ ! -d "$worktree_path" ]; then
        echo -e "${RED} Worktree path does not exist: $worktree_path${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}  Removing worktree: $worktree_path${NC}"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        exit 0
    fi
    
    if git worktree remove "$worktree_path"; then
        echo -e "${GREEN} Worktree removed${NC}"
    else
        echo -e "${RED} Failed to remove worktree${NC}"
        exit 1
    fi
}

switch_worktree() {
    local worktree_path="$1"
    
    if [ ! -d "$worktree_path" ]; then
        echo -e "${RED} Worktree path does not exist: $worktree_path${NC}"
        exit 1
    fi
    
    echo -e "${BLUE} Switching to worktree: $worktree_path${NC}"
    cd "$worktree_path" || exit 1
    echo -e "${GREEN} Switched${NC}"
    echo "   Current directory: $(pwd)"
    echo "   Branch: $(git branch --show-current)"
}

cleanup_worktrees() {
    echo -e "${BLUE} Cleaning up stale worktrees...${NC}"
    
    # Find worktrees that no longer exist on disk
    while IFS= read -r line; do
        worktree_path=$(echo "$line" | awk '{print $1}')
        if [ ! -d "$worktree_path" ]; then
            echo -e "${YELLOW}  Stale worktree detected: $worktree_path${NC}"
            git worktree prune
            break
        fi
    done < <(git worktree list)
    
    echo -e "${GREEN} Cleanup complete${NC}"
}

# Main command dispatcher
main() {
    if [ $# -eq 0 ]; then
        usage
        exit 1
    fi
    
    case "$1" in
        create)
            if [ $# -lt 2 ]; then
                echo -e "${RED} Branch name required${NC}"
                usage
                exit 1
            fi
            create_worktree "$2" "${3:-}"
            ;;
        list)
            list_worktrees
            ;;
        remove)
            if [ $# -lt 2 ]; then
                echo -e "${RED} Worktree path required${NC}"
                usage
                exit 1
            fi
            remove_worktree "$2"
            ;;
        switch)
            if [ $# -lt 2 ]; then
                echo -e "${RED} Worktree path required${NC}"
                usage
                exit 1
            fi
            switch_worktree "$2"
            ;;
        cleanup)
            cleanup_worktrees
            ;;
        *)
            echo -e "${RED} Unknown command: $1${NC}"
            usage
            exit 1
            ;;
    esac
}

main "$@"

