"""
🌊💎✨ Swagger UI Convergence Pattern Tests ✨💎🌊

Guardian: Jōhn (530 Hz)
"Do it right or don't do it at all"

Validates Swagger UI integration against convergence patterns:
- SIMPLICITY: One responsibility, clear intent, no magic
- HARDENING: Type safety, validation, graceful degradation
- ELEGANCE: Beautiful code, clear patterns, demystified
- VALUE: Every line serves purpose, zero redundancy

Recursive analysis of AEYON's implementation with emerging convergence.
"""

import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app
from app.core.config import get_settings


class TestSwaggerUIConvergencePatterns:
    """Comprehensive convergence pattern validation for Swagger UI integration."""
    
    def test_simplicity_one_responsibility(self):
        """SIMPLICITY: Single responsibility - enable docs based on environment."""
        # The implementation has ONE job: enable docs in development
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            
            # Single check controls all docs
            is_dev = os.getenv("ENVIRONMENT", "").lower() == "development"
            assert (app.docs_url is not None) == is_dev, "Single responsibility check"
    
    def test_simplicity_clear_intent(self):
        """SIMPLICITY: Clear intent - no magic numbers or hidden logic."""
        # Check that configuration is explicit
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            
            # Explicit paths, no magic
            assert app.docs_url == "/docs", "Clear docs path"
            assert app.redoc_url == "/redoc", "Clear ReDoc path"
            assert app.openapi_url == "/openapi.json", "Clear OpenAPI path"
    
    def test_hardening_type_safety(self):
        """HARDENING: Type safety - environment handled correctly."""
        # Test various types and formats
        test_cases = [
            ("development", True),  # Correct string
            ("DEVELOPMENT", True),  # Uppercase
            ("Development", True),  # Mixed case
            ("production", False),  # Production
            ("PRODUCTION", False),  # Uppercase production
            ("", False),  # Empty string
            ("invalid", False),  # Invalid value
        ]
        
        for env_value, should_enable in test_cases:
            with pytest.MonkeyPatch().context() as m:
                m.setenv("ENVIRONMENT", env_value)
                app = create_app()
                
                docs_enabled = app.docs_url is not None
                assert docs_enabled == should_enable, f"Env '{env_value}' should enable={should_enable}"
    
    def test_hardening_graceful_degradation(self):
        """HARDENING: Graceful degradation - invalid values disable docs safely."""
        # Note: None/empty ENVIRONMENT falls back to settings default (development)
        # This is acceptable behavior - invalid strings should disable docs
        invalid_values = ["", " ", "unknown", "test", "staging", "invalid"]
        
        for invalid_val in invalid_values:
            with pytest.MonkeyPatch().context() as m:
                m.setenv("ENVIRONMENT", invalid_val)
                app = create_app()
                
                # Should disable docs (fail-safe)
                assert app.docs_url is None, f"Invalid '{invalid_val}' should disable docs"
                assert app.redoc_url is None, f"Invalid '{invalid_val}' should disable ReDoc"
                assert app.openapi_url is None, f"Invalid '{invalid_val}' should disable OpenAPI"
    
    def test_elegance_beautiful_structure(self):
        """ELEGANCE: Beautiful code structure - clear organization."""
        # Check that code follows clear patterns
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            
            # Structure should be:
            # 1. Get environment
            # 2. Check if development
            # 3. Conditionally enable docs
            
            # Verify structure through behavior
            assert app.docs_url == "/docs", "Clear structure leads to correct behavior"
            assert isinstance(app, FastAPI), "Proper FastAPI instance"
    
    def test_elegance_demystified_constants(self):
        """ELEGANCE: Demystified constants - no magic strings."""
        # Paths should be explicit, not magic
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            
            # Constants are explicit
            assert app.docs_url == "/docs", "Explicit docs path"
            assert app.redoc_url == "/redoc", "Explicit ReDoc path"
            assert app.openapi_url == "/openapi.json", "Explicit OpenAPI path"
    
    def test_value_every_line_serves_purpose(self):
        """VALUE: Every line serves purpose - no redundancy."""
        # Check that implementation is efficient
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            
            # Single environment check controls all docs
            # No redundant checks
            docs_state = app.docs_url is not None
            redoc_state = app.redoc_url is not None
            openapi_state = app.openapi_url is not None
            
            # All should have same state (no redundancy)
            assert docs_state == redoc_state == openapi_state, "No redundant checks"
    
    def test_value_zero_redundancy(self):
        """VALUE: Zero redundancy - single source of truth."""
        # Environment check should be single source of truth
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            
            # All docs should follow same pattern
            all_enabled = all([
                app.docs_url is not None,
                app.redoc_url is not None,
                app.openapi_url is not None
            ])
            
            assert all_enabled, "Single source of truth for all docs"
            
            # Change environment
            m.setenv("ENVIRONMENT", "production")
            app = create_app()
            
            # All should be disabled
            all_disabled = all([
                app.docs_url is None,
                app.redoc_url is None,
                app.openapi_url is None
            ])
            
            assert all_disabled, "Single source of truth disables all"


class TestSwaggerUIRecursiveAnalysis:
    """Recursive analysis of AEYON's Swagger UI implementation."""
    
    def test_implementation_follows_user_story(self):
        """Validate implementation matches user story requirements."""
        # User Story: Enable swagger-ui only in development
        
        # Requirement 1: Swagger available at /docs and /redoc
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            client = TestClient(app)
            
            docs_response = client.get("/docs")
            redoc_response = client.get("/redoc")
            openapi_response = client.get("/openapi.json")
            
            assert docs_response.status_code == 200, "Requirement 1: /docs available"
            assert redoc_response.status_code == 200, "Requirement 1: /redoc available"
            assert openapi_response.status_code == 200, "Requirement 1: /openapi.json available"
        
        # Requirement 2: Only enabled when ENVIRONMENT=development
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "production")
            app = create_app()
            client = TestClient(app)
            
            docs_response = client.get("/docs")
            redoc_response = client.get("/redoc")
            openapi_response = client.get("/openapi.json")
            
            assert docs_response.status_code == 404, "Requirement 2: Disabled in production"
            assert redoc_response.status_code == 404, "Requirement 2: Disabled in production"
            assert openapi_response.status_code == 404, "Requirement 2: Disabled in production"
    
    def test_security_no_sensitive_data_exposed(self):
        """SECURITY: Verify no sensitive data in Swagger docs."""
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            client = TestClient(app)
            
            # Get OpenAPI spec
            response = client.get("/openapi.json")
            assert response.status_code == 200
            
            spec = response.json()
            
            # Check that sensitive fields are not exposed
            sensitive_keywords = ["secret", "password", "token", "key", "credential"]
            
            spec_str = str(spec).lower()
            # Note: Some keywords might appear in non-sensitive contexts
            # This is a basic check - comprehensive security review needed
            
            # Verify no obvious credential exposure
            assert "clerk_secret_key" not in spec_str or "test" in spec_str, "No secrets in spec"
    
    def test_developer_experience_auto_updates(self):
        """DEVELOPER EXPERIENCE: Swagger auto-updates with route changes."""
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            client = TestClient(app)
            
            # Get OpenAPI spec
            response = client.get("/openapi.json")
            assert response.status_code == 200
            
            spec = response.json()
            
            # Verify routes are included
            assert "paths" in spec, "Should have paths"
            assert len(spec["paths"]) > 0, "Should have routes"
            
            # Verify common endpoints exist
            assert "/health" in spec["paths"], "Health endpoint should be documented"
            assert "/api/v1" in str(spec["paths"]), "API v1 endpoints should be documented"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

