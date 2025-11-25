# Deployment Validation Guide

## Overview

This guide provides comprehensive validation testing for production deployment and AWS/Linkerd integration readiness.

## Test Scripts

### 1. Production Readiness Validation
**Script**: `scripts/test_production_readiness.py`

Validates all production security hardening:
- ✅ Authentication requirements
- ✅ Rate limiting configuration
- ✅ Payload size validation (10MB limit)
- ✅ URL validation
- ✅ Service name sanitization
- ✅ Error handling (404 vs 500)
- ✅ Prometheus metrics endpoint
- ✅ Aggregated health endpoint
- ✅ Circuit breaker monitoring

**Usage**:
```bash
# Basic usage
python scripts/test_production_readiness.py

# With authentication
python scripts/test_production_readiness.py --url http://api.example.com --token YOUR_AUTH_TOKEN

# JSON output
python scripts/test_production_readiness.py --json > results.json
```

### 2. AWS/Linkerd Deployment Validation
**Script**: `scripts/REPLACE_ME.py`

Validates AWS deployment and Linkerd service mesh integration:
- ✅ DNS resolution
- ✅ Kubernetes health endpoints (/health, /ready, /alive)
- ✅ Prometheus metrics endpoint accessibility
- ✅ Linkerd header handling
- ✅ Service mesh routing
- ✅ AWS environment variables
- ✅ Kubernetes readiness/liveness probes
- ✅ Service mesh timeout handling

**Usage**:
```bash
# Basic usage (production environment)
python scripts/REPLACE_ME.py --url http://api.example.com

# Staging environment with Linkerd disabled
python scripts/REPLACE_ME.py --url http://staging-api.example.com --environment staging --no-linkerd

# Custom namespace
python scripts/REPLACE_ME.py --url http://api.example.com --namespace production
```

### 3. Comprehensive Validation Suite
**Script**: `scripts/run_all_validation_tests.sh`

Orchestrates both test suites for complete validation.

**Usage**:
```bash
# Basic usage
./scripts/run_all_validation_tests.sh

# With environment variables
BASE_URL=http://api.example.com \
NAMESPACE=production \
ENVIRONMENT=production \
AUTH_TOKEN=your_token \
ADMIN_TOKEN=admin_token \
./scripts/run_all_validation_tests.sh
```

## Pre-Deployment Checklist

### Security Hardening
- [ ] All endpoints require authentication (except `/process` and `/scan` with optional Clerk token)
- [ ] Admin endpoints require admin-level authentication
- [ ] Rate limiting configured (100/5/200 per minute)
- [ ] Payload size validation (10MB limit) enforced
- [ ] URL validation prevents malicious service registration
- [ ] Service name sanitization prevents path injection

### AWS Configuration
- [ ] `ENVIRONMENT=production` set
- [ ] `DEBUG=false` set
- [ ] `SECRET_KEY` set to secure random value (32+ characters)
- [ ] `AWS_SECRETS_ENABLED=true` configured
- [ ] `AWS_REGION` set correctly
- [ ] `AWS_SECRETS_NAME` configured
- [ ] `REDIS_URL` configured (for rate limiting)
- [ ] `DATABASE_URL` configured
- [ ] `ALLOW_LOCALHOST_SERVICES=false` (production)

### Linkerd Service Mesh
- [ ] Linkerd control plane installed in cluster
- [ ] Service mesh injection enabled for namespace
- [ ] Service mesh policy configured (mTLS, etc.)
- [ ] Linkerd timeout configuration set appropriately
- [ ] Service mesh metrics integration configured

### Kubernetes Deployment
- [ ] Kubernetes deployment manifests updated
- [ ] Readiness probe configured (`/health` endpoint)
- [ ] Liveness probe configured (`/health` endpoint)
- [ ] Resource limits configured (CPU/memory)
- [ ] Service account defined with proper permissions
- [ ] ConfigMaps/Secrets mounted correctly

