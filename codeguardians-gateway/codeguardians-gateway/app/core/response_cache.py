"""
Response Caching Module

Provides Redis-backed response caching for API endpoints.
Includes health check caching for optimized Kubernetes probes.
"""

import json
import hashlib
from typing import Optional, Dict, Any, Callable
from functools import wraps
import redis.asyncio as redis
from datetime import timedelta

from app.core.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Global Redis client for caching
_cache_client: Optional[redis.Redis] = None


async def get_cache_client() -> Optional[redis.Redis]:
    """Get or create Redis cache client."""
    global _cache_client
    
    if _cache_client is not None:
        return _cache_client
    
    if not settings.REDIS_URL:
        logger.warning("Redis URL not configured, caching disabled")
        return None
    
    try:
        _cache_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
            retry_on_timeout=True,
            health_check_interval=30
        )
        # Test connection
        await _cache_client.ping()
        logger.info("Redis cache client initialized")
        return _cache_client
    except Exception as e:
        logger.warning(f"Failed to initialize Redis cache: {e}")
        _cache_client = None
        return None


def generate_cache_key(endpoint: str, params: Dict[str, Any] = None) -> str:
    """Generate cache key from endpoint and parameters."""
    key_data = {"endpoint": endpoint}
    if params:
        key_data["params"] = params
    
    key_string = json.dumps(key_data, sort_keys=True)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()
    return f"cache:response:{key_hash}"


async def get_cached_response(cache_key: str) -> Optional[Dict[str, Any]]:
    """Get cached response."""
    client = await get_cache_client()
    if not client:
        return None
    
    try:
        cached_data = await client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except Exception as e:
        logger.debug(f"Cache get failed: {e}")
    
    return None


async def set_cached_response(
    cache_key: str,
    data: Dict[str, Any],
    ttl: int = 300
) -> bool:
    """Set cached response."""
    client = await get_cache_client()
    if not client:
        return False
    
    try:
        await client.setex(
            cache_key,
            ttl,
            json.dumps(data, default=str)
        )
        return True
    except Exception as e:
        logger.debug(f"Cache set failed: {e}")
        return False


async def invalidate_cache(pattern: str) -> int:
    """Invalidate cache entries matching pattern."""
    client = await get_cache_client()
    if not client:
        return 0
    
    try:
        keys = await client.keys(pattern)
        if keys:
            return await client.delete(*keys)
        return 0
    except Exception as e:
        logger.debug(f"Cache invalidation failed: {e}")
        return 0


def cache_response(ttl: int = 300, key_params: list = None):
    """
    Decorator for caching endpoint responses.
    
    Args:
        ttl: Time to live in seconds (default: 5 minutes)
        key_params: List of parameter names to include in cache key
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            endpoint = f"{func.__module__}.{func.__name__}"
            params = {}
            if key_params:
                for param in key_params:
                    if param in kwargs:
                        params[param] = kwargs[param]
            
            cache_key = generate_cache_key(endpoint, params)
            
            # Try to get from cache
            cached = await get_cached_response(cache_key)
            if cached:
                logger.debug(f"Cache hit: {cache_key}")
                return cached.get("response")
            
            # Execute function
            response = await func(*args, **kwargs)
            
            # Cache response
            await set_cached_response(
                cache_key,
                {"response": response},
                ttl
            )
            
            return response
        
        return wrapper
    return decorator


# Health check cache (optimized for <50ms requirement)
_health_cache: Optional[Dict[str, Any]] = None
_health_cache_time: float = 0.0
_health_cache_ttl: float = 5.0  # 5 seconds


async def get_cached_health_check() -> Optional[Dict[str, Any]]:
    """Get cached health check result (optimized for speed)."""
    import time
    global _health_cache, _health_cache_time
    
    current_time = time.time()
    
    if _health_cache and (current_time - _health_cache_time) < _health_cache_ttl:
        return _health_cache
    
    # Try Redis cache
    client = await get_cache_client()
    if client:
        try:
            cached = await client.get("cache:health:liveness")
            if cached:
                _health_cache = json.loads(cached)
                _health_cache_time = current_time
                return _health_cache
        except Exception:
            pass
    
    return None


async def set_cached_health_check(data: Dict[str, Any], ttl: int = 5):
    """Set cached health check result."""
    import time
    global _health_cache, _health_cache_time
    
    _health_cache = data
    _health_cache_time = time.time()
    
    # Also cache in Redis
    client = await get_cache_client()
    if client:
        try:
            await client.setex(
                "cache:health:liveness",
                ttl,
                json.dumps(data, default=str)
            )
        except Exception:
            pass

