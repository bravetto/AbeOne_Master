#!/bin/bash
# FINAL ROOT ORGANIZATION - PASS 2 (YAGNI RADICAL SIMPLIFICATION)
# Pattern: YAGNI × SIMPLIFY × REMOVE × UNNECESSARY × ONE

set -e

cd /Users/michaelmataluni/Documents/AbeOne_Master

echo "=========================================="
echo "YAGNI PASS 2: RADICAL SIMPLIFICATION"
echo "=========================================="

# Create additional directories
mkdir -p docs/marketing
mkdir -p docs/reports/validation
mkdir -p archive/logs
mkdir -p archive/backups
mkdir -p archive/pdfs
mkdir -p data
mkdir -p config

echo "✅ Additional directories created"

# Move PDFs
echo "Moving PDFs..."
mv *.pdf docs/marketing/ 2>/dev/null || true
mv MARKETING_DOCUMENTS.zip docs/marketing/ 2>/dev/null || true

# Move HTML files
echo "Moving HTML files..."
mv drift-dashboard-eternal.html docs/reports/validation/ 2>/dev/null || true
mv SYSTEM_EXPERIENCE_MANIFESTATION.html docs/reports/validation/ 2>/dev/null || true

# Move utility Python scripts
echo "Moving utility Python scripts..."
mv aeyon_boot_hardened.py scripts/ 2>/dev/null || true
mv aeyon_boot_integration.py scripts/ 2>/dev/null || true
mv compare_with_source.py scripts/ 2>/dev/null || true
mv consciousness_status.py scripts/ 2>/dev/null || true
mv local_ai_assistant_bridge.py scripts/ 2>/dev/null || true
mv restore_and_push.py scripts/ 2>/dev/null || true
mv FINAL_PR_ORCHESTRATION.py scripts/ 2>/dev/null || true

# Move JSON reports and analyses
echo "Moving JSON reports..."
mv comparison_results.json docs/reports/validation/ 2>/dev/null || true
mv EMAIL_CONVERGENCE_VALIDATION_*.json docs/reports/email-convergence/ 2>/dev/null || true
mv orbital_validation_*.json.gz docs/reports/validation/ 2>/dev/null || true
mv PATTERN_SIGNATURES*.json.gz docs/reports/validation/ 2>/dev/null || true
mv seal_metrics.json docs/reports/validation/ 2>/dev/null || true
mv TRUICE_EPIC_PRESET.json docs/reports/validation/ 2>/dev/null || true
mv universal_repository_awareness.json docs/reports/validation/ 2>/dev/null || true
mv CDF_EXECUTION_NOW.index.json archive/cdf/ 2>/dev/null || true
mv CDF_GO_VIRAL_PLAN.index.json archive/cdf/ 2>/dev/null || true

# Move config files
echo "Moving config files..."
mv newsletters_config.json config/ 2>/dev/null || true

# Move logs
echo "Moving logs..."
mv ngrok.log archive/logs/ 2>/dev/null || true
mv test_results_full.log archive/logs/ 2>/dev/null || true

# Move database files
echo "Moving database files..."
mv poisonguard.db data/ 2>/dev/null || true

# Move backup files
echo "Moving backup files..."
mv hidden_files_backup.zip archive/backups/ 2>/dev/null || true
mv .ai-context-source-of-truth.json.backup archive/backups/ 2>/dev/null || true
mv .gitignore.bak archive/backups/ 2>/dev/null || true

# Move drift status files (these are operational, but can be in .abeone_memory or docs)
echo "Moving drift status files..."
mv .drift-operational.json docs/status/validation/ 2>/dev/null || true
mv .drift-status.json docs/status/validation/ 2>/dev/null || true
mv .drift-status.txt docs/status/validation/ 2>/dev/null || true

# Move other operational files
echo "Moving operational files..."
mv .ignore-pattern-lock.json docs/status/validation/ 2>/dev/null || true
mv .suite-manifest.json docs/status/validation/ 2>/dev/null || true
mv .system-activated.json docs/status/validation/ 2>/dev/null || true

# Move prompt files
echo "Moving prompt files..."
mv FRESH_WINDOW_PROMPT.txt .cursor/prompts/ 2>/dev/null || true
mv NEW_CONTEXT_WINDOW_PROMPT.md .cursor/prompts/ 2>/dev/null || true

# Move documentation
echo "Moving documentation..."
mv FINAL_ROOT_ORGANIZATION_PLAN.md docs/architecture/core/ 2>/dev/null || true
mv ZERO_PRIME_COMBINATION_STRATEGY.md docs/architecture/core/ 2>/dev/null || true

# Move requirements files
echo "Moving requirements files..."
mv discord_bot_requirements.txt docs/status/deployment/ 2>/dev/null || true

# Move .env files (keep templates, move test env)
mv .env.biasguard.test archive/ 2>/dev/null || true

# Count root files
root_file_count=$(find . -maxdepth 1 -type f | wc -l | tr -d ' ')

echo ""
echo "✅ YAGNI PASS 2 COMPLETE"
echo "Root files: $root_file_count"
echo "=========================================="

