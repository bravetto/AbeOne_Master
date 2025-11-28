#!/usr/bin/env python3
"""
End-to-end test script for Clerk webhook integration.

This script simulates the full webhook flow using actual Clerk webhook payload examples
and verifies that the data is correctly processed and stored in the database.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.clerk_webhook_service import ClerkWebhookService, process_clerk_webhook
from app.core.database import get_db
from app.core.models import User
from sqlalchemy import select


# Test data based on the webhook examples provided by the user
TEST_USER_CREATED = {
    "type": "user.created",
    "data": {
        "backup_code_enabled": False,
        "banned": False,
        "create_organization_enabled": True,
        "created_at": 1761092033534,
        "delete_self_enabled": False,
        "email_addresses": [
            {
                "created_at": 1761092024857,
                "email_address": "ben@bravetto.com",
                "id": "idn_34OkUr4TCp5FYMbN1ZzBg9RR3IJ",
                "linked_to": [],
                "matches_sso_connection": False,
                "object": "email_address",
                "reserved": False,
                "updated_at": 1761092033538,
                "verification": {
                    "attempts": 1,
                    "expire_at": 1761092625302,
                    "object": "verification_otp",
                    "status": "verified",
                    "strategy": "email_code"
                }
            }
        ],
        "enterprise_accounts": [],
        "external_accounts": [],
        "external_id": None,
        "first_name": "Benjamin",
        "has_image": False,
        "id": "REPLACE_ME",
        "image_url": "https://img.clerk.com/REPLACE_ME",
        "last_active_at": 1761092033534,
        "last_name": "Richardson",
        "last_sign_in_at": None,
        "legal_accepted_at": None,
        "locale": None,
        "locked": False,
        "lockout_expires_in_seconds": None,
        "mfa_disabled_at": None,
        "mfa_enabled_at": None,
        "object": "user",
        "passkeys": [],
        "password_enabled": True,
        "phone_numbers": [],
        "primary_email_address_id": "idn_34OkUr4TCp5FYMbN1ZzBg9RR3IJ",
        "primary_phone_number_id": None,
        "primary_web3_wallet_id": None,
        "private_metadata": {},
        "profile_image_url": "https://www.gravatar.com/avatar?d=mp",
        "public_metadata": {},
        "saml_accounts": [],
        "totp_enabled": False,
        "two_factor_enabled": False,
        "unsafe_metadata": {},
        "updated_at": 1761092033553,
        "username": None,
        "verification_attempts_remaining": 100,
        "web3_wallets": []
    },
    "event_attributes": {
        "http_request": {
            "client_ip": "2600:1702:6951:5a0:152:3271:5762:9414",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }
    },
    "instance_id": "ins_31vVBr2xPsF5LzAFlPMYFusMfuK",
    "object": "event",
    "timestamp": 1761092033570,
    "type": "user.created"
}

TEST_USER_UPDATED = {
    "type": "user.updated",
    "data": {
        "backup_code_enabled": False,
        "banned": False,
        "create_organization_enabled": True,
        "created_at": 1756854752856,
        "delete_self_enabled": False,
        "email_addresses": [
            {
                "created_at": 1756854737185,
                "email_address": "mike@bravetto.com",
                "id": "idn_32ADyX6umi5u2HjeJkRZhpph1eu",
                "linked_to": [
                    {
                        "id": "idn_32fJpiNS6FvBWjBp2BsETn15DGb",
                        "type": "oauth_google"
                    }
                ],
                "matches_sso_connection": False,
                "object": "email_address",
                "reserved": False,
                "updated_at": 1756854752867,
                "verification": {
                    "attempts": 1,
                    "expire_at": 1756855337628,
                    "object": "verification_otp",
                    "status": "verified",
                    "strategy": "email_code"
                }
            }
        ],
        "enterprise_accounts": [],
        "external_accounts": [
            {
                "approved_scopes": "email https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid profile",
                "avatar_url": "",
                "created_at": 1757805877448,
                "email_address": "mike@bravetto.com",
                "external_account_id": "eac_32fJph9RpazoJhWtkrnWubPds4c",
                "family_name": "Mataluni",
                "first_name": "Michael",
                "given_name": "Michael",
                "google_id": "107288021301459139452",
                "id": "idn_32fJpiNS6FvBWjBp2BsETn15DGb",
                "identification_id": "idn_32fJpiNS6FvBWjBp2BsETn15DGb",
                "label": None,
                "last_name": "Mataluni",
                "object": "google_account",
                "picture": "",
                "provider": "oauth_google",
                "provider_user_id": "107288021301459139452",
                "public_metadata": {},
                "updated_at": 1757805877448,
                "username": None,
                "verification": {
                    "attempts": None,
                    "expire_at": 1757806471844,
                    "object": "verification_oauth",
                    "status": "verified",
                    "strategy": "oauth_google"
                }
            }
        ],
        "external_id": None,
        "first_name": "Michael",
        "has_image": False,
        "id": "REPLACE_ME",
        "image_url": "https://img.clerk.com/REPLACE_ME",
        "last_active_at": 1757749009126,
        "last_name": "Mataluni",
        "last_sign_in_at": 1757749009057,
        "legal_accepted_at": None,
        "locked": False,
        "lockout_expires_in_seconds": None,
        "mfa_disabled_at": None,
        "mfa_enabled_at": None,
        "object": "user",
        "passkeys": [],
        "password_enabled": True,
        "phone_numbers": [],
        "primary_email_address_id": "idn_32ADyX6umi5u2HjeJkRZhpph1eu",
        "primary_phone_number_id": None,
        "primary_web3_wallet_id": None,
        "private_metadata": {},
        "profile_image_url": "https://www.gravatar.com/avatar?d=mp",
        "public_metadata": {},
        "saml_accounts": [],
        "totp_enabled": False,
        "two_factor_enabled": False,
        "unsafe_metadata": {},
        "updated_at": 1757805877456,
        "username": None,
        "verification_attempts_remaining": 100,
        "web3_wallets": []
    },
    "event_attributes": {
        "http_request": {
            "client_ip": "2600:1006:b100:15f2:7542:9a71:5f81:dcad",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }
    },
    "instance_id": "ins_31vVBr2xPsF5LzAFlPMYFusMfuK",
    "object": "event",
    "timestamp": 1757805877468,
    "type": "user.updated"
}

TEST_USER_DELETED = {
    "type": "user.deleted",
    "data": {
        "deleted": True,
        "id": "REPLACE_ME",
        "object": "user"
    },
    "event_attributes": {
        "http_request": {
            "client_ip": "2600:1900:0:2d04::a01",
            "user_agent": "clerk/clerk-sdk-go@v3.0.0"
        }
    },
    "instance_id": "ins_31vVBr2xPsF5LzAFlPMYFusMfuK",
    "object": "event",
    "timestamp": 1761091891440,
    "type": "user.deleted"
}


async def test_webhook_processing():
    """Test webhook processing with real data."""
    print("🧪 Starting Clerk Webhook E2E Test")
    print("=" * 50)
    
    try:
        # Get database session
        async with get_db() as db:
            print("✅ Database connection established")
            
            # Test 1: User Created
            print("\n📝 Test 1: Processing user.created webhook")
            print("-" * 30)
            
            success = await process_clerk_webhook(
                "user.created", 
                TEST_USER_CREATED, 
                db
            )
            
            if success:
                print("✅ user.created webhook processed successfully")
                
                # Verify user was created in database
                result = await db.execute(
                    select(User).where(User.clerk_user_id == "REPLACE_ME")
                )
                user = result.scalar_one_or_none()
                
                if user:
                    print(f"✅ User found in database: {user.email}")
                    print(f"   - Name: {user.first_name} {user.last_name}")
                    print(f"   - Clerk ID: {user.clerk_user_id}")
                    print(f"   - Active: {user.is_active}")
                    print(f"   - Verified: {user.is_verified}")
                else:
                    print("❌ User not found in database")
                    return False
            else:
                print("❌ user.created webhook processing failed")
                return False
            
            # Test 2: User Updated
            print("\n📝 Test 2: Processing user.updated webhook")
            print("-" * 30)
            
            success = await process_clerk_webhook(
                "user.updated", 
                TEST_USER_UPDATED, 
                db
            )
            
            if success:
                print("✅ user.updated webhook processed successfully")
                
                # Verify user was updated in database
                result = await db.execute(
                    select(User).where(User.clerk_user_id == "REPLACE_ME")
                )
                user = result.scalar_one_or_none()
                
                if user:
                    print(f"✅ Updated user found in database: {user.email}")
                    print(f"   - Name: {user.first_name} {user.last_name}")
                    print(f"   - Clerk ID: {user.clerk_user_id}")
                    print(f"   - Last Active: {user.last_active_at}")
                else:
                    print("❌ Updated user not found in database")
                    return False
            else:
                print("❌ user.updated webhook processing failed")
                return False
            
            # Test 3: User Deleted
            print("\n📝 Test 3: Processing user.deleted webhook")
            print("-" * 30)
            
            success = await process_clerk_webhook(
                "user.deleted", 
                TEST_USER_DELETED, 
                db
            )
            
            if success:
                print("✅ user.deleted webhook processed successfully")
                
                # Verify user was soft deleted in database
                result = await db.execute(
                    select(User).where(User.clerk_user_id == "REPLACE_ME")
                )
                user = result.scalar_one_or_none()
                
                if user:
                    print(f"✅ Deleted user found in database: {user.email}")
                    print(f"   - Active: {user.is_active}")
                    if not user.is_active:
                        print("✅ User was properly soft deleted")
                    else:
                        print("❌ User was not soft deleted")
                        return False
                else:
                    print("❌ Deleted user not found in database")
                    return False
            else:
                print("❌ user.deleted webhook processing failed")
                return False
            
            print("\n🎉 All tests passed successfully!")
            print("=" * 50)
            return True
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_validation():
    """Test data validation."""
    print("\n🔍 Testing Data Validation")
    print("-" * 30)
    
    try:
        async with get_db() as db:
            service = ClerkWebhookService(db)
            
            # Test valid data
            valid_data = TEST_USER_CREATED["data"]
            is_valid, error = service.validate_user_data(valid_data)
            if is_valid:
                print("✅ Valid data validation passed")
            else:
                print(f"❌ Valid data validation failed: {error}")
                return False
            
            # Test invalid data (missing email)
            invalid_data = {"id": "user123"}
            is_valid, error = service.validate_user_data(invalid_data)
            if not is_valid:
                print("✅ Invalid data validation correctly rejected")
            else:
                print("❌ Invalid data validation should have failed")
                return False
            
            print("✅ Data validation tests passed")
            return True
            
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 Clerk Webhook Integration E2E Test")
    print("=" * 50)
    
    # Test validation first
    validation_success = await test_validation()
    if not validation_success:
        print("❌ Validation tests failed, stopping")
        return False
    
    # Test webhook processing
    webhook_success = await test_webhook_processing()
    if not webhook_success:
        print("❌ Webhook processing tests failed")
        return False
    
    print("\n🎉 All E2E tests completed successfully!")
    print("The Clerk webhook integration is working correctly.")
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
