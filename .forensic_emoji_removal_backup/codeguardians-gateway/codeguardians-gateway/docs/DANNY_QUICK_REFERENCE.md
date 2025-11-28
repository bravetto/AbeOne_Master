# Danny's Quick Reference Card

**AWS/Linkerd Virtual Environment Testing**

---

## 🚀 One-Command Quick Start

```bash
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway
./scripts/danny_quick_test.sh
```

---

## 📋 Essential Commands

### Virtual Scenario Testing

```bash
# Start single scenario
python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001

# Run all scenarios automatically
./scripts/run_virtual_scenarios.sh

# Test specific pattern
./scripts/run_virtual_scenarios.sh flow_table_exhaustion
```

### Pattern Detection

```bash
# AWS NLB patterns
python scripts/REPLACE_ME.py --url http://localhost:9001

# Linkerd patterns  
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001

# Integration patterns
python scripts/REPLACE_ME.py --url http://localhost:9001
```

### Production Validation

```bash
# Start server
./scripts/launch_no_fail_local.sh

# Production readiness
python scripts/test_production_readiness.py --url http://localhost:8000

# AWS/Linkerd deployment
python scripts/REPLACE_ME.py --url http://localhost:8000
```

### ECR Deployment

```bash
# AWS SSO login
aws sso login --profile mxm0118
export AWS_PROFILE=mxm0118

# Push to ECR (AMD64)
./push-to-ecr.sh
```

---

## 🎯 Available Patterns (11)

| Pattern | Category | Test Script |
|---------|----------|-------------|
| `flow_table_exhaustion` | AWS NLB | `REPLACE_ME.py` |
| `idle_timeout` | AWS NLB | `REPLACE_ME.py` |
| `circuit_breaker` | Linkerd | `test_linkerd_failure_patterns.py` |
| `timeout_cascade` | Integration | `REPLACE_ME.py` |
| `target_group_saturation` | AWS ALB | `REPLACE_ME.py` |
| `connection_refused` | Linkerd | `test_linkerd_failure_patterns.py` |
| `stream_exhaustion` | Linkerd | `test_linkerd_failure_patterns.py` |
| `proxy_timeout` | Linkerd | `test_linkerd_failure_patterns.py` |
| `keep_alive_mismatch` | AWS ALB | `REPLACE_ME.py` |
| `rst_pattern` | Forensic | `test_forensic_signatures.py` |
| `dns_dead_ip` | AWS ALB | `REPLACE_ME.py` |

---

## ⚙️ Configuration

### AWS Configuration
- **Account**: `730335329303`
- **Region**: `us-east-1`
- **Profile**: `mxm0118` (SSO)
- **ECR Repo**: `gateway`
- **Image Tag**: `dev`

### Ports
- **Virtual Simulator**: `9001`
- **Production Server**: `8000`

---

## 🔍 Troubleshooting

```bash
# Check simulator status
curl http://localhost:9001/health

# Check AWS credentials
aws sts get-caller-identity --profile mxm0118

# Check ECR access
aws ecr describe-repositories --region us-east-1 --profile mxm0118

# View test logs
cat /tmp/danny_test_*.log
```

---

## 📊 Test Results Location

- **Virtual Scenarios**: Output to console + logs in `/tmp/scenario_simulator_*.log`
- **Pattern Detection**: Console output + JSON with `--json` flag
- **Production Tests**: Console output + JSON with `--json` flag

---

## 📚 Full Documentation

**Complete Guide**: `docs/DANNY_AWS_LINKERD_VIRTUAL_ENVIRONMENT.md`

**Includes**:
- Detailed architecture overview
- Complete workflow examples
- Kubernetes deployment configs
- Linkerd service profiles
- CloudWatch monitoring setup
- Troubleshooting guide

---

**Last Updated**: November 3, 2025  
**For**: Danny Brody - Infrastructure Excellence Master

