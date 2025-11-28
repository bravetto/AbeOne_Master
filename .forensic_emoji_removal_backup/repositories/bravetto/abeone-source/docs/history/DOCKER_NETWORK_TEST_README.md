# Docker Network Endpoint Testing

This directory contains scripts to test guard service endpoints using Docker network simulation.

## Purpose

These scripts simulate the gateway's behavior when calling guard services, verifying:
- ✅ URL construction (base_url + endpoint)
- ✅ Endpoint paths match service definitions
- ✅ Service health and availability
- ✅ Authentication headers (X-Gateway-Request)
- ✅ Direct service endpoints
- ✅ Gateway routing

## Scripts

### 1. `test_docker_network_endpoints.py`
Main test script that:
- Tests URL construction logic
- Checks service health endpoints
- Tests direct service endpoints (simulating gateway calls)
- Tests services through the gateway

### 2. `run_docker_network_test.sh`
Helper script to run tests either:
- From host machine (executes inside gateway container)
- Inside Docker container directly

## Usage

### Option 1: Run from Host (Recommended)

```bash
# Make sure services are running
docker-compose up -d

# Run tests
./run_docker_network_test.sh
```

Or manually:
```bash
# Copy test script into gateway container
docker cp test_docker_network_endpoints.py codeguardians-gateway-dev:/app/

# Run tests inside gateway container
docker exec codeguardians-gateway-dev python3 /app/test_docker_network_endpoints.py
```

### Option 2: Run Inside Gateway Container

```bash
# Enter gateway container
docker exec -it codeguardians-gateway-dev bash

# Copy script if needed
# (or mount it as volume in docker-compose.yml)

# Run tests
python3 /app/test_docker_network_endpoints.py
```

### Option 3: Run as Standalone Container

```bash
# Use a test container on the same network
docker run --rm \
  --network aiguards-network \
  -v $(pwd)/test_docker_network_endpoints.py:/app/test.py \
  python:3.11-slim \
  bash -c "pip install httpx && python /app/test.py"
```

## Test Coverage

The script tests all guard services:

1. **TokenGuard** (`tokenguard:8000`)
   - Endpoint: `/scan`
   - Health: `/health`

2. **TrustGuard** (`trustguard:8000`)
   - Endpoint: `/v1/validate`
   - Health: `/health`

3. **ContextGuard** (`contextguard:8000`)
   - Endpoint: `/analyze`
   - Health: `/health`

4. **BiasGuard** (`biasguard:8000`)
   - Endpoint: `/analyze`
   - Health: `/health`

5. **HealthGuard** (`healthguard:8000`)
   - Endpoint: `/analyze`
   - Health: `/health`

6. **SecurityGuard** (`securityguard:8000`)
   - Endpoint: `/scan`
   - Health: `/health`

## Test Output

The script provides colored output showing:
- ✅ Green checkmarks for passing tests
- ❌ Red X for failing tests
- 📊 Summary statistics
- 🔍 Detailed error information for failures

## Expected Results

### Success Scenario
```
✓ URL Construction: PASS
✓ Health Checks: 6/6 passed
✓ Direct Endpoints: 6/6 passed
✓ Gateway Endpoints: 6/6 passed
✅ ALL TESTS PASSED
```

### Failure Scenarios

**404 Not Found:**
```
✗ trustguard endpoint test
     URL: http://trustguard:8000/v1/validate
     error: 404 Not Found
     status_code: 404
```

**Connection Error:**
```
✗ trustguard health check
     error: Connection error: Connection refused
```

**Authentication Error:**
```
✗ trustguard endpoint test
     error: Authentication/Authorization issue: 403
     status_code: 403
```

## Troubleshooting

### Services Not Reachable

1. **Check if services are running:**
   ```bash
   docker-compose ps
   ```

2. **Check network connectivity:**
   ```bash
   docker exec codeguardians-gateway-dev ping -c 2 trustguard
   docker exec codeguardians-gateway-dev curl http://trustguard:8000/health
   ```

3. **Check service logs:**
   ```bash
   docker-compose logs trustguard
   docker-compose logs contextguard
   ```

### Port Issues

Verify service ports match configuration:
- `docker-compose.yml` shows services on port 8000 internally
- Environment variables: `TRUSTGUARD_URL=http://trustguard:8000`

### Authentication Issues

TrustGuard requires `X-Gateway-Request: true` header:
- Script automatically includes this header
- If 403 errors occur, verify TrustGuard authentication middleware

## Integration with CI/CD

```yaml
# Example GitHub Actions workflow
- name: Test Docker Network Endpoints
  run: |
    docker-compose up -d
    sleep 30  # Wait for services
    docker exec codeguardians-gateway-dev python3 /app/test_docker_network_endpoints.py
```

## Files Modified

This test verifies fixes made in:
- `codeguardians-gateway/codeguardians-gateway/app/core/guard_orchestrator.py`
  - URL construction with trailing slash handling
  - Enhanced error logging
  - SecurityGuard registration


