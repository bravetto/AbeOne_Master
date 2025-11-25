"""
Subscription Management API

This module provides endpoints for:
- Subscription tier management
- Billing and payment processing
- Usage tracking and quota enforcement
- Subscription lifecycle management

Architecture:
- Integrates with Stripe for payment processing
- Enforces usage quotas based on subscription tier
- Provides subscription analytics and reporting
- Handles subscription upgrades and downgrades
"""

import os
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, desc, select, func
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone
from enum import Enum

from app.core.database import get_db
from app.core.models import (
    Organization, Subscription, SubscriptionTier, 
    PaymentMethod, Invoice, UsageRecord, SubscriptionStatus
)
from app.middleware.tenant_context import (
    TenantContext, CurrentTenant, require_permission, require_role, get_current_tenant
)
from app.utils.logging import get_logger
from app.core.audit_logger import log_subscription_change

logger = get_logger(__name__)
router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


# PaymentStatus enum (SubscriptionStatus imported from models)
class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


# Pydantic models
class SubscriptionTierResponse(BaseModel):
    """Response model for subscription tier information."""
    id: int
    name: str
    description: str
    price_monthly: float
    price_yearly: float
    api_calls_limit: int
    storage_limit: int
    features: List[str]
    
    class Config:
        from_attributes = True


class SubscriptionResponse(BaseModel):
    """Response model for subscription information."""
    id: str
    tier: SubscriptionTierResponse
    status: str
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    trial_end: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class UsageResponse(BaseModel):
    """Response model for usage information."""
    current_period_start: datetime
    current_period_end: datetime
    api_calls_used: int
    api_calls_limit: int
    storage_used: int
    storage_limit: int
    usage_percentage: float
    days_remaining: int


class CheckoutRequest(BaseModel):
    """Request model for creating checkout session."""
    tier_id: str
    billing_cycle: str = "monthly"  # monthly or yearly
    success_url: str
    cancel_url: str


class CheckoutResponse(BaseModel):
    """Response model for checkout session."""
    checkout_url: str
    session_id: str
    expires_at: datetime


