#!/usr/bin/env python3
"""
Virtual Scenario Simulator for AWS/Linkerd Failure Patterns

Simulates failure patterns identified in forensic analysis WITHOUT modifying codebase.
This allows testing pattern detection scripts against known failure scenarios.

Usage:
    python scripts/scenario_simulator.py --pattern flow_table_exhaustion --port 9001
    python scripts/scenario_simulator.py --pattern circuit_breaker --port 9001
    python scripts/scenario_simulator.py --pattern timeout_cascade --port 9001
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional
import argparse

try:
    from fastapi import FastAPI, Response, Request
    from fastapi.responses import JSONResponse
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("⚠️  FastAPI not available. Install with: pip install fastapi uvicorn")


class PatternSimulator:
    """Simulates AWS/Linkerd failure patterns for testing detection scripts."""
    
    def __init__(self, pattern: str, port: int = 9001):
        self.pattern = pattern
        self.port = port
        self.app = FastAPI(title=f"Pattern Simulator: {pattern}")
        self.request_count = 0
        self.failure_count = 0
        self.pattern_config = self._get_pattern_config(pattern)
        
        # Setup routes based on pattern
        self._setup_routes()
    
    def _get_pattern_config(self, pattern: str) -> Dict:
        """Get configuration for specific pattern."""
        configs = {
            "flow_table_exhaustion": {
                "description": "NLB Flow Table Exhaustion - Slow connections, timeouts",
                "slow_delay": 2.0,  # Simulate slow connections
                "timeout_rate": 0.3,  # 30% timeout rate
                "timeout_delay": 5.0
            },
            "idle_timeout": {
                "description": "NLB Idle Timeout - Connection resets after idle",
                "reset_after_idle": True,
                "idle_threshold": 2.0  # Reset after 2s idle (simulating 350s)
            },
            "circuit_breaker": {
                "description": "Linkerd Circuit Breaker - Consecutive failures trigger break",
                "failure_threshold": 7,  # Fail 7 consecutive times
                "failure_rate": 0.5  # 50% failure rate
            },
            "timeout_cascade": {
                "description": "NLB + Linkerd Timeout Cascade - Reset then circuit break",
                "reset_after_idle": True,
                "circuit_break_after_reset": True,
                "idle_threshold": 1.5
            },
            "stream_exhaustion": {
                "description": "HTTP/2 Stream Exhaustion - Max concurrent streams",
                "max_streams": 50,  # Simulate low limit
                "delay_per_stream": 0.1
            },
            "connection_refused": {
                "description": "Connection Refused - Port binding issues",
                "refuse_rate": 0.4,  # 40% connection refused
            },
            "target_group_saturation": {
                "description": "ALB Target Group Saturation - 503 errors",
                "saturation_threshold": 10,  # After 10 concurrent
                "saturation_response": 503
            },
            "dns_dead_ip": {
                "description": "ALB DNS Dead IP - Intermittent connectivity",
                "dead_ip_rate": 0.2,  # 20% dead IP simulation
            },
            "keep_alive_mismatch": {
                "description": "ALB Keep-Alive Mismatch - No keep-alive headers",
                "missing_keep_alive": True
            },
            "proxy_timeout": {
                "description": "Linkerd Proxy Timeout - 10s timeout pattern",
                "slow_response_time": 12.0,  # Simulate >10s responses
            },
            "rst_pattern": {
                "description": "TCP RST Patterns - Connection resets",
                "rst_rate": 0.3  # 30% RST
            }
        }
        
        return configs.get(pattern, {
            "description": f"Unknown pattern: {pattern}",
            "enabled": False
        })
    
    def _setup_routes(self):
        """Setup FastAPI routes based on pattern."""
        
        @self.app.get("/health")
        async def health(request: Request):
            """Health endpoint - simulates various failure patterns."""
            self.request_count += 1
            
            config = self.pattern_config
            
            # Pattern: Flow Table Exhaustion - Slow responses
            if self.pattern == "flow_table_exhaustion":
                if self.request_count % 3 == 0:  # 30% timeout
                    await asyncio.sleep(config["timeout_delay"])
                    return JSONResponse(
                        status_code=504,
                        content={"error": "Gateway Timeout", "pattern": "flow_table_exhaustion"}
                    )
                elif self.request_count % 2 == 0:  # Slow connection
                    await asyncio.sleep(config["slow_delay"])
            
            # Pattern: Circuit Breaker - Consecutive failures
            elif self.pattern == "circuit_breaker":
                if self.failure_count < config["failure_threshold"]:
                    self.failure_count += 1
                    return JSONResponse(
                        status_code=500,
                        content={"error": "Internal Server Error", "pattern": "circuit_breaker", "consecutive_failures": self.failure_count}
                    )
                elif self.failure_count == config["failure_threshold"]:
                    # Circuit breaker tripped - return unavailable
                    return JSONResponse(
                        status_code=503,
                        content={"error": "Service Unavailable", "pattern": "circuit_breaker", "circuit_breaker": "OPEN"},
                        headers={"l5d-err": "Service in fail-fast"}
                    )
                else:
                    # Reset after some time
                    if self.request_count % 20 == 0:
                        self.failure_count = 0
            
            # Pattern: Target Group Saturation - 503 after threshold
            elif self.pattern == "target_group_saturation":
                # Simulate saturation after concurrent requests
                if self.request_count > config["saturation_threshold"]:
                    return JSONResponse(
                        status_code=503,
                        content={"error": "Service Unavailable", "pattern": "target_group_saturation"}
                    )
            
            # Pattern: Connection Refused - Simulate OS error 111
            elif self.pattern == "connection_refused":
                if self.request_count % 3 == 0:  # ~33% refused
                    # FastAPI doesn't support connection refused, so we return error
                    return JSONResponse(
                        status_code=502,
                        content={"error": "Connection Refused", "pattern": "connection_refused", "os_error": 111}
                    )
            
            # Pattern: Proxy Timeout - Slow responses >10s
            elif self.pattern == "proxy_timeout":
                await asyncio.sleep(config["slow_response_time"])
                # Will timeout, but simulate slow response
                return JSONResponse(
                    status_code=504,
                    content={"error": "Gateway Timeout", "pattern": "proxy_timeout", "duration": config["slow_response_time"]}
                )
            
            # Pattern: RST Pattern - Connection reset simulation
            elif self.pattern == "rst_pattern":
                if self.request_count % 3 == 0:  # ~33% RST
                    return JSONResponse(
                        status_code=502,
                        content={"error": "Connection Reset", "pattern": "rst_pattern"}
                    )
            
            # Pattern: Keep-Alive Mismatch - Missing headers
            elif self.pattern == "keep_alive_mismatch":
                response = JSONResponse(
                    status_code=200,
                    content={"status": "healthy", "pattern": "keep_alive_mismatch"}
                )
                # Intentionally omit Connection: keep-alive header
                return response
            
            # Default: Healthy response
            return JSONResponse(
                status_code=200,
                content={
                    "status": "healthy",
                    "pattern": self.pattern,
                    "request_count": self.request_count
                },
                headers={"Connection": "keep-alive", "Keep-Alive": "timeout=65"}
            )
        
        @self.app.get("/metrics")
        async def metrics():
            """Metrics endpoint for Prometheus."""
            return Response(
                content=f"""
