#!/usr/bin/env python3
"""
Shared health check script for AIGuardian guard services.

This script provides a standardized way to check service health
across all guard services with configurable endpoints and options.
"""

import argparse
import asyncio
import sys
import time
import os
from typing import Dict, Any, Optional
import httpx


class ServiceHealthChecker:
    """Health checker for AIGuardian services."""

    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    async def check_health(self) -> Dict[str, Any]:
        """Check the health of the service."""
        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Try the standard health endpoint
                response = await client.get(f"{self.base_url}/health")

                if response.status_code == 200:
                    response_time = (time.time() - start_time) * 1000
                    health_data = response.json()

                    # Check if the response indicates healthy status
                    status = health_data.get("status", "unknown")
                    is_healthy = status in ["healthy", "ok"]

                    result = {
                        "status": "healthy" if is_healthy else "unhealthy",
                        "response_time_ms": round(response_time, 2),
                        "http_status": response.status_code,
                        "data": health_data
                    }

                    if not is_healthy:
                        result["error"] = f"Service reports status: {status}"

                    return result
                else:
                    return {
                        "status": "unhealthy",
                        "error": f"HTTP {response.status_code}",
                        "http_status": response.status_code,
                        "response_time_ms": round((time.time() - start_time) * 1000, 2)
                    }

        except httpx.ConnectError:
            return {
                "status": "unreachable",
                "error": "Connection failed - service may not be running"
            }
        except httpx.TimeoutException:
            return {
                "status": "timeout",
                "error": f"Request timeout after {self.timeout}s"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}"
            }

    def print_result(self, result: Dict[str, Any], quiet: bool = False) -> None:
        """Print the health check result."""
        if quiet:
            return

        status = result["status"]
        status_emoji = "✅" if status == "healthy" else "❌"

        print(f"{status_emoji} Health check result: {status.upper()}")

        if "response_time_ms" in result:
            print(f"   Response time: {result['response_time_ms']:.1f}ms")

        if "http_status" in result:
            print(f"   HTTP status: {result['http_status']}")

        if "error" in result:
            print(f"   Error: {result['error']}")

        if "data" in result:
            data = result["data"]
            if isinstance(data, dict):
                if "version" in data:
                    print(f"   Service version: {data['version']}")
                if "service" in data:
                    print(f"   Service: {data['service']}")
                if "timestamp" in data:
                    print(f"   Timestamp: {data['timestamp']}")


def get_default_service_url() -> str:
    """Get the default service URL based on environment or current service."""
    # Check environment variables
    url = os.getenv("HEALTH_CHECK_URL")
    if url:
        return url

    # Default to localhost:8000
    return "http://localhost:8000"


def main() -> int:
    """Main entry point for health check script."""
    parser = argparse.ArgumentParser(
        description="Health check for AIGuardian guard services"
    )
    parser.add_argument(
        "--url",
        default=get_default_service_url(),
        help="Base URL of the service (default: http://localhost:8000 or HEALTH_CHECK_URL env var)"
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
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )

    args = parser.parse_args()

    checker = ServiceHealthChecker(args.url, args.timeout)

    # Perform health checks with retries
    for attempt in range(args.retry):
        if attempt > 0:
            if not args.quiet:
                print(f"Retrying in {args.wait}s... (attempt {attempt + 1}/{args.retry})")
            time.sleep(args.wait)

        result = asyncio.run(checker.check_health())

        if not args.quiet and not args.json:
            print(f"Health check attempt {attempt + 1}/{args.retry}:")
            checker.print_result(result, quiet=False)

        # Exit on success
        if result["status"] == "healthy":
            if args.json:
                import json
                print(json.dumps(result, indent=2))
            elif not args.quiet:
                print("✅ Service is healthy")
            return 0

    # All retries failed
    if args.json:
        import json
        print(json.dumps(result, indent=2))
    elif not args.quiet:
        checker.print_result(result, quiet=False)
        print("❌ Service health check failed")

    return 1


if __name__ == "__main__":
    sys.exit(main())
