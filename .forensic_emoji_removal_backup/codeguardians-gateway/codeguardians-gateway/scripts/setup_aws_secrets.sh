#!/bin/bash
# CodeGuardians Gateway - AWS Secrets Manager Setup Script
# This script creates and manages secrets in AWS Secrets Manager for production deployment

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
DEFAULT_REGION="us-east-1"
DEFAULT_SECRET_NAME="codeguardians-gateway/production"
DEFAULT_ACCOUNT_ID=""

# Parse command line arguments
REGION=${1:-$DEFAULT_REGION}
SECRET_NAME=${2:-$DEFAULT_SECRET_NAME}
ACCOUNT_ID=${3:-$DEFAULT_ACCOUNT_ID}

log "🔐 CodeGuardians Gateway - AWS Secrets Manager Setup"
log "====================================================="

# Check if AWS CLI is available
log "🔍 Checking AWS CLI..."
if ! command -v aws &> /dev/null; then
    error "AWS CLI not found. Please install AWS CLI first."
    exit 1
fi
success "AWS CLI found"

# Check AWS credentials
log "🔍 Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    error "AWS credentials not configured. Run 'aws configure' first."
    exit 1
fi

# Get current AWS account ID if not provided
if [ -z "$ACCOUNT_ID" ]; then
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
fi

success "AWS credentials configured (Account: $ACCOUNT_ID)"

log "📝 Configuration:"
log "   Region: $REGION"
log "   Secret Name: $SECRET_NAME"
log "   Account ID: $ACCOUNT_ID"

# Function to create or update secret
create_or_update_secret() {
    local secret_name=$1
    local secret_data=$2
    local description=$3
    
    log "📝 Creating/updating secret: $secret_name"
    
    # Check if secret exists
    if aws secretsmanager describe-secret --secret-id "$secret_name" --region "$REGION" &> /dev/null; then
        log "   Secret exists, updating..."
        aws secretsmanager update-secret \
            --secret-id "$secret_name" \
            --secret-string "$secret_data" \
            --description "$description" \
            --region "$REGION"
        success "Secret updated: $secret_name"
    else
        log "   Secret does not exist, creating..."
        aws secretsmanager create-secret \
            --name "$secret_name" \
            --secret-string "$secret_data" \
            --description "$description" \
            --region "$REGION"
        success "Secret created: $secret_name"
    fi
}

# Create main application secrets
log "📝 Creating main application secrets..."

# Required secrets structure
SECRETS_DATA=$(cat <<EOF
{
  "SECRET_KEY": "CHANGE-THIS-TO-A-SECURE-64-CHARACTER-RANDOM-STRING-FOR-PRODUCTION",
  "POSTGRES_PASSWORD": "CHANGE-THIS-TO-A-SECURE-DATABASE-PASSWORD",
  "REDIS_PASSWORD": "CHANGE-THIS-TO-A-SECURE-REDIS-PASSWORD",
  "DATABASE_URL": "postgresql+asyncpg://neondb_owner:npg_quEClk7QZG5v@ep-shiny-dew-afsoljvy-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
  "REDIS_URL": "redis://:CHANGE-THIS-PASSWORD@your-elasticache-endpoint:6379/0",
  "ENVIRONMENT": "production",
  "LOG_LEVEL": "INFO",
  "DEBUG": "false",
  "ALLOWED_ORIGINS": "https://your-frontend-domain.com",
  "ALLOWED_HOSTS": "your-alb-dns-name,localhost"
}
EOF
)

create_or_update_secret \
    "$SECRET_NAME" \
    "$SECRETS_DATA" \
    "Main application secrets for CodeGuardians Gateway"

# Create database secrets (separate secret for database credentials)
log "📝 Creating database secrets..."

DB_SECRETS_DATA=$(cat <<EOF
{
  "username": "codeguardians-gateway",
  "password": "CHANGE-THIS-TO-A-SECURE-DATABASE-PASSWORD",
  "host": "your-rds-endpoint.amazonaws.com",
  "port": "5432",
  "database": "codeguardians_gateway_db",
  "engine": "postgres"
}
EOF
)

create_or_update_secret \
    "${SECRET_NAME}/database" \
    "$DB_SECRETS_DATA" \
    "Database credentials for CodeGuardians Gateway"

# Create Redis secrets (separate secret for Redis credentials)
log "📝 Creating Redis secrets..."

