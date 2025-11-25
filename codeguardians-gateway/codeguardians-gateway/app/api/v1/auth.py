"""
Authentication API endpoints.

This module provides authentication-related endpoints including
login, logout, token refresh, and password management.
"""

from datetime import timedelta, datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, Field

from app.core.database import get_db
from app.core.models import User, BiasGuardAuditLog, BiasGuardPolicyViolation
from app.core.security import (
    create_access_token, create_refresh_token,
    verify_token, generate_password_reset_token, verify_password_reset_token,
    generate_email_verification_token, verify_email_verification_token,
    get_biasguard_validator
)
from app.core.config import get_settings
from app.core.exceptions import AuthenticationError, ValidationError, NotFoundError
from app.api.dependencies import get_current_user, get_optional_current_user_from_db
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()
settings = get_settings()


# Pydantic models
class Token(BaseModel):
    """Token response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token data model."""
    access_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserRegister(BaseModel):
    """User registration model."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=255)


class PasswordReset(BaseModel):
    """Password reset model."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation model."""
    token: str
    new_password: str = Field(..., min_length=8)


class PasswordChange(BaseModel):
    """Password change model."""
    current_password: str
    new_password: str = Field(..., min_length=8)


class EmailVerification(BaseModel):
    """Email verification model."""
    token: str


