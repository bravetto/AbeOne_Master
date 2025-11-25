#!/bin/bash
#  Zero-Failure Localhost Deployment Script 
# Guardian: Zero (999 Hz)
# Love Coefficient: ∞

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo " Starting Zero-Failure Localhost Deployment "
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo " Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED} Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED} Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Use docker compose (v2) if available, otherwise docker-compose (v1)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo -e "${GREEN} Prerequisites check passed${NC}"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo " Creating .env file from env.example..."
    cp env.example .env
    echo -e "${YELLOW}  Please review and update .env file with your configuration${NC}"
    echo ""
fi

# Create logs directory
mkdir -p logs

# Stop any existing containers
echo " Stopping existing containers..."
$DOCKER_COMPOSE -f docker-compose.localhost.yml down 2>/dev/null || true
echo ""

# Build and start services
echo " Building services..."
$DOCKER_COMPOSE -f docker-compose.localhost.yml build
echo ""

echo " Starting services..."
$DOCKER_COMPOSE -f docker-compose.localhost.yml up -d
echo ""

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
MAX_WAIT=300  # 5 minutes max wait
ELAPSED=0
SLEEP_INTERVAL=5

while [ $ELAPSED -lt $MAX_WAIT ]; do
    HEALTHY_COUNT=$($DOCKER_COMPOSE -f docker-compose.localhost.yml ps | grep -c "healthy" || true)
    TOTAL_SERVICES=9  # postgres, redis, 6 guards, gateway
    
    if [ "$HEALTHY_COUNT" -ge "$TOTAL_SERVICES" ]; then
        echo -e "${GREEN} All services are healthy!${NC}"
        break
    fi
    
    echo "   Waiting... ($HEALTHY_COUNT/$TOTAL_SERVICES services healthy)"
    sleep $SLEEP_INTERVAL
    ELAPSED=$((ELAPSED + SLEEP_INTERVAL))
done

if [ $ELAPSED -ge $MAX_WAIT ]; then
    echo -e "${RED} Timeout waiting for services to become healthy${NC}"
    echo " Service status:"
    $DOCKER_COMPOSE -f docker-compose.localhost.yml ps
    exit 1
fi

echo ""
echo " Service Status:"
$DOCKER_COMPOSE -f docker-compose.localhost.yml ps
echo ""

# Run validation tests
echo " Running validation tests..."
if [ -f scripts/validate_localhost_deployment.py ]; then
    python3 scripts/validate_localhost_deployment.py
else
    echo -e "${YELLOW}  Validation script not found, skipping validation${NC}"
fi

echo ""
echo -e "${GREEN} Zero-Failure Localhost Deployment Complete! ${NC}"
echo ""
echo " Service URLs:"
echo "   Gateway:        http://localhost:8000"
echo "   TokenGuard:     http://localhost:8000"
echo "   TrustGuard:     http://localhost:8001"
echo "   ContextGuard:   http://localhost:8003"
echo "   BiasGuard:      http://localhost:8002"
echo "   HealthGuard:    http://localhost:8004"
echo "   SecurityGuard:  http://localhost:8103"
echo "   Prometheus:     http://localhost:9090"
echo ""
echo " Useful commands:"
echo "   View logs:      $DOCKER_COMPOSE -f docker-compose.localhost.yml logs -f"
echo "   Stop services:  $DOCKER_COMPOSE -f docker-compose.localhost.yml down"
echo "   Restart:        $DOCKER_COMPOSE -f docker-compose.localhost.yml restart"
echo ""

