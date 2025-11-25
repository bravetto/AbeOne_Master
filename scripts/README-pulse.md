#  PULSE - Manual Synchronization

Manual trigger to synchronize source of truth and all dashboards.

## Usage

### In Terminal:
```bash
node scripts/pulse.js
```

### With Alias (after sourcing .drift-aliases.sh):
```bash
source .drift-aliases.sh
pulse
```

### In Chat:
Type: `run pulse` or ask AI to run `node scripts/pulse.js`

## What It Does

1. Updates `.ai-context-source-of-truth.json` with current system status
2. Generates all dashboards from source of truth:
   - `DRIFT_DASHBOARD_ETERNAL.md`
   - `DRIFT_STATUS_VISUAL.md`

## When to Use

- Before important operations
- After manual system changes
- When you want to ensure chat truth matches system truth
- When dashboards seem out of sync

## Automation Events

The system also auto-updates on:
- **Git Commit** → pre-commit hook → updates source of truth
- **Git Push** → pre-push hook → updates source of truth + generates dashboards
- **File Changes** → boundary-watcher → updates source of truth + generates dashboards

**Pulse** is the manual override when you want immediate synchronization.

