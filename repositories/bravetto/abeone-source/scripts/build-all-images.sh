#!/usr/bin/env bash
# Build script for all AIGuards Backend containers
# Builds all images individually before orchestration

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_TAG="${IMAGE_TAG:-dev}"
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Service definitions
SERVICES=(
    "gateway:./codeguardians-gateway/codeguardians-gateway:Dockerfile"
    "tokenguard:./guards/tokenguard:Dockerfile"
    "trustguard:./guards/trust-guard:Dockerfile"
    "contextguard:./guards/contextguard:Dockerfile"
    "biasguard:./guards/biasguard-backend:Dockerfile"
    "healthguard:./guards/healthguard:Dockerfile"
)

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to build a single image
build_image() {
    local service_name=$1
    local build_context=$2
    local dockerfile=$3
    local image_name="aiguards-${service_name}:${IMAGE_TAG}"
    
    print_info "Building ${service_name}..."
    print_info "  Context: ${build_context}"
    print_info "  Dockerfile: ${dockerfile}"
    print_info "  Image: ${image_name}"
    
    # Check if context directory exists
    if [ ! -d "$build_context" ]; then
        print_error "Build context not found: ${build_context}"
        return 1
    fi
    
    # Check if Dockerfile exists
    if [ ! -f "${build_context}/${dockerfile}" ]; then
        print_error "Dockerfile not found: ${build_context}/${dockerfile}"
        return 1
    fi
    
    # Build the image
    if docker build \
        --tag "${image_name}" \
        --file "${build_context}/${dockerfile}" \
        --build-arg BUILD_DATE="${BUILD_DATE}" \
        --build-arg GIT_COMMIT="${GIT_COMMIT}" \
        --label "org.opencontainers.image.created=${BUILD_DATE}" \
        --label "org.opencontainers.image.revision=${GIT_COMMIT}" \
        --label "org.opencontainers.image.version=${IMAGE_TAG}" \
        "${build_context}"; then
        print_success "Successfully built ${image_name}"
        
        # Show image size
        local image_size=$(docker images "${image_name}" --format "{{.Size}}" | head -1)
        print_info "  Image size: ${image_size}"
        return 0
    else
        print_error "Failed to build ${image_name}"
        return 1
    fi
}

# Main build function
main() {
    print_info "=========================================="
    print_info "AIGuards Backend - Container Build Script"
    print_info "=========================================="
    print_info "Build Date: ${BUILD_DATE}"
    print_info "Git Commit: ${GIT_COMMIT}"
    print_info "Image Tag: ${IMAGE_TAG}"
    print_info ""
    
    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    
    # Count services
    local total_services=${#SERVICES[@]}
    local current=0
    local failed=0
    local successful=0
    
    # Build each service
    for service_config in "${SERVICES[@]}"; do
        current=$((current + 1))
        IFS=':' read -r service_name build_context dockerfile <<< "$service_config"
        
        print_info ""
        print_info "[${current}/${total_services}] Building ${service_name}..."
        
        if build_image "$service_name" "$build_context" "$dockerfile"; then
            successful=$((successful + 1))
        else
            failed=$((failed + 1))
            print_warning "Continuing with remaining builds..."
        fi
    done
    
    # Summary
    print_info ""
    print_info "=========================================="
    print_info "Build Summary"
    print_info "=========================================="
    print_info "Total services: ${total_services}"
    print_success "Successful: ${successful}"
    if [ $failed -gt 0 ]; then
        print_error "Failed: ${failed}"
    fi
    
    # List built images
    print_info ""
    print_info "Built images:"
    docker images "aiguards-*:${IMAGE_TAG}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    if [ $failed -gt 0 ]; then
        print_error ""
        print_error "Some builds failed. Please check the errors above."
        exit 1
    else
        print_success ""
        print_success "All images built successfully!"
        print_info ""
        print_info "Next steps:"
        print_info "  1. Run 'docker-compose up -d' to start all services"
        print_info "  2. Check status with 'docker-compose ps'"
        print_info "  3. View logs with 'docker-compose logs -f'"
        exit 0
    fi
}

# Run main function
main "$@"

