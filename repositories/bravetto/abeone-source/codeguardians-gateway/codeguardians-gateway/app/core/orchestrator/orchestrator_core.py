"""
Orchestrator Core - Simple and Elegant Integration

Main orchestrator that integrates all components with simplicity and elegance.
Production-hardened and ready for deployment.
"""

import asyncio
import logging
import os
from typing import Dict, Optional, Any
from datetime import datetime
import httpx

from app.core.guard_orchestrator import (
    GuardServiceType,
    GuardServiceConfig,
    OrchestrationRequest,
    OrchestrationResponse,
    ServiceHealth,
    ServiceStatus,
    CircuitBreaker
)
from app.core.exceptions import (
    GuardServiceError,
    ServiceUnavailableError,
    ConfigurationError
)
from app.core.orchestrator.health_monitor import HealthMonitor
from app.core.orchestrator.service_discovery import ServiceDiscovery
from app.core.orchestrator.request_router import RequestRouter
from app.core.orchestrator.event_system import (
    EventBus,
    Event,
    EventType,
    get_event_bus
)
from app.utils.logging import get_logger
from prometheus_client import Counter, Histogram, Gauge

logger = get_logger(__name__)

# Prometheus metrics
ORCHESTRATION_REQUESTS = Counter(
    'orchestrator_requests_total',
    'Total orchestration requests',
    ['service_name', 'status']
)

ORCHESTRATION_DURATION = Histogram(
    'REPLACE_ME',
    'Orchestration request duration',
    ['service_name']
)

ACTIVE_SERVICES = Gauge(
    'orchestrator_active_services',
    'Number of active services'
)


