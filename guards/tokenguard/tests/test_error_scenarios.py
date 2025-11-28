from typing import Any
#!/usr/bin/env python3
"""
Comprehensive error scenario tests for TokenGuard microservice.
"""

import pytest
import sys
import os
from unittest.mock import patch
from fastapi.testclient import TestClient

# Add the project root to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tokenguard.pruning import TokenGuardPruner
from tokenguard.config import TokenGuardConfig
from main import app

# Test client
client = TestClient(app)


class TestErrorScenarios:
    """Test error handling and edge cases."""

    def test_invalid_api_key(self: Any) -> Any:
        """Test requests with invalid API key."""
        with patch("tokenguard.config.config.api_key", "test-key"):
            response = client.post(
                "/v1/prune",
                json={"text": "test", "confidence": 0.5},
                headers={"Authorization": "Bearer invalid_key"},
            )
            assert response.status_code == 401
            assert "Invalid API key" in response.json()["detail"]

    def test_missing_api_key(self: Any) -> Any:
        """Test requests without API key when required."""
        with patch("tokenguard.config.config.api_key", "test-key"):
            response = client.post("/v1/prune", json={"text": "test", "confidence": 0.5})
            assert response.status_code == 401
            assert "Authorization header required" in response.json()["detail"]

    def test_malformed_json(self: Any) -> Any:
        """Test requests with malformed JSON."""
        response = client.post(
            "/v1/prune", data="{invalid json", headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_missing_required_fields(self: Any) -> Any:
        """Test requests missing required fields."""
        # Missing text
        response = client.post("/v1/prune", json={"confidence": 0.5})
        assert response.status_code == 422

        # Missing confidence
        response = client.post("/v1/prune", json={"text": "test"})
        assert response.status_code == 422

    def test_invalid_confidence_values(self: Any) -> Any:
        """Test requests with invalid confidence values."""
        # Confidence > 1.0
        response = client.post("/v1/prune", json={"text": "test", "confidence": 1.5})
        assert response.status_code == 422

        # Confidence < 0.0
        response = client.post("/v1/prune", json={"text": "test", "confidence": -0.5})
        assert response.status_code == 422

        # Non-numeric confidence
        response = client.post("/v1/prune", json={"text": "test", "confidence": "invalid"})
        assert response.status_code == 422

    def test_invalid_text_types(self: Any) -> Any:
        """Test requests with invalid text types."""
        # None text
        response = client.post("/v1/prune", json={"text": None, "confidence": 0.5})
        assert response.status_code == 422

        # Non-string text
        response = client.post("/v1/prune", json={"text": 12345, "confidence": 0.5})
        assert response.status_code == 422

    def test_empty_text(self: Any) -> Any:
        """Test requests with empty text."""
        response = client.post("/v1/prune", json={"text": "", "confidence": 0.5})
        assert response.status_code == 400
        assert "Text field is required and cannot be empty" in response.json()["detail"]

    def test_extremely_long_text(self: Any) -> Any:
        """Test requests with extremely long text."""
        long_text = "x" * 100001  # Beyond max_response_size
        response = client.post("/v1/prune", json={"text": long_text, "confidence": 0.5})
        assert response.status_code == 400
        assert "exceeds maximum allowed length" in response.json()["detail"]

    def test_server_error_simulation(self: Any) -> Any:
        """Test server error handling."""
        with patch(
            "tokenguard.pruning.TokenGuardPruner.should_prune",
            side_effect=Exception("Simulated error"),
        ):
            response = client.post("/v1/prune", json={"text": "test", "confidence": 0.5})
            assert response.status_code == 500
            assert "Failed to analyze pruning requirements" in response.json()["detail"]

    def test_configuration_validation_errors(self: Any) -> Any:
        """Test configuration validation."""
        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            TokenGuardPruner(confidence_threshold=1.5)  # > 1.0

        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            TokenGuardPruner(confidence_threshold=-0.1)  # < 0.0

        with pytest.raises(ValueError, match="must be positive"):
            TokenGuardPruner(check_interval_tokens=0)  # Must be positive

        with pytest.raises(ValueError, match="must be positive"):
            TokenGuardPruner(length_threshold=-1)  # Must be positive

    def test_invalid_logprobs_stream(self: Any) -> Any:
        """Test pruner with invalid logprobs data."""
        pruner = TokenGuardPruner()

        # Non-list input
        confidence = pruner.analyze_token_stream_confidence("not a list")
        assert 0.0 <= confidence <= 1.0

        # List with invalid items
        invalid_stream = [{"invalid": "format"}, "not a dict", None, {"top_logprobs": "not a list"}]
        confidence = pruner.analyze_token_stream_confidence(invalid_stream)
        assert 0.0 <= confidence <= 1.0

        # Valid structure but invalid logprob values
        invalid_logprobs = [
            {
                "top_logprobs": [
                    {"logprob": float("inf")},  # Invalid value
                    {"logprob": "not a number"},  # Wrong type
                    {"no_logprob": 0.5},  # Missing logprob key
                ]
            }
        ]
        confidence = pruner.analyze_token_stream_confidence(invalid_logprobs)
        assert 0.0 <= confidence <= 1.0

    def test_pruning_edge_cases(self: Any) -> Any:
        """Test pruning with edge cases."""
        pruner = TokenGuardPruner()

        # Text shorter than target length
        short_text = "Short"
        decision = pruner.should_prune(short_text, 0.1)  # Low confidence
        assert decision["action"] == "keep"  # Too short to prune effectively

        # Invalid input types
        decision = pruner.should_prune(123, 0.5)  # Non-string text
        assert "error" in decision

        decision = pruner.should_prune("test", "invalid")  # Non-numeric confidence
        assert "error" in decision

        # Edge case: exactly at threshold
        medium_text = "x" * 400  # Half of default length_threshold
        decision = pruner.should_prune(medium_text, 0.7)  # Exactly at confidence threshold
        # Should depend on implementation details
        assert decision["action"] in ["keep", "prune"]

    def test_apply_pruning_edge_cases(self: Any) -> Any:
        """Test apply_pruning with edge cases."""
        pruner = TokenGuardPruner()

        # Invalid prune_decision
        text, was_pruned = pruner.apply_pruning("test", {"invalid": "decision"})
        assert text == "test"
        assert not was_pruned

        # Invalid text type
        text, was_pruned = pruner.apply_pruning(123, {"action": "keep"})
        assert text == 123
        assert not was_pruned

        # Target length greater than text length
        short_decision = {"action": "prune", "target_length": 1000}
        text, was_pruned = pruner.apply_pruning("short", short_decision)
        assert text == "short"
        assert not was_pruned

        # Missing target_length
        incomplete_decision = {"action": "prune"}
        text, was_pruned = pruner.apply_pruning("test text", incomplete_decision)
        assert len(text) > 0  # Should handle gracefully

    def test_concurrent_requests(self: Any) -> Any:
        """Test handling of concurrent requests."""
        import threading

        results = []

        def make_request() -> Any:
            response = client.post("/v1/prune", json={"text": "concurrent test", "confidence": 0.5})
            results.append(response.status_code)

        # Create multiple threads
        threads = [threading.Thread(target=make_request) for _ in range(10)]

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 10

    def test_memory_stress(self: Any) -> Any:
        """Test with large but valid text to check memory handling."""
        # Create a large but valid text (within limits)
        large_text = "This is a test sentence. " * 2000  # About 50,000 chars

        response = client.post("/v1/prune", json={"text": large_text, "confidence": 0.3})

        assert response.status_code == 200
        data = response.json()
        assert data["action"] == "prune"

    def test_unicode_and_special_characters(self: Any) -> Any:
        """Test handling of unicode and special characters."""
        special_texts = [
            "Hello !  Testing unicode",
            "Special chars: \n\r\t\\\"'`",
            "Emojis: ",
            "Mathematical: ∑∫∆√π∞≠≤≥",
            "Mixed: Hello\x00World\xff",  # Contains null and high byte
        ]

        for text in special_texts:
            response = client.post("/v1/prune", json={"text": text, "confidence": 0.5})
            assert response.status_code == 200
            data = response.json()
            assert "action" in data


class TestConfigurationErrorHandling:
    """Test configuration error handling."""

    def test_invalid_environment_variables(self: Any) -> Any:
        """Test handling of invalid environment variables."""
        with patch.dict(
            os.environ,
            {
                "TOKENGUARD_CONFIDENCE_THRESHOLD": "invalid",
                "TOKENGUARD_MAX_LENGTH": "not_a_number",
                "TOKENGUARD_LOG_LEVEL": "INVALID_LEVEL",
            },
        ):
            # Should handle invalid env vars gracefully
            try:
                config = TokenGuardConfig()
                # If it doesn't raise, validation should use defaults
                assert 0.0 <= config.confidence_threshold <= 1.0
            except Exception as e:
                # If it raises, should be a validation error
                assert "validation" in str(e).lower()

    def test_missing_configuration_file(self: Any) -> Any:
        """Test behavior when .env file is missing."""
        # This should work fine with defaults
        config = TokenGuardConfig()
        assert config.confidence_threshold == 0.7  # Default value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
