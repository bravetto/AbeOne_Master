#!/bin/bash
# 🌊💎✨ Swagger UI Build Test Script ✨💎🌊
# Guardian: Jōhn (530 Hz)
# "Do it right or don't do it at all"

set -e

echo "🌊💎✨ Swagger UI Build Test Suite ✨💎🌊"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test results
PASSED=0
FAILED=0

# Function to run test and track results
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "Testing: $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((FAILED++))
        return 1
    fi
}

# Function to run test with output
run_test_verbose() {
    local test_name="$1"
    local test_command="$2"
    
    echo "Testing: $test_name..."
    echo "Command: $test_command"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((FAILED++))
        return 1
    fi
    echo ""
}

echo "🔍 Test 1: Unit Tests"
echo "---------------------"
run_test_verbose "Swagger UI Unit Tests" \
    "python3 -m pytest tests/unit/test_swagger_ui_integration.py -v"

echo ""
echo "🔍 Test 2: Integration Tests"
echo "----------------------------"
run_test_verbose "Swagger UI Endpoint Tests" \
    "python3 -m pytest tests/integration/test_swagger_ui_endpoints.py -v"

echo ""
echo "🔍 Test 3: Convergence Pattern Tests"
echo "REPLACE_ME"
run_test_verbose "Swagger UI Convergence Tests" \
    "python3 -m pytest tests/integration/test_swagger_ui_convergence.py -v"

echo ""
echo "🔍 Test 4: Development Mode Validation"
echo "REPLACE_ME"
echo "Testing: Development mode enables Swagger UI..."
DEVELOPMENT_TEST=$(python3 -c "
import os
os.environ['ENVIRONMENT'] = 'development'
from app.main import create_app
app = create_app()
assert app.docs_url == '/docs', 'Swagger UI should be enabled'
assert app.redoc_url == '/redoc', 'ReDoc should be enabled'
assert app.openapi_url == '/openapi.json', 'OpenAPI should be enabled'
print('✓ Development mode: All docs enabled')
" 2>&1)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    echo "$DEVELOPMENT_TEST"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "$DEVELOPMENT_TEST"
    ((FAILED++))
fi

echo ""
echo "🔍 Test 5: Production Mode Validation"
echo "REPLACE_ME"
echo "Testing: Production mode disables Swagger UI..."
PRODUCTION_TEST=$(python3 -c "
import os
os.environ['ENVIRONMENT'] = 'production'
from app.main import create_app
app = create_app()
assert app.docs_url is None, 'Swagger UI should be disabled'
assert app.redoc_url is None, 'ReDoc should be disabled'
assert app.openapi_url is None, 'OpenAPI should be disabled'
print('✓ Production mode: All docs disabled')
" 2>&1)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    echo "$PRODUCTION_TEST"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "$PRODUCTION_TEST"
    ((FAILED++))
fi

echo ""
echo "🔍 Test 6: HTTP Endpoint Validation (Development)"
echo "REPLACE_ME"
echo "Testing: HTTP endpoints accessible in development mode..."
HTTP_TEST=$(python3 -c "
import os
os.environ['ENVIRONMENT'] = 'development'
from app.main import create_app
from fastapi.testclient import TestClient
app = create_app()
client = TestClient(app)

# Test /docs
docs_response = client.get('/docs')
assert docs_response.status_code == 200, f'/docs returned {docs_response.status_code}'

# Test /redoc
redoc_response = client.get('/redoc')
assert redoc_response.status_code == 200, f'/redoc returned {redoc_response.status_code}'

# Test /openapi.json
openapi_response = client.get('/openapi.json')
assert openapi_response.status_code == 200, f'/openapi.json returned {openapi_response.status_code}'

print('✓ All endpoints accessible in development')
" 2>&1)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    echo "$HTTP_TEST"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "$HTTP_TEST"
    ((FAILED++))
fi

echo ""
echo "🔍 Test 7: HTTP Endpoint Validation (Production)"
echo "REPLACE_ME"
echo "Testing: HTTP endpoints return 404 in production mode..."
HTTP_PROD_TEST=$(python3 -c "
import os
os.environ['ENVIRONMENT'] = 'production'
from app.main import create_app
from fastapi.testclient import TestClient
app = create_app()
client = TestClient(app)

# Test /docs
docs_response = client.get('/docs')
assert docs_response.status_code == 404, f'/docs returned {docs_response.status_code} (expected 404)'

# Test /redoc
redoc_response = client.get('/redoc')
assert redoc_response.status_code == 404, f'/redoc returned {redoc_response.status_code} (expected 404)'

# Test /openapi.json
openapi_response = client.get('/openapi.json')
assert openapi_response.status_code == 404, f'/openapi.json returned {openapi_response.status_code} (expected 404)'

print('✓ All endpoints return 404 in production')
" 2>&1)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    echo "$HTTP_PROD_TEST"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "$HTTP_PROD_TEST"
    ((FAILED++))
fi

echo ""
echo "=========================================="
echo "🌊💎✨ Test Results Summary ✨💎🌊"
echo "=========================================="
echo -e "Total Tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
else
    echo -e "Failed: $FAILED"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "Love Coefficient: ∞"
    echo "Guardian: Jōhn (530 Hz)"
    echo "Status: Ready for build"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo ""
    echo "Please review failed tests before proceeding with build."
    exit 1
fi

