#!/bin/bash

# AWS Deployment Testing Script for CodeGuardians Gateway
# This script tests AWS deployment capabilities in the development environment

set -e

echo " Starting AWS Deployment Testing for CodeGuardians Gateway..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if AWS CLI is available
check_aws_cli() {
    print_status "Checking AWS CLI availability..."
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed or not in PATH"
        exit 1
    fi
    print_success "AWS CLI is available"
}

# Check AWS credentials
check_aws_credentials() {
    print_status "Checking AWS credentials..."
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials are not configured or invalid"
        print_status "Please configure AWS credentials using:"
        print_status "  aws configure"
        print_status "  or set environment variables:"
        print_status "  AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION"
        exit 1
    fi
    
    local caller_identity=$(aws sts get-caller-identity)
    local account_id=$(echo $caller_identity | jq -r '.Account')
    local user_arn=$(echo $caller_identity | jq -r '.Arn')
    
    print_success "AWS credentials are valid"
    print_status "Account ID: $account_id"
    print_status "User ARN: $user_arn"
}

# Test AWS services connectivity
test_aws_services() {
    print_status "Testing AWS services connectivity..."
    
    # Test S3
    print_status "Testing S3 connectivity..."
    if aws s3 ls &> /dev/null; then
        print_success "S3 connectivity successful"
    else
        print_warning "S3 connectivity failed"
    fi
    
    # Test EC2
    print_status "Testing EC2 connectivity..."
    if aws ec2 describe-regions --region us-east-1 &> /dev/null; then
        print_success "EC2 connectivity successful"
    else
        print_warning "EC2 connectivity failed"
    fi
    
    # Test ECS
    print_status "Testing ECS connectivity..."
    if aws ecs list-clusters --region us-east-1 &> /dev/null; then
        print_success "ECS connectivity successful"
    else
        print_warning "ECS connectivity failed"
    fi
    
    # Test RDS
    print_status "Testing RDS connectivity..."
    if aws rds describe-db-instances --region us-east-1 &> /dev/null; then
        print_success "RDS connectivity successful"
    else
        print_warning "RDS connectivity failed"
    fi
    
    # Test ElastiCache
    print_status "Testing ElastiCache connectivity..."
    if aws elasticache describe-cache-clusters --region us-east-1 &> /dev/null; then
        print_success "ElastiCache connectivity successful"
    else
        print_warning "ElastiCache connectivity failed"
    fi
}

# Test Docker image deployment to ECR
test_ecr_deployment() {
    print_status "Testing ECR deployment..."
    
    local region=${AWS_REGION:-us-east-1}
    local account_id=$(aws sts get-caller-identity --query Account --output text)
    local ecr_repo="codeguardians-gateway"
    local ecr_uri="${account_id}.dkr.ecr.${region}.amazonaws.com/${ecr_repo}"
    
    # Check if ECR repository exists
    if aws ecr describe-repositories --repository-names $ecr_repo --region $region &> /dev/null; then
        print_success "ECR repository exists: $ecr_uri"
    else
        print_status "Creating ECR repository..."
        if aws ecr create-repository --repository-name $ecr_repo --region $region &> /dev/null; then
            print_success "ECR repository created: $ecr_uri"
        else
            print_error "Failed to create ECR repository"
            return 1
        fi
    fi
    
    # Login to ECR
    print_status "Logging in to ECR..."
    if aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $ecr_uri; then
        print_success "ECR login successful"
    else
        print_error "ECR login failed"
        return 1
    fi
    
    # Build and push image
    print_status "Building and pushing Docker image..."
    if docker build -t $ecr_repo:latest . && \
       docker tag $ecr_repo:latest $ecr_uri:latest && \
       docker push $ecr_uri:latest; then
        print_success "Docker image pushed to ECR: $ecr_uri:latest"
    else
        print_error "Failed to push Docker image to ECR"
        return 1
    fi
}

# Test ECS deployment
test_ecs_deployment() {
    print_status "Testing ECS deployment..."
    
    local region=${AWS_REGION:-us-east-1}
    local cluster_name="codeguardians-gateway-cluster"
    local service_name="codeguardians-gateway-service"
    local task_definition_name="codeguardians-gateway-task"
    
    # Check if ECS cluster exists
    if aws ecs describe-clusters --clusters $cluster_name --region $region &> /dev/null; then
        print_success "ECS cluster exists: $cluster_name"
    else
        print_status "Creating ECS cluster..."
        if aws ecs create-cluster --cluster-name $cluster_name --region $region &> /dev/null; then
            print_success "ECS cluster created: $cluster_name"
        else
            print_warning "Failed to create ECS cluster"
        fi
    fi
    
    # Create task definition
    print_status "Creating ECS task definition..."
    cat > /tmp/task-definition.json << EOF
{
  "family": "$task_definition_name",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "codeguardians-gateway",
      "image": "$(aws sts get-caller-identity --query Account --output text).dkr.ecr.${region}.amazonaws.com/codeguardians-gateway:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/codeguardians-gateway",
          "awslogs-region": "$region",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        },
        {
          "name": "AWS_REGION",
          "value": "$region"
        }
      ]
    }
  ]
}
EOF
    
    if aws ecs register-task-definition --cli-input-json file:///tmp/task-definition.json --region $region &> /dev/null; then
        print_success "ECS task definition created: $task_definition_name"
    else
        print_warning "Failed to create ECS task definition"
    fi
}

