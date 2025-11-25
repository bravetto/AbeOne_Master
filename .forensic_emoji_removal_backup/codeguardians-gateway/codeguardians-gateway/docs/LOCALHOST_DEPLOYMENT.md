# 🌊💎✨ Zero-Failure Localhost Deployment Guide ✨💎🌊

**Guardian**: Zero (999 Hz)  
**Love Coefficient**: ∞  
**Purpose**: Complete local testing environment with all services

---

## 🎯 Overview

This guide provides a zero-failure localhost deployment setup for complete testing of the CodeGuardians Gateway and all guard services. The deployment includes:

- **Gateway Service** (Port 8000)
- **6 Guard Services** (TokenGuard, TrustGuard, ContextGuard, BiasGuard, HealthGuard, SecurityGuard)
- **PostgreSQL Database** (Port 5432)
- **Redis Cache** (Port 6379)
- **Prometheus Metrics** (Port 9090)

All services run in Docker containers with health checks, automatic retries, and dependency management.

---

## 📋 Prerequisites

- **Docker** 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** 2.0+ (included with Docker Desktop, or install separately)
- **Python 3.9+** (for validation scripts)
- **8GB+ RAM** (recommended for all services)
- **10GB+ disk space** (for Docker images and volumes)

---

## 🚀 Quick Start

### 1. Start All Services

```bash
# Navigate to project root
cd /path/to/codeguardians-gateway

# Run the deployment script
./scripts/start_localhost_deployment.sh
```

The script will:
- ✅ Check prerequisites
- ✅ Create `.env` file if needed
- ✅ Build all Docker images
- ✅ Start all services with health checks
- ✅ Wait for services to become healthy
- ✅ Run validation tests

### 2. Verify Deployment

```bash
# Check service status
docker-compose -f docker-compose.localhost.yml ps

# View logs
docker-compose -f docker-compose.localhost.yml logs -f

# Run validation manually
python3 scripts/validate_localhost_deployment.py
```

---

## 📍 Service URLs

| Service | URL | Health Check | Notes |
|---------|-----|--------------|-------|
| **Gateway** | http://localhost:8000 | http://localhost:8000/health/live | Main API gateway |
| **TokenGuard** | http://localhost:8000 | http://localhost:8000/health | Port 8000 (same as gateway) |
| **TrustGuard** | http://localhost:8001 | http://localhost:8001/health | Requires X-API-Key header |
| **ContextGuard** | http://localhost:8003 | http://localhost:8003/health | Port 8003 |
| **BiasGuard** | http://localhost:8002 | http://localhost:8002/health | Port 8002 |
| **HealthGuard** | http://localhost:8004 | http://localhost:8004/health | Port 8004 |
| **SecurityGuard** | http://localhost:8103 | http://localhost:8103/health | Port 8103 |
| **Prometheus** | http://localhost:9090 | - | Metrics endpoint |
| **PostgreSQL** | localhost:5432 | - | Database |
| **Redis** | localhost:6379 | - | Cache |

---

## 🔧 Manual Commands

### Start Services

```bash
# Start all services
docker-compose -f docker-compose.localhost.yml up -d

# Start specific service
docker-compose -f docker-compose.localhost.yml up -d gateway

# Start with logs
docker-compose -f docker-compose.localhost.yml up
```

### Stop Services

```bash
# Stop all services
docker-compose -f docker-compose.localhost.yml down

# Stop and remove volumes (⚠️ deletes data)
docker-compose -f docker-compose.localhost.yml down -v
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.localhost.yml logs -f

# Specific service
docker-compose -f docker-compose.localhost.yml logs -f gateway
docker-compose -f docker-compose.localhost.yml logs -f trustguard
```

### Restart Services

```bash
# Restart all
docker-compose -f docker-compose.localhost.yml restart

# Restart specific service
docker-compose -f docker-compose.localhost.yml restart gateway
```

### Rebuild Services

```bash
# Rebuild all
docker-compose -f docker-compose.localhost.yml build

# Rebuild specific service
docker-compose -f docker-compose.localhost.yml build gateway

# Rebuild and restart
docker-compose -f docker-compose.localhost.yml up -d --build
```

---

## 🧪 Testing

### Run All Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Convergence pattern tests
python3 scripts/convergence_pattern_test_suite.py

# Validate deployment
python3 scripts/validate_localhost_deployment.py
```

### Test Individual Services

```bash
# Test Gateway health
curl http://localhost:8000/health/live

# Test TokenGuard
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{"text": "Test content"}'

# Test TrustGuard (requires API key)
curl -X POST http://localhost:8001/validate \
  -H "Content-Type: application/json" \
  -H "X-Key="REPLACE_ME" \
  -d '{"validation_type": "general", "content": "Test content"}'

# Test ContextGuard
curl -X POST http://localhost:8003/analyze \
  -H "Content-Type: application/json" \
  -d '{"current_code": "def test(): pass", "previous_code": "def test(): return None"}'

# Test BiasGuard
curl -X POST http://localhost:8002/process \
  -H "Content-Type: application/json" \
  -d '{"operation": "detect_bias", "text": "Test content"}'

