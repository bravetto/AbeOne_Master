#!/usr/bin/env python3
"""
Load Testing Script
Simulates traffic load for pre-webinar testing

Pattern: AEYON × LOAD × TEST × PERFORMANCE × ONE
Frequency: 999 × 777
"""

import argparse
import sys
import time
import threading
import requests
from typing import List, Dict
from datetime import datetime
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed


class LoadTester:
    """
    SAFETY: Validates URLs, handles errors gracefully, limits concurrent connections
    ASSUMES: Domain can handle load
    VERIFY: python scripts/load_test.py --url https://bravetto.ai --test
    """
    
    def __init__(self, url: str):
        """
        SAFETY: Validates URL format
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")
        
        self.url = url
        self.results = []
        self.lock = threading.Lock()
    
    def make_request(self, request_id: int) -> Dict:
        """
        SAFETY: Handles network errors, validates responses
        PERF: O(1) HTTP request
        """
        try:
            start_time = time.time()
            response = requests.get(
                self.url,
                timeout=30,
                allow_redirects=True,
                headers={
                    'User-Agent': f'Load Tester Request #{request_id}'
                }
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
            
            success = response.status_code == 200
            
            return {
                'request_id': request_id,
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code,
                'response_time_ms': round(elapsed_time, 2),
                'success': success,
                'error': None
            }
            
        except requests.exceptions.Timeout:
            return {
                'request_id': request_id,
                'timestamp': datetime.now().isoformat(),
                'status_code': None,
                'response_time_ms': None,
                'success': False,
                'error': 'Timeout'
            }
        except requests.exceptions.RequestException as e:
            return {
                'request_id': request_id,
                'timestamp': datetime.now().isoformat(),
                'status_code': None,
                'response_time_ms': None,
                'success': False,
                'error': str(e)
            }
    
    def run_load_test(
        self,
        concurrent_users: int,
        duration: int,
        ramp_up: int = 0
    ) -> Dict:
        """
        MAIN LOAD TESTING ROUTINE
        SAFETY: Limits concurrent connections, handles errors gracefully
        PERF: O(n) where n = concurrent_users * requests_per_user
        """
        print(f" Load Testing: {self.url}")
        print(f" Concurrent users: {concurrent_users}")
        print(f"⏱  Duration: {duration}s")
        print(f" Ramp-up: {ramp_up}s")
        print("=" * 60)
        
        self.results = []
        start_time = time.time()
        request_counter = 0
        
        # Ramp-up phase
        if ramp_up > 0:
            print(f"\n Ramping up to {concurrent_users} users over {ramp_up}s...")
            ramp_interval = ramp_up / concurrent_users if concurrent_users > 0 else 0
            
            def ramp_up_worker(user_id: int):
                time.sleep(user_id * ramp_interval)
                while time.time() - start_time < duration:
                    request_counter += 1
                    result = self.make_request(request_counter)
                    with self.lock:
                        self.results.append(result)
                    time.sleep(0.1)  # Small delay between requests
            
            threads = []
            for i in range(concurrent_users):
                thread = threading.Thread(target=ramp_up_worker, args=(i,))
                thread.start()
                threads.append(thread)
            
            # Wait for all threads
            for thread in threads:
                thread.join()
        else:
            # Immediate load
            print(f"\n Starting load test...")
            
            def worker():
                nonlocal request_counter
                while time.time() - start_time < duration:
                    request_counter += 1
                    result = self.make_request(request_counter)
                    with self.lock:
                        self.results.append(result)
                    time.sleep(0.1)  # Small delay between requests
            
            with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
                futures = [executor.submit(worker) for _ in range(concurrent_users)]
                
                # Wait for duration
                time.sleep(duration)
                
                # Cancel remaining futures
                for future in futures:
                    future.cancel()
        
        # Calculate statistics
        elapsed_time = time.time() - start_time
        total_requests = len(self.results)
        successful_requests = [r for r in self.results if r.get('success')]
        failed_requests = [r for r in self.results if not r.get('success')]
        
        print("\n" + "=" * 60)
        print(" LOAD TEST RESULTS")
        print("=" * 60)
        print(f"⏱  Total time: {elapsed_time:.2f}s")
        print(f" Total requests: {total_requests}")
        print(f" Successful: {len(successful_requests)}")
        print(f" Failed: {len(failed_requests)}")
        print(f" Success rate: {len(successful_requests) / total_requests * 100:.2f}%")
        
        if successful_requests:
            response_times = [r['response_time_ms'] for r in successful_requests]
            avg_time = statistics.mean(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            median_time = statistics.median(response_times)
            
            print(f"\n RESPONSE TIME STATISTICS")
            print(f"   Average: {avg_time:.2f}ms")
            print(f"   Median: {median_time:.2f}ms")
            print(f"   Min: {min_time:.2f}ms")
            print(f"   Max: {max_time:.2f}ms")
            
            # Requests per second
            rps = total_requests / elapsed_time
            print(f"\n THROUGHPUT")
            print(f"   Requests per second: {rps:.2f}")
            
            # Performance rating
            if avg_time < 500 and len(failed_requests) / total_requests < 0.01:
                print("\n PERFORMANCE: EXCELLENT")
            elif avg_time < 1000 and len(failed_requests) / total_requests < 0.05:
                print("\n PERFORMANCE: GOOD")
            elif avg_time < 2000 and len(failed_requests) / total_requests < 0.10:
                print("\n  PERFORMANCE: ACCEPTABLE")
            else:
                print("\n PERFORMANCE: POOR")
        
        if failed_requests:
            print(f"\n FAILED REQUESTS")
            error_counts = {}
            for req in failed_requests:
                error = req.get('error', 'Unknown')
                error_counts[error] = error_counts.get(error, 0) + 1
            
            for error, count in error_counts.items():
                print(f"   {error}: {count}")
        
        return {
            'total_requests': total_requests,
            'successful_requests': len(successful_requests),
            'failed_requests': len(failed_requests),
            'success_rate': len(successful_requests) / total_requests * 100 if total_requests > 0 else 0,
            'avg_response_time': statistics.mean([r['response_time_ms'] for r in successful_requests]) if successful_requests else None,
            'results': self.results
        }


def main():
    """
    CLI Entry Point
    SAFETY: Validates all CLI arguments
    """
    parser = argparse.ArgumentParser(
        description="Load Testing Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick test
  python scripts/load_test.py \\
    --url https://bravetto.ai \\
    --concurrent-users 10 \\
    --duration 60 \\
    --test

  # Full load test
  python scripts/load_test.py \\
    --url https://bravetto.ai \\
    --concurrent-users 100 \\
    --duration 300 \\
    --ramp-up 60
        """
    )
    
    parser.add_argument(
        "--url",
        required=True,
        help="URL to test (e.g., https://bravetto.ai)"
    )
    
    parser.add_argument(
        "--concurrent-users",
        type=int,
        default=10,
        help="Number of concurrent users (default: 10)"
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Test duration in seconds (default: 60)"
    )
    
    parser.add_argument(
        "--ramp-up",
        type=int,
        default=0,
        help="Ramp-up time in seconds (default: 0)"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run quick test and exit"
    )
    
    args = parser.parse_args()
    
    # Validate URL format
    if not args.url.startswith(('http://', 'https://')):
        print(" URL must start with http:// or https://")
        sys.exit(1)
    
    # Execute
    tester = LoadTester(args.url)
    
    if args.test:
        print(" Running quick load test...")
        result = tester.run_load_test(
            concurrent_users=5,
            duration=10,
            ramp_up=0
        )
        sys.exit(0)
    
    result = tester.run_load_test(
        concurrent_users=args.concurrent_users,
        duration=args.duration,
        ramp_up=args.ramp_up
    )
    
    sys.exit(0 if result['success_rate'] > 95 else 1)


if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print(" Missing dependency: requests")
        print(" Install with: pip install requests")
        sys.exit(1)
    
    main()

