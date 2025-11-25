# Claude Code Integration Guide

**Complete integration of Claude Code cheatsheet features into AbeOne Master**

*Last Updated: 2025-01-27*

---

## 📋 **OVERVIEW**

This document describes the integration of valuable Claude Code features into the AbeOne Master system, including MCP servers, custom slash commands, hooks, git worktrees, and configuration management.

---

## 🎯 **INTEGRATED FEATURES**

### 1. **Root-Level Claude Configuration**

**Location:** `.claude/settings.json`

**Features:**
- ✅ Model selection (Opus 4.1)
- ✅ Theme configuration (dark)
- ✅ Permission management
- ✅ Hook automation
- ✅ Project context

**Usage:**
```bash
# View configuration
cat .claude/settings.json

# Modify via Claude
/claude config set model claude-sonnet-4-20250514
```

---

### 2. **MCP Servers**

**Location:** `.claude/mcp-config.json`

**Configured Servers:**

#### AWS MCP Server
- **Purpose:** Infrastructure management
- **Services:** ECS, ECR, Secrets Manager, CloudWatch, RDS
- **Status:** ✅ Enabled

#### Playwright MCP Server
- **Purpose:** Browser automation and testing
- **Installation:** `npx @playwright/mcp@latest`
- **Status:** ✅ Enabled
- **Use Cases:**
  - E2E testing automation
  - UI validation
  - Screenshot capture
  - Form filling automation

#### Context7 MCP Server
- **Purpose:** Documentation access and search
- **Transport:** HTTP
- **Status:** ✅ Enabled
- **Use Cases:**
  - Code documentation lookup
  - API reference search
  - Pattern discovery

**Adding New MCP Server:**
```bash
# Via Claude
/claude mcp add <name> <command>

# Example
/claude mcp add filesystem npx @modelcontextprotocol/server-filesystem
```

---

### 3. **Custom Slash Commands**

**Location:** `.claude/commands/`

**Available Commands:**

#### `/converge`
Execute convergence workflows and validate system state.

```bash
/converge validation    # Run system validation
/converge amplification  # Execute guardian amplification
/converge synthesis     # Run synthesis convergence
/converge all           # Execute all workflows
```

#### `/guardian`
Manage guardian agents and their states.

```bash
/guardian status AEYON   # Check AEYON status
/guardian activate JOHHN # Activate JOHHN
/guardian list           # List all guardians
```

#### `/worktree`
Manage git worktrees for parallel feature development.

```bash
/worktree create feature/new-module
/worktree list
/worktree remove ../feature-new-module
```

**Creating Custom Commands:**
1. Create markdown file in `.claude/commands/`
2. Document usage and examples
3. Claude will recognize and use the command

---

### 4. **Hooks & Automation**

**Location:** `.claude/hooks/`

**Available Hooks:**

#### Session Start (`session-start.sh`)
- Executes when Claude session begins
- Loads project context
- Reports git branch and worktree status
- Logs session start timestamp

#### Session End (`session-end.sh`)
- Executes when Claude session ends
- Logs session summary
- Records session duration

#### Pre-Tool Use (`pre-tool-use.sh`)
- Executes before Claude uses a tool
- Safety checks for destructive operations
- Tool usage logging

#### Post-Tool Use (`post-tool-use.sh`)
- Executes after Claude uses a tool
- Logs tool usage and exit codes
- Tracks tool performance

**Hook Events:**
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool execution
- `SessionStart` - Session initialization
- `SessionEnd` - Session cleanup
- `UserPromptSubmit` - On user input (not yet implemented)
- `Stop` - On interruption (not yet implemented)

**Enabling/Disabling Hooks:**
Edit `.claude/settings.json`:
```json
{
  "hooks": {
    "preToolUse": {
      "enabled": true,
      "script": ".claude/hooks/pre-tool-use.sh"
    }
  }
}
```

---

### 5. **Git Worktree Automation**

**Location:** `scripts/git-worktree-manager.sh`

**Features:**
- ✅ Create worktrees with branch validation
- ✅ List all active worktrees
- ✅ Remove worktrees safely
- ✅ Switch between worktrees
- ✅ Cleanup stale worktrees

**Usage:**
```bash
# Make executable
chmod +x scripts/git-worktree-manager.sh

# Create new worktree
./scripts/git-worktree-manager.sh create feature/new-module

# List worktrees
./scripts/git-worktree-manager.sh list

# Remove worktree
./scripts/git-worktree-manager.sh remove ../feature-new-module

# Switch to worktree
./scripts/git-worktree-manager.sh switch ../feature-new-module

# Cleanup stale worktrees
./scripts/git-worktree-manager.sh cleanup
```

**Environment Variables:**
```bash
export WORKTREE_BASE_DIR="../worktrees"  # Default: ..
export MAIN_BRANCH="main"                # Default: main
```

**Integration with Claude:**
The `/worktree` slash command uses this script internally.

---

## 🔧 **CONFIGURATION MANAGEMENT**

### Model Selection

**Available Models:**
- **Opus 4.1:** `claude-opus-4-1-20250805` (Most capable) - ✅ Default
- **Sonnet 4:** `claude-sonnet-4-20250514` (Balanced)
- **Haiku 3.5:** `claude-3-5-haiku-20241022` (Fastest)

