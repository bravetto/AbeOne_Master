"""
Comprehensive Unit Tests for Trust Guard Core Components

Tests all detector classes with edge cases, error scenarios, and performance validation.
"""

import pytest
import time
import json
from unittest.mock import Mock, patch
from typing import Dict, Any, List

from trustguard.core import (
    TrustGuardDetector, HallucinationDetector, DriftDetector, BiasDetector,
    DeceptionDetector, SecurityTheaterDetector, DuplicationDetector, StubSyndromeDetector,
    _safe_text_input
)


class TestSafeTextInput:
    """Test the safe text input helper function."""
    
    def test_none_input(self):
        """Test handling of None input."""
        result = _safe_text_input(None)
        assert result == ""
        assert isinstance(result, str)
    
    def test_string_input(self):
        """Test handling of string input."""
        result = _safe_text_input("Hello world")
        assert result == "Hello world"
        assert isinstance(result, str)
    
    def test_integer_input(self):
        """Test handling of integer input."""
        result = _safe_text_input(123)
        assert result == "123"
        assert isinstance(result, str)
    
    def test_float_input(self):
        """Test handling of float input."""
        result = _safe_text_input(123.45)
        assert result == "123.45"
        assert isinstance(result, str)
    
    def test_list_input(self):
        """Test handling of list input."""
        result = _safe_text_input([1, 2, 3])
        assert result == "[1, 2, 3]"
        assert isinstance(result, str)
    
    def test_dict_input(self):
        """Test handling of dictionary input."""
        result = _safe_text_input({"key": "value"})
        assert result == "{'key': 'value'}"
        assert isinstance(result, str)
    
    def test_boolean_input(self):
        """Test handling of boolean input."""
        result = _safe_text_input(True)
        assert result == "True"
        assert isinstance(result, str)
    
    def test_empty_string(self):
        """Test handling of empty string."""
        result = _safe_text_input("")
        assert result == ""
        assert isinstance(result, str)


class TestHallucinationDetector:
    """Test hallucination detection with comprehensive scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = HallucinationDetector()
    
    def test_normal_text(self):
        """Test detection with normal, factual text."""
        text = "The sky is blue and water is wet."
        result = self.detector.detect(text)
        
        assert isinstance(result, dict)
        assert "score" in result
        assert "confidence" in result
        assert "description" in result
        assert "evidence" in result
        assert "risk_level" in result
        assert 0.0 <= result["score"] <= 1.0
        assert 0.0 <= result["confidence"] <= 1.0
    
    def test_overconfident_text(self):
        """Test detection with overconfident language."""
        text = "I absolutely guarantee that this is definitely the best solution without any doubt."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.5  # Should detect overconfidence
        assert "overconfidence" in result["description"].lower() or "overconfidence" in str(result["evidence"])
    
    def test_specific_numbers_without_context(self):
        """Test detection with specific numbers without context."""
        text = "The exact number is 42,847 and it happened on March 15th, 2023."
        result = self.detector.detect(text)
        
        # Should detect potential hallucination due to specific numbers
        assert result["score"] > 0.0
    
    def test_short_response(self):
        """Test detection with very short response."""
        text = "Yes."
        result = self.detector.detect(text)
        
        # Short responses should have some hallucination risk
        assert result["score"] > 0.0
    
    def test_none_input(self):
        """Test detection with None input."""
        result = self.detector.detect(None)
        
        assert isinstance(result, dict)
        assert result["score"] == 0.0  # Should handle gracefully
    
    def test_integer_input(self):
        """Test detection with integer input."""
        result = self.detector.detect(123)
        
        assert isinstance(result, dict)
        assert "score" in result
    
    def test_empty_string(self):
        """Test detection with empty string."""
        result = self.detector.detect("")
        
        assert isinstance(result, dict)
        assert result["score"] == 0.0
    
    def test_very_long_text(self):
        """Test detection with very long text."""
        text = "This is a very long text. " * 1000
        result = self.detector.detect(text)
        
        assert isinstance(result, dict)
        assert "score" in result
    
    def test_special_characters(self):
        """Test detection with special characters."""
        text = "Hello! @#$%^&*()_+-=[]{}|;':\",./<>?"
        result = self.detector.detect(text)
        
        assert isinstance(result, dict)
        assert "score" in result
    
    def test_unicode_text(self):
        """Test detection with unicode text."""
        text = "Hello 世界! 🌍 This is a test with émojis and àccénts."
        result = self.detector.detect(text)
        
        assert isinstance(result, dict)
        assert "score" in result


class TestDriftDetector:
    """Test drift detection with comprehensive scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = DriftDetector()
    
    def test_no_context(self):
        """Test detection without context."""
        text = "This is some text."
        result = self.detector.detect(text)
        
        assert result["score"] == 0.0
        assert "no context" in result["description"].lower()
    
    def test_consistent_topic(self):
        """Test detection with consistent topic."""
        text = "I love programming. Programming is fun. Code is beautiful."
        context = "We were discussing software development and coding practices."
        result = self.detector.detect(text, context)
        
        assert result["score"] < 0.5  # Should be low drift
    
    def test_topic_drift(self):
        """Test detection with topic drift."""
        text = "I love programming. The weather is nice today. My cat is sleeping."
        context = "We were discussing software development and coding practices."
        result = self.detector.detect(text, context)
        
        assert result["score"] > 0.3  # Should detect some drift
    
    def test_none_inputs(self):
        """Test detection with None inputs."""
        result = self.detector.detect(None, None)
        
        assert isinstance(result, dict)
        assert "score" in result
    
    def test_empty_context(self):
        """Test detection with empty context."""
        text = "This is some text."
        result = self.detector.detect(text, "")
        
        assert result["score"] == 0.0
        assert "no context" in result["description"].lower()


