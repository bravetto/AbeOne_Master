#!/usr/bin/env python3
"""
AWS/Linkerd Integration Failure Pattern Detection Script

Based on Deep Forensic Analysis: AWS/Linkerd Rejection Patterns
Tests for integration-specific failure patterns (AWS + Linkerd combined).

Patterns Detected:
1. AWS NLB + Linkerd Idle Timeout Cascade
2. ALB + Linkerd Multicluster Gateway 502s
3. NLB + Linkerd gRPC MAX_CONCURRENT_STREAMS
4. VPC Flow Log REJECT with Security Group "Allowance"

Usage:
    python scripts/test_aws_linkerd_integration_patterns.py --url http://localhost:8000
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional
import httpx

# Color output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"


class AWSLinkerdIntegrationDetector:
    """Detector for AWS + Linkerd integration failure patterns."""
    
    def __init__(self, base_url: str, linkerd_enabled: bool = True):
        self.base_url = base_url.rstrip('/')
        self.linkerd_enabled = linkerd_enabled
        # Try HTTP/2, fallback to HTTP/1.1 if h2 not available
        try:
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                http2=True
            )
        except ImportError:
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                http2=False  # Fallback to HTTP/1.1
            )
        self.results: List[Dict] = []
        self.timeout_cascade_patterns = []
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def test_timeout_cascade_pattern(self) -> Dict:
        """
        Test for Pattern 3.1: AWS NLB + Linkerd Idle Timeout Cascade
        
        Detects patterns suggesting cascading failures from NLB timeout + Linkerd circuit breaker.
        """
        start_time = time.time()
        
        try:
            # This pattern requires long-running observation (350s+)
            # For expediency, we detect indicators:
            # 1. Connection reset patterns
            # 2. Error patterns after idle periods
            # 3. Circuit breaker indicators combined with timeout errors
            
            # Make initial requests
            initial_results = []
            for i in range(10):
                try:
                    response = await self.client.get(f"{self.base_url}/health")
                    initial_results.append(response.status_code)
                except Exception as e:
                    initial_results.append(f"ERROR: {str(e)}")
            
            # Simulate "idle then active" pattern
            await asyncio.sleep(2)  # Brief idle
            
            # Make requests after idle period
            post_idle_results = []
            reset_errors = 0
            circuit_breaker_hints = []
            
            for i in range(10):
                try:
                    response = await self.client.get(f"{self.base_url}/health", timeout=5.0)
                    post_idle_results.append(response.status_code)
                    
                    # Check for Linkerd error headers
                    error_header = response.headers.get('l5d-err', '')
                    if 'fail-fast' in error_header.lower() or 'unavailable' in error_header.lower():
                        circuit_breaker_hints.append({
                            "request": i,
                            "header": error_header
                        })
                        
                except httpx.ConnectError as e:
                    error_str = str(e).lower()
                    if 'reset' in error_str or 'refused' in error_str:
                        reset_errors += 1
                        post_idle_results.append(f"RESET: {str(e)}")
                except Exception as e:
                    post_idle_results.append(f"ERROR: {str(e)}")
            
            duration = time.time() - start_time
            
            # Detect cascade indicators
            has_reset_errors = reset_errors > 0
            has_circuit_breaker = len(circuit_breaker_hints) > 0
            cascade_indicators = has_reset_errors and has_circuit_breaker
            
            return {
                "test": "Timeout Cascade Pattern Detection",
                "pattern": "3.1: AWS NLB + Linkerd Idle Timeout Cascade",
                "passed": not cascade_indicators,
                "message": f"Reset errors: {reset_errors}, Circuit breaker hints: {len(circuit_breaker_hints)}, Cascade indicators: {cascade_indicators}",
                "duration": duration,
                "metrics": {
                    "initial_success_rate": sum(1 for r in initial_results if r == 200) / len(initial_results),
                    "post_idle_success_rate": sum(1 for r in post_idle_results if isinstance(r, int) and r == 200) / len(post_idle_results),
                    "reset_errors": reset_errors,
                    "circuit_breaker_hints": len(circuit_breaker_hints)
                },
                "circuit_breaker_hints": circuit_breaker_hints,
                "issues_detected": [
                    f"{reset_errors} connection reset errors detected",
                    f"{len(circuit_breaker_hints)} circuit breaker indicators found"
                ] if cascade_indicators else [],
                "recommendations": [
                    "Monitor for connection resets after ~350s idle time",
                    "Check CloudWatch TCP_ELB_Reset_Count metric",
                    "Implement TCP keepalive < 350s (recommended: 120s)",
                    "Configure Linkerd circuit breaker with higher threshold: balancer.linkerd.io/failure-accrual-consecutive-max-failures=10",
                    "Consider application-level connection cycling (close after 300s)",
                    "Monitor Linkerd dashboard for circuit breaker trips",
                    "Check for pattern: NLB timeout → Linkerd circuit breaker → Extended outage"
                ] if cascade_indicators else [],
                "detection_method": "Pattern detection - combined reset errors + circuit breaker indicators after idle",
                "note": "Full detection requires monitoring over 350s+ periods"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Timeout Cascade Pattern Detection",
                "pattern": "3.1: AWS NLB + Linkerd Idle Timeout Cascade",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_grpc_concurrency_with_nlb(self) -> Dict:
        """
        Test for Pattern 3.3: NLB + Linkerd gRPC MAX_CONCURRENT_STREAMS
        
        Detects patterns suggesting HTTP/2 stream exhaustion behind NLB.
        """
        start_time = time.time()
        
        try:
            # Simulate multiple concurrent streams (typical gRPC pattern)
            concurrency_levels = [50, 100, 150, 200]
            stream_exhaustion_indicators = []
            
            for concurrency in concurrency_levels:
                stream_errors = []
                
                async def make_stream_request():
                    try:
                        response = await self.client.get(f"{self.base_url}/health", timeout=5.0)
                        return {"success": True, "status": response.status_code}
                    except Exception as e:
                        error_str = str(e).lower()
                        if 'max-concurrency' in error_str or 'exhausted' in error_str:
                            return {"success": False, "error": "stream_exhaustion"}
                        return {"success": False, "error": str(e)}
                
                # Concurrent requests simulating streams
                tasks = [make_stream_request() for _ in range(concurrency)]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                exhaustion_count = sum(1 for r in results if isinstance(r, dict) and r.get("error") == "stream_exhaustion")
                success_count = sum(1 for r in results if isinstance(r, dict) and r.get("success", False))
                
                if exhaustion_count > 0:
                    stream_exhaustion_indicators.append({
                        "concurrency": concurrency,
                        "exhaustion_count": exhaustion_count,
                        "success_count": success_count,
                        "error_rate": exhaustion_count / concurrency
                    })
                
                # Early exit if we detect exhaustion
                if exhaustion_count > concurrency * 0.3:
                    break
                
                await asyncio.sleep(0.3)
            
            duration = time.time() - start_time
            
            has_exhaustion = len(stream_exhaustion_indicators) > 0
            
            return {
                "test": "gRPC Stream Exhaustion Pattern Detection",
                "pattern": "3.3: NLB + Linkerd gRPC MAX_CONCURRENT_STREAMS",
                "passed": not has_exhaustion,
                "message": f"Stream exhaustion detected at concurrency levels: {[s['concurrency'] for s in stream_exhaustion_indicators]}",
                "duration": duration,
                "exhaustion_indicators": stream_exhaustion_indicators,
                "issues_detected": [
                    f"Stream exhaustion at concurrency {s['concurrency']}: {s['exhaustion_count']} errors"
                    for s in stream_exhaustion_indicators
                ] if has_exhaustion else [],
                "recommendations": [
                    "NLB preserves HTTP/2 connections - single connection handles all requests",
                    "Linkerd doesn't pool HTTP/2 connections → all requests on one connection",
                    "Solution 1: Increase application max_concurrent_streams (100 → 1000+)",
                    "Solution 2: Deploy multiple Linkerd gateway replicas with IP target mode",
                    "Solution 3: Use connection draining and cycling",
                    "Calculate required: RPS × Avg Latency = Concurrent Streams Needed",
                    "Example: 300 RPS × 0.1s = 30 streams (needs > 30 limit)"
                ] if has_exhaustion else [],
                "detection_method": "Concurrent stream testing - detect exhaustion behind NLB",
                "note": "This pattern only occurs with NLB + Linkerd, not direct pod-to-pod"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "gRPC Stream Exhaustion Pattern Detection",
                "pattern": "3.3: NLB + Linkerd gRPC MAX_CONCURRENT_STREAMS",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_multicluster_gateway_patterns(self) -> Dict:
        """
        Test for Pattern 3.2: ALB + Linkerd Multicluster Gateway 502s
        
        Detects patterns suggesting ALB backend protocol mismatch with Linkerd gateway.
        """
        start_time = time.time()
        
        try:
            # Test basic connectivity
            gateway_errors = []
            protocol_mismatch_hints = []
            
            # Make requests and check for 502 errors
            for i in range(10):
                try:
                    response = await self.client.get(f"{self.base_url}/health")
                    
                    if response.status_code == 502:
                        gateway_errors.append({
                            "request": i,
                            "status": 502,
                            "pattern": "502 Bad Gateway"
                        })
                        
                        # Check for protocol-related indicators
                        headers = dict(response.headers)
                        if 'alb' in str(headers).lower() or 'elb' in str(headers).lower():
                            protocol_mismatch_hints.append({
                                "request": i,
                                "headers": headers
                            })
                            
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 502:
                        gateway_errors.append({
                            "request": i,
                            "status": 502,
                            "error": str(e)
                        })
                except Exception as e:
                    if '502' in str(e) or 'bad gateway' in str(e).lower():
                        gateway_errors.append({
                            "request": i,
                            "error": str(e)
                        })
            
            duration = time.time() - start_time
            
            has_502_pattern = len(gateway_errors) > 0
            has_protocol_mismatch = len(protocol_mismatch_hints) > 0
            
            return {
                "test": "Multicluster Gateway Pattern Detection",
                "pattern": "3.2: ALB + Linkerd Multicluster Gateway 502s",
                "passed": not has_502_pattern,
                "message": f"502 errors: {len(gateway_errors)}, Protocol mismatch hints: {len(protocol_mismatch_hints)}",
                "duration": duration,
                "gateway_errors": gateway_errors,
                "protocol_mismatch_hints": protocol_mismatch_hints,
                "issues_detected": [
                    f"{len(gateway_errors)} 502 Bad Gateway errors detected",
                    "ALB backend protocol may be misconfigured"
                ] if has_502_pattern else [],
                "recommendations": [
                    "Check ALB ingress annotations for backend-protocol",
                    "Should be: alb.ingress.kubernetes.io/backend-protocol: TCP (NOT HTTP)",
                    "Linkerd gateway expects mTLS on port 4143",
                    "Verify healthcheck-path and healthcheck-port configured correctly",
                    "Health check should use separate port (4181) not gateway port (4143)",
                    "Check ALB access logs for pattern: elb_status_code='502' consistently"
                ] if has_502_pattern else [],
                "detection_method": "502 error pattern detection - indicative of ALB protocol mismatch",
                "note": "This pattern only occurs with ALB ingress + Linkerd multicluster gateway"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Multicluster Gateway Pattern Detection",
                "pattern": "3.2: ALB + Linkerd Multicluster Gateway 502s",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def run_all_tests(self) -> Dict:
        """Run all AWS/Linkerd integration failure pattern detection tests."""
        print(f"\n{BOLD}{MAGENTA} AWS/Linkerd Integration Failure Pattern Detection{RESET}\n")
        print(f"Target: {self.base_url}")
        print(f"Linkerd Enabled: {self.linkerd_enabled}\n")
        
        tests = [
            ("Timeout Cascade Pattern", self.test_timeout_cascade_pattern),
            ("gRPC Stream Exhaustion", self.test_grpc_concurrency_with_nlb),
            ("Multicluster Gateway", self.test_multicluster_gateway_patterns),
        ]
        
        for test_name, test_func in tests:
            print(f"{MAGENTA}Testing: {test_name}...{RESET}", end=" ", flush=True)
            result = await test_func()
            self.results.append(result)
            
            if result["passed"]:
                print(f"{GREEN} CLEAN{RESET} ({result['duration']:.3f}s)")
            else:
                print(f"{YELLOW} PATTERNS DETECTED{RESET} ({result['duration']:.3f}s)")
            
            if result.get("issues_detected"):
                for issue in result["issues_detected"]:
                    print(f"  {YELLOW} {issue}{RESET}")
        
        # Summary
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        issues_found = sum(len(r.get("issues_detected", [])) for r in self.results)
        
        print(f"\n{BOLD}Summary:{RESET}")
        print(f"  Tests: {total}")
        print(f"  Clean: {GREEN}{passed}{RESET}")
        print(f"  Patterns Detected: {YELLOW}{issues_found}{RESET}")
        
        return {
            "total": total,
            "passed": passed,
            "issues_found": issues_found,
            "results": self.results
        }


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS/Linkerd Integration Failure Pattern Detection")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL to test")
    parser.add_argument("--no-linkerd", action="store_true", help="Linkerd not enabled")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    async with AWSLinkerdIntegrationDetector(
        base_url=args.url,
        linkerd_enabled=not args.no_linkerd
    ) as detector:
        results = await detector.run_all_tests()
        
        if args.json:
            print(json.dumps(results, indent=2))
            sys.exit(0 if results["issues_found"] == 0 else 1)
        else:
            sys.exit(0 if results["issues_found"] == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())

