"""
AI Guardians Stripe Service

Complete Stripe integration for payment processing, subscriptions, and billing.
"""

import stripe
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import get_settings
from app.core.models import Organization, Subscription, SubscriptionTier, PaymentMethod, Invoice
from app.core.exceptions import StripeError, StripeCustomerError, StripeSubscriptionError, StripePaymentError, StripeWebhookError
from app.utils.retry import retry_async, circuit_breaker, error_boundary

logger = logging.getLogger(__name__)

# Initialize Stripe
settings = get_settings()
stripe.api_key = settings.stripe_secret_key


class StripeService:
    """Complete Stripe integration service."""
    
    def __init__(self):
        """Initialize Stripe service."""
        self.webhook_secret = settings.stripe_webhook_secret
        logger.info("Stripe service initialized")
    
    async def create_customer(self, organization: Organization, email: str) -> str:
        """
        Create Stripe customer for organization.

        Args:
            organization: Organization instance
            email: Customer email

        Returns:
            Stripe customer ID
        """
        async with error_boundary("stripe", "create_customer"):
            @circuit_breaker("stripe_api", failure_threshold=5, recovery_timeout=60.0)
            async def create_stripe_customer():
                return stripe.Customer.create(
                    email=email,
                    name=organization.name,
                    metadata={
                        'organization_id': str(organization.id),
                        'organization_name': organization.name
                    }
                )

            try:
                customer = await retry_async(
                    create_stripe_customer,
                    max_attempts=2,
                    delay=1.0,
                    exceptions=(stripe.error.StripeError,)
                )

                # Update organization with Stripe customer ID
                organization.stripe_customer_id = customer.id
                logger.info(f"Created Stripe customer {customer.id} for organization {organization.id}")

                return customer.id

            except stripe.error.StripeError as e:
                logger.error(f"Stripe customer creation failed: {e}")
                raise StripeCustomerError.from_stripe_error(e)
    
    async def create_checkout_session(
        self, 
        organization: Organization, 
        tier: SubscriptionTier,
        success_url: str,
        cancel_url: str,
        billing_interval: str = "month"
    ) -> Dict[str, Any]:
        """
        Create Stripe checkout session for subscription.
        
        Args:
            organization: Organization instance
            tier: Subscription tier
            success_url: Success redirect URL
            cancel_url: Cancel redirect URL
            
        Returns:
            Checkout session data
        """
        try:
            # Create or get customer
            if not organization.stripe_customer_id:
                await self.create_customer(organization, organization.owner_email)
            
            # Get price based on billing interval
            price = float(tier.price_monthly) if billing_interval == "month" else float(tier.price_yearly)
            
            # Create checkout session
            session = stripe.checkout.Session.create(
                customer=organization.stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': tier.name,
                            'description': tier.description,
                        },
                        'unit_amount': int(price * 100),  # Convert to cents
                        'recurring': {
                            'interval': billing_interval
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'organization_id': str(organization.id),
                    'tier_id': str(tier.id)
                },
                subscription_data={
                    'metadata': {
                        'organization_id': str(organization.id),
                        'tier_id': str(tier.id)
                    }
                }
            )
            
            logger.info(f"Created checkout session {session.id} for organization {organization.id}")
            
            return {
                'session_id': session.id,
                'url': session.url,
                'expires_at': datetime.fromtimestamp(session.expires_at)
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe checkout session creation failed: {e}", exc_info=True)
            raise StripeSubscriptionError.from_stripe_error(e)
    
    async def create_billing_portal_session(
        self, 
        organization: Organization,
        return_url: str
    ) -> Dict[str, Any]:
        """
        Create Stripe billing portal session.
        
        Args:
            organization: Organization instance
            return_url: Return URL after portal session
            
        Returns:
            Billing portal session data
        """
        try:
            if not organization.stripe_customer_id:
                raise Exception("No Stripe customer found for organization")
            
            session = stripe.billing_portal.Session.create(
                customer=organization.stripe_customer_id,
                return_url=return_url
            )
            
            logger.info(f"Created billing portal session for organization {organization.id}")
            
            return {
                'url': session.url
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe billing portal creation failed: {e}")
            raise StripeCustomerError.from_stripe_error(e)
    
    async def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Get Stripe subscription details.
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Subscription data
        """
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            return {
                'id': subscription.id,
                'status': subscription.status,
                'current_period_start': datetime.fromtimestamp(subscription.current_period_start),
                'current_period_end': datetime.fromtimestamp(subscription.current_period_end),
                'cancel_at_period_end': subscription.cancel_at_period_end,
                'canceled_at': datetime.fromtimestamp(subscription.canceled_at) if subscription.canceled_at else None,
                'trial_start': datetime.fromtimestamp(subscription.trial_start) if subscription.trial_start else None,
                'trial_end': datetime.fromtimestamp(subscription.trial_end) if subscription.trial_end else None
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve Stripe subscription {subscription_id}: {e}")
            raise StripeSubscriptionError.from_stripe_error(e)
    
    async def cancel_subscription(self, subscription_id: str, immediately: bool = False) -> Dict[str, Any]:
        """
        Cancel Stripe subscription.
        
        Args:
            subscription_id: Stripe subscription ID
            immediately: Cancel immediately or at period end
            
        Returns:
            Cancellation result
        """
        try:
            if immediately:
                subscription = stripe.Subscription.delete(subscription_id)
            else:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            
            logger.info(f"Cancelled subscription {subscription_id}")
            
            return {
                'cancelled': True,
                'cancel_at_period_end': subscription.cancel_at_period_end,
                'canceled_at': datetime.fromtimestamp(subscription.canceled_at) if subscription.canceled_at else None
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription {subscription_id}: {e}")
            raise StripeSubscriptionError.from_stripe_error(e)
    
    async def get_payment_methods(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Get customer payment methods.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            List of payment methods
        """
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type='card'
            )
            
            return [
                {
                    'id': pm.id,
                    'type': pm.type,
                    'card': {
                        'brand': pm.card.brand,
                        'last4': pm.card.last4,
                        'exp_month': pm.card.exp_month,
                        'exp_year': pm.card.exp_year
                    },
                    'created': datetime.fromtimestamp(pm.created)
                }
                for pm in payment_methods.data
            ]
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve payment methods for customer {customer_id}: {e}")
            raise StripeCustomerError.from_stripe_error(e)
    
    async def get_invoices(self, customer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get customer invoices.
        
        Args:
            customer_id: Stripe customer ID
            limit: Number of invoices to retrieve
            
        Returns:
            List of invoices
        """
        try:
            invoices = stripe.Invoice.list(
                customer=customer_id,
                limit=limit
            )
            
            return [
                {
                    'id': invoice.id,
                    'number': invoice.number,
                    'status': invoice.status,
                    'amount_paid': invoice.amount_paid / 100,  # Convert from cents
                    'amount_due': invoice.amount_due / 100,
                    'currency': invoice.currency,
                    'created': datetime.fromtimestamp(invoice.created),
                    'due_date': datetime.fromtimestamp(invoice.due_date) if invoice.due_date else None,
                    'paid_at': datetime.fromtimestamp(invoice.status_transitions.paid_at) if invoice.status_transitions.paid_at else None,
                    'invoice_pdf': invoice.invoice_pdf,
                    'hosted_invoice_url': invoice.hosted_invoice_url
                }
                for invoice in invoices.data
            ]
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve invoices for customer {customer_id}: {e}")
            raise StripeCustomerError.from_stripe_error(e)
    
    async def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify Stripe webhook signature.
        
        Args:
            payload: Raw webhook payload
            signature: Stripe signature header
            
        Returns:
            True if signature is valid
        """
        try:
            stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            return True
        except stripe.error.SignatureVerificationError:
            return False
    
    async def handle_webhook_event(self, event: Dict[str, Any], db: AsyncSession) -> None:
        """
        Handle Stripe webhook events.
        
        Args:
            event: Stripe webhook event
            db: Database session
        """
        try:
            event_type = event['type']
            data = event['data']['object']
            
            if event_type == 'checkout.session.completed':
                await self._handle_checkout_completed(data, db)
            elif event_type == 'invoice.payment_succeeded':
                await self._handle_payment_succeeded(data, db)
            elif event_type == 'invoice.payment_failed':
                await self._handle_payment_failed(data, db)
            elif event_type == 'customer.subscription.updated':
                await self._handle_subscription_updated(data, db)
            elif event_type == 'customer.subscription.deleted':
                await self._handle_subscription_deleted(data, db)
            
            logger.info(f"Processed Stripe webhook: {event_type}")
            
        except Exception as e:
            logger.error(f"Error processing Stripe webhook {event['type']}: {e}")
            raise StripeWebhookError(
                message=f"Failed to process Stripe webhook event: {event.get('type', 'unknown')}",
                details={"event_type": event.get('type'), "error": str(e)}
            )
    
    async def _handle_checkout_completed(self, session_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle successful checkout completion."""
        organization_id = session_data['metadata']['organization_id']
        tier_id = session_data['metadata']['tier_id']
        subscription_id = session_data['subscription']
        
        # Update organization subscription
        stmt = select(Organization).where(Organization.id == organization_id)
        result = await db.execute(stmt)
        organization = result.scalar_one_or_none()
        if organization:
            organization.stripe_subscription_id = subscription_id
            organization.subscription_status = 'active'
            await db.commit()
            
            logger.info(f"Updated organization {organization_id} subscription to active")
    
    async def _handle_payment_succeeded(self, invoice_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle successful payment."""
        customer_id = invoice_data['customer']
        subscription_id = invoice_data['subscription']
        
        # Update subscription status
        stmt = select(Organization).where(Organization.stripe_customer_id == customer_id)
        result = await db.execute(stmt)
        organization = result.scalar_one_or_none()
        
        if organization:
            organization.subscription_status = 'active'
            await db.commit()
            
            logger.info(f"Payment succeeded for organization {organization.id}")
    
    async def _handle_payment_failed(self, invoice_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle failed payment."""
        customer_id = invoice_data['customer']
        
        # Update subscription status
        stmt = select(Organization).where(Organization.stripe_customer_id == customer_id)
        result = await db.execute(stmt)
        organization = result.scalar_one_or_none()
        
        if organization:
            organization.subscription_status = 'past_due'
            await db.commit()
            
            logger.info(f"Payment failed for organization {organization.id}")
    
    async def _handle_subscription_updated(self, subscription_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle subscription updates."""
        subscription_id = subscription_data['id']
        status = subscription_data['status']
        
        # Update subscription status
        stmt = select(Organization).where(Organization.stripe_subscription_id == subscription_id)
        result = await db.execute(stmt)
        organization = result.scalar_one_or_none()
        
        if organization:
            organization.subscription_status = status
            await db.commit()
            
            logger.info(f"Updated subscription status for organization {organization.id} to {status}")
    
    async def _handle_subscription_deleted(self, subscription_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle subscription deletion."""
        subscription_id = subscription_data['id']
        
        # Update subscription status
        stmt = select(Organization).where(Organization.stripe_subscription_id == subscription_id)
        result = await db.execute(stmt)
        organization = result.scalar_one_or_none()
        
        if organization:
            organization.subscription_status = 'cancelled'
            await db.commit()
            
            logger.info(f"Cancelled subscription for organization {organization.id}")


# Global Stripe service instance
stripe_service = StripeService()
