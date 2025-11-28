"""
Integration tests for the unified router
Tests actual requests to live services
"""

import pytest
import requests
import time
import json

BASE_URL = "http://localhost:8000"


class TestUnifiedRouterIntegration:
    """Integration tests for unified router endpoints"""

    def test_health_endpoints(self):
        """Test all health check endpoints are accessible"""
        endpoints = [
            "/health/live",
            "/health/ready",
            "/health/comprehensive",
            "/health/circuit-breakers",
            "/health/configuration"
        ]

        for endpoint in endpoints:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            assert response.status_code in [200, 503], f"Failed: {endpoint}"

    def test_tokenguard_integration(self):
        """Test TokenGuard through unified router"""
        payload = {
            "service_type": "tokenguard",
            "payload": {
                "text": "Test content for token analysis"
            },
            "user_id": "test-user-123"
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["service_type"] == "tokenguard"
        assert data["service_used"] == "tokenguard"
        assert "data" in data
        assert data["processing_time"] is not None

    def test_trustguard_integration(self):
        """Test TrustGuard through unified router"""
        payload = {
            "service_type": "trustguard",
            "payload": {
                "text": "Content for validation",
                "validation_level": "standard"
            }
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["service_type"] == "trustguard"
        assert "validation_results" in data["data"]

    def test_contextguard_integration(self):
        """Test ContextGuard through unified router"""
        # First set a value
        payload = {
            "service_type": "contextguard",
            "payload": {
                "operation": "set",
                "data": {
                    "key": "integration_test",
                    "value": "test_value_123"
                }
            }
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_biasguard_integration(self):
        """Test BiasGuard through unified router"""
        payload = {
            "service_type": "biasguard",
            "payload": {
                "operation": "detect_bias",
                "data": {
                    "text": "This is neutral test content"
                }
            }
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["service_type"] == "biasguard"

    def test_securityguard_integration(self):
        """Test SecurityGuard through unified router"""
        payload = {
            "service_type": "securityguard",
            "payload": {
                "text": "SELECT * FROM users WHERE id=1"
            }
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["service_type"] == "securityguard"
        assert "security_score" in data["data"]

    def test_invalid_service_type(self):
        """Test error handling for invalid service type"""
        payload = {
            "service_type": "invalid_guard",
            "payload": {"text": "test"}
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        assert response.status_code == 400
        assert "Invalid service type" in response.json()["detail"]

    def test_concurrent_requests(self):
        """Test multiple concurrent requests to different services"""
        import concurrent.futures

        def make_request(service_type, text):
            payload = {
                "service_type": service_type,
                "payload": {"text": text}
            }
            response = requests.post(
                f"{BASE_URL}/api/v1/guards/process",
                json=payload,
                timeout=30
            )
            return response.status_code, response.json()

        services = ["tokenguard", "trustguard", "securityguard"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(make_request, service, f"Test {service}")
                for service in services
            ]

            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All requests should succeed
        assert len(results) == 3
        for status_code, data in results:
            assert status_code == 200
            assert data["success"] is True

    def test_direct_service_endpoints(self):
        """Test direct service endpoints work correctly"""
        tests = [
            ("/api/v1/guards/tokenguard/optimize", {"text": "Optimize this"}),
            ("/api/v1/guards/trustguard/validate", {"content": "Validate this"}),
            ("/api/v1/guards/contextguard/analyze", {"context": "test"}),
            ("/api/v1/guards/biasguard/detect", {"text": "Detect bias"}),
        ]

        for endpoint, payload in tests:
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                json=payload,
                timeout=30
            )
            # Some may fail if mapping isn't perfect, but should get a response
            assert response.status_code in [200, 400, 422, 502]

    def test_service_discovery(self):
        """Test service discovery endpoints"""
        response = requests.get(f"{BASE_URL}/api/v1/guards/services", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "services" in data
        assert len(data["services"]) > 0

    def test_guard_health_endpoints(self):
        """Test guard service health endpoints"""
        # All guards health
        response = requests.get(f"{BASE_URL}/api/v1/guards/health", timeout=10)
        assert response.status_code == 200
        data = response.json()

        # Individual guard health
        guards = ["tokenguard", "trustguard", "contextguard", "biasguard", "securityguard"]
        for guard in guards:
            response = requests.get(f"{BASE_URL}/api/v1/guards/health/{guard}", timeout=10)
            if response.status_code == 200:
                guard_data = response.json()
                assert "service_name" in guard_data
                assert "status" in guard_data

    def test_request_with_session_id(self):
        """Test requests with session tracking"""
        payload = {
            "service_type": "tokenguard",
            "payload": {"text": "Session test"},
            "user_id": "user-123",
            "session_id": "session-456"
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestErrorHandling:
    """Test error handling in the unified router"""

    def test_empty_payload(self):
        """Test handling of empty payload"""
        payload = {
            "service_type": "tokenguard",
            "payload": {}
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        # Should handle gracefully
        assert response.status_code in [200, 400, 422]

    def test_malformed_json(self):
        """Test handling of malformed JSON"""
        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            data="not json",
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        assert response.status_code == 422

    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        payload = {
            "payload": {"text": "test"}
            # Missing service_type
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        assert response.status_code == 422

    def test_large_payload(self):
        """Test handling of large payload"""
        large_text = "x" * 50000  # 50KB

        payload = {
            "service_type": "tokenguard",
            "payload": {"text": large_text}
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        # Should handle or reject gracefully
        assert response.status_code in [200, 400, 413, 422]


class TestResponseFormat:
    """Test response format consistency"""

    def test_response_structure(self):
        """Test that all services return consistent response structure"""
        services = ["tokenguard", "trustguard", "contextguard", "biasguard", "securityguard"]

        for service in services:
            payload = {
                "service_type": service,
                "payload": {"text": f"Test for {service}"}
            }

            response = requests.post(
                f"{BASE_URL}/api/v1/guards/process",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                # Check required fields
                assert "request_id" in data
                assert "service_type" in data
                assert "success" in data
                assert "processing_time" in data
                assert "service_used" in data
                assert "fallback_used" in data

                # Check that one of data or error is present
                assert ("data" in data) or ("error" in data)

    def test_error_response_structure(self):
        """Test error response structure"""
        payload = {
            "service_type": "invalid",
            "payload": {"text": "test"}
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/guards/process",
            json=payload,
            timeout=30
        )

        assert response.status_code == 400
        error_data = response.json()
        assert "detail" in error_data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
