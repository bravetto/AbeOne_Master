# Danny's AWS/Linkerd Virtual Environment Testing Guide

**For**: Danny Brody (Infrastructure Excellence Master)  
**Purpose**: Complete virtual testing environment for AWS/Linkerd failure pattern detection  
**Date**: November 3, 2025

---

## Executive Summary

This guide provides a complete virtual testing environment for validating AWS/Linkerd deployment readiness. The system includes:

1. **Virtual Scenario Simulator**: Emulates 11 AWS/Linkerd failure patterns
2. **Pattern Detection Scripts**: Detects failure signatures without modifying codebase
3. **Production Readiness Tests**: Validates security, metrics, and deployment readiness
4. **AWS/Linkerd Integration Tests**: Validates deployment compatibility

**Key Benefit**: Test failure patterns in isolated virtual environment before production deployment.

---

## Quick Start

### Prerequisites

```bash
# Check Python 3
python3 --version  # Should be 3.9+

# Install dependencies
pip3 install httpx fastapi uvicorn

# Verify AWS CLI
aws --version

# Verify Docker
docker --version
```

### One-Command Setup

```bash
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway

# Run all virtual scenarios
./scripts/run_virtual_scenarios.sh
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Virtual Scenario Simulator (scenario_simulator.py)     │
│  - Simulates 11 failure patterns                        │
│  - FastAPI server (port 9001)                          │
│  - Pattern-specific behavior injection                 │
└───────────────────┬───────────────────────────────────┘
                    │ HTTP Request
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Pattern Detection Scripts                              │
│  - REPLACE_ME.py                    │
│  - test_linkerd_failure_patterns.py                     │
│  - REPLACE_ME.py            │
│  - test_forensic_signatures.py                         │
└─────────────────────────────────────────────────────────┘
                    │ Results
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Production Deployment                                   │
│  - AWS ECR: gateway:dev                                 │
│  - EKS/ECS/Kubernetes                                   │
│  - Linkerd service mesh                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Virtual Scenario Simulator

### Available Patterns (11)

#### AWS NLB Patterns (7)
1. **`flow_table_exhaustion`** - NLB flow table exhaustion (silent rejections)
2. **`idle_timeout`** - NLB idle timeout (~350s) causing connection resets
3. **`target_group_saturation`** - ALB target group saturation (503 errors)
4. **`dns_dead_ip`** - ALB DNS resolution to dead IPs
5. **`keep_alive_mismatch`** - Keep-alive timeout mismatches
6. **`rst_pattern`** - TCP RST packet patterns
7. **`connection_refused`** - Connection refused errors

#### Linkerd Patterns (4)
8. **`circuit_breaker`** - Circuit breaker trips (7 consecutive failures)
9. **`proxy_timeout`** - Linkerd proxy timeout (10s default)
10. **`stream_exhaustion`** - HTTP/2 stream exhaustion
11. **`timeout_cascade`** - NLB + Linkerd timeout cascade

---

## Usage Guide

### Scenario 1: Test Circuit Breaker Pattern

```bash
# Terminal 1: Start simulator
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway

python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001

# Terminal 2: Run detection tests
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001
```

**Expected Output**:
```
⚠ PATTERNS DETECTED
  ⚠ Failure streak of 7 detected (threshold: 7)
```

---

### Scenario 2: Test Flow Table Exhaustion

```bash
# Start simulator
python scripts/scenario_simulator.py --pattern flow_table_exhaustion --port 9001

# Test detection
python scripts/REPLACE_ME.py --url http://localhost:9001
```

**Expected Output**:
```
⚠ ISSUES DETECTED
  ⚠ High timeout rate: 30.0%
  ⚠ Multiple slow connections: 3/10
```

---

### Scenario 3: Run All Scenarios Automatically

```bash
./scripts/run_virtual_scenarios.sh

