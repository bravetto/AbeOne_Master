"""
Connection Pool Optimizer

FULL MONTY EEAaO: Excellence at Every Level
- HTTP connection pooling
- Database connection pooling
- Redis connection pooling
- Optimal pool sizing
"""

import httpx
from typing import Optional
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine
import redis.asyncio as redis

from app.core.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class ConnectionPoolOptimizer:
    """
    Optimize connection pools for maximum performance.
    
    EEAaO: Excellence at Every Level - Connection optimization
    """
    
    def __init__(self):
        self._http_client: Optional[httpx.AsyncClient] = None
        self._redis_pool: Optional[redis.ConnectionPool] = None
    
    def get_optimized_http_client(self) -> httpx.AsyncClient:
        """
        Get optimized HTTP client with connection pooling.
        
        EEAaO: HTTP connection pooling for excellence
        """
        if self._http_client is None:
            limits = httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100,
                keepalive_expiry=30.0
            )
            
            timeout = httpx.Timeout(
                connect=5.0,
                read=30.0,
                write=10.0,
                pool=5.0
            )
            
            self._http_client = httpx.AsyncClient(
                limits=limits,
                timeout=timeout,
                http2=True  # HTTP/2 for better performance
            )
            logger.info("Optimized HTTP client created with connection pooling")
        
        return self._http_client
    
    def get_optimized_redis_pool(self) -> redis.ConnectionPool:
        """
        Get optimized Redis connection pool.
        
        EEAaO: Redis pooling for excellence
        """
        if self._redis_pool is None:
            self._redis_pool = redis.ConnectionPool.from_url(
                settings.REDIS_URL,
                max_connections=50,
                retry_on_timeout=True,
                health_check_interval=30
            )
            logger.info("Optimized Redis connection pool created")
        
        return self._redis_pool
    
    async def close_all(self):
        """Close all connection pools."""
        from app.core.error_exporter import get_error_exporter
        
        if self._http_client:
            try:
                await self._http_client.aclose()
            except Exception as e:
                get_error_exporter().export_error(
                    e,
                    context={"operation": "close_http_client"},
                    error_code="HTTP_CLIENT_CLOSE_ERROR"
                )
            finally:
                self._http_client = None
        
        if self._redis_pool:
            try:
                await self._redis_pool.disconnect()
            except Exception as e:
                get_error_exporter().export_error(
                    e,
                    context={"operation": "close_redis_pool"},
                    error_code="REDIS_POOL_CLOSE_ERROR"
                )
            finally:
                self._redis_pool = None


# Global optimizer instance
_connection_optimizer: Optional[ConnectionPoolOptimizer] = None


def get_connection_optimizer() -> ConnectionPoolOptimizer:
    """Get global connection pool optimizer."""
    global _connection_optimizer
    if _connection_optimizer is None:
        _connection_optimizer = ConnectionPoolOptimizer()
    return _connection_optimizer

