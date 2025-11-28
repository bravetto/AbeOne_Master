#!/bin/bash

echo "=== QUICK ENDPOINT TEST ==="

# Test endpoints that were failing
echo "Testing /health..."
curl -s -m 3 http://localhost:8000/health | head -1

echo "Testing /api/v1/posts/..."
curl -s -m 3 -w "%{http_code}" -o /dev/null http://localhost:8000/api/v1/posts/

echo "Testing /api/v1/subscriptions/tiers..."
curl -s -m 3 -w "%{http_code}" -o /dev/null http://localhost:8000/api/v1/subscriptions/tiers

echo "Testing /api/v1/guards/process..."
curl -s -m 3 -w "%{http_code}" -o /dev/null -X POST -H "Content-Type: application/json" -d '{"text":"test"}' http://localhost:8000/api/v1/guards/process

echo "=== END TEST ==="
