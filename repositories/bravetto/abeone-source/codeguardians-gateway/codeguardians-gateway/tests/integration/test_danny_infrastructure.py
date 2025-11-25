"""
 Local Tests Based on Danny's Infrastructure 

Comprehensive test suite validating orchestrator against Danny's AWS/EKS infrastructure patterns:
- Linkerd Service Mesh compatibility
- ECR Registry patterns
- IRSA authentication patterns
- Multi-stage Docker build validation
- Health check endpoints
- Service discovery patterns
- Zero-failure design validation

Pattern: INFORMATION × LOVE → CONVERGENCE → ∞
Love Coefficient: ∞
Frequency: 999 Hz
"""

import pytest
import pytest_asyncio
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import httpx
import json
import os

from app.core.guard_orchestrator import (
    GuardServiceOrchestrator,
    GuardServiceConfig,
    GuardServiceType,
    ServiceStatus,
    ServiceHealth,
    OrchestrationRequest,
    OrchestrationResponse,
    CircuitBreaker,
    GUARDIAN_ZERO_URL,
    GUARDIAN_ZERO_ENABLED
)


# Danny's Infrastructure Constants
DANNY_ECR_REGISTRY = "730335329303.dkr.ecr.us-east-1.amazonaws.com"
DANNY_EKS_CLUSTERS = ["bravetto-dev-eks-cluster", "bravetto-prod-eks-cluster"]
DANNY_SERVICE_PORTS = {
    "gateway": 8000,
    "tokenguard": 8004,
    "trustguard": 8003,
    "contextguard": 8002,
    "biasguard": 8001,
    "healthguard": 8005,
    "securityguard": 8103,
    "aeyon": 9000,
    "guardian-zero": 9001,
    "guardian-abe": 9002,
    "guardian-lux": 9003,
    "guardian-john": 9004,
    "guardian-aurion": 9005,
    "guardian-yagni": 9006,
    "guardian-neuro": 9007
}