class OrchestratorCore:
    """
    Main orchestrator core - simple and elegant integration.
    
    PRODUCTION HARDENED:
    - Comprehensive metrics
    - Event-driven architecture
    - Resource limits
    - Error resilience
    - Security hardening
    """
    
    def __init__(self):
        """Initialize orchestrator core."""
        self.services: Dict[str, GuardServiceConfig] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.http_client: Optional[httpx.AsyncClient] = None
        
        # Components
        self.health_monitor: Optional[HealthMonitor] = None
        self.service_discovery: Optional[ServiceDiscovery] = None
        self.request_router: Optional[RequestRouter] = None
        self.event_bus: EventBus = get_event_bus()
        
        # State
        self._initialized = False
        self._initializing = False
        
        # Production hardening: Resource limits
        self.max_concurrent_requests = 100
        self._request_semaphore = asyncio.Semaphore(self.max_concurrent_requests)
    
    async def initialize(self):
        """Initialize orchestrator with all components."""
        if self._initialized:
            return
        
        if self._initializing:
            while self._initializing:
                await asyncio.sleep(0.1)
            return
        
        self._initializing = True
        
        try:
            logger.info("Initializing Orchestrator Core...")
            
            # Initialize HTTP client
            self.http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                limits=httpx.Limits(
                    max_keepalive_connections=20,
                    max_connections=100
                )
            )
            
            # Initialize components
            self.health_monitor = HealthMonitor(self.http_client)
            await self.health_monitor.initialize()
            
            self.service_discovery = ServiceDiscovery(self.http_client)
            await self.service_discovery.initialize()
            
            self.request_router = RequestRouter(self.http_client)
            
            # Load service configurations
            await self._load_service_configurations()
            
            # Initialize circuit breakers
            await self._initialize_circuit_breakers()
            
            # Subscribe to events
            self._subscribe_to_events()
            
            # Start monitoring and discovery
            disable_health_checks = os.getenv('DISABLE_HEALTH_CHECKS', 'false').lower() == 'true'
            if not disable_health_checks:
                await self.health_monitor.start_monitoring(self.services)
            
            await self.service_discovery.start_discovery()
            
            self._initialized = True
            ACTIVE_SERVICES.set(len(self.services))
            logger.info(f"Orchestrator Core initialized with {len(self.services)} services")
            
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}", exc_info=True)
            self._initialized = False
            raise
        finally:
            self._initializing = False
    
    def _subscribe_to_events(self):
        """Subscribe to relevant events."""
        # Subscribe to health changes
        self.event_bus.subscribe(
            EventType.SERVICE_HEALTH_CHANGED,
            self._on_health_changed
        )
        
        # Subscribe to service discovery
        self.event_bus.subscribe(
            EventType.SERVICE_DISCOVERED,
            self._on_service_discovered
        )
    
    async def _on_health_changed(self, event: Event):
        """Handle health change events."""
        service_name = event.data.get("service_name")
        status = event.data.get("status")
        logger.debug(f"Health changed for {service_name}: {status}")
    
    async def _on_service_discovered(self, event: Event):
        """Handle service discovery events."""
        service_name = event.data.get("service_name")
        logger.debug(f"Service discovered: {service_name}")
    
    async def _load_service_configurations(self):
        """Load service configurations."""
        from app.core.guard_orchestrator import GuardServiceType
        
        # Load from environment/config
        service_configs = {
            "tokenguard": {
                "base_url": os.getenv("TOKENGUARD_URL", "http://tokenguard:8001"),
                "service_type": GuardServiceType.TOKEN_GUARD,
                "health_endpoint": "/health",
                "timeout": 30,
                "priority": 1
            },
            "trustguard": {
                "base_url": os.getenv("TRUSTGUARD_URL", "http://trustguard:8002"),
                "service_type": GuardServiceType.TRUST_GUARD,
                "health_endpoint": "/health",
                "timeout": 30,
                "priority": 1
            },
            "contextguard": {
                "base_url": os.getenv("CONTEXTGUARD_URL", "http://contextguard:8003"),
                "service_type": GuardServiceType.CONTEXT_GUARD,
                "health_endpoint": "/health",
                "timeout": 30,
                "priority": 1
            },
            "biasguard": {
                "base_url": os.getenv("BIASGUARD_URL", "http://biasguard:8004"),
                "service_type": GuardServiceType.BIAS_GUARD,
                "health_endpoint": "/health",
                "timeout": 30,
                "priority": 1
            },
            "healthguard": {
                "base_url": os.getenv("HEALTHGUARD_URL", "http://healthguard:8005"),
                "service_type": GuardServiceType.HEALTH_GUARD,
                "health_endpoint": "/health",
                "timeout": 30,
                "priority": 1
            },
            "securityguard": {
                "base_url": os.getenv("SECURITYGUARD_URL", "http://securityguard:8103"),
                "service_type": GuardServiceType.SECURITY_GUARD,
                "health_endpoint": "/health",
                "timeout": 30,
                "priority": 1
            }
        }
        
        for service_name, config_data in service_configs.items():
            config = GuardServiceConfig(
                name=service_name,
                service_type=config_data["service_type"],
                base_url=config_data["base_url"],
                health_endpoint=config_data["health_endpoint"],
                timeout=config_data["timeout"],
                priority=config_data["priority"]
            )
            self.services[service_name] = config
    
    async def _initialize_circuit_breakers(self):
        """Initialize circuit breakers for all services."""
        from app.core.guard_orchestrator import CircuitBreaker
        
        for service_name in self.services.keys():
            self.circuit_breakers[service_name] = CircuitBreaker()
    
    async def orchestrate_request(self, request: OrchestrationRequest) -> OrchestrationResponse:
        """
        Orchestrate a request - simple and elegant.
        
        PRODUCTION: Resource limits, metrics, error handling, events
        """
        import time
        start_time = time.time()
        service_name = request.service_type.value
        
        # Ensure initialization
        if not self._initialized:
            await self.initialize()
        
        if not self._initialized:
            return OrchestrationResponse(
                request_id=request.request_id,
                service_type=request.service_type,
                success=False,
                error="Orchestrator initialization failed",
                processing_time=0.0,
                service_used=None
            )
        
        # Resource limit: Concurrent request limiting
        async with self._request_semaphore:
            try:
                # Check service availability
                if not self._is_service_available(service_name):
                    ORCHESTRATION_REQUESTS.labels(service_name=service_name, status="unavailable").inc()
                    return OrchestrationResponse(
                        request_id=request.request_id,
                        service_type=request.service_type,
                        success=False,
                        error=f"Service {service_name} is not available",
                        processing_time=(time.time() - start_time),
                        service_used=service_name
                    )
                
                # Check circuit breaker
                circuit_breaker = self.circuit_breakers.get(service_name)
                if circuit_breaker and not circuit_breaker.can_execute():
                    ORCHESTRATION_REQUESTS.labels(service_name=service_name, status="circuit_open").inc()
                    
                    # Publish event
                    await self.event_bus.publish(Event(
                        event_type=EventType.CIRCUIT_BREAKER_OPENED,
                        data={"service_name": service_name},
                        source="orchestrator_core"
                    ))
                    
                    return OrchestrationResponse(
                        request_id=request.request_id,
                        service_type=request.service_type,
                        success=False,
                        error=f"Circuit breaker is open for {service_name}",
                        processing_time=(time.time() - start_time),
                        service_used=service_name
                    )
                
                # Get service configuration
                config = self.services.get(service_name)
                if not config:
                    ORCHESTRATION_REQUESTS.labels(service_name=service_name, status="not_found").inc()
                    return OrchestrationResponse(
                        request_id=request.request_id,
                        service_type=request.service_type,
                        success=False,
                        error=f"Service configuration not found: {service_name}",
                        processing_time=(time.time() - start_time),
                        service_used=service_name
                    )
                
                # Route request
                try:
                    response_data = await self.request_router.route_request(request, config)
                    
                    # Record success
                    if circuit_breaker:
                        circuit_breaker.record_success()
                    
                    duration = time.time() - start_time
                    ORCHESTRATION_DURATION.labels(service_name=service_name).observe(duration)
                    ORCHESTRATION_REQUESTS.labels(service_name=service_name, status="success").inc()
                    
                    # Publish event
                    await self.event_bus.publish(Event(
                        event_type=EventType.REQUEST_ROUTED,
                        data={
                            "service_name": service_name,
                            "request_id": request.request_id,
                            "duration": duration
                        },
                        source="orchestrator_core"
                    ))
                    
                    return OrchestrationResponse(
                        request_id=request.request_id,
                        service_type=request.service_type,
                        success=True,
                        data=response_data,
                        processing_time=duration,
                        service_used=service_name
                    )
                
                except GuardServiceError as e:
                    # Record failure
                    if circuit_breaker:
                        circuit_breaker.record_failure()
                    
                    duration = time.time() - start_time
                    ORCHESTRATION_DURATION.labels(service_name=service_name).observe(duration)
                    ORCHESTRATION_REQUESTS.labels(service_name=service_name, status="error").inc()
                    
                    # Publish event
                    await self.event_bus.publish(Event(
                        event_type=EventType.REQUEST_FAILED,
                        data={
                            "service_name": service_name,
                            "request_id": request.request_id,
                            "error": str(e)
                        },
                        source="orchestrator_core"
                    ))
                    
                    return OrchestrationResponse(
                        request_id=request.request_id,
                        service_type=request.service_type,
                        success=False,
                        error=str(e),
                        processing_time=duration,
                        service_used=service_name
                    )
                
            except Exception as e:
                duration = time.time() - start_time
                ORCHESTRATION_DURATION.labels(service_name=service_name).observe(duration)
                ORCHESTRATION_REQUESTS.labels(service_name=service_name, status="exception").inc()
                
                logger.error(f"Orchestration error: {e}", exc_info=True)
                
                return OrchestrationResponse(
                    request_id=request.request_id,
                    service_type=request.service_type,
                    success=False,
                    error=f"Internal error: {str(e)}",
                    processing_time=duration,
                    service_used=service_name
                )
    
    def _is_service_available(self, service_name: str) -> bool:
        """Check if service is available."""
        if service_name not in self.services:
            return False
        
        config = self.services[service_name]
        if not config.enabled:
            return False
        
        # Check health status if health monitor is available
        if self.health_monitor:
            return self.health_monitor.is_service_healthy(service_name)
        
        # Optimistic default if health monitor not available
        return True
    
    async def get_service_health(self, service_name: Optional[str] = None) -> Dict[str, ServiceHealth]:
        """Get health status for services."""
        if self.health_monitor:
            return self.health_monitor.get_health_status(service_name)
        return {}
    
    async def shutdown(self):
        """Shutdown orchestrator and all components."""
        logger.info("Shutting down Orchestrator Core...")
        
        self._initialized = False
        
        # Shutdown components
        if self.health_monitor:
            await self.health_monitor.shutdown()
        
        if self.service_discovery:
            await self.service_discovery.shutdown()
        
        # Shutdown event bus
        self.event_bus.shutdown()
        
        # Close HTTP client
        if self.http_client:
            try:
                await asyncio.wait_for(self.http_client.aclose(), timeout=5.0)
            except Exception as e:
                logger.error(f"Error closing HTTP client: {e}")
            finally:
                self.http_client = None
        
        logger.info("Orchestrator Core shutdown complete")


# Global orchestrator instance
_orchestrator: Optional[OrchestratorCore] = None


def get_orchestrator() -> OrchestratorCore:
    """Get global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = OrchestratorCore()
    return _orchestrator

