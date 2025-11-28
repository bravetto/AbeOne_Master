"""
🌊💎✨ ContextGuard Integration Tests ✨💎🌊

Tests for the simplified pure enhancement layer with persistent memory.
Zero-failure validation tests.
"""

import pytest
from typing import Dict, Any

from app.core.contextguard_integration import (
    ContextGuardIntegration,
    enhance_guard_with_context,
    store_guard_context,
    get_contextguard_integration,
    PersistentContextMemory
)


@pytest.fixture
def integration():
    """Create ContextGuard integration instance."""
    return ContextGuardIntegration()


@pytest.fixture
def fresh_integration():
    """Create fresh integration instance with cleared memory."""
    integration = ContextGuardIntegration()
    integration.memory._memory.clear()
    return integration


def test_enhance_with_context_no_memory(integration):
    """Test enhancement when no context exists."""
    payload = {"text": "test code", "operation": "validate"}
    enhanced = integration.enhance_with_context(
        guard_name="trustguard",
        payload=payload,
        session_id="session-123"
    )
    
    # Should always enhance (even with no context)
    assert "_context" in enhanced
    assert enhanced["_context"]["awareness"] is False  # No context yet
    assert enhanced["_context"]["previous_count"] == 0
    assert enhanced["text"] == "test code"  # Original payload preserved


def test_enhance_with_context_after_storage(fresh_integration):
    """Test enhancement after storing context."""
    # Store context first
    payload1 = {"text": "first code", "operation": "validate"}
    result1 = {"success": True, "score": 0.9}
    fresh_integration.store_context(
        guard_name="trustguard",
        payload=payload1,
        result=result1,
        session_id="session-123"
    )
    
    # Now enhance with context
    payload2 = {"text": "second code", "operation": "detect"}
    enhanced = fresh_integration.enhance_with_context(
        guard_name="trustguard",
        payload=payload2,
        session_id="session-123"
    )
    
    # Should have context awareness
    assert "_context" in enhanced
    assert enhanced["_context"]["awareness"] is True
    assert enhanced["_context"]["previous_count"] == 1
    assert "context" in enhanced
    assert "previous_context" in enhanced["context"] or "pattern_history" in enhanced["context"]


def test_enhance_with_context_graceful_degradation(integration):
    """Test graceful degradation - always returns enhanced payload."""
    # Test with various failure scenarios
    payload = {"text": "test code"}
    
    # No session/user ID
    enhanced1 = integration.enhance_with_context(
        guard_name="biasguard",
        payload=payload
    )
    assert enhanced1 == payload or "_context" in enhanced1
    
    # Empty payload
    enhanced2 = integration.enhance_with_context(
        guard_name="securityguard",
        payload={}
    )
    assert isinstance(enhanced2, dict)
    assert "_context" in enhanced2


def test_guard_specific_enhancement_trustguard(fresh_integration):
    """Test TrustGuard-specific enhancement."""
    # Store context first
    fresh_integration.store_context(
        guard_name="trustguard",
        payload={"text": "previous code"},
        result={"drift_score": 0.25, "validated": True},
        session_id="session-123"
    )
    
    payload = {"text": "test code", "validation_type": "security"}
    enhanced = fresh_integration.enhance_with_context(
        guard_name="trustguard",
        payload=payload,
        session_id="session-123"
    )
    
    # Verify TrustGuard-specific enhancement
    assert "context" in enhanced
    assert "previous_context" in enhanced["context"] or "pattern_history" in enhanced["context"]
    assert enhanced["_context"]["guard"] == "trustguard"


def test_guard_specific_enhancement_biasguard(fresh_integration):
    """Test BiasGuard-specific enhancement."""
    # Store context first
    fresh_integration.store_context(
        guard_name="biasguard",
        payload={"text": "previous code"},
        result={"bias_detected": False, "score": 0.1},
        session_id="session-123"
    )
    
    payload = {"text": "test code", "operation": "detect"}
    enhanced = fresh_integration.enhance_with_context(
        guard_name="biasguard",
        payload=payload,
        session_id="session-123"
    )
    
    # Verify BiasGuard-specific enhancement
    assert "context" in enhanced
    assert "semantic_context" in enhanced["context"] or "bias_patterns" in enhanced["context"]
    assert enhanced["_context"]["guard"] == "biasguard"


def test_guard_specific_enhancement_securityguard(fresh_integration):
    """Test SecurityGuard-specific enhancement."""
    # Store context first
    fresh_integration.store_context(
        guard_name="securityguard",
        payload={"text": "previous code"},
        result={"vulnerabilities": [], "secure": True},
        session_id="session-123"
    )
    
    payload = {"text": "test code"}
    enhanced = fresh_integration.enhance_with_context(
        guard_name="securityguard",
        payload=payload,
        session_id="session-123"
    )
    
    # Verify SecurityGuard-specific enhancement
    assert "context" in enhanced
    assert "historical_patterns" in enhanced["context"] or "security_history" in enhanced["context"]
    assert enhanced["_context"]["guard"] == "securityguard"