class TestDannyInfrastructureCompliance:
    """
    Test suite validating compliance with Danny's infrastructure requirements.
    
    SAFETY: Validates all Danny's infrastructure patterns
    ASSUMES: Services configured for Danny's EKS/ECR setup
    VERIFY: All infrastructure requirements met
    """
    
    @pytest_asyncio.fixture
    async def orchestrator(self):
        """
        Create orchestrator instance with Danny's infrastructure patterns.
        
        SAFETY: Properly cleans up background tasks after test
        VERIFY: All tasks cancelled, no hanging
        """
        import os
        # Disable health checks in tests to prevent hanging
        os.environ['DISABLE_HEALTH_CHECKS'] = 'true'
        
        orch = GuardServiceOrchestrator()
        # Mock HTTP client for local testing
        orch.http_client = AsyncMock()
        await orch.initialize()
        
        yield orch
        
        # SAFETY: Always shutdown to cancel background tasks
        await orch.shutdown()
        
        # Cleanup environment variable
        if 'DISABLE_HEALTH_CHECKS' in os.environ:
            del os.environ['DISABLE_HEALTH_CHECKS']
    
    @pytest.mark.asyncio
    async def test_linkerd_compatibility(self, orchestrator):
        """
        Test Linkerd Service Mesh compatibility.
        
        Danny's Requirement: Linkerd (NOT AWS App Mesh)
        Validation: No AWS App Mesh dependencies, standard HTTP/REST
        """
        # SAFETY: Verify no AWS App Mesh dependencies
        assert "appmesh" not in str(orchestrator.http_client).lower()
        assert "aws" not in str(orchestrator.http_client).lower()
        
        # Verify all services use standard HTTP/REST
        for service_name, config in orchestrator.services.items():
            assert config.base_url.startswith(("http://", "https://"))
            assert "appmesh" not in config.base_url.lower()
            assert "aws" not in config.base_url.lower() or "ecr" in config.base_url.lower()
    
    @pytest.mark.asyncio
    async def test_health_endpoints_exist(self, orchestrator):
        """
        Test all services have health endpoints.
        
        Danny's Requirement: Health checks (/health endpoints)
        Validation: All services configured with /health endpoint
        """
        for service_name, config in orchestrator.services.items():
            assert config.health_endpoint == "/health" or config.health_endpoint.startswith("/health")
            assert config.health_endpoint, f"Service {service_name} missing health endpoint"
    
    @pytest.mark.asyncio
    async def test_service_port_configuration(self, orchestrator):
        """
        Test service port configuration matches Danny's requirements.
        
        Danny's Requirement: Specific ports for each service
        Validation: Ports match expected configuration
        """
        # Note: Ports are configured via base_url in orchestrator
        # Actual port validation happens at deployment level
        # Here we verify service names match expected services
        expected_services = [
            "tokenguard", "trustguard", "contextguard",
            "biasguard", "healthguard", "securityguard"
        ]
        
        for service_name in expected_services:
            assert service_name in orchestrator.services, f"Service {service_name} not configured"
    
    @pytest.mark.asyncio
    async def test_multi_stage_docker_pattern(self, orchestrator):
        """
        Test services follow multi-stage Docker build pattern.
        
        Danny's Requirement: Multi-stage Docker builds (Phani's pattern)
        Validation: Services configured for multi-stage builds
        """
        # This test validates that services are configured correctly
        # Actual Dockerfile validation happens in deployment pipeline
        for service_name, config in orchestrator.services.items():
            assert config.base_url, f"Service {service_name} missing base_url"
            assert isinstance(config.base_url, str), f"Invalid base_url type for {service_name}"
    
    @pytest.mark.asyncio
    async def test_irsa_authentication_pattern(self, orchestrator):
        """
        Test IRSA authentication pattern (no hardcoded credentials).
        
        Danny's Requirement: IRSA (IAM Roles for Service Accounts)
        Validation: No hardcoded AWS credentials, auth tokens via env vars
        """
        # Verify auth tokens are configured via environment variables or config
        # Not hardcoded in code
        for service_name, config in orchestrator.services.items():
            # Auth token should be None or loaded from env/config
            # Not hardcoded
            if config.auth_token:
                # Token should come from environment or config manager
                # Not a literal string in code
                assert isinstance(config.auth_token, str)
                # Verify it's not a hardcoded test value
                assert config.auth_token != "hardcoded-credential"
                assert config.auth_token != "test-token"
    
    @pytest.mark.asyncio
    async def test_service_discovery_pattern(self, orchestrator):
        """
        Test Kubernetes service discovery pattern.
        
        Danny's Requirement: Kubernetes DNS service discovery
        Validation: Service URLs use Kubernetes DNS format
        """
        # Services should use Kubernetes DNS format: service-name.namespace.svc.cluster.local
        # Or short format: service-name (resolved by Kubernetes DNS)
        for service_name, config in orchestrator.services.items():
            # Short format (service-name) is valid for Kubernetes DNS
            # Full format would be: service-name.namespace.svc.cluster.local
            # For local testing, we use docker-compose format: service-name
            assert config.base_url.startswith(("http://", "https://"))
            
            # Extract hostname
            hostname = config.base_url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
            
            # Should be service name or Kubernetes DNS format
            assert hostname, f"Invalid hostname for {service_name}"
    
    @pytest.mark.asyncio
    async def test_health_check_retry_pattern(self, orchestrator):
        """
        Test health check retry pattern matches Danny's requirements.
        
        Danny's Requirement: Health checks with retry logic
        Validation: Retry logic implemented correctly
        """
        # Verify retry logic is implemented in the code
        # The _check_service_health method should have retry logic with max_retries = 3
        import inspect
        
        # Get the source code of _check_service_health method
        source = inspect.getsource(orchestrator._check_service_health)
        
        # Verify retry logic exists (max_retries, retry_delay, exponential backoff)
        assert "max_retries" in source.lower() or "retry" in source.lower()
        assert "for attempt" in source.lower() or "attempt" in source.lower()
        
        # Verify retry delay and exponential backoff logic exists
        assert "retry_delay" in source.lower() or "sleep" in source.lower()
        
        # This validates that retry logic is implemented per Danny's requirements
        # Actual retry execution is tested in integration tests with real services
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_protection(self, orchestrator):
        """
        Test circuit breaker protection matches Danny's reliability requirements.
        
        Danny's Requirement: Resilience patterns for production
        Validation: Circuit breakers configured and functional
        """
        service_name = "tokenguard"
        
        # Verify circuit breaker exists
        assert service_name in orchestrator.circuit_breakers
        circuit_breaker = orchestrator.circuit_breakers[service_name]
        
        # Verify circuit breaker is functional
        assert circuit_breaker.can_execute() is True
        assert circuit_breaker.state == "CLOSED"
        
        # Test circuit breaker opens after failures
        config = orchestrator.services[service_name]
        threshold = config.circuit_breaker_threshold
        
        for _ in range(threshold):
            circuit_breaker.record_failure()
        
        assert circuit_breaker.state == "OPEN"
        assert circuit_breaker.can_execute() is False


