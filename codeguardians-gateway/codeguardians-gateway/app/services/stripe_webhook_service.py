"""Stripe webhook service for handling product and price events."""

import stripe
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.core.models import (
    StripeProduct, StripePrice, StripeCustomer, 
    Subscription, Invoice, User, PaymentStatus
)
from app.core.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

class StripeWebhookService:
    """Service for handling Stripe webhook events."""
    
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
    
    # =============================================================================
    # PRODUCT HANDLERS
    # =============================================================================
    
    async def handle_product_created(self, product_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle product.created webhook event."""
        try:
            stripe_product_id = product_data.get("id")
            if not stripe_product_id:
                logger.error("Product created event missing product ID")
                return
            
            # Check if product already exists
            result = await db.execute(
                select(StripeProduct).where(StripeProduct.stripe_product_id == stripe_product_id)
            )
            existing_product = result.scalar_one_or_none()
            
            if existing_product:
                logger.warning(f"Product {stripe_product_id} already exists")
                return
            
            # Create new product
            product_name = product_data.get("name", "Unnamed Product")
            new_product = StripeProduct(
                stripe_product_id=stripe_product_id,
                name=product_name,
                description=product_data.get("description"),
                active=product_data.get("active", True),
                type=product_data.get("type", "service"),
                unit_label=product_data.get("unit_label"),
                statement_descriptor=product_data.get("statement_descriptor"),
                tax_code=product_data.get("tax_code"),
                url=product_data.get("url"),
                shippable=product_data.get("shippable"),
                package_dimensions=product_data.get("package_dimensions"),
                images=product_data.get("images", []),
                attributes=product_data.get("attributes", []),
                marketing_features=product_data.get("marketing_features", []),
                stripe_metadata=product_data.get("metadata", {}),
                livemode=product_data.get("livemode", False)
            )
            
            db.add(new_product)
            await db.commit()
            await db.refresh(new_product)
            
            logger.info(f"Created product: {stripe_product_id} - {product_name}")
            
        except Exception as e:
            logger.error(f"Error handling product.created: {e}")
            await db.rollback()
            raise
    
    async def handle_product_updated(self, product_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle product.updated webhook event."""
        try:
            stripe_product_id = product_data.get("id")
            if not stripe_product_id:
                logger.error("Product updated event missing product ID")
                return
            
            # Find existing product
            result = await db.execute(
                select(StripeProduct).where(StripeProduct.stripe_product_id == stripe_product_id)
            )
            product = result.scalar_one_or_none()
            
            if not product:
                logger.warning(f"Product {stripe_product_id} not found for update")
                return
            
            # Update product fields
            if "name" in product_data:
                product.name = product_data["name"]
            product.description = product_data.get("description")
            if "active" in product_data:
                product.active = product_data["active"]
            if "type" in product_data:
                product.type = product_data["type"]
            product.unit_label = product_data.get("unit_label")
            product.statement_descriptor = product_data.get("statement_descriptor")
            product.tax_code = product_data.get("tax_code")
            product.url = product_data.get("url")
            product.shippable = product_data.get("shippable")
            product.package_dimensions = product_data.get("package_dimensions")
            product.images = product_data.get("images", [])
            product.attributes = product_data.get("attributes", [])
            product.marketing_features = product_data.get("marketing_features", [])
            product.stripe_metadata = product_data.get("metadata", {})
            product.livemode = product_data["livemode"]
            
            await db.commit()
            await db.refresh(product)
            
            logger.info(f"Updated product: {stripe_product_id} - {product_data['name']}")
            
        except Exception as e:
            logger.error(f"Error handling product.updated: {e}")
            await db.rollback()
            raise
    
    async def handle_product_deleted(self, product_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle product.deleted webhook event."""
        try:
            stripe_product_id = product_data["id"]
            
            # Find existing product
            result = await db.execute(
                select(StripeProduct).where(StripeProduct.stripe_product_id == stripe_product_id)
            )
            product = result.scalar_one_or_none()
            
            if not product:
                logger.warning(f"Product {stripe_product_id} not found for deletion")
                return
            
            # Mark as inactive instead of deleting (soft delete)
            product.active = False
            await db.commit()
            
            logger.info(f"Deactivated product: {stripe_product_id} - {product_data['name']}")
            
        except Exception as e:
            logger.error(f"Error handling product.deleted: {e}")
            await db.rollback()
            raise
    
    # =============================================================================
    # PRICE HANDLERS
    # =============================================================================
    
    async def handle_price_created(self, price_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle price.created webhook event."""
        try:
            stripe_price_id = price_data["id"]
            stripe_product_id = price_data["product"]
            
            # Check if price already exists
            result = await db.execute(
                select(StripePrice).where(StripePrice.stripe_price_id == stripe_price_id)
            )
            existing_price = result.scalar_one_or_none()
            
            if existing_price:
                logger.warning(f"Price {stripe_price_id} already exists")
                return
            
            # Create new price
            new_price = StripePrice(
                stripe_price_id=stripe_price_id,
                stripe_product_id=stripe_product_id,
                active=price_data["active"],
                currency=price_data["currency"],
                type=price_data["type"],
                unit_amount=price_data["unit_amount"],
                unit_amount_decimal=price_data.get("unit_amount_decimal"),
                billing_scheme=price_data["billing_scheme"],
                tiers_mode=price_data.get("tiers_mode"),
                nickname=price_data.get("nickname"),
                lookup_key=price_data.get("lookup_key"),
                tax_behavior=price_data["tax_behavior"],
                custom_unit_amount=price_data.get("custom_unit_amount"),
                transform_quantity=price_data.get("transform_quantity"),
                recurring=price_data.get("recurring"),
                stripe_metadata=price_data.get("metadata", {}),
                livemode=price_data["livemode"]
            )
            
            db.add(new_price)
            await db.commit()
            await db.refresh(new_price)
            
            logger.info(f"Created price: {stripe_price_id} - {price_data['unit_amount']} {price_data['currency']}")
            
        except Exception as e:
            logger.error(f"Error handling price.created: {e}")
            await db.rollback()
            raise
    
    async def handle_price_updated(self, price_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle price.updated webhook event."""
        try:
            stripe_price_id = price_data["id"]
            
            # Find existing price
            result = await db.execute(
                select(StripePrice).where(StripePrice.stripe_price_id == stripe_price_id)
            )
            price = result.scalar_one_or_none()
            
            if not price:
                logger.warning(f"Price {stripe_price_id} not found for update")
                return
            
            # Update price fields
            price.active = price_data["active"]
            price.currency = price_data["currency"]
            price.type = price_data["type"]
            price.unit_amount = price_data["unit_amount"]
            price.unit_amount_decimal = price_data.get("unit_amount_decimal")
            price.billing_scheme = price_data["billing_scheme"]
            price.tiers_mode = price_data.get("tiers_mode")
            price.nickname = price_data.get("nickname")
            price.lookup_key = price_data.get("lookup_key")
            price.tax_behavior = price_data["tax_behavior"]
            price.custom_unit_amount = price_data.get("custom_unit_amount")
            price.transform_quantity = price_data.get("transform_quantity")
            price.recurring = price_data.get("recurring")
            price.stripe_metadata = price_data.get("metadata", {})
            price.livemode = price_data["livemode"]
            
            await db.commit()
            await db.refresh(price)
            
            logger.info(f"Updated price: {stripe_price_id} - {price_data['unit_amount']} {price_data['currency']}")
            
        except Exception as e:
            logger.error(f"Error handling price.updated: {e}")
            await db.rollback()
            raise
    
    async def handle_price_deleted(self, price_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle price.deleted webhook event."""
        try:
            stripe_price_id = price_data["id"]
            
            # Find existing price
            result = await db.execute(
                select(StripePrice).where(StripePrice.stripe_price_id == stripe_price_id)
            )
            price = result.scalar_one_or_none()
            
            if not price:
                logger.warning(f"Price {stripe_price_id} not found for deletion")
                return
            
            # Mark as inactive instead of deleting (soft delete)
            price.active = False
            await db.commit()
            
            logger.info(f"Deactivated price: {stripe_price_id}")
            
        except Exception as e:
            logger.error(f"Error handling price.deleted: {e}")
            await db.rollback()
            raise
    
    # =============================================================================
    # CUSTOMER HANDLERS
    # =============================================================================
    
    async def handle_customer_created(self, customer_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle customer.created webhook event."""
        try:
            stripe_customer_id = customer_data["id"]
            email = customer_data.get("email")
            
            # Check if customer already exists
            result = await db.execute(
                select(StripeCustomer).where(StripeCustomer.stripe_customer_id == stripe_customer_id)
            )
            existing_customer = result.scalar_one_or_none()
            
            if existing_customer:
                logger.warning(f"Customer {stripe_customer_id} already exists")
                return
            
            # Create new customer
            new_customer = StripeCustomer(
                stripe_customer_id=stripe_customer_id,
                email=email,
                name=customer_data.get("name"),
                phone=customer_data.get("phone"),
                description=customer_data.get("description"),
                balance=customer_data.get("balance", 0),
                currency=customer_data.get("currency"),
                delinquent=customer_data.get("delinquent", False),
                invoice_prefix=customer_data.get("invoice_prefix"),
                default_source=customer_data.get("default_source"),
                address=customer_data.get("address"),
                shipping=customer_data.get("shipping"),
                invoice_settings=customer_data.get("invoice_settings"),
                preferred_locales=customer_data.get("preferred_locales"),
                tax_exempt=customer_data.get("tax_exempt"),
                stripe_metadata=customer_data.get("metadata", {}),
                livemode=customer_data["livemode"]
            )
            
            db.add(new_customer)
            await db.commit()
            await db.refresh(new_customer)
            
            # Link to user if email matches
            if email:
                await self._link_customer_to_user(stripe_customer_id, email, db)
            
            logger.info(f"Created customer: {stripe_customer_id} - {email}")
            
        except Exception as e:
            logger.error(f"Error handling customer.created: {e}")
            await db.rollback()
            raise
    
    async def handle_customer_updated(self, customer_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle customer.updated webhook event."""
        try:
            stripe_customer_id = customer_data["id"]
            
            # Find existing customer
            result = await db.execute(
                select(StripeCustomer).where(StripeCustomer.stripe_customer_id == stripe_customer_id)
            )
            customer = result.scalar_one_or_none()
            
            if not customer:
                logger.warning(f"Customer {stripe_customer_id} not found for update")
                return
            
            # Update customer fields
            customer.email = customer_data.get("email")
            customer.name = customer_data.get("name")
            customer.phone = customer_data.get("phone")
            customer.description = customer_data.get("description")
            customer.balance = customer_data.get("balance", 0)
            customer.currency = customer_data.get("currency")
            customer.delinquent = customer_data.get("delinquent", False)
            customer.invoice_prefix = customer_data.get("invoice_prefix")
            customer.default_source = customer_data.get("default_source")
            customer.address = customer_data.get("address")
            customer.shipping = customer_data.get("shipping")
            customer.invoice_settings = customer_data.get("invoice_settings")
            customer.preferred_locales = customer_data.get("preferred_locales")
            customer.tax_exempt = customer_data.get("tax_exempt")
            customer.stripe_metadata = customer_data.get("metadata", {})
            customer.livemode = customer_data["livemode"]
            
            await db.commit()
            await db.refresh(customer)
            
            logger.info(f"Updated customer: {stripe_customer_id}")
            
        except Exception as e:
            logger.error(f"Error handling customer.updated: {e}")
            await db.rollback()
            raise
    
    # =============================================================================
    # SUBSCRIPTION HANDLERS
    # =============================================================================
    
    async def handle_subscription_created(self, subscription_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle customer.subscription.created webhook event."""
        try:
            stripe_subscription_id = subscription_data["id"]
            stripe_customer_id = subscription_data["customer"]

            # Check if subscription already exists
            result = await db.execute(
                select(Subscription).where(Subscription.stripe_subscription_id == stripe_subscription_id)
            )
            existing_subscription = result.scalar_one_or_none()

            if existing_subscription:
                logger.warning(f"Subscription {stripe_subscription_id} already exists")
                return

            # Extract metadata from subscription
            metadata = subscription_data.get("metadata", {})

            # Get organization_id and subscription_tier_id from metadata (set during checkout)
            organization_id = metadata.get("organization_id")
            tier_id = metadata.get("tier_id")

            if not organization_id or not tier_id:
                logger.error(f"Missing organization_id or tier_id in subscription metadata for {stripe_subscription_id}")
                # Try to find organization by Stripe customer ID
                from app.core.models import Organization
                result = await db.execute(
                    select(Organization).where(Organization.stripe_customer_id == stripe_customer_id)
                )
                organization = result.scalar_one_or_none()

                if not organization:
                    logger.error(f"Could not find organization for Stripe customer {stripe_customer_id}")
                    return

                organization_id = organization.id

                # If tier_id is missing, try to determine it from the price
                if not tier_id:
                    stripe_price_id = self._get_primary_price_id(subscription_data)
                    if stripe_price_id:
                        # Look up tier by price ID (this would need additional logic)
                        # For now, use a default tier
                        tier_id = 1  # Default tier
                        logger.warning(f"Using default tier_id=1 for subscription {stripe_subscription_id}")
                    else:
                        logger.error(f"Could not determine tier for subscription {stripe_subscription_id}")
                        return

            # Validate that organization and tier exist
            from app.core.models import Organization, SubscriptionTier

            result = await db.execute(
                select(Organization).where(Organization.id == int(organization_id))
            )
            organization = result.scalar_one_or_none()

            result = await db.execute(
                select(SubscriptionTier).where(SubscriptionTier.id == int(tier_id))
            )
            tier = result.scalar_one_or_none()

            if not organization or not tier:
                logger.error(f"Invalid organization_id={organization_id} or tier_id={tier_id} for subscription {stripe_subscription_id}")
                return

            # Create new subscription
            new_subscription = Subscription(
                stripe_subscription_id=stripe_subscription_id,
                stripe_customer_id=stripe_customer_id,
                status=subscription_data["status"],
                current_period_start=self._parse_timestamp(subscription_data.get("current_period_start")),
                current_period_end=self._parse_timestamp(subscription_data.get("current_period_end")),
                cancel_at_period_end=subscription_data.get("cancel_at_period_end", False),
                canceled_at=self._parse_timestamp(subscription_data.get("canceled_at")),
                stripe_price_id=self._get_primary_price_id(subscription_data),
                billing_cycle_anchor=self._parse_timestamp(subscription_data.get("billing_cycle_anchor")),
                collection_method=subscription_data.get("collection_method"),
                days_until_due=subscription_data.get("days_until_due"),
                default_payment_method=subscription_data.get("default_payment_method"),
                trial_start=self._parse_timestamp(subscription_data.get("trial_start")),
                trial_end=self._parse_timestamp(subscription_data.get("trial_end")),
                items=subscription_data.get("items"),
                stripe_metadata=subscription_data.get("metadata", {}),
                cancel_at=self._parse_timestamp(subscription_data.get("cancel_at")),
                ended_at=self._parse_timestamp(subscription_data.get("ended_at")),
                organization_id=int(organization_id),
                subscription_tier_id=int(tier_id)
            )

            db.add(new_subscription)
            await db.commit()
            await db.refresh(new_subscription)

            logger.info(f"Created subscription: {stripe_subscription_id} for organization {organization_id}")

        except Exception as e:
            logger.error(f"Error handling subscription.created: {e}")
            await db.rollback()
            raise
    
    async def handle_subscription_updated(self, subscription_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle customer.subscription.updated webhook event."""
        try:
            stripe_subscription_id = subscription_data["id"]
            
            # Find existing subscription
            result = await db.execute(
                select(Subscription).where(Subscription.stripe_subscription_id == stripe_subscription_id)
            )
            subscription = result.scalar_one_or_none()
            
            if not subscription:
                logger.warning(f"Subscription {stripe_subscription_id} not found for update")
                return
            
            # Update subscription fields
            subscription.status = subscription_data["status"]
            subscription.current_period_start = self._parse_timestamp(subscription_data.get("current_period_start"))
            subscription.current_period_end = self._parse_timestamp(subscription_data.get("current_period_end"))
            subscription.cancel_at_period_end = subscription_data.get("cancel_at_period_end", False)
            subscription.canceled_at = self._parse_timestamp(subscription_data.get("canceled_at"))
            subscription.stripe_price_id = self._get_primary_price_id(subscription_data)
            subscription.billing_cycle_anchor = self._parse_timestamp(subscription_data.get("billing_cycle_anchor"))
            subscription.collection_method = subscription_data.get("collection_method")
            subscription.days_until_due = subscription_data.get("days_until_due")
            subscription.default_payment_method = subscription_data.get("default_payment_method")
            subscription.trial_start = self._parse_timestamp(subscription_data.get("trial_start"))
            subscription.trial_end = self._parse_timestamp(subscription_data.get("trial_end"))
            subscription.items = subscription_data.get("items")
            subscription.stripe_metadata = subscription_data.get("metadata", {})
            subscription.cancel_at = self._parse_timestamp(subscription_data.get("cancel_at"))
            subscription.ended_at = self._parse_timestamp(subscription_data.get("ended_at"))
            
            await db.commit()
            await db.refresh(subscription)
            
            logger.info(f"Updated subscription: {stripe_subscription_id}")
            
        except Exception as e:
            logger.error(f"Error handling subscription.updated: {e}")
            await db.rollback()
            raise
    
    async def handle_subscription_deleted(self, subscription_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle customer.subscription.deleted webhook event."""
        try:
            stripe_subscription_id = subscription_data["id"]
            
            # Find existing subscription
            result = await db.execute(
                select(Subscription).where(Subscription.stripe_subscription_id == stripe_subscription_id)
            )
            subscription = result.scalar_one_or_none()
            
            if not subscription:
                logger.warning(f"Subscription {stripe_subscription_id} not found for deletion")
                return
            
            # Update subscription status
            subscription.status = "canceled"
            subscription.canceled_at = self._parse_timestamp(subscription_data.get("canceled_at"))
            subscription.ended_at = self._parse_timestamp(subscription_data.get("ended_at"))
            
            await db.commit()
            
            logger.info(f"Canceled subscription: {stripe_subscription_id}")
            
        except Exception as e:
            logger.error(f"Error handling subscription.deleted: {e}")
            await db.rollback()
            raise
    
    # =============================================================================
    # INVOICE HANDLERS
    # =============================================================================
    
    async def handle_invoice_payment_succeeded(self, invoice_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle invoice.payment_succeeded webhook event."""
        try:
            stripe_invoice_id = invoice_data.get("id")
            if not stripe_invoice_id:
                logger.error("Invoice payment_succeeded event missing invoice ID")
                return
                
            stripe_customer_id = invoice_data.get("customer")
            stripe_subscription_id = invoice_data.get("subscription")

            # Find organization and subscription from Stripe IDs
            organization_id = None
            subscription_id = None

            if stripe_subscription_id:
                # Try to find subscription first
                result = await db.execute(
                    select(Subscription).where(Subscription.stripe_subscription_id == stripe_subscription_id)
                )
                subscription = result.scalar_one_or_none()
                if subscription:
                    organization_id = subscription.organization_id
                    subscription_id = subscription.id
            elif stripe_customer_id:
                # Fallback to finding organization by customer ID
                result = await db.execute(
                    select(Organization).where(Organization.stripe_customer_id == stripe_customer_id)
                )
                organization = result.scalar_one_or_none()
                if organization:
                    organization_id = organization.id

            if not organization_id:
                logger.error(f"Could not determine organization for invoice {stripe_invoice_id}")
                # Still save the invoice with null organization_id for audit/debugging purposes
                logger.info(f"Saving invoice {stripe_invoice_id} without organization_id for later processing")
                organization_id = None
                subscription_id = None

            # Check if invoice already exists
            result = await db.execute(
                select(Invoice).where(Invoice.stripe_invoice_id == stripe_invoice_id)
            )
            existing_invoice = result.scalar_one_or_none()

            if existing_invoice:
                # Update existing invoice
                existing_invoice.status = PaymentStatus.SUCCEEDED
                existing_invoice.amount_paid = float(invoice_data.get("amount_paid", 0)) / 100
                existing_invoice.amount_remaining = float(invoice_data.get("amount_remaining", 0)) / 100
                existing_invoice.paid_at = self._parse_timestamp(invoice_data.get("status_transitions", {}).get("paid_at"))
                existing_invoice.stripe_customer_id = stripe_customer_id
                existing_invoice.stripe_charge_id = invoice_data.get("charge")
                existing_invoice.currency = invoice_data.get("currency")
                existing_invoice.subtotal = invoice_data.get("subtotal")
                existing_invoice.tax = invoice_data.get("tax")
                existing_invoice.total = invoice_data.get("total")
                existing_invoice.amount_shipping = invoice_data.get("amount_shipping")
                existing_invoice.billing_reason = invoice_data.get("billing_reason")
                existing_invoice.collection_method = invoice_data.get("collection_method")
                existing_invoice.customer_email = invoice_data.get("customer_email")
                existing_invoice.customer_name = invoice_data.get("customer_name")
                existing_invoice.customer_address = invoice_data.get("customer_address")
                existing_invoice.customer_shipping = invoice_data.get("customer_shipping")
                existing_invoice.lines = invoice_data.get("lines")
                existing_invoice.hosted_invoice_url = invoice_data.get("hosted_invoice_url")
                existing_invoice.invoice_pdf = invoice_data.get("invoice_pdf")
                existing_invoice.stripe_metadata = invoice_data.get("metadata", {})
            else:
                # Create new invoice
                new_invoice = Invoice(
                    stripe_invoice_id=stripe_invoice_id,
                    invoice_number=invoice_data.get("number", ""),
                    amount_due=float(invoice_data.get("amount_due", 0)) / 100,
                    amount_paid=float(invoice_data.get("amount_paid", 0)) / 100,
                    amount_remaining=float(invoice_data.get("amount_remaining", 0)) / 100,
                    status=PaymentStatus.SUCCEEDED,
                    due_date=self._parse_timestamp(invoice_data.get("due_date")),
                    paid_at=self._parse_timestamp(invoice_data.get("status_transitions", {}).get("paid_at")),
                    stripe_customer_id=stripe_customer_id,
                    stripe_charge_id=invoice_data.get("charge"),
                    currency=invoice_data.get("currency"),
                    subtotal=invoice_data.get("subtotal"),
                    tax=invoice_data.get("tax"),
                    total=invoice_data.get("total"),
                    amount_shipping=invoice_data.get("amount_shipping"),
                    billing_reason=invoice_data.get("billing_reason"),
                    collection_method=invoice_data.get("collection_method"),
                    customer_email=invoice_data.get("customer_email"),
                    customer_name=invoice_data.get("customer_name"),
                    customer_address=invoice_data.get("customer_address"),
                    customer_shipping=invoice_data.get("customer_shipping"),
                    lines=invoice_data.get("lines"),
                    hosted_invoice_url=invoice_data.get("hosted_invoice_url"),
                    invoice_pdf=invoice_data.get("invoice_pdf"),
                    stripe_metadata=invoice_data.get("metadata", {}),
                    organization_id=organization_id,
                    subscription_id=subscription_id
                )
                
                db.add(new_invoice)
            
            await db.commit()
            
            logger.info(f"Processed invoice payment: {stripe_invoice_id} - {invoice_data.get('amount_paid', 0)} cents")
            
        except Exception as e:
            logger.error(f"Error handling invoice.payment_succeeded: {e}")
            await db.rollback()
            raise
    
    async def handle_invoice_payment_failed(self, invoice_data: Dict[str, Any], db: AsyncSession) -> None:
        """Handle invoice.payment_failed webhook event."""
        try:
            stripe_invoice_id = invoice_data.get("id")
            if not stripe_invoice_id:
                logger.error("Invoice payment_failed event missing invoice ID")
                return
            
            # Find existing invoice
            result = await db.execute(
                select(Invoice).where(Invoice.stripe_invoice_id == stripe_invoice_id)
            )
            invoice = result.scalar_one_or_none()
            
            if not invoice:
                logger.warning(f"Invoice {stripe_invoice_id} not found for payment failure")
                return
            
            # Update invoice status
            invoice.status = PaymentStatus.FAILED
            
            await db.commit()
            
            logger.info(f"Marked invoice as failed: {stripe_invoice_id}")
            
        except Exception as e:
            logger.error(f"Error handling invoice.payment_failed: {e}")
            await db.rollback()
            raise
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    async def _link_customer_to_user(self, stripe_customer_id: str, email: str, db: AsyncSession) -> None:
        """Link Stripe customer to user by email."""
        try:
            # Find user by email
            result = await db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            
            if user:
                # Update user with stripe_customer_id
                await db.execute(
                    update(User)
                    .where(User.id == user.id)
                    .values(stripe_customer_id=stripe_customer_id)
                )
                await db.commit()
                logger.info(f"Linked customer {stripe_customer_id} to user {user.id}")
        except Exception as e:
            logger.error(f"Error linking customer to user: {e}")
    
    def _parse_timestamp(self, timestamp: Optional[int]) -> Optional[datetime]:
        """Parse Unix timestamp to datetime."""
        if timestamp is None:
            return None
        try:
            from datetime import datetime
            return datetime.fromtimestamp(timestamp)
        except (ValueError, TypeError):
            return None
    
    def _get_primary_price_id(self, subscription_data: Dict[str, Any]) -> Optional[str]:
        """Get the primary price ID from subscription data."""
        try:
            items = subscription_data.get("items", {}).get("data", [])
            if items and isinstance(items, list) and len(items) > 0:
                first_item = items[0]
                if isinstance(first_item, dict):
                    price = first_item.get("price")
                    if isinstance(price, dict):
                        return price.get("id")
                    elif isinstance(price, str):
                        return price
            return None
        except (KeyError, IndexError, TypeError, AttributeError):
            return None
