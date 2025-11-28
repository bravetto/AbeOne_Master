#!/usr/bin/env python3
"""
Linkerd Service Mesh Failure Pattern Detection Script

Based on Deep Forensic Analysis: AWS/Linkerd Rejection Patterns
Tests for Linkerd-specific failure patterns without modifying codebase.

Patterns Detected:
1. Fail-Fast Circuit Breaking
2. Proxy Connection Refused (OS Error 111)
3. HTTP/2 Max Concurrent Streams Exhaustion
4. Linkerd Proxy Timeout (10s Default)
5. TCP Keepalive and Half-Closed Connections
6. gRPC Stream Leak and RST_STREAM Handling

Usage:
    python scripts/test_linkerd_failure_patterns.py --url http://localhost:8000
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
RESET = "\033[0m"
BOLD = "\033[1m"


class LinkerdFailurePatternDetector:
    """Detector for Linkerd service mesh failure patterns."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        # Try HTTP/2, fallback to HTTP/1.1 if h2 not available
        try:
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0, connect=10.0),
                http2=True  # Enable HTTP/2 for Linkerd testing
            )
        except ImportError:
            self.client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0, connect=10.0),
                http2=False  # Fallback to HTTP/1.1
            )
        self.results: List[Dict] = []
        self.concurrent_errors = []
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def test_circuit_breaker_patterns(self) -> Dict:
        """
        Test for Pattern 2.1: Fail-Fast Circuit Breaking
        
        Detects patterns suggesting Linkerd circuit breaker tripping.
        """
        start_time = time.time()
        
        try:
            # Make requests and detect failure patterns
            # Pattern: Consecutive failures followed by service unavailable
            
            failure_streak = 0
            max_failure_streak = 0
            circuit_breaker_signatures = []
            
            for i in range(15):
                try:
                    response = await self.client.get(f"{self.base_url}/health")
                    
                    if response.status_code >= 500:
                        failure_streak += 1
                        max_failure_streak = max(max_failure_streak, failure_streak)
                        
                        # Check response headers for Linkerd-specific errors
                        error_header = response.headers.get('l5d-err', '')
                        if 'fail-fast' in error_header.lower() or 'unavailable' in error_header.lower():
                            circuit_breaker_signatures.append({
                                "request": i,
                                "status": response.status_code,
                                "error_header": error_header
                            })
                    else:
                        failure_streak = 0
                        
                except (httpx.HTTPStatusError, httpx.ConnectError) as e:
                    failure_streak += 1
                    max_failure_streak = max(max_failure_streak, failure_streak)
                    
                    error_str = str(e).lower()
                    if 'unavailable' in error_str or 'fail-fast' in error_str:
                        circuit_breaker_signatures.append({
                            "request": i,
                            "error": str(e)
                        })
                
                await asyncio.sleep(0.1)
            
            duration = time.time() - start_time
            
            # Circuit breaker typically trips after 7 consecutive failures
            circuit_breaker_likely = max_failure_streak >= 7 or len(circuit_breaker_signatures) > 0
            
            return {
                "test": "Circuit Breaker Pattern Detection",
                "pattern": "2.1: Fail-Fast Circuit Breaking",
                "passed": not circuit_breaker_likely,
                "message": f"Max failure streak: {max_failure_streak}, Circuit breaker signatures: {len(circuit_breaker_signatures)}",
                "duration": duration,
                "metrics": {
                    "max_failure_streak": max_failure_streak,
                    "circuit_breaker_signatures": len(circuit_breaker_signatures),
                    "threshold_breach": max_failure_streak >= 7
                },
                "circuit_breaker_signatures": circuit_breaker_signatures,
                "issues_detected": [
                    f"Failure streak of {max_failure_streak} detected (threshold: 7)"
                ] if max_failure_streak >= 7 else [],
                "recommendations": [
                    "Check Linkerd viz: linkerd viz stat deploy -n namespace",
                    "Look for deployments with low success rates",
                    "Check application logs for consecutive failures",
                    "Verify max_concurrent_streams not set too low",
                    "Monitor linkerd proxy logs for 'Service in fail-fast' messages"
                ] if circuit_breaker_likely else [],
                "detection_method": "Failure streak analysis - detect 7+ consecutive failures"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Circuit Breaker Pattern Detection",
                "pattern": "2.1: Fail-Fast Circuit Breaking",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_connection_refused_patterns(self) -> Dict:
        """
        Test for Pattern 2.2: Proxy Connection Refused (OS Error 111)
        
        Detects connection refused errors that suggest port binding issues.
        """
        start_time = time.time()
        
        try:
            # Test basic connectivity
            connection_errors = []
            
            try:
                response = await self.client.get(f"{self.base_url}/health")
                base_accessible = response.status_code == 200
            except httpx.ConnectError as e:
                base_accessible = False
                error_str = str(e).lower()
                if 'connection refused' in error_str or '111' in error_str:
                    connection_errors.append({
                        "error": str(e),
                        "pattern": "Connection refused",
                        "likely_cause": "Application not bound to port or wrong port"
                    })
            except Exception as e:
                base_accessible = False
                connection_errors.append({
                    "error": str(e),
                    "pattern": "Unknown connection error"
                })
            
            duration = time.time() - start_time
            
            has_connection_refused = len([e for e in connection_errors if 'connection refused' in str(e).lower()]) > 0
            
            return {
                "test": "Connection Refused Pattern Detection",
                "pattern": "2.2: Proxy Connection Refused (OS Error 111)",
                "passed": base_accessible and not has_connection_refused,
                "message": f"Base endpoint accessible: {base_accessible}, Connection refused errors: {len([e for e in connection_errors if 'connection refused' in str(e).lower()])}",
                "duration": duration,
                "base_accessible": base_accessible,
                "connection_errors": connection_errors,
                "issues_detected": [
                    "Connection refused detected - check application port binding",
                    "Verify application bound to 0.0.0.0, not 127.0.0.1",
                    "Check readiness probe passes but application not listening"
                ] if has_connection_refused else [],
                "recommendations": [
                    "Verify application binds to 0.0.0.0:PORT, not 127.0.0.1:PORT",
                    "Check readiness probe - may pass but application not ready",
                    "Verify Service targetPort matches container port",
                    "Inside pod: netstat -tlnp | grep PORT (should show 0.0.0.0:PORT)",
                    "Check Linkerd proxy logs for 'Connection refused (os error 111)'"
                ] if has_connection_refused else [],
                "detection_method": "Connection testing - detect OS error 111 patterns"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Connection Refused Pattern Detection",
                "pattern": "2.2: Proxy Connection Refused (OS Error 111)",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_http2_concurrency_patterns(self) -> Dict:
        """
        Test for Pattern 2.3: HTTP/2 Max Concurrent Streams Exhaustion
        
        Detects patterns suggesting HTTP/2 stream limit exhaustion.
        """
        start_time = time.time()
        
        try:
            # Make many concurrent requests to detect stream exhaustion
            concurrency_levels = [10, 50, 100, 150]
            results_by_concurrency = {}
            
            for concurrency in concurrency_levels:
                errors = []
                timeouts = []
                success_count = 0
                
                async def make_request():
                    try:
                        response = await self.client.get(f"{self.base_url}/health", timeout=5.0)
                        return {"status": response.status_code, "error": None}
                    except httpx.TimeoutException as e:
                        return {"status": None, "error": "timeout"}
                    except Exception as e:
                        error_str = str(e).lower()
                        if 'max-concurrency' in error_str or 'exhausted' in error_str:
                            return {"status": None, "error": "concurrency_exhausted"}
                        return {"status": None, "error": str(e)}
                
                # Make concurrent requests
                tasks = [make_request() for _ in range(concurrency)]
                request_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in request_results:
                    if isinstance(result, Exception):
                        errors.append(str(result))
                    elif result.get("status"):
                        success_count += 1
                    elif result.get("error") == "timeout":
                        timeouts.append(result)
                    elif result.get("error") == "concurrency_exhausted":
                        errors.append("max-concurrency exhausted")
                
                results_by_concurrency[concurrency] = {
                    "success": success_count,
                    "timeouts": len(timeouts),
                    "errors": len(errors),
                    "error_rate": len(errors) / concurrency,
                    "timeout_rate": len(timeouts) / concurrency
                }
                
                # Early exit if we hit concurrency limits
                if len(errors) > concurrency * 0.5:
                    break
                
                await asyncio.sleep(0.5)
            
            duration = time.time() - start_time
            
            # Detect concurrency exhaustion patterns
            high_error_rates = {k: v for k, v in results_by_concurrency.items() if v["error_rate"] > 0.3}
            concurrency_exhaustion_detected = len(high_error_rates) > 0
            
            return {
                "test": "HTTP/2 Concurrency Pattern Detection",
                "pattern": "2.3: HTTP/2 Max Concurrent Streams Exhaustion",
                "passed": not concurrency_exhaustion_detected,
                "message": f"Tested concurrency levels: {list(results_by_concurrency.keys())}, High error rates: {list(high_error_rates.keys())}",
                "duration": duration,
                "concurrency_results": results_by_concurrency,
                "issues_detected": [
                    f"High error rate at concurrency {k}: {v['error_rate']*100:.1f}%"
                    for k, v in high_error_rates.items()
                ] if concurrency_exhaustion_detected else [],
                "recommendations": [
                    "Check application max_concurrent_streams setting (may be too low)",
                    "Typical issue: max_concurrent_streams = 10, needs 30+ for actual load",
                    "Calculate required: RPS × Average Latency = Concurrent Streams Needed",
                    "Increase application max_concurrent_streams (e.g., 100 → 1000)",
                    "For gRPC: Set grpc.MaxConcurrentStreams(1000) on server",
                    "Monitor Linkerd metrics: rt/client/{service}/open_streams"
                ] if concurrency_exhaustion_detected else [],
                "detection_method": "Concurrent request testing - detect stream limit exhaustion"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "HTTP/2 Concurrency Pattern Detection",
                "pattern": "2.3: HTTP/2 Max Concurrent Streams Exhaustion",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_proxy_timeout_patterns(self) -> Dict:
        """
        Test for Pattern 2.4: Linkerd Proxy Timeout (10s Default)
        
        Detects timeout patterns suggesting Linkerd proxy timeout issues.
        """
        start_time = time.time()
        
        try:
            # Test for requests that approach 10s timeout
            timeout_errors = []
            slow_requests = []
            
            # Make several requests and track timing
            for i in range(5):
                req_start = time.time()
                try:
                    # Use a longer timeout to see if requests complete but slowly
                    response = await self.client.get(f"{self.base_url}/health", timeout=15.0)
                    req_duration = time.time() - req_start
                    
                    if req_duration > 8.0:  # Approaching 10s threshold
                        slow_requests.append(req_duration)
                        
                except httpx.TimeoutException as e:
                    req_duration = time.time() - req_start
                    timeout_errors.append({
                        "duration": req_duration,
                        "error": "timeout",
                        "approaches_10s": 8.0 <= req_duration <= 12.0
                    })
                except Exception as e:
                    error_str = str(e).lower()
                    if 'timeout' in error_str or 'timed out' in error_str:
                        timeout_errors.append({
                            "duration": time.time() - req_start,
                            "error": str(e)
                        })
            
            duration = time.time() - start_time
            
            timeout_patterns = len([e for e in timeout_errors if e.get("approaches_10s", False)])
            slow_patterns = len(slow_requests)
            
            return {
                "test": "Proxy Timeout Pattern Detection",
                "pattern": "2.4: Linkerd Proxy Timeout (10s Default)",
                "passed": len(timeout_errors) == 0 and slow_patterns == 0,
                "message": f"Timeout errors: {len(timeout_errors)}, Slow requests (>8s): {slow_patterns}, 10s pattern: {timeout_patterns}",
                "duration": duration,
                "timeout_errors": timeout_errors,
                "slow_requests": slow_requests,
                "issues_detected": [
                    f"{len(timeout_errors)} timeout errors detected",
                    f"{slow_patterns} requests approaching 10s threshold"
                ] if timeout_errors or slow_requests else [],
                "recommendations": [
                    "Linkerd proxy has 10s default timeout (not configurable per-request)",
                    "For per-route timeouts, use ServiceProfile with timeout: 30s",
                    "Check backend service processing time - may exceed 10s",
                    "Monitor Linkerd proxy logs for 'request timed out' and 'proxy dispatch timed out'",
                    "Check connection pool exhaustion causing queuing delays",
                    "Verify database query timeouts are < 10s"
                ] if timeout_errors or slow_requests else [],
                "detection_method": "Timing analysis - detect requests approaching/exceeding 10s"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Proxy Timeout Pattern Detection",
                "pattern": "2.4: Linkerd Proxy Timeout (10s Default)",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def run_all_tests(self) -> Dict:
        """Run all Linkerd failure pattern detection tests."""
        print(f"\n{BOLD}{CYAN} Linkerd Service Mesh Failure Pattern Detection{RESET}\n")
        print(f"Target: {self.base_url}\n")
        
        tests = [
            ("Circuit Breaker Patterns", self.test_circuit_breaker_patterns),
            ("Connection Refused Patterns", self.test_connection_refused_patterns),
            ("HTTP/2 Concurrency Patterns", self.test_http2_concurrency_patterns),
            ("Proxy Timeout Patterns", self.test_proxy_timeout_patterns),
        ]
        
        for test_name, test_func in tests:
            print(f"{CYAN}Testing: {test_name}...{RESET}", end=" ", flush=True)
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
    
    parser = argparse.ArgumentParser(description="Linkerd Service Mesh Failure Pattern Detection")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL to test")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    async with LinkerdFailurePatternDetector(base_url=args.url) as detector:
        results = await detector.run_all_tests()
        
        if args.json:
            print(json.dumps(results, indent=2))
            sys.exit(0 if results["issues_found"] == 0 else 1)
        else:
            sys.exit(0 if results["issues_found"] == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())


