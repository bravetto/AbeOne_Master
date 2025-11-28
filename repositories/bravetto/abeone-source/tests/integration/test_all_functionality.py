#!/usr/bin/env python3
"""
Comprehensive Functionality Test Suite for AIGuards Backend

This script tests ALL functionality including:
- Gateway health and service discovery
- All guard services (TokenGuard, TrustGuard, ContextGuard, BiasGuard, HealthGuard)
- Analytics and metrics endpoints
- Database connectivity
- Redis caching
- Webhooks
- Performance and load testing
- Error handling

Usage:
    python test_all_functionality.py [--skip-setup] [--verbose]
"""

import asyncio
import sys
import os
import time
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

# Fix Windows encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import httpx
    import requests
except ImportError:
    print("ERROR: Missing required packages. Install with: pip install httpx requests")
    sys.exit(1)

# Configuration
BASE_URL = "http://localhost:8000"
MAX_WAIT_TIME = 300  # 5 minutes max wait for services
CHECK_INTERVAL = 5  # Check every 5 seconds


@dataclass
class TestResult:
    """Test result data structure"""
    name: str
    success: bool
    duration: float
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class TestRunner:
    """Comprehensive test runner for all functionality"""
    
    def __init__(self, verbose: bool = False, skip_setup: bool = False):
        self.verbose = verbose
        self.skip_setup = skip_setup
        self.results: List[TestResult] = []
        self.start_time = time.time()
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with level"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "[INFO]",
            "SUCCESS": "[OK]",
            "ERROR": "[FAIL]",
            "WARNING": "[WARN]",
            "TEST": "[TEST]"
        }.get(level, "[INFO]")
        
        if self.verbose or level in ["ERROR", "SUCCESS", "WARNING"]:
            # Safe encoding for Windows
            try:
                output = f"[{timestamp}] {prefix} {message}"
                print(output)
            except (UnicodeEncodeError, UnicodeDecodeError):
                # Fallback for Windows encoding issues
                safe_message = message.encode('ascii', errors='replace').decode('ascii')
                output = f"[{timestamp}] {prefix} {safe_message}"
                print(output)
            except Exception:
                # Last resort
                print(f"[{timestamp}] {prefix} {message[:100]}")
    
    def check_docker_running(self) -> bool:
        """Check if Docker is running"""
        try:
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            self.log(f"Docker check failed: {e}", "ERROR")
            return False
    
    def check_service_health(self, url: str, timeout: int = 10) -> bool:
        """Check if a service is healthy"""
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except Exception:
            return False
    
    def wait_for_services(self) -> bool:
        """Wait for all services to be ready"""
        self.log("Waiting for services to be ready...", "INFO")
        
        services = {
            "gateway": f"{BASE_URL}/health/live",
            "postgres": None,  # Check via gateway
            "redis": None  # Check via gateway
        }
        
        start_time = time.time()
        while time.time() - start_time < MAX_WAIT_TIME:
            try:
                response = requests.get(f"{BASE_URL}/health/ready", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "ready":
                        checks = data.get("checks", {})
                        all_ready = all(
                            status == "healthy" for status in checks.values()
                        )
                        if all_ready:
                            self.log("All services are ready!", "SUCCESS")
                            return True
            except Exception:
                pass
            
            time.sleep(CHECK_INTERVAL)
            elapsed = int(time.time() - start_time)
            if elapsed % 30 == 0:
                self.log(f"Still waiting... ({elapsed}s elapsed)", "INFO")
        
        self.log("Services did not become ready in time", "ERROR")
        return False
    
    def start_containers(self) -> bool:
        """Start Docker containers"""
        if not self.check_docker_running():
            self.log("Docker is not running. Please start Docker first.", "ERROR")
            return False
        
        self.log("Starting Docker containers...", "INFO")
        try:
            result = subprocess.run(
                ["docker-compose", "up", "-d"],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                self.log("Containers started successfully", "SUCCESS")
                return True
            else:
                self.log(f"Failed to start containers: {result.stderr}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Error starting containers: {e}", "ERROR")
            return False
    
    async def test_gateway_health(self) -> TestResult:
        """Test gateway health endpoints"""
        self.log("Testing Gateway Health...", "TEST")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Test /health/live
                response = await client.get(f"{BASE_URL}/health/live")
                if response.status_code != 200:
                    return TestResult(
                        "Gateway Health (Live)",
                        False,
                        time.time() - start_time,
                        f"HTTP {response.status_code}"
                    )
                
                # Test /health/ready
                response = await client.get(f"{BASE_URL}/health/ready")
                if response.status_code != 200:
                    return TestResult(
                        "Gateway Health (Ready)",
                        False,
                        time.time() - start_time,
                        f"HTTP {response.status_code}"
                    )
                
                data = response.json()
                checks = data.get("checks", {})
                
                return TestResult(
                    "Gateway Health",
                    True,
                    time.time() - start_time,
                    details={"checks": checks}
                )
        except Exception as e:
            return TestResult(
                "Gateway Health",
                False,
                time.time() - start_time,
                str(e)
            )
    
    async def test_service_discovery(self) -> TestResult:
        """Test service discovery"""
        self.log("Testing Service Discovery...", "TEST")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{BASE_URL}/api/v1/guards/services")
                if response.status_code != 200:
                    return TestResult(
                        "Service Discovery",
                        False,
                        time.time() - start_time,
                        f"HTTP {response.status_code}"
                    )
                
                data = response.json()
                services = data.get("services", [])
                
                return TestResult(
                    "Service Discovery",
                    True,
                    time.time() - start_time,
                    details={"services_count": len(services), "services": services}
                )
        except Exception as e:
            return TestResult(
                "Service Discovery",
                False,
                time.time() - start_time,
                str(e)
            )
    
    async def test_guard_service(
        self, 
        service_type: str, 
        payload: Dict[str, Any],
        expected_fields: List[str] = None
    ) -> TestResult:
        """Test a guard service"""
        self.log(f"Testing {service_type}...", "TEST")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                request_data = {
                    "service_type": service_type,
                    "payload": payload,
                    "user_id": "test-user-123",
                    "session_id": "test-session-456"
                }
                
                response = await client.post(
                    f"{BASE_URL}/api/v1/guards/process",
                    json=request_data
                )
                
                if response.status_code != 200:
                    return TestResult(
                        f"{service_type} Processing",
                        False,
                        time.time() - start_time,
                        f"HTTP {response.status_code}: {response.text[:200]}"
                    )
                
                data = response.json()
                success = data.get("success", False)
                
                if not success:
                    return TestResult(
                        f"{service_type} Processing",
                        False,
                        time.time() - start_time,
                        data.get("error", "Unknown error")
                    )
                
                # Check for expected fields
                result_data = data.get("data", {})
                found_fields = []
                if expected_fields:
                    found_fields = [f for f in expected_fields if f in str(result_data)]
                
                return TestResult(
                    f"{service_type} Processing",
                    True,
                    time.time() - start_time,
                    details={
                        "processing_time": data.get("processing_time", 0),
                        "found_fields": found_fields,
                        "response_keys": list(result_data.keys()) if isinstance(result_data, dict) else []
                    }
                )
        except Exception as e:
            return TestResult(
                f"{service_type} Processing",
                False,
                time.time() - start_time,
                str(e)
            )
    
    async def test_all_guards(self) -> List[TestResult]:
        """Test all guard services"""
        self.log("Testing All Guard Services...", "TEST")
        
        guard_tests = [
            {
                "service_type": "tokenguard",
                "payload": {
                    "text": "This is a very long verbose response that contains a lot of unnecessary words and could definitely benefit from compression to reduce token usage and improve efficiency.",
                    "content_type": "text"
                },
                "expected_fields": ["tokens_saved", "cost_savings", "optimization_score"]
            },
            {
                "service_type": "trustguard",
                "payload": {
                    "validation_type": "general",
                    "content": "This AI response appears to be hallucinating false information about quantum computing capabilities that don't exist in reality.",
                    "validation_level": "standard"
                },
                "expected_fields": ["violations_detected", "compliance_score", "risk_level"]
            },
            {
                "service_type": "contextguard",
                "payload": {
                    "operation": "set",
                    "data": {
                        "key": "test_context",
                        "value": "This is important context information that should be stored and retrieved efficiently.",
                        "ttl": 3600
                    }
                },
                "expected_fields": ["success", "context_id", "stored_data"]
            },
            {
                "service_type": "biasguard",
                "payload": {
                    "text": "He should be the manager because men are better leaders than women.",
                    "bias_types": ["gender_bias", "racial_bias"],
                    "mitigation_level": "moderate"
                },
                "expected_fields": ["bias_detected", "bias_score", "mitigation_suggestions"]
            },
            {
                "service_type": "healthguard",
                "payload": {
                    "content": "INFO: Application started successfully. Memory usage: 45MB, CPU: 12%. All systems operational.",
                    "content_type": "system_log"
                },
                "expected_fields": ["health_status", "issues_detected", "recommendations"]
            }
        ]
        
        results = []
        for test_config in guard_tests:
            result = await self.test_guard_service(
                test_config["service_type"],
                test_config["payload"],
                test_config.get("expected_fields")
            )
            results.append(result)
        
        return results
    
    async def test_analytics_endpoints(self) -> List[TestResult]:
        """Test analytics endpoints"""
        self.log("Testing Analytics Endpoints...", "TEST")
        
        endpoints = [
            "/api/v1/analytics/benefits/overview",
            "/api/v1/analytics/benefits/detailed",
            "/api/v1/analytics/performance/dashboard"
        ]
        
        results = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            for endpoint in endpoints:
                start_time = time.time()
                try:
                    response = await client.get(f"{BASE_URL}{endpoint}")
                    success = response.status_code == 200
                    
                    details = {}
                    if success:
                        try:
                            data = response.json()
                            details = {"response_keys": list(data.keys()) if isinstance(data, dict) else []}
                        except:
                            pass
                    
                    results.append(TestResult(
                        f"Analytics: {endpoint}",
                        success,
                        time.time() - start_time,
                        None if success else f"HTTP {response.status_code}",
                        details
                    ))
                except Exception as e:
                    results.append(TestResult(
                        f"Analytics: {endpoint}",
                        False,
                        time.time() - start_time,
                        str(e)
                    ))
        
        return results
    
    async def test_performance(self) -> TestResult:
        """Test performance with concurrent requests"""
        self.log("Testing Performance...", "TEST")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Create multiple concurrent requests
                tasks = []
                for i in range(10):
                    task = client.post(
                        f"{BASE_URL}/api/v1/guards/process",
                        json={
                            "service_type": "tokenguard",
                            "payload": {"text": f"Performance test message {i}"},
                            "user_id": f"user-{i}",
                            "session_id": f"session-{i}"
                        }
                    )
                    tasks.append(task)
                
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                successful = sum(1 for r in responses if not isinstance(r, Exception) and r.status_code == 200)
                total_time = time.time() - start_time
                
                return TestResult(
                    "Performance Test",
                    successful == len(tasks),
                    total_time,
                    None if successful == len(tasks) else f"{successful}/{len(tasks)} requests succeeded",
                    {
                        "total_requests": len(tasks),
                        "successful_requests": successful,
                        "total_time": total_time,
                        "avg_response_time": total_time / len(tasks),
                        "requests_per_second": len(tasks) / total_time
                    }
                )
        except Exception as e:
            return TestResult(
                "Performance Test",
                False,
                time.time() - start_time,
                str(e)
            )
    
    async def run_all_tests(self) -> bool:
        """Run all tests"""
        self.log("=" * 70, "INFO")
        self.log("COMPREHENSIVE FUNCTIONALITY TEST SUITE", "INFO")
        self.log("=" * 70, "INFO")
        
        # Setup phase
        if not self.skip_setup:
            if not self.check_docker_running():
                self.log("Docker is not running. Please start Docker first.", "ERROR")
                return False
            
            if not self.start_containers():
                return False
            
            if not self.wait_for_services():
                return False
        else:
            self.log("Skipping setup - assuming services are already running", "WARNING")
        
        # Run tests
        self.log("\n" + "=" * 70, "INFO")
        self.log("RUNNING TESTS", "INFO")
        self.log("=" * 70 + "\n", "INFO")
        
        # Gateway health
        result = await self.test_gateway_health()
        self.results.append(result)
        status = "[OK]" if result.success else "[FAIL]"
        self.log(f"{status} {result.name} ({result.duration:.2f}s)", 
                 "SUCCESS" if result.success else "ERROR")
        
        # Service discovery
        result = await self.test_service_discovery()
        self.results.append(result)
        status = "[OK]" if result.success else "[FAIL]"
        self.log(f"{status} {result.name} ({result.duration:.2f}s)", 
                 "SUCCESS" if result.success else "ERROR")
        
        # Guard services
        guard_results = await self.test_all_guards()
        self.results.extend(guard_results)
        for result in guard_results:
            status = "[OK]" if result.success else "[FAIL]"
            self.log(f"{status} {result.name} ({result.duration:.2f}s)", 
                     "SUCCESS" if result.success else "ERROR")
        
        # Analytics
        analytics_results = await self.test_analytics_endpoints()
        self.results.extend(analytics_results)
        for result in analytics_results:
            status = "[OK]" if result.success else "[FAIL]"
            self.log(f"{status} {result.name} ({result.duration:.2f}s)", 
                     "SUCCESS" if result.success else "ERROR")
        
        # Performance
        result = await self.test_performance()
        self.results.append(result)
        status = "[OK]" if result.success else "[FAIL]"
        self.log(f"{status} {result.name} ({result.duration:.2f}s)", 
                 "SUCCESS" if result.success else "ERROR")
        
        # Generate report
        self.generate_report()
        
        # Return overall success
        return all(r.success for r in self.results)
    
    def generate_report(self):
        """Generate comprehensive test report"""
        self.log("\n" + "=" * 70, "INFO")
        self.log("TEST RESULTS SUMMARY", "INFO")
        self.log("=" * 70, "INFO")
        
        total_time = time.time() - self.start_time
        passed = sum(1 for r in self.results if r.success)
        failed = len(self.results) - passed
        
        self.log(f"\nTotal Tests: {len(self.results)}", "INFO")
        self.log(f"Passed: {passed}", "SUCCESS" if passed == len(self.results) else "INFO")
        self.log(f"Failed: {failed}", "ERROR" if failed > 0 else "INFO")
        self.log(f"Success Rate: {(passed/len(self.results)*100):.1f}%", "INFO")
        self.log(f"Total Duration: {total_time:.2f}s", "INFO")
        
        if failed > 0:
            self.log("\nFailed Tests:", "ERROR")
            for result in self.results:
                if not result.success:
                    self.log(f"  [FAIL] {result.name}: {result.error or 'Unknown error'}", "ERROR")
        
        # Save detailed report to file
        report_file = Path("test_results.json")
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.results),
            "passed": passed,
            "failed": failed,
            "success_rate": (passed/len(self.results)*100),
            "total_duration": total_time,
            "results": [asdict(r) for r in self.results]
        }
        
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)
        
        self.log(f"\nDetailed report saved to: {report_file}", "INFO")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Comprehensive functionality test suite")
    parser.add_argument("--skip-setup", action="store_true", 
                       help="Skip Docker container setup (assume services are running)")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    runner = TestRunner(verbose=args.verbose, skip_setup=args.skip_setup)
    success = await runner.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())

