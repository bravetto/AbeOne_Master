#!/usr/bin/env python3
"""
Unified Router Testing Script
Tests the gateway's unified API endpoint with all guard services
"""

import requests
import json
import time
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_unified_router():
    """Test the unified router with all guard services"""

    print("=" * 80)
    print("Unified Router Testing - AIGuards Gateway")
    print("=" * 80)
    print(f"Testing Gateway at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # First check if gateway is running
    print("\n[1] Checking Gateway Health...")
    try:
        response = requests.get(f"{BASE_URL}/health/live", timeout=5)
        if response.status_code == 200:
            print(" Gateway is healthy")
        else:
            print(f" Gateway health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f" Cannot connect to gateway: {e}")
        print("Please start the gateway first: docker-compose up -d")
        return False

    # Test service discovery
    print("\n[2] Testing Service Discovery...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/guards/services", timeout=10)
        if response.status_code == 200:
            services = response.json().get('services', [])
            print(f" Service discovery works - {len(services)} services registered")
            print(f"  Available services: {', '.join(services) if services else 'None'}")
        else:
            print(f" Service discovery failed: {response.status_code}")
            return False
    except Exception as e:
        print(f" Service discovery error: {e}")
        return False

    # Test cases for each guard service
    test_cases = [
        {
            "name": "TokenGuard",
            "service_type": "tokenguard",
            "payload": {
                "text": "This is a test message that should be optimized for token usage and processed by TokenGuard. It contains some repetitive information that could be compressed to reduce costs.",
                "content_type": "text"
            },
            "expected_fields": ["tokens_saved", "cost_savings", "compression_ratio"]
        },
        {
            "name": "TrustGuard",
            "service_type": "trustguard",
            "payload": {
                "validation_type": "general",
                "content": "This AI response appears to be hallucinating false information about quantum computing capabilities that don't exist in reality.",
                "validation_level": "standard"
            },
            "expected_fields": ["compliance_score", "risk_level", "violations_detected"]
        },
        {
            "name": "ContextGuard",
            "service_type": "contextguard",
            "payload": {
                "operation": "set",
                "data": {
                    "key": "test_context",
                    "value": "This is important context information that should be stored and retrieved efficiently for conversational continuity.",
                    "ttl": 3600
                }
            },
            "expected_fields": ["success", "context_id"]
        },
        {
            "name": "BiasGuard",
            "service_type": "biasguard",
            "payload": {
                "operation": "detect_bias",
                "data": {
                    "text": "All women are naturally better at nurturing and caregiving roles than men due to their inherent maternal instincts.",
                    "bias_types": ["gender", "stereotype"]
                }
            },
            "expected_fields": ["bias_detected", "bias_score", "fairness_score"]
        },
        {
            "name": "HealthGuard",
            "service_type": "healthguard",
            "payload": {
                "content": "INFO: Application started successfully. Memory usage: 45MB, CPU: 12%. Database connections: 5/10. All systems operational.",
                "content_type": "system_log"
            },
            "expected_fields": ["health_status", "issues_detected"]
        }
    ]

    passed = 0
    failed = 0
    results = []

    for i, test_case in enumerate(test_cases, 3):
        print(f"\n[{i}] Testing {test_case['name']} via Unified Router...")

        request_data = {
            "service_type": test_case["service_type"],
            "payload": test_case["payload"],
            "user_id": "test-user-123",
            "session_id": "test-session-456",
            "request_id": f"test-{test_case['service_type']}-{int(time.time())}"
        }

        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/v1/guards/process",
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)

            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get("success", False)

                    if success:
                        print(f" {test_case['name']}: SUCCESS ({response_time}ms)")
                        print(f"  Service: {data.get('service_type', 'unknown')}")
                        print(f"  Processing Time: {data.get('processing_time_ms', 0)}ms")

                        # Check for expected fields
                        guard_response = data.get("guard_response", {})
                        found_fields = []
                        if test_case.get("expected_fields"):
                            for field in test_case["expected_fields"]:
                                if field in str(guard_response):
                                    found_fields.append(field)

                        if found_fields:
                            print(f"  Found expected fields: {', '.join(found_fields)}")

                        results.append({
                            "service": test_case["name"],
                            "status": "PASS",
                            "response_time_ms": response_time,
                            "found_fields": found_fields
                        })
                        passed += 1
                    else:
                        error_msg = data.get("error", "Unknown error")
                        print(f" {test_case['name']}: FAILED - {error_msg} ({response_time}ms)")
                        results.append({
                            "service": test_case["name"],
                            "status": "FAIL",
                            "error": error_msg,
                            "response_time_ms": response_time
                        })
                        failed += 1

                except json.JSONDecodeError:
                    print(f" {test_case['name']}: FAILED - Invalid JSON response ({response_time}ms)")
                    results.append({
                        "service": test_case["name"],
                        "status": "FAIL",
                        "error": "Invalid JSON response",
                        "response_time_ms": response_time
                    })
                    failed += 1

            else:
                print(f" {test_case['name']}: FAILED - HTTP {response.status_code} ({response_time}ms)")
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", response.text[:200])
                except:
                    error_msg = response.text[:200]
                print(f"  Error: {error_msg}")

                results.append({
                    "service": test_case["name"],
                    "status": "FAIL",
                    "http_code": response.status_code,
                    "error": error_msg,
                    "response_time_ms": response_time
                })
                failed += 1

        except requests.exceptions.Timeout:
            print(f" {test_case['name']}: FAILED - Timeout (30s)")
            results.append({
                "service": test_case["name"],
                "status": "FAIL",
                "error": "Timeout"
            })
            failed += 1
        except Exception as e:
            print(f" {test_case['name']}: FAILED - {str(e)}")
            results.append({
                "service": test_case["name"],
                "status": "FAIL",
                "error": str(e)
            })
            failed += 1

    # Final summary
    print("\n" + "=" * 80)
    print("UNIFIED ROUTER TEST RESULTS")
    print("=" * 80)
    print(f"Gateway URL: {BASE_URL}")
    print(f"Total Services Tested: {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
    # Detailed results
    print("\nService Results:")
    for result in results:
        status_icon = "" if result["status"] == "PASS" else ""
        print(f"  {status_icon} {result['service']}: {result['status']}")
        if "response_time_ms" in result:
            print(f"    Response time: {result['response_time_ms']}ms")
        if "error" in result:
            print(f"    Error: {result['error']}")

    print("\n" + "=" * 80)

    if failed == 0:
        print(" SUCCESS: Unified router works perfectly for all guard services!")
        print("The AIGuards Gateway is fully operational.")
        return True
    else:
        print(f"  WARNING: {failed} services failed routing through the unified router.")
        print("Check individual service health and gateway configuration.")
        return False

if __name__ == "__main__":
    success = test_unified_router()
    sys.exit(0 if success else 1)
