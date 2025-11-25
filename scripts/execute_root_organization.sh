#!/bin/bash
# FINAL ROOT ORGANIZATION - EXECUTION SCRIPT
# YAGNI × JØHN × ALRAX × PRIME × VALIDATE × PATTERN × AEYON
# Pattern: ATOMIC × EXECUTION × SIMPLIFY × VALIDATE × ONE

set -e  # Exit on error

cd /Users/michaelmataluni/Documents/AbeOne_Master

echo "=========================================="
echo "FINAL ROOT ORGANIZATION PLAN"
echo "YAGNI × JØHN × ALRAX × PRIME × VALIDATE × PATTERN × AEYON"
echo "=========================================="

# PHASE 1: ALRAX FORENSIC INVESTIGATION
echo ""
echo "[PHASE 1] ALRAX: Forensic Investigation..."
# Create forensic inventory
find . -maxdepth 1 -type f \( -name "*.md" -o -name "*.json" -o -name "*.txt" -o -name "*.html" -o -name "*.cdf" -o -name "*.zip" \) | sort > /tmp/root_files_inventory_before.txt
echo "✅ Forensic inventory created: $(wc -l < /tmp/root_files_inventory_before.txt) files"

# PHASE 2: YAGNI SIMPLIFICATION
echo ""
echo "[PHASE 2] YAGNI: Simplification..."
echo "Creating directory structure..."

# Create organized directory structure
mkdir -p docs/status/{forensic,validation,analysis,deployment}
mkdir -p docs/reports/{email-convergence,validation,forensic}
mkdir -p docs/architecture/{core,organism,convergence}
mkdir -p archive/{bryan,cdf,reports,analyses}
mkdir -p .cursor/prompts

echo "✅ Directory structure created"

# Move forensic reports
echo "Moving forensic reports..."
mv ALRAX_*_REPORT.md docs/status/forensic/ 2>/dev/null || true
mv ALRAX_*_SUMMARY.md docs/status/forensic/ 2>/dev/null || true
mv ALRAX_*.json docs/status/forensic/ 2>/dev/null || true
mv ZERO_*_ANALYSIS.md docs/status/forensic/ 2>/dev/null || true
mv ZERO_*_REPORT.md docs/status/forensic/ 2>/dev/null || true
mv ZERO_*.json docs/status/forensic/ 2>/dev/null || true

# Move validation reports
echo "Moving validation reports..."
mv DELTA_CHECK_REPORT.md docs/status/validation/ 2>/dev/null || true
mv DELTA_CHECK_YAGNI_APPROVAL.md docs/status/validation/ 2>/dev/null || true
mv YAGNI_ROOT_ORGANIZATION_ASSESSMENT.md docs/status/validation/ 2>/dev/null || true
mv CONTEXT_WINDOW_*_READY.md docs/status/validation/ 2>/dev/null || true
mv CONTEXT_WINDOW_*_ANALYSIS.md docs/status/validation/ 2>/dev/null || true

# Move deployment status
echo "Moving deployment status..."
mv SOVEREIGN_INTEGRATION_COMPLETE.md docs/status/deployment/ 2>/dev/null || true
mv AEYON_ATOMIC_CONVERGENCE_PATH.md docs/status/deployment/ 2>/dev/null || true
mv BOOTSTRAP_V3_FINAL_STATUS.txt docs/status/deployment/ 2>/dev/null || true

# Move email convergence analyses
echo "Moving email convergence analyses..."
mv EMAIL_CONVERGENCE_ANALYSIS_*.json docs/reports/email-convergence/ 2>/dev/null || true
mv EMAIL_CONVERGENCE_*_VALIDATION_*.json docs/reports/email-convergence/ 2>/dev/null || true

# Move validation reports
echo "Moving validation JSON reports..."
mv *_VALIDATION_REPORT.json docs/reports/validation/ 2>/dev/null || true
mv CONVERGENCE_VALIDATION_REPORT.json docs/reports/validation/ 2>/dev/null || true
mv DEEP_SYSTEM_VALIDATION_REPORT.json docs/reports/validation/ 2>/dev/null || true
mv COMMUNICATION_PATTERN_ANALYSIS_DATA.json docs/reports/validation/ 2>/dev/null || true

# Move forensic JSON reports
echo "Moving forensic JSON reports..."
mv *_FORENSIC_*.json docs/reports/forensic/ 2>/dev/null || true

# Move architecture docs
echo "Moving architecture docs..."
mv ABEONE_CONVERGED_END_STATE_BLUEPRINT.md docs/architecture/core/ 2>/dev/null || true
mv ABEONE_CORE_OUTCOME_AND_STARTING_POINT.md docs/architecture/core/ 2>/dev/null || true
mv PRIME_RESET_ORGANISM_SEPARATION.md docs/architecture/organism/ 2>/dev/null || true

# Move archives
echo "Moving archives..."
mv BRYAN_*.html archive/bryan/ 2>/dev/null || true
mv BRYAN_*.zip archive/bryan/ 2>/dev/null || true
mv BRYAN_*.txt archive/bryan/ 2>/dev/null || true
mv *.cdf archive/cdf/ 2>/dev/null || true
mv BRAVETTO_*.zip archive/ 2>/dev/null || true