class TestBiasDetector:
    """Test bias detection with comprehensive scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = BiasDetector()
    
    def test_neutral_text(self):
        """Test detection with neutral text."""
        text = "The weather is nice today."
        result = self.detector.detect(text)
        
        assert isinstance(result, dict)
        assert result["score"] < 0.3  # Should be low bias
    
    def test_gender_bias(self):
        """Test detection with gender bias."""
        text = "Women are naturally better at cooking and men are better at math."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.3  # Should detect bias
        assert "gender" in result["evidence"] or "bias" in result["description"].lower()
    
    def test_racial_bias(self):
        """Test detection with racial bias."""
        text = "Certain races are inherently more intelligent than others."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.3  # Should detect bias
    
    def test_economic_bias(self):
        """Test detection with economic bias."""
        text = "Poor people are lazy and don't want to work hard."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.3  # Should detect bias
    
    def test_none_input(self):
        """Test detection with None input."""
        result = self.detector.detect(None)
        
        assert isinstance(result, dict)
        assert "score" in result
    
    def test_empty_string(self):
        """Test detection with empty string."""
        result = self.detector.detect("")
        
        assert isinstance(result, dict)
        assert result["score"] == 0.0


class TestDeceptionDetector:
    """Test deception detection with comprehensive scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = DeceptionDetector()
    
    def test_honest_text(self):
        """Test detection with honest text."""
        text = "I don't know the answer to that question."
        result = self.detector.detect(text)
        
        assert isinstance(result, dict)
        assert result["score"] < 0.3  # Should be low deception
    
    def test_equivocation(self):
        """Test detection with equivocation."""
        text = "To be fair, technically speaking, essentially this is basically correct."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.3  # Should detect equivocation
    
    def test_evasive_language(self):
        """Test detection with evasive language."""
        text = "I can't really say for sure, but maybe it could be possible."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.2  # Should detect some evasion
    
    def test_none_input(self):
        """Test detection with None input."""
        result = self.detector.detect(None)
        
        assert isinstance(result, dict)
        assert "score" in result


class TestSecurityTheaterDetector:
    """Test security theater detection with comprehensive scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = SecurityTheaterDetector()
    
    def test_normal_security_text(self):
        """Test detection with normal security text."""
        text = "We use encryption to protect your data."
        result = self.detector.detect(text)
        
        assert isinstance(result, dict)
        assert result["score"] < 0.3  # Should be low
    
    def test_security_theater_phrases(self):
        """Test detection with security theater phrases."""
        text = "We have 100% secure military-grade ironclad protection with all threats neutralized."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.5  # Should detect security theater
    
    def test_false_assurances(self):
        """Test detection with false security assurances."""
        text = "Your data is completely safe and unhackable with our advanced security measures."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.3  # Should detect false assurances
    
    def test_none_input(self):
        """Test detection with None input."""
        result = self.detector.detect(None)
        
        assert isinstance(result, dict)
        assert "score" in result


class TestDuplicationDetector:
    """Test duplication detection with comprehensive scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = DuplicationDetector()
    
    def test_unique_content(self):
        """Test detection with unique content."""
        text = "This is a unique sentence with different words and ideas."
        result = self.detector.detect(text)
        
        assert isinstance(result, dict)
        assert result["score"] < 0.3  # Should be low duplication
    
    def test_repetitive_content(self):
        """Test detection with repetitive content."""
        text = "This is important. This is important. This is important. This is important."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.5  # Should detect duplication
    
    def test_short_text(self):
        """Test detection with short text."""
        text = "Hello."
        result = self.detector.detect(text)
        
        assert result["score"] == 0.0
        assert "too short" in result["description"].lower()
    
    def test_none_input(self):
        """Test detection with None input."""
        result = self.detector.detect(None)
        
        assert isinstance(result, dict)
        assert "score" in result


