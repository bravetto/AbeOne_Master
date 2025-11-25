#!/usr/bin/env python3
"""
Minimal test to validate the unified API without database dependency
"""

import asyncio
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

async def test_minimal():
    """Test the application components without starting the server"""
    try:
        # Test 1: Import the main app
        print("Testing application imports...")
        from app.main import app
        print("SUCCESS: Main app imported")
        
        # Test 2: Check if the app has the unified endpoint
        print("Testing unified endpoint registration...")
        
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        print(f"Available routes: {routes}")
        
        # Check for unified endpoint
        unified_endpoint = "/api/v1/guards/process"
        if unified_endpoint in routes:
            print(f"SUCCESS: Unified endpoint {unified_endpoint} is registered")
        else:
            print(f"FAILED: Unified endpoint {unified_endpoint} not found")
            return False
        
        # Test 3: Check guard orchestrator
        print("Testing guard orchestrator...")
        from app.core.guard_orchestrator import GuardServiceOrchestrator
        orchestrator = GuardServiceOrchestrator()
        print(f"SUCCESS: Guard orchestrator created with {len(orchestrator.services)} services")
        
        # Test 4: Check AWS secrets integration
        print("Testing AWS secrets integration...")
        from app.core.config import get_settings
        settings = get_settings()
        print(f"SUCCESS: Settings loaded, AWS secrets enabled: {settings.AWS_SECRETS_ENABLED}")
        
        return True
        
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test execution"""
    print("Testing AIGuards Application Components")
    print("=" * 50)
    
    success = await test_minimal()
    
    if success:
        print("\nSUCCESS: All components are working correctly!")
        print("The unified API should be functional when the server starts.")
        return 0
    else:
        print("\nFAILED: Some components are not working")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
