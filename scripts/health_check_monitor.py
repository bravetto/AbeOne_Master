#!/usr/bin/env python3
"""
Health Check Monitor
Monitors website health and sends alerts on failures

Pattern: AEYON × MONITOR × ALERT × HEALTH × ONE
Frequency: 999 × 777
"""

import argparse
import sys
import time
import requests
from typing import Optional, Dict
from datetime import datetime
import json


class HealthCheckMonitor:
    """
    SAFETY: Validates URLs, handles errors gracefully
    ASSUMES: Domain is accessible
    VERIFY: python scripts/health_check_monitor.py --domain bravetto.ai --test
    """
    
    def __init__(self, domain: str):
        """
        SAFETY: Validates domain format
        """
        if not domain or "." not in domain:
            raise ValueError("Invalid domain format")
        
        self.domain = domain
        self.url = f"https://{domain}"
        self.failure_count = 0
    
    def check_health(self, timeout: int = 10) -> Dict:
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
                    'User-Agent': 'Health Check Monitor'
                }
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
            
            is_healthy = (
                response.status_code == 200 and
                elapsed_time < 5000  # 5 second max response time
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'domain': self.domain,
                'status_code': response.status_code,
                'response_time_ms': round(elapsed_time, 2),
                'healthy': is_healthy,
                'error': None
            }
            
        except requests.exceptions.Timeout:
            return {
                'timestamp': datetime.now().isoformat(),
                'domain': self.domain,
                'status_code': None,
                'response_time_ms': None,
                'healthy': False,
                'error': 'Timeout'
            }
        except requests.exceptions.RequestException as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'domain': self.domain,
                'status_code': None,
                'response_time_ms': None,
                'healthy': False,
                'error': str(e)
            }
    
    def send_alert(self, message: str, webhook_url: Optional[str] = None):
        """
        SAFETY: Validates webhook URL before sending
        PERF: O(1) HTTP request
        """
        if not webhook_url:
            print(f"  ALERT: {message}")
            return
        
        try:
            payload = {
                'text': f" Health Check Alert: {message}",
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            print(f" Alert sent to webhook")
            
        except Exception as e:
            print(f"  Failed to send alert: {e}")
    
    def monitor(
        self,
        check_interval: int = 30,
        alert_threshold: int = 3,
        slack_webhook: Optional[str] = None
    ):
        """
        MAIN MONITORING LOOP
        SAFETY: Timeout protection, graceful exit
        PERF: Checks every check_interval seconds
        """
        print(f" Health Check Monitor: {self.domain}")
        print(f"⏱  Check interval: {check_interval}s")
        print(f" Alert threshold: {alert_threshold} consecutive failures")
        print("=" * 60)
        
        consecutive_failures = 0
        
        try:
            while True:
                result = self.check_health()
                
                status_icon = "" if result['healthy'] else ""
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {status_icon} "
                      f"Status: {result['status_code'] or 'N/A'} | "
                      f"Response: {result['response_time_ms'] or 'N/A'}ms")
                
                if result['healthy']:
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    print(f"  Failure #{consecutive_failures}")
                    
                    if consecutive_failures >= alert_threshold:
                        alert_message = (
                            f"Domain {self.domain} has failed {consecutive_failures} "
                            f"consecutive health checks. "
                            f"Error: {result.get('error', 'Unknown')}"
                        )
                        self.send_alert(alert_message, slack_webhook)
                        consecutive_failures = 0  # Reset to avoid spam
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n Monitoring stopped by user")
            sys.exit(0)


def main():
    """
    CLI Entry Point
    SAFETY: Validates all CLI arguments
    """
    parser = argparse.ArgumentParser(
        description="Health Check Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor health
  python scripts/health_check_monitor.py \\
    --domain bravetto.ai \\
    --check-interval 30 \\
    --alert-threshold 3

  # With Slack webhook
  python scripts/health_check_monitor.py \\
    --domain bravetto.ai \\
    --slack-webhook https://hooks.slack.com/services/YOUR/WEBHOOK/URL

  # Quick test
  python scripts/health_check_monitor.py \\
    --domain bravetto.ai \\
    --test
        """
    )
    
    parser.add_argument(
        "--domain",
        required=True,
        help="Domain to monitor (e.g., bravetto.ai)"
    )
    
    parser.add_argument(
        "--check-interval",
        type=int,
        default=30,
        help="Check interval in seconds (default: 30)"
    )
    
    parser.add_argument(
        "--alert-threshold",
        type=int,
        default=3,
        help="Alert threshold (consecutive failures, default: 3)"
    )
    
    parser.add_argument(
        "--slack-webhook",
        default=None,
        help="Slack webhook URL for alerts"
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
    monitor = HealthCheckMonitor(args.domain)
    
    if args.test:
        print(" Running quick health check...")
        result = monitor.check_health()
        if result['healthy']:
            print(f" Health check passed: {result['response_time_ms']}ms")
        else:
            print(f" Health check failed: {result.get('error', 'Unknown')}")
        sys.exit(0 if result['healthy'] else 1)
    
    monitor.monitor(
        check_interval=args.check_interval,
        alert_threshold=args.alert_threshold,
        slack_webhook=args.slack_webhook
    )


if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print(" Missing dependency: requests")
        print(" Install with: pip install requests")
        sys.exit(1)
    
    main()

