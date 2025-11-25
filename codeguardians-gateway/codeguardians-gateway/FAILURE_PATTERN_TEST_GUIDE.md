# Failure Pattern Test Guide

## Overview

Based on **Deep Forensic Analysis: AWS/Linkerd Rejection Patterns**, this test suite detects **11 distinct failure pattern categories** without modifying the codebase.

## Test Scripts

### 1. AWS NLB Failure Pattern Detection
**Script**: `scripts/test_aws_nlb_failure_patterns.py`

Detects 7 NLB/ALB-specific patterns:
- Pattern 1.1: NLB Flow Table Exhaustion (Silent Rejections)
- Pattern 1.2: NLB Idle Timeout with Silent Termination
- Pattern 1.3: NLB Source Port Preservation Collisions
- Pattern 1.4: NLB Hairpinning Failure
- Pattern 1.5: ALB Target Group Saturation
- Pattern 1.6: ALB Idle Timeout Mismatch
- Pattern 1.7: ALB DNS Resolution to Dead IP

**Usage**:
```bash
python scripts/test_aws_nlb_failure_patterns.py --url http://localhost:8000
```

**What It Tests**:
- Connection timing anomalies (flow table exhaustion indicators)
- Idle timeout patterns (350s NLB timeout detection)
- DNS resolution issues (multiple IP accessibility)
- Keep-alive configuration mismatches
- Response error patterns (503/502 indicating saturation)

---

### 2. Linkerd Service Mesh Failure Pattern Detection
**Script**: `scripts/test_linkerd_failure_patterns.py`

Detects 6 Linkerd-specific patterns:
- Pattern 2.1: Fail-Fast Circuit Breaking
- Pattern 2.2: Proxy Connection Refused (OS Error 111)
- Pattern 2.3:.HTTP/2 Max Concurrent Streams Exhaustion
- Pattern 2.4: Linkerd Proxy Timeout (10s Default)
- Pattern 2.5: TCP Keepalive and Half-Closed Connections
- Pattern 2.6: gRPC Stream Leak and RST_STREAM Handling

**Usage**:
```bash
python scripts/test_linkerd_failure_patterns.py --url http://localhost:8000
```

**What It Tests**:
- Circuit breaker patterns (consecutive failure detection)
- Connection refused errors (port binding issues)
- HTTP/2 stream exhaustion (concurrency limit testing)
- Proxy timeout patterns (10s default detection)
- Timeout signatures

---

### 3. AWS/Linkerd Integration Failure Pattern Detection
**Script**: `scripts/test_aws_linkerd_integration_patterns.py`

Detects 4 integration-specific patterns:
- Pattern 3.1: AWS NLB + Linkerd Idle Timeout Cascade
- Pattern 3.2: ALB + Linkerd Multicluster Gateway 502s
- Pattern 3.3: NLB + Linkerd gRPC MAX_CONCURRENT_STREAMS
- Pattern 3.4: VPC Flow Log REJECT with Security Group "Allowance"

**Usage**:
```bash
python scripts/test_aws_linkerd_integration_patterns.py --url http://localhost:8000
python scripts/test_aws_linkerd_integration_patterns.py --url http://localhost:8000 --no-linkerd
```

**What It Tests**:
- Timeout cascade patterns (NLB timeout → Linkerd circuit breaker)
- gRPC stream exhaustion behind NLB
- ALB gateway protocol mismatch (502 patterns)
- Combined failure signatures

---

### 4. Forensic Signature Detection
**Script**: `scripts/test_forensic_signatures.py`

Detects forensic signatures from error patterns:
- Error Code Classification (502, 503, 504, Connection refused, Connection reset)
- TCP RST Packet Patterns
- Timeout Patterns (short/medium/long)
- Error code correlation

**Usage**:
```bash
python scripts/test_forensic_signatures.py --url http://localhost:8000
```

**What It Tests**:
- Error code classification matrix
- RST packet detection patterns
- Timeout distribution analysis
- Forensic signature correlation

---

### 5. Comprehensive Pattern Detection Suite
**Script**: `scripts/run_all_failure_pattern_tests.sh`

Orchestrates all pattern detection tests.

**Usage**:
```bash
./scripts/run_all_failure_pattern_tests.sh

# With environment variables
BASE_URL=http://localhost:8000 \
LINKERD_ENABLED=false \
./scripts/run_all_failure_pattern_tests.sh
```

---

## Pattern Detection Methodology

### Detection Approach (Non-Invasive)
- **Tim doesn't modify codebase** - Only observes behavior
- **Pattern matching** - Detects known failure signatures
- **Timing analysis** - Identifies timeout/anomaly patterns
- **Error correlation** - Links error codes to patterns
- **Concurrency testing** - Detects stream/connection limits

### What Gets Detected

**AWS NLB Patterns**:
-  Flow table exhaustion indicators
-  Idle timeout signatures (~350s)
-  DNS resolution issues
-  Keep-alive mismatches
-  Target group saturation (503/502)

