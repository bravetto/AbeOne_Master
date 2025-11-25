# CodeGuardians Gateway - Docker Run Commands
# Alternative to docker-compose for running individual containers

Write-Host "🚀 CodeGuardians Gateway - Docker Run Setup" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Create a custom network for the services
Write-Host "📡 Creating Docker network..." -ForegroundColor Yellow
docker network create codeguardians-network

# Set environment variables
$env:POSTGRES_PASSWORD = "postgres-password-dev"
$env:REDIS_PASSWORD = "redis-password-dev"
$env:SECRET_KEY = "change-me-in-production-min-32-chars-for-security"

Write-Host "🐘 Starting PostgreSQL container..." -ForegroundColor Yellow
docker run -d `
    --name codeguardians-postgres `
    --network codeguardians-network `
    -e POSTGRES_DB=codeguardians-gateway_db `
    -e POSTGRES_USER=codeguardians-gateway `
    -e POSTGRES_PASSWORD=$env:POSTGRES_PASSWORD `
    -e POSTGRES_INITDB_ARGS="--encoding=UTF-8 --lc-collate=C --lc-ctype=C" `
    -p 5433:5432 `
    -v postgres_data:/var/lib/postgresql/data `
    --restart unless-stopped `
    postgres:15-alpine

Write-Host "🔴 Starting Redis container..." -ForegroundColor Yellow
docker run -d `
    --name codeguardians-redis `
    --network codeguardians-network `
    -e REDIS_PASSWORD=$env:REDIS_PASSWORD `
    -p 6380:6379 `
    -v redis_data:/data `
    --restart unless-stopped `
    redis:7-alpine redis-server --appendonly yes --requirepass $env:REDIS_PASSWORD --maxmemory 256mb --maxmemory-policy allkeys-lru

Write-Host "⏳ Waiting for database and Redis to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Wait for PostgreSQL to be ready
Write-Host "🔍 Checking PostgreSQL readiness..." -ForegroundColor Cyan
do {
    $pgReady = docker exec codeguardians-postgres pg_isready -U codeguardians-gateway -d codeguardians-gateway_db
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   PostgreSQL not ready yet, waiting..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }
} while ($LASTEXITCODE -ne 0)

Write-Host "✅ PostgreSQL is ready!" -ForegroundColor Green

# Wait for Redis to be ready
Write-Host "🔍 Checking Redis readiness..." -ForegroundColor Cyan
do {
    $redisReady = docker exec codeguardians-redis redis-cli --raw incr ping
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   Redis not ready yet, waiting..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }
} while ($LASTEXITCODE -ne 0)

Write-Host "✅ Redis is ready!" -ForegroundColor Green

Write-Host "🏗️ Building CodeGuardians Gateway image..." -ForegroundColor Yellow
docker build -t codeguardians-gateway:latest .

Write-Host "🚀 Starting CodeGuardians Gateway container..." -ForegroundColor Yellow
docker run -d `
    --name codeguardians-gateway `
    --network codeguardians-network `
    -e DATABASE_URL="postgresql+asyncpg://codeguardians-gateway:postgres-password-dev@codeguardians-postgres:5432/codeguardians-gateway_db" `
    -e REDIS_URL="redis://:redis-password-dev@codeguardians-redis:6379/0" `
    -e SECRET_KEY=$env:SECRET_KEY `
    -e ENVIRONMENT=development `
    -e DEBUG=true `
    -e LOG_LEVEL=DEBUG `
    -e ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8080,http://localhost:8001" `
    -e ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0" `
    -e DATABASE_ENABLED=true `
    -e BIASGUARD_ENABLED=true `
    -e BIASGUARD_ENFORCE_FAIRNESS=true `
    -e BIASGUARD_ENFORCE_COMPLIANCE=true `
    -e BIASGUARD_ENFORCE_ATTRIBUTION=true `
    -p 8001:8000 `
    -p 5678:5678 `
    -v "${PWD}:/app" `
    --restart unless-stopped `
    --depends-on codeguardians-postgres `
    --depends-on codeguardians-redis `
    codeguardians-gateway:latest

Write-Host "⏳ Waiting for Gateway to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "🔍 Checking container status..." -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host ""
Write-Host "✅ CodeGuardians Gateway is running!" -ForegroundColor Green
Write-Host "🌐 Access points:" -ForegroundColor Cyan
Write-Host "   • Application: http://localhost:8001" -ForegroundColor White
Write-Host "   • Health Check: http://localhost:8001/health/live" -ForegroundColor White
Write-Host "   • Database: localhost:5433" -ForegroundColor White
Write-Host "   • Redis: localhost:6380" -ForegroundColor White

Write-Host ""
Write-Host "📋 Useful commands:" -ForegroundColor Cyan
Write-Host "   • View logs: docker logs codeguardians-gateway" -ForegroundColor White
Write-Host "   • Stop all: docker stop codeguardians-gateway codeguardians-postgres codeguardians-redis" -ForegroundColor White
Write-Host "   • Remove all: docker rm codeguardians-gateway codeguardians-postgres codeguardians-redis" -ForegroundColor White
Write-Host "   • Remove network: docker network rm codeguardians-network" -ForegroundColor White

Write-Host ""
Write-Host "🧪 Test connectivity:" -ForegroundColor Cyan
Write-Host "   docker exec codeguardians-gateway python test_connectivity.py" -ForegroundColor White
