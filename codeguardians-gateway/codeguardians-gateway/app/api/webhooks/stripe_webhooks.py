"""Stripe webhook endpoints for product and price management."""

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.config import get_settings
from app.core.exceptions import StripeWebhookError
from app.utils.logging import get_logger

logger = get_logger(__name__)

# Separate routers for webhooks and API endpoints
webhook_router = APIRouter(tags=["Stripe Webhooks"])
api_router = APIRouter(tags=["Stripe API"])

settings = get_settings()

# Lazy stripe import to avoid startup issues
_stripe = None

def _get_stripe():
    """Lazy import stripe to avoid startup issues."""
    global _stripe
    if _stripe is None:
        try:
            import stripe
            _stripe = stripe
            # Initialize Stripe
            stripe.api_key = settings.STRIPE_SECRET_KEY
        except ImportError:
            logger.warning("Stripe module not available")
            _stripe = None
    return _stripe

# Placeholder webhook service when stripe is not available
class MockStripeWebhookService:
    """Mock service for when stripe is not available."""
    
    async def handle_product_created(self, obj, db):
        logger.info("Mock: Product created event")
    
    async def handle_product_updated(self, obj, db):
        logger.info("Mock: Product updated event")
    
    async def handle_product_deleted(self, obj, db):
        logger.info("Mock: Product deleted event")
    
    async def handle_price_created(self, obj, db):
        logger.info("Mock: Price created event")
    
    async def handle_price_updated(self, obj, db):
        logger.info("Mock: Price updated event")
    
    async def handle_price_deleted(self, obj, db):
        logger.info("Mock: Price deleted event")
    
    async def handle_customer_created(self, obj, db):
        logger.info("Mock: Customer created event")
    
    async def handle_customer_updated(self, obj, db):
        logger.info("Mock: Customer updated event")
    
    async def handle_subscription_created(self, obj, db):
        logger.info("Mock: Subscription created event")
    
    async def handle_subscription_updated(self, obj, db):
        logger.info("Mock: Subscription updated event")
    
    async def handle_subscription_deleted(self, obj, db):
        logger.info("Mock: Subscription deleted event")
    
    async def handle_invoice_payment_succeeded(self, obj, db):
        logger.info("Mock: Invoice payment succeeded event")
    
    async def handle_invoice_payment_failed(self, obj, db):
        logger.info("Mock: Invoice payment failed event")

