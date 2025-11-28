#!/usr/bin/env python3
"""
Comprehensive endpoint testing suite for AIGuardian API
Tests all endpoints to ensure functionality across domains:
- api.aiguardian.ai (API endpoints)
- aiguardian.ai (main website)
- dashboard.aiguardian.ai (dashboard)
"""

import requests
import json
import time
from typing import Dict, Any, List
from dataclasses import dataclass
import sys


@dataclass
class TestResult:
    """Test result data class"""
    endpoint: str
    method: str
    status_code: int
    success: bool
    response_time: float
    error: str = None
    response_data: Dict[str, Any] = None


class EndpointTester:
    """Comprehensive endpoint testing class"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[TestResult] = []

    def test_endpoint(
        self,
        endpoint: str,
        method: str = "GET",
        data: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        expected_status: int = 200
    ) -> TestResult:
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"

        if headers is None:
            headers = {"Content-Type": "application/json"}

        start_time = time.time()

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response_time = time.time() - start_time

            # Try to parse JSON response
            try:
                response_data = response.json()
            except:
                response_data = {"raw": response.text}

            success = response.status_code == expected_status

            result = TestResult(
                endpoint=endpoint,
                method=method,
                status_code=response.status_code,
                success=success,
                response_time=response_time,
                response_data=response_data
            )

        except Exception as e:
            response_time = time.time() - start_time
            result = TestResult(
                endpoint=endpoint,
                method=method,
                status_code=0,
                success=False,
                response_time=response_time,
                error=str(e)
            )

        self.results.append(result)
        return result

    def run_health_checks(self):
        """Test all health check endpoints"""
        print("\n Testing Health Check Endpoints...")
        print("=" * 80)

        endpoints = [
            ("/health/live", "GET", 200),
            ("/health/ready", "GET", 200),
            ("/health/comprehensive", "GET", 200),
            ("/health/circuit-breakers", "GET", 200),
            ("/health/configuration", "GET", 200),
        ]

        for endpoint, method, expected_status in endpoints:
            result = self.test_endpoint(endpoint, method, expected_status=expected_status)
            self.print_result(result)

    def run_guard_service_tests(self):
        """Test all guard service endpoints"""
        print("\n Testing Guard Service Endpoints...")
        print("=" * 80)

        # Test unified guard process endpoint
        guard_request = {
            "service_type": "tokenguard",
            "payload": {
                "text": "This is a test message for token optimization",
                "max_tokens": 100
            },
            "user_id": "test-user-123",
            "session_id": "test-session-456",
            "priority": 1,
            "timeout": 30,
            "fallback_enabled": True
        }

        result = self.test_endpoint(
            "/api/v1/guards/process",
            "POST",
            data=guard_request,
            expected_status=200
        )
        self.print_result(result)

        # Test individual guard endpoints
        guard_tests = [
            ("/api/v1/guards/tokenguard/optimize", {
                "text": "Test text for token optimization",
                "max_tokens": 100
            }),
            ("/api/v1/guards/trustguard/validate", {
                "content": "Test content for trust validation"
            }),
            ("/api/v1/guards/contextguard/analyze", {
                "context": "Test context for analysis",
                "conversation_history": []
            }),
            ("/api/v1/guards/biasguard/detect", {
                "text": "Test text for bias detection"
            })
        ]

        for endpoint, payload in guard_tests:
            result = self.test_endpoint(endpoint, "POST", data=payload, expected_status=200)
            self.print_result(result)

    def run_guard_health_tests(self):
        """Test guard service health endpoints"""
        print("\n Testing Guard Service Health Endpoints...")
        print("=" * 80)

        # Test all guards health
        result = self.test_endpoint("/api/v1/guards/health", "GET", expected_status=200)
        self.print_result(result)

        # Test individual guard health
        guard_services = [
            "tokenguard",
            "trustguard",
            "contextguard",
            "biasguard",
            "securityguard"
        ]

        for service in guard_services:
            result = self.test_endpoint(
                f"/api/v1/guards/health/{service}",
                "GET",
                expected_status=200
            )
            self.print_result(result)

    def run_discovery_tests(self):
        """Test service discovery endpoints"""
        print("\n Testing Service Discovery Endpoints...")
        print("=" * 80)

        # Test service listing
        result = self.test_endpoint("/api/v1/guards/services", "GET", expected_status=200)
        self.print_result(result)

        # Test discovery info
        result = self.test_endpoint("/api/v1/guards/discovery/services", "GET", expected_status=200)
        self.print_result(result)

    def run_metrics_tests(self):
        """Test metrics endpoint"""
        print("\n Testing Metrics Endpoint...")
        print("=" * 80)

        result = self.test_endpoint("/metrics", "GET", expected_status=200)
        self.print_result(result)

    def run_cors_tests(self):
        """Test CORS configuration"""
        print("\n Testing CORS Configuration...")
        print("=" * 80)

        origins = [
            "https://aiguardian.ai",
            "https://api.aiguardian.ai",
            "https://dashboard.aiguardian.ai"
        ]

        for origin in origins:
            headers = {
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }

            # OPTIONS request for CORS preflight
            try:
                response = requests.options(
                    f"{self.base_url}/api/v1/guards/process",
                    headers=headers,
                    timeout=10
                )

                print(f"\n   Origin: {origin}")
                print(f"   Status: {response.status_code}")
                print(f"   CORS Headers: {dict(response.headers)}")

            except Exception as e:
                print(f"\n   Origin: {origin}")
                print(f"   Error: {str(e)}")

    def run_all_tests(self):
        """Run all test suites"""
        print("\n" + "=" * 80)
        print(" AIGuardian Endpoint Testing Suite")
        print("=" * 80)
        print(f"Base URL: {self.base_url}")
        print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Run all test suites
        self.run_health_checks()
        self.run_guard_service_tests()
        self.run_guard_health_tests()
        self.run_discovery_tests()
        self.run_metrics_tests()
        self.run_cors_tests()

        # Print summary
        self.print_summary()

    def print_result(self, result: TestResult):
        """Print test result"""
        status_icon = "" if result.success else ""
        print(f"\n{status_icon} {result.method} {result.endpoint}")
        print(f"   Status: {result.status_code}")
        print(f"   Response Time: {result.response_time:.3f}s")

        if result.error:
            print(f"   Error: {result.error}")

        if result.response_data and result.success:
            print(f"   Response: {json.dumps(result.response_data, indent=2)[:200]}...")

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print(" Test Summary")
        print("=" * 80)

        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests

        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests} ")
        print(f"Failed: {failed_tests} ")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")

        if failed_tests > 0:
            print("\n Failed Tests:")
            for result in self.results:
                if not result.success:
                    print(f"   - {result.method} {result.endpoint}")
                    if result.error:
                        print(f"     Error: {result.error}")

        # Average response time
        avg_response_time = sum(r.response_time for r in self.results) / total_tests
        print(f"\nAverage Response Time: {avg_response_time:.3f}s")

        print("\n" + "=" * 80)

        # Exit with error code if tests failed
        if failed_tests > 0:
            sys.exit(1)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="AIGuardian Endpoint Testing Suite")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--suite",
        choices=["all", "health", "guards", "discovery", "metrics", "cors"],
        default="all",
        help="Test suite to run (default: all)"
    )

    args = parser.parse_args()

    tester = EndpointTester(base_url=args.base_url)

    if args.suite == "all":
        tester.run_all_tests()
    elif args.suite == "health":
        tester.run_health_checks()
    elif args.suite == "guards":
        tester.run_guard_service_tests()
    elif args.suite == "discovery":
        tester.run_discovery_tests()
    elif args.suite == "metrics":
        tester.run_metrics_tests()
    elif args.suite == "cors":
        tester.run_cors_tests()


if __name__ == "__main__":
    main()
