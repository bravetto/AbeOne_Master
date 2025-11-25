#!/bin/bash
# Runtime Testing Script for AWS Secrets Manager Integration

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

# Configuration
TEST_MODE=${TEST_MODE:-"local"}  # local, docker, aws
AWS_SECRETS_ENABLED=${AWS_SECRETS_ENABLED:-true}
AWS_SECRETS_NAME=${AWS_SECRETS_NAME:-codeguardians-gateway/production}
AWS_REGION=${AWS_REGION:-us-east-1}

log " Starting Runtime Testing for AWS Secrets Manager Integration"
log "Test Mode: $TEST_MODE"
log "AWS Secrets Enabled: $AWS_SECRETS_ENABLED"

# Test 1: Environment Variables
test_environment_variables() {
    log " Testing Environment Variables..."
    
    echo "AWS_SECRETS_ENABLED: ${AWS_SECRETS_ENABLED}"
    echo "AWS_SECRETS_NAME: ${AWS_SECRETS_NAME}"
    echo "AWS_REGION: ${AWS_REGION}"
    echo "ENVIRONMENT: ${ENVIRONMENT:-not set}"
    echo "LOG_LEVEL: ${LOG_LEVEL:-not set}"
    
    success "Environment variables test completed"
}

# Test 2: AWS CLI and Credentials
test_aws_setup() {
    log " Testing AWS Setup..."
    
    # Check AWS CLI
    if command -v aws &> /dev/null; then
        success "AWS CLI available: $(aws --version)"
    else
        error "AWS CLI not found"
        return 1
    fi
    
    # Check AWS credentials
    if aws sts get-caller-identity &> /dev/null; then
        IDENTITY=$(aws sts get-caller-identity)
        success "AWS credentials valid"
        echo "Account: $(echo $IDENTITY | jq -r '.Account')"
        echo "Arn: $(echo $IDENTITY | jq -r '.Arn')"
    else
        error "AWS credentials not configured"
        return 1
    fi
}

