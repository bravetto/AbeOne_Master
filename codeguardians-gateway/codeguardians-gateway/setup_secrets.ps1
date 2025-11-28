# CodeGuardians Gateway - AWS Secrets Manager Setup Script
# This script creates all necessary secrets for production deployment

param(
    [string]$Region = "us-east-1",
    [string]$AccountId = "730335329303"
)

Write-Host "🔐 CodeGuardians Gateway - AWS Secrets Manager Setup" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green

# Check if AWS CLI is available
Write-Host "🔍 Checking AWS CLI..." -ForegroundColor Yellow
try {
    $awsVersion = aws --version
    Write-Host "✅ AWS CLI found: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Please install AWS CLI first." -ForegroundColor Red
    exit 1
}

# Check AWS credentials
Write-Host "🔍 Checking AWS credentials..." -ForegroundColor Yellow
try {
    $callerIdentity = aws sts get-caller-identity --region $Region
    Write-Host "✅ AWS credentials configured" -ForegroundColor Green
    Write-Host "   Account: $($callerIdentity | ConvertFrom-Json | Select-Object -ExpandProperty Account)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ AWS credentials not configured. Run 'aws configure' first." -ForegroundColor Red
    exit 1
}

Write-Host "`n📝 Creating secrets for CodeGuardians Gateway..." -ForegroundColor Yellow

# 1. Create main application secrets
Write-Host "`n1. Creating application secrets..." -ForegroundColor Cyan
$appSecrets = @{
    SECRET_KEY = "your-super-secret-key-32-chars-minimum-for-production"
    DATABASE_URL = "postgresql+asyncpg://codeguardians-gateway:your-db-password@your-rds-endpoint:5432/codeguardians_gateway_db"
    REDIS_URL = "redis://:your-redis-password@your-elasticache-endpoint:6379/0"
    ENVIRONMENT = "production"
    LOG_LEVEL = "INFO"
    DEBUG = "false"
    ALLOWED_ORIGINS = "https://your-frontend-domain.com"
    ALLOWED_HOSTS = "your-alb-dns-name,localhost"
} | ConvertTo-Json -Compress

try {
    aws secretsmanager create-secret `
        --name "codeguardians-gateway/app-secrets" `
        --description "Main application secrets for CodeGuardians Gateway" `
        --secret-string $appSecrets `
        --region $Region
    Write-Host "✅ Application secrets created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Application secrets might already exist" -ForegroundColor Yellow
}

# 2. Create database secrets
Write-Host "`n2. Creating database secrets..." -ForegroundColor Cyan
$dbSecrets = @{
    username = "codeguardians-gateway"
    password = "your-secure-database-password"
    host = "your-rds-endpoint.amazonaws.com"
    port = "5432"
    database = "codeguardians_gateway_db"
    engine = "postgres"
} | ConvertTo-Json -Compress

try {
    aws secretsmanager create-secret `
        --name "codeguardians-gateway/database" `
        --description "Database credentials for CodeGuardians Gateway" `
        --secret-string $dbSecrets `
        --region $Region
    Write-Host "✅ Database secrets created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Database secrets might already exist" -ForegroundColor Yellow
}

# 3. Create Redis secrets
Write-Host "`n3. Creating Redis secrets..." -ForegroundColor Cyan
$redisSecrets = @{
    host = "your-elasticache-endpoint.amazonaws.com"
    port = "6379"
    password = "your-redis-password"
    database = "0"
} | ConvertTo-Json -Compress

try {
    aws secretsmanager create-secret `
        --name "codeguardians-gateway/redis" `
        --description "Redis credentials for CodeGuardians Gateway" `
        --secret-string $redisSecrets `
        --region $Region
    Write-Host "✅ Redis secrets created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Redis secrets might already exist" -ForegroundColor Yellow
}

# 4. List created secrets
Write-Host "`n📋 Created secrets:" -ForegroundColor Yellow
aws secretsmanager list-secrets `
    --query "SecretList[?contains(Name, 'codeguardians-gateway')].{Name:Name,Description:Description}" `
    --output table `
    --region $Region

Write-Host "`n🎉 Secrets setup complete!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Update the secret values with your actual credentials" -ForegroundColor White
Write-Host "2. Create your ECS task definition with the secret ARNs" -ForegroundColor White
Write-Host "3. Deploy your application to ECS" -ForegroundColor White

Write-Host "`n🔧 To update secret values:" -ForegroundColor Yellow
Write-Host "aws secretsmanager update-secret --secret-id 'codeguardians-gateway/app-secrets' --secret-string '{\"SECRET_KEY\": \"your-actual-secret\"}' --region $Region" -ForegroundColor Gray

