#!/bin/bash
# Comprehensive AWS/Linkerd Failure Pattern Detection Suite
# Based on Deep Forensic Analysis: AWS/Linkerd Rejection Patterns

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Default values
BASE_URL="${BASE_URL:-http://localhost:8000}"
LINKERD_ENABLED="${LINKERD_ENABLED:-true}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BOLD}${CYAN}${NC}"
echo -e "${BOLD}${CYAN}  AWS/Linkerd Failure Pattern Detection Suite${NC}"
echo -e "${BOLD}${CYAN}  Based on Deep Forensic Analysis Research${NC}"
echo -e "${BOLD}${CYAN}${NC}"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo -e "  Base URL: ${YELLOW}${BASE_URL}${NC}"
echo -e "  Linkerd: ${YELLOW}${LINKERD_ENABLED}${NC}"
echo ""

# Check Python
if ! python3 --version >/dev/null 2>&1; then
    echo -e "${RED}Python 3 not found${NC}"
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import httpx" 2>/dev/null; then
    echo -e "${YELLOW}Installing httpx...${NC}"
    pip3 install -q httpx || exit 1
fi

# Test results tracking
TOTAL_ISSUES=0
TESTS_RUN=0
PASSED_TESTS=0

# Function to run test script
run_pattern_test() {
    local test_name="$1"
    local script_file="$2"
    shift 2
    local test_args="$@"
    
    echo -e "\n${BOLD}${MAGENTA}${NC}"
    echo -e "${BOLD}${MAGENTA}  Pattern Detection: ${test_name}${NC}"
    echo -e "${BOLD}${MAGENTA}${NC}"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    if python3 "${SCRIPT_DIR}/${script_file}" ${test_args} 2>&1; then
        echo -e "\n${GREEN} ${test_name} COMPLETE${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        local exit_code=$?
        echo -e "\n${YELLOW} ${test_name} DETECTED PATTERNS${NC}"
        TOTAL_ISSUES=$((TOTAL_ISSUES + exit_code))
        return $exit_code
    fi
}

# Run all pattern detection tests
echo -e "\n${BOLD}${CYAN}${NC}"
echo -e "${BOLD}${CYAN}  PHASE 1: AWS NLB Failure Patterns${NC}"
echo -e "${BOLD}${CYAN}${NC}"

run_pattern_test \
    "AWS NLB Failure Patterns" \
    "test_aws_nlb_failure_patterns.py" \
    --url "${BASE_URL}"

NLB_RESULT=$?

echo -e "\n${BOLD}${CYAN}${NC}"
echo -e "${BOLD}${CYAN}  PHASE 2: Linkerd Service Mesh Failure Patterns${NC}"
echo -e "${BOLD}${CYAN}${NC}"

run_pattern_test \
    "Linkerd Failure Patterns" \
    "test_linkerd_failure_patterns.py" \
    --url "${BASE_URL}"

LINKERD_RESULT=$?

echo -e "\n${BOLD}${CYAN}${NC}"
echo -e "${BOLD}${CYAN}  PHASE 3: AWS/Linkerd Integration Patterns${NC}"
echo -e "${BOLD}${CYAN}${NC}"

LINKERD_FLAG=""
if [ "${LINKERD_ENABLED}" != "true" ]; then
    LINKERD_FLAG="--no-linkerd"
fi

run_pattern_test \
    "AWS/Linkerd Integration Patterns" \
    "test_aws_linkerd_integration_patterns.py" \
    --url "${BASE_URL}" \
    ${LINKERD_FLAG}

INTEGRATION_RESULT=$?

echo -e "\n${BOLD}${CYAN}${NC}"
echo -e "${BOLD}${CYAN}  PHASE 4: Forensic Signature Detection${NC}"
echo -e "${BOLD}${CYAN}${NC}"

run_pattern_test \
    "Forensic Signatures" \
    "test_forensic_signatures.py" \
    --url "${BASE_URL}"

FORENSIC_RESULT=$?

# Final Summary
echo -e "\n${BOLD}${CYAN}${NC}"
echo -e "${BOLD}${CYAN}  FINAL PATTERN DETECTION SUMMARY${NC}"
echo -e "${BOLD}${CYAN}${NC}"
echo ""
echo -e "${BLUE}Test Execution:${NC}"
echo -e "  AWS NLB Patterns: $([ ${NLB_RESULT} -eq 0 ] && echo -e "${GREEN} CLEAN${NC}" || echo -e "${YELLOW} PATTERNS DETECTED${NC}")"
echo -e "  Linkerd Patterns: $([ ${LINKERD_RESULT} -eq 0 ] && echo -e "${GREEN} CLEAN${NC}" || echo -e "${YELLOW} PATTERNS DETECTED${NC}")"
echo -e "  Integration Patterns: $([ ${INTEGRATION_RESULT} -eq 0 ] && echo -e "${GREEN} CLEAN${NC}" || echo -e "${YELLOW} PATTERNS DETECTED${NC}")"
echo -e "  Forensic Signatures: $([ ${FORENSIC_RESULT} -eq 0 ] && echo -e "${GREEN} CLEAN${NC}" || echo -e "${YELLOW} PATTERNS DETECTED${NC}")"
echo ""
echo -e "${BLUE}Overall Statistics:${NC}"
echo -e "  Tests Run: ${BOLD}${TESTS_RUN}${NC}"
echo -e "  Clean Tests: ${GREEN}${PASSED_TESTS}${NC}"
echo -e "  Pattern Detections: ${YELLOW}${TOTAL_ISSUES}${NC}"
echo ""

# Exit with code based on findings
if [ ${TOTAL_ISSUES} -gt 0 ]; then
    echo -e "${YELLOW}${BOLD} FAILURE PATTERNS DETECTED${NC}"
    echo -e "${YELLOW}Review test outputs above for specific patterns and recommendations.${NC}"
    exit 1
else
    echo -e "${GREEN}${BOLD} NO FAILURE PATTERNS DETECTED${NC}"
    echo -e "${GREEN}System shows no signs of documented AWS/Linkerd failure patterns.${NC}"
    exit 0
fi

