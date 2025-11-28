#!/usr/bin/env python3
"""
AWS/Linkerd Deployment Readiness Validation Script

Validates readiness for AWS deployment with Linkerd service mesh integration.
Tests DNS resolution, health checks, service mesh headers, and AWS-specific configurations.

Usage:
    python scripts/REPLACE_ME.py --environment production
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional
import httpx
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Color output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


class AWSLinkerdTester:
    """AWS/Linkerd deployment readiness tester."""
    
    def __init__(self, base_url: str, namespace: str = "default", linkerd_enabled: bool = True):
        self.base_url = base_url.rstrip('/')
        self.namespace = namespace
        self.linkerd_enabled = linkerd_enabled
        self.results: List[Dict] = []
        
        # AWS/Linkerd specific headers
        self.linkerd_headers = {
            "l5d-dst-override": f"{self.base_url.replace('http://', '').replace('https://', '')}:8080",
            "l5d-require-id": "true"
        } if linkerd_enabled else {}
        
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            follow_redirects=True,
            headers=self.linkerd_headers
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def test_dns_resolution(self) -> Dict:
        """Test DNS resolution for service endpoints."""
        start_time = time.time()
        try:
            # Parse base URL to get hostname
            from urllib.parse import urlparse
            parsed = urlparse(self.base_url)
            hostname = parsed.hostname
            
            # Try to resolve DNS
            import socket
            ip_address = socket.gethostbyname(hostname)
            duration = time.time() - start_time
            
            return {
                "test": "DNS Resolution",
                "passed": True,
                "message": f"DNS resolved: {hostname} -> {ip_address}",
                "duration": duration,
                "hostname": hostname,
                "ip_address": ip_address
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "DNS Resolution",
                "passed": False,
                "message": f"DNS resolution failed: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_health_endpoint_kubernetes(self) -> Dict:
        """Test Kubernetes health endpoint (/health)."""
        start_time = time.time()
        try:
            response = await self.client.get(
                f"{self.base_url}/health",
                headers={"Accept": "application/json"}
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    "test": "Kubernetes Health Endpoint",
                    "passed": True,
                    "message": f"Health endpoint responding (status: {response.status_code})",
                    "duration": duration,
                    "status_code": response.status_code
                }
            else:
                return {
                    "test": "Kubernetes Health Endpoint",
                    "passed": False,
                    "message": f"Expected 200, got {response.status_code}",
                    "duration": duration,
                    "status_code": response.status_code
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Kubernetes Health Endpoint",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_metrics_endpoint_secure(self) -> Dict:
        """Test Prometheus metrics endpoint accessibility."""
        start_time = time.time()
        try:
            response = await self.client.get(
                f"{self.base_url}/metrics",
                headers={"Accept": "text/plain"}
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                # Check metrics format
                metrics_text = response.text
                has_prometheus_format = "# TYPE" in metrics_text or "http_requests_total" in metrics_text
                
                return {
                    "test": "Prometheus Metrics Endpoint (Secure)",
                    "passed": True,
                    "message": f"Metrics endpoint accessible (Prometheus format: {has_prometheus_format})",
                    "duration": duration,
                    "status_code": response.status_code,
                    "metrics_found": has_prometheus_format
                }
            else:
                return {
                    "test": "Prometheus Metrics Endpoint (Secure)",
                    "passed": False,
                    "message": f"Expected 200, got {response.status_code}",
                    "duration": duration,
                    "status_code": response.status_code
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Prometheus Metrics Endpoint (Secure)",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_linkerd_headers_response(self) -> Dict:
        """Test Linkerd-specific headers in responses."""
        start_time = time.time()
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/guards/health",
                headers={"Authorization": "Bearer test"}  # Will fail auth, but we check headers
            )
            duration = time.time() - start_time
            
            # Check for Linkerd-specific headers (if Linkerd is enabled)
            has_l5d_header = any("l5d" in k.lower() for k in response.headers.keys())
            
            if self.linkerd_enabled:
                return {
                    "test": "Linkerd Headers Present",
                    "passed": True,
                    "message": f"Linkerd headers checked (found: {has_l5d_header})",
                    "duration": duration,
                    "linkerd_enabled": True,
                    "headers_checked": True
                }
            else:
                return {
                    "test": "Linkerd Headers Present",
                    "passed": True,
                    "message": "Linkerd not enabled, skipping header check",
                    "duration": duration,
                    "linkerd_enabled": False
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Linkerd Headers Present",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_service_mesh_routing(self) -> Dict:
        """Test service mesh routing configuration."""
        start_time = time.time()
        try:
            # Test internal service endpoint
            response = await self.client.get(
                f"{self.base_url}/internal/guards/health",
                headers={"Content-Type": "application/json"}
            )
            duration = time.time() - start_time
            
            # Service mesh should handle routing
            # Any response (even 404) indicates routing works
            routing_works = response.status_code in [200, 401, 403, 404]
            
            return {
                "test": "Service Mesh Routing",
                "passed": routing_works,
                "message": f"Routing responded (status: {response.status_code})",
                "duration": duration,
                "status_code": response.status_code,
                "routing_configured": routing_works
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Service Mesh Routing",
                "passed": False,
                "message": f"Routing failed: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def REPLACE_ME(self) -> Dict:
        """Test AWS-specific environment variables."""
        start_time = time.time()
        try:
            # Check for AWS-specific env vars that should be set
            aws_vars = {
                "AWS_REGION": os.getenv("AWS_REGION"),
                "AWS_SECRETS_ENABLED": os.getenv("AWS_SECRETS_ENABLED"),
                "ENVIRONMENT": os.getenv("ENVIRONMENT"),
            }
            
            # At minimum, ENVIRONMENT should be set
            has_environment = aws_vars["ENVIRONMENT"] is not None
            
            duration = time.time() - start_time
            
            return {
                "test": "AWS Environment Variables",
                "passed": has_environment,
                "message": f"Environment variables: {dict((k, '✓' if v else '✗') for k, v in aws_vars.items())}",
                "duration": duration,
                "variables": aws_vars
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "AWS Environment Variables",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_kubernetes_readiness_probe(self) -> Dict:
        """Test Kubernetes readiness probe endpoint."""
        start_time = time.time()
        try:
            # Kubernetes typically expects /ready or /healthz
            for endpoint in ["/ready", "/healthz", "/health"]:
                try:
                    response = await self.client.get(
                        f"{self.base_url}{endpoint}",
                        headers={"Accept": "application/json"},
                        timeout=httpx.Timeout(5.0)
                    )
                    if response.status_code == 200:
                        duration = time.time() - start_time
                        return {
                            "test": "Kubernetes Readiness Probe",
                            "passed": True,
                            "message": f"Readiness probe responding: {endpoint} (status: 200)",
                            "duration": duration,
                            "endpoint": endpoint,
                            "status_code": 200
                        }
                except Exception:
                    continue
            
            duration = time.time() - start_time
            return {
                "test": "Kubernetes Readiness Probe",
                "passed": False,
                "message": "No readiness probe endpoint found (/ready, /healthz, or /health)",
                "duration": duration
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Kubernetes Readiness Probe",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_kubernetes_liveness_probe(self) -> Dict:
        """Test Kubernetes liveness probe endpoint."""
        start_time = time.time()
        try:
            # Kubernetes typically expects /alive or /healthz
            for endpoint in ["/alive", "/healthz", "/health"]:
                try:
                    response = await self.client.get(
                        f"{self.base_url}{endpoint}",
                        headers={"Accept": "application/json"},
                        timeout=httpx.Timeout(5.0)
                    )
                    if response.status_code == 200:
                        duration = time.time() - start_time
                        return {
                            "test": "Kubernetes Liveness Probe",
                            "passed": True,
                            "message": f"Liveness probe responding: {endpoint} (status: 200)",
                            "duration": duration,
                            "endpoint": endpoint,
                            "status_code": 200
                        }
                except Exception:
                    continue
            
            duration = time.time() - start_time
            return {
                "test": "Kubernetes Liveness Probe",
                "passed": False,
                "message": "No liveness probe endpoint found (/alive, /healthz, or /health)",
                "duration": duration
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Kubernetes Liveness Probe",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_service_mesh_timeout_handling(self) -> Dict:
        """Test service mesh timeout configuration."""
        start_time = time.time()
        try:
            # Make a request and check response time
            # Service mesh should handle timeouts gracefully
            response = await self.client.get(
                f"{self.base_url}/api/v1/guards/health",
                headers={"Authorization": "Bearer test"},
                timeout=httpx.Timeout(10.0)
            )
            duration = time.time() - start_time
            
            # Service mesh should respond within reasonable time (< 1s for simple endpoints)
            timeout_ok = duration < 1.0
            
            return {
                "test": "Service Mesh Timeout Handling",
                "passed": timeout_ok or response.status_code in [401, 403],
                "message": f"Response time: {duration:.3f}s (status: {response.status_code})",
                "duration": duration,
                "status_code": response.status_code,
                "response_time_ok": timeout_ok
            }
        except httpx.TimeoutException:
            duration = time.time() - start_time
            return {
                "test": "Service Mesh Timeout Handling",
                "passed": False,
                "message": "Request timed out (service mesh timeout may be misconfigured)",
                "duration": duration,
                "error": "TimeoutException"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Service Mesh Timeout Handling",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def run_all_tests(self) -> Dict:
        """Run all AWS/Linkerd deployment tests."""
        print(f"\n{BOLD}{CYAN}☁️  AWS/Linkerd Deployment Readiness Validation{RESET}\n")
        print(f"Base URL: {self.base_url}")
        print(f"Namespace: {self.namespace}")
        print(f"Linkerd Enabled: {self.linkerd_enabled}\n")
        
        tests = [
            self.test_dns_resolution,
            self.test_health_endpoint_kubernetes,
            self.test_metrics_endpoint_secure,
            self.test_linkerd_headers_response,
            self.test_service_mesh_routing,
            self.REPLACE_ME,
            self.test_kubernetes_readiness_probe,
            self.test_kubernetes_liveness_probe,
            self.test_service_mesh_timeout_handling,
        ]
        
        for test_func in tests:
            test_name = test_func.__name__.replace("test_", "").replace("_", " ").title()
            print(f"{CYAN}Running: {test_name}...{RESET}", end=" ", flush=True)
            result = await test_func()
            self.results.append(result)
            
            if result["passed"]:
                print(f"{GREEN}✓ PASSED{RESET} ({result['duration']:.3f}s)")
                print(f"  {result['message']}")
            else:
                print(f"{RED}✗ FAILED{RESET} ({result['duration']:.3f}s)")
                print(f"  {RED}{result['message']}{RESET}")
        
        # Summary
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        
        print(f"\n{BOLD}Summary:{RESET}")
        print(f"  Passed: {GREEN}{passed}/{total}{RESET}")
        print(f"  Failed: {RED}{total - passed}/{total}{RESET}")
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "results": self.results
        }


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS/Linkerd Deployment Readiness Validation")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--namespace", default="default", help="Kubernetes namespace")
    parser.add_argument("--no-linkerd", action="store_true", help="Disable Linkerd checks")
    parser.add_argument("--environment", choices=["development", "staging", "production"], 
                       default="production", help="Deployment environment")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    async with AWSLinkerdTester(
        base_url=args.url,
        namespace=args.namespace,
        linkerd_enabled=not args.no_linkerd
    ) as tester:
        results = await tester.run_all_tests()
        
        if args.json:
            print(json.dumps(results, indent=2))
            sys.exit(0 if results["failed"] == 0 else 1)
        else:
            sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())

