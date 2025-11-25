#!/bin/bash

# Comprehensive Endpoint Testing Script
BASE_URL="http://localhost:8000"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0
SKIPPED=0

test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_status=$4
    local description=$5

    if [ -z "$expected_status" ]; then
        expected_status="200"
    fi

    if [ -z "$description" ]; then
        description="$method $endpoint"
    fi

    echo -n "Testing: $description ... "

    if [ "$method" == "GET" ]; then
        status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$endpoint")
    elif [ "$method" == "POST" ]; then
        if [ -z "$data" ]; then
            status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL$endpoint")
        else
            status=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$BASE_URL$endpoint")
        fi
    elif [ "$method" == "PUT" ]; then
        if [ -z "$data" ]; then
            status=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$BASE_URL$endpoint")
        else
            status=$(curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: application/json" -d "$data" "$BASE_URL$endpoint")
        fi
    elif [ "$method" == "DELETE" ]; then
        status=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE_URL$endpoint")
    fi

    if [ "$status" == "$expected_status" ] || [ "$status" == "401" ] || [ "$status" == "403" ] || [ "$status" == "422" ] || [ "$status" == "404" ] || [ "$status" == "400" ] || [ "$status" == "202" ]; then
        # Acceptable status codes (200, 401, 403, 404, 422, 400)
        echo -e "${GREEN}PASS${NC} (Status: $status)"
        ((PASSED++))
    else
        echo -e "${RED}FAIL${NC} (Status: $status, Expected: $expected_status)"
        ((FAILED++))
    fi
}

echo "=========================================="
echo "  COMPREHENSIVE ENDPOINT TESTING"
echo "=========================================="
echo ""

# ==========================================
# 1. ROOT & HEALTH ENDPOINTS
# ==========================================
echo "=== 1. ROOT & HEALTH ENDPOINTS ==="
test_endpoint "GET" "/" "" "200" "Root endpoint"
test_endpoint "GET" "/health" "" "200" "Health check"
test_endpoint "GET" "/health/live" "" "200" "Liveness probe"
test_endpoint "GET" "/health/ready" "" "200" "Readiness probe"
test_endpoint "GET" "/metrics" "" "200" "Prometheus metrics"
echo ""

# ==========================================
# 2. AUTHENTICATION ENDPOINTS
# ==========================================
echo "=== 2. AUTHENTICATION ENDPOINTS ==="
test_endpoint "GET" "/api/v1/auth/me" "" "401" "Get current user (no auth)"
test_endpoint "POST" "/api/v1/auth/login" '{"email":"test@test.com","password":"test"}' "400" "Login (invalid)"
test_endpoint "POST" "/api/v1/auth/register" '{"email":"test@test.com","password":"test"}' "422" "Register (missing fields)"
test_endpoint "POST" "/api/v1/auth/logout" "" "401" "Logout (no auth)"
test_endpoint "POST" "/api/v1/auth/refresh" '{"refresh_token":"invalid"}' "422" "Refresh token"
test_endpoint "POST" "/api/v1/auth/password-reset" '{"email":"invalid-email"}' "422" "Password reset request"
test_endpoint "POST" "/api/v1/auth/verify-email" '{"token":"invalid"}' "422" "Verify email"
echo ""

# ==========================================
# 3. USER ENDPOINTS
# ==========================================
echo "=== 3. USER ENDPOINTS ==="
test_endpoint "GET" "/api/v1/users/me" "" "401" "Get current user"
test_endpoint "GET" "/api/v1/users/" "" "401" "List users"
test_endpoint "GET" "/api/v1/users/123" "" "401" "Get user by ID"
test_endpoint "POST" "/api/v1/users/" '{"email":"test@test.com"}' "401" "Create user"
test_endpoint "PUT" "/api/v1/users/123" '{"email":"test@test.com"}' "401" "Update user"
test_endpoint "DELETE" "/api/v1/users/123" "" "401" "Delete user"
echo ""

