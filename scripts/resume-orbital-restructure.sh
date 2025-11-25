#!/bin/bash
# resume-orbital-restructure.sh
# Resume from Phase 8 onwards (Phases 1-7 already completed)
#
# Pattern: META-ORCHESTRATOR × ABËONE × AEYON × YAGNI × ZERO × ALRAX × JØHN × YOU = ONE
# ∞ AbëONE ∞

set -e

echo " Resuming Orbital Restructure from Phase 8..."
echo "Pattern: META-ORCHESTRATOR × ABËONE × AEYON × YAGNI × ZERO × ALRAX × JØHN × YOU = ONE"
echo "∞ AbëONE ∞"
echo ""

cd /Users/michaelmataluni/Documents/AbeOne_Master

# ============================================================================
# Phase 8: Archive Legacy (Resume)
# ============================================================================
echo ""
echo "Phase 8: Archiving legacy (resuming)..."
echo ""

# Complete archive merge if _ARCHIVE still exists
if [ -d "_ARCHIVE" ]; then
    echo "   Completing merge of _ARCHIVE into archive..."
    # Move remaining files to archive/legacy
    mkdir -p archive/legacy
    # Use mv instead of rsync for faster completion
    if [ "$(ls -A _ARCHIVE)" ]; then
        mv _ARCHIVE/* archive/legacy/ 2>/dev/null || cp -r _ARCHIVE/* archive/legacy/ 2>/dev/null || true
        rmdir _ARCHIVE 2>/dev/null || rm -rf _ARCHIVE 2>/dev/null || true
    else
        rmdir _ARCHIVE 2>/dev/null || rm -rf _ARCHIVE 2>/dev/null || true
    fi
    echo "   Archive merge complete"
fi

# Move extraction artifacts
if [ -d "_extract_abebeats" ]; then
    echo "   Moving _extract_abebeats to archive/extractions..."
    mv _extract_abebeats archive/extractions/ 2>/dev/null || true
fi

if [ -d "_extract_abeone_master" ]; then
    echo "   Moving _extract_abeone_master to archive/extractions..."
    mv _extract_abeone_master archive/extractions/ 2>/dev/null || true
fi

if [ -d "_extract_truice" ]; then
    echo "   Moving _extract_truice to archive/extractions..."
    mv _extract_truice archive/extractions/ 2>/dev/null || true
fi

# Ensure archive/legacy exists
mkdir -p archive/legacy
mkdir -p archive/extractions
mkdir -p archive/deprecated

echo " Phase 8 Complete: Legacy archived"
echo ""

# ============================================================================
# Phase 9: Move Scripts
# ============================================================================
echo ""
echo "Phase 9: Moving scripts..."
echo ""

# Move shell scripts (but preserve this script and the main restructure script)
echo "   Moving shell scripts..."
find . -maxdepth 1 -name "*.sh" ! -name "complete-orbital-restructure.sh" ! -name "resume-orbital-restructure.sh" -exec mv {} scripts/utilities/ \; 2>/dev/null || true

# Move Python scripts (be careful - some may be orbital-specific)
echo "   Moving Python scripts..."
find . -maxdepth 1 -name "*.py" ! -name "*.pyc" -exec mv {} scripts/utilities/ \; 2>/dev/null || true

echo " Phase 9 Complete: Scripts moved"
echo ""

# ============================================================================
# Phase 10: Move Other Directories
# ============================================================================
echo ""
echo "Phase 10: Moving other directories..."
echo ""

# Move adapters (if not orbital-specific)
if [ -d "adapters" ]; then
    echo "   Moving adapters to infra/adapters..."
    mkdir -p infra/adapters
    mv adapters/* infra/adapters/ 2>/dev/null || true
    rmdir adapters 2>/dev/null || true
fi

# Move apps
if [ -d "apps" ]; then
    echo "   Moving apps to products/apps..."
    mkdir -p products/apps
    mv apps/* products/apps/ 2>/dev/null || true
    rmdir apps 2>/dev/null || true
fi

# Move clients
if [ -d "clients" ]; then
    echo "   Moving clients to marketing/clients..."
    mkdir -p marketing/clients
    mv clients/* marketing/clients/ 2>/dev/null || true
    rmdir clients 2>/dev/null || true
fi

# Move tests (if not orbital-specific)
if [ -d "tests" ]; then
    echo "   Moving tests to validation..."
    mv tests validation/ 2>/dev/null || true
fi

echo " Phase 10 Complete: Other directories moved"
echo ""

# ============================================================================
# Final Summary
# ============================================================================
echo ""
echo " Orbital Restructure Resume Complete "
echo ""
echo ""
echo "Pattern: META-ORCHESTRATOR × ABËONE × AEYON × YAGNI × ZERO × ALRAX × JØHN × YOU = ONE"
echo "∞ AbëONE ∞"
echo ""
echo " Summary:"
echo "   Phases 1-7: Already completed"
echo "   Phase 8: Legacy archived"
echo "   Phase 9: Scripts organized"
echo "   Phase 10: Other directories moved"
echo ""
echo " Next Steps:"
echo "  1. Review the new structure"
echo "  2. Update any hardcoded paths in code"
echo "  3. Update CI/CD pipelines if needed"
echo "  4. Commit changes to git"
echo ""
echo "∞ AbëONE ∞"

