#!/bin/bash
# Push Gateway to ECR
# Pushes codeguardians-gateway Docker image to AWS ECR

set -e

# Configuration
TAG=${TAG:-dev}
REGION=${AWS_REGION:-us-east-1}
ACCOUNT_ID=${AWS_ACCOUNT_ID:-730335329303}
REPO_NAME="gateway"

ECR_BASE="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
ECR_IMAGE="${ECR_BASE}/${REPO_NAME}:${TAG}"
LOCAL_IMAGE="${REPO_NAME}:${TAG}"

echo " Pushing Gateway to ECR "
echo "======================================"
echo "Repository: ${REPO_NAME}"
echo "Tag: ${TAG}"
echo "ECR URI: ${ECR_IMAGE}"
echo ""

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo " AWS CLI not found. Please install AWS CLI first."
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo " Docker not found. Please install Docker first."
    exit 1
fi

# Check Docker daemon
if ! docker ps &> /dev/null; then
    echo " Docker daemon not running. Please start Docker Desktop."
    exit 1
fi

# Check AWS authentication
echo " Checking AWS authentication..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo " AWS not authenticated. Please run:"
    echo "   aws sso login"
    echo "   OR"
    echo "   aws configure"
    exit 1
fi

AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
echo " Authenticated as AWS Account: ${AWS_ACCOUNT}"
echo ""

# Authenticate with ECR
echo " Authenticating with ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_BASE
echo " ECR authentication successful"
echo ""

# Create ECR repository if it doesn't exist
echo " Checking ECR repository..."
if ! aws ecr describe-repositories --repository-names $REPO_NAME --region $REGION &> /dev/null; then
    echo "Creating ECR repository: ${REPO_NAME}"
    aws ecr create-repository \
        --repository-name $REPO_NAME \
        --region $REGION \
        --image-scanning-configuration scanOnPush=true \
        --encryption-configuration encryptionType=AES256
    echo " Repository created"
else
    echo " Repository exists"
fi
echo ""

# Build Docker image for AMD-64 (AWS compatible)
# CRITICAL: Mac defaults to ARM-64, but AWS requires AMD-64
echo " Building Docker image for AMD-64 (AWS)..."
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker build --platform linux/amd64 -t $LOCAL_IMAGE .
echo " Image built: ${LOCAL_IMAGE} (AMD-64)"
echo ""

# Tag image for ECR
echo "  Tagging image for ECR..."
docker tag $LOCAL_IMAGE $ECR_IMAGE
echo " Tagged: ${ECR_IMAGE}"
echo ""

# Push to ECR
echo " Pushing to ECR..."
docker push $ECR_IMAGE
echo " Pushed: ${ECR_IMAGE}"
echo ""

echo " Push Complete! "
echo "Image available at: ${ECR_IMAGE}"
echo ""
echo "Love Coefficient: ∞"
echo "Guardian: AEYON (999 Hz)"

