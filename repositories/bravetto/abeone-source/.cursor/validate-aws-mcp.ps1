# Validate AWS MCP Server Configuration (PowerShell)
# This script tests all AWS services used by the AIGuards project

$ErrorActionPreference = "Continue"

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

$test_passed = 0
$test_failed = 0

Write-Host "=========================================="
Write-Host "  AWS MCP Server Validation"
Write-Host "=========================================="
Write-Host ""

# Test 1: AWS CLI Installation
Write-Info "Test 1: AWS CLI Installation"
try {
    $awsVersion = aws --version 2>&1
    Write-Success "AWS CLI is installed: $awsVersion"
    $test_passed++
} catch {
    Write-Error "AWS CLI is not installed"
    $test_failed++
}
Write-Host ""

# Test 2: AWS Credentials
Write-Info "Test 2: AWS Credentials Configuration"
try {
    $identity = aws sts get-caller-identity 2>&1 | ConvertFrom-Json
    Write-Success "AWS credentials are configured"
    Write-Host "Account: $($identity.Account), User: $($identity.Arn)"
    $test_passed++
} catch {
    Write-Error "AWS credentials are not configured or invalid"
    Write-Host "Run: .\.cursor\setup-aws-credentials.ps1"
    $test_failed++
}
Write-Host ""

# Test 3: ECS Access
Write-Info "Test 3: ECS (Elastic Container Service) Access"
try {
    $clusters = aws ecs list-clusters 2>&1 | ConvertFrom-Json
    Write-Success "ECS access verified"
    $cluster_count = $clusters.clusterArns.Count
    Write-Info "Found $cluster_count ECS cluster(s)"
    
    # Check for our specific cluster
    try {
        $null = aws ecs describe-clusters --clusters codeguardians-gateway-cluster --region us-east-1 2>&1 | ConvertFrom-Json
        Write-Success "Found codeguardians-gateway-cluster"
    } catch {
        Write-Warning "codeguardians-gateway-cluster not found (may not be created yet)"
    }
    $test_passed++
} catch {
    Write-Error "ECS access failed - check IAM permissions"
    $test_failed++
}
Write-Host ""

# Test 4: ECR Access
Write-Info "Test 4: ECR (Elastic Container Registry) Access"
try {
    $repos = aws ecr describe-repositories 2>&1 | ConvertFrom-Json
    Write-Success "ECR access verified"
    $repo_count = $repos.repositories.Count
    Write-Info "Found $repo_count ECR repository(ies)"
    $test_passed++
} catch {
    Write-Error "ECR access failed - check IAM permissions"
    $test_failed++
}
Write-Host ""

# Test 5: Secrets Manager Access
Write-Info "Test 5: AWS Secrets Manager Access"
try {
    $null = aws secretsmanager list-secrets 2>&1 | ConvertFrom-Json
    Write-Success "Secrets Manager access verified"
    
    # Check for our specific secret
    try {
        $null = aws secretsmanager describe-secret --secret-id codeguardians-gateway/production --region us-east-1 2>&1 | ConvertFrom-Json
        Write-Success "Found codeguardians-gateway/production secret"
    } catch {
        Write-Warning "codeguardians-gateway/production secret not found (may not be created yet)"
    }
    $test_passed++
} catch {
    Write-Error "Secrets Manager access failed - check IAM permissions"
    $test_failed++
}
Write-Host ""

# Test 6: CloudWatch Logs Access
Write-Info "Test 6: CloudWatch Logs Access"
try {
    $null = aws logs describe-log-groups 2>&1 | ConvertFrom-Json
    Write-Success "CloudWatch Logs access verified"
    
    # Check for our specific log group
    try {
        $logGroups = aws logs describe-log-groups --log-group-name-prefix /ecs/codeguardians-gateway --region us-east-1 2>&1 | ConvertFrom-Json
        if ($logGroups.logGroups.Count -gt 0) {
            Write-Info "Found /ecs/codeguardians-gateway log group"
        } else {
            Write-Warning "/ecs/codeguardians-gateway log group not found (may not be created yet)"
        }
    } catch {
        Write-Warning "/ecs/codeguardians-gateway log group not found (may not be created yet)"
    }
    $test_passed++
} catch {
    Write-Error "CloudWatch Logs access failed - check IAM permissions"
    $test_failed++
}
Write-Host ""

# Test 7: Node.js and NPX (for MCP server)
Write-Info "Test 7: Node.js and NPX Installation"
try {
    $nodeVersion = node --version 2>&1
    $npmVersion = npm --version 2>&1
    Write-Success "Node.js and NPX are installed"
    Write-Info "Node.js: $nodeVersion, NPM: $npmVersion"
    $test_passed++
} catch {
    Write-Error "Node.js or NPX not found - required for MCP server"
    Write-Host "Install from: https://nodejs.org/"
    $test_failed++
}
Write-Host ""

# Test 8: MCP Configuration File
Write-Info "Test 8: MCP Configuration File"
if (Test-Path ".cursor\mcp-config.json") {
    Write-Success "MCP configuration file exists"
    try {
        $null = Get-Content ".cursor\mcp-config.json" | ConvertFrom-Json
        Write-Success "MCP configuration is valid JSON"
    } catch {
        Write-Error "MCP configuration has invalid JSON"
        $test_failed++
    }
    $test_passed++
} else {
    Write-Error "MCP configuration file not found at .cursor\mcp-config.json"
    $test_failed++
}
Write-Host ""

# Test 9: MCP Server Package
Write-Info "Test 9: AWS MCP Server Package"
try {
    $null = npx -y @modelcontextprotocol/server-aws --help 2>&1
    Write-Success "AWS MCP Server package is accessible"
    $test_passed++
} catch {
    Write-Warning "AWS MCP Server package check skipped (may require internet)"
}
Write-Host ""

# Summary
Write-Host "=========================================="
Write-Host "  Validation Summary"
Write-Host "=========================================="
Write-Host ""
Write-Success "Tests Passed: $test_passed"
if ($test_failed -gt 0) {
    Write-Error "Tests Failed: $test_failed"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Run: .\.cursor\setup-aws-credentials.ps1"
    Write-Host "  2. Check IAM permissions (see .cursor\aws-mcp-setup.md)"
    Write-Host "  3. Re-run this validation script"
    exit 1
} else {
    Write-Host ""
    Write-Success "All tests passed! ✨"
    Write-Host ""
    Write-Host "Your AWS MCP Server is ready to use!"
    Write-Host ""
    Write-Host "Try asking the AI:"
    Write-Host "  - 'List my ECS clusters'"
    Write-Host "  - 'Show ECR repositories'"
    Write-Host "  - 'Check Secrets Manager secrets'"
    Write-Host ""
    Write-Host "See .cursor\aws-mcp-setup.md for more information"
}
Write-Host ""


