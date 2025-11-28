#!/usr/bin/env python3
"""
Stripe Webhook Event Simulator for AIGuards Backend Testing

This script simulates various Stripe webhook events to test the integration.
"""

import json
import requests
import hmac
import hashlib
from datetime import datetime
import argparse
import sys

class StripeWebhookSimulator:
    """Simulates Stripe webhook events for testing."""

    def __init__(self, webhook_url="http://localhost:8000/webhooks/stripe", webhook_secret=None):
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret or "whsec_test_secret"

    def create_signature(self, payload: str) -> str:
        """Create Stripe webhook signature."""
        timestamp = int(datetime.now().timestamp())
        signed_payload = f"{timestamp}.{payload}"
        signature = hmac.new(
            self.webhook_secret.encode(),
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"t={timestamp},v1={signature}"

    def send_event(self, event_type: str, event_data: dict, event_id: str = None):
        """Send a webhook event."""
        if event_id is None:
            event_id = f"evt_{int(datetime.now().timestamp())}"

        payload = {
            "id": event_id,
            "object": "event",
            "api_version": "2020-08-27",
            "created": int(datetime.now().timestamp()),
            "data": {
                "object": event_data,
                "previous_attributes": None
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": f"req_{int(datetime.now().timestamp())}",
                "idempotency_key": None
            },
            "type": event_type
        }

        payload_str = json.dumps(payload, separators=(',', ':'))
        signature = self.create_signature(payload_str)

        headers = {
            "Content-Type": "application/json",
            "Stripe-Signature": signature,
            "User-Agent": "Stripe/1.0 (+https://stripe.com/docs/webhooks)"
        }

        print(f" Sending {event_type} event...")
        print(f"   URL: {self.webhook_url}")
        print(f"   Payload: {payload_str[:200]}...")

        try:
            response = requests.post(
                self.webhook_url,
                data=payload_str,
                headers=headers,
                timeout=10
            )

            print(f" Response Status: {response.status_code}")
            print(f" Response: {response.text}")

            return response.status_code == 200

        except requests.RequestException as e:
            print(f" Request failed: {e}")
            return False

    def simulate_all_events(self):
        """Simulate all supported Stripe webhook events."""
        events = [
            # Product events
            ("product.created", {
                "id": "prod_test_123",
                "object": "product",
                "active": True,
                "created": int(datetime.now().timestamp()),
                "description": "Test Product",
                "name": "AI Guardian Pro",
                "type": "service",
                "livemode": False,
                "updated": int(datetime.now().timestamp())
            }),

            ("product.updated", {
                "id": "prod_test_123",
                "object": "product",
                "active": True,
                "created": int(datetime.now().timestamp()),
                "description": "Updated Test Product",
                "name": "AI Guardian Pro Plus",
                "type": "service",
                "updated": int(datetime.now().timestamp())
            }),

            # Price events
            ("price.created", {
                "id": "price_test_123",
                "object": "price",
                "active": True,
                "billing_scheme": "per_unit",
                "created": int(datetime.now().timestamp()),
                "currency": "usd",
                "product": "prod_test_123",
                "type": "recurring",
                "unit_amount": 2900,
                "recurring": {
                    "interval": "month",
                    "interval_count": 1
                }
            }),

            # Customer events
            ("customer.created", {
                "id": "cus_test_123",
                "object": "customer",
                "created": int(datetime.now().timestamp()),
                "livemode": False,
                "email": "test@example.com",
                "name": "Test Customer",
                "description": None,
                "metadata": {}
            }),

            # Subscription events
            ("customer.subscription.created", {
                "id": "sub_test_123",
                "object": "subscription",
                "customer": "cus_test_123",
                "status": "active",
                "current_period_start": int(datetime.now().timestamp()),
                "current_period_end": int(datetime.now().timestamp()) + 30*24*60*60,
                "items": {
                    "data": [{
                        "price": {
                            "id": "price_test_123",
                            "product": "prod_test_123"
                        }
                    }]
                }
            }),

            ("customer.subscription.updated", {
                "id": "sub_test_123",
                "object": "subscription",
                "customer": "cus_test_123",
                "status": "active",
                "current_period_start": int(datetime.now().timestamp()),
                "current_period_end": int(datetime.now().timestamp()) + 30*24*60*60
            }),

            # Invoice events
            ("invoice.payment_succeeded", {
                "id": "in_test_123",
                "object": "invoice",
                "customer": "cus_test_123",
                "subscription": "sub_test_123",
                "status": "paid",
                "amount_paid": 2900,
                "amount_due": 2900,
                "currency": "usd"
            }),

            ("invoice.payment_failed", {
                "id": "in_test_456",
                "object": "invoice",
                "customer": "cus_test_123",
                "subscription": "sub_test_123",
                "status": "open",
                "amount_paid": 0,
                "amount_due": 2900,
                "currency": "usd",
                "attempt_count": 3
            })
        ]

        results = []
        for event_type, event_data in events:
            success = self.send_event(event_type, event_data)
            results.append((event_type, success))
            print()

        print(" SIMULATION RESULTS:")
        print("=" * 50)
        for event_type, success in results:
            status = " PASSED" if success else " FAILED"
            print(f"{event_type:30} {status}")

        passed = sum(1 for _, success in results if success)
        total = len(results)
        print(f"\n SUMMARY: {passed}/{total} events processed successfully")

        return passed == total


def main():
    parser = argparse.ArgumentParser(description="Stripe Webhook Event Simulator")
    parser.add_argument("--url", default="http://localhost:8000/webhooks/stripe",
                       help="Webhook URL (default: http://localhost:8000/webhooks/stripe)")
    parser.add_argument("--secret", default="whsec_test_secret",
                       help="Webhook secret (default: whsec_test_secret)")
    parser.add_argument("--event", help="Specific event type to simulate")
    parser.add_argument("--all", action="store_true", help="Simulate all events")

    args = parser.parse_args()

    simulator = StripeWebhookSimulator(args.url, args.secret)

    if args.all:
        success = simulator.simulate_all_events()
        sys.exit(0 if success else 1)
    elif args.event:
        # Send specific event
        event_data = {
            "id": f"obj_test_{int(datetime.now().timestamp())}",
            "object": "test_object",
            "created": int(datetime.now().timestamp())
        }
        success = simulator.send_event(args.event, event_data)
        sys.exit(0 if success else 1)
    else:
        print("Use --all to simulate all events or --event <event_type> for specific event")
        print("Available events: product.created, product.updated, price.created, customer.created,")
        print("                  customer.subscription.created, customer.subscription.updated,")
        print("                  invoice.payment_succeeded, invoice.payment_failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
