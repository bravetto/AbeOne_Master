"""
Comprehensive Unit Tests for Trust Guard Metrics System

Tests metrics collection with edge cases, error scenarios, and performance validation.
"""

import pytest
import time
import threading
from unittest.mock import Mock, patch
from typing import Dict, Any, List

from trustguard.metrics import ReliabilityMetrics


class TestReliabilityMetrics:
    """Test the ReliabilityMetrics class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.metrics = ReliabilityMetrics()
    
    def test_initialization(self):
        """Test metrics initialization."""
        assert hasattr(self.metrics, 'detection_counts')
        assert hasattr(self.metrics, 'validation_counts')
        assert hasattr(self.metrics, 'mitigation_counts')
        assert hasattr(self.metrics, 'pattern_counts')
        assert hasattr(self.metrics, 'start_time')
        
        assert self.metrics.detection_counts == 0
        assert self.metrics.mitigation_counts == 0
        assert isinstance(self.metrics.validation_counts, dict)
        assert isinstance(self.metrics.pattern_counts, dict)
        assert self.metrics.start_time > 0
    
    def test_is_healthy(self):
        """Test health check."""
        assert self.metrics.is_healthy() is True
    
    def test_record_detection_normal(self):
        """Test detection recording with normal inputs."""
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.8, "risk_level": "high"},
                "bias": {"score": 0.3, "risk_level": "low"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        assert self.metrics.pattern_counts["hallucination"] == 1
        assert self.metrics.pattern_counts["bias"] == 1
    
    def test_record_detection_none_input(self):
        """Test detection recording with None input."""
        self.metrics.record_detection(None, 0.1)
        
        assert self.metrics.detection_counts == 1
        # Should handle None gracefully
    
    def test_record_detection_invalid_input(self):
        """Test detection recording with invalid input."""
        self.metrics.record_detection("invalid", 0.1)
        
        assert self.metrics.detection_counts == 1
        # Should handle invalid input gracefully
    
    def test_record_detection_empty_detections(self):
        """Test detection recording with empty detections."""
        detection_result = {"detections": {}}
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        # Should handle empty detections gracefully
    
    def test_record_detection_missing_detections_key(self):
        """Test detection recording with missing detections key."""
        detection_result = {"other_key": "value"}
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        # Should handle missing detections key gracefully
    
    def test_record_detection_invalid_pattern_data(self):
        """Test detection recording with invalid pattern data."""
        detection_result = {
            "detections": {
                "hallucination": "invalid_data",
                "bias": {"score": "invalid", "risk_level": "low"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        # Should handle invalid pattern data gracefully
    
    def test_record_validation_normal(self):
        """Test validation recording with normal inputs."""
        validation_result = {"risk_level": "medium"}
        
        self.metrics.record_validation(validation_result)
        
        assert self.metrics.validation_counts["total"] == 1
        assert self.metrics.validation_counts["by_risk_level"]["medium"] == 1
    
    def test_record_validation_none_input(self):
        """Test validation recording with None input."""
        self.metrics.record_validation(None)
        
        assert self.metrics.validation_counts["total"] == 1
        # Should handle None gracefully
    
    def test_record_validation_invalid_input(self):
        """Test validation recording with invalid input."""
        self.metrics.record_validation("invalid")
        
        assert self.metrics.validation_counts["total"] == 1
        # Should handle invalid input gracefully
    
    def test_record_validation_missing_risk_level(self):
        """Test validation recording with missing risk level."""
        validation_result = {"other_key": "value"}
        self.metrics.record_validation(validation_result)
        
        assert self.metrics.validation_counts["total"] == 1
        # Should handle missing risk level gracefully
    
    def test_record_validation_invalid_risk_level(self):
        """Test validation recording with invalid risk level."""
        validation_result = {"risk_level": "invalid"}
        self.metrics.record_validation(validation_result)
        
        assert self.metrics.validation_counts["total"] == 1
        # Should handle invalid risk level gracefully
    
    def test_record_mitigation_normal(self):
        """Test mitigation recording with normal inputs."""
        mitigation_result = {"technique": "constitutional_prompting"}
        
        self.metrics.record_mitigation(mitigation_result)
        
        assert self.metrics.mitigation_counts == 1
    
    def test_record_mitigation_none_input(self):
        """Test mitigation recording with None input."""
        self.metrics.record_mitigation(None)
        
        assert self.metrics.mitigation_counts == 1
        # Should handle None gracefully
    
    def test_record_mitigation_invalid_input(self):
        """Test mitigation recording with invalid input."""
        self.metrics.record_mitigation("invalid")
        
        assert self.metrics.mitigation_counts == 1
        # Should handle invalid input gracefully
    
    def test_record_mitigation_missing_technique(self):
        """Test mitigation recording with missing technique."""
        mitigation_result = {"other_key": "value"}
        self.metrics.record_mitigation(mitigation_result)
        
        assert self.metrics.mitigation_counts == 1
        # Should handle missing technique gracefully
    
    def test_get_average_risk_score_no_data(self):
        """Test average risk score calculation with no data."""
        score = self.metrics.get_average_risk_score()
        
        assert isinstance(score, float)
        assert score == 0.0
    
    def test_get_average_risk_score_with_data(self):
        """Test average risk score calculation with data."""
        # Record some detections with different risk levels
        detection_result_1 = {
            "detections": {
                "hallucination": {"score": 0.8, "risk_level": "high"}
            }
        }
        detection_result_2 = {
            "detections": {
                "bias": {"score": 0.3, "risk_level": "low"}
            }
        }
        
        self.metrics.record_detection(detection_result_1, 0.1)
        self.metrics.record_detection(detection_result_2, 0.1)
        
        score = self.metrics.get_average_risk_score()
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 10.0
    
    def test_get_patterns_detected_today_no_data(self):
        """Test patterns detected today with no data."""
        count = self.metrics.get_patterns_detected_today()
        
        assert isinstance(count, int)
        assert count == 0
    
    def test_get_patterns_detected_today_with_data(self):
        """Test patterns detected today with data."""
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.8, "risk_level": "high"},
                "bias": {"score": 0.3, "risk_level": "low"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        count = self.metrics.get_patterns_detected_today()
        
        assert isinstance(count, int)
        assert count == 2
    
    def test_get_metrics_summary(self):
        """Test metrics summary generation."""
        # Record some data
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.8, "risk_level": "high"}
            }
        }
        validation_result = {"risk_level": "medium"}
        mitigation_result = {"technique": "constitutional_prompting"}
        
        self.metrics.record_detection(detection_result, 0.1)
        self.metrics.record_validation(validation_result)
        self.metrics.record_mitigation(mitigation_result)
        
        summary = self.metrics.get_metrics_summary()
        
        assert isinstance(summary, dict)
        assert "total_detections" in summary
        assert "total_validations" in summary
        assert "total_mitigations" in summary
        assert "pattern_counts" in summary
        assert "validation_breakdown" in summary
        assert "average_risk_score" in summary
        assert "uptime_seconds" in summary
        assert "last_updated" in summary
        assert "prometheus_available" in summary
        
        assert summary["total_detections"] == 1
        assert summary["total_validations"] == 1
        assert summary["total_mitigations"] == 1
        assert summary["pattern_counts"]["hallucination"] == 1
        assert summary["validation_breakdown"]["medium"] == 1
        assert isinstance(summary["average_risk_score"], float)
        assert isinstance(summary["uptime_seconds"], float)
        assert summary["uptime_seconds"] > 0
        assert isinstance(summary["last_updated"], float)
        assert summary["last_updated"] > 0
        assert isinstance(summary["prometheus_available"], bool)
    
    def test_record_request_metrics(self):
        """Test request metrics recording."""
        self.metrics.record_request("GET", "/health", 0.1, 200, "test_user")
        
        # Should not raise any exceptions
        assert True
    
    def test_record_validation_metrics(self):
        """Test validation metrics recording."""
        self.metrics.record_validation_metrics("medium", 0.2)
        
        # Should not raise any exceptions
        assert True
    
    def test_record_mitigation_metrics(self):
        """Test mitigation metrics recording."""
        self.metrics.record_mitigation_metrics("constitutional_prompting", 0.3)
        
        # Should not raise any exceptions
        assert True
    
    def test_calculate_sli_slo_metrics(self):
        """Test SLI/SLO metrics calculation."""
        self.metrics.calculate_sli_slo_metrics()
        
        # Should not raise any exceptions
        assert True
    
    def test_get_prometheus_metrics(self):
        """Test Prometheus metrics generation."""
        metrics_text = self.metrics.get_prometheus_metrics()
        
        assert isinstance(metrics_text, str)
        assert len(metrics_text) > 0
    
    def test_performance_large_volume(self):
        """Test performance with large volume of metrics."""
        start_time = time.time()
        
        # Record many detections
        for i in range(1000):
            detection_result = {
                "detections": {
                    "hallucination": {"score": 0.5, "risk_level": "medium"}
                }
            }
            self.metrics.record_detection(detection_result, 0.1)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        assert self.metrics.detection_counts == 1000
        assert processing_time < 5.0  # Should complete within 5 seconds
    
    def test_concurrent_metrics_recording(self):
        """Test concurrent metrics recording."""
        results = []
        errors = []
        
        def record_metrics_worker(worker_id):
            try:
                for i in range(100):
                    detection_result = {
                        "detections": {
                            "hallucination": {"score": 0.5, "risk_level": "medium"}
                        }
                    }
                    self.metrics.record_detection(detection_result, 0.1)
                results.append(worker_id)
            except Exception as e:
                errors.append((worker_id, e))
        
        # Start multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=record_metrics_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 10, f"Expected 10 results, got {len(results)}"
        assert self.metrics.detection_counts == 1000  # 10 workers * 100 detections each
    
    def test_metrics_persistence_across_instances(self):
        """Test that metrics are properly isolated between instances."""
        metrics1 = ReliabilityMetrics()
        metrics2 = ReliabilityMetrics()
        
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.8, "risk_level": "high"}
            }
        }
        
        metrics1.record_detection(detection_result, 0.1)
        
        assert metrics1.detection_counts == 1
        assert metrics2.detection_counts == 0  # Should be independent
    
    def test_edge_case_very_high_scores(self):
        """Test metrics with very high scores."""
        detection_result = {
            "detections": {
                "hallucination": {"score": 1.0, "risk_level": "high"},
                "bias": {"score": 1.0, "risk_level": "high"},
                "deception": {"score": 1.0, "risk_level": "high"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        assert self.metrics.pattern_counts["hallucination"] == 1
        assert self.metrics.pattern_counts["bias"] == 1
        assert self.metrics.pattern_counts["deception"] == 1
    
    def test_edge_case_very_low_scores(self):
        """Test metrics with very low scores."""
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.0, "risk_level": "low"},
                "bias": {"score": 0.0, "risk_level": "low"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        assert self.metrics.pattern_counts["hallucination"] == 1
        assert self.metrics.pattern_counts["bias"] == 1
    
    def test_edge_case_mixed_risk_levels(self):
        """Test metrics with mixed risk levels."""
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.8, "risk_level": "high"},
                "bias": {"score": 0.5, "risk_level": "medium"},
                "deception": {"score": 0.2, "risk_level": "low"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        assert self.metrics.pattern_counts["hallucination"] == 1
        assert self.metrics.pattern_counts["bias"] == 1
        assert self.metrics.pattern_counts["deception"] == 1
    
    def test_edge_case_all_patterns(self):
        """Test metrics with all available patterns."""
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.5, "risk_level": "medium"},
                "drift": {"score": 0.5, "risk_level": "medium"},
                "bias": {"score": 0.5, "risk_level": "medium"},
                "deception": {"score": 0.5, "risk_level": "medium"},
                "security_theater": {"score": 0.5, "risk_level": "medium"},
                "duplication": {"score": 0.5, "risk_level": "medium"},
                "stub_syndrome": {"score": 0.5, "risk_level": "medium"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        for pattern in ["hallucination", "drift", "bias", "deception", 
                       "security_theater", "duplication", "stub_syndrome"]:
            assert self.metrics.pattern_counts[pattern] == 1


class TestEdgeCasesMetrics:
    """Test edge cases and error scenarios for metrics."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.metrics = ReliabilityMetrics()
    
    def test_very_large_detection_result(self):
        """Test with very large detection result."""
        # Create a large detection result
        detections = {}
        for i in range(1000):
            detections[f"pattern_{i}"] = {"score": 0.5, "risk_level": "medium"}
        
        detection_result = {"detections": detections}
        
        start_time = time.time()
        self.metrics.record_detection(detection_result, 0.1)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        assert self.metrics.detection_counts == 1
        assert processing_time < 5.0  # Should complete within 5 seconds
    
    def test_unicode_pattern_names(self):
        """Test with unicode pattern names."""
        detection_result = {
            "detections": {
                "hallucination_世界": {"score": 0.5, "risk_level": "medium"},
                "bias_🌍": {"score": 0.5, "risk_level": "medium"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        assert self.metrics.pattern_counts["hallucination_世界"] == 1
        assert self.metrics.pattern_counts["bias_🌍"] == 1
    
    def test_special_characters_in_pattern_names(self):
        """Test with special characters in pattern names."""
        detection_result = {
            "detections": {
                "pattern@#$%": {"score": 0.5, "risk_level": "medium"},
                "pattern!@#$%^&*()": {"score": 0.5, "risk_level": "medium"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        assert self.metrics.pattern_counts["pattern@#$%"] == 1
        assert self.metrics.pattern_counts["pattern!@#$%^&*()"] == 1
    
    def test_none_values_in_detection_data(self):
        """Test with None values in detection data."""
        detection_result = {
            "detections": {
                "hallucination": {"score": None, "risk_level": None},
                "bias": {"score": 0.5, "risk_level": "medium"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        # Should handle None values gracefully
    
    def test_empty_strings_in_detection_data(self):
        """Test with empty strings in detection data."""
        detection_result = {
            "detections": {
                "hallucination": {"score": "", "risk_level": ""},
                "bias": {"score": 0.5, "risk_level": "medium"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        # Should handle empty strings gracefully
    
    def test_nested_detection_data(self):
        """Test with nested detection data."""
        detection_result = {
            "detections": {
                "hallucination": {
                    "score": 0.5,
                    "risk_level": "medium",
                    "nested": {
                        "sub_score": 0.3,
                        "sub_risk": "low"
                    }
                }
            }
        }
        
        self.metrics.record_detection(detection_result, 0.1)
        
        assert self.metrics.detection_counts == 1
        assert self.metrics.pattern_counts["hallucination"] == 1
    
    def test_very_long_processing_time(self):
        """Test with very long processing time."""
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.5, "risk_level": "medium"}
            }
        }
        
        self.metrics.record_detection(detection_result, 999.9)  # Very long processing time
        
        assert self.metrics.detection_counts == 1
        # Should handle very long processing times gracefully
    
    def test_negative_processing_time(self):
        """Test with negative processing time."""
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.5, "risk_level": "medium"}
            }
        }
        
        self.metrics.record_detection(detection_result, -0.1)  # Negative processing time
        
        assert self.metrics.detection_counts == 1
        # Should handle negative processing times gracefully
    
    def test_zero_processing_time(self):
        """Test with zero processing time."""
        detection_result = {
            "detections": {
                "hallucination": {"score": 0.5, "risk_level": "medium"}
            }
        }
        
        self.metrics.record_detection(detection_result, 0.0)  # Zero processing time
        
        assert self.metrics.detection_counts == 1
        # Should handle zero processing time gracefully


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
