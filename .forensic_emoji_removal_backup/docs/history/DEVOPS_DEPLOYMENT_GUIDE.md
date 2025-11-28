# DevOps Deployment Guide

**AIGuards Backend - Production Deployment Reference**

## Overview

This guide provides DevOps engineers with everything needed to deploy and maintain the AIGuards Backend system. The application is a **multi-container microservices architecture** where all guard services route through a single gateway container.

---

## Architecture Summary

### Container Structure
- **1 Gateway Container** (`codeguardians-gateway`) - Routes all requests
- **5 Guard Service Containers** (tokenguard, trustguard, contextguard, biasguard, healthguard)
- **2 Infrastructure Containers** (postgres, redis)
- **4 Monitoring Containers** (elasticsearch, kibana, prometheus, grafana)

**Total: 12 containers** (all run in dev environment, DevOps handles production)

### Network Architecture
- All containers communicate via Docker network: `aiguards-network`
- **Only gateway exposes external port** (8000)
- Guard services are **internal-only** (accessed via gateway)
- Gateway performs request routing, load balancing, and health checks

---

## Docker Compose Configuration

### File Location
- **Single docker-compose.yml** at repository root
- **No profiles** - all services run by default (dev environment)
- **All images tagged**: `:dev`

### Key Configuration Points

```yaml
# Gateway (Main Entry Point)
codeguardians-gateway:
  image: aiguards-gateway:dev
  ports:
    - "8000:8000"  # Only external port
  environment:
    - ENVIRONMENT=development
    - DEBUG=true
  networks:
    - aiguards-network

# Guard Services (Internal Only)
tokenguard:
  image: aiguards-tokenguard:dev
  # No exposed ports - internal network only
  networks:
    - aiguards-network
```

### Required Environment Variables

**Minimum Required for Gateway:**
```bash
# Core Application
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Database (if enabled)
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_USER=aiguardian
DATABASE_PASSWORD=REPLACE_ME
DATABASE_URL=REPLACE_ME
# Redis (if enabled)
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=REPLACE_ME
REDIS_URL=redis=REPLACE_MEredis:6379/0

# AWS Secrets Manager (Production)
AWS_SECRETS_ENABLED=false  # Set to true for production
AWS_SECRETS_NAME=codeguardians-gateway/production
AWS_REGION=us-east-1
```

---

## Service Verification

### 1. Container Status Check

```bash
# Check all containers
docker-compose ps

# Expected output shows:
# - Gateway: healthy
# - Tokenguard, Trustguard, Contextguard: healthy
# - Postgres, Redis: healthy
# - Monitoring services: healthy
```

### 2. Gateway Health Endpoints

```bash
# Liveness check
curl http://localhost:8000/health/live

# Expected: {"status":"alive","service":"codeguardians-gateway"}

# Readiness check
curl http://localhost:8000/health/ready

# Expected: {"status":"ready","services":{...}}

# Service discovery
curl http://localhost:8000/api/v1/guards/services

# Expected: JSON with all available guard services
```

### 3. Test Guard Service Processing

#### TokenGuard Test
```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {
      "text": "This is a test message for token optimization",
      "content_type": "text"
    },
    "user_id": "test-user",
    "session_id": "test-session"
  }'
```

**Expected Response:**
```json
{
  "request_id": "<uuid>",
  "service_type": "tokenguard",
  "success": true,
  "data": {
    "text_length": 45,
    "confidence_score": 0.7,
    "decision": {
      "action": "keep",
      "confidence": 0.7,
      "reason": "High confidence (0.70) and acceptable length"
    },
    "recommendation": "keep",
    "processing_time_ms": 0.14
  },
  "error": null,
  "processing_time": 0.00676,
  "service_used": "tokenguard"
}
```

#### TrustGuard Test
```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "trustguard",
    "payload": {
      "validation_type": "general",
      "content": "This information is accurate and reliable",
      "validation_level": "standard"
    },
    "user_id": "test-user",
    "session_id": "test-session"
  }'
```

#### ContextGuard Test
```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "contextguard",
    "payload": {
      "text": "Sample text for context analysis",
      "content_type": "text"
    },
    "user_id": "test-user",
    "session_id": "test-session"
  }'
```

---

## Known Issues & Expected Behavior

### HealthGuard Service
**Status**: ✅ FIXED - Now healthy after database URL normalization fix
**Issue**: HealthGuard was trying to use asyncpg driver with sync SQLAlchemy engine
**Fix Applied**: 
- Added `asyncpg` dependency to `pyproject.toml`
- Added database URL normalization to convert `postgresql+asyncpg://` to `postgresql://` for sync engine
- Service now starts correctly

