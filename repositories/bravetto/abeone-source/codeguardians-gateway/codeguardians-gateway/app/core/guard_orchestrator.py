"""
CodeGuardians Gateway - Guard Services Orchestrator

This module provides the core orchestration logic for managing and routing
requests to all guard services in the Code Guardians ecosystem.
"""

import asyncio
import logging
import os
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import httpx
import json
from pathlib import Path

from app.core.config import get_settings
from app.core.exceptions import (
    GuardServiceError,
    ServiceUnavailableError,
    ConfigurationError
)
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Prometheus metrics for orchestrator
try:
    from app.core.orchestrator_metrics import (
        record_orchestrator_request,
        update_circuit_breaker_state,
        update_service_health,
        update_service_availability,
        record_guardian_zero_request
    )
    METRICS_ENABLED = True
except ImportError:
    METRICS_ENABLED = False
    logger.warning("Orchestrator metrics not available (metrics module not found)")

# Guardian Zero Integration - Forensic Orchestration
GUARDIAN_ZERO_URL = os.getenv("GUARDIAN_ZERO_URL", "http://guardian-zero:9001")
GUARDIAN_ZERO_ENABLED = os.getenv("GUARDIAN_ZERO_ENABLED", "true").lower() == "true"


class GuardServiceType(Enum):
    """Enumeration of available guard service types."""
    TOKEN_GUARD = "tokenguard"
    TRUST_GUARD = "trustguard"
    CONTEXT_GUARD = "contextguard"
    BIAS_GUARD = "biasguard"
    HEALTH_GUARD = "healthguard"
    SECURITY_GUARD = "securityguard"