def test_guard_specific_enhancement_tokenguard(fresh_integration):
    """Test TokenGuard-specific enhancement."""
    # Store context first
    fresh_integration.store_context(
        guard_name="tokenguard",
        payload={"text": "previous code"},
        result={"tokens": 100, "optimized": True},
        session_id="session-123"
    )
    
    payload = {"text": "test code"}
    enhanced = fresh_integration.enhance_with_context(
        guard_name="tokenguard",
        payload=payload,
        session_id="session-123"
    )
    
    # Verify TokenGuard-specific enhancement
    assert "context" in enhanced
    assert "usage_patterns" in enhanced["context"]
    assert enhanced["_context"]["guard"] == "tokenguard"


def test_guard_specific_enhancement_healthguard(fresh_integration):
    """Test HealthGuard-specific enhancement."""
    # Store context first
    fresh_integration.store_context(
        guard_name="healthguard",
        payload={"text": "previous code"},
        result={"health_score": 0.95, "healthy": True},
        session_id="session-123"
    )
    
    payload = {"text": "test code"}
    enhanced = fresh_integration.enhance_with_context(
        guard_name="healthguard",
        payload=payload,
        session_id="session-123"
    )
    
    # Verify HealthGuard-specific enhancement
    assert "context" in enhanced
    assert "health_history" in enhanced["context"] or "health_patterns" in enhanced["context"]
    assert enhanced["_context"]["guard"] == "healthguard"


def test_store_context_success(fresh_integration):
    """Test successful context storage."""
    payload = {"text": "test code", "operation": "validate"}
    result = {"bias_detected": False, "score": 0.1}
    
    # Store context
    fresh_integration.store_context(
        guard_name="biasguard",
        payload=payload,
        result=result,
        session_id="session-123"
    )
    
    # Verify storage by checking memory
    context = fresh_integration.memory.get_context("session-123")
    assert context["has_context"] is True
    assert context["previous_count"] == 1
    assert context["latest_content"] == "test code"
    assert context["latest_guard"] == "biasguard"


def test_store_context_empty_content(fresh_integration):
    """Test storage with empty content (should skip)."""
    payload = {}  # No content
    result = {"result": "success"}
    
    # Store context (should skip silently)
    fresh_integration.store_context(
        guard_name="trustguard",
        payload=payload,
        result=result,
        session_id="session-123"
    )
    
    # Should not store empty content
    context = fresh_integration.memory.get_context("session-123")
    assert context["has_context"] is False


def test_store_context_multiple_entries(fresh_integration):
    """Test storing multiple context entries."""
    # Store multiple entries
    for i in range(5):
        fresh_integration.store_context(
            guard_name="trustguard",
            payload={"text": f"code {i}"},
            result={"iteration": i},
            session_id="session-123"
        )
    
    # Verify all stored
    context = fresh_integration.memory.get_context("session-123")
    assert context["has_context"] is True
    assert context["previous_count"] == 5
    assert len(context["history"]) == 3  # Last 3 entries


def test_persistent_memory_ttl_expiration(fresh_integration):
    """Test TTL expiration of context entries."""
    from datetime import datetime, timedelta
    
    # Store entry with old timestamp
    entry = fresh_integration.memory._memory["session-123"] = [
        type('ContextEntry', (), {
            'content': 'old code',
            'guard_name': 'trustguard',
            'result': {},
            'timestamp': datetime.now() - timedelta(seconds=4000)  # Older than TTL
        })()
    ]
    
    # Get context (should trigger cleanup)
    context = fresh_integration.memory.get_context("session-123")
    
    # Should have no context after cleanup
    assert context["has_context"] is False


def test_persistent_memory_max_history(fresh_integration):
    """Test max history limit."""
    # Store more than max_history entries
    for i in range(15):  # More than default max_history (10)
        fresh_integration.store_context(
            guard_name="trustguard",
            payload={"text": f"code {i}"},
            result={"iteration": i},
            session_id="session-123"
        )
    
    # Verify only max_history entries kept
    context = fresh_integration.memory.get_context("session-123")
    assert context["previous_count"] == 10  # MAX_CONTEXT_HISTORY
    assert len(context["history"]) == 3  # Last 3 entries in history


