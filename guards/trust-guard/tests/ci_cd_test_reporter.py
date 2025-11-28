#!/usr/bin/env python3
"""
CI/CD Test Reporter for Trust Guard

Generates comprehensive test reports in structured MD format with log scraping
and health check integration for CI/CD pipelines.
"""

import os
import sys
import json
import time
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CICDTestReporter:
    """Comprehensive CI/CD test reporter with log scraping and health checks."""
    
    def __init__(self, base_url: str = "http://localhost:8000", output_dir: str = "test-results"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_data = {
            "timestamp": datetime.now().isoformat(),
            "test_results": {},
            "health_checks": {},
            "log_analysis": {},
            "performance_metrics": {},
            "summary": {}
        }
    
    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite and generate report."""
        logger.info("Starting comprehensive CI/CD test suite...")
        
        # Run unit tests
        self._run_unit_tests()
        
        # Run integration tests
        self._run_integration_tests()
        
        # Run health checks
        self._run_health_checks()
        
        # Scrape logs
        self._scrape_logs()
        
        # Run performance tests
        self._run_performance_tests()
        
        # Generate report
        self._generate_report()
        
        return self.report_data
    
    def _run_unit_tests(self):
        """Run unit tests and capture results."""
        logger.info("Running unit tests...")
        
        test_suites = [
            "tests/unit/test_comprehensive_core.py",
            "tests/unit/test_comprehensive_validation.py",
            "tests/unit/test_comprehensive_constitutional.py",
            "tests/unit/test_comprehensive_metrics.py",
            "tests/unit/test_comprehensive_logging.py",
            "tests/unit/test_comprehensive_error_handling.py"
        ]
        
        unit_test_results = {}
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        
        for test_suite in test_suites:
            if os.path.exists(test_suite):
                try:
                    result = subprocess.run([
                        sys.executable, "-m", "pytest", test_suite, 
                        "--tb=short", "--json-report", "--json-report-file=/tmp/pytest_report.json"
                    ], capture_output=True, text=True, timeout=300)
                    
                    # Parse results from stdout
                    lines = result.stdout.split('\n')
                    passed = 0
                    failed = 0
                    skipped = 0
                    
                    for line in lines:
                        if "passed" in line and "failed" in line:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part == "passed":
                                    passed = int(parts[i-1])
                                elif part == "failed":
                                    failed = int(parts[i-1])
                                elif part == "skipped":
                                    skipped = int(parts[i-1])
                            break
                    
                    unit_test_results[test_suite] = {
                        "passed": passed,
                        "failed": failed,
                        "skipped": skipped,
                        "return_code": result.returncode,
                        "stdout": result.stdout,
                        "stderr": result.stderr
                    }
                    
                    total_passed += passed
                    total_failed += failed
                    total_skipped += skipped
                    
                except subprocess.TimeoutExpired:
                    unit_test_results[test_suite] = {
                        "passed": 0,
                        "failed": 1,
                        "skipped": 0,
                        "return_code": -1,
                        "stdout": "",
                        "stderr": "Test suite timed out after 5 minutes"
                    }
                    total_failed += 1
                except Exception as e:
                    unit_test_results[test_suite] = {
                        "passed": 0,
                        "failed": 1,
                        "skipped": 0,
                        "return_code": -1,
                        "stdout": "",
                        "stderr": str(e)
                    }
                    total_failed += 1
        
        self.report_data["test_results"]["unit_tests"] = {
            "suites": unit_test_results,
            "summary": {
                "total_passed": total_passed,
                "total_failed": total_failed,
                "total_skipped": total_skipped,
                "total_tests": total_passed + total_failed + total_skipped,
                "success_rate": (total_passed / (total_passed + total_failed + total_skipped) * 100) if (total_passed + total_failed + total_skipped) > 0 else 0
            }
        }
    
    def _run_integration_tests(self):
        """Run integration tests against the running service."""
        logger.info("Running integration tests...")
        
        integration_tests = {}
        
        # Test health endpoint
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            integration_tests["health_endpoint"] = {
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "response_data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
        except Exception as e:
            integration_tests["health_endpoint"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        # Test liveness probe
        try:
            response = requests.get(f"{self.base_url}/health/live", timeout=10)
            integration_tests["liveness_probe"] = {
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000
            }
        except Exception as e:
            integration_tests["liveness_probe"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        # Test readiness probe
        try:
            response = requests.get(f"{self.base_url}/health/ready", timeout=10)
            integration_tests["readiness_probe"] = {
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000
            }
        except Exception as e:
            integration_tests["readiness_probe"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        # Test detailed health check
        try:
            response = requests.get(f"{self.base_url}/health/detailed", timeout=10)
            integration_tests["detailed_health"] = {
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "response_data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
        except Exception as e:
            integration_tests["detailed_health"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        # Test metrics endpoint
        try:
            response = requests.get(f"{self.base_url}/metrics", timeout=10)
            integration_tests["metrics_endpoint"] = {
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "content_type": response.headers.get('content-type', '')
            }
        except Exception as e:
            integration_tests["metrics_endpoint"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        # Test API endpoints (if authentication is available)
        try:
            # Test detect endpoint with sample data
            test_data = {
                "text": "This is a test message for pattern detection.",
                "context": "Testing context",
                "metadata": {"test": True}
            }
            response = requests.post(f"{self.base_url}/v1/detect", json=test_data, timeout=30)
            integration_tests["detect_endpoint"] = {
                "status": "PASS" if response.status_code in [200, 401, 403] else "FAIL",  # 401/403 are acceptable for auth
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000
            }
        except Exception as e:
            integration_tests["detect_endpoint"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        self.report_data["test_results"]["integration_tests"] = integration_tests
    
    def _run_health_checks(self):
        """Run comprehensive health checks."""
        logger.info("Running health checks...")
        
        health_checks = {}
        
        try:
            # Basic health check
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                health_checks["basic_health"] = {
                    "status": "PASS",
                    "overall_status": health_data.get("status", "unknown"),
                    "uptime_seconds": health_data.get("uptime_seconds", 0),
                    "components": health_data.get("components", [])
                }
            else:
                health_checks["basic_health"] = {
                    "status": "FAIL",
                    "status_code": response.status_code
                }
        except Exception as e:
            health_checks["basic_health"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        try:
            # Detailed health check
            response = requests.get(f"{self.base_url}/health/detailed", timeout=10)
            if response.status_code == 200:
                detailed_health = response.json()
                health_checks["detailed_health"] = {
                    "status": "PASS",
                    "overall_status": detailed_health.get("status", "unknown"),
                    "summary": detailed_health.get("summary", {}),
                    "components": detailed_health.get("components", [])
                }
            else:
                health_checks["detailed_health"] = {
                    "status": "FAIL",
                    "status_code": response.status_code
                }
        except Exception as e:
            health_checks["detailed_health"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        try:
            # Tracer health check
            response = requests.get(f"{self.base_url}/v1/tracer/health", timeout=10)
            if response.status_code == 200:
                tracer_health = response.json()
                health_checks["tracer_health"] = {
                    "status": "PASS",
                    "health_score": tracer_health.get("health_score", 0),
                    "total_bullets": tracer_health.get("total_bullets", 0),
                    "error_count": tracer_health.get("error_count", 0)
                }
            else:
                health_checks["tracer_health"] = {
                    "status": "FAIL",
                    "status_code": response.status_code
                }
        except Exception as e:
            health_checks["tracer_health"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        self.report_data["health_checks"] = health_checks
    
    def _scrape_logs(self):
        """Scrape and analyze logs from the service."""
        logger.info("Scraping and analyzing logs...")
        
        log_analysis = {
            "log_sources": [],
            "error_patterns": [],
            "performance_metrics": [],
            "security_events": []
        }
        
        # Look for log files in common locations
        log_locations = [
            "logs/",
            "*.log",
            "/var/log/trustguard/",
            "/tmp/trustguard.log"
        ]
        
        for location in log_locations:
            if os.path.exists(location):
                if os.path.isfile(location):
                    log_files = [location]
                else:
                    log_files = list(Path(location).glob("*.log"))
                
                for log_file in log_files:
                    try:
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            log_content = f.read()
                            
                        # Analyze log content
                        analysis = self._analyze_log_content(log_content)
                        log_analysis["log_sources"].append({
                            "file": str(log_file),
                            "size_bytes": os.path.getsize(log_file),
                            "analysis": analysis
                        })
                    except Exception as e:
                        logger.warning(f"Could not read log file {log_file}: {e}")
        
        # Analyze recent tracer bullets if available
        try:
            response = requests.get(f"{self.base_url}/v1/tracer/bullets?count=1000", timeout=10)
            if response.status_code == 200:
                tracer_data = response.json()
                bullets = tracer_data.get("bullets", [])
                
                # Analyze tracer bullets
                error_bullets = [b for b in bullets if "error" in b.get("event_type", "")]
                performance_bullets = [b for b in bullets if "performance" in b.get("event_type", "")]
                security_bullets = [b for b in bullets if "security" in b.get("event_type", "")]
                
                log_analysis["tracer_analysis"] = {
                    "total_bullets": len(bullets),
                    "error_bullets": len(error_bullets),
                    "performance_bullets": len(performance_bullets),
                    "security_bullets": len(security_bullets),
                    "recent_errors": error_bullets[-10:] if error_bullets else [],
                    "recent_performance": performance_bullets[-10:] if performance_bullets else []
                }
        except Exception as e:
            logger.warning(f"Could not fetch tracer bullets: {e}")
        
        self.report_data["log_analysis"] = log_analysis
    
    def _analyze_log_content(self, log_content: str) -> Dict[str, Any]:
        """Analyze log content for patterns and metrics."""
        analysis = {
            "total_lines": len(log_content.split('\n')),
            "error_count": 0,
            "warning_count": 0,
            "info_count": 0,
            "performance_entries": 0,
            "security_events": 0
        }
        
        lines = log_content.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            
            if 'error' in line_lower:
                analysis["error_count"] += 1
            elif 'warning' in line_lower or 'warn' in line_lower:
                analysis["warning_count"] += 1
            elif 'info' in line_lower:
                analysis["info_count"] += 1
            
            if 'performance' in line_lower or 'duration' in line_lower:
                analysis["performance_entries"] += 1
            
            if 'security' in line_lower or 'auth' in line_lower:
                analysis["security_events"] += 1
        
        return analysis
    
    def _run_performance_tests(self):
        """Run performance tests."""
        logger.info("Running performance tests...")
        
        performance_tests = {}
        
        # Test response times for different endpoints
        endpoints = [
            ("/health", "GET"),
            ("/health/live", "GET"),
            ("/health/ready", "GET"),
            ("/metrics", "GET")
        ]
        
        for endpoint, method in endpoints:
            try:
                start_time = time.time()
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", timeout=10)
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to ms
                
                performance_tests[endpoint] = {
                    "status": "PASS" if response.status_code in [200, 401, 403] else "FAIL",
                    "response_time_ms": response_time,
                    "status_code": response.status_code,
                    "content_length": len(response.content)
                }
            except Exception as e:
                performance_tests[endpoint] = {
                    "status": "FAIL",
                    "error": str(e)
                }
        
        # Load test simulation (simple)
        try:
            start_time = time.time()
            successful_requests = 0
            failed_requests = 0
            
            for i in range(10):  # Simple load test with 10 requests
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=5)
                    if response.status_code == 200:
                        successful_requests += 1
                    else:
                        failed_requests += 1
                except:
                    failed_requests += 1
            
            end_time = time.time()
            total_time = end_time - start_time
            
            performance_tests["load_test"] = {
                "status": "PASS" if failed_requests == 0 else "FAIL",
                "total_requests": 10,
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "total_time_seconds": total_time,
                "requests_per_second": 10 / total_time if total_time > 0 else 0
            }
        except Exception as e:
            performance_tests["load_test"] = {
                "status": "FAIL",
                "error": str(e)
            }
        
        self.report_data["performance_metrics"] = performance_tests
    
    def _generate_report(self):
        """Generate comprehensive test report in MD format."""
        logger.info("Generating comprehensive test report...")
        
        # Calculate summary
        self._calculate_summary()
        
        # Generate markdown report
        self._generate_markdown_report()
        
        # Generate JSON report
        self._generate_json_report()
    
    def _calculate_summary(self):
        """Calculate overall test summary."""
        summary = {
            "overall_status": "PASS",
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "success_rate": 0.0,
            "health_status": "UNKNOWN",
            "performance_status": "UNKNOWN"
        }
        
        # Calculate unit test summary
        if "unit_tests" in self.report_data["test_results"]:
            unit_summary = self.report_data["test_results"]["unit_tests"]["summary"]
            summary["total_tests"] += unit_summary["total_tests"]
            summary["passed_tests"] += unit_summary["total_passed"]
            summary["failed_tests"] += unit_summary["total_failed"]
        
        # Calculate integration test summary
        if "integration_tests" in self.report_data["test_results"]:
            integration_tests = self.report_data["test_results"]["integration_tests"]
            for test_name, test_result in integration_tests.items():
                summary["total_tests"] += 1
                if test_result["status"] == "PASS":
                    summary["passed_tests"] += 1
                else:
                    summary["failed_tests"] += 1
        
        # Calculate success rate
        if summary["total_tests"] > 0:
            summary["success_rate"] = (summary["passed_tests"] / summary["total_tests"]) * 100
        
        # Determine overall status
        if summary["failed_tests"] > 0:
            summary["overall_status"] = "FAIL"
        
        # Determine health status
        if "health_checks" in self.report_data:
            health_checks = self.report_data["health_checks"]
            failed_health = sum(1 for check in health_checks.values() if check["status"] == "FAIL")
            if failed_health == 0:
                summary["health_status"] = "HEALTHY"
            elif failed_health < len(health_checks) / 2:
                summary["health_status"] = "DEGRADED"
            else:
                summary["health_status"] = "UNHEALTHY"
        
        # Determine performance status
        if "performance_metrics" in self.report_data:
            perf_tests = self.report_data["performance_metrics"]
            failed_perf = sum(1 for test in perf_tests.values() if test["status"] == "FAIL")
            if failed_perf == 0:
                summary["performance_status"] = "GOOD"
            elif failed_perf < len(perf_tests) / 2:
                summary["performance_status"] = "DEGRADED"
            else:
                summary["performance_status"] = "POOR"
        
        self.report_data["summary"] = summary
    
    def _generate_markdown_report(self):
        """Generate markdown test report."""
        report_file = self.output_dir / f"test_report_{self.timestamp}.md"
        
        with open(report_file, 'w') as f:
            f.write(self._get_markdown_content())
        
        logger.info(f"Markdown report generated: {report_file}")
    
    def _get_markdown_content(self) -> str:
        """Generate markdown content for the test report."""
        summary = self.report_data["summary"]
        
        content = f"""# Trust Guard CI/CD Test Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Test Run ID:** {self.timestamp}  
**Overall Status:** {summary['overall_status']}  

## Executive Summary

| Metric | Value |
|--------|-------|
| **Overall Status** | {summary['overall_status']} |
| **Total Tests** | {summary['total_tests']} |
| **Passed Tests** | {summary['passed_tests']} |
| **Failed Tests** | {summary['failed_tests']} |
| **Success Rate** | {summary['success_rate']:.1f}% |
| **Health Status** | {summary['health_status']} |
| **Performance Status** | {summary['performance_status']} |

## Test Results

### Unit Tests

"""
        
        # Add unit test results
        if "unit_tests" in self.report_data["test_results"]:
            unit_tests = self.report_data["test_results"]["unit_tests"]
            content += f"""
| Test Suite | Passed | Failed | Skipped | Status |
|------------|--------|--------|---------|--------|
"""
            for suite_name, suite_result in unit_tests["suites"].items():
                status = "PASS" if suite_result["failed"] == 0 else "FAIL"
                content += f"| {suite_name} | {suite_result['passed']} | {suite_result['failed']} | {suite_result['skipped']} | {status} |\n"
        
        content += """
### Integration Tests

| Test | Status | Response Time (ms) | Details |
|------|--------|-------------------|---------|
"""
        
        # Add integration test results
        if "integration_tests" in self.report_data["test_results"]:
            integration_tests = self.report_data["test_results"]["integration_tests"]
            for test_name, test_result in integration_tests.items():
                response_time = test_result.get("response_time_ms", "N/A")
                details = test_result.get("error", "OK")
                content += f"| {test_name} | {test_result['status']} | {response_time} | {details} |\n"
        
        content += """
## Health Checks

| Check | Status | Details |
|-------|--------|---------|
"""
        
        # Add health check results
        if "health_checks" in self.report_data:
            health_checks = self.report_data["health_checks"]
            for check_name, check_result in health_checks.items():
                details = check_result.get("overall_status", check_result.get("error", "OK"))
                content += f"| {check_name} | {check_result['status']} | {details} |\n"
        
        content += """
## Performance Metrics

| Endpoint | Status | Response Time (ms) | Status Code |
|----------|--------|-------------------|-------------|
"""
        
        # Add performance test results
        if "performance_metrics" in self.report_data:
            perf_tests = self.report_data["performance_metrics"]
            for endpoint, test_result in perf_tests.items():
                if endpoint != "load_test":
                    response_time = test_result.get("response_time_ms", "N/A")
                    status_code = test_result.get("status_code", "N/A")
                    content += f"| {endpoint} | {test_result['status']} | {response_time} | {status_code} |\n"
        
        content += """
## Log Analysis

"""
        
        # Add log analysis
        if "log_analysis" in self.report_data:
            log_analysis = self.report_data["log_analysis"]
            if "tracer_analysis" in log_analysis:
                tracer = log_analysis["tracer_analysis"]
                content += f"""
### Tracer Bullets Analysis

- **Total Bullets:** {tracer.get('total_bullets', 0)}
- **Error Bullets:** {tracer.get('error_bullets', 0)}
- **Performance Bullets:** {tracer.get('performance_bullets', 0)}
- **Security Bullets:** {tracer.get('security_bullets', 0)}

"""
        
        content += """
## Recommendations

"""
        
        # Add recommendations based on results
        recommendations = []
        
        if summary["failed_tests"] > 0:
            recommendations.append("Address failed tests to improve system reliability")
        
        if summary["health_status"] != "HEALTHY":
            recommendations.append("Investigate and resolve health check issues")
        
        if summary["performance_status"] != "GOOD":
            recommendations.append("Optimize performance for better response times")
        
        if not recommendations:
            recommendations.append("System is performing well - continue monitoring")
        
        for i, rec in enumerate(recommendations, 1):
            content += f"{i}. {rec}\n"
        
        content += f"""
## Report Metadata

- **Report Generated:** {datetime.now().isoformat()}
- **Test Environment:** CI/CD Pipeline
- **Base URL:** {self.base_url}
- **Output Directory:** {self.output_dir}

---
*This report was generated automatically by the Trust Guard CI/CD Test Reporter*
"""
        
        return content
    
    def _generate_json_report(self):
        """Generate JSON test report."""
        report_file = self.output_dir / f"test_report_{self.timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.report_data, f, indent=2)
        
        logger.info(f"JSON report generated: {report_file}")


def main():
    """Main entry point for CI/CD test reporter."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Trust Guard CI/CD Test Reporter")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of the service")
    parser.add_argument("--output-dir", default="test-results", help="Output directory for reports")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    reporter = CICDTestReporter(base_url=args.base_url, output_dir=args.output_dir)
    
    try:
        report_data = reporter.run_comprehensive_tests()
        
        # Exit with appropriate code
        if report_data["summary"]["overall_status"] == "PASS":
            logger.info("All tests passed successfully")
            sys.exit(0)
        else:
            logger.error("Some tests failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Test run interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Test reporter failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