@router.get("/tiers", response_model=List[SubscriptionTierResponse])
async def get_subscription_tiers(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all available subscription tiers.
    
    Returns list of subscription tiers with pricing and features.
    """
    try:
        stmt = select(SubscriptionTier).where(
            SubscriptionTier.is_active == True
        ).order_by(SubscriptionTier.price_monthly.asc())
        result = await db.execute(stmt)
        tiers = result.scalars().all()
        
        tier_responses = []
        for tier in tiers:
            tier_responses.append(SubscriptionTierResponse(
                id=tier.id,
                name=tier.name,
                description=tier.description,
                price_monthly=tier.price_monthly,
                price_yearly=tier.price_yearly,
                api_calls_limit=tier.limits.get("api_calls_limit", 0) if tier.limits else 0,
                storage_limit=tier.limits.get("storage_limit", 0) if tier.limits else 0,
                features=tier.features or []
            ))
        
        logger.info(f"Retrieved {len(tier_responses)} subscription tiers")
        
        return tier_responses
        
    except Exception as e:
        logger.error(f"Error retrieving subscription tiers: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve subscription tiers"
        )


@router.get("/current", response_model=SubscriptionResponse)
async def get_current_subscription(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current organization subscription.

    Returns current subscription details including tier and billing information.
    """
    try:
        # Find current subscription for organization
        stmt = select(Subscription).where(
            and_(
                Subscription.organization_id == tenant_context.organization_id,
                Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING, SubscriptionStatus.PAST_DUE])
            )
        ).order_by(desc(Subscription.created_at)).limit(1)
        
        result = await db.execute(stmt)
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="No active subscription found"
            )
        
        # Load subscription tier
        tier_stmt = select(SubscriptionTier).where(
            SubscriptionTier.id == subscription.subscription_tier_id
        )
        tier_result = await db.execute(tier_stmt)
        tier = tier_result.scalar_one_or_none()
        
        if not tier:
            raise HTTPException(
                status_code=404,
                detail="Subscription tier not found"
            )
        
        tier_response = SubscriptionTierResponse(
            id=tier.id,
            name=tier.name,
            description=tier.description,
            price_monthly=float(tier.price_monthly),
            price_yearly=float(tier.price_yearly),
            api_calls_limit=tier.limits.get("api_calls_limit", 0) if tier.limits else 0,
            storage_limit=tier.limits.get("storage_limit", 0) if tier.limits else 0,
            features=tier.features or []
        )
        
        return SubscriptionResponse(
            id=str(subscription.id),
            tier=tier_response,
            status=subscription.status.value if hasattr(subscription.status, 'value') else str(subscription.status),
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
            trial_end=subscription.trial_end,
            created_at=subscription.created_at
        )
        
    except HTTPException:
        raise
    except RuntimeError as e:
        # Database is disabled or unavailable
        logger.error(f"Database unavailable for subscription retrieval: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable - database connection failed"
        )
    except Exception as e:
        logger.error(f"Error retrieving current subscription: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve current subscription"
        )


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout_session(
    checkout_request: CheckoutRequest,
    tenant_context: TenantContext = require_permission("subscription:manage"),
    db: AsyncSession = Depends(get_db)
):
    """
    Create Stripe checkout session for subscription.
    
    Requires 'subscription:manage' permission.
    Creates Stripe checkout session and returns checkout URL.
    """
    try:
        # Validate subscription tier
        tier_stmt = select(SubscriptionTier).where(
            and_(
                SubscriptionTier.id == checkout_request.tier_id,
                SubscriptionTier.is_active == True
            )
        )
        tier_result = await db.execute(tier_stmt)
        tier = tier_result.scalar_one_or_none()
        
        if not tier:
            raise HTTPException(
                status_code=404,
                detail="Subscription tier not found"
            )
        
        # Check if organization already has active subscription
        existing_stmt = select(Subscription).where(
            and_(
                Subscription.organization_id == tenant_context.organization_id,
                Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING])
            )
        )
        existing_result = await db.execute(existing_stmt)
        existing_subscription = existing_result.scalar_one_or_none()
        
        if existing_subscription:
            raise HTTPException(
                status_code=400,
                detail="Organization already has an active subscription"
            )
        
        # Get organization
        org_stmt = select(Organization).where(
            Organization.id == tenant_context.organization_id
        )
        org_result = await db.execute(org_stmt)
        organization = org_result.scalar_one_or_none()
        
        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )
        
        # Create real Stripe checkout session
        from app.services.stripe_service import stripe_service
        from app.core.config import get_settings
        
        settings = get_settings()
        frontend_url = getattr(settings, 'FRONTEND_URL', os.getenv('FRONTEND_URL', 'http://localhost:3000'))
        
        success_url = checkout_request.success_url or f"{frontend_url}/dashboard/billing/success"
        cancel_url = checkout_request.cancel_url or f"{frontend_url}/dashboard/billing/cancel"
        
        # Convert billing_cycle to Stripe interval format
        billing_interval = "month" if checkout_request.billing_cycle == "monthly" else "year"
        
        checkout_session = await stripe_service.create_checkout_session(
            organization=organization,
            tier=tier,
            success_url=success_url,
            cancel_url=cancel_url,
            billing_interval=billing_interval
        )
        
        checkout_url = checkout_session['url']
        session_id = checkout_session['session_id']
        expires_at = checkout_session['expires_at']
        
        logger.info(f"Created checkout session for organization: {tenant_context.organization_id}")
        
        return CheckoutResponse(
            checkout_url=checkout_url,
            session_id=session_id,
            expires_at=expires_at
        )
        
    except HTTPException:
        raise
    except RuntimeError as e:
        # Database is disabled or unavailable
        logger.error(f"Database unavailable for checkout session: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable - database connection failed"
        )
    except Exception as e:
        # Check if it's a Stripe error
        error_str = str(e).lower()
        if 'stripe' in error_str or isinstance(e.__class__.__name__, str) and 'stripe' in e.__class__.__name__.lower():
            logger.error(f"Stripe error during checkout session creation: {e}", exc_info=True)
            raise HTTPException(
                status_code=503,
                detail="Payment service temporarily unavailable"
            )
        logger.error(f"Error creating checkout session: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to create checkout session"
        )


