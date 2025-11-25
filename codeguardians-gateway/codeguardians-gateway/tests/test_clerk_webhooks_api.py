"""
Integration tests for Clerk webhooks API.

This module tests the API endpoints for handling Clerk webhook events.
"""

import pytest
import json
import os
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import create_app
from app.core.models import User

# Set database enabled for tests
os.environ.setdefault("DATABASE_ENABLED", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")


@pytest.fixture
def app():
    """Create test application."""
    # Set database enabled before creating app
    os.environ["DATABASE_ENABLED"] = "true"
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    return create_app()


@pytest.fixture
def client(app, mock_db):
    """Create test client."""
    from app.core.database import get_db
    
    # Override get_db dependency to return mock_db
    async def override_get_db():
        yield mock_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def mock_db():
    """Create mock database session."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def valid_user_created_payload():
    """Valid user.created webhook payload."""
    return {
        "type": "user.created",
        "data": {
            "id": "user_test123",
            "first_name": "John",
            "last_name": "Doe",
            "email_addresses": [{"email_address": "john.doe@example.com"}],
            "image_url": "https://example.com/image.jpg",
            "created_at": 1761092033534,
            "updated_at": 1761092033553,
            "banned": False,
            "locked": False,
            "two_factor_enabled": False
        }
    }


@pytest.fixture
def valid_user_updated_payload():
    """Valid user.updated webhook payload."""
    return {
        "type": "user.updated",
        "data": {
            "id": "user_test123",
            "first_name": "John",
            "last_name": "Smith",  # Updated last name
            "email_addresses": [{"email_address": "john.smith@example.com"}],
            "image_url": "https://example.com/new-image.jpg",
            "created_at": 1761092033534,
            "updated_at": 1761092033553,
            "banned": False,
            "locked": False,
            "two_factor_enabled": False
        }
    }


@pytest.fixture
def valid_user_deleted_payload():
    """Valid user.deleted webhook payload."""
    return {
        "type": "user.deleted",
        "data": {
            "id": "user_test123"
        }
    }


class TestClerkWebhooksAPI:
    """Test cases for Clerk webhooks API endpoints."""
    
    @patch('app.api.webhooks.clerk_webhooks.get_db')
    @patch('app.api.webhooks.clerk_webhooks.process_clerk_webhook')
    def test_handle_clerk_webhook_user_created_success(
        self, mock_process_webhook, mock_get_db, client, valid_user_created_payload, mock_db
    ):
        """Test successful user.created webhook processing."""
        # Setup mocks
        mock_get_db.return_value = mock_db
        mock_process_webhook.return_value = True
        
        # Make request
        response = client.post(
            "/webhooks/clerk",
            json=valid_user_created_payload,
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["event_type"] == "user.created"
        mock_process_webhook.assert_called_once()

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    @patch('app.api.webhooks.clerk_webhooks.process_clerk_webhook')
    def test_handle_clerk_webhook_user_updated_success(
        self, mock_process_webhook, mock_get_db, client, valid_user_updated_payload, mock_db
    ):
        """Test successful user.updated webhook processing."""
        # Setup mocks
        mock_get_db.return_value = mock_db
        mock_process_webhook.return_value = True
        
        # Make request
        response = client.post(
            "/webhooks/clerk",
            json=valid_user_updated_payload,
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["event_type"] == "user.updated"

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    @patch('app.api.webhooks.clerk_webhooks.process_clerk_webhook')
    def test_handle_clerk_webhook_user_deleted_success(
        self, mock_process_webhook, mock_get_db, client, valid_user_deleted_payload, mock_db
    ):
        """Test successful user.deleted webhook processing."""
        # Setup mocks
        mock_get_db.return_value = mock_db
        mock_process_webhook.return_value = True
        
        # Make request
        response = client.post(
            "/webhooks/clerk",
            json=valid_user_deleted_payload,
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["event_type"] == "user.deleted"

    def test_handle_clerk_webhook_invalid_json(self, client):
        """Test webhook with invalid JSON."""
        response = client.post(
            "/webhooks/clerk",
            data="invalid json",
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Invalid JSON payload" in data["detail"]

    def test_handle_clerk_webhook_missing_event_type(self, client):
        """Test webhook with missing event type."""
        payload = {"data": {"id": "user123"}}
        
        response = client.post(
            "/webhooks/clerk",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Missing event type" in data["detail"]

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    @patch('app.api.webhooks.clerk_webhooks.process_clerk_webhook')
    def test_handle_clerk_webhook_processing_failure(
        self, mock_process_webhook, mock_get_db, client, valid_user_created_payload, mock_db
    ):
        """Test webhook processing failure."""
        # Setup mocks
        mock_get_db.return_value = mock_db
        mock_process_webhook.return_value = False
        
        # Make request
        response = client.post(
            "/webhooks/clerk",
            json=valid_user_created_payload,
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        # Assertions
        assert response.status_code == 500
        data = response.json()
        assert data["status"] == "error"
        assert data["event_type"] == "user.created"

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    @patch('app.api.webhooks.clerk_webhooks.process_clerk_webhook')
    def test_handle_clerk_webhook_exception(
        self, mock_process_webhook, mock_get_db, client, valid_user_created_payload, mock_db
    ):
        """Test webhook with unexpected exception."""
        # Setup mocks
        mock_get_db.return_value = mock_db
        mock_process_webhook.side_effect = Exception("Unexpected error")
        
        # Make request
        response = client.post(
            "/webhooks/clerk",
            json=valid_user_created_payload,
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        # Assertions
        assert response.status_code == 500
        data = response.json()
        assert "Internal server error" in data["detail"]

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    def test_get_user_by_clerk_id_success(self, mock_get_db, client, mock_db):
        """Test successful user retrieval by Clerk ID."""
        # Mock user data
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.clerk_user_id = "user_test123"
        mock_user.email = "john.doe@example.com"
        mock_user.full_name = "John Doe"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.username = "johndoe"
        mock_user.is_active = True
        mock_user.is_verified = True
        mock_user.created_at = "2024-01-01T00:00:00Z"
        mock_user.updated_at = "2024-01-01T00:00:00Z"
        mock_user.last_login = None
        mock_user.last_active_at = None
        mock_user.last_sign_in_at = None
        mock_user.image_url = "https://example.com/image.jpg"
        mock_user.profile_image_url = "https://example.com/profile.jpg"
        mock_user.locale = "en"
        mock_user.banned = False
        mock_user.locked = False
        mock_user.two_factor_enabled = False
        mock_user.stripe_customer_id = "cus_test123"
        
        # Mock database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value = mock_db
        
        # Make request
        response = client.get("/api/v1/clerk/users/user_test123", headers={"Host": "localhost"})
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["clerk_user_id"] == "user_test123"
        assert data["email"] == "john.doe@example.com"
        assert data["full_name"] == "John Doe"

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    def test_get_user_by_clerk_id_not_found(self, mock_get_db, client, mock_db):
        """Test user retrieval by Clerk ID when user not found."""
        # Mock no user found
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value = mock_db
        
        # Make request
        response = client.get("/api/v1/clerk/users/nonexistent_user", headers={"Host": "localhost"})
        
        # Assertions
        assert response.status_code == 404
        data = response.json()
        assert "User not found" in data["detail"]

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    def test_get_user_by_email_success(self, mock_get_db, client, mock_db):
        """Test successful user retrieval by email."""
        # Mock user data
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.clerk_user_id = "user_test123"
        mock_user.email = "john.doe@example.com"
        mock_user.full_name = "John Doe"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.username = "johndoe"
        mock_user.is_active = True
        mock_user.is_verified = True
        mock_user.created_at = "2024-01-01T00:00:00Z"
        mock_user.updated_at = "2024-01-01T00:00:00Z"
        mock_user.last_login = None
        mock_user.last_active_at = None
        mock_user.last_sign_in_at = None
        mock_user.image_url = "https://example.com/image.jpg"
        mock_user.profile_image_url = "https://example.com/profile.jpg"
        mock_user.locale = "en"
        mock_user.banned = False
        mock_user.locked = False
        mock_user.two_factor_enabled = False
        mock_user.stripe_customer_id = "cus_test123"
        
        # Mock database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value = mock_db
        
        # Make request
        response = client.get("/api/v1/clerk/users/email/john.doe@example.com", headers={"Host": "localhost"})
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "john.doe@example.com"
        assert data["clerk_user_id"] == "user_test123"

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    def test_get_user_by_email_not_found(self, mock_get_db, client, mock_db):
        """Test user retrieval by email when user not found."""
        # Mock no user found
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value = mock_db
        
        # Make request
        response = client.get("/api/v1/clerk/users/email/nonexistent@example.com", headers={"Host": "localhost"})
        
        # Assertions
        assert response.status_code == 404
        data = response.json()
        assert "User not found" in data["detail"]

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    def test_get_user_by_clerk_id_database_error(self, mock_get_db, client, mock_db):
        """Test user retrieval with database error."""
        # Mock database error
        mock_db.execute.side_effect = Exception("Database error")
        mock_get_db.return_value = mock_db
        
        # Make request
        response = client.get("/api/v1/clerk/users/user_test123", headers={"Host": "localhost"})
        
        # Assertions
        assert response.status_code == 500
        data = response.json()
        assert "Internal server error" in data["detail"]

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    @patch('app.api.webhooks.clerk_webhooks.process_clerk_webhook')
    def test_handle_clerk_webhook_email_required_error(
        self, mock_process_webhook, mock_get_db, client, valid_user_created_payload, mock_db
    ):
        """Test webhook handler raises EmailRequiredError correctly."""
        from app.core.exceptions import EmailRequiredError
        
        # Setup mocks
        mock_get_db.return_value = mock_db
        mock_process_webhook.side_effect = EmailRequiredError(
            message="Email address is required for user creation",
            details={"user_id": "user_test123", "field": "email_addresses"}
        )
        
        # Make request
        response = client.post(
            "/webhooks/clerk",
            json=valid_user_created_payload,
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        # Assertions
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error"] == "EMAIL_REQUIRED"
        assert "Email address is required" in data["detail"]["message"]
        assert data["detail"]["details"]["user_id"] == "user_test123"
        assert data["detail"]["details"]["field"] == "email_addresses"

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    @patch('app.api.webhooks.clerk_webhooks.process_clerk_webhook')
    def test_handle_clerk_webhook_validation_error(
        self, mock_process_webhook, mock_get_db, client, valid_user_created_payload, mock_db
    ):
        """Test webhook handler raises ValidationError correctly."""
        from app.core.exceptions import ValidationError
        
        # Setup mocks
        mock_get_db.return_value = mock_db
        mock_process_webhook.side_effect = ValidationError(
            message="Invalid user data format",
            details={"field": "first_name", "reason": "invalid_format"},
            error_code="INVALID_FORMAT"
        )
        
        # Make request
        response = client.post(
            "/webhooks/clerk",
            json=valid_user_created_payload,
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        # Assertions
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error"] == "INVALID_FORMAT"
        assert "Invalid user data format" in data["detail"]["message"]
        assert data["detail"]["details"]["field"] == "first_name"

    @patch('app.api.webhooks.clerk_webhooks.get_db')
    @patch('app.api.webhooks.clerk_webhooks.process_clerk_webhook')
    def test_handle_clerk_webhook_validation_error_default_code(
        self, mock_process_webhook, mock_get_db, client, valid_user_created_payload, mock_db
    ):
        """Test webhook handler with ValidationError using default error code."""
        from app.core.exceptions import ValidationError
        
        # Setup mocks
        mock_get_db.return_value = mock_db
        mock_process_webhook.side_effect = ValidationError(
            message="Validation failed",
            details={"issue": "data_format"}
        )
        
        # Make request
        response = client.post(
            "/webhooks/clerk",
            json=valid_user_created_payload,
            headers={
                "Content-Type": "application/json",
                "Host": "localhost"
            }
        )
        
        # Assertions
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error"] == "VALIDATION_ERROR"  # Default error code
        assert "Validation failed" in data["detail"]["message"]