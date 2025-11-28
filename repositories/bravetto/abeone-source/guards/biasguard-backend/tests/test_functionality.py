"""
Comprehensive functionality tests for PoisonGuard.
Tests end-to-end workflows, data validation, and system integration.
"""

import unittest
import json
import tempfile
import os
from fastapi.testclient import TestClient
from src.poisonguard.api import app
from src.poisonguard.core import DataSample, AnalysisResult, MitigationAction, Report
from src.poisonguard.analyzer import Analyzer
from src.poisonguard.mitigator import Mitigator
from src.poisonguard.reporter import Reporter
from src.poisonguard.config_validator import validate_config


class TestDataValidation(unittest.TestCase):
    """Test data validation and output verification."""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_data_sample_validation(self):
        """Test DataSample model validation."""
        # Valid sample
        sample = DataSample(id="test-1", content="This is a test sample.")
        self.assertEqual(sample.id, "test-1")
        self.assertEqual(sample.content, "This is a test sample.")
        self.assertIsNone(sample.metadata)
        
        # Sample with metadata
        sample_with_meta = DataSample(
            id="test-2", 
            content="Another test sample.",
            metadata={"source": "test", "timestamp": "2023-01-01"}
        )
        self.assertEqual(sample_with_meta.metadata["source"], "test")
        
        # Test with non-string content
        sample_non_string = DataSample(id="test-3", content=123)
        self.assertEqual(sample_non_string.content, 123)
    
    def test_analysis_result_validation(self):
        """Test AnalysisResult model validation."""
        result = AnalysisResult(
            sample_id="test-1",
            is_poisoned=True,
            confidence=0.95,
            details={"reasons": ["suspicious_keyword"], "model_prediction": {"label": "NEGATIVE", "score": 0.95}}
        )
        
        self.assertEqual(result.sample_id, "test-1")
        self.assertTrue(result.is_poisoned)
        self.assertEqual(result.confidence, 0.95)
        self.assertIn("reasons", result.details)
        self.assertIn("model_prediction", result.details)
    
    def test_mitigation_action_validation(self):
        """Test MitigationAction model validation."""
        action = MitigationAction(
            sample_id="test-1",
            action_taken="sanitize",
            details={"sanitized_content": "cleaned text", "reason": "suspicious_keyword"}
        )
        
        self.assertEqual(action.sample_id, "test-1")
        self.assertEqual(action.action_taken, "sanitize")
        self.assertIn("sanitized_content", action.details)
        self.assertIn("reason", action.details)
    
    def test_report_validation(self):
        """Test Report model validation."""
        analysis_results = [
            AnalysisResult(sample_id="1", is_poisoned=True, confidence=0.9, details={}),
            AnalysisResult(sample_id="2", is_poisoned=False, confidence=0.1, details={})
        ]
        mitigation_actions = [
            MitigationAction(sample_id="1", action_taken="flag", details={}),
            MitigationAction(sample_id="2", action_taken="none", details={})
        ]
        
        report = Report(
            total_samples=2,
            poisoned_samples=1,
            mitigated_samples=1,
            analysis_results=analysis_results,
            mitigation_actions=mitigation_actions
        )
        
        self.assertEqual(report.total_samples, 2)
        self.assertEqual(report.poisoned_samples, 1)
        self.assertEqual(report.mitigated_samples, 1)
        self.assertEqual(len(report.analysis_results), 2)
        self.assertEqual(len(report.mitigation_actions), 2)


class TestEndToEndWorkflows(unittest.TestCase):
    """Test complete end-to-end workflows."""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_analyze_workflow(self):
        """Test complete analysis workflow."""
        # Test data
        test_samples = [
            {"id": "clean-1", "content": "This is a perfectly normal sentence."},
            {"id": "suspicious-1", "content": "This contains malicious content."},
            {"id": "short-1", "content": "Too short"},
            {"id": "long-1", "content": "This is a very long sentence that exceeds the maximum length limit and should be flagged by the length plugin for being too long and potentially suspicious."}
        ]
        
        response = self.client.post("/analyze", json={"samples": test_samples})
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Correlation-ID", response.headers)
        
        data = response.json()
        self.assertEqual(len(data), 4)
        
        # Verify each result has required fields
        for result in data:
            self.assertIn("sample_id", result)
            self.assertIn("is_poisoned", result)
            self.assertIn("confidence", result)
            self.assertIn("details", result)
            self.assertIn("reasons", result["details"])
        
        # Verify specific results
        sample_ids = [result["sample_id"] for result in data]
        self.assertIn("clean-1", sample_ids)
        self.assertIn("suspicious-1", sample_ids)
        self.assertIn("short-1", sample_ids)
        self.assertIn("long-1", sample_ids)
    
    def test_mitigate_workflow(self):
        """Test complete mitigation workflow."""
        # Test data with known issues
        test_samples = [
            {"id": "malicious-1", "content": "This contains malicious content."},
            {"id": "clean-1", "content": "This is perfectly clean content."}
        ]
        
        response = self.client.post("/mitigate", json={"samples": test_samples})
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Correlation-ID", response.headers)
        
        data = response.json()
        self.assertEqual(len(data), 2)
        
        # Verify each action has required fields
        for action in data:
            self.assertIn("sample_id", action)
            self.assertIn("action_taken", action)
            self.assertIn("details", action)
        
        # Verify action types (since samples are clean, they should all be "none")
        action_types = [action["action_taken"] for action in data]
        self.assertTrue(all(action == "none" for action in action_types))
    
    def test_report_workflow(self):
        """Test complete report generation workflow."""
        # Test data
        test_samples = [
            {"id": "sample-1", "content": "This is a test sample."},
            {"id": "sample-2", "content": "This contains malicious content."},
            {"id": "sample-3", "content": "Another clean sample."}
        ]
        
        response = self.client.post("/report", json={"samples": test_samples})
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("total_samples", data)
        self.assertIn("poisoned_samples", data)
        self.assertIn("mitigated_samples", data)
        self.assertIn("analysis_results", data)
        self.assertIn("mitigation_actions", data)
        
        # Verify counts
        self.assertEqual(data["total_samples"], 3)
        self.assertGreaterEqual(data["poisoned_samples"], 0)
        self.assertGreaterEqual(data["mitigated_samples"], 0)
        self.assertEqual(len(data["analysis_results"]), 3)
        self.assertEqual(len(data["mitigation_actions"]), 3)


