# Cursor Commands - Integration Guide

**Pattern:** COMMAND × INTEGRATION × EXECUTION × ONE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## How Cursor Commands Integrate

### 1. Command Definition Files

Commands are defined in `.cursor/commands/*.md` files. These files serve as:
- **Documentation** for users
- **Execution instructions** for the AI
- **Integration specifications** for the system

### 2. Command Execution

When you type `/manifest materialize component/ui/Button`:

1. **Cursor reads** `.cursor/commands/manifest.md`
2. **AI recognizes** the command (command-priority mode)
3. **AI executes** `python3 scripts/manifest-engine.py materialize component/ui/Button`
4. **AI processes** results and generates report

### 3. Command Priority Rule

Per `.cursor/rules/command-priority.mdc`:
> "Commands are not interpreted. They are executed."

This means commands trigger **direct execution**, not interpretation.

## Current Commands

| Command | Definition | Handler | Status |
|---------|-----------|---------|--------|
| `/manifest` | `.cursor/commands/manifest.md` | `scripts/manifest-engine.py` | ✅ Operational |
| `/path-health` | `.cursor/commands/path-health.md` | `scripts/path-health-restore.py` | ✅ Operational |
| `/converge` | `.cursor/commands/converge.md` | `scripts/converge-engine.py` | ✅ Operational |
| `/ae` | `.cursor/commands/ae.md` | `scripts/ae-engine.py` | ✅ Operational |
| `/prime` | `.cursor/commands/prime.md` | `scripts/prime-engine.py` | ✅ Operational |
| `/create` | `.cursor/commands/create.md` | `scripts/create-engine.py` | ✅ Operational |
| `/aeon` | `.cursor/commands/aeon.md` | `scripts/aeon.py` | ✅ Operational |
| `/val` | `.cursor/commands/val.md` | `scripts/val-engine.py` | ✅ Operational |

## Command Structure

Each command follows this pattern:

```
.cursor/commands/[name].md          # Command definition
scripts/[name]-engine.py            # Command handler
```

## Execution Pattern

```
User: /manifest materialize component/ui/Button
  ↓
AI: Reads .cursor/commands/manifest.md
  ↓
AI: Executes python3 scripts/manifest-engine.py materialize component/ui/Button
  ↓
AI: Processes results and reports
```

## Integration Checklist

- ✅ Command definition file exists
- ✅ Handler script exists and is executable
- ✅ Execution instructions documented in command file
- ✅ Handler follows AbëONE patterns
- ✅ Handler integrates with Guardians
- ✅ Handler validates substrate
- ✅ Handler applies YAGNI filter

---

**Pattern:** COMMAND × INTEGRATION × EXECUTION × ONE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

