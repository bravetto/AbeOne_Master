#!/bin/bash
# Danny's Complete Test Suite - AWS/Linkerd Virtual Environment
# Runs comprehensive testing workflow for infrastructure validation

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GATEWAY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="/tmp/danny_test_results_${TIMESTAMP}"
mkdir -p "$RESULTS_DIR"

echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}  Danny's Complete Test Suite - AWS/Linkerd Virtual Environment${NC}"
echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Results Directory: ${RESULTS_DIR}${NC}"
echo ""

cd "$GATEWAY_DIR"

# Track results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run test and capture results
run_and_capture() {
    local test_name="$1"
    local command="$2"
    local output_file="$RESULTS_DIR/${test_name// /_}.log"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -e "${CYAN}▶️  ${test_name}...${NC}"
    if eval "$command" > "$output_file" 2>&1; then
        echo -e "${GREEN}   ✓ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${YELLOW}   ⚠ FAILED (see ${output_file})${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Phase 1: Prerequisites Check
echo -e "${BOLD}${MAGENTA}─── Phase 1: Prerequisites Check ───${NC}"
echo ""

run_and_capture "Python 3 Check" "python3 --version"
run_and_capture "AWS CLI Check" "aws --version"
run_and_capture "Docker Check" "docker --version"

# Phase 2: AWS Authentication
echo ""
echo -e "${BOLD}${MAGENTA}─── Phase 2: AWS Authentication ───${NC}"
echo ""

if aws sts get-caller-identity --profile mxm0118 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ AWS SSO authenticated (mxm0118)${NC}"
    export AWS_PROFILE=mxm0118
elif aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${GREEN}✓ AWS authenticated (default profile)${NC}"
else
    echo -e "${YELLOW}⚠ AWS not authenticated (skipping AWS tests)${NC}"
fi

# Phase 3: Virtual Scenario Testing
echo ""
echo -e "${BOLD}${MAGENTA}─── Phase 3: Virtual Scenario Testing ───${NC}"
echo ""

SCENARIO_PATTERNS=("circuit_breaker" "flow_table_exhaustion" "target_group_saturation")
for pattern in "${SCENARIO_PATTERNS[@]}"; do
    echo -e "${CYAN}Testing pattern: ${pattern}${NC}"
    
    # Start simulator
    python3 scripts/scenario_simulator.py \
        --pattern "$pattern" \
        --port 9001 \
        > "$RESULTS_DIR/simulator_${pattern}.log" 2>&1 &
    SIMULATOR_PID=$!
    
    sleep 3
    
    # Run detection tests
    case "$pattern" in
        circuit_breaker|connection_refused|proxy_timeout|stream_exhaustion)
            python3 scripts/test_linkerd_failure_patterns.py \
                --url http://localhost:9001 \
                --json > "$RESULTS_DIR/linkerd_${pattern}.json" 2>&1 || true
            ;;
        flow_table_exhaustion|target_group_saturation|keep_alive_mismatch|dns_dead_ip|rst_pattern)
            python3 scripts/REPLACE_ME.py \
                --url http://localhost:9001 \
                --json > "$RESULTS_DIR/nlb_${pattern}.json" 2>&1 || true
            ;;
        timeout_cascade)
            python3 scripts/REPLACE_ME.py \
                --url http://localhost:9001 \
                --json > "$RESULTS_DIR/integration_${pattern}.json" 2>&1 || true
            ;;
    esac
    
    # Stop simulator
    kill $SIMULATOR_PID 2>/dev/null || true
    wait $SIMULATOR_PID 2>/dev/null || true
    sleep 1
done

echo -e "${GREEN}✓ Virtual scenario testing complete${NC}"

# Phase 4: Pattern Detection Scripts Validation
echo ""
echo -e "${BOLD}${MAGENTA}─── Phase 4: Pattern Detection Scripts ───${NC}"
echo ""

# Just verify scripts are executable and can be imported
run_and_capture "AWS NLB Test Script" "python3 scripts/REPLACE_ME.py --list 2>&1 || python3 -c 'import scripts.REPLACE_ME; print(\"OK\")'"
run_and_capture "Linkerd Test Script" "python3 scripts/test_linkerd_failure_patterns.py --list 2>&1 || python3 -c 'import scripts.test_linkerd_failure_patterns; print(\"OK\")'"
run_and_capture "Forensic Test Script" "python3 scripts/test_forensic_signatures.py --list 2>&1 || python3 -c 'import scripts.test_forensic_signatures; print(\"OK\")'"

# Phase 5: Production Readiness (if server running)
echo ""
echo -e "${BOLD}${MAGENTA}─── Phase 5: Production Readiness Validation ───${NC}"
echo ""

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Production server detected on port 8000${NC}"
    
    python3 scripts/test_production_readiness.py \
        --url http://localhost:8000 \
        --json > "$RESULTS_DIR/production_readiness.json" 2>&1 || true
    
    python3 scripts/REPLACE_ME.py \
        --url http://localhost:8000 \
        --no-linkerd \
        --json > "$RESULTS_DIR/aws_linkerd_deployment.json" 2>&1 || true
    
    echo -e "${GREEN}✓ Production readiness tests complete${NC}"
else
    echo -e "${YELLOW}⚠ No server on port 8000 (start with: ./scripts/launch_no_fail_local.sh)${NC}"
fi

# Phase 6: ECR Access (if authenticated)
echo ""
echo -e "${BOLD}${MAGENTA}─── Phase 6: ECR Access Validation ───${NC}"
echo ""

if [ -n "$AWS_PROFILE" ] || aws sts get-caller-identity > /dev/null 2>&1; then
    if aws ecr get-login-password --region us-east-1 ${AWS_PROFILE:+--profile $AWS_PROFILE} > /dev/null 2>&1; then
        echo -e "${GREEN}✓ ECR access confirmed${NC}"
        
        # Check repository exists
        if aws ecr describe-repositories \
            --repository-names gateway \
            --region us-east-1 \
            ${AWS_PROFILE:+--profile $AWS_PROFILE} > /dev/null 2>&1; then
            echo -e "${GREEN}✓ ECR repository 'gateway' exists${NC}"
        else
            echo -e "${YELLOW}⚠ ECR repository 'gateway' not found${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ ECR access failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Not authenticated - skipping ECR validation${NC}"
fi

# Final Summary
echo ""
echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}  Test Suite Summary${NC}"
echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Test Execution:${NC}"
echo -e "  Total Tests: ${BOLD}${TOTAL_TESTS}${NC}"
echo -e "  Passed: ${GREEN}${PASSED_TESTS}${NC}"
echo -e "  Failed: ${RED}${FAILED_TESTS}${NC}"
echo ""
echo -e "${BLUE}Results Directory:${NC}"
echo -e "  ${RESULTS_DIR}"
echo ""
echo -e "${BLUE}Key Results Files:${NC}"
ls -1 "$RESULTS_DIR" | head -10 | grep -E "\.(json|log)$" | while read file; do
    echo -e "  • ${file}"
done
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Review results in: ${RESULTS_DIR}"
echo "  2. Check virtual scenario logs"
echo "  3. Review pattern detection results"
echo "  4. For production: ./scripts/launch_no_fail_local.sh"
echo ""
echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"

# Exit with appropriate code
if [ $FAILED_TESTS -eq 0 ]; then
    exit 0
else
    exit 1
fi

