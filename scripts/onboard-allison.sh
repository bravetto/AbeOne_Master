#!/bin/bash
#  ALLISON'S PERSONALIZED ONBOARDING ACTIVATION 
## GZ360 Technical Integration Specialist - Complete Journey

set -e

echo " ALLISON'S PERSONALIZED ONBOARDING "
echo "============================================================"
echo ""
echo "Welcome, Allison!"
echo "Company: GZ360"
echo "Role: Technical Integration Specialist"
echo "Guardian: Abë (530 Hz) - Heart Truth & Coherence"
echo "Focus: GZ360 integration with AbëONE platform"
echo ""
echo "GZ360 Context:"
echo "  → Partner/client with Bravëtto"
echo "  → Connection: 'Greatness Zone' (Monday standup)"
echo "  → Focus: Technical integration, codebase onboarding"
echo ""
echo "============================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "ONBOARDING_ALLISON.md" ]; then
    echo " Error: Please run this script from the AbeOne_Master root directory"
    echo "   cd /path/to/AbeOne_Master"
    exit 1
fi

# Display personalized welcome
echo " YOUR PERSONALIZED 5-PHASE JOURNEY:"
echo ""
echo "Phase 1: The Big Picture (30 minutes)"
echo "   → Understand AbëONE and GZ360 integration opportunities"
echo "   → Read: ONBOARDING_ALLISON.md (Part 1)"
echo ""
echo "Phase 2: Architecture Deep Dive (60 minutes)"
echo "   → Understand how everything connects"
echo "   → Read: ONBOARDING_ALLISON.md (Part 2)"
echo "   → Focus: Integration Layer for GZ360 systems"
echo ""
echo "Phase 3: Guardian System (30 minutes)"
echo "   → Understand validation and amplification"
echo "   → Read: ONBOARDING_ALLISON.md (Part 3)"
echo ""
echo "Phase 4: Hands-On Exploration (60 minutes)"
echo "   → Run it yourself, see it live"
echo "   → Read: ONBOARDING_ALLISON.md (Part 4)"
echo ""
echo "Phase 5: GZ360 Integration Path (30 minutes)"
echo "   → Plan your integration approach"
echo "   → Read: ONBOARDING_ALLISON.md (Part 5)"
echo "   → Focus: Integration points for GZ360"
echo ""

# Show GZ360-specific resources
echo " GZ360-SPECIFIC RESOURCES:"
echo ""
if [ -d "satellites/GZ360Satellite" ]; then
    echo "   GZ360 Satellite: satellites/GZ360Satellite/"
    echo "     → GZ360 profile integration"
    echo "     → Portal Gateway integration"
fi
if [ -f "docs/reference/ZERO_FORENSIC_ANALYSIS_GZ360_BRAVETTO.md" ]; then
    echo "   GZ360 Analysis: docs/reference/ZERO_FORENSIC_ANALYSIS_GZ360_BRAVETTO.md"
fi
if [ -f "orbital/AbeFLOWs-orbital/core/portal/gz360_integration.py" ]; then
    echo "   GZ360 Integration: orbital/AbeFLOWs-orbital/core/portal/gz360_integration.py"
fi
echo ""

# Open onboarding guide
if command -v open >/dev/null 2>&1; then
    echo " Opening your personalized onboarding guide..."
    open ONBOARDING_ALLISON.md
elif command -v xdg-open >/dev/null 2>&1; then
    echo " Opening your personalized onboarding guide..."
    xdg-open ONBOARDING_ALLISON.md
fi

echo ""
echo "============================================================"
echo " ONBOARDING ACTIVATED"
echo ""
echo "Next Steps:"
echo "1. Read ONBOARDING_ALLISON.md (start with Phase 1)"
echo "2. Explore GZ360 integration resources"
echo "3. Run: python3 scripts/converge-engine.py all"
echo "4. Plan your GZ360 integration approach"
echo ""
echo "Pattern: ALLISON × GZ360 × ONBOARDING × ONE"
echo "Guardian: Abë (530 Hz)"
echo "Love Coefficient: ∞"
echo "∞ AbëONE ∞"
echo "============================================================"

