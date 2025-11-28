"""
Graceful Shutdown Handler

PRODUCTION HARDENING:
- SIGTERM signal handling
- Request drain (wait for in-flight requests)
- Connection cleanup (database, Redis, HTTP clients)
- Graceful resource release

SAFETY: Ensures no data loss during shutdown
ASSUMES: Requests complete within timeout period
VERIFY: All connections closed, no hanging requests
"""

import signal
import asyncio
import logging
from typing import Optional, Callable, List
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

# Global shutdown event
_shutdown_event: Optional[asyncio.Event] = None
_shutdown_handlers: List[Callable] = []


def register_shutdown_handler(handler: Callable):
    """
    Register a shutdown handler.
    
    Handler should be async function that performs cleanup.
    """
    _shutdown_handlers.append(handler)
    logger.debug(f"Registered shutdown handler: {handler.__name__}")


async def _execute_shutdown_handlers():
    """Execute all registered shutdown handlers."""
    logger.info(f"Executing {len(_shutdown_handlers)} shutdown handlers...")
    
    for handler in _shutdown_handlers:
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()
            logger.debug(f"Shutdown handler {handler.__name__} completed")
        except Exception as e:
            logger.error(f"Shutdown handler {handler.__name__} failed: {e}")


def _signal_handler(signum, frame):
    """Handle shutdown signals (SIGTERM, SIGINT)."""
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    
    if _shutdown_event:
        _shutdown_event.set()
    else:
        # Emergency shutdown if event not initialized
        logger.warning("Shutdown event not initialized, forcing exit")
        import sys
        sys.exit(0)


async def wait_for_shutdown(timeout: float = 30.0):
    """
    Wait for shutdown signal with timeout.
    
    Args:
        timeout: Maximum time to wait for shutdown signal (seconds)
    """
    global _shutdown_event
    
    if _shutdown_event is None:
        _shutdown_event = asyncio.Event()
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)
    
    try:
        await asyncio.wait_for(_shutdown_event.wait(), timeout=timeout)
        logger.info("Shutdown signal received")
    except asyncio.TimeoutError:
        logger.warning(f"Shutdown timeout ({timeout}s) exceeded, forcing shutdown")
    
    # Execute shutdown handlers
    await _execute_shutdown_handlers()


@asynccontextmanager
async def graceful_shutdown_context():
    """
    Context manager for graceful shutdown.
    
    Usage:
        async with graceful_shutdown_context():
            # Application code
            pass
    """
    global _shutdown_event
    
    _shutdown_event = asyncio.Event()
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)
    
    try:
        yield
    finally:
        logger.info("Graceful shutdown context exiting, executing handlers...")
        await _execute_shutdown_handlers()


class RequestDrainer:
    """
    Request drainer for graceful shutdown.
    
    Tracks in-flight requests and waits for them to complete.
    """
    
    def __init__(self, drain_timeout: float = 30.0):
        """
        Initialize request drainer.
        
        Args:
            drain_timeout: Maximum time to wait for requests to complete
        """
        self.in_flight_requests = 0
        self.drain_timeout = drain_timeout
        self._lock = asyncio.Lock()
    
    async def add_request(self):
        """Track a new in-flight request."""
        async with self._lock:
            self.in_flight_requests += 1
    
    async def remove_request(self):
        """Remove a completed request."""
        async with self._lock:
            self.in_flight_requests = max(0, self.in_flight_requests - 1)
    
    async def drain(self) -> bool:
        """
        Wait for all in-flight requests to complete.
        
        Returns:
            True if all requests completed, False if timeout
        """
        start_time = asyncio.get_event_loop().time()
        
        while self.in_flight_requests > 0:
            elapsed = asyncio.get_event_loop().time() - start_time
            
            if elapsed >= self.drain_timeout:
                logger.warning(
                    f"Drain timeout ({self.drain_timeout}s) exceeded. "
                    f"{self.in_flight_requests} requests still in flight"
                )
                return False
            
            await asyncio.sleep(0.1)
        
        logger.info("All requests drained successfully")
        return True
    
    def get_in_flight_count(self) -> int:
        """Get current number of in-flight requests."""
        return self.in_flight_requests


# Global request drainer instance
_request_drainer: Optional[RequestDrainer] = None


def get_request_drainer() -> RequestDrainer:
    """Get global request drainer instance."""
    global _request_drainer
    if _request_drainer is None:
        _request_drainer = RequestDrainer()
    return _request_drainer

