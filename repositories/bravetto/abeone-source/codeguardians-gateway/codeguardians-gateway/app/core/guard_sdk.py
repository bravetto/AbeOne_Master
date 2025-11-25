"""
AI Guardians SDK - Guard Service Development Kit

This module provides a comprehensive SDK for developing and integrating
new guard services into the AI Guardians platform.

The SDK includes:
- Base classes for guard services
- Standard interfaces and protocols
- Helper utilities for common patterns
- Testing and validation tools
- Documentation templates
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import httpx
from pydantic import BaseModel, Field
import json

logger = logging.getLogger(__name__)


class GuardServiceStatus(Enum):
    """Status of a guard service."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class GuardServicePriority(Enum):
    """Priority levels for guard services."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


@dataclass
class GuardServiceConfig:
    """Configuration for a guard service."""
    name: str
    service_type: str
    base_url: str
    health_endpoint: str = "/health"
    priority: GuardServicePriority = GuardServicePriority.NORMAL
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GuardServiceHealth:
    """Health status of a guard service."""
    service_name: str
    status: GuardServiceStatus
    last_check: float
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class GuardServiceRequest(BaseModel):
    """Standard request model for guard services."""
    text: str = Field(..., description="Text to analyze")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    user_id: Optional[str] = Field(None, description="User ID for tracking")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    options: Dict[str, Any] = Field(default_factory=dict, description="Service-specific options")


class GuardServiceResponse(BaseModel):
    """Standard response model for guard services."""
    success: bool = Field(..., description="Whether the operation was successful")
    data: Dict[str, Any] = Field(default_factory=dict, description="Response data")
    confidence: float = Field(0.0, description="Confidence score (0.0-1.0)")
    warnings: List[str] = Field(default_factory=list, description="Warning messages")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    processing_time: float = Field(0.0, description="Processing time in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    error: Optional[str] = Field(None, description="Error message if failed")


class BaseGuardService(ABC):
    """
    Base class for all guard services.
    
    This class provides the standard interface and common functionality
    that all guard services must implement.
    """
    
    def __init__(self, config: GuardServiceConfig):
        self.config = config
        self.logger = logging.getLogger(f"guard.{config.name}")
        self._health_status = GuardServiceHealth(
            service_name=config.name,
            status=GuardServiceStatus.UNKNOWN,
            last_check=0.0
        )
        self._circuit_breaker_failures = 0
        self._circuit_breaker_last_failure = 0.0
    
    @abstractmethod
    async def process_request(self, request: GuardServiceRequest) -> GuardServiceResponse:
        """
        Process a guard service request.
        
        This is the main method that all guard services must implement.
        It should contain the core logic for the guard service.
        
        Args:
            request: The guard service request
            
        Returns:
            Guard service response
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> GuardServiceHealth:
        """
        Perform a health check on the guard service.
        
        Returns:
            Health status of the service
        """
        pass
    
    async def initialize(self) -> bool:
        """
        Initialize the guard service.
        
        This method is called when the service is first started.
        Override this method to perform any initialization tasks.
        
        Returns:
            True if initialization was successful
        """
        self.logger.info(f"Initializing guard service: {self.config.name}")
        return True
    
    async def shutdown(self) -> None:
        """
        Shutdown the guard service.
        
        This method is called when the service is being stopped.
        Override this method to perform any cleanup tasks.
        """
        self.logger.info(f"Shutting down guard service: {self.config.name}")
    
    async def validate_request(self, request: GuardServiceRequest) -> bool:
        """
        Validate a guard service request.
        
        Override this method to add custom validation logic.
        
        Args:
            request: The request to validate
            
        Returns:
            True if the request is valid
        """
        if not request.text or not request.text.strip():
            return False
        
        # Add any additional validation logic here
        return True
    
    async def preprocess_request(self, request: GuardServiceRequest) -> GuardServiceRequest:
        """
        Preprocess a guard service request.
        
        Override this method to add preprocessing logic.
        
        Args:
            request: The original request
            
        Returns:
            Preprocessed request
        """
        # Add any preprocessing logic here
        return request
    
    async def postprocess_response(self, response: GuardServiceResponse) -> GuardServiceResponse:
        """
        Postprocess a guard service response.
        
        Override this method to add postprocessing logic.
        
        Args:
            response: The original response
            
        Returns:
            Postprocessed response
        """
        # Add any postprocessing logic here
        return response
    
    async def handle_error(self, error: Exception, request: GuardServiceRequest) -> GuardServiceResponse:
        """
        Handle errors that occur during request processing.
        
        Override this method to add custom error handling logic.
        
        Args:
            error: The exception that occurred
            request: The original request
            
        Returns:
            Error response
        """
        self.logger.error(f"Error processing request: {error}")
        
        return GuardServiceResponse(
            success=False,
            error=str(error),
            processing_time=0.0
        )
    
    def is_circuit_breaker_open(self) -> bool:
        """Check if the circuit breaker is open."""
        if self._circuit_breaker_failures >= self.config.circuit_breaker_threshold:
            time_since_failure = time.time() - self._circuit_breaker_last_failure
            if time_since_failure < self.config.circuit_breaker_timeout:
                return True
            else:
                # Reset circuit breaker
                self._circuit_breaker_failures = 0
        return False
    
    def record_success(self) -> None:
        """Record a successful operation."""
        self._circuit_breaker_failures = 0
    
    def record_failure(self) -> None:
        """Record a failed operation."""
        self._circuit_breaker_failures += 1
        self._circuit_breaker_last_failure = time.time()
    
    async def execute_with_circuit_breaker(
        self, 
        request: GuardServiceRequest
    ) -> GuardServiceResponse:
        """
        Execute a request with circuit breaker protection.
        
        Args:
            request: The request to execute
            
        Returns:
            Guard service response
        """
        if self.is_circuit_breaker_open():
            return GuardServiceResponse(
                success=False,
                error="Service temporarily unavailable (circuit breaker open)",
                processing_time=0.0
            )
        
        try:
            # Validate request
            if not await self.validate_request(request):
                return GuardServiceResponse(
                    success=False,
                    error="Invalid request",
                    processing_time=0.0
                )
            
            # Preprocess request
            processed_request = await self.preprocess_request(request)
            
            # Process request
            start_time = time.time()
            response = await self.process_request(processed_request)
            processing_time = time.time() - start_time
            
            # Update processing time
            response.processing_time = processing_time
            
            # Postprocess response
            response = await self.postprocess_response(response)
            
            # Record success
            self.record_success()
            
            return response
            
        except Exception as error:
            # Record failure
            self.record_failure()
            
            # Handle error
            return await self.handle_error(error, request)


