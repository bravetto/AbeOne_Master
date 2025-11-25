#!/bin/bash

echo "=== GUARD SERVICES FUNCTIONALITY TEST ==="

# Test guard processing endpoint with proper data
echo "Testing guard processing with valid data..."
curl -s -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"text":"This is a test message for bias detection","guard_type":"biasguard"}' | head -1

echo ""
echo "Testing guard processing with tokenguard..."
curl -s -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"content":"This is a test message for token optimization","guard_type":"tokenguard"}' | head -1

echo ""
echo "Testing unified API status..."
curl -s http://localhost:8000/api/v1/guards/status | head -2

echo ""
echo "=== END GUARD TEST ==="
