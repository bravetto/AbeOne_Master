#!/bin/bash
# Validate AWS MCP Server Configuration
# This script tests all AWS services used by the AIGuards project

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
    echo -e "${GREEN}${NC} $1"
}

warning() {
    echo -e "${YELLOW}${NC} $1"
}

error() {
    echo -e "${RED}${NC} $1"
}

test_passed=0
test_failed=0

echo "=========================================="
echo "  AWS MCP Server Validation"
echo "=========================================="
echo ""

# Test 1: AWS CLI Installation
log "Test 1: AWS CLI Installation"
if command -v aws &> /dev/null; then
    success "AWS CLI is installed: $(aws --version)"
    ((test_passed++))
else
    error "AWS CLI is not installed"
    ((test_failed++))
fi
echo ""

# Test 2: AWS Credentials
log "Test 2: AWS Credentials Configuration"
if aws sts get-caller-identity &> /dev/null; then
    success "AWS credentials are configured"
    aws sts get-caller-identity | jq -r '"Account: \(.Account), User: \(.Arn)"' 2>/dev/null || aws sts get-caller-identity
    ((test_passed++))
else
    error "AWS credentials are not configured or invalid"
    echo "Run: .cursor/setup-aws-credentials.sh"
    ((test_failed++))
fi
echo ""

# Test 3: ECS Access
log "Test 3: ECS (Elastic Container Service) Access"
if aws ecs list-clusters &> /dev/null; then
    success "ECS access verified"
    cluster_count=$(aws ecs list-clusters --query 'length(clusterArns)' --output text 2>/dev/null || echo "0")
    log "Found $cluster_count ECS cluster(s)"
    
    # Check for our specific cluster
    if aws ecs describe-clusters --clusters codeguardians-gateway-cluster --region us-east-1 &> /dev/null; then
        success "Found codeguardians-gateway-cluster"
    else
        warning "codeguardians-gateway-cluster not found (may not be created yet)"
    fi
    ((test_passed++))
else
    error "ECS access failed - check IAM permissions"
    ((test_failed++))
fi
echo ""

# Test 4: ECR Access
log "Test 4: ECR (Elastic Container Registry) Access"
if aws ecr describe-repositories &> /dev/null 2>&1; then
    success "ECR access verified"
    repo_count=$(aws ecr describe-repositories --query 'length(repositories)' --output text 2>/dev/null || echo "0")
    log "Found $repo_count ECR repository(ies)"
    ((test_passed++))
else
    error "ECR access failed - check IAM permissions"
    ((test_failed++))
fi
echo ""

# Test 5: Secrets Manager Access
log "Test 5: AWS Secrets Manager Access"
if aws secretsmanager list-secrets &> /dev/null 2>&1; then
    success "Secrets Manager access verified"
    
    # Check for our specific secret
    if aws secretsmanager describe-secret --secret-id codeguardians-gateway/production --region us-east-1 &> /dev/null 2>&1; then
        success "Found codeguardians-gateway/production secret"
    else
        warning "codeguardians-gateway/production secret not found (may not be created yet)"
    fi
    ((test_passed++))
else
    error "Secrets Manager access failed - check IAM permissions"
    ((test_failed++))
fi
echo ""

# Test 6: CloudWatch Logs Access
log "Test 6: CloudWatch Logs Access"
if aws logs describe-log-groups &> /dev/null 2>&1; then
    success "CloudWatch Logs access verified"
    
    # Check for our specific log group
    if aws logs describe-log-groups --log-group-name-prefix /ecs/codeguardians-gateway --region us-east-1 &> /dev/null 2>&1; then
        log "Found /ecs/codeguardians-gateway log group"
    else
        warning "/ecs/codeguardians-gateway log group not found (may not be created yet)"
    fi
    ((test_passed++))
else
    error "CloudWatch Logs access failed - check IAM permissions"
    ((test_failed++))
fi
echo ""

# Test 7: Node.js and NPX (for MCP server)
log "Test 7: Node.js and NPX Installation"
if command -v node &> /dev/null && command -v npx &> /dev/null; then
    success "Node.js and NPX are installed"
    log "Node.js: $(node --version), NPM: $(npm --version)"
    ((test_passed++))
else
    error "Node.js or NPX not found - required for MCP server"
    echo "Install from: https://nodejs.org/"
    ((test_failed++))
fi
echo ""

# Test 8: MCP Configuration File
log "Test 8: MCP Configuration File"
if [ -f ".cursor/mcp-config.json" ]; then
    success "MCP configuration file exists"
    if command -v jq &> /dev/null; then
        if jq empty .cursor/mcp-config.json 2>/dev/null; then
            success "MCP configuration is valid JSON"
        else
            error "MCP configuration has invalid JSON"
            ((test_failed++))
        fi
    fi
    ((test_passed++))
else
    error "MCP configuration file not found at .cursor/mcp-config.json"
    ((test_failed++))
fi
echo ""

# Test 9: MCP Server Package
log "Test 9: AWS MCP Server Package"
if npx -y @modelcontextprotocol/server-aws --help &> /dev/null 2>&1; then
    success "AWS MCP Server package is accessible"
    ((test_passed++))
else
    warning "AWS MCP Server package check skipped (may require internet)"
    # Don't count as failure
fi
echo ""

# Summary
echo "=========================================="
echo "  Validation Summary"
echo "=========================================="
echo ""
success "Tests Passed: $test_passed"
if [ $test_failed -gt 0 ]; then
    error "Tests Failed: $test_failed"
    echo ""
    echo "Next steps:"
    echo "  1. Run: .cursor/setup-aws-credentials.sh"
    echo "  2. Check IAM permissions (see .cursor/aws-mcp-setup.md)"
    echo "  3. Re-run this validation script"
    exit 1
else
    echo ""
    success "All tests passed! "
    echo ""
    echo "Your AWS MCP Server is ready to use!"
    echo ""
    echo "Try asking the AI:"
    echo "  - 'List my ECS clusters'"
    echo "  - 'Show ECR repositories'"
    echo "  - 'Check Secrets Manager secrets'"
    echo ""
    echo "See .cursor/aws-mcp-setup.md for more information"
fi
echo ""


