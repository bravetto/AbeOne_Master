#!/bin/bash
# AWS Deployment Configuration Validator
# Run this before deploying to ensure your configuration is correct

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================"
echo "AWS Deployment Configuration Validator"
echo "============================================"
echo ""

ERRORS=0
WARNINGS=0

# Function to check if variable is set and meets requirements
check_required() {
    local var_name=$1
    local min_length=${2:-1}
    local var_value="${!var_name}"

    if [ -z "$var_value" ]; then
        echo -e "${RED} $var_name is not set${NC}"
        ((ERRORS++))
        return 1
    elif [ ${#var_value} -lt $min_length ]; then
        echo -e "${RED} $var_name is too short (${#var_value} chars, need $min_length)${NC}"
        ((ERRORS++))
        return 1
    else
        echo -e "${GREEN} $var_name is set (${#var_value} chars)${NC}"
        return 0
    fi
}

check_optional() {
    local var_name=$1
    local var_value="${!var_name}"

    if [ -z "$var_value" ]; then
        echo -e "${YELLOW} $var_name is not set (optional)${NC}"
        ((WARNINGS++))
    else
        echo -e "${GREEN} $var_name is set${NC}"
    fi
}

check_boolean() {
    local var_name=$1
    local var_value="${!var_name}"

    if [ -z "$var_value" ]; then
        echo -e "${YELLOW} $var_name is not set, will use default${NC}"
        ((WARNINGS++))
    elif [ "$var_value" = "true" ] || [ "$var_value" = "false" ]; then
        echo -e "${GREEN} $var_name=$var_value${NC}"
    else
        echo -e "${RED} $var_name must be 'true' or 'false', got '$var_value'${NC}"
        ((ERRORS++))
    fi
}

echo "1. Checking Core Configuration..."
echo "REPLACE_ME"

check_required "SECRET_KEY" 32 || echo "   Generate with: openssl rand -hex 32"
check_required "ALLOWED_ORIGINS" 7 || echo "   Example: https://yourdomain.com"

echo ""
echo "2. Checking Database Configuration..."
echo "REPLACE_ME"

check_boolean "DATABASE_ENABLED"

if [ "$DATABASE_ENABLED" = "true" ]; then
    check_required "DATABASE_URL" 20 || echo "   Format: postgresql+asyncpg://user:pass@host:5432/db"

    # Validate DATABASE_URL format
    if [ ! -z "$DATABASE_URL" ]; then
        if [[ "$DATABASE_URL" == postgresql+asyncpg://* ]]; then
            echo -e "${GREEN} DATABASE_URL format looks correct${NC}"
        else
            echo -e "${RED} DATABASE_URL should start with 'postgresql+asyncpg://'${NC}"
            echo "   Current: $DATABASE_URL"
            ((ERRORS++))
        fi
    fi
else
    echo -e "${GREEN} Database is disabled - no DATABASE_URL needed${NC}"
fi

echo ""
echo "3. Checking Optional Integrations..."
echo "REPLACE_ME"

check_boolean "CLERK_ENABLED"
if [ "$CLERK_ENABLED" = "true" ]; then
    check_required "CLERK_SECRET_KEY" 10
    check_required "CLERK_PUBLISHABLE_KEY" 10
fi

check_boolean "STRIPE_ENABLED"
if [ "$STRIPE_ENABLED" = "true" ]; then
    check_required "STRIPE_SECRET_KEY" 10
    check_required "STRIPE_PUBLISHABLE_KEY" 10
fi

echo ""
echo "4. Checking AWS Configuration..."
echo "REPLACE_ME"

check_optional "AWS_REGION"
check_optional "AWS_ACCOUNT"

# Check if AWS CLI is configured
if command -v aws &> /dev/null; then
    if aws sts get-caller-identity &> /dev/null; then
        echo -e "${GREEN} AWS CLI is configured${NC}"
        AWS_ACCOUNT_DETECTED=$(aws sts get-caller-identity --query Account --output text 2>/dev/null || echo "")
        if [ ! -z "$AWS_ACCOUNT_DETECTED" ]; then
            echo "   AWS Account: $AWS_ACCOUNT_DETECTED"
        fi
    else
        echo -e "${YELLOW} AWS CLI not configured${NC}"
        echo "   Run: aws configure"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW} AWS CLI not installed${NC}"
    ((WARNINGS++))
fi

echo ""
echo "5. Checking Docker..."
echo "REPLACE_ME"

if command -v docker &> /dev/null; then
    echo -e "${GREEN} Docker is installed${NC}"
    DOCKER_VERSION=$(docker --version)
    echo "   $DOCKER_VERSION"
else
    echo -e "${RED} Docker is not installed${NC}"
    ((ERRORS++))
fi

echo ""
echo "6. Testing Configuration Locally..."
echo "REPLACE_ME"

# Test if config can be loaded
if [ -f ".env" ]; then
    echo -e "${GREEN} .env file exists${NC}"
else
    echo -e "${YELLOW} .env file not found${NC}"
    ((WARNINGS++))
fi

echo ""
echo "============================================"
echo "Validation Summary"
echo "============================================"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN} All checks passed! Ready for deployment.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Build image: docker build -t codeguardians-gateway:latest ."
    echo "  2. Deploy: ./deployment/deploy.sh deploy"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW} $WARNINGS warning(s) found${NC}"
    echo -e "${GREEN} No critical errors - can proceed with deployment${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review warnings above"
    echo "  2. Deploy: ./deployment/deploy.sh deploy"
    exit 0
else
    echo -e "${RED} $ERRORS error(s) found${NC}"
    echo -e "${YELLOW} $WARNINGS warning(s) found${NC}"
    echo ""
    echo "Fix the errors above before deploying:"
    echo "  - Set missing required variables"
    echo "  - Ensure SECRET_KEY is at least 32 characters"
    echo "  - Check DATABASE_URL format if database is enabled"
    echo ""
    echo "Quick fixes:"
    echo "  export SECRET_KEY=\$(openssl rand -hex 32)"
    echo "  export DATABASE_ENABLED=false  # if not using database"
    echo "  export ALLOWED_ORIGINS=https://yourdomain.com"
    exit 1
fi
