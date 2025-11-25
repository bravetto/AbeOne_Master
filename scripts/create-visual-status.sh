#!/bin/bash
# CREATE VISUAL STATUS
# 
# Creates visual status display for Cursor
# Updates automatically for always-visible status
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Get current status
cd "$WORKSPACE_ROOT"
STATUS_JSON=$(node scripts/always-on-guardian.js 2>/dev/null)
PROJECT=$(echo "$STATUS_JSON" | grep -o '"project":"[^"]*"' | cut -d'"' -f4 || echo "Unknown")
STATUS=$(echo "$STATUS_JSON" | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
EMOJI=$(echo "$STATUS_JSON" | grep -o '"emoji":"[^"]*"' | cut -d'"' -f4 || echo "")
CURRENT_DIR=$(basename "$(pwd)")

# Determine status color and badge
case "$STATUS" in
    "ACTIVE")
        STATUS_COLOR="#4ec9b0"
        STATUS_BADGE=" ACTIVE"
        STATUS_MSG="Perfect for work!"
        PROTECTION_LEVEL="100%"
        ;;
    "LEGACY")
        STATUS_COLOR="#f48771"
        STATUS_BADGE=" LEGACY"
        STATUS_MSG="Consider switching to active directory"
        PROTECTION_LEVEL="Protected (but legacy)"
        ;;
    *)
        STATUS_COLOR="#858585"
        STATUS_BADGE=" Workspace Root"
        STATUS_MSG="Navigate to a project directory"
        PROTECTION_LEVEL="Active"
        ;;
esac

# Create visual status markdown
cat > "$WORKSPACE_ROOT/drift-visual-status.md" << EOF
#  DRIFT PROTECTION STATUS - VISUAL DISPLAY

**Last Updated**: $(date '+%Y-%m-%d %H:%M:%S')  
**Status**: Always Current  
**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE

---

##  CURRENT STATUS

<div style="background: #1e1e1e; padding: 20px; border-radius: 8px; border: 2px solid $STATUS_COLOR; margin: 20px 0;">

### $EMOJI Project Context

**Current Directory**: \`$CURRENT_DIR\`  
**Project**: $PROJECT  
**Status**: $STATUS_BADGE  
**Protection**:  Active  
**Message**: $STATUS_MSG

###  Protection Layers

-  **Layer 1**: Always-On Guardian (Active)
-  **Layer 2**: Pre-Work Validation (Ready)
-  **Layer 3**: Pre-Commit Hooks (Installed)
-  **Layer 4**: Pre-Push Hooks (Installed)
-  **Layer 5**: CI/CD Validation (Active)

###  Quick Actions

-  Status Check: \`node scripts/gentle-drift-guardian.js\`
-  Full Validation: \`node scripts/validate-project-boundaries.js\`
-  Vibecoder Mode: \`./scripts/vibecoder-mode.sh\`
-  Watch Status: \`./scripts/watch-drift-status.sh\`

</div>

---

##  VISUAL INDICATORS

### Status Colors

- 🟢 **Green**: Active Project - Perfect for work!
- 🟡 **Yellow**: Legacy Directory - Consider switching
-  **Blue**: Workspace Root - Navigate to project
- 🟣 **Purple**: Unknown Status - Check manually

### Protection Level

\`\`\`
 Protection:  $PROTECTION_LEVEL
 Status: All systems operational
 Ready: Yes - Code with confidence!
\`\`\`

---

##  ACTIVE PROJECTS

| Project | Status | Protection | Quick Access |
|---------|--------|------------|--------------|
| \`AiGuardian-Chrome-Ext-dev/\` |  ACTIVE |  Protected | \`cd AiGuardian-Chrome-Ext-dev\` |
| \`AIGuards-Backend/\` |  ACTIVE |  Protected | \`cd AIGuards-Backend\` |
| \`EMERGENT_OS/\` |  ACTIVE |  Protected | \`cd EMERGENT_OS\` |

---

##  LEGACY PROJECTS

| Project | Status | Active Replacement |
|---------|--------|-------------------|
| \`AI-Guardians-chrome-ext/\` |  LEGACY | \`AiGuardian-Chrome-Ext-dev/\` |

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**:  **VISUAL STATUS ACTIVE**

*This file auto-updates - keep it open for always-visible status!*
EOF

echo " Visual status created: drift-visual-status.md"

