"""
🌊💎✨ Swagger UI Integration Tests ✨💎🌊

Guardian: Jōhn (530 Hz)
"Do it right or don't do it at all"

Unit tests for Swagger UI conditional enablement based on environment.
Tests the core logic with convergence patterns in mind.

Convergence Patterns Applied:
- SIMPLICITY: Clear test structure, one assertion per test
- HARDENING: Type safety, edge cases, invalid inputs
- ELEGANCE: Beautiful test organization, clear naming
- VALUE: Every test serves purpose, zero redundancy
"""

import os
import pytest
from unittest.mock import patch
from fastapi import FastAPI

from app.main import create_app
from app.core.config import get_settings


class TestSwaggerUIEnvironmentControl:
    """Test Swagger UI conditional enablement based on ENVIRONMENT."""
    
    def test_development_mode_enables_all_docs(self):
        """SIMPLICITY: Development mode enables all documentation endpoints."""
        with patch.dict(os.environ, {"ENVIRONMENT": "development"}):
            # Reload app to pick up new environment
            from app.main import create_app
            app = create_app()
            
            assert app.docs_url == "/docs", "Swagger UI should be enabled in development"
            assert app.redoc_url == "/redoc", "ReDoc should be enabled in development"
            assert app.openapi_url == "/openapi.json", "OpenAPI JSON should be enabled in development"
    
    def test_production_mode_disables_all_docs(self):
        """HARDENING: Production mode disables all documentation endpoints."""
        with patch.dict(os.environ, {"ENVIRONMENT": "production"}):
            from app.main import create_app
            app = create_app()
            
            assert app.docs_url is None, "Swagger UI should be disabled in production"
            assert app.redoc_url is None, "ReDoc should be disabled in production"
            assert app.openapi_url is None, "OpenAPI JSON should be disabled in production"
    
    def test_case_insensitive_environment_check(self):
        """HARDENING: Environment check should be case-insensitive."""
        # Test uppercase
        with patch.dict(os.environ, {"ENVIRONMENT": "DEVELOPMENT"}):
            from app.main import create_app
            app = create_app()
            assert app.docs_url == "/docs", "Should work with uppercase DEVELOPMENT"
        
        # Test mixed case
        with patch.dict(os.environ, {"ENVIRONMENT": "DeVeLoPmEnT"}):
            from app.main import create_app
            app = create_app()
            assert app.docs_url == "/docs", "Should work with mixed case"
        
        # Test lowercase production
        with patch.dict(os.environ, {"ENVIRONMENT": "PRODUCTION"}):
            from app.main import create_app
            app = create_app()
            assert app.docs_url is None, "Should work with uppercase PRODUCTION"
    
    def test_default_environment_fallback(self):
        """HARDENING: Default environment should fallback to settings."""
        # Remove ENVIRONMENT from env if it exists
        env_backup = os.environ.pop("ENVIRONMENT", None)
        
        try:
            # Use settings default (which is "development")
            from app.main import create_app
            app = create_app()
            
            # Should use settings.ENVIRONMENT default
            settings = get_settings()
            if settings.ENVIRONMENT.lower() == "development":
                assert app.docs_url == "/docs", "Should use settings default"
            else:
                assert app.docs_url is None, "Should respect settings default"
        finally:
            # Restore environment
            if env_backup:
                os.environ["ENVIRONMENT"] = env_backup
    
    def test_test_environment_disables_docs(self):
        """HARDENING: Test environment should disable docs (unless explicitly enabled)."""
        with patch.dict(os.environ, {"ENVIRONMENT": "test"}):
            from app.main import create_app
            app = create_app()
            
            # Test environment should disable docs by default
            assert app.docs_url is None, "Test environment should disable docs"
            assert app.redoc_url is None, "Test environment should disable ReDoc"
            assert app.openapi_url is None, "Test environment should disable OpenAPI"
    
    def test_staging_environment_disables_docs(self):
        """HARDENING: Staging environment should disable docs."""
        with patch.dict(os.environ, {"ENVIRONMENT": "staging"}):
            from app.main import create_app
            app = create_app()
            
            assert app.docs_url is None, "Staging should disable docs"
            assert app.redoc_url is None, "Staging should disable ReDoc"
            assert app.openapi_url is None, "Staging should disable OpenAPI"
    
    def test_invalid_environment_disables_docs(self):
        """HARDENING: Invalid environment values should disable docs (fail-safe)."""
        invalid_envs = ["invalid", "unknown", "", " ", "dev", "prod"]
        
        for invalid_env in invalid_envs:
            with patch.dict(os.environ, {"ENVIRONMENT": invalid_env}):
                from app.main import create_app
                app = create_app()
                
                assert app.docs_url is None, f"Invalid env '{invalid_env}' should disable docs"
                assert app.redoc_url is None, f"Invalid env '{invalid_env}' should disable ReDoc"
                assert app.openapi_url is None, f"Invalid env '{invalid_env}' should disable OpenAPI"
    
    def test_app_creation_preserves_other_config(self):
        """ELEGANCE: App creation should preserve other FastAPI configuration."""
        with patch.dict(os.environ, {"ENVIRONMENT": "development"}):
            from app.main import create_app
            app = create_app()
            
            # Verify other config is preserved
            assert app.title == "AI Guardian API", "Title should be preserved"
            assert app.version == "1.0.0", "Version should be preserved"
            assert app.description is not None, "Description should be preserved"
            assert len(app.servers) > 0, "Servers should be configured"
    
    def test_docs_urls_are_correct_paths(self):
        """VALUE: Documentation URLs should be correct paths."""
        with patch.dict(os.environ, {"ENVIRONMENT": "development"}):
            from app.main import create_app
            app = create_app()
            
            assert app.docs_url == "/docs", "docs_url should be /docs"
            assert app.redoc_url == "/redoc", "redoc_url should be /redoc"
            assert app.openapi_url == "/openapi.json", "openapi_url should be /openapi.json"


class TestSwaggerUISecurity:
    """Test security aspects of Swagger UI conditional enablement."""
    
    def test_production_never_exposes_docs(self):
        """SECURITY: Production should never expose documentation."""
        production_envs = ["production", "PRODUCTION", "prod", "Prod"]
        
        for env in production_envs:
            with patch.dict(os.environ, {"ENVIRONMENT": env}):
                from app.main import create_app
                app = create_app()
                
                assert app.docs_url is None, f"Production env '{env}' should never expose docs"
                assert app.redoc_url is None, f"Production env '{env}' should never expose ReDoc"
                assert app.openapi_url is None, f"Production env '{env}' should never expose OpenAPI"
    
    def test_only_strict_development_enables_docs(self):
        """SECURITY: Only strict 'development' should enable docs."""
        # These should NOT enable docs (security)
        non_dev_envs = ["dev", "devel", "develop", "DEV", "development-staging"]
        
        for env in non_dev_envs:
            with patch.dict(os.environ, {"ENVIRONMENT": env}):
                from app.main import create_app
                app = create_app()
                
                assert app.docs_url is None, f"Non-development env '{env}' should not enable docs"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

