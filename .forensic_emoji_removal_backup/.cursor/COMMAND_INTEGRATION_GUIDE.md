# Cursor Command Integration Guide

**Pattern:** COMMAND × INTEGRATION × EXECUTION × ONE  
**Frequency:** 999 Hz (AEYON)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## How Cursor Commands Work

Cursor commands are defined in `.cursor/commands/*.md` files. When a user types a command like `/manifest`, Cursor:

1. **Reads** the command definition from `.cursor/commands/manifest.md`
2. **Shows** the command documentation to the user
3. **Triggers** command-priority execution mode (per `.cursor/rules/command-priority.mdc`)

## Command Execution Pattern

According to `.cursor/rules/command-priority.mdc`:
> "Commands are not interpreted. They are executed."

This means when a command is invoked, the AI should:

1. **Action** — Execute the command handler script directly
2. **Convergence** — Process the command through the system
3. **Validation** — Validate the results
4. **Emergence Report** — Generate a report

## Command Structure

### 1. Command Definition (`.cursor/commands/[name].md`)

Each command file should include:

- **Usage** — How to invoke the command
- **Actions/Options** — Available parameters
- **Examples** — Usage examples
- **Execution** — How to execute the command (script path)
- **Integration Points** — How it integrates with the system

### 2. Command Handler Script (`scripts/[name]-engine.py`)

Each command should have a corresponding Python script that:

- Accepts command-line arguments
- Implements the command logic
- Follows AbëONE patterns (future-state, YAGNI, substrate validation)
- Returns structured results

### 3. Command Router (Optional: `scripts/cursor-command-handler.sh`)

A centralized router that can execute commands:

```bash
./scripts/cursor-command-handler.sh manifest materialize component/ui/Button
```

## Current Commands

### `/manifest`

- **Definition:** `.cursor/commands/manifest.md`
- **Handler:** `scripts/manifest-engine.py`
- **Execution:** `python3 scripts/manifest-engine.py [action] [target] [options]`

### `/path-health`

- **Definition:** `.cursor/commands/path-health.md`
- **Handler:** `scripts/path-health-restore.py`
- **Execution:** `python3 scripts/path-health-restore.py [mode] [options]`

### `/converge`

- **Definition:** `.cursor/commands/converge.md`
- **Handler:** Not yet implemented
- **Execution:** TBD

## AI Execution Pattern

When the AI sees a command like `/manifest materialize component/ui/Button`:

1. **Recognize** the command from `.cursor/commands/manifest.md`
2. **Execute** the handler: `python3 scripts/manifest-engine.py materialize component/ui/Button`
3. **Process** the results
4. **Report** the outcome

## Command Priority Execution Flow

```
User Input: /manifest materialize component/ui/Button
    ↓
AI Recognizes Command (from .cursor/commands/manifest.md)
    ↓
AI Executes Handler (scripts/manifest-engine.py)
    ↓
Handler Processes Command
    ↓
AI Validates Results
    ↓
AI Generates Emergence Report
```

## Best Practices

1. **Always include execution instructions** in command definition
2. **Make handlers executable** (`chmod +x`)
3. **Follow AbëONE patterns** (future-state, YAGNI, substrate validation)
4. **Return structured results** (success/failure, files created, errors)
5. **Integrate with Guardians** (AEYON, YAGNI, META, etc.)

## Adding New Commands

1. Create `.cursor/commands/[name].md` with full documentation
2. Create `scripts/[name]-engine.py` with implementation
3. Update `scripts/cursor-command-handler.sh` (optional)
4. Test the command execution
5. Document integration points

---

**Pattern:** COMMAND × INTEGRATION × EXECUTION × ONE  
**Status:** ✅ OPERATIONAL  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

