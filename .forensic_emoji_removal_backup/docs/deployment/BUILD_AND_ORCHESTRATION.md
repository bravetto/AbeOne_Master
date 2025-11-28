# AIGuards Backend - Container Build & Orchestration Guide

This guide explains how to build all container images individually and orchestrate them through the unified gateway using Docker Compose.

## 📋 Overview

The AIGuards Backend consists of:
- **1 Gateway Service** - Unified API gateway (`codeguardians-gateway`)
- **5 Guard Services** - Specialized AI security services
  - TokenGuard - Token optimization & cost management
  - TrustGuard - Trust validation & reliability
  - ContextGuard - Context drift detection & memory management
  - BiasGuard - Bias detection & content analysis
  - HealthGuard - Health monitoring & validation
- **2 Infrastructure Services** - PostgreSQL & Redis

## 🏗️ Building Images Individually

### Option 1: Using Bash Script (Linux/Mac/Git Bash)

```bash
# Make script executable (if needed)
chmod +x scripts/build-all-images.sh

# Build all images with default tag (dev)
./scripts/build-all-images.sh

# Build with custom tag
IMAGE_TAG=latest ./scripts/build-all-images.sh
```

### Option 2: Using PowerShell Script (Windows)

```powershell
# Build all images with default tag (dev)
.\scripts\build-all-images.ps1

# Build with custom tag
.\scripts\build-all-images.ps1 -ImageTag latest
```

### Option 3: Manual Build

Build each image individually:

```bash
# Gateway
docker build -t aiguards-gateway:dev \
  -f ./codeguardians-gateway/codeguardians-gateway/Dockerfile \
  ./codeguardians-gateway/codeguardians-gateway

# TokenGuard
docker build -t aiguards-tokenguard:dev \
  -f ./guards/tokenguard/Dockerfile \
  ./guards/tokenguard

# TrustGuard
docker build -t aiguards-trustguard:dev \
  -f ./guards/trust-guard/Dockerfile \
  ./guards/trust-guard

# ContextGuard
docker build -t aiguards-contextguard:dev \
  -f ./guards/contextguard/Dockerfile \
  ./guards/contextguard

# BiasGuard
docker build -t aiguards-biasguard:dev \
  -f ./guards/biasguard-backend/Dockerfile \
  ./guards/biasguard-backend

# HealthGuard
docker build -t aiguards-healthguard:dev \
  -f ./guards/healthguard/Dockerfile \
  ./guards/healthguard
```

## 🚀 Orchestrating with Docker Compose

The `docker-compose.yml` file orchestrates all services through the unified gateway.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│              External Clients                           │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│         codeguardians-gateway (Port 8000)                │
│         Unified API Gateway & Orchestrator               │
└──┬──────────┬──────────┬──────────┬──────────┬──────────┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│Token│  │Trust│  │Ctx  │  │Bias │  │Hlth │
│Guard│  │Guard│  │Guard│  │Guard│  │Guard│
└──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘
   │        │        │        │        │
   └────────┴────────┴────────┴────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
    ┌─────────┐        ┌─────────┐
    │Postgres │        │  Redis  │
    └─────────┘        └─────────┘
```

### Starting All Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop all services
docker-compose down
```

### Service Discovery

The gateway automatically discovers all guard services via Docker's internal DNS:

- `tokenguard:8000` - TokenGuard service
- `trustguard:8000` - TrustGuard service
- `contextguard:8000` - ContextGuard service
- `biasguard:8000` - BiasGuard service
- `healthguard:8000` - HealthGuard service

These URLs are configured via environment variables:
- `TOKENGUARD_URL=http://tokenguard:8000`
- `TRUSTGUARD_URL=http://trustguard:8000`
- `CONTEXTGUARD_URL=http://contextguard:8000`
- `BIASGUARD_URL=http://biasguard:8000`
- `HEALTHGUARD_URL=http://healthguard:8000`

### Health Checks & Dependencies

The docker-compose.yml is configured with:
- **Health checks** for all services
- **Dependency management** - Gateway waits for all guard services to be healthy
- **Automatic restart** - Services restart on failure
- **Internal networking** - All services communicate via `aiguards-network`

### Startup Order

1. **Infrastructure** (PostgreSQL, Redis) - Start first
2. **Guard Services** - Start after infrastructure is healthy
3. **Gateway** - Starts last, after all guard services are healthy

## 🧪 Testing the Setup

After starting all services:

```bash
# Check gateway health
curl http://localhost:8000/health/live

# Check all services via gateway
curl http://localhost:8000/api/v1/guards/services

# Test a guard service through gateway
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {
      "text": "Test content",
      "confidence": 0.7
    }
  }'
```

## 📊 Monitoring

### View Service Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f codeguardians-gateway
docker-compose logs -f tokenguard
docker-compose logs -f trustguard
```

### Check Service Health

```bash
# Check container health status
docker-compose ps

# Check individual service health
docker inspect codeguardians-gateway-dev --format='{{.State.Health.Status}}'
docker inspect codeguardians-tokenguard --format='{{.State.Health.Status}}'
```

## 🔧 Troubleshooting

### Images Not Building

1. Check Dockerfile exists in each service directory
2. Verify build context paths are correct
3. Check for dependency issues in requirements.txt

### Services Not Starting

1. Check health check logs: `docker-compose logs <service-name>`
2. Verify environment variables in `.env` file
3. Check network connectivity: `docker network inspect aiguards-network`

### Gateway Can't Reach Guard Services

1. Verify all services are on `aiguards-network`
2. Check service discovery URLs are correct
3. Verify guard services are healthy before gateway starts

## 📝 Environment Variables

Key environment variables (set in `.env`):

```bash
# Database
DATABASE_URL=REPLACE_MEPOSTGRES_PASSWORD=REPLACE_ME

# Redis
REDIS_URL=redis=REPLACE_MEredis:6379/0
REDIS_PASSWORD=REPLACE_ME

# API Keys
UNIFIED_API_KEY=your-api-key-here

# Logging
LOG_LEVEL=INFO
```

## 🎯 Next Steps

1. **Build all images**: `./scripts/build-all-images.sh`
2. **Start services**: `docker-compose up -d`
3. **Verify health**: `docker-compose ps`
4. **Test API**: Use the test endpoints above
5. **Monitor logs**: `docker-compose logs -f`

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Service Documentation](./docs/README.md)
- [API Documentation](./docs/api/README.md)

