"""
ContextGuard Integration Layer

Pure enhancement layer that enhances other Guards with context awareness.
Uses persistent memory to track context across requests.

Design Principles:
- Zero dependencies: No external services, no HTTP clients
- Pure enhancement: Only enhances guard payloads with context
- Persistent memory: Simple in-memory storage with session-based tracking
- Guard-specific: Each guard gets tailored context enhancement
"""

import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict

from app.utils.logging import get_logger

logger = get_logger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

CONTEXT_MEMORY_TTL_SECONDS = 3600  # 1 hour default retention
MAX_CONTEXT_HISTORY = 10  # Keep last 10 context entries per session

# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

class ContextEntry:
    """Single context entry for a session."""
    def __init__(self, content: str, guard_name: str, result: Dict[str, Any], timestamp: datetime):
        self.content = content
        self.guard_name = guard_name
        self.result = result
        self.timestamp = timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "guard_name": self.guard_name,
            "result": self.result,
            "timestamp": self.timestamp.isoformat()
        }


# ============================================================================
# PERSISTENT MEMORY STORAGE
# ============================================================================

class PersistentContextMemory:
    """
    Simple persistent memory for context tracking.
    
    Stores context per session/user, automatically expires old entries.
    Thread-safe in-memory storage (can be extended to Redis/file later).
    """
    
    def __init__(self, ttl_seconds: int = CONTEXT_MEMORY_TTL_SECONDS, max_history: int = MAX_CONTEXT_HISTORY):
        self.ttl_seconds = ttl_seconds
        self.max_history = max_history
        # Session-based storage: {session_id: [ContextEntry, ...]}
        self._memory: Dict[str, list] = defaultdict(list)
    
    def store(self, session_id: str, content: str, guard_name: str, result: Dict[str, Any]) -> None:
        """
        Store context entry for session.
        
        Args:
            session_id: Session identifier
            content: Content that was processed
            guard_name: Name of guard that processed it
            result: Guard processing result
        """
        # Clean up old entries first
        self._cleanup(session_id)
        
        # Add new entry
        entry = ContextEntry(content, guard_name, result, datetime.now())
        self._memory[session_id].append(entry)
        
        # Limit history size
        if len(self._memory[session_id]) > self.max_history:
            self._memory[session_id] = self._memory[session_id][-self.max_history:]
    
    def get_context(self, session_id: str) -> Dict[str, Any]:
        """
        Get context for session.
        
        Returns:
            Context data including previous entries and patterns
        """
        # Clean up old entries
        self._cleanup(session_id)
        
        entries = self._memory.get(session_id, [])
        if not entries:
            return {
                "has_context": False,
                "previous_count": 0,
                "drift_score": 0.0,
                "similarity": 1.0
            }
        
        # Extract patterns from history
        guard_patterns = {}
        for entry in entries:
            guard_name = entry.guard_name
            if guard_name not in guard_patterns:
                guard_patterns[guard_name] = []
            guard_patterns[guard_name].append(entry.result)
        
        # Get most recent entry
        latest = entries[-1]
        
        return {
            "has_context": True,
            "previous_count": len(entries),
            "drift_score": 0.0,  # Simple implementation - can be enhanced
            "similarity": 1.0,  # Simple implementation - can be enhanced
            "latest_content": latest.content,
            "latest_guard": latest.guard_name,
            "latest_result": latest.result,
            "guard_patterns": guard_patterns,
            "history": [entry.to_dict() for entry in entries[-3:]]  # Last 3 entries
        }
    
    def _cleanup(self, session_id: str) -> None:
        """Remove expired entries for session."""
        if session_id not in self._memory:
            return
        
        now = datetime.now()
        expired_entries = [
            entry for entry in self._memory[session_id]
            if (now - entry.timestamp).total_seconds() > self.ttl_seconds
        ]
        
        for entry in expired_entries:
            self._memory[session_id].remove(entry)
        
        # Remove empty sessions
        if not self._memory[session_id]:
            del self._memory[session_id]
    
    def clear_session(self, session_id: str) -> None:
        """Clear all context for a session."""
        if session_id in self._memory:
            del self._memory[session_id]


# ============================================================================
# CORE INTEGRATION CLASS
# ============================================================================

