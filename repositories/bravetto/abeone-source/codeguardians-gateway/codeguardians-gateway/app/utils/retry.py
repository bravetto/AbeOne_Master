"""
Retry and circuit breaker utilities for external service calls.

This module provides decorators and utilities for implementing retry logic
and circuit breaker patterns for external API calls.
"""

import asyncio
import logging
import time
from functools import wraps
from typing import Callable, Any, Optional, Dict, List
from dataclasses import dataclass, field
from contextlib import asynccontextmanager

from app.core.exceptions import CircuitBreakerOpenError, RetryExhaustedError, ExternalServiceError
from app.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class CircuitBreakerState:
    """Circuit breaker state tracking."""
    service_name: str
    failure_threshold: int = 5
    recovery_timeout: float = 60.0  # seconds
    expected_exception: tuple = (Exception,)

    # Internal state
    failures: int = 0
    last_failure_time: Optional[float] = None
    state: str = "closed"  # "closed", "open", "half_open"

    def record_success(self):
        """Record a successful call."""
        self.failures = 0
        self.state = "closed"
        logger.debug(f"Circuit breaker for {self.service_name}: success recorded, state={self.state}")

    def record_failure(self):
        """Record a failed call."""
        self.failures += 1
        self.last_failure_time = time.time()

        if self.failures >= self.failure_threshold:
            self.state = "open"
            logger.warning(f"Circuit breaker for {self.service_name}: opened after {self.failures} failures")

    def can_attempt_call(self) -> bool:
        """Check if a call can be attempted."""
        if self.state == "closed":
            return True

        if self.state == "open":
            if self.last_failure_time and (time.time() - self.last_failure_time) > self.recovery_timeout:
                self.state = "half_open"
                logger.info(f"Circuit breaker for {self.service_name}: attempting recovery")
                return True
            return False

        # half_open state
        return True

    def is_call_permitted(self) -> bool:
        """Check if the circuit breaker allows the call."""
        if not self.can_attempt_call():
            raise CircuitBreakerOpenError(self.service_name)
        return True


class CircuitBreakerRegistry:
    """Registry for managing circuit breakers."""

    def __init__(self):
        self._breakers: Dict[str, CircuitBreakerState] = {}

    def get_or_create(self, service_name: str, **kwargs) -> CircuitBreakerState:
        """Get or create a circuit breaker for a service."""
        if service_name not in self._breakers:
            self._breakers[service_name] = CircuitBreakerState(service_name=service_name, **kwargs)
        return self._breakers[service_name]

    def get_all_states(self) -> Dict[str, Dict[str, Any]]:
        """Get the state of all circuit breakers."""
        return {
            name: {
                "state": breaker.state,
                "failures": breaker.failures,
                "last_failure_time": breaker.last_failure_time
            }
            for name, breaker in self._breakers.items()
        }


# Global registry
circuit_breaker_registry = CircuitBreakerRegistry()


def circuit_breaker(
    service_name: str,
    failure_threshold: int = 5,
    recovery_timeout: float = 60.0,
    expected_exception: tuple = (Exception,)
):
    """
    Circuit breaker decorator for external service calls.

    Args:
        service_name: Name of the service for monitoring
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Time in seconds to wait before attempting recovery
        expected_exception: Tuple of exceptions that count as failures
    """
    def decorator(func):
        breaker = circuit_breaker_registry.get_or_create(
            service_name,
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            expected_exception=expected_exception
        )

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            breaker.is_call_permitted()

            try:
                result = await func(*args, **kwargs)
                breaker.record_success()
                return result
            except expected_exception as e:
                breaker.record_failure()
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            breaker.is_call_permitted()

            try:
                result = func(*args, **kwargs)
                breaker.record_success()
                return result
            except expected_exception as e:
                breaker.record_failure()
                raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


async def retry_async(
    func: Callable,
    *args,
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    jitter: bool = True,
    exceptions: tuple = (Exception,),
    **kwargs
) -> Any:
    """
    Retry an async function with exponential backoff.

    Args:
        func: Function to retry
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts
        backoff: Backoff multiplier
        jitter: Add random jitter to delay
        exceptions: Tuple of exceptions to retry on
        *args, **kwargs: Arguments to pass to func
    """
    import random

    last_exception = None
    current_delay = delay

    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except exceptions as e:
            last_exception = e

            if attempt == max_attempts - 1:
                # Last attempt failed
                logger.error(f"All {max_attempts} attempts failed for {func.__name__}: {e}")
                raise RetryExhaustedError(
                    service_name=getattr(func, '__name__', 'unknown_function'),
                    attempts=max_attempts,
                    details={"last_error": str(e)}
                ) from e

            # Calculate delay with optional jitter
            actual_delay = current_delay
            if jitter:
                actual_delay *= (0.5 + random.random() * 0.5)  # 0.5x to 1.0x

            logger.warning(f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. Retrying in {actual_delay:.2f}s")
            await asyncio.sleep(actual_delay)
            current_delay *= backoff

    # This should never be reached, but just in case
    raise last_exception


def retry_with_circuit_breaker(
    service_name: str,
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    failure_threshold: int = 5,
    recovery_timeout: float = 60.0,
    exceptions: tuple = (ExternalServiceError,)
):
    """
    Combine retry logic with circuit breaker pattern.

    This decorator applies both retry logic and circuit breaker protection
    to external service calls.
    """
    def decorator(func):
        # Apply circuit breaker first, then retry
        circuit_breaked_func = circuit_breaker(
            service_name=service_name,
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            expected_exception=exceptions
        )(func)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await retry_async(
                circuit_breaked_func,
                *args,
                max_attempts=max_attempts,
                delay=delay,
                backoff=backoff,
                exceptions=exceptions,
                **kwargs
            )

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For sync functions, we can't easily combine retry + circuit breaker
            # Just apply circuit breaker
            return circuit_breaked_func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


@asynccontextmanager
async def error_boundary(service_name: str, operation: str):
    """
    Context manager for error boundaries around external service calls.

    Usage:
        async with error_boundary("stripe", "create_customer"):
            await stripe_service.create_customer(...)
    """
    start_time = time.time()

    try:
        logger.debug(f"Starting {operation} on service {service_name}")
        yield
        duration = time.time() - start_time
        logger.debug(f"Completed {operation} on service {service_name} in {duration:.3f}s")

    except ExternalServiceError as e:
        duration = time.time() - start_time
        logger.error(f"External service error in {operation} on {service_name}: {e} (took {duration:.3f}s)")
        raise

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Unexpected error in {operation} on {service_name}: {e} (took {duration:.3f}s)")
        raise ExternalServiceError(
            message=f"Unexpected error during {operation}",
            details={"service": service_name, "operation": operation, "error": str(e)}
        ) from e
