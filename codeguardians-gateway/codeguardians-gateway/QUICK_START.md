# Quick Start - Virtual Scenarios

## Correct Directory

The scripts are located in:
```
/Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway
```

## Quick Commands

### Navigate to Correct Directory

```bash
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway
```

### Run Scenario Simulator

```bash
# List available patterns
python scripts/scenario_simulator.py --list

# Start simulator (pattern: circuit_breaker)
python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001
```

### Run Detection Tests (in another terminal)

```bash
# Navigate to correct directory first
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway

# Test against simulator
python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001
python scripts/test_aws_nlb_failure_patterns.py --url http://localhost:9001
```

### Run All Scenarios Automatically

```bash
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway

./scripts/run_virtual_scenarios.sh
```

## One-Liner Examples

```bash
# Start circuit breaker simulator
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway && python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001

# Test detection (in another terminal)
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway && python scripts/test_linkerd_failure_patterns.py --url http://localhost:9001
```

## Create Alias (Optional)

Add to your `~/.zshrc`:

```bash
# AI Guards Test Scripts
alias ag-test='cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway'
alias ag-scenario='cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway && python scripts/scenario_simulator.py'
alias ag-detect='cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway && python scripts'
```

Then reload:
```bash
source ~/.zshrc
```

Usage:
```bash
ag-test
./scripts/run_virtual_scenarios.sh
```

