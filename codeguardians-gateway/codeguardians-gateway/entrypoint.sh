#!/bin/bash
# CodeGuardians Gateway - Docker Entrypoint Script
# Fetches secrets from AWS Secrets Manager and starts the application

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

log " Starting CodeGuardians Gateway entrypoint..."

# Check if AWS Secrets Manager is enabled
# Default to false for local development, true for production
if [ "${AWS_SECRETS_ENABLED:-false}" = "true" ]; then
    log " AWS Secrets Manager integration enabled"
    
    # Check if AWS CLI is available
    if ! command -v aws &> /dev/null; then
        error "AWS CLI not found. Please install AWS CLI or set AWS_SECRETS_ENABLED=false"
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS credentials not configured. Please check IAM role or environment variables."
        exit 1
    fi
    
    # Set AWS region
    AWS_REGION=${AWS_REGION:-us-east-1}
    AWS_SECRETS_NAME=${AWS_SECRETS_NAME:-codeguardians-gateway/production}
    
    log " Fetching secrets from AWS Secrets Manager..."
    log "   Region: $AWS_REGION"
    log "   Secret Name: $AWS_SECRETS_NAME"
    
    # Fetch secrets from AWS Secrets Manager
    try_fetch_secrets() {
        local max_attempts=3
        local attempt=1
        
        while [ $attempt -le $max_attempts ]; do
            log "   Attempt $attempt/$max_attempts: Fetching secrets..."
            
            if aws secretsmanager get-secret-value \
                --secret-id "$AWS_SECRETS_NAME" \
                --region "$AWS_REGION" \
                --query SecretString \
                --output text > /tmp/secrets.json 2>/dev/null; then
                
                success "Secrets fetched successfully from AWS"
                return 0
            else
                warning "Failed to fetch secrets (attempt $attempt/$max_attempts)"
                sleep 2
                ((attempt++))
            fi
        done
        
        return 1
    }
    
    if try_fetch_secrets; then
        # Parse secrets and export as environment variables
        log " Processing secrets from AWS..."
        
        # Extract secrets from JSON and export as environment variables
        if command -v jq &> /dev/null; then
            # Use jq if available - AWS Secrets Manager returns a flat JSON object
            while IFS='=' read -r key value; do
                if [ -n "$key" ] && [ -n "$value" ]; then
                    # Remove quotes from value if present
                    value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//')
                    export "$key"="$value"
                    log "   Loaded: $key"
                fi
            done < <(jq -r 'to_entries[] | "\(.key)=\(.value)"' /tmp/secrets.json)
        else
            # Fallback: simple JSON parsing using Python
            python3 << 'PYTHON_SCRIPT' > /tmp/export_secrets.sh
import json
import os
import sys

try:
    with open('/tmp/secrets.json', 'r') as f:
        secrets = json.load(f)
    
    for key, value in secrets.items():
        if value is not None:
            # Escape value for shell
            value_str = str(value).replace('"', '\\"').replace('$', '\\$')
            print(f'export {key}="{value_str}"')
except Exception as e:
    print(f'Error parsing secrets: {e}', file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT
            
            if [ -f /tmp/export_secrets.sh ]; then
                source /tmp/export_secrets.sh
                log "   Secrets exported using Python fallback"
            else
                error "Failed to parse secrets from AWS"
                exit 1
            fi
        fi
        
        # Clean up temporary files
        rm -f /tmp/secrets.json /tmp/export_secrets.sh
        
        # Validate required secrets
        log " Validating required secrets..."
        REQUIRED_SECRETS=("SECRET_KEY" "POSTGRES_PASSWORD" "REDIS_PASSWORD" "DATABASE_URL" "REDIS_URL")
        MISSING_SECRETS=()
        
        for secret in "${REQUIRED_SECRETS[@]}"; do
            if [ -z "${!secret}" ]; then
                MISSING_SECRETS+=("$secret")
            fi
        done
        
        if [ ${#MISSING_SECRETS[@]} -ne 0 ]; then
            error "Missing required secrets from AWS: ${MISSING_SECRETS[*]}"
            exit 1
        fi
        
        success "All required secrets validated"
        
    else
        error "Failed to fetch secrets from AWS Secrets Manager after multiple attempts"
        error "Please check AWS credentials and secret permissions"
        exit 1
    fi
    
else
    log " AWS Secrets Manager disabled, using environment variables"
fi

# Validate SECRET_KEY length
if [ -z "${SECRET_KEY}" ]; then
    error "SECRET_KEY is not set. Please set SECRET_KEY environment variable."
    exit 1
fi

if [ ${#SECRET_KEY} -lt 32 ]; then
    error "SECRET_KEY must be at least 32 characters long for security"
    exit 1
fi

# Set production environment variables if not set
export ENVIRONMENT=${ENVIRONMENT:-production}
export DEBUG=${DEBUG:-false}
export LOG_LEVEL=${LOG_LEVEL:-INFO}

log " Environment configuration:"
log "   Environment: $ENVIRONMENT"
log "   Debug: $DEBUG"
log "   Log Level: $LOG_LEVEL"
log "   AWS Secrets: ${AWS_SECRETS_ENABLED:-true}"

# Start the application
log " Starting CodeGuardians Gateway application..."

# Execute the main application
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1 \
    --log-level info \
    --access-log \
    --no-use-colors