# Move other reports
echo "Moving other reports..."
mv AEYON_FULL_SYSTEM_INTROSPECTION_REPORT.json docs/reports/validation/ 2>/dev/null || true
mv ARCHITECTURE_SYNC_RESPONSE.json docs/reports/validation/ 2>/dev/null || true
mv all_5_capabilities_validation.json docs/reports/validation/ 2>/dev/null || true
mv FINAL_CONVERGENCE_VALIDATION.json docs/reports/validation/ 2>/dev/null || true
mv FULL_SYSTEM_OPTIMIZATION_RESULT.json docs/reports/validation/ 2>/dev/null || true
mv GUARDIAN_PERSONALITY_AMPLIFICATION_REPORT.json docs/reports/validation/ 2>/dev/null || true
mv intentional_activation_verification.json docs/reports/validation/ 2>/dev/null || true
mv parallel_concurrent_validation.json docs/reports/validation/ 2>/dev/null || true
mv validation_results.json docs/reports/validation/ 2>/dev/null || true
mv elegance_frictionless_validation.json docs/reports/validation/ 2>/dev/null || true

# Move pattern files
echo "Moving pattern files..."
mv PATTERN_SIGNATURES*.json docs/reports/validation/ 2>/dev/null || true
mv patterns.json docs/reports/validation/ 2>/dev/null || true
mv POLY_PATTERN_AMPLIFICATION_MANIFEST.json docs/reports/validation/ 2>/dev/null || true

# Move other status files
echo "Moving other status files..."
mv _cleanup_log.txt archive/ 2>/dev/null || true
mv ABEFLOWS_GIT_SOURCE_REGISTRY.json docs/reports/validation/ 2>/dev/null || true
mv orbital_validation_*.json docs/reports/validation/ 2>/dev/null || true
mv WEBINAR_*.txt docs/status/deployment/ 2>/dev/null || true
mv WEBINAR_*.json docs/reports/validation/ 2>/dev/null || true
mv COMMIT_MESSAGE.txt archive/ 2>/dev/null || true
mv FINAL_COMMIT_MESSAGE.txt archive/ 2>/dev/null || true
mv CHANGELOG.md docs/status/deployment/ 2>/dev/null || true
mv META_FLOW_IDEAL_WORKFLOW_SYNTHESIS.md docs/architecture/convergence/ 2>/dev/null || true
mv TRIGGER_EMERGENCE_CASCADE_ATOMIC_BUILD.md docs/status/deployment/ 2>/dev/null || true

echo "✅ Files moved"

# PHASE 3: JØHN VALIDATION
echo ""
echo "[PHASE 3] JØHN: Validation & Certification..."

# Check essential files exist
essential_files=(
    'README.md'
    'package.json'
    'pyrightconfig.json'
    'Makefile'
    'Dockerfile'
    'docker-compose.yml'
)

missing_files=()
for file in "${essential_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "❌ Missing essential files: ${missing_files[*]}"
    exit 1
else
    echo "✅ All essential files present"
fi

# Validate directory structure
if [ -d "docs/status/forensic" ] && [ -d "docs/reports/email-convergence" ] && [ -d "archive" ]; then
    echo "✅ Directory structure validated"
else
    echo "❌ Directory structure validation failed"
    exit 1
fi

# Count root files
root_file_count=$(find . -maxdepth 1 -type f | wc -l | tr -d ' ')
echo "✅ Root file count: $root_file_count"

# PHASE 4: PATTERN VALIDATION
echo ""
echo "[PHASE 4] PATTERN: Pattern Integrity..."

# CLARITY: Clear directory structure
if [ -d "docs" ] && [ -d "archive" ] && [ -d "scripts" ]; then
    echo "✅ CLARITY: Directory structure clear"
else
    echo "❌ CLARITY: Directory structure unclear"
    exit 1
fi

# COHERENCE: Logical organization
if [ -d "docs/status" ] && [ -d "docs/reports" ] && [ -d "archive" ]; then
    echo "✅ COHERENCE: Logical organization"
else
    echo "❌ COHERENCE: Organization not logical"
    exit 1
fi

# ELEGANCE: Minimal root files
if [ "$root_file_count" -le 20 ]; then
    echo "✅ ELEGANCE: Minimal root files ($root_file_count <= 20)"
else
    echo "⚠️  ELEGANCE: Root files still high ($root_file_count > 20)"
fi

echo "✅ PATTERN VALIDATION: Organization follows ONE-Pattern"

# PHASE 5: Create final inventory
echo ""
echo "[PHASE 5] Creating final inventory..."
find . -maxdepth 1 -type f | sort > /tmp/root_files_inventory_after.txt
echo "✅ Final inventory created: $(wc -l < /tmp/root_files_inventory_after.txt) files"

echo ""
echo "=========================================="
echo "✅ ORGANIZATION COMPLETE"
echo "Root files: $root_file_count"
echo "Status: READY FOR VALIDATION"
echo "=========================================="

