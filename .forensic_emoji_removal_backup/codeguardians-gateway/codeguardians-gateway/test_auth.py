#!/usr/bin/env python3
"""Test script to verify auth module can be imported."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test importing the auth module
    from app.api.v1 import auth
    print("✅ Auth module imported successfully!")
    
    # Test router properties
    print(f"✅ Auth router prefix: {auth.router.prefix}")
    print(f"✅ Auth router tags: {auth.router.tags}")
    
    # List routes
    routes = [route for route in auth.router.routes if hasattr(route, 'path')]
    print(f"✅ Number of auth routes: {len(routes)}")
    
    for route in routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            print(f"  - {list(route.methods)} {route.path}")
    
    print("\n🎉 Auth module tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
