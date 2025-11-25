"""
Unit tests for Payload Transformation
Tests the _transform_payload method for all guard service types
"""

import pytest
from app.core.guard_orchestrator import (
    GuardServiceOrchestrator,
    GuardServiceType,
    OrchestrationRequest
)


class TestPayloadTransformation:
    """Test payload transformation for different service types"""

    def setup_method(self):
        """Setup test orchestrator"""
        self.orchestrator = GuardServiceOrchestrator()

    # TokenGuard Tests
    def test_tokenguard_basic_text_payload(self):
        """Test TokenGuard with basic text payload"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "Hello world"}
        )

        result = self.orchestrator._transform_payload(request)

        assert result["content"] == "Hello world"
        assert result["confidence"] == 0.7
        assert "logprobs_stream" in result or result.get("logprobs_stream") is None
        # Metadata should be preserved
        assert result.get("request_id") == "test-123"

    def test_tokenguard_with_user_id(self):
        """Test TokenGuard with user_id"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "Test"},
            user_id="user-123"
        )

        result = self.orchestrator._transform_payload(request)

        # TokenGuard now includes user_id in transformed payload (metadata preservation)
        assert result["content"] == "Test"
        assert result["confidence"] == 0.7
        assert result["user_id"] == "user-123"
        assert result["request_id"] == "test-123"

    def test_tokenguard_with_explicit_content(self):
        """Test TokenGuard with explicit content field"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={
                "content": "Direct content",
                "confidence": 0.9
            }
        )

        result = self.orchestrator._transform_payload(request)

        assert result["content"] == "Direct content"
        assert result["confidence"] == 0.9
        assert result["request_id"] == "test-123"

    def test_tokenguard_with_confidence(self):
        """Test TokenGuard with custom confidence"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={
                "text": "Test",
                "confidence": 0.95,
                "logprobs_stream": "stream_data"
            }
        )

        result = self.orchestrator._transform_payload(request)

        assert result["content"] == "Test"
        assert result["confidence"] == 0.95
        assert result["logprobs_stream"] == "stream_data"
        assert result["request_id"] == "test-123"

    # TrustGuard Tests
    def test_trustguard_basic_payload(self):
        """Test TrustGuard with basic payload"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TRUST_GUARD,
            payload={"text": "Validation content"}
        )

        result = self.orchestrator._transform_payload(request)

        # New format: validation_type and content (not input_text/output_text)
        assert result["validation_type"] == "general"  # Default value
        assert result["content"] == "Validation content"
        assert result.get("context") is None
        # Metadata fields removed - services reject them with 422 errors
        assert "user_id" not in result
        assert "session_id" not in result
        assert "request_id" not in result

    def test_trustguard_with_context_and_metadata(self):
        """Test TrustGuard with context and metadata"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TRUST_GUARD,
            payload={
                "content": "Security check",
                "context": {"source": "api"},
                "metadata": {"level": "comprehensive"}
            }
        )

        result = self.orchestrator._transform_payload(request)

        # New format: validation_type and content (not input_text/output_text)
        assert result["validation_type"] == "general"  # Default value
        assert result["content"] == "Security check"
        # Context kept as dict (not JSON string) - matches SecurityGuard pattern
        assert isinstance(result["context"], dict)
        assert result["context"]["source"] == "api"
        # Metadata fields removed - services reject them with 422 errors
        assert "user_id" not in result
        assert "session_id" not in result
        assert "request_id" not in result

    def test_trustguard_text_to_content_mapping(self):
        """Test TrustGuard maps 'text' or 'content' to 'content' field"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TRUST_GUARD,
            payload={"text": "Test content"}
        )

        result = self.orchestrator._transform_payload(request)

        # New format: validation_type and content (maps from text/content/input_text)
        assert result["validation_type"] == "general"  # Default value
        assert result["content"] == "Test content"
        # Metadata fields removed - services reject them with 422 errors
        assert "user_id" not in result
        assert "session_id" not in result
        assert "request_id" not in result

    # ContextGuard Tests
    def test_contextguard_basic_payload(self):
        """Test ContextGuard with basic payload"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.CONTEXT_GUARD,
            payload={"text": "some code"}
        )

        result = self.orchestrator._transform_payload(request)

        assert result["current_code"] == "some code"
        assert result["previous_code"] == ""

    def test_contextguard_default_operation(self):
        """Test ContextGuard with default operation (empty previous_code)"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.CONTEXT_GUARD,
            payload={"content": "current code"}
        )

        result = self.orchestrator._transform_payload(request)

        assert result["current_code"] == "current code"
        assert result["previous_code"] == ""

    def test_contextguard_operation_mapping(self):
        """Test ContextGuard with previous_code"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.CONTEXT_GUARD,
            payload={
                "text": "new code",
                "previous_code": "old code"
            }
        )

        result = self.orchestrator._transform_payload(request)

        assert result["current_code"] == "new code"
        assert result["previous_code"] == "old code"

    def test_contextguard_with_max_items(self):
        """Test ContextGuard with previous_content field"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.CONTEXT_GUARD,
            payload={
                "text": "current code",
                "previous_content": "old code content"
            }
        )

        result = self.orchestrator._transform_payload(request)

        assert result["current_code"] == "current code"
        assert result["previous_code"] == "old code content"

    # BiasGuard Tests
    def test_biasguard_basic_payload(self):
        """Test BiasGuard with basic payload"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.BIAS_GUARD,
            payload={"text": "Test text"}
        )

        result = self.orchestrator._transform_payload(request)

        # BiasGuard expects text field (not samples array) - matches service API contract
        assert "text" in result
        assert isinstance(result["text"], str)
        assert result["text"] == "Test text"
        # Metadata fields removed - services reject them with 422 errors
        assert "user_id" not in result
        assert "session_id" not in result
        assert "request_id" not in result

    def test_biasguard_default_operation(self):
        """Test BiasGuard with content field"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.BIAS_GUARD,
            payload={"content": "test content"}
        )

        result = self.orchestrator._transform_payload(request)

        # BiasGuard expects text field (content maps to text)
        assert "text" in result
        assert result["text"] == "test content"
        # Metadata fields removed - services reject them with 422 errors
        assert "user_id" not in result
        assert "session_id" not in result
        assert "request_id" not in result

    def test_biasguard_with_context(self):
        """Test BiasGuard with context"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.BIAS_GUARD,
            payload={
                "text": "Test content",
                "context": {"source": "test"}
            }
        )

        result = self.orchestrator._transform_payload(request)

        # BiasGuard expects text field with optional context
        assert "text" in result
        assert result["text"] == "Test content"
        assert "context" in result
        assert result["context"]["source"] == "test"
        # Metadata fields removed - services reject them with 422 errors
        assert "user_id" not in result
        assert "session_id" not in result
        assert "request_id" not in result

    # HealthGuard Tests
    def test_healthguard_basic_payload(self):
        """Test HealthGuard with basic payload"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.HEALTH_GUARD,
            payload={"text": "Test content"}
        )

        result = self.orchestrator._transform_payload(request)

        assert "samples" in result
        assert len(result["samples"]) == 1
        assert result["samples"][0]["content"] == "Test content"
        assert "id" in result["samples"][0]
        assert "metadata" in result["samples"][0]

    def test_healthguard_with_metadata(self):
        """Test HealthGuard with custom metadata"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.HEALTH_GUARD,
            payload={
                "text": "Test",
                "confidence": 0.9,
                "metrics": {"test": "value"}
            }
        )

        result = self.orchestrator._transform_payload(request)

        assert result["samples"][0]["metadata"]["confidence"] == 0.9
        assert result["samples"][0]["metadata"]["metrics"]["test"] == "value"

    # Edge Cases
    def test_empty_payload(self):
        """Test transformation with empty payload"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={}
        )

        result = self.orchestrator._transform_payload(request)

        assert result["content"] == ""
        assert result["confidence"] == 0.7
        assert result["request_id"] == "test-123"

    def test_missing_text_field(self):
        """Test transformation when text field is missing"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"confidence": 0.8}
        )

        result = self.orchestrator._transform_payload(request)

        assert result["content"] == ""
        assert result["confidence"] == 0.8
        assert result["request_id"] == "test-123"

    def test_user_id_preserved_in_transformed_payload(self):
        """Test that user_id is preserved in TokenGuard transformed payload"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "test"},
            user_id="request-user"
        )

        result = self.orchestrator._transform_payload(request)

        # TokenGuard transformation now preserves user_id and other metadata
        assert "user_id" in result
        assert result["user_id"] == "request-user"
        assert result["content"] == "test"
        assert result["request_id"] == "test-123"

    def test_complex_nested_data(self):
        """Test transformation with text and previous_code"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.CONTEXT_GUARD,
            payload={
                "text": "current code content",
                "previous_code": "previous version"
            }
        )

        result = self.orchestrator._transform_payload(request)

        assert result["current_code"] == "current code content"
        assert result["previous_code"] == "previous version"


