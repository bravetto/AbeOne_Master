#!/bin/bash
# Quick help for Claude automation

cat << 'HELP'
 CLAUDE AUTOMATION QUICK REFERENCE

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
