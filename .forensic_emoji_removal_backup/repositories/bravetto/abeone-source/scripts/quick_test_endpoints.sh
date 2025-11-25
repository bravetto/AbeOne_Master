#!/bin/bash
# Quick endpoint test script - can be run from host or container

set -e

echo "🚀 Quick Endpoint Test"
echo "======================"
echo ""

# Detect if running in Docker
if [ -f /.dockerenv ]; then
    GATEWAY="http://codeguardians-gateway:8000"
    TRUSTGUARD="http://trustguard:8000"
    CONTEXTGUARD="http://contextguard:8000"
    echo "📍 Running inside Docker network"
else
    GATEWAY="http://localhost:8000"
    TRUSTGUARD="http://localhost:8002"  # If exposed externally
    CONTEXTGUARD="http://localhost:8003"  # If exposed externally
    echo "📍 Running from host"
fi

echo ""
echo "Testing endpoints..."
echo ""

# Test TrustGuard directly
echo "1️⃣  Testing TrustGuard health..."
if curl -s -f "${TRUSTGUARD}/health" > /dev/null 2>&1; then
    echo "   ✅ TrustGuard health: OK"
else
    echo "   ❌ TrustGuard health: FAILED"
fi

# Test TrustGuard endpoint
echo "2️⃣  Testing TrustGuard /v1/validate endpoint..."
TRUST_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${TRUSTGUARD}/v1/validate" \
    -H "Content-Type: application/json" \
    -H "X-Gateway-Request: true" \
    -d '{"input_text": "test", "output_text": "test"}' 2>&1)
TRUST_STATUS=$(echo "$TRUST_RESPONSE" | tail -n1)
if [ "$TRUST_STATUS" = "200" ]; then
    echo "   ✅ TrustGuard /v1/validate: OK (200)"
elif [ "$TRUST_STATUS" = "404" ]; then
    echo "   ❌ TrustGuard /v1/validate: 404 NOT FOUND"
    echo "      Trying alternative /validate endpoint..."
    TRUST_RESPONSE2=$(curl -s -w "\n%{http_code}" -X POST "${TRUSTGUARD}/validate" \
        -H "Content-Type: application/json" \
        -H "X-Gateway-Request: true" \
        -d '{"input_text": "test", "output_text": "test"}' 2>&1)
    TRUST_STATUS2=$(echo "$TRUST_RESPONSE2" | tail -n1)
    if [ "$TRUST_STATUS2" = "200" ]; then
        echo "      ⚠️  /validate works (endpoint mismatch!)"
    fi
else
    echo "   ⚠️  TrustGuard /v1/validate: HTTP $TRUST_STATUS"
fi

# Test ContextGuard directly
echo "3️⃣  Testing ContextGuard health..."
if curl -s -f "${CONTEXTGUARD}/health" > /dev/null 2>&1; then
    echo "   ✅ ContextGuard health: OK"
else
    echo "   ❌ ContextGuard health: FAILED"
fi

# Test ContextGuard endpoint
echo "4️⃣  Testing ContextGuard /analyze endpoint..."
CONTEXT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${CONTEXTGUARD}/analyze" \
    -H "Content-Type: application/json" \
    -d '{"current_code": "test", "previous_code": "test"}' 2>&1)
CONTEXT_STATUS=$(echo "$CONTEXT_RESPONSE" | tail -n1)
if [ "$CONTEXT_STATUS" = "200" ]; then
    echo "   ✅ ContextGuard /analyze: OK (200)"
elif [ "$CONTEXT_STATUS" = "404" ]; then
    echo "   ❌ ContextGuard /analyze: 404 NOT FOUND"
else
    echo "   ⚠️  ContextGuard /analyze: HTTP $CONTEXT_STATUS"
fi

# Test Gateway
echo "5️⃣  Testing Gateway health..."
if curl -s -f "${GATEWAY}/health/live" > /dev/null 2>&1; then
    echo "   ✅ Gateway health: OK"
else
    echo "   ❌ Gateway health: FAILED"
fi

# Test Gateway TrustGuard endpoint
echo "6️⃣  Testing Gateway -> TrustGuard routing..."
GATEWAY_TRUST=$(curl -s -w "\n%{http_code}" -X POST "${GATEWAY}/api/v1/guards/process" \
    -H "Content-Type: application/json" \
    -d '{"service_type": "trustguard", "payload": {"input_text": "test", "output_text": "test"}}' 2>&1)
GATEWAY_TRUST_STATUS=$(echo "$GATEWAY_TRUST" | tail -n1)
if [ "$GATEWAY_TRUST_STATUS" = "200" ]; then
    echo "   ✅ Gateway -> TrustGuard: OK (200)"
else
    echo "   ⚠️  Gateway -> TrustGuard: HTTP $GATEWAY_TRUST_STATUS"
    echo "      Response: $(echo "$GATEWAY_TRUST" | head -n -1)"
fi

# Test Gateway ContextGuard endpoint
echo "7️⃣  Testing Gateway -> ContextGuard routing..."
GATEWAY_CONTEXT=$(curl -s -w "\n%{http_code}" -X POST "${GATEWAY}/api/v1/guards/process" \
    -H "Content-Type: application/json" \
    -d '{"service_type": "contextguard", "payload": {"current_code": "test", "previous_code": "test"}}' 2>&1)
GATEWAY_CONTEXT_STATUS=$(echo "$GATEWAY_CONTEXT" | tail -n1)
if [ "$GATEWAY_CONTEXT_STATUS" = "200" ]; then
    echo "   ✅ Gateway -> ContextGuard: OK (200)"
else
    echo "   ⚠️  Gateway -> ContextGuard: HTTP $GATEWAY_CONTEXT_STATUS"
    echo "      Response: $(echo "$GATEWAY_CONTEXT" | head -n -1)"
fi

echo ""
echo "✅ Quick test complete!"

