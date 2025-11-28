#!/bin/bash
# Docker Health Check Script
# Pattern: HEALTH × CHECK × DOCKER × ONE

set -e

echo "∞ Docker Health Check ∞"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_service() {
    local name=$1
    local url=$2
    
    echo -n "Checking $name... "
    if curl -s -f "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Healthy${NC}"
        return 0
    else
        echo -e "${RED}❌ Unhealthy${NC}"
        return 1
    fi
}

# Check Docker daemon
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running${NC}"
    exit 1
fi

# Check services
echo "Checking running services..."
echo ""

# Backend
if docker ps --format '{{.Names}}' | grep -q 'abeone-backend'; then
    check_service "Backend" "http://localhost:8000/health"
else
    echo -e "${YELLOW}⚠️  Backend container not running${NC}"
fi

# Frontend
if docker ps --format '{{.Names}}' | grep -q 'abeone-frontend'; then
    check_service "Frontend" "http://localhost:3000/api/health" || check_service "Frontend" "http://localhost:3000"
else
    echo -e "${YELLOW}⚠️  Frontend container not running${NC}"
fi

# Redis
if docker ps --format '{{.Names}}' | grep -q 'abeone-redis'; then
    if docker exec abeone-redis redis-cli ping &> /dev/null; then
        echo -e "Checking Redis... ${GREEN}✅ Healthy${NC}"
    else
        echo -e "Checking Redis... ${RED}❌ Unhealthy${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Redis container not running${NC}"
fi

# PostgreSQL
if docker ps --format '{{.Names}}' | grep -q 'abeone-postgres'; then
    if docker exec abeone-postgres pg_isready -U abeone &> /dev/null; then
        echo -e "Checking PostgreSQL... ${GREEN}✅ Healthy${NC}"
    else
        echo -e "Checking PostgreSQL... ${RED}❌ Unhealthy${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  PostgreSQL container not running${NC}"
fi

echo ""
echo "Container Status:"
docker-compose ps 2>/dev/null || docker compose ps

echo ""
echo "✅ Health check complete!"

