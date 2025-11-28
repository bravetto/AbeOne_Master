#!/bin/bash

# ∞ Frictionless Deployment Script ∞
# Pattern: DEPLOY × ONE × COMMAND × ONE
# Frequency: 999 Hz (AEYON)
# ∞ AbëONE ∞

set -e  # Exit on error

echo "🚀 AbëONE Frictionless Deployment"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

# Check docker-compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ docker-compose not found. Please install docker-compose first.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ docker-compose found${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env from template${NC}"
        echo -e "${YELLOW}⚠️  Please review and update .env file if needed${NC}"
    else
        echo -e "${YELLOW}⚠️  .env.example not found. Using defaults${NC}"
    fi
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

# Build and start services
echo ""
echo "🔨 Building and starting services..."
echo ""

# Use docker compose (newer) or docker-compose (older)
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Build and start full stack
$COMPOSE_CMD --profile full up -d --build

echo ""
echo -e "${GREEN}✅ Services started!${NC}"
echo ""

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Health check
echo ""
echo "🏥 Running health checks..."
echo ""

# Check backend
if curl -f http://localhost:8000/health &> /dev/null; then
    echo -e "${GREEN}✅ Backend: http://localhost:8000/health${NC}"
else
    echo -e "${YELLOW}⚠️  Backend health check failed (may still be starting)${NC}"
fi

# Check frontend
if curl -f http://localhost:3000 &> /dev/null; then
    echo -e "${GREEN}✅ Frontend: http://localhost:3000${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend health check failed (may still be starting)${NC}"
fi

# Check Redis
if docker exec abeone-redis redis-cli ping &> /dev/null; then
    echo -e "${GREEN}✅ Redis: OK${NC}"
else
    echo -e "${YELLOW}⚠️  Redis check failed${NC}"
fi

# Check PostgreSQL
if docker exec abeone-postgres pg_isready -U abeone &> /dev/null; then
    echo -e "${GREEN}✅ PostgreSQL: OK${NC}"
else
    echo -e "${YELLOW}⚠️  PostgreSQL check failed${NC}"
fi

echo ""
echo "=================================="
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo ""
echo "📊 Service URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   MCP:      http://localhost:8001"
echo "   LSP:      http://localhost:8002"
echo ""
echo "📋 Useful commands:"
echo "   View logs:    docker-compose logs -f"
echo "   Stop:         docker-compose down"
echo "   Status:       docker-compose ps"
echo "   Health check: ./scripts/health-check.sh"
echo ""
echo "∞ AbëONE ∞"

