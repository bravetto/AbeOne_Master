#!/bin/bash

# TokenGuard Deployment Script
# This script builds and deploys the TokenGuard service

set -e

echo " Starting TokenGuard deployment..."

# Configuration
IMAGE_NAME="tokenguard"
TAG="latest"
NAMESPACE="default"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    print_warning "kubectl not found. Skipping Kubernetes deployment."
    K8S_DEPLOY=false
else
    K8S_DEPLOY=true
fi

# Build Docker image
print_status "Building Docker image: ${IMAGE_NAME}:${TAG}"
docker build -t ${IMAGE_NAME}:${TAG} .

if [ $? -eq 0 ]; then
    print_status "Docker image built successfully"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Test the image
print_status "Testing Docker image..."
docker run --rm -d --name tokenguard-test -p 8000:8000 ${IMAGE_NAME}:${TAG}

# Wait for service to start
sleep 5

# Test health endpoint
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "Health check passed"
else
    print_warning "Health check failed, but continuing..."
fi

# Stop test container
docker stop tokenguard-test

# Deploy to Kubernetes if available
if [ "$K8S_DEPLOY" = true ]; then
    print_status "Deploying to Kubernetes..."
    
    # Check if namespace exists
    if ! kubectl get namespace ${NAMESPACE} > /dev/null 2>&1; then
        print_status "Creating namespace: ${NAMESPACE}"
        kubectl create namespace ${NAMESPACE}
    fi
    
    # Apply Kubernetes manifests
    if [ -d "k8s" ]; then
        kubectl apply -f k8s/ -n ${NAMESPACE}
        print_status "Kubernetes deployment completed"
        
        # Wait for deployment to be ready
        print_status "Waiting for deployment to be ready..."
        kubectl wait --for=condition=available --timeout=300s deployment/tokenguard -n ${NAMESPACE}
        
        # Show deployment status
        print_status "Deployment status:"
        kubectl get pods -l app=tokenguard -n ${NAMESPACE}
        kubectl get services -l app=tokenguard -n ${NAMESPACE}
    else
        print_warning "k8s directory not found. Skipping Kubernetes deployment."
    fi
else
    print_warning "Kubernetes deployment skipped (kubectl not available)"
fi

# Run tests
print_status "Running tests..."
if [ -d "tests" ]; then
    # Run tests in container
    docker run --rm ${IMAGE_NAME}:${TAG} python -m pytest tests/ -v
    if [ $? -eq 0 ]; then
        print_status "All tests passed"
    else
        print_warning "Some tests failed"
    fi
else
    print_warning "Tests directory not found"
fi

print_status "TokenGuard deployment completed successfully! "

# Show useful commands
echo ""
echo "Useful commands:"
echo "  View logs: kubectl logs -l app=tokenguard -n ${NAMESPACE}"
echo "  Scale deployment: kubectl scale deployment tokenguard --replicas=3 -n ${NAMESPACE}"
echo "  Port forward: kubectl port-forward service/tokenguard 8000:80 -n ${NAMESPACE}"
echo "  Access API: http://localhost:8000/docs"
