"""
Test complete request flow tracing and validation
"""

import pytest
import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi.testclient import TestClient
from main import app


class TestFlowTracing:
    """Test complete request flow tracing and validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
    
    def test_complete_detection_flow(self):
        """Test complete detection flow from request to response."""
        # Test data
        test_text = "This is definitely the correct answer without any doubt. All politicians are corrupt."
        
        # Step 1: Send detection request
        start_time = time.time()
        response = self.client.post("/v1/detect", json={
            "text": test_text,
            "context": "Testing complete flow",
            "metadata": {"test": True}
        })
        detection_time = time.time() - start_time
        
        # Validate response
        assert response.status_code == 200
        data = response.json()
        
        # Validate structure
        assert "detections" in data
        assert "risk_assessment" in data
        assert "processing_time_ms" in data
        assert "timestamp" in data
        
        # Validate detections
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
        
        # Validate risk assessment
        risk_assessment = data["risk_assessment"]
        assert "score" in risk_assessment
        assert "level" in risk_assessment
        assert "description" in risk_assessment
        assert "components" in risk_assessment
        
        # Validate processing time is reasonable
        assert detection_time < 2.0  # Should complete within 2 seconds
        assert data["processing_time_ms"] > 0
        
        return data
    
    def test_complete_validation_flow(self):
        """Test complete validation flow from request to response."""
        # Test data
        input_text = "What is the capital of France?"
        output_text = "Paris is the capital of France with a population of 2.1 million people."
        
        # Step 1: Send validation request
        start_time = time.time()
        response = self.client.post("/v1/validate", json={
            "input_text": input_text,
            "output_text": output_text,
            "context": "Geography quiz",
            "expected_factors": ["factual_accuracy", "context_relevance"]
        })
        validation_time = time.time() - start_time
        
        # Validate response
        assert response.status_code == 200
        data = response.json()
        
        # Validate structure
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
        
        # Validate processing time is reasonable
        assert validation_time < 3.0  # Should complete within 3 seconds
        
        return data
    
    def test_complete_mitigation_flow(self):
        """Test complete mitigation flow from request to response."""
        # Test data
        test_text = "The AI is now safe and secure with 100% trustworthiness."
        detected_patterns = ["security_theater", "deception"]
        
        # Step 1: Send mitigation request
        start_time = time.time()
        response = self.client.post("/v1/mitigate", json={
            "text": test_text,
            "detected_patterns": detected_patterns,
            "severity": "high"
        })
        mitigation_time = time.time() - start_time
        
        # Validate response
        assert response.status_code == 200
        data = response.json()
        
        # Validate structure
        assert "original_text" in data
        assert "mitigated_text" in data
        assert "applied_techniques" in data
        assert "constitutional_prompts_used" in data
        assert "confidence_improvement" in data
        assert "processing_time_ms" in data
        assert "timestamp" in data
        
        # Validate content
        assert data["original_text"] == test_text
        assert len(data["mitigated_text"]) > 0
        assert isinstance(data["applied_techniques"], list)
        assert isinstance(data["constitutional_prompts_used"], list)
        assert 0 <= data["confidence_improvement"] <= 1.0
        
        # Validate processing time is reasonable
        assert mitigation_time < 2.0  # Should complete within 2 seconds
        
        return data
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        # Test data
        input_text = "Explain quantum computing"
        output_text = "Quantum computing is definitely the future of technology. It will solve all problems."
        
        # Step 1: Detection
        detection_response = self.client.post("/v1/detect", json={
            "text": output_text,
            "context": input_text
        })
        assert detection_response.status_code == 200
        detection_data = detection_response.json()
        
        # Step 2: Validation
        validation_response = self.client.post("/v1/validate", json={
            "input_text": input_text,
            "output_text": output_text,
            "context": "Technical explanation"
        })
        assert validation_response.status_code == 200
        validation_data = validation_response.json()
        
        # Step 3: Extract high-risk patterns for mitigation
        high_risk_patterns = []
        for pattern, detection in detection_data["detections"].items():
            if detection["score"] > 0.5:
                high_risk_patterns.append(pattern)
        
        # Step 4: Mitigation (if high-risk patterns found)
        if high_risk_patterns:
            mitigation_response = self.client.post("/v1/mitigate", json={
                "text": output_text,
                "detected_patterns": high_risk_patterns,
                "severity": validation_data["risk_level"]
            })
            assert mitigation_response.status_code == 200
            mitigation_data = mitigation_response.json()
            
            # Validate mitigation improved the text
            assert len(mitigation_data["mitigated_text"]) > len(output_text)
            assert mitigation_data["confidence_improvement"] > 0
        
        # Step 5: Get metrics
        metrics_response = self.client.get("/v1/metrics")
        assert metrics_response.status_code == 200
        metrics_data = metrics_response.json()
        
        # Validate metrics structure
        assert "service_health" in metrics_data
        assert "performance_metrics" in metrics_data
        assert "pattern_statistics" in metrics_data
        
        return {
            "detection": detection_data,
            "validation": validation_data,
            "metrics": metrics_data
        }
    
    def test_health_check_flow(self):
        """Test health check flow and component status."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # Validate structure
        assert "status" in data
        assert "version" in data
        assert "components" in data
        assert "metrics" in data
        
        # Validate status
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
        assert data["version"] == "1.0.0"
        
        # Validate components
        components = data["components"]
        assert "detector" in components
        assert "validator" in components
        assert "constitutional" in components
        assert "metrics" in components
        
        # All components should be healthy
        for component, status in components.items():
            assert status is True
        
        # Validate metrics
        metrics = data["metrics"]
        assert "uptime_seconds" in metrics
        assert "cpu_usage" in metrics
        assert "memory_mb" in metrics
        assert "patterns_detected_today" in metrics
        assert "average_risk_score" in metrics
        
        return data
    
    def test_error_flow_handling(self):
        """Test error flow handling and recovery."""
        # Test invalid input
        response = self.client.post("/v1/detect", json={
            "text": ""  # Empty text should be handled gracefully
        })
        assert response.status_code == 422  # Validation error
        
        # Test malformed JSON
        response = self.client.post("/v1/detect", 
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
        
        # Test large payload
        large_text = "This is a test. " * 1000
        response = self.client.post("/v1/detect", json={
            "text": large_text
        })
        # Should handle gracefully (either accept or return appropriate error)
        assert response.status_code in [200, 413, 422]
    
    def test_concurrent_requests(self):
        """Test concurrent request handling."""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                response = self.client.post("/v1/detect", json={
                    "text": "This is a concurrent test request."
                })
                results.append(response.status_code)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Should have 5 successful responses and no errors
        assert len(results) == 5
        assert len(errors) == 0
        assert all(status == 200 for status in results)
    
    def test_performance_benchmarks(self):
        """Test performance benchmarks."""
        test_cases = [
            "Short text",
            "This is a medium length text with some complexity and multiple sentences.",
            "This is a longer text with multiple paragraphs and complex sentences. " * 10
        ]
        
        for text in test_cases:
            start_time = time.time()
            response = self.client.post("/v1/detect", json={"text": text})
            processing_time = time.time() - start_time
            
            assert response.status_code == 200
            assert processing_time < 1.0  # Should complete within 1 second
            
            # Validate response structure
            data = response.json()
            assert "detections" in data
            assert "processing_time_ms" in data
            assert data["processing_time_ms"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
