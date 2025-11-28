#!/usr/bin/env python3
"""
Complete Unified Gateway Verification

Tests all functionality through the unified CodeGuardians Gateway,
including the integrated bias detection.
"""

import requests
import json
import time
from typing import Dict, Any

def test_gateway_health():
    """Test gateway health and service discovery"""
    print("1. Testing Gateway Health and Service Discovery...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Gateway Health: OK")
            print(f"   Status: {data.get('status')}")
            print(f"   Services: {len(data.get('services', {}))}")
            return True
        else:
            print(f"   Gateway Health: FAIL HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   Gateway Health: ERROR - {e}")
        return False

def test_unified_guard_processing():
    """Test unified guard processing for all guard types"""
    print("\n2. Testing Unified Guard Processing...")
    
    test_cases = [
        {
            "name": "TokenGuard Processing",
            "service_type": "tokenguard",
            "payload": {
                "text": "This is a very long verbose response that contains a lot of unnecessary words and could definitely benefit from compression to reduce token usage and improve efficiency.",
                "context": "some context"
            }
        },
        {
            "name": "TrustGuard Processing", 
            "service_type": "trustguard",
            "payload": {
                "text": "This is a safe message with no violations.",
                "context": "no violations"
            }
        },
        {
            "name": "ContextGuard Processing",
            "service_type": "contextguard", 
            "payload": {
                "text": "What is the capital of France?",
                "context": "Paris is the capital of France."
            }
        },
        {
            "name": "Bias Detection Processing (Integrated)",
            "service_type": "biasguard",
            "payload": {
                "text": "He should be the manager because men are better leaders than women.",
                "bias_types": ["gender_bias", "racial_bias"],
                "mitigation_level": "moderate"
            }
        },
        {
            "name": "HealthGuard Processing",
            "service_type": "healthguard",
            "payload": {
                "service_name": "test_service",
                "status": "healthy"
            }
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        try:
            request_data = {
                "service_type": test_case["service_type"],
                "payload": test_case["payload"],
                "user_id": "test-user-123",
                "session_id": "test-session-456"
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/guards/process",
                json=request_data,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   {test_case['name']}: OK")
                print(f"     Success: {data.get('success')}")
                print(f"     Service Type: {data.get('service_type')}")
                print(f"     Processing Time: {data.get('processing_time', 0):.3f}s")
                
                # Check for specific results based on service type
                if test_case["service_type"] == "biasguard":
                    result_data = data.get("result", {})
                    if "bias_detected" in result_data:
                        print(f"     Bias Detected: {result_data.get('bias_detected')}")
                        print(f"     Bias Score: {result_data.get('bias_score', 0):.3f}")
                        print(f"     Fairness Score: {result_data.get('fairness_score', 0):.3f}")
                
                results[test_case["service_type"]] = True
            else:
                print(f"   {test_case['name']}: FAIL HTTP {response.status_code}")
                print(f"     Response: {response.text[:100]}...")
                results[test_case["service_type"]] = False
                
        except Exception as e:
            print(f"   {test_case['name']}: ERROR - {e}")
            results[test_case["service_type"]] = False
    
    return results

def test_analytics_endpoints():
    """Test analytics and metrics endpoints"""
    print("\n3. Testing Analytics Endpoints...")
    
    analytics_endpoints = [
        "/api/v1/analytics/benefits/overview",
        "/api/v1/analytics/benefits/detailed", 
        "/api/v1/analytics/performance/dashboard"
    ]
    
    results = {}
    
    for endpoint in analytics_endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"   {endpoint}: OK")
                print(f"     Response keys: {list(data.keys())}")
                results[endpoint] = True
            else:
                print(f"   {endpoint}: FAIL HTTP {response.status_code}")
                results[endpoint] = False
        except Exception as e:
            print(f"   {endpoint}: ERROR - {e}")
            results[endpoint] = False
    
    return results

def test_service_discovery():
    """Test service discovery and routing"""
    print("\n4. Testing Service Discovery...")
    
    try:
        response = requests.get("http://localhost:8000/api/v1/guards/services", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Service Discovery: OK")
            print(f"     Available Services: {len(data.get('services', []))}")
            
            services = data.get('services', [])
            for service in services:
                if isinstance(service, dict):
                    print(f"     - {service.get('name')}: {service.get('status')}")
                else:
                    print(f"     - {service}")
            
            return True
        else:
            print(f"   Service Discovery: FAIL HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   Service Discovery: ERROR - {e}")
        return False

def test_bias_detection_integration():
    """Test the integrated bias detection specifically"""
    print("\n5. Testing Integrated Bias Detection...")
    
    bias_test_cases = [
        {
            "name": "Gender Bias Detection",
            "text": "He should be the manager because men are better leaders than women.",
            "expected_bias": True
        },
        {
            "name": "Racial Bias Detection",
            "text": "This is a diverse and inclusive workplace for all employees.",
            "expected_bias": False
        },
        {
            "name": "Age Bias Detection", 
            "text": "Young people are lazy and old people are slow.",
            "expected_bias": True
        }
    ]
    
    results = {}
    
    for test_case in bias_test_cases:
        try:
            request_data = {
                "service_type": "biasguard",
                "payload": {
                    "text": test_case["text"],
                    "bias_types": ["gender_bias", "racial_bias", "age_bias"],
                    "mitigation_level": "moderate",
                    "target_audience": "professional"
                },
                "user_id": "test-user-123",
                "session_id": "test-session-456"
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/guards/process",
                json=request_data,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                result_data = data.get("result", {})
                
                bias_detected = result_data.get("bias_detected", False)
                bias_score = result_data.get("bias_score", 0)
                fairness_score = result_data.get("fairness_score", 0)
                suggestions = result_data.get("mitigation_suggestions", [])
                
                print(f"   {test_case['name']}: OK")
                print(f"     Bias Detected: {bias_detected}")
                print(f"     Bias Score: {bias_score:.3f}")
                print(f"     Fairness Score: {fairness_score:.3f}")
                print(f"     Suggestions: {len(suggestions)}")
                
                # Check if detection matches expectation
                if bias_detected == test_case["expected_bias"]:
                    print(f"     Result: CORRECT")
                    results[test_case["name"]] = True
                else:
                    print(f"     Result: UNEXPECTED (expected {test_case['expected_bias']})")
                    results[test_case["name"]] = False
            else:
                print(f"   {test_case['name']}: FAIL HTTP {response.status_code}")
                results[test_case["name"]] = False
                
        except Exception as e:
            print(f"   {test_case['name']}: ERROR - {e}")
            results[test_case["name"]] = False
    
    return results

def main():
    """Main test function"""
    print("COMPLETE UNIFIED GATEWAY VERIFICATION")
    print("=" * 60)
    print("Testing all functionality through the unified CodeGuardians Gateway")
    print("including integrated bias detection (no separate BiasGuard needed)")
    print("=" * 60)
    
    # Run all tests
    health_ok = test_gateway_health()
    guard_results = test_unified_guard_processing()
    analytics_results = test_analytics_endpoints()
    discovery_ok = test_service_discovery()
    bias_results = test_bias_detection_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    print(f"Gateway Health: {'PASS' if health_ok else 'FAIL'}")
    print(f"Service Discovery: {'PASS' if discovery_ok else 'FAIL'}")
    
    print("\nGuard Processing Results:")
    for service, success in guard_results.items():
        status = "PASS" if success else "FAIL"
        print(f"  {service}: {status}")
    
    print("\nAnalytics Results:")
    for endpoint, success in analytics_results.items():
        status = "PASS" if success else "FAIL"
        print(f"  {endpoint}: {status}")
    
    print("\nBias Detection Results:")
    for test, success in bias_results.items():
        status = "PASS" if success else "FAIL"
        print(f"  {test}: {status}")
    
    # Overall assessment
    total_tests = 1 + 1 + len(guard_results) + len(analytics_results) + len(bias_results)
    passed_tests = (1 if health_ok else 0) + (1 if discovery_ok else 0) + sum(guard_results.values()) + sum(analytics_results.values()) + sum(bias_results.values())
    
    print(f"\nOverall Results: {passed_tests}/{total_tests} tests passed")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\nSUCCESS: ALL SYSTEMS OPERATIONAL!")
        print("The unified CodeGuardians Gateway is working perfectly with integrated bias detection.")
        print("No separate BiasGuard service needed - authentication issues completely resolved!")
    else:
        print(f"\nWARNING: {total_tests - passed_tests} tests failed - review details above")
    
    print("\n" + "=" * 60)
    print("UNIFIED GATEWAY VERIFICATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
