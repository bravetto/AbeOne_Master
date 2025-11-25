# Setup AWS Credentials for MCP Server (PowerShell)
# This script helps configure AWS credentials for the MCP server to use

$ErrorActionPreference = "Stop"

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

Write-Host "======================================"
Write-Host "  AWS MCP Server Credentials Setup"
Write-Host "======================================"
Write-Host ""

# Check if AWS CLI is installed
Write-Info "Checking AWS CLI installation..."
try {
    $awsVersion = aws --version 2>&1
    Write-Success "AWS CLI is installed: $awsVersion"
} catch {
    Write-Error "AWS CLI is not installed!"
    Write-Host ""
    Write-Host "Install AWS CLI:"
    Write-Host "  Download: https://awscli.amazonaws.com/AWSCLIV2.msi"
    Write-Host "  Or use: winget install Amazon.AWSCLI"
    exit 1
}

Write-Host ""

# Check current configuration
Write-Info "Checking current AWS configuration..."
$configList = aws configure list 2>&1 | Out-String

if ($configList -match "<not set>") {
    Write-Warning "AWS credentials are not configured"
} else {
    Write-Success "AWS credentials are already configured"
    Write-Host $configList
    Write-Host ""
    $reconfigure = Read-Host "Do you want to reconfigure? (y/N)"
    if ($reconfigure -notmatch "^[Yy]$") {
        Write-Info "Skipping reconfiguration"
        exit 0
    }
}

Write-Host ""
Write-Info "AWS credentials can be configured in two ways:"
Write-Host ""
Write-Host "1. Interactive Configuration (Recommended for development)"
Write-Host "   - Uses 'aws configure' command"
Write-Host "   - Stores credentials in ~/.aws/credentials"
Write-Host ""
Write-Host "2. Environment Variables (Recommended for CI/CD)"
Write-Host "   - Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY"
Write-Host "   - Temporary, not persisted"
Write-Host ""

$method = Read-Host "Choose method (1 or 2)"

if ($method -eq "1") {
    Write-Info "Starting interactive AWS configuration..."
    Write-Host ""
    Write-Host "You will need:"
    Write-Host "  - AWS Access Key ID"
    Write-Host "  - AWS Secret Access Key"
    Write-Host "  - Default region (e.g., us-east-1)"
    Write-Host "  - Output format (default: json)"
    Write-Host ""
    
    aws configure
    
    Write-Host ""
    Write-Success "AWS configuration complete!"
    
} elseif ($method -eq "2") {
    Write-Info "Setting up environment variables..."
    Write-Host ""
    
    $aws_access_key_id = Read-Host "Enter AWS Access Key ID"
    $aws_secret_access_key = Read-Host "Enter AWS Secret Access Key" -AsSecureString
    $aws_secret_access_key_plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($aws_secret_access_key)
    )
    $aws_region = Read-Host "Enter AWS Region [us-east-1]"
    if ([string]::IsNullOrWhiteSpace($aws_region)) {
        $aws_region = "us-east-1"
    }
    
    # Set environment variables for current session
    $env:AWS_ACCESS_KEY_ID = $aws_access_key_id
    $env:AWS_SECRET_ACCESS_KEY = $aws_secret_access_key_plain
    $env:AWS_REGION = $aws_region
    
    # Create a PowerShell profile script for future use
    $envScript = @"
# AWS Credentials for MCP Server
# Load this file: . .\.cursor\.aws-env.ps1
`$env:AWS_ACCESS_KEY_ID = "$aws_access_key_id"
`$env:AWS_SECRET_ACCESS_KEY = "$aws_secret_access_key_plain"
`$env:AWS_REGION = "$aws_region"
"@
    
    $envScript | Out-File -FilePath ".cursor\.aws-env.ps1" -Encoding UTF8
    
    Write-Success "Environment variables set for current session"
    Write-Info "To persist for future sessions, run: . .\.cursor\.aws-env.ps1"
    
} else {
    Write-Error "Invalid option selected"
    exit 1
}

Write-Host ""
Write-Info "Validating AWS credentials..."
try {
    $identity = aws sts get-caller-identity 2>&1 | ConvertFrom-Json
    Write-Success "AWS credentials are valid!"
    Write-Host ""
    Write-Host "Account: $($identity.Account)"
    Write-Host "User ARN: $($identity.Arn)"
} catch {
    Write-Error "AWS credentials validation failed!"
    Write-Host $_.Exception.Message
    exit 1
}

Write-Host ""
Write-Host "======================================"
Write-Success "AWS MCP Server Setup Complete!"
Write-Host "======================================"
Write-Host ""
Write-Info "Next steps:"
Write-Host "  1. Restart Cursor to load the MCP configuration"
Write-Host "  2. Try asking: 'List my ECS clusters'"
Write-Host "  3. See .cursor/aws-mcp-setup.md for more information"
Write-Host ""