class HTTPGuardService(BaseGuardService):
    """
    Base class for HTTP-based guard services.
    
    This class provides common functionality for guard services that
    communicate via HTTP.
    """
    
    def __init__(self, config: GuardServiceConfig):
        super().__init__(config)
        self.client = httpx.AsyncClient(
            timeout=config.timeout,
            base_url=config.base_url
        )
    
    async def health_check(self) -> GuardServiceHealth:
        """Perform HTTP health check."""
        try:
            start_time = time.time()
            response = await self.client.get(self.config.health_endpoint)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                status = GuardServiceStatus.HEALTHY
                error_message = None
            else:
                status = GuardServiceStatus.UNHEALTHY
                error_message = f"HTTP {response.status_code}"
            
            self._health_status = GuardServiceHealth(
                service_name=self.config.name,
                status=status,
                last_check=time.time(),
                response_time=response_time,
                error_message=error_message
            )
            
        except Exception as e:
            self._health_status = GuardServiceHealth(
                service_name=self.config.name,
                status=GuardServiceStatus.UNHEALTHY,
                last_check=time.time(),
                error_message=str(e)
            )
        
        return self._health_status
    
    async def shutdown(self) -> None:
        """Shutdown HTTP client."""
        await super().shutdown()
        await self.client.aclose()


class GuardServiceRegistry:
    """
    Registry for managing guard services.
    
    This class provides functionality for registering, discovering,
    and managing guard services.
    """
    
    def __init__(self):
        self._services: Dict[str, BaseGuardService] = {}
        self._service_configs: Dict[str, GuardServiceConfig] = {}
        self.logger = logging.getLogger("guard.registry")
    
    def register_service(self, service: BaseGuardService) -> None:
        """
        Register a guard service.
        
        Args:
            service: The guard service to register
        """
        self._services[service.config.name] = service
        self._service_configs[service.config.name] = service.config
        self.logger.info(f"Registered guard service: {service.config.name}")
    
    def unregister_service(self, service_name: str) -> bool:
        """
        Unregister a guard service.
        
        Args:
            service_name: Name of the service to unregister
            
        Returns:
            True if service was unregistered
        """
        if service_name in self._services:
            del self._services[service_name]
            del self._service_configs[service_name]
            self.logger.info(f"Unregistered guard service: {service_name}")
            return True
        return False
    
    def get_service(self, service_name: str) -> Optional[BaseGuardService]:
        """
        Get a guard service by name.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Guard service or None if not found
        """
        return self._services.get(service_name)
    
    def list_services(self) -> List[str]:
        """
        List all registered service names.
        
        Returns:
            List of service names
        """
        return list(self._services.keys())
    
    async def health_check_all(self) -> Dict[str, GuardServiceHealth]:
        """
        Perform health check on all services.
        
        Returns:
            Dictionary of service health statuses
        """
        health_statuses = {}
        
        for service_name, service in self._services.items():
            try:
                health = await service.health_check()
                health_statuses[service_name] = health
            except Exception as e:
                self.logger.error(f"Health check failed for {service_name}: {e}")
                health_statuses[service_name] = GuardServiceHealth(
                    service_name=service_name,
                    status=GuardServiceStatus.UNHEALTHY,
                    last_check=time.time(),
                    error_message=str(e)
                )
        
        return health_statuses


