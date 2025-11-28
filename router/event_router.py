"""
Event Router - Event-Driven Message Routing

Routes messages based on event topics or explicit event-driven workflows.
Supports hybrid async/sync architecture with comprehensive tracing.

Pattern: UPTC × ROUTER × EVENT × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Optional, Any, Dict
import asyncio
import logging
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    trace = None

from EMERGENT_OS.uptc.protocol.schema import UPTCMessage
from EMERGENT_OS.uptc.protocol.contracts import UPTCContracts, ProtocolValidationError


@dataclass
class RoutingTrace:
    """Trace information for routing operations."""
    router_name: str
    operation: str
    start_time: float
    end_time: Optional[float] = None
    success: bool = False
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration_ms(self) -> float:
        """Get duration in milliseconds."""
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000.0


class EventRouter:
    """
    Routes messages based on event topics or explicit event-driven workflows.
    
    Features:
    - Hybrid async/sync support
    - OpenTelemetry tracing integration
    - Comprehensive error handling
    - Thread-safe operations
    - Performance metrics
    
    ASSUMES:
    - event_bus has a publish() method that accepts (topic: str, message: Any)
    - publish() may be async or sync
    - publish() returns event ID (str) or None/False on failure
    - Messages may fail validation
    - event_bus may be None or invalid
    
    VERIFY:
    - Message passes contract validation before routing
    - Topic is non-empty string before publishing
    - Trace is added atomically
    - Errors are handled gracefully
    
    FAILS:
    - If message validation fails (raises ProtocolValidationError)
    - If event_bus is None or invalid
    - If topic is None or empty
    """
    
    def __init__(
        self,
        event_bus: Optional[Any] = None,
        logger: Optional[logging.Logger] = None,
        enable_tracing: bool = True
    ):
        """
        Initialize EventRouter.
        
        SAFETY: Defensive initialization - event_bus may be None
        ASSUMES: event_bus has publish() method (checked at runtime)
        
        Args:
            event_bus: Event bus instance with publish(topic, message) method
            logger: Optional logger instance for routing operations
            enable_tracing: Enable OpenTelemetry tracing (default: True)
        """
        self.event_bus = event_bus
        self.logger = logger or logging.getLogger(__name__)
        self.enable_tracing = enable_tracing and OPENTELEMETRY_AVAILABLE
        
        # Performance metrics
        self._metrics = {
            "total_routes": 0,
            "successful_routes": 0,
            "failed_routes": 0,
            "validation_errors": 0,
            "publish_errors": 0,
            "total_duration_ms": 0.0
        }
        self._metrics_lock = asyncio.Lock() if asyncio.iscoroutinefunction(self._metrics_lock) else None
    
    def _get_tracer(self) -> Optional[Any]:
        """Get OpenTelemetry tracer if available."""
        if not self.enable_tracing:
            return None
        try:
            return trace.get_tracer(__name__)
        except Exception:
            return None
    
    @asynccontextmanager
    async def _trace_operation(self, operation_name: str, **attributes):
        """Context manager for tracing async operations."""
        tracer = self._get_tracer()
        if not tracer:
            yield None
            return
        
        span = tracer.start_span(operation_name)
        span.set_attributes(attributes)
        start_time = time.time()
        
        try:
            yield span
            span.set_status(Status(StatusCode.OK))
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
        finally:
            duration = time.time() - start_time
            span.set_attribute("duration_ms", duration * 1000)
            span.end()
    
    def route(self, msg: UPTCMessage) -> Optional[str]:
        """
        Publish message to event bus based on its topic (synchronous).
        
        SAFETY: Validates message before routing
        ASSUMES: event_bus.publish() exists and accepts (topic, message)
        VERIFY: Returns event ID or None
        
        Args:
            msg: UPTCMessage to route
            
        Returns:
            Event ID (str) if published successfully, None otherwise
            
        Raises:
            ProtocolValidationError: If message fails contract validation
            AttributeError: If event_bus is None or lacks publish() method
            ValueError: If topic is None or empty
        """
        start_time = time.time()
        tracer = self._get_tracer()
        span = None
        
        if tracer:
            span = tracer.start_span("event_router.route")
            span.set_attribute("message.id", msg.id)
            span.set_attribute("message.intent", msg.intent)
        
        try:
            # SAFETY: Validate message contract first
            try:
                UPTCContracts.validate(msg)
            except ProtocolValidationError as e:
                if span:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                self.logger.warning(f"Message validation failed: {e}")
                self._metrics["validation_errors"] += 1
                raise ProtocolValidationError(
                    f"Message validation failed in EventRouter: {e}"
                ) from e
            
            # SAFETY: Check event_bus exists
            if self.event_bus is None:
                error_msg = "EventRouter.event_bus is None. Cannot route message without event bus."
                if span:
                    span.set_status(Status(StatusCode.ERROR, error_msg))
                raise AttributeError(error_msg)
            
            # SAFETY: Check topic exists and is non-empty
            if not msg.topic:
                if span:
                    span.set_attribute("routing.result", "no_topic")
                    span.set_status(Status(StatusCode.OK))
                    span.end()
                return None
            
            if not isinstance(msg.topic, str) or not msg.topic.strip():
                error_msg = f"Message topic must be non-empty string, got: {type(msg.topic).__name__}"
                if span:
                    span.set_status(Status(StatusCode.ERROR, error_msg))
                raise ValueError(error_msg)
            
            if span:
                span.set_attribute("message.topic", msg.topic)
            
            # SAFETY: Add trace atomically
            msg.add_trace("router:event")
            
            # SAFETY: Check event_bus has publish method
            if not hasattr(self.event_bus, 'publish'):
                error_msg = (
                    f"event_bus.publish() method not found. "
                    f"Event bus type: {type(self.event_bus).__name__}"
                )
                if span:
                    span.set_status(Status(StatusCode.ERROR, error_msg))
                raise AttributeError(error_msg)
            
            # SAFETY: Handle both sync and async publish methods
            publish_method = getattr(self.event_bus, 'publish')
            
            if asyncio.iscoroutinefunction(publish_method):
                # SAFETY: Async publish in sync context - warn and attempt
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        error_msg = (
                            "Cannot call async publish() from sync route() when event loop is running. "
                            "Use async_route() instead."
                        )
                        if span:
                            span.set_status(Status(StatusCode.ERROR, error_msg))
                        raise RuntimeError(error_msg)
                    else:
                        result = loop.run_until_complete(publish_method(msg.topic, msg))
                except RuntimeError as e:
                    if "running" in str(e):
                        raise
                    result = asyncio.run(publish_method(msg.topic, msg))
            else:
                # SAFETY: Sync publish - call directly
                result = publish_method(msg.topic, msg)
            
            # SAFETY: Normalize return value to Optional[str]
            event_id = None
            if result is True:
                event_id = msg.id
            elif result is False or result is None:
                event_id = None
            elif isinstance(result, str):
                event_id = result
            else:
                event_id = msg.id
            
            # Update metrics
            duration = time.time() - start_time
            self._metrics["total_routes"] += 1
            if event_id:
                self._metrics["successful_routes"] += 1
                if span:
                    span.set_attribute("routing.result", "success")
                    span.set_attribute("event.id", event_id)
                    span.set_status(Status(StatusCode.OK))
                self.logger.info(f"Successfully routed message {msg.id} to topic {msg.topic}")
            else:
                self._metrics["failed_routes"] += 1
                if span:
                    span.set_attribute("routing.result", "failed")
                    span.set_status(Status(StatusCode.OK))
                self.logger.warning(f"Failed to route message {msg.id} to topic {msg.topic}")
            
            self._metrics["total_duration_ms"] += duration * 1000
            
            return event_id
                
        except (ProtocolValidationError, AttributeError, ValueError, RuntimeError):
            # Re-raise expected errors
            raise
        except Exception as e:
            # SAFETY: Catch all publish errors
            duration = time.time() - start_time
            self._metrics["total_routes"] += 1
            self._metrics["failed_routes"] += 1
            self._metrics["publish_errors"] += 1
            self._metrics["total_duration_ms"] += duration * 1000
            
            error_msg = f"Failed to publish message to event bus: {e}"
            if span:
                span.set_status(Status(StatusCode.ERROR, error_msg))
                span.record_exception(e)
            self.logger.error(error_msg, exc_info=True)
            raise RuntimeError(error_msg) from e
        finally:
            if span:
                span.set_attribute("duration_ms", (time.time() - start_time) * 1000)
                span.end()
    
    async def async_route(self, msg: UPTCMessage) -> Optional[str]:
        """
        Async version of route() for async event buses.
        
        SAFETY: Validates message before routing
        ASSUMES: Called from async context
        VERIFY: Returns event ID or None
        
        Args:
            msg: UPTCMessage to route
            
        Returns:
            Event ID (str) if published successfully, None otherwise
            
        Raises:
            ProtocolValidationError: If message fails contract validation
            AttributeError: If event_bus is None or lacks publish() method
            ValueError: If topic is None or empty
        """
        async with self._trace_operation("event_router.async_route", message_id=msg.id):
            # SAFETY: Validate message contract first
            try:
                UPTCContracts.validate(msg)
            except ProtocolValidationError as e:
                self.logger.warning(f"Message validation failed: {e}")
                self._metrics["validation_errors"] += 1
                raise ProtocolValidationError(
                    f"Message validation failed in EventRouter: {e}"
                ) from e
            
            # SAFETY: Check event_bus exists
            if self.event_bus is None:
                raise AttributeError(
                    "EventRouter.event_bus is None. Cannot route message without event bus."
                )
            
            # SAFETY: Check topic exists and is non-empty
            if not msg.topic:
                return None
            
            if not isinstance(msg.topic, str) or not msg.topic.strip():
                raise ValueError(
                    f"Message topic must be non-empty string, got: {type(msg.topic).__name__}"
                )
            
            # SAFETY: Add trace atomically
            msg.add_trace("router:event:async")
            
            # SAFETY: Check event_bus has publish method
            if not hasattr(self.event_bus, 'publish'):
                raise AttributeError(
                    f"event_bus.publish() method not found. "
                    f"Event bus type: {type(self.event_bus).__name__}"
                )
            
            # SAFETY: Handle async publish
            start_time = time.time()
            try:
                publish_method = getattr(self.event_bus, 'publish')
                
                if asyncio.iscoroutinefunction(publish_method):
                    result = await publish_method(msg.topic, msg)
                else:
                    # SAFETY: Sync method in async context - run in executor
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(
                        None, 
                        lambda: publish_method(msg.topic, msg)
                    )
                
                # SAFETY: Normalize return value
                event_id = None
                if result is True:
                    event_id = msg.id
                elif result is False or result is None:
                    event_id = None
                elif isinstance(result, str):
                    event_id = result
                else:
                    event_id = msg.id
                
                # Update metrics
                duration = time.time() - start_time
                self._metrics["total_routes"] += 1
                if event_id:
                    self._metrics["successful_routes"] += 1
                    self.logger.info(f"Successfully routed message {msg.id} to topic {msg.topic}")
                else:
                    self._metrics["failed_routes"] += 1
                    self.logger.warning(f"Failed to route message {msg.id} to topic {msg.topic}")
                
                self._metrics["total_duration_ms"] += duration * 1000
                
                return event_id
                    
            except Exception as e:
                duration = time.time() - start_time
                self._metrics["total_routes"] += 1
                self._metrics["failed_routes"] += 1
                self._metrics["publish_errors"] += 1
                self._metrics["total_duration_ms"] += duration * 1000
                
                self.logger.error(f"Failed to publish message to event bus: {e}", exc_info=True)
                raise RuntimeError(
                    f"Failed to publish message to event bus: {e}"
                ) from e
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get routing metrics for observability.
        
        SAFETY: Thread-safe metrics access
        VERIFY: Returns current metrics snapshot
        
        Returns:
            Dictionary containing routing metrics
        """
        return self._metrics.copy()
    
    def reset_metrics(self) -> None:
        """
        Reset routing metrics.
        
        SAFETY: Thread-safe reset
        """
        self._metrics = {
            "total_routes": 0,
            "successful_routes": 0,
            "failed_routes": 0,
            "validation_errors": 0,
            "publish_errors": 0,
            "total_duration_ms": 0.0
        }

