#!/usr/bin/env python3
"""
Test suite for cascading error scenarios and circuit breaker recovery.

TEST: Circuit breaker prevents cascading failures, half-open recovery works
PERF: O(1) time per request, O(n) space for circuit breaker state
FAILS: if circuit breaker doesn't prevent cascades or recovery fails
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta

# SAFETY: Test circuit breaker isolation and recovery
# ASSUMES: Circuit breaker initialized with threshold=5, timeout=60
# VERIFY: Cascading failures prevented, half-open state recovers


class TestCircuitBreakerCascadingErrors:
    """Test circuit breaker prevents cascading failures."""
    
    @pytest.fixture
    def circuit_breaker(self):
        """Create circuit breaker instance."""
        from app.core.guard_orchestrator import CircuitBreaker
        return CircuitBreaker(threshold=5, timeout=60)
    
    def test_circuit_breaker_closed_initially(self, circuit_breaker):
        """TEST: Circuit breaker starts in CLOSED state"""
        # Assert
        assert circuit_breaker.state == "CLOSED", "Circuit breaker should start closed"
        assert circuit_breaker.can_execute(), "Should allow execution when closed"
    
    def test_circuit_breaker_opens_after_threshold(self, circuit_breaker):
        """TEST: Circuit breaker opens after threshold failures"""
        # Arrange
        threshold = circuit_breaker.threshold
        
        # Act - Record failures up to threshold
        for i in range(threshold):
            circuit_breaker.record_failure()
        
        # Assert
        assert circuit_breaker.state == "OPEN", "Circuit breaker should open after threshold"
        assert not circuit_breaker.can_execute(), "Should block execution when open"
    
    def test_circuit_breaker_prevents_cascading(self, circuit_breaker):
        """TEST: OPEN circuit breaker prevents cascading failures"""
        # Arrange - Open the circuit
        for _ in range(circuit_breaker.threshold):
            circuit_breaker.record_failure()
        
        # Act - Try to execute when open
        can_execute = circuit_breaker.can_execute()
        
        # Assert
        assert not can_execute, "Should prevent execution when open (prevents cascade)"
        assert circuit_breaker.state == "OPEN", "Should remain open"
    
    def test_circuit_breaker_half_open_after_timeout(self, circuit_breaker):
        """TEST: Circuit breaker moves to HALF_OPEN after timeout"""
        # Arrange - Open the circuit
        for _ in range(circuit_breaker.threshold):
            circuit_breaker.record_failure()
        
        # Simulate time passing (set last_failure_time to past)
        circuit_breaker.last_failure_time = datetime.now() - timedelta(seconds=circuit_breaker.timeout + 1)
        
        # Act - Check if can execute (should move to half-open)
        can_execute = circuit_breaker.can_execute()
        
        # Assert
        assert can_execute, "Should allow execution after timeout (half-open)"
        assert circuit_breaker.state == "HALF_OPEN", "Should be in half-open state"
    
    def test_circuit_breaker_recovery_on_success(self, circuit_breaker):
        """TEST: Circuit breaker recovers to CLOSED on success in half-open"""
        # Arrange - Move to half-open
        for _ in range(circuit_breaker.threshold):
            circuit_breaker.record_failure()
        circuit_breaker.last_failure_time = datetime.now() - timedelta(seconds=circuit_breaker.timeout + 1)
        circuit_breaker.can_execute()  # Moves to half-open
        
        # Act - Record success
        circuit_breaker.record_success()
        
        # Assert
        assert circuit_breaker.state == "CLOSED", "Should recover to closed on success"
        assert circuit_breaker.failure_count == 0, "Failure count should reset"
    
    def test_circuit_breaker_reopens_on_failure_in_half_open(self, circuit_breaker):
        """TEST: Circuit breaker reopens on failure in half-open state"""
        # Arrange - Move to half-open
        for _ in range(circuit_breaker.threshold):
            circuit_breaker.record_failure()
        circuit_breaker.last_failure_time = datetime.now() - timedelta(seconds=circuit_breaker.timeout + 1)
        circuit_breaker.can_execute()  # Moves to half-open
        
        # Act - Record failure in half-open
        circuit_breaker.record_failure()
        
        # Assert
        assert circuit_breaker.state == "OPEN", "Should reopen on failure in half-open"
    
    def test_circuit_breaker_exponential_backoff_simulation(self):
        """TEST: Simulate exponential backoff behavior"""
        # Arrange
        retry_delay = 1
        max_retries = 3
        
        # Act - Simulate exponential backoff
        delays = []
        for attempt in range(max_retries):
            delays.append(retry_delay)
            retry_delay *= 2  # Exponential backoff
        
        # Assert
        assert delays == [1, 2, 4], "Should use exponential backoff"
        assert max(delays) < 30, "Backoff should be reasonable (<30s)"


class TestOrchestratorCascadingErrors:
    """Test orchestrator handles cascading errors."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance."""
        from app.core.guard_orchestrator import GuardServiceOrchestrator
        return GuardServiceOrchestrator()
    
    @pytest.mark.asyncio
    async def test_orchestrator_handles_service_unavailable(self, orchestrator):
        """TEST: Orchestrator handles ServiceUnavailableError gracefully"""
        # Arrange
        from app.core.guard_orchestrator import OrchestrationRequest, GuardServiceType
        from app.core.exceptions import ServiceUnavailableError
        
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"content": "test"}
        )
        
        # Mock service unavailable
        with patch.object(orchestrator, '_route_request', side_effect=ServiceUnavailableError("Service down")):
            # Act
            response = await orchestrator.orchestrate_request(request)
        
        # Assert
        assert not response.success, "Should indicate failure"
        assert response.error is not None, "Should have error message"
        assert response.error_code is not None, "Should have error code"
        assert response.timestamp is not None, "Should have timestamp"
    
    @pytest.mark.asyncio
    async def test_orchestrator_circuit_breaker_prevents_cascade(self, orchestrator):
        """TEST: Circuit breaker prevents cascading failures"""
        # Arrange
        from app.core.guard_orchestrator import OrchestrationRequest, GuardServiceType
        from app.core.exceptions import ServiceUnavailableError
        
        await orchestrator.initialize()
        service_name = "tokenguard"
        
        # Open circuit breaker
        if service_name in orchestrator.circuit_breakers:
            cb = orchestrator.circuit_breakers[service_name]
            for _ in range(cb.threshold):
                cb.record_failure()
        
        request = OrchestrationRequest(
            request_id="test-123",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"content": "test"}
        )
        
        # Act
        response = await orchestrator.orchestrate_request(request)
        
        # Assert
        assert not response.success, "Should fail fast when circuit open"
        assert "circuit breaker" in response.error.lower() or "unavailable" in response.error.lower(), \
            "Should indicate circuit breaker or unavailable"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

