"""
Basic tests that verify core functionality without complex dependencies.
"""

import pytest
from pydantic import ValidationError


class TestBasicFunctionality:
    """Test basic application functionality."""
    
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
    
    def test_import_security(self):
        """Test that security modules can be imported."""
        from app.core.security import get_password_hash, verify_password
        assert get_password_hash is not None
        assert verify_password is not None


class TestPydanticSchemas:
    """Test Pydantic schema validation."""
    
    def test_user_create_schema(self):
        """Test UserCreate schema validation."""
        from app.api.v1.users import UserCreate
        
        # Valid user data
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
        """Test UserCreate with invalid email."""
        from app.api.v1.users import UserCreate
        
        with pytest.raises(ValidationError):
            UserCreate(
                email="invalid-email",
                REPLACE_ME,
                full_name="Test User"
            )
    
    def test_user_create_weak_password(self):
        """Test UserCreate with weak password."""
        from app.api.v1.users import UserCreate
        
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                password="123",  # Too short
                full_name="Test User"
            )
    
    def test_post_create_schema(self):
        """Test PostCreate schema validation."""
        from app.api.v1.posts import PostCreate
        
        # Valid post data
        post_data = {
            "title": "Test Post",
            "content": "This is test content"
        }
        
        post = PostCreate(**post_data)
        assert post.title == "Test Post"
        assert post.content == "This is test content"
        assert post.is_published is False
        assert post.is_featured is False
    
    def test_post_create_empty_title(self):
        """Test PostCreate with empty title."""
        from app.api.v1.posts import PostCreate
        
        with pytest.raises(ValidationError):
            PostCreate(
                title="",  # Empty title
                content="Test content"
            )


class TestApplicationEndpoints:
    """Test basic application endpoints."""
    
    def test_health_endpoint_import(self):
        """Test that health endpoints can be imported."""
        # Health endpoints are in main.py, not a separate module
        from app.main import app
        assert app is not None
    
    def test_auth_endpoint_import(self):
        """Test that auth endpoints can be imported."""
        from app.api.v1 import auth
        assert auth is not None
    
    def test_users_endpoint_import(self):
        """Test that users endpoints can be imported."""
        from app.api.v1 import users
        assert users is not None


class TestDatabaseModels:
    """Test database model definitions."""
    
    def test_user_model_fields(self):
        """Test User model has required fields."""
        from app.core.models import User
        
        # Check that User model has expected attributes
        assert hasattr(User, '__tablename__')
        assert hasattr(User, 'id')
        assert hasattr(User, 'email')
        assert hasattr(User, 'full_name')
        assert hasattr(User, 'is_active')
    
    def test_post_model_fields(self):
        """Test Post model has required fields."""
        from app.core.models import Post
        
        # Check that Post model has expected attributes
        assert hasattr(Post, '__tablename__')
        assert hasattr(Post, 'id')
        assert hasattr(Post, 'title')
        assert hasattr(Post, 'content')
        assert hasattr(Post, 'is_published')
