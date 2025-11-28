#!/usr/bin/env python3
"""Test script to verify models can be imported without database connection."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test importing the models
    from app.core.models import (
        User, StripeProduct, StripePrice, StripeCustomer, 
        Subscription, Invoice
    )
    print(" All models imported successfully!")
    
    # Test model creation (without database)
    print("\n Testing model creation...")
    
    # Test User model
    user = User(
        email="test@example.com",
        full_name="Test User",
        clerk_user_id="clerk_123",
        stripe_customer_id="cus_123"
    )
    print(f" User model: {user}")
    
    # Test StripeProduct model
    product = StripeProduct(
        stripe_product_id="prod_123",
        name="Test Product",
        type="service",
        active=True
    )
    print(f" StripeProduct model: {product}")
    
    # Test StripePrice model
    price = StripePrice(
        stripe_price_id="price_123",
        stripe_product_id="prod_123",
        currency="usd",
        type="recurring",
        unit_amount=1000,
        billing_scheme="per_unit",
        tax_behavior="unspecified"
    )
    print(f" StripePrice model: {price}")
    
    # Test StripeCustomer model
    customer = StripeCustomer(
        stripe_customer_id="cus_123",
        email="test@example.com",
        name="Test Customer"
    )
    print(f" StripeCustomer model: {customer}")
    
    # Test Subscription model
    subscription = Subscription(
        organization_id=1,
        subscription_tier_id=1,
        stripe_subscription_id="sub_123",
        stripe_customer_id="cus_123",
        stripe_price_id="price_123"
    )
    print(f" Subscription model: {subscription}")
    
    # Test Invoice model
    invoice = Invoice(
        organization_id=1,
        subscription_id=1,
        invoice_number="INV-123",
        amount_due=10.00,
        amount_paid=0.00,
        amount_remaining=10.00,
        stripe_invoice_id="in_123",
        stripe_customer_id="cus_123"
    )
    print(f" Invoice model: {invoice}")
    
    print("\n All model tests passed! The models are correctly defined.")
    
except Exception as e:
    print(f" Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