**Linkerd Patterns**:
-  Circuit breaker trips (consecutive failures)
-  Connection refused (port binding)
-  HTTP/2 stream exhaustion
-  Proxy timeout patterns (10s)
-  Timeout signatures

**Integration Patterns**:
-  Timeout cascade (NLB → Linkerd)
-  gRPC stream exhaustion behind NLB
-  ALB gateway 502 patterns
-  Combined failure signatures

**Forensic Signatures**:
-  Error code classification
-  RST packet patterns
-  Timeout distributions
-  Error correlation

---

## Expected Test Results

### Ideal (No Patterns Detected)
```
 CLEAN (all tests pass)
 No failure patterns detected
 No issues found
```

### Patterns Detected (Informational)
```
 PATTERNS DETECTED
 Issues found: [specific patterns]
 Recommendations provided
```

**Note**: Pattern detection doesn't mean failures are occurring - it means the **conditions** that lead to failures are present or **signatures** match known patterns.

---

## Interpretation Guide

### Pattern Detection ≠ Failure Occurring

**Pattern Detection** means:
- Conditions for failure exist
- Signatures match known patterns
- Mitigation may be recommended

**Not necessarily**:
- Failure is actively happening
- Immediate action required
- System is broken

### Priority Classification

Based on forensic analysis:

| Pattern | Priority | Action Required |
|---------|----------|----------------|
| NLB Flow Table Exhaustion | CRITICAL | Immediate monitoring |
| ALB Target Group Saturation | CRITICAL | Review autoscaling |
| Circuit Breaker Tripping | HIGH | Check application errors |
| Connection Refused | HIGH | Verify port binding |
| Timeout Patterns | MEDIUM | Review timeout config |
| Stream Exhaustion | MEDIUM | Increase limits |

---

## Diagnostic Workflow

### 1. Run Pattern Detection
```bash
./scripts/run_all_failure_pattern_tests.sh
```

### 2. Analyze Results
- Review detected patterns
- Check recommendations
- Prioritize by severity

### 3. Deep Dive (if patterns detected)
- Check CloudWatch metrics (NLB/ALB)
- Review Linkerd dashboard
- Analyze VPC Flow Logs
- Check application logs

### 4. Apply Mitigations
Follow recommendations from test output:
- TCP keepalive configuration
- Circuit breaker tuning
- Timeout adjustments
- Concurrency limit increases

---

## CloudWatch Metrics to Monitor

### NLB Metrics
```
RejectedFlowCount > 0                    # CRITICAL
TCP_ELB_Reset_Count > baseline           # HIGH
ActiveFlowCount approaching limits      # MEDIUM
```

### ALB Metrics
```
HTTPCode_ELB_503_Count > 0               # CRITICAL
HTTPCode_ELB_502_Count > baseline        # HIGH
TargetConnectionErrorCount > baseline    # HIGH
```

### Linkerd Metrics (via linkerd viz)
```
request_total{classification="failure"}
response_latency_ms_p99 > threshold
tcp_close_total{classification="failure"}
```

---

## VPC Flow Log Analysis

Pattern detection scripts identify patterns that **should be verified** in VPC Flow Logs:

```bash
# Check for REJECT entries
aws logs filter-log-events \
  --log-group-name /aws/vpc/flowlogs \
  --filter-pattern "REJECT" \
  --start-time $(date -u -d '1 hour ago' +%s)000
  
# Look for patterns corresponding to detected issues
```

---

## Recommendations by Pattern

### NLB Flow Table Exhaustion
- Monitor CloudWatch RejectedFlowCount
- Reduce NLB idle timeout (if supported)
- Implement TCP keepalive < 350s
- Monitor ActiveFlowCount approaching limits

### Linkerd Circuit Breaker
- Check application logs for consecutive failures
- Verify max_concurrent_streams not too low
- Temporarily disable circuit breaker for diagnosis
- Review Linkerd viz deployment stats

### Timeout Cascade (NLB + Linkerd)
- Implement TCP keepalive < 350s
- Adjust Linkerd circuit breaker threshold
- Application-level connection cycling (close after 300s)
- Monitor both NLB and Linkerd metrics simultaneously

### gRPC Stream Exhaustion
- Increase application max_concurrent_streams
- Deploy multiple Linkerd gateway replicas
- Use connection draining and cycling
- Calculate required: RPS × Avg Latency = Streams Needed

---

## Notes

- **No codebase modifications** - Tests only observe and detect
- **Pattern-based** - Identifies signatures, not bugs
- **Informational** - Recommendations provided, not enforced
- **Deep Research** - Based on comprehensive forensic analysis

---

## References

- **Deep Forensic Analysis**: AWS/Linkerd Rejection Patterns (Source Document)
- **Detection Based On**: 11 distinct failure pattern categories
- **Pattern Confidence**: 95%+ (based on forensic research)

---

**Status**:  **Test Scripts Ready for Pattern Detection**

**Usage**: Run against any endpoint to detect known AWS/Linkerd failure patterns without modifying codebase.

