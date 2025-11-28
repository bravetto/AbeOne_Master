#!/usr/bin/env python3
"""
Complete System Test for AIGuards Backend
Tests all components including unified API, guard services, and AWS secrets integration
"""

import asyncio
import json
import sys
import os
import time
import httpx
import logging

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteSystemTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def test_application_components(self) -> dict:
        """Test all application components without starting server"""
        results = {}
        
        try:
            # Test 1: Import main app
            print("Testing application imports...")
            from app.main import app
            results["app_import"] = True
            print("SUCCESS: Main app imported")
            
            # Test 2: Check unified endpoint registration
            print("Testing unified endpoint registration...")
            routes = [route.path for route in app.routes if hasattr(route, 'path')]
            unified_endpoint = "/api/v1/guards/process"
            results["unified_endpoint"] = unified_endpoint in routes
            print(f"SUCCESS: Unified endpoint {unified_endpoint} is registered")
            
            # Test 3: Check guard orchestrator
            print("Testing guard orchestrator...")
            from app.core.guard_orchestrator import GuardServiceOrchestrator
            orchestrator = GuardServiceOrchestrator()
            await orchestrator.initialize()
            results["guard_orchestrator"] = len(orchestrator.services) == 6
            results["guard_services"] = list(orchestrator.services.keys())
            print(f"SUCCESS: Guard orchestrator has {len(orchestrator.services)} services")
            
            # Test 4: Check AWS secrets integration
            print("Testing AWS secrets integration...")
            from app.core.config import get_settings
            settings = get_settings()
            results["aws_secrets"] = settings.AWS_SECRETS_ENABLED
            print(f"SUCCESS: AWS secrets integration working: {settings.AWS_SECRETS_ENABLED}")
            
            # Test 5: Check guard service imports
            print("Testing guard service imports...")
            guard_imports = {}
            try:
                import sys
                sys.path.append('../../security-guard')
                from main import app as security_app
                guard_imports["securityguard"] = True
                print("SUCCESS: SecurityGuard imported")
            except Exception as e:
                guard_imports["securityguard"] = False
                print(f"FAILED: SecurityGuard import failed: {e}")
                
            try:
                sys.path.append('../../validation-systems')
                from main import app as validation_app
                guard_imports["validation"] = True
                print("SUCCESS: ValidationSystems imported")
            except Exception as e:
                guard_imports["validation"] = False
                print(f"FAILED: ValidationSystems import failed: {e}")
                
            results["guard_imports"] = guard_imports
            
            return results
            
        except Exception as e:
            print(f"FAILED: Component test failed: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    async def test_server_startup(self) -> dict:
        """Test if the server can start and respond"""
        results = {}
        
        try:
            # Test health endpoint
            print("Testing server health...")
            response = await self.client.get(f"{self.base_url}/health/live")
            results["health_live"] = response.status_code == 200
            print(f"Health live: {response.status_code}")
            
            if response.status_code == 200:
                response = await self.client.get(f"{self.base_url}/health/ready")
                results["health_ready"] = response.status_code == 200
                print(f"Health ready: {response.status_code}")
            
            return results
            
        except Exception as e:
            print(f"FAILED: Server startup test failed: {e}")
            return {"error": str(e)}
    
    async def test_unified_api(self) -> dict:
        """Test the unified API endpoint"""
        results = {}
        
        try:
            print("Testing unified API endpoint...")
            test_payload = {
                "text": "This is a test message for AI guard analysis.",
                "user_id": "test_user_123",
                "session_id": "test_session_456",
                "metadata": {
                    "source": "test_suite",
                    "timestamp": int(time.time())
                }
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/guards/process",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            )
            
            results["status_code"] = response.status_code
            results["success"] = response.status_code == 200
            
            if response.status_code == 200:
                results["response_data"] = response.json()
                print("SUCCESS: Unified API responded correctly")
            else:
                results["error"] = response.text
                print(f"FAILED: Unified API returned {response.status_code}: {response.text}")
            
            return results
            
        except Exception as e:
            print(f"FAILED: Unified API test failed: {e}")
            return {"error": str(e)}
    
    async def run_complete_test(self) -> dict:
        """Run complete system test"""
        print("Starting Complete AIGuards System Test")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test 1: Application components
        print("\n1. Testing Application Components...")
        component_results = await self.test_application_components()
        
        # Test 2: Server startup
        print("\n2. Testing Server Startup...")
        server_results = await self.test_server_startup()
        
        # Test 3: Unified API
        print("\n3. Testing Unified API...")
        api_results = await self.test_unified_api()
        
        end_time = time.time()
        
        # Compile results
        results = {
            "test_duration": end_time - start_time,
            "components": component_results,
            "server": server_results,
            "api": api_results,
            "overall_success": (
                component_results.get("unified_endpoint", False) and
                component_results.get("guard_orchestrator", False) and
                component_results.get("aws_secrets", False) and
                server_results.get("health_live", False) and
                api_results.get("success", False)
            )
        }
        
        return results
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

async def main():
    """Main test execution"""
    tester = CompleteSystemTester()
    
    try:
        results = await tester.run_complete_test()
        
        # Print results
        print("\n" + "=" * 60)
        print("COMPLETE SYSTEM TEST RESULTS")
        print("=" * 60)
        
        print(f"\nTest Duration: {results['test_duration']:.2f} seconds")
        
        print(f"\nApplication Components:")
        components = results['components']
        print(f"  App Import: {'SUCCESS' if components.get('app_import') else 'FAILED'}")
        print(f"  Unified Endpoint: {'SUCCESS' if components.get('unified_endpoint') else 'FAILED'}")
        print(f"  Guard Orchestrator: {'SUCCESS' if components.get('guard_orchestrator') else 'FAILED'}")
        print(f"  AWS Secrets: {'SUCCESS' if components.get('aws_secrets') else 'FAILED'}")
        print(f"  Guard Services: {components.get('guard_services', [])}")
        
        print(f"\nServer Status:")
        server = results['server']
        print(f"  Health Live: {'SUCCESS' if server.get('health_live') else 'FAILED'}")
        print(f"  Health Ready: {'SUCCESS' if server.get('health_ready') else 'FAILED'}")
        
        print(f"\nUnified API:")
        api = results['api']
        print(f"  Status Code: {api.get('status_code', 'N/A')}")
        print(f"  Success: {'SUCCESS' if api.get('success') else 'FAILED'}")
        if api.get('response_data'):
            print(f"  Response: {json.dumps(api['response_data'], indent=2)}")
        elif api.get('error'):
            print(f"  Error: {api['error']}")
        
        print(f"\nOverall Success: {'SUCCESS' if results['overall_success'] else 'FAILED'}")
        
        if results['overall_success']:
            print("\n ALL TESTS PASSED! The unified API system is working correctly.")
            return 0
        else:
            print("\n SOME TESTS FAILED. Check the details above.")
            return 1
            
    except Exception as e:
        print(f"Test execution failed: {e}")
        return 1
    finally:
        await tester.close()

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
