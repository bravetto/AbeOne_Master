# Virtual Scenario Testing Guide

## Overview

The Virtual Scenario Simulator allows you to **test pattern detection scripts against simulated failure scenarios** without modifying any codebase or test files.

This validates that the detection scripts can actually identify the failure patterns they're designed to detect.

---

## Quick Start

### 1. List Available Patterns

```bash
python scripts/scenario_simulator.py --list
```

### 2. Run Single Scenario

```bash
# Start simulator for specific pattern
python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001

# In another terminal, run detection tests
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001
```

### 3. Run All Scenarios Automatically

```bash
./scripts/run_virtual_scenarios.sh

# Or test specific pattern
./scripts/run_virtual_scenarios.sh circuit_breaker
```

---

## Available Patterns

### 1. `flow_table_exhaustion`
**Simulates**: NLB Flow Table Exhaustion
- Slow connections (2s delay)
- Timeout errors (30% rate)
- Gateway timeout responses

**Detection Test**: `test_aws_nlb_failure_patterns.py`

---

### 2. `circuit_breaker`
**Simulates**: Linkerd Circuit Breaker
- 7 consecutive failures
- Circuit breaker opens
- Returns "Service in fail-fast" error header

**Detection Test**: `test_linkerd_failure_patterns.py`

---

### 3. `target_group_saturation`
**Simulates**: ALB Target Group Saturation
- 503 Service Unavailable after threshold
- Target group saturation indicators

**Detection Test**: `test_aws_nlb_failure_patterns.py`

---

### 4. `connection_refused`
**Simulates**: Connection Refused (OS Error 111)
- Intermittent connection refused
- OS error 111 patterns
- Port binding issues

**Detection Test**: `test_linkerd_failure_patterns.py`

---

### 5. `keep_alive_mismatch`
**Simulates**: Keep-Alive Mismatch
- Missing keep-alive headers
- ALB idle timeout issues

**Detection Test**: `test_aws_nlb_failure_patterns.py`

---

### 6. `proxy_timeout`
**Simulates**: Linkerd Proxy Timeout (10s)
- Slow responses (>10s)
- Gateway timeout patterns

**Detection Test**: `test_linkerd_failure_patterns.py`

---

### 7. `rst_pattern`
**Simulates**: TCP RST Patterns
- Connection reset errors
- RST packet signatures

**Detection Test**: `test_forensic_signatures.py`

---

### 8. `timeout_cascade`
**Simulates**: NLB + Linkerd Timeout Cascade
- Idle timeout triggers reset
- Cascade to circuit breaker
- Combined failure patterns

**Detection Test**: `test_aws_linkerd_integration_patterns.py`

---

## Usage Examples

### Example 1: Test Circuit Breaker Detection

```bash
# Terminal 1: Start simulator
python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001

# Terminal 2: Run detection tests
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001
```

**Expected**: Detection script should identify:
-  Consecutive failure patterns
-  Circuit breaker trip signature
-  "Service in fail-fast" header detection

---

### Example 2: Test Flow Table Exhaustion

```bash
# Terminal 1: Start simulator
python scripts/scenario_simulator.py --pattern flow_table_exhaustion --port 9001

# Terminal 2: Run detection tests
python scripts/test_aws_nlb_failure_patterns.py --url http://localhost:9001
```

**Expected**: Detection script should identify:
-  Slow connection patterns
-  Timeout rate analysis
-  Flow table exhaustion indicators

---

### Example 3: Automated Scenario Testing

```bash
# Run all scenarios automatically
./scripts/run_virtual_scenarios.sh

# Output shows:
# 1. Each scenario starts simulator
# 2. Detection tests run against simulator
# 3. Results show pattern detection capabilities
# 4. Simulator stops automatically
```

---

## How It Works

### Simulator Architecture

```

   Pattern Detection Scripts             
   (test_*_failure_patterns.py)          

                HTTP Request
               

   Virtual Scenario Simulator             
   (scenario_simulator.py)                
   - FastAPI server                       
   - Pattern-specific behavior            
   - Controlled failure injection        

```

### Pattern Simulation Logic

Each pattern has specific behavior:

1. **circuit_breaker**: Fails 7 times, then returns 503 with fail-fast header
2. **flow_table_exhaustion**: Randomly delays or times out based on request count
3. **target_group_saturation**: Returns 503 after threshold concurrent requests
4. **connection_refused**: Returns 502 with connection refused error
5. **proxy_timeout**: Delays response >10s to trigger timeout

---

## Validation Workflow

