# CodeGuardians Gateway - Quick Setup Script (Windows PowerShell)
# This script sets up the local development environment

Write-Host "🚀 CodeGuardians Gateway - Local Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "1. Checking Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check if env.unified exists
Write-Host "2. Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path "env.unified")) {
    Write-Host "⚠️  env.unified not found. Creating from env.example..." -ForegroundColor Yellow
    if (Test-Path "env.example") {
        Copy-Item "env.example" "env.unified"
        Write-Host "✅ Created env.unified from env.example" -ForegroundColor Green
    } else {
        Write-Host "❌ env.example not found. Cannot create env.unified." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ env.unified exists" -ForegroundColor Green
}
Write-Host ""

# Validate required environment variables
Write-Host "3. Validating environment variables..." -ForegroundColor Yellow
$requiredVars = @("POSTGRES_PASSWORD", "REDIS_PASSWORD")
$missingVars = @()

foreach ($var in $requiredVars) {
    if (-not (Select-String -Path "env.unified" -Pattern "^${var}=" -Quiet)) {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "❌ Missing required variables in env.unified:" -ForegroundColor Red
    foreach ($var in $missingVars) {
        Write-Host "   - $var" -ForegroundColor Red
    }
    exit 1
}
Write-Host "✅ All required variables present" -ForegroundColor Green
Write-Host ""

# Clean up old containers and volumes
Write-Host "4. Cleaning up old containers and volumes..." -ForegroundColor Yellow
docker-compose down -v 2>&1 | Out-Null
Write-Host "✅ Cleaned up" -ForegroundColor Green
Write-Host ""

# Start services
Write-Host "5. Starting services..." -ForegroundColor Yellow
docker-compose up -d
Write-Host "✅ Services starting..." -ForegroundColor Green
Write-Host ""

# Wait for services to be healthy
Write-Host "6. Waiting for services to become healthy (this may take 30-60 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check container status
Write-Host ""
Write-Host "7. Checking service health..." -ForegroundColor Yellow
$healthyCount = 0
$totalCount = 8

$services = @(
    "codeguardians-gateway-production",
    "codeguardians-gateway-postgres",
    "codeguardians-gateway-redis",
    "tokenguard-service",
    "trustguard-service",
    "contextguard-service",
    "biasguard-service",
    "securityguard-service"
)

foreach ($service in $services) {
    try {
        $status = docker inspect --format='{{.State.Health.Status}}' $service 2>$null
        if ($status -eq "healthy") {
            Write-Host "  ✅ $service" -ForegroundColor Green
            $healthyCount++
        } else {
            Write-Host "  ⏳ $service (status: $status)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ❌ $service (not running)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Service Health: $healthyCount/$totalCount healthy" -ForegroundColor Cyan
Write-Host ""

# Test API endpoint
Write-Host "8. Testing API endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health/live" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API is responding!" -ForegroundColor Green
        Write-Host ""
        Write-Host "======================================" -ForegroundColor Cyan
        Write-Host "✅ Setup Complete!" -ForegroundColor Green
        Write-Host "======================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Your services are running at:"
        Write-Host "  - Gateway API:  http://localhost:8000"
        Write-Host "  - API Docs:     http://localhost:8000/docs"
        Write-Host "  - PostgreSQL:   localhost:5433"
        Write-Host "  - Redis:        localhost:6380"
        Write-Host ""
        Write-Host "To view logs:    docker-compose logs -f"
        Write-Host "To stop:         docker-compose down"
        Write-Host "To restart:      docker-compose restart"
        Write-Host ""
    }
} catch {
    Write-Host "⚠️  API not responding yet. Give it a few more seconds..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To check status:  docker ps"
    Write-Host "To view logs:     docker-compose logs -f"
}
