#!/bin/bash
# Start Backend Server
# Pattern: START × BACKEND × SCRIPT × ONE

set -e

echo "∞ Starting Backend Server ∞"
echo ""

BACKEND_DIR="jimmy-aiagentsuite"
PORT=${PORT:-8000}

# Check if Docker is available
if command -v docker &> /dev/null && docker info &> /dev/null; then
    echo "🐳 Using Docker..."
    echo ""
    echo "Starting backend with Docker Compose..."
    docker-compose --profile backend up -d
    
    echo ""
    echo "Waiting for backend to start..."
    sleep 5
    
    echo ""
    echo "Checking health..."
    curl -s http://localhost:${PORT}/health || echo "Backend not ready yet"
    
    echo ""
    echo "✅ Backend started!"
    echo "View logs: docker-compose logs -f backend"
    echo "Stop: docker-compose --profile backend down"
    
elif [ -d "$BACKEND_DIR" ]; then
    echo "🐍 Using Python directly..."
    echo ""
    
    cd "$BACKEND_DIR"
    
    # Check if uv is available
    if command -v uv &> /dev/null; then
        echo "Using uv..."
        uv run python -m aiagentsuite.integration.server --host 0.0.0.0 --port ${PORT}
    elif command -v python3 &> /dev/null; then
        echo "Using python3..."
        python3 -m aiagentsuite.integration.server --host 0.0.0.0 --port ${PORT}
    else
        echo "❌ Python not found"
        exit 1
    fi
else
    echo "❌ Backend directory not found: $BACKEND_DIR"
    exit 1
fi