### Step 1: Start Simulator

```bash
python scripts/scenario_simulator.py --pattern <pattern_name> --port 9001
```

### Step 2: Run Detection Tests

```bash
# Appropriate test based on pattern
python scripts/test_*_failure_patterns.py --url http://localhost:9001
```

### Step 3: Verify Detection

Expected outputs:
-  **Pattern Detected**: Detection script identifies the pattern
-  **Issues Found**: Specific issues listed
-  **Recommendations**: Mitigation steps provided

---

## Scenario Endpoints

### `/health`
Health endpoint with pattern-specific behavior:
- Returns 200 for normal requests
- Returns error codes based on pattern simulation
- Includes pattern metadata in response

### `/metrics`
Prometheus metrics endpoint:
- Request counts
- Failure counts
- Pattern status

### `/`
Pattern information:
- Pattern name and description
- Current request/failure counts
- Available endpoints

---

## Pattern Mapping

| Pattern | Detection Test | Test Focus |
|---------|---------------|------------|
| `flow_table_exhaustion` | `test_aws_nlb_failure_patterns.py` | Connection timing, timeouts |
| `circuit_breaker` | `test_linkerd_failure_patterns.py` | Failure streaks, circuit breaker |
| `target_group_saturation` | `test_aws_nlb_failure_patterns.py` | 503 errors, saturation |
| `connection_refused` | `test_linkerd_failure_patterns.py` | Connection errors, OS 111 |
| `keep_alive_mismatch` | `test_aws_nlb_failure_patterns.py` | Header analysis |
| `proxy_timeout` | `test_linkerd_failure_patterns.py` | Timeout patterns, 10s threshold |
| `rst_pattern` | `test_forensic_signatures.py` | RST detection, error codes |
| `timeout_cascade` | `test_aws_linkerd_integration_patterns.py` | Combined patterns |

---

## Advanced Usage

### Custom Port

```bash
python scripts/scenario_simulator.py --pattern circuit_breaker --port 8080
python scripts/test_linkerd_failure_patterns.py --url http://localhost:8080
```

### Multiple Simulators (Different Ports)

```bash
# Terminal 1
python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001

# Terminal 2
python scripts/scenario_simulator.py --pattern flow_table_exhaustion --port 9002

# Terminal 3: Test against both
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001
python scripts/test_aws_nlb_failure_patterns.py --url http://localhost:9002
```

### JSON Output

```bash
# Simulator provides JSON at root endpoint
curl http://localhost:9001/ | jq

# Detection tests support JSON output
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001 --json
```

---

## Troubleshooting

### Simulator Not Starting

```bash
# Check if port is available
lsof -i :9001

# Check FastAPI installation
python3 -c "import fastapi; print('OK')"

# Install if needed
pip install fastapi uvicorn
```

### Tests Not Connecting

```bash
# Verify simulator is running
curl http://localhost:9001/health

# Check logs
cat /tmp/scenario_simulator_*.log
```

### Pattern Not Detected

- Verify simulator is running the correct pattern
- Check pattern behavior matches expected signatures
- Review detection test logs for false negatives
- Ensure test is targeting correct URL

---

## Integration with CI/CD

### Example GitHub Actions Workflow

```yaml
- name: Run Virtual Scenarios
  run: |
    # Start simulator in background
    python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001 &
    
    # Wait for startup
    sleep 3
    
    # Run detection tests
    python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001
    
    # Verify detection worked
    # (exit code 1 if patterns detected = test validation success)
```

---

## Benefits

1. **Validates Detection Scripts**: Confirms detection scripts actually work
2. **No Codebase Changes**: Completely separate from application code
3. **Reproducible**: Same pattern behavior every time
4. **Isolated Testing**: Can test detection capabilities independently
5. **Educational**: Shows what each pattern looks like

---

## Limitations

1. **Simplified Simulation**: Real-world patterns are more complex
2. **Single Pattern**: One pattern per simulator instance
3. **HTTP Only**: Simulates HTTP layer, not TCP layer directly
4. **Timing Limitations**: Some patterns require longer observation periods

---

## Next Steps

1. **Run Scenarios**: Test detection scripts against simulated patterns
2. **Validate Detection**: Confirm scripts identify patterns correctly
3. **Extend Patterns**: Add more pattern simulations as needed
4. **Integrate Testing**: Include in CI/CD pipeline for validation

---

**Status**:  **Virtual Scenario Simulator Ready**

**Usage**: Run scenarios to validate pattern detection scripts work correctly.