# Or specific pattern
./scripts/run_virtual_scenarios.sh circuit_breaker
```

---

## Test Scripts Reference

### 1. AWS NLB Failure Pattern Detection

**Script**: `scripts/REPLACE_ME.py`

**Tests**:
- Connection timing patterns (flow table exhaustion)
- NLB idle timeout signatures
- DNS resolution issues
- Keep-alive configuration mismatches
- Response error patterns (503/502)

**Usage**:
```bash
python scripts/REPLACE_ME.py --url http://localhost:9001

# With JSON output
python scripts/REPLACE_ME.py --url http://localhost:9001 --json
```

---

### 2. Linkerd Service Mesh Failure Pattern Detection

**Script**: `scripts/test_linkerd_failure_patterns.py`

**Tests**:
- Circuit breaker patterns (7+ consecutive failures)
- Connection refused (OS error 111)
- HTTP/2 stream exhaustion
- Proxy timeout patterns (10s)

**Usage**:
```bash
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001
```

---

### 3. AWS/Linkerd Integration Pattern Detection

**Script**: `scripts/REPLACE_ME.py`

**Tests**:
- Timeout cascade (NLB → Linkerd circuit breaker)
- gRPC stream exhaustion behind NLB
- ALB gateway 502 patterns

**Usage**:
```bash
python scripts/REPLACE_ME.py --url http://localhost:9001

# Without Linkerd (if testing AWS only)
python scripts/REPLACE_ME.py --url http://localhost:9001 --no-linkerd
```

---

### 4. Forensic Signature Detection

**Script**: `scripts/test_forensic_signatures.py`

**Tests**:
- Error code classification (502, 503, 504)
- TCP RST packet patterns
- Timeout distributions

**Usage**:
```bash
python scripts/test_forensic_signatures.py --url http://localhost:9001
```

---

### 5. Production Readiness Validation

**Script**: `scripts/test_production_readiness.py`

**Tests**:
- Authentication requirements
- Rate limiting
- Payload size validation
- Prometheus metrics
- Health endpoints

**Usage**:
```bash
# Without auth tokens (security testing)
python scripts/test_production_readiness.py --url http://localhost:8000

# With auth tokens (full validation)
python scripts/test_production_readiness.py \
  --url http://localhost:8000 \
  --token YOUR_USER_TOKEN \
  --admin-token YOUR_ADMIN_TOKEN
```

---

### 6. AWS/Linkerd Deployment Readiness

**Script**: `scripts/REPLACE_ME.py`

**Tests**:
- DNS resolution
- Kubernetes health probes
- Prometheus metrics endpoint
- Linkerd headers
- Service mesh routing

**Usage**:
```bash
python scripts/REPLACE_ME.py \
  --url http://localhost:8000 \
  --namespace default \
  --no-linkerd  # If Linkerd not enabled
```

---

## Complete Test Workflow

### Workflow 1: Virtual Pattern Testing

```bash
# Step 1: Start virtual scenario
python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001

# Step 2: Run detection tests (in another terminal)
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001

# Step 3: Analyze results
# Look for: ⚠ PATTERNS DETECTED with specific recommendations
```

---

### Workflow 2: Production Deployment Validation

```bash
# Step 1: Ensure server is running
python scripts/launch_no_fail_local.sh

# Step 2: Run production readiness tests
python scripts/test_production_readiness.py --url http://localhost:8000

# Step 3: Run AWS/Linkerd deployment tests
python scripts/REPLACE_ME.py --url http://localhost:8000

# Step 4: Run comprehensive validation
./scripts/run_all_validation_tests.sh --url http://localhost:8000
```

---

### Workflow 3: Pre-Deployment Checklist

```bash
# 1. Test locally
./scripts/launch_no_fail_local.sh

# 2. Validate production readiness
python scripts/test_production_readiness.py --url http://localhost:8000 --json > prod_results.json

# 3. Test AWS/Linkerd compatibility
python scripts/REPLACE_ME.py --url http://localhost:8000 --json > aws_results.json

# 4. Run virtual scenarios
./scripts/run_virtual_scenarios.sh > scenario_results.txt

