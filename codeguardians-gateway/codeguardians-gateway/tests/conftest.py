"""
Simplified pytest configuration and fixtures for testing.

This module provides basic fixtures without complex imports.
"""

import asyncio
import os
import sys
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import Mock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Add tests directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app.core.config import get_settings
from app.core.database import get_db, Base
from app.main import app
from app.core.models import User, Post
from app.core.security import create_access_token


# Test configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings():
    """Test settings with in-memory database."""
    settings = get_settings()
    settings.DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    settings.SECRET_KEY = "test-secret-key"
    settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
    settings.ENVIRONMENT = "test"
    return settings


@pytest_asyncio.fixture(scope="session")
async def test_engine(test_settings):
    """Create test database engine."""
    engine = create_async_engine(
        test_settings.DATABASE_URL,
        echo=False,
        future=True
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Clean up
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def test_session_factory(test_engine):
    """Create test session factory."""
    return sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


@pytest_asyncio.fixture
async def db_session(test_session_factory):
    """Create database session for testing."""
    async with test_session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
def client(test_settings, db_session):
    """Create test client."""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(test_settings, db_session):
    """Create async test client."""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user():
    """Create test user."""
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_REPLACE_ME,
        is_active=True
    )


@pytest.fixture
def test_post():
    """Create test post."""
    return Post(
        id=1,
        title="Test Post",
        content="Test content",
        author_id=1
    )


@pytest.fixture
def auth_headers(test_user):
    """Create auth headers for test user."""
    token = create_access_token(data={"sub": test_user.username})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    mock_redis = Mock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    mock_redis.delete.return_value = True
    mock_redis.exists.return_value = False
    mock_redis.ping.return_value = True
    return mock_redis


@pytest.fixture
def test_logger():
    """Provide a test-specific logger."""
    import logging
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    return logger


# Guard Service Fixtures
@pytest.fixture
def guard_services():
    """Fixture providing access to all guard services."""
    return {
        'securityguard': 'http://localhost:8005',
        'contextguard': 'http://localhost:8003',
        'trustguard': 'http://localhost:8002',
        'biasguard': 'http://localhost:8004'
    }


@pytest.fixture
def gateway_url():
    """Fixture providing the gateway URL."""
    return 'http://localhost:8000'


@pytest_asyncio.fixture
async def http_client():
    """Fixture providing HTTP client for testing."""
    async with AsyncClient() as client:
        yield client


@pytest.fixture
def sample_payloads():
    """Fixture providing sample payloads for testing."""
    return {
        'security_scan': {
            'content': 'This is normal content for security scanning',
            'content_type': 'text',
            'scan_level': 'standard'
        },
        'malicious_content': {
            'content': 'This is malicious content with potential threats',
            'content_type': 'text',
            'scan_level': 'deep'
        },
        'context_set': {
            'operation': 'set',
            'data': {
                'key': 'test_key',
                'value': 'test_value'
            },
            'consciousness_context': {
                'context': 'test context'
            }
        },
        'trust_validation': {
            'validation_type': 'general',
            'content': 'This is content for trust validation',
            'validation_level': 'standard'
        },
        'bias_detection': {
            'operation': 'detect_bias',
            'data': {
                'text': 'This is neutral content for bias detection'
            },
            'context': {
                'context': 'neutral context'
            }
        }
    }
