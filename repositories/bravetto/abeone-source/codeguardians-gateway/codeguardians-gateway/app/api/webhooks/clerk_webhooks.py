"""
Clerk webhook endpoints for handling user events.

This module provides API endpoints for receiving and processing
Clerk webhook events related to user management.
"""

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.clerk_webhook_service import process_clerk_webhook, verify_clerk_webhook_signature
from app.core.config import get_settings
from app.core.database import get_db
from app.core.exceptions import ClerkWebhookError, EmailRequiredError, ValidationError

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/clerk")
async def handle_clerk_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    settings = Depends(get_settings)
) -> JSONResponse:
    """
    Handle Clerk webhook events.
    
    This endpoint receives webhook events from Clerk for user management
    including user creation, updates, and deletion.
    
    Args:
        request: The incoming HTTP request
        settings: Application settings
        
    Returns:
        JSONResponse: Success or error response
    """
    try:
        # Get the raw body for webhook signature verification
        body = await request.body()
        
        # Verify webhook signature if secret is configured
        if settings.CLERK_WEBHOOK_SECRET:
            if not verify_clerk_webhook_signature(body, dict(request.headers), settings.CLERK_WEBHOOK_SECRET):
                logger.error("Clerk webhook signature verification failed")
                raise HTTPException(status_code=401, detail="Invalid webhook signature")
        else:
            logger.warning("CLERK_WEBHOOK_SECRET not configured, skipping signature verification")
        
        # Parse the JSON payload
        import json
        try:
            payload = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in Clerk webhook payload: {e}")
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # Extract event information
        event_type = payload.get('type')
        event_data = payload.get('data', {})
        
        if not event_type:
            logger.error("No event type found in Clerk webhook payload")
            raise HTTPException(status_code=400, detail="Missing event type")
        
        logger.info(f"Received Clerk webhook event: {event_type}")
        
        # Process the webhook event
        success = await process_clerk_webhook(event_type, payload, db)

        if success:
            logger.info(f"Successfully processed Clerk webhook event: {event_type}")
            return JSONResponse(
                content={"status": "success", "event_type": event_type},
                status_code=200
            )
        else:
            # This shouldn't happen anymore since we now raise exceptions
            logger.error(f"Failed to process Clerk webhook event: {event_type}")
            return JSONResponse(
                content={"status": "error", "event_type": event_type, "message": "Failed to process event"},
                status_code=500
            )
            
    except EmailRequiredError as e:
        logger.error(f"Email required error in Clerk webhook: {e.message}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "EMAIL_REQUIRED",
                "message": e.message,
                "details": e.details
            }
        )
    except ValidationError as e:
        logger.error(f"Validation error in Clerk webhook: {e.message}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": e.error_code or "VALIDATION_ERROR",
                "message": e.message,
                "details": e.details
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing Clerk webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/clerk/users/{clerk_user_id}")
async def get_user_by_clerk_id(
    clerk_user_id: str,
    db: AsyncSession = Depends(get_db),
    settings = Depends(get_settings)
) -> Dict[str, Any]:
    """
    Get user information by Clerk user ID.
    
    Args:
        clerk_user_id: The Clerk user ID
        settings: Application settings
        
    Returns:
        Dict containing user information
    """
    try:
        from app.core.models import User
        from sqlalchemy import select
        
        result = await db.execute(
            select(User).where(User.clerk_user_id == clerk_user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": user.id,
            "clerk_user_id": user.clerk_user_id,
            "email": user.email,
            "full_name": user.full_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "last_login": user.last_login,
            "last_active_at": user.last_active_at,
            "last_sign_in_at": user.last_sign_in_at,
            "image_url": user.image_url,
            "profile_image_url": user.profile_image_url,
            "locale": user.locale,
            "banned": user.banned,
            "locked": user.locked,
            "two_factor_enabled": user.two_factor_enabled,
            "stripe_customer_id": user.stripe_customer_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user by Clerk ID {clerk_user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/clerk/users/email/{email}")
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
    settings = Depends(get_settings)
) -> Dict[str, Any]:
    """
    Get user information by email address.
    
    Args:
        email: The user's email address
        settings: Application settings
        
    Returns:
        Dict containing user information
    """
    try:
        from app.core.models import User
        from sqlalchemy import select
        
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": user.id,
            "clerk_user_id": user.clerk_user_id,
            "email": user.email,
            "full_name": user.full_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "last_login": user.last_login,
            "last_active_at": user.last_active_at,
            "last_sign_in_at": user.last_sign_in_at,
            "image_url": user.image_url,
            "profile_image_url": user.profile_image_url,
            "locale": user.locale,
            "banned": user.banned,
            "locked": user.locked,
            "two_factor_enabled": user.two_factor_enabled,
            "stripe_customer_id": user.stripe_customer_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user by email {email}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
