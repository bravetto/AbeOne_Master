#!/usr/bin/env python3
"""
Test TrustGuard Authentication Fix
Tests the service-to-service authentication via gateway
"""

import requests
import json
import sys

GATEWAY_URL = "http://localhost:8000"
TRUSTGUARD_URL = "http://localhost:8002"  # Note: TrustGuard runs on port 8000 internally but may be exposed on 8002

def test_gateway_health():
    """Test gateway health endpoint"""
    print(" Testing Gateway Health...")
    try:
        response = requests.get(f"{GATEWAY_URL}/health/live", timeout=5)
        if response.status_code == 200:
            print(" Gateway health check passed")
            return True
        else:
            print(f" Gateway health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f" Gateway not accessible: {e}")
        return False

def test_trustguard_health():
    """Test TrustGuard health endpoint"""
    print("\n Testing TrustGuard Health...")
    try:
        response = requests.get(f"{TRUSTGUARD_URL}/health", timeout=5)
        if response.status_code == 200:
            print(" TrustGuard health check passed")
            return True
        else:
            print(f" TrustGuard health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f" TrustGuard not accessible: {e}")
        return False

def test_trustguard_via_gateway():
    """Test TrustGuard via gateway with service-to-service auth"""
    print("\n Testing TrustGuard via Gateway (Service-to-Service Auth)...")
    
    payload = {
        "service_type": "trustguard",
        "payload": {
            "text": "This is a test message for TrustGuard detection",
            "context": None,
            "metadata": {}
        }
    }
    
    try:
        response = requests.post(
            f"{GATEWAY_URL}/api/v1/guards/process",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(" TrustGuard request via gateway succeeded!")
            result = response.json()
            print(f"Response keys: {list(result.keys())}")
            if "data" in result:
                print(f" Data returned: {type(result['data'])}")
            return True
        elif response.status_code == 403:
            print(" FAILED: 403 Forbidden - Authentication issue!")
            print(f"Error: {response.text}")
            return False
        elif response.status_code == 401:
            print(" FAILED: 401 Unauthorized - Authentication issue!")
            print(f"Error: {response.text}")
            return False
        else:
            print(f" Unexpected status code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f" Request failed: {e}")
        return False

def test_service_discovery():
    """Test service discovery endpoint"""
    print("\n Testing Service Discovery...")
    try:
        response = requests.get(f"{GATEWAY_URL}/api/v1/guards/services", timeout=10)
        if response.status_code == 200:
            data = response.json()
            services = data.get("services", {})
            print(f" Found {len(services)} services")
            for name, service in services.items():
                status = service.get("status", "unknown")
                print(f"  - {name}: {status}")
            return True
        else:
            print(f" Service discovery failed: {response.status_code}")
            return False
    except Exception as e:
        print(f" Service discovery error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print(" TrustGuard Authentication Fix Test Suite")
    print("=" * 60)
    
    results = {
        "gateway_health": test_gateway_health(),
        "trustguard_health": test_trustguard_health(),
        "service_discovery": test_service_discovery(),
        "trustguard_via_gateway": test_trustguard_via_gateway()
    }
    
    print("\n" + "=" * 60)
    print(" Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = " PASS" if result else " FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n All tests passed! Authentication fix is working correctly!")
        return 0
    else:
        print("\n  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