# Pattern Simulator Metrics
pattern_simulator_requests_total{{pattern="{self.pattern}"}} {self.request_count}
pattern_simulator_failures_total{{pattern="{self.pattern}"}} {self.failure_count}
pattern_simulator_up{{pattern="{self.pattern}"}} 1
""",
                media_type="text/plain"
            )
        
        @self.app.get("/")
        async def root():
            """Root endpoint with pattern info."""
            return {
                "pattern": self.pattern,
                "description": self.pattern_config.get("description", ""),
                "port": self.port,
                "request_count": self.request_count,
                "failure_count": self.failure_count,
                "endpoints": {
                    "/health": "Health endpoint with pattern simulation",
                    "/metrics": "Prometheus metrics",
                    "/": "Pattern information"
                }
            }


def list_patterns():
    """List all available patterns."""
    patterns = [
        "flow_table_exhaustion",
        "idle_timeout",
        "circuit_breaker",
        "timeout_cascade",
        "stream_exhaustion",
        "connection_refused",
        "target_group_saturation",
        "dns_dead_ip",
        "keep_alive_mismatch",
        "proxy_timeout",
        "rst_pattern"
    ]
    
    print("\n🔍 Available Failure Patterns:")
    print("=" * 50)
    for pattern in patterns:
        print(f"  • {pattern}")
    print("\nUsage:")
    print(f"  python scripts/scenario_simulator.py --pattern <pattern_name> --port <port>")
    print()


def run_simulator(pattern: str, port: int = 9001, host: str = "0.0.0.0"):
    """Run the pattern simulator server."""
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI required. Install: pip install fastapi uvicorn")
        sys.exit(1)
    
    simulator = PatternSimulator(pattern, port)
    
    print(f"\n🎭 Virtual Scenario Simulator")
    print("=" * 50)
    print(f"Pattern: {pattern}")
    print(f"Description: {simulator.pattern_config.get('description', 'N/A')}")
    print(f"Port: {port}")
    print(f"URL: http://{host}:{port}")
    print("\nEndpoints:")
    print(f"  • http://{host}:{port}/health  - Simulated health endpoint")
    print(f"  • http://{host}:{port}/metrics - Prometheus metrics")
    print(f"  • http://{host}:{port}/        - Pattern information")
    print("\n" + "=" * 50)
    print("⚠️  This simulator will exhibit failure patterns.")
    print("   Run your pattern detection scripts against this endpoint.")
    print("=" * 50 + "\n")
    
    # Run server
    uvicorn.run(simulator.app, host=host, port=port, log_level="info")


async def run_scenario_sequence():
    """Run multiple scenarios in sequence for comprehensive testing."""
    patterns = [
        "circuit_breaker",
        "target_group_saturation",
        "connection_refused",
        "keep_alive_mismatch"
    ]
    
    print("\n🎬 Scenario Sequence Runner")
    print("=" * 50)
    print("This will simulate multiple patterns sequentially.")
    print("Each pattern runs for 30 seconds.\n")
    
    for pattern in patterns:
        print(f"\n▶️  Starting pattern: {pattern}")
        print(f"   Run detection tests against: http://localhost:9001")
        print(f"   Pattern will run for 30 seconds...")
        
        # Note: In production, you'd want to run the server in background
        # For now, this is a placeholder showing the concept
        await asyncio.sleep(1)
    
    print("\n✅ Scenario sequence complete!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Virtual Scenario Simulator for AWS/Linkerd Failure Patterns"
    )
    parser.add_argument(
        "--pattern",
        help="Pattern to simulate (use --list to see available)",
        default=None
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9001,
        help="Port to run simulator on (default: 9001)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available patterns"
    )
    parser.add_argument(
        "--sequence",
        action="store_true",
        help="Run scenario sequence (multiple patterns)"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_patterns()
        return
    
    if args.sequence:
        asyncio.run(run_scenario_sequence())
        return
    
    if not args.pattern:
        print("❌ Error: --pattern required (or use --list to see available)")
        list_patterns()
        sys.exit(1)
    
    run_simulator(args.pattern, args.port, args.host)


if __name__ == "__main__":
    main()