class TestStubSyndromeDetector:
    """Test stub syndrome detection with comprehensive scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = StubSyndromeDetector()
    
    def test_comprehensive_response(self):
        """Test detection with comprehensive response."""
        text = "This is a comprehensive response that provides detailed information about the topic. " * 20
        result = self.detector.detect(text)
        
        assert isinstance(result, dict)
        assert result["score"] < 0.3  # Should be low stub syndrome
    
    def test_stub_response(self):
        """Test detection with stub response."""
        text = "I don't know."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.5  # Should detect stub syndrome
    
    def test_placeholder_phrases(self):
        """Test detection with placeholder phrases."""
        text = "This is a placeholder response. More information will be added later."
        result = self.detector.detect(text)
        
        assert result["score"] > 0.3  # Should detect placeholder language
    
    def test_none_input(self):
        """Test detection with None input."""
        result = self.detector.detect(None)
        
        assert isinstance(result, dict)
        assert "score" in result


class TestTrustGuardDetector:
    """Test the main TrustGuardDetector class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = TrustGuardDetector()
    
    def test_detect_all_patterns_normal_text(self):
        """Test detection with normal text."""
        text = "This is a normal response with factual information."
        result = self.detector.detect_all_patterns(text)
        
        assert isinstance(result, dict)
        assert len(result) == 7  # Should have 7 pattern results
        
        expected_patterns = [
            "hallucination", "drift", "bias", "deception", 
            "security_theater", "duplication", "stub_syndrome"
        ]
        
        for pattern in expected_patterns:
            assert pattern in result
            assert isinstance(result[pattern], dict)
            assert "score" in result[pattern]
            assert "confidence" in result[pattern]
            assert "description" in result[pattern]
            assert "evidence" in result[pattern]
            assert "risk_level" in result[pattern]
    
    def test_detect_all_patterns_none_input(self):
        """Test detection with None input."""
        result = self.detector.detect_all_patterns(None)
        
        assert isinstance(result, dict)
        assert len(result) == 7
        
        # All patterns should handle None gracefully
        for pattern_result in result.values():
            assert isinstance(pattern_result, dict)
            assert "score" in pattern_result
    
    def test_detect_all_patterns_integer_input(self):
        """Test detection with integer input."""
        result = self.detector.detect_all_patterns(123)
        
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_detect_all_patterns_with_context(self):
        """Test detection with context."""
        text = "This is a response about programming."
        context = "We were discussing software development."
        result = self.detector.detect_all_patterns(text, context)
        
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_detect_all_patterns_with_metadata(self):
        """Test detection with metadata."""
        text = "This is a response."
        metadata = {"user_id": "test", "session_id": "abc123"}
        result = self.detector.detect_all_patterns(text, metadata=metadata)
        
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_is_healthy(self):
        """Test health check."""
        assert self.detector.is_healthy() is True
    
    def test_performance_large_text(self):
        """Test performance with large text."""
        text = "This is a test sentence. " * 1000  # ~25KB of text
        
        start_time = time.time()
        result = self.detector.detect_all_patterns(text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        assert isinstance(result, dict)
        assert len(result) == 7
        assert processing_time < 5.0  # Should complete within 5 seconds
    
    def test_concurrent_detection(self):
        """Test concurrent detection calls."""
        import threading
        import queue
        
        results = queue.Queue()
        errors = queue.Queue()
        
        def detect_worker(text_id):
            try:
                text = f"This is test text number {text_id}."
                result = self.detector.detect_all_patterns(text)
                results.put((text_id, result))
            except Exception as e:
                errors.put((text_id, e))
        
        # Start multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=detect_worker, args=(i,))
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
            assert len(result) == 7


class TestEdgeCases:
    """Test edge cases and error scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = TrustGuardDetector()
    
    def test_very_long_text(self):
        """Test with very long text (1MB)."""
        text = "A" * 1000000  # 1MB of text
        
        start_time = time.time()
        result = self.detector.detect_all_patterns(text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        assert isinstance(result, dict)
        assert len(result) == 7
        assert processing_time < 10.0  # Should complete within 10 seconds
    
    def test_special_characters_only(self):
        """Test with only special characters."""
        text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = self.detector.detect_all_patterns(text)
        
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_unicode_text(self):
        """Test with unicode text."""
        text = "Hello 世界! 🌍 This is a test with émojis and àccénts. 中文测试"
        result = self.detector.detect_all_patterns(text)
        
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_json_input(self):
        """Test with JSON string input."""
        json_data = {"key": "value", "number": 123, "array": [1, 2, 3]}
        text = json.dumps(json_data)
        result = self.detector.detect_all_patterns(text)
        
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_html_input(self):
        """Test with HTML input."""
        text = "<html><body><h1>Title</h1><p>Content</p></body></html>"
        result = self.detector.detect_all_patterns(text)
        
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_sql_input(self):
        """Test with SQL input."""
        text = "SELECT * FROM users WHERE id = 1; DROP TABLE users;"
        result = self.detector.detect_all_patterns(text)
        
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_malicious_input(self):
        """Test with potentially malicious input."""
        text = "<script>alert('xss')</script>"
        result = self.detector.detect_all_patterns(text)
        
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_empty_after_sanitization(self):
        """Test with input that becomes empty after sanitization."""
        text = None
        result = self.detector.detect_all_patterns(text)
        
        assert isinstance(result, dict)
        assert len(result) == 7
        
        # All patterns should handle empty input gracefully
        for pattern_result in result.values():
            assert isinstance(pattern_result, dict)
            assert "score" in pattern_result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
