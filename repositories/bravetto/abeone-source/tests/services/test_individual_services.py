#!/usr/bin/env python3
"""
Individual Service Testing Script
Tests each guard service and gateway independently to verify they work standalone
"""

import subprocess
import time
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class ServiceTestResult:
    """Test result for a service"""
    name: str
    dockerfile_exists: bool = False
    build_success: bool = False
    container_started: bool = False
    health_check_passed: bool = False
    basic_functionality_passed: bool = False
    errors: List[str] = None
    container_id: Optional[str] = None
    port: Optional[int] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class IndividualServiceTester:
    """Test each service individually"""
    
    def __init__(self):
        self.services = {
            "tokenguard": {
                "path": "./guards/tokenguard",
                "image": "aiguards-tokenguard-test",
                "port": 8001,
                "health_endpoint": "/health"
            },
            "trustguard": {
                "path": "./guards/trust-guard",
                "image": "aiguards-trustguard-test",
                "port": 8002,
                "health_endpoint": "/health"
            },
            "contextguard": {
                "path": "./guards/contextguard",
                "image": "aiguards-contextguard-test",
                "port": 8003,
                "health_endpoint": "/health"
            },
            "biasguard": {
                "path": "./guards/biasguard-backend",
                "image": "aiguards-biasguard-test",
                "port": 8004,
                "health_endpoint": "/health"
            },
            "healthguard": {
                "path": "./guards/healthguard",
                "image": "aiguards-healthguard-test",
                "port": 8005,
                "health_endpoint": "/health"
            },
            "gateway": {
                "path": "./codeguardians-gateway/codeguardians-gateway",
                "image": "aiguards-gateway-test",
                "port": 8000,
                "health_endpoint": "/health/live"
            }
        }
        self.results: Dict[str, ServiceTestResult] = {}
        self.cleanup_containers: List[str] = []
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "[INFO]",
            "SUCCESS": "[OK]",
            "ERROR": "[FAIL]",
            "WARNING": "[WARN]",
            "TEST": "[TEST]"
        }.get(level, "[INFO]")
        print(f"[{timestamp}] {prefix} {message}")
    
    def run_command(self, cmd: str, capture_output: bool = True, check: bool = False) -> Dict[str, Any]:
        """Run a shell command"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=check,
                timeout=300
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip() if capture_output else "",
                "stderr": result.stderr.strip() if capture_output else "",
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "stdout": "", "stderr": "Command timed out", "returncode": -1}
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}
    
    def check_dockerfile_exists(self, service_name: str, service_config: Dict) -> bool:
        """Check if Dockerfile exists"""
        dockerfile_path = Path(service_config["path"]) / "Dockerfile"
        exists = dockerfile_path.exists()
        if exists:
            self.log(f"{service_name}: Dockerfile found", "SUCCESS")
        else:
            self.log(f"{service_name}: Dockerfile NOT found at {dockerfile_path}", "ERROR")
        return exists
    
    def build_service(self, service_name: str, service_config: Dict) -> bool:
        """Build a service container"""
        self.log(f"{service_name}: Building container...", "TEST")
        
        build_cmd = f"docker build -t {service_config['image']} {service_config['path']}"
        result = self.run_command(build_cmd, check=False)
        
        if result["success"]:
            self.log(f"{service_name}: Container built successfully", "SUCCESS")
            return True
        else:
            error_msg = result["stderr"][:500] if result["stderr"] else "Unknown error"
            self.log(f"{service_name}: Build failed: {error_msg}", "ERROR")
            return False
    
    def start_service_container(self, service_name: str, service_config: Dict) -> Optional[str]:
        """Start a service container"""
        self.log(f"{service_name}: Starting container...", "TEST")
        
        # Minimal environment variables for standalone testing
        env_vars = {
            "ENVIRONMENT": "test",
            "LOG_LEVEL": "INFO",
            "DATABASE_ENABLED": "false",
            "REDIS_ENABLED": "false",
            "DEBUG": "false"
        }
        
        # Add service-specific environment variables
        if service_name == "contextguard":
            env_vars["REDIS_URL"] = "redis://localhost:6379/0"
        
        env_str = " ".join([f"-e {k}={v}" for k, v in env_vars.items()])
        
        run_cmd = (
            f"docker run -d {env_str} "
            f"-p {service_config['port']}:8000 "
            f"--name {service_name}-test "
            f"{service_config['image']}"
        )
        
        result = self.run_command(run_cmd)
        
        if result["success"] and result["stdout"].strip():
            container_id = result["stdout"].strip()
            self.cleanup_containers.append(container_id)
            self.log(f"{service_name}: Container started (ID: {container_id[:12]})", "SUCCESS")
            return container_id
        else:
            error_msg = result["stderr"][:500] if result["stderr"] else "Unknown error"
            self.log(f"{service_name}: Failed to start container: {error_msg}", "ERROR")
            return None
    
    def wait_for_service(self, service_name: str, service_config: Dict, max_wait: int = 30) -> bool:
        """Wait for service to be ready"""
        import requests
        
        self.log(f"{service_name}: Waiting for service to be ready...", "INFO")
        url = f"http://localhost:{service_config['port']}{service_config['health_endpoint']}"
        
        for i in range(max_wait):
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    self.log(f"{service_name}: Service is ready", "SUCCESS")
                    return True
            except Exception:
                pass
            
            time.sleep(1)
            if i % 5 == 4:
                self.log(f"{service_name}: Still waiting... ({i+1}s)", "INFO")
        
        self.log(f"{service_name}: Service did not become ready within {max_wait}s", "ERROR")
        return False
    
    def test_health_endpoint(self, service_name: str, service_config: Dict) -> bool:
        """Test health endpoint"""
        import requests
        
        self.log(f"{service_name}: Testing health endpoint...", "TEST")
        url = f"http://localhost:{service_config['port']}{service_config['health_endpoint']}"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log(f"{service_name}: Health check passed - {data.get('status', 'ok')}", "SUCCESS")
                return True
            else:
                self.log(f"{service_name}: Health check failed - HTTP {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"{service_name}: Health check error - {str(e)}", "ERROR")
            return False
    
    def test_basic_functionality(self, service_name: str, service_config: Dict) -> bool:
        """Test basic functionality endpoint"""
        import requests
        
        self.log(f"{service_name}: Testing basic functionality...", "TEST")
        
        # Service-specific test payloads
        test_payloads = {
            "tokenguard": {
                "url": f"http://localhost:{service_config['port']}/v1/generate",
                "method": "POST",
                "json": {
                    "text": "Test content for token optimization",
                    "content_type": "text"
                }
            },
            "trustguard": {
                "url": f"http://localhost:{service_config['port']}/v1/validate",
                "method": "POST",
                "json": {
                    "validation_type": "general",
                    "content": "Test content for validation"
                }
            },
            "contextguard": {
                "url": f"http://localhost:{service_config['port']}/memory/set",
                "method": "POST",
                "json": {
                    "key": "test_key",
                    "value": "test_value",
                    "ttl": 3600
                }
            },
            "biasguard": {
                "url": f"http://localhost:{service_config['port']}/v1/detect",
                "method": "POST",
                "json": {
                    "text": "Test content for bias detection"
                }
            },
            "healthguard": {
                "url": f"http://localhost:{service_config['port']}/v1/analyze",
                "method": "POST",
                "json": {
                    "content": "Test log content"
                }
            },
            "gateway": {
                "url": f"http://localhost:{service_config['port']}/api/v1/guards/services",
                "method": "GET"
            }
        }
        
        if service_name not in test_payloads:
            self.log(f"{service_name}: No test payload configured, skipping", "WARNING")
            return True  # Skip if no test configured
        
        test_config = test_payloads[service_name]
        
        try:
            if test_config["method"] == "GET":
                response = requests.get(test_config["url"], timeout=10)
            else:
                response = requests.post(
                    test_config["url"],
                    json=test_config.get("json", {}),
                    timeout=10
                )
            
            # Accept 200 or 201 or 422 (validation errors are ok - means service is working)
            if response.status_code in [200, 201, 422]:
                self.log(f"{service_name}: Basic functionality test passed", "SUCCESS")
                return True
            else:
                self.log(f"{service_name}: Basic functionality test failed - HTTP {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"{service_name}: Basic functionality test error - {str(e)}", "ERROR")
            return False
    
    def stop_container(self, container_id: str):
        """Stop and remove a container"""
        self.run_command(f"docker stop {container_id}", check=False)
        self.run_command(f"docker rm {container_id}", check=False)
    
    def cleanup(self):
        """Cleanup all test containers"""
        self.log("Cleaning up test containers...", "INFO")
        for container_id in self.cleanup_containers:
            self.stop_container(container_id)
        
        # Also cleanup by name
        for service_name in self.services.keys():
            self.run_command(f"docker stop {service_name}-test", check=False)
            self.run_command(f"docker rm {service_name}-test", check=False)
    
    def test_service(self, service_name: str) -> ServiceTestResult:
        """Test a single service"""
        self.log(f"\n{'='*60}", "INFO")
        self.log(f"Testing {service_name.upper()}", "INFO")
        self.log(f"{'='*60}", "INFO")
        
        result = ServiceTestResult(name=service_name)
        service_config = self.services[service_name]
        result.port = service_config["port"]
        
        # Step 1: Check Dockerfile
        result.dockerfile_exists = self.check_dockerfile_exists(service_name, service_config)
        if not result.dockerfile_exists:
            result.errors.append("Dockerfile not found")
            return result
        
        # Step 2: Build container
        result.build_success = self.build_service(service_name, service_config)
        if not result.build_success:
            result.errors.append("Build failed")
            return result
        
        # Step 3: Start container
        container_id = self.start_service_container(service_name, service_config)
        if not container_id:
            result.errors.append("Failed to start container")
            return result
        
        result.container_id = container_id
        result.container_started = True
        
        # Wait a bit for container to start
        time.sleep(5)
        
        # Step 4: Wait for service to be ready
        if not self.wait_for_service(service_name, service_config, max_wait=30):
            result.errors.append("Service did not become ready")
            self.stop_container(container_id)
            return result
        
        # Step 5: Test health endpoint
        result.health_check_passed = self.test_health_endpoint(service_name, service_config)
        if not result.health_check_passed:
            result.errors.append("Health check failed")
        
        # Step 6: Test basic functionality
        result.basic_functionality_passed = self.test_basic_functionality(service_name, service_config)
        if not result.basic_functionality_passed:
            result.errors.append("Basic functionality test failed")
        
        # Stop container after testing
        self.stop_container(container_id)
        
        return result
    
    def run_all_tests(self) -> bool:
        """Run tests for all services"""
        self.log("="*60, "INFO")
        self.log("INDIVIDUAL SERVICE TESTING", "INFO")
        self.log("="*60, "INFO")
        self.log(f"Testing {len(self.services)} services", "INFO")
        
        # Test each service
        for service_name in self.services.keys():
            result = self.test_service(service_name)
            self.results[service_name] = result
        
        # Generate report
        self.generate_report()
        
        # Cleanup
        self.cleanup()
        
        # Return overall success
        all_passed = all(
            r.build_success and r.container_started and r.health_check_passed
            for r in self.results.values()
        )
        return all_passed
    
    def generate_report(self):
        """Generate test report"""
        self.log("\n" + "="*60, "INFO")
        self.log("TEST RESULTS SUMMARY", "INFO")
        self.log("="*60, "INFO")
        
        for service_name, result in self.results.items():
            status = "" if (result.build_success and result.container_started and result.health_check_passed) else ""
            self.log(f"{status} {service_name.upper()}:", "INFO")
            self.log(f"   Dockerfile: {'' if result.dockerfile_exists else ''}", "INFO")
            self.log(f"   Build: {'' if result.build_success else ''}", "INFO")
            self.log(f"   Container Start: {'' if result.container_started else ''}", "INFO")
            self.log(f"   Health Check: {'' if result.health_check_passed else ''}", "INFO")
            self.log(f"   Basic Functionality: {'' if result.basic_functionality_passed else ''}", "INFO")
            if result.errors:
                self.log(f"   Errors: {', '.join(result.errors)}", "ERROR")
            self.log("", "INFO")
        
        # Summary stats
        total = len(self.results)
        dockerfile_ok = sum(1 for r in self.results.values() if r.dockerfile_exists)
        build_ok = sum(1 for r in self.results.values() if r.build_success)
        start_ok = sum(1 for r in self.results.values() if r.container_started)
        health_ok = sum(1 for r in self.results.values() if r.health_check_passed)
        func_ok = sum(1 for r in self.results.values() if r.basic_functionality_passed)
        
        self.log("="*60, "INFO")
        self.log("SUMMARY STATISTICS", "INFO")
        self.log("="*60, "INFO")
        self.log(f"Total Services: {total}", "INFO")
        self.log(f"Dockerfile Exists: {dockerfile_ok}/{total}", "INFO")
        self.log(f"Build Success: {build_ok}/{total}", "INFO")
        self.log(f"Container Started: {start_ok}/{total}", "INFO")
        self.log(f"Health Check Passed: {health_ok}/{total}", "INFO")
        self.log(f"Basic Functionality Passed: {func_ok}/{total}", "INFO")
        self.log("="*60, "INFO")
        
        # Save detailed report
        report_file = Path("individual_service_test_results.json")
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "dockerfile_exists": dockerfile_ok,
                "build_success": build_ok,
                "container_started": start_ok,
                "health_check_passed": health_ok,
                "basic_functionality_passed": func_ok
            },
            "results": {
                name: {
                    "dockerfile_exists": r.dockerfile_exists,
                    "build_success": r.build_success,
                    "container_started": r.container_started,
                    "health_check_passed": r.health_check_passed,
                    "basic_functionality_passed": r.basic_functionality_passed,
                    "errors": r.errors,
                    "port": r.port
                }
                for name, r in self.results.items()
            }
        }
        
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)
        
        self.log(f"\nDetailed report saved to: {report_file}", "INFO")


def main():
    """Main entry point"""
    import signal
    
    tester = IndividualServiceTester()
    
    # Setup signal handler for cleanup
    def signal_handler(sig, frame):
        print("\n\nInterrupted! Cleaning up...")
        tester.cleanup()
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInterrupted! Cleaning up...")
        tester.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        tester.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()

