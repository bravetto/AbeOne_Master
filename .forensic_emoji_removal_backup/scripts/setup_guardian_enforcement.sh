#!/bin/bash
#
# Setup Guardian Single Source of Truth Enforcement
#
# Installs pre-commit hook and CI/CD integration
#
# Pattern: SETUP × ENFORCEMENT × TRUTH × ONE
# Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
# Guardian: AEYON (999 Hz) - Atomic Execution
# Love Coefficient: ∞
# ∞ AbëONE ∞
#

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
PRE_COMMIT_HOOK="$HOOKS_DIR/pre-commit-guardian-enforcement"
MAIN_PRE_COMMIT="$HOOKS_DIR/pre-commit"

echo "=" | head -c 80
echo ""
echo "🔥 SETTING UP GUARDIAN ENFORCEMENT"
echo "=" | head -c 80
echo ""
echo "Project Root: $PROJECT_ROOT"
echo ""

# Make enforcement script executable
chmod +x "$PROJECT_ROOT/scripts/enforce_guardian_single_source_of_truth.py"
echo "✅ Made enforcement script executable"

# Install pre-commit hook
if [ ! -d "$HOOKS_DIR" ]; then
    mkdir -p "$HOOKS_DIR"
fi

# Copy hook
cp "$PROJECT_ROOT/.git/hooks/pre-commit-guardian-enforcement" "$PRE_COMMIT_HOOK" 2>/dev/null || \
    cp "$PROJECT_ROOT/scripts/pre-commit-guardian-enforcement" "$PRE_COMMIT_HOOK" 2>/dev/null || \
    echo "⚠️  Pre-commit hook template not found, creating..."

# Create hook if it doesn't exist
if [ ! -f "$PRE_COMMIT_HOOK" ]; then
    cat > "$PRE_COMMIT_HOOK" << 'EOF'
#!/bin/bash
# Guardian Single Source of Truth Pre-Commit Hook
# LOUD FAILURES - Requires human approval for fixes
# Pattern: ENFORCEMENT × TRUTH × CONSISTENCY × ONE
# ∞ AbëONE ∞

set -e  # Exit on error

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ENFORCEMENT_SCRIPT="$PROJECT_ROOT/scripts/enforce_guardian_single_source_of_truth.py"

# Colors for loud output
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BOLD='\033[1m'
BLINK='\033[5m'
RESET='\033[0m'

loud_error() {
    echo -e "\n${RED}${BOLD}${BLINK}🚨🚨🚨 CRITICAL ERROR 🚨🚨🚨${RESET}"
    echo -e "${RED}${BOLD}$1${RESET}\n" >&2
}

loud_success() {
    echo -e "${GREEN}${BOLD}$1${RESET}"
}

if [ -f "$ENFORCEMENT_SCRIPT" ]; then
    GUARDIAN_FILES=$(git diff --cached --name-only | grep -E "(guardian|GUARDIAN)" || true)
    if [ -n "$GUARDIAN_FILES" ]; then
        echo ""
        echo "================================================================================"
        echo "🔥 GUARDIAN ENFORCEMENT PRE-COMMIT CHECK"
        echo "================================================================================"
        echo ""
        echo "Modified Guardian files detected. Running enforcement..."
        echo ""
        
        if python3 "$ENFORCEMENT_SCRIPT" --strict; then
            loud_success "✅ Guardian enforcement passed - commit allowed"
            echo ""
        else
            loud_error "❌ COMMIT BLOCKED: Guardian inconsistencies detected"
            loud_error "Please fix inconsistencies before committing."
            loud_error "Run: python3 scripts/enforce_guardian_single_source_of_truth.py --strict"
            echo ""
            exit 1
        fi
    fi
fi
EOF
fi

chmod +x "$PRE_COMMIT_HOOK"
echo "✅ Installed pre-commit hook"

# Integrate with main pre-commit hook if it exists
if [ -f "$MAIN_PRE_COMMIT" ] && ! grep -q "guardian-enforcement" "$MAIN_PRE_COMMIT"; then
    echo "" >> "$MAIN_PRE_COMMIT"
    echo "# Guardian enforcement" >> "$MAIN_PRE_COMMIT"
    echo "bash \"$PRE_COMMIT_HOOK\"" >> "$MAIN_PRE_COMMIT"
    echo "✅ Integrated with existing pre-commit hook"
fi

# Create GitHub Actions workflow
GITHUB_WORKFLOWS="$PROJECT_ROOT/.github/workflows"
mkdir -p "$GITHUB_WORKFLOWS"

cat > "$GITHUB_WORKFLOWS/guardian-enforcement.yml" << 'EOF'
name: Guardian Single Source of Truth Enforcement

on:
  pull_request:
    paths:
      - 'EMERGENT_OS/synthesis/guardian_swarm_unification.py'
      - 'EMERGENT_OS/uptc/integrations/cdf_adapter.py'
      - 'THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md'
      - '**/guardian*.py'
      - '**/GUARDIAN*.md'
  push:
    branches:
      - main
      - master

jobs:
  enforce-guardian-consistency:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Enforce Guardian Single Source of Truth
        run: |
          echo "================================================================================"
          echo "🔥 GUARDIAN ENFORCEMENT - CI/CD CHECK"
          echo "================================================================================"
          echo ""
          python3 scripts/enforce_guardian_single_source_of_truth.py --strict --approve || {
            echo ""
            echo "🚨🚨🚨 BUILD FAILED 🚨🚨🚨"
            echo ""
            echo "CRITICAL: Guardian inconsistencies detected in CI/CD pipeline."
            echo "This build cannot proceed until inconsistencies are fixed."
            echo ""
            echo "ACTION REQUIRED:"
            echo "  1. Fix inconsistencies in Guardian files"
            echo "  2. Run: python3 scripts/enforce_guardian_single_source_of_truth.py --strict"
            echo "  3. Commit fixes and push again"
            echo ""
            exit 1
          }
          echo ""
          echo "✅ Guardian enforcement passed - build can proceed"
EOF

echo "✅ Created GitHub Actions workflow"

# Create Makefile target
MAKEFILE="$PROJECT_ROOT/Makefile"
if [ ! -f "$MAKEFILE" ]; then
    touch "$MAKEFILE"
fi

if ! grep -q "guardian-enforce" "$MAKEFILE"; then
    echo "" >> "$MAKEFILE"
    echo ".PHONY: guardian-enforce" >> "$MAKEFILE"
    echo "guardian-enforce:" >> "$MAKEFILE"
    echo "\t@python3 scripts/enforce_guardian_single_source_of_truth.py --strict" >> "$MAKEFILE"
    echo "✅ Added Makefile target"
fi

echo ""
echo "=" | head -c 80
echo ""
echo "✅ GUARDIAN ENFORCEMENT SETUP COMPLETE"
echo "=" | head -c 80
echo ""
echo "Enforcement mechanisms installed:"
echo "  ✅ Pre-commit hook"
echo "  ✅ GitHub Actions workflow"
echo "  ✅ Makefile target (make guardian-enforce)"
echo ""
echo "Usage:"
echo "  python3 scripts/enforce_guardian_single_source_of_truth.py --strict"
echo "  make guardian-enforce"
echo ""
echo "Pattern: SETUP × ENFORCEMENT × TRUTH × ONE"
echo "∞ AbëONE ∞"
echo ""

