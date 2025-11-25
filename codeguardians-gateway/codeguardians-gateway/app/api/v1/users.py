"""
User management API endpoints.

This module provides user management endpoints including
user CRUD operations and profile management.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, or_
from pydantic import BaseModel, EmailStr, Field

from app.core.database import get_db
from app.core.models import User
from app.core.security import get_password_hash, validate_password_strength, get_current_user
from app.core.exceptions import ValidationError, NotFoundError, ConflictError
from app.api.dependencies import (
    get_current_superuser, get_user_by_id,
    get_pagination_params, require_permissions,
    require_admin_access
)
from app.middleware.tenant_context import CurrentTenant
from app.core.security import get_current_user_from_db
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


# Pydantic models
class UserResponse(BaseModel):
    """User response model."""
    id: int
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: str
    last_login: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """User creation model."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserProfileUpdate(BaseModel):
    """User profile update model."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)


class PasswordUpdate(BaseModel):
    """Password update model."""
    current_password: str
    new_password: str = Field(..., min_length=8)


class UserListResponse(BaseModel):
    """User list response model."""
    users: List[UserResponse]
    total: int
    page: int
    size: int
    pages: int


# User management endpoints
@router.get("/me", response_model=UserResponse, summary="Get current user profile")
async def get_my_profile() -> UserResponse:
    """
    Get current user's profile.

    Returns:
        User profile information
    """
    # For now, return 401 since we don't have real authentication set up
    from fastapi import HTTPException
    raise HTTPException(status_code=401, detail="Authentication required")


@router.put("/me", response_model=UserResponse, summary="Update current user profile")
async def update_my_profile(
    profile_data: UserProfileUpdate
) -> UserResponse:
    """
    Update current user's profile.

    Args:
        profile_data: Profile update data

    Returns:
        Updated user profile

    Raises:
        HTTPException: Authentication required
    """
    # For now, return 401 since we don't have real authentication set up
    from fastapi import HTTPException
    raise HTTPException(status_code=401, detail="Authentication required")


@router.delete("/me", summary="Delete current user account")
async def delete_my_account() -> Dict[str, str]:
    """
    Delete current user's account.

    Returns:
        Success message
    """
    # For now, return 401 since we don't have real authentication set up
    from fastapi import HTTPException
    raise HTTPException(status_code=401, detail="Authentication required")


# Admin endpoints
@router.get("/", response_model=UserListResponse, summary="List all users (Admin)")
async def list_users(
    pagination: Dict[str, int] = Depends(get_pagination_params),
    search: Optional[str] = Query(None, description="Search by email or name"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_verified: Optional[bool] = Query(None, description="Filter by verification status"),
    admin_user: User = Depends(require_admin_access),
    db: AsyncSession = Depends(get_db)
) -> UserListResponse:
    """
    List all users with pagination and filtering (Admin only).

    Args:
        pagination: Pagination parameters
        search: Search query
        is_active: Filter by active status
        is_verified: Filter by verification status
        admin_user: Admin user (verified by dependency)
        db: Database session

    Returns:
        Paginated list of users
    """
    try:
        query = select(User)
        
        # Apply filters
        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                or_(
                    User.email.ilike(search_pattern),
                    User.full_name.ilike(search_pattern)
                )
            )
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        if is_verified is not None:
            query = query.where(User.is_verified == is_verified)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        query = query.offset(pagination["offset"]).limit(pagination["page_size"])
        query = query.order_by(User.created_at.desc())
        
        # Execute query
        result = await db.execute(query)
        users = result.scalars().all()
        
        # Convert to response format
        user_responses = [
            UserResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                is_superuser=user.is_superuser,
                created_at=user.created_at.isoformat() if user.created_at else "",
                last_login=user.last_login.isoformat() if user.last_login else None
            )
            for user in users
        ]
        
        pages = (total + pagination["page_size"] - 1) // pagination["page_size"]
        
        return UserListResponse(
            users=user_responses,
            total=total,
            page=pagination["page"],
            size=pagination["page_size"],
            pages=pages
        )
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")


@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID (Admin)")
async def get_user(
    user_id: int,
    admin_user: User = Depends(require_admin_access),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Get user by ID (Admin only).

    Args:
        user_id: User ID
        admin_user: Admin user (verified by dependency)
        db: Database session

    Returns:
        User information

    Raises:
        HTTPException: Admin access required or user not found
    """
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        return UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
            created_at=user.created_at.isoformat() if user.created_at else "",
            last_login=user.last_login.isoformat() if user.last_login else None
        )
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user")