class TestEndpointDetermination:
    """Test endpoint routing logic"""

    def setup_method(self):
        """Setup test orchestrator"""
        self.orchestrator = GuardServiceOrchestrator()

    def test_tokenguard_endpoint(self):
        """Test TokenGuard endpoint is /scan"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={}
        )

        endpoint = self.orchestrator._determine_endpoint(request)
        assert endpoint == "/scan"

    def test_trustguard_endpoint(self):
        """Test TrustGuard endpoint is /validate"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TRUST_GUARD,
            payload={}
        )

        endpoint = self.orchestrator._determine_endpoint(request)
        assert endpoint == "/validate"

    def test_contextguard_endpoint(self):
        """Test ContextGuard endpoint is /analyze"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.CONTEXT_GUARD,
            payload={}
        )

        endpoint = self.orchestrator._determine_endpoint(request)
        assert endpoint == "/analyze"

    def test_biasguard_endpoint(self):
        """Test BiasGuard endpoint is /process"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.BIAS_GUARD,
            payload={}
        )

        endpoint = self.orchestrator._determine_endpoint(request)
        assert endpoint == "/process"

    def test_healthguard_endpoint(self):
        """Test HealthGuard endpoint is /analyze"""
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.HEALTH_GUARD,
            payload={}
        )

        endpoint = self.orchestrator._determine_endpoint(request)
        assert endpoint == "/analyze"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
