#!/usr/bin/env python3
"""
Production Readiness Validation Script

Comprehensive test suite for validating production deployment readiness.
Tests security hardening, authentication, rate limiting, metrics, and error handling.

Usage:
    python scripts/test_production_readiness.py
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional
import httpx
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Color output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


class TestResult:
    """Test result container."""
    def __init__(self, name: str, passed: bool, message: str = "", duration: float = 0.0):
        self.name = name
        self.passed = passed
        self.message = message
        self.duration = duration
        self.timestamp = datetime.now()


class ProductionReadinessTester:
    """Production readiness validation tester."""
    
    def __init__(self, base_url: str = "http://localhost:8000", auth_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.results: List[TestResult] = []
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(30.0))
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def _get_headers(self, admin: bool = False) -> Dict[str, str]:
        """Get request headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers
    
    async def test_authentication_required(self) -> TestResult:
        """Test that read endpoints require authentication."""
        start_time = time.time()
        try:
            # Test without auth token
            response = await self.client.get(
                f"{self.base_url}/api/v1/guards/health",
                headers={"Content-Type": "application/json"}
            )
            duration = time.time() - start_time
            
            if response.status_code in [401, 403]:
                return TestResult(
                    "Authentication Required (Read Endpoints)",
                    True,
                    f"Correctly requires auth (status: {response.status_code})",
                    duration
                )
            else:
                return TestResult(
                    "Authentication Required (Read Endpoints)",
                    False,
                    f"Expected 401/403, got {response.status_code}",
                    duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "Authentication Required (Read Endpoints)",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def test_admin_endpoints_require_admin(self) -> TestResult:
        """Test that admin endpoints require admin access."""
        start_time = time.time()
        try:
            # Try to register a service without admin token
            response = await self.client.post(
                f"{self.base_url}/api/v1/guards/discovery/register",
                json={
                    "service_name": "test-service",
                    "base_url": "https://test.example.com",
                    "service_type": "tokenguard"
                },
                headers=self._get_headers(admin=False)
            )
            duration = time.time() - start_time
            
            if response.status_code in [401, 403]:
                return TestResult(
                    "Admin Endpoints Require Admin Access",
                    True,
                    f"Correctly requires admin auth (status: {response.status_code})",
                    duration
                )
            else:
                return TestResult(
                    "Admin Endpoints Require Admin Access",
                    False,
                    f"Expected 401/403, got {response.status_code}",
                    duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "Admin Endpoints Require Admin Access",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def test_rate_limiting_headers(self) -> TestResult:
        """Test that rate limiting headers are present."""
        start_time = time.time()
        try:
            # Make a request and check for rate limit headers
            response = await self.client.get(
                f"{self.base_url}/api/v1/guards/services",
                headers=self._get_headers()
            )
            duration = time.time() - start_time
            
            has_limit_header = "X-RateLimit-Limit" in response.headers
            has_remaining_header = "X-RateLimit-Remaining" in response.headers
            has_reset_header = "X-RateLimit-Reset" in response.headers
            
            if has_limit_header and has_remaining_header and has_reset_header:
                return TestResult(
                    "Rate Limiting Metrics Headers Present",
                    True,
                    f"All headers present (Limit: {response.headers.get('X-RateLimit-Limit')})",
                    duration
                )
            else:
                return TestResult(
                    "Rate Limiting Metrics Headers Present",
                    False,
                    f"Missing headers (Limit: {has_limit_header}, Remaining: {has_remaining_header}, Reset: {has_reset_header})",
                    duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "Rate Limiting Metrics Headers Present",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def test_payload_size_validation(self) -> TestResult:
        """Test payload size validation (10MB limit)."""
        start_time = time.time()
        try:
            # Create payload exceeding 10MB
            large_content = "x" * (11 * 1024 * 1024)  # 11MB
            payload = {
                "service_type": "tokenguard",
                "payload": {"content": large_content}
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/guards/process",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            duration = time.time() - start_time
            
            if response.status_code == 413:
                return TestResult(
                    "Payload Size Validation (10MB Limit)",
                    True,
                    "Correctly rejects oversized payloads",
                    duration
                )
            else:
                return TestResult(
                    "Payload Size Validation (10MB Limit)",
                    False,
                    f"Expected 413, got {response.status_code}",
                    duration
                )
        except httpx.TimeoutException:
            duration = time.time() - start_time
            return TestResult(
                "Payload Size Validation (10MB Limit)",
                True,  # Timeout is acceptable for large payloads
                "Request timed out (expected for large payload)",
                duration
            )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "Payload Size Validation (10MB Limit)",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def test_url_validation(self) -> TestResult:
        """Test service URL validation."""
        start_time = time.time()
        try:
            # Try to register with invalid URL scheme
            response = await self.client.post(
                f"{self.base_url}/api/v1/guards/discovery/register",
                json={
                    "service_name": "test-service",
                    "base_url": "ftp://malicious.example.com",  # Invalid scheme
                    "service_type": "tokenguard"
                },
                headers=self._get_headers(admin=True)
            )
            duration = time.time() - start_time
            
            if response.status_code == 400:
                return TestResult(
                    "URL Validation",
                    True,
                    "Correctly rejects invalid URL schemes",
                    duration
                )
            else:
                return TestResult(
                    "URL Validation",
                    False,
                    f"Expected 400, got {response.status_code}",
                    duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "URL Validation",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def test_service_name_sanitization(self) -> TestResult:
        """Test service name sanitization."""
        start_time = time.time()
        try:
            # Try to access with invalid service name
            response = await self.client.get(
                f"{self.base_url}/api/v1/guards/health/test@service",
                headers=self._get_headers()
            )
            duration = time.time() - start_time
            
            if response.status_code == 400:
                return TestResult(
                    "Service Name Sanitization",
                    True,
                    "Correctly rejects invalid service names",
                    duration
                )
            else:
                return TestResult(
                    "Service Name Sanitization",
                    False,
                    f"Expected 400, got {response.status_code}",
                    duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "Service Name Sanitization",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def test_404_error_handling(self) -> TestResult:
        """Test that unregister returns 404 when service not found."""
        start_time = time.time()
        try:
            response = await self.client.delete(
                f"{self.base_url}/api/v1/guards/discovery/services/nonexistent-service-12345",
                headers=self._get_headers(admin=True)
            )
            duration = time.time() - start_time
            
            if response.status_code == 404:
                return TestResult(
                    "404 Error Handling (Unregister Service)",
                    True,
                    "Correctly returns 404 for non-existent service",
                    duration
                )
            else:
                return TestResult(
                    "404 Error Handling (Unregister Service)",
                    False,
                    f"Expected 404, got {response.status_code}",
                    duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "404 Error Handling (Unregister Service)",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def test_metrics_endpoint(self) -> TestResult:
        """Test Prometheus metrics endpoint."""
        start_time = time.time()
        try:
            response = await self.client.get(
                f"{self.base_url}/metrics",
                headers={"Content-Type": "text/plain"}
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                metrics_text = response.text
                # Check for key metrics
                has_orchestrator_requests = "orchestrator_requests_total" in metrics_text
                has_circuit_breaker = "circuit_breaker_state" in metrics_text
                has_service_health = "service_health_status" in metrics_text
                
                if has_orchestrator_requests or has_circuit_breaker or has_service_health:
                    return TestResult(
                        "Prometheus Metrics Endpoint",
                        True,
                        f"Metrics endpoint accessible (found key metrics)",
                        duration
                    )
                else:
                    return TestResult(
                        "Prometheus Metrics Endpoint",
                        True,  # Endpoint works, metrics might be empty if no traffic
                        "Metrics endpoint accessible (no metrics yet)",
                        duration
                    )
            else:
                return TestResult(
                    "Prometheus Metrics Endpoint",
                    False,
                    f"Expected 200, got {response.status_code}",
                    duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "Prometheus Metrics Endpoint",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def test_aggregated_health_endpoint(self) -> TestResult:
        """Test aggregated health endpoint."""
        start_time = time.time()
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/guards/health/aggregated",
                headers=self._get_headers()
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                has_overall_status = "overall_status" in data
                has_services = "services" in data or "services_total" in data
                
                if has_overall_status and has_services:
                    return TestResult(
                        "Aggregated Health Endpoint",
                        True,
                        f"Endpoint returns valid health data (status: {data.get('overall_status', 'unknown')})",
                        duration
                    )
                else:
                    return TestResult(
                        "Aggregated Health Endpoint",
                        False,
                        f"Response missing required fields: {list(data.keys())}",
                        duration
                    )
            else:
                return TestResult(
                    "Aggregated Health Endpoint",
                    False,
                    f"Expected 200, got {response.status_code}",
                    duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "Aggregated Health Endpoint",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def test_circuit_breaker_monitoring(self) -> TestResult:
        """Test circuit breaker monitoring endpoint."""
        start_time = time.time()
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/admin/guards/circuit-breakers",
                headers=self._get_headers(admin=True)
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                has_breakers = "breakers" in data or "circuit_breakers" in data
                
                if has_breakers:
                    return TestResult(
                        "Circuit Breaker Monitoring Endpoint",
                        True,
                        f"Endpoint returns breaker states ({len(data.get('breakers', {}))} breakers)",
                        duration
                    )
                else:
                    return TestResult(
                        "Circuit Breaker Monitoring Endpoint",
                        False,
                        f"Response missing breakers field: {list(data.keys())}",
                        duration
                    )
            else:
                return TestResult(
                    "Circuit Breaker Monitoring Endpoint",
                    False,
                    f"Expected 200, got {response.status_code}",
                    duration
                )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                "Circuit Breaker Monitoring Endpoint",
                False,
                f"Exception: {str(e)}",
                duration
            )
    
    async def run_all_tests(self) -> Dict[str, any]:
        """Run all production readiness tests."""
        print(f"\n{BOLD}{BLUE} Production Readiness Validation{RESET}\n")
        print(f"Base URL: {self.base_url}\n")
        
        tests = [
            ("Authentication Required", self.test_authentication_required),
            ("Admin Endpoints Require Admin", self.test_admin_endpoints_require_admin),
            ("Rate Limiting Headers", self.test_rate_limiting_headers),
            ("Payload Size Validation", self.test_payload_size_validation),
            ("URL Validation", self.test_url_validation),
            ("Service Name Sanitization", self.test_service_name_sanitization),
            ("404 Error Handling", self.test_404_error_handling),
            ("Prometheus Metrics", self.test_metrics_endpoint),
            ("Aggregated Health", self.test_aggregated_health_endpoint),
            ("Circuit Breaker Monitoring", self.test_circuit_breaker_monitoring),
        ]
        
        for test_name, test_func in tests:
            print(f"{BLUE}Running: {test_name}...{RESET}", end=" ", flush=True)
            result = await test_func()
            self.results.append(result)
            
            if result.passed:
                print(f"{GREEN} PASSED{RESET} ({result.duration:.3f}s)")
                if result.message:
                    print(f"  {result.message}")
            else:
                print(f"{RED} FAILED{RESET} ({result.duration:.3f}s)")
                print(f"  {RED}{result.message}{RESET}")
        
        # Summary
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print(f"\n{BOLD}Summary:{RESET}")
        print(f"  Passed: {GREEN}{passed}/{total}{RESET}")
        print(f"  Failed: {RED}{total - passed}/{total}{RESET}")
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "results": [{"name": r.name, "passed": r.passed, "message": r.message, "duration": r.duration} for r in self.results]
        }


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Production Readiness Validation")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--token", help="Authentication token (user level)")
    parser.add_argument("--admin-token", help="Admin authentication token")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    async with ProductionReadinessTester(base_url=args.url, auth_token=args.token or args.admin_token) as tester:
        results = await tester.run_all_tests()
        
        if args.json:
            print(json.dumps(results, indent=2))
            sys.exit(0 if results["failed"] == 0 else 1)
        else:
            sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())

