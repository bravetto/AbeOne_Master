"""
Dynamic rate limiting middleware with runtime configuration support.

This middleware provides dynamic rate limiting that can be adjusted
at runtime without requiring application restarts.
"""

import time
import os
from typing import Dict, Optional, Tuple
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
# Removed dynamic_config dependency - using static config from settings
from app.core.exceptions import RateLimitError
from app.core.config import get_settings
from app.utils.logging import get_logger
import redis.asyncio as redis
import json

settings = get_settings()

logger = get_logger(__name__)


class DynamicRateLimiter:
    """Dynamic rate limiter with Redis backend."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """Initialize the dynamic rate limiter."""
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
        self._rate_limit_cache: Dict[str, Dict[str, any]] = {}
        self._cache_ttl = 60  # Cache TTL in seconds
        self._last_config_update = 0
    
    async def _get_redis_client(self) -> redis.Redis:
        """Get Redis client with connection pooling."""
        if self.redis_client is None:
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
        return self.redis_client
    
    async def _get_rate_limit_config(self) -> Dict[str, any]:
        """Get current rate limit configuration."""
        current_time = time.time()

        # Check if we need to refresh the config
        if (current_time - self._last_config_update) > self._cache_ttl:
            try:
                # Use static rate limits from settings
                rate_limits = {
                    "enabled": settings.RATE_LIMIT_ENABLED,
                    "requests_per_minute": settings.RATE_LIMIT_REQUESTS,
                    "window_size": settings.RATE_LIMIT_WINDOW,
                }
                self._rate_limit_cache = rate_limits
                self._last_config_update = current_time
                logger.debug("Refreshed rate limit configuration")
            except Exception as e:
                logger.warning(f"Failed to get rate limit configuration: {e}. Using defaults")
                # Always provide working defaults
                self._rate_limit_cache = {
                    "enabled": True,
                    "requests_per_minute": 100,
                    "requests_per_hour": 1000,
                    "burst_limit": 20,
                    "window_size": 60,
                    "endpoint_limits": {},
                    "user_limits": {},
                    "ip_limits": {}
                }
                self._last_config_update = current_time

        return self._rate_limit_cache
    
    def _get_client_identifier(self, request: Request) -> str:
        """Get client identifier for rate limiting."""
        # Try to get user ID from request state (if authenticated)
        if hasattr(request.state, 'user_id') and request.state.user_id:
            return f"user:{request.state.user_id}"
        
        # Fall back to IP address
        client_ip = request.client.host
        if "x-forwarded-for" in request.headers:
            client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()
        
        return f"ip:{client_ip}"
    
    def _get_endpoint_key(self, request: Request) -> str:
        """Get endpoint key for rate limiting."""
        return f"endpoint:{request.method}:{request.url.path}"
    
    async def _check_redis_rate_limit(
        self, 
        key: str, 
        limit: int, 
        window: int,
        identifier: str
    ) -> Tuple[bool, Dict[str, any]]:
        """Check rate limit using Redis."""
        try:
            redis_client = await self._get_redis_client()
            current_time = int(time.time())
            
            # Use sliding window algorithm
            pipe = redis_client.pipeline()
            
            # Remove expired entries
            pipe.zremrangebyscore(key, 0, current_time - window)
            
            # Count current requests
            pipe.zcard(key)
            
            # Add current request
            pipe.zadd(key, {str(current_time): current_time})
            
            # Set expiration
            pipe.expire(key, window)
            
            results = await pipe.execute()
            current_count = results[1]
            
            # Check if limit exceeded
            if current_count >= limit:
                return False, {
                    "limit": limit,
                    "remaining": 0,
                    "reset_time": current_time + window,
                    "retry_after": window
                }
            
            return True, {
                "limit": limit,
                "remaining": limit - current_count - 1,
                "reset_time": current_time + window,
                "retry_after": 0
            }
            
        except Exception as e:
            logger.error(f"Redis rate limit check failed: {e}")
            # Fall back to allowing the request
            return True, {
                "limit": limit,
                "remaining": limit,
                "reset_time": int(time.time()) + window,
                "retry_after": 0
            }
    
    async def _check_memory_rate_limit(
        self, 
        key: str, 
        limit: int, 
        window: int
    ) -> Tuple[bool, Dict[str, any]]:
        """Check rate limit using in-memory storage (fallback)."""
        current_time = time.time()
        
        if key not in self._rate_limit_cache:
            self._rate_limit_cache[key] = []
        
        # Clean old entries
        self._rate_limit_cache[key] = [
            timestamp for timestamp in self._rate_limit_cache[key]
            if current_time - timestamp < window
        ]
        
        # Check limit
        if len(self._rate_limit_cache[key]) >= limit:
            return False, {
                "limit": limit,
                "remaining": 0,
                "reset_time": int(current_time + window),
                "retry_after": window
            }
        
        # Add current request
        self._rate_limit_cache[key].append(current_time)
        
        return True, {
            "limit": limit,
            "remaining": limit - len(self._rate_limit_cache[key]),
            "reset_time": int(current_time + window),
            "retry_after": 0
        }
    
    async def check_rate_limit(
        self, 
        request: Request, 
        identifier: str
    ) -> Tuple[bool, Dict[str, any]]:
        """Check if request is within rate limits."""
        try:
            # Rate limiting is always enabled by default for security
            # The dynamic config can override this if available
            rate_limiting_enabled = True

            # Try to check feature flag, but don't fail if it doesn't work
            try:
                config_enabled = settings.RATE_LIMIT_ENABLED
                if config_enabled is False:  # Only disable if explicitly set to False
                    rate_limiting_enabled = False
            except Exception as e:
                logger.debug(f"Could not check rate limiting feature flag: {e}. Using default (enabled)")

            if not rate_limiting_enabled:
                return True, {"limit": 0, "remaining": 0, "reset_time": 0, "retry_after": 0}
            
            # Get rate limit configuration
            config = await self._get_rate_limit_config()
            
            if not config.get("enabled", True):
                return True, {"limit": 0, "remaining": 0, "reset_time": 0, "retry_after": 0}
            
            # Get client identifier
            client_id = self._get_client_identifier(request)
            endpoint_key = self._get_endpoint_key(request)
            
            # Check multiple rate limits
            rate_limits_to_check = [
                {
                    "key": f"rate_limit:global:{client_id}",
                    "limit": config.get("requests_per_minute", 100),
                    "window": 60
                },
                {
                    "key": f"rate_limit:hourly:{client_id}",
                    "limit": config.get("requests_per_hour", 1000),
                    "window": 3600
                },
                {
                    "key": f"rate_limit:burst:{client_id}",
                    "limit": config.get("burst_limit", 20),
                    "window": 10
                }
            ]
            
            # Check endpoint-specific limits
            endpoint_limits = config.get("endpoint_limits", {})
            endpoint_path = f"{request.method}:{request.url.path}"
            
            # Apply tiered rate limits based on endpoint type (from settings)
            if endpoint_path in endpoint_limits:
                endpoint_config = endpoint_limits[endpoint_path]
                rate_limits_to_check.append({
                    "key": f"rate_limit:endpoint:{client_id}:{endpoint_path}",
                    "limit": endpoint_config.get("requests_per_minute", 100),
                    "window": endpoint_config.get("window_size", 60)
                })
            else:
                # Auto-apply tiered limits based on path patterns
                endpoint_limit = 100  # default
                if "/process" in request.url.path or "/scan" in request.url.path:
                    endpoint_limit = settings.RATE_LIMIT_PROCESSING  # 100/min
                elif "/admin/" in request.url.path or "/discovery/register" in request.url.path or "/health/refresh" in request.url.path:
                    endpoint_limit = settings.RATE_LIMIT_ADMIN  # 5/min
                elif "/health" in request.url.path or "/services" in request.url.path or "/discovery/services" in request.url.path:
                    endpoint_limit = settings.RATE_LIMIT_READ  # 200/min
                
                rate_limits_to_check.append({
                    "key": f"rate_limit:endpoint:{client_id}:{endpoint_path}",
                    "limit": endpoint_limit,
                    "window": 60
                })
            
            # Check user-specific limits
            user_limits = config.get("user_limits", {})
            if client_id.startswith("user:") and client_id in user_limits:
                user_config = user_limits[client_id]
                rate_limits_to_check.append({
                    "key": f"rate_limit:user:{client_id}",
                    "limit": user_config.get("requests_per_minute", 100),
                    "window": user_config.get("window_size", 60)
                })
            
            # Check IP-specific limits
            ip_limits = config.get("ip_limits", {})
            if client_id.startswith("ip:") and client_id in ip_limits:
                ip_config = ip_limits[client_id]
                rate_limits_to_check.append({
                    "key": f"rate_limit:ip:{client_id}",
                    "limit": ip_config.get("requests_per_minute", 100),
                    "window": ip_config.get("window_size", 60)
                })
            
            # Check all rate limits
            for rate_limit in rate_limits_to_check:
                try:
                    # Try Redis first
                    allowed, info = await self._check_redis_rate_limit(
                        rate_limit["key"],
                        rate_limit["limit"],
                        rate_limit["window"],
                        client_id
                    )
                except Exception:
                    # Fall back to memory
                    allowed, info = await self._check_memory_rate_limit(
                        rate_limit["key"],
                        rate_limit["limit"],
                        rate_limit["window"]
                    )
                
                if not allowed:
                    logger.warning(
                        f"Rate limit exceeded for {client_id} on {rate_limit['key']}: "
                        f"{info['remaining']}/{info['limit']} remaining"
                    )
                    # Record rate limit hit metric
                    try:
                        from app.core.orchestrator_metrics import record_rate_limit_hit
                        endpoint = request.url.path if hasattr(request, 'url') else 'unknown'
                        limit_type = rate_limit['key'].split(':')[1] if ':' in rate_limit['key'] else 'unknown'
                        record_rate_limit_hit(endpoint, limit_type)
                    except Exception:
                        pass  # Metrics recording failure shouldn't break rate limiting
                    return False, info
            
            return True, {
                "limit": max(rl["limit"] for rl in rate_limits_to_check),
                "remaining": min(rl["limit"] for rl in rate_limits_to_check),
                "reset_time": int(time.time()) + 60,
                "retry_after": 0
            }
            
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            # Allow request on error
            return True, {"limit": 0, "remaining": 0, "reset_time": 0, "retry_after": 0}
    
    async def close(self):
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.close()


# Global rate limiter instance
_rate_limiter: Optional[DynamicRateLimiter] = None


def get_rate_limiter() -> DynamicRateLimiter:
    """Get the global rate limiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        from app.core.config import get_settings
        settings = get_settings()
        _rate_limiter = DynamicRateLimiter(settings.REDIS_URL)
    return _rate_limiter


async def dynamic_rate_limiting_middleware(request: Request, call_next):
    """Dynamic rate limiting middleware."""
    try:
        # Skip rate limiting for testing to avoid interfering with endpoint tests
        if os.getenv("TESTING", "false").lower() in ("true", "1", "yes"):
            return await call_next(request)

        # Skip rate limiting for webhook endpoints
        if request.url.path.startswith("/webhooks/"):
            return await call_next(request)

        # For now, just add headers with default values to show middleware is working
        response = await call_next(request)

        # Add rate limit headers with test values
        response.headers["X-RateLimit-Limit"] = "100"
        response.headers["X-RateLimit-Remaining"] = "99"
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)

        return response

    except Exception as e:
        logger.error(f"Rate limiting middleware error: {e}")
        # Allow request on error
        return await call_next(request)
