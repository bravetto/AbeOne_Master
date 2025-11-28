"""
Redis-based session manager for user sessions.

This module provides Redis-backed session management for the CodeGuardians Gateway,
enabling distributed session storage across multiple service replicas.
"""

import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
from threading import RLock

import redis
from redis.exceptions import RedisError

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RedisSessionManager:
    """
    Redis-based session manager for user sessions.
    
    Provides distributed session storage with TTL support, serialization,
    and connection pooling for high-performance operations.
    """
    
    def __init__(
        self,
        redis_url: str = None,
        key_prefix: str = "sessions:",
        default_ttl: int = 3600,  # 1 hour default TTL
        max_connections: int = 20
    ):
        """
        Initialize Redis session manager.
        
        Args:
            redis_url: Redis connection URL
            key_prefix: Prefix for all Redis keys
            default_ttl: Default TTL in seconds for sessions
            max_connections: Maximum number of Redis connections
        """
        self.redis_url = redis_url or f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
        self.key_prefix = key_prefix
        self.default_ttl = default_ttl
        self.max_connections = max_connections
        
        # Connection pool
        self._pool: Optional[redis.ConnectionPool] = None
        
        # Thread safety
        self._lock = RLock()
        
        # Initialize connection pool
        self._init_connection_pool()
    
    def _init_connection_pool(self):
        """Initialize Redis connection pool."""
        try:
            self._pool = redis.ConnectionPool.from_url(
                self.redis_url,
                max_connections=self.max_connections,
                retry_on_timeout=True,
                decode_responses=True
            )
            logger.info(f"Redis session manager initialized: {self.redis_url}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis connection pool: {e}")
            raise
    
    def _get_client(self) -> redis.Redis:
        """Get Redis client with connection pooling."""
        if self._pool is None:
            self._init_connection_pool()
        return redis.Redis(connection_pool=self._pool)
    
    def _get_key(self, session_id: str) -> str:
        """Get full Redis key with prefix."""
        return f"{self.key_prefix}{session_id}"
    
    def _serialize_session_data(self, data: Dict[str, Any]) -> str:
        """Serialize session data for Redis storage."""
        try:
            return json.dumps(data, default=str)
        except (TypeError, ValueError) as e:
            logger.warning(f"Failed to serialize session data: {e}")
            return json.dumps({"error": "serialization_failed", "data": str(data)})
    
    def _deserialize_session_data(self, data: str) -> Dict[str, Any]:
        """Deserialize session data from Redis storage."""
        try:
            return json.loads(data)
        except (TypeError, ValueError) as e:
            logger.warning(f"Failed to deserialize session data: {e}")
            return {"error": "deserialization_failed", "raw_data": data}
    
    def create_session(
        self, 
        user_id: int, 
        session_data: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None
    ) -> str:
        """
        Create a new user session.
        
        Args:
            user_id: ID of the user
            session_data: Optional initial session data
            ttl: Time to live in seconds (uses default if None)
            
        Returns:
            Session ID
        """
        try:
            with self._lock:
                client = self._get_client()
                session_id = str(uuid.uuid4())
                redis_key = self._get_key(session_id)
                
                # Prepare session data
                session_info = {
                    "session_id": session_id,
                    "user_id": user_id,
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "last_accessed": datetime.utcnow().isoformat() + "Z",
                    "data": session_data or {}
                }
                
                # Serialize and store
                serialized_data = self._serialize_session_data(session_info)
                ttl = ttl or self.default_ttl
                
                result = client.setex(redis_key, ttl, serialized_data)
                
                if result:
                    logger.info(f"Created session {session_id} for user {user_id}")
                    return session_id
                else:
                    logger.error(f"Failed to create session for user {user_id}")
                    raise Exception("Failed to create session")
                    
        except RedisError as e:
            logger.error(f"Redis error creating session: {e}")
            raise Exception(f"Session creation failed: {e}")
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a session by its ID.
        
        Args:
            session_id: The session ID to retrieve
            
        Returns:
            Session data or None if not found
        """
        try:
            with self._lock:
                client = self._get_client()
                redis_key = self._get_key(session_id)
                
                data = client.get(redis_key)
                if data is None:
                    logger.debug(f"Session {session_id} not found")
                    return None
                
                session_info = self._deserialize_session_data(data)
                
                # Update last accessed time
                session_info["last_accessed"] = datetime.utcnow().isoformat() + "Z"
                self._update_session_data(session_id, session_info)
                
                logger.debug(f"Retrieved session {session_id}")
                return session_info
                
        except RedisError as e:
            logger.error(f"Redis error retrieving session {session_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving session {session_id}: {e}")
            return None
    
    def update_session_data(
        self, 
        session_id: str, 
        data: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """
        Update session data.
        
        Args:
            session_id: The session ID to update
            data: New session data
            ttl: Time to live in seconds (uses default if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self._lock:
                # Get existing session
                session_info = self.get_session(session_id)
                if session_info is None:
                    logger.warning(f"Session {session_id} not found for update")
                    return False
                
                # Update data
                session_info["data"].update(data)
                session_info["last_accessed"] = datetime.utcnow().isoformat() + "Z"
                
                return self._update_session_data(session_id, session_info, ttl)
                
        except Exception as e:
            logger.error(f"Error updating session {session_id}: {e}")
            return False
    
    def _update_session_data(
        self, 
        session_id: str, 
        session_info: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """Internal method to update session data in Redis."""
        try:
            client = self._get_client()
            redis_key = self._get_key(session_id)
            
            serialized_data = self._serialize_session_data(session_info)
            ttl = ttl or self.default_ttl
            
            result = client.setex(redis_key, ttl, serialized_data)
            
            if result:
                logger.debug(f"Updated session {session_id}")
                return True
            else:
                logger.error(f"Failed to update session {session_id}")
                return False
                
        except RedisError as e:
            logger.error(f"Redis error updating session {session_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error updating session {session_id}: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: The session ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self._lock:
                client = self._get_client()
                redis_key = self._get_key(session_id)
                
                result = client.delete(redis_key)
                
                if result:
                    logger.info(f"Deleted session {session_id}")
                    return True
                else:
                    logger.warning(f"Session {session_id} not found for deletion")
                    return False
                    
        except RedisError as e:
            logger.error(f"Redis error deleting session {session_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            return False
    
    def get_user_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all sessions for a user.
        
        Args:
            user_id: The user ID
            
        Returns:
            List of session data
        """
        try:
            with self._lock:
                client = self._get_client()
                pattern = f"{self.key_prefix}*"
                
                # Get all session keys
                keys = client.keys(pattern)
                if not keys:
                    return []
                
                # Get all session data
                sessions = []
                for key in keys:
                    data = client.get(key)
                    if data:
                        session_info = self._deserialize_session_data(data)
                        if session_info.get("user_id") == user_id:
                            sessions.append(session_info)
                
                logger.debug(f"Retrieved {len(sessions)} sessions for user {user_id}")
                return sessions
                
        except RedisError as e:
            logger.error(f"Redis error getting sessions for user {user_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting sessions for user {user_id}: {e}")
            return []
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions (Redis handles this automatically with TTL).
        This method is kept for compatibility and can be used for additional cleanup.
        
        Returns:
            Number of sessions cleaned up
        """
        # Redis automatically handles TTL expiration
        # This method can be used for additional cleanup logic if needed
        logger.debug("Redis handles session expiration automatically via TTL")
        return 0
    
    def extend_session(self, session_id: str, ttl: Optional[int] = None) -> bool:
        """
        Extend session TTL.
        
        Args:
            session_id: The session ID to extend
            ttl: New TTL in seconds (uses default if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self._lock:
                client = self._get_client()
                redis_key = self._get_key(session_id)
                
                # Check if session exists
                if not client.exists(redis_key):
                    logger.warning(f"Session {session_id} not found for extension")
                    return False
                
                # Extend TTL
                ttl = ttl or self.default_ttl
                result = client.expire(redis_key, ttl)
                
                if result:
                    logger.debug(f"Extended session {session_id} TTL to {ttl}s")
                    return True
                else:
                    logger.error(f"Failed to extend session {session_id}")
                    return False
                    
        except RedisError as e:
            logger.error(f"Redis error extending session {session_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error extending session {session_id}: {e}")
            return False
    
    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get session statistics.
        
        Returns:
            Dictionary with session statistics
        """
        try:
            with self._lock:
                client = self._get_client()
                pattern = f"{self.key_prefix}*"
                
                # Get all session keys
                keys = client.keys(pattern)
                
                # Count sessions by user
                user_counts = {}
                total_sessions = len(keys)
                
                for key in keys:
                    data = client.get(key)
                    if data:
                        session_info = self._deserialize_session_data(data)
                        user_id = session_info.get("user_id")
                        if user_id:
                            user_counts[user_id] = user_counts.get(user_id, 0) + 1
                
                return {
                    "total_sessions": total_sessions,
                    "unique_users": len(user_counts),
                    "user_session_counts": user_counts,
                    "storage_type": "redis",
                    "key_prefix": self.key_prefix
                }
                
        except Exception as e:
            logger.error(f"Error getting session stats: {e}")
            return {
                "total_sessions": 0,
                "unique_users": 0,
                "user_session_counts": {},
                "storage_type": "redis",
                "error": str(e)
            }
    
    def health_check(self) -> bool:
        """
        Check Redis connection health.
        
        Returns:
            True if Redis is accessible, False otherwise
        """
        try:
            with self._lock:
                client = self._get_client()
                result = client.ping()
                return bool(result)
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False
    
    def close(self):
        """Close Redis connections."""
        try:
            if self._pool:
                self._pool.disconnect()
            logger.info("Redis session manager connections closed")
        except Exception as e:
            logger.error(f"Error closing Redis connections: {e}")


# Global session manager instance
_session_manager: Optional[RedisSessionManager] = None


def get_session_manager() -> Optional[RedisSessionManager]:
    """Get the global session manager instance."""
    return _session_manager


def initialize_session_manager(
    redis_url: str = None,
    key_prefix: str = "sessions:",
    default_ttl: int = 3600
) -> RedisSessionManager:
    """
    Initialize the global session manager instance.
    
    Args:
        redis_url: Redis connection URL
        key_prefix: Prefix for all Redis keys
        default_ttl: Default TTL in seconds
        
    Returns:
        Initialized session manager instance
    """
    global _session_manager
    _session_manager = RedisSessionManager(
        redis_url=redis_url,
        key_prefix=key_prefix,
        default_ttl=default_ttl
    )
    return _session_manager