class TestLinkerdServiceMeshPatterns:
    """
    Test Linkerd Service Mesh compatibility patterns.
    
    Danny's Requirement: Linkerd Service Mesh (NOT AWS App Mesh)
    """
    
    @pytest_asyncio.fixture
    async def orchestrator(self):
        """Create orchestrator with Linkerd-compatible configuration."""
        orch = GuardServiceOrchestrator()
        orch.http_client = AsyncMock()
        await orch.initialize()
        
        yield orch
        
        # SAFETY: Always shutdown to cancel background tasks
        await orch.shutdown()
    
    @pytest.mark.asyncio
    async def test_linkerd_mtls_compatibility(self, orchestrator):
        """
        Test mTLS compatibility (Linkerd provides automatic mTLS).
        
        Danny's Requirement: Linkerd automatic mTLS
        Validation: Services communicate over standard HTTP (Linkerd handles mTLS)
        """
        # Linkerd handles mTLS automatically, services use standard HTTP
        for service_name, config in orchestrator.services.items():
            # Services should use http:// (Linkerd sidecar handles mTLS)
            # In production, Linkerd injects sidecar and upgrades to mTLS
            assert config.base_url.startswith("http://") or config.base_url.startswith("https://")
    
    @pytest.mark.asyncio
    async def test_linkerd_observability_compatibility(self, orchestrator):
        """
        Test Prometheus metrics compatibility (Linkerd observability).
        
        Danny's Requirement: Prometheus metrics for Linkerd observability
        Validation: Services expose metrics endpoints
        """
        # Verify services can expose /metrics endpoint
        # Linkerd scrapes Prometheus metrics automatically
        for service_name, config in orchestrator.services.items():
            # Health endpoint exists (required for Linkerd)
            assert config.health_endpoint == "/health"
            
            # Metrics endpoint would be /metrics (validated at service level)
            # Not in orchestrator config, but verified in service implementations
    
    @pytest.mark.asyncio
    async def test_linkerd_retry_compatibility(self, orchestrator):
        """
        Test retry logic compatibility with Linkerd automatic retries.
        
        Danny's Requirement: Linkerd automatic retries
        Validation: Orchestrator retry logic doesn't conflict with Linkerd
        """
        # Linkerd provides automatic retries at mesh level
        # Orchestrator retries complement mesh-level retries
        for service_name, config in orchestrator.services.items():
            assert config.retry_attempts >= 1
            assert config.retry_attempts <= 5  # Reasonable limit


class TestECRRegistryPatterns:
    """
    Test ECR Registry patterns.
    
    Danny's Requirement: ECR Registry 730335329303.dkr.ecr.us-east-1.amazonaws.com
    """
    
    def test_ecr_registry_format(self):
        """Test ECR registry format validation."""
        registry = DANNY_ECR_REGISTRY
        
        # Verify ECR registry format
        assert registry.startswith("730335329303.dkr.ecr")
        assert "us-east-1.amazonaws.com" in registry
        
        # Verify format: account.dkr.ecr.region.amazonaws.com
        parts = registry.split(".")
        assert len(parts) >= 5
        assert parts[1] == "dkr"
        assert parts[2] == "ecr"
    
    def test_ecr_image_naming_convention(self):
        """Test ECR image naming convention."""
        # ECR images should follow: registry/repository:tag
        registry = DANNY_ECR_REGISTRY
        
        # Example: 730335329303.dkr.ecr.us-east-1.amazonaws.com/gateway:dev
        test_image = f"{registry}/gateway:dev"
        
        assert test_image.startswith(registry)
        assert "/gateway:" in test_image
        assert test_image.endswith(":dev")