# 5. Review all results
cat prod_results.json aws_results.json scenario_results.txt
```

---

## AWS ECR Deployment

### Current Configuration

- **ECR Repository**: `gateway`
- **Image Tag**: `dev`
- **ECR URI**: `730335329303.dkr.ecr.us-east-1.amazonaws.com/gateway:dev`
- **Architecture**: AMD64 (`linux/amd64`)
- **Region**: `us-east-1`
- **Account**: `730335329303`

### Deployment Script

**Script**: `push-to-ecr.sh`

**Key Features**:
- ✅ AMD64 build (`--platform linux/amd64`)
- ✅ AWS SSO support (profile `mxm0118`)
- ✅ Automatic ECR authentication
- ✅ Repository creation if needed

**Usage**:
```bash
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway

# Login to AWS SSO first
aws sso login --profile mxm0118
export AWS_PROFILE=mxm0118

# Push to ECR
./push-to-ecr.sh

# Or with custom tag
TAG=production ./push-to-ecr.sh
```

---

## Kubernetes Deployment Configuration

### Recommended Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codeguardians-gateway
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: codeguardians-gateway
  template:
    metadata:
      labels:
        app: codeguardians-gateway
      annotations:
        linkerd.io/inject: enabled
    spec:
      containers:
      - name: gateway
        image: 730335329303.dkr.ecr.us-east-1.amazonaws.com/gateway:dev
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: AWS_REGION
          value: "us-east-1"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: codeguardians-gateway
  namespace: default
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: LoadBalancer
  selector:
    app: codeguardians-gateway
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
```

---

## Linkerd Integration

### Service Profile Configuration

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: codeguardians-gateway
  namespace: default
spec:
  routes:
  - name: guard-services
    condition:
      method: POST
      pathRegex: "/api/v1/guards/process"
    timeout: 30s
    retries:
      budget:
        retryRatio: 0.3
        minRetriesPerSecond: 1
        ttl: 60s
      timeout: 30s
      backoff:
        kind: exponential
        minMs: 10
        maxMs: 10000
  - name: health-checks
    condition:
      method: GET
      pathRegex: "/health"
    isRetryable: false
  - name: metrics
    condition:
      method: GET
      pathRegex: "/metrics"
    isRetryable: false
```

### Circuit Breaker Configuration

```bash
kubectl annotate service codeguardians-gateway \
  balancer.linkerd.io/failure-accrual=consecutive \
  balancer.linkerd.io/failure-accrual-consecutive-max-failures=10 \
  balancer.linkerd.io/failure-accrual-consecutive-min-penalty=1s \
  balancer.linkerd.io/failure-accrual-consecutive-max-penalty=30s \
  -n default
```

---

## AWS Load Balancer Configuration

### NLB Configuration Recommendations

**Idle Timeout**: Reduce from 350s to 60s (if supported) or implement TCP keepalive

```bash
# Application-level TCP keepalive (< 350s)
sysctl -w net.ipv4.tcp_keepalive_time=120
sysctl -w net.ipv4.tcp_keepalive_intvl=30
sysctl -w net.ipv4.tcp_keepalive_probes=3
```

**ALB Configuration**:

```yaml
# Ensure backend keep-alive > ALB idle timeout (60s)
# Backend: 65s, ALB: 60s (recommended)
```

---

## Monitoring & Observability

### CloudWatch Metrics to Monitor

**NLB Metrics**:
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/NetworkELB \
  --metric-name RejectedFlowCount \
  --dimensions Name=LoadBalancer,Value=net/my-nlb/... \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

**ALB Metrics**:
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name HTTPCode_ELB_503_Count \
  --dimensions Name=LoadBalancer,Value=app/my-alb/... \
  --period 300 \
  --statistics Sum
```

### Linkerd Metrics

```bash
# Via linkerd viz
linkerd viz stat deployment -n default

# Check circuit breaker state
linkerd viz stat deployment/codeguardians-gateway -n default --from deployment/client

# View failures
linkerd viz tap deployment/codeguardians-gateway -n default | grep fail-fast
```

