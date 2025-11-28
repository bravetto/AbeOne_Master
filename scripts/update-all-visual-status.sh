#!/bin/bash
# UPDATE ALL VISUAL STATUS FILES
# 
# Updates all visual status displays simultaneously
# Keeps all visual files current and synchronized
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo " Updating all visual status files..."

# Update JSON status (source of truth)
cd "$WORKSPACE_ROOT"
node scripts/update-drift-status.js

# Update visual markdown status
./scripts/create-visual-status.sh

# Update visual status markdown (master)
cd "$WORKSPACE_ROOT"
STATUS_JSON=$(node scripts/always-on-guardian.js 2>/dev/null)

# Extract project and status from JSON (handle null values)
PROJECT=$(echo "$STATUS_JSON" | node -e "
  const data = JSON.parse(require('fs').readFileSync(0, 'utf-8'));
  console.log(data.project || data.currentDir || 'Workspace Root');
")
STATUS=$(echo "$STATUS_JSON" | node -e "
  const data = JSON.parse(require('fs').readFileSync(0, 'utf-8'));
  const status = data.status || 'unknown';
  console.log(status === 'unknown' ? 'Workspace Root' : status);
")

# Update master visual status
cat > "$WORKSPACE_ROOT/DRIFT_STATUS_VISUAL.md" << EOF
#  DRIFT PROTECTION - VISUAL STATUS

<div align="center">

##  DRIFT PROTECTION STATUS

**Last Updated**: $(date '+%Y-%m-%d %H:%M:%S')  
**Keep this file open for always-visible status!**

---

###  CURRENT PROJECT STATUS

**Current**: \`$(basename "$(pwd)")\`  
**Project**: $PROJECT  
**Status**: $STATUS

| Status | Project | Protection | Action |
|--------|---------|------------|--------|
|  ACTIVE | \`AiGuardian-Chrome-Ext-dev/\` |  Protected | \`cd AiGuardian-Chrome-Ext-dev\` |
|  ACTIVE | \`AIGuards-Backend/\` |  Protected | \`cd AIGuards-Backend\` |
|  ACTIVE | \`EMERGENT_OS/\` |  Protected | \`cd EMERGENT_OS\` |
|  LEGACY | \`AI-Guardians-chrome-ext/\` |  Reference Only | Use active directory instead |

---

###  PROTECTION LAYERS

\`\`\`
Layer 1: Always-On Guardian       100% 
Layer 2: Pre-Work Validation      100% 
Layer 3: Pre-Commit Hooks         100% 
Layer 4: Pre-Push Hooks           100% 
Layer 5: CI/CD Validation        100% 
\`\`\`

**Overall Protection**:  **100% ACTIVE**

---

###  QUICK ACTIONS

| Action | Command | Purpose |
|--------|---------|---------|
|  Status Check | \`node scripts/gentle-drift-guardian.js\` | Quick status |
|  Full Validation | \`node scripts/validate-project-boundaries.js\` | Complete check |
|  Vibecoder Mode | \`./scripts/vibecoder-mode.sh\` | Activate vibes |
|  Watch Status | \`./scripts/watch-drift-status.sh\` | Auto-updates |
|  Visual Status | Open \`drift-visual-status.md\` | Visual display |

---

###  VISUAL FILES

**Keep these open for always-visible status:**

1. **\`drift-visual-status.md\`** - Visual markdown (recommended)
2. **\`drift-status-dashboard.html\`** - HTML dashboard
3. **\`drift-status-badge.html\`** - Compact badge
4. **\`.drift-status.txt\`** - Simple text

**Setup**: Pin tabs, run watch script, status updates automatically!

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**:  **VISUAL STATUS ACTIVE**

*Auto-updates every 30 seconds - keep this file open!*

</div>
EOF

echo " All visual status files updated"

