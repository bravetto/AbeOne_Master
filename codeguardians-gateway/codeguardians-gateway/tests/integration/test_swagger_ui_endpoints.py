"""
 Swagger UI Endpoint Integration Tests 

Guardian: Jōhn (530 Hz)
"Do it right or don't do it at all"

Integration tests for Swagger UI endpoints.
Tests actual HTTP responses with convergence patterns in mind.

Convergence Patterns Applied:
- SIMPLICITY: Clear test structure, direct HTTP checks
- HARDENING: Real endpoint testing, status code validation
- ELEGANCE: Beautiful test organization, comprehensive coverage
- VALUE: Every test validates real user scenarios
"""

import os
import pytest
from fastapi.testclient import TestClient

from app.main import create_app


class TestSwaggerUIEndpointsDevelopment:
    """Test Swagger UI endpoints in development mode."""
    
    @pytest.fixture(autouse=True)
    def setup_development_env(self):
        """Setup development environment for each test."""
        self.original_env = os.environ.get("ENVIRONMENT")
        os.environ["ENVIRONMENT"] = "development"
        yield
        # Restore original environment
        if self.original_env:
            os.environ["ENVIRONMENT"] = self.original_env
        elif "ENVIRONMENT" in os.environ:
            del os.environ["ENVIRONMENT"]
    
    def test_docs_endpoint_accessible_in_development(self):
        """SIMPLICITY: /docs endpoint should be accessible in development."""
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/docs")
        assert response.status_code == 200, "Swagger UI should return 200 in development"
        assert "text/html" in response.headers.get("content-type", ""), "Should return HTML"
        assert "swagger" in response.text.lower(), "Should contain Swagger UI content"
    
    def test_redoc_endpoint_accessible_in_development(self):
        """SIMPLICITY: /redoc endpoint should be accessible in development."""
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/redoc")
        assert response.status_code == 200, "ReDoc should return 200 in development"
        assert "text/html" in response.headers.get("content-type", ""), "Should return HTML"
        assert "redoc" in response.text.lower(), "Should contain ReDoc content"
    
    def test_openapi_json_accessible_in_development(self):
        """SIMPLICITY: /openapi.json endpoint should be accessible in development."""
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/openapi.json")
        assert response.status_code == 200, "OpenAPI JSON should return 200 in development"
        assert "application/json" in response.headers.get("content-type", ""), "Should return JSON"
        
        # Validate OpenAPI structure
        data = response.json()
        assert "openapi" in data, "Should contain OpenAPI version"
        assert "info" in data, "Should contain API info"
        assert "paths" in data, "Should contain API paths"
    
    def test_root_endpoint_shows_docs_available(self):
        """VALUE: Root endpoint should indicate docs availability."""
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200, "Root endpoint should work"
        
        data = response.json()
        assert "docs" in data, "Root should include docs status"
        assert data["docs"] == "/docs", "Root should show /docs path in development"


class TestSwaggerUIEndpointsProduction:
    """Test Swagger UI endpoints in production mode."""
    
    @pytest.fixture(autouse=True)
    def setup_production_env(self):
        """Setup production environment for each test."""
        self.original_env = os.environ.get("ENVIRONMENT")
        os.environ["ENVIRONMENT"] = "production"
        yield
        # Restore original environment
        if self.original_env:
            os.environ["ENVIRONMENT"] = self.original_env
        elif "ENVIRONMENT" in os.environ:
            del os.environ["ENVIRONMENT"]
    
    def test_docs_endpoint_returns_404_in_production(self):
        """SECURITY: /docs endpoint should return 404 in production."""
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/docs")
        assert response.status_code == 404, "Swagger UI should return 404 in production"
    
    def test_redoc_endpoint_returns_404_in_production(self):
        """SECURITY: /redoc endpoint should return 404 in production."""
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/redoc")
        assert response.status_code == 404, "ReDoc should return 404 in production"
    
    def test_openapi_json_returns_404_in_production(self):
        """SECURITY: /openapi.json endpoint should return 404 in production."""
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/openapi.json")
        assert response.status_code == 404, "OpenAPI JSON should return 404 in production"
    
    def test_root_endpoint_shows_docs_disabled(self):
        """VALUE: Root endpoint should indicate docs are disabled."""
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200, "Root endpoint should work"
        
        data = response.json()
        assert "docs" in data, "Root should include docs status"
        assert "disabled" in data["docs"].lower(), "Root should show docs disabled in production"


class TestSwaggerUIConvergencePatterns:
    """Test Swagger UI integration against convergence patterns."""
    
    def test_simplicity_pattern_single_environment_check(self):
        """SIMPLICITY: Single environment check controls all docs."""
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            
            # All docs controlled by single check
            assert app.docs_url is not None
            assert app.redoc_url is not None
            assert app.openapi_url is not None
            
            # Change environment
            m.setenv("ENVIRONMENT", "production")
            app = create_app()
            
            # All docs disabled by same check
            assert app.docs_url is None
            assert app.redoc_url is None
            assert app.openapi_url is None
    
    def test_hardening_pattern_edge_cases_handled(self):
        """HARDENING: Edge cases handled gracefully."""
        edge_cases = ["", " ", "invalid", "UNKNOWN", "test", "staging"]
        
        for env in edge_cases:
            with pytest.MonkeyPatch().context() as m:
                m.setenv("ENVIRONMENT", env)
                app = create_app()
                
                # Should disable docs (fail-safe)
                assert app.docs_url is None, f"Edge case '{env}' should disable docs"
                assert app.redoc_url is None, f"Edge case '{env}' should disable ReDoc"
                assert app.openapi_url is None, f"Edge case '{env}' should disable OpenAPI"
    
    def test_elegance_pattern_clear_configuration(self):
        """ELEGANCE: Configuration is clear and maintainable."""
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            
            # Configuration should be clear
            assert app.docs_url == "/docs", "Clear docs path"
            assert app.redoc_url == "/redoc", "Clear ReDoc path"
            assert app.openapi_url == "/openapi.json", "Clear OpenAPI path"
    
    def test_value_pattern_no_redundancy(self):
        """VALUE: No redundant configuration or checks."""
        with pytest.MonkeyPatch().context() as m:
            m.setenv("ENVIRONMENT", "development")
            app = create_app()
            
            # Single source of truth for environment
            # All docs use same environment check
            # No duplicate logic
            
            # Verify single check controls all
            docs_enabled = app.docs_url is not None
            redoc_enabled = app.redoc_url is not None
            openapi_enabled = app.openapi_url is not None
            
            assert docs_enabled == redoc_enabled == openapi_enabled, "All docs should have same state"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

