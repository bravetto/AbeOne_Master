#!/bin/bash

# Test script for BiasGuard API endpoint
# Usage: ./test_biasguard_api.sh <CLERK_TOKEN>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if token is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Clerk token is required${NC}"
    echo "Usage: $0 <CLERK_TOKEN>"
    echo ""
    echo "To get your Clerk token:"
    echo "1. Open your browser's developer console"
    echo "2. Go to https://dashboard.aiguardian.ai (or your app)"
    echo "3. Check localStorage or sessionStorage for 'clerk-session'"
    echo "4. Or use Clerk's getToken() method in browser console"
    exit 1
fi

CLERK_TOKEN="$1"
API_URL="https://api.aiguardian.ai/api/v1/guards/process"

echo -e "${YELLOW}Testing BiasGuard API...${NC}"
echo "Endpoint: $API_URL"
echo ""

# Test request
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $CLERK_TOKEN" \
  -d '{
    "service_type": "biasguard",
    "payload": {
        "text": "hello world",
        "contentType": "text",
        "scanLevel": "standard",
        "context": "webpage-content"
    },
    "user_id": "REPLACE_ME",
    "session_id": "manual_terminal_test",
    "client_type": "chrome",
    "client_version": "1.0.0"
  }')

# Extract HTTP status code (last line)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
# Extract response body (all but last line)
BODY=$(echo "$RESPONSE" | sed '$d')

echo -e "${YELLOW}HTTP Status Code:${NC} $HTTP_CODE"
echo ""
echo -e "${YELLOW}Response Body:${NC}"
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"

# Check if request was successful
if [ "$HTTP_CODE" -eq 200 ]; then
    echo ""
    echo -e "${GREEN} Request successful!${NC}"
    
    # Extract bias score if available
    BIAS_SCORE=$(echo "$BODY" | jq -r '.data.bias_score // .data.score // "N/A"' 2>/dev/null)
    if [ "$BIAS_SCORE" != "N/A" ] && [ "$BIAS_SCORE" != "null" ]; then
        echo -e "${GREEN}Bias Score: $BIAS_SCORE${NC}"
    fi
else
    echo ""
    echo -e "${RED} Request failed with status $HTTP_CODE${NC}"
    exit 1
fi