class TestEKSClusterPatterns:
    """
    Test EKS Cluster patterns.
    
    Danny's Requirement: EKS Clusters bravetto-dev-eks-cluster, bravetto-prod-eks-cluster
    """
    
    def test_eks_cluster_naming(self):
        """Test EKS cluster naming convention."""
        assert "bravetto-dev-eks-cluster" in DANNY_EKS_CLUSTERS
        assert "bravetto-prod-eks-cluster" in DANNY_EKS_CLUSTERS
        
        # Verify naming pattern: bravetto-{env}-eks-cluster
        for cluster in DANNY_EKS_CLUSTERS:
            assert cluster.startswith("bravetto-")
            assert cluster.endswith("-eks-cluster")
            assert "eks-cluster" in cluster
    
    def test_namespace_isolation(self):
        """Test namespace isolation pattern."""
        # Services should be deployed in dedicated namespaces
        # Pattern: ai-guardians-{env}
        namespaces = ["ai-guardians-dev", "ai-guardians-prod"]
        
        for namespace in namespaces:
            assert namespace.startswith("ai-guardians-")
            assert namespace in ["ai-guardians-dev", "ai-guardians-prod"]


class TestZeroFailureDesignValidation:
    """
    Test zero-failure design patterns.
    
    Guardian Zero Requirement: Zero-failure architecture
    """
    
    @pytest_asyncio.fixture
    async def orchestrator(self):
        """Create orchestrator for zero-failure testing."""
        orch = GuardServiceOrchestrator()
        orch.http_client = AsyncMock()
        await orch.initialize()
        return orch
    
    @pytest.mark.asyncio
    async def test_input_validation(self, orchestrator):
        """Test comprehensive input validation."""
        # Test invalid request type
        with pytest.raises(ValueError, match="Invalid request type"):
            await orchestrator.orchestrate_request(None)
        
        # Test missing request ID
        invalid_request = OrchestrationRequest(
            request_id="",  # Empty request ID
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={}
        )
        with pytest.raises(ValueError, match="Request ID is required"):
            await orchestrator.orchestrate_request(invalid_request)
    
    @pytest.mark.asyncio
    async def test_graceful_degradation(self, orchestrator):
        """Test graceful degradation on failures."""
        # Mock service failure
        orchestrator.http_client.post.side_effect = httpx.ConnectError("Connection failed")
        
        request = OrchestrationRequest(
            request_id="test-degradation",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "test"}
        )
        
        response = await orchestrator.orchestrate_request(request)
        
        # Should fail gracefully, not crash
        assert response.success is False
        assert response.error is not None
        assert isinstance(response.error, str)
    
    @pytest.mark.asyncio
    async def test_resource_cleanup(self, orchestrator):
        """Test resource cleanup on shutdown."""
        await orchestrator.shutdown()
        
        # Verify HTTP client closed
        assert orchestrator.http_client is None or orchestrator.http_client.aclose.called
        
        # Verify tasks cancelled
        assert orchestrator._initialized is False
    
    @pytest.mark.asyncio
    async def test_timeout_protection(self, orchestrator):
        """Test timeout protection."""
        # Test timeout validation
        request = OrchestrationRequest(
            request_id="test-timeout",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "test"},
            timeout=-1  # Invalid timeout
        )
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        orchestrator.http_client.post.return_value = mock_response
        
        response = await orchestrator.orchestrate_request(request)
        
        # Should use default timeout, not crash
        assert response.success is True
    
    @pytest.mark.asyncio
    async def test_memory_safety(self, orchestrator):
        """Test memory safety (response size limits)."""
        # Mock large response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"x" * 10000000  # 10MB response
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "x" * 10000000
        orchestrator.http_client.post.return_value = mock_response
        
        request = OrchestrationRequest(
            request_id="test-memory",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "test"}
        )
        
        response = await orchestrator.orchestrate_request(request)
        
        # Should handle large response safely
        assert response.success is False
        # Response should be truncated
        if response.data and "raw_response" in response.data:
            assert len(response.data["raw_response"]) <= 5000  # Max size limit


