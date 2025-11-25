"""
Simple tests that don't require complex fixtures.
These tests verify basic functionality without database dependencies.

NOTE: These tests overlap with test_basic.py and are kept for backwards compatibility.
For new tests, add them to test_basic.py instead.
"""

import pytest
from pydantic import ValidationError
from app.api.v1.users import UserCreate, UserUpdate
from app.api.v1.posts import PostCreate, PostUpdate
from app.core.security import get_password_hash, verify_password


class TestPasswordHashing:
    """Test password hashing functionality."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpass123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrongpass", hashed)
    
    def test_password_hashing_short_password(self):
        """Test password hashing with short password (bcrypt limit)."""
        password = "pass123"  # Short password to avoid bcrypt 72-byte limit
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed)


class TestUserSchemas:
    """Test Pydantic user schemas."""
    
    def test_user_create_valid(self):
        """Test valid user creation."""
        user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
        
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.password == "testpass123"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert user.is_superuser is False
    
    def test_user_create_invalid_email(self):
        """Test user creation with invalid email."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="invalid-email",
                REPLACE_ME,
                full_name="Test User"
            )
    
    def test_user_create_weak_password(self):
        """Test user creation with weak password."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                password="123",  # Too short
                full_name="Test User"
            )
    
    def test_user_update_partial(self):
        """Test partial user update."""
        user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
        
        user = UserCreate(**user_data)
        update_data = {"full_name": "Updated Name"}
        
        update = UserUpdate(**update_data)
        assert update.full_name == "Updated Name"
        assert update.email is None
        assert update.is_active is None


class TestPostSchemas:
    """Test Pydantic post schemas."""
    
    def test_post_create_valid(self):
        """Test valid post creation."""
        post_data = {
            "title": "Test Post",
            "content": "This is test content for validation"
        }
        
        post = PostCreate(**post_data)
        assert post.title == "Test Post"
        assert post.content == "This is test content for validation"
        assert post.is_published is False
    
    def test_post_create_empty_title(self):
        """Test post creation with empty title."""
        with pytest.raises(ValidationError):
            PostCreate(
                title="",  # Empty title
                content="Test content",
                author_id=1
            )
    
    def test_post_update_partial(self):
        """Test partial post update."""
        update_data = {"title": "Updated Title"}
        
        update = PostUpdate(**update_data)
        assert update.title == "Updated Title"
        assert update.content is None
        assert update.is_published is None


class TestApplicationHealth:
    """Test application health and basic functionality."""
    
    def test_import_app(self):
        """Test that the main app can be imported."""
        from app.main import app
        assert app is not None
    
    def test_import_config(self):
        """Test that configuration can be imported."""
        from app.core.config import get_settings
        settings = get_settings()
        assert settings is not None
        assert hasattr(settings, 'SECRET_KEY')
        assert hasattr(settings, 'DATABASE_URL')
    
    def test_import_models(self):
        """Test that models can be imported."""
        from app.core.models import User, Post
        assert User is not None
        assert Post is not None
