#!/bin/bash
# CodeGuardians Gateway - Quick Setup Script
# This script sets up the local development environment

set -e  # Exit on error

echo " CodeGuardians Gateway - Local Setup"
echo "======================================"
echo ""

# Check if Docker is running
echo "1. Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo " Docker is not running. Please start Docker Desktop first."
    exit 1
fi
echo " Docker is running"
echo ""

# Check if env.unified exists
echo "2. Checking environment configuration..."
if [ ! -f "env.unified" ]; then
    echo "  env.unified not found. Creating from env.example..."
    if [ -f "env.example" ]; then
        cp env.example env.unified
        echo " Created env.unified from env.example"
    else
        echo " env.example not found. Cannot create env.unified."
        exit 1
    fi
else
    echo " env.unified exists"
fi
echo ""

# Validate required environment variables
echo "3. Validating environment variables..."
required_vars=("POSTGRES_PASSWORD" "REDIS_PASSWORD")
missing_vars=()

for var in "${required_vars[@]}"; do
    if ! grep -q "^${var}=" env.unified; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo " Missing required variables in env.unified:"
    printf '   - %s\n' "${missing_vars[@]}"
    exit 1
fi
echo " All required variables present"
echo ""

# Clean up old containers and volumes
echo "4. Cleaning up old containers and volumes..."
docker-compose down -v > /dev/null 2>&1 || true
echo " Cleaned up"
echo ""

# Start services
echo "5. Starting services..."
docker-compose up -d
echo " Services starting..."
echo ""

# Wait for services to be healthy
echo "6. Waiting for services to become healthy (this may take 30-60 seconds)..."
sleep 30

# Check container status
echo ""
echo "7. Checking service health..."
healthy_count=0
total_count=8

services=("REPLACE_ME" "codeguardians-gateway-postgres" "codeguardians-gateway-redis" "tokenguard-service" "trustguard-service" "contextguard-service" "biasguard-service" "securityguard-service")

for service in "${services[@]}"; do
    status=$(docker inspect --format='{{.State.Health.Status}}' "$service" 2>/dev/null || echo "not running")
    if [ "$status" = "healthy" ]; then
        echo "   $service"
        ((healthy_count++))
    else
        echo "  ⏳ $service (status: $status)"
    fi
done

echo ""
echo "Service Health: $healthy_count/$total_count healthy"
echo ""

# Test API endpoint
echo "8. Testing API endpoint..."
if curl -s -f http://localhost:8000/health/live > /dev/null; then
    echo " API is responding!"
    echo ""
    echo "======================================"
    echo " Setup Complete!"
    echo "======================================"
    echo ""
    echo "Your services are running at:"
    echo "  - Gateway API:  http://localhost:8000"
    echo "  - API Docs:     http://localhost:8000/docs"
    echo "  - PostgreSQL:   localhost:5433"
    echo "  - Redis:        localhost:6380"
    echo ""
    echo "To view logs:    docker-compose logs -f"
    echo "To stop:         docker-compose down"
    echo "To restart:      docker-compose restart"
    echo ""
else
    echo "  API not responding yet. Give it a few more seconds..."
    echo ""
    echo "To check status:  docker ps"
    echo "To view logs:     docker-compose logs -f"
fi
