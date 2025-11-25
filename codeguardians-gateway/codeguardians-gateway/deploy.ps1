# CodeGuardians Gateway - One-Command AWS Deployment
# This script deploys your application to AWS with minimal complexity

param(
    [string]$Region = "us-east-1",
    [string]$AccountId = "730335329303",
    [string]$VpcId = "",
    [string]$SubnetId = "",
    [string]$SecurityGroupId = ""
)

Write-Host "🚀 CodeGuardians Gateway - AWS Easy Deployment" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

# Check AWS CLI
try {
    $awsVersion = aws --version
    Write-Host "✅ AWS CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Please install AWS CLI first." -ForegroundColor Red
    exit 1
}

# Check AWS credentials
try {
    $callerIdentity = aws sts get-caller-identity --region $Region
    Write-Host "✅ AWS credentials configured" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS credentials not configured. Run 'aws configure' first." -ForegroundColor Red
    exit 1
}

# Check if ECR image exists
Write-Host "🔍 Checking ECR image..." -ForegroundColor Yellow
try {
    $images = aws ecr list-images --repository-name codeguardians-gateway --region $Region
    if ($images -match "imageTag") {
        Write-Host "✅ ECR image found" -ForegroundColor Green
    } else {
        Write-Host "❌ ECR image not found. Please push your image to ECR first." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ ECR repository not found. Please create and push your image first." -ForegroundColor Red
    exit 1
}

Write-Host "`n📝 Starting deployment process..." -ForegroundColor Cyan

# Step 1: Create secrets
Write-Host "`n1. Creating AWS Secrets Manager secrets..." -ForegroundColor Yellow
try {
    # Create app secrets
    $appSecrets = @{
        SECRET_KEY = "your-super-secret-key-32-chars-minimum-for-production"
        ENVIRONMENT = "production"
        LOG_LEVEL = "INFO"
        DEBUG = "false"
    } | ConvertTo-Json -Compress

    aws secretsmanager create-secret `
        --name "codeguardians-gateway/app-secrets" `
        --description "Main application secrets" `
        --secret-string $appSecrets `
        --region $Region 2>$null
    Write-Host "✅ Application secrets created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Application secrets might already exist" -ForegroundColor Yellow
}

# Step 2: Create CloudWatch log group
Write-Host "`n2. Creating CloudWatch log group..." -ForegroundColor Yellow
try {
    aws logs create-log-group `
        --log-group-name "/ecs/codeguardians-gateway" `
        --region $Region 2>$null
    Write-Host "✅ CloudWatch log group created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Log group might already exist" -ForegroundColor Yellow
}

# Step 3: Create ECS cluster
Write-Host "`n3. Creating ECS cluster..." -ForegroundColor Yellow
try {
    aws ecs create-cluster `
        --cluster-name "codeguardians-gateway-cluster" `
        --capacity-providers "FARGATE" `
        --default-capacity-provider-strategy "capacityProvider=FARGATE,weight=1" `
        --region $Region
    Write-Host "✅ ECS cluster created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  ECS cluster might already exist" -ForegroundColor Yellow
}

# Step 4: Create task definition
Write-Host "`n4. Creating ECS task definition..." -ForegroundColor Yellow

# Create task definition JSON
$taskDefinition = @{
    family = "codeguardians-gateway"
    networkMode = "awsvpc"
    requiresCompatibilities = @("FARGATE")
    cpu = "512"
    memory = "1024"
    executionRoleArn = "arn:aws:iam::$AccountId`:role/ecsTaskExecutionRole"
    containerDefinitions = @(
        @{
            name = "codeguardians-gateway"
            image = "$AccountId.dkr.ecr.$Region.amazonaws.com/codeguardians-gateway:latest"
            portMappings = @(
                @{
                    containerPort = 8000
                    protocol = "tcp"
                }
            )
            environment = @(
                @{
                    name = "ENVIRONMENT"
                    value = "production"
                },
                @{
                    name = "LOG_LEVEL"
                    value = "INFO"
                }
            )
            secrets = @(
                @{
                    name = "SECRET_KEY"
                    valueFrom = "arn:aws:secretsmanager:$Region`:$AccountId`:secret:codeguardians-gateway/app-secrets:SECRET_KEY"
                }
            )
            logConfiguration = @{
                logDriver = "awslogs"
                options = @{
                    "awslogs-group" = "/ecs/codeguardians-gateway"
                    "awslogs-region" = $Region
                    "awslogs-stream-prefix" = "ecs"
                }
            }
            healthCheck = @{
                command = @("CMD-SHELL", "curl -f http://localhost:8000/health/live || exit 1")
                interval = 30
                timeout = 5
                retries = 3
                startPeriod = 60
            }
        }
    )
} | ConvertTo-Json -Depth 10

# Save task definition to file
$taskDefinition | Out-File -FilePath "task-definition.json" -Encoding UTF8

try {
    aws ecs register-task-definition `
        --cli-input-json file://task-definition.json `
        --region $Region
    Write-Host "✅ Task definition registered" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to register task definition" -ForegroundColor Red
    Write-Host "   Check the task-definition.json file for errors" -ForegroundColor Yellow
    exit 1
}

# Step 5: Create ECS service (if VPC details provided)
if ($VpcId -and $SubnetId -and $SecurityGroupId) {
    Write-Host "`n5. Creating ECS service..." -ForegroundColor Yellow
    try {
        aws ecs create-service `
            --cluster "codeguardians-gateway-cluster" `
            --service-name "codeguardians-gateway-service" `
            --task-definition "codeguardians-gateway:1" `
            --desired-count 1 `
            --launch-type "FARGATE" `
            --network-configuration "awsvpcConfiguration={subnets=[$SubnetId],securityGroups=[$SecurityGroupId],assignPublicIp=ENABLED}" `
            --region $Region
        Write-Host "✅ ECS service created" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  ECS service might already exist" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n5. Skipping ECS service creation (VPC details not provided)" -ForegroundColor Yellow
    Write-Host "   To create the service manually, run:" -ForegroundColor Cyan
    Write-Host "   aws ecs create-service --cluster codeguardians-gateway-cluster --service-name codeguardians-gateway-service --task-definition codeguardians-gateway:1 --desired-count 1 --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}'" -ForegroundColor Gray
}

# Cleanup
Remove-Item "task-definition.json" -ErrorAction SilentlyContinue

Write-Host "`n🎉 Deployment process complete!" -ForegroundColor Green
Write-Host "`n📋 What was created:" -ForegroundColor Cyan
Write-Host "✅ AWS Secrets Manager secrets" -ForegroundColor White
Write-Host "✅ CloudWatch log group" -ForegroundColor White
Write-Host "✅ ECS cluster" -ForegroundColor White
Write-Host "✅ ECS task definition" -ForegroundColor White
if ($VpcId -and $SubnetId -and $SecurityGroupId) {
    Write-Host "✅ ECS service" -ForegroundColor White
}

Write-Host "`n🔧 Next steps:" -ForegroundColor Yellow
Write-Host "1. Create RDS database for PostgreSQL" -ForegroundColor White
Write-Host "2. Create ElastiCache cluster for Redis" -ForegroundColor White
Write-Host "3. Create Application Load Balancer" -ForegroundColor White
Write-Host "4. Update secrets with actual database credentials" -ForegroundColor White

Write-Host "`n📊 Check your deployment:" -ForegroundColor Cyan
Write-Host "aws ecs describe-services --cluster codeguardians-gateway-cluster --services codeguardians-gateway-service --region $Region" -ForegroundColor Gray

