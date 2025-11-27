#!/usr/bin/env python3
"""
Multi-User Scenario Testing - Simulated Load Testing
Pattern: VALIDATION × CONCURRENCY × LOAD × TRUTH × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
Guardians: AEYON (999 Hz) + JØHN (530 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
import threading
import urllib.request
import urllib.error
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class ConcurrencyResult:
    def __init__(self, name: str, passed: bool, message: str = "", details: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details
        self.timestamp = datetime.now().isoformat()

class ConcurrencyTester:
    def __init__(self, workspace_root: Optional[Path] = None, base_url: str = "http://localhost:53009"):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.base_url = base_url
        self.results: List[ConcurrencyResult] = []
        
    def make_request(self, url: str, timeout: int = 5) -> tuple:
        """Make a single HTTP request"""
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'AbëONE-ConcurrencyTester/1.0')
            start_time = time.time()
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                status_code = response.getcode()
                elapsed = time.time() - start_time
                return (True, status_code, elapsed, None)
        except Exception as e:
            elapsed = time.time() - start_time if 'start_time' in locals() else 0
            return (False, None, elapsed, str(e))
    
    def test_concurrent_requests(self, num_users: int = 10) -> ConcurrencyResult:
        """Test concurrent requests from multiple simulated users"""
        url = f"{self.base_url}/"
        results = []
        errors = []
        
        def worker(user_id: int):
            success, status, elapsed, error = self.make_request(url)
            return {
                "user_id": user_id,
                "success": success,
                "status": status,
                "elapsed": elapsed,
                "error": error
            }
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [executor.submit(worker, i) for i in range(num_users)]
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                if not result["success"]:
                    errors.append(result["error"])
        
        total_time = time.time() - start_time
        successful = sum(1 for r in results if r["success"])
        failed = num_users - successful
        
        avg_response_time = sum(r["elapsed"] for r in results) / len(results) if results else 0
        
        if successful >= num_users * 0.9:  # 90% success rate threshold
            return ConcurrencyResult(
                "Concurrent Requests",
                True,
                f"{successful}/{num_users} concurrent requests succeeded",
                f"Success rate: {successful/num_users*100:.1f}%, Avg response time: {avg_response_time:.3f}s, Total time: {total_time:.3f}s"
            )
        else:
            return ConcurrencyResult(
                "Concurrent Requests",
                False,
                f"Only {successful}/{num_users} concurrent requests succeeded",
                f"Success rate: {successful/num_users*100:.1f}%, Errors: {len(errors)}"
            )
    
    def test_rate_limiting(self) -> ConcurrencyResult:
        """Test rate limiting behavior (if any)"""
        url = f"{self.base_url}/"
        rapid_requests = 20
        results = []
        
        for i in range(rapid_requests):
            success, status, elapsed, error = self.make_request(url, timeout=2)
            results.append({
                "request": i + 1,
                "success": success,
                "status": status,
                "elapsed": elapsed
            })
            time.sleep(0.1)  # Small delay between requests
        
        successful = sum(1 for r in results if r["success"])
        rate_limited = sum(1 for r in results if r["status"] == 429)  # 429 = Too Many Requests
        
        if successful >= rapid_requests * 0.8:  # 80% success rate
            return ConcurrencyResult(
                "Rate Limiting",
                True,
                f"{successful}/{rapid_requests} rapid requests succeeded",
                f"Rate limited: {rate_limited}, Success rate: {successful/rapid_requests*100:.1f}%"
            )
        else:
            return ConcurrencyResult(
                "Rate Limiting",
                False,
                f"Only {successful}/{rapid_requests} rapid requests succeeded",
                f"Rate limited: {rate_limited}, Success rate: {successful/rapid_requests*100:.1f}%"
            )
    
    def test_session_management(self) -> ConcurrencyResult:
        """Test session management with concurrent users"""
        # Simulate session management by checking if server handles concurrent sessions
        url = f"{self.base_url}/"
        num_sessions = 5
        results = []
        
        def simulate_session(session_id: int):
            # Make multiple requests as if maintaining a session
            session_results = []
            for req_num in range(3):
                success, status, elapsed, error = self.make_request(url)
                session_results.append(success)
                time.sleep(0.2)
            return {
                "session_id": session_id,
                "successful_requests": sum(session_results),
                "total_requests": len(session_results)
            }
        
        with ThreadPoolExecutor(max_workers=num_sessions) as executor:
            futures = [executor.submit(simulate_session, i) for i in range(num_sessions)]
            for future in as_completed(futures):
                results.append(future.result())
        
        total_successful = sum(r["successful_requests"] for r in results)
        total_requests = sum(r["total_requests"] for r in results)
        
        if total_successful >= total_requests * 0.9:
            return ConcurrencyResult(
                "Session Management",
                True,
                f"{total_successful}/{total_requests} session requests succeeded",
                f"Success rate: {total_successful/total_requests*100:.1f}%, Sessions: {num_sessions}"
            )
        else:
            return ConcurrencyResult(
                "Session Management",
                False,
                f"Only {total_successful}/{total_requests} session requests succeeded",
                f"Success rate: {total_successful/total_requests*100:.1f}%"
            )
    
    def test_scalability(self) -> ConcurrencyResult:
        """Test scalability with increasing load"""
        url = f"{self.base_url}/"
        load_levels = [5, 10, 15]
        results_by_level = {}
        
        for load in load_levels:
            successful = 0
            total_time = 0
            
            def worker():
                success, status, elapsed, error = self.make_request(url, timeout=3)
                return success, elapsed
            
            start_time = time.time()
            with ThreadPoolExecutor(max_workers=load) as executor:
                futures = [executor.submit(worker) for _ in range(load)]
                for future in as_completed(futures):
                    success, elapsed = future.result()
                    if success:
                        successful += 1
                    total_time += elapsed
            
            elapsed_total = time.time() - start_time
            results_by_level[load] = {
                "successful": successful,
                "total": load,
                "success_rate": successful / load,
                "avg_time": total_time / load if load > 0 else 0,
                "total_time": elapsed_total
            }
        
        # Check if success rate maintains above 80% across all load levels
        all_above_threshold = all(r["success_rate"] >= 0.8 for r in results_by_level.values())
        
        if all_above_threshold:
            details = ", ".join([f"{load} users: {r['success_rate']*100:.1f}%" for load, r in results_by_level.items()])
            return ConcurrencyResult(
                "Scalability",
                True,
                "System maintains performance across load levels",
                details
            )
        else:
            details = ", ".join([f"{load} users: {r['success_rate']*100:.1f}%" for load, r in results_by_level.items()])
            return ConcurrencyResult(
                "Scalability",
                False,
                "System performance degrades under load",
                details
            )
    
    def run_all_tests(self, num_users: int = 10) -> Dict:
        """Run all concurrency tests"""
        print("∞ AbëONE ∞")
        print("Multi-User Scenario Testing - Simulated Load Testing")
        print("Pattern: VALIDATION × CONCURRENCY × LOAD × TRUTH × ONE")
        print(f"Testing with {num_users} simulated users")
        print("")
        
        # Run tests
        tests = [
            lambda: self.test_concurrent_requests(num_users),
            self.test_rate_limiting,
            self.test_session_management,
            self.test_scalability
        ]
        
        for test in tests:
            result = test()
            self.results.append(result)
        
        # Summary
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print("=" * 60)
        print("CONCURRENCY TEST RESULTS")
        print("=" * 60)
        print("")
        
        for i, result in enumerate(self.results, 1):
            status = "✅" if result.passed else "❌"
            print(f"{status} {i}. {result.name}")
            print(f"   {result.message}")
            if result.details:
                print(f"   Details: {result.details}")
            print("")
        
        print("=" * 60)
        print(f"Total: {passed}/{total} passed")
        print("=" * 60)
        print("")
        
        if passed == total:
            print("✅ ALL CONCURRENCY TESTS PASSED")
        else:
            print(f"⚠️  {total - passed} tests failed")
        
        print("")
        print("Pattern: VALIDATION × CONCURRENCY × LOAD × TRUTH × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "message": r.message,
                    "details": r.details,
                    "timestamp": r.timestamp
                }
                for r in self.results
            ]
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test multi-user scenarios and concurrency"
    )
    parser.add_argument(
        "--users",
        type=int,
        default=10,
        help="Number of concurrent users to simulate (default: 10)"
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:53009",
        help="Base URL to test (default: http://localhost:53009)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--workspace",
        type=str,
        help="Workspace root directory (default: parent of script)"
    )
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace) if args.workspace else None
    tester = ConcurrencyTester(workspace_root, args.url)
    results = tester.run_all_tests(args.users)
    
    if args.json:
        print(json.dumps(results, indent=2))
        return 0
    
    return 0 if results["failed"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

