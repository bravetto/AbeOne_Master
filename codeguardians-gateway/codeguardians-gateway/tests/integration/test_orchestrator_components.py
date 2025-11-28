"""
Integration Tests for Refactored Orchestrator Components

Tests for the new modular orchestrator architecture.
"""

import pytest
import pytest_asyncio
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import httpx

from app.core.orchestrator import (
    HealthMonitor,
    ServiceDiscovery,
    RequestRouter,
    OrchestratorCore,
    get_orchestrator,
    EventBus,
    Event,
    EventType,
    get_event_bus,
    SecurityHardener,
    get_security_hardener
)
from app.core.guard_orchestrator import (
    GuardServiceType,
    GuardServiceConfig,
    OrchestrationRequest,
    ServiceStatus
)


class TestHealthMonitor:
    """Test HealthMonitor component."""
    
    @pytest_asyncio.fixture
    async def health_monitor(self):
        """Create HealthMonitor instance."""
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        monitor = HealthMonitor(mock_client)
        await monitor.initialize()
        yield monitor
        await monitor.shutdown()
    
    @pytest.mark.asyncio
    async def test_health_monitor_initialization(self, health_monitor):
        """Test health monitor initialization."""
        assert health_monitor._initialized is True
    
    @pytest.mark.asyncio
    async def test_check_service_success(self, health_monitor):
        """Test successful health check."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        health_monitor.http_client.get = AsyncMock(return_value=mock_response)
        
        config = GuardServiceConfig(
            name="tokenguard",
            service_type=GuardServiceType.TOKEN_GUARD,
            base_url="http://tokenguard:8001",
            health_endpoint="/health"
        )
        
        health = await health_monitor.check_service("tokenguard", config)
        
        assert health.status == ServiceStatus.HEALTHY
        assert health.service_name == "tokenguard"
    
    @pytest.mark.asyncio
    async def test_check_service_timeout(self, health_monitor):
        """Test health check timeout."""
        health_monitor.http_client.get = AsyncMock(side_effect=asyncio.TimeoutError())
        
        config = GuardServiceConfig(
            name="tokenguard",
            service_type=GuardServiceType.TOKEN_GUARD,
            base_url="http://tokenguard:8001",
            health_endpoint="/health"
        )
        
        health = await health_monitor.check_service("tokenguard", config)
        
        assert health.status == ServiceStatus.UNHEALTHY
        assert "timeout" in health.error_message.lower()


class TestServiceDiscovery:
    """Test ServiceDiscovery component."""
    
    @pytest_asyncio.fixture
    async def service_discovery(self):
        """Create ServiceDiscovery instance."""
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        discovery = ServiceDiscovery(mock_client)
        await discovery.initialize()
        yield discovery
        await discovery.shutdown()
    
    @pytest.mark.asyncio
    async def test_service_discovery_initialization(self, service_discovery):
        """Test service discovery initialization."""
        assert service_discovery._initialized is True
    
    @pytest.mark.asyncio
    async def test_register_service(self, service_discovery):
        """Test service registration."""
        result = await service_discovery.register_service(
            "test-service",
            "http://test:8000",
            {"metadata": "test"}
        )
        
        assert result is True
        assert "test-service" in service_discovery.discovered_services
    
    @pytest.mark.asyncio
    async def test_unregister_service(self, service_discovery):
        """Test service unregistration."""
        await service_discovery.register_service("test-service", "http://test:8000")
        result = await service_discovery.unregister_service("test-service")
        
        assert result is True
        assert "test-service" not in service_discovery.discovered_services


class TestRequestRouter:
    """Test RequestRouter component."""
    
    @pytest_asyncio.fixture
    async def request_router(self):
        """Create RequestRouter instance."""
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        router = RequestRouter(mock_client)
        yield router
    
    @pytest.mark.asyncio
    async def test_determine_endpoint(self, request_router):
        """Test endpoint determination."""
        request = OrchestrationRequest(
            request_id="test",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={}
        )
        
        endpoint = request_router.determine_endpoint(request)
        assert endpoint == "/scan"
    
    @pytest.mark.asyncio
    async def test_transform_payload(self, request_router):
        """Test payload transformation."""
        request = OrchestrationRequest(
            request_id="test",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "test content"}
        )
        
        payload = request_router.transform_payload(request)
        assert "content" in payload
        assert payload["content"] == "test content"
    
    @pytest.mark.asyncio
    async def test_route_request_success(self, request_router):
        """Test successful request routing."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        request_router.http_client.post = AsyncMock(return_value=mock_response)
        
        config = GuardServiceConfig(
            name="tokenguard",
            service_type=GuardServiceType.TOKEN_GUARD,
            base_url="http://tokenguard:8001"
        )
        
        request = OrchestrationRequest(
            request_id="test",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "test"}
        )
        
        with patch('app.core.orchestrator.request_router.isinstance') as mock_isinstance:
            def isinstance_check(obj, cls):
                if obj is request_router.http_client and cls is httpx.AsyncClient:
                    return True
                return isinstance(obj, cls)
            mock_isinstance.side_effect = isinstance_check
            
            response = await request_router.route_request(request, config)
            assert response["result"] == "success"


