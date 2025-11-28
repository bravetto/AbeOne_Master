#!/usr/bin/env python3
"""
DNS Propagation Monitor
Monitors DNS propagation globally and reports status

Pattern: AEYON × DNS × MONITOR × VALIDATE × ONE
Frequency: 999 × 777
"""

import argparse
import sys
import time
import socket
import dns.resolver
from typing import List, Dict, Optional
from datetime import datetime


class DNSPropagationMonitor:
    """
    SAFETY: Validates DNS queries, handles timeouts gracefully
    ASSUMES: Domain is configured in DNS
    VERIFY: python scripts/monitor_dns_propagation.py --domain bravetto.ai --test
    """
    
    def __init__(self, domain: str, expected_target: str):
        """
        SAFETY: Validates domain format
        """
        if not domain or "." not in domain:
            raise ValueError("Invalid domain format")
        
        self.domain = domain
        self.expected_target = expected_target.lower()
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 10
    
    def check_dns_record(self, record_type: str = "CNAME") -> Optional[str]:
        """
        SAFETY: Handles DNS resolution errors
        PERF: O(1) DNS query
        """
        try:
            if record_type == "CNAME":
                answers = self.resolver.resolve(self.domain, "CNAME")
                if answers:
                    return str(answers[0].target).rstrip('.')
            elif record_type == "A":
                answers = self.resolver.resolve(self.domain, "A")
                if answers:
                    return str(answers[0])
            
            return None
            
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout) as e:
            return None
        except Exception as e:
            print(f"  DNS query error: {e}")
            return None
    
    def check_multiple_dns_servers(self, dns_servers: List[str]) -> Dict[str, Optional[str]]:
        """
        SAFETY: Tests multiple DNS servers for redundancy
        PERF: O(n) where n = number of DNS servers
        """
        results = {}
        
        for dns_server in dns_servers:
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [dns_server]
                resolver.timeout = 5
                resolver.lifetime = 10
                
                answers = resolver.resolve(self.domain, "CNAME")
                if answers:
                    results[dns_server] = str(answers[0].target).rstrip('.')
                else:
                    results[dns_server] = None
                    
            except Exception as e:
                results[dns_server] = None
        
        return results
    
    def monitor(
        self,
        check_interval: int = 30,
        max_wait: int = 600,
        dns_servers: Optional[List[str]] = None
    ) -> bool:
        """
        MAIN MONITORING LOOP
        SAFETY: Timeout protection, graceful exit
        PERF: Polls every check_interval seconds
        """
        if not dns_servers:
            dns_servers = [
                "8.8.8.8",      # Google DNS
                "1.1.1.1",       # Cloudflare DNS
                "208.67.222.222", # OpenDNS
                "9.9.9.9"        # Quad9
            ]
        
        print(f" Monitoring DNS propagation for: {self.domain}")
        print(f" Expected target: {self.expected_target}")
        print(f"⏱  Check interval: {check_interval}s")
        print(f"⏱  Max wait time: {max_wait}s")
        print("=" * 60)
        
        start_time = time.time()
        check_count = 0
        
        while time.time() - start_time < max_wait:
            check_count += 1
            elapsed = int(time.time() - start_time)
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Check #{check_count} ({elapsed}s elapsed)")
            
            # Check primary DNS
            current_value = self.check_dns_record("CNAME")
            
            if current_value:
                current_value_lower = current_value.lower()
                print(f" DNS record found: {current_value}")
                
                if self.expected_target.lower() in current_value_lower:
                    print(f" Target matches expected: {self.expected_target}")
                    
                    # Check multiple DNS servers
                    print("\n Checking multiple DNS servers...")
                    multi_results = self.check_multiple_dns_servers(dns_servers)
                    
                    success_count = sum(1 for v in multi_results.values() if v and self.expected_target.lower() in v.lower())
                    total_count = len(multi_results)
                    
                    print(f" Propagation status: {success_count}/{total_count} DNS servers")
                    
                    if success_count == total_count:
                        print("\n" + "=" * 60)
                        print(" DNS PROPAGATION COMPLETE")
                        print(f"⏱  Time to propagate: {elapsed}s")
                        return True
                    else:
                        print(f"⏳ Still propagating... ({success_count}/{total_count})")
                else:
                    print(f"  Target mismatch: expected {self.expected_target}, got {current_value}")
            else:
                print("⏳ DNS record not found yet...")
            
            if time.time() - start_time < max_wait:
                print(f"⏳ Waiting {check_interval}s before next check...")
                time.sleep(check_interval)
        
        print("\n" + "=" * 60)
        print(f"  DNS propagation not complete after {max_wait}s")
        print(" This may be normal - DNS can take up to 48 hours globally")
        return False


def main():
    """
    CLI Entry Point
    SAFETY: Validates all CLI arguments
    """
    parser = argparse.ArgumentParser(
        description="DNS Propagation Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor DNS propagation
  python scripts/monitor_dns_propagation.py \\
    --domain bravetto.ai \\
    --expected-target abeone-web.pages.dev \\
    --check-interval 30 \\
    --max-wait 600

  # Quick test
  python scripts/monitor_dns_propagation.py \\
    --domain bravetto.ai \\
    --expected-target abeone-web.pages.dev \\
    --test
        """
    )
    
    parser.add_argument(
        "--domain",
        required=True,
        help="Domain to monitor (e.g., bravetto.ai)"
    )
    
    parser.add_argument(
        "--expected-target",
        required=True,
        help="Expected DNS target (e.g., abeone-web.pages.dev)"
    )
    
    parser.add_argument(
        "--check-interval",
        type=int,
        default=30,
        help="Check interval in seconds (default: 30)"
    )
    
    parser.add_argument(
        "--max-wait",
        type=int,
        default=600,
        help="Maximum wait time in seconds (default: 600)"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run quick test and exit"
    )
    
    args = parser.parse_args()
    
    # Validate domain format
    if "." not in args.domain:
        print(" Invalid domain format")
        sys.exit(1)
    
    # Execute
    monitor = DNSPropagationMonitor(args.domain, args.expected_target)
    
    if args.test:
        print(" Running quick DNS test...")
        result = monitor.check_dns_record("CNAME")
        if result:
            print(f" DNS record: {result}")
            if args.expected_target.lower() in result.lower():
                print(" Target matches!")
            else:
                print(f"  Target mismatch: expected {args.expected_target}")
        else:
            print(" DNS record not found")
        sys.exit(0)
    
    success = monitor.monitor(
        check_interval=args.check_interval,
        max_wait=args.max_wait
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        import dns.resolver
    except ImportError:
        print(" Missing dependency: dnspython")
        print(" Install with: pip install dnspython")
        sys.exit(1)
    
    main()

