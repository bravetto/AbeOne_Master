#!/bin/bash
# Quick Test Script for Danny - AWS/Linkerd Virtual Environment

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GATEWAY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BOLD}${CYAN}${NC}"
echo -e "${BOLD}${CYAN}  Danny's Quick Test Suite - AWS/Linkerd Virtual Environment${NC}"
echo -e "${BOLD}${CYAN}${NC}"
echo ""

# Function to run test
run_test() {
    local test_name="$1"
    local command="$2"
    
    echo -e "${CYAN}Testing: ${test_name}...${NC}"
    if eval "$command" > /tmp/danny_test_${test_name// /_}.log 2>&1; then
        echo -e "${GREEN} PASSED${NC}"
        return 0
    else
        echo -e "${YELLOW} FAILED (check /tmp/danny_test_${test_name// /_}.log)${NC}"
        return 1
    fi
}

# Test 1: Check prerequisites
echo -e "${BOLD}Phase 1: Prerequisites${NC}"
echo ""

run_test "Python 3" "python3 --version"
run_test "AWS CLI" "aws --version"
run_test "Docker" "docker --version"

# Test 2: AWS Authentication
echo ""
echo -e "${BOLD}Phase 2: AWS Authentication${NC}"
echo ""

if aws sts get-caller-identity --profile mxm0118 > /dev/null 2>&1; then
    echo -e "${GREEN} AWS SSO authenticated (mxm0118)${NC}"
    export AWS_PROFILE=mxm0118
elif aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${GREEN} AWS authenticated (default)${NC}"
else
    echo -e "${YELLOW} AWS not authenticated - run: aws sso login --profile mxm0118${NC}"
fi

# Test 3: Virtual Scenario Testing
echo ""
echo -e "${BOLD}Phase 3: Virtual Scenario Testing${NC}"
echo ""

echo -e "${CYAN}Starting virtual scenario simulator (circuit_breaker pattern)...${NC}"
cd "$GATEWAY_DIR"

# Start simulator in background
python3 scripts/scenario_simulator.py \
    --pattern circuit_breaker \
    --port 9001 \
    > /tmp/danny_scenario.log 2>&1 &
SIMULATOR_PID=$!

# Wait for startup
sleep 3

# Check if simulator is running
if curl -s http://localhost:9001/health > /dev/null 2>&1; then
    echo -e "${GREEN} Simulator running on port 9001${NC}"
    
    # Run detection tests
    echo ""
    echo -e "${CYAN}Running Linkerd pattern detection...${NC}"
    python3 scripts/test_linkerd_failure_patterns.py \
        --url http://localhost:9001 || true
    
    # Stop simulator
    kill $SIMULATOR_PID 2>/dev/null || true
    wait $SIMULATOR_PID 2>/dev/null || true
    echo -e "${GREEN} Simulator stopped${NC}"
else
    echo -e "${YELLOW} Simulator not responding${NC}"
    kill $SIMULATOR_PID 2>/dev/null || true
fi

# Test 4: Production Readiness (if server running)
echo ""
echo -e "${BOLD}Phase 4: Production Readiness${NC}"
echo ""

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN} Production server detected on port 8000${NC}"
    echo -e "${CYAN}Running production readiness tests...${NC}"
    python3 scripts/test_production_readiness.py \
        --url http://localhost:8000 || true
else
    echo -e "${YELLOW} No server on port 8000 (start with: ./scripts/launch_no_fail_local.sh)${NC}"
fi

# Test 5: ECR Push Test (if authenticated)
echo ""
echo -e "${BOLD}Phase 5: ECR Push Validation${NC}"
echo ""

if [ -n "$AWS_PROFILE" ] || aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${CYAN}Testing ECR access...${NC}"
    if aws ecr get-login-password --region us-east-1 ${AWS_PROFILE:+--profile $AWS_PROFILE} > /dev/null 2>&1; then
        echo -e "${GREEN} ECR access confirmed${NC}"
        echo -e "${CYAN}Ready to push: ./push-to-ecr.sh${NC}"
    else
        echo -e "${YELLOW} ECR access failed - check credentials${NC}"
    fi
else
    echo -e "${YELLOW} Not authenticated - skipping ECR test${NC}"
fi

# Summary
echo ""
echo -e "${BOLD}${CYAN}${NC}"
echo -e "${BOLD}${CYAN}  Test Suite Complete${NC}"
echo -e "${BOLD}${CYAN}${NC}"
echo ""
echo -e "${BLUE}Quick Commands:${NC}"
echo "  Virtual Scenarios: ./scripts/run_virtual_scenarios.sh"
echo "  Pattern Detection: python scripts/test_*.py --url <url>"
echo "  ECR Push: ./push-to-ecr.sh"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  Full Guide: docs/DANNY_AWS_LINKERD_VIRTUAL_ENVIRONMENT.md"
echo ""

