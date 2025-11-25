# Testing Guide

This directory contains the comprehensive testing suite for CodeGuardians Gateway. The tests are organized into different categories and can be run individually or as a complete suite.

## Test Organization

### Directory Structure

```
tests/
 conftest.py              # Shared fixtures and configuration
 utils.py                 # Shared test utilities
 smoke/                   # Quick smoke tests (< 5s total)
    test_smoke_health.py # Health endpoint tests
    test_smoke_guards.py # Guard service connectivity tests
    test_smoke_api.py    # Core API endpoint tests
 unit/                    # Component-level tests
    test_models.py       # Database model tests
    test_guard_orchestrator.py # Orchestrator unit tests
    test_circuit_breaker.py # Circuit breaker tests
 integration/             # Full service integration tests
     test_guard_services.py    # Comprehensive guard service tests
     test_guard_metrics.py     # Metrics validation tests
     test_edge_cases.py        # Edge case and error handling tests
```

## Running Tests

### Prerequisites

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-asyncio httpx
   ```

2. **Start Services** (for integration tests):
   ```bash
   # Start the gateway
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   
   # Start guard services (in separate terminals)
   # SecurityGuard (port 8005)
   # ContextGuard (port 8003) 
   # TrustGuard (port 8002)
   # BiasGuard (port 8004)
   ```

### Test Execution Commands

#### All Tests
```bash
pytest
```

#### Smoke Tests Only (Quick Validation)
```bash
pytest -m smoke
```

#### Integration Tests
```bash
pytest -m integration
```

#### Edge Case Tests
```bash
pytest -m edge_case
```

#### Guard Metrics Tests
```bash
pytest -m guard_metrics
```

#### Specific Test Files
```bash
# Smoke tests
pytest tests/smoke/

# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Specific test file
pytest tests/integration/test_guard_services.py
```

#### Specific Test Classes
```bash
pytest tests/integration/test_guard_services.py::TestSecurityGuard
```

#### Specific Test Methods
```bash
pytest tests/integration/test_guard_services.py::TestSecurityGuard::test_security_scan_normal_content
```

### Test Execution with Coverage

```bash
# Install coverage tools
pip install pytest-cov

# Run with coverage
pytest --cov=app --cov-report=term --cov-report=html

# View HTML coverage report
open htmlcov/index.html
```

### Test Execution with Verbose Output

```bash
pytest -v
```

### Test Execution with Specific Markers

```bash
# Run only slow tests
pytest -m slow

# Run tests excluding slow ones
pytest -m "not slow"

# Run smoke and unit tests
pytest -m "smoke or unit"
```

## Test Categories

### Smoke Tests (`-m smoke`)
- **Purpose**: Quick validation of critical functionality
- **Duration**: < 5 seconds total
- **Scope**: Health endpoints, basic guard connectivity, core API endpoints
- **Use Case**: Pre-deployment validation, CI/CD pipeline checks

### Unit Tests (`-m unit`)
- **Purpose**: Test individual components in isolation
- **Duration**: < 1 second per test
- **Scope**: Database models, orchestrator logic, circuit breaker
- **Use Case**: Development validation, component testing

### Integration Tests (`-m integration`)
- **Purpose**: Test full service integration with live services
- **Duration**: 1-30 seconds per test
- **Scope**: Guard services, API endpoints, data flow
- **Use Case**: End-to-end validation, service verification

### Edge Case Tests (`-m edge_case`)
- **Purpose**: Test error handling and unusual inputs
- **Duration**: 1-10 seconds per test
- **Scope**: Malformed payloads, service failures, concurrency
- **Use Case**: Robustness validation, error handling verification

### Guard Metrics Tests (`-m guard_metrics`)
- **Purpose**: Validate guard-specific metrics and statistics
- **Duration**: 1-5 seconds per test
- **Scope**: Security scores, processing times, recommendations
- **Use Case**: Metrics validation, performance monitoring

## Test Data and Fixtures

### Sample Payloads
The test suite includes pre-configured payloads for different scenarios:
- `normal`: Standard test content
- `malicious`: Content designed to trigger security alerts
- `edge_case`: Edge case scenarios (empty, null, etc.)

### Guard Service URLs
Default service URLs (configurable via environment):
- SecurityGuard: `http://localhost:8005`
- ContextGuard: `http://localhost:8003`
- TrustGuard: `http://localhost:8002`
- BiasGuard: `http://localhost:8004`