def test_enhance_guard_with_context_function(fresh_integration):
    """Test convenience function."""
    # Use the same integration instance via singleton
    from app.core.contextguard_integration import _contextguard_integration
    import app.core.contextguard_integration as cg_module
    cg_module._contextguard_integration = fresh_integration
    
    # Store context first
    store_guard_context(
        guard_name="securityguard",
        payload={"text": "previous code"},
        result={"secure": True},
        session_id="session-123"
    )
    
    payload = {"text": "test code"}
    enhanced = enhance_guard_with_context(
        guard_name="securityguard",
        payload=payload,
        session_id="session-123"
    )
    
    assert "_context" in enhanced
    assert enhanced["_context"]["awareness"] is True


def test_store_guard_context_function(fresh_integration):
    """Test convenience function for storage."""
    # Use the same integration instance via singleton
    from app.core.contextguard_integration import _contextguard_integration
    import app.core.contextguard_integration as cg_module
    cg_module._contextguard_integration = fresh_integration
    
    payload = {"text": "test code"}
    result = {"result": "success"}
    
    store_guard_context(
        guard_name="trustguard",
        payload=payload,
        result=result,
        session_id="session-123"
    )
    
    # Verify storage using the same instance
    context = fresh_integration.memory.get_context("session-123")
    assert context["has_context"] is True


def test_get_contextguard_integration_singleton():
    """Test singleton pattern."""
    instance1 = get_contextguard_integration()
    instance2 = get_contextguard_integration()
    
    # Should be same instance
    assert instance1 is instance2


def test_zero_failure_operation_missing_fields(integration):
    """Test zero-failure with missing fields."""
    # Test with various payload shapes
    test_payloads = [
        {},  # Empty
        {"text": "code"},  # Minimal
        {"current_code": "code"},  # Alternative field
        {"content": "code"},  # Another alternative
        {"code": "code"},  # Yet another
    ]
    
    for payload in test_payloads:
        # Should never fail
        enhanced = integration.enhance_with_context(
            guard_name="trustguard",
            payload=payload,
            session_id="session-123"
        )
        assert isinstance(enhanced, dict)
        assert "_context" in enhanced


def test_zero_failure_operation_exception_handling(integration):
    """Test exception handling in storage."""
    # Force exception by corrupting memory
    integration.memory._memory = None
    
    # Should handle gracefully
    try:
        integration.store_context(
            guard_name="trustguard",
            payload={"text": "code"},
            result={},
            session_id="session-123"
        )
    except Exception:
        pytest.fail("Storage should never raise exceptions")


def test_persistent_memory_guard_patterns(fresh_integration):
    """Test guard pattern extraction."""
    # Store entries from different guards
    fresh_integration.store_context(
        guard_name="trustguard",
        payload={"text": "code1"},
        result={"result": "trust1"},
        session_id="session-123"
    )
    fresh_integration.store_context(
        guard_name="biasguard",
        payload={"text": "code2"},
        result={"result": "bias1"},
        session_id="session-123"
    )
    fresh_integration.store_context(
        guard_name="trustguard",
        payload={"text": "code3"},
        result={"result": "trust2"},
        session_id="session-123"
    )
    
    # Get context
    context = fresh_integration.memory.get_context("session-123")
    
    # Verify patterns
    assert "guard_patterns" in context
    assert "trustguard" in context["guard_patterns"]
    assert "biasguard" in context["guard_patterns"]
    assert len(context["guard_patterns"]["trustguard"]) == 2
    assert len(context["guard_patterns"]["biasguard"]) == 1


def test_enhancement_preserves_original_payload(integration):
    """Test that enhancement preserves original payload fields."""
    payload = {
        "text": "test code",
        "operation": "validate",
        "custom_field": "custom_value",
        "nested": {"key": "value"}
    }
    
    enhanced = integration.enhance_with_context(
        guard_name="trustguard",
        payload=payload,
        session_id="session-123"
    )
    
    # All original fields preserved
    assert enhanced["text"] == "test code"
    assert enhanced["operation"] == "validate"
    assert enhanced["custom_field"] == "custom_value"
    assert enhanced["nested"] == {"key": "value"}
    
    # Plus context enhancement
    assert "_context" in enhanced


def test_context_key_precedence(fresh_integration):
    """Test session_id vs user_id precedence."""
    # Store with session_id
    fresh_integration.store_context(
        guard_name="trustguard",
        payload={"text": "session code"},
        result={},
        session_id="session-123",
        user_id="user-456"
    )
    
    # Retrieve with session_id (should get session context)
    context1 = fresh_integration.memory.get_context("session-123")
    assert context1["has_context"] is True
    
    # Retrieve with user_id (should not get session context)
    context2 = fresh_integration.memory.get_context("user-456")
    assert context2["has_context"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
