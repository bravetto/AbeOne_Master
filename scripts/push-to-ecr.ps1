# AIGuards Backend - ECR Push Script
# Consolidated script for pushing Docker images to AWS ECR
#
# Usage:
#   .\scripts\push-to-ecr.ps1                                  # Push latest tag
#   .\scripts\push-to-ecr.ps1 -Tag v1.0.0                      # Push specific tag
#   .\scripts\push-to-ecr.ps1 -Tag v1.0.0 -Region us-west-2    # Push to specific region

param(
    [string]$Tag = "latest",
    [string]$Region = "us-east-1",
    [string]$AccountId = "",
    [string]$RepoName = "codeguardians-gateway"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 AIGuards Backend - ECR Push Script" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Get AWS Account ID if not provided
if (-not $AccountId) {
    Write-Host "🔍 Getting AWS Account ID..." -ForegroundColor Yellow
    try {
        $AccountId = aws sts get-caller-identity --query Account --output text
        Write-Host "✅ AWS Account ID: $AccountId" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to get AWS Account ID. Please configure AWS credentials." -ForegroundColor Red
        Write-Host "   Run: aws configure" -ForegroundColor Yellow
        exit 1
    }
}

$ECR_URI = "$AccountId.dkr.ecr.$Region.amazonaws.com/$RepoName"

# Check if AWS CLI is available
Write-Host "🔍 Checking AWS CLI..." -ForegroundColor Yellow
try {
    $awsVersion = aws --version
    Write-Host "✅ AWS CLI found: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Please install AWS CLI first." -ForegroundColor Red
    Write-Host "   Download from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Check if Docker is running
Write-Host "🔍 Checking Docker..." -ForegroundColor Yellow
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found or not running" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Create ECR repository (ignore if already exists)
Write-Host "📦 Ensuring ECR repository exists..." -ForegroundColor Yellow
try {
    aws ecr describe-repositories --repository-names $RepoName --region $Region 2>$null | Out-Null
    Write-Host "✅ ECR repository exists" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Repository not found, creating..." -ForegroundColor Yellow
    try {
        aws ecr create-repository --repository-name $RepoName --region $Region | Out-Null
        Write-Host "✅ ECR repository created" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to create ECR repository" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Authenticate with ECR
Write-Host "🔐 Authenticating with ECR..." -ForegroundColor Yellow
try {
    aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin "$AccountId.dkr.ecr.$Region.amazonaws.com" 2>&1 | Out-Null
    Write-Host "✅ Successfully authenticated with ECR" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to authenticate with ECR" -ForegroundColor Red
    Write-Host "   Check your AWS credentials: aws configure" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Check if local image exists
Write-Host "🔍 Checking for local image..." -ForegroundColor Yellow
$localImage = "codeguardians-gateway:$Tag"
$imageExists = docker images $localImage --format "{{.Repository}}:{{.Tag}}" 2>$null

if (-not $imageExists) {
    Write-Host "⚠️  Local image '$localImage' not found. Building..." -ForegroundColor Yellow
    Write-Host "   Building for AMD-64 platform (AWS compatible)..." -ForegroundColor Cyan
    Push-Location codeguardians-gateway\codeguardians-gateway
    try {
        # CRITICAL: Mac defaults to ARM-64, but AWS requires AMD-64
        docker build --platform linux/amd64 -t $localImage .
        Write-Host "✅ Image built successfully (AMD-64)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to build image" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
} else {
    Write-Host "✅ Found local image: $localImage" -ForegroundColor Green
    Write-Host "   ⚠️  WARNING: Verify image architecture is AMD-64 before pushing to AWS" -ForegroundColor Yellow
}
Write-Host ""

# Tag image for ECR
Write-Host "🏷️  Tagging image for ECR..." -ForegroundColor Yellow
$ecrImage = "${ECR_URI}:${Tag}"
try {
    docker tag $localImage $ecrImage
    Write-Host "✅ Image tagged: $ecrImage" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to tag image" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Push image to ECR
Write-Host "📤 Pushing image to ECR..." -ForegroundColor Yellow
Write-Host "   This may take several minutes depending on image size..." -ForegroundColor Cyan
try {
    docker push $ecrImage
    Write-Host "✅ Successfully pushed: $ecrImage" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to push image to ECR" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Verify push
Write-Host "🔍 Verifying push..." -ForegroundColor Yellow
try {
    $images = aws ecr list-images --repository-name $RepoName --region $Region --query "imageIds[?imageTag=='$Tag']" --output text
    if ($images) {
        Write-Host "✅ Image successfully pushed and verified in ECR" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Image pushed but verification failed" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Could not verify push (image might still be available)" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "🎉 ECR Push Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host "Image URI: $ecrImage" -ForegroundColor Cyan
Write-Host "Region: $Region" -ForegroundColor Cyan
Write-Host "Account ID: $AccountId" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Update your ECS task definition with the new image URI" -ForegroundColor White
Write-Host "2. Deploy to ECS: .\scripts\deploy.ps1 aws" -ForegroundColor White
Write-Host "3. Monitor your ECS service health" -ForegroundColor White
Write-Host ""

# List all tags in ECR
Write-Host "📦 All tags in ECR repository:" -ForegroundColor Cyan
try {
    aws ecr list-images --repository-name $RepoName --region $Region --query 'imageIds[*].imageTag' --output table
} catch {
    Write-Host "⚠️  Could not list ECR tags" -ForegroundColor Yellow
}