**Change Model:**
```bash
# Via Claude CLI
claude config set model claude-sonnet-4-20250514

# Via Claude in Cursor
/model claude-sonnet-4-20250514
```

### Theme Configuration

**Available Themes:**
- `dark` - ✅ Default
- `light`
- `auto`

**Change Theme:**
```bash
claude config set -g theme dark
```

---

## 📁 **FILE STRUCTURE**

```
AbeOne_Master/
├── .claude/
│   ├── settings.json              # Root configuration
│   ├── mcp-config.json            # MCP server configuration
│   ├── commands/                  # Custom slash commands
│   │   ├── converge.md
│   │   ├── guardian.md
│   │   └── worktree.md
│   └── hooks/                     # Automation hooks
│       ├── session-start.sh
│       ├── session-end.sh
│       ├── pre-tool-use.sh
│       └── post-tool-use.sh
├── scripts/
│   └── git-worktree-manager.sh    # Worktree automation
└── AIGuards-Backend/
    └── .claude/
        └── settings.local.json    # Project-specific settings
```

---

## 🚀 **QUICK START**

### 1. Initialize Configuration

```bash
# Configuration is already created
# Verify it exists
ls -la .claude/
```

### 2. Enable MCP Servers

```bash
# MCP servers are configured in .claude/mcp-config.json
# They will be available when Claude starts
```

### 3. Test Custom Commands

```bash
# In Claude chat, try:
/converge validation
/guardian list
/worktree list
```

### 4. Use Git Worktrees

```bash
# Create a new feature worktree
./scripts/git-worktree-manager.sh create feat/new-feature

# Switch to it
./scripts/git-worktree-manager.sh switch ../feat-new-feature
```

---

## 🔐 **SECURITY CONSIDERATIONS**

### Permission Management

**Current Permissions:**
- ✅ Read access to all files
- ✅ Git operations
- ✅ Build tools (npm, python, docker)
- ⚠️ Destructive operations require confirmation

**Modifying Permissions:**
Edit `.claude/settings.json`:
```json
{
  "permissions": {
    "allow": ["Read(/**)", "Bash(git:*)"],
    "deny": ["Bash(rm -rf:*)"],
    "ask": ["Bash(sudo:*)"]
  }
}
```

### Hook Security

- Hooks are executed with user permissions
- Pre-tool hooks can block dangerous operations
- All hook executions are logged

---

## 📊 **MONITORING & LOGGING**

### Tool Usage Log

**Location:** `.claude/tool-usage.log`

**Format:**
```
2025-01-27T10:30:00 | read_file | 0
2025-01-27T10:30:05 | search_replace | 0
2025-01-27T10:30:10 | run_terminal_cmd | 1
```

### Session Logs

**Location:** `.claude/session.log`

**Content:**
- Session start/end timestamps
- Active worktrees
- Git branch information
- Project context status

---

## 🎓 **BEST PRACTICES**

### 1. **Worktree Management**
- Use worktrees for parallel feature development
- Clean up stale worktrees regularly
- Follow branch naming conventions: `type/description`

### 2. **MCP Server Usage**
- Use Playwright for E2E testing automation
- Use Context7 for documentation lookup
- Use AWS MCP for infrastructure management

### 3. **Custom Commands**
- Keep commands focused and atomic
- Document usage clearly
- Test commands before committing

### 4. **Hooks**
- Keep hooks lightweight
- Avoid blocking operations
- Log important events

---

## 🔄 **INTEGRATION WITH EXISTING SYSTEMS**

### AIGuards-Backend

The AIGuards-Backend project has its own `.claude/` configuration:
- **Location:** `AIGuards-Backend/.claude/`
- **Settings:** `settings.local.json`
- **MCP Config:** `.cursor/mcp-config.json`

These configurations work alongside the root-level configuration.

### EMERGENT_OS

The EMERGENT_OS workspace benefits from:
- Root-level MCP servers
- Custom slash commands
- Git worktree automation

---

## 📚 **REFERENCES**

- **Claude Code Cheatsheet:** `awesomeclaude.ai/code-cheatsheet`
- **MCP Protocol:** `modelcontextprotocol.io`
- **Git Worktrees:** `git-scm.com/docs/git-worktree`

---

## ✅ **VALIDATION**

### Check Configuration

```bash
# Verify settings
cat .claude/settings.json | jq .

# Verify MCP config
cat .claude/mcp-config.json | jq .

# Verify hooks
ls -la .claude/hooks/

# Verify commands
ls -la .claude/commands/
```

### Test Worktree Manager

```bash
# Test script
./scripts/git-worktree-manager.sh list

# Should show current worktree
```

---

## 🎯 **NEXT STEPS**

1. ✅ Root configuration created
2. ✅ MCP servers configured
3. ✅ Custom commands created
4. ✅ Hooks implemented
5. ✅ Worktree automation ready
6. ⏭️ Test integration in practice
7. ⏭️ Add more custom commands as needed
8. ⏭️ Expand hook functionality

---

**Pattern: OBSERVER × TRUTH × ATOMIC × ONE**
∞ AbëONE ∞