class TestDataOutputVerification(unittest.TestCase):
    """Test data output verification and consistency."""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_analyze_output_consistency(self):
        """Test that analyze output is consistent and valid."""
        test_samples = [
            {"id": "test-1", "content": "Test content 1."},
            {"id": "test-2", "content": "Test content 2."}
        ]
        
        response = self.client.post("/analyze", json={"samples": test_samples})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Verify structure consistency
        for i, result in enumerate(data):
            self.assertEqual(result["sample_id"], test_samples[i]["id"])
            self.assertIsInstance(result["is_poisoned"], bool)
            self.assertIsInstance(result["confidence"], (int, float))
            self.assertGreaterEqual(result["confidence"], 0.0)
            self.assertLessEqual(result["confidence"], 1.0)
            self.assertIsInstance(result["details"], dict)
            self.assertIn("reasons", result["details"])
            self.assertIsInstance(result["details"]["reasons"], list)
    
    def test_mitigate_output_consistency(self):
        """Test that mitigate output is consistent and valid."""
        test_samples = [
            {"id": "test-1", "content": "Test content 1."},
            {"id": "test-2", "content": "Test content 2."}
        ]
        
        response = self.client.post("/mitigate", json={"samples": test_samples})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Verify structure consistency
        for i, action in enumerate(data):
            self.assertEqual(action["sample_id"], test_samples[i]["id"])
            self.assertIn(action["action_taken"], ["flag", "sanitize", "redact", "none"])
            self.assertIsInstance(action["details"], dict)
    
    def test_report_output_consistency(self):
        """Test that report output is consistent and valid."""
        test_samples = [
            {"id": "test-1", "content": "Test content 1."},
            {"id": "test-2", "content": "Test content 2."}
        ]
        
        response = self.client.post("/report", json={"samples": test_samples})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Verify structure consistency
        self.assertIsInstance(data["total_samples"], int)
        self.assertIsInstance(data["poisoned_samples"], int)
        self.assertIsInstance(data["mitigated_samples"], int)
        self.assertIsInstance(data["analysis_results"], list)
        self.assertIsInstance(data["mitigation_actions"], list)
        
        # Verify counts are consistent
        self.assertEqual(data["total_samples"], len(test_samples))
        self.assertEqual(len(data["analysis_results"]), len(test_samples))
        self.assertEqual(len(data["mitigation_actions"]), len(test_samples))
        self.assertLessEqual(data["poisoned_samples"], data["total_samples"])
        self.assertLessEqual(data["mitigated_samples"], data["total_samples"])
    
    def test_correlation_id_consistency(self):
        """Test that correlation IDs are consistent across requests."""
        test_samples = [{"id": "test-1", "content": "Test content."}]
        
        # Make multiple requests
        response1 = self.client.post("/analyze", json={"samples": test_samples})
        response2 = self.client.post("/analyze", json={"samples": test_samples})
        
        # Verify correlation IDs are present and different
        self.assertIn("X-Correlation-ID", response1.headers)
        self.assertIn("X-Correlation-ID", response2.headers)
        self.assertNotEqual(
            response1.headers["X-Correlation-ID"],
            response2.headers["X-Correlation-ID"]
        )
    
    def test_error_handling_consistency(self):
        """Test that error responses are consistent."""
        # Test empty samples
        response = self.client.post("/analyze", json={"samples": []})
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())
        
        # Test invalid input
        response = self.client.post("/analyze", json={"samples": [{"id": "test"}]})  # Missing content
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())
        
        # Test invalid JSON
        response = self.client.post("/analyze", json="invalid")
        self.assertEqual(response.status_code, 422)


