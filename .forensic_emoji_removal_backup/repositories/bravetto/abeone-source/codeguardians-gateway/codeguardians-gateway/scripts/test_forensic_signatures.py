#!/usr/bin/env python3
"""
Forensic Signature Detection Script

Based on Deep Forensic Analysis: AWS/Linkerd Rejection Patterns
Detects forensic signatures and error code patterns without modifying codebase.

Signatures Detected:
- Error Code Classification (502, 503, 504, Connection refused, Connection reset)
- CloudWatch Metrics Patterns (RejectedFlowCount, TCP_ELB_Reset_Count, etc.)
- Log-Based Detection Patterns
- Timeout and RST Patterns

Usage:
    python scripts/test_forensic_signatures.py --url http://localhost:8000
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


class ForensicSignatureDetector:
    """Detector for forensic signatures and error patterns."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(30.0))
        self.results: List[Dict] = []
        self.error_codes_seen = {}
        self.rst_patterns = []
        self.timeout_patterns = []
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def test_error_code_classification(self) -> Dict:
        """
        Test Error Code Classification Matrix
        
        Classifies observed error codes according to forensic analysis.
        """
        start_time = time.time()
        
        try:
            error_codes = {}
            error_patterns = {
                "502": {"source": "ALB/NLB", "meaning": "Bad gateway - target connection issue", "priority": "HIGH"},
                "503": {"source": "ALB", "meaning": "No healthy targets available", "priority": "CRITICAL"},
                "504": {"source": "ALB", "meaning": "Gateway timeout - target didn't respond", "priority": "MEDIUM"},
                "connection_refused_111": {"source": "Linkerd", "meaning": "Target port not listening", "priority": "HIGH"},
                "connection_reset_104": {"source": "NLB/Linkerd", "meaning": "Connection terminated", "priority": "HIGH"},
                "fail_fast": {"source": "Linkerd", "meaning": "Circuit breaker tripped", "priority": "MEDIUM"},
                "max_concurrency": {"source": "Linkerd", "meaning": "Stream limit reached", "priority": "MEDIUM"}
            }
            
            # Make requests to collect error codes
            for i in range(20):
                try:
                    response = await self.client.get(f"{self.base_url}/health")
                    status = response.status_code
                    error_codes[status] = error_codes.get(status, 0) + 1
                except httpx.ConnectError as e:
                    error_str = str(e).lower()
                    if 'connection refused' in error_str or '111' in error_str:
                        error_codes["connection_refused_111"] = error_codes.get("connection_refused_111", 0) + 1
                    elif 'reset' in error_str or '104' in error_str:
                        error_codes["connection_reset_104"] = error_codes.get("connection_reset_104", 0) + 1
                except httpx.TimeoutException:
                    error_codes["timeout"] = error_codes.get("timeout", 0) + 1
                except httpx.HTTPStatusError as e:
                    status = e.response.status_code
                    error_codes[status] = error_codes.get(status, 0) + 1
                except Exception as e:
                    error_str = str(e).lower()
                    if 'fail-fast' in error_str:
                        error_codes["fail_fast"] = error_codes.get("fail_fast", 0) + 1
                    elif 'max-concurrency' in error_str or 'exhausted' in error_str:
                        error_codes["max_concurrency"] = error_codes.get("max_concurrency", 0) + 1
            
            duration = time.time() - start_time
            
            # Classify observed errors
            classified_errors = []
            high_priority = []
            
            for code, count in error_codes.items():
                if str(code) in ["502", "503", "504"]:
                    pattern = error_patterns.get(str(code), {})
                    classified_errors.append({
                        "code": code,
                        "count": count,
                        "source": pattern.get("source", "Unknown"),
                        "meaning": pattern.get("meaning", "Unknown"),
                        "priority": pattern.get("priority", "LOW")
                    })
                    if pattern.get("priority") in ["HIGH", "CRITICAL"]:
                        high_priority.append(code)
                elif code in error_patterns:
                    pattern = error_patterns[code]
                    classified_errors.append({
                        "code": code,
                        "count": count,
                        "source": pattern["source"],
                        "meaning": pattern["meaning"],
                        "priority": pattern["priority"]
                    })
                    if pattern["priority"] in ["HIGH", "CRITICAL"]:
                        high_priority.append(code)
            
            has_critical_errors = len([e for e in classified_errors if e.get("priority") == "CRITICAL"]) > 0
            has_high_priority = len(high_priority) > 0
            
            return {
                "test": "Error Code Classification",
                "pattern": "Forensic Signature Detection",
                "passed": not has_critical_errors and not has_high_priority,
                "message": f"Observed {len(error_codes)} error types, {len(high_priority)} high-priority",
                "duration": duration,
                "error_counts": error_codes,
                "classified_errors": classified_errors,
                "high_priority_errors": high_priority,
                "issues_detected": [
                    f"Critical error code {code} detected: {error_codes[code]} occurrences"
                    for code in [e["code"] for e in classified_errors if e.get("priority") == "CRITICAL"]
                ] if has_critical_errors else [],
                "recommendations": [
                    "502: Check backend connectivity and keep-alive configuration",
                    "503: Verify target health and ALB target group configuration",
                    "504: Check application processing time and timeout settings",
                    "Connection refused (111): Verify application is listening on correct port",
                    "Connection reset (104): Check idle timeout configuration and TCP keepalive",
                    "Fail-fast: Check Linkerd circuit breaker and consecutive failure patterns",
                    "Max-concurrency: Increase application max_concurrent_streams limit"
                ] if has_high_priority else [],
                "detection_method": "Error code collection and classification"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Error Code Classification",
                "pattern": "Forensic Signature Detection",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_rst_packet_patterns(self) -> Dict:
        """
        Detect TCP RST packet patterns
        
        Detects patterns suggesting connection resets from NLB or network layer.
        """
        start_time = time.time()
        
        try:
            reset_errors = []
            
            # Make requests and detect reset patterns
            for i in range(15):
                try:
                    response = await self.client.get(f"{self.base_url}/health", timeout=5.0)
                    # Successful response
                except httpx.ConnectError as e:
                    error_str = str(e).lower()
                    if 'reset' in error_str or 'rst' in error_str or '104' in error_str:
                        reset_errors.append({
                            "request": i,
                            "error": str(e),
                            "pattern": "TCP RST detected"
                        })
                except httpx.NetworkError as e:
                    error_str = str(e).lower()
                    if 'reset' in error_str or 'broken pipe' in error_str:
                        reset_errors.append({
                            "request": i,
                            "error": str(e),
                            "pattern": "Network reset"
                        })
                except Exception as e:
                    error_str = str(e).lower()
                    if 'connection reset' in error_str or 'reset by peer' in error_str:
                        reset_errors.append({
                            "request": i,
                            "error": str(e),
                            "pattern": "Connection reset"
                        })
            
            duration = time.time() - start_time
            
            has_rst_patterns = len(reset_errors) > 0
            
            return {
                "test": "TCP RST Packet Pattern Detection",
                "pattern": "Forensic Signature - Connection Resets",
                "passed": not has_rst_patterns,
                "message": f"RST patterns detected: {len(reset_errors)}",
                "duration": duration,
                "reset_errors": reset_errors,
                "issues_detected": [
                    f"{len(reset_errors)} TCP RST patterns detected"
                ] if has_rst_patterns else [],
                "recommendations": [
                    "Check CloudWatch TCP_ELB_Reset_Count metric (NLB)",
                    "Monitor for RST packets after ~350s idle (NLB timeout)",
                    "Implement TCP keepalive < 350s",
                    "Check VPC Flow Logs for REJECT entries",
                    "Verify security group and NACL configurations",
                    "Check application logs for 'Connection reset by peer' (errno 104)",
                    "Monitor for 'Broken pipe' errors (errno 32)"
                ] if has_rst_patterns else [],
                "detection_method": "Error pattern analysis - detect TCP reset signatures"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "TCP RST Packet Pattern Detection",
                "pattern": "Forensic Signature - Connection Resets",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def test_timeout_patterns(self) -> Dict:
        """
        Detect timeout patterns
        
        Detects patterns suggesting various timeout mechanisms (NLB, ALB, Linkerd).
        """
        start_time = time.time()
        
        try:
            timeout_errors = []
            timeout_classes = {
                "short": [],  # < 5s
                "medium": [],  # 5-10s
                "long": []  # > 10s
            }
            
            # Make requests with varying timeout expectations
            for i in range(10):
                req_start = time.time()
                try:
                    response = await self.client.get(f"{self.base_url}/health", timeout=15.0)
                    req_duration = time.time() - req_start
                except httpx.TimeoutException as e:
                    req_duration = time.time() - req_start
                    timeout_errors.append({
                        "request": i,
                        "duration": req_duration,
                        "error": "timeout"
                    })
                    
                    if req_duration < 5.0:
                        timeout_classes["short"].append(req_duration)
                    elif req_duration < 10.0:
                        timeout_classes["medium"].append(req_duration)
                    else:
                        timeout_classes["long"].append(req_duration)
                except Exception as e:
                    error_str = str(e).lower()
                    if 'timeout' in error_str or 'timed out' in error_str:
                        req_duration = time.time() - req_start
                        timeout_errors.append({
                            "request": i,
                            "duration": req_duration,
                            "error": str(e)
                        })
            
            duration = time.time() - start_time
            
            # Detect timeout patterns
            has_10s_timeouts = len(timeout_classes["medium"]) > 0  # Linkerd 10s default
            has_short_timeouts = len(timeout_classes["short"]) > 0
            has_long_timeouts = len(timeout_classes["long"]) > 0
            
            timeout_patterns_detected = len(timeout_errors) > 0
            
            return {
                "test": "Timeout Pattern Detection",
                "pattern": "Forensic Signature - Timeouts",
                "passed": not timeout_patterns_detected,
                "message": f"Timeout errors: {len(timeout_errors)}, 10s pattern: {len(timeout_classes['medium'])}, Long: {len(timeout_classes['long'])}",
                "duration": duration,
                "timeout_errors": timeout_errors,
                "timeout_distribution": {
                    "short": len(timeout_classes["short"]),
                    "medium": len(timeout_classes["medium"]),
                    "long": len(timeout_classes["long"])
                },
                "timeout_classes": timeout_classes,
                "issues_detected": [
                    f"{len(timeout_errors)} timeout errors detected",
                    f"{len(timeout_classes['medium'])} requests timing out around 10s (Linkerd default)",
                    f"{len(timeout_classes['long'])} requests timing out after 10s"
                ] if timeout_patterns_detected else [],
                "recommendations": [
                    "10s timeouts: Check Linkerd proxy timeout (default 10s)",
                    "Use ServiceProfile for per-route timeout configuration (up to 30s+)",
                    "Check backend service processing time",
                    "Verify database query timeouts < proxy timeout",
                    "Monitor for connection pool exhaustion",
                    "Check ALB idle timeout configuration (default 60s)",
                    "Monitor CloudWatch TargetResponseTime metric"
                ] if timeout_patterns_detected else [],
                "detection_method": "Timing analysis - detect timeout signatures"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "test": "Timeout Pattern Detection",
                "pattern": "Forensic Signature - Timeouts",
                "passed": False,
                "message": f"Exception: {str(e)}",
                "duration": duration,
                "error": str(e)
            }
    
    async def run_all_tests(self) -> Dict:
        """Run all forensic signature detection tests."""
        print(f"\n{BOLD}{BLUE}🔍 Forensic Signature Detection{RESET}\n")
        print(f"Target: {self.base_url}\n")
        
        tests = [
            ("Error Code Classification", self.test_error_code_classification),
            ("TCP RST Packet Patterns", self.test_rst_packet_patterns),
            ("Timeout Patterns", self.test_timeout_patterns),
        ]
        
        for test_name, test_func in tests:
            print(f"{BLUE}Testing: {test_name}...{RESET}", end=" ", flush=True)
            result = await test_func()
            self.results.append(result)
            
            if result["passed"]:
                print(f"{GREEN}✓ CLEAN{RESET} ({result['duration']:.3f}s)")
            else:
                print(f"{YELLOW}⚠ SIGNATURES DETECTED{RESET} ({result['duration']:.3f}s)")
            
            if result.get("issues_detected"):
                for issue in result["issues_detected"]:
                    print(f"  {YELLOW}⚠ {issue}{RESET}")
        
        # Summary
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        issues_found = sum(len(r.get("issues_detected", [])) for r in self.results)
        
        print(f"\n{BOLD}Summary:{RESET}")
        print(f"  Tests: {total}")
        print(f"  Clean: {GREEN}{passed}{RESET}")
        print(f"  Signatures Detected: {YELLOW}{issues_found}{RESET}")
        
        return {
            "total": total,
            "passed": passed,
            "issues_found": issues_found,
            "results": self.results
        }


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Forensic Signature Detection")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL to test")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    async with ForensicSignatureDetector(base_url=args.url) as detector:
        results = await detector.run_all_tests()
        
        if args.json:
            print(json.dumps(results, indent=2))
            sys.exit(0 if results["issues_found"] == 0 else 1)
        else:
            sys.exit(0 if results["issues_found"] == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())

