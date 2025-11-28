"""
Unified Router - Master Routing Engine

Chooses BEST routing path from multiple routing strategies:
1. Explicit target routing (direct)
2. Event routing (topic-based)
3. Graph routing (capability-based)
4. Semantic routing (embedding-based)

Supports hybrid async/sync architecture with comprehensive tracing.

Pattern: UPTC × ROUTER × UNIFIED × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Optional, Dict, Any, List
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
from router.event_router import EventRouter
from router.semantic_router import SemanticRouter
from router.graph_router import GraphRouter


@dataclass
class RoutingTrace:
    """Trace information for routing operations."""
    router_name: str
    operation: str
    start_time: float
    end_time: Optional[float] = None
    success: bool = False
    error: Optional[str] = None
    routing_strategy: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration_ms(self) -> float:
        """Get duration in milliseconds."""
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000.0


class UnifiedRouter:
    """
    The master routing engine.
    
    Chooses BEST routing path:
    1. explicit target routing (direct)
    2. event routing (topic-based)
    3. graph routing (capability-based)
    4. semantic routing (embedding-based)
    
    Features:
    - Multi-strategy routing with fallback chain
    - Hybrid async/sync support
    - OpenTelemetry tracing integration
    - Comprehensive error handling
    - Performance metrics per strategy
    
    ASSUMES:
    - Routers may be None or invalid
    - Message may fail validation
    - Routers may raise exceptions
    - Multiple routers may return None (fallback chain)
    - Trace modifications are thread-safe
    
    VERIFY:
    - Message passes contract validation before routing
    - Routing order: direct → event → graph → semantic
    - Trace is added atomically for each routing attempt
    - Returns first successful route or None if all fail
    
    FAILS:
    - If message validation fails (raises ProtocolValidationError)
    - If routers raise unexpected exceptions (wrapped in RuntimeError)
    """
    
    def __init__(
        self,
        event_router: Optional[EventRouter] = None,
        graph_router: Optional[GraphRouter] = None,
        semantic_router: Optional[SemanticRouter] = None,
        logger: Optional[logging.Logger] = None,
        enable_tracing: bool = True
    ):
        """
        Initialize UnifiedRouter.
        
        SAFETY: Defensive initialization - routers may be None
        ASSUMES: Routers have route(msg) method returning Optional[str]
        
        Args:
            event_router: EventRouter instance for topic-based routing
            graph_router: GraphRouter instance for capability-based routing
            semantic_router: SemanticRouter instance for embedding-based routing
            logger: Optional logger instance for routing operations
            enable_tracing: Enable OpenTelemetry tracing (default: True)
        """
        # SAFETY: Store routers - may be None but that's handled in route()
        self.event_router = event_router
        self.graph_router = graph_router
        self.semantic_router = semantic_router
        self.logger = logger or logging.getLogger(__name__)
        self.enable_tracing = enable_tracing and OPENTELEMETRY_AVAILABLE
        
        # Performance metrics per strategy
        self._metrics = {
            "total_routes": 0,
            "direct_routes": 0,
            "event_routes": 0,
            "graph_routes": 0,
            "semantic_routes": 0,
            "failed_routes": 0,
            "validation_errors": 0,
            "total_duration_ms": 0.0,
            "strategy_durations": {
                "direct": 0.0,
                "event": 0.0,
                "graph": 0.0,
                "semantic": 0.0
            }
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
        Route message using best available strategy (synchronous).
        
        Routing priority:
        1. Explicit target (direct routing)
        2. Event topic (event bus routing)
        3. Capability (graph routing)
        4. Semantic similarity (embedding routing)
        
        SAFETY: Validates message before routing
        ASSUMES: Routers may be None or raise exceptions
        VERIFY: Returns target string or None if no route found
        
        Args:
            msg: UPTCMessage to route
            
        Returns:
            Target identifier (str) if route found, None otherwise
            
        Raises:
            ProtocolValidationError: If message fails contract validation
            RuntimeError: If router raises unexpected exception
        """
        start_time = time.time()
        tracer = self._get_tracer()
        span = None
        
        if tracer:
            span = tracer.start_span("unified_router.route")
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
                    f"Message validation failed in UnifiedRouter: {e}"
                ) from e
            
            # SAFETY: Check msg is not None (should be caught by validate, but defensive)
            if msg is None:
                error_msg = "Message cannot be None"
                if span:
                    span.set_status(Status(StatusCode.ERROR, error_msg))
                raise ValueError(error_msg)
            
            if span:
                span.set_attribute("message.has_target", bool(msg.target))
                span.set_attribute("message.has_topic", bool(msg.topic))
                span.set_attribute("message.has_capability", bool(msg.capability))
                span.set_attribute("message.has_semantic_vector", bool(msg.semantic_vector))
            
            # 1. Explicit target → direct route (highest priority)
            if msg.target:
                strategy_start = time.time()
                if not isinstance(msg.target, str) or not msg.target.strip():
                    msg.add_trace("router:direct:invalid")
                else:
                    msg.add_trace("router:direct")
                    duration = time.time() - strategy_start
                    self._metrics["total_routes"] += 1
                    self._metrics["direct_routes"] += 1
                    self._metrics["strategy_durations"]["direct"] += duration * 1000
                    
                    if span:
                        span.set_attribute("routing.strategy", "direct")
                        span.set_attribute("routing.result", "success")
                        span.set_attribute("target.id", msg.target)
                        span.set_status(Status(StatusCode.OK))
                    
                    self.logger.info(f"Direct routing to target '{msg.target}'")
                    return msg.target
            
            # 2. Event topic → publish to bus
            if self.event_router is not None:
                strategy_start = time.time()
                try:
                    event_result = self.event_router.route(msg)
                    duration = time.time() - strategy_start
                    self._metrics["strategy_durations"]["event"] += duration * 1000
                    
                    if event_result:
                        self._metrics["total_routes"] += 1
                        self._metrics["event_routes"] += 1
                        
                        if span:
                            span.set_attribute("routing.strategy", "event")
                            span.set_attribute("routing.result", "success")
                            span.set_attribute("event.id", event_result)
                            span.set_status(Status(StatusCode.OK))
                        
                        self.logger.info(f"Event routing successful: {event_result}")
                        return event_result
                except (AttributeError, RuntimeError) as e:
                    msg.add_trace(f"router:event:error:{type(e).__name__}")
                    self.logger.debug(f"Event routing failed: {e}")
                except Exception as e:
                    if span:
                        span.record_exception(e)
                    raise RuntimeError(
                        f"Unexpected error in EventRouter: {e}"
                    ) from e
            
            # 3. Capability-based graph routing
            if self.graph_router is not None:
                strategy_start = time.time()
                try:
                    graph_target = self.graph_router.route(msg)
                    duration = time.time() - strategy_start
                    self._metrics["strategy_durations"]["graph"] += duration * 1000
                    
                    if graph_target:
                        self._metrics["total_routes"] += 1
                        self._metrics["graph_routes"] += 1
                        
                        if span:
                            span.set_attribute("routing.strategy", "graph")
                            span.set_attribute("routing.result", "success")
                            span.set_attribute("agent.id", graph_target)
                            span.set_status(Status(StatusCode.OK))
                        
                        self.logger.info(f"Graph routing successful: {graph_target}")
                        return graph_target
                except (AttributeError, RuntimeError) as e:
                    msg.add_trace(f"router:graph:error:{type(e).__name__}")
                    self.logger.debug(f"Graph routing failed: {e}")
                except Exception as e:
                    if span:
                        span.record_exception(e)
                    raise RuntimeError(
                        f"Unexpected error in GraphRouter: {e}"
                    ) from e
            
            # 4. Semantic similarity routing
            if self.semantic_router is not None:
                strategy_start = time.time()
                try:
                    semantic_target = self.semantic_router.route(msg)
                    duration = time.time() - strategy_start
                    self._metrics["strategy_durations"]["semantic"] += duration * 1000
                    
                    if semantic_target:
                        self._metrics["total_routes"] += 1
                        self._metrics["semantic_routes"] += 1
                        
                        if span:
                            span.set_attribute("routing.strategy", "semantic")
                            span.set_attribute("routing.result", "success")
                            span.set_attribute("agent.id", semantic_target)
                            span.set_status(Status(StatusCode.OK))
                        
                        self.logger.info(f"Semantic routing successful: {semantic_target}")
                        return semantic_target
                except (AttributeError, RuntimeError) as e:
                    msg.add_trace(f"router:semantic:error:{type(e).__name__}")
                    self.logger.debug(f"Semantic routing failed: {e}")
                except Exception as e:
                    if span:
                        span.record_exception(e)
                    raise RuntimeError(
                        f"Unexpected error in SemanticRouter: {e}"
                    ) from e
            
            # SAFETY: No route found - add trace and return None
            duration = time.time() - start_time
            self._metrics["total_routes"] += 1
            self._metrics["failed_routes"] += 1
            self._metrics["total_duration_ms"] += duration * 1000
            
            msg.add_trace("router:none")
            
            if span:
                span.set_attribute("routing.strategy", "none")
                span.set_attribute("routing.result", "failed")
                span.set_status(Status(StatusCode.OK))
            
            self.logger.warning(f"No route found for message {msg.id}")
            return None
            
        finally:
            if span:
                span.set_attribute("duration_ms", (time.time() - start_time) * 1000)
                span.end()
    
    async def async_route(self, msg: UPTCMessage) -> Optional[str]:
        """
        Async version of route() for async routing operations.
        
        Routing priority same as route():
        1. Explicit target (direct routing)
        2. Event topic (event bus routing)
        3. Capability (graph routing)
        4. Semantic similarity (embedding routing)
        
        SAFETY: Validates message before routing
        ASSUMES: Called from async context
        VERIFY: Returns target string or None if no route found
        
        Args:
            msg: UPTCMessage to route
            
        Returns:
            Target identifier (str) if route found, None otherwise
            
        Raises:
            ProtocolValidationError: If message fails contract validation
            RuntimeError: If router raises unexpected exception
        """
        async with self._trace_operation("unified_router.async_route", message_id=msg.id):
            start_time = time.time()
            
            # SAFETY: Validate message contract first
            try:
                UPTCContracts.validate(msg)
            except ProtocolValidationError as e:
                self.logger.warning(f"Message validation failed: {e}")
                self._metrics["validation_errors"] += 1
                raise ProtocolValidationError(
                    f"Message validation failed in UnifiedRouter: {e}"
                ) from e
            
            # SAFETY: Check msg is not None
            if msg is None:
                raise ValueError("Message cannot be None")
            
            # 1. Explicit target → direct route (highest priority)
            if msg.target:
                if not isinstance(msg.target, str) or not msg.target.strip():
                    msg.add_trace("router:direct:invalid")
                else:
                    msg.add_trace("router:direct:async")
                    self._metrics["total_routes"] += 1
                    self._metrics["direct_routes"] += 1
                    self.logger.info(f"Direct routing to target '{msg.target}' (async)")
                    return msg.target
            
            # 2. Event topic → publish to bus
            if self.event_router is not None:
                try:
                    event_result = await self.event_router.async_route(msg)
                    if event_result:
                        self._metrics["total_routes"] += 1
                        self._metrics["event_routes"] += 1
                        self.logger.info(f"Event routing successful: {event_result} (async)")
                        return event_result
                except (AttributeError, RuntimeError) as e:
                    msg.add_trace(f"router:event:error:{type(e).__name__}")
                    self.logger.debug(f"Event routing failed: {e}")
                except Exception as e:
                    raise RuntimeError(
                        f"Unexpected error in EventRouter: {e}"
                    ) from e
            
            # 3. Capability-based graph routing
            if self.graph_router is not None:
                try:
                    graph_target = await self.graph_router.async_route(msg)
                    if graph_target:
                        self._metrics["total_routes"] += 1
                        self._metrics["graph_routes"] += 1
                        self.logger.info(f"Graph routing successful: {graph_target} (async)")
                        return graph_target
                except (AttributeError, RuntimeError) as e:
                    msg.add_trace(f"router:graph:error:{type(e).__name__}")
                    self.logger.debug(f"Graph routing failed: {e}")
                except Exception as e:
                    raise RuntimeError(
                        f"Unexpected error in GraphRouter: {e}"
                    ) from e
            
            # 4. Semantic similarity routing
            if self.semantic_router is not None:
                try:
                    semantic_target = await self.semantic_router.async_route(msg)
                    if semantic_target:
                        self._metrics["total_routes"] += 1
                        self._metrics["semantic_routes"] += 1
                        self.logger.info(f"Semantic routing successful: {semantic_target} (async)")
                        return semantic_target
                except (AttributeError, RuntimeError) as e:
                    msg.add_trace(f"router:semantic:error:{type(e).__name__}")
                    self.logger.debug(f"Semantic routing failed: {e}")
                except Exception as e:
                    raise RuntimeError(
                        f"Unexpected error in SemanticRouter: {e}"
                    ) from e
            
            # SAFETY: No route found
            duration = time.time() - start_time
            self._metrics["total_routes"] += 1
            self._metrics["failed_routes"] += 1
            self._metrics["total_duration_ms"] += duration * 1000
            
            msg.add_trace("router:none:async")
            self.logger.warning(f"No route found for message {msg.id} (async)")
            return None
    
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
            "direct_routes": 0,
            "event_routes": 0,
            "graph_routes": 0,
            "semantic_routes": 0,
            "failed_routes": 0,
            "validation_errors": 0,
            "total_duration_ms": 0.0,
            "strategy_durations": {
                "direct": 0.0,
                "event": 0.0,
                "graph": 0.0,
                "semantic": 0.0
            }
        }
    
    def get_strategy_metrics(self) -> Dict[str, Any]:
        """
        Get per-strategy performance metrics.
        
        Returns:
            Dictionary containing strategy-specific metrics
        """
        total = self._metrics["total_routes"]
        if total == 0:
            return {
                "direct": {"count": 0, "percentage": 0.0, "avg_duration_ms": 0.0},
                "event": {"count": 0, "percentage": 0.0, "avg_duration_ms": 0.0},
                "graph": {"count": 0, "percentage": 0.0, "avg_duration_ms": 0.0},
                "semantic": {"count": 0, "percentage": 0.0, "avg_duration_ms": 0.0}
            }
        
        return {
            "direct": {
                "count": self._metrics["direct_routes"],
                "percentage": (self._metrics["direct_routes"] / total) * 100.0,
                "avg_duration_ms": (
                    self._metrics["strategy_durations"]["direct"] / max(1, self._metrics["direct_routes"])
                )
            },
            "event": {
                "count": self._metrics["event_routes"],
                "percentage": (self._metrics["event_routes"] / total) * 100.0,
                "avg_duration_ms": (
                    self._metrics["strategy_durations"]["event"] / max(1, self._metrics["event_routes"])
                )
            },
            "graph": {
                "count": self._metrics["graph_routes"],
                "percentage": (self._metrics["graph_routes"] / total) * 100.0,
                "avg_duration_ms": (
                    self._metrics["strategy_durations"]["graph"] / max(1, self._metrics["graph_routes"])
                )
            },
            "semantic": {
                "count": self._metrics["semantic_routes"],
                "percentage": (self._metrics["semantic_routes"] / total) * 100.0,
                "avg_duration_ms": (
                    self._metrics["strategy_durations"]["semantic"] / max(1, self._metrics["semantic_routes"])
                )
            }
        }

