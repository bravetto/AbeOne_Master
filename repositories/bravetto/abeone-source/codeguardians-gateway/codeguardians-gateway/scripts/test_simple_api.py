#!/usr/bin/env python3
"""
Simplified API Test - Tests the unified endpoint without database dependency
"""

import asyncio
import json
import sys
import time
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_unified_api():
    """Test the unified API endpoint"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 1: Health endpoint
        try:
            response = await client.get(f"{base_url}/health/live")
            print(f"Health endpoint: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS: Gateway is running")
            else:
                print("FAILED: Gateway health check failed")
                return False
        except Exception as e:
            print(f"FAILED: Cannot connect to gateway: {e}")
            return False
        
        # Test 2: Unified guard endpoint
        test_payload = {
            "text": "This is a test message for AI guard analysis.",
            "user_id": "test_user_123",
            "session_id": "test_session_456"
        }
        
        try:
            print("Testing unified guard endpoint...")
            response = await client.post(
                f"{base_url}/api/v1/guards/process",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Unified endpoint status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("SUCCESS: Unified API is working!")
                print(f"Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print(f"FAILED: Unified API failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"FAILED: Unified API test failed: {e}")
            return False

async def main():
    """Main test execution"""
    print("Testing AIGuards Unified API")
    print("=" * 50)
    
    success = await test_unified_api()
    
    if success:
        print("\nSUCCESS: Unified API is working correctly!")
        return 0
    else:
        print("\nFAILED: Unified API is not working")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
