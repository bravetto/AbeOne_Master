"""
AI Guardians Circuit Breaker Implementation

Circuit breaker pattern for handling service failures and preventing cascade failures.
"""

import asyncio
import time
from enum import Enum
from typing import Any, Callable, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Circuit is open, requests fail fast
    HALF_OPEN = "HALF_OPEN"  # Testing if service is back


class CircuitBreaker:
    """
    Circuit breaker implementation for service failure handling.
    
    Prevents cascade failures by opening the circuit when a service
    fails repeatedly, and gradually testing if the service is back.
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception,
        name: str = "default"
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Time in seconds before trying to close circuit
            expected_exception: Exception type to count as failures
            name: Name of the circuit breaker
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.name = name
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.success_count = 0
        
        logger.info(f"Circuit breaker '{name}' initialized")
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerOpenError: When circuit is open
            Exception: Original function exception
        """
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info(f"Circuit breaker '{self.name}' moved to HALF_OPEN")
            else:
                raise CircuitBreakerOpenError(f"Circuit breaker '{self.name}' is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
            
        except self.expected_exception as e:
            await self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        
        return time.time() - self.last_failure_time >= self.recovery_timeout
    
    async def _on_success(self):
        """Handle successful call."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= 3:  # Require 3 successes to close
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                logger.info(f"Circuit breaker '{self.name}' moved to CLOSED")
        else:
            # Reset failure count on success
            self.failure_count = 0
    
    async def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker '{self.name}' moved to OPEN after {self.failure_count} failures")
    
    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time,
            "is_open": self.state == CircuitState.OPEN
        }
    
    def reset(self):
        """Manually reset circuit breaker."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        logger.info(f"Circuit breaker '{self.name}' manually reset")


class CircuitBreakerOpenError(Exception):
    """Exception raised when circuit breaker is open."""
    pass


class CircuitBreakerManager:
    """Manager for multiple circuit breakers."""
    
    def __init__(self):
        self.breakers: Dict[str, CircuitBreaker] = {}
    
    def get_breaker(self, name: str, **kwargs) -> CircuitBreaker:
        """Get or create circuit breaker."""
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker(name=name, **kwargs)
        return self.breakers[name]
    
    def get_all_states(self) -> Dict[str, Dict[str, Any]]:
        """Get states of all circuit breakers."""
        return {name: breaker.get_state() for name, breaker in self.breakers.items()}
    
    def reset_all(self):
        """Reset all circuit breakers."""
        for breaker in self.breakers.values():
            breaker.reset()


# Global circuit breaker manager
circuit_breaker_manager = CircuitBreakerManager()


def circuit_breaker(name: str, **kwargs):
    """
    Decorator for circuit breaker protection.
    
    Args:
        name: Circuit breaker name
        **kwargs: Circuit breaker configuration
    """
    def decorator(func):
        async def wrapper(*args, **func_kwargs):
            breaker = circuit_breaker_manager.get_breaker(name, **kwargs)
            return await breaker.call(func, *args, **func_kwargs)
        return wrapper
    return decorator


class ServiceHealthChecker:
    """Service health checker with circuit breaker integration."""
    
    def __init__(self):
        self.health_breakers = {}
    
    async def check_service_health(self, service_name: str, health_url: str) -> Dict[str, Any]:
        """
        Check service health with circuit breaker protection.
        
        Args:
            service_name: Name of the service
            health_url: Health check URL
            
        Returns:
            Health check result
        """
        breaker = circuit_breaker_manager.get_breaker(
            f"{service_name}_health",
            failure_threshold=3,
            recovery_timeout=30
        )
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(health_url, timeout=5) as response:
                    if response.status == 200:
                        return {
                            "service": service_name,
                            "status": "healthy",
                            "response_time": response.headers.get("X-Response-Time", 0),
                            "timestamp": time.time()
                        }
                    else:
                        return {
                            "service": service_name,
                            "status": "unhealthy",
                            "status_code": response.status,
                            "timestamp": time.time()
                        }
        except Exception as e:
            logger.error(f"Health check failed for {service_name}: {e}")
            return {
                "service": service_name,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def check_all_services(self, services: Dict[str, str]) -> Dict[str, Any]:
        """
        Check health of all services.
        
        Args:
            services: Dictionary of service names to health URLs
            
        Returns:
            Health check results for all services
        """
        tasks = []
        for service_name, health_url in services.items():
            task = self.check_service_health(service_name, health_url)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            service_name: result for service_name, result in 
            zip(services.keys(), results)
        }


# Global service health checker
service_health_checker = ServiceHealthChecker()
