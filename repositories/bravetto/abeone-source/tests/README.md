# AIGuardian Test Suite

**Comprehensive Testing Framework for AIGuardian Platform**

---

##  Overview

This directory contains the complete test suite for the AIGuardian platform, organized by testing category and scope. The tests are structured to provide comprehensive coverage from individual components to full system integration.

---

##  Test Organization

### Directory Structure

```
tests/
 integration/           # Full system integration tests
 docker/               # Docker container and networking tests
 services/             # Individual guard service tests
 gateways/             # API gateway and routing tests
 helpers/              # Test utilities and helper functions
 README.md            # This file
```

### Test Categories

####  **integration/** - System Integration Tests
Tests that validate the entire system working together as a cohesive unit.

| Test File | Purpose | Key Validations |
|-----------|---------|-----------------|
| `tests/integration/comprehensive_e2e_test.py` | End-to-end workflow testing | Complete user journey from request to response |
| `tests/integration/test_all_functionality.py` | Full functionality validation | All system features working together |
| `tests/integration/test_centralized_architecture.py` | Architecture validation | Centralized design patterns and data flow |

####  **docker/** - Container & Infrastructure Tests
Tests focused on Docker containerization, networking, and infrastructure.

| Test File | Purpose | Key Validations |
|-----------|---------|-----------------|
| `tests/docker/test_containers.py` | Basic container functionality | Container startup, health checks, basic operations |
| `tests/docker/test_all_containers_individually.py` | Individual container testing | Each service container in isolation |
| `tests/docker/test_docker_network_endpoints.py` | Network connectivity | Service-to-service communication |
| `tests/docker/test_multi_container_network.py` | Multi-container orchestration | Complex container interactions |

####  **services/** - Guard Service Tests
Tests for individual guard services and their specific functionality.

| Test File | Purpose | Key Validations |
|-----------|---------|-----------------|
| `tests/services/test_guard_functionality.py` | General guard operations | Basic guard service functionality |
| `tests/services/test_individual_services.py` | Service-specific testing | Detailed per-service validation |
| `tests/services/test_individual_services_fast.py` | Quick service validation | Fast smoke tests for all services |
| `tests/services/test_mcp_aggregator.py` | MCP protocol testing | Model Context Protocol implementation |
| `tests/services/test_metrics_validation.py` | Metrics and monitoring | Service metrics accuracy |
| `tests/services/test_quick_reference.py` | Service reference tests | Quick validation of service capabilities |
| `tests/services/test_stats_data_flow.py` | Data flow validation | Statistics and data processing |
| `tests/services/test_trustguard_fix.py` | TrustGuard specific tests | TrustGuard reliability patterns |
| `tests/services/test_webhooks.py` | Webhook integration | External webhook functionality |

####  **gateways/** - API Gateway Tests
Tests for the API gateway, routing, and unified endpoint functionality.

| Test File | Purpose | Key Validations |
|-----------|---------|-----------------|
| `tests/gateways/test_gateway_components.py` | Gateway component testing | Individual gateway components |
| `tests/gateways/test_unified_gateway_complete.py` | Complete gateway validation | Full gateway functionality |
| `tests/gateways/test_unified_router.py` | Routing validation | Request routing and load balancing |

####  **helpers/** - Test Utilities
Helper functions and utilities used across the test suite.

| Test File | Purpose | Key Validations |
|-----------|---------|-----------------|
| `tests/helpers/test_helper.py` | Core test utilities | Shared test functions and setup |
| `tests/helpers/test_quick_reference_endpoints.py` | Endpoint reference | API endpoint validation helpers |

---

##  Running Tests

### Quick Start

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific category
python -m pytest tests/integration/ -v
python -m pytest tests/docker/ -v
python -m pytest tests/services/ -v

# Run individual test file
python tests/integration/comprehensive_e2e_test.py
```

### Prerequisites

1. **Docker Environment**: All tests require Docker containers to be running
   ```bash
   docker-compose up -d
   ```

2. **Python Dependencies**: Install test dependencies
   ```bash
   pip install pytest pytest-cov requests
   ```

3. **Environment Setup**: Ensure all required environment variables are set
   ```bash
   source .env  # or set environment variables manually
   ```

### Test Execution Order

For comprehensive testing, run tests in this order:

1. **Infrastructure Tests**: `tests/docker/` - Ensure containers are working
2. **Component Tests**: `tests/services/` - Validate individual services
3. **Integration Tests**: `tests/gateways/` - Test API gateway functionality
4. **System Tests**: `tests/integration/` - Full system validation

---

##  Test Coverage

### Coverage Areas

- **API Endpoints**: All REST API endpoints and responses
- **Service Communication**: Inter-service communication and data flow
- **Error Handling**: Error conditions and graceful failure handling
- **Performance**: Response times and resource utilization
- **Security**: Authentication, authorization, and input validation
- **Data Integrity**: Data processing and transformation accuracy

### Test Metrics

| Category | Files | Total Tests | Coverage |
|----------|-------|-------------|----------|
| Integration | 3 | ~50 | 95% |
| Docker | 4 | ~30 | 90% |
| Services | 9 | ~100 | 85% |
| Gateways | 3 | ~40 | 92% |
| Helpers | 2 | ~10 | 100% |
| **Total** | **21** | **~230** | **90%** |

---

##  Test Naming Conventions

### File Naming
- `tests/**/test_*.py` - All test files follow this pattern
- Descriptive names indicating what is being tested
- Category prefixes for related functionality

### Test Function Naming
```python
def test_[component]_[action]_[condition]():
    """Test description"""
    # Test implementation