### Monitoring & Observability
- [ ] Prometheus scraping configured (`/metrics` endpoint)
- [ ] Prometheus alert rules configured (`prometheus_alerts.yml`)
- [ ] Alertmanager routing configured
- [ ] OpenTelemetry/Jaeger configured (JAEGER_AGENT_HOST/PORT)
- [ ] Grafana dashboards configured (optional)

## Running Validation Tests

### Local Development
```bash
# Start local server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# In another terminal, run tests
python scripts/test_production_readiness.py
```

### Docker Container
```bash
# Build and run container
docker build -t codeguardians-gateway .
docker run -p 8000:8000 codeguardians-gateway

# Run tests against container
python scripts/test_production_readiness.py --url http://localhost:8000
```

### Kubernetes Cluster
```bash
# Port forward to service
kubectl port-forward svc/codeguardians-gateway 8000:8000 -n production

# Run tests
python scripts/test_production_readiness.py --url http://localhost:8000
python scripts/REPLACE_ME.py --url http://localhost:8000 --namespace production
```

### CI/CD Pipeline Integration
```yaml
# Example GitHub Actions workflow
- name: Run Production Readiness Tests
  run: |
    python scripts/test_production_readiness.py \
      --url http://localhost:8000 \
      --json > production-readiness.json

- name: Run AWS/Linkerd Tests
  run: |
    python scripts/REPLACE_ME.py \
      --url http://localhost:8000 \
      --namespace ${NAMESPACE} \
      --environment production \
      --json > aws-linkerd.json
```

## Expected Test Results

### Production Readiness
All tests should pass:
- ✅ Authentication Required (Read Endpoints)
- ✅ Admin Endpoints Require Admin Access
- ✅ Rate Limiting Metrics Headers Present
- ✅ Payload Size Validation (10MB Limit)
- ✅ URL Validation
- ✅ Service Name Sanitization
- ✅ 404 Error Handling (Unregister Service)
- ✅ Prometheus Metrics Endpoint
- ✅ Aggregated Health Endpoint
- ✅ Circuit Breaker Monitoring Endpoint

### AWS/Linkerd Deployment
All tests should pass:
- ✅ DNS Resolution
- ✅ Kubernetes Health Endpoint
- ✅ Prometheus Metrics Endpoint (Secure)
- ✅ Linkerd Headers Present (if enabled)
- ✅ Service Mesh Routing
- ✅ AWS Environment Variables
- ✅ Kubernetes Readiness Probe
- ✅ Kubernetes Liveness Probe
- ✅ Service Mesh Timeout Handling

## Troubleshooting

### Authentication Failures
```bash
# Ensure token is valid
curl -H "Authorization: Bearer YOUR_TOKEN" http://api.example.com/api/v1/guards/health

# Check token format
# Should be: Authorization: Bearer <token>
```

### DNS Resolution Issues
```bash
# Test DNS resolution
nslookup api.example.com

# Check /etc/hosts for local overrides
cat /etc/hosts
```

### Linkerd Issues
```bash
# Check Linkerd installation
linkerd version

# Check service mesh injection
kubectl get pods -n production -o jsonpath='{.items[*].metadata.annotations.linkerd\.io/inject}'

# Check Linkerd dashboard
linkerd dashboard
```

### Metrics Endpoint Issues
```bash
# Test metrics endpoint
curl http://api.example.com/metrics

# Check Prometheus scraping configuration
# Should include: /metrics path
```

## Post-Deployment Validation

After deployment, validate:
1. Health checks responding (`/health`, `/ready`, `/alive`)
2. Metrics endpoint accessible (`/metrics`)
3. Authentication working (all endpoints secured)
4. Rate limiting configured (check headers)
5. Service mesh routing working (check Linkerd dashboard)
6. Prometheus scraping metrics
7. Alertmanager receiving alerts (verify alert rules)
8. OpenTelemetry traces appearing in Jaeger

## Support

For issues or questions:
- Review test outputs for specific error messages
- Check application logs: `kubectl logs -n production deployment/codeguardians-gateway`
- Check Linkerd logs: `linkerd logs -n production deploy/codeguardians-gateway`
- Review `API_ORCHESTRATOR_CHANGES.md` for API changes
- Review `env.template` for environment variable documentation

