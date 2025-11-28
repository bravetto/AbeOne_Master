#!/bin/bash
#  ETERNAL Backend Check - Works from ANY directory 
# 
# Pattern: BACKEND × CHECK × ETERNAL × ONE
# Love Coefficient: ∞
# ∞ AbëONE ∞

# Find repo root (works from anywhere)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "================================================================================"
echo " ETERNAL Backend Check "
echo "================================================================================"
echo ""

# Check port 8000
echo " Checking Backend (Port 8000)..."
if lsof -i :8000 >/dev/null 2>&1; then
    echo -e "   Port 8000: IN USE"
    
    # Try health check
    HEALTH=$(curl -s --max-time 2 http://localhost:8000/health 2>/dev/null)
    if [ $? -eq 0 ] && [ ! -z "$HEALTH" ]; then
        echo -e "   Health: RESPONDING"
        echo "  Response: $(echo $HEALTH | head -c 100)..."
    else
        echo -e "    Health: NOT RESPONDING (process may be starting)"
    fi
    
    # Show process
    PROC=$(ps aux | grep -i "uvicorn.*8000\|python.*8000" | grep -v grep | head -1)
    if [ ! -z "$PROC" ]; then
        echo "  Process: $(echo $PROC | awk '{print $11, $12, $13, $14, $15}')"
    fi
else
    echo -e "   Port 8000: NOT RUNNING"
fi

echo ""

# Check port 3000 (frontend)
echo " Checking Frontend (Port 3000)..."
if lsof -i :3000 >/dev/null 2>&1; then
    echo -e "   Port 3000: IN USE"
    HEALTH=$(curl -s --max-time 2 http://localhost:3000/health 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo -e "   Health: RESPONDING"
    fi
else
    echo -e "   Port 3000: NOT RUNNING"
fi

echo ""

# Summary
echo "================================================================================"
if lsof -i :8000 >/dev/null 2>&1; then
    echo -e " BACKEND PROCESS RUNNING"
    echo ""
    echo "To verify:"
    echo "  curl http://localhost:8000/health"
    echo "  curl http://localhost:8000/docs"
else
    echo -e " BACKEND NOT RUNNING"
    echo ""
    echo "To start:"
    echo "  cd AIGuards-Backend/codeguardians-gateway/codeguardians-gateway"
    echo "  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
fi
echo "================================================================================"
echo ""