### BiasGuard Service
**Status**: ✅ FIXED - Now healthy after logger and Stripe initialization fixes
**Issues Fixed**: 
1. Logger utility API mismatch - Updated to accept optional context parameter
2. Stripe initialization failure - Changed to lazy initialization with null checks
**Impact**: Service now starts and runs correctly even without Stripe configuration
**Note**: Stripe-dependent endpoints return 503 if Stripe not configured (instead of crashing)

### Service Resilience
- **Gateway continues operating** even if individual guard services are down
- **Service discovery** reports status accurately
- **Fallback mechanisms** handle service unavailability gracefully
- **No single point of failure** - gateway remains functional

---

## Production Deployment Checklist

### Pre-Deployment

- [ ] **Environment Variables Configured**
  - [ ] SECRET_KEY (64+ characters, cryptographically secure)
  - [ ] DATABASE_URL (if database enabled)
  - [ ] REDIS_URL (if redis enabled)
  - [ ] AWS_SECRETS_ENABLED=true (for production)
  - [ ] AWS_SECRETS_NAME configured
  - [ ] AWS_REGION configured

- [ ] **AWS Resources Created**
  - [ ] ECR repository created: `codeguardians-gateway`
  - [ ] ECS cluster created
  - [ ] RDS PostgreSQL instance (if using managed database)
  - [ ] ElastiCache Redis cluster (if using managed cache)
  - [ ] Security groups configured
  - [ ] IAM roles and policies configured

- [ ] **Secrets Management**
  - [ ] AWS Secrets Manager secret created: `codeguardians-gateway/production`
  - [ ] Secret contains all required keys:
    - SECRET_KEY
    - DATABASE_URL
    - REDIS_URL
    - POSTGRES_PASSWORD
    - REDIS_PASSWORD
    - ALLOWED_ORIGINS
    - ALLOWED_HOSTS
  - [ ] ECS task execution role has secrets read permissions

- [ ] **Docker Images Built**
  - [ ] Gateway image built and tagged: `aiguards-gateway:dev`
  - [ ] Guard service images built (if deploying separately)
  - [ ] Images pushed to ECR (if using AWS)

### Deployment Steps

1. **Build Images** (if not using pre-built)
   ```bash
   docker-compose build
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Verify Gateway Health**
   ```bash
   curl http://localhost:8000/health/live
   curl http://localhost:8000/health/ready
   ```

4. **Verify Service Discovery**
   ```bash
   curl http://localhost:8000/api/v1/guards/services
   ```

5. **Test Guard Processing**
   ```bash
   # Test TokenGuard
   curl -X POST http://localhost:8000/api/v1/guards/process \
     -H "Content-Type: application/json" \
     -d '{"service_type":"tokenguard","payload":{"text":"test"},"user_id":"test"}'
   ```

6. **Monitor Logs**
   ```bash
   docker-compose logs -f codeguardians-gateway
   ```

### Post-Deployment Verification

- [ ] Gateway responds to health checks
- [ ] Service discovery returns all services
- [ ] At least one guard service (TokenGuard/TrustGuard/ContextGuard) processes requests successfully
- [ ] Logs show no critical errors
- [ ] Database connectivity works (if enabled)
- [ ] Redis connectivity works (if enabled)

---

## Monitoring & Logging

### Health Endpoints

| Endpoint | Purpose | Expected Response |
|----------|---------|-------------------|
| `GET /health/live` | Liveness probe | `{"status":"alive"}` |
| `GET /health/ready` | Readiness probe | `{"status":"ready"}` |
| `GET /api/v1/guards/services` | Service discovery | `{"services":{...}}` |

### Container Logs

```bash
# Gateway logs
docker-compose logs -f codeguardians-gateway

# All services logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f tokenguard
docker-compose logs -f trustguard
```

### Monitoring Services

**Prometheus** (Metrics): `http://localhost:9090`
**Grafana** (Dashboards): `http://localhost:3000` (admin/admin)
**Elasticsearch** (Logs): `http://localhost:9200`
**Kibana** (Log Visualization): `http://localhost:5601`

---

## API Endpoints Reference

### Primary Endpoint: `/api/v1/guards/process`

**Method**: `POST`
**Content-Type**: `application/json`

**Request Format:**
```json
{
  "service_type": "tokenguard|trustguard|contextguard|biasguard|healthguard",
  "payload": {
    "text": "Content to analyze",
    "content_type": "text|code|document",
    "scan_level": "standard|comprehensive"
  },
  "user_id": "optional-user-id",
  "session_id": "optional-session-id",
  "priority": 1,
  "timeout": 30,
  "fallback_enabled": true,
  "client_type": "web|vscode|chrome|api"
}
```