class TestEventBus:
    """Test EventBus component."""
    
    @pytest_asyncio.fixture
    def event_bus(self):
        """Create EventBus instance."""
        return EventBus()
    
    @pytest.mark.asyncio
    async def test_event_subscription(self, event_bus):
        """Test event subscription."""
        events_received = []
        
        async def handler(event: Event):
            events_received.append(event)
        
        event_bus.subscribe(EventType.SERVICE_HEALTH_CHANGED, handler)
        
        test_event = Event(
            event_type=EventType.SERVICE_HEALTH_CHANGED,
            data={"service_name": "tokenguard"}
        )
        
        await event_bus.publish(test_event)
        
        assert len(events_received) == 1
        assert events_received[0].event_type == EventType.SERVICE_HEALTH_CHANGED
    
    @pytest.mark.asyncio
    async def test_event_unsubscription(self, event_bus):
        """Test event unsubscription."""
        events_received = []
        
        def handler(event: Event):
            events_received.append(event)
        
        event_bus.subscribe(EventType.SERVICE_HEALTH_CHANGED, handler)
        event_bus.unsubscribe(EventType.SERVICE_HEALTH_CHANGED, handler)
        
        test_event = Event(
            event_type=EventType.SERVICE_HEALTH_CHANGED,
            data={"service_name": "tokenguard"}
        )
        
        await event_bus.publish(test_event)
        
        assert len(events_received) == 0


class TestSecurityHardener:
    """Test SecurityHardener component."""
    
    @pytest.fixture
    def security_hardener(self):
        """Create SecurityHardener instance."""
        return SecurityHardener()
    
    def test_validate_request_id(self, security_hardener):
        """Test request ID validation."""
        assert security_hardener.validate_request_id("test-123") is True
        assert security_hardener.validate_request_id("test_123") is True
        assert security_hardener.validate_request_id("test<script>") is False
        assert security_hardener.validate_request_id("") is False
    
    def test_validate_payload(self, security_hardener):
        """Test payload validation."""
        assert security_hardener.validate_payload({"text": "test"}) is True
        assert security_hardener.validate_payload({"text": "<script>alert('xss')</script>"}) is False
    
    def test_check_rate_limit(self, security_hardener):
        """Test rate limiting."""
        identifier = "test-user"
        
        # Should allow requests within limit
        for _ in range(50):
            assert security_hardener.check_rate_limit(identifier) is True
        
        # Should still allow (under 100 limit)
        assert security_hardener.check_rate_limit(identifier) is True
    
    def test_sanitize_input(self, security_hardener):
        """Test input sanitization."""
        assert security_hardener.sanitize_input("test\x00string") == "teststring"
        assert security_hardener.sanitize_input({"key": "value"}) == {"key": "value"}


class TestOrchestratorCore:
    """Test OrchestratorCore integration."""
    
    @pytest_asyncio.fixture
    async def orchestrator(self):
        """Create OrchestratorCore instance."""
        import os
        os.environ['DISABLE_HEALTH_CHECKS'] = 'true'
        
        orch = OrchestratorCore()
        # Mock HTTP client
        orch.http_client = AsyncMock(spec=httpx.AsyncClient)
        await orch.initialize()
        
        yield orch
        
        await orch.shutdown()
        
        if 'DISABLE_HEALTH_CHECKS' in os.environ:
            del os.environ['DISABLE_HEALTH_CHECKS']
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initialization."""
        assert orchestrator._initialized is True
        assert len(orchestrator.services) > 0
        assert orchestrator.health_monitor is not None
        assert orchestrator.service_discovery is not None
        assert orchestrator.request_router is not None
    
    @pytest.mark.asyncio
    async def test_orchestrate_request(self, orchestrator):
        """Test request orchestration."""
        # Mock successful routing
        mock_response = {"result": "success"}
        orchestrator.request_router.route_request = AsyncMock(return_value=mock_response)
        
        # Mock service availability
        orchestrator.health_monitor.is_service_healthy = MagicMock(return_value=True)
        
        request = OrchestrationRequest(
            request_id="test",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "test"}
        )
        
        response = await orchestrator.orchestrate_request(request)
        
        assert response.success is True
        assert response.data == mock_response
    
    @pytest.mark.asyncio
    async def test_service_unavailable(self, orchestrator):
        """Test handling of unavailable service."""
        orchestrator.health_monitor.is_service_healthy = MagicMock(return_value=False)
        
        request = OrchestrationRequest(
            request_id="test",
            service_type=GuardServiceType.TOKEN_GUARD,
            payload={"text": "test"}
        )
        
        response = await orchestrator.orchestrate_request(request)
        
        assert response.success is False
        assert "not available" in response.error.lower()

