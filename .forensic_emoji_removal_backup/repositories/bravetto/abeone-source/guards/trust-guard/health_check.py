#!/usr/bin/env python3
"""
Health check script for TrustGuard microservice.

This script can be used for:
- Docker health checks
- Kubernetes readiness/liveness probes
- Monitoring system checks
- CI/CD validation
"""

import argparse
import sys
import time
import requests
from typing import Dict, Any


def check_health(base_url: str, timeout: int = 5) -> Dict[str, Any]:
    """
    Check the health of the TrustGuard service.
    
    Args:
        base_url: Base URL of the service (e.g., http://localhost:8000)
        timeout: Request timeout in seconds
        
    Returns:
        Dict containing health check results
    """
    try:
        url = f"{base_url.rstrip('/')}/health"
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            health_data = response.json()
            return {
                "status": "healthy",
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "data": health_data
            }
        else:
            return {
                "status": "unhealthy",
                "error": f"HTTP {response.status_code}",
                "response_time_ms": response.elapsed.total_seconds() * 1000
            }
            
    except requests.exceptions.ConnectionError:
        return {
            "status": "unreachable",
            "error": "Connection failed"
        }
    except requests.exceptions.Timeout:
        return {
            "status": "timeout",
            "error": f"Request timeout after {timeout}s"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main() -> Any:
    """Main entry point for health check script."""
    parser = argparse.ArgumentParser(description="Health check for TrustGuard microservice")
    parser.add_argument(
        "--url", 
        default="http://localhost:8000",
        help="Base URL of the service (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--timeout", 
        type=int, 
        default=5,
        help="Request timeout in seconds (default: 5)"
    )
    parser.add_argument(
        "--retry", 
        type=int, 
        default=1,
        help="Number of retry attempts (default: 1)"
    )
    parser.add_argument(
        "--wait", 
        type=int, 
        default=1,
        help="Wait time between retries in seconds (default: 1)"
    )
    parser.add_argument(
        "--quiet", 
        action="store_true",
        help="Suppress output (exit code only)"
    )
    
    args = parser.parse_args()
    
    # Perform health checks with retries
    for attempt in range(args.retry):
        if attempt > 0:
            if not args.quiet:
                print(f"Retrying in {args.wait}s... (attempt {attempt + 1}/{args.retry})")
            time.sleep(args.wait)
        
        result = check_health(args.url, args.timeout)
        
        if not args.quiet:
            print(f"Health check attempt {attempt + 1}:")
            print(f"  Status: {result['status']}")
            if 'response_time_ms' in result:
                print(f"  Response time: {result['response_time_ms']:.1f}ms")
            if 'error' in result:
                print(f"  Error: {result['error']}")
            if 'data' in result:
                data = result['data']
                print(f"  Service version: {data.get('version', 'unknown')}")
                if 'system' in data:
                    system = data['system']
                    if isinstance(system, dict):
                        print(f"  Memory usage: {system.get('memory_mb', 'unknown')}MB")
                        print(f"  CPU usage: {system.get('cpu_percent', 'unknown')}%")
        
        # Exit on success
        if result['status'] == "healthy":
            if not args.quiet:
                print("✅ Service is healthy")
            sys.exit(0)
    
    # All retries failed
    if not args.quiet:
        print("❌ Service health check failed")
    sys.exit(1)


if __name__ == "__main__":
    main()