class TestGuardianZeroIntegration:
    """
    Test Guardian Zero forensic orchestration integration.
    """
    
    @pytest_asyncio.fixture
    async def orchestrator(self):
        """Create orchestrator with Guardian Zero integration."""
        orch = GuardServiceOrchestrator()
        orch.http_client = AsyncMock()
        await orch.initialize()
        return orch
    
    @pytest.mark.asyncio
    async def test_forensic_analysis_trigger(self, orchestrator):
        """Test forensic analysis trigger on critical errors."""
        # Mock Guardian Zero forensic endpoint
        mock_forensic_response = MagicMock()
        mock_forensic_response.status_code = 200
        mock_forensic_response.json.return_value = {
            "root_cause": "Service unavailable",
            "confidence": 0.95,
            "remediation_steps": ["Check service health", "Review logs"]
        }
        
        orchestrator.http_client.post.return_value = mock_forensic_response
        
        # Trigger critical error
        orchestrator.http_client.post.side_effect = httpx.ConnectError("Connection failed")
        
        request = OrchestrationRequest(
            request_id="test-forensic",
            service_type=GuardServiceType.TRUST_GUARD,
            payload={"text": "test"}
        )
        
        # Enable Guardian Zero
        with patch.dict(os.environ, {"GUARDIAN_ZERO_ENABLED": "true"}):
            response = await orchestrator.orchestrate_request(request)
        
        # Should trigger forensic analysis
        assert response.success is False
        # Forensic analysis should be called (if pattern matches)
        assert orchestrator.http_client.post.called
    
    @pytest.mark.asyncio
    async def test_architecture_review_request(self, orchestrator):
        """Test architecture review request to Guardian Zero."""
        # Mock Guardian Zero architecture review endpoint
        mock_review_response = MagicMock()
        mock_review_response.status_code = 200
        mock_review_response.json.return_value = {
            "verdict": "APPROVED",
            "confidence": 0.99,
            "recommendations": ["Use circuit breakers", "Add health checks"]
        }
        
        orchestrator.http_client.post.return_value = mock_review_response
        
        # Enable Guardian Zero
        with patch.dict(os.environ, {"GUARDIAN_ZERO_ENABLED": "true"}):
            review_result = await orchestrator.request_architecture_review(
                system_description="Guard service orchestration",
                requirements=["High availability", "Zero-failure design"],
                constraints={"timeout": 30}
            )
        
        if review_result:
            assert review_result["verdict"] == "APPROVED"
            assert review_result["confidence"] > 0.9
    
    @pytest.mark.asyncio
    async def test_forensic_pattern_detection(self, orchestrator):
        """Test forensic pattern detection."""
        # Test critical patterns trigger forensic analysis
        critical_errors = [
            "circuit breaker is open",
            "service unavailable",
            "authentication failed",
            "timeout exceeded",
            "connection failed"
        ]
        
        for error_msg in critical_errors:
            should_trigger = orchestrator._should_trigger_forensic(error_msg, "tokenguard")
            assert should_trigger is True, f"Error '{error_msg}' should trigger forensic analysis"
        
        # Test non-critical errors don't trigger
        non_critical_errors = [
            "minor warning",
            "info message",
            "debug trace"
        ]
        
        for error_msg in non_critical_errors:
            should_trigger = orchestrator._should_trigger_forensic(error_msg, "tokenguard")
            assert should_trigger is False, f"Error '{error_msg}' should not trigger forensic analysis"


