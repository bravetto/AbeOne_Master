# AIGuardians - Getting Started Guide

**Welcome to AIGuardians!** This guide will help you quickly get started testing and using the system.

---

## Quick Start for Users

### Prerequisites
- Docker and Docker Compose installed
- Python 3.9+ (for running tests)
- Git

### 1. Clone and Start Services

```bash
# Clone the repository (without submodules - recommended for most users)
git clone <repository-url>
cd AIGuards-Backend-1

# Note: If you need submodule source code, see docs/SUBMODULE_CLONING_GUIDE.md
# For Docker usage, empty submodule directories won't affect functionality

# Start all services
docker-compose up -d

# Wait for services to initialize (~30 seconds)
sleep 30
```

### 2. Verify Services are Running

```bash
# Check service health
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready

# Expected response: {"status":"alive",...} and {"status":"ready",...}
```

### 3. Test the API

Run the comprehensive test suite:

```bash
cd codeguardians-gateway/codeguardians-gateway
python scripts/simple_test.py
```

Expected output: **All tests passed! (13/13)**

### 4. Use the API

#### Example: Security Scan with TokenGuard

```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "Hello, world!"}
  }'
```

#### Example: Content Validation with TrustGuard

```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "trustguard",
    "payload": {"text": "Content to validate"}
  }'
```

#### Example: Bias Detection with BiasGuard

```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "biasguard",
    "payload": {
      "operation": "detect_bias",
      "data": {"text": "Text to analyze for bias"}
    }
  }'
```

---

## Available Services

| Service | Purpose | Endpoint |
|---------|---------|----------|
| **TokenGuard** | Token optimization & cost management | `/api/v1/guards/process` (service_type: "tokenguard") |
| **TrustGuard** | Content validation & trust scoring | `/api/v1/guards/process` (service_type: "trustguard") |
| **ContextGuard** | Context management & drift detection | `/api/v1/guards/process` (service_type: "contextguard") |
| **BiasGuard** | Bias detection & mitigation | `/api/v1/guards/process` (service_type: "biasguard") |
| **HealthGuard** | Health monitoring & validation | `/api/v1/guards/process` (service_type: "healthguard") |

---

## Testing the System

### Run All Tests

```bash
cd codeguardians-gateway/codeguardians-gateway

# Functional tests (13 tests)
python scripts/simple_test.py

# Unit tests (25 tests)
python -m pytest tests/test_payload_transformation.py -v

# Integration tests (18 tests)
python -m pytest tests/test_integration.py -v
```

### Expected Results
- **Functional**: 13/13 passed (100%)
- **Unit**: 25/25 passed (100%)
- **Integration**: 18/18 passed (100%)

---

## API Documentation

### Interactive API Documentation

Once services are running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Unified Router Endpoint

**POST** `/api/v1/guards/process`

**Request Body:**
```json
{
  "service_type": "tokenguard|trustguard|contextguard|biasguard|healthguard",
  "payload": {
    "text": "Content to process",
    // Additional service-specific fields
  },
  "user_id": "optional-user-id",
  "session_id": "optional-session-id",
  "priority": 1,
  "timeout": 30,
  "fallback_enabled": true
}
```

**Response:**
```json
{
  "request_id": "uuid",
  "service_type": "tokenguard",
  "success": true,
  "data": {
    // Service-specific response data
  },
  "error": null,
  "processing_time": 0.123,
  "service_used": "tokenguard",
  "fallback_used": false
}
```

---

## Health Monitoring

```bash
# Basic health check
curl http://localhost:8000/health/live

# Readiness check (includes database & services)
curl http://localhost:8000/health/ready

# Comprehensive health check
curl http://localhost:8000/health/comprehensive

# Guard services health
curl http://localhost:8000/api/v1/guards/health
```

---

## Troubleshooting

### Services Won't Start

```bash
# Check if ports are already in use
docker ps
netstat -an | grep "8000\|5432\|6379"

# Stop conflicting services
docker stop $(docker ps -q)

# Restart
docker-compose down
docker-compose up -d
```

### Tests Failing

```bash
# Ensure services are healthy
curl http://localhost:8000/health/ready

# Check service logs
docker logs codeguardians-gateway-production
docker logs tokenguard-service
docker logs trustguard-service
```

### API Returning Errors

```bash
# Check service health
curl http://localhost:8000/api/v1/guards/health

# Verify request format
curl -v -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"service_type":"tokenguard","payload":{"text":"test"}}'
```

---

## Next Steps

### For Users
- **User Guide**: See [USER_GUIDE.md](USER_GUIDE.md) for detailed API usage
- **API Reference**: Visit http://localhost:8000/docs for interactive documentation
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

### For Developers
- **Developer Guide**: See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for development setup

- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

---

## Support

- **Issues**: https://github.com/your-repo/issues
- **Documentation**: https://docs.aiguardian.ai
- **Email**: support@aiguardian.ai

---

**Status**:  All systems operational (100% test pass rate)
**Version**: 0.1.0
**Last Updated**: 2025-10-24