class GuardServiceBuilder:
    """
    Builder class for creating guard services.
    
    This class provides a fluent interface for building guard services
    with proper configuration and validation.
    """
    
    def __init__(self):
        self._config = None
        self._service_class = None
        self._middleware = []
    
    def with_config(self, config: GuardServiceConfig) -> 'GuardServiceBuilder':
        """Set the service configuration."""
        self._config = config
        return self
    
    def with_service_class(self, service_class: type) -> 'GuardServiceBuilder':
        """Set the service class."""
        self._service_class = service_class
        return self
    
    def with_middleware(self, middleware: Callable) -> 'GuardServiceBuilder':
        """Add middleware to the service."""
        self._middleware.append(middleware)
        return self
    
    def build(self) -> BaseGuardService:
        """
        Build the guard service.
        
        Returns:
            Configured guard service instance
        """
        if not self._config:
            raise ValueError("Service configuration is required")
        
        if not self._service_class:
            raise ValueError("Service class is required")
        
        service = self._service_class(self._config)
        
        # Apply middleware
        for middleware in self._middleware:
            service = middleware(service)
        
        return service


# Example guard service implementation
class ExampleGuardService(HTTPGuardService):
    """
    Example guard service implementation.
    
    This class demonstrates how to implement a guard service using the SDK.
    """
    
    async def process_request(self, request: GuardServiceRequest) -> GuardServiceResponse:
        """Process a request using the example guard service."""
        try:
            # Example processing logic
            text_length = len(request.text)
            word_count = len(request.text.split())
            
            # Simulate some processing
            await asyncio.sleep(0.1)
            
            # Generate example response
            response_data = {
                "text_length": text_length,
                "word_count": word_count,
                "analysis": "Example analysis completed",
                "score": 0.85
            }
            
            return GuardServiceResponse(
                success=True,
                data=response_data,
                confidence=0.85,
                warnings=["This is an example warning"],
                recommendations=["This is an example recommendation"],
                processing_time=0.1,
                metadata={"service": "example"}
            )
            
        except Exception as e:
            return await self.handle_error(e, request)


# Utility functions
def create_guard_service_config(
    name: str,
    service_type: str,
    base_url: str,
    **kwargs
) -> GuardServiceConfig:
    """
    Create a guard service configuration.
    
    Args:
        name: Service name
        service_type: Type of service
        base_url: Base URL of the service
        **kwargs: Additional configuration options
        
    Returns:
        Guard service configuration
    """
    return GuardServiceConfig(
        name=name,
        service_type=service_type,
        base_url=base_url,
        **kwargs
    )


def validate_guard_service(service: BaseGuardService) -> List[str]:
    """
    Validate a guard service implementation.
    
    Args:
        service: The guard service to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check required methods
    if not hasattr(service, 'process_request'):
        errors.append("Missing required method: process_request")
    
    if not hasattr(service, 'health_check'):
        errors.append("Missing required method: health_check")
    
    # Check method signatures
    if hasattr(service, 'process_request'):
        import inspect
        sig = inspect.signature(service.process_request)
        if len(sig.parameters) != 2:  # self + request
            errors.append("process_request method must take exactly 2 parameters")
    
    return errors


# Documentation template
GUARD_SERVICE_TEMPLATE = """
# {service_name} Guard Service

## Overview
{description}

## Configuration
- **Name**: {name}
- **Type**: {service_type}
- **Base URL**: {base_url}
- **Priority**: {priority}
- **Timeout**: {timeout}s

## API Endpoints
- **Health Check**: `GET {base_url}{health_endpoint}`
- **Process**: `POST {base_url}/process`

## Request Format
```json
{{
    "text": "Text to analyze",
    "context": {{}},
    "user_id": "optional",
    "session_id": "optional",
    "metadata": {{}},
    "options": {{}}
}}
```

## Response Format
```json
{{
    "success": true,
    "data": {{}},
    "confidence": 0.85,
    "warnings": [],
    "recommendations": [],
    "processing_time": 0.1,
    "metadata": {{}}
}}
```

## Implementation
```python
from app.core.guard_sdk import BaseGuardService, GuardServiceRequest, GuardServiceResponse

class {service_name}GuardService(BaseGuardService):
    async def process_request(self, request: GuardServiceRequest) -> GuardServiceResponse:
        # Implementation here
        pass
    
    async def health_check(self) -> GuardServiceHealth:
        # Health check implementation
        pass
```

## Testing
Use the provided test utilities to validate your implementation:

```python
from app.core.guard_sdk import validate_guard_service

service = {service_name}GuardService(config)
errors = validate_guard_service(service)
if errors:
    print("Validation errors:", errors)
```
"""

