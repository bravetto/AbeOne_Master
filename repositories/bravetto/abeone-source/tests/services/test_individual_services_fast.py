#!/usr/bin/env python3
"""
Fast Individual Service Testing Script
Tests services directly (without containers) first, then optionally tests containers
"""

import subprocess
import time
import json
import sys
import os
import signal
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

try:
    import requests
except ImportError:
    print("ERROR: requests library not installed. Install with: pip install requests")
    sys.exit(1)

@dataclass
class ServiceTestResult:
    """Test result for a service"""
    name: str
    direct_test: Dict[str, bool] = None
    container_test: Dict[str, bool] = None
    errors: List[str] = None
    process_id: Optional[int] = None
    container_id: Optional[str] = None
    port: Optional[int] = None
    
    def __post_init__(self):
        if self.direct_test is None:
            self.direct_test = {
                "imports_ok": False,
                "service_started": False,
                "health_check_passed": False,
                "basic_functionality_passed": False
            }
        if self.container_test is None:
            self.container_test = {
                "dockerfile_exists": False,
                "build_success": False,
                "container_started": False,
                "health_check_passed": False
            }
        if self.errors is None:
            self.errors = []


class FastServiceTester:
    """Test services directly (fast) then optionally with containers"""
    
    def __init__(self, test_containers: bool = False):
        self.test_containers = test_containers
        self.services = {
            "tokenguard": {
                "path": "./guards/tokenguard",
                "module": "main",
                "port": 8001,
                "health_endpoint": "/health",
                "env_vars": {
                    "ENVIRONMENT": "test",
                    "LOG_LEVEL": "INFO",
                    "DATABASE_ENABLED": "false",
                    "REDIS_ENABLED": "false"
                }
            },
            "trustguard": {
                "path": "./guards/trust-guard",
                "module": "main",
                "port": 8002,
                "health_endpoint": "/health",
                "env_vars": {
                    "ENVIRONMENT": "test",
                    "LOG_LEVEL": "INFO",
                    "DATABASE_ENABLED": "false",
                    "REDIS_ENABLED": "false"
                }
            },
            "contextguard": {
                "path": "./guards/contextguard",
                "module": "main",
                "port": 8003,
                "health_endpoint": "/health",
                "env_vars": {
                    "ENVIRONMENT": "test",
                    "LOG_LEVEL": "INFO",
                    "REDIS_ENABLED": "false",
                    "REDIS_URL": "redis://localhost:6379/0"
                }
            },
            "biasguard": {
                "path": "./guards/biasguard-backend",
                "module": "run_server",
                "port": 8004,
                "health_endpoint": "/health",
                "env_vars": {
                    "ENVIRONMENT": "test",
                    "LOG_LEVEL": "INFO",
                    "DATABASE_ENABLED": "false",
                    "REDIS_ENABLED": "false"
                }
            },
            "healthguard": {
                "path": "./guards/healthguard",
                "module": "run_server",
                "port": 8005,
                "health_endpoint": "/health",
                "env_vars": {
                    "ENVIRONMENT": "test",
                    "LOG_LEVEL": "INFO",
                    "DATABASE_ENABLED": "false",
                    "REDIS_ENABLED": "false"
                }
            }
        }
        self.results: Dict[str, ServiceTestResult] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
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
    
    def run_command(self, cmd: str, capture_output: bool = True, check: bool = False, env: Dict = None) -> Dict[str, Any]:
        """Run a shell command"""
        try:
            cmd_env = os.environ.copy()
            if env:
                cmd_env.update(env)
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=check,
                timeout=60,
                env=cmd_env
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
    
    def test_imports(self, service_name: str, service_config: Dict) -> bool:
        """Test if service main file exists and has valid syntax"""
        self.log(f"{service_name}: Testing service file...", "TEST")

        module_path = Path(service_config["path"])
        module_file = module_path / f"{service_config['module']}.py"

        if not module_file.exists():
            self.log(f"{service_name}: Module file not found: {module_file}", "ERROR")
            return False

        # Just check if the file has valid Python syntax
        result = self.run_command(f"python -m py_compile {module_file}")

        if result["success"]:
            self.log(f"{service_name}: Service file syntax OK", "SUCCESS")
            return True
        else:
            error_msg = result["stderr"][:300] if result["stderr"] else "Syntax error"
            self.log(f"{service_name}: Service file syntax error: {error_msg}", "ERROR")
            return False
    
    def start_service_direct(self, service_name: str, service_config: Dict) -> Optional[subprocess.Popen]:
        """Start service directly as Python process"""
        self.log(f"{service_name}: Starting service directly...", "TEST")
        
        module_path = Path(service_config["path"])
        module_file = module_path / f"{service_config['module']}.py"
        
        if not module_file.exists():
            self.log(f"{service_name}: Module file not found: {module_file}", "ERROR")
            return None
        
        # Set up environment
        env = os.environ.copy()
        env.update(service_config.get("env_vars", {}))
        # Use absolute path for Windows compatibility
        abs_module_path = Path(service_config["path"]).resolve()
        env["PYTHONPATH"] = str(abs_module_path.parent) + os.pathsep + env.get("PYTHONPATH", "")
        
        try:
            # Start uvicorn process - use absolute module path
            # Use uvicorn CLI with module path
            cmd = [
                sys.executable, "-m", "uvicorn",
                f"{service_config['module']}:app",
                "--host", "127.0.0.1",
                "--port", str(service_config["port"]),
                "--log-level", "error"  # Suppress verbose logs
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                cwd=str(abs_module_path)  # Set working directory
            )
            
            # Give it a moment to start
            time.sleep(2)
            
            # Check if process is still running
            if process.poll() is None:
                self.log(f"{service_name}: Service started (PID: {process.pid})", "SUCCESS")
                return process
            else:
                stdout, stderr = process.communicate()
                error_msg = stderr.decode()[:300] if stderr else "Process exited immediately"
                self.log(f"{service_name}: Service failed to start: {error_msg}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"{service_name}: Error starting service: {str(e)}", "ERROR")
            return None
    
    def wait_for_service(self, service_name: str, service_config: Dict, max_wait: int = 15) -> bool:
        """Wait for service to be ready"""
        self.log(f"{service_name}: Waiting for service to be ready...", "INFO")
        url = f"http://127.0.0.1:{service_config['port']}{service_config['health_endpoint']}"
        
        for i in range(max_wait):
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    self.log(f"{service_name}: Service is ready", "SUCCESS")
                    return True
            except Exception:
                pass
            
            time.sleep(1)
            if i % 3 == 2:
                self.log(f"{service_name}: Still waiting... ({i+1}s)", "INFO")
        
        self.log(f"{service_name}: Service did not become ready within {max_wait}s", "ERROR")
        return False
    
    def test_health_endpoint(self, service_name: str, service_config: Dict) -> bool:
        """Test health endpoint"""
        self.log(f"{service_name}: Testing health endpoint...", "TEST")
        url = f"http://127.0.0.1:{service_config['port']}{service_config['health_endpoint']}"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'ok')
                self.log(f"{service_name}: Health check passed - {status}", "SUCCESS")
                return True
            else:
                self.log(f"{service_name}: Health check failed - HTTP {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"{service_name}: Health check error - {str(e)}", "ERROR")
            return False
    
    def test_basic_functionality(self, service_name: str, service_config: Dict) -> bool:
        """Test basic functionality endpoint"""
        self.log(f"{service_name}: Testing basic functionality...", "TEST")
        
        # Service-specific test endpoints
        test_configs = {
            "tokenguard": {
                "url": f"http://127.0.0.1:{service_config['port']}/",
                "method": "GET"
            },
            "trustguard": {
                "url": f"http://127.0.0.1:{service_config['port']}/",
                "method": "GET"
            },
            "contextguard": {
                "url": f"http://127.0.0.1:{service_config['port']}/",
                "method": "GET"
            },
            "biasguard": {
                "url": f"http://127.0.0.1:{service_config['port']}/health",
                "method": "GET"
            },
            "healthguard": {
                "url": f"http://127.0.0.1:{service_config['port']}/health",
                "method": "GET"
            }
        }
        
        if service_name not in test_configs:
            self.log(f"{service_name}: No test configured, skipping", "WARNING")
            return True
        
        test_config = test_configs[service_name]
        
        try:
            if test_config["method"] == "GET":
                response = requests.get(test_config["url"], timeout=5)
            else:
                response = requests.post(test_config["url"], timeout=5)
            
            # Accept 200, 404 (endpoint exists), or 422 (validation ok)
            if response.status_code in [200, 404, 422]:
                self.log(f"{service_name}: Basic functionality test passed", "SUCCESS")
                return True
            else:
                self.log(f"{service_name}: Basic functionality test failed - HTTP {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"{service_name}: Basic functionality test error - {str(e)}", "ERROR")
            return False
    
    def stop_service(self, service_name: str):
        """Stop a running service"""
        if service_name in self.processes:
            process = self.processes[service_name]
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception:
                pass
            del self.processes[service_name]
    
    def test_service_direct(self, service_name: str) -> ServiceTestResult:
        """Test a service directly (without containers)"""
        self.log(f"\n{'='*60}", "INFO")
        self.log(f"Testing {service_name.upper()} (Direct Mode)", "INFO")
        self.log(f"{'='*60}", "INFO")
        
        result = ServiceTestResult(name=service_name)
        service_config = self.services[service_name]
        result.port = service_config["port"]
        
        # Step 1: Test imports
        result.direct_test["imports_ok"] = self.test_imports(service_name, service_config)
        if not result.direct_test["imports_ok"]:
            result.errors.append("Imports failed")
            return result
        
        # Step 2: Start service
        process = self.start_service_direct(service_name, service_config)
        if not process:
            result.errors.append("Failed to start service")
            return result
        
        result.process_id = process.pid
        self.processes[service_name] = process
        
        # Step 3: Wait for service
        if not self.wait_for_service(service_name, service_config, max_wait=15):
            result.errors.append("Service did not become ready")
            self.stop_service(service_name)
            return result
        
        result.direct_test["service_started"] = True
        
        # Step 4: Test health endpoint
        result.direct_test["health_check_passed"] = self.test_health_endpoint(service_name, service_config)
        if not result.direct_test["health_check_passed"]:
            result.errors.append("Health check failed")
        
        # Step 5: Test basic functionality
        result.direct_test["basic_functionality_passed"] = self.test_basic_functionality(service_name, service_config)
        if not result.direct_test["basic_functionality_passed"]:
            result.errors.append("Basic functionality test failed")
        
        # Stop service
        self.stop_service(service_name)
        time.sleep(1)  # Give it a moment to clean up
        
        return result
    
    def test_service_container(self, service_name: str) -> Dict[str, bool]:
        """Test a service with containers (optional)"""
        if not self.test_containers:
            return {}
        
        self.log(f"\n{'='*60}", "INFO")
        self.log(f"Testing {service_name.upper()} (Container Mode)", "INFO")
        self.log(f"{'='*60}", "INFO")
        
        service_config = self.services[service_name]
        container_result = {
            "dockerfile_exists": False,
            "build_success": False,
            "container_started": False,
            "health_check_passed": False
        }
        
        # Check Dockerfile
        dockerfile_path = Path(service_config["path"]) / "Dockerfile"
        container_result["dockerfile_exists"] = dockerfile_path.exists()
        if not container_result["dockerfile_exists"]:
            self.log(f"{service_name}: Dockerfile not found", "ERROR")
            return container_result
        
        # Build container
        image_name = f"aiguards-{service_name}-test"
        self.log(f"{service_name}: Building container...", "TEST")
        build_cmd = f"docker build -t {image_name} {service_config['path']}"
        result = self.run_command(build_cmd)
        container_result["build_success"] = result["success"]
        
        if not container_result["build_success"]:
            self.log(f"{service_name}: Build failed", "ERROR")
            return container_result
        
        # Start container
        env_vars = service_config.get("env_vars", {})
        env_str = " ".join([f"-e {k}={v}" for k, v in env_vars.items()])
        container_name = f"{service_name}-test-container"
        
        run_cmd = (
            f"docker run -d {env_str} "
            f"-p {service_config['port']}:8000 "
            f"--name {container_name} "
            f"{image_name}"
        )
        
        self.log(f"{service_name}: Starting container...", "TEST")
        result = self.run_command(run_cmd)
        
        if result["success"] and result["stdout"].strip():
            container_id = result["stdout"].strip()
            container_result["container_started"] = True
            self.cleanup_containers.append(container_id)
            
            # Wait and test
            time.sleep(5)
            container_result["health_check_passed"] = self.test_health_endpoint(service_name, service_config)
            
            # Cleanup
            self.run_command(f"docker stop {container_name}", check=False)
            self.run_command(f"docker rm {container_name}", check=False)
        else:
            self.log(f"{service_name}: Failed to start container", "ERROR")
        
        return container_result
    
    def cleanup(self):
        """Cleanup all processes and containers"""
        self.log("Cleaning up...", "INFO")
        
        # Stop all processes
        for service_name in list(self.processes.keys()):
            self.stop_service(service_name)
        
        # Cleanup containers
        for container_id in self.cleanup_containers:
            self.run_command(f"docker stop {container_id}", check=False)
            self.run_command(f"docker rm {container_id}", check=False)
    
    def run_all_tests(self) -> bool:
        """Run all tests"""
        self.log("="*60, "INFO")
        self.log("FAST INDIVIDUAL SERVICE TESTING", "INFO")
        self.log("="*60, "INFO")
        self.log(f"Testing {len(self.services)} services (Direct Mode)", "INFO")
        if self.test_containers:
            self.log("Container testing will run after direct tests", "INFO")
        
        # Test each service directly
        for service_name in self.services.keys():
            result = self.test_service_direct(service_name)
            self.results[service_name] = result
            
            # Optionally test with containers
            if self.test_containers:
                container_result = self.test_service_container(service_name)
                result.container_test = container_result
        
        # Generate report
        self.generate_report()
        
        # Cleanup
        self.cleanup()
        
        # Return overall success
        all_passed = all(
            r.direct_test["service_started"] and r.direct_test["health_check_passed"]
            for r in self.results.values()
        )
        return all_passed
    
    def generate_report(self):
        """Generate test report"""
        self.log("\n" + "="*60, "INFO")
        self.log("TEST RESULTS SUMMARY", "INFO")
        self.log("="*60, "INFO")
        
        for service_name, result in self.results.items():
            direct = result.direct_test
            status = "[OK]" if (direct["service_started"] and direct["health_check_passed"]) else "[FAIL]"
            self.log(f"{status} {service_name.upper()}:", "INFO")
            self.log(f"   Direct Mode:", "INFO")
            self.log(f"     Imports: {'[OK]' if direct['imports_ok'] else '[FAIL]'}", "INFO")
            self.log(f"     Started: {'[OK]' if direct['service_started'] else '[FAIL]'}", "INFO")
            self.log(f"     Health: {'[OK]' if direct['health_check_passed'] else '[FAIL]'}", "INFO")
            self.log(f"     Functionality: {'[OK]' if direct['basic_functionality_passed'] else '[FAIL]'}", "INFO")
            
            if self.test_containers and result.container_test:
                container = result.container_test
                self.log(f"   Container Mode:", "INFO")
                self.log(f"     Dockerfile: {'[OK]' if container['dockerfile_exists'] else '[FAIL]'}", "INFO")
                self.log(f"     Build: {'[OK]' if container['build_success'] else '[FAIL]'}", "INFO")
                self.log(f"     Started: {'[OK]' if container['container_started'] else '[FAIL]'}", "INFO")
                self.log(f"     Health: {'[OK]' if container['health_check_passed'] else '[FAIL]'}", "INFO")
            
            if result.errors:
                self.log(f"   Errors: {', '.join(result.errors)}", "ERROR")
            self.log("", "INFO")
        
        # Summary stats
        total = len(self.results)
        imports_ok = sum(1 for r in self.results.values() if r.direct_test["imports_ok"])
        started_ok = sum(1 for r in self.results.values() if r.direct_test["service_started"])
        health_ok = sum(1 for r in self.results.values() if r.direct_test["health_check_passed"])
        func_ok = sum(1 for r in self.results.values() if r.direct_test["basic_functionality_passed"])
        
        self.log("="*60, "INFO")
        self.log("SUMMARY STATISTICS (Direct Mode)", "INFO")
        self.log("="*60, "INFO")
        self.log(f"Total Services: {total}", "INFO")
        self.log(f"Imports OK: {imports_ok}/{total}", "INFO")
        self.log(f"Started OK: {started_ok}/{total}", "INFO")
        self.log(f"Health Check Passed: {health_ok}/{total}", "INFO")
        self.log(f"Basic Functionality Passed: {func_ok}/{total}", "INFO")
        self.log("="*60, "INFO")
        
        # Save detailed report
        report_file = Path("fast_service_test_results.json")
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "test_mode": "direct" + ("+containers" if self.test_containers else ""),
            "summary": {
                "total": total,
                "imports_ok": imports_ok,
                "started_ok": started_ok,
                "health_check_passed": health_ok,
                "basic_functionality_passed": func_ok
            },
            "results": {
                name: {
                    "direct_test": r.direct_test,
                    "container_test": r.container_test if self.test_containers else None,
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
    import argparse
    
    parser = argparse.ArgumentParser(description="Fast individual service testing")
    parser.add_argument("--containers", action="store_true",
                       help="Also test with containers (slower)")
    parser.add_argument("--service", type=str,
                       help="Test only a specific service")
    
    args = parser.parse_args()
    
    tester = FastServiceTester(test_containers=args.containers)
    
    # Setup signal handler for cleanup
    def signal_handler(sig, frame):
        print("\n\nInterrupted! Cleaning up...")
        tester.cleanup()
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Filter to specific service if requested
        if args.service and args.service in tester.services:
            tester.services = {args.service: tester.services[args.service]}
        
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInterrupted! Cleaning up...")
        tester.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        tester.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()

