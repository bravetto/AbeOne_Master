#!/bin/bash
# Environment Variable Validation Script
# Validates that all required environment variables are set and secure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track validation status
VALIDATION_FAILED=0
WARNINGS=0

echo " Starting environment variable validation..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED} Error: .env file not found!${NC}"
    echo "Please copy env.template to .env and configure it."
    exit 1
fi

# Source the .env file
set -a
source .env
set +a

# Function to check if variable is set
check_required() {
    local var_name=$1
    local var_value="${!var_name}"
    
    if [ -z "$var_value" ]; then
        echo -e "${RED} Required variable $var_name is not set${NC}"
        VALIDATION_FAILED=1
        return 1
    fi
    return 0
}

# Function to check if variable contains placeholder
check_placeholder() {
    local var_name=$1
    local var_value="${!var_name}"
    local placeholder=$2
    
    if [[ "$var_value" == *"$placeholder"* ]]; then
        echo -e "${YELLOW}  Warning: $var_name contains placeholder value ($placeholder)${NC}"
        WARNINGS=1
        return 1
    fi
    return 0
}

# Function to check minimum length
check_min_length() {
    local var_name=$1
    local var_value="${!var_name}"
    local min_length=$2
    
    if [ ${#var_value} -lt $min_length ]; then
        echo -e "${RED} $var_name must be at least $min_length characters long (current: ${#var_value})${NC}"
        VALIDATION_FAILED=1
        return 1
    fi
    return 0
}

# Function to check if DEBUG is false in production
check_debug_mode() {
    if [ "$ENVIRONMENT" = "production" ] && [ "$DEBUG" = "true" ]; then
        echo -e "${RED} DEBUG must be false in production environment!${NC}"
        VALIDATION_FAILED=1
        return 1
    fi
    return 0
}

# Function to check if password is in URL
check_password_in_url() {
    local var_name=$1
    local var_value="${!var_name}"
    
    # Check for common password patterns in URLs
    if [[ "$var_value" == *":password@"* ]] || [[ "$var_value" == *"password="* ]]; then
        echo -e "${YELLOW}  Warning: $var_name appears to contain password in URL${NC}"
        echo "   Consider using separate password variables instead"
        WARNINGS=1
    fi
}

# Core Required Variables
echo ""
echo " Checking core required variables..."
check_required "SECRET_KEY"
if check_required "SECRET_KEY"; then
    check_min_length "SECRET_KEY" 32
    check_placeholder "SECRET_KEY" "CHANGE-ME"
fi

check_required "ENVIRONMENT"
check_required "DATABASE_URL"

# Check DEBUG mode
if check_required "DEBUG"; then
    check_debug_mode
fi

# Database Variables
echo ""
echo " Checking database configuration..."
if [ "$DATABASE_ENABLED" = "true" ]; then
    check_password_in_url "DATABASE_URL"
    
    if [ -n "$DATABASE_PASSWORD" ]; then
        check_placeholder "DATABASE_PASSWORD" "CHANGE-ME"
    fi
    
    if [ -n "$POSTGRES_PASSWORD" ]; then
        check_placeholder "POSTGRES_PASSWORD" "CHANGE-ME"
    fi
fi

# Redis Variables
echo ""
echo " Checking Redis configuration..."
check_password_in_url "REDIS_URL"

if [ -n "$REDIS_PASSWORD" ]; then
    check_placeholder "REDIS_PASSWORD" "CHANGE-ME"
fi

# Production-specific checks
if [ "$ENVIRONMENT" = "production" ]; then
    echo ""
    echo " Checking production-specific security settings..."
    
    # Check AWS Secrets Manager
    if [ "$AWS_SECRETS_ENABLED" != "true" ]; then
        echo -e "${YELLOW}  Warning: AWS_SECRETS_ENABLED is not true in production${NC}"
        echo "   Consider using AWS Secrets Manager for production deployments"
        WARNINGS=1
    fi
    
    # Check for development keys
    if [[ "$SECRET_KEY" == *"development"* ]]; then
        echo -e "${RED} SECRET_KEY appears to be a development key in production!${NC}"
        VALIDATION_FAILED=1
    fi
    
    # Check CORS origins
    if [[ "$ALLOWED_ORIGINS" == *"localhost"* ]]; then
        echo -e "${YELLOW}  Warning: ALLOWED_ORIGINS includes localhost in production${NC}"
        WARNINGS=1
    fi
fi

# Optional service checks
echo ""
echo " Checking optional service configuration..."

if [ "$CLERK_ENABLED" = "true" ]; then
    check_required "CLERK_SECRET_KEY"
    check_required "CLERK_PUBLISHABLE_KEY"
    check_placeholder "CLERK_SECRET_KEY" "CHANGE-ME"
fi

if [ "$STRIPE_ENABLED" = "true" ]; then
    check_required "STRIPE_SECRET_KEY"
    check_required "STRIPE_PUBLISHABLE_KEY"
    check_placeholder "STRIPE_SECRET_KEY" "CHANGE-ME"
fi

if [ "$S3_ENABLED" = "true" ]; then
    check_required "S3_ACCESS_KEY_ID"
    check_required "S3_SECRET_ACCESS_KEY"
    check_placeholder "S3_ACCESS_KEY_ID" "CHANGE-ME"
fi

# Summary
echo ""
echo "================================"
if [ $VALIDATION_FAILED -eq 1 ]; then
    echo -e "${RED} Validation failed!${NC}"
    echo "Please fix the errors above before proceeding."
    exit 1
elif [ $WARNINGS -eq 1 ]; then
    echo -e "${YELLOW}  Validation completed with warnings${NC}"
    echo "Please review the warnings above."
    exit 0
else
    echo -e "${GREEN} All validations passed!${NC}"
    exit 0
fi


