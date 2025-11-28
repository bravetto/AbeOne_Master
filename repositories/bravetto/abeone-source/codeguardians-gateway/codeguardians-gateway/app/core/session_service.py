"""
Session service for managing user sessions.

This service provides a unified interface for session management that can work
with both Redis (for distributed systems) and PostgreSQL (for backward compatibility).
"""

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from app.core.database import get_session_factory
from app.core.models import Session as SessionModel
from app.core.session_manager import get_session_manager, initialize_session_manager
from app.core.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
settings = get_settings()


class SessionService:
    """
    Unified session service supporting both Redis and database backends.
    
    Automatically detects the preferred storage method and provides
    a consistent interface for session operations.
    """
    
    def __init__(self, use_redis: bool = None):
        """
        Initialize session service.
        
        Args:
            use_redis: Whether to use Redis. If None, auto-detect from environment.
        """
        if use_redis is None:
            use_redis = settings.REDIS_ENABLED
        
        self.use_redis = use_redis
        self.redis_manager = None
        
        if self.use_redis:
            try:
                self.redis_manager = get_session_manager()
                if self.redis_manager is None:
                    # Initialize Redis session manager
                    redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
                    self.redis_manager = initialize_session_manager(
                        redis_url=redis_url,
                        key_prefix="sessions:",
                        default_ttl=settings.SESSION_TTL
                    )
                logger.info("Session service initialized with Redis backend")
            except Exception as e:
                logger.warning(f"Failed to initialize Redis session manager: {e}. Falling back to database.")
                self.use_redis = False
        
        if not self.use_redis:
            logger.info("Session service initialized with database backend")
    
    async def create_session(
        self, 
        user_id: int, 
        session_data: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        ttl: Optional[int] = None
    ) -> str:
        """
        Create a new user session.
        
        Args:
            user_id: ID of the user
            session_data: Optional initial session data
            ip_address: Client IP address
            user_agent: Client user agent
            ttl: Time to live in seconds
            
        Returns:
            Session ID
        """
        if self.use_redis and self.redis_manager:
            return self._create_redis_session(user_id, session_data, ttl)
        else:
            return await self._create_db_session(user_id, session_data, ip_address, user_agent)
    
    def _create_redis_session(
        self, 
        user_id: int, 
        session_data: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None
    ) -> str:
        """Create session in Redis."""
        try:
            # Add metadata to session data
            enhanced_data = {
                "ip_address": None,
                "user_agent": None,
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat() + "Z",
                "last_accessed": datetime.now(timezone.utc).isoformat() + "Z",
                "data": session_data or {}
            }
            
            return self.redis_manager.create_session(user_id, enhanced_data, ttl)
        except Exception as e:
            logger.error(f"Failed to create Redis session: {e}")
            raise
    
    async def _create_db_session(
        self, 
        user_id: int, 
        session_data: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> str:
        """Create session in database."""
        try:
            import uuid
            session_id = str(uuid.uuid4())
            
            # Create session in database
            db_session = SessionModel(
                session_id=session_id,
                user_id=user_id,
                data=json.dumps(session_data or {}),
                ip_address=ip_address,
                user_agent=user_agent,
                is_active=True,
                created_at=datetime.now(timezone.utc),
                last_accessed=datetime.now(timezone.utc)
            )
            
            # Get database session factory and create async session
            session_factory = get_session_factory()
            if not session_factory:
                raise RuntimeError("Database session factory not available")
            
            async with session_factory() as db:
                try:
                    db.add(db_session)
                    await db.commit()
                    logger.info(f"Created database session {session_id} for user {user_id}")
                    return session_id
                except Exception as e:
                    await db.rollback()
                    raise
                
        except Exception as e:
            logger.error(f"Failed to create database session: {e}")
            raise
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a session by its ID.
        
        Args:
            session_id: The session ID to retrieve
            
        Returns:
            Session data or None if not found
        """
        if self.use_redis and self.redis_manager:
            return self._get_redis_session(session_id)
        else:
            return await self._get_db_session(session_id)
    
    def _get_redis_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session from Redis."""
        try:
            return self.redis_manager.get_session(session_id)
        except Exception as e:
            logger.error(f"Failed to get Redis session {session_id}: {e}")
            return None
    
    async def _get_db_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session from database."""
        try:
            session_factory = get_session_factory()
            if not session_factory:
                logger.error("Database session factory not available")
                return None
            
            async with session_factory() as db:
                try:
                    stmt = select(SessionModel).where(
                        SessionModel.session_id == session_id,
                        SessionModel.is_active == True
                    )
                    result = await db.execute(stmt)
                    session_record = result.scalar_one_or_none()
                    
                    if session_record is None:
                        return None
                    
                    # Update last accessed time
                    session_record.last_accessed = datetime.now(timezone.utc)
                    await db.commit()
                    
                    # Convert to dictionary
                    session_data = {
                        "session_id": session_record.session_id,
                        "user_id": session_record.user_id,
                        "data": json.loads(session_record.data) if session_record.data else {},
                        "ip_address": session_record.ip_address,
                        "user_agent": session_record.user_agent,
                        "is_active": session_record.is_active,
                        "created_at": session_record.created_at.isoformat() + "Z",
                        "last_accessed": session_record.last_accessed.isoformat() + "Z"
                    }
                    
                    return session_data
                    
                except Exception as e:
                    await db.rollback()
                    raise
                
        except Exception as e:
            logger.error(f"Failed to get database session {session_id}: {e}")
            return None
    
    async def update_session_data(
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
            ttl: Time to live in seconds (Redis only)
            
        Returns:
            True if successful, False otherwise
        """
        if self.use_redis and self.redis_manager:
            return self._update_redis_session(session_id, data, ttl)
        else:
            return await self._update_db_session(session_id, data)
    
    def _update_redis_session(
        self, 
        session_id: str, 
        data: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """Update session in Redis."""
        try:
            return self.redis_manager.update_session_data(session_id, data, ttl)
        except Exception as e:
            logger.error(f"Failed to update Redis session {session_id}: {e}")
            return False
    
    async def _update_db_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Update session in database."""
        try:
            session_factory = get_session_factory()
            if not session_factory:
                logger.error("Database session factory not available")
                return False
            
            async with session_factory() as db:
                try:
                    stmt = select(SessionModel).where(
                        SessionModel.session_id == session_id,
                        SessionModel.is_active == True
                    )
                    result = await db.execute(stmt)
                    session_record = result.scalar_one_or_none()
                    
                    if session_record is None:
                        return False
                    
                    # Update session data
                    session_record.data = json.dumps(data)
                    session_record.last_accessed = datetime.now(timezone.utc)
                    await db.commit()
                    
                    return True
                    
                except Exception as e:
                    await db.rollback()
                    raise
                
        except Exception as e:
            logger.error(f"Failed to update database session {session_id}: {e}")
            return False
    
    async def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: The session ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        if self.use_redis and self.redis_manager:
            return self._delete_redis_session(session_id)
        else:
            return await self._delete_db_session(session_id)
    
    def _delete_redis_session(self, session_id: str) -> bool:
        """Delete session from Redis."""
        try:
            return self.redis_manager.delete_session(session_id)
        except Exception as e:
            logger.error(f"Failed to delete Redis session {session_id}: {e}")
            return False
    
    async def _delete_db_session(self, session_id: str) -> bool:
        """Delete session from database."""
        try:
            session_factory = get_session_factory()
            if not session_factory:
                logger.error("Database session factory not available")
                return False
            
            async with session_factory() as db:
                try:
                    stmt = delete(SessionModel).where(SessionModel.session_id == session_id)
                    result = await db.execute(stmt)
                    await db.commit()
                    
                    return result.rowcount > 0
                    
                except Exception as e:
                    await db.rollback()
                    raise
                
        except Exception as e:
            logger.error(f"Failed to delete database session {session_id}: {e}")
            return False
    
    async def get_user_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all sessions for a user.
        
        Args:
            user_id: The user ID
            
        Returns:
            List of session data
        """
        if self.use_redis and self.redis_manager:
            return self._get_redis_user_sessions(user_id)
        else:
            return await self._get_db_user_sessions(user_id)
    
    def _get_redis_user_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user sessions from Redis."""
        try:
            return self.redis_manager.get_user_sessions(user_id)
        except Exception as e:
            logger.error(f"Failed to get Redis sessions for user {user_id}: {e}")
            return []
    
    async def _get_db_user_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user sessions from database."""
        try:
            session_factory = get_session_factory()
            if not session_factory:
                logger.error("Database session factory not available")
                return []
            
            async with session_factory() as db:
                try:
                    stmt = select(SessionModel).where(
                        SessionModel.user_id == user_id,
                        SessionModel.is_active == True
                    )
                    result = await db.execute(stmt)
                    results = result.scalars().all()
                    
                    sessions = []
                    for session_record in results:
                        session_data = {
                            "session_id": session_record.session_id,
                            "user_id": session_record.user_id,
                            "data": json.loads(session_record.data) if session_record.data else {},
                            "ip_address": session_record.ip_address,
                            "user_agent": session_record.user_agent,
                            "is_active": session_record.is_active,
                            "created_at": session_record.created_at.isoformat() + "Z",
                            "last_accessed": session_record.last_accessed.isoformat() + "Z"
                        }
                        sessions.append(session_data)
                    
                    return sessions
                    
                except Exception as e:
                    await db.rollback()
                    raise
                
        except Exception as e:
            logger.error(f"Failed to get database sessions for user {user_id}: {e}")
            return []
    
    async def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions.
        
        Returns:
            Number of sessions cleaned up
        """
        if self.use_redis and self.redis_manager:
            # Redis handles TTL automatically
            return self.redis_manager.cleanup_expired_sessions()
        else:
            return await self._cleanup_db_sessions()
    
    async def _cleanup_db_sessions(self) -> int:
        """Clean up expired database sessions."""
        try:
            session_factory = get_session_factory()
            if not session_factory:
                logger.error("Database session factory not available")
                return 0
            
            async with session_factory() as db:
                try:
                    # Delete sessions older than SESSION_TTL
                    cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=settings.SESSION_TTL)
                    
                    stmt = delete(SessionModel).where(
                        SessionModel.last_accessed < cutoff_time
                    )
                    result = await db.execute(stmt)
                    await db.commit()
                    
                    deleted_count = result.rowcount
                    logger.info(f"Cleaned up {deleted_count} expired database sessions")
                    return deleted_count
                    
                except Exception as e:
                    await db.rollback()
                    raise
                
        except Exception as e:
            logger.error(f"Failed to cleanup database sessions: {e}")
            return 0
    
    async def get_session_stats(self) -> Dict[str, Any]:
        """
        Get session statistics.
        
        Returns:
            Dictionary with session statistics
        """
        if self.use_redis and self.redis_manager:
            return self.redis_manager.get_session_stats()
        else:
            return await self._get_db_session_stats()
    
    async def _get_db_session_stats(self) -> Dict[str, Any]:
        """Get database session statistics."""
        try:
            session_factory = get_session_factory()
            if not session_factory:
                logger.error("Database session factory not available")
                return {
                    "total_sessions": 0,
                    "unique_users": 0,
                    "user_session_counts": {},
                    "storage_type": "database",
                    "error": "Session factory not available"
                }
            
            async with session_factory() as db:
                try:
                    from sqlalchemy import func
                    # Count total sessions
                    total_query = select(func.count(SessionModel.id)).where(SessionModel.is_active == True)
                    total_result = await db.execute(total_query)
                    total_sessions = total_result.scalar() or 0
                    
                    # Get all sessions to count by user
                    sessions_query = select(SessionModel).where(SessionModel.is_active == True)
                    sessions_result = await db.execute(sessions_query)
                    sessions = sessions_result.scalars().all()
                    
                    # Count sessions by user
                    user_counts = {}
                    for session in sessions:
                        user_id = session.user_id
                        user_counts[user_id] = user_counts.get(user_id, 0) + 1
                    
                    return {
                        "total_sessions": total_sessions,
                        "unique_users": len(user_counts),
                        "user_session_counts": user_counts,
                        "storage_type": "database"
                    }
                    
                except Exception as e:
                    await db.rollback()
                    raise
                
        except Exception as e:
            logger.error(f"Failed to get database session stats: {e}")
            return {
                "total_sessions": 0,
                "unique_users": 0,
                "user_session_counts": {},
                "storage_type": "database",
                "error": str(e)
            }
    
    async def health_check(self) -> bool:
        """
        Check session service health.
        
        Returns:
            True if healthy, False otherwise
        """
        if self.use_redis and self.redis_manager:
            return self.redis_manager.health_check()
        else:
            # Database health check
            try:
                session_factory = get_session_factory()
                if not session_factory:
                    return False
                
                async with session_factory() as db:
                    try:
                        # Simple query to check database connectivity
                        from sqlalchemy import text
                        result = await db.execute(text("SELECT 1"))
                        result.scalar()
                        return True
                    except Exception:
                        return False
            except Exception:
                return False


# Global session service instance
_session_service: Optional[SessionService] = None


def get_session_service() -> Optional[SessionService]:
    """Get the global session service instance."""
    return _session_service


def initialize_session_service(use_redis: bool = None) -> SessionService:
    """
    Initialize the global session service instance.
    
    Args:
        use_redis: Whether to use Redis. If None, auto-detect from environment.
        
    Returns:
        Initialized session service instance
    """
    global _session_service
    _session_service = SessionService(use_redis=use_redis)
    return _session_service