class ContextGuardIntegration:
    """
    Pure enhancement layer for ContextGuard.
    
    Single Responsibility: Enhance guard payloads with context awareness.
    
    Design Principles:
    - Zero dependencies: No HTTP, no external services
    - Pure enhancement: Only enhances, never replaces
    - Persistent memory: Uses simple in-memory storage
    - Guard-specific: Tailored enhancement per guard type
    """
    
    def __init__(self):
        """Initialize ContextGuard integration."""
        self.memory = PersistentContextMemory()
    
    def enhance_with_context(
        self,
        guard_name: str,
        payload: Dict[str, Any],
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Enhance guard payload with context awareness.
        
        Uses persistent memory to enhance payload with historical context.
        Zero-failure: Always returns enhanced payload (even if no context).
        
        Args:
            guard_name: Name of the guard requesting enhancement
            payload: Original guard payload
            session_id: Session ID for context continuity (optional)
            user_id: User ID for context continuity (optional)
            
        Returns:
            Enhanced payload with context awareness
        """
        # Generate context key
        context_key = session_id or user_id or "default"
        
        # Get context from memory
        context_data = self.memory.get_context(context_key)
        
        # Enhance payload with context
        enhanced_payload = self._merge_context(payload, context_data, guard_name)
        
        logger.debug(f"ContextGuard enhanced {guard_name} payload with context awareness")
        return enhanced_payload
    
    def _merge_context(
        self,
        payload: Dict[str, Any],
        context_data: Dict[str, Any],
        guard_name: str
    ) -> Dict[str, Any]:
        """
        Merge context data into guard payload.
        
        Each guard gets context-enhanced payload tailored to their needs.
        
        Args:
            payload: Original guard payload
            context_data: Context data from persistent memory
            guard_name: Name of guard (for guard-specific enhancement)
            
        Returns:
            Enhanced payload with context awareness
        """
        # Copy payload (don't mutate original)
        enhanced = payload.copy()
        
        # Add context metadata
        enhanced["_context"] = {
            "awareness": context_data.get("has_context", False),
            "previous_count": context_data.get("previous_count", 0),
            "drift_score": context_data.get("drift_score", 0.0),
            "similarity": context_data.get("similarity", 1.0),
            "guard": guard_name,
            "timestamp": datetime.now().isoformat()
        }
        
        # Guard-specific context enhancement
        if guard_name == "trustguard":
            # TrustGuard: Enhance with drift detection and previous context
            enhanced["context"] = enhanced.get("context", {})
            enhanced["context"]["drift_detected"] = context_data.get("drift_score", 0.0) > 0.2
            enhanced["context"]["previous_context"] = context_data.get("latest_result", {})
            enhanced["context"]["pattern_history"] = context_data.get("guard_patterns", {}).get("trustguard", [])
            
        elif guard_name == "biasguard":
            # BiasGuard: Enhance with semantic context and continuity
            enhanced["context"] = enhanced.get("context", {})
            enhanced["context"]["semantic_context"] = context_data.get("latest_result", {})
            enhanced["context"]["continuity"] = context_data.get("similarity", 1.0)
            enhanced["context"]["bias_patterns"] = context_data.get("guard_patterns", {}).get("biasguard", [])
            
        elif guard_name == "securityguard":
            # SecurityGuard: Enhance with historical patterns
            enhanced["context"] = enhanced.get("context", {})
            enhanced["context"]["historical_patterns"] = context_data.get("guard_patterns", {})
            enhanced["context"]["security_history"] = context_data.get("history", [])
            
        elif guard_name == "tokenguard":
            # TokenGuard: Enhance with usage patterns
            enhanced["context"] = enhanced.get("context", {})
            enhanced["context"]["usage_patterns"] = context_data.get("guard_patterns", {}).get("tokenguard", [])
            
        elif guard_name == "healthguard":
            # HealthGuard: Enhance with health history
            enhanced["context"] = enhanced.get("context", {})
            enhanced["context"]["health_history"] = context_data.get("history", [])
            enhanced["context"]["health_patterns"] = context_data.get("guard_patterns", {}).get("healthguard", [])
        
        # All guards get basic context awareness
        if "context" not in enhanced:
            enhanced["context"] = {}
        
        enhanced["context"]["has_memory"] = context_data.get("has_context", False)
        enhanced["context"]["memory_count"] = context_data.get("previous_count", 0)
        
        return enhanced
    
    def store_context(
        self,
        guard_name: str,
        payload: Dict[str, Any],
        result: Dict[str, Any],
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> None:
        """
        Store context after guard processing.
        
        Stores guard results in persistent memory for future context awareness.
        Non-blocking, zero-failure operation.
        
        Args:
            guard_name: Name of guard that processed request
            payload: Original guard payload
            result: Guard processing result
            session_id: Session ID for context storage (optional)
            user_id: User ID for context storage (optional)
        """
        try:
            # Extract content for storage
            content = (
                payload.get("current_code") or 
                payload.get("text") or 
                payload.get("content") or 
                payload.get("code") or
                ""
            )
            
            # Skip if no content to store
            if not content:
                return
            
            # Generate context key
            context_key = session_id or user_id or "default"
            
            # Store in persistent memory
            self.memory.store(context_key, content, guard_name, result)
            
            logger.debug(f"ContextGuard stored context for {guard_name}")
            
        except Exception as e:
            # Zero-failure: Log but never propagate
            logger.debug(f"ContextGuard storage failed (non-critical): {e}")


# ============================================================================
# MODULE-LEVEL FUNCTIONS
# ============================================================================

# Global instance for easy access (singleton pattern)
_contextguard_integration: Optional[ContextGuardIntegration] = None


def get_contextguard_integration() -> ContextGuardIntegration:
    """
    Get or create ContextGuard integration instance.
    
    Singleton pattern: One instance per process, shared across requests.
    
    Returns:
        ContextGuard integration instance
    """
    global _contextguard_integration
    if _contextguard_integration is None:
        _contextguard_integration = ContextGuardIntegration()
    return _contextguard_integration


def enhance_guard_with_context(
    guard_name: str,
    payload: Dict[str, Any],
    session_id: Optional[str] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Enhance guard payload with ContextGuard awareness.
    
    Called automatically before routing to any guard.
    Zero-failure: Always returns enhanced payload.
    
    Args:
        guard_name: Name of guard requesting enhancement
        payload: Original guard payload
        session_id: Session ID for context continuity (optional)
        user_id: User ID for personalized context (optional)
        
    Returns:
        Enhanced payload with context awareness
    """
    integration = get_contextguard_integration()
    return integration.enhance_with_context(guard_name, payload, session_id, user_id)


def store_guard_context(
    guard_name: str,
    payload: Dict[str, Any],
    result: Dict[str, Any],
    session_id: Optional[str] = None,
    user_id: Optional[str] = None
) -> None:
    """
    Store guard result in ContextGuard persistent memory.
    
    Called automatically after guard processing to build context awareness.
    Non-blocking, graceful degradation.
    
    Args:
        guard_name: Name of guard that processed request
        payload: Original guard payload
        result: Guard processing result
        session_id: Session ID for context storage (optional)
        user_id: User ID for context storage (optional)
    """
    integration = get_contextguard_integration()
    integration.store_context(guard_name, payload, result, session_id, user_id)
