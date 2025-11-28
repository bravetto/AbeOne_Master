#!/bin/bash
# Build Verification Script
# Validates Docker images before deployment

set -e

REGISTRY="${ECR_REGISTRY:-730335329303.dkr.ecr.us-east-1.amazonaws.com}"
REGION="${AWS_REGION:-us-east-1}"
TAG="${IMAGE_TAG:-dev}"

SERVICES=(
    "tokenguard"
    "trustguard"
    "contextguard"
    "biasguard"
    "healthguard"
    "codeguardians-gateway"
)

MAX_IMAGE_SIZE_MB=500
REQUIRED_PLATFORM="linux/amd64"

echo "🔍 Build Verification Script"
echo "Registry: $REGISTRY"
echo "Region: $REGION"
echo "Tag: $TAG"
echo ""

ERRORS=0
WARNINGS=0

# Function to check image exists locally
check_local_image() {
    local service=$1
    local image_name="${service}:${TAG}"
    
    if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${image_name}$"; then
        echo "✅ Local image found: $image_name"
        return 0
    else
        echo "❌ Local image not found: $image_name"
        return 1
    fi
}

# Function to check image size
check_image_size() {
    local service=$1
    local image_name="${service}:${TAG}"
    
    local size_mb=$(docker images --format "{{.Size}}" "$image_name" | sed 's/MB//' | sed 's/GB/*1024/' | bc)
    
    if (( $(echo "$size_mb > $MAX_IMAGE_SIZE_MB" | bc -l) )); then
        echo "⚠️  Image size exceeds limit: ${size_mb}MB > ${MAX_IMAGE_SIZE_MB}MB"
        ((WARNINGS++))
    else
        echo "✅ Image size OK: ${size_mb}MB"
    fi
}

# Function to check platform
check_platform() {
    local service=$1
    local image_name="${service}:${TAG}"
    
    local platform=$(docker inspect --format='{{.Architecture}}' "$image_name" 2>/dev/null || echo "unknown")
    
    if [ "$platform" != "amd64" ] && [ "$platform" != "linux/amd64" ]; then
        echo "⚠️  Platform may not be AMD-64: $platform"
        ((WARNINGS++))
    else
        echo "✅ Platform OK: $platform"
    fi
}

# Function to check health endpoint exists
check_health_endpoint() {
    local service=$1
    local image_name="${service}:${TAG}"
    
    # Check if Dockerfile has health check
    local dockerfile_path=""
    case $service in
        tokenguard)
            dockerfile_path="guards/tokenguard/Dockerfile"
            ;;
        trustguard)
            dockerfile_path="guards/trust-guard/Dockerfile"
            ;;
        contextguard)
            dockerfile_path="guards/contextguard/Dockerfile"
            ;;
        biasguard)
            dockerfile_path="guards/biasguard-backend/Dockerfile"
            ;;
        healthguard)
            dockerfile_path="guards/healthguard/Dockerfile"
            ;;
        codeguardians-gateway)
            dockerfile_path="codeguardians-gateway/codeguardians-gateway/Dockerfile"
            ;;
    esac
    
    if [ -f "$dockerfile_path" ] && grep -q "HEALTHCHECK" "$dockerfile_path"; then
        echo "✅ Health check configured"
    else
        echo "⚠️  Health check not found in Dockerfile"
        ((WARNINGS++))
    fi
}

# Function to check for secrets in image
check_secrets() {
    local service=$1
    local image_name="${service}:${TAG}"
    
    # Check for common secret patterns
    if docker run --rm "$image_name" env | grep -iE "(password|secret|key|token)" | grep -v "^PATH=" | grep -v "null"; then
        echo "⚠️  Potential secrets found in environment"
        ((WARNINGS++))
    else
        echo "✅ No obvious secrets in environment"
    fi
}

# Verify ECR access
echo "🔐 Verifying ECR access..."
if aws ecr describe-repositories --region "$REGION" --query "repositories[?repositoryName=='tokenguard']" --output text | grep -q tokenguard; then
    echo "✅ ECR access verified"
else
    echo "❌ ECR access failed"
    ((ERRORS++))
fi
echo ""

# Verify each service
for service in "${SERVICES[@]}"; do
    echo "📦 Verifying: $service"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Check local image
    if ! check_local_image "$service"; then
        ((ERRORS++))
        echo ""
        continue
    fi
    
    # Check image size
    check_image_size "$service"
    
    # Check platform
    check_platform "$service"
    
    # Check health endpoint
    check_health_endpoint "$service"
    
    # Check secrets
    check_secrets "$service"
    
    echo ""
done

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Verification Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ Build verification PASSED"
    exit 0
else
    echo "❌ Build verification FAILED"
    exit 1
fi

