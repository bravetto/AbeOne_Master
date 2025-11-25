"""
Comprehensive Test Runner for Trust Guard

Runs all tests and provides detailed reporting on system health and functionality.
"""

import pytest
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, List
import subprocess


class TestRunner:
    """Comprehensive test runner for Trust Guard system."""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        self.test_suites = [
            "tests/unit/test_comprehensive_core.py",
            "tests/unit/test_comprehensive_validation.py", 
            "tests/unit/test_comprehensive_constitutional.py",
            "tests/unit/test_comprehensive_metrics.py",
            "tests/unit/test_comprehensive_logging.py",
            "tests/unit/test_comprehensive_error_handling.py",
        ]
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites and collect results."""
        print("Starting Comprehensive Trust Guard Test Suite")
        print("=" * 60)
        
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        total_tests = 0
        
        for test_suite in self.test_suites:
            print(f"\nRunning {test_suite}...")
            suite_result = self._run_test_suite(test_suite)
            
            self.test_results[test_suite] = suite_result
            total_passed += suite_result["passed"]
            total_failed += suite_result["failed"]
            total_skipped += suite_result["skipped"]
            total_tests += suite_result["total"]
            
            status = "PASSED" if suite_result["failed"] == 0 else "FAILED"
            print(f"   {status} - {suite_result['passed']} passed, {suite_result['failed']} failed, {suite_result['skipped']} skipped")
        
        end_time = time.time()
        total_time = end_time - self.start_time
        
        summary = {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_skipped": total_skipped,
            "total_time": total_time,
            "success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
            "test_suites": self.test_results
        }
        
        self._print_summary(summary)
        return summary
    
    def _run_test_suite(self, test_suite: str) -> Dict[str, Any]:
        """Run a single test suite and return results."""
        try:
            # Run pytest with JSON output
            result = subprocess.run([
                sys.executable, "-m", "pytest", test_suite, 
                "--tb=short", "--json-report", "--json-report-file=/tmp/pytest_report.json"
            ], capture_output=True, text=True, timeout=300)
            
            # Parse results from stdout
            lines = result.stdout.split('\n')
            passed = 0
            failed = 0
            skipped = 0
            total = 0
            
            for line in lines:
                if "passed" in line and "failed" in line:
                    # Extract numbers from summary line
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "passed":
                            passed = int(parts[i-1])
                        elif part == "failed":
                            failed = int(parts[i-1])
                        elif part == "skipped":
                            skipped = int(parts[i-1])
                    total = passed + failed + skipped
                    break
            
            return {
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "total": total,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "passed": 0,
                "failed": 1,
                "skipped": 0,
                "total": 1,
                "return_code": -1,
                "stdout": "",
                "stderr": "Test suite timed out after 5 minutes"
            }
        except Exception as e:
            return {
                "passed": 0,
                "failed": 1,
                "skipped": 0,
                "total": 1,
                "return_code": -1,
                "stdout": "",
                "stderr": str(e)
            }
    
    def _print_summary(self, summary: Dict[str, Any]):
        """Print comprehensive test summary."""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['total_passed']}")
        print(f"Failed: {summary['total_failed']}")
        print(f"Skipped: {summary['total_skipped']}")
        print(f"Total Time: {summary['total_time']:.2f} seconds")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        
        if summary['total_failed'] > 0:
            print(f"\nFAILED TEST SUITES:")
            for suite, result in summary['test_suites'].items():
                if result['failed'] > 0:
                    print(f"   FAILED {suite}: {result['failed']} failures")
        
        print("\n" + "=" * 60)
        
        # Overall assessment
        if summary['success_rate'] >= 90:
            print("EXCELLENT: System is highly reliable and production-ready!")
        elif summary['success_rate'] >= 80:
            print("GOOD: System is mostly reliable with minor issues to address.")
        elif summary['success_rate'] >= 70:
            print("FAIR: System has some reliability issues that need attention.")
        else:
            print("POOR: System has significant reliability issues requiring immediate attention.")
        
        print("=" * 60)
    
    def generate_report(self, summary: Dict[str, Any], output_file: str = "test_report.json"):
        """Generate detailed JSON report."""
        report = {
            "timestamp": time.time(),
            "summary": summary,
            "recommendations": self._generate_recommendations(summary)
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nDetailed report saved to: {output_file}")
    
    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        if summary['success_rate'] < 90:
            recommendations.append("Focus on fixing failing tests to improve system reliability")
        
        if summary['total_failed'] > 0:
            recommendations.append("Review and fix error handling in components with test failures")
        
        if summary['total_time'] > 60:
            recommendations.append("Consider optimizing test performance for faster feedback")
        
        # Specific recommendations based on failing suites
        for suite, result in summary['test_suites'].items():
            if result['failed'] > 0:
                if "core" in suite:
                    recommendations.append("Review core detection algorithms and input handling")
                elif "validation" in suite:
                    recommendations.append("Check validation engine mathematical calculations")
                elif "metrics" in suite:
                    recommendations.append("Verify metrics collection and error handling")
                elif "logging" in suite:
                    recommendations.append("Ensure logging system handles all edge cases")
                elif "error_handling" in suite:
                    recommendations.append("Improve graceful degradation mechanisms")
        
        if not recommendations:
            recommendations.append("System is performing well - continue monitoring and maintenance")
        
        return recommendations


def main():
    """Main entry point for test runner."""
    runner = TestRunner()
    
    try:
        summary = runner.run_all_tests()
        runner.generate_report(summary)
        
        # Exit with appropriate code
        if summary['total_failed'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\nTest run interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nTest runner failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
