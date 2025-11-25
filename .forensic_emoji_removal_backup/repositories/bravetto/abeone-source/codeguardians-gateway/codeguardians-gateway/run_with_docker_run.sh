#!/bin/bash
# CodeGuardians Gateway - Docker Run Commands
# Alternative to docker-compose for running individual containers

echo "🚀 CodeGuardians Gateway - Docker Run Setup"
echo "============================================="

# Create a custom network for the services
echo "📡 Creating Docker network..."
docker network create codeguardians-network

# Set environment variables
export POSTGRES_PASSWORD="REPLACE_ME"
export REDIS_PASSWORD="REPLACE_ME"
export SECRET_KEY="change-me-in-production-min-32-chars-for-security"

echo "🐘 Starting PostgreSQL container..."
docker run -d \
    --name codeguardians-postgres \
    --network codeguardians-network \
    -e POSTGRES_DB=codeguardians-gateway_db \
    -e POSTGRES_USER=codeguardians-gateway \
    -e POSTGRES_PASSWORD=REPLACE_ME \
    -e POSTGRES_INITDB_ARGS="--encoding=UTF-8 --lc-collate=C --lc-ctype=C" \
    -p 5433:5432 \
    -v postgres_data:/var/lib/postgresql/data \
    --restart unless-stopped \
    postgres:15-alpine

echo "🔴 Starting Redis container..."
docker run -d \
    --name codeguardians-redis \
    --network codeguardians-network \
    -e REDIS_PASSWORD=REPLACE_ME \
    -p 6380:6379 \
    -v redis_data:/data \
    --restart unless-stopped \
    redis:7-alpine redis-server --appendonly yes --requirepass $REDIS_PASSWORD --maxmemory 256mb --maxmemory-policy allkeys-lru

echo "⏳ Waiting for database and Redis to be ready..."
sleep 10

# Wait for PostgreSQL to be ready
echo "🔍 Checking PostgreSQL readiness..."
until docker exec codeguardians-postgres pg_isready -U codeguardians-gateway -d codeguardians-gateway_db; do
    echo "   PostgreSQL not ready yet, waiting..."
    sleep 2
done
echo "✅ PostgreSQL is ready!"

# Wait for Redis to be ready
echo "🔍 Checking Redis readiness..."
until docker exec codeguardians-redis redis-cli --raw incr ping; do
    echo "   Redis not ready yet, waiting..."
    sleep 2
done
echo "✅ Redis is ready!"

echo "🏗️ Building CodeGuardians Gateway image..."
docker build -t codeguardians-gateway:latest .

echo "🚀 Starting CodeGuardians Gateway container..."
docker run -d \
    --name codeguardians-gateway \
    --network codeguardians-network \
    -e DATABASE_URL="REPLACE_ME" \
    -e REDIS_URL="redis=REPLACE_MEcodeguardians-redis:6379/0" \
    -e SECRET_KEY=$SECRET_KEY \
    -e ENVIRONMENT=development \
    -e DEBUG=true \
    -e LOG_LEVEL=DEBUG \
    -e ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8080,http://localhost:8001" \
    -e ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0" \
    -e DATABASE_ENABLED=true \
    -e BIASGUARD_ENABLED=true \
    -e BIASGUARD_ENFORCE_FAIRNESS=true \
    -e BIASGUARD_ENFORCE_COMPLIANCE=true \
    -e BIASGUARD_ENFORCE_ATTRIBUTION=true \
    -p 8001:8000 \
    -p 5678:5678 \
    -v "$(pwd):/app" \
    --restart unless-stopped \
    codeguardians-gateway:latest

echo "⏳ Waiting for Gateway to start..."
sleep 15

echo "🔍 Checking container status..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "✅ CodeGuardians Gateway is running!"
echo "🌐 Access points:"
echo "   • Application: http://localhost:8001"
echo "   • Health Check: http://localhost:8001/health/live"
echo "   • Database: localhost:5433"
echo "   • Redis: localhost:6380"

echo ""
echo "📋 Useful commands:"
echo "   • View logs: docker logs codeguardians-gateway"
echo "   • Stop all: docker stop codeguardians-gateway codeguardians-postgres codeguardians-redis"
echo "   • Remove all: docker rm codeguardians-gateway codeguardians-postgres codeguardians-redis"
echo "   • Remove network: docker network rm codeguardians-network"

echo ""
echo "🧪 Test connectivity:"
echo "   docker exec codeguardians-gateway python test_connectivity.py"
