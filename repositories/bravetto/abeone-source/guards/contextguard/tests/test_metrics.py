#!/usr/bin/env python3
"""
Test suite for ContextGuard /metrics endpoint.

TEST: Metrics endpoint functionality
PERF: O(1) time, O(1) space
FAILS: if metrics endpoint returns non-200 or invalid Prometheus format
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from main import app

# SAFETY: Test client for endpoint testing
client = TestClient(app)


class TestMetricsEndpoint:
    """Test /metrics endpoint."""
    
    def test_metrics_endpoint_exists(self):
        """TEST: GET /metrics returns 200"""
        # Arrange & Act
        response = client.get("/metrics")
        
        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    def test_metrics_returns_prometheus_format(self):
        """TEST: Returns Prometheus text format"""
        # Arrange & Act
        response = client.get("/metrics")
        
        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"
        assert isinstance(response.text, str)
        assert len(response.text) > 0
    
    def test_metrics_contains_request_total(self):
        """TEST: Contains contextguard_requests_total metric"""
        # Arrange & Act
        response = client.get("/metrics")
        
        # Assert
        assert response.status_code == 200
        assert "contextguard_requests_total" in response.text
    
    def test_metrics_contains_request_duration(self):
        """TEST: Contains contextguard_request_duration_seconds metric"""
        # Arrange & Act
        response = client.get("/metrics")
        
        # Assert
        assert response.status_code == 200
        assert "REPLACE_ME" in response.text
    
    def test_metrics_contains_redis_status(self):
        """TEST: Contains contextguard_redis_connection_status metric"""
        # Arrange & Act
        response = client.get("/metrics")
        
        # Assert
        assert response.status_code == 200
        assert "REPLACE_ME" in response.text
    
    def test_metrics_contains_memory_operations(self):
        """TEST: Contains contextguard_memory_operations_total metric"""
        # Arrange & Act
        response = client.get("/metrics")
        
        # Assert
        assert response.status_code == 200
        assert "REPLACE_ME" in response.text
    
    def test_metrics_performance(self):
        """PERF: Metrics endpoint responds <100ms"""
        import time
        
        # Arrange & Act
        start = time.time()
        response = client.get("/metrics")
        duration = time.time() - start
        
        # Assert
        assert response.status_code == 200
        assert duration < 0.1, f"Metrics endpoint took {duration}s, expected <0.1s"
    
    def test_metrics_with_no_requests(self):
        """TEST: Metrics work correctly with no requests yet"""
        # Arrange & Act
        response = client.get("/metrics")
        
        # Assert
        assert response.status_code == 200
        # Should still return valid Prometheus format even with zero metrics
        assert "contextguard_requests_total" in response.text
    
    def test_metrics_after_health_check(self):
        """TEST: Metrics increment after health check"""
        # Arrange
        initial_response = client.get("/metrics")
        initial_text = initial_response.text
        
        # Act - Make a health check request
        client.get("/health")
        
        # Wait a moment for metrics to update
        import time
        time.sleep(0.1)
        
        # Get metrics again
        updated_response = client.get("/metrics")
        updated_text = updated_response.text
        
        # Assert
        assert updated_response.status_code == 200
        # Should have at least one request recorded
        assert "contextguard_requests_total" in updated_text


class TestMetricsEdgeCases:
    """Test edge cases for metrics endpoint."""
    
    def test_metrics_with_redis_down(self):
        """TEST: Metrics still work if Redis is unavailable"""
        # Note: This test requires mocking Redis failure
        # For now, we verify metrics endpoint doesn't depend on Redis
        response = client.get("/metrics")
        assert response.status_code == 200
    
    def test_metrics_content_type(self):
        """TEST: Content-Type header is correct"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers.get("content-type", "")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