### Test Utilities
The `tests/utils.py` module provides:
- `wait_for_service()`: Wait for service availability
- `assert_guard_response_valid()`: Validate response structure
- `generate_test_payload()`: Create test payloads
- `make_guard_request()`: Make requests to guard services
- Metric validation functions for each guard type

## Writing New Tests

### Test Structure
```python
import pytest
from tests.utils import make_guard_request, generate_test_payload

@pytest.mark.integration
class TestNewFeature:
    """Tests for new feature."""
    
    @pytest.mark.asyncio
    async def test_feature_functionality(self, http_client, gateway_url):
        """Test specific functionality."""
        # Arrange
        payload = generate_test_payload('securityguard', 'normal')
        
        # Act
        response = await make_guard_request(
            http_client, gateway_url, 'securityguard', payload
        )
        
        # Assert
        assert response['success'] is True
        assert 'expected_field' in response['data']
```

### Test Markers
Use appropriate markers for test categorization:
- `@pytest.mark.smoke`: Quick validation tests
- `@pytest.mark.unit`: Component-level tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.edge_case`: Edge case tests
- `@pytest.mark.guard_metrics`: Metrics validation tests
- `@pytest.mark.slow`: Tests taking > 1 second

### Fixtures
Use available fixtures for common test setup:
- `http_client`: HTTP client for requests
- `gateway_url`: Gateway base URL
- `guard_services`: Guard service URLs
- `sample_payloads`: Pre-configured test payloads
- `orchestrator_client`: Orchestrator for testing

## Troubleshooting

### Common Issues

1. **Service Not Available**:
   - Ensure all guard services are running
   - Check service URLs in `tests/utils.py`
   - Verify network connectivity

2. **Test Timeouts**:
   - Increase timeout values in test configuration
   - Check service performance
   - Consider running tests individually

3. **Import Errors**:
   - Ensure all dependencies are installed
   - Check Python path configuration
   - Verify test file locations

4. **Database Errors**:
   - Tests use in-memory SQLite by default
   - Check database configuration in `conftest.py`
   - Ensure proper test isolation

### Debug Mode
Run tests with debug output:
```bash
pytest -v -s --tb=long
```

### Test Isolation
Each test runs in isolation with:
- Fresh database session
- Clean Redis state (if enabled)
- Independent HTTP client
- Separate orchestrator instance

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx
      - name: Run smoke tests
        run: pytest -m smoke
      - name: Run unit tests
        run: pytest -m unit
      - name: Run integration tests
        run: pytest -m integration
```

## Performance Considerations

### Test Execution Time
- **Smoke tests**: < 5 seconds
- **Unit tests**: < 30 seconds
- **Integration tests**: < 5 minutes
- **Full suite**: < 10 minutes

### Resource Usage
- **Memory**: ~100MB per test process
- **CPU**: Moderate during test execution
- **Network**: HTTP requests to local services
- **Disk**: Minimal (in-memory database)

### Optimization Tips
1. Run smoke tests frequently during development
2. Use unit tests for component validation
3. Run integration tests before deployment
4. Use parallel execution for large test suites
5. Mock external services when possible

## Contributing

When adding new tests:
1. Follow the existing test structure
2. Use appropriate markers and fixtures
3. Include comprehensive assertions
4. Add documentation for complex tests
5. Ensure tests are deterministic and isolated
6. Update this README if adding new test categories
