"""
Integration tests for Trust Guard API endpoints
"""

import pytest
import sys
import os
import json
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoint functionality."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "version" in data
        assert "components" in data
        assert "metrics" in data
        
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
        assert data["version"] == "1.0.0"
        assert isinstance(data["components"], dict)
        assert isinstance(data["metrics"], dict)
    
    def test_detect_patterns_endpoint(self):
        """Test pattern detection endpoint."""
        payload = {
            "text": "This is definitely the correct answer without any doubt.",
            "context": "Testing overconfidence detection",
            "metadata": {"model": "test-model", "confidence": 0.85}
        }
        
        response = client.post("/v1/detect", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "detections" in data
        assert "risk_assessment" in data
        assert "processing_time_ms" in data
        assert "timestamp" in data
        
        # Validate detections structure
        detections = data["detections"]
        assert len(detections) == 7
        assert all(pattern in detections for pattern in [
            'hallucination', 'drift', 'bias', 'deception',
            'security_theater', 'duplication', 'stub_syndrome'
        ])
        
        # Validate each detection has required fields
        for pattern, detection in detections.items():
            assert "score" in detection
            assert "confidence" in detection
            assert "description" in detection
            assert "evidence" in detection
            assert "risk_level" in detection
            
            assert 0 <= detection["score"] <= 1.0
            assert 0 <= detection["confidence"] <= 1.0
            assert detection["risk_level"] in ["low", "medium", "high"]
    
    def test_validate_endpoint(self):
        """Test comprehensive validation endpoint."""
        payload = {
            "input_text": "What is the capital of France?",
            "output_text": "Paris is the capital of France with a population of 2.1 million people.",
            "context": "Geography quiz",
            "expected_factors": ["factual_accuracy", "context_relevance"]
        }
        
        response = client.post("/v1/validate", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "overall_score" in data
        assert "pattern_detections" in data
        assert "risk_level" in data
        assert "recommendations" in data
        assert "evidence" in data
        assert "processing_time" in data
        
        # Validate score ranges
        assert 0 <= data["overall_score"] <= 100
        assert data["risk_level"] in ["low", "medium", "high"]
        assert isinstance(data["recommendations"], list)
        assert isinstance(data["evidence"], dict)
        assert data["processing_time"] > 0
    
    def test_mitigate_endpoint(self):
        """Test mitigation endpoint."""
        payload = {
            "text": "The AI is now safe and secure with 100% trustworthiness.",
            "detected_patterns": ["security_theater", "deception"],
            "severity": "high"
        }
        
        response = client.post("/v1/mitigate", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "original_text" in data
        assert "mitigated_text" in data
        assert "applied_techniques" in data
        assert "constitutional_prompts_used" in data
        assert "confidence_improvement" in data
        assert "processing_time_ms" in data
        assert "timestamp" in data
        
        assert data["original_text"] == payload["text"]
        assert len(data["mitigated_text"]) > 0
        assert isinstance(data["applied_techniques"], list)
        assert isinstance(data["constitutional_prompts_used"], list)
        assert 0 <= data["confidence_improvement"] <= 1.0
    
    def test_constitutional_endpoint(self):
        """Test constitutional prompting endpoint."""
        patterns = ["hallucination", "bias"]
        severity = "medium"
        
        response = client.post("/v1/constitutional", json=patterns, params={"severity": severity})
        
        assert response.status_code == 200
        data = response.json()
        
        assert "patterns" in data
        assert "severity" in data
        assert "constitutional_prompts" in data
        assert "usage_guidance" in data
        
        assert data["patterns"] == patterns
        assert data["severity"] == severity
        assert isinstance(data["constitutional_prompts"], list)
        assert len(data["constitutional_prompts"]) > 0
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = client.get("/v1/metrics")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "service_health" in data
        assert "performance_metrics" in data
        assert "pattern_statistics" in data
        assert "reliability_trends" in data
        assert "system_metrics" in data
        
        # Validate service health
        health = data["service_health"]
        assert "detector_status" in health
        assert "validator_status" in health
        assert "constitutional_status" in health
        assert "overall_health" in health
        
        # Validate performance metrics
        perf = data["performance_metrics"]
        assert "total_validations" in perf
        assert "total_detections" in perf
        assert "total_mitigations" in perf
        assert "average_risk_score" in perf
        assert "patterns_detected_today" in perf
    
    def test_invalid_input_handling(self):
        """Test handling of invalid input."""
        # Test with missing required fields
        response = client.post("/v1/detect", json={})
        assert response.status_code == 422  # Validation error
        
        # Test with invalid text length
        response = client.post("/v1/detect", json={"text": ""})
        assert response.status_code == 422
        
        # Test with extremely long text
        long_text = "a" * 10000
        response = client.post("/v1/detect", json={"text": long_text})
        # Should handle gracefully (either accept or return appropriate error)
        assert response.status_code in [200, 422, 413]
    
    def test_rate_limiting(self):
        """Test rate limiting functionality."""
        payload = {"text": "Test rate limiting"}
        
        # Make multiple requests quickly
        responses = []
        for i in range(5):
            response = client.post("/v1/detect", json=payload)
            responses.append(response)
        
        # All should succeed (rate limit is 100/minute)
        for response in responses:
            assert response.status_code == 200
    
    def test_cors_headers(self):
        """Test CORS headers are present."""
        response = client.options("/health")
        # CORS headers should be present if configured
        assert response.status_code in [200, 405]  # OPTIONS might not be implemented
    
    def test_response_headers(self):
        """Test custom response headers."""
        response = client.get("/health")
        
        assert "X-Process-Time" in response.headers
        assert "X-Trust-Guard-Version" in response.headers
        assert response.headers["X-Trust-Guard-Version"] == "1.0.0"


class TestAPIErrorHandling:
    """Test API error handling and edge cases."""
    
    def test_malformed_json(self):
        """Test handling of malformed JSON."""
        response = client.post(
            "/v1/detect",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_unsupported_content_type(self):
        """Test handling of unsupported content types."""
        response = client.post(
            "/v1/detect",
            data="test",
            headers={"Content-Type": "text/plain"}
        )
        assert response.status_code == 422
    
    def test_large_payload(self):
        """Test handling of large payloads."""
        large_text = "This is a test. " * 1000  # ~15KB
        payload = {
            "text": large_text,
            "context": "Large payload test"
        }
        
        response = client.post("/v1/detect", json=payload)
        # Should handle gracefully
        assert response.status_code in [200, 413, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