@router.post("/", response_model=UserResponse, summary="Create new user (Admin)")
async def create_user(
    user_data: UserCreate
) -> UserResponse:
    """
    Create a new user (Admin only).

    Args:
        user_data: User creation data

    Returns:
        Created user information

    Raises:
        HTTPException: Admin access required
    """
    # For now, return 403 since we don't have real authentication set up
    from fastapi import HTTPException
    raise HTTPException(status_code=403, detail="Admin access required")


@router.put("/{user_id}", response_model=UserResponse, summary="Update user (Admin)")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    admin_user: User = Depends(require_admin_access),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Update user (Admin only).

    Args:
        user_id: User ID
        user_data: User update data
        admin_user: Admin user (verified by dependency)
        db: Database session

    Returns:
        Updated user information

    Raises:
        HTTPException: Admin access required or user not found
    """
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Update user fields
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        
        logger.info(f"Admin {admin_user.email} updated user: {user.email}")
        
        return UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
            created_at=user.created_at.isoformat() if user.created_at else "",
            last_login=user.last_login.isoformat() if user.last_login else None
        )
    except NotFoundError:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user")


@router.delete("/{user_id}", summary="Delete user (Admin)")
async def delete_user(
    user_id: int,
    admin_user: User = Depends(require_admin_access),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Delete user (Admin only).

    Args:
        user_id: User ID
        admin_user: Admin user (verified by dependency)
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: Admin access required or user not found
    """
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Prevent self-deletion
        if user.id == admin_user.id:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")
        
        await db.execute(delete(User).where(User.id == user_id))
        await db.commit()
        
        logger.info(f"Admin {admin_user.email} deleted user: {user.email}")
        
        return {"message": f"User {user_id} deleted successfully"}
    except NotFoundError:
        raise
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete user")


@router.post("/{user_id}/activate", summary="Activate user (Admin)")
async def activate_user(
    user_id: int,
    admin_user: User = Depends(require_admin_access),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Activate user account (Admin only).

    Args:
        user_id: User ID
        admin_user: Admin user (verified by dependency)
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: Admin access required or user not found
    """
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        user.is_active = True
        await db.commit()
        await db.refresh(user)
        
        logger.info(f"Admin {admin_user.email} activated user: {user.email}")
        
        return {"message": f"User {user_id} activated successfully"}
    except NotFoundError:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error activating user: {e}")
        raise HTTPException(status_code=500, detail="Failed to activate user")


@router.post("/{user_id}/deactivate", summary="Deactivate user (Admin)")
async def deactivate_user(
    user_id: int,
    request: Request,
    admin_user: User = Depends(require_admin_access),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Deactivate user account (Admin only).

    Args:
        user_id: User ID
        admin_user: Admin user (verified by dependency)
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: Admin access required or user not found
    """
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Prevent self-deactivation
        if user.id == admin_user.id:
            raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
        
        user.is_active = False
        await db.commit()
        await db.refresh(user)
        
        # Audit log
        from app.core.audit_logger import log_user_deactivation
        await log_user_deactivation(
            db=db,
            admin_user_id=admin_user.id,
            target_user_id=user_id,
            organization_id=str(getattr(admin_user, 'organization_id', None)) if hasattr(admin_user, 'organization_id') else None,
            request=request
        )
        
        logger.info(f"Admin {admin_user.email} deactivated user: {user.email}")
        
        return {"message": f"User {user_id} deactivated successfully"}
    except NotFoundError:
        raise
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deactivating user: {e}")
        raise HTTPException(status_code=500, detail="Failed to deactivate user")
