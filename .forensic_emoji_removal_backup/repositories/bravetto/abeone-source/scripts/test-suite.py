#!/usr/bin/env python3
"""
AIGuards Backend - Consolidated Test Suite
Runs comprehensive tests for all system components

Usage:
    python scripts/test-suite.py              # Run all tests
    python scripts/test-suite.py --quick      # Run quick tests only
    python scripts/test-suite.py --guards     # Test guard services only
    python scripts/test-suite.py --infra      # Test infrastructure only
    python scripts/test-suite.py --e2e        # Run end-to-end tests
"""

import asyncio
import argparse
import sys
import time
from typing import Dict, Any, List
import httpx
import requests

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

BASE_URL = "http://localhost:8000"


class TestRunner:
    """Consolidated test runner for AIGuards Backend."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "tests": []
        }
    
    def print_header(self, title: str):
        """Print a formatted header."""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}{title.center(60)}{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")
    
    def print_result(self, test_name: str, passed: bool, details: str = "", duration: float = 0):
        """Print test result."""
        status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
        duration_str = f" ({duration:.3f}s)" if duration > 0 else ""
        print(f"{status} {test_name}{duration_str}")
        if details:
            print(f"  {details}")
        
        self.results["tests"].append({
            "name": test_name,
            "passed": passed,
            "details": details,
            "duration": duration
        })
        
        if passed:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
    
    async def test_gateway_health(self):
        """Test gateway health endpoint."""
        self.print_header("Gateway Health Tests")
        
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/health/live")
                duration = time.time() - start
                
                if response.status_code == 200:
                    data = response.json()
                    self.print_result(
                        "Gateway Live Check",
                        True,
                        f"Status: {data.get('status')}",
                        duration
                    )
                else:
                    self.print_result(
                        "Gateway Live Check",
                        False,
                        f"HTTP {response.status_code}",
                        duration
                    )
        except Exception as e:
            duration = time.time() - start
            self.print_result("Gateway Live Check", False, str(e), duration)
    
    async def test_service_discovery(self):
        """Test service discovery."""
        self.print_header("Service Discovery Tests")
        
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/v1/guards/services")
                duration = time.time() - start
                
                if response.status_code == 200:
                    data = response.json()
                    services = data.get('services', [])
                    self.print_result(
                        "Service Discovery",
                        True,
                        f"Found {len(services)} services",
                        duration
                    )
                else:
                    self.print_result(
                        "Service Discovery",
                        False,
                        f"HTTP {response.status_code}",
                        duration
                    )
        except Exception as e:
            duration = time.time() - start
            self.print_result("Service Discovery", False, str(e), duration)
    
    async def test_guard_services(self):
        """Test all guard services."""
        self.print_header("Guard Services Tests")
        
        test_cases = [
            {
                "name": "TokenGuard",
                "service_type": "tokenguard",
                "payload": {
                    "text": "This is a test message for token optimization and compression.",
                    "context": "test"
                }
            },
            {
                "name": "TrustGuard",
                "service_type": "trustguard",
                "payload": {
                    "text": "This is a safe message with no violations.",
                    "context": "test"
                }
            },
            {
                "name": "ContextGuard",
                "service_type": "contextguard",
                "payload": {
                    "text": "This is a test message for context analysis.",
                    "context": "test conversation"
                }
            },
            {
                "name": "BiasGuard",
                "service_type": "biasguard",
                "payload": {
                    "text": "This is a test message for bias detection.",
                    "bias_types": ["gender", "age"]
                }
            },
            {
                "name": "HealthGuard",
                "service_type": "healthguard",
                "payload": {
                    "metrics": {
                        "cpu_usage": 45.0,
                        "memory_usage": 60.0,
                        "response_time": 150
                    }
                }
            }
        ]
        
        for test_case in test_cases:
            start = time.time()
            try:
                request_data = {
                    "service_type": test_case["service_type"],
                    "payload": test_case["payload"],
                    "user_id": "test-user",
                    "client_type": "api"
                }
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.base_url}/api/v1/guards/process",
                        json=request_data
                    )
                    duration = time.time() - start
                    
                    if response.status_code == 200:
                        data = response.json()
                        self.print_result(
                            f"{test_case['name']} Processing",
                            True,
                            f"Processing time: {data.get('processing_time_ms', 0)}ms",
                            duration
                        )
                    else:
                        self.print_result(
                            f"{test_case['name']} Processing",
                            False,
                            f"HTTP {response.status_code}",
                            duration
                        )
            except Exception as e:
                duration = time.time() - start
                self.print_result(
                    f"{test_case['name']} Processing",
                    False,
                    str(e),
                    duration
                )
    
    async def test_infrastructure(self):
        """Test infrastructure components."""
        self.print_header("Infrastructure Tests")
        
        # Test database connection
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/health/ready")
                duration = time.time() - start
                
                if response.status_code == 200:
                    self.print_result(
                        "Infrastructure Ready",
                        True,
                        "All dependencies available",
                        duration
                    )
                else:
                    self.print_result(
                        "Infrastructure Ready",
                        False,
                        f"HTTP {response.status_code}",
                        duration
                    )
        except Exception as e:
            duration = time.time() - start
            self.print_result("Infrastructure Ready", False, str(e), duration)
    
    async def run_quick_tests(self):
        """Run quick smoke tests."""
        print(f"\n{YELLOW}Running Quick Tests...{RESET}")
        await self.test_gateway_health()
        await self.test_service_discovery()
    
    async def run_guard_tests(self):
        """Run guard service tests."""
        print(f"\n{YELLOW}Running Guard Tests...{RESET}")
        await self.test_guard_services()
    
    async def run_infra_tests(self):
        """Run infrastructure tests."""
        print(f"\n{YELLOW}Running Infrastructure Tests...{RESET}")
        await self.test_infrastructure()
    
    async def run_all_tests(self):
        """Run all tests."""
        print(f"\n{YELLOW}Running All Tests...{RESET}")
        await self.test_gateway_health()
        await self.test_service_discovery()
        await self.test_guard_services()
        await self.test_infrastructure()
    
    def print_summary(self):
        """Print test summary."""
        self.print_header("Test Summary")
        
        total = self.results["passed"] + self.results["failed"]
        pass_rate = (self.results["passed"] / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"{GREEN}Passed: {self.results['passed']}{RESET}")
        print(f"{RED}Failed: {self.results['failed']}{RESET}")
        print(f"Pass Rate: {pass_rate:.1f}%\n")
        
        if self.results["failed"] > 0:
            print(f"{RED}Failed Tests:{RESET}")
            for test in self.results["tests"]:
                if not test["passed"]:
                    print(f"  - {test['name']}: {test['details']}")
        
        return self.results["failed"] == 0


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AIGuards Backend Test Suite")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick smoke tests only"
    )
    parser.add_argument(
        "--guards",
        action="store_true",
        help="Test guard services only"
    )
    parser.add_argument(
        "--infra",
        action="store_true",
        help="Test infrastructure only"
    )
    parser.add_argument(
        "--e2e",
        action="store_true",
        help="Run end-to-end tests"
    )
    parser.add_argument(
        "--url",
        default=BASE_URL,
        help=f"Base URL for tests (default: {BASE_URL})"
    )
    
    args = parser.parse_args()
    
    runner = TestRunner(base_url=args.url)
    
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{'AIGuards Backend Test Suite'.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"\nTarget: {args.url}\n")
    
    try:
        if args.quick:
            await runner.run_quick_tests()
        elif args.guards:
            await runner.run_guard_tests()
        elif args.infra:
            await runner.run_infra_tests()
        elif args.e2e:
            await runner.run_all_tests()
        else:
            await runner.run_all_tests()
        
        success = runner.print_summary()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Test suite error: {e}{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())



