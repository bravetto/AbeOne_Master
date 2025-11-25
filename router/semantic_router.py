"""
Semantic Router - FAISS-Compatible Embedding-Based Agent Selection

Selects best target agent/module via embedding similarity using FAISS for
high-performance vector search. Supports hybrid async/sync architecture with
comprehensive tracing.

Pattern: UPTC × ROUTER × SEMANTIC × FAISS × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Optional, List, Tuple, Dict, Any
import threading
import logging
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    faiss = None
    np = None

try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    trace = None

from EMERGENT_OS.uptc.protocol.schema import UPTCMessage
from EMERGENT_OS.uptc.protocol.contracts import UPTCContracts
from EMERGENT_OS.uptc.utils.embeddings import EmbeddingEngine

# SAFETY: Type alias for capability index structure
# {capability: {agent: vector}}
CapabilityIndex = Dict[str, Dict[str, List[float]]]


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


class SemanticRouter:
    """
    Selects best target agent/module via embedding similarity using FAISS.
    
    Features:
    - FAISS-accelerated vector search (IndexFlatIP for cosine similarity)
    - Hybrid async/sync support
    - OpenTelemetry tracing integration
    - Fallback to EmbeddingEngine if FAISS unavailable
    - Thread-safe operations
    - Performance metrics
    
    ASSUMES:
    - capability_index structure: {capability: {agent: vector}}
    - Vectors in capability_index match semantic_vector dimensions
    - EmbeddingEngine.similarity() returns comparable scores
    - capability_index may be modified concurrently (thread-safe access needed)
    - FAISS index uses IndexFlatIP (inner product) for cosine similarity
    
    VERIFY:
    - Returns agent only if similarity >= threshold
    - Handles empty/malformed indices gracefully
    - Validates vector dimensions before comparison
    - Thread-safe iteration over capability_index
    - FAISS search returns valid results
    
    FAILS:
    - If semantic_vector dimensions don't match capability vectors
    - If similarity computation raises exception
    - If capability_index structure is malformed
    - If FAISS index is corrupted (falls back to EmbeddingEngine)
    """
    
    def __init__(
        self,
        embedding_engine: EmbeddingEngine,
        capability_index: CapabilityIndex,
        similarity_threshold: float = 0.5,
        logger: Optional[logging.Logger] = None,
        enable_faiss: bool = True,
        enable_tracing: bool = True,
        vector_dimension: Optional[int] = None
    ):
        """
        Initialize SemanticRouter.
        
        SAFETY: Validates inputs and sets up thread safety
        ASSUMES: embedding_engine implements similarity() method
        VERIFY: Router ready for routing operations
        
        Args:
            embedding_engine: Engine for computing vector similarity (fallback)
            capability_index: Index mapping capabilities to agents and vectors
            similarity_threshold: Minimum similarity score to route (default: 0.5)
            logger: Optional logger for routing decisions
            enable_faiss: Enable FAISS acceleration (default: True)
            enable_tracing: Enable OpenTelemetry tracing (default: True)
            vector_dimension: Vector dimension for FAISS index (auto-detected if None)
            
        Raises:
            TypeError: If embedding_engine is not EmbeddingEngine instance
            ValueError: If similarity_threshold not in [0.0, 1.0]
        """
        # SAFETY: Type validation
        if not isinstance(embedding_engine, EmbeddingEngine):
            raise TypeError(
                f"embedding_engine must be EmbeddingEngine instance, "
                f"got {type(embedding_engine).__name__}"
            )
        
        # SAFETY: Threshold validation
        if not isinstance(similarity_threshold, (int, float)):
            raise TypeError(
                f"similarity_threshold must be numeric, "
                f"got {type(similarity_threshold).__name__}"
            )
        if not 0.0 <= similarity_threshold <= 1.0:
            raise ValueError(
                f"similarity_threshold must be in [0.0, 1.0], "
                f"got {similarity_threshold}"
            )
        
        self.embedding_engine = embedding_engine
        self.capability_index = capability_index
        self.similarity_threshold = float(similarity_threshold)
        self.logger = logger or logging.getLogger(__name__)
        self.enable_faiss = enable_faiss and FAISS_AVAILABLE
        self.enable_tracing = enable_tracing and OPENTELEMETRY_AVAILABLE
        
        # SAFETY: Thread safety for index access
        self._index_lock = threading.RLock()
        
        # FAISS index setup
        self.faiss_index: Optional[Any] = None
        self.faiss_id_map: Dict[int, Tuple[str, str]] = {}  # FAISS idx -> (capability, agent)
        self._vector_dimension = vector_dimension
        
        if self.enable_faiss:
            self._build_faiss_index()
        
        # SAFETY: Routing metrics for observability
        self.routing_metrics = {
            "total_routes": 0,
            "successful_routes": 0,
            "threshold_rejections": 0,
            "dimension_mismatches": 0,
            "empty_index_routes": 0,
            "faiss_routes": 0,
            "fallback_routes": 0,
            "errors": 0
        }
        self._metrics_lock = threading.RLock()
    
    def _build_faiss_index(self) -> None:
        """
        Build FAISS index from capability_index.
        
        SAFETY: Validates vectors before indexing
        ASSUMES: capability_index structure is valid
        VERIFY: FAISS index created successfully
        """
        if not self.enable_faiss:
            return
        
        try:
            # Collect all vectors and determine dimension
            vectors = []
            id_mapping = []
            
            with self._index_lock:
                for capability, entries in self.capability_index.items():
                    if not isinstance(entries, dict):
                        continue
                    
                    for agent, vector in entries.items():
                        if not isinstance(vector, list) or len(vector) == 0:
                            continue
                        
                        # Determine dimension from first vector
                        if self._vector_dimension is None:
                            self._vector_dimension = len(vector)
                        
                        if len(vector) != self._vector_dimension:
                            self.logger.warning(
                                f"Skipping vector for {capability}:{agent} - "
                                f"dimension mismatch: {len(vector)} != {self._vector_dimension}"
                            )
                            continue
                        
                        vectors.append(vector)
                        id_mapping.append((capability, agent))
            
            if not vectors:
                self.logger.warning("No valid vectors found for FAISS index")
                return
            
            # Create FAISS index (IndexFlatIP for cosine similarity)
            dimension = self._vector_dimension
            self.faiss_index = faiss.IndexFlatIP(dimension)
            
            # Convert vectors to numpy array and normalize
            vectors_array = np.array(vectors, dtype=np.float32)
            faiss.normalize_L2(vectors_array)
            
            # Add vectors to index
            self.faiss_index.add(vectors_array)
            
            # Build ID mapping
            for idx, (cap, agent) in enumerate(id_mapping):
                self.faiss_id_map[idx] = (cap, agent)
            
            self.logger.info(
                f"Built FAISS index with {len(vectors)} vectors (dimension: {dimension})"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to build FAISS index: {e}", exc_info=True)
            self.faiss_index = None
            self.enable_faiss = False
    
    def _get_tracer(self) -> Optional[Any]:
        """Get OpenTelemetry tracer if available."""
        if not self.enable_tracing:
            return None
        try:
            return trace.get_tracer(__name__)
        except Exception:
            return None
    
    def route(self, msg: UPTCMessage) -> Optional[str]:
        """
        Route message to best matching agent based on semantic similarity.
        
        Uses FAISS for fast vector search if available, falls back to EmbeddingEngine.
        
        SAFETY: Defensive validation, error handling, threshold enforcement
        ASSUMES: msg may have None/malformed semantic_vector
        VERIFY: Returns agent only if similarity >= threshold
        FAILS: Returns None if no suitable agent found
        
        Args:
            msg: UPTCMessage with semantic_vector for routing
            
        Returns:
            Agent identifier if suitable match found, None otherwise
            
        PERF: O(log n) with FAISS, O(n*m) without where n=vectors, m=capabilities
        """
        start_time = time.time()
        tracer = self._get_tracer()
        span = None
        
        if tracer:
            span = tracer.start_span("semantic_router.route")
            span.set_attribute("message.id", msg.id)
            span.set_attribute("message.intent", msg.intent)
        
        try:
            # SAFETY: Contract validation first
            try:
                UPTCContracts.validate(msg)
            except Exception as e:
                if span:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                self.logger.warning(f"Message validation failed: {e}")
                with self._metrics_lock:
                    self.routing_metrics["errors"] += 1
                return None
            
            # SAFETY: Early return if no semantic vector
            if not msg.semantic_vector:
                if span:
                    span.set_attribute("routing.result", "no_semantic_vector")
                    span.set_status(Status(StatusCode.OK))
                    span.end()
                self.logger.debug("No semantic_vector in message, cannot route semantically")
                return None
            
            # SAFETY: Check capability_index exists and is non-empty
            with self._index_lock:
                if not self.capability_index:
                    if span:
                        span.set_attribute("routing.result", "empty_index")
                        span.set_status(Status(StatusCode.OK))
                        span.end()
                    self.logger.debug("capability_index is empty")
                    with self._metrics_lock:
                        self.routing_metrics["empty_index_routes"] += 1
                    return None
            
            # SAFETY: Validate semantic_vector dimensions
            msg_vector_dim = len(msg.semantic_vector)
            if msg_vector_dim == 0:
                if span:
                    span.set_status(Status(StatusCode.ERROR, "Empty semantic vector"))
                    span.end()
                self.logger.warning("semantic_vector is empty")
                with self._metrics_lock:
                    self.routing_metrics["errors"] += 1
                return None
            
            if span:
                span.set_attribute("vector.dimension", msg_vector_dim)
                span.set_attribute("faiss.enabled", self.enable_faiss and self.faiss_index is not None)
            
            # Add trace
            msg.add_trace("router:semantic")
            
            # Try FAISS search first if available
            if self.enable_faiss and self.faiss_index is not None:
                try:
                    result = self._route_with_faiss(msg, msg_vector_dim, span)
                    if result:
                        with self._metrics_lock:
                            self.routing_metrics["faiss_routes"] += 1
                        return result
                except Exception as e:
                    self.logger.warning(f"FAISS routing failed, falling back to EmbeddingEngine: {e}")
                    with self._metrics_lock:
                        self.routing_metrics["fallback_routes"] += 1
            
            # Fallback to EmbeddingEngine-based routing
            result = self._route_with_engine(msg, msg_vector_dim, span)
            
            if result:
                with self._metrics_lock:
                    self.routing_metrics["fallback_routes"] += 1
            
            return result
            
        finally:
            if span:
                duration = time.time() - start_time
                span.set_attribute("duration_ms", duration * 1000)
                span.end()
    
    def _route_with_faiss(
        self,
        msg: UPTCMessage,
        msg_vector_dim: int,
        span: Optional[Any]
    ) -> Optional[str]:
        """
        Route using FAISS index.
        
        SAFETY: Validates vector dimensions and handles FAISS errors
        ASSUMES: FAISS index is initialized and valid
        VERIFY: Returns agent if similarity >= threshold
        """
        if self._vector_dimension and msg_vector_dim != self._vector_dimension:
            if span:
                span.set_attribute("routing.result", "dimension_mismatch")
            self.logger.debug(
                f"Dimension mismatch: msg_vector={msg_vector_dim}, "
                f"index_dimension={self._vector_dimension}"
            )
            with self._metrics_lock:
                self.routing_metrics["dimension_mismatches"] += 1
            return None
        
        try:
            # Convert message vector to numpy array
            query_vector = np.array([msg.semantic_vector], dtype=np.float32)
            faiss.normalize_L2(query_vector)
            
            # Search FAISS index (top 1 result)
            k = min(1, self.faiss_index.ntotal)
            if k == 0:
                return None
            
            distances, indices = self.faiss_index.search(query_vector, k)
            
            if len(indices[0]) == 0 or indices[0][0] == -1:
                return None
            
            # Get best match
            best_idx = indices[0][0]
            best_score = float(distances[0][0])
            
            # Convert inner product to similarity (already normalized, so score is cosine similarity)
            # IndexFlatIP returns values in [-1, 1] for normalized vectors
            similarity = (best_score + 1.0) / 2.0  # Normalize to [0, 1]
            
            if span:
                span.set_attribute("similarity.score", similarity)
                span.set_attribute("similarity.best_score", best_score)
            
            # Check threshold
            if similarity < self.similarity_threshold:
                if span:
                    span.set_attribute("routing.result", "below_threshold")
                self.logger.debug(
                    f"Best match score {similarity:.3f} below threshold "
                    f"{self.similarity_threshold:.3f}"
                )
                with self._metrics_lock:
                    self.routing_metrics["total_routes"] += 1
                    self.routing_metrics["threshold_rejections"] += 1
                return None
            
            # Get agent ID from mapping
            if best_idx not in self.faiss_id_map:
                return None
            
            capability, agent_id = self.faiss_id_map[best_idx]
            
            if span:
                span.set_attribute("routing.result", "success")
                span.set_attribute("agent.id", agent_id)
                span.set_attribute("capability", capability)
                span.set_status(Status(StatusCode.OK))
            
            self.logger.info(
                f"Routed to agent '{agent_id}' (capability: '{capability}') "
                f"with similarity {similarity:.3f} (FAISS)"
            )
            
            with self._metrics_lock:
                self.routing_metrics["total_routes"] += 1
                self.routing_metrics["successful_routes"] += 1
            
            return agent_id
            
        except Exception as e:
            self.logger.error(f"FAISS search error: {e}", exc_info=True)
            if span:
                span.record_exception(e)
            raise
    
    def _route_with_engine(
        self,
        msg: UPTCMessage,
        msg_vector_dim: int,
        span: Optional[Any]
    ) -> Optional[str]:
        """
        Route using EmbeddingEngine (fallback method).
        
        SAFETY: Validates vectors and handles errors
        ASSUMES: EmbeddingEngine.similarity() works correctly
        VERIFY: Returns agent if similarity >= threshold
        """
        # Create snapshot to avoid modification during iteration
        with self._index_lock:
            index_snapshot = {
                cap: {agent: vec.copy() if isinstance(vec, list) else vec
                      for agent, vec in agents.items()}
                for cap, agents in self.capability_index.items()
            }
        
        best_agent: Optional[str] = None
        best_score: float = -1.0
        best_capability: Optional[str] = None
        
        # Iterate over snapshot (thread-safe)
        for capability, entries in index_snapshot.items():
            if not isinstance(entries, dict):
                continue
            
            for agent, vector in entries.items():
                # Validate vector structure
                if not isinstance(vector, list) or len(vector) == 0:
                    continue
                
                # Dimension validation
                if len(vector) != msg_vector_dim:
                    continue
                
                # Compute similarity with error handling
                try:
                    score = self.embedding_engine.similarity(msg.semantic_vector, vector)
                    
                    if not isinstance(score, (int, float)):
                        continue
                    
                    score = float(score)
                    
                    # Track best match
                    if score > best_score:
                        best_score = score
                        best_agent = agent
                        best_capability = capability
                        
                except Exception as e:
                    self.logger.warning(
                        f"Similarity computation failed for agent '{agent}': {e}"
                    )
                    with self._metrics_lock:
                        self.routing_metrics["errors"] += 1
                    continue
        
        # Threshold enforcement
        if best_agent is None:
            if span:
                span.set_attribute("routing.result", "no_match")
                span.set_status(Status(StatusCode.OK))
            self.logger.debug("No matching agent found")
            with self._metrics_lock:
                self.routing_metrics["total_routes"] += 1
            return None
        
        if best_score < self.similarity_threshold:
            if span:
                span.set_attribute("routing.result", "below_threshold")
                span.set_attribute("similarity.score", best_score)
                span.set_status(Status(StatusCode.OK))
            self.logger.debug(
                f"Best match score {best_score:.3f} below threshold "
                f"{self.similarity_threshold:.3f} for agent '{best_agent}'"
            )
            with self._metrics_lock:
                self.routing_metrics["total_routes"] += 1
                self.routing_metrics["threshold_rejections"] += 1
            return None
        
        # Successful route
        if span:
            span.set_attribute("routing.result", "success")
            span.set_attribute("agent.id", best_agent)
            span.set_attribute("capability", best_capability)
            span.set_attribute("similarity.score", best_score)
            span.set_status(Status(StatusCode.OK))
        
        self.logger.info(
            f"Routed to agent '{best_agent}' (capability: '{best_capability}') "
            f"with similarity {best_score:.3f}"
        )
        
        with self._metrics_lock:
            self.routing_metrics["total_routes"] += 1
            self.routing_metrics["successful_routes"] += 1
        
        return best_agent
    
    async def async_route(self, msg: UPTCMessage) -> Optional[str]:
        """
        Async version of route().
        
        SAFETY: Same as route() but async-compatible
        ASSUMES: Called from async context
        
        Args:
            msg: UPTCMessage with semantic_vector for routing
            
        Returns:
            Agent identifier if suitable match found, None otherwise
        """
        # For now, route() is already thread-safe and doesn't block
        # In the future, we could add async FAISS operations if needed
        return self.route(msg)
    
    def rebuild_index(self) -> None:
        """
        Rebuild FAISS index from current capability_index.
        
        SAFETY: Thread-safe index rebuild
        VERIFY: Index rebuilt successfully
        """
        if self.enable_faiss:
            with self._index_lock:
                self.faiss_index = None
                self.faiss_id_map = {}
                self._build_faiss_index()
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get routing metrics for observability.
        
        SAFETY: Thread-safe metrics access
        VERIFY: Returns current metrics snapshot
        
        Returns:
            Dictionary containing routing metrics
        """
        with self._metrics_lock:
            return self.routing_metrics.copy()
    
    def reset_metrics(self) -> None:
        """
        Reset routing metrics.
        
        SAFETY: Thread-safe reset
        """
        with self._metrics_lock:
            self.routing_metrics = {
                "total_routes": 0,
                "successful_routes": 0,
                "threshold_rejections": 0,
                "dimension_mismatches": 0,
                "empty_index_routes": 0,
                "faiss_routes": 0,
                "fallback_routes": 0,
                "errors": 0
            }

