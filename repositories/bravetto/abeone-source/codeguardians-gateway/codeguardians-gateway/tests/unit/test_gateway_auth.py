#!/usr/bin/env python3
"""
Test suite for Gateway authentication requirements.

TEST: Authentication enforcement on orchestrator endpoints
PERF: O(1) time, O(1) space
FAILS: if endpoints accessible without auth or incorrect auth applied
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from fastapi import HTTPException

# SAFETY: Test authentication on all protected endpoints
# ASSUMES: Endpoints require auth per API_ORCHESTRATOR_CHANGES.md
# VERIFY: 401 returned without auth, 403 for insufficient permissions


class TestGatewayAuthentication:
    """Test authentication requirements on Gateway endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        from app.main import app
        return TestClient(app)
    
    @pytest.fixture
    def mock_user(self):
        """Mock authenticated user."""
        user = Mock()
        user.id = 1
        user.email = "test@example.com"
        user.is_admin = False
        return user
    
    @pytest.fixture
    def mock_admin(self):
        """Mock admin user."""
        admin = Mock()
        admin.id = 1
        admin.email = "admin@example.com"
        admin.is_admin = True
        return admin
    
    def test_process_endpoint_optional_auth(self, client):
        """TEST: /process endpoint accepts optional Clerk token"""
        # Arrange & Act - Should work without auth (backward compatible)
        response = client.post(
            "/api/v1/guards/process",
            json={
                "service_type": "tokenguard",
                "payload": {"content": "test"}
            }
        )
        
        # Assert - May fail for other reasons but not auth
        assert response.status_code != 401, "Process endpoint should not require auth"
    
    def test_health_endpoint_requires_auth(self, client):
        """TEST: GET /health requires authentication"""
        # Arrange & Act
        response = client.get("/api/v1/guards/health")
        
        # Assert
        assert response.status_code == 401, "Health endpoint should require authentication"
    
    def test_health_endpoint_with_auth(self, client, mock_user):
        """TEST: GET /health works with authentication"""
        # Arrange
        with patch('app.api.v1.guards.get_current_user', return_value=mock_user):
            # Act
            response = client.get(
                "/api/v1/guards/health",
                headers={"Authorization": "Bearer test-token"}
            )
        
        # Assert
        assert response.status_code in [200, 503], "Health endpoint should work with auth"
    
    def test_services_endpoint_requires_auth(self, client):
        """TEST: GET /services requires authentication"""
        # Arrange & Act
        response = client.get("/api/v1/guards/services")
        
        # Assert
        assert response.status_code == 401, "Services endpoint should require authentication"
    
    def test_discovery_register_requires_admin(self, client, mock_user):
        """TEST: POST /discovery/register requires admin access"""
        # Arrange
        with patch('app.api.v1.guards.require_admin_access', side_effect=HTTPException(status_code=403, detail="Admin required")):
            # Act
            response = client.post(
                "/api/v1/guards/discovery/register",
                json={
                    "service_name": "test",
                    "base_url": "http://test:8000",
                    "service_type": "tokenguard"
                },
                headers={"Authorization": "Bearer user-token"}
            )
        
        # Assert
        assert response.status_code == 403, "Discovery register should require admin"
    
    def test_discovery_register_with_admin(self, client, mock_admin):
        """TEST: POST /discovery/register works with admin access"""
        # Arrange
        with patch('app.api.v1.guards.require_admin_access', return_value=mock_admin):
            # Act
            response = client.post(
                "/api/v1/guards/discovery/register",
                params={
                    "service_name": "test",
                    "base_url": "http://test:8000",
                    "service_type": "tokenguard"
                },
                headers={"Authorization": "Bearer admin-token"}
            )
        
        # Assert - May fail for validation but not auth
        assert response.status_code != 401 and response.status_code != 403, \
            "Discovery register should work with admin auth"
    
    def test_health_refresh_requires_admin(self, client, mock_user):
        """TEST: POST /health/refresh requires admin access"""
        # Arrange
        with patch('app.api.v1.guards.require_admin_access', side_effect=HTTPException(status_code=403, detail="Admin required")):
            # Act
            response = client.post(
                "/api/v1/guards/health/refresh",
                headers={"Authorization": "Bearer user-token"}
            )
        
        # Assert
        assert response.status_code == 403, "Health refresh should require admin"
    
    def test_discovery_services_requires_auth(self, client):
        """TEST: GET /discovery/services requires authentication"""
        # Arrange & Act
        response = client.get("/api/v1/guards/discovery/services")
        
        # Assert
        assert response.status_code == 401, "Discovery services should require auth"
    
    def test_discovery_unregister_requires_admin(self, client, mock_user):
        """TEST: DELETE /discovery/services/{name} requires admin"""
        # Arrange
        with patch('app.api.v1.guards.require_admin_access', side_effect=HTTPException(status_code=403, detail="Admin required")):
            # Act
            response = client.delete(
                "/api/v1/guards/discovery/services/test",
                headers={"Authorization": "Bearer user-token"}
            )
        
        # Assert
        assert response.status_code == 403, "Discovery unregister should require admin"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

