#!/usr/bin/env python3
"""
Webhook Testing Script for AIGuards Backend

This script tests the webhook endpoints to ensure they're properly configured
and responding correctly.

Usage:
    python test_webhooks.py --base-url https://your-domain.com
"""

import argparse
import requests
import json
import hmac
import hashlib
import time
from typing import Dict, Any


def generate_stripe_signature(payload: str, secret: str) -> str:
    """Generate a Stripe webhook signature for testing."""
    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.{payload}"
    signature = hmac.new(
        secret.encode('utf-8'),
        signed_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"t={timestamp},v1={signature}"


def generate_clerk_signature(payload: str, secret: str) -> Dict[str, str]:
    """Generate Clerk webhook headers for testing."""
    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.{payload}"
    signature = hmac.new(
        secret.encode('utf-8'),
        signed_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return {
        'svix-id': f'msg_test_{int(time.time())}',
        'svix-timestamp': timestamp,
        'svix-signature': f'v1,{signature}'
    }


def test_stripe_webhook(base_url: str, webhook_secret: str = "whsec_test_secret"):
    """Test Stripe webhook endpoint."""
    print(" Testing Stripe Webhook...")
    
    # Test payload
    payload = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_test_1234567890",
                "customer": "cus_test_1234567890",
                "subscription": "sub_test_1234567890",
                "metadata": {
                    "organization_id": "org_test_123",
                    "tier_id": "tier_test_123"
                }
            }
        }
    }
    
    payload_str = json.dumps(payload)
    signature = generate_stripe_signature(payload_str, webhook_secret)
    
    headers = {
        'Content-Type': 'application/json',
        'Stripe-Signature': signature
    }
    
    # Test the correct endpoint
    endpoint = f"{base_url}/webhooks/stripe"
    
    try:
        print(f"  Testing: {endpoint}")
        response = requests.post(
            endpoint,
            data=payload_str,
            headers=headers,
            timeout=10
        )
        
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("   Stripe webhook test passed")
        else:
            print(f"   Stripe webhook test failed (Status: {response.status_code})")
            try:
                error_detail = response.json()
                print(f"  Error details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
                
    except requests.exceptions.RequestException as e:
        print(f"   Error testing {endpoint}: {e}")


def test_clerk_webhook(base_url: str, webhook_secret: str = "whsec_test_secret"):
    """Test Clerk webhook endpoint."""
    print(" Testing Clerk Webhook...")
    
    # Test payload
    payload = {
        "type": "user.created",
        "data": {
            "id": "user_test_1234567890",
            "email_addresses": [
                {
                    "id": "email_test_123",
                    "email_address": "test@example.com",
                    "verification": {"status": "verified"}
                }
            ],
            "primary_email_address_id": "email_test_123",
            "first_name": "Test",
            "last_name": "User"
        }
    }
    
    payload_str = json.dumps(payload)
    headers = generate_clerk_signature(payload_str, webhook_secret)
    headers['Content-Type'] = 'application/json'
    
    endpoint = f"{base_url}/webhooks/clerk"
    
    try:
        print(f"  Testing: {endpoint}")
        response = requests.post(
            endpoint,
            data=payload_str,
            headers=headers,
            timeout=10
        )
        
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("   Clerk webhook test passed")
        else:
            print(f"   Clerk webhook test failed (Status: {response.status_code})")
            try:
                error_detail = response.json()
                print(f"  Error details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
            
    except requests.exceptions.RequestException as e:
        print(f"   Error testing {endpoint}: {e}")


def test_health_endpoints(base_url: str):
    """Test health and basic endpoints."""
    print(" Testing Health Endpoints...")
    
    health_endpoints = [
        f"{base_url}/health",
        f"{base_url}/api/v1/health",
        f"{base_url}/metrics"
    ]
    
    for endpoint in health_endpoints:
        try:
            print(f"  Testing: {endpoint}")
            response = requests.get(endpoint, timeout=5)
            print(f"  Status: {response.status_code}")
            
            if response.status_code in [200, 404]:  # 404 is ok if endpoint doesn't exist
                print("   Health endpoint accessible")
            else:
                print("   Health endpoint failed")
                
        except requests.exceptions.RequestException as e:
            print(f"   Error testing {endpoint}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Test AIGuards Backend webhooks')
    parser.add_argument('--base-url', required=True, help='Base URL of your application')
    parser.add_argument('--stripe-secret', default='whsec_test_secret', help='Stripe webhook secret for testing')
    parser.add_argument('--clerk-secret', default='whsec_test_secret', help='Clerk webhook secret for testing')
    parser.add_argument('--skip-webhooks', action='store_true', help='Skip webhook tests (only test health endpoints)')
    
    args = parser.parse_args()
    
    print(" AIGuards Backend Webhook Testing")
    print("=" * 50)
    print(f"Base URL: {args.base_url}")
    print()
    
    # Test health endpoints first
    test_health_endpoints(args.base_url)
    print()
    
    if not args.skip_webhooks:
        # Test webhook endpoints
        test_stripe_webhook(args.base_url, args.stripe_secret)
        print()
        test_clerk_webhook(args.base_url, args.clerk_secret)
        print()
    
    print(" Testing completed!")
    print()
    print(" Next Steps:")
    print("1. If webhook tests failed, check your webhook secret configuration")
    print("2. Ensure your webhook endpoints are properly deployed")
    print("3. Check your application logs for any errors")
    print("4. Verify that your webhook secrets match between your service and Stripe/Clerk")


if __name__ == "__main__":
    main()
