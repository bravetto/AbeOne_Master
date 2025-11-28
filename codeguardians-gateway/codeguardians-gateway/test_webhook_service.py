#!/usr/bin/env python3
"""Test script to verify webhook service can be imported and initialized."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test importing the webhook service
    from app.services.stripe_webhook_service import StripeWebhookService
    print(" StripeWebhookService imported successfully!")
    
    # Test service initialization
    service = StripeWebhookService()
    print(" StripeWebhookService initialized successfully!")
    
    # Test helper methods
    print("\n Testing helper methods...")
    
    # Test timestamp parsing
    timestamp = 1640995200  # 2022-01-01 00:00:00 UTC
    parsed_time = service._parse_timestamp(timestamp)
    print(f" Timestamp parsing: {timestamp} -> {parsed_time}")
    
    # Test price ID extraction
    subscription_data = {
        "items": {
            "data": [
                {
                    "price": {
                        "id": "price_123"
                    }
                }
            ]
        }
    }
    price_id = service._get_primary_price_id(subscription_data)
    print(f" Price ID extraction: {price_id}")
    
    print("\n All webhook service tests passed!")
    
except Exception as e:
    print(f" Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
