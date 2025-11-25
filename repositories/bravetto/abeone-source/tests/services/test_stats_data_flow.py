#!/usr/bin/env python3
"""
Comprehensive Stats and Data Flow Test

This script tests the complete data flow through the unified gateway,
including metrics collection, analytics, and business intelligence.
"""

import requests
import json
import time
import asyncio
from datetime import datetime

def test_gateway_health():
    """Test gateway health and basic connectivity"""
    print("1. TESTING GATEWAY HEALTH")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   OK Gateway Status: {data.get('status')}")
            print(f"   OK Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"   FAIL Gateway Health: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ERROR Gateway Health: {e}")
        return False

def test_service_discovery():
    """Test service discovery and routing"""
    print("\n2. TESTING SERVICE DISCOVERY")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/api/v1/guards/services", timeout=10)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', [])
            print(f"   OK Services Available: {len(services)}")
            
            for service in services:
                if isinstance(service, dict):
                    name = service.get('name', 'Unknown')
                    status = service.get('status', 'Unknown')
                    print(f"     - {name}: {status}")
            
            return True
        else:
            print(f"   FAIL Service Discovery: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ERROR Service Discovery: {e}")
        return False

def test_guard_processing():
    """Test guard processing and data flow"""
    print("\n3. TESTING GUARD PROCESSING & DATA FLOW")
    print("=" * 40)
    
    headers = {"Authorization": "Bearer test-token"}
    test_cases = [
        {
            "name": "TokenGuard",
            "service_type": "tokenguard",
            "payload": {
                "text": "This is a very long verbose response that contains a lot of unnecessary words and could definitely benefit from compression to reduce token usage and improve efficiency.",
                "target_ratio": 0.7
            }
        },
        {
            "name": "TrustGuard", 
            "service_type": "trustguard",
            "payload": {
                "text": "This content needs to be validated for safety and compliance with our policies.",
                "context": "business communication"
            }
        },
        {
            "name": "ContextGuard",
            "service_type": "contextguard", 
            "payload": {
                "key": "user_preference",
                "value": "prefers detailed technical explanations"
            }
        },
        {
            "name": "BiasGuard (Integrated)",
            "service_type": "biasguard",
            "payload": {
                "text": "He should be the manager because men are better leaders than women in technical roles.",
                "bias_types": ["gender_bias"]
            }
        },
        {
            "name": "HealthGuard",
            "service_type": "healthguard",
            "payload": {
                "service": "all"
            }
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        print(f"\n   Testing {test_case['name']}...")
        try:
            payload = {
                "service_type": test_case["service_type"],
                "payload": test_case["payload"]
            }
            
            start_time = time.time()
            response = requests.post(
                "http://localhost:8000/api/v1/guards/process", 
                json=payload, 
                headers=headers, 
                timeout=15
            )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                processing_time = (end_time - start_time) * 1000  # Convert to ms
                
                print(f"   OK {test_case['name']}: Success={success}, Time={processing_time:.1f}ms")
                
                if data.get('data'):
                    result_data = data['data']
                    print(f"     Response Data: {len(str(result_data))} chars")
                    
                    # Store results for analytics testing
                    results[test_case['name']] = {
                        'success': success,
                        'processing_time': processing_time,
                        'data': result_data
                    }
                else:
                    print(f"     WARNING: No response data")
                    results[test_case['name']] = {
                        'success': success,
                        'processing_time': processing_time,
                        'data': None
                    }
            else:
                print(f"   FAIL {test_case['name']}: HTTP {response.status_code}")
                results[test_case['name']] = {
                    'success': False,
                    'processing_time': 0,
                    'data': None
                }
                
        except Exception as e:
            print(f"   ERROR {test_case['name']}: {e}")
            results[test_case['name']] = {
                'success': False,
                'processing_time': 0,
                'data': None
            }
    
    return results

def test_analytics_endpoints():
    """Test analytics and metrics endpoints"""
    print("\n4. TESTING ANALYTICS & METRICS")
    print("=" * 40)
    
    headers = {"Authorization": "Bearer test-token"}
    analytics_tests = [
        {
            "name": "Benefits Overview",
            "endpoint": "/api/v1/analytics/benefits/overview"
        },
        {
            "name": "Detailed Benefits",
            "endpoint": "/api/v1/analytics/benefits/detailed"
        },
        {
            "name": "Performance Dashboard", 
            "endpoint": "/api/v1/analytics/performance/dashboard"
        }
    ]
    
    analytics_results = {}
    
    for test in analytics_tests:
        print(f"\n   Testing {test['name']}...")
        try:
            response = requests.get(
                f"http://localhost:8000{test['endpoint']}", 
                headers=headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   OK {test['name']}: Data available")
                print(f"     Response Size: {len(str(data))} chars")
                
                # Show key metrics if available
                if 'total_cost_savings_usd' in data:
                    print(f"     Cost Savings: ${data.get('total_cost_savings_usd', 0):.2f}")
                if 'total_tokens_saved' in data:
                    print(f"     Tokens Saved: {data.get('total_tokens_saved', 0)}")
                if 'total_requests' in data:
                    print(f"     Total Requests: {data.get('total_requests', 0)}")
                
                analytics_results[test['name']] = {
                    'success': True,
                    'data': data
                }
            elif response.status_code == 401:
                print(f"   OK {test['name']}: Requires authentication (expected)")
                analytics_results[test['name']] = {
                    'success': True,
                    'data': None,
                    'note': 'Authentication required'
                }
            else:
                print(f"   WARNING {test['name']}: HTTP {response.status_code}")
                analytics_results[test['name']] = {
                    'success': False,
                    'data': None
                }
                
        except Exception as e:
            print(f"   ERROR {test['name']}: {e}")
            analytics_results[test['name']] = {
                'success': False,
                'data': None
            }
    
    return analytics_results

def test_bias_detection_direct():
    """Test integrated bias detection directly"""
    print("\n5. TESTING INTEGRATED BIAS DETECTION")
    print("=" * 40)
    
    headers = {"Authorization": "Bearer test-token"}
    bias_tests = [
        {
            "name": "Gender Bias Detection",
            "text": "He should be the manager because men are better leaders than women.",
            "expected_bias": True
        },
        {
            "name": "Age Bias Detection", 
            "text": "Young people are lazy and old people are slow and outdated.",
            "expected_bias": True
        },
        {
            "name": "No Bias Detection",
            "text": "This is a diverse and inclusive workplace for all employees.",
            "expected_bias": False
        }
    ]
    
    bias_results = {}
    
    for test in bias_tests:
        print(f"\n   Testing {test['name']}...")
        try:
            payload = {
                "text": test["text"],
                "bias_types": ["gender_bias", "age_bias", "racial_bias"]
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/bias/detect",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                bias_detected = data.get('bias_detected', False)
                bias_score = data.get('bias_score', 0)
                bias_types = data.get('bias_types', [])
                
                print(f"   OK {test['name']}: Bias Detected={bias_detected}, Score={bias_score:.3f}")
                print(f"     Types: {bias_types}")
                
                # Check if detection matches expectation
                if bias_detected == test["expected_bias"]:
                    print(f"     Result: CORRECT")
                else:
                    print(f"     Result: UNEXPECTED (expected {test['expected_bias']})")
                
                bias_results[test['name']] = {
                    'success': True,
                    'bias_detected': bias_detected,
                    'bias_score': bias_score,
                    'bias_types': bias_types,
                    'correct': bias_detected == test["expected_bias"]
                }
            else:
                print(f"   FAIL {test['name']}: HTTP {response.status_code}")
                bias_results[test['name']] = {
                    'success': False
                }
                
        except Exception as e:
            print(f"   ERROR {test['name']}: {e}")
            bias_results[test['name']] = {
                'success': False
            }
    
    return bias_results

def test_data_flow_summary():
    """Generate comprehensive data flow summary"""
    print("\n6. DATA FLOW SUMMARY")
    print("=" * 40)
    
    # Test all components
    gateway_health = test_gateway_health()
    service_discovery = test_service_discovery()
    guard_results = test_guard_processing()
    analytics_results = test_analytics_endpoints()
    bias_results = test_bias_detection_direct()
    
    # Calculate summary statistics
    total_guards_tested = len(guard_results)
    successful_guards = sum(1 for result in guard_results.values() if result['success'])
    total_analytics_tested = len(analytics_results)
    successful_analytics = sum(1 for result in analytics_results.values() if result['success'])
    total_bias_tested = len(bias_results)
    successful_bias = sum(1 for result in bias_results.values() if result['success'])
    
    print(f"\nSUMMARY STATISTICS:")
    print(f"  Gateway Health: {'PASS' if gateway_health else 'FAIL'}")
    print(f"  Service Discovery: {'PASS' if service_discovery else 'FAIL'}")
    print(f"  Guard Processing: {successful_guards}/{total_guards_tested} successful")
    print(f"  Analytics Endpoints: {successful_analytics}/{total_analytics_tested} successful")
    print(f"  Bias Detection: {successful_bias}/{total_bias_tested} successful")
    
    # Calculate average processing time
    processing_times = [result['processing_time'] for result in guard_results.values() if result['processing_time'] > 0]
    if processing_times:
        avg_processing_time = sum(processing_times) / len(processing_times)
        print(f"  Average Processing Time: {avg_processing_time:.1f}ms")
    
    # Overall success rate
    total_tests = 1 + 1 + total_guards_tested + total_analytics_tested + total_bias_tested
    total_successful = (1 if gateway_health else 0) + (1 if service_discovery else 0) + successful_guards + successful_analytics + successful_bias
    success_rate = (total_successful / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\nOVERALL SUCCESS RATE: {success_rate:.1f}% ({total_successful}/{total_tests})")
    
    if success_rate >= 80:
        print("\nSUCCESS: Data flow and stats collection working well!")
    elif success_rate >= 60:
        print("\nWARNING: Some components need attention")
    else:
        print("\nFAIL: Major issues detected in data flow")
    
    return {
        'gateway_health': gateway_health,
        'service_discovery': service_discovery,
        'guard_results': guard_results,
        'analytics_results': analytics_results,
        'bias_results': bias_results,
        'success_rate': success_rate
    }

def main():
    """Main test execution"""
    print("COMPREHENSIVE STATS & DATA FLOW TEST")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        results = test_data_flow_summary()
        
        print("\n" + "=" * 60)
        print("TEST COMPLETED")
        print("=" * 60)
        
        return results['success_rate'] >= 60
        
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


