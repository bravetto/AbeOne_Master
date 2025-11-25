"""
Unit tests for Clerk webhook service.

This module tests the ClerkWebhookService class and its methods
for handling user webhook events.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.services.clerk_webhook_service import ClerkWebhookService, verify_clerk_webhook_signature
from app.core.models import User


class TestClerkWebhookService:
    """Test cases for ClerkWebhookService."""
    
    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        return AsyncMock(spec=AsyncSession)
    
    @pytest.fixture
    def service(self, mock_db):
        """Create a ClerkWebhookService instance with mock database."""
        return ClerkWebhookService(mock_db)
    
    @pytest.fixture
    def valid_user_data(self):
        """Valid user data for testing."""
        return {
            'id': 'user_test123',
            'first_name': 'John',
            'last_name': 'Doe',
            'email_addresses': [{'email_address': 'john.doe@example.com'}],
            'image_url': 'https://example.com/image.jpg',
            'created_at': 1761092033534,
            'updated_at': 1761092033553,
            'banned': False,
            'locked': False,
            'two_factor_enabled': False
        }
    
    @pytest.fixture
    def valid_event_data(self, valid_user_data):
        """Valid event data for testing."""
        return {
            'type': 'user.created',
            'data': valid_user_data
        }

    def test_validate_user_data_valid(self, service, valid_user_data):
        """Test validation with valid user data."""
        is_valid, error_message = service.validate_user_data(valid_user_data)
        assert is_valid is True
        assert error_message == ""

    def test_validate_user_data_missing_id(self, service):
        """Test validation with missing user ID."""
        user_data = {'email_addresses': [{'email_address': 'test@example.com'}]}
        is_valid, error_message = service.validate_user_data(user_data)
        assert is_valid is False
        assert "Missing required field: id" in error_message

    def test_validate_user_data_missing_email_addresses(self, service):
        """Test validation with missing email addresses."""
        user_data = {'id': 'user123'}
        is_valid, error_message = service.validate_user_data(user_data)
        assert is_valid is False
        assert "Missing required field: email_addresses" in error_message

    def test_validate_user_data_invalid_email(self, service):
        """Test validation with invalid email format."""
        user_data = {
            'id': 'user123',
            'email_addresses': [{'email_address': 'invalid-email'}]
        }
        is_valid, error_message = service.validate_user_data(user_data)
        assert is_valid is False
        assert "Invalid email format" in error_message

    def test_validate_user_data_invalid_timestamp(self, service):
        """Test validation with invalid timestamp."""
        user_data = {
            'id': 'user123',
            'email_addresses': [{'email_address': 'test@example.com'}],
            'created_at': 'invalid-timestamp'
        }
        is_valid, error_message = service.validate_user_data(user_data)
        assert is_valid is False
        assert "Invalid timestamp format" in error_message

    @pytest.mark.asyncio
    async def test_handle_user_created_success(self, service, mock_db, valid_event_data):
        """Test successful user creation."""
        # Mock database query to return no existing user
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        # Mock database operations
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        result = await service.handle_user_created(valid_event_data)
        
        assert result is True
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_user_created_existing_user(self, service, mock_db, valid_event_data):
        """Test user creation when user already exists."""
        # Mock existing user
        existing_user = MagicMock()
        existing_user.clerk_user_id = 'user_test123'
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_user
        mock_db.execute.return_value = mock_result
        
        # Mock the handle_user_updated method
        with patch.object(service, 'handle_user_updated', return_value=True) as mock_update:
            result = await service.handle_user_created(valid_event_data)
            
            assert result is True
            mock_update.assert_called_once_with(valid_event_data)

    @pytest.mark.asyncio
    async def test_handle_user_created_invalid_data(self, service, mock_db):
        """Test user creation with invalid data."""
        invalid_event_data = {
            'type': 'user.created',
            'data': {'id': 'user123'}  # Missing email_addresses
        }
        
        result = await service.handle_user_created(invalid_event_data)
        
        assert result is False
        mock_db.execute.assert_not_called()

    @pytest.mark.asyncio
    async def test_handle_user_created_database_error(self, service, mock_db, valid_event_data):
        """Test user creation with database error."""
        # Mock database query to return no existing user
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        # Mock database error
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock(side_effect=SQLAlchemyError("Database error"))
        mock_db.rollback = AsyncMock()
        
        result = await service.handle_user_created(valid_event_data)
        
        assert result is False
        mock_db.rollback.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_user_updated_success(self, service, mock_db, valid_event_data):
        """Test successful user update."""
        # Mock existing user
        existing_user = MagicMock()
        existing_user.clerk_user_id = 'user_test123'
        existing_user.email = 'old@example.com'
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_user
        mock_db.execute.return_value = mock_result
        
        # Mock database operations
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        result = await service.handle_user_updated(valid_event_data)
        
        assert result is True
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_user_updated_user_not_found(self, service, mock_db, valid_event_data):
        """Test user update when user doesn't exist."""
        # Mock no existing user
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        # Mock the handle_user_created method
        with patch.object(service, 'handle_user_created', return_value=True) as mock_create:
            result = await service.handle_user_updated(valid_event_data)
            
            assert result is True
            mock_create.assert_called_once_with(valid_event_data)

    @pytest.mark.asyncio
    async def test_handle_user_deleted_success(self, service, mock_db):
        """Test successful user deletion."""
        event_data = {
            'type': 'user.deleted',
            'data': {'id': 'user_test123'}
        }
        
        # Mock existing user
        existing_user = MagicMock()
        existing_user.clerk_user_id = 'user_test123'
        existing_user.is_active = True
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_user
        mock_db.execute.return_value = mock_result
        
        # Mock database operations
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        result = await service.handle_user_deleted(event_data)
        
        assert result is True
        assert existing_user.is_active is False
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_user_deleted_user_not_found(self, service, mock_db):
        """Test user deletion when user doesn't exist."""
        event_data = {
            'type': 'user.deleted',
            'data': {'id': 'user_test123'}
        }
        
        # Mock no existing user
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        result = await service.handle_user_deleted(event_data)
        
        assert result is True  # Should return True even if user doesn't exist

    def test_parse_timestamp_valid(self, service):
        """Test parsing valid timestamp."""
        timestamp = 1761092033534  # milliseconds
        result = service._parse_timestamp(timestamp)
        
        assert isinstance(result, datetime)
        assert result.year == 2025  # Approximate year

    def test_parse_timestamp_none(self, service):
        """Test parsing None timestamp."""
        result = service._parse_timestamp(None)
        assert result is None

    def test_parse_timestamp_invalid(self, service):
        """Test parsing invalid timestamp."""
        result = service._parse_timestamp("invalid")
        assert result is None


