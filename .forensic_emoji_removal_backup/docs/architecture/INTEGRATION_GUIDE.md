# Guard Services Integration Guide

This guide explains how the real guard services are integrated into the AIGuards-Backend-2 system using git submodules and Docker containers.

## Architecture Overview

The system now uses a microservices architecture with real AI implementations:

```
┌─────────────────────────────────────────────────────────────┐
│                    CodeGuardians Gateway                    │
│                     (FastAPI + Python)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │TokenGuard│   │TrustGuard│   │ContextGuard│
   │(Python)  │   │(Python)  │   │(Python)   │
   └─────────┘   └─────────┘   └─────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                 ┌────▼────┐
                 │BiasGuard│
                 │(Node.js)│
                 └─────────┘
```

## Guard Services

### 1. TokenGuard (Port 8001)
- **Technology**: Python + FastAPI
- **Purpose**: Intelligent token pruning and response optimization
- **Features**: Confidence-based truncation, uncertainty analysis
- **Repository**: `guards/tokenguard/`
- **Key Files**: `tokenguard/pruning.py`, `main.py`

### 2. TrustGuard (Port 8002)
- **Technology**: Python + FastAPI
- **Purpose**: AI failure pattern detection
- **Features**: 7 failure patterns (hallucination, drift, bias, etc.)
- **Repository**: `guards/trust-guard/`
- **Key Files**: `trustguard/core.py`, `main.py`

### 3. ContextGuard (Port 8003)
- **Technology**: Python + FastAPI (Backend wrapper)
- **Purpose**: Context drift detection and memory management
- **Features**: 96% accuracy, context analysis, memory storage
- **Repository**: `guards/contextguard-backend/`
- **Key Files**: `main.py`, `Dockerfile`

### 4. BiasGuard (Port 8004)
- **Technology**: Node.js + Express
- **Purpose**: Bias detection and mitigation
- **Features**: Payment integration, user management, enterprise features
- **Repository**: `guards/biasguard-backend/`
- **Key Files**: `src/app.ts`, `Dockerfile`

## Git Submodules

The guard services are integrated as git submodules for easy updates:

```bash
# Initialize submodules
git submodule update --init --recursive

# Update all guard services
./scripts/update-guards.sh  # Linux/Mac
./scripts/update-guards.ps1  # Windows

# Update specific service
git submodule update --remote --merge guards/tokenguard
```

### Submodule Configuration

```ini
[submodule "guards/tokenguard"]
    path = guards/tokenguard
    url = https://github.com/bravetto/tokenguard.git
    branch = feature/migration
[submodule "guards/trust-guard"]
    path = guards/trust-guard
    url = https://github.com/bravetto/trust-guard.git
    branch = feature/internal-review-preparation
[submodule "guards/contextguard"]
    path = guards/contextguard
    url = https://github.com/bravetto/contextguard.git
    branch = feature/merge-contextguard-features
[submodule "guards/biasguard-backend"]
    path = guards/biasguard-backend
    url = https://github.com/bravetto/biasguard-backend.git
```

## Docker Compose Configuration

The services are orchestrated using Docker Compose:

```yaml
services:
  codeguardians-gateway:
    # Main gateway service
    depends_on:
      - tokenguard
      - trustguard
      - contextguard
      - biasguard

  tokenguard:
    build:
      context: ../../guards/tokenguard
    ports:
      - "8001:8001"

  trustguard:
    build:
      context: ../../guards/trust-guard
    ports:
      - "8002:8002"

  contextguard:
    build:
      context: ../../guards/contextguard-backend
    ports:
      - "8003:8003"

  biasguard:
    build:
      context: ../../guards/biasguard-backend
    ports:
      - "8004:8004"
```

## API Endpoints

### Gateway Endpoints

- `POST /api/v1/guards/process` - Process requests through guard services
- `GET /api/v1/guards/health` - Get health status of all services
- `GET /api/v1/guards/{service}/health` - Get health of specific service

### Guard Service Endpoints

#### TokenGuard
- `POST /optimize` - Optimize token usage
- `POST /generate` - Generate optimized content
- `GET /health` - Health check

#### TrustGuard
- `POST /detect` - Detect AI failure patterns
- `POST /validate` - Validate content trustworthiness
- `GET /health` - Health check

#### ContextGuard
- `POST /analyze` - Analyze context drift
- `POST /drift` - Detect context drift
- `POST /memory` - Store context data
- `GET /memory/{key}` - Retrieve context data
- `GET /health` - Health check