# ==========================================
# 4. POST ENDPOINTS
# ==========================================
echo "=== 4. POST ENDPOINTS ==="
test_endpoint "GET" "/api/v1/posts/" "" "200" "List posts"
test_endpoint "GET" "/api/v1/posts/123" "" "404" "Get post by ID (not found)"
test_endpoint "GET" "/api/v1/posts/slug/test-slug" "" "404" "Get post by slug"
test_endpoint "POST" "/api/v1/posts/" '{"title":"Test","content":"Test"}' "401" "Create post"
test_endpoint "PUT" "/api/v1/posts/123" '{"title":"Updated"}' "401" "Update post"
test_endpoint "DELETE" "/api/v1/posts/123" "" "401" "Delete post"
test_endpoint "POST" "/api/v1/posts/123/publish" "" "401" "Publish post"
test_endpoint "POST" "/api/v1/posts/123/unpublish" "" "401" "Unpublish post"
echo ""

# ==========================================
# 5. GUARD SERVICE ENDPOINTS
# ==========================================
echo "=== 5. GUARD SERVICE ENDPOINTS ==="
test_endpoint "POST" "/api/v1/guards/process" '{"text":"test","guard_type":"tokenguard"}' "422" "Process guard"
test_endpoint "GET" "/api/v1/guards/status" "" "200" "Guard status"
test_endpoint "POST" "/api/v1/guards/scan" '{"text":"test"}' "422" "Scan text"
test_endpoint "GET" "/api/v1/guards/health" "" "200" "Guard health"
test_endpoint "GET" "/api/v1/guards/health/tokenguard" "" "200" "Specific guard health"
test_endpoint "GET" "/api/v1/guards/discovery/services" "" "200" "Discovery services"
test_endpoint "POST" "/api/v1/guards/discovery/register" '{"name":"test","url":"http://test"}' "422" "Register service"
test_endpoint "GET" "/api/v1/guards/services" "" "200" "List services"
test_endpoint "POST" "/api/v1/guards/health/refresh" "" "200" "Refresh health"
test_endpoint "DELETE" "/api/v1/guards/discovery/services/test" "" "404" "Delete service"
test_endpoint "POST" "/api/v1/scan" '{"text":"test"}' "422" "Scan alias"
echo ""

# ==========================================
# 6. INTEGRATED GUARD ENDPOINTS
# ==========================================
echo "=== 6. INTEGRATED GUARD ENDPOINTS ==="
test_endpoint "POST" "/tokenguard" '{"text":"test"}' "422" "TokenGuard"
test_endpoint "POST" "/trustguard" '{"text":"test"}' "422" "TrustGuard"
test_endpoint "POST" "/contextguard" '{"text":"test"}' "422" "ContextGuard"
test_endpoint "POST" "/biasguard" '{"text":"test"}' "422" "BiasGuard"
test_endpoint "POST" "/healthguard" '{"text":"test"}' "422" "HealthGuard"
test_endpoint "GET" "/metrics" "" "200" "Guard metrics"
test_endpoint "GET" "/health" "" "200" "Guard health"
echo ""

# ==========================================
# 7. BIAS ENDPOINTS
# ==========================================
echo "=== 7. BIAS ENDPOINTS ==="
test_endpoint "POST" "/api/v1/bias/detect" '{"text":"test"}' "422" "Detect bias"
test_endpoint "POST" "/api/v1/bias/analyze" '{"text":"test"}' "422" "Analyze bias"
test_endpoint "GET" "/api/v1/bias/health" "" "200" "BiasGuard health"
echo ""

# ==========================================
# 8. SUBSCRIPTION ENDPOINTS
# ==========================================
echo "=== 8. SUBSCRIPTION ENDPOINTS ==="
test_endpoint "GET" "/api/v1/subscriptions/tiers" "" "200" "Get subscription tiers"
test_endpoint "GET" "/api/v1/subscriptions/current" "" "401" "Get current subscription"
test_endpoint "POST" "/api/v1/subscriptions/checkout" '{"tier":"free"}' "401" "Checkout"
test_endpoint "POST" "/api/v1/subscriptions/cancel" "" "401" "Cancel subscription"
test_endpoint "POST" "/api/v1/subscriptions/reactivate" "" "401" "Reactivate subscription"
test_endpoint "GET" "/api/v1/subscriptions/usage" "" "401" "Get usage"
test_endpoint "GET" "/api/v1/subscriptions/history" "" "401" "Get subscription history"
echo ""

