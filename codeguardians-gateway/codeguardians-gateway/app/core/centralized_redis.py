"""
Centralized Redis Management for AIGuardian
Unified caching and session management for all guard services
"""

import json
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta

import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.aws_secrets import aws_secrets
from app.core.config import get_settings


class CentralizedRedis:
    """Centralized Redis management for all AIGuardian services."""
    
    def __init__(self, config=None, logger=None):
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self.redis_client = None
        
    async def initialize(self):
        """Initialize the centralized Redis client."""
        try:
            # Get Redis URL from AWS Secrets Manager or config
            redis_url = None
            settings = get_settings()
            
            if settings.AWS_SECRETS_ENABLED:
                try:
                    redis_url = aws_secrets.get_redis_url()
                    if redis_url:
                        self.logger.info("Using Redis URL from AWS Secrets Manager")
                except Exception as e:
                    self.logger.warning(f"Failed to get Redis URL from AWS Secrets Manager: {e}")
            
            # Fallback to config or environment
            if not redis_url:
                if self.config and hasattr(self.config, 'get_redis_url'):
                    redis_url = self.config.get_redis_url()
                else:
                    redis_url = settings.REDIS_URL
            
            if not redis_url:
                self.logger.warning("No Redis URL available. Redis features will be disabled.")
                return
            
            # Create Redis connection pool
            self.redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            await self.redis_client.ping()
            self.logger.info("Centralized Redis initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize centralized Redis: {e}")
            # Don't raise - allow the app to continue without Redis
            self.redis_client = None
    
    async def set_guard_context(self, guard_name: str, session_id: str, 
                              context_data: Dict[str, Any], ttl: int = 3600):
        """Set context data for a guard service."""
        try:
            key = f"guard_context:{guard_name}:{session_id}"
            await self.redis_client.setex(
                key, 
                ttl, 
                json.dumps(context_data)
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to set guard context: {e}")
            return False
    
    async def get_guard_context(self, guard_name: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Get context data for a guard service."""
        try:
            key = f"guard_context:{guard_name}:{session_id}"
            data = await self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            self.logger.error(f"Failed to get guard context: {e}")
            return None
    
    async def delete_guard_context(self, guard_name: str, session_id: str):
        """Delete context data for a guard service."""
        try:
            key = f"guard_context:{guard_name}:{session_id}"
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete guard context: {e}")
            return False
    
    async def set_guard_metrics(self, guard_name: str, metrics_data: Dict[str, Any], ttl: int = 86400):
        """Set metrics data for a guard service."""
        try:
            key = f"guard_metrics:{guard_name}:{datetime.now().strftime('%Y%m%d%H')}"
            await self.redis_client.setex(
                key,
                ttl,
                json.dumps(metrics_data)
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to set guard metrics: {e}")
            return False
    
    async def get_guard_metrics(self, guard_name: str, hour: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get metrics data for a guard service."""
        try:
            if not hour:
                hour = datetime.now().strftime('%Y%m%d%H')
            key = f"guard_metrics:{guard_name}:{hour}"
            data = await self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            self.logger.error(f"Failed to get guard metrics: {e}")
            return None
    
    async def increment_counter(self, key: str, amount: int = 1, ttl: Optional[int] = None):
        """Increment a counter in Redis."""
        try:
            result = await self.redis_client.incrby(key, amount)
            if ttl:
                await self.redis_client.expire(key, ttl)
            return result
        except Exception as e:
            self.logger.error(f"Failed to increment counter: {e}")
            return 0
    
    async def get_counter(self, key: str) -> int:
        """Get a counter value from Redis."""
        try:
            value = await self.redis_client.get(key)
            return int(value) if value else 0
        except Exception as e:
            self.logger.error(f"Failed to get counter: {e}")
            return 0
    
    async def set_rate_limit(self, key: str, limit: int, window: int):
        """Set up rate limiting."""
        try:
            current = await self.redis_client.get(key)
            if current is None:
                await self.redis_client.setex(key, window, 1)
                return True
            elif int(current) < limit:
                await self.redis_client.incr(key)
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"Failed to set rate limit: {e}")
            return False
    
    async def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check if rate limit is exceeded."""
        try:
            current = await self.redis_client.get(key)
            return int(current) < limit if current else True
        except Exception as e:
            self.logger.error(f"Failed to check rate limit: {e}")
            return True
    
    async def set_session_data(self, session_id: str, data: Dict[str, Any], ttl: int = 3600):
        """Set session data."""
        try:
            key = f"session:{session_id}"
            await self.redis_client.setex(
                key,
                ttl,
                json.dumps(data)
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to set session data: {e}")
            return False
    
    async def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data."""
        try:
            key = f"session:{session_id}"
            data = await self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            self.logger.error(f"Failed to get session data: {e}")
            return None
    
    async def delete_session_data(self, session_id: str):
        """Delete session data."""
        try:
            key = f"session:{session_id}"
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete session data: {e}")
            return False
    
    async def set_cache(self, key: str, data: Any, ttl: int = 300):
        """Set cache data."""
        try:
            await self.redis_client.setex(
                key,
                ttl,
                json.dumps(data, default=str)
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to set cache: {e}")
            return False
    
    async def get_cache(self, key: str) -> Optional[Any]:
        """Get cache data."""
        try:
            data = await self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            self.logger.error(f"Failed to get cache: {e}")
            return None
    
    async def delete_cache(self, key: str):
        """Delete cache data."""
        try:
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete cache: {e}")
            return False
    
    async def get_all_keys(self, pattern: str = "*") -> List[str]:
        """Get all keys matching a pattern."""
        try:
            return await self.redis_client.keys(pattern)
        except Exception as e:
            self.logger.error(f"Failed to get keys: {e}")
            return []
    
    async def get_redis_info(self) -> Dict[str, Any]:
        """Get Redis server information."""
        try:
            info = await self.redis_client.info()
            return {
                'redis_version': info.get('redis_version'),
                'used_memory': info.get('used_memory_human'),
                'connected_clients': info.get('connected_clients'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace': info.get('keyspace'),
                'uptime_in_seconds': info.get('uptime_in_seconds')
            }
        except Exception as e:
            self.logger.error(f"Failed to get Redis info: {e}")
            return {}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform Redis health check."""
        try:
            # Test ping
            pong = await self.redis_client.ping()
            if pong:
                # Get basic info
                info = await self.get_redis_info()
                return {
                    'status': 'healthy',
                    'redis_url': self.config.get_redis_url(),
                    'info': info,
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': 'Ping failed',
                    'timestamp': datetime.utcnow().isoformat()
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def cleanup(self):
        """Cleanup Redis resources."""
        if self.redis_client:
            await self.redis_client.close()


# Global instance
_centralized_redis_instance = None

def get_centralized_redis() -> CentralizedRedis:
    """Get the global CentralizedRedis instance."""
    global _centralized_redis_instance
    if _centralized_redis_instance is None:
        import logging
        logger = logging.getLogger(__name__)
        _centralized_redis_instance = CentralizedRedis(logger=logger)
    return _centralized_redis_instance


