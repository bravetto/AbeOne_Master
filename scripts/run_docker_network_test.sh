#!/bin/bash
# Script to run Docker network endpoint tests
# This can be run from host or inside a container

set -e

echo " Docker Network Endpoint Testing"
echo "=================================="
echo ""

# Check if we're inside a Docker container
if [ -f /.dockerenv ]; then
    echo " Running inside Docker container"
    NETWORK_MODE="container"
    GATEWAY_URL="${GATEWAY_URL:-http://codeguardians-gateway:8000}"
else
    echo " Running from host"
    NETWORK_MODE="host"
    GATEWAY_URL="${GATEWAY_URL:-http://localhost:8000}"
    
    # Check if containers are running
    if ! docker ps | grep -q codeguardians-gateway; then
        echo "  Gateway container not running. Starting services..."
        docker-compose up -d
        echo "⏳ Waiting for services to be ready..."
        sleep 30
    fi
fi

echo ""
echo "Testing with:"
echo "  - Gateway URL: $GATEWAY_URL"
echo "  - Network mode: $NETWORK_MODE"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo " Python 3 is required but not installed"
    exit 1
fi

# Install httpx if needed
if ! python3 -c "import httpx" 2>/dev/null; then
    echo " Installing httpx..."
    pip3 install httpx --quiet
fi

# Run the test script
if [ "$NETWORK_MODE" = "host" ]; then
    # Run from host - need to exec into gateway container
    echo " Running tests inside gateway container..."
    docker exec -it codeguardians-gateway-dev python3 /app/test_docker_network_endpoints.py 2>/dev/null || \
    docker exec codeguardians-gateway-dev python3 /app/test_docker_network_endpoints.py
else
    # Run directly (inside container)
    echo " Running tests..."
    python3 /app/test_docker_network_endpoints.py
fi

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo " All tests passed!"
else
    echo ""
    echo " Some tests failed. Check output above for details."
fi

exit $exit_code