#### BiasGuard
- `POST /api/bias/detect` - Detect bias in content
- `POST /api/bias/analyze` - Analyze bias patterns
- `GET /health` - Health check

## Environment Configuration

### Required Environment Variables

```env
# Guard Service URLs
TOKENGUARD_URL=http://tokenguard-service:8001
TRUSTGUARD_URL=http://trustguard-service:8002
CONTEXTGUARD_URL=http://contextguard-service:8003
BIASGUARD_URL=http://biasguard-service:8004

# BiasGuard Configuration
BIASGUARD_DATABASE_URL=postgresql=REPLACE_MEpostgres:5432/biasguard_db
CLERK_SECRET_KEY=${CLERK_SECRET_KEY}
STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
```

## Development Workflow

### 1. Initial Setup

```bash
# Clone with submodules
git clone --recursive https://github.com/your-org/AIGuards-Backend-2.git
cd AIGuards-Backend-2

# Update all guard services
./scripts/update-guards.sh
```

### 2. Running the System

```bash
# Start all services
cd codeguardians-gateway/codeguardians-gateway
docker-compose up --build

# Check service health
curl http://localhost:8000/api/v1/guards/health
```

### 3. Updating Guard Services

```bash
# Update all services
./scripts/update-guards.sh

# Update specific service
git submodule update --remote --merge guards/tokenguard

# Commit changes
git add .
git commit -m "chore: update guard services"
git push
```

## Manual Updates for ECR Builds

Before building containers for ECR, ensure submodules are up to date:

```bash
# Update all guard services before ECR build
./scripts/update-guards.sh  # Linux/Mac
./scripts/update-guards.ps1  # Windows

# Verify submodule status
git submodule status

# Commit any updates
git add .
git commit -m "chore: update guard services for ECR build"
git push
```

## Testing

### Integration Tests

```bash
# Run integration tests
cd codeguardians-gateway/codeguardians-gateway
pytest tests/integration/test_real_guards.py

# Test specific service
pytest tests/integration/test_tokenguard.py
```

### Health Checks

```bash
# Check all services
curl http://localhost:8000/api/v1/guards/health

# Check specific service
curl http://localhost:8001/health  # TokenGuard
curl http://localhost:8002/health  # TrustGuard
curl http://localhost:8003/health  # ContextGuard
curl http://localhost:8004/health  # BiasGuard
```

## Monitoring

### Prometheus Metrics

Each service exposes Prometheus metrics:

- **TokenGuard**: `http://localhost:8001/metrics`
- **TrustGuard**: `http://localhost:8002/metrics`
- **ContextGuard**: `http://localhost:8003/metrics`
- **BiasGuard**: `http://localhost:8004/metrics`

### Logging

Services use structured logging with different levels:

```bash
# View logs
docker-compose logs -f tokenguard
docker-compose logs -f trustguard
docker-compose logs -f contextguard
docker-compose logs -f biasguard
```

## Troubleshooting

### Common Issues

1. **Submodule not updating**: Run `git submodule update --remote --merge`
2. **Service not starting**: Check Docker logs and health endpoints
3. **Network issues**: Verify Docker network configuration
4. **Dependencies missing**: Run `pip install -r requirements.txt`

### Debug Commands

```bash
# Check submodule status
git submodule status

# Check service health
docker-compose ps

# View service logs
docker-compose logs [service-name]

# Restart specific service
docker-compose restart [service-name]
```

## Migration from Mock Services

The original mock implementations have been archived in `archived-mocks/`:

- `archived-mocks/security-guard/` - Original SecurityGuard mock
- `archived-mocks/validation-systems/` - Original TrustGuard mock
- `archived-mocks/consciousness-core/` - Original ContextGuard mock
- `archived-mocks/neuromorphic-integration/` - Original BiasGuard mock

These are preserved for reference and can be restored if needed.

## Security Considerations

1. **Service Isolation**: Each guard service runs in its own container
2. **Network Security**: Services communicate over internal Docker network
3. **Authentication**: BiasGuard includes Clerk authentication
4. **Secrets Management**: Environment variables for sensitive data
5. **Health Monitoring**: Circuit breakers and health checks

## Performance Optimization

1. **Resource Limits**: Each service has CPU and memory limits
2. **Caching**: Redis for session and data caching
3. **Load Balancing**: Gateway handles request distribution
4. **Monitoring**: Prometheus metrics for performance tracking

## Support

For issues with guard services:

1. Check service health endpoints
2. Review Docker logs
3. Verify submodule updates
4. Check environment configuration
5. Review GitHub Actions workflow status
