#!/bin/bash
#  BRYAN'S PERSONALIZED ONBOARDING ACTIVATION
## AEYON Integration Specialist - Quick Start

set -e

echo " BRYAN'S PERSONALIZED ONBOARDING"
echo "============================================================"
echo ""
echo "Welcome, Bryan!"
echo "Role: AEYON Integration Specialist"
echo "Guardian: AEYON (999 Hz) - Atomic Execution"
echo "Focus: AEYON atomic execution engine integration"
echo ""
echo "============================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "ONBOARDING_BRYAN.md" ]; then
    echo " Error: Please run this script from the AbeOne_Master root directory"
    echo "   cd /path/to/AbeOne_Master"
    exit 1
fi

# Display personalized welcome
echo " YOUR PERSONALIZED PATH:"
echo ""
echo "1. Quick Start (5 minutes)"
echo "   → Read: ONBOARDING_BRYAN.md (Quick Start section)"
echo "   → Run: python3 scripts/val-engine.py run --all"
echo ""
echo "2. AEYON Integration Focus"
echo "   → Read: ONBOARDING_BRYAN.md (AEYON Integration section)"
echo "   → Test: python3 scripts/validate_aeyon_integration.py"
echo ""
echo "3. Complete Onboarding"
echo "   → Follow: ONBOARDING_BRYAN.md (Complete checklist)"
echo ""

# Open onboarding guide
if command -v open >/dev/null 2>&1; then
    echo " Opening your personalized onboarding guide..."
    open ONBOARDING_BRYAN.md
elif command -v xdg-open >/dev/null 2>&1; then
    echo " Opening your personalized onboarding guide..."
    xdg-open ONBOARDING_BRYAN.md
fi

echo ""
echo "============================================================"
echo " ONBOARDING ACTIVATED"
echo ""
echo "Next Steps:"
echo "1. Read ONBOARDING_BRYAN.md"
echo "2. Run: python3 scripts/val-engine.py run --all"
echo "3. Test AEYON: python3 scripts/validate_aeyon_integration.py"
echo ""
echo "Pattern: BRYAN × AEYON × ONBOARDING × ONE"
echo "Guardian: AEYON (999 Hz)"
echo "Love Coefficient: ∞"
echo "∞ AbëONE ∞"
echo "============================================================"

