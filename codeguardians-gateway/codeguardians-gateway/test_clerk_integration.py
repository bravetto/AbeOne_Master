#!/usr/bin/env python3
"""Test script to verify Clerk integration can be imported."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test importing the Clerk integration
    from app.core.clerk_integration import (
        verify_clerk_token, get_or_create_user_from_clerk,
        get_user_by_clerk_id, link_user_to_stripe_customer,
        extract_clerk_user_from_token
    )
    print(" Clerk integration functions imported successfully!")
    
    # Test token extraction (without verification)
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjbGVya18xMjMiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJuYW1lIjoiVGVzdCBVc2VyIn0.test"
    user_data = extract_clerk_user_from_token(test_token)
    print(f" Token extraction: {user_data}")
    
    print("\n Clerk integration tests passed!")
    
except Exception as e:
    print(f" Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
