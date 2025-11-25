# Local Testing Guide

## Overview

This guide covers how to test the AI Guardians platform locally, including unit tests, integration tests, and end-to-end testing.

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Node.js 16+ (for frontend testing)
- Git

## Test Structure

```
tests/
├── unit/                 # Unit tests
├── integration/          # Integration tests
├── e2e/                  # End-to-end tests
├── fixtures/             # Test fixtures
└── conftest.py          # Test configuration
```

## Running Tests

### All Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run with verbose output
pytest -v
```

### Specific Test Types

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# End-to-end tests only
pytest tests/e2e/
```

### Specific Test Files

```bash
# Test specific file
pytest tests/unit/test_guard_orchestrator.py

# Test specific function
pytest tests/unit/test_guard_orchestrator.py::test_orchestrate_request
```

## Test Categories

### Unit Tests

Test individual components in isolation.

```python
# Example unit test
def test_guard_orchestrator_initialization():
    orchestrator = GuardServiceOrchestrator()
    assert orchestrator.services == {}
    assert orchestrator.health_status == {}
```

### Integration Tests

Test component interactions.

```python
# Example integration test
async def test_guard_service_integration():
    async with AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/guards/process",
            json={
                "service_type": "tokenguard",
                "payload": {"text": "test"}
            }
        )
        assert response.status_code == 200
```

### End-to-End Tests

Test complete user workflows.

```python
# Example E2E test
async def test_complete_guard_workflow():
    # 1. Start services
    # 2. Send request
    # 3. Verify response
    # 4. Check side effects
    pass
```

## Test Configuration

### Environment Setup

```bash
# Set test environment
export TESTING=true
export DATABASE_URL=sqlite:///./test.db
export REDIS_URL=redis://localhost:6379/1
```

### Test Database

```python
# conftest.py
@pytest.fixture(scope="session")
def test_db():
    # Setup test database
    pass

@pytest.fixture(autouse=True)
def clean_db():
    # Clean database before each test
    pass
```

## Mock Services

### External API Mocks

```python
# Mock external services
@pytest.fixture
def mock_tokenguard():
    with patch('app.core.guard_orchestrator.httpx.AsyncClient') as mock:
        mock.return_value.post.return_value = MockResponse(
            status_code=200,
            json={"confidence": 0.85}
        )
        yield mock
```

### Database Mocks

```python
# Mock database operations
@pytest.fixture
def mock_db():
    with patch('app.core.database.get_db') as mock:
        mock.return_value = MockSession()
        yield mock
```

## Performance Testing

### Load Testing

```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/performance/load_test.py --host=http://localhost:8000
```

### Stress Testing

```python
# Example stress test
async def test_high_load():
    tasks = []
    for i in range(1000):
        task = asyncio.create_task(
            client.post("/api/v1/guards/process", json=test_data)
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    assert all(r.status_code == 200 for r in results)
```

## Security Testing

### Authentication Tests

```python
def test_authentication_required():
    response = client.post("/api/v1/guards/process")
    assert response.status_code == 401

def test_valid_api_key():
    response = client.post(
        "/api/v1/guards/process",
        headers={"X-API-Key": "valid-key"}
    )
    assert response.status_code == 200
```

### Authorization Tests

```python
def test_admin_only_endpoint():
    response = client.get("/api/v1/users/")
    assert response.status_code == 403
```

## API Testing

### Request/Response Validation

```python
def test_guard_request_validation():
    # Test valid request
    valid_request = {
        "service_type": "tokenguard",
        "payload": {"text": "test"}
    }
    response = client.post("/api/v1/guards/process", json=valid_request)
    assert response.status_code == 200
    
    # Test invalid request
    invalid_request = {
        "service_type": "invalid",
        "payload": {}
    }
    response = client.post("/api/v1/guards/process", json=invalid_request)
    assert response.status_code == 400
```

### Error Handling Tests

```python
def test_service_unavailable():
    with patch('app.core.guard_orchestrator.orchestrator') as mock:
        mock.orchestrate_request.side_effect = ServiceUnavailableError("Service down")
        response = client.post("/api/v1/guards/process", json=test_data)
        assert response.status_code == 503
```

## Database Testing

### Migration Tests

```python
def test_database_migrations():
    # Test migration up
    alembic.upgrade("head")
    
    # Test migration down
    alembic.downgrade("base")
```

### Data Integrity Tests

```python
def test_user_creation():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Verify user exists in database
    user = db.query(User).filter(User.username == "testuser").first()
    assert user is not None
```

## Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
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
          python-version: 3.8
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

## Test Data Management

### Fixtures

```python
# conftest.py
@pytest.fixture
def sample_text():
    return "This is a sample text for testing."

@pytest.fixture
def guard_request():
    return {
        "service_type": "tokenguard",
        "payload": {"text": "test"},
        "client_type": "api"
    }
```

### Test Database Seeding

```python
@pytest.fixture
def seeded_db():
    # Create test data
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    yield db
    # Cleanup
    db.rollback()
```

## Debugging Tests

### Debug Mode

```bash
# Run tests in debug mode
pytest --pdb

# Run specific test in debug mode
pytest tests/unit/test_guard_orchestrator.py::test_function -s --pdb
```

### Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

def test_with_logging():
    logger = logging.getLogger(__name__)
    logger.debug("Test starting")
    # Test code
    logger.debug("Test completed")
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Naming**: Use descriptive test names
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Mock External Dependencies**: Don't rely on external services
5. **Test Edge Cases**: Include boundary conditions
6. **Keep Tests Fast**: Avoid slow operations
7. **Maintain Test Data**: Keep fixtures up to date

## Troubleshooting

### Common Issues

1. **Tests failing randomly**
   - Check for shared state
   - Ensure proper cleanup

2. **Database connection errors**
   - Verify test database setup
   - Check connection strings

3. **Import errors**
   - Verify PYTHONPATH
   - Check relative imports

### Getting Help

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Discord Community](https://discord.gg/aiguardian)