@router.post("/cancel")
async def cancel_subscription(
    request: Request,
    tenant_context: TenantContext = require_permission("subscription:manage"),
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel current subscription at period end.

    Requires 'subscription:manage' permission.
    Sets subscription to cancel at period end.
    """
    try:
        # Find current active subscription
        stmt = select(Subscription).where(
            and_(
                Subscription.organization_id == tenant_context.organization_id,
                Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING])
            )
        ).order_by(desc(Subscription.created_at)).limit(1)
        
        result = await db.execute(stmt)
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="No active subscription found"
            )
        
        # Set to cancel at period end
        subscription.cancel_at_period_end = True
        subscription.canceled_at = datetime.now(timezone.utc)
        subscription.updated_at = datetime.now(timezone.utc)
        await db.commit()
        
        # Audit log
        await log_subscription_change(
            db=db,
            user_id=tenant_context.user_id,
            subscription_id=str(subscription.id),
            action="cancel",
            details={
                "subscription_id": str(subscription.id),
                "tier_id": subscription.subscription_tier_id,
                "cancel_at_period_end": True
            },
            organization_id=tenant_context.organization_id,
            request=request
        )
        
        logger.info(f"Cancelled subscription for organization: {tenant_context.organization_id}")
        
        return {
            "message": "Subscription will be cancelled at period end",
            "cancel_at": subscription.current_period_end
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling subscription: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to cancel subscription"
        )


@router.post("/reactivate")
async def reactivate_subscription(
    request: Request,
    tenant_context: TenantContext = require_permission("subscription:manage"),
    db: AsyncSession = Depends(get_db)
):
    """
    Reactivate cancelled subscription.

    Requires 'subscription:manage' permission.
    Removes cancellation flag from subscription.
    """
    try:
        stmt = select(Subscription).where(
            and_(
                Subscription.organization_id == tenant_context.organization_id,
                Subscription.status == SubscriptionStatus.ACTIVE,
                Subscription.cancel_at_period_end == True
            )
        )
        result = await db.execute(stmt)
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="No cancelled subscription found"
            )
        
        # Remove cancellation
        subscription.cancel_at_period_end = False
        subscription.updated_at = datetime.now(timezone.utc)
        await db.commit()
        
        # Audit log
        await log_subscription_change(
            db=db,
            user_id=tenant_context.user_id,
            subscription_id=str(subscription.id),
            action="reactivate",
            details={
                "subscription_id": str(subscription.id),
                "tier_id": subscription.subscription_tier_id
            },
            organization_id=tenant_context.organization_id,
            request=request
        )
        
        logger.info(f"Reactivated subscription for organization: {tenant_context.organization_id}")
        
        return {
            "message": "Subscription reactivated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reactivating subscription: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to reactivate subscription"
        )


@router.get("/usage", response_model=UsageResponse)
async def get_usage_information(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current usage information for the organization.

    Returns usage statistics including API calls and storage usage.
    """
    try:
        # Get current subscription
        subscription_stmt = select(Subscription).where(
            and_(
                Subscription.organization_id == tenant_context.organization_id,
                Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING])
            )
        ).order_by(desc(Subscription.created_at)).limit(1)
        
        subscription_result = await db.execute(subscription_stmt)
        subscription = subscription_result.scalar_one_or_none()
        
        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="No active subscription found"
            )
        
        # Get subscription tier for limits
        tier_stmt = select(SubscriptionTier).where(
            SubscriptionTier.id == subscription.subscription_tier_id
        )
        tier_result = await db.execute(tier_stmt)
        tier = tier_result.scalar_one_or_none()
        
        # Get usage records for current period
        period_start = subscription.current_period_start or subscription.created_at
        period_end = subscription.current_period_end or datetime.now(timezone.utc) + timedelta(days=30)
        
        usage_stmt = select(func.sum(UsageRecord.request_count).label('total_requests')).where(
            and_(
                UsageRecord.organization_id == tenant_context.organization_id,
                UsageRecord.recorded_at >= period_start,
                UsageRecord.recorded_at <= period_end
            )
        )
        usage_result = await db.execute(usage_stmt)
        api_calls_used = usage_result.scalar() or 0
        
        # Get limits from tier
        api_calls_limit = tier.limits.get("api_calls_limit", 0) if tier and tier.limits else 0
        storage_limit = tier.limits.get("storage_limit", 0) if tier and tier.limits else 0
        
        # Calculate usage percentage
        usage_percentage = (api_calls_used / api_calls_limit * 100) if api_calls_limit > 0 else 0
        
        # Calculate days remaining
        days_remaining = (period_end - datetime.now(timezone.utc)).days if period_end else 0
        
        return UsageResponse(
            current_period_start=period_start,
            current_period_end=period_end,
            api_calls_used=int(api_calls_used),
            api_calls_limit=api_calls_limit,
            storage_used=0,  # TODO: Implement storage tracking
            storage_limit=storage_limit,
            usage_percentage=round(usage_percentage, 2),
            days_remaining=max(0, days_remaining)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving usage information: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve usage information"
        )