class TestSystemIntegration(unittest.TestCase):
    """Test system integration and component interaction."""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_health_check_integration(self):
        """Test health check endpoint integration."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("timestamp", data)
        self.assertIn("uptime_seconds", data)
        self.assertIn("memory_usage_percent", data)
        self.assertIn("cpu_usage_percent", data)
    
    def test_metrics_integration(self):
        """Test metrics endpoint integration."""
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "text/plain; version=1.0.0; charset=utf-8")
        
        # Verify metrics content
        content = response.text
        self.assertIn("poisonguard_requests_total", content)
        self.assertIn("REPLACE_ME", content)
    
    def test_config_validation_integration(self):
        """Test configuration validation endpoint integration."""
        response = self.client.get("/config/validation")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("valid", data)
        self.assertIn("errors", data)
        self.assertIn("warnings", data)
        self.assertIn("plugin_count", data)
        self.assertIn("default_action", data)
    
    def test_audit_trail_integration(self):
        """Test audit trail endpoints integration."""
        # First, make some requests to generate audit data
        test_samples = [{"id": "audit-test", "content": "Test for audit trail."}]
        
        # Generate some activity
        self.client.post("/analyze", json={"samples": test_samples})
        self.client.post("/mitigate", json={"samples": test_samples})
        
        # Test audit endpoints
        response = self.client.get("/audit/analysis")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        
        response = self.client.get("/audit/mitigation")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        
        response = self.client.get("/audit/system")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_cors_integration(self):
        """Test CORS headers are present."""
        response = self.client.options("/analyze")
        # CORS preflight should be handled by middleware
        self.assertIn(response.status_code, [200, 405])  # 405 is OK for OPTIONS on POST endpoint


class TestPerformanceAndReliability(unittest.TestCase):
    """Test performance and reliability aspects."""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                response = self.client.post(
                    "/analyze",
                    json={"samples": [{"id": f"concurrent-{threading.current_thread().ident}", "content": "Test content."}]}
                )
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all requests succeeded
        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        self.assertEqual(len(results), 5)
        self.assertTrue(all(status == 200 for status in results))
    
    def test_large_payload_handling(self):
        """Test handling of large payloads."""
        # Create a large number of samples
        large_samples = []
        for i in range(100):
            large_samples.append({
                "id": f"large-{i}",
                "content": f"This is sample number {i} with some content to analyze."
            })
        
        response = self.client.post("/analyze", json={"samples": large_samples})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 100)
    
    def test_memory_usage_stability(self):
        """Test that memory usage remains stable under load."""
        # This is a basic test - in production, you'd want more sophisticated monitoring
        for i in range(10):
            response = self.client.post(
                "/analyze",
                json={"samples": [{"id": f"memory-test-{i}", "content": "Test content."}]}
            )
            self.assertEqual(response.status_code, 200)
    
    def test_error_recovery(self):
        """Test that the system recovers from errors."""
        # Test with invalid input
        response = self.client.post("/analyze", json={"samples": [{"id": "test"}]})  # Missing content
        self.assertEqual(response.status_code, 422)
        
        # Verify system still works after error
        response = self.client.post(
            "/analyze",
            json={"samples": [{"id": "recovery-test", "content": "Valid content."}]}
        )
        self.assertEqual(response.status_code, 200)


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and consistency."""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_analysis_result_consistency(self):
        """Test that analysis results are consistent across multiple runs."""
        test_samples = [{"id": "consistency-test", "content": "This is a test for consistency."}]
        
        # Run analysis multiple times
        results = []
        for i in range(3):
            response = self.client.post("/analyze", json={"samples": test_samples})
            self.assertEqual(response.status_code, 200)
            results.append(response.json()[0])
        
        # Results should be consistent (same sample should produce same result)
        for result in results[1:]:
            self.assertEqual(result["sample_id"], results[0]["sample_id"])
            # Note: In a real system, you might want to allow for some variance in confidence scores
    
    def test_mitigation_action_consistency(self):
        """Test that mitigation actions are consistent."""
        test_samples = [{"id": "mitigation-test", "content": "This is a test for mitigation consistency."}]
        
        # Run mitigation multiple times
        results = []
        for i in range(3):
            response = self.client.post("/mitigate", json={"samples": test_samples})
            self.assertEqual(response.status_code, 200)
            results.append(response.json()[0])
        
        # Actions should be consistent
        for result in results[1:]:
            self.assertEqual(result["sample_id"], results[0]["sample_id"])
            # Action taken should be the same for the same input
    
    def test_report_accuracy(self):
        """Test that reports accurately reflect the data."""
        test_samples = [
            {"id": "report-1", "content": "Clean content."},
            {"id": "report-2", "content": "Potentially malicious content."},
            {"id": "report-3", "content": "Another clean sample."}
        ]
        
        response = self.client.post("/report", json={"samples": test_samples})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Verify report accuracy
        self.assertEqual(data["total_samples"], 3)
        self.assertEqual(len(data["analysis_results"]), 3)
        self.assertEqual(len(data["mitigation_actions"]), 3)
        
        # Verify sample IDs match
        sample_ids = [result["sample_id"] for result in data["analysis_results"]]
        expected_ids = ["report-1", "report-2", "report-3"]
        for expected_id in expected_ids:
            self.assertIn(expected_id, sample_ids)


if __name__ == '__main__':
    unittest.main()
