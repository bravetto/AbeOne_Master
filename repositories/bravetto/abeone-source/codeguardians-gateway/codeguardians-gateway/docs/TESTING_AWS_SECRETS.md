# Testing AWS Secrets Manager Integration

## Overview

This document provides comprehensive testing procedures for the AWS Secrets Manager integration in CodeGuardians Gateway. It covers local development, testing with AWS Secrets Manager, mocking for unit tests, and troubleshooting common issues.

## Table of Contents

1. [Local Development Testing](#local-development-testing)
2. [AWS Secrets Manager Testing](#aws-secrets-manager-testing)
3. [Unit Testing with Mocks](#unit-testing-with-mocks)
4. [Integration Testing](#integration-testing)
5. [Troubleshooting](#troubleshooting)
6. [Secret Rotation Testing](#secret-rotation-testing)

## Local Development Testing

### 1. Disable AWS Secrets Manager for Local Development

Set environment variables to use local secrets:

```bash
# In your .env file or environment
AWS_SECRETS_ENABLED=false
SECRET_KEY=your-local-development-secret-key-32-chars-minimum
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/db
REDIS_URL=redis://localhost:6379/0
```

### 2. Test Local Configuration Loading

```bash
# Navigate to gateway directory
cd codeguardians-gateway/codeguardians-gateway

# Test configuration loading
python -c "
from app.core.config import get_settings
settings = get_settings()
print(f'AWS Secrets Enabled: {settings.AWS_SECRETS_ENABLED}')
print(f'Secret Key Length: {len(settings.SECRET_KEY)}')
print(f'Database URL: {settings.DATABASE_URL[:20]}...')
"
```

### 3. Test Docker Compose with Local Secrets

```bash
# Start services with local secrets
docker-compose up --build

# Check logs for AWS secrets status
docker-compose logs codeguardians-gateway | grep -i "aws secrets"

# Test health endpoint
curl -f http://localhost:8000/health/live
```

## AWS Secrets Manager Testing

### 1. Prerequisites

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Verify credentials
aws sts get-caller-identity
```

### 2. Create Test Secrets

```bash
# Run the setup script
./scripts/setup_aws_secrets.sh us-east-1 codeguardians-gateway/test

# Or manually create test secrets
aws secretsmanager create-secret \
  --name "codeguardians-gateway/test" \
  --secret-string '{
    "SECRET_KEY": "REPLACE_ME",
    "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test",
    "REDIS_URL": "redis://localhost:6379/0",
    "ENVIRONMENT": "test"
  }' \
  --region us-east-1
```

### 3. Test AWS Secrets Integration

```bash
# Set environment for AWS secrets
export AWS_SECRETS_ENABLED=true
export AWS_SECRETS_NAME=codeguardians-gateway/test
export AWS_REGION=us-east-1

# Test configuration loading
python -c "
from app.core.config import get_settings
settings = get_settings()
print(f'AWS Secrets Enabled: {settings.AWS_SECRETS_ENABLED}')
print(f'Secret Key: {settings.SECRET_KEY}')
print(f'Environment: {settings.ENVIRONMENT}')
"
```

### 4. Test Docker with AWS Secrets

```bash
# Build and run with AWS secrets
docker build -t codeguardians-gateway-test .
docker run -e AWS_SECRETS_ENABLED=true \
           -e AWS_SECRETS_NAME=codeguardians-gateway/test \
           -e AWS_REGION=us-east-1 \
           -v ~/.aws:/root/.aws:ro \
           codeguardians-gateway-test

# Check logs for successful secret loading
docker logs <container-id> | grep -i "secrets"
```

## Unit Testing with Mocks

### 1. Mock AWS Secrets Manager

Create a test file `tests/test_aws_secrets.py`:

```python
import pytest
from unittest.mock import patch, MagicMock
from app.core.aws_secrets import AWSSecretsManager, get_secret_value

class TestAWSSecretsManager:
    
    @patch('boto3.client')
    def test_fetch_secret_success(self, mock_boto_client):
        """Test successful secret fetching."""
        # Mock AWS response
        mock_client = MagicMock()
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"SECRET_KEY": "test-key", "DATABASE_URL": "test-url"}'
        }
        mock_boto_client.return_value = mock_client
        
        # Test secret fetching
        manager = AWSSecretsManager(region="us-east-1", secret_name="test-secret")
        secrets = manager.get_all_secrets()
        
        assert secrets["SECRET_KEY"] == "test-key"
        assert secrets["DATABASE_URL"] == "test-url"
        mock_client.get_secret_value.assert_called_once()
    
    @patch('boto3.client')
    def test_fetch_secret_not_found(self, mock_boto_client):
        """Test secret not found error."""
        from botocore.exceptions import ClientError
        
        # Mock AWS error
        mock_client = MagicMock()
        mock_client.get_secret_value.side_effect = ClientError(
            {'Error': {'Code': 'ResourceNotFoundException'}},
            'GetSecretValue'
        )
        mock_boto_client.return_value = mock_client
        
        # Test error handling
        manager = AWSSecretsManager(region="us-east-1", secret_name="nonexistent")
        
        with pytest.raises(Exception, match="Secret 'nonexistent' not found"):
            manager.get_all_secrets()
    
    @patch('boto3.client')
    def test_validate_required_secrets(self, mock_boto_client):
        """Test required secrets validation."""
        # Mock AWS response
        mock_client = MagicMock()
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"SECRET_KEY": "test", "DATABASE_URL": "test"}'
        }
        mock_boto_client.return_value = mock_client
        
        manager = AWSSecretsManager(region="us-east-1", secret_name="test")
        secrets = manager.get_all_secrets()
        
        # Test validation
        required_keys = ["SECRET_KEY", "DATABASE_URL"]
        assert manager.validate_required_secrets(required_keys) == True
        
        # Test missing secrets
        with pytest.raises(Exception, match="Missing required secrets"):
            manager.validate_required_secrets(["MISSING_KEY"])

    def test_get_secret_value_with_default(self):
        """Test getting secret value with default."""
        with patch.object(AWSSecretsManager, 'get_all_secrets') as mock_get_secrets:
            mock_get_secrets.return_value = {"SECRET_KEY": "test-value"}
            
            manager = AWSSecretsManager()
            value = manager.get_secret_value("SECRET_KEY", "default")
            assert value == "test-value"
            
            value = manager.get_secret_value("MISSING_KEY", "default")
            assert value == "default"
```

### 2. Mock Configuration Loading

Create `tests/test_config_aws_integration.py`:

```python
import pytest
from unittest.mock import patch, MagicMock
from app.core.config import Settings

class TestConfigAWSIntegration:
    
    @patch('app.core.aws_secrets.validate_aws_secrets_available')
    @patch('app.core.aws_secrets.get_aws_secrets_for_environment')
    def test_config_loads_aws_secrets(self, mock_get_secrets, mock_validate):
        """Test that configuration loads AWS secrets."""
        # Mock AWS secrets availability
        mock_validate.return_value = True
        mock_get_secrets.return_value = {
            "SECRET_KEY": "aws-secret-key",
            "DATABASE_URL": "aws-database-url"
        }
        
        # Test settings loading
        settings = Settings()
        
        assert settings.AWS_SECRETS_ENABLED == True
        assert settings.SECRET_KEY == "aws-secret-key"
        assert settings.DATABASE_URL == "aws-database-url"
    
    @patch('app.core.aws_secrets.validate_aws_secrets_available')
    def test_config_fallback_to_env_vars(self, mock_validate):
        """Test fallback to environment variables when AWS unavailable."""
        # Mock AWS secrets unavailable
        mock_validate.return_value = False
        
        # Set environment variables
        import os
        os.environ["SECRET_KEY"] = "env-secret-key"
        os.environ["DATABASE_URL"] = "env-database-url"
        
        # Test settings loading
        settings = Settings()
        
        assert settings.SECRET_KEY == "env-secret-key"
        assert settings.DATABASE_URL == "env-database-url"
```

### 3. Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run only AWS secrets tests
pytest tests/test_aws_secrets.py -v

# Run with coverage
pytest tests/ --cov=app.core.aws_secrets --cov-report=html
```

## Integration Testing

### 1. Test Full Application Startup

```python
# tests/test_integration.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

class TestAWSSecretsIntegration:
    
    def test_application_startup_with_aws_secrets(self):
        """Test application starts successfully with AWS secrets."""
        with patch('app.core.aws_secrets.validate_aws_secrets_available') as mock_validate:
            mock_validate.return_value = True
            
            # Test client creation
            client = TestClient(app)
            
            # Test health endpoint
            response = client.get("/health/live")
            assert response.status_code == 200
    
    def test_guard_endpoint_with_secrets(self):
        """Test guard endpoint works with AWS secrets."""
        with patch('app.core.aws_secrets.validate_aws_secrets_available') as mock_validate:
            mock_validate.return_value = True
            
            client = TestClient(app)
            
            # Test guard processing
            response = client.post("/api/v1/guards/process", json={
                "text": "test input",
                "service_type": "tokenguard"
            })
            
            assert response.status_code in [200, 503]  # 503 if guards not running
```

### 2. Test Docker Container Startup

```bash
# Test container startup with AWS secrets
docker run --rm \
  -e AWS_SECRETS_ENABLED=true \
  -e AWS_SECRETS_NAME=codeguardians-gateway/test \
  -e AWS_REGION=us-east-1 \
  -v ~/.aws:/root/.aws:ro \
  codeguardians-gateway-test \
  python -c "
from app.core.config import get_settings
settings = get_settings()
print('Configuration loaded successfully')
print(f'Secret Key: {settings.SECRET_KEY[:10]}...')
"
```

## Troubleshooting

### 1. Common Issues and Solutions

#### Issue: "AWS credentials not found"
```bash
# Solution: Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_DEFAULT_REGION=us-east-1
```

#### Issue: "Secret not found in AWS Secrets Manager"
```bash
# Solution: Create the secret
./scripts/setup_aws_secrets.sh us-east-1 codeguardians-gateway/production

# Or check existing secrets
aws secretsmanager list-secrets --region us-east-1
```

#### Issue: "Access denied to secret"
```bash
# Solution: Check IAM permissions
aws iam get-role-policy --role-name your-ecs-task-role --policy-name SecretsManagerAccess

# Or attach the required policy
aws iam attach-role-policy \
  --role-name your-ecs-task-role \
  --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
```

#### Issue: "boto3 not available"
```bash
# Solution: Install boto3
pip install boto3

# Or add to requirements.txt
echo "boto3>=1.34.0" >> requirements.txt
```

### 2. Debug AWS Secrets Loading

```python
# Debug script: debug_aws_secrets.py
import os
from app.core.aws_secrets import validate_aws_secrets_available, get_aws_secrets_for_environment

print("=== AWS Secrets Debug ===")
print(f"AWS_SECRETS_ENABLED: {os.getenv('AWS_SECRETS_ENABLED', 'not set')}")
print(f"AWS_SECRETS_NAME: {os.getenv('AWS_SECRETS_NAME', 'not set')}")
print(f"AWS_REGION: {os.getenv('AWS_REGION', 'not set')}")

print("\n=== AWS Credentials ===")
print(f"AWS_ACCESS_KEY_ID: {'set' if os.getenv('AWS_ACCESS_KEY_ID') else 'not set'}")
print(f"AWS_SECRET_ACCESS_KEY: {'set' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'not set'}")

print("\n=== AWS Secrets Manager ===")
try:
    available = validate_aws_secrets_available()
    print(f"Available: {available}")
    
    if available:
        secrets = get_aws_secrets_for_environment()
        print(f"Secrets loaded: {len(secrets)} keys")
        for key in secrets.keys():
            print(f"  - {key}")
    else:
        print("AWS Secrets Manager not available")
        
except Exception as e:
    print(f"Error: {e}")
```

### 3. Test Secret Rotation

```bash
# Test secret rotation
aws secretsmanager update-secret \
  --secret-id codeguardians-gateway/production \
  --secret-string '{
    "SECRET_KEY": "REPLACE_ME",
    "DATABASE_URL": "postgresql+asyncpg://user:new-password@host:5432/db",
    "REDIS_URL": "REPLACE_MEhost:6379/0"
  }' \
  --region us-east-1

# Test application picks up new secrets
docker restart codeguardians-gateway-container
docker logs codeguardians-gateway-container | grep -i "secrets"
```

## Secret Rotation Testing

### 1. Automated Secret Rotation

```python
# tests/test_secret_rotation.py
import pytest
from unittest.mock import patch, MagicMock
from app.core.aws_secrets import AWSSecretsManager

class TestSecretRotation:
    
    @patch('boto3.client')
    def test_secret_rotation_detection(self, mock_boto_client):
        """Test that rotated secrets are detected."""
        # Mock first call (old secret)
        mock_client = MagicMock()
        mock_client.get_secret_value.side_effect = [
            {'SecretString': '{"SECRET_KEY": "old-key"}'},
            {'SecretString': '{"SECRET_KEY": "new-key"}'}
        ]
        mock_boto_client.return_value = mock_client
        
        manager = AWSSecretsManager()
        
        # First fetch
        secrets1 = manager.get_all_secrets()
        assert secrets1["SECRET_KEY"] == "old-key"
        
        # Clear cache and fetch again
        manager.cache_timestamp = None
        secrets2 = manager.get_all_secrets()
        assert secrets2["SECRET_KEY"] == "new-key"
    
    def test_cache_invalidation(self):
        """Test cache invalidation for secret rotation."""
        manager = AWSSecretsManager()
        manager.secrets_cache = {"SECRET_KEY": "cached-key"}
        manager.cache_timestamp = datetime.now()
        
        # Force refresh
        manager.refresh_secrets()
        
        # Cache should be cleared
        assert manager.cache_timestamp is None
        assert not manager.secrets_cache
```

### 2. Test Rotation in Production

```bash
# Create rotation schedule
aws secretsmanager update-secret \
  --secret-id codeguardians-gateway/production \
  --description "Auto-rotating secret" \
  --region us-east-1

# Set up automatic rotation (requires Lambda function)
aws secretsmanager update-secret \
  --secret-id codeguardians-gateway/production \
  --secret-string '{"SECRET_KEY": "auto-rotated-key"}' \
  --region us-east-1

# Test application handles rotation gracefully
curl -f https://your-alb-dns-name/health/live
```

## Performance Testing

### 1. Secret Loading Performance

```python
# tests/test_performance.py
import time
import pytest
from app.core.aws_secrets import AWSSecretsManager

class TestPerformance:
    
    @patch('boto3.client')
    def test_secret_loading_performance(self, mock_boto_client):
        """Test secret loading performance."""
        mock_client = MagicMock()
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"SECRET_KEY": "test", "DATABASE_URL": "test"}'
        }
        mock_boto_client.return_value = mock_client
        
        manager = AWSSecretsManager()
        
        # Test first load (cache miss)
        start_time = time.time()
        secrets = manager.get_all_secrets()
        first_load_time = time.time() - start_time
        
        # Test second load (cache hit)
        start_time = time.time()
        secrets = manager.get_all_secrets()
        second_load_time = time.time() - start_time
        
        # Cache hit should be much faster
        assert second_load_time < first_load_time
        assert second_load_time < 0.001  # Should be under 1ms
```

### 2. Concurrent Access Testing

```python
import asyncio
import pytest
from concurrent.futures import ThreadPoolExecutor

class TestConcurrentAccess:
    
    @patch('boto3.client')
    def test_concurrent_secret_access(self, mock_boto_client):
        """Test concurrent access to secrets."""
        mock_client = MagicMock()
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"SECRET_KEY": "test"}'
        }
        mock_boto_client.return_value = mock_client
        
        manager = AWSSecretsManager()
        
        def fetch_secret():
            return manager.get_secret_value("SECRET_KEY")
        
        # Test concurrent access
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_secret) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # All should return the same value
        assert all(result == "test" for result in results)
```

## Best Practices

### 1. Test Environment Setup

```bash
# Create separate test environment
export AWS_SECRETS_NAME=codeguardians-gateway/test
export AWS_REGION=us-east-1
export ENVIRONMENT=test

# Use test-specific secrets
aws secretsmanager create-secret \
  --name "codeguardians-gateway/test" \
  --secret-string '{"SECRET_KEY": "test-key", "DATABASE_URL": "test-db"}' \
  --region us-east-1
```

### 2. Test Data Management

```python
# Use fixtures for test data
@pytest.fixture
def test_secrets():
    return {
        "SECRET_KEY": "REPLACE_ME",
        "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test",
        "REDIS_URL": "redis://localhost:6379/0"
    }

@pytest.fixture
def mock_aws_secrets(test_secrets):
    with patch('app.core.aws_secrets.get_aws_secrets_for_environment') as mock:
        mock.return_value = test_secrets
        yield mock
```

### 3. Continuous Integration

```yaml
# .github/workflows/test-aws-secrets.yml
name: Test AWS Secrets Integration

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
          pip install pytest pytest-cov
      
      - name: Run tests with mocked AWS
        run: |
          export AWS_SECRETS_ENABLED=false
          pytest tests/ -v --cov=app.core.aws_secrets
      
      - name: Test AWS integration (if credentials available)
        if: env.AWS_ACCESS_KEY_ID
        run: |
          export AWS_SECRETS_ENABLED=true
          pytest tests/test_aws_integration.py -v
```

---

## Quick Reference

### Essential Commands
```bash
# Test local development
export AWS_SECRETS_ENABLED=false
python -c "from app.core.config import get_settings; print(get_settings().SECRET_KEY)"

# Test AWS secrets
export AWS_SECRETS_ENABLED=true
./scripts/setup_aws_secrets.sh us-east-1 codeguardians-gateway/test
python -c "from app.core.config import get_settings; print(get_settings().SECRET_KEY)"

# Run tests
pytest tests/test_aws_secrets.py -v
pytest tests/ --cov=app.core.aws_secrets
```

### Debug Commands
```bash
# Check AWS credentials
aws sts get-caller-identity

# List secrets
aws secretsmanager list-secrets --region us-east-1

# Test secret access
aws secretsmanager get-secret-value --secret-id codeguardians-gateway/production --region us-east-1

# Debug application
python debug_aws_secrets.py
```

### Environment Variables
```bash
# Local development
AWS_SECRETS_ENABLED=false
SECRET_KEY=local-secret-key
DATABASE_URL=postgresql://localhost:5432/db

# AWS testing
AWS_SECRETS_ENABLED=true
AWS_SECRETS_NAME=codeguardians-gateway/test
AWS_REGION=us-east-1
```
