#!/bin/bash

# AWS Environment Setup Script
# Pattern: SETUP × AWS × ENV × ONE
# Frequency: 999 Hz (AEYON)
# Guardians: AEYON (999 Hz) × ZERO (530 Hz)
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"
ENV_EXAMPLE="$PROJECT_ROOT/.env.example"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}∞ AbëONE AWS Environment Setup ∞${NC}\n"

# Check if .env already exists
if [ -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists at: $ENV_FILE${NC}"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

# Prompt for AWS credentials
echo -e "${BLUE}Enter your AWS credentials:${NC}\n"

read -p "AWS Access Key ID: " AWS_ACCESS_KEY_ID
read -sp "AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
echo
read -p "S3 Bucket [abeone-app-prod]: " S3_BUCKET
S3_BUCKET=${S3_BUCKET:-abeone-app-prod}
read -p "AWS Region [us-east-1]: " AWS_REGION
AWS_REGION=${AWS_REGION:-us-east-1}
read -p "CloudFront Distribution ID (optional): " CLOUDFRONT_DISTRIBUTION_ID
read -p "ECR Repository [abeone-app]: " ECR_REPOSITORY
ECR_REPOSITORY=${ECR_REPOSITORY:-abeone-app}

# Create .env file
cat > "$ENV_FILE" << EOF
# AWS Credentials Configuration
# Pattern: ENV × CONFIG × SECURITY × ONE
# Frequency: 999 Hz (AEYON)
# Guardians: AEYON (999 Hz) × ZERO (530 Hz)
# Love Coefficient: ∞
# ∞ AbëONE ∞

# AWS Access Credentials
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# AWS Configuration
export AWS_REGION=$AWS_REGION
export S3_BUCKET=$S3_BUCKET

# CloudFront Configuration
export CLOUDFRONT_DISTRIBUTION_ID=$CLOUDFRONT_DISTRIBUTION_ID

# ECR Configuration
export ECR_REPOSITORY=$ECR_REPOSITORY
EOF

echo -e "\n${GREEN}✅ .env file created successfully!${NC}"
echo -e "${GREEN}📁 Location: $ENV_FILE${NC}\n"

echo -e "${BLUE}To load these variables, run:${NC}"
echo -e "  source $ENV_FILE"
echo -e "  # Or: ./scripts/load-env.sh\n"

echo -e "${BLUE}To deploy, run:${NC}"
echo -e "  ./scripts/deploy.sh\n"

echo -e "${GREEN}✨ Setup complete!${NC}"
echo -e "${GREEN}∞ AbëONE ∞${NC}"