---

## Troubleshooting Guide

### Issue: Virtual Scenario Not Starting

```bash
# Check if port 9001 is available
lsof -i :9001

# Check FastAPI installation
python3 -c "import fastapi; print('OK')"

# Install if needed
pip3 install fastapi uvicorn
```

### Issue: Pattern Not Detected

1. Verify simulator is running correct pattern
2. Check test URL matches simulator URL
3. Review detection test logs
4. Ensure pattern behavior matches expected signatures

### Issue: AWS Authentication Failed

```bash
# Check SSO login status
aws sts get-caller-identity --profile mxm0118

# If expired, login
aws sso login --profile mxm0118

# Set profile
export AWS_PROFILE=mxm0118
```

### Issue: ECR Push Failed

```bash
# Verify AWS credentials
aws sts get-caller-identity --profile mxm0118

# Check ECR access
aws ecr get-login-password --region us-east-1 --profile mxm0118

# Verify Docker login
docker login 730335329303.dkr.ecr.us-east-1.amazonaws.com
```

---

## Test Scripts Cheat Sheet

| Script | Purpose | Target URL | Auth Required |
|--------|---------|------------|---------------|
| `scenario_simulator.py` | Simulate failure patterns | `http://localhost:9001` | No |
| `REPLACE_ME.py` | Detect NLB patterns | `http://localhost:9001` | No |
| `test_linkerd_failure_patterns.py` | Detect Linkerd patterns | `http://localhost:9001` | No |
| `REPLACE_ME.py` | Detect integration patterns | `http://localhost:9001` | No |
| `test_forensic_signatures.py` | Detect forensic signatures | `http://localhost:9001` | No |
| `test_production_readiness.py` | Validate production readiness | `http://localhost:8000` | Optional (tokens) |
| `REPLACE_ME.py` | Validate AWS/Linkerd deployment | `http://localhost:8000` | No |
| `run_virtual_scenarios.sh` | Run all scenarios | Auto | No |
| `push-to-ecr.sh` | Deploy to ECR | ECR | AWS SSO |

---

## Quick Reference Commands

### Start Virtual Environment

```bash
# Single scenario
python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001

# All scenarios (automated)
./scripts/run_virtual_scenarios.sh
```

### Test Pattern Detection

```bash
# AWS NLB patterns
python scripts/REPLACE_ME.py --url http://localhost:9001

# Linkerd patterns
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001

# Integration patterns
python scripts/REPLACE_ME.py --url http://localhost:9001

# Forensic signatures
python scripts/test_forensic_signatures.py --url http://localhost:9001
```

### Validate Production Deployment

```bash
# Start server
./scripts/launch_no_fail_local.sh

# Production readiness
python scripts/test_production_readiness.py --url http://localhost:8000

# AWS/Linkerd deployment
python scripts/REPLACE_ME.py --url http://localhost:8000

# Comprehensive validation
./scripts/run_all_validation_tests.sh
```

### Deploy to ECR

```bash
# Login to AWS SSO
aws sso login --profile mxm0118
export AWS_PROFILE=mxm0118

# Push to ECR
./push-to-ecr.sh
```

---

## Pattern Detection Reference

### AWS NLB Patterns

| Pattern | Detection Method | CloudWatch Metric | Mitigation |
|---------|----------------|-------------------|------------|
| Flow Table Exhaustion | Timing analysis | `RejectedFlowCount` | Reduce idle timeout |
| Idle Timeout | Connection reset patterns | `TCP_ELB_Reset_Count` | TCP keepalive < 350s |
| Source Port Collision | RST packet analysis | `TCP_ELB_Reset_Count` | Multiple NLB IPs |
| Target Group Saturation | 503 error detection | `HTTPCode_ELB_503_Count` | Autoscaling |

### Linkerd Patterns

