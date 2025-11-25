#!/usr/bin/env python3
"""
Test suite specifically for QUICK_REFERENCE.md request examples.
Validates that all documented request formats work correctly.
"""

import requests
import json
import sys
from typing import Dict, Any


class QuickReferenceEndpointTester:
    """Test all endpoint examples from QUICK_REFERENCE.md"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.results = []
    
    def test_endpoint(self, name: str, service_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Test an endpoint using the documented payload format."""
        url = f"{self.base_url}/api/v1/guards/process"
        
        request_data = {
            "service_type": service_type,
            "payload": payload,
            "user_id": "user-123",
            "session_id": "session-456"
        }
        
        try:
            response = self.session.post(url, json=request_data, timeout=30)
            response_data = response.json() if response.text else {}
            
            success = response.status_code == 200 and response_data.get("success", False)
            
            result = {
                "name": name,
                "service_type": service_type,
                "success": success,
                "status_code": response.status_code,
                "has_request_id": "request_id" in response_data,
                "error": response_data.get("error"),
                "processing_time": response_data.get("processing_time"),
                "service_used": response_data.get("service_used")
            }
            
            return result
            
        except Exception as e:
            return {
                "name": name,
                "service_type": service_type,
                "success": False,
                "error": str(e),
                "status_code": None
            }
    
    def run_all_tests(self):
        """Run all tests from QUICK_REFERENCE.md examples"""
        print("=" * 80)
        print("QUICK_REFERENCE.md ENDPOINT TESTING")
        print("=" * 80)
        print(f"Base URL: {self.base_url}\n")
        
        # Test TokenGuard (from QUICK_REFERENCE.md)
        print("[TEST] TokenGuard - QUICK_REFERENCE.md example")
        result = self.test_endpoint(
            name="TokenGuard",
            service_type="tokenguard",
            payload={
                "text": "Your content to optimize",
                "confidence": 0.7
            }
        )
        self.print_result(result)
        self.results.append(result)
        
        # Test TrustGuard (from QUICK_REFERENCE.md)
        print("\n[TEST] TrustGuard - QUICK_REFERENCE.md example")
        result = self.test_endpoint(
            name="TrustGuard",
            service_type="trustguard",
            payload={
                "text": "Content to validate",
                "trust_threshold": 0.8
            }
        )
        self.print_result(result)
        self.results.append(result)
        
        # Test ContextGuard (from QUICK_REFERENCE.md)
        print("\n[TEST] ContextGuard - QUICK_REFERENCE.md example")
        result = self.test_endpoint(
            name="ContextGuard",
            service_type="contextguard",
            payload={
                "text": "Current content",
                "context_window": 1024,
                "drift_threshold": 0.1
            }
        )
        self.print_result(result)
        self.results.append(result)
        
        # Test BiasGuard - Samples format (from QUICK_REFERENCE.md)
        print("\n[TEST] BiasGuard - QUICK_REFERENCE.md example (samples format)")
        result = self.test_endpoint(
            name="BiasGuard (samples)",
            service_type="biasguard",
            payload={
                "samples": [
                    {
                        "id": "sample_1",
                        "content": "Content to analyze",
                        "metadata": {}
                    }
                ]
            }
        )
        self.print_result(result)
        self.results.append(result)
        
        # Test BiasGuard - Alternative format (from QUICK_REFERENCE.md)
        print("\n[TEST] BiasGuard - QUICK_REFERENCE.md alternative format")
        result = self.test_endpoint(
            name="BiasGuard (text format)",
            service_type="biasguard",
            payload={
                "text": "Content to analyze",
                "metadata": {}
            }
        )
        self.print_result(result)
        self.results.append(result)
        
        # Test HealthGuard (from QUICK_REFERENCE.md)
        print("\n[TEST] HealthGuard - QUICK_REFERENCE.md example")
        result = self.test_endpoint(
            name="HealthGuard",
            service_type="healthguard",
            payload={
                "samples": [
                    {
                        "content": "Content to monitor",
                        "metadata": {}
                    }
                ]
            }
        )
        self.print_result(result)
        self.results.append(result)
        
        # Print summary
        self.print_summary()
        
        return self.results
    
    def print_result(self, result: Dict[str, Any]):
        """Print test result."""
        status = "[PASS]" if result["success"] else "[FAIL]"
        print(f"{status} {result['name']}")
        
        if result.get("status_code"):
            print(f"   Status Code: {result['status_code']}")
        
        if result.get("processing_time"):
            print(f"   Processing Time: {result['processing_time']:.3f}s")
        
        if result.get("service_used"):
            print(f"   Service Used: {result['service_used']}")
        
        if result.get("has_request_id"):
            print(f"   Request ID: Present")
        
        if result.get("error"):
            print(f"   Error: {result['error'][:150]}")
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["success"])
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"[PASS] Passed: {passed}")
        print(f"[FAIL] Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\nFAILED TESTS:")
            for result in self.results:
                if not result["success"]:
                    print(f"  [FAIL] {result['name']}: {result.get('error', 'Unknown error')[:100]}")
        
        print("=" * 80)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test QUICK_REFERENCE.md endpoint examples")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL for the gateway")
    
    args = parser.parse_args()
    
    tester = QuickReferenceEndpointTester(base_url=args.url)
    results = tester.run_all_tests()
    
    # Exit with error code if any tests failed
    failed_count = sum(1 for r in results if not r["success"])
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()

