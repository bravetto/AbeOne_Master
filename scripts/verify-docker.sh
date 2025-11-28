#!/bin/bash
# Verify Docker Compose Setup
# Pattern: VERIFY × DOCKER × COMPOSE × ONE

set -e

echo "∞ Verifying Docker Compose Setup ∞"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found"
    exit 1
fi

echo "✅ Docker found: $(docker --version)"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose not found"
    exit 1
fi

if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose found: $(docker-compose --version)"
    COMPOSE_CMD="docker-compose"
else
    echo "✅ Docker Compose found: $(docker compose version)"
    COMPOSE_CMD="docker compose"
fi

# Check docker-compose.yml
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found"
    exit 1
fi

echo "✅ docker-compose.yml found"

# Validate configuration
echo ""
echo "Validating docker-compose.yml..."
$COMPOSE_CMD config > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ docker-compose.yml is valid"
else
    echo "❌ docker-compose.yml has errors"
    $COMPOSE_CMD config
    exit 1
fi

# Check Docker daemon
echo ""
echo "Checking Docker daemon..."
if docker info &> /dev/null; then
    echo "✅ Docker daemon is running"
else
    echo "⚠️  Docker daemon is not running"
    echo "   Start Docker Desktop or Docker daemon"
    exit 1
fi

# Check required Dockerfiles
echo ""
echo "Checking Dockerfiles..."

if [ -f "jimmy-aiagentsuite/Dockerfile" ]; then
    echo "✅ Backend Dockerfile found"
else
    echo "⚠️  Backend Dockerfile not found"
fi

if [ -f "abe-touch/abeone-touch/Dockerfile" ]; then
    echo "✅ Frontend Dockerfile found"
else
    echo "⚠️  Frontend Dockerfile not found (may need to be created)"
fi

if [ -f "integration/Dockerfile" ]; then
    echo "✅ Integration Dockerfile found"
else
    echo "⚠️  Integration Dockerfile not found (may need to be created)"
fi

echo ""
echo "✅ Docker Compose setup verified!"
echo ""
echo "To start services:"
echo "  docker-compose --profile full up -d"
echo ""
echo "To check status:"
echo "  docker-compose ps"
echo ""

