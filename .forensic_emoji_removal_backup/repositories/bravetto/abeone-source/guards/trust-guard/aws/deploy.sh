#!/bin/bash
# Trust Guard AWS Deployment Script

set -euo pipefail

# Configuration
STACK_NAME="${STACK_NAME:-trust-guard-prod}"
ENVIRONMENT="${ENVIRONMENT:-prod}"
AWS_REGION="${AWS_REGION:-us-east-1}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    if ! command -v aws &> /dev/null; then
        error "AWS CLI is not installed. Please install it first."
        exit 1
    fi

    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install it first."
        exit 1
    fi

    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS credentials are not configured. Please run 'aws configure'."
        exit 1
    fi

    success "Prerequisites check passed"
}

# Get AWS account ID and ECR repository
get_aws_info() {
    log "Getting AWS account information..."
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    if [ -z "$AWS_ACCOUNT_ID" ]; then
        error "Could not get AWS Account ID"
        exit 1
    fi

    ECR_REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ENVIRONMENT}-trust-guard"
    success "AWS Account ID: ${AWS_ACCOUNT_ID}"
    success "ECR Repository: ${ECR_REPO_URI}"
}

# Authenticate Docker to ECR
docker_login() {
    log "Authenticating Docker to ECR..."
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URI
    success "Docker authenticated to ECR"
}

# Build Docker image
build_image() {
    log "Building Docker image..."
    docker build -t trust-guard:latest .
    success "Docker image built"
}

# Tag and push Docker image
push_image() {
    log "Tagging and pushing Docker image..."
    docker tag trust-guard:latest $ECR_REPO_URI:latest
    docker push $ECR_REPO_URI:latest
    success "Docker image pushed to ECR"
}

# Create ECR repository if it doesn't exist
create_ecr_repo() {
    log "Ensuring ECR repository exists..."
    if ! aws ecr describe-repositories --repository-names $ENVIRONMENT-trust-guard --region $AWS_REGION &> /dev/null; then
        aws ecr create-repository --repository-name $ENVIRONMENT-trust-guard --region $AWS_REGION --image-scanning-configuration scanOnPush=true
        success "ECR repository created"
    else
        success "ECR repository already exists"
    fi
}

# Deploy CloudFormation stack
deploy_infrastructure() {
    log "Deploying CloudFormation infrastructure..."

    # Get VPC ID (using default VPC)
    VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text 2>/dev/null)
    if [ -z "$VPC_ID" ] || [ "$VPC_ID" == "None" ]; then
        warning "No default VPC found. Please specify VPC_ID environment variable."
        error "VPC setup required for AWS deployment"
        exit 1
    fi

    # Get subnets for the VPC
    SUBNET_IDS=$(aws ec2 describe-subnets \
        --filters "Name=vpc-id,Values=$VPC_ID" "Name=state,Values=available" \
        --query "Subnets[*].SubnetId" --output text | tr '\t' ',')

    if [ -z "$SUBNET_IDS" ]; then
        error "No subnets found in VPC $VPC_ID"
        exit 1
    fi

    # Get list as array for CloudFormation
    SUBNET_LIST=$(echo $SUBNET_IDS | sed 's/,/,/g')

    log "Deploying CloudFormation stack: ${STACK_NAME}"
    log "VPC ID: ${VPC_ID}"
    log "Subnets: ${SUBNET_LIST}"

    aws cloudformation deploy \
        --template-file aws/infrastructure.yml \
        --stack-name $STACK_NAME \
        --parameter-overrides \
            EnvironmentName=$ENVIRONMENT \
            VpcId=$VPC_ID \
            SubnetIds=\"$SUBNET_LIST\" \
        --capabilities CAPABILITY_IAM \
        --region $AWS_REGION \
        --no-fail-on-empty-changeset

    success "CloudFormation stack deployed"

    # Get outputs
    ALB_DNS=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerDNS'].OutputValue" \
        --output text \
        --region $AWS_REGION)

    if [ -n "$ALB_DNS" ] && [ "$ALB_DNS" != "None" ]; then
        success "Load Balancer DNS: http://$ALB_DNS"
    fi
}

# Wait for service to be healthy
wait_for_service() {
    if [ -n "${ALB_DNS:-}" ]; then
        log "Waiting for service to be healthy..."

        # Simple health check
        for i in {1..30}; do
            if curl -f -s "http://$ALB_DNS/health" > /dev/null 2>&1; then
                success "Service is healthy!"
                return 0
            fi
            log "Waiting... ($i/30)"
            sleep 10
        done

        warning "Service health check timed out, but deployment completed"
    fi
}

# Main deployment function
main() {
    echo "🚀 Trust Guard AWS Deployment"
    echo "================================"
    log "Environment: $ENVIRONMENT"
    log "AWS Region: $AWS_REGION"
    log "Stack Name: $STACK_NAME"
    echo ""

    check_prerequisites
    get_aws_info
    create_ecr_repo
    docker_login
    build_image
    push_image
    deploy_infrastructure
    wait_for_service

    echo ""
    success "Deployment completed successfully! 🎉"

    if [ -n "${ALB_DNS:-}" ]; then
        echo ""
        echo "🌐 Service URLs:"
        echo "  Health Check: http://$ALB_DNS/health"
        echo "  API Documentation: http://$ALB_DNS/docs"
        echo ""
        echo "🔍 Check service status:"
        echo "  aws ecs describe-services --cluster $ENVIRONMENT-trust-guard --services $ENVIRONMENT-trust-guard-service --region $AWS_REGION"
        echo ""
        echo "📊 View logs:"
        echo "  aws logs tail /ecs/$ENVIRONMENT/trust-guard --region $AWS_REGION --follow"
    fi
}

# Handle script arguments
case "${1:-}" in
    "infrastructure")
        check_prerequisites
        get_aws_info
        deploy_infrastructure
        ;;
    "image")
        check_prerequisites
        get_aws_info
        create_ecr_repo
        docker_login
        build_image
        push_image
        ;;
    "all"|*)
        main
        ;;
esac
