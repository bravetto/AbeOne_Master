"""
Comprehensive Unit Tests for Trust Guard Validation Engine

Tests validation engine with edge cases, error scenarios, and mathematical validation.
"""

import pytest
import time
import math
from unittest.mock import Mock, patch
from typing import Dict, Any, List

from trustguard.validation import ValidationEngine, _safe_text_input


class TestSafeTextInputValidation:
    """Test the safe text input helper function in validation module."""
    
    def test_none_input(self):
        """Test handling of None input."""
        result = _safe_text_input(None)
        assert result == ""
        assert isinstance(result, str)
    
    def test_various_input_types(self):
        """Test handling of various input types."""
        test_cases = [
            ("hello", "hello"),
            (123, "123"),
            (123.45, "123.45"),
            ([1, 2, 3], "[1, 2, 3]"),
            ({"key": "value"}, "{'key': 'value'}"),
            (True, "True"),
            ("", ""),
        ]
        
        for input_val, expected in test_cases:
            result = _safe_text_input(input_val)
            assert result == expected
            assert isinstance(result, str)


class TestValidationEngine:
    """Test the ValidationEngine class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = ValidationEngine()
    
    def test_initialization(self):
        """Test validator initialization."""
        assert self.validator.kl_divergence_threshold == 0.5
        assert self.validator.uncertainty_threshold == 0.7
        assert isinstance(self.validator.evidence_weights, dict)
        assert "pattern_detections" in self.validator.evidence_weights
        assert "mathematical_scores" in self.validator.evidence_weights
        assert "contextual_factors" in self.validator.evidence_weights
        assert "metadata_factors" in self.validator.evidence_weights
    
    def test_is_healthy(self):
        """Test health check."""
        assert self.validator.is_healthy() is True
    
    def test_perform_mathematical_validation_normal(self):
        """Test mathematical validation with normal inputs."""
        input_text = "This is a normal response."
        output_text = "This is a normal response with additional context."
        
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "kl_divergence" in result
        assert "uncertainty_score" in result
        assert "consistency_score" in result
        assert "statistical_analysis" in result
        assert "confidence_intervals" in result
        assert "overall_score" in result
        assert "risk_level" in result
        
        # Check score ranges
        assert 0.0 <= result["kl_divergence"] <= 1.0
        assert 0.0 <= result["uncertainty_score"] <= 1.0
        assert 0.0 <= result["consistency_score"] <= 1.0
        assert 0.0 <= result["overall_score"] <= 10.0
        assert result["risk_level"] in ["low", "medium", "high", "unknown"]
    
    def test_perform_mathematical_validation_none_inputs(self):
        """Test mathematical validation with None inputs."""
        result = self.validator.perform_mathematical_validation(None, None)
        
        assert isinstance(result, dict)
        assert "kl_divergence" in result
        assert "uncertainty_score" in result
        assert "consistency_score" in result
        assert "overall_score" in result
        assert "risk_level" in result
    
    def test_perform_mathematical_validation_integer_inputs(self):
        """Test mathematical validation with integer inputs."""
        result = self.validator.perform_mathematical_validation(123, 456)
        
        assert isinstance(result, dict)
        assert "kl_divergence" in result
        assert "overall_score" in result
    
    def test_perform_mathematical_validation_empty_strings(self):
        """Test mathematical validation with empty strings."""
        result = self.validator.perform_mathematical_validation("", "")
        
        assert isinstance(result, dict)
        assert "kl_divergence" in result
        assert "overall_score" in result
    
    def test_perform_mathematical_validation_identical_texts(self):
        """Test mathematical validation with identical texts."""
        text = "This is identical text."
        result = self.validator.perform_mathematical_validation(text, text)
        
        assert isinstance(result, dict)
        assert result["kl_divergence"] == 0.0  # Should be 0 for identical texts
        assert result["consistency_score"] > 0.8  # Should be high consistency
    
    def test_perform_mathematical_validation_completely_different_texts(self):
        """Test mathematical validation with completely different texts."""
        input_text = "This is about cats and dogs."
        output_text = "Quantum physics and mathematics are fascinating subjects."
        
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert result["kl_divergence"] > 0.5  # Should be high divergence
        assert result["consistency_score"] < 0.5  # Should be low consistency
    
    def test_calculate_risk_assessment_normal(self):
        """Test risk assessment calculation with normal inputs."""
        detections = {
            "hallucination": {"score": 0.3, "confidence": 0.8},
            "bias": {"score": 0.2, "confidence": 0.7},
            "deception": {"score": 0.1, "confidence": 0.9}
        }
        
        result = self.validator.calculate_risk_assessment(detections)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
        assert "risk_level" in result
        assert "confidence" in result
        assert "evidence" in result
        assert "recommendations" in result
        
        assert 0.0 <= result["overall_score"] <= 10.0
        assert result["risk_level"] in ["low", "medium", "high", "unknown"]
        assert 0.0 <= result["confidence"] <= 1.0
        assert isinstance(result["evidence"], list)
        assert isinstance(result["recommendations"], list)
    
    def test_calculate_risk_assessment_none_input(self):
        """Test risk assessment calculation with None input."""
        result = self.validator.calculate_risk_assessment(None)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
        assert "risk_level" in result
        assert result["risk_level"] == "unknown"
    
    def test_calculate_risk_assessment_empty_dict(self):
        """Test risk assessment calculation with empty dictionary."""
        result = self.validator.calculate_risk_assessment({})
        
        assert isinstance(result, dict)
        assert "overall_score" in result
        assert "risk_level" in result
        assert result["overall_score"] == 0.0
        assert result["risk_level"] == "low"
    
    def test_calculate_risk_assessment_high_scores(self):
        """Test risk assessment calculation with high risk scores."""
        detections = {
            "hallucination": {"score": 0.9, "confidence": 0.9},
            "bias": {"score": 0.8, "confidence": 0.8},
            "deception": {"score": 0.7, "confidence": 0.7}
        }
        
        result = self.validator.calculate_risk_assessment(detections)
        
        assert result["overall_score"] > 4.0  # Should be high score
        assert result["risk_level"] == "medium"
    
    def test_calculate_risk_assessment_mixed_scores(self):
        """Test risk assessment calculation with mixed scores."""
        detections = {
            "hallucination": {"score": 0.9, "confidence": 0.9},
            "bias": {"score": 0.2, "confidence": 0.8},
            "deception": {"score": 0.1, "confidence": 0.7}
        }
        
        result = self.validator.calculate_risk_assessment(detections)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
        assert "risk_level" in result
        assert result["risk_level"] in ["low", "medium", "high"]
    
    def test_calculate_risk_assessment_invalid_scores(self):
        """Test risk assessment calculation with invalid scores."""
        detections = {
            "hallucination": {"score": "invalid", "confidence": 0.8},
            "bias": {"score": 0.2, "confidence": "invalid"},
            "deception": {"score": None, "confidence": 0.7}
        }
        
        result = self.validator.calculate_risk_assessment(detections)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
        assert "risk_level" in result
        # Should handle invalid scores gracefully
    
    def test_quantify_uncertainty_normal(self):
        """Test uncertainty quantification with normal text."""
        text = "I think this might be correct, but I'm not entirely sure."
        result = self.validator._quantify_uncertainty(text)
        
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
        assert result > 0.1  # Should detect uncertainty
    
    def test_quantify_uncertainty_confident_text(self):
        """Test uncertainty quantification with confident text."""
        text = "This is definitely correct without any doubt."
        result = self.validator._quantify_uncertainty(text)
        
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
        assert result < 0.3  # Should detect low uncertainty
    
    def test_quantify_uncertainty_none_input(self):
        """Test uncertainty quantification with None input."""
        result = self.validator._quantify_uncertainty(None)
        
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
    
    def test_quantify_uncertainty_integer_input(self):
        """Test uncertainty quantification with integer input."""
        result = self.validator._quantify_uncertainty(123)
        
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
    
    def test_perform_statistical_analysis_normal(self):
        """Test statistical analysis with normal text."""
        text = "This is a test sentence with multiple words and some punctuation."
        result = self.validator._perform_statistical_analysis(text)
        
        assert isinstance(result, dict)
        assert "word_count" in result
        assert "unique_words" in result
        assert "avg_sentence_length" in result
        assert "lexical_diversity" in result
        assert "readability_score" in result
        
        assert result["word_count"] > 0
        assert result["unique_words"] > 0
        assert result["lexical_diversity"] > 0.0
        assert result["lexical_diversity"] <= 1.0
    
    def test_perform_statistical_analysis_none_input(self):
        """Test statistical analysis with None input."""
        result = self.validator._perform_statistical_analysis(None)
        
        assert isinstance(result, dict)
        assert "word_count" in result
        assert result["word_count"] == 0
    
    def test_perform_statistical_analysis_integer_input(self):
        """Test statistical analysis with integer input."""
        result = self.validator._perform_statistical_analysis(123)
        
        assert isinstance(result, dict)
        assert "word_count" in result
    
    def test_perform_statistical_analysis_empty_string(self):
        """Test statistical analysis with empty string."""
        result = self.validator._perform_statistical_analysis("")
        
        assert isinstance(result, dict)
        assert "word_count" in result
        assert result["word_count"] == 0
    
    def test_perform_statistical_analysis_very_long_text(self):
        """Test statistical analysis with very long text."""
        text = "This is a test sentence. " * 1000
        result = self.validator._perform_statistical_analysis(text)
        
        assert isinstance(result, dict)
        assert "word_count" in result
        assert result["word_count"] > 1000
    
    def test_calculate_confidence_intervals_normal(self):
        """Test confidence interval calculation with normal inputs."""
        text = "This is a test sentence."
        context = "This is the context."
        result = self.validator._calculate_confidence_intervals(text, context)
        
        assert isinstance(result, dict)
        assert "lower_bound" in result
        assert "upper_bound" in result
        assert "confidence_level" in result
        
        assert 0.0 <= result["lower_bound"] <= 1.0
        assert 0.0 <= result["upper_bound"] <= 1.0
        assert result["lower_bound"] <= result["upper_bound"]
    
    def test_calculate_confidence_intervals_none_inputs(self):
        """Test confidence interval calculation with None inputs."""
        result = self.validator._calculate_confidence_intervals(None, None)
        
        assert isinstance(result, dict)
        assert "lower_bound" in result
        assert "upper_bound" in result
    
    def test_extract_word_frequencies_normal(self):
        """Test word frequency extraction with normal text."""
        text = "The quick brown fox jumps over the lazy dog. The fox is quick."
        result = self.validator._extract_word_frequencies(text)
        
        assert isinstance(result, dict)
        assert "the" in result
        assert "fox" in result
        assert "quick" in result
        assert result["the"] == 3
        assert result["fox"] == 2
        assert result["quick"] == 2
    
    def test_extract_word_frequencies_none_input(self):
        """Test word frequency extraction with None input."""
        result = self.validator._extract_word_frequencies(None)
        
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_extract_word_frequencies_integer_input(self):
        """Test word frequency extraction with integer input."""
        result = self.validator._extract_word_frequencies(123)
        
        assert isinstance(result, dict)
        assert len(result) == 0  # Numbers don't match the word pattern
    
    def test_performance_large_text(self):
        """Test performance with large text."""
        input_text = "This is a test sentence. " * 1000
        output_text = "This is another test sentence. " * 1000
        
        start_time = time.time()
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        assert isinstance(result, dict)
        assert "overall_score" in result
        assert processing_time < 5.0  # Should complete within 5 seconds
    
    def test_concurrent_validation(self):
        """Test concurrent validation calls."""
        import threading
        import queue
        
        results = queue.Queue()
        errors = queue.Queue()
        
        def validation_worker(text_id):
            try:
                input_text = f"This is input text number {text_id}."
                output_text = f"This is output text number {text_id}."
                result = self.validator.perform_mathematical_validation(input_text, output_text)
                results.put((text_id, result))
            except Exception as e:
                errors.put((text_id, e))
        
        # Start multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=validation_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        assert errors.empty(), f"Errors occurred: {list(errors.queue)}"
        assert results.qsize() == 10, f"Expected 10 results, got {results.qsize()}"
        
        # Verify all results are valid
        while not results.empty():
            text_id, result = results.get()
            assert isinstance(result, dict)
            assert "overall_score" in result


class TestEdgeCasesValidation:
    """Test edge cases and error scenarios for validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = ValidationEngine()
    
    def test_very_long_texts(self):
        """Test with very long texts (1MB each)."""
        input_text = "A" * 1000000
        output_text = "B" * 1000000
        
        start_time = time.time()
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        assert isinstance(result, dict)
        assert "overall_score" in result
        assert processing_time < 10.0  # Should complete within 10 seconds
    
    def test_special_characters_only(self):
        """Test with only special characters."""
        input_text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        output_text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
    
    def test_unicode_texts(self):
        """Test with unicode texts."""
        input_text = "Hello 世界! 🌍 This is a test with émojis and àccénts."
        output_text = "Bonjour le monde! 🌍 Ceci est un test avec des émojis et des accents."
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
    
    def test_json_texts(self):
        """Test with JSON string texts."""
        import json
        input_data = {"key": "value", "number": 123, "array": [1, 2, 3]}
        output_data = {"key": "value", "number": 123, "array": [1, 2, 3], "extra": "field"}
        
        input_text = json.dumps(input_data)
        output_text = json.dumps(output_data)
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
    
    def test_html_texts(self):
        """Test with HTML texts."""
        input_text = "<html><body><h1>Title</h1><p>Content</p></body></html>"
        output_text = "<html><body><h1>Title</h1><p>Content</p><p>More content</p></body></html>"
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
    
    def test_sql_texts(self):
        """Test with SQL texts."""
        input_text = "SELECT * FROM users WHERE id = 1;"
        output_text = "SELECT * FROM users WHERE id = 1 AND active = true;"
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
    
    def test_malicious_texts(self):
        """Test with potentially malicious texts."""
        input_text = "<script>alert('xss')</script>"
        output_text = "<script>alert('xss')</script><p>Content</p>"
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
    
    def test_numeric_texts(self):
        """Test with numeric texts."""
        input_text = "123456789"
        output_text = "1234567890"
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "overall_score" in result
    
    def test_mixed_content_texts(self):
        """Test with mixed content texts."""
        input_text = "Hello 123 world! @#$%^&*()"
        output_text = "Hello 123 world! @#$%^&*() and more content."
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "overall_score" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