@router.get("/history")
async def get_subscription_history(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get subscription history for the organization.

    Returns list of all subscriptions and their status changes.
    """
    try:
        # Get all subscriptions for organization
        stmt = select(Subscription).where(
            Subscription.organization_id == tenant_context.organization_id
        ).order_by(desc(Subscription.created_at))
        
        result = await db.execute(stmt)
        subscriptions = result.scalars().all()
        
        history = []
        for subscription in subscriptions:
            tier_stmt = select(SubscriptionTier).where(
                SubscriptionTier.id == subscription.subscription_tier_id
            )
            tier_result = await db.execute(tier_stmt)
            tier = tier_result.scalar_one_or_none()
            
            history.append({
                "id": str(subscription.id),
                "tier_name": tier.name if tier else "Unknown",
                "status": subscription.status.value if hasattr(subscription.status, 'value') else str(subscription.status),
                "created_at": subscription.created_at.isoformat(),
                "current_period_start": subscription.current_period_start.isoformat() if subscription.current_period_start else None,
                "current_period_end": subscription.current_period_end.isoformat() if subscription.current_period_end else None,
                "cancel_at_period_end": subscription.cancel_at_period_end,
                "canceled_at": subscription.canceled_at.isoformat() if subscription.canceled_at else None
            })
        
        return {
            "history": history,
            "total": len(history)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving subscription history: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve subscription history"
        )
@router.post("/webhook/stripe")
async def handle_stripe_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Handle Stripe webhook events.
    
    Processes Stripe webhook events for subscription lifecycle management.
    """
    try:
        # Get the raw body and signature
        body = await request.body()
        signature = request.headers.get("stripe-signature")
        
        if not signature:
            raise HTTPException(
                status_code=400,
                detail="Missing Stripe signature"
            )
        
        # Verify webhook signature
        from app.services.stripe_service import StripeService
        stripe_service = StripeService()
        
        if not await stripe_service.verify_webhook_signature(body, signature):
            raise HTTPException(
                status_code=400,
                detail="Invalid webhook signature"
            )
        
        # Parse the verified event
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if not webhook_secret:
            raise HTTPException(
                status_code=500,
                detail="Webhook secret not configured"
            )
            
        # Import stripe only when needed
        try:
            import stripe
        except ImportError:
            raise HTTPException(
                status_code=500,
                detail="Stripe integration not available"
            )
            
        event = stripe.Webhook.construct_event(
            body, signature, webhook_secret
        )
        
        event_type = event.get("type")
        
        if event_type == "checkout.session.completed":
            # Handle successful checkout
            session_data = event.get("data", {}).get("object", {})
            await _handle_checkout_completed(session_data, background_tasks)
            
        elif event_type == "invoice.payment_succeeded":
            # Handle successful payment
            invoice_data = event.get("data", {}).get("object", {})
            await _handle_payment_succeeded(invoice_data, background_tasks)
            
        elif event_type == "invoice.payment_failed":
            # Handle failed payment
            invoice_data = event.get("data", {}).get("object", {})
            await _handle_payment_failed(invoice_data, background_tasks)
            
        elif event_type == "customer.subscription.updated":
            # Handle subscription updates
            subscription_data = event.get("data", {}).get("object", {})
            await _handle_subscription_updated(subscription_data, background_tasks)
        
        logger.info(f"Processed Stripe webhook: {event_type}")
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Error processing Stripe webhook: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process webhook"
        )


