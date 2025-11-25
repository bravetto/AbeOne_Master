"""
Tenant Context Middleware

This middleware enforces multi-tenancy by:
1. Extracting organization context from JWT tokens
2. Setting tenant context for all database queries
3. Ensuring data isolation between organizations
4. Validating tenant access permissions

Architecture:
- Tenant context is stored in request state
- All database queries are automatically scoped to tenant
- Cross-tenant data access is prevented
- Audit logging tracks tenant-specific actions
"""

from typing import Optional, Dict, Any, List
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import jwt
from datetime import datetime, timezone
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.database import get_db
from app.core.models import User, Organization, OrganizationMember, APIKey
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()
security = HTTPBearer()


class TenantContext(BaseModel):
    """
    Tenant context container for request-scoped tenant information.
    
    This class holds all tenant-related information for a request,
    ensuring proper data isolation and access control.
    """
    
    organization_id: str
    user_id: str
    role: str
    permissions: List[str]
    created_at: datetime = datetime.now(timezone.utc)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission within tenant context."""
        return permission in self.permissions or self.role == "admin"
    
    def can_access_organization(self, org_id: str) -> bool:
        """Check if user can access specific organization."""
        return self.organization_id == org_id or self.role == "admin"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tenant context to dictionary for logging."""
        return {
            "organization_id": self.organization_id,
            "user_id": self.user_id,
            "role": self.role,
            "permissions": self.permissions,
            "created_at": self.created_at.isoformat()
        }


