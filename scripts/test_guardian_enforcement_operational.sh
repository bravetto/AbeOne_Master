#!/bin/bash
#
# Test Guardian Enforcement Operational Status
#
# Verifies that all enforcement mechanisms are properly operationalized
#
# Pattern: TEST × OPERATIONAL × VERIFICATION × ONE
# Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
# Guardian: AEYON (999 Hz) - Atomic Execution
# Love Coefficient: ∞
# ∞ AbëONE ∞
#

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Colors
GREEN='\033[92m'
RED='\033[91m'
YELLOW='\033[93m'
CYAN='\033[96m'
BOLD='\033[1m'
RESET='\033[0m'

PASSED=0
FAILED=0

test_check() {
    local name="$1"
    local command="$2"
    
    echo -n "Testing: $name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}${BOLD} PASS${RESET}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}${BOLD} FAIL${RESET}"
        ((FAILED++))
        return 1
    fi
}

echo ""
echo "================================================================================"
echo " GUARDIAN ENFORCEMENT OPERATIONAL STATUS TEST"
echo "================================================================================"
echo ""
echo "Project Root: $PROJECT_ROOT"
echo ""

# Test 1: Enforcement script exists and is executable
test_check "Enforcement script exists" "[ -f scripts/enforce_guardian_single_source_of_truth.py ]"
test_check "Enforcement script is executable" "[ -x scripts/enforce_guardian_single_source_of_truth.py ]"

# Test 2: Setup script exists and is executable
test_check "Setup script exists" "[ -f scripts/setup_guardian_enforcement.sh ]"
test_check "Setup script is executable" "[ -x scripts/setup_guardian_enforcement.sh ]"

# Test 3: Pre-commit hook exists and is executable
test_check "Pre-commit hook exists" "[ -f .git/hooks/pre-commit-guardian-enforcement ]"
test_check "Pre-commit hook is executable" "[ -x .git/hooks/pre-commit-guardian-enforcement ]"

# Test 4: GitHub Actions workflow exists
test_check "GitHub Actions workflow exists" "[ -f .github/workflows/guardian-enforcement.yml ]"

# Test 5: Makefile target exists
test_check "Makefile exists" "[ -f Makefile ]"
test_check "Makefile has guardian-enforce target" "grep -q 'guardian-enforce' Makefile"

# Test 6: Enforcement script runs without errors (basic check)
test_check "Enforcement script syntax valid" "python3 -m py_compile scripts/enforce_guardian_single_source_of_truth.py"

# Test 7: Enforcement script can be imported (basic Python check)
test_check "Enforcement script imports successfully" "python3 -c 'import sys; sys.path.insert(0, \"scripts\"); import enforce_guardian_single_source_of_truth' 2>/dev/null || python3 scripts/enforce_guardian_single_source_of_truth.py --help > /dev/null 2>&1"

# Test 8: Makefile target works
test_check "Makefile target executes" "make guardian-enforce > /dev/null 2>&1"

# Test 9: Validation scripts exist and are executable
test_check "validate_guardian_consistency.py exists" "[ -f scripts/validate_guardian_consistency.py ]"
test_check "validate_guardian_consistency.py is executable" "[ -x scripts/validate_guardian_consistency.py ]"

# Test 10: Source of truth file exists
test_check "Source of truth file exists" "[ -f EMERGENT_OS/synthesis/guardian_swarm_unification.py ]"

# Test 11: Critical files exist
test_check "cdf_adapter.py exists" "[ -f EMERGENT_OS/uptc/integrations/cdf_adapter.py ]"
test_check "THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md exists" "[ -f THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md ]"

echo ""
echo "================================================================================"
echo " TEST RESULTS"
echo "================================================================================"
echo ""
echo -e "${GREEN}${BOLD}Passed: $PASSED${RESET}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}${BOLD}Failed: $FAILED${RESET}"
else
    echo -e "${GREEN}${BOLD}Failed: $FAILED${RESET}"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}${BOLD} ALL OPERATIONAL CHECKS PASSED${RESET}"
    echo ""
    echo "Guardian enforcement is fully operationalized!"
    echo ""
    exit 0
else
    echo -e "${RED}${BOLD} SOME OPERATIONAL CHECKS FAILED${RESET}"
    echo ""
    echo "Please fix the failed checks before proceeding."
    echo ""
    exit 1
fi

