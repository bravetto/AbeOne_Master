#!/bin/bash
# Quick test of validate_dockerfile.sh
cd "$(dirname "$0")/.."
echo "Testing Dockerfile validation..."
echo ""

# Test on a known Dockerfile
if [ -f "AIGuards-Backend-orbital/Dockerfile" ]; then
    echo "Testing: AIGuards-Backend-orbital/Dockerfile"
    head -1 "AIGuards-Backend-orbital/Dockerfile"
    echo ""
fi

# Run the actual validation
bash scripts/validate_dockerfile.sh 2>&1 | head -20

