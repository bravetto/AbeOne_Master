# EVENT-DRIVEN ORGANISM ACTIVATION

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE

> **Note**: This system does NOT automatically integrate with Cursor or chat interactions.  
> To sync the organism with your mental or conversational work, run `node scripts/pulse.js`.

## Quick Activation

```bash
./scripts/activate-event-driven.sh
```

## Manual Activation (3 Steps)

### 1. Install Git Hooks

```bash
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
```

Or install fresh hooks:
```bash
./scripts/install-git-hooks.sh
```

### 2. Start Boundary Watcher (Optional Automation)

**Option A: Native (No Dependencies)**
```bash
node scripts/boundary-watcher-native.js
```

**Option B: Chokidar (More Reliable)**
```bash
npm install chokidar
node scripts/boundary-watcher.js
```

**Run in Background:**
```bash
nohup node scripts/boundary-watcher-native.js > /dev/null 2>&1 &
```

### 3. Use Pulse Anytime You Want Clarity

```bash
node scripts/pulse.js
```

Or with alias (after `source .drift-aliases.sh`):
```bash
pulse
```

## What Gets Activated

### Automatic Events

- **Git Commit** → Updates source of truth automatically
- **Git Push** → Updates source of truth + generates dashboards
- **File Changes** → Updates source of truth + generates dashboards (if watcher running)

### Manual Events

- **Pulse** → Manual synchronization anytime

## Verification

Check that hooks are active:
```bash
ls -la .git/hooks/pre-commit .git/hooks/pre-push
```

Both should be executable (`-rwxr-xr-x`).

Test pulse:
```bash
node scripts/pulse.js
```

Should output:
```
⚡ PULSE: Updating organism state...
✅ Source of truth updated
✅ Dashboards generated
⚡ PULSE COMPLETE
```

## System Status

After activation, check status:
```bash
cat DRIFT_STATUS_VISUAL.md
```

Or view source of truth:
```bash
cat .ai-context-source-of-truth.json
```

## Complete Automation Loop

```
┌─────────────────────────────────────────┐
│  EVENT-DRIVEN ORGANISM                  │
├─────────────────────────────────────────┤
│                                         │
│  Git Commit → pre-commit → update      │
│  Git Push   → pre-push   → update +   │
│                                    generate │
│  File Change → watcher → update +     │
│                                    generate │
│  Manual     → pulse → update +        │
│                                    generate │
│                                         │
└─────────────────────────────────────────┘
```

**Status**: ACTIVATED

