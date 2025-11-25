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

