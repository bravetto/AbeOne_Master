#!/bin/bash
# CodeGuardians Gateway - Configuration Test Script
# Validates the streamlined configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Test Docker configuration
test_docker_config() {
    log "Testing Docker configuration..."
    
    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        error "docker-compose.yml not found"
        return 1
    fi
    
    # Validate docker-compose.yml syntax
    if ! docker-compose config > /dev/null 2>&1; then
        error "docker-compose.yml has syntax errors"
        return 1
    fi
    
    success "Docker configuration is valid"
}

# Test environment configuration
test_env_config() {
    log "Testing environment configuration..."
    
    # Check if env.unified exists
    if [ ! -f "env.unified" ]; then
        error "env.unified not found"
        return 1
    fi
    
    # Load environment variables
    set -a
    source env.unified
    set +a
    
    # Check required variables
    local required_vars=("ENVIRONMENT" "SECRET_KEY" "POSTGRES_PASSWORD" "REDIS_PASSWORD")
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            error "Required environment variable $var is not set"
            return 1
        fi
    done
    
    success "Environment configuration is valid"
}

# Test startup script
test_startup_script() {
    log "Testing startup script..."
    
    # Check if start.sh exists
    if [ ! -f "start.sh" ]; then
        error "start.sh not found"
        return 1
    fi
    
    # Check if start.sh is executable
    if [ ! -x "start.sh" ]; then
        warning "start.sh is not executable, making it executable..."
        chmod +x start.sh
    fi
    
    # Test help command
    if ! ./start.sh help > /dev/null 2>&1; then
        error "start.sh help command failed"
        return 1
    fi
    
    success "Startup script is valid"
}

# Test Dockerfile
test_dockerfile() {
    log "Testing Dockerfile..."
    
    # Check if Dockerfile exists
    if [ ! -f "Dockerfile" ]; then
        error "Dockerfile not found"
        return 1
    fi
    
    # Check if Dockerfile has required stages
    if ! grep -q "FROM python:3.11-slim" Dockerfile; then
        error "Dockerfile missing Python base image"
        return 1
    fi
    
    if ! grep -q "FROM python:3.11-slim as production" Dockerfile; then
        error "Dockerfile missing production stage"
        return 1
    fi
    
    if ! grep -q "FROM python:3.11-slim as development" Dockerfile; then
        error "Dockerfile missing development stage"
        return 1
    fi
    
    success "Dockerfile is valid"
}

# Test requirements
test_requirements() {
    log "Testing requirements..."
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        error "requirements.txt not found"
        return 1
    fi
    
    # Check if requirements.txt has content
    if [ ! -s "requirements.txt" ]; then
        error "requirements.txt is empty"
        return 1
    fi
    
    success "Requirements are valid"
}

# Test main application
test_main_app() {
    log "Testing main application..."
    
    # Check if main.py exists
    if [ ! -f "app/main.py" ]; then
        error "app/main.py not found"
        return 1
    fi
    
    # Check if app directory exists
    if [ ! -d "app" ]; then
        error "app directory not found"
        return 1
    fi
    
    success "Main application is valid"
}

# Run all tests
run_tests() {
    log "Running configuration tests..."
    
    local tests=(
        "test_docker_config"
        "test_env_config"
        "test_startup_script"
        "test_dockerfile"
        "test_requirements"
        "test_main_app"
    )
    
    local passed=0
    local failed=0
    
    for test in "${tests[@]}"; do
        if $test; then
            ((passed++))
        else
            ((failed++))
        fi
    done
    
    log ""
    log "Test Results:"
    log "  Passed: $passed"
    log "  Failed: $failed"
    
    if [ $failed -eq 0 ]; then
        success "All tests passed! Configuration is valid."
        return 0
    else
        error "Some tests failed. Please fix the issues above."
        return 1
    fi
}

# Main function
main() {
    local command=${1:-test}
    
    case $command in
        test)
            run_tests
            ;;
        help|--help|-h)
            echo "CodeGuardians Gateway - Configuration Test Script"
            echo ""
            echo "Usage: $0 [COMMAND]"
            echo ""
            echo "Commands:"
            echo "  test                Run all tests"
            echo "  help                Show this help"
            echo ""
            echo "Tests:"
            echo "  - Docker configuration"
            echo "  - Environment configuration"
            echo "  - Startup script"
            echo "  - Dockerfile"
            echo "  - Requirements"
            echo "  - Main application"
            ;;
        *)
            error "Invalid command: $command"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
