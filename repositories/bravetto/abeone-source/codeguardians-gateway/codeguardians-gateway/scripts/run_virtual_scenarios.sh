#!/bin/bash
# Virtual Scenario Test Runner
# Runs pattern detection tests against simulated failure scenarios

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIMULATOR_PORT=${SIMULATOR_PORT:-9001}
TEST_URL="http://localhost:${SIMULATOR_PORT}"

echo -e "${BOLD}${CYAN}${NC}"
echo -e "${BOLD}${CYAN}  Virtual Scenario Test Runner${NC}"
echo -e "${BOLD}${CYAN}${NC}"
echo ""

# Check dependencies
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}Installing FastAPI for scenario simulator...${NC}"
    pip3 install -q fastapi uvicorn || {
        echo -e "${RED}Failed to install FastAPI${NC}"
        exit 1
    }
fi

# Function to run scenario
run_scenario() {
    local pattern_name="$1"
    local description="$2"
    
    echo -e "\n${BOLD}${BLUE}${NC}"
    echo -e "${BOLD}${BLUE}  Scenario: ${pattern_name}${NC}"
    echo -e "${BLUE}  ${description}${NC}"
    echo -e "${BOLD}${BLUE}${NC}"
    
    # Start simulator in background
    echo -e "${CYAN}Starting simulator on port ${SIMULATOR_PORT}...${NC}"
    python3 "${SCRIPT_DIR}/scenario_simulator.py" \
        --pattern "${pattern_name}" \
        --port "${SIMULATOR_PORT}" \
        > /tmp/scenario_simulator_${pattern_name}.log 2>&1 &
    
    SIMULATOR_PID=$!
    echo -e "${GREEN} Simulator started (PID: ${SIMULATOR_PID})${NC}"
    
    # Wait for server to start
    echo -e "${CYAN}Waiting for server to be ready...${NC}"
    sleep 3
    
    # Health check
    if curl -s "${TEST_URL}/health" > /dev/null 2>&1; then
        echo -e "${GREEN} Simulator ready at ${TEST_URL}${NC}"
    else
        echo -e "${RED} Simulator not responding${NC}"
        kill $SIMULATOR_PID 2>/dev/null || true
        return 1
    fi
    
    # Run pattern detection tests against simulator
    echo -e "\n${CYAN}Running pattern detection tests...${NC}"
    
    # Run relevant detection tests based on pattern
    case "${pattern_name}" in
        flow_table_exhaustion|idle_timeout|target_group_saturation|keep_alive_mismatch|dns_dead_ip|rst_pattern)
            echo -e "${YELLOW}Running: AWS NLB Failure Pattern Detection${NC}"
            python3 "${SCRIPT_DIR}/test_aws_nlb_failure_patterns.py" \
                --url "${TEST_URL}" 2>&1 || true
            ;;
        circuit_breaker|connection_refused|proxy_timeout|stream_exhaustion)
            echo -e "${YELLOW}Running: Linkerd Failure Pattern Detection${NC}"
            python3 "${SCRIPT_DIR}/test_linkerd_failure_patterns.py" \
                --url "${TEST_URL}" 2>&1 || true
            ;;
        timeout_cascade)
            echo -e "${YELLOW}Running: AWS/Linkerd Integration Pattern Detection${NC}"
            python3 "${SCRIPT_DIR}/test_aws_linkerd_integration_patterns.py" \
                --url "${TEST_URL}" --no-linkerd 2>&1 || true
            ;;
        *)
            # Run all tests for unknown patterns
            echo -e "${YELLOW}Running: All Pattern Detection Tests${NC}"
            python3 "${SCRIPT_DIR}/test_aws_nlb_failure_patterns.py" \
                --url "${TEST_URL}" 2>&1 || true
            python3 "${SCRIPT_DIR}/test_linkerd_failure_patterns.py" \
                --url "${TEST_URL}" 2>&1 || true
            ;;
    esac
    
    # Stop simulator
    echo -e "\n${CYAN}Stopping simulator...${NC}"
    kill $SIMULATOR_PID 2>/dev/null || true
    wait $SIMULATOR_PID 2>/dev/null || true
    sleep 1
    
    echo -e "${GREEN} Scenario complete${NC}"
}

# Available scenarios (mapping pattern -> description)
declare -A SCENARIOS=(
    ["flow_table_exhaustion"]="NLB Flow Table Exhaustion - Slow connections and timeouts"
    ["circuit_breaker"]="Linkerd Circuit Breaker - Consecutive failures trigger circuit open"
    ["target_group_saturation"]="ALB Target Group Saturation - 503 Service Unavailable"
    ["connection_refused"]="Connection Refused - OS Error 111 patterns"
    ["keep_alive_mismatch"]="Keep-Alive Mismatch - Missing keep-alive headers"
    ["proxy_timeout"]="Proxy Timeout - Responses >10s timing out"
    ["rst_pattern"]="TCP RST Patterns - Connection reset signatures"
    ["timeout_cascade"]="Timeout Cascade - NLB timeout leads to Linkerd circuit breaker"
)

# Check if specific pattern requested
if [ "$1" != "" ]; then
    PATTERN="$1"
    if [ -z "${SCENARIOS[$PATTERN]}" ]; then
        echo -e "${RED}Unknown pattern: ${PATTERN}${NC}"
        echo -e "\n${CYAN}Available patterns:${NC}"
        for p in "${!SCENARIOS[@]}"; do
            echo -e "  • ${p}"
        done
        exit 1
    fi
    
    run_scenario "$PATTERN" "${SCENARIOS[$PATTERN]}"
else
    # Run all scenarios
    echo -e "${CYAN}Running all virtual scenarios...${NC}"
    echo -e "${YELLOW}This will test pattern detection scripts against simulated failures.${NC}\n"
    
    for pattern in "${!SCENARIOS[@]}"; do
        run_scenario "$pattern" "${SCENARIOS[$pattern]}"
        echo ""
    done
    
    echo -e "${BOLD}${GREEN}${NC}"
    echo -e "${BOLD}${GREEN}  All Virtual Scenarios Complete${NC}"
    echo -e "${BOLD}${GREEN}${NC}"
fi