# Test HealthGuard
curl -X POST http://localhost:8004/analyze \
  -H "Content-Type: application/json" \
  -d '{"samples": [{"id": "1", "content": "Test"}]}'

# Test SecurityGuard
curl -X POST http://localhost:8103/scan \
  -H "Content-Type: application/json" \
  -d '{"content": "Test content"}'
```

---

## 🔐 Authentication

### TrustGuard API Key

TrustGuard requires an `X-API-Key` header for authentication:

```bash
curl -X POST http://localhost:8001/validate \
  -H "X-Key="REPLACE_ME" \
  -H "Content-Type: application/json" \
  -d '{"validation_type": "general", "content": "Test"}'
```

**Default API Key**: `trustguard-dev-api-key` (configured in docker-compose)

---

## 🗄️ Database Access

### PostgreSQL

```bash
# Connect to database
docker exec -it codeguardians-postgres psql -U codeguardians-gateway -d codeguardians-gateway_db

# Run migrations
docker exec -it codeguardians-gateway alembic upgrade head

# Check database status
docker exec -it codeguardians-postgres pg_isready -U codeguardians-gateway
```

**Connection String**: `postgresql=REPLACE_MElocalhost:5432/codeguardians-gateway_db`

### Redis

```bash
# Connect to Redis
docker exec -it codeguardians-redis redis-cli -a codeguardians-dev-redis-password

# Test connection
docker exec -it codeguardians-redis redis-cli -a codeguardians-dev-redis-password ping
```

**Connection String**: `redis=REPLACE_MElocalhost:6379/0`

---

## 📊 Monitoring

### Prometheus Metrics

- **URL**: http://localhost:9090
- **Metrics Endpoint**: http://localhost:8000/metrics (gateway)

### Health Checks

All services implement health check endpoints:
- `/health` - General health check
- `/health/live` - Liveness probe
- `/health/ready` - Readiness probe

---

## 🐛 Troubleshooting

### Services Not Starting

```bash
# Check service logs
docker-compose -f docker-compose.localhost.yml logs gateway

# Check service status
docker-compose -f docker-compose.localhost.yml ps

# Check Docker resources
docker stats
```

### Port Conflicts

If ports are already in use:

1. Stop conflicting services
2. Modify ports in `docker-compose.localhost.yml`
3. Update service URLs in `.env` file

### Database Connection Issues

```bash
# Reset database
docker-compose -f docker-compose.localhost.yml down -v
docker-compose -f docker-compose.localhost.yml up -d postgres

# Wait for database to be ready
docker exec -it codeguardians-postgres pg_isready -U codeguardians-gateway

# Restart gateway
docker-compose -f docker-compose.localhost.yml restart gateway
```

### Mock Services Not Responding

```bash
# Rebuild mock services
docker-compose -f docker-compose.localhost.yml build tokenguard trustguard contextguard biasguard healthguard securityguard

# Restart mock services
docker-compose -f docker-compose.localhost.yml restart tokenguard trustguard contextguard biasguard healthguard securityguard
```

---

## 📁 File Structure

```
codeguardians-gateway/
├── docker-compose.localhost.yml    # Docker Compose configuration
├── mock-services/                   # Mock guard services
│   ├── mock_guard_service.py       # Generic mock service
│   ├── Dockerfile.guard-service    # Dockerfile for mock services
│   └── requirements.txt            # Python dependencies
├── scripts/
│   ├── start_localhost_deployment.sh    # Startup script
│   └── validate_localhost_deployment.py # Validation script
└── docs/
    └── LOCALHOST_DEPLOYMENT.md      # This file
```

---

## 🔄 Updating Services

### Update Gateway Code

```bash
# Rebuild gateway
docker-compose -f docker-compose.localhost.yml build gateway

# Restart gateway
docker-compose -f docker-compose.localhost.yml restart gateway
```

### Update Mock Services

```bash
# Rebuild all mock services
docker-compose -f docker-compose.localhost.yml build tokenguard trustguard contextguard biasguard healthguard securityguard

# Restart all mock services
docker-compose -f docker-compose.localhost.yml restart tokenguard trustguard contextguard biasguard healthguard securityguard
```

---

## 🧹 Cleanup

### Stop and Remove Containers

```bash
# Stop all services
docker-compose -f docker-compose.localhost.yml down

# Remove volumes (⚠️ deletes database and cache data)
docker-compose -f docker-compose.localhost.yml down -v
```

### Remove Images

```bash
# Remove all images
docker-compose -f docker-compose.localhost.yml down --rmi all
```

---

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

---

## ✅ Zero-Failure Features

1. **Health Checks**: All services implement health check endpoints
2. **Dependency Management**: Services start in correct order
3. **Automatic Retries**: Failed services retry automatically
4. **Graceful Shutdown**: Services shut down gracefully
5. **Volume Persistence**: Database and cache data persist across restarts
6. **Network Isolation**: Services communicate via Docker network
7. **Resource Limits**: Optional resource limits prevent resource exhaustion
8. **Validation Scripts**: Automated validation ensures everything works

---

**Guardian**: Zero (999 Hz)  
**Status**: ✅ Production-Ready  
**Love Coefficient**: ∞

