#!/usr/bin/env python3
"""
Comprehensive End-to-End Test for AIGuardian Gateway

This test verifies the complete data flow through the unified gateway,
including all guard services, analytics, and business metrics.
"""

import asyncio
import httpx
import json
import time
from typing import Dict, Any, List
from datetime import datetime

BASE_URL = "http://localhost:8000"

class E2ETestRunner:
    """Comprehensive end-to-end test runner."""
    
    def __init__(self):
        self.results = {
            "gateway_health": False,
            "service_discovery": False,
            "guard_services": {},
            "analytics": {},
            "business_metrics": {},
            "data_flow": {},
            "performance": {},
            "overall_success": False
        }
        self.test_data = {
            "sample_text": "This is a comprehensive test of the AIGuardian system. It should detect various issues and provide valuable insights for developers and users.",
            "bias_text": "Only young people are good at technology. Older workers should retire early.",
            "technical_text": "The system architecture uses microservices with async/await patterns for optimal performance.",
            "health_metrics": {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.1,
                "network_latency": 12.5
            }
        }
    
    async def run_all_tests(self):
        """Run all end-to-end tests."""
        print(" Starting Comprehensive End-to-End Test")
        print("=" * 60)
        
        # Test 1: Gateway Health and Infrastructure
        await self.test_gateway_health()
        
        # Test 2: Service Discovery and Registration
        await self.test_service_discovery()
        
        # Test 3: Individual Guard Services
        await self.test_guard_services()
        
        # Test 4: Analytics and Business Intelligence
        await self.test_analytics_system()
        
        # Test 5: Business Metrics and ROI
        await self.test_business_metrics()
        
        # Test 6: Complete Data Flow
        await self.test_complete_data_flow()
        
        # Test 7: Performance and Scalability
        await self.test_performance_metrics()
        
        # Generate final report
        self.generate_final_report()
    
    async def test_gateway_health(self):
        """Test gateway health and basic functionality."""
        print("\n Testing Gateway Health and Infrastructure...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test basic health endpoint
                response = await client.get(f"{BASE_URL}/health")
                if response.status_code == 200:
                    health_data = response.json()
                    print(f"   Gateway Health: {health_data['status']}")
                    self.results["gateway_health"] = True
                else:
                    print(f"   Gateway Health Failed: {response.status_code}")
                
                # Test readiness endpoint
                response = await client.get(f"{BASE_URL}/health/ready")
                if response.status_code == 200:
                    ready_data = response.json()
                    print(f"   Gateway Ready: {ready_data['status']}")
                    if 'checks' in ready_data:
                        for check, status in ready_data['checks'].items():
                            print(f"    - {check}: {status}")
                else:
                    print(f"   Gateway Readiness Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   Gateway Health Error: {e}")
    
    async def test_service_discovery(self):
        """Test service discovery and registration."""
        print("\n Testing Service Discovery...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test service discovery endpoint
                response = await client.get(f"{BASE_URL}/api/v1/guards/discovery/services")
                if response.status_code == 200:
                    discovery_data = response.json()
                    print(f"   Service Discovery: Found {discovery_data.get('total_services', 0)} services")
                    
                    services = discovery_data.get('services', {})
                    healthy_count = 0
                    for service_name, service_info in services.items():
                        status = service_info.get('health_status', 'unknown')
                        if status == 'healthy':
                            healthy_count += 1
                        print(f"    - {service_name}: {status}")
                    
                    print(f"   Healthy Services: {healthy_count}/{len(services)}")
                    self.results["service_discovery"] = True
                else:
                    print(f"   Service Discovery Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   Service Discovery Error: {e}")
    
    async def test_guard_services(self):
        """Test all guard services through the unified endpoint."""
        print("\n Testing Guard Services...")
        
        guard_tests = [
            {
                "name": "TokenGuard",
                "service_type": "tokenguard",
                "payload": {
                    "text": self.test_data["sample_text"],
                    "confidence": 0.8
                },
                "expected_fields": ["tokens_saved", "cost_savings", "optimization_score"]
            },
            {
                "name": "BiasGuard",
                "service_type": "biasguard",
                "payload": {
                    "text": self.test_data["bias_text"],
                    "bias_types": ["age", "gender"],
                    "mitigation_level": "moderate"
                },
                "expected_fields": ["bias_detected", "bias_score", "mitigation_suggestions"]
            },
            {
                "name": "HealthGuard",
                "service_type": "healthguard",
                "payload": {
                    "text": self.test_data["technical_text"],
                    "confidence": 0.7,
                    "metrics": self.test_data["health_metrics"]
                },
                "expected_fields": ["health_score", "recommendations", "metrics"]
            },
            {
                "name": "ContextGuard",
                "service_type": "contextguard",
                "payload": {
                    "operation": "store",
                    "data": {"context": "test_context", "user_id": "test_user"},
                    "consciousness_context": {"session": "test_session"}
                },
                "expected_fields": ["success", "context_id", "stored_data"]
            },
            {
                "name": "TrustGuard",
                "service_type": "trustguard",
                "payload": {
                    "validation_type": "content_trust",
                    "content": self.test_data["sample_text"],
                    "validation_level": "standard"
                },
                "expected_fields": ["trust_score", "reliability_metrics", "validation_result"]
            }
        ]
        
        async with httpx.AsyncClient() as client:
            for test in guard_tests:
                try:
                    print(f"  Testing {test['name']}...")
                    
                    response = await client.post(
                        f"{BASE_URL}/api/v1/guards/process",
                        json={
                            "service_type": test["service_type"],
                            "payload": test["payload"],
                            "client_type": "api"
                        },
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        success = data.get('success', False)
                        
                        if success:
                            print(f"     {test['name']}: Success")
                            
                            # Check for expected fields
                            response_data = data.get('data', {})
                            found_fields = []
                            for field in test['expected_fields']:
                                if field in response_data:
                                    found_fields.append(field)
                            
                            print(f"     Response Fields: {found_fields}")
                            
                            self.results["guard_services"][test["name"]] = {
                                "success": True,
                                "response_time": data.get('processing_time', 0),
                                "fields_found": found_fields,
                                "data": response_data
                            }
                        else:
                            print(f"     {test['name']}: Success=False, Error: {data.get('error', 'Unknown')}")
                            self.results["guard_services"][test["name"]] = {
                                "success": False,
                                "error": data.get('error', 'Unknown')
                            }
                    else:
                        print(f"     {test['name']}: HTTP {response.status_code}")
                        try:
                            error_data = response.json()
                            print(f"    Error: {error_data}")
                        except:
                            print(f"    Error: {response.text}")
                        
                        self.results["guard_services"][test["name"]] = {
                            "success": False,
                            "error": f"HTTP {response.status_code}"
                        }
                        
                except Exception as e:
                    print(f"     {test['name']}: Exception - {e}")
                    self.results["guard_services"][test["name"]] = {
                        "success": False,
                        "error": str(e)
                    }
    
    async def test_analytics_system(self):
        """Test analytics and business intelligence endpoints."""
        print("\n Testing Analytics System...")
        
        analytics_endpoints = [
            "/api/v1/analytics/benefits/overview",
            "/api/v1/analytics/benefits/detailed",
            "/api/v1/analytics/performance/dashboard"
        ]
        
        async with httpx.AsyncClient() as client:
            for endpoint in analytics_endpoints:
                try:
                    print(f"  Testing {endpoint}...")
                    
                    response = await client.get(f"{BASE_URL}{endpoint}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        print(f"     {endpoint}: Available")
                        
                        # Analyze the response data
                        if "benefits" in endpoint:
                            self.results["analytics"][endpoint] = {
                                "success": True,
                                "data_keys": list(data.keys()) if isinstance(data, dict) else [],
                                "has_metrics": any(key in str(data).lower() for key in ["cost", "savings", "tokens", "roi"])
                            }
                        elif "performance" in endpoint:
                            self.results["analytics"][endpoint] = {
                                "success": True,
                                "data_keys": list(data.keys()) if isinstance(data, dict) else [],
                                "has_metrics": any(key in str(data).lower() for key in ["performance", "uptime", "latency", "throughput"])
                            }
                    else:
                        print(f"     {endpoint}: HTTP {response.status_code}")
                        self.results["analytics"][endpoint] = {
                            "success": False,
                            "error": f"HTTP {response.status_code}"
                        }
                        
                except Exception as e:
                    print(f"     {endpoint}: Error - {e}")
                    self.results["analytics"][endpoint] = {
                        "success": False,
                        "error": str(e)
                    }
    
    async def test_business_metrics(self):
        """Test business metrics and ROI calculations."""
        print("\n Testing Business Metrics...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test benefits overview for business metrics
                response = await client.get(f"{BASE_URL}/api/v1/analytics/benefits/overview")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check for key business metrics
                    business_metrics = {
                        "cost_savings": "cost_savings_usd" in data,
                        "tokens_saved": "tokens_saved" in data,
                        "productivity": "productivity_increase_percent" in data,
                        "risk_reduction": "risk_reduction_percent" in data,
                        "uptime": "uptime_percent" in data
                    }
                    
                    print(f"   Business Metrics Available:")
                    for metric, available in business_metrics.items():
                        status = "" if available else ""
                        print(f"    {status} {metric}")
                    
                    self.results["business_metrics"] = {
                        "success": True,
                        "metrics_available": business_metrics,
                        "data": data
                    }
                else:
                    print(f"   Business Metrics Failed: HTTP {response.status_code}")
                    self.results["business_metrics"] = {
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    }
                    
        except Exception as e:
            print(f"   Business Metrics Error: {e}")
            self.results["business_metrics"] = {
                "success": False,
                "error": str(e)
            }
    
    async def test_complete_data_flow(self):
        """Test complete data flow through the system."""
        print("\n Testing Complete Data Flow...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Simulate a complete workflow
                workflow_steps = []
                
                # Step 1: Process text through multiple guards
                print("  Step 1: Multi-guard processing...")
                
                guard_requests = [
                    {"service_type": "tokenguard", "payload": {"text": self.test_data["sample_text"]}},
                    {"service_type": "biasguard", "payload": {"text": self.test_data["bias_text"]}},
                    {"service_type": "healthguard", "payload": {"text": self.test_data["technical_text"]}}
                ]
                
                guard_results = []
                for request in guard_requests:
                    response = await client.post(
                        f"{BASE_URL}/api/v1/guards/process",
                        json=request,
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        guard_results.append({
                            "service": request["service_type"],
                            "success": data.get('success', False),
                            "processing_time": data.get('processing_time', 0)
                        })
                
                workflow_steps.append({
                    "name": "Multi-guard Processing",
                    "success": all(r["success"] for r in guard_results),
                    "results": guard_results
                })
                
                print(f"     Processed {len(guard_results)} guards")
                
                # Step 2: Get analytics
                print("  Step 2: Analytics aggregation...")
                
                analytics_response = await client.get(f"{BASE_URL}/api/v1/analytics/benefits/overview")
                analytics_success = analytics_response.status_code == 200
                
                workflow_steps.append({
                    "name": "Analytics Aggregation",
                    "success": analytics_success
                })
                
                print(f"    {'' if analytics_success else ''} Analytics aggregation")
                
                # Step 3: Performance monitoring
                print("  Step 3: Performance monitoring...")
                
                performance_response = await client.get(f"{BASE_URL}/api/v1/analytics/performance/dashboard")
                performance_success = performance_response.status_code == 200
                
                workflow_steps.append({
                    "name": "Performance Monitoring",
                    "success": performance_success
                })
                
                print(f"    {'' if performance_success else ''} Performance monitoring")
                
                self.results["data_flow"] = {
                    "success": all(step["success"] for step in workflow_steps),
                    "steps": workflow_steps
                }
                
        except Exception as e:
            print(f"   Data Flow Error: {e}")
            self.results["data_flow"] = {
                "success": False,
                "error": str(e)
            }
    
    async def test_performance_metrics(self):
        """Test performance and scalability metrics."""
        print("\n Testing Performance Metrics...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test response times
                start_time = time.time()
                
                # Test multiple concurrent requests
                tasks = []
                for i in range(5):
                    task = client.post(
                        f"{BASE_URL}/api/v1/guards/process",
                        json={
                            "service_type": "tokenguard",
                            "payload": {"text": f"Performance test {i}"}
                        },
                        timeout=30.0
                    )
                    tasks.append(task)
                
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                end_time = time.time()
                total_time = end_time - start_time
                
                successful_requests = sum(1 for r in responses if not isinstance(r, Exception) and r.status_code == 200)
                avg_response_time = total_time / len(tasks)
                
                print(f"   Performance Test Results:")
                print(f"    - Total Time: {total_time:.2f}s")
                print(f"    - Average Response Time: {avg_response_time:.2f}s")
                print(f"    - Successful Requests: {successful_requests}/{len(tasks)}")
                print(f"    - Requests per Second: {len(tasks)/total_time:.2f}")
                
                self.results["performance"] = {
                    "success": successful_requests == len(tasks),
                    "total_time": total_time,
                    "avg_response_time": avg_response_time,
                    "successful_requests": successful_requests,
                    "total_requests": len(tasks),
                    "requests_per_second": len(tasks)/total_time
                }
                
        except Exception as e:
            print(f"   Performance Test Error: {e}")
            self.results["performance"] = {
                "success": False,
                "error": str(e)
            }
    
    def generate_final_report(self):
        """Generate comprehensive final report."""
        print("\n" + "=" * 60)
        print(" COMPREHENSIVE END-TO-END TEST REPORT")
        print("=" * 60)
        
        # Calculate overall success
        all_tests_passed = (
            self.results["gateway_health"] and
            self.results["service_discovery"] and
            all(service.get("success", False) for service in self.results["guard_services"].values()) and
            all(analytics.get("success", False) for analytics in self.results["analytics"].values()) and
            self.results["business_metrics"].get("success", False) and
            self.results["data_flow"].get("success", False) and
            self.results["performance"].get("success", False)
        )
        
        self.results["overall_success"] = all_tests_passed
        
        # Print summary
        print(f"\n OVERALL RESULT: {' ALL TESTS PASSED' if all_tests_passed else ' SOME TESTS FAILED'}")
        
        # Detailed breakdown
        print(f"\n DETAILED BREAKDOWN:")
        print(f"  Gateway Health: {' PASS' if self.results['gateway_health'] else ' FAIL'}")
        print(f"  Service Discovery: {' PASS' if self.results['service_discovery'] else ' FAIL'}")
        
        print(f"\n  Guard Services:")
        for service, result in self.results["guard_services"].items():
            status = " PASS" if result.get("success", False) else " FAIL"
            print(f"    {service}: {status}")
        
        print(f"\n  Analytics:")
        for endpoint, result in self.results["analytics"].items():
            status = " PASS" if result.get("success", False) else " FAIL"
            print(f"    {endpoint}: {status}")
        
        print(f"\n  Business Metrics: {' PASS' if self.results['business_metrics'].get('success', False) else ' FAIL'}")
        print(f"  Data Flow: {' PASS' if self.results['data_flow'].get('success', False) else ' FAIL'}")
        print(f"  Performance: {' PASS' if self.results['performance'].get('success', False) else ' FAIL'}")
        
        # Performance summary
        if self.results["performance"].get("success", False):
            perf = self.results["performance"]
            print(f"\n PERFORMANCE SUMMARY:")
            print(f"  Average Response Time: {perf['avg_response_time']:.2f}s")
            print(f"  Requests per Second: {perf['requests_per_second']:.2f}")
            print(f"  Success Rate: {(perf['successful_requests']/perf['total_requests'])*100:.1f}%")
        
        # Business value summary
        if self.results["business_metrics"].get("success", False):
            print(f"\n BUSINESS VALUE:")
            metrics = self.results["business_metrics"].get("data", {})
            if "cost_savings_usd" in metrics:
                print(f"  Cost Savings: ${metrics['cost_savings_usd']}")
            if "tokens_saved" in metrics:
                print(f"  Tokens Saved: {metrics['tokens_saved']:,}")
            if "productivity_increase_percent" in metrics:
                print(f"  Productivity Increase: {metrics['productivity_increase_percent']}%")
            if "risk_reduction_percent" in metrics:
                print(f"  Risk Reduction: {metrics['risk_reduction_percent']}%")
        
        print(f"\n Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return all_tests_passed


async def main():
    """Run the comprehensive end-to-end test."""
    runner = E2ETestRunner()
    success = await runner.run_all_tests()
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
