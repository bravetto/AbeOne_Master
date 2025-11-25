#!/usr/bin/env python3
"""Test script to verify webhook router can be imported."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test importing the webhook router
    from app.api.webhooks.stripe_webhooks import router
    print("✅ Stripe webhooks router imported successfully!")
    
    # Test router properties
    print(f"✅ Router prefix: {router.prefix}")
    print(f"✅ Router tags: {router.tags}")
    
    # List routes
    routes = [route for route in router.routes]
    print(f"✅ Number of routes: {len(routes)}")
    
    for route in routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            print(f"  - {list(route.methods)} {route.path}")
    
    print("\n🎉 Webhook router tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
