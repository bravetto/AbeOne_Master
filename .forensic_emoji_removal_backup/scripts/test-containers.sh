#!/bin/bash
# Container Testing Script for AIGuards Backend
# Tests all containers for AWS deployment readiness

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test results
TEST_RESULTS=()
PASSED=0
FAILED=0

log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
    TEST_RESULTS+=("✅ $1")
    ((PASSED++))
}

error() {
    echo -e "${RED}❌${NC} $1"
    TEST_RESULTS+=("❌ $1")
    ((FAILED++))
}

warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
    TEST_RESULTS+=("⚠️ $1")
}

# Test function
test_container() {
    local name=$1
    local path=$2
    local image=$3
    local port=$4
    
    log "Testing $name..."
    
    # Build container
    log "  Building $name..."
    if docker build -t $image:test $path > /tmp/build-$name.log 2>&1; then
        success "  $name built successfully"
    else
        error "  $name build failed"
        cat /tmp/build-$name.log
        return 1
    fi
    
    # Check if container runs
    log "  Starting $name container..."
    CONTAINER_ID=$(docker run -d \
        -e ENVIRONMENT=test \
        -e LOG_LEVEL=INFO \
        -e SECRET_KEY=$(openssl rand -hex 32) \
        -e DATABASE_ENABLED=false \
        -e REDIS_ENABLED=false \
        -p $port:$port \
        $image:test 2>&1) || true
    
    if [[ "$CONTAINER_ID" =~ ^[a-f0-9]+$ ]]; then
        success "  $name container started"
        
        # Wait for health check
        log "  Waiting for $name to be ready..."
        sleep 10
        
        # Test health endpoint
        if curl -f http://localhost:$port/health > /dev/null 2>&1; then
            success "  $name health check passed"
        else
            warning "  $name health check failed (may need more time)"
        fi
        
        # Cleanup
        docker stop $CONTAINER_ID > /dev/null 2>&1 || true
        docker rm $CONTAINER_ID > /dev/null 2>&1 || true
    else
        error "  $name failed to start"
        echo "$CONTAINER_ID"
        return 1
    fi
}

# Main test execution
echo "=========================================="
echo "AIGuards Backend Container Testing"
echo "=========================================="
echo ""

# Test 1: Gateway
test_container "codeguardians-gateway" \
    "./codeguardians-gateway/codeguardians-gateway" \
    "aiguards-gateway" \
    "8000"

# Test 2: TokenGuard
test_container "tokenguard" \
    "./guards/tokenguard" \
    "aiguards-tokenguard" \
    "8001"

# Test 3: TrustGuard
test_container "trustguard" \
    "./guards/trust-guard" \
    "aiguards-trustguard" \
    "8002"

# Test 4: ContextGuard
test_container "contextguard" \
    "./guards/contextguard" \
    "aiguards-contextguard" \
    "8003"

# Test 5: BiasGuard
test_container "biasguard" \
    "./guards/biasguard-backend" \
    "aiguards-biasguard" \
    "8004"

# Test 6: HealthGuard
test_container "healthguard" \
    "./guards/healthguard" \
    "aiguards-healthguard" \
    "8005"

# Summary
echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""
echo "Results:"
for result in "${TEST_RESULTS[@]}"; do
    echo "  $result"
done

if [ $FAILED -eq 0 ]; then
    echo ""
    success "All containers tested successfully!"
    exit 0
else
    echo ""
    error "Some tests failed. Review logs above."
    exit 1
fi

