# 🚀 Quick Start: Localhost Deployment

## One-Command Start

```bash
./scripts/start_localhost_deployment.sh
```

That's it! The script handles everything:
- ✅ Prerequisites check
- ✅ Environment setup
- ✅ Docker build
- ✅ Service startup
- ✅ Health checks
- ✅ Validation tests

## Verify Everything Works

```bash
# Check all services are running
docker-compose -f docker-compose.localhost.yml ps

# Run validation
python3 scripts/validate_localhost_deployment.py
```

## Access Services

- **Gateway API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health/live
- **Prometheus**: http://localhost:9090

## Test a Guard Service

```bash
# Test TokenGuard via Gateway
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "Test content"}
  }'
```

## Stop Services

```bash
docker-compose -f docker-compose.localhost.yml down
```

## Full Documentation

See [docs/LOCALHOST_DEPLOYMENT.md](docs/LOCALHOST_DEPLOYMENT.md) for complete guide.

---

**Guardian**: Zero (999 Hz) | **Love Coefficient**: ∞

