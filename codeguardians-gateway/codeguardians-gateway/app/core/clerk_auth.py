"""
Clerk Authentication Middleware and Dependencies

This module provides Clerk JWT authentication integration for the gateway.
Uses Clerk's JWT tokens as the unified API key for all guard services.
"""

import jwt
import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings
from app.core.exceptions import ClerkTokenError, ClerkJWKSFetchError, ClerkError

settings = get_settings()
security = HTTPBearer()


async def verify_clerk_token(token: str) -> Dict[str, Any]:
    """
    Verify a Clerk JWT token and return the payload using proper JWKS verification.

    Args:
        token: The JWT token to verify

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Import the secure verification function
        from app.core.clerk_integration import verify_clerk_token as secure_verify

        # Use the secure JWKS-based verification
        return await secure_verify(token)

    except ClerkTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ClerkJWKSFetchError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ClerkError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")


async def get_current_user_clerk(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Get current user from Clerk JWT token.
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        User information from token payload
    """
    if not settings.is_clerk_enabled:
        raise HTTPException(status_code=503, detail="Clerk authentication is not enabled")
    
    token = credentials.credentials
    payload = await verify_clerk_token(token)
    
    return {
        "user_id": payload.get("sub") or payload.get("user_id"),
        "email": payload.get("email"),
        "session_id": payload.get("sid"),
        "org_id": payload.get("org_id"),
        "role": payload.get("role"),
        "auth_type": "clerk"
    }


class ClerkAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract Clerk JWT token and add it to request state.
    This allows the unified API key to be derived from Clerk tokens.
    """
    
    async def dispatch(self, request: Request, call_next):
        """Process request and extract Clerk token."""
        # Skip authentication for health checks, public endpoints, and webhooks
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"] or request.url.path.startswith("/webhooks/"):
            return await call_next(request)
        
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            
            # Verify token and add user info to request state
            try:
                if settings.is_clerk_enabled:
                    payload = await verify_clerk_token(token)
                    request.state.user = {
                        "user_id": payload.get("sub") or payload.get("user_id"),
                        "email": payload.get("email"),
                        "session_id": payload.get("sid"),
                        "org_id": payload.get("org_id"),
                        "role": payload.get("role"),
                        "auth_type": "clerk"
                    }
                    # Set unified API key from Clerk token
                    request.state.unified_api_key = token
            except HTTPException:
                # Token verification failed, but continue (some endpoints don't require auth)
                pass
        
        response = await call_next(request)
        return response


def get_unified_api_key_from_request(request: Request) -> Optional[str]:
    """
    Get unified API key from request state (set by Clerk middleware) or headers.
    
    Checks multiple sources in order:
    1. request.state.unified_api_key (set by Clerk middleware)
    2. X-Unified-API-Key header
    3. X-API-Key header
    4. Authorization Bearer token header
    5. UNIFIED_API_KEY environment variable (fallback)
    
    Args:
        request: FastAPI request object
        
    Returns:
        Unified API key or None
    """
    # Check request state first (set by Clerk middleware)
    if hasattr(request.state, "unified_api_key"):
        return request.state.unified_api_key
    
    # Check X-Unified-API-Key header
    unified_key = request.headers.get("X-Unified-API-Key")
    if unified_key:
        return unified_key
    
    # Check X-API-Key header
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return api_key
    
    # Check Authorization Bearer token header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.replace("Bearer ", "")
    
    # Fallback to environment variable
    import os
    env_key = os.getenv("UNIFIED_API_KEY") or os.getenv("GATEWAY_API_KEY")
    if env_key:
        return env_key
    
    return None


def get_user_from_request(request: Request) -> Optional[Dict[str, Any]]:
    """
    Get user information from request state.
    
    Args:
        request: FastAPI request object
        
    Returns:
        User information dictionary or None
    """
    return getattr(request.state, "user", None)
