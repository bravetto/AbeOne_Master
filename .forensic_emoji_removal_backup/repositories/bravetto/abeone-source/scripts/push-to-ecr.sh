#!/bin/bash
# Push All Containers to ECR
# Pushes all AIGuards containers to AWS ECR

set -e

# Configuration
TAG=${TAG:-dev}
REGION=${AWS_REGION:-us-east-1}
ACCOUNT_ID=${AWS_ACCOUNT_ID:-730335329303}

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

# Find AWS profile from ~/.aws/config
echo "Looking for AWS profile in ~/.aws/config..."
AWS_CONFIG_FILE="${HOME}/.aws/config"

if [ ! -f "$AWS_CONFIG_FILE" ]; then
    echo "Error: AWS config file not found at $AWS_CONFIG_FILE"
    echo "Please configure AWS CLI first"
    exit 1
fi

# Try to find a profile that matches the account ID or contains "Developer"
if [ -n "$AWS_PROFILE" ]; then
    echo "Using AWS_PROFILE from environment: $AWS_PROFILE"
else
    # Look for profile matching account ID or Developer role
    AWS_PROFILE=$(grep -E "^\[profile " "$AWS_CONFIG_FILE" | \
        sed 's/\[profile //' | sed 's/\]//' | \
        grep -E "(Developer|${ACCOUNT_ID})" | \
        head -1)
    
    if [ -z "$AWS_PROFILE" ]; then
        echo "Error: Could not find AWS profile matching account $ACCOUNT_ID"
        echo "Available profiles:"
        grep -E "^\[profile " "$AWS_CONFIG_FILE" | sed 's/\[profile /  - /' | sed 's/\]//'
        echo ""
        echo "Please set AWS_PROFILE environment variable or update the script"
        exit 1
    fi
    
    echo "Found AWS profile: $AWS_PROFILE"
fi

export AWS_PROFILE

# Login with SSO
echo "Logging in with AWS SSO..."
aws sso login 

# Authenticate with ECR
echo "Authenticating with ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_BASE > /dev/null 2>&1

# Build all images using docker-compose with AMD-64 platform
echo ""
echo "Building all images with docker-compose for AMD-64 (linux/amd64)..."
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose build
if [ $? -ne 0 ]; then
    echo "Error: docker-compose build failed"
    exit 1
fi
echo "✓ All images built successfully for AMD-64"
echo ""

# Create repositories and push images
for repo in "${REPOS[@]}"; do
    # Determine local image name based on docker-compose naming convention
    if [ "$repo" = "gateway" ]; then
        local_image="${repo}:${TAG}"
    else
        # Guard services use aiguards- prefix in docker-compose
        local_image="aiguards-${repo}:${TAG}"
    fi
    ecr_image="${ECR_BASE}/${repo}:${TAG}"
    
    echo "Processing: $repo"
    echo "  Local image: $local_image"
    echo "  ECR image: $ecr_image"
    
    # Verify local image exists
    if ! docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${local_image}$"; then
        echo "  ⚠️  Warning: Local image $local_image not found, skipping..."
        echo ""
        continue
    fi
    
    # Create ECR repository if it doesn't exist
    aws ecr describe-repositories --repository-names $repo --region $REGION > /dev/null 2>&1 || \
        aws ecr create-repository --repository-name $repo --region $REGION --image-scanning-configuration scanOnPush=true > /dev/null 2>&1
    
    # Tag image for ECR
    echo "  Tagging $local_image -> $ecr_image"
    docker tag $local_image $ecr_image
    
    # Push to ECR
    echo "  Pushing to ECR..."
    docker push $ecr_image
    echo "  ✓ Pushed: $ecr_image"
    echo ""
done

echo "✓ All images pushed to ECR!"