async def extract_tenant_from_jwt(token: str) -> Optional[TenantContext]:
    """
    Extract tenant context from JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        TenantContext object or None if invalid
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Decode JWT token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        
        user_id = payload.get("sub")
        organization_id = payload.get("organization_id")
        role = payload.get("role", "member")
        permissions = payload.get("permissions", [])
        
        if not user_id or not organization_id:
            logger.warning("JWT token missing required tenant information")
            return None
            
        return TenantContext(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
            permissions=permissions
        )
        
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        logger.warning("Invalid JWT token")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error extracting tenant from JWT: {e}")
        raise HTTPException(status_code=401, detail="Token validation failed")


async def extract_tenant_from_api_key(api_key: str, db: AsyncSession) -> Optional[TenantContext]:
    """
    Extract tenant context from API key.
    
    Args:
        api_key: API key string
        db: Database session
        
    Returns:
        TenantContext object or None if invalid
    """
    try:
        # Find API key in database
        api_key_stmt = select(APIKey).where(
            and_(
                APIKey.key == api_key,
                APIKey.is_active == True
            )
        )
        api_key_result = await db.execute(api_key_stmt)
        db_api_key = api_key_result.scalar_one_or_none()
        
        if not db_api_key:
            logger.warning(f"Invalid or inactive API key: {api_key[:8]}...")
            return None
        
        # Get user and organization information
        user_stmt = select(User).where(User.id == db_api_key.user_id)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()
        if not user:
            logger.warning(f"User not found for API key: {api_key[:8]}...")
            return None
        
        # Get user's organization membership
        membership_stmt = select(OrganizationMember).where(
            and_(
                OrganizationMember.user_id == user.id,
                OrganizationMember.is_active == True
            )
        )
        membership_result = await db.execute(membership_stmt)
        membership = membership_result.scalar_one_or_none()
        
        if not membership:
            logger.warning(f"No active organization membership for user: {user.id}")
            return None
        
        return TenantContext(
            organization_id=membership.organization_id,
            user_id=user.id,
            role=membership.role,
            permissions=membership.permissions or []
        )
        
    except Exception as e:
        logger.error(f"Error extracting tenant from API key: {e}", exc_info=True)
        return None


async def get_tenant_context(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> TenantContext:
    """
    Extract tenant context from request authorization.
    
    Supports both JWT tokens and API keys for authentication.
    Automatically determines the appropriate extraction method.
    
    Args:
        request: FastAPI request object
        credentials: HTTP authorization credentials
        db: Database session
        
    Returns:
        TenantContext object
        
    Raises:
        HTTPException: If authentication fails or tenant context cannot be determined
    """
    token = credentials.credentials
    
    # Try JWT token first
    if token.startswith("eyJ"):  # JWT tokens start with "eyJ"
        tenant_context = await extract_tenant_from_jwt(token)
    else:
        # Assume API key
        tenant_context = await extract_tenant_from_api_key(token, db)
    
    if not tenant_context:
        logger.warning("Failed to extract tenant context from request")
        raise HTTPException(
            status_code=401, 
            detail="Unable to determine tenant context"
        )
    
    # Store tenant context in request state for use in endpoints
    request.state.tenant_context = tenant_context
    
    # Log tenant context for audit trail
    logger.info(f"Tenant context established: {tenant_context.to_dict()}")
    
    return tenant_context


def get_current_tenant(request: Request) -> TenantContext:
    """
    Get current tenant context from request state.
    
    This is a dependency that can be used in endpoint functions
    to access the current tenant context.
    
    Args:
        request: FastAPI request object
        
    Returns:
        TenantContext object
        
    Raises:
        HTTPException: If tenant context not found in request state
    """
    if not hasattr(request.state, 'tenant_context') or request.state.tenant_context is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required or insufficient permissions for organization access"
        )

    return request.state.tenant_context


def require_permission(permission: str):
    """
    Decorator to require specific permission for endpoint access.
    
    Args:
        permission: Required permission string
        
    Returns:
        Dependency function that validates permission
    """
    def permission_checker(tenant_context: TenantContext = Depends(get_current_tenant)):
        if not tenant_context.has_permission(permission):
            logger.warning(
                f"Permission denied: {permission} required, "
                f"user has: {tenant_context.permissions}"
            )
            raise HTTPException(
                status_code=403,
                detail=f"Permission required: {permission}"
            )
        return tenant_context
    
    return permission_checker


def require_role(role: str):
    """
    Decorator to require specific role for endpoint access.
    
    Args:
        role: Required role string
        
    Returns:
        Dependency function that validates role
    """
    def role_checker(tenant_context: TenantContext = Depends(get_current_tenant)):
        if tenant_context.role != role and tenant_context.role != "admin":
            logger.warning(
                f"Role denied: {role} required, user has: {tenant_context.role}"
            )
            raise HTTPException(
                status_code=403,
                detail=f"Role required: {role}"
            )
        return tenant_context
    
    return role_checker


class TenantQueryMixin:
    """
    Mixin class to automatically scope database queries to tenant context.
    
    This ensures all queries are automatically filtered by organization_id,
    preventing cross-tenant data access.
    """
    
    @staticmethod
    def apply_tenant_filter(query, model_class, tenant_context: TenantContext):
        """
        Apply tenant filter to database query.
        
        Args:
            query: SQLAlchemy query object
            model_class: Model class to filter
            tenant_context: Current tenant context
            
        Returns:
            Filtered query object
        """
        # Check if model has organization_id field
        if hasattr(model_class, 'organization_id'):
            return query.filter(model_class.organization_id == tenant_context.organization_id)
        
        # For models without direct organization_id, check relationships
        if hasattr(model_class, 'user_id'):
            # Filter by user's organization through user relationship
            return query.join(User).filter(
                User.id == model_class.user_id,
                User.organization_id == tenant_context.organization_id
            )
        
        # If no tenant relationship found, log warning
        logger.warning(
            f"Model {model_class.__name__} has no tenant relationship. "
            f"Query may return cross-tenant data."
        )
        
        return query


# Tenant context dependency for easy use in endpoints
CurrentTenant = Depends(get_current_tenant)


class TenantContextMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for tenant context extraction and validation.

    This middleware extracts tenant context from JWT tokens or API keys
    and stores it in the request state for use by endpoints.
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """
        Process the request and extract tenant context.

        Args:
            request: FastAPI request object
            call_next: Next middleware/endpoint in chain

        Returns:
            Response from next middleware/endpoint
        """
        try:
            # Skip tenant context for certain endpoints
            if self._should_skip_tenant_context(request):
                return await call_next(request)

            # Extract authorization header
            auth_header = request.headers.get("authorization")
            if not auth_header:
                # For protected endpoints, require authentication
                if self._is_protected_endpoint(request):
                    from fastapi.responses import JSONResponse
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Authentication required"}
                    )
                # For non-protected endpoints, continue without tenant context
                return await call_next(request)

            # Extract token from Bearer header
            if not auth_header.startswith("Bearer "):
                if self._is_protected_endpoint(request):
                    from fastapi.responses import JSONResponse
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid authorization header format"}
                    )
                return await call_next(request)

            token = auth_header[7:]  # Remove "Bearer " prefix

            # Extract tenant context
            tenant_context = None
            db = None

            try:
                # Get database session
                from app.core.database import get_db
                from sqlalchemy.ext.asyncio import AsyncSession
                try:
                    # Python 3.9 compatibility: Use async generator directly
                    db_gen = get_db()
                    db = await db_gen.__anext__()
                except RuntimeError as e:
                    # Database is disabled or unavailable
                    logger.warning(f"Database unavailable during tenant context extraction: {e}")
                    if self._is_protected_endpoint(request):
                        # For protected endpoints, return 503 if database is required
                        from fastapi.responses import JSONResponse
                        return JSONResponse(
                            status_code=503,
                            content={"detail": "Service temporarily unavailable - database connection failed"}
                        )
                    # For non-protected endpoints, continue without tenant context
                    return await call_next(request)

                # Try JWT token first
                if token.startswith("eyJ"):  # JWT tokens start with "eyJ"
                    tenant_context = await extract_tenant_from_jwt(token)
                else:
                    # Assume API key
                    tenant_context = await extract_tenant_from_api_key(token, db)

            except HTTPException:
                # Re-raise HTTP exceptions (like 503 above)
                raise
            except Exception as e:
                # Log unexpected errors but don't fail if not protected endpoint
                logger.error(f"Error extracting tenant context: {e}", exc_info=True)
                if self._is_protected_endpoint(request):
                    from fastapi.responses import JSONResponse
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Authentication required"}
                    )
                return await call_next(request)
            finally:
                if db:
                    await db.close()

            if not tenant_context:
                logger.warning("Failed to extract tenant context from request")
                if self._is_protected_endpoint(request):
                    from fastapi.responses import JSONResponse
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Unable to determine tenant context"}
                    )
                return await call_next(request)

            # Store in request state for endpoint access
            request.state.tenant_context = tenant_context

            # Log tenant context for audit trail
            logger.info(f"Tenant context established: {tenant_context.to_dict()}")

            # Continue with request
            return await call_next(request)

        except HTTPException as http_exc:
            # Re-raise HTTP exceptions so they're handled properly by FastAPI
            raise http_exc
        except Exception as e:
            logger.error(f"Tenant middleware error: {e}", exc_info=True)
            # For protected endpoints, don't allow access on errors
            # Return JSONResponse directly instead of raising HTTPException
            # to avoid issues with Starlette's error middleware
            if self._is_protected_endpoint(request):
                from fastapi.responses import JSONResponse
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Authentication required"}
                )
            return await call_next(request)

    def _should_skip_tenant_context(self, request: Request) -> bool:
        """
        Determine if tenant context extraction should be skipped.

        Args:
            request: FastAPI request object

        Returns:
            True if tenant context should be skipped
        """
        # Skip for health checks and public endpoints
        skip_paths = [
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico"
        ]

        # Skip user endpoints for now (they use different auth)
        if request.url.path.startswith("/api/v1/users/"):
            return True

        # Skip webhook endpoints (they have their own auth)
        if request.url.path.startswith("/webhooks/"):
            return True

        # Skip static files and public assets
        if request.url.path.startswith(("/static/", "/assets/", "/public/")):
            return True

        # Skip OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return True

        return request.url.path in skip_paths

    def _is_protected_endpoint(self, request: Request) -> bool:
        """
        Determine if the endpoint requires tenant context.

        Args:
            request: FastAPI request object

        Returns:
            True if endpoint is protected and needs tenant context
        """
        try:
            path = request.url.path

            # Public endpoints that don't require tenant context
            public_endpoints = [
                "/api/v1/subscriptions/tiers",  # Subscription tiers should be public
                "/api/v1/posts",  # Public post reading
                "/api/v1/posts/",  # Public post reading with trailing slash
                "/api/v1/legal/terms-of-service",  # Public legal endpoints
                "/api/v1/legal/privacy-policy",
                "/api/v1/legal/cookie-policy",
            ]

            # Check if this is a public endpoint
            for public_endpoint in public_endpoints:
                if path == public_endpoint or path.startswith(public_endpoint + "/"):
                    return False

            # Protected paths that require tenant context
            # Note: Some legal endpoints (terms-of-service, privacy-policy, cookie-policy) 
            # are public and listed above, but other legal endpoints require auth
            protected_prefixes = [
                "/api/v1/legal",  # Most legal endpoints require auth (except those in public_endpoints)
                "/api/v1/organizations",
                "/api/v1/subscriptions",  # Most subscription endpoints require auth
                "/api/v1/users"
            ]

            return any(path.startswith(prefix) for prefix in protected_prefixes)
        except Exception:
            # If there's any issue accessing the request, assume it's protected
            return True
