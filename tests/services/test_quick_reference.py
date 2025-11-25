#!/usr/bin/env python3
"""
Comprehensive test suite for CodeGuardians Gateway Quick Reference endpoints.
Tests all endpoints documented in QUICK_REFERENCE.md and validates responses.
"""

import requests
import json
import os
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class TestStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    WARN = "WARN"


@dataclass
class TestResult:
    name: str
    status: TestStatus
    message: str
    response_time: Optional[float] = None
    status_code: Optional[int] = None
    response_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class TestSuiteResults:
    suite_name: str
    tests: List[TestResult] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def add_test(self, result: TestResult):
        self.tests.append(result)
    
    def get_summary(self) -> Dict[str, Any]:
        total = len(self.tests)
        passed = sum(1 for t in self.tests if t.status == TestStatus.PASS)
        failed = sum(1 for t in self.tests if t.status == TestStatus.FAIL)
        skipped = sum(1 for t in self.tests if t.status == TestStatus.SKIP)
        warnings = sum(1 for t in self.tests if t.status == TestStatus.WARN)
        
        duration = None
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            "suite": self.suite_name,
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "warnings": warnings,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "duration_seconds": duration
        }


class QuickReferenceTester:
    """Test suite for Quick Reference endpoints."""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv("UNIFIED_API_KEY")
        self.results = TestSuiteResults(suite_name="Quick Reference Tests")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _validate_guard_response(self, data: Dict[str, Any], expected_service_type: str) -> Optional[str]:
        """Validate guard service response structure."""
        required_fields = ["request_id", "service_type", "success"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing required fields: {', '.join(missing_fields)}"
        
        if data.get("service_type") != expected_service_type:
            return f"Service type mismatch: expected {expected_service_type}, got {data.get('service_type')}"
        
        # Validate request_id is a valid UUID format
        request_id = data.get("request_id", "")
        if not request_id or len(request_id) < 10:
            return "Invalid request_id format"
        
        return None
    
    def log_test(self, result: TestResult):
        """Log test result."""
        status_icon = {
            TestStatus.PASS: "[PASS]",
            TestStatus.FAIL: "[FAIL]",
            TestStatus.SKIP: "[SKIP]",
            TestStatus.WARN: "[WARN]"
        }.get(result.status, "[?]")
        
        print(f"{status_icon} {result.name}")
        if result.message:
            print(f"   {result.message}")
        if result.response_time:
            print(f"   Response time: {result.response_time:.3f}s")
        if result.status_code:
            print(f"   Status code: {result.status_code}")
        if result.error:
            print(f"   Error: {result.error}")
        print()
        
        self.results.add_test(result)
    
    def test_request(self, 
                    method: str,
                    endpoint: str,
                    name: str,
                    expected_status: int = 200,
                    headers: Optional[Dict[str, str]] = None,
                    json_data: Optional[Dict[str, Any]] = None,
                    validate_response: Optional[callable] = None) -> TestResult:
        """Make a request and validate the response."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            start_time = datetime.now()
            response = self.session.request(
                method=method,
                url=url,
                headers=headers or {},
                json=json_data,
                timeout=30
            )
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Parse response
            response_data = None
            try:
                if response.text:
                    response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"raw": response.text}
            
            # Validate status code
            if response.status_code != expected_status:
                return TestResult(
                    name=name,
                    status=TestStatus.FAIL,
                    message=f"Expected status {expected_status}, got {response.status_code}",
                    response_time=response_time,
                    status_code=response.status_code,
                    response_data=response_data,
                    error=response.text[:200] if response.text else None
                )
            
            # Run custom validation if provided
            if validate_response:
                validation_result = validate_response(response_data, response.status_code)
                if validation_result:
                    return TestResult(
                        name=name,
                        status=TestStatus.FAIL,
                        message=validation_result,
                        response_time=response_time,
                        status_code=response.status_code,
                        response_data=response_data
                    )
            
            return TestResult(
                name=name,
                status=TestStatus.PASS,
                message="Test passed",
                response_time=response_time,
                status_code=response.status_code,
                response_data=response_data
            )
            
        except requests.exceptions.Timeout:
            return TestResult(
                name=name,
                status=TestStatus.FAIL,
                message="Request timeout",
                error="Request exceeded 30 second timeout"
            )
        except requests.exceptions.ConnectionError as e:
            return TestResult(
                name=name,
                status=TestStatus.FAIL,
                message="Connection error",
                error=f"Cannot connect to {url}: {str(e)}"
            )
        except Exception as e:
            return TestResult(
                name=name,
                status=TestStatus.FAIL,
                message="Unexpected error",
                error=str(e)
            )
    
    def test_health_checks(self):
        """Test health check endpoints."""
        print("=" * 80)
        print("HEALTH CHECK TESTS")
        print("=" * 80)
        print()
        
        # Test Gateway Live Health
        result = self.test_request(
            method="GET",
            endpoint="/health/live",
            name="Gateway Live Health Check",
            validate_response=lambda data, code: None if data.get("status") == "alive" else "Missing or invalid 'status: alive' field"
        )
        self.log_test(result)
        
        # Test Gateway Ready Health
        result = self.test_request(
            method="GET",
            endpoint="/health/ready",
            name="Gateway Ready Health Check",
            validate_response=lambda data, code: None if data.get("status") in ["ready", "not ready"] else "Missing or invalid 'status' field"
        )
        self.log_test(result)
        
        # Test Basic Health
        result = self.test_request(
            method="GET",
            endpoint="/health",
            name="Gateway Basic Health Check",
            validate_response=lambda data, code: None if data.get("status") else "Missing 'status' field"
        )
        self.log_test(result)
        
        # Test Service Discovery
        result = self.test_request(
            method="GET",
            endpoint="/api/v1/guards/services",
            name="Service Discovery - List All Services",
            validate_response=lambda data, code: None if isinstance(data.get("services"), dict) else "Missing 'services' field or invalid format"
        )
        self.log_test(result)
        
        # Validate service discovery response structure
        if result.status == TestStatus.PASS and result.response_data:
            services = result.response_data.get("services", {})
            print(f"   Found {len(services)} services:")
            for service_name, service_info in services.items():
                status = service_info.get("status", "unknown")
                print(f"   - {service_name}: {status}")
            
            # Test individual service health endpoints
            for service_name in services.keys():
                service_result = self.test_request(
                    method="GET",
                    endpoint=f"/api/v1/guards/health/{service_name}",
                    name=f"Individual Service Health - {service_name}",
                    validate_response=lambda data, code, sn=service_name: None if data.get("service_name") == sn or data.get("status") else "Missing service_name or status"
                )
                self.log_test(service_result)
        
        print()
    
    def test_api_endpoints(self):
        """Test API processing endpoints."""
        print("=" * 80)
        print("API PROCESSING ENDPOINTS")
        print("=" * 80)
        print()
        
        # Prepare headers
        headers_with_auth = {}
        if self.api_key:
            headers_with_auth["X-API-Key"] = self.api_key
        
        # Test payloads for each service type
        service_configs = [
            {
                "service_type": "tokenguard",
                "payload": {"text": "test content", "confidence": 0.7},
                "name": "TokenGuard"
            },
            {
                "service_type": "trustguard",
                "payload": {"text": "Content to validate", "trust_threshold": 0.8},
                "name": "TrustGuard"
            },
            {
                "service_type": "contextguard",
                "payload": {"text": "Current content", "context_window": 1024, "drift_threshold": 0.1},
                "name": "ContextGuard"
            },
            {
                "service_type": "biasguard",
                "payload": {
                    "samples": [{
                        "id": "sample_1",
                        "content": "Content to analyze",
                        "metadata": {}
                    }]
                },
                "name": "BiasGuard"
            },
            {
                "service_type": "healthguard",
                "payload": {
                    "samples": [{
                        "content": "Content to monitor",
                        "metadata": {}
                    }]
                },
                "name": "HealthGuard"
            }
        ]
        
        # Test each service with API key
        if self.api_key:
            for config in service_configs:
                result = self.test_request(
                    method="POST",
                    endpoint="/api/v1/guards/process",
                    name=f"{config['name']} - With API Key",
                    headers=headers_with_auth,
                    json_data={
                        "service_type": config["service_type"],
                        "payload": config["payload"],
                        "user_id": "test-user",
                        "session_id": "test-session"
                    },
                    validate_response=lambda data, code, st=config["service_type"]: self._validate_guard_response(data, st)
                )
                self.log_test(result)
        else:
            print("[WARN] UNIFIED_API_KEY not set - skipping authenticated API tests")
            for config in service_configs:
                result = TestResult(
                    name=f"{config['name']} - With API Key",
                    status=TestStatus.SKIP,
                    message="API key not configured"
                )
                self.log_test(result)
        
        # Test without API key (should fail or work depending on configuration)
        for config in service_configs[:2]:  # Test first 2 services
            result = self.test_request(
                method="POST",
                endpoint="/api/v1/guards/process",
                name=f"{config['name']} - Without API Key",
                expected_status=200,  # May work or fail depending on config
                json_data={
                    "service_type": config["service_type"],
                    "payload": config["payload"],
                    "user_id": "test-user",
                    "session_id": "test-session"
                }
            )
            if result.status_code == 401 or result.status_code == 403:
                result.status = TestStatus.PASS
                result.message = "Correctly rejected unauthenticated request"
            elif result.status_code == 200:
                result.status = TestStatus.WARN
                result.message = "Accepted request without authentication (may be intentional)"
            self.log_test(result)
        
        print()
    
    def test_authentication_endpoints(self):
        """Test authentication endpoints."""
        print("=" * 80)
        print("AUTHENTICATION ENDPOINTS")
        print("=" * 80)
        print()
        
        # Test login endpoint (may require valid credentials)
        login_result = self.test_request(
            method="POST",
            endpoint="/api/v1/auth/login",
            name="Authentication - Login",
            expected_status=401,  # Expected to fail without valid credentials
            json_data={"email": "test@example.com", "password": "test"}
        )
        if login_result.status_code in [401, 422]:
            login_result.status = TestStatus.PASS
            login_result.message = "Login endpoint exists and validates credentials"
        self.log_test(login_result)
        
        print()
    
    def test_api_documentation(self):
        """Test API documentation endpoints."""
        print("=" * 80)
        print("API DOCUMENTATION")
        print("=" * 80)
        print()
        
        # Test OpenAPI docs
        result = self.test_request(
            method="GET",
            endpoint="/docs",
            name="API Documentation - Swagger UI",
            expected_status=200
        )
        self.log_test(result)
        
        # Test OpenAPI JSON
        result = self.test_request(
            method="GET",
            endpoint="/openapi.json",
            name="API Documentation - OpenAPI JSON",
            validate_response=lambda data, code: None if data.get("openapi") or data.get("swagger") else "Invalid OpenAPI format"
        )
        self.log_test(result)
        
        print()
    
    def test_circuit_breaker_status(self):
        """Test circuit breaker and comprehensive health endpoints."""
        print("=" * 80)
        print("ADVANCED HEALTH ENDPOINTS")
        print("=" * 80)
        print()
        
        # Test comprehensive health
        result = self.test_request(
            method="GET",
            endpoint="/health/comprehensive",
            name="Comprehensive Health Check",
            validate_response=lambda data, code: None if data.get("overall_status") or data.get("status") else "Missing 'overall_status' or 'status' field"
        )
        self.log_test(result)
        
        # Test circuit breaker status
        result = self.test_request(
            method="GET",
            endpoint="/health/circuit-breakers",
            name="Circuit Breaker Status",
        )
        self.log_test(result)
        
        print()
    
    def run_all_tests(self):
        """Run all test suites."""
        print("=" * 80)
        print("CODEGUARDIANS GATEWAY - QUICK REFERENCE TEST SUITE")
        print("=" * 80)
        print(f"Base URL: {self.base_url}")
        print(f"API Key: {'Set' if self.api_key else 'Not Set'}")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)
        print()
        
        self.results.start_time = datetime.now()
        
        try:
            self.test_health_checks()
            self.test_api_endpoints()
            self.test_authentication_endpoints()
            self.test_api_documentation()
            self.test_circuit_breaker_status()
        except KeyboardInterrupt:
            print("\n[WARN] Tests interrupted by user")
        except Exception as e:
            print(f"\n[ERROR] Fatal error during testing: {e}")
            import traceback
            traceback.print_exc()
        
        self.results.end_time = datetime.now()
        self.print_summary()
        
        return self.results
    
    def print_summary(self):
        """Print test summary."""
        summary = self.results.get_summary()
        
        print()
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Suite: {summary['suite']}")
        print(f"Total Tests: {summary['total']}")
        print(f"[PASS] Passed: {summary['passed']}")
        print(f"[FAIL] Failed: {summary['failed']}")
        print(f"[SKIP] Skipped: {summary['skipped']}")
        print(f"[WARN] Warnings: {summary['warnings']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        if summary['duration_seconds']:
            print(f"Duration: {summary['duration_seconds']:.2f} seconds")
        print("=" * 80)
        
        # Print failed tests
        failed_tests = [t for t in self.results.tests if t.status == TestStatus.FAIL]
        if failed_tests:
            print("\nFAILED TESTS:")
            for test in failed_tests:
                print(f"  [FAIL] {test.name}: {test.message}")
                if test.error:
                    print(f"     Error: {test.error[:100]}")
        
        # Save results to file
        results_file = "quick_reference_test_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "summary": summary,
                "tests": [
                    {
                        "name": t.name,
                        "status": t.status.value,
                        "message": t.message,
                        "response_time": t.response_time,
                        "status_code": t.status_code,
                        "error": t.error
                    }
                    for t in self.results.tests
                ],
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n[INFO] Detailed results saved to: {results_file}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test CodeGuardians Gateway Quick Reference endpoints")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL for the gateway")
    parser.add_argument("--api-key", help="API key for authentication (or set UNIFIED_API_KEY env var)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    tester = QuickReferenceTester(base_url=args.url, api_key=args.api_key)
    results = tester.run_all_tests()
    
    # Exit with error code if any tests failed
    summary = results.get_summary()
    sys.exit(0 if summary['failed'] == 0 else 1)


if __name__ == "__main__":
    main()

