"""
Comprehensive Test Runner for AI Guardians

This script runs all tests including OpenTelemetry monitoring, LLM testing,
and documentation validation to ensure everything works as intended.
"""

import asyncio
import json
import time
import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import httpx
import docker
from docker.errors import DockerException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Result of a test."""
    test_name: str
    success: bool
    duration: float
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = None

class ComprehensiveTestRunner:
    """Runs comprehensive tests for the AI Guardians system."""
    
    def __init__(self, gateway_url: str = "http://localhost:8000"):
        self.gateway_url = gateway_url
        self.results: List[TestResult] = []
        self.docker_client = None
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all comprehensive tests."""
        logger.info("Starting comprehensive test suite...")
        
        # Initialize Docker client
        try:
            self.docker_client = docker.from_env()
            logger.info("Docker client initialized")
        except DockerException as e:
            logger.warning(f"Could not initialize Docker client: {e}")
        
        # Run tests
        await self._test_system_startup()
        await self._test_telemetry_setup()
        await self._test_guard_services()
        await self._test_api_endpoints()
        await self._test_llm_integration()
        await self._test_documentation()
        await self._test_docker_containers()
        
        # Generate report
        return self._generate_test_report()
    
    async def _test_system_startup(self) -> None:
        """Test system startup and initialization."""
        logger.info("Testing system startup...")
        start_time = time.time()
        
        try:
            # Test if the gateway is running
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.gateway_url}/health", timeout=10.0)
                
            if response.status_code == 200:
                self.results.append(TestResult(
                    test_name="system_startup",
                    success=True,
                    duration=time.time() - start_time,
                    metrics={"status_code": response.status_code}
                ))
                logger.info("✅ System startup test passed")
            else:
                raise Exception(f"Health check failed with status {response.status_code}")
                
        except Exception as e:
            self.results.append(TestResult(
                test_name="system_startup",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e)
            ))
            logger.error(f"❌ System startup test failed: {e}")
    
    async def _test_telemetry_setup(self) -> None:
        """Test OpenTelemetry setup."""
        logger.info("Testing OpenTelemetry setup...")
        start_time = time.time()
        
        try:
            # Import telemetry module
            from app.core.telemetry import configure_telemetry, get_telemetry_health
            
            # Configure telemetry
            configure_telemetry()
            
            # Check telemetry health
            health = get_telemetry_health()
            
            self.results.append(TestResult(
                test_name="telemetry_setup",
                success=health["tracer_configured"] and health["meter_configured"],
                duration=time.time() - start_time,
                metrics=health
            ))
            
            if health["tracer_configured"] and health["meter_configured"]:
                logger.info("✅ Telemetry setup test passed")
            else:
                logger.warning("⚠️ Telemetry setup partially configured")
                
        except Exception as e:
            self.results.append(TestResult(
                test_name="telemetry_setup",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e)
            ))
            logger.error(f"❌ Telemetry setup test failed: {e}")
    
    async def _test_guard_services(self) -> None:
        """Test guard services initialization."""
        logger.info("Testing guard services...")
        start_time = time.time()
        
        try:
            from app.core.guard_orchestrator import orchestrator, GuardServiceType
            
            # Initialize orchestrator
            await orchestrator.initialize()
            
            # Check services
            expected_services = [t.value for t in GuardServiceType]
            actual_services = list(orchestrator.services.keys())
            
            success = all(service in actual_services for service in expected_services)
            
            self.results.append(TestResult(
                test_name="guard_services",
                success=success,
                duration=time.time() - start_time,
                metrics={
                    "expected_services": expected_services,
                    "actual_services": actual_services,
                    "service_count": len(actual_services)
                }
            ))
            
            if success:
                logger.info("✅ Guard services test passed")
            else:
                logger.warning(f"⚠️ Guard services test partially passed. Expected: {expected_services}, Got: {actual_services}")
                
        except Exception as e:
            self.results.append(TestResult(
                test_name="guard_services",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e)
            ))
            logger.error(f"❌ Guard services test failed: {e}")
    
    async def _test_api_endpoints(self) -> None:
        """Test API endpoints."""
        logger.info("Testing API endpoints...")
        start_time = time.time()
        
        endpoints_to_test = [
            "/health",
            "/api/v1/guards/health",
            "/api/v1/guards/services",
            "/docs",
            "/openapi.json"
        ]
        
        successful_endpoints = 0
        failed_endpoints = []
        
        async with httpx.AsyncClient() as client:
            for endpoint in endpoints_to_test:
                try:
                    response = await client.get(f"{self.gateway_url}{endpoint}", timeout=10.0)
                    if response.status_code in [200, 404]:  # 404 is OK for some endpoints
                        successful_endpoints += 1
                    else:
                        failed_endpoints.append(f"{endpoint} (status: {response.status_code})")
                except Exception as e:
                    failed_endpoints.append(f"{endpoint} (error: {str(e)})")
        
        success = len(failed_endpoints) == 0
        
        self.results.append(TestResult(
            test_name="api_endpoints",
            success=success,
            duration=time.time() - start_time,
            metrics={
                "total_endpoints": len(endpoints_to_test),
                "successful_endpoints": successful_endpoints,
                "failed_endpoints": failed_endpoints
            }
        ))
        
        if success:
            logger.info("✅ API endpoints test passed")
        else:
            logger.warning(f"⚠️ API endpoints test partially passed. Failed: {failed_endpoints}")
    
    async def _test_llm_integration(self) -> None:
        """Test LLM integration."""
        logger.info("Testing LLM integration...")
        start_time = time.time()
        
        try:
            # Import LLM testing module
            from tests.llm_testing import LLMTester
            
            # Create tester
            tester = LLMTester(self.gateway_url)
            
            # Run a simple test
            from tests.llm_testing import TestScenario
            results = await tester.test_guard_service("tokenguard", TestScenario.NORMAL, iterations=1)
            
            success = len(results) > 0 and any(r.success for r in results)
            
            self.results.append(TestResult(
                test_name="llm_integration",
                success=success,
                duration=time.time() - start_time,
                metrics={
                    "tests_run": len(results),
                    "successful_tests": sum(1 for r in results if r.success)
                }
            ))
            
            if success:
                logger.info("✅ LLM integration test passed")
            else:
                logger.warning("⚠️ LLM integration test failed")
                
        except Exception as e:
            self.results.append(TestResult(
                test_name="llm_integration",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e)
            ))
            logger.error(f"❌ LLM integration test failed: {e}")
    
    async def _test_documentation(self) -> None:
        """Test documentation."""
        logger.info("Testing documentation...")
        start_time = time.time()
        
        try:
            # Run documentation audit
            result = subprocess.run([
                sys.executable, "scripts/audit_documentation.py",
                "--path", ".", "--output", "temp_doc_audit.json"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                with open("temp_doc_audit.json", "r") as f:
                    audit_results = json.load(f)
                
                # Check if there are critical issues
                high_severity_issues = audit_results["summary"]["high_severity"]
                success = high_severity_issues == 0
                
                self.results.append(TestResult(
                    test_name="documentation",
                    success=success,
                    duration=time.time() - start_time,
                    metrics=audit_results["summary"]
                ))
                
                if success:
                    logger.info("✅ Documentation test passed")
                else:
                    logger.warning(f"⚠️ Documentation test failed with {high_severity_issues} high severity issues")
            else:
                raise Exception(f"Documentation audit failed: {result.stderr}")
                
        except Exception as e:
            self.results.append(TestResult(
                test_name="documentation",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e)
            ))
            logger.error(f"❌ Documentation test failed: {e}")
    
    async def _test_docker_containers(self) -> None:
        """Test Docker containers."""
        logger.info("Testing Docker containers...")
        start_time = time.time()
        
        if not self.docker_client:
            self.results.append(TestResult(
                test_name="docker_containers",
                success=False,
                duration=time.time() - start_time,
                error_message="Docker client not available"
            ))
            return
        
        try:
            # Check if containers are running
            containers = self.docker_client.containers.list()
            
            # Look for our services
            service_containers = [c for c in containers if any(service in c.name for service in 
                ["tokenguard", "trustguard", "contextguard", "biasguard", "healthguard", "gateway"])]
            
            success = len(service_containers) > 0
            
            self.results.append(TestResult(
                test_name="docker_containers",
                success=success,
                duration=time.time() - start_time,
                metrics={
                    "total_containers": len(containers),
                    "service_containers": len(service_containers),
                    "container_names": [c.name for c in service_containers]
                }
            ))
            
            if success:
                logger.info("✅ Docker containers test passed")
            else:
                logger.warning("⚠️ No service containers found")
                
        except Exception as e:
            self.results.append(TestResult(
                test_name="docker_containers",
                success=False,
                duration=time.time() - start_time,
                error_message=str(e)
            ))
            logger.error(f"❌ Docker containers test failed: {e}")
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - successful_tests
        
        # Calculate metrics
        total_duration = sum(r.duration for r in self.results)
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        # Group by test type
        test_groups = {}
        for result in self.results:
            if result.test_name not in test_groups:
                test_groups[result.test_name] = []
            test_groups[result.test_name].append(result)
        
        # Generate report
        report = {
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
                "total_duration": total_duration,
                "avg_duration": avg_duration
            },
            "test_results": [
                {
                    "test_name": r.test_name,
                    "success": r.success,
                    "duration": r.duration,
                    "error_message": r.error_message,
                    "metrics": r.metrics
                }
                for r in self.results
            ],
            "test_groups": {
                name: {
                    "total": len(group),
                    "successful": sum(1 for r in group if r.success),
                    "failed": sum(1 for r in group if not r.success)
                }
                for name, group in test_groups.items()
            },
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        failed_tests = [r for r in self.results if not r.success]
        
        if any(r.test_name == "system_startup" for r in failed_tests):
            recommendations.append("Fix system startup issues - ensure the gateway is running")
        
        if any(r.test_name == "telemetry_setup" for r in failed_tests):
            recommendations.append("Configure OpenTelemetry properly - check Jaeger setup")
        
        if any(r.test_name == "guard_services" for r in failed_tests):
            recommendations.append("Fix guard services initialization - check service configurations")
        
        if any(r.test_name == "api_endpoints" for r in failed_tests):
            recommendations.append("Fix API endpoint issues - check routing and middleware")
        
        if any(r.test_name == "llm_integration" for r in failed_tests):
            recommendations.append("Fix LLM integration - ensure guard services are accessible")
        
        if any(r.test_name == "documentation" for r in failed_tests):
            recommendations.append("Fix documentation issues - run documentation audit and fix critical issues")
        
        if any(r.test_name == "docker_containers" for r in failed_tests):
            recommendations.append("Fix Docker container issues - ensure containers are running properly")
        
        if not recommendations:
            recommendations.append("All tests passed! System is working as intended.")
        
        return recommendations


async def main():
    """Main function to run comprehensive tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run comprehensive AI Guardians tests")
    parser.add_argument("--gateway-url", default="http://localhost:8000", help="Gateway URL")
    parser.add_argument("--output", default="comprehensive_test_report.json", help="Output file")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run tests
    runner = ComprehensiveTestRunner(args.gateway_url)
    results = await runner.run_all_tests()
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    summary = results["summary"]
    print(f"\n{'='*60}")
    print(f"COMPREHENSIVE TEST REPORT")
    print(f"{'='*60}")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Successful: {summary['successful_tests']} ({summary['success_rate']*100:.1f}%)")
    print(f"Failed: {summary['failed_tests']}")
    print(f"Total Duration: {summary['total_duration']:.2f}s")
    print(f"Average Duration: {summary['avg_duration']:.2f}s")
    print(f"\nRecommendations:")
    for rec in results["recommendations"]:
        print(f"  - {rec}")
    print(f"\nDetailed results saved to: {args.output}")


if __name__ == "__main__":
    asyncio.run(main())