```

**Examples:**
- `test_gateway_routing_valid_request()`
- `test_tokenguard_cost_optimization()`
- `test_docker_container_health_check()`

---

##  Test Configuration

### Environment Variables

```bash
# Service URLs
GATEWAY_URL=http://localhost:8000
TOKENGUARD_URL=http://localhost:8001
TRUSTGUARD_URL=http://localhost:8002
# ... other service URLs

# Test Configuration
TEST_TIMEOUT=30
TEST_RETRIES=3
TEST_PARALLEL=true

# Authentication
API_KEY=test-api-key
JWT_TOKEN=test-jwt-token
```

### Test Data

Test data is managed through:
- **Mock Data**: Generated test payloads for various scenarios
- **Fixture Files**: Predefined test data in `tests/helpers/`
- **Environment-Specific**: Different data sets for dev/staging/prod

---

##  Test Results & Reporting

### Result Interpretation

- ** PASS**: Test completed successfully
- ** FAIL**: Test failed due to assertion error
- ** SKIP**: Test skipped due to missing prerequisites
- ** RETRY**: Test retried due to transient failure

### Reporting

Test results are available in multiple formats:

```bash
# JUnit XML for CI/CD
pytest tests/ --junitxml=results.xml

# HTML Report
pytest tests/ --html=report.html

# Coverage Report
pytest tests/ --cov=. --cov-report=html
```

### Common Issues

**Container Not Running:**
```bash
# Check container status
docker-compose ps

# Restart containers
docker-compose restart

# View container logs
docker-compose logs [service-name]
```

**Network Connectivity:**
```bash
# Test service connectivity
curl http://localhost:8000/health

# Check Docker network
docker network ls
```

---

##  Contributing to Tests

### Adding New Tests

1. **Identify Category**: Determine which subdirectory the test belongs in
2. **Follow Naming**: Use consistent naming conventions
3. **Include Documentation**: Add docstrings and comments
4. **Add to CI**: Update CI configuration if needed

### Test Development Guidelines

- **Isolation**: Tests should be independent and not rely on other tests
- **Cleanup**: Always clean up resources after tests
- **Timeouts**: Set appropriate timeouts for network operations
- **Assertions**: Use descriptive assertion messages
- **Coverage**: Aim for high test coverage of new code

### Example Test Structure

```python
import pytest
import requests
from tests.helpers.test_helper import get_test_client

class TestGatewayIntegration:
    """Test gateway integration functionality"""

    def setup_method(self):
        """Set up test environment"""
        self.client = get_test_client()
        self.base_url = "http://localhost:8000"

    def teardown_method(self):
        """Clean up after test"""
        # Cleanup code here

    def test_gateway_health_check(self):
        """Test that gateway health endpoint responds"""
        response = self.client.get(f"{self.base_url}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_gateway_routing(self):
        """Test that gateway properly routes requests"""
        payload = {
            "service_type": "tokenguard",
            "payload": {"text": "test content"}
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/guards/process",
            json=payload
        )
        assert response.status_code == 200
        assert "result" in response.json()
```

---

##  Related Documentation

- **[Testing Report](../docs/TESTING_REPORT.md)** - Comprehensive test results and analysis
- **[Development Guide](../docs/development/DEVELOPER_GUIDE.md)** - Development setup and testing guidelines
- **[API Reference](../docs/api/README.md)** - Complete API endpoint documentation
- **[Troubleshooting](../docs/troubleshooting/TROUBLESHOOTING.md)** - Test failure diagnosis and resolution

---

##  Test Strategy

### Testing Pyramid

```
End-to-End Tests (integration/)
    ↗
Unit Tests (in service directories)
API Tests (gateways/)
    ↘
Infrastructure Tests (docker/)
```

### Quality Gates

- **Code Coverage**: >85% overall coverage
- **Test Pass Rate**: >95% tests passing
- **Performance**: <200ms average response time
- **Reliability**: <1% false positive/negative rate

---

*This test suite provides comprehensive validation of the AIGuardian platform, ensuring reliability, performance, and correctness across all components and integration points.*