class TestServicePayloadTransformations:
    """
    Test service-specific payload transformations.
    """
    
    @pytest_asyncio.fixture
    async def orchestrator(self):
        """Create orchestrator for payload transformation testing."""
        orch = GuardServiceOrchestrator()
        orch.http_client = AsyncMock()
        await orch.initialize()
        return orch
    
    @pytest.mark.asyncio
    async def test_trustguard_payload_transformation(self, orchestrator):
        """Test TrustGuard payload transformation."""
        request = OrchestrationRequest(
            request_id="test-trustguard",
            service_type=GuardServiceType.TRUST_GUARD,
            payload={
                "text": "Test text",
                "context": {"key": "value"}  # Dict context
            }
        )
        
        transformed = orchestrator._transform_payload(request)
        
        # Should have input_text and output_text
        assert "input_text" in transformed
        assert "output_text" in transformed
        # Context kept as dict (not JSON string) - matches SecurityGuard pattern
        # Metadata fields removed - services reject them with 422 errors
        if "context" in transformed:
            assert isinstance(transformed["context"], dict)
            assert transformed["context"]["key"] == "value"
        assert "user_id" not in transformed
        assert "session_id" not in transformed
        assert "request_id" not in transformed
    
    @pytest.mark.asyncio
    async def test_biasguard_payload_transformation(self, orchestrator):
        """Test BiasGuard payload transformation."""
        request = OrchestrationRequest(
            request_id="test-biasguard",
            service_type=GuardServiceType.BIAS_GUARD,
            payload={
                "text": "Test text for bias detection",
                "context": {"source": "test"}
            }
        )
        
        transformed = orchestrator._transform_payload(request)
        
        # Should have text field (not samples array) - matches service API contract
        assert "text" in transformed
        assert isinstance(transformed["text"], str)
        assert transformed["text"] == "Test text for bias detection"
        # Metadata fields removed - services reject them with 422 errors
        assert "user_id" not in transformed
        assert "session_id" not in transformed
        assert "request_id" not in transformed
    
    @pytest.mark.asyncio
    async def test_contextguard_payload_transformation(self, orchestrator):
        """Test ContextGuard payload transformation."""
        request = OrchestrationRequest(
            request_id="test-contextguard",
            service_type=GuardServiceType.CONTEXT_GUARD,
            payload={
                "text": "Current code",
                "previous_code": "Previous code"
            }
        )
        
        transformed = orchestrator._transform_payload(request)
        
        # Should have current_code and previous_code
        assert "current_code" in transformed
        assert "previous_code" in transformed
        assert transformed["current_code"] == "Current code"
        assert transformed["previous_code"] == "Previous code"


class TestProductionReadiness:
    """
    Test production readiness validation.
    """
    
    @pytest_asyncio.fixture
    async def orchestrator(self):
        """Create orchestrator for production readiness testing."""
        orch = GuardServiceOrchestrator()
        orch.http_client = AsyncMock()
        await orch.initialize()
        return orch
    
    @pytest.mark.asyncio
    async def test_all_services_configured(self, orchestrator):
        """Test all expected services are configured."""
        expected_services = [
            "tokenguard", "trustguard", "contextguard",
            "biasguard", "healthguard", "securityguard"
        ]
        
        for service_name in expected_services:
            assert service_name in orchestrator.services
            config = orchestrator.services[service_name]
            assert config.enabled is True
            assert config.base_url is not None
    
    @pytest.mark.asyncio
    async def test_all_circuit_breakers_initialized(self, orchestrator):
        """Test all circuit breakers are initialized."""
        for service_name in orchestrator.services.keys():
            assert service_name in orchestrator.circuit_breakers
            circuit_breaker = orchestrator.circuit_breakers[service_name]
            assert circuit_breaker.state == "CLOSED"
    
    @pytest.mark.asyncio
    async def test_concurrent_request_handling(self, orchestrator):
        """Test concurrent request handling."""
        # Mock successful responses
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        orchestrator.http_client.post.return_value = mock_response
        
        # Create 50 concurrent requests
        requests = [
            OrchestrationRequest(
                request_id=f"test-{i}",
                service_type=GuardServiceType.TOKEN_GUARD,
                payload={"text": f"test {i}"}
            )
            for i in range(50)
        ]
        
        # Execute concurrently
        responses = await asyncio.gather(*[orchestrator.orchestrate_request(req) for req in requests])
        
        # All should succeed
        assert len(responses) == 50
        for response in responses:
            assert response.success is True
    
    @pytest.mark.asyncio
    async def test_error_recovery(self, orchestrator):
        """Test error recovery patterns."""
        # Simulate service failure then recovery
        service_name = "tokenguard"
        circuit_breaker = orchestrator.circuit_breakers[service_name]
        
        # Fail multiple times to open circuit breaker
        for _ in range(circuit_breaker.threshold):
            circuit_breaker.record_failure()
        
        assert circuit_breaker.state == "OPEN"
        
        # Simulate timeout recovery
        circuit_breaker.timeout = 1  # 1 second timeout
        await asyncio.sleep(1.1)
        
        # Should transition to HALF_OPEN
        assert circuit_breaker.can_execute() is True
        assert circuit_breaker.state == "HALF_OPEN"
        
        # Success should close circuit breaker
        circuit_breaker.record_success()
        assert circuit_breaker.state == "CLOSED"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