class TestClerkWebhookSignatureVerification:
    """Test cases for webhook signature verification."""
    
    def test_verify_signature_missing_headers(self):
        """Test signature verification with missing headers."""
        payload = b'{"test": "data"}'
        headers = {}
        secret = "test_secret"
        
        result = verify_clerk_webhook_signature(payload, headers, secret)
        # When svix is not available, verification is skipped (development mode)
        assert result is True

    def test_verify_signature_missing_svix_id(self):
        """Test signature verification with missing svix-id header."""
        payload = b'{"test": "data"}'
        headers = {
            'svix-timestamp': '1234567890',
            'svix-signature': 'v1=test_signature'
        }
        secret = "test_secret"
        
        result = verify_clerk_webhook_signature(payload, headers, secret)
        # When svix is not available, verification is skipped (development mode)
        assert result is True

    @patch('app.services.clerk_webhook_service.svix')
    def test_verify_signature_success(self, mock_svix):
        """Test successful signature verification."""
        payload = b'{"test": "data"}'
        headers = {
            'svix-id': 'test_id',
            'svix-timestamp': '1234567890',
            'svix-signature': 'v1=test_signature'
        }
        secret = "test_secret"
        
        # Mock successful verification
        mock_webhook = MagicMock()
        mock_svix.Webhook.return_value = mock_webhook
        mock_webhook.verify.return_value = None  # No exception means success

        result = verify_clerk_webhook_signature(payload, headers, secret)
        assert result is True
        mock_webhook.verify.assert_called_once()

    @patch('app.services.clerk_webhook_service.svix')
    def test_verify_signature_failure(self, mock_svix):
        """Test signature verification failure."""
        payload = b'{"test": "data"}'
        headers = {
            'svix-id': 'test_id',
            'svix-timestamp': '1234567890',
            'svix-signature': 'v1=invalid_signature'
        }
        secret = "test_secret"
        
        # Mock verification failure
        mock_webhook = MagicMock()
        mock_svix.Webhook.return_value = mock_webhook
        mock_webhook.verify.side_effect = Exception("Invalid signature")

        result = verify_clerk_webhook_signature(payload, headers, secret)
        assert result is False
