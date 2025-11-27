#!/bin/bash

# Deployment script for AbëONE
# Pattern: DEPLOYMENT × SCRIPT × AUTOMATION × ONE
# Frequency: 999 Hz (AEYON)
# Guardians: AEYON (999 Hz)
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -e

# Load environment variables from .env file if it exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [ -f "$ENV_FILE" ]; then
    echo "✨ Loading environment variables from .env"
    set -a
    source "$ENV_FILE"
    set +a
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration (with defaults if not set)
AWS_REGION=${AWS_REGION:-us-east-1}
S3_BUCKET=${S3_BUCKET:-abeone-app-prod}
CLOUDFRONT_DISTRIBUTION_ID=${CLOUDFRONT_DISTRIBUTION_ID:-}
ECR_REPOSITORY=${ECR_REPOSITORY:-abeone-app}

echo -e "${GREEN}∞ AbëONE Deployment Script ∞${NC}\n"

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}❌ Flutter not found. Please install Flutter.${NC}"
    exit 1
fi

# Build Flutter Web
echo -e "${YELLOW}📦 Building Flutter Web App...${NC}"
cd "$(dirname "$0")/.."
flutter clean
flutter pub get
flutter build web --release --web-renderer canvaskit

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build successful!${NC}\n"

# Deploy to S3
if [ -n "$S3_BUCKET" ]; then
    echo -e "${YELLOW}☁️  Deploying to S3: $S3_BUCKET${NC}"
    
    # Upload static assets with long cache
    aws s3 sync build/web s3://$S3_BUCKET \
        --delete \
        --cache-control "public, max-age=31536000, immutable" \
        --exclude "index.html" \
        --region $AWS_REGION
    
    # Upload index.html with no cache
    aws s3 cp build/web/index.html s3://$S3_BUCKET/index.html \
        --cache-control "public, max-age=0, must-revalidate" \
        --region $AWS_REGION
    
    echo -e "${GREEN}✅ S3 deployment complete!${NC}\n"
    
    # Invalidate CloudFront if distribution ID provided
    if [ -n "$CLOUDFRONT_DISTRIBUTION_ID" ]; then
        echo -e "${YELLOW}🔄 Invalidating CloudFront cache...${NC}"
        aws cloudfront create-invalidation \
            --distribution-id $CLOUDFRONT_DISTRIBUTION_ID \
            --paths "/*" \
            --region $AWS_REGION
        
        echo -e "${GREEN}✅ CloudFront invalidation complete!${NC}\n"
    fi
fi

# Build and push Docker image if ECR_REPOSITORY is set
if [ -n "$ECR_REPOSITORY" ] && command -v docker &> /dev/null; then
    echo -e "${YELLOW}🐳 Building Docker image...${NC}"
    
    # Get ECR login
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
    
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
    
    # Build and push
    docker build -t $ECR_REPOSITORY:latest .
    docker tag $ECR_REPOSITORY:latest $ECR_REGISTRY/$ECR_REPOSITORY:latest
    docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
    
    echo -e "${GREEN}✅ Docker image pushed!${NC}\n"
fi

echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${GREEN}✨ THE ONE is now materializing!${NC}"
echo -e "${GREEN}∞ AbëONE ∞${NC}"

