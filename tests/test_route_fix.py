#!/usr/bin/env python3
"""
Test script to verify the webhook route prefix fix.
"""
import sys
import os

# Add the codeguardians-gateway directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'codeguardians-gateway', 'codeguardians-gateway'))

def test_webhook_route_prefix():
    """Test that webhook routes have correct prefixes."""
    try:
        import app.main
        app = app.main.create_app()
        print(" FastAPI app created successfully")

        # Check that all expected routes are registered
        routes = [route.path for route in app.routes if hasattr(route, 'path')]

        # Check webhook routes - should be /webhooks/stripe, not /webhooks/webhooks/stripe
        expected_webhook_routes = [
            '/webhooks/stripe',  # Fixed: was /webhooks/webhooks/stripe
            '/webhooks/clerk',
            '/webhooks/clerk/users/{clerk_user_id}',
            '/webhooks/clerk/users/email/{email}'
        ]

        for route in expected_webhook_routes:
            if route in routes:
                print(f" Webhook route {route} correctly registered")
            else:
                print(f" Webhook route {route} missing or incorrectly prefixed")
                print(f"   Found webhook routes: {[r for r in routes if 'webhooks' in r]}")
                return False

        # Check that the double-prefixed route is NOT present
        double_prefixed = '/webhooks/webhooks/stripe'
        if double_prefixed in routes:
            print(f" Double-prefixed route {double_prefixed} still exists")
            return False
        else:
            print(" Double-prefixed route correctly removed")

        return True

    except Exception as e:
        print(f" Route prefix test failed: {e}")
        return False

if __name__ == "__main__":
    print(" Testing webhook route prefix fix...\n")

    if test_webhook_route_prefix():
        print("\n Webhook route prefix fix verified successfully!")
        sys.exit(0)
    else:
        print("\n Route prefix fix failed")
        sys.exit(1)
