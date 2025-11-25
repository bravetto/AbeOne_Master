#!/bin/bash
# Setup AWS Credentials for MCP Server
# This script helps configure AWS credentials for the MCP server to use

set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "======================================"
echo "  AWS MCP Server Credentials Setup"
echo "======================================"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    error "AWS CLI is not installed!"
    echo ""
    echo "Install AWS CLI:"
    echo "  Windows: https://awscli.amazonaws.com/AWSCLIV2.msi"
    echo "  macOS:   brew install awscli"
    echo "  Linux:   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

success "AWS CLI is installed: $(aws --version)"
echo ""

# Check current configuration
log "Checking current AWS configuration..."
if aws configure list | grep -q "<not set>"; then
    warning "AWS credentials are not configured"
else
    success "AWS credentials are already configured"
    aws configure list
    echo ""
    read -p "Do you want to reconfigure? (y/N): " reconfigure
    if [[ ! "$reconfigure" =~ ^[Yy]$ ]]; then
        log "Skipping reconfiguration"
        exit 0
    fi
fi

echo ""
log "AWS credentials can be configured in two ways:"
echo ""
echo "1. Interactive Configuration (Recommended for development)"
echo "   - Uses 'aws configure' command"
echo "   - Stores credentials in ~/.aws/credentials"
echo ""
echo "2. Environment Variables (Recommended for CI/CD)"
echo "   - Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY"
echo "   - Temporary, not persisted"
echo ""

read -p "Choose method (1 or 2): " method

if [ "$method" = "1" ]; then
    log "Starting interactive AWS configuration..."
    echo ""
    echo "You will need:"
    echo "  - AWS Access Key ID"
    echo "  - AWS Secret Access Key"
    echo "  - Default region (e.g., us-east-1)"
    echo "  - Output format (default: json)"
    echo ""
    
    aws configure
    
    echo ""
    success "AWS configuration complete!"
    
elif [ "$method" = "2" ]; then
    log "Setting up environment variables..."
    echo ""
    
    read -p "Enter AWS Access Key ID: " aws_access_key_id
    read -sp "Enter AWS Secret Access Key: " aws_secret_access_key
    echo ""
    read -p "Enter AWS Region [us-east-1]: " aws_region
    aws_region=${aws_region:-us-east-1}
    
    # Export for current session
    export AWS_ACCESS_KEY_ID="$aws_access_key_id"
    export AWS_SECRET_ACCESS_KEY="$aws_secret_access_key"
    export AWS_REGION="$aws_region"
    
    # Create a .env file for future use
    cat > .cursor/.aws-env << EOF
# AWS Credentials for MCP Server
# Source this file: source .cursor/.aws-env
export AWS_ACCESS_KEY_ID="$aws_access_key_id"
export AWS_SECRET_ACCESS_KEY="$aws_secret_access_key"
export AWS_REGION="$aws_region"
EOF
    
    success "Environment variables set for current session"
    log "To persist for future sessions, source .cursor/.aws-env"
    
else
    error "Invalid option selected"
    exit 1
fi

echo ""
log "Validating AWS credentials..."
if aws sts get-caller-identity &> /dev/null; then
    success "AWS credentials are valid!"
    echo ""
    aws sts get-caller-identity
else
    error "AWS credentials validation failed!"
    exit 1
fi

echo ""
echo "======================================"
success "AWS MCP Server Setup Complete!"
echo "======================================"
echo ""
log "Next steps:"
echo "  1. Restart Cursor to load the MCP configuration"
echo "  2. Try asking: 'List my ECS clusters'"
echo "  3. See .cursor/aws-mcp-setup.md for more information"
echo ""


