"""
Graph Router - Capability-Based Message Routing

Uses a capability graph to find appropriate agent/module targets.
Supports hybrid async/sync architecture with comprehensive tracing.

Pattern: UPTC × ROUTER × GRAPH × CAPABILITY × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Optional, Dict, Any
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
from EMERGENT_OS.uptc.registry.capability_graph import CapabilityGraph


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


class GraphRouter:
    """
    Uses a capability graph to find appropriate agent/module targets.
    
    Features:
    - Capability-based routing via graph resolution
    - Hybrid async/sync support
    - OpenTelemetry tracing integration
    - Comprehensive error handling
    - Performance metrics
    
    ASSUMES:
    - graph has a resolve(capability: str) -> Optional[str] method
    - graph.resolve() may return None if capability not found
    - Messages may fail validation
    - Messages may not have capability field set
    - graph may be None or invalid
    
    VERIFY:
    - Message passes contract validation before routing
    - Capability is non-empty string before resolution
    - Trace is added atomically
    - Returns agent/module ID or None
    
    FAILS:
    - If message validation fails (raises ProtocolValidationError)
    - If graph is None or invalid
    - If capability is None or empty (returns None, not error)
    """
    
    def __init__(
        self,
        graph: CapabilityGraph,
        logger: Optional[logging.Logger] = None,
        enable_tracing: bool = True
    ):
        """
        Initialize GraphRouter.
        
        SAFETY: Defensive initialization - graph may be None
        ASSUMES: graph has resolve() method (checked at runtime)
        
        Args:
            graph: CapabilityGraph instance for capability resolution
            logger: Optional logger instance for routing operations
            enable_tracing: Enable OpenTelemetry tracing (default: True)
        """
        self.graph = graph
        self.logger = logger or logging.getLogger(__name__)
        self.enable_tracing = enable_tracing and OPENTELEMETRY_AVAILABLE
        
        # Performance metrics
        self._metrics = {
            "total_routes": 0,
            "successful_routes": 0,
            "failed_routes": 0,
            "no_capability": 0,
            "validation_errors": 0,
            "resolution_errors": 0,
            "total_duration_ms": 0.0
        }
    
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
        Route message based on capability graph resolution (synchronous).
        
        SAFETY: Validates message before routing
        ASSUMES: graph.resolve() exists and accepts capability string
        VERIFY: Returns agent/module ID or None
        
        Args:
            msg: UPTCMessage to route
            
        Returns:
            Agent/module ID (str) if capability resolved, None otherwise
            
        Raises:
            ProtocolValidationError: If message fails contract validation
            AttributeError: If graph is None or lacks resolve() method
            ValueError: If capability is invalid type
        """
        start_time = time.time()
        tracer = self._get_tracer()
        span = None
        
        if tracer:
            span = tracer.start_span("graph_router.route")
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
                    f"Message validation failed in GraphRouter: {e}"
                ) from e
            
            # SAFETY: Check graph exists
            if self.graph is None:
                error_msg = "GraphRouter.graph is None. Cannot route message without capability graph."
                if span:
                    span.set_status(Status(StatusCode.ERROR, error_msg))
                raise AttributeError(error_msg)
            
            # SAFETY: Check capability exists
            if not msg.capability:
                if span:
                    span.set_attribute("routing.result", "no_capability")
                    span.set_status(Status(StatusCode.OK))
                    span.end()
                self.logger.debug("No capability in message, cannot route via graph")
                self._metrics["no_capability"] += 1
                return None
            
            # SAFETY: Validate capability is string
            if not isinstance(msg.capability, str):
                error_msg = f"Message capability must be string, got: {type(msg.capability).__name__}"
                if span:
                    span.set_status(Status(StatusCode.ERROR, error_msg))
                raise ValueError(error_msg)
            
            # SAFETY: Check capability is non-empty after stripping
            capability = msg.capability.strip()
            if not capability:
                if span:
                    span.set_attribute("routing.result", "empty_capability")
                    span.set_status(Status(StatusCode.OK))
                    span.end()
                self.logger.debug("Empty capability in message")
                self._metrics["no_capability"] += 1
                return None
            
            if span:
                span.set_attribute("message.capability", capability)
            
            # SAFETY: Add trace atomically
            msg.add_trace("router:graph")
            
            # SAFETY: Check graph has resolve method
            if not hasattr(self.graph, 'resolve'):
                error_msg = (
                    f"graph.resolve() method not found. "
                    f"Graph type: {type(self.graph).__name__}"
                )
                if span:
                    span.set_status(Status(StatusCode.ERROR, error_msg))
                raise AttributeError(error_msg)
            
            # SAFETY: Query the graph for best match
            try:
                agent_id = self.graph.resolve(capability)
                
                duration = time.time() - start_time
                self._metrics["total_routes"] += 1
                self._metrics["total_duration_ms"] += duration * 1000
                
                if agent_id:
                    self._metrics["successful_routes"] += 1
                    if span:
                        span.set_attribute("routing.result", "success")
                        span.set_attribute("agent.id", agent_id)
                        span.set_status(Status(StatusCode.OK))
                    self.logger.info(
                        f"Successfully routed message {msg.id} via capability '{capability}' "
                        f"to agent '{agent_id}'"
                    )
                else:
                    self._metrics["failed_routes"] += 1
                    if span:
                        span.set_attribute("routing.result", "not_found")
                        span.set_status(Status(StatusCode.OK))
                    self.logger.debug(
                        f"No agent found for capability '{capability}'"
                    )
                
                return agent_id
                
            except Exception as e:
                duration = time.time() - start_time
                self._metrics["total_routes"] += 1
                self._metrics["failed_routes"] += 1
                self._metrics["resolution_errors"] += 1
                self._metrics["total_duration_ms"] += duration * 1000
                
                error_msg = f"Failed to resolve capability '{capability}' in graph: {e}"
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
        Async version of route() for async graph operations.
        
        SAFETY: Validates message before routing
        ASSUMES: Called from async context
        VERIFY: Returns agent/module ID or None
        
        Args:
            msg: UPTCMessage to route
            
        Returns:
            Agent/module ID (str) if capability resolved, None otherwise
            
        Raises:
            ProtocolValidationError: If message fails contract validation
            AttributeError: If graph is None or lacks resolve() method
            ValueError: If capability is invalid type
        """
        async with self._trace_operation("graph_router.async_route", message_id=msg.id):
            # SAFETY: Validate message contract first
            try:
                UPTCContracts.validate(msg)
            except ProtocolValidationError as e:
                self.logger.warning(f"Message validation failed: {e}")
                self._metrics["validation_errors"] += 1
                raise ProtocolValidationError(
                    f"Message validation failed in GraphRouter: {e}"
                ) from e
            
            # SAFETY: Check graph exists
            if self.graph is None:
                raise AttributeError(
                    "GraphRouter.graph is None. Cannot route message without capability graph."
                )
            
            # SAFETY: Check capability exists
            if not msg.capability:
                self.logger.debug("No capability in message, cannot route via graph")
                self._metrics["no_capability"] += 1
                return None
            
            # SAFETY: Validate capability is string
            if not isinstance(msg.capability, str):
                raise ValueError(
                    f"Message capability must be string, got: {type(msg.capability).__name__}"
                )
            
            # SAFETY: Check capability is non-empty after stripping
            capability = msg.capability.strip()
            if not capability:
                self.logger.debug("Empty capability in message")
                self._metrics["no_capability"] += 1
                return None
            
            # SAFETY: Add trace atomically
            msg.add_trace("router:graph:async")
            
            # SAFETY: Check graph has resolve method
            if not hasattr(self.graph, 'resolve'):
                raise AttributeError(
                    f"graph.resolve() method not found. "
                    f"Graph type: {type(self.graph).__name__}"
                )
            
            # SAFETY: Query the graph for best match
            start_time = time.time()
            try:
                # For now, resolve() is sync, but we run it in executor for async compatibility
                import asyncio
                loop = asyncio.get_event_loop()
                agent_id = await loop.run_in_executor(
                    None,
                    lambda: self.graph.resolve(capability)
                )
                
                duration = time.time() - start_time
                self._metrics["total_routes"] += 1
                self._metrics["total_duration_ms"] += duration * 1000
                
                if agent_id:
                    self._metrics["successful_routes"] += 1
                    self.logger.info(
                        f"Successfully routed message {msg.id} via capability '{capability}' "
                        f"to agent '{agent_id}' (async)"
                    )
                else:
                    self._metrics["failed_routes"] += 1
                    self.logger.debug(
                        f"No agent found for capability '{capability}'"
                    )
                
                return agent_id
                
            except Exception as e:
                duration = time.time() - start_time
                self._metrics["total_routes"] += 1
                self._metrics["failed_routes"] += 1
                self._metrics["resolution_errors"] += 1
                self._metrics["total_duration_ms"] += duration * 1000
                
                self.logger.error(
                    f"Failed to resolve capability '{capability}' in graph: {e}",
                    exc_info=True
                )
                raise RuntimeError(
                    f"Failed to resolve capability '{capability}' in graph: {e}"
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
            "no_capability": 0,
            "validation_errors": 0,
            "resolution_errors": 0,
            "total_duration_ms": 0.0
        }