REDIS_SECRETS_DATA=$(cat <<EOF
{
  "host": "your-elasticache-endpoint.amazonaws.com",
  "port": "6379",
  "password": "CHANGE-THIS-TO-A-SECURE-REDIS-PASSWORD",
  "database": "0"
}
EOF
)

create_or_update_secret \
    "${SECRET_NAME}/redis" \
    "$REDIS_SECRETS_DATA" \
    "Redis credentials for CodeGuardians Gateway"

# Create optional secrets (Clerk, Stripe, etc.)
log "📝 Creating optional secrets..."

OPTIONAL_SECRETS_DATA=$(cat <<EOF
{
  "CLERK_SECRET_KEY": "CHANGE-THIS-TO-YOUR-CLERK-SECRET-KEY-IF-USING-CLERK",
  "CLERK_PUBLISHABLE_KEY": "CHANGE-THIS-TO-YOUR-CLERK-PUBLISHABLE-KEY-IF-USING-CLERK",
  "STRIPE_SECRET_KEY": "CHANGE-THIS-TO-YOUR-STRIPE-SECRET-KEY-IF-USING-STRIPE",
  "STRIPE_PUBLISHABLE_KEY": "CHANGE-THIS-TO-YOUR-STRIPE-PUBLISHABLE-KEY-IF-USING-STRIPE",
  "STRIPE_WEBHOOK_SECRET": "CHANGE-THIS-TO-YOUR-STRIPE-WEBHOOK-SECRET-IF-USING-STRIPE"
}
EOF
)

create_or_update_secret \
    "${SECRET_NAME}/optional" \
    "$OPTIONAL_SECRETS_DATA" \
    "Optional service secrets for CodeGuardians Gateway"

# List created secrets
log "📋 Created secrets:"
aws secretsmanager list-secrets \
    --query "SecretList[?contains(Name, 'codeguardians-gateway')].{Name:Name,Description:Description}" \
    --output table \
    --region "$REGION"

# Generate IAM policy for ECS task role
log "📝 Generating IAM policy for ECS task role..."

IAM_POLICY=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:${REGION}:${ACCOUNT_ID}:secret:${SECRET_NAME}*",
        "arn:aws:secretsmanager:${REGION}:${ACCOUNT_ID}:secret:${SECRET_NAME}/database*",
        "arn:aws:secretsmanager:${REGION}:${ACCOUNT_ID}:secret:${SECRET_NAME}/redis*",
        "arn:aws:secretsmanager:${REGION}:${ACCOUNT_ID}:secret:${SECRET_NAME}/optional*"
      ]
    }
  ]
}
EOF
)

# Save IAM policy to file
echo "$IAM_POLICY" > /tmp/codeguardians-gateway-iam-policy.json

log "📄 IAM Policy saved to: /tmp/codeguardians-gateway-iam-policy.json"
log "   Use this policy for your ECS task role"

# Display secret ARNs for Terraform/CloudFormation
log "🔗 Secret ARNs for infrastructure:"
echo "Main Secret ARN:"
aws secretsmanager describe-secret --secret-id "$SECRET_NAME" --region "$REGION" --query ARN --output text

echo "Database Secret ARN:"
aws secretsmanager describe-secret --secret-id "${SECRET_NAME}/database" --region "$REGION" --query ARN --output text

echo "Redis Secret ARN:"
aws secretsmanager describe-secret --secret-id "${SECRET_NAME}/redis" --region "$REGION" --query ARN --output text

echo "Optional Secret ARN:"
aws secretsmanager describe-secret --secret-id "${SECRET_NAME}/optional" --region "$REGION" --query ARN --output text

success "🎉 AWS Secrets Manager setup complete!"

log "📝 Next steps:"
log "1. Update the secret values with your actual credentials"
log "2. Create ECS task definition with the secret ARNs"
log "3. Deploy your application to ECS"
log "4. Use the IAM policy for your ECS task role"

log "🔧 To update secret values:"
log "aws secretsmanager update-secret --secret-id '$SECRET_NAME' --secret-string '{\"SECRET_KEY\": \"your-actual-secret\"}' --region $REGION"

log "📚 For Terraform/CloudFormation:"
log "   Use the ARNs above in your infrastructure code"
log "   Attach the IAM policy to your ECS task role"

warning "⚠️  IMPORTANT: Update all placeholder values with actual secure credentials before production deployment!"
