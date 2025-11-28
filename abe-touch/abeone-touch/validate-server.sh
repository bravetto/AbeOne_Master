#!/bin/bash

# AbëONE Server Validation Script
# Full validation of host server and best practices
# LOVE = LIFE = ONE

echo "∞ AbëONE Server Validation ∞"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Server URL
SERVER_URL="http://localhost:3000"
API_URL="${SERVER_URL}/api/llm/chat"

# Validation counters
PASSED=0
FAILED=0

# Test function
test_endpoint() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "Testing ${name}... "
    
    response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code, expected $expected_status)"
        ((FAILED++))
        return 1
    fi
}

# 1. Server Status
echo -e "${BLUE}1. Server Status${NC}"
echo "-------------------"
if lsof -ti:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server running on port 3000${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Server not running on port 3000${NC}"
    ((FAILED++))
    exit 1
fi
echo ""

# 2. API Health Check
echo -e "${BLUE}2. API Health Check${NC}"
echo "-------------------"
test_endpoint "GET /api/llm/chat" "$API_URL" 200
if [ $? -eq 0 ]; then
    echo "  Response:"
    echo "$body" | jq . 2>/dev/null || echo "$body" | head -5
fi
echo ""

# 3. Security Headers
echo -e "${BLUE}3. Security Headers${NC}"
echo "-------------------"
headers=$(curl -s -I "$SERVER_URL" 2>/dev/null)

check_header() {
    local header=$1
    if echo "$headers" | grep -qi "$header"; then
        echo -e "${GREEN}✓ $header${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠ $header (missing)${NC}"
        ((FAILED++))
    fi
}

check_header "X-Content-Type-Options"
check_header "X-Frame-Options"
check_header "Strict-Transport-Security"
echo ""

# 4. Response Time
echo -e "${BLUE}4. Performance${NC}"
echo "-------------------"
start_time=$(date +%s%N)
curl -s "$API_URL" > /dev/null 2>&1
end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))
if [ $duration -lt 1000 ]; then
    echo -e "${GREEN}✓ Response time: ${duration}ms${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ Response time: ${duration}ms (slow)${NC}"
    ((FAILED++))
fi
echo ""

# 5. TypeScript Compilation
echo -e "${BLUE}5. Type Safety${NC}"
echo "-------------------"
cd "$(dirname "$0")"
if npx tsc --noEmit > /dev/null 2>&1; then
    echo -e "${GREEN}✓ TypeScript compilation: PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ TypeScript compilation: FAIL${NC}"
    ((FAILED++))
fi
echo ""

# 6. Build Check
echo -e "${BLUE}6. Production Build${NC}"
echo "-------------------"
if npm run build > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Production build: PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Production build: FAIL${NC}"
    ((FAILED++))
fi
echo ""

# Summary
echo "================================"
echo -e "${BLUE}Validation Summary${NC}"
echo "================================"
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
else
    echo -e "${GREEN}Failed: 0${NC}"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}∞ All validations passed! ∞${NC}"
    echo ""
    echo "Server URL: $SERVER_URL"
    echo "API URL: $API_URL"
    echo ""
    echo "LOVE = LIFE = ONE"
    echo "Humans ⟡ Ai = ∞"
    echo "∞ AbëONE ∞"
    exit 0
else
    echo -e "${RED}Some validations failed. Please review above.${NC}"
    exit 1
fi

