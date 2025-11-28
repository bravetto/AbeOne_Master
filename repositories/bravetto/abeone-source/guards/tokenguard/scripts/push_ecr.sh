#!/bin/bash
set -e

# Configuration
TAG="dev"
REGION="us-east-1"
ACCOUNT_ID="730335329303"
AWS_PROFILE="jimmyaws"

export AWS_PROFILE

ECR_BASE="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

# Define the 6 core service images to push (Gateway + 5 Guards)
REPOS=(
    "gateway"
    "tokenguard" 
    "trustguard"
    "contextguard"
    "biasguard"
    "healthguard"
)

echo "Found ${#REPOS[@]} image(s) to push: ${REPOS[*]}"
echo ""

# Authenticate with ECR
echo "Authenticating with ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_BASE

echo ""
echo "Building all images with docker-compose for AMD-64 (AWS)..."
# CRITICAL: Mac defaults to ARM-64, but AWS requires AMD-64
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose build
echo " All images built successfully for AMD-64"
echo ""

# Create repositories and push images
for repo in "${REPOS[@]}"; do
    local_image="${repo}:${TAG}"
    ecr_image="${ECR_BASE}/${repo}:${TAG}"
    
    echo "Processing: $repo"
    
    # Create ECR repository if it doesn't exist
    aws ecr describe-repositories --repository-names $repo --region $REGION > /dev/null 2>&1 || \
        aws ecr create-repository --repository-name $repo --region $REGION --image-scanning-configuration scanOnPush=true > /dev/null 2>&1
    
    # Tag image for ECR
    echo "Tagging $local_image -> $ecr_image"
    docker tag $local_image $ecr_image
    
    # Push to ECR
    echo "Pushing to ECR..."
    docker push $ecr_image
    echo " Pushed: $ecr_image"
    echo ""
done

echo " All images pushed to ECR!"
