# Claude Code Quick Reference

**Essential commands and shortcuts for AbeOne Master**

---

## ⌨️ **KEYBOARD SHORTCUTS**

| Shortcut | Action |
|----------|--------|
| `!` | Bash mode prefix |
| `@` | Mention files/folders |
| `\` | Line break (backslash + Enter) |
| `Esc` | Interrupt Claude |
| `Ctrl+R` | Full output/context |
| `Ctrl+V` | Paste image |
| `Esc+Esc` | History navigation |
| `Shift+Tab` | Auto-accept ("yolo mode") |
| `Shift+Tab+Tab` | Plan mode |
| `Cmd+Esc` | Quick launch in IDEs |
| `Cmd+Opt+K` | Insert file references |

---

## 🎯 **CUSTOM SLASH COMMANDS**

### `/converge`
Execute convergence workflows.

```bash
/converge validation    # System validation
/converge amplification # Guardian amplification
/converge synthesis     # Synthesis convergence
/converge all           # All workflows
```

### `/guardian`
Manage guardian agents.

```bash
/guardian status AEYON   # Check status
/guardian activate JOHHN # Activate guardian
/guardian list           # List all
```

### `/worktree`
Manage git worktrees.

```bash
/worktree create feature/new-module
/worktree list
/worktree remove ../feature-new-module
```

### Standard Commands
```bash
/clear      # Clear history
/model      # Change AI model
/cost       # Token usage stats
/review     # Code review
/config     # View/modify config
/doctor     # Health check
/mcp        # MCP servers
```

---

## 🔧 **CONFIGURATION**

### View Settings
```bash
cat .claude/settings.json | jq .
```

### Change Model
```bash
# Via Claude
/model claude-sonnet-4-20250514

# Via CLI
claude config set model claude-sonnet-4-20250514
```

### Change Theme
```bash
claude config set -g theme dark
```

---

## 🌳 **GIT WORKTREES**

### Quick Commands
```bash
# Create worktree
./scripts/git-worktree-manager.sh create feature/new-module

# List worktrees
./scripts/git-worktree-manager.sh list

# Remove worktree
./scripts/git-worktree-manager.sh remove ../feature-new-module

# Switch to worktree
./scripts/git-worktree-manager.sh switch ../feature-new-module
```

### Manual Git Worktree
```bash
# Create
git worktree add ../app-feature -b feature main

# List
git worktree list

# Remove
git worktree remove <path>
```

---

## 🔌 **MCP SERVERS**

### Available Servers
- **AWS** - Infrastructure management ✅
- **Playwright** - Browser automation ✅
- **Context7** - Documentation access ✅

### Add Server
```bash
/claude mcp add <name> <command>
```

---

## 🤖 **AI MODELS**

| Model | Identifier | Use Case |
|-------|-----------|----------|
| **Opus 4.1** | `claude-opus-4-1-20250805` | Most capable (default) |
| **Sonnet 4** | `claude-sonnet-4-20250514` | Balanced performance |
| **Haiku 3.5** | `claude-3-5-haiku-20241022` | Fastest responses |

---

## 📁 **KEY FILE LOCATIONS**

```
.claude/
├── settings.json          # Root configuration
├── mcp-config.json        # MCP servers
├── commands/              # Custom slash commands
└── hooks/                 # Automation hooks

scripts/
└── git-worktree-manager.sh  # Worktree automation
```

---

## 🔄 **HOOKS**

Hooks execute automatically:
- **Session Start** - On session begin
- **Session End** - On session end
- **Pre-Tool Use** - Before tool execution
- **Post-Tool Use** - After tool execution

**Location:** `.claude/hooks/`

---

## 💡 **TIPS**

1. **Use worktrees** for parallel feature development
2. **Custom commands** for frequent workflows
3. **MCP servers** extend Claude capabilities
4. **Hooks** automate repetitive tasks
5. **Model selection** based on task complexity

---

**Full Documentation:** `CLAUDE_CODE_INTEGRATION.md`