# Authentication endpoints
@router.post("/login", response_model=Token, summary="User login with Clerk")
async def login(
    clerk_token: str,
    db: AsyncSession = Depends(get_db)
) -> Token:
    """
    Authenticate user using Clerk JWT token and return access and refresh tokens.
    
    Args:
        clerk_token: Clerk JWT token
        db: Database session
        
    Returns:
        Token response with access and refresh tokens
        
    Raises:
        AuthenticationError: If authentication fails
    """
    try:
        from app.core.clerk_integration import verify_clerk_token, get_or_create_user_from_clerk
        
        # Verify Clerk JWT token
        clerk_user = await verify_clerk_token(clerk_token)
        
        # Get or create user from Clerk data
        user = await get_or_create_user_from_clerk(clerk_user, db)
        
        if not user.is_active:
            raise AuthenticationError("User account is disabled")
        
    except AuthenticationError:
        # Re-raise authentication errors
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise AuthenticationError("Authentication failed")
    
    # Enforce BiasGuard policies
    if settings.is_biasguard_enabled:
        biasguard = get_biasguard_validator()
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "is_superuser": user.is_superuser,
        }
        
        # Check fairness policy if enabled
        if settings.BIASGUARD_ENFORCE_FAIRNESS:
            fairness_result = biasguard.enforce_policy("BIAS_FAIRNESS_001", user_data)
            if not fairness_result.get("enforced"):
                logger.warning(f"BiasGuard fairness check failed for user {user.email}: {fairness_result['violations']}")
                # Log the violation
                try:
                    audit_log = BiasGuardAuditLog(
                        audit_id=fairness_result.get("audit_id"),
                        user_id=user.id,
                        user_email=user.email,
                        event_type="fairness_check_failed",
                        event_status="violation",
                        enforcement_type="fairness_check",
                        policy_name="Equal Opportunity Policy",
                        enforcement_passed=False,
                        violations=fairness_result.get("violations"),
                        fairness_metrics=fairness_result.get("fairness_metrics")
                    )
                    db.add(audit_log)
                    await db.commit()
                except Exception as e:
                    logger.error(f"Failed to log BiasGuard violation: {e}")
        
        # Check compliance policy if enabled
        if settings.BIASGUARD_ENFORCE_COMPLIANCE:
            compliance_result = biasguard.enforce_policy("BIAS_COMPLIANCE_001", user_data)
            if not compliance_result.get("enforced"):
                logger.warning(f"BiasGuard compliance check failed for user {user.email}: {compliance_result['violations']}")
                try:
                    audit_log = BiasGuardAuditLog(
                        audit_id=compliance_result.get("audit_id"),
                        user_id=user.id,
                        user_email=user.email,
                        event_type="compliance_check_failed",
                        event_status="violation",
                        enforcement_type="compliance",
                        policy_name="Compliance & Audit Policy",
                        enforcement_passed=False,
                        violations=compliance_result.get("violations")
                    )
                    db.add(audit_log)
                    await db.commit()
                except Exception as e:
                    logger.error(f"Failed to log compliance violation: {e}")
        
        # Log attribution if enabled
        if settings.BIASGUARD_ENFORCE_ATTRIBUTION:
            attribution_result = biasguard.enforce_policy("BIAS_ATTR_001", user_data)
            try:
                audit_log = BiasGuardAuditLog(
                    audit_id=attribution_result.get("audit_id"),
                    user_id=user.id,
                    user_email=user.email,
                    event_type="login_attribution",
                    event_status="success",
                    enforcement_type="attribute_based",
                    policy_name="Attribution Tracking Policy",
                    enforcement_passed=True,
                    context_data={
                        "login_timestamp": datetime.now(timezone.utc).isoformat(),
                        "user_full_name": user.full_name
                    }
                )
                db.add(audit_log)
                await db.commit()
            except Exception as e:
                logger.error(f"Failed to log attribution: {e}")
    
    # Update last login
    from sqlalchemy import update, func
    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(last_login=func.now())
    )
    await db.commit()
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=refresh_token_expires
    )
    
    logger.info(f"User {user.email} logged in successfully")
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/register", response_model=Dict[str, str], summary="User registration with Clerk")
async def register(
    clerk_token: str,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Register a new user using Clerk JWT token.
    
    Args:
        clerk_token: Clerk JWT token
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        AuthenticationError: If token verification fails
    """
    try:
        from app.core.clerk_integration import verify_clerk_token, get_or_create_user_from_clerk
        
        # Verify Clerk JWT token
        clerk_user = await verify_clerk_token(clerk_token)
        
        # Get or create user from Clerk data
        user = await get_or_create_user_from_clerk(clerk_user, db)
        
        logger.info(f"User {user.email} registered/updated successfully via Clerk")
        
        return {
            "message": "User registered successfully",
            "user_id": str(user.id),
            "email": user.email
        }
        
    except AuthenticationError:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise AuthenticationError("Registration failed")


@router.post("/refresh", response_model=TokenData, summary="Refresh access token")
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
) -> TokenData:
    """
    Refresh access token using refresh token.
    
    Args:
        refresh_token: Refresh token
        db: Database session
        
    Returns:
        New access token
        
    Raises:
        AuthenticationError: If refresh token is invalid
    """
    try:
        # Verify refresh token
        payload = verify_token(refresh_token, token_type="refresh")
        user_email = payload.get("sub")
        
        if not user_email:
            raise AuthenticationError("Invalid refresh token")
        
        # Get user
        from sqlalchemy import select
        result = await db.execute(
            select(User).where(User.email == user_email)
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        return TokenData(access_token=access_token)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise AuthenticationError("Token refresh failed")


@router.post("/logout", summary="User logout")
async def logout(
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Logout user (invalidate tokens on client side).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    # In a real application, you would invalidate the token
    # by adding it to a blacklist or updating the user's session
    
    logger.info(f"User {current_user.email} logged out")
    
    return {"message": "Logged out successfully"}


@router.post("/password-reset", summary="Request password reset")
async def request_password_reset(
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Password reset is handled by Clerk - this endpoint validates input and redirects.

    Args:
        reset_data: Password reset request data
        db: Database session

    Returns:
        Success message directing user to Clerk

    Raises:
        ValidationError: If email format is invalid
        HTTPException: If database is unavailable
    """
    from app.core.exceptions import ValidationError

    # Validate email format
    if not reset_data.email or "@" not in reset_data.email:
        raise ValidationError("Invalid email format")

    try:
        # Check if user exists (don't reveal if user exists for security)
        from sqlalchemy import select
        result = await db.execute(
            select(User).where(User.email == reset_data.email)
        )
        user = result.scalar_one_or_none()
    except RuntimeError as e:
        # Database is disabled or unavailable
        logger.error(f"Database unavailable for password reset: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable - database connection failed"
        )
    except Exception as e:
        # Other database errors
        logger.error(f"Database error during password reset: {e}", exc_info=True)
        # Still return success message for security (don't reveal if error occurred)
        pass

    # Always return the same message for security (don't reveal if user exists)
    logger.info(f"Password reset requested for {reset_data.email} - redirecting to Clerk")

    return {
        "message": "If an account with this email exists, a password reset link has been sent.",
        "clerk_redirect": "Use Clerk's password reset functionality",
        "next_steps": [
            "Check your email for password reset instructions",
            "Click the reset link to create a new password",
            "The link will expire in 24 hours"
        ]
    }


@router.post("/password-reset/confirm", summary="Confirm password reset")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Password reset confirmation is handled by Clerk - this endpoint is kept for compatibility.
    
    Args:
        reset_data: Password reset confirmation data
        db: Database session
        
    Returns:
        Success message directing user to Clerk
    """
    logger.info(f"Password reset confirmation requested - redirecting to Clerk")
    
    return {
        "message": "Password reset confirmation is handled by Clerk. Please use the Clerk password reset flow.",
        "clerk_redirect": "Use Clerk's password reset functionality"
    }


# Password change functionality removed - using Clerk for authentication


@router.post("/verify-email", summary="Verify email address")
async def verify_email(
    verification_data: EmailVerification,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Verify email address with token.

    Args:
        verification_data: Email verification data
        db: Database session

    Returns:
        Success message

    Raises:
        ValidationError: If token format is invalid
        NotFoundError: If user is not found
    """
    from app.core.exceptions import ValidationError

    # Validate token format
    if not verification_data.token or len(verification_data.token.strip()) == 0:
        raise ValidationError(message="Verification token is required")

    # Verify email verification token
    try:
        email = verify_email_verification_token(verification_data.token)
    except ValueError as e:
        logger.warning(f"Invalid verification token format: {e}")
        raise ValidationError(message="Invalid or expired verification token")
    except Exception as e:
        logger.error(f"Email verification failed: {type(e).__name__}: {e}")
        raise ValidationError(message="Email verification failed")
    
    # Get user
    from sqlalchemy import select, update
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundError("User not found")
    
    # Update user verification status
    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(is_verified=True)
    )
    await db.commit()
    
    logger.info(f"Email verified for user {email}")
    
    return {"message": "Email verified successfully"}


@router.get("/me", summary="Get current user")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "is_superuser": current_user.is_superuser,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }
