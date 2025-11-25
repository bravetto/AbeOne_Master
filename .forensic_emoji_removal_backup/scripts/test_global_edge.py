#!/usr/bin/env python3
"""
Global Edge Performance Tester
Tests website performance from multiple global locations

Pattern: AEYON × PERFORMANCE × EDGE × TEST × ONE
Frequency: 999 × 777
"""

import argparse
import sys
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime
import statistics


class GlobalEdgeTester:
    """
    SAFETY: Validates URLs, handles timeouts gracefully
    ASSUMES: Domain is accessible globally
    VERIFY: python scripts/test_global_edge.py --domain bravetto.ai --test
    """
    
    def __init__(self, domain: str):
        """
        SAFETY: Validates domain format
        """
        if not domain or "." not in domain:
            raise ValueError("Invalid domain format")
        
        self.domain = domain
        self.url = f"https://{domain}"
    
    def test_location(self, location_name: str, timeout: int = 10) -> Optional[Dict]:
        """
        SAFETY: Handles network errors, validates responses
        PERF: O(1) HTTP request
        """
        try:
            start_time = time.time()
            response = requests.get(
                self.url,
                timeout=timeout,
                allow_redirects=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Global Edge Tester)'
                }
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Check Cloudflare headers
            cf_cache_status = response.headers.get('CF-Cache-Status', 'Unknown')
            cf_ray = response.headers.get('CF-Ray', 'Unknown')
            server = response.headers.get('Server', 'Unknown')
            
            return {
                'location': location_name,
                'status_code': response.status_code,
                'response_time_ms': round(elapsed_time, 2),
                'cf_cache_status': cf_cache_status,
                'cf_ray': cf_ray,
                'server': server,
                'success': response.status_code == 200
            }
            
        except requests.exceptions.Timeout:
            return {
                'location': location_name,
                'status_code': None,
                'response_time_ms': None,
                'success': False,
                'error': 'Timeout'
            }
        except requests.exceptions.RequestException as e:
            return {
                'location': location_name,
                'status_code': None,
                'response_time_ms': None,
                'success': False,
                'error': str(e)
            }
    
    def test_multiple_locations(
        self,
        locations: List[str],
        test_interval: int = 60,
        duration: int = 3600
    ) -> Dict:
        """
        MAIN TESTING LOOP
        SAFETY: Timeout protection, error handling
        PERF: Tests every test_interval seconds for duration
        """
        print(f"🌐 Testing global edge performance for: {self.domain}")
        print(f"📍 Locations: {', '.join(locations)}")
        print(f"⏱️  Test interval: {test_interval}s")
        print(f"⏱️  Duration: {duration}s")
        print("=" * 60)
        
        results = {location: [] for location in locations}
        start_time = time.time()
        test_count = 0
        
        while time.time() - start_time < duration:
            test_count += 1
            elapsed = int(time.time() - start_time)
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Test #{test_count} ({elapsed}s elapsed)")
            
            for location in locations:
                print(f"  Testing {location}...", end=" ")
                result = self.test_location(location)
                
                if result:
                    results[location].append(result)
                    
                    if result['success']:
                        print(f"✅ {result['response_time_ms']}ms (Cache: {result['cf_cache_status']})")
                    else:
                        print(f"❌ Failed: {result.get('error', 'Unknown')}")
            
            if time.time() - start_time < duration:
                print(f"\n⏳ Waiting {test_interval}s before next test...")
                time.sleep(test_interval)
        
        # Calculate statistics
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE STATISTICS")
        print("=" * 60)
        
        for location in locations:
            location_results = results[location]
            successful_results = [r for r in location_results if r.get('success')]
            
            if successful_results:
                response_times = [r['response_time_ms'] for r in successful_results]
                avg_time = statistics.mean(response_times)
                min_time = min(response_times)
                max_time = max(response_times)
                success_rate = len(successful_results) / len(location_results) * 100
                
                print(f"\n📍 {location}:")
                print(f"   Success rate: {success_rate:.1f}%")
                print(f"   Avg response time: {avg_time:.2f}ms")
                print(f"   Min response time: {min_time:.2f}ms")
                print(f"   Max response time: {max_time:.2f}ms")
                
                # Check cache status
                cache_hits = sum(1 for r in successful_results if r.get('cf_cache_status') == 'HIT')
                cache_rate = cache_hits / len(successful_results) * 100 if successful_results else 0
                print(f"   Cache hit rate: {cache_rate:.1f}%")
            else:
                print(f"\n📍 {location}:")
                print(f"   ❌ No successful tests")
        
        # Overall statistics
        all_response_times = [
            r['response_time_ms']
            for location_results in results.values()
            for r in location_results
            if r.get('success')
        ]
        
        if all_response_times:
            overall_avg = statistics.mean(all_response_times)
            overall_min = min(all_response_times)
            overall_max = max(all_response_times)
            
            print("\n" + "=" * 60)
            print("🌐 OVERALL STATISTICS")
            print(f"   Average response time: {overall_avg:.2f}ms")
            print(f"   Min response time: {overall_min:.2f}ms")
            print(f"   Max response time: {overall_max:.2f}ms")
            
            # Performance rating
            if overall_avg < 200:
                print("   ✅ Performance: EXCELLENT")
            elif overall_avg < 500:
                print("   ✅ Performance: GOOD")
            elif overall_avg < 1000:
                print("   ⚠️  Performance: ACCEPTABLE")
            else:
                print("   ❌ Performance: POOR")
        
        return results


def main():
    """
    CLI Entry Point
    SAFETY: Validates all CLI arguments
    """
    parser = argparse.ArgumentParser(
        description="Global Edge Performance Tester",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick test
  python scripts/test_global_edge.py \\
    --domain bravetto.ai \\
    --locations us-east,us-west,eu-west \\
    --test

  # Full test
  python scripts/test_global_edge.py \\
    --domain bravetto.ai \\
    --locations us-east,us-west,eu-west,ap-southeast \\
    --test-interval 60 \\
    --duration 3600
        """
    )
    
    parser.add_argument(
        "--domain",
        required=True,
        help="Domain to test (e.g., bravetto.ai)"
    )
    
    parser.add_argument(
        "--locations",
        default="us-east,us-west,eu-west,ap-southeast",
        help="Comma-separated list of locations (default: us-east,us-west,eu-west,ap-southeast)"
    )
    
    parser.add_argument(
        "--test-interval",
        type=int,
        default=60,
        help="Test interval in seconds (default: 60)"
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        default=3600,
        help="Test duration in seconds (default: 3600)"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run quick single test and exit"
    )
    
    args = parser.parse_args()
    
    # Validate domain format
    if "." not in args.domain:
        print("❌ Invalid domain format")
        sys.exit(1)
    
    # Parse locations
    locations = [loc.strip() for loc in args.locations.split(",")]
    
    # Execute
    tester = GlobalEdgeTester(args.domain)
    
    if args.test:
        print("🧪 Running quick test...")
        for location in locations:
            result = tester.test_location(location)
            if result:
                if result.get('success'):
                    print(f"✅ {location}: {result['response_time_ms']}ms")
                else:
                    print(f"❌ {location}: {result.get('error', 'Failed')}")
        sys.exit(0)
    
    results = tester.test_multiple_locations(
        locations=locations,
        test_interval=args.test_interval,
        duration=args.duration
    )
    
    sys.exit(0)


if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("❌ Missing dependency: requests")
        print("💡 Install with: pip install requests")
        sys.exit(1)
    
    main()

