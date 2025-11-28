#!/usr/bin/env python3
"""
Quick integration validation for TokenGuard microservice.

This script provides a simplified validation for basic deployment verification.
For comprehensive testing, use the test suite in tests/ directory:

- python -m pytest tests/
- python tests/validation_final.py  
- python tests/test_service.py

This script validates that all components work together and meet the 
basic production requirements.
"""

import subprocess
import time
import requests
import json
import sys
import os
from typing import Dict, Any, List


class TokenGuardValidator:
    """Comprehensive validation suite for TokenGuard deployment."""
    
    def __init__(self: Any, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "passed": [],
            "failed": [],
            "warnings": []
        }
    
    def log_result(self: Any, test_name: str, passed: bool, details: str = "") -> Any:
        """Log test result."""
        if passed:
            self.results["passed"].append(f"✅ {test_name}: {details}")
            print(f"✅ {test_name}: {details}")
        else:
            self.results["failed"].append(f"❌ {test_name}: {details}")
            print(f"❌ {test_name}: {details}")
    
    def log_warning(self: Any, message: str) -> Any:
        """Log warning message."""
        self.results["warnings"].append(f"⚠️  {message}")
        print(f"⚠️  {message}")
    
    def validate_service_availability(self: Any) -> bool:
        """Validate that the service is running and accessible."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_result("Service Availability", True, "Service is healthy and responsive")
                    return True
                else:
                    self.log_result("Service Availability", False, f"Unhealthy status: {data}")
                    return False
            else:
                self.log_result("Service Availability", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Service Availability", False, f"Connection failed: {e}")
            return False
    
    def validate_api_endpoints(self: Any) -> bool:
        """Validate all API endpoints work correctly."""
        all_passed = True
        
        # Test prune endpoint - should keep
        try:
            response = requests.post(f"{self.base_url}/v1/prune", json={
                "text": "Short high confidence text.",
                "confidence": 0.9
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("action") == "keep":
                    self.log_result("Prune Endpoint (Keep)", True, "High confidence text kept as expected")
                else:
                    self.log_result("Prune Endpoint (Keep)", False, f"Unexpected action: {data.get('action')}")
                    all_passed = False
            else:
                self.log_result("Prune Endpoint (Keep)", False, f"HTTP {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Prune Endpoint (Keep)", False, f"Request failed: {e}")
            all_passed = False
        
        # Test prune endpoint - should prune
        try:
            long_text = "This is a very long response that should be pruned due to low confidence. " * 20
            response = requests.post(f"{self.base_url}/v1/prune", json={
                "text": long_text,
                "confidence": 0.4
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("action") == "prune":
                    savings = data.get("original_length", 0) - data.get("pruned_length", 0)
                    self.log_result("Prune Endpoint (Prune)", True, f"Low confidence text pruned, saved {savings} chars")
                else:
                    self.log_result("Prune Endpoint (Prune)", False, f"Expected prune, got: {data.get('action')}")
                    all_passed = False
            else:
                self.log_result("Prune Endpoint (Prune)", False, f"HTTP {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Prune Endpoint (Prune)", False, f"Request failed: {e}")
            all_passed = False
        
        # Test analyze endpoint
        try:
            response = requests.post(f"{self.base_url}/v1/analyze", json={
                "text": "Sample text for analysis.",
                "confidence": 0.7
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["text_length", "confidence_score", "decision", "recommendation"]
                if all(field in data for field in required_fields):
                    self.log_result("Analyze Endpoint", True, "All required fields present")
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_result("Analyze Endpoint", False, f"Missing fields: {missing}")
                    all_passed = False
            else:
                self.log_result("Analyze Endpoint", False, f"HTTP {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Analyze Endpoint", False, f"Request failed: {e}")
            all_passed = False
        
        return all_passed
    
    def validate_performance_requirements(self: Any) -> bool:
        """Validate performance meets requirements (sub-100ms total latency)."""
        test_cases = [
            {
                "name": "Short Text High Confidence",
                "payload": {"text": "Short response.", "confidence": 0.9},
                "target_ms": 20
            },
            {
                "name": "Medium Text Medium Confidence", 
                "payload": {"text": "Medium length response for testing. " * 10, "confidence": 0.7},
                "target_ms": 30
            },
            {
                "name": "Long Text Low Confidence",
                "payload": {"text": "Long response that should be pruned. " * 50, "confidence": 0.4},
                "target_ms": 50
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            latencies = []
            
            # Run multiple iterations for statistical validity
            for _ in range(10):
                start_time = time.perf_counter()
                try:
                    response = requests.post(
                        f"{self.base_url}/v1/prune", 
                        json=test_case["payload"],
                        timeout=5
                    )
                    end_time = time.perf_counter()
                    
                    if response.status_code == 200:
                        latency_ms = (end_time - start_time) * 1000
                        latencies.append(latency_ms)
                    else:
                        all_passed = False
                        break
                except Exception:
                    all_passed = False
                    break
            
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
                
                if p95_latency < test_case["target_ms"]:
                    self.log_result(
                        f"Performance: {test_case['name']}", 
                        True, 
                        f"P95: {p95_latency:.1f}ms (target: <{test_case['target_ms']}ms)"
                    )
                else:
                    self.log_result(
                        f"Performance: {test_case['name']}", 
                        False, 
                        f"P95: {p95_latency:.1f}ms exceeds target of {test_case['target_ms']}ms"
                    )
                    all_passed = False
            else:
                self.log_result(f"Performance: {test_case['name']}", False, "No successful requests")
                all_passed = False
        
        return all_passed
    
    def validate_error_handling(self: Any) -> bool:
        """Validate proper error handling."""
        all_passed = True
        
        # Test invalid confidence
        try:
            response = requests.post(f"{self.base_url}/v1/prune", json={
                "text": "Valid text",
                "confidence": 1.5  # Invalid
            }, timeout=5)
            
            if response.status_code == 422:
                self.log_result("Error Handling: Invalid Confidence", True, "Returns 422 for invalid confidence")
            else:
                self.log_result("Error Handling: Invalid Confidence", False, f"Expected 422, got {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Error Handling: Invalid Confidence", False, f"Request failed: {e}")
            all_passed = False
        
        # Test missing fields
        try:
            response = requests.post(f"{self.base_url}/v1/prune", json={
                "text": "Valid text"
                # Missing confidence
            }, timeout=5)
            
            if response.status_code == 422:
                self.log_result("Error Handling: Missing Fields", True, "Returns 422 for missing fields")
            else:
                self.log_result("Error Handling: Missing Fields", False, f"Expected 422, got {response.status_code}")
                all_passed = False
        except Exception as e:
            self.log_result("Error Handling: Missing Fields", False, f"Request failed: {e}")
            all_passed = False
        
        return all_passed
    
    def validate_configuration(self: Any) -> bool:
        """Validate configuration is working correctly."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                config = data.get("config", {})
                
                # Check key configuration values are present
                required_config = ["confidence_threshold", "max_length", "rate_limit_enabled"]
                if all(key in config for key in required_config):
                    self.log_result("Configuration", True, f"All config values present: {config}")
                    return True
                else:
                    missing = [key for key in required_config if key not in config]
                    self.log_result("Configuration", False, f"Missing config values: {missing}")
                    return False
            else:
                self.log_result("Configuration", False, f"Health endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Configuration", False, f"Request failed: {e}")
            return False
    
    def validate_docker_build(self: Any) -> bool:
        """Validate Docker container can be built successfully."""
        try:
            # Check if Docker is available
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                self.log_warning("Docker not available - skipping container build test")
                return True
            
            # Try to build the container
            print("Building Docker container (this may take a few minutes)...")
            result = subprocess.run(
                ["docker", "build", "-t", "tokenguard-test", "."],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                self.log_result("Docker Build", True, "Container built successfully")
                
                # Clean up test image
                subprocess.run(["docker", "rmi", "tokenguard-test"], capture_output=True)
                return True
            else:
                self.log_result("Docker Build", False, f"Build failed: {result.stderr[:200]}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_result("Docker Build", False, "Build timed out after 5 minutes")
            return False
        except Exception as e:
            self.log_result("Docker Build", False, f"Build failed: {e}")
            return False
    
    def validate_unit_tests(self: Any) -> bool:
        """Run unit tests to validate code quality."""
        try:
            # Check if pytest is available
            result = subprocess.run(["python", "-m", "pytest", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                self.log_warning("pytest not available - skipping unit tests")
                return True
            
            # Run tests
            print("Running unit tests...")
            result = subprocess.run(
                ["python", "-m", "pytest", "test_tokenguard.py", "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Count passed tests
                passed_count = result.stdout.count("PASSED")
                self.log_result("Unit Tests", True, f"{passed_count} tests passed")
                return True
            else:
                failed_count = result.stdout.count("FAILED")
                self.log_result("Unit Tests", False, f"{failed_count} tests failed")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_result("Unit Tests", False, "Tests timed out after 60 seconds")
            return False
        except Exception as e:
            self.log_result("Unit Tests", False, f"Test execution failed: {e}")
            return False
    
    def run_comprehensive_validation(self: Any) -> Dict[str, Any]:
        """Run all validation tests."""
        print("🚀 Starting comprehensive TokenGuard validation...\n")
        
        validations = [
            ("Service Availability", self.validate_service_availability),
            ("API Endpoints", self.validate_api_endpoints),
            ("Performance Requirements", self.validate_performance_requirements),
            ("Error Handling", self.validate_error_handling),
            ("Configuration", self.validate_configuration),
            ("Unit Tests", self.validate_unit_tests),
            ("Docker Build", self.validate_docker_build),
        ]
        
        overall_success = True
        
        for name, validation_func in validations:
            print(f"\n--- {name} ---")
            try:
                success = validation_func()
                if not success:
                    overall_success = False
            except Exception as e:
                self.log_result(name, False, f"Validation crashed: {e}")
                overall_success = False
        
        # Generate summary
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        for result in self.results["passed"]:
            print(result)
        
        if self.results["warnings"]:
            print("\nWarnings:")
            for warning in self.results["warnings"]:
                print(warning)
        
        if self.results["failed"]:
            print("\nFailures:")
            for failure in self.results["failed"]:
                print(failure)
        
        print(f"\nOverall Result: {'✅ PASS' if overall_success else '❌ FAIL'}")
        print(f"Passed: {len(self.results['passed'])}")
        print(f"Failed: {len(self.results['failed'])}")
        print(f"Warnings: {len(self.results['warnings'])}")
        
        if overall_success:
            print("\n🎉 TokenGuard is ready for production deployment!")
        else:
            print("\n⚠️  TokenGuard has issues that need to be addressed before production.")
        
        return {
            "overall_success": overall_success,
            "results": self.results,
            "summary": {
                "passed": len(self.results["passed"]),
                "failed": len(self.results["failed"]),
                "warnings": len(self.results["warnings"])
            }
        }


def main() -> Any:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TokenGuard Comprehensive Validation")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of TokenGuard service")
    parser.add_argument("--output", help="Save results to JSON file")
    
    args = parser.parse_args()
    
    validator = TokenGuardValidator(args.url)
    results = validator.run_comprehensive_validation()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Results saved to {args.output}")
    
    # Exit with appropriate code
    sys.exit(0 if results["overall_success"] else 1)


if __name__ == "__main__":
    main()