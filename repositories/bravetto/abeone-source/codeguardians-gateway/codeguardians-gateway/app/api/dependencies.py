"""
API Dependencies

This module provides common dependencies for API endpoints including
authentication, authorization, and access control.
"""

from typing import Optional, List
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.core.database import get_db
from app.core.models import User
from app.core.security import verify_token, get_current_user, get_optional_current_user_from_db, get_current_superuser, get_user_by_id, get_pagination_params
from app.core.config import get_settings

logger = logging.getLogger(__name__)
security = HTTPBearer()
settings = get_settings()


def require_permissions(required_permissions: List[str]):
    """
    Dependency to require specific permissions.
    
    Args:
        required_permissions: List of permission strings required
        
    Returns:
        Dependency function that checks permissions
    """
    def permission_checker(current_user: User = Depends(get_current_user)):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        # Check if user has any of the required permissions
        user_permissions = getattr(current_user, 'permissions', [])
        if not any(perm in user_permissions for perm in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {required_permissions}"
            )
        
        return current_user
    
    return permission_checker


def require_internal_access(request: Request) -> None:
    """
    Dependency to require internal access.
    
    This checks for internal access tokens or IP whitelisting.
    """
    # Check for internal access token
    internal_token = request.headers.get("X-Internal-Token")
    if internal_token and internal_token == settings.INTERNAL_ACCESS_TOKEN:
        return None
    
    # Check for internal IP whitelist
    client_ip = request.client.host
    internal_ips = getattr(settings, 'INTERNAL_IP_WHITELIST', ['127.0.0.1', '::1'])
    
    if client_ip in internal_ips:
        return None
    
    # Check for service-to-service authentication
    service_token = request.headers.get("X-Service-Token")
    if service_token and service_token in getattr(settings, 'SERVICE_TOKENS', []):
        return None
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Internal access required"
    )


def require_admin_access(current_user: User = Depends(get_current_user)):
    """
    Dependency to require admin access.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


def get_pagination_params(
    page: int = 1,
    page_size: int = 20,
    max_page_size: int = 100
) -> dict:
    """
    Dependency to get pagination parameters.
    
    Args:
        page: Page number (1-based)
        page_size: Number of items per page
        max_page_size: Maximum allowed page size
        
    Returns:
        Dictionary with pagination parameters
    """
    if page < 1:
        page = 1
    
    if page_size < 1:
        page_size = 20
    elif page_size > max_page_size:
        page_size = max_page_size
    
    return {
        "page": page,
        "page_size": page_size,
        "offset": (page - 1) * page_size
    }


def get_current_tenant(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Dependency to get current tenant context.
    
    Returns:
        Dictionary with tenant information
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Get user's organization/tenant
    tenant_id = getattr(current_user, 'tenant_id', None)
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not associated with any tenant"
        )
    
    return {
        "tenant_id": tenant_id,
        "user_id": current_user.id,
        "user_role": getattr(current_user, 'role', 'user')
    }


def require_tenant_permission(permission: str):
    """
    Dependency to require tenant-specific permissions.
    
    Args:
        permission: Permission string required
        
    Returns:
        Dependency function that checks tenant permissions
    """
    def permission_checker(
        tenant_context: dict = Depends(get_current_tenant),
        current_user: User = Depends(get_current_user)
    ):
        # Check tenant-level permissions
        tenant_permissions = getattr(current_user, 'tenant_permissions', [])
        if permission not in tenant_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Tenant permission required: {permission}"
            )
        
        return tenant_context
    
    return permission_checker


def validate_request_size(max_size: int = 1024 * 1024):  # 1MB default
    """
    Dependency to validate request size.
    
    Args:
        max_size: Maximum allowed request size in bytes
        
    Returns:
        Dependency function that validates request size
    """
    def size_validator(request: Request):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Request too large. Maximum size: {max_size} bytes"
            )
        return None
    
    return size_validator


def rate_limit_by_user(
    requests_per_minute: int = 60,
    requests_per_hour: int = 1000
):
    """
    Dependency to apply rate limiting by user.
    
    Args:
        requests_per_minute: Max requests per minute
        requests_per_hour: Max requests per hour
        
    Returns:
        Dependency function that applies rate limiting
    """
    def rate_limiter(
        current_user: User = Depends(get_current_user),
        request: Request = None
    ):
        # This would integrate with Redis-based rate limiting
        # For now, we'll just return the user
        return current_user
    
    return rate_limiter


def require_api_key(api_key: Optional[str] = None):
    """
    Dependency to require API key authentication.
    
    Args:
        api_key: API key from query parameter or header
        
    Returns:
        Dependency function that validates API key
    """
    def api_key_validator(request: Request):
        # Check for API key in header
        api_key_header = request.headers.get("X-API-Key")
        
        # Check for API key in query parameter
        api_key_query = request.query_params.get("api_key")
        
        # Use provided key or from request
        key_to_check = api_key or api_key_header or api_key_query
        
        if not key_to_check:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required"
            )
        
        # Validate API key
        valid_keys = getattr(settings, 'API_KEYS', [])
        if key_to_check not in valid_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        return key_to_check
    
    return api_key_validator