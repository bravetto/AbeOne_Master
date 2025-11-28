#!/bin/bash
# No-Fail Local Launch Protocol
# Ensures clean startup at localhost:8000 with validation

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PORT=8000
HOST="0.0.0.0"

echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN}  CodeGuardians Gateway - No-Fail Local Launch Protocol${NC}"
echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Check port availability
echo -e "${BLUE}Step 1: Checking port ${PORT} availability...${NC}"
if lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Port ${PORT} is already in use. Checking process...${NC}"
    PID=$(lsof -Pi :${PORT} -sTCP:LISTEN -t)
    echo -e "${YELLOW}Process ${PID} is using port ${PORT}${NC}"
    read -p "Kill process ${PID}? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill -9 ${PID} 2>/dev/null || true
        sleep 1
        echo -e "${GREEN}Port ${PORT} freed${NC}"
    else
        echo -e "${RED}Aborting: Port ${PORT} is in use${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Port ${PORT} is available${NC}"
fi

# Step 2: Verify Python environment
echo -e "\n${BLUE}Step 2: Verifying Python environment...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ ${PYTHON_VERSION}${NC}"

# Step 3: Check dependencies
echo -e "\n${BLUE}Step 3: Checking dependencies...${NC}"
cd "${PROJECT_ROOT}"

MISSING_DEPS=()
if ! python3 -c "import uvicorn" 2>/dev/null; then
    MISSING_DEPS+=("uvicorn")
fi
if ! python3 -c "import fastapi" 2>/dev/null; then
    MISSING_DEPS+=("fastapi")
fi
if ! python3 -c "import httpx" 2>/dev/null; then
    MISSING_DEPS+=("httpx")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo -e "${YELLOW}Installing missing dependencies: ${MISSING_DEPS[*]}${NC}"
    python3 -m pip install -q ${MISSING_DEPS[@]} || {
        echo -e "${RED}✗ Failed to install dependencies${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ All dependencies available${NC}"
fi

# Step 4: Verify application files
echo -e "\n${BLUE}Step 4: Verifying application files...${NC}"
if [ ! -f "${PROJECT_ROOT}/app/main.py" ]; then
    echo -e "${RED}✗ app/main.py not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Application files verified${NC}"

# Step 5: Set environment variables
echo -e "\n${BLUE}Step 5: Setting environment variables...${NC}"
export ENVIRONMENT=development
export DEBUG=true
export TESTING=false
export LOG_LEVEL=INFO
export RATE_LIMIT_ENABLED=true
export ENABLE_METRICS=true

# Set defaults if not already set
export SECRET_KEY="${SECRET_KEY:-change-me-in-development-min-32-chars-replace-in-production}"
export DATABASE_ENABLED="${DATABASE_ENABLED:-false}"  # Can run without DB
export REDIS_URL="${REDIS_URL:-redis://localhost:6379/0}"

echo -e "${GREEN}✓ Environment variables set${NC}"

# Step 6: Health check function
health_check() {
    local max_attempts=30
    local attempt=1
    
    echo -e "\n${BLUE}Step 6: Waiting for server to be ready...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "http://localhost:${PORT}/health" > /dev/null 2>&1 || \
           curl -s -f "http://localhost:${PORT}/" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Server is ready on port ${PORT}${NC}"
            return 0
        fi
        
        echo -ne "${YELLOW}.${NC}"
        sleep 1
        attempt=$((attempt + 1))
    done
    
    echo -e "\n${RED}✗ Server failed to start after ${max_attempts} seconds${NC}"
    return 1
}

# Step 7: Launch server
echo -e "\n${BLUE}Step 7: Launching server...${NC}"
echo -e "${CYAN}Starting CodeGuardians Gateway on http://${HOST}:${PORT}${NC}"
echo ""

cd "${PROJECT_ROOT}"

# Start server in background
python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --reload > /tmp/gateway_server.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Verify server process is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${RED}✗ Server process died immediately${NC}"
    echo -e "${YELLOW}Last 20 lines of server log:${NC}"
    tail -20 /tmp/gateway_server.log || true
    exit 1
fi

echo -e "${GREEN}✓ Server process started (PID: ${SERVER_PID})${NC}"

# Health check
if health_check; then
    echo ""
    echo -e "${BOLD}${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${GREEN}  ✓ Server Successfully Launched${NC}"
    echo -e "${BOLD}${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Server URL: ${BOLD}http://localhost:${PORT}${NC}"
    echo -e "${CYAN}API Docs: ${BOLD}http://localhost:${PORT}/docs${NC}"
    echo -e "${CYAN}Health Endpoint: ${BOLD}http://localhost:${PORT}/health${NC}"
    echo -e "${CYAN}Metrics Endpoint: ${BOLD}http://localhost:${PORT}/metrics${NC}"
    echo ""
    echo -e "${YELLOW}Server PID: ${SERVER_PID}${NC}"
    echo -e "${YELLOW}Logs: tail -f /tmp/gateway_server.log${NC}"
    echo -e "${YELLOW}Stop: kill ${SERVER_PID}${NC}"
    echo ""
    
    # Run quick validation
    echo -e "${BLUE}Quick Validation Tests:${NC}"
    echo -n "  Health endpoint: "
    if curl -s "http://localhost:${PORT}/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
    fi
    
    echo -n "  Root endpoint: "
    if curl -s "http://localhost:${PORT}/" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
    fi
    
    echo ""
    exit 0
else
    echo ""
    echo -e "${RED}✗ Server launch failed${NC}"
    echo -e "${YELLOW}Server log:${NC}"
    tail -50 /tmp/gateway_server.log || true
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

