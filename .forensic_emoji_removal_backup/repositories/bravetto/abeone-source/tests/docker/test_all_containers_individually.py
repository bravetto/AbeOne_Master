#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Individual Container Testing Script
Tests all containers individually for functionality
"""

import subprocess
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("WARNING: psycopg2 not installed. PostgreSQL tests will be skipped.")
    psycopg2 = None

try:
    import redis
except ImportError:
    print("WARNING: redis not installed. Redis tests will be skipped.")
    redis = None

try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. Install with: pip install httpx")
    sys.exit(1)


@dataclass
class ContainerTestResult:
    """Test result for a container"""
    name: str
    container_running: bool = False
    health_check_passed: bool = False
    connectivity_test_passed: bool = False
    functionality_test_passed: bool = False
    errors: List[str] = field(default_factory=list)
    test_details: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.test_details is None:
            self.test_details = {}


class ContainerTester:
    """Test each container individually"""
    
    def __init__(self):
        self.containers = {
            "postgres": {
                "container_name": "codeguardians-postgres",
                "type": "database",
                "port": 5432,
                "host": "localhost"
            },
            "redis": {
                "container_name": "codeguardians-redis",
                "type": "cache",
                "port": 6379,
                "host": "localhost"
            },
            "tokenguard": {
                "container_name": "codeguardians-tokenguard",
                "type": "guard_service",
                "port": 8000,
                "health_endpoint": "/health",
                "functionality_endpoint": "/v1/analyze",
                "functionality_payload": {
                    "text": "This is a test text for token optimization. It should be analyzed and optimized for token usage.",
                    "confidence": 0.7
                },
                "requires_auth": True
            },
            "trustguard": {
                "container_name": "codeguardians-trustguard",
                "type": "guard_service",
                "port": 8000,
                "health_endpoint": "/health",
                "functionality_endpoint": "/v1/test/detect",
                "functionality_payload": {
                    "text": "This is a test message for trust validation.",
                    "context": None,
                    "metadata": {}
                },
                "requires_auth": False
            },
            "contextguard": {
                "container_name": "codeguardians-contextguard",
                "type": "guard_service",
                "port": 8000,
                "health_endpoint": "/health",
                "functionality_endpoint": "/memory",
                "functionality_payload": {
                    "key": "test_key_123",
                    "value": "test_context_value",
                    "ttl": 60
                },
                "requires_auth": False
            },
            "biasguard": {
                "container_name": "codeguardians-biasguard",
                "type": "guard_service",
                "port": 8000,
                "health_endpoint": "/health",
                "functionality_endpoint": "/analyze",
                "functionality_payload": {
                    "samples": [
                        {
                            "id": "test-1",
                            "content": "Only young people are good at technology. Older workers should retire early."
                        }
                    ]
                },
                "requires_auth": False
            },
            "healthguard": {
                "container_name": "codeguardians-healthguard",
                "type": "guard_service",
                "port": 8000,
                "health_endpoint": "/health",
                "functionality_endpoint": "/analyze",
                "functionality_payload": {
                    "samples": [
                        {
                            "id": "test-1",
                            "content": "This is a technical text for health validation."
                        }
                    ]
                },
                "requires_auth": False
            }
        }
        self.results: Dict[str, ContainerTestResult] = {}
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level_symbols = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️"
        }
        symbol = level_symbols.get(level, "•")
        print(f"[{timestamp}] {symbol} {message}")
    
    def run_command(self, cmd: List[str], check: bool = True) -> tuple[bool, str, str]:
        """Run a shell command"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def check_container_running(self, container_name: str) -> bool:
        """Check if container is running"""
        success, stdout, stderr = self.run_command([
            "docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"
        ])
        if success and stdout.strip() == container_name:
            return True
        return False
    
    def get_container_ip(self, container_name: str) -> Optional[str]:
        """Get container IP address on Docker network"""
        success, stdout, stderr = self.run_command([
            "docker", "inspect", "-f", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}", container_name
        ])
        if success and stdout.strip():
            return stdout.strip()
        return None
    
    def test_postgres(self) -> ContainerTestResult:
        """Test PostgreSQL container"""
        self.log(f"\n{'='*70}", "INFO")
        self.log(f"Testing PostgreSQL Container", "INFO")
        self.log(f"{'='*70}", "INFO")
        
        result = ContainerTestResult(name="postgres")
        
        # Check if container is running
        if not self.check_container_running("codeguardians-postgres"):
            result.errors.append("Container is not running")
            self.log("Container is not running", "ERROR")
            return result
        
        result.container_running = True
        self.log("Container is running", "SUCCESS")
        
        # Test database connectivity
        if psycopg2 is None:
            result.errors.append("psycopg2 library not available")
            self.log("Skipping database connectivity test (psycopg2 not installed)", "WARNING")
            return result
        
        try:
            # Try to connect to database
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="aiguardian_unified",
                user="aiguardian",
                password="REPLACE_ME",
                connect_timeout=5
            )
            conn.close()
            result.connectivity_test_passed = True
            self.log("Database connectivity test passed", "SUCCESS")
            
            # Test database operations
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="aiguardian_unified",
                user="aiguardian",
                password="REPLACE_ME",
                connect_timeout=5
            )
            cursor = conn.cursor()
            
            # Test query
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            result.test_details["postgres_version"] = version
            
            # Test database list
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = [row[0] for row in cursor.fetchall()]
            result.test_details["databases"] = databases
            
            # Check expected databases exist
            expected_dbs = ["tokenguard", "trustguard", "contextguard", "biasguard", "healthguard"]
            found_dbs = [db for db in databases if db in expected_dbs]
            result.test_details["found_guard_databases"] = found_dbs
            
            cursor.close()
            conn.close()
            
            result.functionality_test_passed = True
            self.log(f"Database operations test passed. Found {len(found_dbs)} guard databases", "SUCCESS")
            
        except Exception as e:
            result.errors.append(f"Database test failed: {str(e)}")
            self.log(f"Database test failed: {e}", "ERROR")
        
        return result
    
    def test_redis(self) -> ContainerTestResult:
        """Test Redis container"""
        self.log(f"\n{'='*70}", "INFO")
        self.log(f"Testing Redis Container", "INFO")
        self.log(f"{'='*70}", "INFO")
        
        result = ContainerTestResult(name="redis")
        
        # Check if container is running
        if not self.check_container_running("codeguardians-redis"):
            result.errors.append("Container is not running")
            self.log("Container is not running", "ERROR")
            return result
        
        result.container_running = True
        self.log("Container is running", "SUCCESS")
        
        # Test Redis connectivity
        if redis is None:
            result.errors.append("redis library not available")
            self.log("Skipping Redis connectivity test (redis library not installed)", "WARNING")
            return result
        
        try:
            # Try to connect to Redis
            r = redis.Redis(
                host="localhost",
                port=6379,
                password="REPLACE_ME",
                decode_responses=True,
                socket_connect_timeout=5
            )
            
            # Test PING
            response = r.ping()
            if response:
                result.connectivity_test_passed = True
                self.log("Redis connectivity test passed", "SUCCESS")
            
            # Test basic operations
            # Set a test key
            r.set("test:container:test", "test_value", ex=60)
            
            # Get the test key
            value = r.get("test:container:test")
            if value == "test_value":
                result.test_details["set_get_test"] = "passed"
            
            # Delete the test key
            r.delete("test:container:test")
            
            # Test info command
            info = r.info()
            result.test_details["redis_version"] = info.get("redis_version")
            result.test_details["used_memory_human"] = info.get("used_memory_human")
            
            result.functionality_test_passed = True
            self.log("Redis operations test passed", "SUCCESS")
            
        except Exception as e:
            result.errors.append(f"Redis test failed: {str(e)}")
            self.log(f"Redis test failed: {e}", "ERROR")
        
        return result
    
    async def test_guard_service_via_helper(self, service_name: str, config: Dict[str, Any]) -> ContainerTestResult:
        """Test a guard service container using a helper container on the Docker network"""
        result = ContainerTestResult(name=service_name)
        container_name = config["container_name"]
        
        # Check if container is running
        if not self.check_container_running(container_name):
            result.errors.append("Container is not running")
            return result
        
        result.container_running = True
        
        # Test health endpoint via helper container
        try:
            helper_cmd = [
                "docker", "run", "--rm", "--network", "aiguards-network",
                "-v", f"{os.getcwd()}:/app", "python:3.11-slim", "sh", "-c",
                "pip install httpx -q >/dev/null 2>&1 && python /app/test_helper.py " +
                f"{container_name} {config['port']} {config['health_endpoint']} GET"
            ]
            
            success, stdout, stderr = self.run_command(helper_cmd, check=False)
            if success and stdout.strip():
                try:
                    health_result = json.loads(stdout)
                    if health_result.get("status") == 200:
                        result.health_check_passed = True
                        result.test_details["health_response"] = health_result.get("data", {})
                        self.log(f"Health check passed", "SUCCESS")
                    else:
                        result.errors.append(f"Health check returned {health_result.get('status')}")
                except Exception as e:
                    result.errors.append(f"Failed to parse health response: {str(e)}")
            else:
                result.errors.append(f"Health check failed: {stderr[:200]}")
        except Exception as e:
            result.errors.append(f"Health check error: {str(e)}")
        
        # Test functionality endpoint
        if "functionality_endpoint" in config:
            try:
                payload = config.get("functionality_payload", {})
                requires_auth = config.get("requires_auth", False)
                api_key = os.environ.get("UNIFIED_API_KEY", "test-api-key") if requires_auth else None
                
                payload_json = json.dumps(payload)
                endpoint = config["functionality_endpoint"]
                
                # Build command
                cmd_parts = [
                    "docker", "run", "--rm", "--network", "aiguards-network",
                    "-v", f"{os.getcwd()}:/app", "python:3.11-slim", "sh", "-c",
                    f"pip install httpx -q >/dev/null 2>&1 && python /app/test_helper.py " +
                    f"{container_name} {config['port']} {endpoint} POST '{payload_json}'"
                ]
                
                if api_key:
                    # Add API key as last argument
                    cmd_parts[-1] = cmd_parts[-1] + f" {api_key}"
                
                helper_cmd = cmd_parts
                
                success, stdout, stderr = self.run_command(helper_cmd, check=False)
                if success and stdout.strip():
                    try:
                        func_result = json.loads(stdout)
                        status = func_result.get("status")
                        if status == 200 or status == 201:
                            result.functionality_test_passed = True
                            result.test_details["functionality_response"] = func_result.get("data", func_result.get("text", ""))
                            self.log(f"Functionality test passed", "SUCCESS")
                        else:
                            error_msg = func_result.get('text', func_result.get('error', ''))[:200]
                            result.errors.append(f"Functionality test returned {status}: {error_msg}")
                            self.log(f"Functionality test returned {status}", "WARNING")
                    except Exception as e:
                        result.errors.append(f"Failed to parse functionality response: {str(e)}")
                        self.log(f"Failed to parse response: {e}", "WARNING")
                else:
                    result.errors.append(f"Functionality test failed: {stderr[:200]}")
            except Exception as e:
                result.errors.append(f"Functionality test error: {str(e)}")
        
        return result
    
    async def test_guard_service(self, service_name: str, config: Dict[str, Any]) -> ContainerTestResult:
        """Test a guard service container"""
        self.log(f"\n{'='*70}", "INFO")
        self.log(f"Testing {service_name.upper()} Container", "INFO")
        self.log(f"{'='*70}", "INFO")
        
        result = ContainerTestResult(name=service_name)
        container_name = config["container_name"]
        
        # Check if container is running
        if not self.check_container_running(container_name):
            result.errors.append("Container is not running")
            self.log("Container is not running", "ERROR")
            return result
        
        result.container_running = True
        self.log("Container is running", "SUCCESS")
        
        # Use helper container approach for testing on Docker network
        result = await self.test_guard_service_via_helper(service_name, config)
        
        return result
    
    async def run_all_tests(self):
        """Run all container tests"""
        self.log("="*70, "INFO")
        self.log("COMPREHENSIVE INDIVIDUAL CONTAINER TESTING", "INFO")
        self.log("="*70, "INFO")
        self.log(f"Testing {len(self.containers)} containers", "INFO")
        
        # Test PostgreSQL
        if "postgres" in self.containers:
            self.results["postgres"] = self.test_postgres()
        
        # Test Redis
        if "redis" in self.containers:
            self.results["redis"] = self.test_redis()
        
        # Test Guard Services
        for service_name, config in self.containers.items():
            if config["type"] == "guard_service":
                self.results[service_name] = await self.test_guard_service(service_name, config)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        self.log("\n" + "="*70, "INFO")
        self.log("TEST RESULTS SUMMARY", "INFO")
        self.log("="*70, "INFO")
        
        total_tests = len(self.results)
        passed_tests = 0
        
        for service_name, result in self.results.items():
            all_passed = (
                result.container_running and
                result.connectivity_test_passed if result.name in ["postgres", "redis"] else result.health_check_passed and
                result.functionality_test_passed
            )
            
            if all_passed:
                passed_tests += 1
            
            status = "✅ PASS" if all_passed else "❌ FAIL"
            self.log(f"\n{service_name.upper()}: {status}", "SUCCESS" if all_passed else "ERROR")
            self.log(f"  Container Running: {'✅' if result.container_running else '❌'}", "INFO")
            
            if result.name in ["postgres", "redis"]:
                self.log(f"  Connectivity: {'✅' if result.connectivity_test_passed else '❌'}", "INFO")
            else:
                self.log(f"  Health Check: {'✅' if result.health_check_passed else '❌'}", "INFO")
            
            self.log(f"  Functionality: {'✅' if result.functionality_test_passed else '❌'}", "INFO")
            
            if result.errors:
                self.log(f"  Errors:", "ERROR")
                for error in result.errors:
                    self.log(f"    - {error}", "ERROR")
            
            if result.test_details:
                self.log(f"  Details:", "INFO")
                for key, value in result.test_details.items():
                    if key not in ["health_response", "functionality_response"]:
                        self.log(f"    - {key}: {value}", "INFO")
        
        self.log("\n" + "="*70, "INFO")
        self.log(f"OVERALL RESULT: {passed_tests}/{total_tests} containers passed", 
                 "SUCCESS" if passed_tests == total_tests else "ERROR")
        self.log("="*70, "INFO")
        
        # Save results to JSON
        results_dict = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": total_tests - passed_tests
            },
            "results": {name: asdict(result) for name, result in self.results.items()}
        }
        
        with open("container_test_results.json", "w") as f:
            json.dump(results_dict, f, indent=2, default=str)
        
        self.log(f"\nDetailed results saved to: container_test_results.json", "INFO")


async def main():
    """Main entry point"""
    tester = ContainerTester()
    await tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(
        (
            r.container_running and
            (r.connectivity_test_passed if r.name in ["postgres", "redis"] else r.health_check_passed) and
            r.functionality_test_passed
        )
        for r in tester.results.values()
    )
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    import asyncio
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

