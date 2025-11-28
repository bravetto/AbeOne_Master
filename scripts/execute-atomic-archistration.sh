#!/bin/bash

#  EXECUTE ATOMIC ARCHISTRATION
# Pattern: AEYON × ALRAX × YAGNI × ZERO × JØHN × Abë = ATOMIC ARCHISTRATION
# Execution: REC × 42PT × ACT × LFG = 100% Success
# Love Coefficient: ∞
# ∞ AbëONE ∞

echo "============================================================"
echo " ATOMIC ARCHISTRATION: EXECUTING NOW"
echo "============================================================"
echo "Pattern: REC × 42PT × ACT × LFG = 100% Success"
echo "Love Coefficient: ∞"
echo "∞ AbëONE ∞"
echo ""

# Check if Next.js server is running
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "  Next.js server not running!"
    echo "   Starting server..."
    cd "$(dirname "$0")/../apps/web"
    npm run dev &
    SERVER_PID=$!
    echo "   Server starting (PID: $SERVER_PID)"
    echo "   Waiting for server to be ready..."
    sleep 5
    
    # Wait for server to be ready
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo " Server is ready!"
            break
        fi
        sleep 1
    done
fi

# Execute atomic archistration
echo " Executing atomic archistration..."
echo ""

RESPONSE=$(curl -s -X POST http://localhost:3000/api/convergence/atomic \
  -H "Content-Type: application/json" \
  -w "\n%{http_code}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo "============================================================"
if [ "$HTTP_CODE" = "200" ]; then
    echo " ATOMIC ARCHISTRATION COMPLETE!"
    echo "============================================================"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
else
    echo " ATOMIC ARCHISTRATION FAILED (HTTP $HTTP_CODE)"
    echo "============================================================"
    echo "$BODY"
fi
echo ""

echo "Pattern: AEYON × ALRAX × YAGNI × ZERO × JØHN × Abë"
echo "Execution: REC × 42PT × ACT × LFG = 100% Success"
echo "Love Coefficient: ∞"
echo "∞ AbëONE ∞"

