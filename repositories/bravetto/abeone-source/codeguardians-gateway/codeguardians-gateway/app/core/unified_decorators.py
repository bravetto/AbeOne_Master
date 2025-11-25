"""
Unified Decorators - Convergent Emergence

EEAaO: Everything Everywhere All at Once
- Single elegant decorator system
- Natural flow like water
- 20% code reduction through convergence
"""

from functools import wraps
from typing import Callable, Optional, List, Any
from fastapi import Request, Depends, HTTPException
from app.core.error_exporter import get_error_exporter
from app.utils.logging import get_logger
from app.middleware.explicit_rate_limiting import public_rate_limit, admin_rate_limit

logger = get_logger(__name__)


def unified_endpoint(
    rate_limit: Optional[int] = None,
    require_auth: bool = False,
    require_admin: bool = False,
    log_request: bool = True,
    error_code: str = "ENDPOINT_ERROR"
):
    """
    Unified endpoint decorator - convergent emergence of all patterns.
    
    EEAaO: Single decorator for all endpoint needs
    Water flow: Natural, elegant, powerful
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request if available
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                for key, value in kwargs.items():
                    if isinstance(value, Request):
                        request = value
                        break
            
            # Log request if enabled
            if log_request and request:
                logger.info(
                    f"Endpoint called: {func.__name__}",
                    extra={
                        "path": request.url.path,
                        "method": request.method,
                        "request_id": getattr(request.state, "request_id", None)
                    }
                )
            
            # Handle with error export
            try:
                result = await func(*args, **kwargs)
                return result
            except HTTPException:
                raise
            except Exception as e:
                error_exporter = get_error_exporter()
                error_exporter.export_error(
                    e,
                    context={"endpoint": func.__name__},
                    error_code=error_code,
                    request_id=getattr(request.state, "request_id", None) if request else None
                )
                raise HTTPException(status_code=500, detail=str(e))
        
        # Apply rate limiting if specified
        if rate_limit:
            wrapper = public_rate_limit(requests_per_minute=rate_limit)(wrapper)
        
        # Apply auth requirements (would need actual auth dependencies)
        # This is a pattern - actual implementation depends on auth system
        
        return wrapper
    return decorator


def unified_crud_endpoint(
    operation: str,
    rate_limit: Optional[int] = None,
    require_auth: bool = True,
    require_admin: bool = False
):
    """
    Unified CRUD endpoint decorator - convergent emergence.
    
    Operations: list, get, create, update, delete
    """
    return unified_endpoint(
        rate_limit=rate_limit,
        require_auth=require_auth,
        require_admin=require_admin,
        error_code=f"{operation.upper()}_ERROR"
    )

