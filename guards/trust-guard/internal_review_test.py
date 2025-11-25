#!/usr/bin/env python3
"""
Internal Review Test Script for Trust Guard

This script tests all available endpoints and provides a comprehensive
assessment of the system's readiness for internal review.
"""

import requests
import json
import time
from datetime import datetime

class TrustGuardTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {}
        }
    
    def test_endpoint(self, name, method, endpoint, data=None, headers=None, expected_status=200):
        """Test a single endpoint."""
        try:
            url = f"{self.base_url}{endpoint}"
            start_time = time.time()
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response_time = (time.time() - start_time) * 1000
            
            result = {
                "status": "PASS" if response.status_code == expected_status else "FAIL",
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response_time_ms": round(response_time, 2),
                "content_length": len(response.text),
                "error": None
            }
            
            # Try to parse JSON response
            try:
                result["response_data"] = response.json()
            except:
                result["response_data"] = response.text[:200]  # First 200 chars
            
            self.results["tests"][name] = result
            return result
            
        except Exception as e:
            result = {
                "status": "ERROR",
                "error": str(e),
                "response_time_ms": 0
            }
            self.results["tests"][name] = result
            return result
    
    def run_all_tests(self):
        """Run all available tests."""
        print("Trust Guard Internal Review Test")
        print("=" * 50)
        print(f"Testing server at: {self.base_url}")
        print(f"Timestamp: {self.results['timestamp']}")
        print()
        
        # Test 1: Health endpoints
        print("1. Testing Health Endpoints...")
        self.test_endpoint("health_basic", "GET", "/health")
        self.test_endpoint("health_live", "GET", "/health/live")
        self.test_endpoint("health_ready", "GET", "/health/ready")
        self.test_endpoint("health_detailed", "GET", "/health/detailed")
        
        # Test 2: Metrics endpoints
        print("2. Testing Metrics Endpoints...")
        self.test_endpoint("metrics_prometheus", "GET", "/metrics")
        
        # Test 3: API Documentation
        print("3. Testing API Documentation...")
        self.test_endpoint("docs", "GET", "/docs")
        self.test_endpoint("openapi", "GET", "/openapi.json")
        
        # Test 4: Debug endpoints
        print("4. Testing Debug Endpoints...")
        self.test_endpoint("debug_api_key", "GET", "/debug/api-key")
        
        # Test 5: Authentication endpoints (these will fail without proper auth)
        print("5. Testing Authentication-Required Endpoints...")
        self.test_endpoint("detect_no_auth", "POST", "/v1/detect", 
                          data={"text": "Test text"}, expected_status=401)
        self.test_endpoint("validate_no_auth", "POST", "/v1/validate",
                          data={"input_text": "Test", "output_text": "Test"}, expected_status=401)
        
        # Test 6: Error handling
        print("6. Testing Error Handling...")
        self.test_endpoint("not_found", "GET", "/nonexistent", expected_status=404)
        
        self.generate_summary()
        self.print_results()
    
    def generate_summary(self):
        """Generate test summary."""
        total_tests = len(self.results["tests"])
        passed_tests = len([t for t in self.results["tests"].values() if t["status"] == "PASS"])
        failed_tests = len([t for t in self.results["tests"].values() if t["status"] == "FAIL"])
        error_tests = len([t for t in self.results["tests"].values() if t["status"] == "ERROR"])
        
        # Calculate average response time
        response_times = [t.get("response_time_ms", 0) for t in self.results["tests"].values() 
                         if t.get("response_time_ms", 0) > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "average_response_time_ms": round(avg_response_time, 2)
        }
    
    def print_results(self):
        """Print test results."""
        print("\n" + "=" * 50)
        print("TEST RESULTS SUMMARY")
        print("=" * 50)
        
        summary = self.results["summary"]
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Errors: {summary['errors']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Average Response Time: {summary['average_response_time_ms']}ms")
        
        print("\nDETAILED RESULTS:")
        print("-" * 50)
        
        for test_name, result in self.results["tests"].items():
            status_icon = "[PASS]" if result["status"] == "PASS" else "[FAIL]" if result["status"] == "FAIL" else "[ERROR]"
            print(f"{status_icon} {test_name}: {result['status']}")
            if result.get("response_time_ms", 0) > 0:
                print(f"   Response Time: {result['response_time_ms']}ms")
            if result.get("error"):
                print(f"   Error: {result['error']}")
            if result.get("status_code"):
                print(f"   Status Code: {result['status_code']}")
        
        # Production readiness assessment
        print("\n" + "=" * 50)
        print("PRODUCTION READINESS ASSESSMENT")
        print("=" * 50)
        
        health_working = all([
            self.results["tests"].get("health_basic", {}).get("status") == "PASS",
            self.results["tests"].get("health_live", {}).get("status") == "PASS",
            self.results["tests"].get("health_ready", {}).get("status") == "PASS"
        ])
        
        metrics_working = self.results["tests"].get("metrics_prometheus", {}).get("status") == "PASS"
        docs_working = self.results["tests"].get("docs", {}).get("status") == "PASS"
        
        response_time_ok = summary["average_response_time_ms"] < 1000  # Less than 1 second
        
        print(f"Health Monitoring: {'[READY]' if health_working else '[ISSUES]'}")
        print(f"Metrics Collection: {'[READY]' if metrics_working else '[ISSUES]'}")
        print(f"API Documentation: {'[READY]' if docs_working else '[ISSUES]'}")
        print(f"Response Performance: {'[READY]' if response_time_ok else '[SLOW]'}")
        
        # Overall assessment
        if health_working and metrics_working and docs_working and response_time_ok:
            print(f"\n[SUCCESS] OVERALL STATUS: READY FOR INTERNAL REVIEW")
            print("   All core infrastructure components are working properly.")
        elif health_working and metrics_working:
            print(f"\n[WARNING] OVERALL STATUS: MOSTLY READY")
            print("   Core infrastructure is working, but some issues need attention.")
        else:
            print(f"\n[ERROR] OVERALL STATUS: NOT READY")
            print("   Critical infrastructure issues need to be resolved.")
        
        # Save results to file
        with open("internal_review_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\nDetailed results saved to: internal_review_results.json")

def main():
    """Main test function."""
    tester = TrustGuardTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
