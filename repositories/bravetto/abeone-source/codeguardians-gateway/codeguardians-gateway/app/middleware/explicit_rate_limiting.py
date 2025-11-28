"""
Explicit Rate Limiting Middleware

Provides explicit rate limiting decorators for endpoints.
Complements global rate limiting middleware.
"""

from typing import Callable, Optional
from functools import wraps
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import RateLimitError
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


def rate_limit(
    requests_per_minute: int = 100,
    requests_per_hour: int = 1000,
    key_func: Optional[Callable] = None
):
    """
    Decorator for explicit rate limiting on endpoints.
    
    Args:
        requests_per_minute: Maximum requests per minute
        requests_per_hour: Maximum requests per hour
        key_func: Optional function to generate rate limit key
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from kwargs
            request: Optional[Request] = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                for key, value in kwargs.items():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if not request:
                # No request found, proceed without rate limiting
                return await func(*args, **kwargs)
            
            # Generate rate limit key
            if key_func:
                rate_key = key_func(request)
            else:
                # Default: use endpoint + IP
                endpoint = f"{request.method}:{request.url.path}"
                client_ip = request.client.host if request.client else "unknown"
                rate_key = f"rate_limit:{endpoint}:{client_ip}"
            
            # Check rate limits (this would integrate with Redis rate limiter)
            # For now, this is a placeholder that works with global middleware
            # In production, this would check Redis and increment counters
            
            try:
                return await func(*args, **kwargs)
            except RateLimitError as e:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded: {str(e)}"
                )
        
        return wrapper
    return decorator


def public_rate_limit(requests_per_minute: int = 60):
    """
    Decorator for public endpoints with stricter rate limiting.
    
    Args:
        requests_per_minute: Maximum requests per minute for public endpoints
    """
    return rate_limit(
        requests_per_minute=requests_per_minute,
        requests_per_hour=requests_per_minute * 60
    )


def admin_rate_limit(requests_per_minute: int = 200):
    """
    Decorator for admin endpoints with higher rate limits.
    
    Args:
        requests_per_minute: Maximum requests per minute for admin endpoints
    """
    return rate_limit(
        requests_per_minute=requests_per_minute,
        requests_per_hour=requests_per_minute * 60
    )

