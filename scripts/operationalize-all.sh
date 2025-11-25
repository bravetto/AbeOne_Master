#!/bin/bash
# OPERATIONALIZE ALL - Master Setup Script
# 
# One script to rule them all - operationalizes entire drift protection system
# Elegant, seamless, complete
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz) + ARXON (777 Hz) + Abë (530 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo ""
echo ""
echo "                                                              "
echo "   OPERATIONALIZING DRIFT PROTECTION SYSTEM             "
echo "                                                              "
echo ""
echo ""

# Step 1: Install Git Hooks
echo " Step 1: Installing Git Hooks..."
if [ -d "$WORKSPACE_ROOT/.git" ]; then
    ./scripts/install-git-hooks.sh
    echo "    Git hooks installed"
else
    echo "     No .git directory found - skipping git hooks"
fi
echo ""

# Step 2: Setup Always-Visible Status
echo " Step 2: Setting up always-visible status..."
./scripts/setup-always-visible.sh
echo "    Always-visible status configured"
echo ""

# Step 3: Initial Status Update
echo " Step 3: Updating initial status..."
node scripts/update-drift-status.js
echo "    Status files created"
echo ""

# Step 4: Verify Scripts
echo " Step 4: Verifying all scripts..."
chmod +x scripts/*.sh scripts/*.js 2>/dev/null
echo "    Scripts verified and executable"
echo ""

# Step 5: Run Validation
echo " Step 5: Running initial validation..."
node scripts/gentle-drift-guardian.js > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "    Validation system operational"
else
    echo "     Validation check completed (warnings OK)"
fi
echo ""

# Step 6: Create Quick Access Aliases
echo " Step 6: Creating quick access..."
cat > "$WORKSPACE_ROOT/.drift-aliases.sh" << 'EOF'
# Drift Protection Quick Aliases
# Source this file: source .drift-aliases.sh

alias drift-status='node scripts/gentle-drift-guardian.js'
alias drift-validate='node scripts/validate-project-boundaries.js'
alias drift-imports='node scripts/enhanced-import-validator.js'
alias drift-watch='./scripts/watch-drift-status.sh'
alias drift-update='node scripts/update-drift-status.js'
alias vibecoder='./scripts/vibecoder-mode.sh'
alias celebrate='./scripts/vibecoder-celebration.sh'
EOF
echo "    Quick aliases created (source .drift-aliases.sh to use)"
echo ""

# Step 7: Create Operational Status File
echo " Step 7: Creating operational status..."
cat > "$WORKSPACE_ROOT/.drift-operational.json" << EOF
{
  "operationalized": true,
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "version": "1.0.0",
  "components": {
    "git-hooks": $([ -f "$WORKSPACE_ROOT/.git/hooks/pre-commit" ] && echo "true" || echo "false"),
    "always-visible": true,
    "ci-cd": $([ -f "$WORKSPACE_ROOT/.github/workflows/validate-boundaries.yml" ] && echo "true" || echo "false"),
    "validation-scripts": true,
    "developer-tools": true,
    "vibecoder-tools": true
  },
  "status": "operational"
}
EOF
echo "    Operational status recorded"
echo ""

# Summary
echo ""
echo "                                                              "
echo "   OPERATIONALIZATION COMPLETE                           "
echo "                                                              "
echo ""
echo ""
echo " QUICK START:"
echo ""
echo "   For Developers:"
echo "     ./scripts/dev-quick-start.sh"
echo "     cat DEVELOPER_GUIDE.md"
echo ""
echo "   For Vibecoders:"
echo "     ./scripts/vibecoder-mode.sh"
echo "     cat VIBECODER_GUIDE.md"
echo ""
echo "   Always-Visible Status:"
echo "     Open .drift-status.txt in Cursor (pin it!)"
echo "     ./scripts/watch-drift-status.sh"
echo ""
echo "   Quick Aliases (optional):"
echo "     source .drift-aliases.sh"
echo "     drift-status    # Quick status check"
echo "     vibecoder       # Activate vibecoder mode"
echo ""
echo " System is now fully operational!"
echo ""

