#!/usr/bin/env python3
"""
Comprehensive Guard Functionality Test
Tests the actual AI guard processing capabilities
"""

import asyncio
import httpx
import json
import time
from typing import Dict, Any

async def test_tokenguard_processing():
    """Test TokenGuard functionality"""
    print("\n[*] Testing TokenGuard Processing...")

    payload = {
        "service_type": "tokenguard",
        "payload": {
            "content": "This is a test message that should be optimized for token usage and processed by the TokenGuard service. It contains some repetitive information that could be compressed.",
            "content_type": "text",
            "scan_level": "standard"
        },
        "user_id": "test-user",
        "client_type": "api"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            start_time = time.time()
            response = await client.post("http://localhost:8000/api/v1/guards/process", json=payload)
            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                print(f"[OK] TokenGuard: SUCCESS ({end_time - start_time:.3f}s)")
                print(f"   Service: {data.get('service_type')}")
                print(f"   Processing Time: {data.get('processing_time_ms')}ms")

                if 'guard_response' in data:
                    guard_resp = data['guard_response']
                    print(f"   Tokens Saved: {guard_resp.get('tokens_saved', 'N/A')}")
                    print(f"   Compression Ratio: {guard_resp.get('compression_ratio', 'N/A')}")
                    print(f"   Cost Savings: ${guard_resp.get('cost_savings', 0):.6f}")

                return True
            else:
                print(f"[ERROR] TokenGuard: FAILED - Status {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                return False

    except Exception as e:
        print(f"[ERROR] TokenGuard: ERROR - {e}")
        return False

async def test_trustguard_processing():
    """Test TrustGuard functionality"""
    print("\n[*] Testing TrustGuard Processing...")

    payload = {
        "service_type": "trustguard",
        "payload": {
            "validation_type": "general",
            "content": "This AI response appears to be hallucinating false information about quantum computing capabilities that don't exist in reality.",
            "validation_level": "standard"
        },
        "user_id": "test-user",
        "client_type": "api"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            start_time = time.time()
            response = await client.post("http://localhost:8000/api/v1/guards/process", json=payload)
            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                print(f"[OK] TrustGuard: SUCCESS ({end_time - start_time:.3f}s)")
                print(f"   Service: {data.get('service_type')}")
                print(f"   Processing Time: {data.get('processing_time_ms')}ms")

                if 'guard_response' in data:
                    guard_resp = data['guard_response']
                    print(f"   Violations Detected: {guard_resp.get('violations_detected', 'N/A')}")
                    print(f"   Compliance Score: {guard_resp.get('compliance_score', 'N/A')}")
                    print(f"   Risk Level: {guard_resp.get('risk_level', 'N/A')}")

                return True
            else:
                print(f"[ERROR] TrustGuard: FAILED - Status {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                return False

    except Exception as e:
        print(f"[ERROR] TrustGuard: ERROR - {e}")
        return False

async def test_contextguard_processing():
    """Test ContextGuard functionality"""
    print("\n[*] Testing ContextGuard Processing...")

    payload = {
        "service_type": "contextguard",
        "payload": {
            "operation": "set",
            "data": {
                "key": "test_context",
                "value": "This is important context information that should be stored and retrieved efficiently.",
                "ttl": 3600
            }
        },
        "user_id": "test-user",
        "client_type": "api"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            start_time = time.time()
            response = await client.post("http://localhost:8000/api/v1/guards/process", json=payload)
            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                print(f"[OK] ContextGuard: SUCCESS ({end_time - start_time:.3f}s)")
                print(f"   Service: {data.get('service_type')}")
                print(f"   Processing Time: {data.get('processing_time_ms')}ms")

                if 'guard_response' in data:
                    guard_resp = data['guard_response']
                    print(f"   Memory Slots: {guard_resp.get('memory_slots', 'N/A')}")
                    print(f"   Relevance Score: {guard_resp.get('relevance_score', 'N/A')}")
                    print(f"   Productivity Increase: {guard_resp.get('productivity_increase', 'N/A')}%")

                return True
            else:
                print(f"[ERROR] ContextGuard: FAILED - Status {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                return False

    except Exception as e:
        print(f"[ERROR] ContextGuard: ERROR - {e}")
        return False

async def test_biasguard_processing():
    """Test BiasGuard functionality"""
    print("\n[*] Testing BiasGuard Processing...")

    payload = {
        "service_type": "biasguard",
        "payload": {
            "operation": "detect_bias",
            "data": {
                "text": "All women are naturally better at nurturing and caregiving roles than men.",
                "bias_types": ["gender", "stereotype"]
            }
        },
        "user_id": "test-user",
        "client_type": "api"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            start_time = time.time()
            response = await client.post("http://localhost:8000/api/v1/guards/process", json=payload)
            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                print(f"[OK] BiasGuard: SUCCESS ({end_time - start_time:.3f}s)")
                print(f"   Service: {data.get('service_type')}")
                print(f"   Processing Time: {data.get('processing_time_ms')}ms")

                if 'guard_response' in data:
                    guard_resp = data['guard_response']
                    print(f"   Bias Detected: {guard_resp.get('bias_detected', 'N/A')}")
                    print(f"   Bias Score: {guard_resp.get('bias_score', 'N/A')}")
                    print(f"   Fairness Score: {guard_resp.get('fairness_score', 'N/A')}")
                    print(f"   Suggestions Count: {len(guard_resp.get('suggestions', []))}")

                return True
            else:
                print(f"[ERROR] BiasGuard: FAILED - Status {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                return False

    except Exception as e:
        print(f"[ERROR] BiasGuard: ERROR - {e}")
        return False

async def test_healthguard_processing():
    """Test HealthGuard functionality"""
    print("\n[*] Testing HealthGuard Processing...")

    payload = {
        "service_type": "healthguard",
        "payload": {
            "content": "INFO: Application started successfully. Memory usage: 45MB, CPU: 12%. All systems operational.",
            "content_type": "system_log",
            "scan_level": "basic"
        },
        "user_id": "test-user",
        "client_type": "api"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            start_time = time.time()
            response = await client.post("http://localhost:8000/api/v1/guards/process", json=payload)
            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                print(f"[OK] HealthGuard: SUCCESS ({end_time - start_time:.3f}s)")
                print(f"   Service: {data.get('service_type')}")
                print(f"   Processing Time: {data.get('processing_time_ms')}ms")

                if 'guard_response' in data:
                    guard_resp = data['guard_response']
                    print(f"   Health Status: {guard_resp.get('health_status', 'N/A')}")
                    print(f"   Issues Detected: {len(guard_resp.get('issues_detected', []))}")
                    print(f"   Recommendations: {len(guard_resp.get('recommendations', []))}")

                return True
            else:
                print(f"[ERROR] HealthGuard: FAILED - Status {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                return False

    except Exception as e:
        print(f"[ERROR] HealthGuard: ERROR - {e}")
        return False

async def main():
    """Run all guard functionality tests"""
    print("COMPREHENSIVE GUARD FUNCTIONALITY VALIDATION")
    print("=" * 60)

    # Test gateway health first
    print("\n[*] Testing Gateway Health...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("[OK] Gateway: HEALTHY")
            else:
                print(f"[ERROR] Gateway: UNHEALTHY - Status {response.status_code}")
                return
    except Exception as e:
        print(f"[ERROR] Gateway: ERROR - {e}")
        return

    # Run all guard tests
    results = []
    results.append(await test_tokenguard_processing())
    results.append(await test_trustguard_processing())
    results.append(await test_contextguard_processing())
    results.append(await test_biasguard_processing())
    results.append(await test_healthguard_processing())

    # Summary
    print("\n" + "=" * 60)
    print("FUNCTIONALITY TEST SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")

    guard_names = ["TokenGuard", "TrustGuard", "ContextGuard", "BiasGuard", "HealthGuard"]
    for i, (name, result) in enumerate(zip(guard_names, results)):
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {name}: {status}")

    print("\n" + "=" * 60)
    if passed == total:
        print("SUCCESS: ALL GUARD FUNCTIONALITY TESTS PASSED!")
        print("The AI Guardians backend is fully operational.")
    else:
        print(f"WARNING: {total - passed} tests failed - review output above.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