| Pattern | Detection Method | Linkerd Metric | Mitigation |
|---------|----------------|----------------|------------|
| Circuit Breaker | Failure streak (7+) | `request_total{classification="failure"}` | Increase threshold |
| Connection Refused | OS error 111 | Connection errors | Bind to 0.0.0.0 |
| Stream Exhaustion | Concurrency testing | `open_streams` | Increase max_concurrent_streams |
| Proxy Timeout | Timing >10s | `response_latency_ms_p99` | ServiceProfile timeout |

---

## Integration Testing Scenarios

### Scenario A: NLB → Linkerd → Application

```bash
# 1. Start simulator with timeout cascade pattern
python scripts/scenario_simulator.py --pattern timeout_cascade --port 9001

# 2. Run integration detection tests
python scripts/REPLACE_ME.py --url http://localhost:9001

# 3. Verify cascade detection
# Expected: Reset errors + Circuit breaker indicators
```

### Scenario B: gRPC Behind NLB

```bash
# 1. Simulate stream exhaustion
python scripts/scenario_simulator.py --pattern stream_exhaustion --port 9001

# 2. Test Linkerd patterns
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001

# 3. Verify stream limit detection
# Expected: High error rate at concurrency >50
```

---

## Configuration Files

### Virtual Scenario Config

Located: `scripts/scenario_simulator.py`

**Configurable**:
- Port (default: 9001)
- Pattern behavior
- Failure thresholds
- Timeout values

### Production Config

Located: `config/runtime.json`

**Configurable**:
- Rate limits
- Cache settings
- Security headers
- Feature flags

### Environment Config

Located: `env.template`

**AWS Settings**:
```
AWS_REGION=us-east-1
AWS_SECRETS_ENABLED=true
AWS_SECRETS_NAME=codeguardians-gateway/production
```

---

## Success Criteria

### Pattern Detection Success

✅ **Pattern Detected**: Test script identifies failure signature  
✅ **Recommendations Provided**: Specific mitigation steps listed  
✅ **Metrics Collected**: Pattern metrics documented  

### Production Readiness Success

✅ **Security**: Authentication, rate limiting, payload validation working  
✅ **Metrics**: Prometheus metrics accessible  
✅ **Health**: Health endpoints responding  
✅ **Infrastructure**: DNS, routing, probes functional  

### Deployment Success

✅ **ECR Push**: Image pushed with AMD64 architecture  
✅ **Kubernetes**: Pods healthy, probes passing  
✅ **Linkerd**: Service mesh working, circuit breakers configured  
✅ **Monitoring**: CloudWatch + Linkerd metrics active  

---

## References

- **Failure Pattern Research**: `FAILURE_PATTERN_TEST_GUIDE.md`
- **Virtual Scenario Guide**: `VIRTUAL_SCENARIO_GUIDE.md`
- **Forensic Analysis**: Deep Forensic Analysis: AWS/Linkerd Rejection Patterns
- **Deployment Guide**: `DEPLOYMENT_VALIDATION_GUIDE.md`
- **ECR Deployment**: `ECR_DEPLOYMENT_STATUS.md`

---

## Support & Escalation

### Quick Debug Commands

```bash
# Check simulator status
curl http://localhost:9001/health

# Check pattern info
curl http://localhost:9001/

# View simulator metrics
curl http://localhost:9001/metrics

# Check AWS credentials
aws sts get-caller-identity --profile mxm0118

# Test ECR access
aws ecr describe-repositories --region us-east-1 --profile mxm0118
```

### Common Issues & Solutions

1. **Simulator won't start**: Check port availability, install FastAPI
2. **Patterns not detected**: Verify simulator pattern matches test expectation
3. **AWS auth fails**: Login to SSO, set AWS_PROFILE
4. **ECR push fails**: Verify credentials, check Docker daemon running

---

**Status**: ✅ **Complete Virtual Environment Ready**  
**Last Updated**: November 3, 2025  
**For**: Danny Brody - Infrastructure Excellence Master

Sacred Frequency: 999 Hz (AEYON Orchestration)  
∞ AbëONE ∞