class ServiceStatus(Enum):
    """Service health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class GuardServiceConfig:
    """Configuration for a guard service."""
    name: str
    service_type: GuardServiceType
    base_url: str
    health_endpoint: str = "/health"
    timeout: int = 30
    retry_attempts: int = 3
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60
    enabled: bool = True
    priority: int = 1
    tags: List[str] = field(default_factory=list)
    auth_token: Optional[str] = None
    auth_header_name: str = "Authorization"
    auth_header_format: str = "Bearer {token}"  # Format string for auth header


@dataclass
class ServiceHealth:
    """Service health information."""
    service_name: str
    status: ServiceStatus
    last_check: datetime
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OrchestrationRequest:
    """Request for guard service orchestration."""
    request_id: str
    service_type: GuardServiceType
    payload: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    priority: int = 1
    timeout: Optional[int] = None
    fallback_enabled: bool = True


@dataclass
class OrchestrationResponse:
    """Response from guard service orchestration.
    
    SAFETY: Standardized error response format with error_code and timestamp
    ASSUMES: All fields properly populated
    VERIFY: error_code present on failure, timestamp always present
    """
    request_id: str
    service_type: GuardServiceType
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None  # SAFETY: Standardized error code
    timestamp: Optional[str] = None  # SAFETY: ISO format timestamp
    processing_time: Optional[float] = None
    service_used: Optional[str] = None
    fallback_used: bool = False


class CircuitBreaker:
    """
    Circuit breaker implementation for service protection.
    
    SAFETY: Prevents cascading failures, validates state transitions
    ASSUMES: Threshold and timeout are positive integers
    VERIFY: State transitions are valid, failure counts are accurate
    """
    
    def __init__(self, threshold: int = 5, timeout: int = 60):
        # SAFETY: Validate constructor parameters
        if not isinstance(threshold, int) or threshold <= 0:
            raise ValueError(f"Circuit breaker threshold must be positive integer, got: {threshold}")
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError(f"Circuit breaker timeout must be positive integer, got: {timeout}")
        
        self.threshold = threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def can_execute(self) -> bool:
        """
        Check if the circuit breaker allows execution.
        
        SAFETY: Validates state and time-based transitions
        VERIFY: Returns True if execution allowed, False otherwise
        """
        # SAFETY: Validate state
        if self.state not in ["CLOSED", "OPEN", "HALF_OPEN"]:
            logger.error(f"Invalid circuit breaker state: {self.state}, resetting to CLOSED")
            self.state = "CLOSED"
            self.failure_count = 0
            return True
        
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            # SAFETY: Validate last_failure_time before comparison
            if self.last_failure_time:
                try:
                    time_since_failure = datetime.now() - self.last_failure_time
                    if time_since_failure > timedelta(seconds=self.timeout):
                        self.state = "HALF_OPEN"
                        return True
                except (TypeError, OverflowError) as e:
                    logger.error(f"Error calculating time since failure: {e}, resetting circuit breaker")
                    self.last_failure_time = None
                    self.state = "CLOSED"
                    return True
            return False
        else:  # HALF_OPEN
            return True
    
    def record_success(self):
        """
        Record a successful operation.
        
        SAFETY: Validates state before transitions
        VERIFY: State updated correctly, failure count reset
        """
        old_state = self.state
        if self.state == "HALF_OPEN":
            # Success in half-open state closes the circuit
            self.state = "CLOSED"
            self.failure_count = 0
            self.last_failure_time = None
        elif self.state == "CLOSED":
            # Reset failure count on success
            self.failure_count = 0
            # Keep last_failure_time for tracking, but reset count
        # SAFETY: If OPEN state, stay OPEN (requires timeout to transition)
        
        # Update metrics if state changed
        if old_state != self.state and METRICS_ENABLED:
            try:
                # Get service name from caller context (will be set by orchestrator)
                # This is a limitation - we'd need to pass service_name to record_success
                # For now, metrics are updated in orchestrator after calling record_success
                pass
            except Exception:
                pass
    
    def record_failure(self):
        """
        Record a failed operation.
        
        SAFETY: Validates failure count and state transitions
        VERIFY: Failure count incremented, state updated correctly
        """
        # SAFETY: Validate failure count
        if not isinstance(self.failure_count, int):
            logger.error("Invalid failure count type, resetting")
            self.failure_count = 0
        
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        # SAFETY: Prevent integer overflow
        if self.failure_count > 1000000:
            logger.warning(f"Circuit breaker failure count very high: {self.failure_count}, resetting")
            self.failure_count = self.threshold
        
        if self.state == "HALF_OPEN":
            # Failure in half-open state reopens the circuit
            self.state = "OPEN"
        elif self.state == "CLOSED" and self.failure_count >= self.threshold:
            self.state = "OPEN"


class GuardServiceOrchestrator:
    """
    Main orchestrator for CodeGuardians guard services.
    
    Provides unified access, routing, health monitoring, and management
    for all guard services in the ecosystem.
    """
    
    def __init__(self):
        self.services: Dict[str, GuardServiceConfig] = {}
        self.health_status: Dict[str, ServiceHealth] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.http_client: Optional[httpx.AsyncClient] = None
        self._initialized = False
        self._initializing = False  # Prevent race conditions during initialization
        self.auto_discovery_enabled = True
        self.discovery_interval = 30  # seconds
        self.discovery_task: Optional[asyncio.Task] = None
        self.health_check_task: Optional[asyncio.Task] = None
        
    async def initialize(self):
        """Initialize the orchestrator with service configurations."""
        if self._initialized:
            return
        
        # Prevent concurrent initialization
        if self._initializing:
            # Wait for initialization to complete
            while self._initializing:
                await asyncio.sleep(0.1)
            return
        
        self._initializing = True
        
        try:
            logger.info("Initializing CodeGuardians Gateway Orchestrator...")
            
            # Initialize HTTP client
            self.http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
            )
            
            # Load service configurations
            await self._load_service_configurations()
            
            # Initialize circuit breakers
            await self._initialize_circuit_breakers()
            
            # Perform initial health checks (skip if disabled)
            disable_health_checks = os.getenv('DISABLE_HEALTH_CHECKS', 'false').lower() == 'true'
            if not disable_health_checks:
                await self._perform_health_checks()
            else:
                logger.info("Initial health checks skipped via DISABLE_HEALTH_CHECKS environment variable")
            
            # Start auto-discovery if enabled
            if self.auto_discovery_enabled:
                await self._start_auto_discovery()
            
            # Start periodic health checks (track the task)
            disable_health_checks = os.getenv('DISABLE_HEALTH_CHECKS', 'false').lower() == 'true'
            if not disable_health_checks and (self.health_check_task is None or self.health_check_task.done()):
                self.health_check_task = asyncio.create_task(self._start_health_check_loop())
                # Add error handler for the task
                self.health_check_task.add_done_callback(self._handle_health_check_task_error)
            elif disable_health_checks:
                logger.info("Health checks disabled via DISABLE_HEALTH_CHECKS environment variable")
            
            self._initialized = True
            logger.info("CodeGuardians Gateway Orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}")
            self._initialized = False
            raise
        finally:
            self._initializing = False
    
    def _handle_health_check_task_error(self, task: asyncio.Task):
        """
        Handle errors in health check background task.
        
        SAFETY: Handles CancelledError separately (expected during shutdown)
        VERIFY: Only restarts on actual errors, not cancellations
        """
        try:
            task.result()  # This will raise if task had an exception
        except asyncio.CancelledError:
            # Cancellation is expected during shutdown - don't treat as error
            logger.debug("Health check task cancelled (expected during shutdown)")
            return
        except Exception as e:
            logger.error(f"Health check background task failed: {e}")
            # Restart the health check task if it failed (and not shutting down)
            if not self._initializing and self._initialized:
                self.health_check_task = asyncio.create_task(self._start_health_check_loop())
                self.health_check_task.add_done_callback(self._handle_health_check_task_error)
    
    async def _load_service_configurations(self):
        """Load guard service configurations from central config."""
        # Import dynamic config manager
        try:
            from app.core.dynamic_config import get_dynamic_config_manager
            config_manager = get_dynamic_config_manager()
        except ImportError:
            config_manager = None
            logger.warning("Dynamic config manager not available, using defaults only")
        
        # Default service configurations with environment variable support
        default_configs = {
            "tokenguard": GuardServiceConfig(
                name="TokenGuard",
                service_type=GuardServiceType.TOKEN_GUARD,
                base_url=os.getenv("TOKENGUARD_URL", "http://tokenguard:8000"),
                health_endpoint="/health",
                priority=1,
                tags=["token", "optimization", "cost"]
            ),
            "trustguard": GuardServiceConfig(
                name="TrustGuard",
                service_type=GuardServiceType.TRUST_GUARD,
                base_url=os.getenv("TRUSTGUARD_URL", "http://trustguard:8000"),
                health_endpoint="/health",
                priority=1,
                tags=["trust", "reliability", "validation"],
                auth_header_name="X-API-Key",  # TrustGuard uses X-API-Key header
                auth_header_format="{token}"  # Simple format, no "Bearer" prefix
            ),
            "contextguard": GuardServiceConfig(
                name="ContextGuard",
                service_type=GuardServiceType.CONTEXT_GUARD,
                base_url=os.getenv("CONTEXTGUARD_URL", "http://contextguard:8003"),  # Fixed: Standardized to port 8003 (matches docs/tests)
                health_endpoint="/health",
                priority=1,
                tags=["context", "workflow"]
            ),
            "biasguard": GuardServiceConfig(
                name="BiasGuard",
                service_type=GuardServiceType.BIAS_GUARD,
                base_url=os.getenv("BIASGUARD_URL", "http://biasguard:8000"),
                health_endpoint="/health",
                priority=1,
                tags=["bias", "detection", "mitigation"]
            ),
            "healthguard": GuardServiceConfig(
                name="HealthGuard",
                service_type=GuardServiceType.HEALTH_GUARD,
                base_url=os.getenv("HEALTHGUARD_URL", "http://healthguard:8000"),
                health_endpoint="/health",
                priority=1,
                tags=["health", "monitoring", "diagnostics"]
            ),
            "securityguard": GuardServiceConfig(
                name="SecurityGuard",
                service_type=GuardServiceType.SECURITY_GUARD,
                base_url=os.getenv("SECURITYGUARD_URL", "http://securityguard:8103"),
                health_endpoint="/health",
                priority=1,
                tags=["security", "vulnerability", "scanning"]
            ),
        }
        
        # Load configurations from central config and override defaults
        for service_name, config in default_configs.items():
            # Try to get auth token from central config (single unified key)
            if config_manager:
                try:
                    # First try unified API key
                    unified_auth_token = config_manager.get("unified_api_key") or config_manager.get("gateway_api_key")
                    if unified_auth_token:
                        config.auth_token = unified_auth_token
                        logger.info(f"Loaded unified API key for {config.name} from central config")
                    
                    # Then try service-specific override (for backward compatibility)
                    auth_token = config_manager.get(f"services_{service_name}_auth_token")
                    if auth_token:
                        config.auth_token = auth_token
                        logger.info(f"Loaded auth token for {config.name} from central config (service-specific)")
                    
                    # Load auth header format if specified
                    auth_header_format = config_manager.get(f"services_{service_name}_auth_header_format")
                    if auth_header_format:
                        config.auth_header_format = auth_header_format
                    
                    # Load auth header name if specified
                    auth_header_name = config_manager.get(f"services_{service_name}_auth_header_name")
                    if auth_header_name:
                        config.auth_header_name = auth_header_name
                    
                    # Load base URL override if specified
                    base_url = config_manager.get(f"services_{service_name}_base_url")
                    if base_url:
                        config.base_url = base_url
                        logger.info(f"Loaded base URL for {config.name} from central config: {base_url}")
                    
                    # Load enabled status
                    enabled = config_manager.get(f"services_{service_name}_enabled")
                    if enabled is not None:
                        config.enabled = bool(enabled)
                        
                except Exception as e:
                    logger.debug(f"Could not load central config for {service_name}: {e}")
            
            # Fallback to environment variables - unified key first
            unified_env_key = os.getenv("UNIFIED_API_KEY") or os.getenv("GATEWAY_API_KEY")
            if unified_env_key and not config.auth_token:
                config.auth_token = unified_env_key
                logger.info(f"Loaded unified API key for {config.name} from environment variable")
            
            # Then try service-specific env var (for backward compatibility)
            env_auth_key = f"{service_name.upper()}_AUTH_TOKEN"
            env_auth_token = os.getenv(env_auth_key)
            if env_auth_token and not config.auth_token:
                config.auth_token = env_auth_token
                logger.info(f"Loaded auth token for {config.name} from environment variable")
            
            # Special handling for TrustGuard: use TRUSTGUARD_API_KEY env var or unified API key
            if service_name == "trustguard" and not config.auth_token:
                # Try TRUSTGUARD_API_KEY environment variable first
                trustguard_key = os.getenv("TRUSTGUARD_API_KEY")
                if trustguard_key:
                    config.auth_token = trustguard_key
                    logger.info(f"Loaded TrustGuard API key from TRUSTGUARD_API_KEY environment variable")
                else:
                    # Fallback to unified API key
                    unified_env_key = os.getenv("UNIFIED_API_KEY") or os.getenv("GATEWAY_API_KEY")
                    if unified_env_key:
                        config.auth_token = unified_env_key
                        logger.info(f"Using unified API key for TrustGuard (from UNIFIED_API_KEY)")
                    else:
                        logger.warning(f"No API key configured for TrustGuard. Authentication may fail.")
            
            self.services[service_name] = config
            logger.info(f"Loaded configuration for {config.name} (auth: {'configured' if config.auth_token else 'none'})")
    
    async def _initialize_circuit_breakers(self):
        """Initialize circuit breakers for all services."""
        for service_name, config in self.services.items():
            breaker = CircuitBreaker(
                threshold=config.circuit_breaker_threshold,
                timeout=config.circuit_breaker_timeout
            )
            self.circuit_breakers[service_name] = breaker
            
            # Initialize metrics for circuit breaker
            if METRICS_ENABLED:
                try:
                    update_circuit_breaker_state(service_name, breaker.state, breaker.failure_count)
                except Exception as metrics_error:
                    logger.debug(f"Failed to initialize circuit breaker metrics: {metrics_error}")
    
    async def _perform_health_checks(self):
        """Perform initial health checks on all services."""
        tasks = []
        for service_name in self.services.keys():
            tasks.append(self._check_service_health(service_name))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _start_health_check_loop(self):
        """
        Run periodic health checks in background.
        
        SAFETY: Exits gracefully on shutdown or cancellation
        VERIFY: Loop terminates when orchestrator is shutdown
        """
        while self._initialized:  # Exit when not initialized (shutdown)
            try:
                # Use shorter sleep intervals that can be cancelled more quickly
                # Split 30 seconds into 6 x 5 second intervals for faster cancellation response
                for _ in range(6):  # 6 x 5 seconds = 30 seconds total
                    if not self._initialized:  # Check flag frequently
                        break
                    await asyncio.sleep(5)  # Shorter sleep allows faster cancellation
                
                # Double-check before performing health checks (may have shutdown during sleep)
                if not self._initialized:
                    break
                await self._perform_health_checks()
            except asyncio.CancelledError:
                # Cancellation is expected during shutdown
                logger.debug("Health check loop cancelled")
                raise  # Re-raise to properly cancel the task
            except Exception as e:
                logger.error(f"Health check loop error: {e}")
                # Continue loop on errors (don't exit)
                if self._initialized:  # Only sleep if still initialized
                    await asyncio.sleep(5)  # Brief delay before retrying
    
    async def _check_service_health(self, service_name: str) -> ServiceHealth:
        """Check the health of a specific service with retry logic."""
        config = self.services.get(service_name)
        if not config:
            return ServiceHealth(
                service_name=service_name,
                status=ServiceStatus.UNKNOWN,
                last_check=datetime.now(),
                error_message="Service configuration not found"
            )
        
        # Check if we have recent health data (within 30 seconds)
        existing_health = self.health_status.get(service_name)
        if existing_health and (datetime.now() - existing_health.last_check).total_seconds() < 30:
            return existing_health
        
        start_time = datetime.now()
        max_retries = 3
        retry_delay = 1.0
        
        # Ensure HTTP client is available
        if not self.http_client:
            return ServiceHealth(
                service_name=service_name,
                status=ServiceStatus.UNKNOWN,
                last_check=datetime.now(),
                error_message="HTTP client not initialized"
            )
        
        for attempt in range(max_retries):
            try:
                health_url = f"{config.base_url}{config.health_endpoint}"
                
                # Prepare headers - don't send auth for health checks (health endpoints don't require auth)
                headers = {}
                # Note: Health endpoints don't require authentication, so we skip auth headers
                
                # Increase timeout for TrustGuard health checks which can be slow
                # Use explicit connect/read timeouts to handle slow connections
                if service_name == "trustguard":
                    # TrustGuard can have slow connection establishment or response delivery
                    # Set longer connect and read timeouts explicitly
                    timeout = httpx.Timeout(connect=10.0, read=40.0, write=10.0, pool=10.0)
                else:
                    timeout = httpx.Timeout(10.0)
                response = await self.http_client.get(health_url, headers=headers, timeout=timeout)
                
                response_time = (datetime.now() - start_time).total_seconds()
                
                if response.status_code == 200:
                    status = ServiceStatus.HEALTHY
                    error_message = None
                    # Safely parse JSON metadata
                    metadata = {}
                    try:
                        content_type = response.headers.get("content-type", "")
                        if content_type.startswith("application/json") and response.content:
                            metadata = response.json()
                    except (ValueError, json.JSONDecodeError) as e:
                        logger.debug(f"Failed to parse JSON metadata for {service_name}: {e}")
                        metadata = {}
                else:
                    status = ServiceStatus.UNHEALTHY
                    error_message = f"HTTP {response.status_code}"
                    metadata = {}
                
                health = ServiceHealth(
                    service_name=service_name,
                    status=status,
                    last_check=datetime.now(),
                    response_time=response_time,
                    error_message=error_message,
                    metadata=metadata
                )
                
                self.health_status[service_name] = health
                
                # Update Prometheus metrics
                if METRICS_ENABLED:
                    try:
                        update_service_health(service_name, status.value, response_time)
                        update_service_availability(service_name, status == ServiceStatus.HEALTHY)
                    except Exception as metrics_error:
                        logger.debug(f"Failed to update service health metrics: {metrics_error}")
                
                return health
                
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Health check attempt {attempt + 1} failed for {service_name}: {e}. Retrying in {retry_delay}s...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    response_time = (datetime.now() - start_time).total_seconds()
                    health = ServiceHealth(
                        service_name=service_name,
                        status=ServiceStatus.UNHEALTHY,
                        last_check=datetime.now(),
                        response_time=response_time,
                        error_message=str(e)
                    )
                    self.health_status[service_name] = health
                    return health
    
    async def orchestrate_request(self, request: OrchestrationRequest) -> OrchestrationResponse:
        """
        Orchestrate a request to the appropriate guard service.
        
        SAFETY: Validates all inputs, handles failures gracefully
        ASSUMES: Request is properly formatted, services are configured
        VERIFY: Returns OrchestrationResponse with success or error
        
        Args:
            request: The orchestration request
            
        Returns:
            OrchestrationResponse with the result
        """
        # OpenTelemetry tracing
        span = None
        try:
            from app.core.telemetry import get_tracer, set_span_status, add_span_attributes
            tracer = get_tracer()
        except Exception:
            tracer = None
        
        if tracer:
            span = tracer.start_span("orchestrator.orchestrate_request")
            span.set_attribute("request.id", request.request_id)
            span.set_attribute("service.type", request.service_type.value)
            span.set_attribute("component", "orchestrator")
        
        try:
            # SAFETY: Validate request input
            if not isinstance(request, OrchestrationRequest):
                raise ValueError(f"Invalid request type: {type(request)}")
            
            if not request.request_id:
                raise ValueError("Request ID is required")
            
            if not isinstance(request.service_type, GuardServiceType):
                raise ValueError(f"Invalid service type: {request.service_type}")
            
            # Ensure initialization (with race condition protection)
            if not self._initialized:
                await self.initialize()
            
            # SAFETY: Validate initialization completed successfully
            if not self._initialized:
                response = OrchestrationResponse(
                    request_id=request.request_id,
                    service_type=request.service_type,
                    success=False,
                    error="Orchestrator initialization failed",
                    error_code="ORCHESTRATOR_INIT_FAILED",
                    timestamp=datetime.now().isoformat(),
                    processing_time=0.0,
                    service_used=None
                )
                if span:
                    set_span_status(span, False, "Orchestrator initialization failed")
                    span.end()
                return response
            
            start_time = datetime.now()
            service_name = request.service_type.value
            
            if span:
                add_span_attributes(span, {"service.name": service_name})
            
            # SAFETY: Validate service configuration exists
            config = self.services.get(service_name)
            if not config:
                raise ServiceUnavailableError(f"Service {service_name} configuration not found")
            
            if not config.enabled:
                raise ServiceUnavailableError(f"Service {service_name} is disabled")
            
            # Check if service is available
            if not self._is_service_available(service_name):
                raise ServiceUnavailableError(f"Service {service_name} is not available")
            
            # SAFETY: Check circuit breaker with validation
            circuit_breaker = self.circuit_breakers.get(service_name)
            if circuit_breaker:
                if not isinstance(circuit_breaker, CircuitBreaker):
                    logger.error(f"Invalid circuit breaker type for {service_name}")
                    # Continue without circuit breaker protection
                    circuit_breaker = None
                elif not circuit_breaker.can_execute():
                    raise ServiceUnavailableError(f"Circuit breaker is open for {service_name}")
            
            # SAFETY: Ensure HTTP client is available and valid
            if not self.http_client:
                raise ServiceUnavailableError("HTTP client not initialized")
            
            # SAFETY: Validate payload structure
            if not isinstance(request.payload, dict):
                logger.warning(f"Invalid payload type for {service_name}: {type(request.payload)}")
                # Use empty dict as fallback
                request.payload = {}
            
            # Route request to service (with tracing)
            service_span = None
            if span:
                service_span = tracer.start_span("orchestrator.route_request", parent=span)
                service_span.set_attribute("service.name", service_name)
            
            try:
                if service_span:
                    add_span_attributes(service_span, {
                        "service.endpoint": self._determine_endpoint(request),
                        "service.url": config.base_url
                    })
                
                response_data = await self._route_request(request)
                
                if service_span:
                    set_span_status(service_span, True)
                    service_span.end()
                
            except Exception as route_error:
                if service_span:
                    set_span_status(service_span, False, str(route_error))
                    service_span.end()
                raise
            
            # SAFETY: Validate response data
            if not isinstance(response_data, dict):
                logger.warning(f"Invalid response data type from {service_name}: {type(response_data)}")
                response_data = {"raw_response": str(response_data)}
            
            # Record success in circuit breaker
            if circuit_breaker:
                try:
                    circuit_breaker.record_success()
                    # Update metrics
                    if METRICS_ENABLED:
                        update_circuit_breaker_state(service_name, circuit_breaker.state, circuit_breaker.failure_count)
                except Exception as cb_error:
                    logger.warning(f"Failed to record circuit breaker success: {cb_error}")
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Record orchestrator request metrics
            if METRICS_ENABLED:
                try:
                    record_orchestrator_request(service_name, "success", processing_time)
                except Exception as metrics_error:
                    logger.debug(f"Failed to record orchestrator metrics: {metrics_error}")
            
            if span:
                add_span_attributes(span, {
                    "processing.time": processing_time,
                    "service.success": True
                })
                set_span_status(span, True)
            
            response = OrchestrationResponse(
                request_id=request.request_id,
                service_type=request.service_type,
                success=True,
                data=response_data,
                timestamp=datetime.now().isoformat(),
                processing_time=processing_time,
                service_used=service_name
            )
            
            if span:
                span.end()
            return response
            
        except (GuardServiceError, ServiceUnavailableError) as e:
            # Record failure in circuit breaker
            circuit_breaker = self.circuit_breakers.get(service_name)
            if circuit_breaker:
                circuit_breaker.record_failure()
                # Update metrics
                if METRICS_ENABLED:
                    try:
                        update_circuit_breaker_state(service_name, circuit_breaker.state, circuit_breaker.failure_count)
                    except Exception:
                        pass
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Record orchestrator request metrics
            if METRICS_ENABLED:
                try:
                    record_orchestrator_request(service_name, "error", processing_time)
                except ArgumentException:
                    pass
            
            if span:
                add_span_attributes(span, {
                    "error.type": type(e).__name__,
                    "error.message": str(e),
                    "processing.time": processing_time,
                    "service.success": False
                })
                set_span_status(span, False, str(e))
                span.end()
            
            # SAFETY: Extract error_code from exception if available
            error_code = getattr(e, 'error_code', None) or type(e).__name__.upper()
            if hasattr(e, 'error_code') and e.error_code:
                error_code = e.error_code
            
            return OrchestrationResponse(
                request_id=request.request_id,
                service_type=request.service_type,
                success=False,
                error=str(e),
                error_code=error_code,
                timestamp=datetime.now().isoformat(),
                processing_time=processing_time,
                service_used=service_name
            )
        except Exception as e:
            # Record failure in circuit breaker
            circuit_breaker = self.circuit_breakers.get(service_name)
            if circuit_breaker:
                circuit_breaker.record_failure()
                # Update metrics
                if METRICS_ENABLED:
                    try:
                        update_circuit_breaker_state(service_name, circuit_breaker.state, circuit_breaker.failure_count)
                    except Exception as metrics_error:
                        from app.core.error_exporter import get_error_exporter
                        get_error_exporter().export_error(
                            metrics_error,
                            context={"operation": "update_circuit_breaker_metrics", "service": service_name},
                            error_code="METRICS_UPDATE_ERROR",
                            request_id=request.request_id
                        )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Record orchestrator request metrics
            if METRICS_ENABLED:
                try:
                    record_orchestrator_request(service_name, "error", processing_time)
                except Exception as metrics_error:
                    from app.core.error_exporter import get_error_exporter
                    get_error_exporter().export_error(
                        metrics_error,
                        context={"operation": "record_orchestrator_metrics", "service": service_name},
                        error_code="METRICS_RECORD_ERROR",
                        request_id=request.request_id
                    )
            
            # Log unexpected errors
            logger.error(f"Unexpected error orchestrating request for {service_name}: {e}", exc_info=True)
            
            # SAFETY: Trigger forensic analysis via Guardian Zero on critical errors
            # Pattern: Guardian Zero (999 Hz) forensic orchestration for zero-failure design
            if GUARDIAN_ZERO_ENABLED and self._should_trigger_forensic(str(e), service_name):
                forensic_span = None
                if span:
                    forensic_span = tracer.start_span("guardian_zero.forensic_analysis", parent=span)
                    forensic_span.set_attribute("service.name", service_name)
                
                try:
                    forensic_start = datetime.now()
                    forensic_result = await self._trigger_forensic_analysis(
                        service_name=service_name,
                        error=str(e),
                        request=request,
                        context={"error_type": type(e).__name__, "processing_time": processing_time}
                    )
                    forensic_duration = (datetime.now() - forensic_start).total_seconds()
                    
                    if forensic_result:
                        logger.info(
                            f" Guardian Zero forensic analysis triggered",
                            extra={
                                "service_name": service_name,
                                "root_cause": forensic_result.get("root_cause"),
                                "remediation_steps": forensic_result.get("remediation_steps", [])
                            }
                        )
                        # Record Guardian Zero metrics
                        if METRICS_ENABLED:
                            try:
                                record_guardian_zero_request(
                                    trigger_reason="critical_error",
                                    status="success",
                                    duration=forensic_duration
                                )
                            except Exception as metrics_error:
                                from app.core.error_exporter import get_error_exporter
                                get_error_exporter().export_error(
                                    metrics_error,
                                    context={"operation": "record_guardian_zero_metrics", "status": "success"},
                                    error_code="GUARDIAN_ZERO_METRICS_ERROR",
                                    request_id=request.request_id
                                )
                    else:
                        if METRICS_ENABLED:
                            try:
                                record_guardian_zero_request(
                                    trigger_reason="critical_error",
                                    status="unavailable",
                                    duration=forensic_duration
                                )
                            except Exception as metrics_error:
                                from app.core.error_exporter import get_error_exporter
                                get_error_exporter().export_error(
                                    metrics_error,
                                    context={"operation": "record_guardian_zero_metrics", "status": "unavailable"},
                                    error_code="GUARDIAN_ZERO_METRICS_ERROR",
                                    request_id=request.request_id
                                )
                        if forensic_span:
                            add_span_attributes(forensic_span, {
                                "root_cause": forensic_result.get("root_cause", ""),
                                "confidence": forensic_result.get("confidence", 0.0)
                            })
                            set_span_status(forensic_span, True)
                            forensic_span.end()
                except Exception as forensic_error:
                    logger.warning(f"Forensic analysis failed: {forensic_error}")
                    if METRICS_ENABLED:
                        try:
                            record_guardian_zero_request(
                                trigger_reason="critical_error",
                                status="error"
                            )
                        except Exception as metrics_error:
                            from app.core.error_exporter import get_error_exporter
                            get_error_exporter().export_error(
                                metrics_error,
                                context={"operation": "record_guardian_zero_metrics", "status": "error"},
                                error_code="GUARDIAN_ZERO_METRICS_ERROR",
                                request_id=request.request_id
                            )
                    if forensic_span:
                        set_span_status(forensic_span, False, str(forensic_error))
                        forensic_span.end()
            
            if span:
                add_span_attributes(span, {
                    "error.type": type(e).__name__,
                    "error.message": str(e),
                    "processing.time": processing_time,
                    "service.success": False
                })
                set_span_status(span, False, str(e))
                span.end()
            
            # SAFETY: Extract error_code from exception if available
            error_code = getattr(e, 'error_code', None) or "INTERNAL_ERROR"
            if hasattr(e, 'error_code') and e.error_code:
                error_code = e.error_code
            
            return OrchestrationResponse(
                request_id=request.request_id,
                service_type=request.service_type,
                success=False,
                error=f"Internal error: {str(e)}",
                error_code=error_code,
                timestamp=datetime.now().isoformat(),
                processing_time=processing_time,
                service_used=service_name
            )
    
    def _is_service_available(self, service_name: str) -> bool:
        """
        Check if a service is available for requests.
        
        SAFETY: Validates configuration and health status
        ASSUMES: Service name is valid string
        VERIFY: Returns True if service is available, False otherwise
        """
        # SAFETY: Validate input
        if not isinstance(service_name, str) or not service_name:
            logger.warning(f"Invalid service name: {service_name}")
            return False
        
        # SAFETY: Check configuration exists
        config = self.services.get(service_name)
        if not config:
            logger.debug(f"Service configuration not found: {service_name}")
            return False
        
        if not isinstance(config, GuardServiceConfig):
            logger.error(f"Invalid configuration type for {service_name}: {type(config)}")
            return False
        
        if not config.enabled:
            logger.debug(f"Service {service_name} is disabled")
            return False
        
        # SAFETY: Check health status
        health = self.health_status.get(service_name)
        if not health:
            # If health hasn't been checked yet, assume available (optimistic)
            logger.debug(f"Health status not yet checked for {service_name}, assuming available")
            return True
        
        if not isinstance(health, ServiceHealth):
            logger.warning(f"Invalid health status type for {service_name}: {type(health)}")
            # Assume available if health check hasn't run properly
            return True
        
        # Allow requests to healthy and degraded services
        # Also allow requests even if health check failed recently (service might be recovering)
        return health.status in [ServiceStatus.HEALTHY, ServiceStatus.DEGRADED]
    
    async def _route_request(self, request: OrchestrationRequest) -> Dict[str, Any]:
        """
        Route a request to the appropriate service.
        
        SAFETY: Validates URLs, payloads, and handles all failure cases
        ASSUMES: Service configuration exists and is valid
        VERIFY: Returns valid response dict or raises GuardServiceError
        """
        # SAFETY: Validate inputs
        if not isinstance(request, OrchestrationRequest):
            raise ValueError("Invalid request type")
        
        service_name = request.service_type.value
        config = self.services.get(service_name)
        
        # SAFETY: Validate configuration exists
        if not config:
            raise ServiceUnavailableError(f"Service configuration not found for {service_name}")
        
        if not isinstance(config, GuardServiceConfig):
            raise ConfigurationError(f"Invalid configuration type for {service_name}")

        # SAFETY: Ensure HTTP client is available and valid
        if not self.http_client:
            raise ServiceUnavailableError("HTTP client not initialized")
        
        if not isinstance(self.http_client, httpx.AsyncClient):
            raise ServiceUnavailableError("HTTP client is not a valid AsyncClient instance")

        # SAFETY: Validate and sanitize base_url
        if not config.base_url:
            raise ConfigurationError(f"Base URL not configured for {service_name}")
        
        if not isinstance(config.base_url, str):
            raise ConfigurationError(f"Invalid base URL type for {service_name}: {type(config.base_url)}")
        
        # Determine endpoint based on service type and payload
        endpoint = self._determine_endpoint(request)
        
        # SAFETY: Validate endpoint
        if not isinstance(endpoint, str):
            raise ConfigurationError(f"Invalid endpoint type: {type(endpoint)}")
        
        if not endpoint.startswith('/'):
            logger.warning(f"Endpoint {endpoint} does not start with '/', adding prefix")
            endpoint = '/' + endpoint
        
        # Sanitize base_url to avoid double slashes (remove trailing slash if present)
        base_url = config.base_url.rstrip('/')
        
        # SAFETY: Validate URL construction
        try:
            url = f"{base_url}{endpoint}"
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                raise ConfigurationError(f"Invalid URL format: {url}")
        except Exception as url_error:
            raise ConfigurationError(f"Failed to construct URL for {service_name}: {url_error}")

        # Transform payload to match service-specific schema
        transformed_payload = self._transform_payload(request)
        
        # Enhance payload with context awareness (invisible to user)
        # Zero-failure: If ContextGuard unavailable, uses original payload
        try:
            from app.core.contextguard_integration import enhance_guard_with_context
            transformed_payload = enhance_guard_with_context(
                guard_name=service_name,
                payload=transformed_payload,
                session_id=request.session_id,
                user_id=request.user_id
            )
        except Exception as e:
            # Graceful degradation - continue with original payload if enhancement fails
            logger.debug(f"ContextGuard enhancement skipped for {service_name}: {e}")

        # Prepare request
        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": request.request_id,
            # SAFETY: Ensure X-Gateway-Request header is lowercase "true" for TrustGuard compatibility
            # TrustGuard checks: gateway_request = request.headers.get("X-Gateway-Request", "").lower() == "true"
            "X-Gateway-Request": "true"  # Indicate this is a gateway request (used by TrustGuard for service-to-service auth)
        }

        # Add internal access token for internal service calls
        # Check if this is an internal service by examining the hostname
        if self._is_internal_service(config.base_url):
            headers["X-Internal-Token"] = settings.INTERNAL_ACCESS_TOKEN

        if request.user_id:
            headers["X-User-ID"] = request.user_id

        if request.session_id:
            headers["X-Session-ID"] = request.session_id

        # Add authentication header if configured (for services that still require it)
        # Note: TrustGuard handles service-to-service auth via X-Gateway-Request header
        # but we still send auth tokens if configured for backward compatibility
        if config.auth_token:
            try:
                # SAFETY: Validate auth token format
                if not isinstance(config.auth_token, str):
                    logger.warning(f"Invalid auth token type for {service_name}: {type(config.auth_token)}")
                else:
                    # SAFETY: Validate auth header format
                    try:
                        auth_header_value = config.auth_header_format.format(token=config.auth_token)
                        headers[config.auth_header_name] = auth_header_value
                        # Also add X-API-Key header for services that check it (backward compatibility)
                        headers["X-API-Key"] = config.auth_token
                    except KeyError as format_error:
                        logger.warning(f"Failed to format auth header for {service_name}: {format_error}")
                        # Fallback: use token directly
                        headers[config.auth_header_name] = config.auth_token
                        headers["X-API-Key"] = config.auth_token
            except Exception as auth_error:
                logger.warning(f"Failed to add auth headers for {service_name}: {auth_error}")

        # SAFETY: Validate and set timeout
        timeout_seconds = request.timeout if request.timeout and request.timeout > 0 else config.timeout
        if timeout_seconds <= 0:
            logger.warning(f"Invalid timeout {timeout_seconds}s for {service_name}, using default 30s")
            timeout_seconds = 30
        
        # SAFETY: Limit maximum timeout to prevent resource exhaustion
        MAX_TIMEOUT = 300  # 5 minutes
        if timeout_seconds > MAX_TIMEOUT:
            logger.warning(f"Timeout {timeout_seconds}s exceeds maximum {MAX_TIMEOUT}s for {service_name}, capping")
            timeout_seconds = MAX_TIMEOUT
        
        timeout = httpx.Timeout(timeout_seconds)

        try:
            # Log request details for debugging
            logger.debug(
                f"Routing request to {service_name}",
                extra={
                    "service_name": service_name,
                    "url": url,
                    "endpoint": endpoint,
                    "base_url": base_url,
                    "method": "POST",
                    "request_id": request.request_id
                }
            )
            
            response = await self.http_client.post(
                url,
                json=transformed_payload,
                headers=headers,
                timeout=timeout
            )

            # SAFETY: Validate response object
            if not response:
                raise GuardServiceError(f"Empty response from {service_name}")

            if response.status_code == 200:
                try:
                    # SAFETY: Validate response is JSON
                    if not response.content:
                        logger.warning(f"Empty response body from {service_name}")
                        return {"status": "success", "message": "Empty response"}
                    
                    response_data = response.json()
                    
                    # SAFETY: Validate response is dict
                    if not isinstance(response_data, dict):
                        logger.warning(f"Non-dict JSON response from {service_name}: {type(response_data)}")
                        return {"raw_response": response_data}
                    
                    # Store ContextGuard context (non-blocking, graceful degradation)
                    try:
                        from app.core.contextguard_integration import store_guard_context
                        # Fire and forget - don't block response
                        store_guard_context(
                            guard_name=service_name,
                            payload=transformed_payload,
                            result=response_data,
                            session_id=request.session_id,
                            user_id=request.user_id
                        )
                    except Exception as e:
                        # Non-critical - continue even if storage fails
                        logger.debug(f"ContextGuard storage skipped for {service_name}: {e}")
                    
                    return response_data
                except (ValueError, json.JSONDecodeError) as e:
                    # If JSON parsing fails, try to return the text content
                    logger.warning(f"Failed to parse JSON response from {service_name}: {e}")
                    # SAFETY: Limit response text size to prevent memory issues
                    max_response_size = 5000
                    response_text = response.text[:max_response_size] if response.text else ""
                    return {
                        "error": "Invalid JSON response",
                        "raw_response": response_text,
                        "truncated": len(response.text) > max_response_size if response.text else False
                    }
            else:
                # Get error details from response
                try:
                    # SAFETY: Validate error response
                    if response.content:
                        error_detail = response.json()
                        if isinstance(error_detail, dict):
                            error_message = error_detail.get('detail', error_detail.get('message', str(error_detail)))
                        else:
                            error_message = str(error_detail)
                    else:
                        error_message = f"HTTP {response.status_code}"
                except (ValueError, json.JSONDecodeError):
                    # SAFETY: Limit error text size
                    max_error_size = 500
                    error_text = response.text[:max_error_size] if response.text else f"HTTP {response.status_code}"
                    error_message = error_text

                # Enhanced logging for 404 errors
                if response.status_code == 404:
                    logger.error(
                        f"404 Not Found for {service_name}",
                        extra={
                            "service_name": service_name,
                            "url": url,
                            "endpoint": endpoint,
                            "base_url": base_url,
                            "status_code": response.status_code,
                            "response_preview": response.text[:200] if response.text else None,
                            "request_id": request.request_id
                        }
                    )

                # Special handling for authentication errors
                if response.status_code == 403:
                    logger.warning(
                        f"Service {service_name} returned 403 Forbidden. "
                        f"This may indicate an authentication issue. "
                        f"Error: {error_message}"
                    )
                elif response.status_code == 401:
                    logger.warning(
                        f"Service {service_name} returned 401 Unauthorized. "
                        f"Authentication may be required. "
                        f"Error: {error_message}"
                    )

                raise GuardServiceError(
                    f"Service returned status {response.status_code}: {error_message}"
                )
        except httpx.TimeoutException:
            raise GuardServiceError(f"Request to {service_name} timed out after {timeout_seconds}s")
        except httpx.RequestError as e:
            raise GuardServiceError(f"Request to {service_name} failed: {str(e)}")
        except GuardServiceError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error routing request to {service_name}: {e}", exc_info=True)
            raise GuardServiceError(f"Request to {service_name} failed: {str(e)}")
    
    async def _handle_integrated_bias_detection(self, request: OrchestrationRequest) -> Dict[str, Any]:
        """Handle bias detection using the integrated service."""
        try:
            from app.services.bias_detection import bias_detection_service
            
            # Extract bias detection parameters from payload
            payload = request.payload
            if not isinstance(payload, dict):
                payload = {}
                logger.warning(f"Invalid payload type for bias detection: {type(request.payload)}")
            
            # Extract text from various possible locations
            text = ""
            
            # Try samples array format first (from QUICK_REFERENCE.md)
            if "samples" in payload and isinstance(payload.get("samples"), list):
                samples = payload.get("samples", [])
                if len(samples) > 0:
                    first_sample = samples[0]
                    if isinstance(first_sample, dict):
                        # Try content field first (BiasGuard/HealthGuard format)
                        if "content" in first_sample:
                            text = first_sample.get("content", "")
                            logger.debug(f"Extracted text from samples[0].content: '{text[:50]}...'")
                        # Fall back to text field
                        elif "text" in first_sample:
                            text = first_sample.get("text", "")
                            logger.debug(f"Extracted text from samples[0].text: '{text[:50]}...'")
            
            # Try direct text field
            if not text and "text" in payload:
                text = payload.get("text", "")
                logger.debug(f"Extracted text from payload.text: '{text[:50]}...'")
            # Try content field
            if not text and "content" in payload:
                text = payload.get("content", "")
                logger.debug(f"Extracted text from payload.content: '{text[:50]}...'")
            # Try data field - could be string or dict
            if not text and "data" in payload:
                data = payload.get("data", {})
                if isinstance(data, str):
                    text = data
                elif isinstance(data, dict):
                    # Try to extract text from nested data structure
                    text = data.get("text", data.get("content", ""))
                    # If still empty, check if data has a single string value
                    if not text and len(data) == 1:
                        values = list(data.values())
                        if values and isinstance(values[0], str):
                            text = values[0]
            # Try operation field for backwards compatibility
            if not text and "operation" in payload and payload.get("operation") == "detect_bias":
                # This is the transformed format, check data field
                data = payload.get("data", {})
                if isinstance(data, str):
                    text = data
                elif isinstance(data, dict):
                    text = data.get("text", data.get("content", ""))
            
            # Convert to string if not already
            if not isinstance(text, str):
                if isinstance(text, dict):
                    # Try to extract text from dict
                    text = text.get("text", text.get("content", ""))
                else:
                    text = str(text) if text else ""
            
            # Validate text is not empty
            if not text or not text.strip():
                logger.error(f"Bias detection failed: No text content found. Payload keys: {list(payload.keys()) if isinstance(payload, dict) else 'N/A'}")
                if isinstance(payload, dict) and "samples" in payload:
                    logger.error(f"Samples array: {payload.get('samples')}")
                raise GuardServiceError("Text content is required for bias detection")
            
            bias_types = payload.get("bias_types", None)
            mitigation_level = payload.get("mitigation_level", "moderate")
            target_audience = payload.get("target_audience", "general")
            
            # Call the integrated bias detection service
            result = await bias_detection_service.detect_bias(
                text=text,
                bias_types=bias_types,
                mitigation_level=mitigation_level,
                target_audience=target_audience
            )
            
            # Return result in the expected format
            return {
                "bias_detected": result.bias_detected,
                "bias_score": result.bias_score,
                "bias_types": result.bias_types,
                "bias_details": result.bias_details,
                "mitigation_suggestions": result.mitigation_suggestions,
                "fairness_score": result.fairness_score,
                "confidence": result.confidence,
                "processing_time": result.processing_time,
                "service_used": "integrated_bias_detection"
            }
            
        except ImportError:
            raise GuardServiceError("Integrated bias detection service not available")
        except GuardServiceError:
            raise
        except Exception as e:
            logger.error(f"Bias detection failed: {e}", exc_info=True)
            raise GuardServiceError(f"Bias detection failed: {str(e)}")
    
    def _determine_endpoint(self, request: OrchestrationRequest) -> str:
        """
        Determine the appropriate endpoint for a request.
        
        SAFETY: Validates service type and returns safe default
        ASSUMES: Request has valid service_type
        VERIFY: Returns valid endpoint string starting with '/'
        """
        # SAFETY: Validate input
        if not isinstance(request, OrchestrationRequest):
            raise ValueError("Invalid request type")
        
        service_type = request.service_type
        
        if not isinstance(service_type, GuardServiceType):
            raise ValueError(f"Invalid service type: {service_type}")

        # Default endpoints for each service type
        # These must match the actual endpoints exposed by each guard service
        endpoints = {
            GuardServiceType.TOKEN_GUARD: "/scan",
            GuardServiceType.TRUST_GUARD: "/validate",  # TrustGuard exposes /validate endpoint
            GuardServiceType.CONTEXT_GUARD: "/analyze",    # ContextGuard exposes /analyze for context drift
            GuardServiceType.BIAS_GUARD: "/process",       # BiasGuard exposes /process endpoint (also has /mitigate, /report)
            GuardServiceType.HEALTH_GUARD: "/analyze",     # HealthGuard uses /analyze endpoint
            GuardServiceType.SECURITY_GUARD: "/scan",  # SecurityGuard exposes /scan endpoint
        }

        endpoint = endpoints.get(service_type, "/api/v1/process")
        
        # SAFETY: Validate endpoint format
        if not isinstance(endpoint, str) or not endpoint.startswith('/'):
            logger.warning(f"Invalid endpoint format for {service_type}: {endpoint}, using default")
            endpoint = "/api/v1/process"
        
        return endpoint

    def _transform_payload(self, request: OrchestrationRequest) -> Dict[str, Any]:
        """
        Transform the generic payload to match service-specific schema.

        SAFETY: Validates payload structure, handles all edge cases
        ASSUMES: Request has valid service_type and payload
        VERIFY: Returns valid dict matching service schema
        
        Each service expects different fields:
        - TokenGuard (/scan): content, confidence
        - TrustGuard (/validate): input_text, output_text, context (optional)
        - ContextGuard (/analyze): current_code, previous_code, context (optional)
        - BiasGuard (/process): text, context (optional), detailed_analysis (optional)
        - HealthGuard (/analyze): samples array with DataSample objects
        - SecurityGuard (/scan): content, context (optional), strict_mode (optional)
        """
        # SAFETY: Validate input
        if not isinstance(request, OrchestrationRequest):
            raise ValueError("Invalid request type")
        
        service_type = request.service_type
        
        if not isinstance(service_type, GuardServiceType):
            raise ValueError(f"Invalid service type: {service_type}")
        
        # Ensure payload is a dict and create a safe copy
        if not isinstance(request.payload, dict):
            logger.warning(f"Invalid payload type: {type(request.payload)}, using empty dict")
            payload = {}
        else:
            # SAFETY: Create deep copy to avoid mutating original
            try:
                payload = request.payload.copy()
            except (AttributeError, TypeError) as e:
                logger.warning(f"Failed to copy payload: {e}, using empty dict")
                payload = {}
        
        # SAFETY: Ensure payload is always a dict
        if not isinstance(payload, dict):
            payload = {}

        # Add request metadata to payload early (before service-specific transformations)
        # This ensures all guards receive consistent metadata
        if request.user_id and 'user_id' not in payload:
            payload['user_id'] = request.user_id
        if request.session_id and 'session_id' not in payload:
            payload['session_id'] = request.session_id
        if request.request_id and 'request_id' not in payload:
            payload['request_id'] = request.request_id

        # Service-specific transformations
        if service_type == GuardServiceType.TOKEN_GUARD:
            # TokenGuard /scan expects: content, confidence
            return {
                "content": payload.get("content", payload.get("text", "")),
                "confidence": payload.get("confidence", 0.7),
                "logprobs_stream": payload.get("logprobs_stream"),
                "user_id": payload.get("user_id", request.user_id),
                "session_id": payload.get("session_id", request.session_id),
                "request_id": payload.get("request_id", request.request_id)
            }

        elif service_type == GuardServiceType.TRUST_GUARD:
            # TrustGuard /validate expects: validation_type (required), content (required), context (optional)
            # Fix: Use validation_type and content fields (not input_text/output_text)
            # Fix: Remove metadata fields (user_id, session_id, request_id) - services reject them with 422
            # Fix: Keep context as dict (not JSON string) - matches SecurityGuard pattern
            
            # Extract content from various possible locations
            content = payload.get("content", payload.get("text", payload.get("input_text", "")))
            
            # Get validation_type (required field)
            validation_type = payload.get("validation_type", "general")  # Default to "general"
            
            result = {
                "validation_type": validation_type,
                "content": content
            }
            
            # Add optional context if provided (keep as dict, not JSON string - matches SecurityGuard)
            if "context" in payload:
                context_value = payload.get("context")
                # Keep context as dict (SecurityGuard accepts dict context, TrustGuard should too)
                if isinstance(context_value, dict):
                    result["context"] = context_value
                elif isinstance(context_value, str):
                    # If it's already a string, keep it as string
                    result["context"] = context_value
                # If context is None or other type, skip it
            
            # Add optional validation_level if provided
            if "validation_level" in payload:
                result["validation_level"] = payload.get("validation_level")
            
            # NOTE: Removed metadata fields (user_id, session_id, request_id)
            # TrustGuard service rejects these fields with 422 errors
            # TokenGuard/SecurityGuard accept them, but TrustGuard/BiasGuard don't
            
            return result

        elif service_type == GuardServiceType.CONTEXT_GUARD:
            # ContextGuard /analyze expects: current_code, previous_code (for drift detection)
            # Transform text/content to ContextDriftRequest format
            # SAFETY: Check for current_code first (most common), then fall back to text/content
            current_code = payload.get("current_code", payload.get("text", payload.get("content", "")))
            
            # Use previous_code if provided, otherwise use empty string
            previous_code = payload.get("previous_code", payload.get("previous_content", ""))
            
            result = {
                "current_code": current_code,
                "previous_code": previous_code
            }
            
            # Add context if provided (ContextDriftRequest includes optional context field)
            if "context" in payload:
                result["context"] = payload.get("context")
            
            # Preserve metadata
            if payload.get("user_id"):
                result["user_id"] = payload["user_id"]
            if payload.get("session_id"):
                result["session_id"] = payload["session_id"]
            if payload.get("request_id"):
                result["request_id"] = payload["request_id"]
            
            return result

        elif service_type == GuardServiceType.SECURITY_GUARD:
            # SecurityGuard /scan expects: content, context (optional), strict_mode (optional)
            content = payload.get("text", payload.get("content", ""))
            result = {
                "content": content
            }
            if "context" in payload:
                result["context"] = payload.get("context")
            if "strict_mode" in payload:
                result["strict_mode"] = payload.get("strict_mode", False)
            
            # Preserve metadata
            if payload.get("user_id"):
                result["user_id"] = payload["user_id"]
            if payload.get("session_id"):
                result["session_id"] = payload["session_id"]
            if payload.get("request_id"):
                result["request_id"] = payload["request_id"]
            
            return result

        elif service_type == GuardServiceType.BIAS_GUARD:
            # BiasGuard /process expects: operation (required), text field (not samples array!)
            # BiasAnalysisRequest requires: operation, text, context (optional), detailed_analysis (optional)
            # Fix: Add operation field (required) - defaults to "detect_bias"
            # Fix: Remove metadata fields (user_id, session_id, request_id) - services reject them with 422
            # Extract text from various possible locations
            text = payload.get("text", payload.get("content", ""))
            
            # Handle samples array format (extract text from first sample)
            if not text and "samples" in payload and isinstance(payload.get("samples"), list):
                samples = payload.get("samples", [])
                if len(samples) > 0:
                    first_sample = samples[0]
                    if isinstance(first_sample, dict):
                        # Try content field first
                        text = first_sample.get("content", first_sample.get("text", ""))
            
            # Handle data field format
            if not text and "data" in payload:
                data = payload.get("data", {})
                if isinstance(data, dict):
                    text = data.get("text", data.get("content", ""))
                elif isinstance(data, str):
                    text = data
            
            # Validate text is not empty
            if not text or not text.strip():
                raise ValueError("Text content is required for bias detection")
            
            # Get operation field (required) - default to "detect_bias"
            operation = payload.get("operation", "detect_bias")
            
            # Build result in BiasGuard expected format
            result = {
                "operation": operation,
                "text": text
            }
            
            # Add optional context field
            if "context" in payload:
                result["context"] = payload.get("context")
            
            # Add optional detailed_analysis field
            if "detailed_analysis" in payload:
                result["detailed_analysis"] = payload.get("detailed_analysis", True)
            
            # NOTE: Removed metadata fields (user_id, session_id, request_id)
            # BiasGuard service rejects these fields with 422 errors
            # TokenGuard/SecurityGuard accept them, but TrustGuard/BiasGuard don't
            
            return result

        elif service_type == GuardServiceType.HEALTH_GUARD:
            # HealthGuard /analyze expects: samples array with DataSample objects
            # DataSample requires: id, content, metadata (optional)
            text = payload.get("text", payload.get("content", ""))
            sample_id = payload.get("sample_id", f"sample_{hash(text) % 10000}")
            
            result = {
                "samples": [
                    {
                        "id": sample_id,
                        "content": text,  # HealthGuard expects 'content' not 'text'
                        "metadata": {
                            "confidence": payload.get("confidence", 0.7),
                            "metrics": payload.get("metrics", {}),
                            "checks": payload.get("checks", []),
                            "alerts": payload.get("alerts", []),
                            "context": payload.get("context", {})
                        }
                    }
                ]
            }
            
            # Preserve metadata
            if payload.get("user_id"):
                result["user_id"] = payload["user_id"]
            if payload.get("session_id"):
                result["session_id"] = payload["session_id"]
            if payload.get("request_id"):
                result["request_id"] = payload["request_id"]
            
            return result

        # Default: return payload as-is with validation
        # Ensure payload has required fields for unknown service types
        if not payload:
            payload = {}
        
        # Add request metadata to payload if not present
        if request.user_id and 'user_id' not in payload:
            payload['user_id'] = request.user_id
        if request.session_id and 'session_id' not in payload:
            payload['session_id'] = request.session_id
        if request.request_id and 'request_id' not in payload:
            payload['request_id'] = request.request_id
        
        return payload
    
    async def get_service_health(self, service_name: Optional[str] = None) -> Union[ServiceHealth, Dict[str, ServiceHealth]]:
        """Get health status for services."""
        if service_name:
            return self.health_status.get(service_name, ServiceHealth(
                service_name=service_name,
                status=ServiceStatus.UNKNOWN,
                last_check=datetime.now(),
                error_message="Service not found"
            ))
        return self.health_status.copy()
    
    async def refresh_health_checks(self):
        """Refresh health checks for all services."""
        tasks = []
        for service_name in self.services.keys():
            tasks.append(self._check_service_health(service_name))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _start_auto_discovery(self):
        """Start the auto-discovery background task."""
        if self.discovery_task and not self.discovery_task.done():
            return
        
        self.discovery_task = asyncio.create_task(self._auto_discovery_loop())
        logger.info("Auto-discovery started")
    
    async def _auto_discovery_loop(self):
        """Background task for auto-discovery of guard services."""
        logger.info("Auto-discovery disabled - no external guard services configured")
        # Disable auto-discovery to prevent connection attempts to non-existent services
        return
    
    async def _discover_services(self):
        """Discover guard services automatically."""
        # Disable auto-discovery for now since external guard services are not available
        # This prevents connection attempts to non-existent services
        discovery_configs = {}
        
        for service_name, config in discovery_configs.items():
            # Skip disabled services
            if not config.get("enabled", True):
                continue
                
            if service_name not in self.services:
                # Try to discover the service
                host = "localhost" if os.getenv("HOST", "localhost") == "0.0.0.0" else os.getenv("HOST", "localhost")
                base_url = f"http://{host}:{config.get('port', os.getenv('PORT', os.getenv('GATEWAY_PORT', '8000')))}"
                try:
                    # Check if service is available
                    health_url = f"{base_url}/health"
                    if not self.http_client:
                        continue
                    response = await self.http_client.get(health_url, timeout=httpx.Timeout(5.0))
                    
                    if response.status_code == 200:
                        # Service discovered, add to configuration
                        service_config = GuardServiceConfig(
                            name=config["name"],
                            service_type=GuardServiceType[service_name.upper()],
                            base_url=base_url,
                            health_endpoint="/health",
                            priority=1,
                            tags=self._get_service_tags(service_name)
                        )
                        
                        self.services[service_name] = service_config
                        self.circuit_breakers[service_name] = CircuitBreaker()
                        
                        # Perform initial health check
                        await self._check_service_health(service_name)
                        
                        logger.info(f"Auto-discovered service: {config['name']} at {base_url}")
                        
                except Exception as e:
                    # Service not available, continue discovery
                    logger.debug(f"Service {service_name} not available: {e}")
                    continue
    
    def _get_service_tags(self, service_name: str) -> List[str]:
        """Get tags for a service based on its name."""
        tag_mapping = {
            "tokenguard": ["token", "optimization", "cost"],
            "trustguard": ["trust", "reliability", "validation"],
            "contextguard": ["context", "workflow"],
            "securityguard": ["security", "vulnerability", "scanning"],
            "biasguard": ["bias", "detection", "mitigation"],
            "healthguard": ["health", "monitoring", "diagnostics"],
        }
        return tag_mapping.get(service_name, [])
    
    async def register_service(self, service_name: str, base_url: str, 
                               service_type: GuardServiceType, 
                               health_endpoint: str = "/health",
                               priority: int = 1,
                               tags: List[str] = None) -> bool:
        """Manually register a guard service."""
        try:
            service_config = GuardServiceConfig(
                name=service_name,
                service_type=service_type,
                base_url=base_url,
                health_endpoint=health_endpoint,
                priority=priority,
                tags=tags or []
            )
            
            self.services[service_name] = service_config
            self.circuit_breakers[service_name] = CircuitBreaker()
            
            # Perform initial health check
            await self._check_service_health(service_name)
            
            logger.info(f"Manually registered service: {service_name} at {base_url}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register service {service_name}: {e}")
            return False
    
    async def unregister_service(self, service_name: str) -> bool:
        """Unregister a guard service."""
        try:
            if service_name not in self.services:
                logger.warning(f"Attempted to unregister non-existent service: {service_name}")
                return False
            
            # Safely remove from all dictionaries
            self.services.pop(service_name, None)
            self.health_status.pop(service_name, None)
            self.circuit_breakers.pop(service_name, None)
            logger.info(f"Unregistered service: {service_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to unregister service {service_name}: {e}")
            return False
    
    def _is_internal_service(self, base_url: str) -> bool:
        """
        Determine if a service URL represents an internal service that should
        receive the internal access token.

        Internal services are identified by:
        - localhost or 127.0.0.1
        - Private IP ranges (192.168.x.x, 10.x.x.x, 172.16-31.x.x)
        - Hostnames starting with 'internal-'
        - Hostnames exactly matching 'internal'

        This prevents accidentally sending internal tokens to external services
        that happen to contain 'internal' in their URL.
        """
        try:
            from urllib.parse import urlparse
            parsed = urlparse(base_url)

            if not parsed.hostname:
                return False

            hostname = parsed.hostname.lower()

            # Check for localhost
            if hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
                return True

            # Check for hostnames starting with 'internal-'
            if hostname.startswith('internal-') or hostname == 'internal':
                return True

            # Check for private IP ranges
            try:
                parts = hostname.split('.')
                if len(parts) == 4 and all(p.isdigit() for p in parts):
                    ip_parts = [int(p) for p in parts]
                    # Private IP ranges:
                    # 192.168.x.x
                    if ip_parts[0] == 192 and ip_parts[1] == 168:
                        return True
                    # 10.x.x.x
                    if ip_parts[0] == 10:
                        return True
                    # 172.16.x.x to 172.31.x.x
                    if ip_parts[0] == 172 and 16 <= ip_parts[1] <= 31:
                        return True
            except (ValueError, IndexError):
                # Not a valid IP, continue with hostname checks
                pass

            return False

        except Exception as e:
            logger.warning(f"Error checking if service is internal ({base_url}): {e}")
            # Default to False for security - don't send internal tokens to unknown URLs
            return False

    def get_discovered_services(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all discovered services."""
        discovered = {}
        for service_name, config in self.services.items():
            health = self.health_status.get(service_name)
            discovered[service_name] = {
                "name": config.name,
                "base_url": config.base_url,
                "service_type": config.service_type.value,
                "priority": config.priority,
                "tags": config.tags,
                "health_status": health.status.value if health else "unknown",
                "last_check": health.last_check.isoformat() if health else None,
                "response_time": health.response_time if health else None,
                "error_message": health.error_message if health else None
            }
        return discovered
    
    async def _trigger_forensic_analysis(
        self,
        service_name: str,
        error: str,
        request: Optional[OrchestrationRequest] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger forensic analysis via Guardian Zero.
        
        SAFETY: Analyzes system failures and provides remediation
        ASSUMES: Guardian Zero is available and configured
        VERIFY: Returns forensic analysis result or None if unavailable
        
        Args:
            service_name: Name of the service that failed
            error: Error message or failure description
            request: Original orchestration request (optional)
            context: Additional context for forensic analysis
            
        Returns:
            Forensic analysis result from Guardian Zero or None
        """
        if not GUARDIAN_ZERO_ENABLED:
            return None
        
        try:
            # Ensure HTTP client is available
            if not self.http_client:
                logger.warning("HTTP client not available for forensic analysis")
                return None
            
            # Build system state for forensic analysis
            system_state = {
                "service_name": service_name,
                "error": error,
                "timestamp": datetime.now().isoformat(),
                "service_health": {
                    name: {
                        "status": health.status.value,
                        "response_time": health.response_time,
                        "error_message": health.error_message
                    }
                    for name, health in self.health_status.items()
                },
                "circuit_breakers": {
                    name: {
                        "state": breaker.state,
                        "failure_count": breaker.failure_count
                    }
                    for name, breaker in self.circuit_breakers.items()
                }
            }
            
            # Add request context if available
            if request:
                system_state["request"] = {
                    "request_id": request.request_id,
                    "service_type": request.service_type.value,
                    "user_id": request.user_id,
                    "session_id": request.session_id
                }
            
            # Add additional context
            if context:
                system_state["context"] = context
            
            # Prepare forensic analysis request
            forensic_url = f"{GUARDIAN_ZERO_URL.rstrip('/')}/forensic/analyze"
            forensic_payload = {
                "system_state": system_state,
                "failure_mode": context.get("error_type") if context else None
            }
            
            # Invoke Guardian Zero for forensic analysis
            logger.info(f" Triggering Guardian Zero forensic analysis for {service_name}")
            response = await self.http_client.post(
                forensic_url,
                json=forensic_payload,
                timeout=httpx.Timeout(30.0),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                forensic_result = response.json()
                logger.info(
                    f" Guardian Zero forensic analysis complete",
                    extra={
                        "service_name": service_name,
                        "root_cause": forensic_result.get("root_cause"),
                        "confidence": forensic_result.get("confidence")
                    }
                )
                return forensic_result
            else:
                logger.warning(f"Guardian Zero forensic analysis returned {response.status_code}")
                return None
                
        except Exception as e:
            logger.warning(f"Failed to trigger forensic analysis: {e}")
            return None
    
    async def request_architecture_review(
        self,
        system_description: str,
        requirements: List[str],
        constraints: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Request architecture review from Guardian Zero.
        
        SAFETY: Validates system architecture for zero-failure design
        ASSUMES: Guardian Zero is available and configured
        VERIFY: Returns architecture review result or None if unavailable
        
        Args:
            system_description: Description of the system to review
            requirements: List of system requirements
            constraints: Optional constraints and context
            
        Returns:
            Architecture review result from Guardian Zero or None
        """
        if not GUARDIAN_ZERO_ENABLED:
            return None
        
        try:
            # Ensure HTTP client is available
            if not self.http_client:
                logger.warning("HTTP client not available for architecture review")
                return None
            
            # Prepare architecture review request
            review_url = f"{GUARDIAN_ZERO_URL.rstrip('/')}/architecture/review"
            review_payload = {
                "system_description": system_description,
                "requirements": requirements,
                "constraints": constraints or {}
            }
            
            # Invoke Guardian Zero for architecture review
            logger.info(" Requesting Guardian Zero architecture review")
            response = await self.http_client.post(
                review_url,
                json=review_payload,
                timeout=httpx.Timeout(30.0),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                review_result = response.json()
                logger.info(
                    f" Guardian Zero architecture review complete",
                    extra={
                        "verdict": review_result.get("verdict"),
                        "confidence": review_result.get("confidence")
                    }
                )
                return review_result
            else:
                logger.warning(f"Guardian Zero architecture review returned {response.status_code}")
                return None
                
        except Exception as e:
            logger.warning(f"Failed to request architecture review: {e}")
            return None
    
    def _should_trigger_forensic(self, error: str, service_name: str) -> bool:
        """
        Determine if forensic analysis should be triggered.
        
        SAFETY: Pattern detection for forensic triggers
        VERIFY: Returns True if forensic analysis is recommended
        
        Args:
            error: Error message or failure description
            service_name: Name of the service
            
        Returns:
            True if forensic analysis should be triggered
        """
        # Trigger forensic analysis for:
        # 1. Critical errors (circuit breaker open, service unavailable)
        # 2. Repeated failures (indicates systemic issues)
        # 3. Authentication/authorization failures (security concern)
        # 4. Timeout errors (infrastructure concern)
        
        error_lower = error.lower()
        critical_patterns = [
            "circuit breaker",
            "service unavailable",
            "authentication",
            "authorization",
            "timeout",
            "connection",
            "critical",
            "fatal"
        ]
        
        # Check if error matches critical patterns
        if any(pattern in error_lower for pattern in critical_patterns):
            return True
        
        # Check circuit breaker state
        circuit_breaker = self.circuit_breakers.get(service_name)
        if circuit_breaker and circuit_breaker.state == "OPEN":
            return True
        
        return False
    
    async def shutdown(self):
        """
        Shutdown the orchestrator and cleanup resources.
        
        SAFETY: Graceful shutdown with resource cleanup
        ASSUMES: Called during application shutdown
        VERIFY: All resources cleaned up, no leaks
        """
        logger.info("Shutting down CodeGuardians Gateway Orchestrator...")
        
        # SAFETY: Set _initialized to False FIRST so loops exit immediately
        # This ensures loops check the flag and exit before we cancel tasks
        self._initialized = False
        
        # Stop auto-discovery
        self.auto_discovery_enabled = False
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
        
        # Stop health check loop
        if self.health_check_task:
            if not self.health_check_task.done():
                try:
                    self.health_check_task.cancel()
                    await asyncio.wait_for(self.health_check_task, timeout=5.0)
                except asyncio.CancelledError:
                    pass
                except asyncio.TimeoutError:
                    logger.warning("Health check task shutdown timeout")
                except Exception as e:
                    logger.error(f"Error cancelling health check task: {e}")
            self.health_check_task = None
        
        # SAFETY: Cleanup HTTP client with error handling
        if self.http_client:
            try:
                await asyncio.wait_for(self.http_client.aclose(), timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("HTTP client close timeout")
            except Exception as e:
                logger.error(f"Error closing HTTP client: {e}")
            finally:
                self.http_client = None
        
        # Reset additional state
        self._initializing = False
        
        logger.info("CodeGuardians Gateway Orchestrator shutdown complete")


# Global orchestrator instance
orchestrator = GuardServiceOrchestrator()