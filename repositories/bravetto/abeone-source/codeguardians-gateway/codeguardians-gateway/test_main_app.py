#!/usr/bin/env python3
"""Test script to verify main application can be imported."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test importing the main application
    from app.main import app
    print(" Main application imported successfully!")
    
    # Test app properties
    print(f" App title: {app.title}")
    print(f" App version: {app.version}")
    
    # List routes
    routes = [route for route in app.routes if hasattr(route, 'path')]
    print(f" Number of routes: {len(routes)}")
    
    # Check for Stripe webhooks route
    stripe_routes = [route for route in routes if 'stripe' in route.path.lower()]
    print(f" Stripe webhook routes: {len(stripe_routes)}")
    
    for route in stripe_routes:
        print(f"  - {route.path}")
    
    print("\n Main application tests passed!")
    
except Exception as e:
    print(f" Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