@webhook_router.post("/stripe")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle Stripe webhook events."""
    stripe = _get_stripe()

    if not stripe:
        logger.warning("Stripe not available - webhook request ignored")
        raise HTTPException(status_code=503, detail="Stripe service not available")

    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    if not sig_header:
        logger.error("Missing stripe-signature header")
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    # Check if webhook secret is configured
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    if not webhook_secret or (isinstance(webhook_secret, str) and not webhook_secret.strip()):
        logger.error("STRIPE_WEBHOOK_SECRET not configured or empty")
        raise HTTPException(status_code=500, detail="Stripe webhook secret not configured")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        logger.error("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except Exception as e:
        # Check if it's a signature verification error
        error_type_name = type(e).__name__
        error_module = type(e).__module__
        
        if error_type_name == 'SignatureVerificationError' and 'stripe' in error_module:
            logger.error("Invalid signature")
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Re-raise if it's a different error
        logger.error(f"Error constructing webhook event: {type(e).__name__}: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing webhook: {str(e)}")
    
    # Initialize webhook service
    try:
        from app.services.stripe_webhook_service import StripeWebhookService
        webhook_service = StripeWebhookService()
    except ImportError:
        logger.warning("Using mock webhook service")
        webhook_service = MockStripeWebhookService()
    
    try:
        # Handle different event types
        event_type = event['type']
        
        if event_type == 'product.created':
            await webhook_service.handle_product_created(event['data']['object'], db)
            
        elif event_type == 'product.updated':
            await webhook_service.handle_product_updated(event['data']['object'], db)
            
        elif event_type == 'product.deleted':
            await webhook_service.handle_product_deleted(event['data']['object'], db)
            
        elif event_type == 'price.created':
            await webhook_service.handle_price_created(event['data']['object'], db)
            
        elif event_type == 'price.updated':
            await webhook_service.handle_price_updated(event['data']['object'], db)
            
        elif event_type == 'price.deleted':
            await webhook_service.handle_price_deleted(event['data']['object'], db)
            
        elif event_type == 'customer.created':
            await webhook_service.handle_customer_created(event['data']['object'], db)
            
        elif event_type == 'customer.updated':
            await webhook_service.handle_customer_updated(event['data']['object'], db)
            
        elif event_type == 'customer.subscription.created':
            await webhook_service.handle_subscription_created(event['data']['object'], db)
            
        elif event_type == 'customer.subscription.updated':
            await webhook_service.handle_subscription_updated(event['data']['object'], db)
            
        elif event_type == 'customer.subscription.deleted':
            await webhook_service.handle_subscription_deleted(event['data']['object'], db)
            
        elif event_type == 'customer.subscription.paused':
            # Handle paused subscription (similar to updated)
            await webhook_service.handle_subscription_updated(event['data']['object'], db)
            
        elif event_type == 'customer.subscription.resumed':
            # Handle resumed subscription (similar to updated)
            await webhook_service.handle_subscription_updated(event['data']['object'], db)
            
        elif event_type == 'invoice.payment_succeeded':
            await webhook_service.handle_invoice_payment_succeeded(event['data']['object'], db)
            
        elif event_type == 'invoice.payment_failed':
            await webhook_service.handle_invoice_payment_failed(event['data']['object'], db)
            
        else:
            logger.info(f"Unhandled event type: {event_type}")
    
    except StripeWebhookError as e:
        logger.error(f"Stripe webhook processing error: {e}", exc_info=True)
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error processing webhook: {type(e).__name__}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")
    
    return {"status": "success"}

@api_router.get("/products")
async def get_products(db: AsyncSession = Depends(get_db)):
    """Get all active products."""
    from sqlalchemy import select
    from app.core.models import StripeProduct
    
    result = await db.execute(
        select(StripeProduct).where(StripeProduct.active == True)
    )
    products = result.scalars().all()
    
    return {"products": products}

@api_router.get("/prices/{product_id}")
async def get_prices_for_product(product_id: str, db: AsyncSession = Depends(get_db)):
    """Get all active prices for a product."""
    from sqlalchemy import select
    from app.core.models import StripePrice
    
    result = await db.execute(
        select(StripePrice).where(
            StripePrice.stripe_product_id == product_id,
            StripePrice.active == True
        )
    )
    prices = result.scalars().all()
    
    return {"prices": prices}

@api_router.get("/customers/{email}")
async def get_customer_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """Get customer by email."""
    from sqlalchemy import select
    from app.core.models import StripeCustomer
    
    result = await db.execute(
        select(StripeCustomer).where(StripeCustomer.email == email)
    )
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"customer": customer}

@api_router.get("/subscriptions/{customer_id}")
async def get_subscriptions_for_customer(customer_id: str, db: AsyncSession = Depends(get_db)):
    """Get all subscriptions for a customer."""
    from sqlalchemy import select
    from app.core.models import Subscription
    
    result = await db.execute(
        select(Subscription).where(Subscription.stripe_customer_id == customer_id)
    )
    subscriptions = result.scalars().all()
    
    return {"subscriptions": subscriptions}

@api_router.get("/invoices/{customer_id}")
async def get_invoices_for_customer(customer_id: str, db: AsyncSession = Depends(get_db)):
    """Get all invoices for a customer."""
    from sqlalchemy import select
    from app.core.models import Invoice
    
    result = await db.execute(
        select(Invoice).where(Invoice.stripe_customer_id == customer_id)
    )
    invoices = result.scalars().all()
    
    return {"invoices": invoices}

# Export both routers for main.py
router = webhook_router  # Default export (backward compatibility)
stripe_api_router = api_router  # API endpoints export