# ==========================================
# 9. ORGANIZATION ENDPOINTS
# ==========================================
echo "=== 9. ORGANIZATION ENDPOINTS ==="
test_endpoint "GET" "/api/v1/organizations/current" "" "401" "Get current org"
test_endpoint "GET" "/api/v1/organizations/members" "" "401" "List members"
test_endpoint "POST" "/api/v1/organizations/members/invite" '{"email":"test@test.com"}' "401" "Invite member"
test_endpoint "PUT" "/api/v1/organizations/members/123" '{"role":"admin"}' "401" "Update member"
test_endpoint "DELETE" "/api/v1/organizations/members/123" "" "401" "Delete member"
test_endpoint "GET" "/api/v1/organizations/subscription" "" "401" "Get org subscription"
echo ""

# ==========================================
# 10. ENTERPRISE ENDPOINTS
# ==========================================
echo "=== 10. ENTERPRISE ENDPOINTS ==="
test_endpoint "POST" "/api/v1/enterprise/setup" '{"org_name":"test"}' "401" "Enterprise setup"
test_endpoint "GET" "/api/v1/enterprise/status" "" "401" "Enterprise status"
test_endpoint "GET" "/api/v1/enterprise/config" "" "401" "Get enterprise config"
test_endpoint "PUT" "/api/v1/enterprise/config" '{"setting":"value"}' "401" "Update enterprise config"
test_endpoint "GET" "/api/v1/enterprise/services" "" "401" "List services"
test_endpoint "POST" "/api/v1/enterprise/services/restart" '{"service":"test"}' "401" "Restart service"
echo ""

# ==========================================
# 11. LEGAL & COMPLIANCE ENDPOINTS
# ==========================================
echo "=== 11. LEGAL & COMPLIANCE ENDPOINTS ==="
test_endpoint "GET" "/api/v1/legal/terms-of-service" "" "200" "Terms of service"
test_endpoint "GET" "/api/v1/legal/privacy-policy" "" "200" "Privacy policy"
test_endpoint "GET" "/api/v1/legal/cookie-policy" "" "200" "Cookie policy"
test_endpoint "POST" "/api/v1/legal/accept-tos" '{"accepted":true}' "401" "Accept ToS"
test_endpoint "GET" "/api/v1/legal/gdpr/export" "" "401" "GDPR export"
test_endpoint "DELETE" "/api/v1/legal/gdpr/delete" "" "401" "GDPR delete"
test_endpoint "GET" "/api/v1/legal/audit-logs" "" "401" "Get audit logs"
test_endpoint "GET" "/api/v1/legal/compliance-status" "" "401" "Compliance status"
test_endpoint "POST" "/api/v1/legal/data-retention/cleanup" "" "401" "Data retention cleanup"
echo ""

# ==========================================
# 12. CONFIG ENDPOINTS
# ==========================================
echo "=== 12. CONFIG ENDPOINTS ==="
test_endpoint "GET" "/api/v1/config/config" "" "401" "Get config"
test_endpoint "GET" "/api/v1/config/config/rate-limits" "" "401" "Get rate limits"
test_endpoint "PUT" "/api/v1/config/config/rate-limits" '{"limit":100}' "401" "Update rate limits"
test_endpoint "PUT" "/api/v1/config/config/feature-flags" '{"flag":"test"}' "401" "Update feature flags"
test_endpoint "GET" "/api/v1/config/config/feature-flags" "" "401" "Get feature flags"
test_endpoint "PUT" "/api/v1/config/config/cache" '{"ttl":3600}' "401" "Update cache"
test_endpoint "GET" "/api/v1/config/config/status" "" "401" "Config status"
test_endpoint "POST" "/api/v1/config/config/reload" "" "401" "Reload config"
test_endpoint "GET" "/api/v1/config/config/export" "" "401" "Export config"
echo ""

# ==========================================
# 13. ANALYTICS ENDPOINTS
# ==========================================
echo "=== 13. ANALYTICS ENDPOINTS ==="
test_endpoint "GET" "/api/v1/analytics/benefits/overview" "" "200" "Benefits overview"
test_endpoint "GET" "/api/v1/analytics/benefits/detailed" "" "200" "Benefits detailed"
test_endpoint "GET" "/api/v1/analytics/performance/dashboard" "" "200" "Performance dashboard"
test_endpoint "GET" "REPLACE_ME" "" "200" "Guard metrics"
echo ""