# Background task handlers
async def _handle_checkout_completed(session_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """Handle successful checkout completion."""
    try:
        from app.core.database import get_session_factory
        from app.services.stripe_webhook_service import StripeWebhookService
        
        session_factory = get_session_factory()
        if not session_factory:
            logger.error("Database session factory not available")
            return
        
        # Import stripe only when needed
        try:
            import stripe
        except ImportError:
            logger.error("Stripe package not available")
            return
        
        async with session_factory() as db:
            webhook_service = StripeWebhookService()
            
            # Extract customer and subscription information from checkout session
            customer_id = session_data.get("customer")
            subscription_id = session_data.get("subscription")
            mode = session_data.get("mode")
            
            if mode == "subscription" and subscription_id:
                # Fetch subscription details from Stripe
                stripe_subscription = stripe.Subscription.retrieve(subscription_id)
                
                # Update subscription in database using webhook service
                await webhook_service.handle_subscription_created(
                    stripe_subscription.to_dict(),
                    db
                )
            
            logger.info(f"Processed checkout completion for session {session_data.get('id')}")
    except Exception as e:
        logger.error(f"Error handling checkout completion: {e}")


async def _handle_payment_succeeded(invoice_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """Handle successful payment."""
    try:
        from app.core.database import get_session_factory
        from app.services.stripe_webhook_service import StripeWebhookService
        
        session_factory = get_session_factory()
        if not session_factory:
            logger.error("Database session factory not available")
            return
        
        async with session_factory() as db:
            webhook_service = StripeWebhookService()
            
            # Process invoice payment succeeded
            await webhook_service.handle_invoice_payment_succeeded(invoice_data, db)
            
            logger.info(f"Processed payment success for invoice {invoice_data.get('id')}")
    except Exception as e:
        logger.error(f"Error handling payment success: {e}")


async def _handle_payment_failed(invoice_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """Handle failed payment."""
    try:
        from app.core.database import get_session_factory
        from app.services.stripe_webhook_service import StripeWebhookService
        
        session_factory = get_session_factory()
        if not session_factory:
            logger.error("Database session factory not available")
            return
        
        async with session_factory() as db:
            webhook_service = StripeWebhookService()
            
            # Process invoice payment failed
            await webhook_service.handle_invoice_payment_failed(invoice_data, db)
            
            # Send notification email to customer
            await _send_payment_failure_notification(invoice_data)
            
            logger.info(f"Processed payment failure for invoice {invoice_data.get('id')}")
    except Exception as e:
        logger.error(f"Error handling payment failure: {e}")


async def _handle_subscription_updated(subscription_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """Handle subscription updates."""
    try:
        from app.core.database import get_session_factory
        from app.services.stripe_webhook_service import StripeWebhookService
        
        session_factory = get_session_factory()
        if not session_factory:
            logger.error("Database session factory not available")
            return
        
        async with session_factory() as db:
            webhook_service = StripeWebhookService()
            
            # Process subscription update
            await webhook_service.handle_subscription_updated(subscription_data, db)
            
            logger.info(f"Processed subscription update for {subscription_data.get('id')}")
    except Exception as e:
        logger.error(f"Error handling subscription update: {e}")


# Email notification functions
async def _send_payment_failure_notification(invoice_data: Dict[str, Any]) -> None:
    """Send payment failure notification email."""
    try:
        # Get customer email from invoice data
        customer_email = invoice_data.get("customer_email")
        if not customer_email:
            logger.warning("No customer email found for payment failure notification")
            return
        
        # Get invoice details
        invoice_id = invoice_data.get("id")
        amount_due = invoice_data.get("amount_due", 0) / 100  # Convert from cents
        currency = invoice_data.get("currency", "usd").upper()
        
        # Create email content
        subject = "Payment Failed - Action Required"
        body = f"""
Dear Customer,

We were unable to process your payment for invoice {invoice_id}.

Invoice Details:
- Amount Due: {currency} {amount_due:.2f}
- Invoice ID: {invoice_id}
- Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

Please update your payment method or contact support if you need assistance.

Best regards,
AIGuards Team
        """
        
        # Send email (in production, use a proper email service like SendGrid, SES, etc.)
        await _send_email(customer_email, subject, body)
        
        logger.info(f"Payment failure notification sent to {customer_email}")
        
    except Exception as e:
        logger.error(f"Error sending payment failure notification: {e}")


async def _send_subscription_success_notification(subscription_data: Dict[str, Any]) -> None:
    """Send subscription success notification email."""
    try:
        # Get customer email from subscription data
        customer_email = subscription_data.get("customer", {}).get("email")
        if not customer_email:
            logger.warning("No customer email found for subscription success notification")
            return
        
        # Get subscription details
        subscription_id = subscription_data.get("id")
        status = subscription_data.get("status")
        current_period_start = subscription_data.get("current_period_start")
        current_period_end = subscription_data.get("current_period_end")
        
        # Create email content
        subject = "Subscription Activated Successfully"
        body = f"""
Dear Customer,

Your subscription has been activated successfully!

Subscription Details:
- Subscription ID: {subscription_id}
- Status: {status.title()}
- Current Period: {current_period_start} to {current_period_end}

Thank you for choosing AIGuards!

Best regards,
AIGuards Team
        """
        
        # Send email
        await _send_email(customer_email, subject, body)
        
        logger.info(f"Subscription success notification sent to {customer_email}")
        
    except Exception as e:
        logger.error(f"Error sending subscription success notification: {e}")


async def _send_email(to_email: str, subject: str, body: str) -> None:
    """Send email using configured email service."""
    try:
        # In production, integrate with a proper email service
        # For now, just log the email content
        logger.info(f"Email would be sent to {to_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Body: {body}")
        
        # TODO: Integrate with actual email service (SendGrid, SES, etc.)
        # Example with SendGrid:
        # import sendgrid
        # from sendgrid.helpers.mail import Mail
        # 
        # sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
        # message = Mail(
        #     from_email='noreply@aiguards.com',
        #     to_emails=to_email,
        #     subject=subject,
        #     plain_text_content=body
        # )
        # response = sg.send(message)
        
    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {e}")
