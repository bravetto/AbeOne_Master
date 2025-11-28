#!/bin/bash
# Comprehensive Production + AWS/Linkerd Validation Test Suite
# Orchestrates all validation tests for production deployment readiness

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Default values
BASE_URL="${BASE_URL:-http://localhost:8000}"
NAMESPACE="${NAMESPACE:-default}"
ENVIRONMENT="${ENVIRONMENT:-production}"
AUTH_TOKEN="${AUTH_TOKEN:-}"
ADMIN_TOKEN="${ADMIN_TOKEN:-}"
LINKERD_ENABLED="${LINKERD_ENABLED:-true}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}  Production & AWS/Linkerd Deployment Validation Suite${NC}"
echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo -e "  Base URL: ${YELLOW}${BASE_URL}${NC}"
echo -e "  Namespace: ${YELLOW}${NAMESPACE}${NC}"
echo -e "  Environment: ${YELLOW}${ENVIRONMENT}${NC}"
echo -e "  Linkerd: ${YELLOW}${LINKERD_ENABLED}${NC}"
echo ""

# Check if Python virtual environment exists
if [ -d "${PROJECT_ROOT}/venv" ]; then
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source "${PROJECT_ROOT}/venv/bin/activate"
elif [ -d "${PROJECT_ROOT}/.venv" ]; then
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source "${PROJECT_ROOT}/.venv/bin/activate"
fi

# Check Python and dependencies
echo -e "${BLUE}Checking Python environment...${NC}"
python3 --version || { echo -e "${RED}Python 3 not found${NC}"; exit 1; }

# Install required packages if needed
if ! python3 -c "import httpx" 2>/dev/null; then
    echo -e "${YELLOW}Installing required packages...${NC}"
    pip3 install httpx asyncio || { echo -e "${RED}Failed to install dependencies${NC}"; exit 1; }
fi

# Test results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run test and track results
run_test() {
    local test_name="$1"
    local test_script="$2"
    shift 2
    local test_args="$@"
    
    echo -e "\n${BOLD}${CYAN}─────────────────────────────────────────────────────────────${NC}"
    echo -e "${BOLD}${CYAN}  Running: ${test_name}${NC}"
    echo -e "${BOLD}${CYAN}─────────────────────────────────────────────────────────────${NC}"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if python3 "${SCRIPT_DIR}/${test_script}" ${test_args}; then
        echo -e "\n${GREEN}✓ ${test_name} PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "\n${RED}✗ ${test_name} FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Phase 1: Production Readiness Tests
echo -e "\n${BOLD}${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${BLUE}  PHASE 1: Production Readiness Validation${NC}"
echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════════════${NC}"

run_test \
    "Production Readiness" \
    "test_production_readiness.py" \
    --url "${BASE_URL}" \
    --token "${AUTH_TOKEN}" \
    ${ADMIN_TOKEN:+--admin-token "${ADMIN_TOKEN}"}

PROD_RESULT=$?

# Phase 2: AWS/Linkerd Deployment Tests
echo -e "\n${BOLD}${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${BLUE}  PHASE 2: AWS/Linkerd Deployment Readiness${NC}"
echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════════════${NC}"

LINKERD_FLAG=""
if [ "${LINKERD_ENABLED}" != "true" ]; then
    LINKERD_FLAG="--no-linkerd"
fi

run_test \
    "AWS/Linkerd Deployment" \
    "REPLACE_ME.py" \
    --url "${BASE_URL}" \
    --namespace "${NAMESPACE}" \
    --environment "${ENVIRONMENT}" \
    ${LINKERD_FLAG}

AWS_RESULT=$?

# Final Summary
echo -e "\n${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}  FINAL VALIDATION SUMMARY${NC}"
echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Test Results:${NC}"
echo -e "  Production Readiness: $([ ${PROD_RESULT} -eq 0 ] && echo -e "${GREEN}PASSED${NC}" || echo -e "${RED}FAILED${NC}")"
echo -e "  AWS/Linkerd Deployment: $([ ${AWS_RESULT} -eq 0 ] && echo -e "${GREEN}PASSED${NC}" || echo -e "${RED}FAILED${NC}")"
echo ""
echo -e "${BLUE}Overall Statistics:${NC}"
echo -e "  Total Test Suites: ${BOLD}${TOTAL_TESTS}${NC}"
echo -e "  Passed: ${GREEN}${PASSED_TESTS}${NC}"
echo -e "  Failed: ${RED}${FAILED_TESTS}${NC}"
echo ""

# Exit with error if any test failed
if [ ${FAILED_TESTS} -gt 0 ]; then
    echo -e "${RED}${BOLD}✗ VALIDATION FAILED${NC}"
    echo -e "${YELLOW}Review the test outputs above for details.${NC}"
    exit 1
else
    echo -e "${GREEN}${BOLD}✓ ALL VALIDATION TESTS PASSED${NC}"
    echo -e "${GREEN}System is ready for production deployment!${NC}"
    exit 0
fi

