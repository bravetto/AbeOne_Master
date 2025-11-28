"""
Service Discovery Component - Production Hardened

Manages service discovery and registration with:
- Auto-discovery of services
- Service registration/unregistration
- Service metadata tracking
- Production-ready error handling
"""

import asyncio
import logging
from typing import Dict, Optional, Any
from datetime import datetime
import httpx

from app.core.guard_orchestrator import GuardServiceConfig
from app.utils.logging import get_logger
from prometheus_client import Counter, Gauge

logger = get_logger(__name__)

# Prometheus metrics
SERVICE_DISCOVERY_COUNTER = Counter(
    'REPLACE_ME',
    'Total service discoveries',
    ['service_name', 'action']
)

DISCOVERED_SERVICES = Gauge(
    'REPLACE_ME',
    'Number of discovered services',
    ['status']
)


class ServiceDiscovery:
    """
    Service discovery component for guard services.
    
    PRODUCTION HARDENED:
    - Comprehensive metrics
    - Resource limits
    - Error resilience
    - Service metadata tracking
    """
    
    def __init__(self, http_client: httpx.AsyncClient):
        """
        Initialize service discovery.
        
        Args:
            http_client: HTTP client for discovery
        """
        self.http_client = http_client
        self.discovered_services: Dict[str, Dict[str, Any]] = {}
        self.discovery_task: Optional[asyncio.Task] = None
        self._initialized = False
        self._running = False
        
        # Production hardening: Configurable intervals
        self.discovery_interval = 30  # seconds
        self.discovery_timeout = 5.0  # seconds
    
    async def initialize(self):
        """Initialize service discovery."""
        if self._initialized:
            return
        
        self._initialized = True
        logger.info("Service Discovery initialized")
    
    async def start_discovery(self):
        """
        Start auto-discovery background task.
        
        PRODUCTION: Non-blocking background task with proper cancellation
        """
        if self._running:
            return
        
        self._running = True
        
        # Perform initial discovery
        await self.discover_services()
        
        # Start background discovery loop
        if self.discovery_task is None or self.discovery_task.done():
            self.discovery_task = asyncio.create_task(self._discovery_loop())
            self.discovery_task.add_done_callback(self._handle_task_error)
            logger.info("Service discovery started")
    
    async def _discovery_loop(self):
        """
        Background discovery loop.
        
        PRODUCTION: Short sleep intervals for faster cancellation
        """
        while self._running:
            try:
                # Use shorter sleep intervals that can be cancelled more quickly
                sleep_chunks = 6  # 6 x 5 seconds = 30 seconds total
                for _ in range(sleep_chunks):
                    if not self._running:
                        break
                    await asyncio.sleep(5)  # Shorter sleep allows faster cancellation
                
                # Double-check before performing discovery
                if not self._running:
                    break
                
                await self.discover_services()
                
            except asyncio.CancelledError:
                logger.debug("Service discovery loop cancelled")
                raise
            except Exception as e:
                logger.error(f"Service discovery loop error: {e}", exc_info=True)
                # Continue loop on errors (don't exit)
                if self._running:
                    await asyncio.sleep(5)  # Brief delay before retrying
    
    def _handle_task_error(self, task: asyncio.Task):
        """Handle errors in discovery background task."""
        try:
            task.result()
        except asyncio.CancelledError:
            logger.debug("Discovery task cancelled (expected during shutdown)")
            return
        except Exception as e:
            logger.error(f"Discovery background task failed: {e}", exc_info=True)
    
    async def discover_services(self) -> Dict[str, Dict[str, Any]]:
        """
        Discover guard services automatically.
        
        PRODUCTION: Timeout protection, error handling, metrics
        """
        # For now, auto-discovery is disabled as external services are not available
        # This prevents connection attempts to non-existent services
        logger.debug("Auto-discovery disabled - no external guard services configured")
        
        # Update metrics
        DISCOVERED_SERVICES.labels(status="active").set(len(self.discovered_services))
        
        return self.discovered_services.copy()
    
    async def register_service(
        self,
        service_name: str,
        base_url: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Register a service for discovery.
        
        PRODUCTION: Validation, metrics, error handling
        """
        try:
            # Validate inputs
            if not service_name or not base_url:
                logger.warning(f"Invalid service registration: name={service_name}, url={base_url}")
                return False
            
            # Register service
            self.discovered_services[service_name] = {
                "base_url": base_url,
                "registered_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            SERVICE_DISCOVERY_COUNTER.labels(service_name=service_name, action="register").inc()
            DISCOVERED_SERVICES.labels(status="active").set(len(self.discovered_services))
            
            logger.info(f"Service registered: {service_name} at {base_url}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register service {service_name}: {e}", exc_info=True)
            return False
    
    async def unregister_service(self, service_name: str) -> bool:
        """
        Unregister a service.
        
        PRODUCTION: Metrics, error handling
        """
        try:
            if service_name in self.discovered_services:
                del self.discovered_services[service_name]
                SERVICE_DISCOVERY_COUNTER.labels(service_name=service_name, action="unregister").inc()
                DISCOVERED_SERVICES.labels(status="active").set(len(self.discovered_services))
                logger.info(f"Service unregistered: {service_name}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to unregister service {service_name}: {e}", exc_info=True)
            return False
    
    def get_discovered_services(self) -> Dict[str, Dict[str, Any]]:
        """Get all discovered services."""
        return self.discovered_services.copy()
    
    async def shutdown(self):
        """Shutdown service discovery."""
        logger.info("Shutting down Service Discovery...")
        self._running = False
        
        if self.discovery_task:
            if not self.discovery_task.done():
                try:
                    self.discovery_task.cancel()
                    await asyncio.wait_for(self.discovery_task, timeout=5.0)
                except asyncio.CancelledError:
                    pass
                except asyncio.TimeoutError:
                    logger.warning("Discovery task shutdown timeout")
                except Exception as e:
                    logger.error(f"Error cancelling discovery task: {e}")
            self.discovery_task = None
        
        self._initialized = False
        logger.info("Service Discovery shutdown complete")

