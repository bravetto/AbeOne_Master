#!/bin/bash
# Start dependencies and test containers with .env file

set -e

echo "=== Starting Dependencies ==="
docker-compose up -d postgres redis
echo "Waiting for dependencies to be healthy..."
sleep 5

echo ""
echo "=== Starting Gateway ==="
docker run --rm -d \
  --name gateway-local-test \
  -p 8000:8000 \
  --network aiguards-network \
  --env-file .env \
  -e DATABASE_HOST=codeguardians-postgres \
  -e REDIS_HOST=codeguardians-redis \
  -e ENVIRONMENT=development \
  -e DEBUG=true \
  aiguards-gateway:dev

echo "Waiting for Gateway to start..."
sleep 10

echo ""
echo "=== Starting TokenGuard ==="
docker run --rm -d \
  --name tokenguard-local-test \
  -p 8001:8000 \
  --env-file .env \
  aiguards-tokenguard:dev

echo "Waiting for TokenGuard to start..."
sleep 5

echo ""
echo "=== Testing Services ==="
echo "Gateway Health:"
curl -s http://localhost:8000/health 2>/dev/null | python -m json.tool 2>/dev/null | head -10 || echo "Gateway not responding"

echo ""
echo "TokenGuard Health:"
curl -s http://localhost:8001/health 2>/dev/null | python -m json.tool 2>/dev/null | head -10 || echo "TokenGuard not responding"

echo ""
echo "=== Status ==="
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(NAMES|gateway|tokenguard|postgres|redis)"

echo ""
echo "=== To stop containers ==="
echo "docker stop gateway-local-test tokenguard-local-test"
echo "docker-compose down"