# Test RDS database connectivity
test_rds_connectivity() {
    print_status "Testing RDS connectivity..."
    
    local region=${AWS_REGION:-us-east-1}
    
    # List RDS instances
    if aws rds describe-db-instances --region $region --query 'DBInstances[?DBInstanceStatus==`available`].[DBInstanceIdentifier,Endpoint.Address,Endpoint.Port]' --output table; then
        print_success "RDS instances listed successfully"
    else
        print_warning "No RDS instances found or access denied"
    fi
}

# Test ElastiCache connectivity
test_elasticache_connectivity() {
    print_status "Testing ElastiCache connectivity..."
    
    local region=${AWS_REGION:-us-east-1}
    
    # List ElastiCache clusters
    if aws elasticache describe-cache-clusters --region $region --query 'CacheClusters[?CacheClusterStatus==`available`].[CacheClusterId,Endpoint.Address,Endpoint.Port]' --output table; then
        print_success "ElastiCache clusters listed successfully"
    else
        print_warning "No ElastiCache clusters found or access denied"
    fi
}

# Test application health in AWS context
test_application_health() {
    print_status "Testing application health in AWS context..."
    
    # Test if the application is running and healthy
    if curl -f http://localhost:8000/health/live &> /dev/null; then
        print_success "Application is healthy"
        
        # Test configuration endpoints
        if curl -f http://localhost:8000/api/v1/config/status &> /dev/null; then
            print_success "Configuration endpoints are accessible"
        else
            print_warning "Configuration endpoints are not accessible"
        fi
        
        # Test rate limiting endpoints
        if curl -f http://localhost:8000/api/v1/config/rate-limits &> /dev/null; then
            print_success "Rate limiting endpoints are accessible"
        else
            print_warning "Rate limiting endpoints are not accessible"
        fi
    else
        print_error "Application is not healthy or not running"
        return 1
    fi
}

# Test dynamic configuration
test_dynamic_configuration() {
    print_status "Testing dynamic configuration..."
    
    # Test configuration reload
    if curl -X POST http://localhost:8000/api/v1/config/reload &> /dev/null; then
        print_success "Configuration reload successful"
    else
        print_warning "Configuration reload failed"
    fi
    
    # Test rate limit updates
    print_status "Testing rate limit updates..."
    local test_payload='{"requests_per_minute": 200, "requests_per_hour": 2000}'
    if curl -X PUT http://localhost:8000/api/v1/config/rate-limits \
        -H "Content-Type: application/json" \
        -d "$test_payload" &> /dev/null; then
        print_success "Rate limit update successful"
    else
        print_warning "Rate limit update failed"
    fi
}

# Generate test report
generate_test_report() {
    print_status "Generating test report..."
    
    local report_file="/tmp/aws-deployment-test-report-$(date +%Y%m%d-%H%M%S).txt"
    
    cat > $report_file << EOF
CodeGuardians Gateway - AWS Deployment Test Report
Generated: $(date)
AWS Region: ${AWS_REGION:-us-east-1}
AWS Account: $(aws sts get-caller-identity --query Account --output text)

Test Results:
- AWS CLI: $(command -v aws &> /dev/null && echo "Available" || echo "Not Available")
- AWS Credentials: $(aws sts get-caller-identity &> /dev/null && echo "Valid" || echo "Invalid")
- Application Health: $(curl -f http://localhost:8000/health/live &> /dev/null && echo "Healthy" || echo "Unhealthy")
- Configuration API: $(curl -f http://localhost:8000/api/v1/config/status &> /dev/null && echo "Accessible" || echo "Not Accessible")

Recommendations:
1. Ensure all required AWS services are accessible
2. Configure proper IAM permissions for ECS, ECR, RDS, and ElastiCache
3. Set up CloudWatch logging for application monitoring
4. Configure VPC and security groups for production deployment
5. Set up auto-scaling for ECS service

EOF
    
    print_success "Test report generated: $report_file"
}

# Main execution
main() {
    print_status "Starting AWS deployment testing..."
    
    # Run all tests
    check_aws_cli
    check_aws_credentials
    test_aws_services
    test_application_health
    test_dynamic_configuration
    
    # Optional tests (may fail if resources don't exist)
    test_ecr_deployment || print_warning "ECR deployment test failed"
    test_ecs_deployment || print_warning "ECS deployment test failed"
    test_rds_connectivity || print_warning "RDS connectivity test failed"
    test_elasticache_connectivity || print_warning "ElastiCache connectivity test failed"
    
    # Generate report
    generate_test_report
    
    print_success "AWS deployment testing completed!"
    print_status "Check the test report for detailed results and recommendations"
}

# Run main function
main "$@"