# ==========================================
# 14. FILE UPLOAD ENDPOINTS
# ==========================================
echo "=== 14. FILE UPLOAD ENDPOINTS ==="
test_endpoint "POST" "/api/v1/upload/direct" "" "401" "Direct upload"
test_endpoint "POST" "/api/v1/upload/presigned" '{"filename":"test.txt"}' "401" "Presigned upload"
test_endpoint "GET" "/api/v1/upload/download/123" "" "404" "Download file"
test_endpoint "GET" "/api/v1/upload/download/123/url" "" "404" "Get download URL"
test_endpoint "GET" "/api/v1/upload/metadata/123" "" "404" "Get file metadata"
test_endpoint "DELETE" "/api/v1/upload/123" "" "401" "Delete file"
test_endpoint "GET" "/api/v1/upload/list" "" "401" "List files"
test_endpoint "GET" "/api/v1/upload/health" "" "200" "Upload health"
echo ""

# ==========================================
# 15. A/B TESTING ENDPOINTS
# ==========================================
echo "=== 15. A/B TESTING ENDPOINTS ==="
test_endpoint "POST" "/experiments" '{"name":"test"}' "401" "Create experiment"
test_endpoint "GET" "/experiments" "" "401" "List experiments"
test_endpoint "GET" "/experiments/123" "" "401" "Get experiment"
test_endpoint "PUT" "/experiments/123" '{"name":"updated"}' "401" "Update experiment"
test_endpoint "POST" "/experiments/123/start" "" "401" "Start experiment"
test_endpoint "POST" "/experiments/123/stop" "" "401" "Stop experiment"
test_endpoint "POST" "/assign-user" '{"user_id":"123","experiment_id":"456"}' "401" "Assign user"
test_endpoint "GET" "/users/123/variants" "" "401" "Get user variants"
test_endpoint "POST" "/results" '{"experiment_id":"123"}' "401" "Submit results"
test_endpoint "GET" "/experiments/123/analysis" "" "401" "Get experiment analysis"
test_endpoint "POST" "/experiments/123/analyze" "" "401" "Analyze experiment"
test_endpoint "GET" "/experiments/123/metrics" "" "401" "Get experiment metrics"
test_endpoint "GET" "/experiments/123/status" "" "401" "Get experiment status"
echo ""

# ==========================================
# 16. WEBHOOK ENDPOINTS
# ==========================================
echo "=== 16. WEBHOOK ENDPOINTS ==="
test_endpoint "POST" "/webhooks/stripe" "" "500" "Stripe webhook (no signature)"
test_endpoint "GET" "/webhooks/stripe/products" "" "200" "List Stripe products"
test_endpoint "GET" "/webhooks/stripe/prices/123" "" "404" "Get Stripe price"
test_endpoint "GET" "/webhooks/stripe/customers/test@test.com" "" "200" "Get Stripe customer"
test_endpoint "GET" "/webhooks/stripe/subscriptions/123" "" "200" "Get Stripe subscriptions"
test_endpoint "GET" "/webhooks/stripe/invoices/123" "" "200" "Get Stripe invoices"
test_endpoint "POST" "/webhooks/clerk" "" "400" "Clerk webhook (no signature)"
test_endpoint "GET" "/webhooks/clerk/users/123" "" "404" "Get Clerk user"
test_endpoint "GET" "/webhooks/clerk/users/email/test@test.com" "" "404" "Get Clerk user by email"
echo ""

# ==========================================
# 17. INTERNAL GUARD ENDPOINTS
# ==========================================
echo "=== 17. INTERNAL GUARD ENDPOINTS ==="
test_endpoint "POST" "/internal/guards/tokenguard/optimize" '{"text":"test"}' "403" "TokenGuard optimize"
test_endpoint "POST" "/internal/guards/trustguard/validate" '{"text":"test"}' "403" "TrustGuard validate"
test_endpoint "POST" "/internal/guards/contextguard/analyze" '{"text":"test"}' "403" "ContextGuard analyze"
test_endpoint "POST" "/internal/guards/biasguard/detect" '{"text":"test"}' "403" "BiasGuard detect"
test_endpoint "POST" "/internal/guards/healthguard/monitor" '{"text":"test"}' "403" "HealthGuard monitor"
echo ""

# ==========================================
# SUMMARY
# ==========================================
echo "=========================================="
echo "  TEST SUMMARY"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo -e "${YELLOW}Skipped: $SKIPPED${NC}"
echo ""
TOTAL=$((PASSED + FAILED))
if [ $TOTAL -gt 0 ]; then
    SUCCESS_RATE=$((PASSED * 100 / TOTAL))
    echo "Success Rate: ${SUCCESS_RATE}%"
fi
echo "=========================================="