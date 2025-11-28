#!/usr/bin/env python3
"""
Complete End-to-End Test for AIGuards Unified API
Tests the unified /api/v1/guards/process endpoint with all 6 guard services
"""

import asyncio
import json
import sys
import time
from typing import Dict, List, Any
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def test_health_endpoints(self) -> Dict[str, bool]:
        """Test all health endpoints"""
        results = {}
        
        # Test main gateway health
        try:
            response = await self.client.get(f"{self.base_url}/health/live")
            results["gateway_live"] = response.status_code == 200
            logger.info(f"Gateway live health: {results['gateway_live']}")
        except Exception as e:
            results["gateway_live"] = False
            logger.error(f"Gateway live health failed: {e}")
            
        try:
            response = await self.client.get(f"{self.base_url}/health/ready")
            results["gateway_ready"] = response.status_code == 200
            logger.info(f"Gateway ready health: {results['gateway_ready']}")
        except Exception as e:
            results["gateway_ready"] = False
            logger.error(f"Gateway ready health failed: {e}")
            
        return results
    
    async def test_unified_guard_endpoint(self) -> Dict[str, Any]:
        """Test the unified guard processing endpoint"""
        test_payload = {
            "text": "This is a test message for AI guard analysis. Please analyze for security, bias, context, and trust.",
            "user_id": "test_user_123",
            "session_id": "test_session_456",
            "metadata": {
                "source": "test_suite",
                "timestamp": int(time.time())
            }
        }
        
        try:
            logger.info("Testing unified guard endpoint...")
            response = await self.client.post(
                f"{self.base_url}/api/v1/guards/process",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            )
            
            result = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response_data": response.json() if response.status_code == 200 else None,
                "error": response.text if response.status_code != 200 else None
            }
            
            logger.info(f"Unified endpoint response: {response.status_code}")
            return result
            
        except Exception as e:
            logger.error(f"Unified endpoint test failed: {e}")
            return {
                "status_code": 0,
                "success": False,
                "response_data": None,
                "error": str(e)
            }
    
    async def test_individual_guard_health(self) -> Dict[str, bool]:
        """Test individual guard service health endpoints"""
        guard_services = [
            "tokenguard",
            "trustguard", 
            "contextguard",
            "biasguard",
            "securityguard",
            "healthguard"
        ]
        
        results = {}
        
        for guard in guard_services:
            try:
                # Test health endpoint for each guard
                response = await self.client.get(f"{self.base_url}/guards/{guard}/health")
                results[guard] = response.status_code == 200
                logger.info(f"Guard {guard} health: {results[guard]}")
            except Exception as e:
                results[guard] = False
                logger.error(f"Guard {guard} health failed: {e}")
                
        return results
    
    async def test_guard_specific_endpoints(self) -> Dict[str, Any]:
        """Test guard-specific endpoints"""
        results = {}
        
        # Test TokenGuard optimization
        try:
            response = await self.client.post(
                f"{self.base_url}/tokenguard/optimize",
                json={"text": "Test token optimization", "max_tokens": 100}
            )
            results["tokenguard_optimize"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200
            }
        except Exception as e:
            results["tokenguard_optimize"] = {"status_code": 0, "success": False, "error": str(e)}
        
        # Test TrustGuard validation
        try:
            response = await self.client.post(
                f"{self.base_url}/trustguard/validate",
                json={"text": "Test trust validation", "user_id": "test_user"}
            )
            results["trustguard_validate"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200
            }
        except Exception as e:
            results["trustguard_validate"] = {"status_code": 0, "success": False, "error": str(e)}
            
        return results
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run complete end-to-end test suite"""
        logger.info(" Starting Comprehensive AIGuards Unified API Test")
        
        start_time = time.time()
        
        # Test 1: Health endpoints
        logger.info(" Testing health endpoints...")
        health_results = await self.test_health_endpoints()
        
        # Test 2: Individual guard health
        logger.info(" Testing individual guard health...")
        guard_health = await self.test_individual_guard_health()
        
        # Test 3: Guard-specific endpoints
        logger.info(" Testing guard-specific endpoints...")
        guard_endpoints = await self.test_guard_specific_endpoints()
        
        # Test 4: Unified guard endpoint (main test)
        logger.info(" Testing unified guard endpoint...")
        unified_result = await self.test_unified_guard_endpoint()
        
        end_time = time.time()
        
        # Compile results
        results = {
            "test_duration": end_time - start_time,
            "health_endpoints": health_results,
            "guard_health": guard_health,
            "guard_endpoints": guard_endpoints,
            "unified_endpoint": unified_result,
            "overall_success": (
                health_results.get("gateway_live", False) and
                health_results.get("gateway_ready", False) and
                unified_result.get("success", False)
            )
        }
        
        return results
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

async def main():
    """Main test execution"""
    tester = UnifiedAPITester()
    
    try:
        results = await tester.run_comprehensive_test()
        
        # Print results
        print("\n" + "="*60)
        print(" AIGUARDS UNIFIED API TEST RESULTS")
        print("="*60)
        
        print(f"\n⏱  Test Duration: {results['test_duration']:.2f} seconds")
        
        print(f"\n Health Endpoints:")
        for endpoint, status in results['health_endpoints'].items():
            status_icon = "" if status else ""
            print(f"  {status_icon} {endpoint}: {status}")
        
        print(f"\n  Guard Services Health:")
        for guard, status in results['guard_health'].items():
            status_icon = "" if status else ""
            print(f"  {status_icon} {guard}: {status}")
        
        print(f"\n Guard Endpoints:")
        for endpoint, result in results['guard_endpoints'].items():
            status_icon = "" if result.get('success', False) else ""
            print(f"  {status_icon} {endpoint}: {result.get('status_code', 'N/A')}")
        
        print(f"\n Unified Endpoint:")
        unified = results['unified_endpoint']
        status_icon = "" if unified.get('success', False) else ""
        print(f"  {status_icon} Status: {unified.get('status_code', 'N/A')}")
        
        if unified.get('response_data'):
            print(f"   Response: {json.dumps(unified['response_data'], indent=2)}")
        elif unified.get('error'):
            print(f"   Error: {unified['error']}")
        
        print(f"\n Overall Success: {' YES' if results['overall_success'] else ' NO'}")
        
        if results['overall_success']:
            print("\n All tests passed! The unified API is working correctly.")
            return 0
        else:
            print("\n Some tests failed. Check the logs above for details.")
            return 1
            
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return 1
    finally:
        await tester.close()

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
