#!/usr/bin/env python3
"""
Deployment validation script for Trust Guard.

Runs comprehensive checks to ensure production readiness including:
- Unit test execution
- API endpoint testing
- Health check validation
- Performance benchmarking
- Security validation
- Configuration validation
"""

import argparse
import json
import subprocess
import sys
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DeploymentValidator:
    """Comprehensive deployment validation for Trust Guard."""
    
    def __init__(self, base_url: str, output_dir: str, verbose: bool = False):
        """Initialize the deployment validator.
        
        Args:
            base_url: Base URL of the Trust Guard service
            output_dir: Directory to save validation results
            verbose: Enable verbose logging
        """
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        self.verbose = verbose
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'tests': {},
            'summary': {},
            'recommendations': []
        }
        
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
    
    def run_validation(self) -> Dict[str, Any]:
        """Run complete deployment validation.
        
        Returns:
            Dict containing validation results and recommendations
        """
        logger.info("Starting Trust Guard deployment validation...")
        
        # Run all validation tests
        self._validate_unit_tests()
        self._validate_integration_tests()
        self._validate_health_endpoints()
        self._validate_metrics_endpoint()
        self._validate_authentication()
        self._validate_performance()
        self._validate_security()
        self._validate_configuration()
        
        # Generate summary and recommendations
        self._generate_summary()
        self._generate_recommendations()
        
        # Save results
        self._save_results()
        
        logger.info("Deployment validation completed!")
        return self.results
    
    def _validate_unit_tests(self) -> None:
        """Run unit tests and validate results."""
        logger.info("Running unit tests...")
        
        try:
            # Run pytest with JSON output
            result = subprocess.run([
                'python', '-m', 'pytest', 
                'tests/unit/', 
                '--json-report', 
                '--json-report-file', f'{self.output_dir}/unit_test_results.json',
                '-v'
            ], capture_output=True, text=True, timeout=300)
            
            # Parse results
            test_results = {
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'total': 0
            }
            
            # Try to parse JSON report
            try:
                with open(f'{self.output_dir}/unit_test_results.json', 'r') as f:
                    json_report = json.load(f)
                    test_results.update({
                        'passed': json_report.get('summary', {}).get('passed', 0),
                        'failed': json_report.get('summary', {}).get('failed', 0),
                        'skipped': json_report.get('summary', {}).get('skipped', 0),
                        'total': json_report.get('summary', {}).get('total', 0)
                    })
            except (FileNotFoundError, json.JSONDecodeError):
                logger.warning("Could not parse JSON test report")
            
            self.results['tests']['unit_tests'] = test_results
            
            # Check if tests passed
            if result.returncode == 0 and test_results['failed'] == 0:
                logger.info(f"Unit tests passed: {test_results['passed']}/{test_results['total']}")
            else:
                logger.error(f"Unit tests failed: {test_results['failed']}/{test_results['total']}")
                
        except subprocess.TimeoutExpired:
            logger.error("Unit tests timed out after 5 minutes")
            self.results['tests']['unit_tests'] = {
                'exit_code': -1,
                'error': 'Timeout',
                'passed': 0,
                'failed': 0,
                'total': 0
            }
        except Exception as e:
            logger.error(f"Error running unit tests: {e}")
            self.results['tests']['unit_tests'] = {
                'exit_code': -1,
                'error': str(e),
                'passed': 0,
                'failed': 0,
                'total': 0
            }
    
    def _validate_integration_tests(self) -> None:
        """Test API endpoints for integration validation."""
        logger.info("Running integration tests...")
        
        endpoints = [
            '/health',
            '/health/live',
            '/health/ready',
            '/health/detailed',
            '/metrics',
            '/v1/detect',
            '/v1/validate',
            '/v1/mitigate',
            '/v1/constitutional'
        ]
        
        integration_results = {}
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                
                if endpoint in ['/v1/detect', '/v1/validate', '/v1/mitigate', '/v1/constitutional']:
                    # These endpoints require authentication
                    response = self._test_authenticated_endpoint(endpoint)
                else:
                    # Public endpoints
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                
                response_time = time.time() - start_time
                
                integration_results[endpoint] = {
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'success': response.status_code == 200,
                    'content_length': len(response.content) if response.content else 0
                }
                
                if response.status_code == 200:
                    logger.info(f"✓ {endpoint} - {response.status_code} ({response_time:.3f}s)")
                else:
                    logger.warning(f"✗ {endpoint} - {response.status_code} ({response_time:.3f}s)")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"✗ {endpoint} - Connection error: {e}")
                integration_results[endpoint] = {
                    'status_code': 0,
                    'response_time': 0,
                    'success': False,
                    'error': str(e)
                }
        
        self.results['tests']['integration_tests'] = integration_results
    
    def _test_authenticated_endpoint(self, endpoint: str) -> requests.Response:
        """Test an endpoint that requires authentication."""
        # First, get an API key from the debug endpoint
        try:
            debug_response = requests.get(f"{self.base_url}/debug/api-key", timeout=5)
            if debug_response.status_code == 200:
                api_key = debug_response.json().get('api_key')
                if api_key:
                    headers = {'X-API-Key': api_key}
                    
                    if endpoint == '/v1/detect':
                        data = {'text': 'This is a test message for validation'}
                        return requests.post(f"{self.base_url}{endpoint}", 
                                           json=data, headers=headers, timeout=10)
                    else:
                        return requests.get(f"{self.base_url}{endpoint}", 
                                          headers=headers, timeout=10)
        except Exception:
            pass
        
        # Fallback: try without authentication (should return 401)
        return requests.get(f"{self.base_url}{endpoint}", timeout=10)
    
    def _validate_health_endpoints(self) -> None:
        """Validate health check endpoints."""
        logger.info("Validating health endpoints...")
        
        health_endpoints = {
            '/health': {'max_response_time': 0.1, 'required_fields': ['status', 'timestamp']},
            '/health/live': {'max_response_time': 0.05, 'required_fields': ['status']},
            '/health/ready': {'max_response_time': 0.05, 'required_fields': ['status']},
            '/health/detailed': {'max_response_time': 0.2, 'required_fields': ['status', 'components']}
        }
        
        health_results = {}
        
        for endpoint, criteria in health_endpoints.items():
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                response_time = time.time() - start_time
                
                result = {
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'meets_time_criteria': response_time <= criteria['max_response_time'],
                    'success': response.status_code == 200
                }
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        result['has_required_fields'] = all(
                            field in data for field in criteria['required_fields']
                        )
                        result['data'] = data
                    except json.JSONDecodeError:
                        result['has_required_fields'] = False
                        result['error'] = 'Invalid JSON response'
                else:
                    result['has_required_fields'] = False
                
                health_results[endpoint] = result
                
                if result['success'] and result['meets_time_criteria']:
                    logger.info(f"✓ {endpoint} - Healthy ({response_time:.3f}s)")
                else:
                    logger.warning(f"✗ {endpoint} - Issues detected")
                    
            except Exception as e:
                logger.error(f"✗ {endpoint} - Error: {e}")
                health_results[endpoint] = {
                    'status_code': 0,
                    'response_time': 0,
                    'success': False,
                    'error': str(e)
                }
        
        self.results['tests']['health_endpoints'] = health_results
    
    def _validate_metrics_endpoint(self) -> None:
        """Validate Prometheus metrics endpoint."""
        logger.info("Validating metrics endpoint...")
        
        try:
            response = requests.get(f"{self.base_url}/metrics", timeout=10)
            
            metrics_result = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'content_type': response.headers.get('content-type', ''),
                'content_length': len(response.content)
            }
            
            if response.status_code == 200:
                content = response.text
                
                # Check for Prometheus format
                metrics_result['is_prometheus_format'] = '# HELP' in content and '# TYPE' in content
                
                # Check for Trust Guard specific metrics
                trustguard_metrics = [
                    'trustguard_requests_total',
                    'REPLACE_ME',
                    'REPLACE_ME'
                ]
                
                found_metrics = [metric for metric in trustguard_metrics if metric in content]
                metrics_result['trustguard_metrics_found'] = found_metrics
                metrics_result['trustguard_metrics_count'] = len(found_metrics)
                
                logger.info(f"✓ Metrics endpoint - {len(found_metrics)} Trust Guard metrics found")
            else:
                logger.error(f"✗ Metrics endpoint - Status {response.status_code}")
                
        except Exception as e:
            logger.error(f"✗ Metrics endpoint - Error: {e}")
            metrics_result = {
                'status_code': 0,
                'success': False,
                'error': str(e)
            }
        
        self.results['tests']['metrics_endpoint'] = metrics_result
    
    def _validate_authentication(self) -> None:
        """Validate authentication system."""
        logger.info("Validating authentication...")
        
        auth_results = {}
        
        # Test without API key (should return 401)
        try:
            response = requests.post(f"{self.base_url}/v1/detect", 
                                   json={'text': 'test'}, timeout=5)
            auth_results['no_auth_returns_401'] = response.status_code == 401
        except Exception as e:
            auth_results['no_auth_returns_401'] = False
            auth_results['no_auth_error'] = str(e)
        
        # Test with invalid API key (should return 401)
        try:
            headers = {'X-API-Key': 'invalid-key'}
            response = requests.post(f"{self.base_url}/v1/detect", 
                                   json={'text': 'test'}, headers=headers, timeout=5)
            auth_results['invalid_auth_returns_401'] = response.status_code == 401
        except Exception as e:
            auth_results['invalid_auth_returns_401'] = False
            auth_results['invalid_auth_error'] = str(e)
        
        # Test with valid API key (should return 200)
        try:
            debug_response = requests.get(f"{self.base_url}/debug/api-key", timeout=5)
            if debug_response.status_code == 200:
                api_key = debug_response.json().get('api_key')
                if api_key:
                    headers = {'X-API-Key': api_key}
                    response = requests.post(f"{self.base_url}/v1/detect", 
                                           json={'text': 'test'}, headers=headers, timeout=10)
                    auth_results['valid_auth_returns_200'] = response.status_code == 200
                    auth_results['valid_auth_response_time'] = response.elapsed.total_seconds()
                else:
                    auth_results['valid_auth_returns_200'] = False
                    auth_results['valid_auth_error'] = 'No API key returned'
            else:
                auth_results['valid_auth_returns_200'] = False
                auth_results['valid_auth_error'] = 'Debug endpoint not accessible'
        except Exception as e:
            auth_results['valid_auth_returns_200'] = False
            auth_results['valid_auth_error'] = str(e)
        
        self.results['tests']['authentication'] = auth_results
        
        # Log results
        if all([
            auth_results.get('no_auth_returns_401', False),
            auth_results.get('invalid_auth_returns_401', False),
            auth_results.get('valid_auth_returns_200', False)
        ]):
            logger.info("✓ Authentication system working correctly")
        else:
            logger.warning("✗ Authentication system has issues")
    
    def _validate_performance(self) -> None:
        """Run basic performance tests."""
        logger.info("Running performance tests...")
        
        performance_results = {}
        
        # Test health endpoint performance
        health_times = []
        for _ in range(10):
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}/health", timeout=5)
                response_time = time.time() - start_time
                if response.status_code == 200:
                    health_times.append(response_time)
            except Exception:
                pass
        
        if health_times:
            performance_results['health_endpoint'] = {
                'avg_response_time': sum(health_times) / len(health_times),
                'max_response_time': max(health_times),
                'min_response_time': min(health_times),
                'samples': len(health_times)
            }
        
        # Test detect endpoint performance (if authentication works)
        try:
            debug_response = requests.get(f"{self.base_url}/debug/api-key", timeout=5)
            if debug_response.status_code == 200:
                api_key = debug_response.json().get('api_key')
                if api_key:
                    headers = {'X-API-Key': api_key}
                    detect_times = []
                    
                    for _ in range(5):  # Fewer samples for authenticated endpoint
                        try:
                            start_time = time.time()
                            response = requests.post(f"{self.base_url}/v1/detect", 
                                                   json={'text': 'Performance test message'}, 
                                                   headers=headers, timeout=10)
                            response_time = time.time() - start_time
                            if response.status_code == 200:
                                detect_times.append(response_time)
                        except Exception:
                            pass
                    
                    if detect_times:
                        performance_results['detect_endpoint'] = {
                            'avg_response_time': sum(detect_times) / len(detect_times),
                            'max_response_time': max(detect_times),
                            'min_response_time': min(detect_times),
                            'samples': len(detect_times)
                        }
        except Exception:
            pass
        
        self.results['tests']['performance'] = performance_results
        
        # Log results
        if 'health_endpoint' in performance_results:
            avg_time = performance_results['health_endpoint']['avg_response_time']
            if avg_time < 0.1:
                logger.info(f"✓ Health endpoint performance: {avg_time:.3f}s average")
            else:
                logger.warning(f"⚠ Health endpoint performance: {avg_time:.3f}s average (slow)")
        
        if 'detect_endpoint' in performance_results:
            avg_time = performance_results['detect_endpoint']['avg_response_time']
            if avg_time < 2.0:
                logger.info(f"✓ Detect endpoint performance: {avg_time:.3f}s average")
            else:
                logger.warning(f"⚠ Detect endpoint performance: {avg_time:.3f}s average (slow)")
    
    def _validate_security(self) -> None:
        """Validate security configuration."""
        logger.info("Validating security configuration...")
        
        security_results = {}
        
        # Check for security headers
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            headers = response.headers
            
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security'
            ]
            
            found_headers = [header for header in security_headers if header in headers]
            security_results['security_headers'] = {
                'found': found_headers,
                'count': len(found_headers),
                'total_expected': len(security_headers)
            }
            
        except Exception as e:
            security_results['security_headers'] = {'error': str(e)}
        
        # Check CORS headers
        try:
            response = requests.options(f"{self.base_url}/health", timeout=5)
            cors_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers'
            ]
            
            found_cors = [header for header in cors_headers if header in response.headers]
            security_results['cors_headers'] = {
                'found': found_cors,
                'count': len(found_cors)
            }
            
        except Exception as e:
            security_results['cors_headers'] = {'error': str(e)}
        
        self.results['tests']['security'] = security_results
        
        # Log results
        if 'security_headers' in security_results and 'count' in security_results['security_headers']:
            count = security_results['security_headers']['count']
            if count >= 2:
                logger.info(f"✓ Security headers: {count} found")
            else:
                logger.warning(f"⚠ Security headers: Only {count} found")
    
    def _validate_configuration(self) -> None:
        """Validate configuration settings."""
        logger.info("Validating configuration...")
        
        config_results = {}
        
        # Check if debug endpoint is accessible (should be disabled in production)
        try:
            response = requests.get(f"{self.base_url}/debug/api-key", timeout=5)
            config_results['debug_endpoint_accessible'] = response.status_code == 200
            if response.status_code == 200:
                logger.warning("⚠ Debug endpoint is accessible (should be disabled in production)")
            else:
                logger.info("✓ Debug endpoint is not accessible")
        except Exception:
            config_results['debug_endpoint_accessible'] = False
            logger.info("✓ Debug endpoint is not accessible")
        
        # Check log level (if accessible through health endpoint)
        try:
            response = requests.get(f"{self.base_url}/health/detailed", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'configuration' in data:
                    log_level = data['configuration'].get('log_level', 'unknown')
                    config_results['log_level'] = log_level
                    if log_level in ['WARNING', 'ERROR']:
                        logger.info(f"✓ Log level: {log_level} (appropriate for production)")
                    else:
                        logger.warning(f"⚠ Log level: {log_level} (consider WARNING or ERROR for production)")
        except Exception:
            pass
        
        self.results['tests']['configuration'] = config_results
    
    def _generate_summary(self) -> None:
        """Generate validation summary."""
        summary = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'overall_success': False
        }
        
        # Count test results
        for test_category, results in self.results['tests'].items():
            if isinstance(results, dict):
                if 'success' in results:
                    summary['total_tests'] += 1
                    if results['success']:
                        summary['passed_tests'] += 1
                    else:
                        summary['failed_tests'] += 1
                elif 'exit_code' in results:  # Unit tests
                    summary['total_tests'] += 1
                    if results['exit_code'] == 0:
                        summary['passed_tests'] += 1
                    else:
                        summary['failed_tests'] += 1
        
        # Calculate success rate
        if summary['total_tests'] > 0:
            success_rate = (summary['passed_tests'] / summary['total_tests']) * 100
            summary['success_rate'] = success_rate
            summary['overall_success'] = success_rate >= 90
        
        self.results['summary'] = summary
        
        # Log summary
        logger.info(f"Validation Summary: {summary['passed_tests']}/{summary['total_tests']} tests passed ({summary.get('success_rate', 0):.1f}%)")
        
        if summary['overall_success']:
            logger.info("✓ Deployment validation PASSED - Ready for production")
        else:
            logger.warning("✗ Deployment validation FAILED - Not ready for production")
    
    def _generate_recommendations(self) -> None:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        # Check unit tests
        unit_tests = self.results['tests'].get('unit_tests', {})
        if unit_tests.get('failed', 0) > 0:
            recommendations.append({
                'category': 'Testing',
                'priority': 'High',
                'issue': f"{unit_tests['failed']} unit tests failed",
                'recommendation': 'Fix failing unit tests before deployment'
            })
        
        # Check integration tests
        integration_tests = self.results['tests'].get('integration_tests', {})
        failed_endpoints = [ep for ep, result in integration_tests.items() if not result.get('success', False)]
        if failed_endpoints:
            recommendations.append({
                'category': 'Integration',
                'priority': 'High',
                'issue': f"Failed endpoints: {', '.join(failed_endpoints)}",
                'recommendation': 'Fix failing API endpoints'
            })
        
        # Check health endpoints
        health_tests = self.results['tests'].get('health_endpoints', {})
        slow_endpoints = [ep for ep, result in health_tests.items() 
                         if not result.get('meets_time_criteria', True)]
        if slow_endpoints:
            recommendations.append({
                'category': 'Performance',
                'priority': 'Medium',
                'issue': f"Slow health endpoints: {', '.join(slow_endpoints)}",
                'recommendation': 'Optimize health endpoint response times'
            })
        
        # Check authentication
        auth_tests = self.results['tests'].get('authentication', {})
        if not auth_tests.get('valid_auth_returns_200', False):
            recommendations.append({
                'category': 'Security',
                'priority': 'High',
                'issue': 'Authentication system not working',
                'recommendation': 'Fix authentication system before deployment'
            })
        
        # Check configuration
        config_tests = self.results['tests'].get('configuration', {})
        if config_tests.get('debug_endpoint_accessible', False):
            recommendations.append({
                'category': 'Security',
                'priority': 'Medium',
                'issue': 'Debug endpoint is accessible',
                'recommendation': 'Disable debug endpoint in production'
            })
        
        self.results['recommendations'] = recommendations
        
        # Log recommendations
        if recommendations:
            logger.info("Recommendations:")
            for rec in recommendations:
                logger.info(f"  [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
        else:
            logger.info("No recommendations - all validations passed!")
    
    def _save_results(self) -> None:
        """Save validation results to file."""
        import os
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Save detailed results
        results_file = f"{self.output_dir}/deployment_validation_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save summary report
        summary_file = f"{self.output_dir}/deployment_validation_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_markdown_report())
        
        logger.info(f"Validation results saved to {self.output_dir}/")
    
    def _generate_markdown_report(self) -> str:
        """Generate markdown report of validation results."""
        summary = self.results['summary']
        
        report = f"""# Trust Guard Deployment Validation Report

**Generated:** {self.results['timestamp']}  
**Base URL:** {self.results['base_url']}  
**Overall Success:** {'✅ PASSED' if summary['overall_success'] else '❌ FAILED'}

## Summary

- **Total Tests:** {summary['total_tests']}
- **Passed:** {summary['passed_tests']}
- **Failed:** {summary['failed_tests']}
- **Success Rate:** {summary.get('success_rate', 0):.1f}%

## Test Results

"""
        
        # Add test results
        for test_category, results in self.results['tests'].items():
            report += f"### {test_category.replace('_', ' ').title()}\n\n"
            
            if isinstance(results, dict):
                if 'success' in results:
                    status = "✅ PASSED" if results['success'] else "❌ FAILED"
                    report += f"- **Status:** {status}\n"
                elif 'exit_code' in results:
                    status = "✅ PASSED" if results['exit_code'] == 0 else "❌ FAILED"
                    report += f"- **Status:** {status}\n"
                    if 'passed' in results:
                        report += f"- **Tests Passed:** {results['passed']}/{results['total']}\n"
            
            report += "\n"
        
        # Add recommendations
        if self.results['recommendations']:
            report += "## Recommendations\n\n"
            for rec in self.results['recommendations']:
                report += f"### [{rec['priority']}] {rec['category']}\n"
                report += f"- **Issue:** {rec['issue']}\n"
                report += f"- **Recommendation:** {rec['recommendation']}\n\n"
        
        return report


def main():
    """Main entry point for deployment validation script."""
    parser = argparse.ArgumentParser(description='Validate Trust Guard deployment readiness')
    parser.add_argument('--base-url', default='http://localhost:8000',
                       help='Base URL of Trust Guard service (default: http://localhost:8000)')
    parser.add_argument('--output-dir', default='validation-results',
                       help='Output directory for validation results (default: validation-results)')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Create validator and run validation
    validator = DeploymentValidator(args.base_url, args.output_dir, args.verbose)
    results = validator.run_validation()
    
    # Exit with appropriate code
    if results['summary']['overall_success']:
        logger.info("Deployment validation completed successfully!")
        sys.exit(0)
    else:
        logger.error("Deployment validation failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()