**Response Format:**
```json
{
  "request_id": "<uuid>",
  "service_type": "tokenguard",
  "success": true,
  "data": {
    "result": "...",
    "confidence_score": 0.95
  },
  "error": null,
  "processing_time": 0.123,
  "service_used": "tokenguard"
}
```

---

## Troubleshooting

### Gateway Not Starting

**Symptoms**: Container exits immediately or keeps restarting

**Diagnosis:**
```bash
docker-compose logs codeguardians-gateway --tail=50
```

**Common Causes:**
1. Missing SECRET_KEY environment variable
2. Invalid DATABASE_URL format (if DATABASE_ENABLED=true)
3. Invalid ALLOWED_ORIGINS format

**Fix:**
- Ensure SECRET_KEY is set (64+ characters)
- Set DATABASE_ENABLED=false if not using database
- Verify ALLOWED_ORIGINS is comma-separated string

### Guard Services Unavailable

**Symptoms**: Service discovery shows services as "unhealthy"

**Diagnosis:**
```bash
curl http://localhost:8000/api/v1/guards/services
docker-compose logs tokenguard  # Check specific service
```

**Expected Behavior:**
- Gateway continues to function
- Requests to unavailable services return error
- Other healthy services continue processing

**Fix:**
- Check guard service container logs
- Verify guard service dependencies installed
- Check network connectivity

### Database Connection Issues

**Symptoms**: Gateway logs show database connection errors

**Diagnosis:**
```bash
docker-compose logs codeguardians-gateway | grep -i database
```

**Fix:**
- Verify DATABASE_URL format: `postgresql+asyncpg://user:pass@host:5432/dbname`
- Check DATABASE_HOST points to postgres container
- Verify DATABASE_PASSWORD matches postgres container
- Ensure postgres container is healthy: `docker-compose ps postgres`

### Redis Connection Issues

**Symptoms**: Gateway logs show redis connection errors

**Diagnosis:**
```bash
docker-compose logs codeguardians-gateway | grep -i redis
```

**Fix:**
- Verify REDIS_URL format: `redis=REPLACE_MEredis:6379/0`
- Check REDIS_HOST points to redis container
- Verify REDIS_PASSWORD matches redis container
- Ensure redis container is healthy: `docker-compose ps redis`

---

## Production Environment Variables

### Required Production Settings

```bash
# Security
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# AWS Secrets Manager
AWS_SECRETS_ENABLED=true
AWS_SECRETS_NAME=codeguardians-gateway/production
AWS_REGION=us-east-1

# Database (if using managed RDS)
DATABASE_URL=REPLACE_MEDATABASE_HOST=rds-endpoint.amazonaws.com
DATABASE_PORT=5432
DATABASE_USER=<rds-user>
DATABASE_PASSWORD=REPLACE_ME

# Redis (if using managed ElastiCache)
REDIS_URL=redis=REPLACE_MEelasticache-endpoint:6379/0
REDIS_HOST=elasticache-endpoint.amazonaws.com
REDIS_PORT=6379
REDIS_PASSWORD=REPLACE_ME

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

---

## Expected Service Status

### Healthy Services (Should Work)
- ✅ **Gateway** - Main entry point
- ✅ **TokenGuard** - Token optimization
- ✅ **TrustGuard** - Trust validation
- ✅ **ContextGuard** - Context analysis
- ✅ **Postgres** - Database
- ✅ **Redis** - Cache

### Known Issues

- ✅ **All Services Operational** - All 5 guard services are healthy and working

**Note**: 
- System is 100% operational (5/5 guard services working)
- BiasGuard gracefully handles missing Stripe configuration
- HealthGuard handles database URL format automatically

---

## Quick Reference Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart gateway
docker-compose restart codeguardians-gateway

# Check service status
docker-compose ps

# Health check
curl http://localhost:8000/health/live

# Service discovery
curl http://localhost:8000/api/v1/guards/services

# Test TokenGuard
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"service_type":"tokenguard","payload":{"text":"test"},"user_id":"test"}'
```

---

## Summary

- **Single docker-compose.yml** - All services defined in one file
- **All images tagged `:dev`** - Dev environment
- **Gateway-only external port** - Port 8000
- **Resilient architecture** - Gateway continues even if guard services fail
- **Service discovery** - Automatic health checking and routing
- **DevOps handles production** - Dev environment is for testing only

For production deployment specifics, refer to AWS ECS/EKS deployment guides specific to your infrastructure setup.