# Test 3: AWS Secrets Manager Access
test_aws_secrets_access() {
    log " Testing AWS Secrets Manager Access..."
    
    if [ "$AWS_SECRETS_ENABLED" != "true" ]; then
        warning "AWS Secrets Manager disabled, skipping test"
        return 0
    fi
    
    # Check if secret exists
    if aws secretsmanager describe-secret --secret-id "$AWS_SECRETS_NAME" --region "$AWS_REGION" &> /dev/null; then
        success "Secret '$AWS_SECRETS_NAME' exists"
    else
        error "Secret '$AWS_SECRETS_NAME' not found"
        return 1
    fi
    
    # Test secret access
    log "Testing secret access..."
    if aws secretsmanager get-secret-value --secret-id "$AWS_SECRETS_NAME" --region "$AWS_REGION" &> /dev/null; then
        success "Secret access successful"
        
        # Parse and validate secret content
        SECRET_DATA=$(aws secretsmanager get-secret-value --secret-id "$AWS_SECRETS_NAME" --region "$AWS_REGION" --query SecretString --output text)
        
        if [ -n "$SECRET_DATA" ]; then
            # Check for required secrets
            REQUIRED_SECRETS=("SECRET_KEY" "DATABASE_URL" "REDIS_URL")
            MISSING_SECRETS=()
            
            for secret in "${REQUIRED_SECRETS[@]}"; do
                if ! echo "$SECRET_DATA" | jq -e ".$secret" &> /dev/null; then
                    MISSING_SECRETS+=("$secret")
                fi
            done
            
            if [ ${#MISSING_SECRETS[@]} -eq 0 ]; then
                success "All required secrets present"
            else
                error "Missing required secrets: ${MISSING_SECRETS[*]}"
                return 1
            fi
        else
            error "Secret data is empty"
            return 1
        fi
    else
        error "Failed to access secret"
        return 1
    fi
}

# Test 4: Python Dependencies
test_python_dependencies() {
    log " Testing Python Dependencies..."
    
    # Test boto3 import
    if python3 -c "import boto3; print('boto3 version:', boto3.__version__)" 2>/dev/null; then
        success "boto3 available"
    else
        error "boto3 not available"
        return 1
    fi
    
    # Test other required modules
    REQUIRED_MODULES=("fastapi" "uvicorn" "pydantic" "httpx")
    for module in "${REQUIRED_MODULES[@]}"; do
        if python3 -c "import $module" 2>/dev/null; then
            success "$module available"
        else
            error "$module not available"
            return 1
        fi
    done
}

# Test 5: Application Configuration Loading
test_app_config_loading() {
    log " Testing Application Configuration Loading..."
    
    # Test configuration loading
    if python3 -c "
import sys
sys.path.insert(0, '/app')
from app.core.config import get_settings
settings = get_settings()
print('AWS Secrets Enabled:', getattr(settings, 'AWS_SECRETS_ENABLED', False))
print('Secret Key Length:', len(getattr(settings, 'SECRET_KEY', '')))
print('Database URL Present:', bool(getattr(settings, 'DATABASE_URL', '')))
print('Redis URL Present:', bool(getattr(settings, 'REDIS_URL', '')))
" 2>/dev/null; then
        success "Application configuration loaded successfully"
    else
        error "Application configuration loading failed"
        return 1
    fi
}

# Test 6: Docker Container Startup
test_docker_startup() {
    log " Testing Docker Container Startup..."
    
    # Build the image
    log "Building Docker image..."
    if docker build -t codeguardians-gateway-test . &> /dev/null; then
        success "Docker image built successfully"
    else
        error "Docker image build failed"
        return 1
    fi
    
    # Test container startup with AWS secrets
    log "Testing container startup with AWS secrets..."
    CONTAINER_ID=$(docker run -d \
        -e AWS_SECRETS_ENABLED=true \
        -e AWS_SECRETS_NAME="$AWS_SECRETS_NAME" \
        -e AWS_REGION="$AWS_REGION" \
        -v ~/.aws:/root/.aws:ro \
        codeguardians-gateway-test)
    
    if [ -n "$CONTAINER_ID" ]; then
        success "Container started: $CONTAINER_ID"
        
        # Wait for container to initialize
        log "Waiting for container to initialize..."
        sleep 10
        
        # Check container logs
        log "Checking container logs..."
        docker logs "$CONTAINER_ID" | grep -i "secrets" || warning "No secrets-related logs found"
        
        # Test health endpoint
        log "Testing health endpoint..."
        if docker exec "$CONTAINER_ID" curl -f http://localhost:8000/health/live &> /dev/null; then
            success "Health endpoint responding"
        else
            warning "Health endpoint not responding"
        fi
        
        # Clean up
        docker stop "$CONTAINER_ID" &> /dev/null
        docker rm "$CONTAINER_ID" &> /dev/null
        success "Container cleaned up"
    else
        error "Failed to start container"
        return 1
    fi
}

# Test 7: Docker Compose Integration
test_docker_compose() {
    log " Testing Docker Compose Integration..."
    
    # Test docker-compose configuration
    if docker-compose config &> /dev/null; then
        success "Docker Compose configuration valid"
    else
        error "Docker Compose configuration invalid"
        return 1
    fi
    
    # Test environment variable substitution
    if docker-compose config | grep -q "AWS_SECRETS_ENABLED"; then
        success "AWS secrets configuration present in docker-compose"
    else
        warning "AWS secrets configuration not found in docker-compose"
    fi
}

# Test 8: API Endpoint Testing
test_api_endpoints() {
    log " Testing API Endpoints..."
    
    # Start services
    log "Starting services with docker-compose..."
    docker-compose up -d &> /dev/null
    
    # Wait for services to start
    log "Waiting for services to start..."
    sleep 30
    
    # Test health endpoints
    if curl -f http://localhost:8000/health/live &> /dev/null; then
        success "Gateway health endpoint responding"
    else
        error "Gateway health endpoint not responding"
    fi
    
    if curl -f http://localhost:8000/health/ready &> /dev/null; then
        success "Gateway readiness endpoint responding"
    else
        error "Gateway readiness endpoint not responding"
    fi
    
    # Test API endpoint
    log "Testing unified guards API endpoint..."
    if curl -X POST http://localhost:8000/api/v1/guards/process \
        -H "Content-Type: application/json" \
        -d '{"text": "test input", "service_type": "tokenguard"}' \
        &> /dev/null; then
        success "API endpoint responding"
    else
        warning "API endpoint not responding (guards may not be running)"
    fi
    
    # Clean up
    log "Cleaning up services..."
    docker-compose down &> /dev/null
    success "Services cleaned up"
}

# Test 9: Performance Testing
test_performance() {
    log " Testing Performance..."
    
    # Test configuration loading time
    log "Testing configuration loading performance..."
    start_time=$(date +%s.%N)
    python3 -c "
import sys
sys.path.insert(0, '/app')
from app.core.config import get_settings
settings = get_settings()
" &> /dev/null
    end_time=$(date +%s.%N)
    config_time=$(echo "$end_time - $start_time" | bc)
    
    if (( $(echo "$config_time < 2.0" | bc -l) )); then
        success "Configuration loading time: ${config_time}s"
    else
        warning "Configuration loading time: ${config_time}s (slow)"
    fi
    
    # Test AWS secrets loading time
    if [ "$AWS_SECRETS_ENABLED" = "true" ]; then
        log "Testing AWS secrets loading performance..."
        start_time=$(date +%s.%N)
        aws secretsmanager get-secret-value --secret-id "$AWS_SECRETS_NAME" --region "$AWS_REGION" &> /dev/null
        end_time=$(date +%s.%N)
        secrets_time=$(echo "$end_time - $start_time" | bc)
        
        if (( $(echo "$secrets_time < 5.0" | bc -l) )); then
            success "AWS secrets loading time: ${secrets_time}s"
        else
            warning "AWS secrets loading time: ${secrets_time}s (slow)"
        fi
    fi
}

# Test 10: Telemetry and Logging
test_telemetry() {
    log " Testing Telemetry and Logging..."
    
    # Test structured logging
    if python3 -c "
import sys
sys.path.insert(0, '/app')
from app.utils.logging import get_logger
logger = get_logger('test')
logger.info('Test telemetry message')
" &> /dev/null; then
        success "Structured logging working"
    else
        error "Structured logging failed"
        return 1
    fi
    
    # Test log levels
    for level in "DEBUG" "INFO" "WARNING" "ERROR"; do
        if python3 -c "
import sys
sys.path.insert(0, '/app')
from app.utils.logging import get_logger
logger = get_logger('test')
logger.$level('Test $level message')
" &> /dev/null; then
            success "Log level $level working"
        else
            warning "Log level $level failed"
        fi
    done
}

# Main test runner
run_tests() {
    log " Starting Runtime Tests..."
    
    local tests_passed=0
    local tests_failed=0
    local total_tests=0
    
    # Define test functions
    local test_functions=(
        "test_environment_variables"
        "test_aws_setup"
        "test_aws_secrets_access"
        "test_python_dependencies"
        "test_app_config_loading"
        "test_docker_startup"
        "test_docker_compose"
        "test_api_endpoints"
        "test_performance"
        "test_telemetry"
    )
    
    # Run tests
    for test_func in "${test_functions[@]}"; do
        total_tests=$((total_tests + 1))
        log "Running test: $test_func"
        
        if $test_func; then
            tests_passed=$((tests_passed + 1))
        else
            tests_failed=$((tests_failed + 1))
        fi
        
        echo ""
    done
    
    # Generate summary
    log " Test Summary"
    log "==============="
    log "Total Tests: $total_tests"
    log "Passed: $tests_passed"
    log "Failed: $tests_failed"
    
    local success_rate=$((tests_passed * 100 / total_tests))
    log "Success Rate: ${success_rate}%"
    
    if [ $success_rate -ge 80 ]; then
        success " Runtime testing completed successfully!"
        return 0
    else
        error " Runtime testing failed!"
        return 1
    fi
}

# Run tests based on mode
case "$TEST_MODE" in
    "local")
        log "Running local tests..."
        test_environment_variables
        test_aws_setup
        test_aws_secrets_access
        test_python_dependencies
        test_app_config_loading
        test_performance
        test_telemetry
        ;;
    "docker")
        log "Running Docker tests..."
        test_environment_variables
        test_aws_setup
        test_aws_secrets_access
        test_python_dependencies
        test_docker_startup
        test_docker_compose
        test_performance
        ;;
    "full")
        log "Running full test suite..."
        run_tests
        ;;
    *)
        error "Invalid test mode: $TEST_MODE"
        error "Valid modes: local, docker, full"
        exit 1
        ;;
esac

success "Runtime testing completed!"

