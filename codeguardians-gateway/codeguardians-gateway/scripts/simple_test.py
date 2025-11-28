#!/usr/bin/env python3
"""
Simple endpoint testing script for AIGuardian API
Tests all guard services through the unified router
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(name, url, method="GET", data=None):
    """Test a single endpoint"""
    try:
        print(f"\nTesting: {name}")
        print(f"  URL: {url}")

        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"}, timeout=30)

        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"  Success: {json.dumps(result, indent=2)[:200]}...")
            return True
        else:
            print(f"  Error: {response.text}")
            return False

    except Exception as e:
        print(f"  Exception: {str(e)}")
        return False

def main():
    print("=" * 80)
    print("AIGuardian Endpoint Testing Suite")
    print("=" * 80)

    passed = 0
    failed = 0

    # Health checks
    print("\n[1] Health Check Endpoints")
    if test_endpoint("Liveness", f"{BASE_URL}/health/live"):
        passed += 1
    else:
        failed += 1

    if test_endpoint("Readiness", f"{BASE_URL}/health/ready"):
        passed += 1
    else:
        failed += 1

    if test_endpoint("Comprehensive Health", f"{BASE_URL}/health/comprehensive"):
        passed += 1
    else:
        failed += 1

    # Guard services health
    print("\n[2] Guard Services Health")
    if test_endpoint("All Guards Health", f"{BASE_URL}/api/v1/guards/health"):
        passed += 1
    else:
        failed += 1

    # Unified router tests
    print("\n[3] Unified Guard Router - TokenGuard")
    if test_endpoint(
        "TokenGuard via Unified Router",
        f"{BASE_URL}/api/v1/guards/process",
        method="POST",
        data={
            "service_type": "tokenguard",
            "payload": {"text": "Hello world"}
        }
    ):
        passed += 1
    else:
        failed += 1

    print("\n[4] Unified Guard Router - TrustGuard")
    if test_endpoint(
        "TrustGuard via Unified Router",
        f"{BASE_URL}/api/v1/guards/process",
        method="POST",
        data={
            "service_type": "trustguard",
            "payload": {"text": "Test content for validation"}
        }
    ):
        passed += 1
    else:
        failed += 1

    print("\n[5] Unified Guard Router - ContextGuard")
    if test_endpoint(
        "ContextGuard via Unified Router",
        f"{BASE_URL}/api/v1/guards/process",
        method="POST",
        data={
            "service_type": "contextguard",
            "payload": {"operation": "get", "data": {"key": "test"}}
        }
    ):
        passed += 1
    else:
        failed += 1

    print("\n[6] Unified Guard Router - BiasGuard")
    if test_endpoint(
        "BiasGuard via Unified Router",
        f"{BASE_URL}/api/v1/guards/process",
        method="POST",
        data={
            "service_type": "biasguard",
            "payload": {"operation": "detect_bias", "data": {"text": "Test text"}}
        }
    ):
        passed += 1
    else:
        failed += 1

    print("\n[7] Unified Guard Router - SecurityGuard")
    if test_endpoint(
        "SecurityGuard via Unified Router",
        f"{BASE_URL}/api/v1/guards/process",
        method="POST",
        data={
            "service_type": "securityguard",
            "payload": {"text": "SELECT * FROM users"}
        }
    ):
        passed += 1
    else:
        failed += 1

    # Direct service endpoints
    print("\n[8] Direct Service Endpoint - TokenGuard Optimize")
    if test_endpoint(
        "TokenGuard Optimize",
        f"{BASE_URL}/api/v1/guards/tokenguard/optimize",
        method="POST",
        data={"text": "Test text for optimization"}
    ):
        passed += 1
    else:
        failed += 1

    print("\n[9] Direct Service Endpoint - TrustGuard Validate")
    if test_endpoint(
        "TrustGuard Validate",
        f"{BASE_URL}/api/v1/guards/trustguard/validate",
        method="POST",
        data={"content": "Test content"}
    ):
        passed += 1
    else:
        failed += 1

    print("\n[10] Service Discovery")
    if test_endpoint("List Services", f"{BASE_URL}/api/v1/guards/services"):
        passed += 1
    else:
        failed += 1

    if test_endpoint("Discovery Services", f"{BASE_URL}/api/v1/guards/discovery/services"):
        passed += 1
    else:
        failed += 1

    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)
    else:
        print("\nAll tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
