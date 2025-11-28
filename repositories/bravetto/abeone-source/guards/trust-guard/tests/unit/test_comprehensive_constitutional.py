"""
Comprehensive Unit Tests for Trust Guard Constitutional Prompting System

Tests constitutional prompting with edge cases, error scenarios, and mitigation strategies.
"""

import pytest
import time
from unittest.mock import Mock, patch
from typing import Dict, Any, List

from trustguard.constitutional import ConstitutionalPrompting, _safe_text_input


class TestSafeTextInputConstitutional:
    """Test the safe text input helper function in constitutional module."""
    
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


class TestConstitutionalPrompting:
    """Test the ConstitutionalPrompting class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.constitutional = ConstitutionalPrompting()
    
    def test_initialization(self):
        """Test constitutional prompting initialization."""
        assert hasattr(self.constitutional, 'constitutional_guidelines')
        assert isinstance(self.constitutional.constitutional_guidelines, dict)
        
        # Check that all expected patterns are present
        expected_patterns = [
            "hallucination", "drift", "bias", "deception",
            "security_theater", "duplication", "stub_syndrome"
        ]
        
        for pattern in expected_patterns:
            assert pattern in self.constitutional.constitutional_guidelines
            assert isinstance(self.constitutional.constitutional_guidelines[pattern], list)
            assert len(self.constitutional.constitutional_guidelines[pattern]) > 0
    
    def test_is_healthy(self):
        """Test health check."""
        assert self.constitutional.is_healthy() is True
    
    def test_apply_mitigation_normal(self):
        """Test mitigation application with normal inputs."""
        text = "This is definitely correct without any doubt."
        patterns = ["hallucination"]
        risk_level = "medium"
        
        result = self.constitutional.apply_mitigation(text, patterns, risk_level)
        
        assert isinstance(result, dict)
        assert "original_text" in result
        assert "mitigated_text" in result
        assert "applied_techniques" in result
        assert "confidence_improvement" in result
        assert "risk_reduction" in result
        
        assert result["original_text"] == text
        assert isinstance(result["mitigated_text"], str)
        assert isinstance(result["applied_techniques"], list)
        assert isinstance(result["confidence_improvement"], float)
        assert isinstance(result["risk_reduction"], float)
        
        # Check that mitigation was applied
        assert result["mitigated_text"] != text
        assert len(result["applied_techniques"]) > 0
    
    def test_apply_mitigation_none_input(self):
        """Test mitigation application with None input."""
        result = self.constitutional.apply_mitigation(None, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "original_text" in result
        assert "mitigated_text" in result
        assert result["original_text"] == ""
        assert isinstance(result["mitigated_text"], str)
    
    def test_apply_mitigation_integer_input(self):
        """Test mitigation application with integer input."""
        result = self.constitutional.apply_mitigation(123, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "original_text" in result
        assert "mitigated_text" in result
        assert result["original_text"] == "123"
    
    def test_apply_mitigation_empty_patterns(self):
        """Test mitigation application with empty patterns list."""
        text = "This is some text."
        result = self.constitutional.apply_mitigation(text, [], "medium")
        
        assert isinstance(result, dict)
        assert result["original_text"] == text
        assert result["mitigated_text"] == text  # Should be unchanged
        assert len(result["applied_techniques"]) == 0
    
    def test_apply_mitigation_invalid_patterns(self):
        """Test mitigation application with invalid patterns."""
        text = "This is some text."
        result = self.constitutional.apply_mitigation(text, ["invalid_pattern"], "medium")
        
        assert isinstance(result, dict)
        assert result["original_text"] == text
        assert result["mitigated_text"] == text  # Should be unchanged
        assert len(result["applied_techniques"]) == 0
    
    def test_apply_mitigation_multiple_patterns(self):
        """Test mitigation application with multiple patterns."""
        text = "This is definitely correct and I absolutely guarantee it."
        patterns = ["hallucination", "deception"]
        result = self.constitutional.apply_mitigation(text, patterns, "high")
        
        assert isinstance(result, dict)
        assert result["original_text"] == text
        assert result["mitigated_text"] != text  # Should be modified
        assert len(result["applied_techniques"]) > 0
    
    def test_apply_mitigation_different_risk_levels(self):
        """Test mitigation application with different risk levels."""
        text = "This is definitely correct."
        patterns = ["hallucination"]
        
        for risk_level in ["low", "medium", "high"]:
            result = self.constitutional.apply_mitigation(text, patterns, risk_level)
            
            assert isinstance(result, dict)
            assert "original_text" in result
            assert "mitigated_text" in result
            assert "applied_techniques" in result
    
    def test_generate_constitutional_prompts_normal(self):
        """Test constitutional prompt generation with normal inputs."""
        patterns = ["hallucination", "bias"]
        severity = "medium"
        
        result = self.constitutional.generate_constitutional_prompts(patterns, severity)
        
        assert isinstance(result, list)
        assert len(result) > 0
        
        for prompt in result:
            assert isinstance(prompt, str)
            assert len(prompt) > 0
    
    def test_generate_constitutional_prompts_none_patterns(self):
        """Test constitutional prompt generation with None patterns."""
        result = self.constitutional.generate_constitutional_prompts(None, "medium")
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_generate_constitutional_prompts_empty_patterns(self):
        """Test constitutional prompt generation with empty patterns."""
        result = self.constitutional.generate_constitutional_prompts([], "medium")
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_generate_constitutional_prompts_invalid_patterns(self):
        """Test constitutional prompt generation with invalid patterns."""
        result = self.constitutional.generate_constitutional_prompts(["invalid_pattern"], "medium")
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_generate_constitutional_prompts_different_severities(self):
        """Test constitutional prompt generation with different severities."""
        patterns = ["hallucination"]
        
        for severity in ["low", "medium", "high"]:
            result = self.constitutional.generate_constitutional_prompts(patterns, severity)
            
            assert isinstance(result, list)
            # Higher severity should generally produce more prompts
            if severity == "high":
                assert len(result) > 0
    
    def test_apply_constitutional_enhancements_normal(self):
        """Test constitutional enhancements application with normal text."""
        text = "This is definitely correct without any doubt."
        patterns = ["hallucination"]
        
        result = self.constitutional._apply_constitutional_enhancements(text, patterns)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should modify the text to reduce overconfidence
        assert result != text
    
    def test_apply_constitutional_enhancements_none_input(self):
        """Test constitutional enhancements application with None input."""
        result = self.constitutional._apply_constitutional_enhancements(None, ["hallucination"])
        
        assert isinstance(result, str)
        assert result == ""
    
    def test_apply_constitutional_enhancements_integer_input(self):
        """Test constitutional enhancements application with integer input."""
        result = self.constitutional._apply_constitutional_enhancements(123, ["hallucination"])
        
        assert isinstance(result, str)
        assert result == "123"
    
    def test_apply_constitutional_enhancements_empty_patterns(self):
        """Test constitutional enhancements application with empty patterns."""
        text = "This is some text."
        result = self.constitutional._apply_constitutional_enhancements(text, [])
        
        assert isinstance(result, str)
        assert result == text  # Should be unchanged
    
    def test_apply_constitutional_enhancements_bias_pattern(self):
        """Test constitutional enhancements application with bias pattern."""
        text = "Women are naturally better at cooking."
        patterns = ["bias"]
        
        result = self.constitutional._apply_constitutional_enhancements(text, patterns)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should modify the text to reduce bias
    
    def test_apply_constitutional_enhancements_deception_pattern(self):
        """Test constitutional enhancements application with deception pattern."""
        text = "To be fair, technically speaking, this is basically correct."
        patterns = ["deception"]
        
        result = self.constitutional._apply_constitutional_enhancements(text, patterns)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should modify the text to reduce equivocation
    
    def test_apply_constitutional_enhancements_security_theater_pattern(self):
        """Test constitutional enhancements application with security theater pattern."""
        text = "We have 100% secure military-grade protection."
        patterns = ["security_theater"]
        
        result = self.constitutional._apply_constitutional_enhancements(text, patterns)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should modify the text to reduce false security claims
    
    def test_apply_constitutional_enhancements_duplication_pattern(self):
        """Test constitutional enhancements application with duplication pattern."""
        text = "This is important. This is important. This is important."
        patterns = ["duplication"]
        
        result = self.constitutional._apply_constitutional_enhancements(text, patterns)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should modify the text to reduce repetition
    
    def test_apply_constitutional_enhancements_stub_syndrome_pattern(self):
        """Test constitutional enhancements application with stub syndrome pattern."""
        text = "I don't know."
        patterns = ["stub_syndrome"]
        
        result = self.constitutional._apply_constitutional_enhancements(text, patterns)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should modify the text to be more comprehensive
    
    def test_performance_large_text(self):
        """Test performance with large text."""
        text = "This is a test sentence. " * 1000
        
        start_time = time.time()
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
        assert processing_time < 5.0  # Should complete within 5 seconds
    
    def test_concurrent_mitigation(self):
        """Test concurrent mitigation calls."""
        import threading
        import queue
        
        results = queue.Queue()
        errors = queue.Queue()
        
        def mitigation_worker(text_id):
            try:
                text = f"This is test text number {text_id}."
                result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
                results.put((text_id, result))
            except Exception as e:
                errors.put((text_id, e))
        
        # Start multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=mitigation_worker, args=(i,))
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
            assert "mitigated_text" in result


class TestEdgeCasesConstitutional:
    """Test edge cases and error scenarios for constitutional prompting."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.constitutional = ConstitutionalPrompting()
    
    def test_very_long_text(self):
        """Test with very long text (1MB)."""
        text = "A" * 1000000
        
        start_time = time.time()
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
        assert processing_time < 10.0  # Should complete within 10 seconds
    
    def test_special_characters_only(self):
        """Test with only special characters."""
        text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
    
    def test_unicode_text(self):
        """Test with unicode text."""
        text = "Hello !  This is a test with émojis and àccénts."
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
    
    def test_json_text(self):
        """Test with JSON string text."""
        import json
        json_data = {"key": "value", "number": 123, "array": [1, 2, 3]}
        text = json.dumps(json_data)
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
    
    def test_html_text(self):
        """Test with HTML text."""
        text = "<html><body><h1>Title</h1><p>Content</p></body></html>"
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
    
    def test_sql_text(self):
        """Test with SQL text."""
        text = "SELECT * FROM users WHERE id = 1; DROP TABLE users;"
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
    
    def test_malicious_text(self):
        """Test with potentially malicious text."""
        text = "<script>alert('xss')</script>"
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
    
    def test_numeric_text(self):
        """Test with numeric text."""
        text = "123456789"
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
    
    def test_mixed_content_text(self):
        """Test with mixed content text."""
        text = "Hello 123 world! @#$%^&*()"
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "medium")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
    
    def test_all_patterns_mitigation(self):
        """Test mitigation with all available patterns."""
        text = "This is definitely correct and I absolutely guarantee it without any doubt."
        patterns = [
            "hallucination", "drift", "bias", "deception",
            "security_theater", "duplication", "stub_syndrome"
        ]
        
        result = self.constitutional.apply_mitigation(text, patterns, "high")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
        assert len(result["applied_techniques"]) > 0
    
    def test_invalid_risk_level(self):
        """Test mitigation with invalid risk level."""
        text = "This is some text."
        result = self.constitutional.apply_mitigation(text, ["hallucination"], "invalid")
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
        # Should handle invalid risk level gracefully
    
    def test_none_risk_level(self):
        """Test mitigation with None risk level."""
        text = "This is some text."
        result = self.constitutional.apply_mitigation(text, ["hallucination"], None)
        
        assert isinstance(result, dict)
        assert "mitigated_text" in result
        # Should handle None risk level gracefully


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
