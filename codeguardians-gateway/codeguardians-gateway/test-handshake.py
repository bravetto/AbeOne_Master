#!/usr/bin/env python3
"""
Client-Server Handshake Testing Script for Tailscale
Perfect for internal testing and client-server communication validation
"""

import asyncio
import aiohttp
import json
import time
import logging
from typing import Dict, List, Optional
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TailscaleHandshakeTester:
    """Test client-server handshakes over Tailscale network"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.results: List[Dict] = []
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_health_check(self) -> Dict:
        """Test basic health check endpoint"""
        logger.info("Testing health check endpoint...")
        start_time = time.time()
        
        try:
            async with self.session.get(f"{self.base_url}/health/live") as response:
                duration = time.time() - start_time
                result = {
                    "test": "health_check",
                    "status": "PASS" if response.status == 200 else "FAIL",
                    "status_code": response.status,
                    "duration_ms": round(duration * 1000, 2),
                    "response_size": len(await response.text())
                }
                logger.info(f"Health check: {result['status']} ({result['duration_ms']}ms)")
                return result
        except Exception as e:
            duration = time.time() - start_time
            result = {
                "test": "health_check",
                "status": "FAIL",
                "error": str(e),
                "duration_ms": round(duration * 1000, 2)
            }
            logger.error(f"Health check failed: {e}")
            return result
    
    async def test_ready_check(self) -> Dict:
        """Test readiness endpoint"""
        logger.info("Testing readiness endpoint...")
        start_time = time.time()
        
        try:
            async with self.session.get(f"{self.base_url}/health/ready") as response:
                duration = time.time() - start_time
                result = {
                    "test": "ready_check",
                    "status": "PASS" if response.status == 200 else "FAIL",
                    "status_code": response.status,
                    "duration_ms": round(duration * 1000, 2),
                    "response_size": len(await response.text())
                }
                logger.info(f"Readiness check: {result['status']} ({result['duration_ms']}ms)")
                return result
        except Exception as e:
            duration = time.time() - start_time
            result = {
                "test": "ready_check",
                "status": "FAIL",
                "error": str(e),
                "duration_ms": round(duration * 1000, 2)
            }
            logger.error(f"Readiness check failed: {e}")
            return result
    
    async def test_api_endpoints(self) -> List[Dict]:
        """Test various API endpoints"""
        endpoints = [
            "/api/v1/health",
            "/api/v1/status",
            "/docs",
            "/openapi.json"
        ]
        
        results = []
        for endpoint in endpoints:
            logger.info(f"Testing endpoint: {endpoint}")
            start_time = time.time()
            
            try:
                async with self.session.get(f"{self.base_url}{endpoint}") as response:
                    duration = time.time() - start_time
                    result = {
                        "test": f"endpoint_{endpoint.replace('/', '_').replace('.', '_')}",
                        "endpoint": endpoint,
                        "status": "PASS" if response.status in [200, 404] else "FAIL",
                        "status_code": response.status,
                        "duration_ms": round(duration * 1000, 2),
                        "response_size": len(await response.text())
                    }
                    logger.info(f"Endpoint {endpoint}: {result['status']} ({result['duration_ms']}ms)")
                    results.append(result)
            except Exception as e:
                duration = time.time() - start_time
                result = {
                    "test": f"endpoint_{endpoint.replace('/', '_').replace('.', '_')}",
                    "endpoint": endpoint,
                    "status": "FAIL",
                    "error": str(e),
                    "duration_ms": round(duration * 1000, 2)
                }
                logger.error(f"Endpoint {endpoint} failed: {e}")
                results.append(result)
        
        return results
    
    async def test_connection_pooling(self, num_requests: int = 10) -> Dict:
        """Test connection pooling and concurrent requests"""
        logger.info(f"Testing connection pooling with {num_requests} concurrent requests...")
        start_time = time.time()
        
        async def single_request():
            try:
                async with self.session.get(f"{self.base_url}/health/live") as response:
                    return {
                        "status_code": response.status,
                        "success": response.status == 200
                    }
            except Exception as e:
                return {"error": str(e), "success": False}
        
        # Run concurrent requests
        tasks = [single_request() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
        
        duration = time.time() - start_time
        successful = sum(1 for r in results if r.get("success", False))
        
        result = {
            "test": "connection_pooling",
            "total_requests": num_requests,
            "successful_requests": successful,
            "failed_requests": num_requests - successful,
            "success_rate": round((successful / num_requests) * 100, 2),
            "total_duration_ms": round(duration * 1000, 2),
            "avg_duration_ms": round((duration * 1000) / num_requests, 2),
            "requests_per_second": round(num_requests / duration, 2)
        }
        
        logger.info(f"Connection pooling: {result['success_rate']}% success rate")
        return result
    
    async def test_latency(self, num_requests: int = 5) -> Dict:
        """Test latency across multiple requests"""
        logger.info(f"Testing latency with {num_requests} requests...")
        latencies = []
        
        for i in range(num_requests):
            start_time = time.time()
            try:
                async with self.session.get(f"{self.base_url}/health/live") as response:
                    duration = time.time() - start_time
                    latencies.append(duration * 1000)  # Convert to milliseconds
            except Exception as e:
                logger.error(f"Latency test request {i+1} failed: {e}")
                latencies.append(float('inf'))
        
        # Calculate statistics
        valid_latencies = [l for l in latencies if l != float('inf')]
        if not valid_latencies:
            return {
                "test": "latency",
                "status": "FAIL",
                "error": "All requests failed"
            }
        
        result = {
            "test": "latency",
            "status": "PASS",
            "num_requests": num_requests,
            "min_latency_ms": round(min(valid_latencies), 2),
            "max_latency_ms": round(max(valid_latencies), 2),
            "avg_latency_ms": round(sum(valid_latencies) / len(valid_latencies), 2),
            "latencies": [round(l, 2) for l in valid_latencies]
        }
        
        logger.info(f"Latency test: avg {result['avg_latency_ms']}ms")
        return result
    
    async def run_all_tests(self) -> Dict:
        """Run all handshake tests"""
        logger.info("Starting Tailscale handshake tests...")
        start_time = time.time()
        
        # Run individual tests
        health_result = await self.test_health_check()
        ready_result = await self.test_ready_check()
        endpoint_results = await self.test_api_endpoints()
        pooling_result = await self.test_connection_pooling()
        latency_result = await self.test_latency()
        
        # Compile results
        all_results = [health_result, ready_result, pooling_result, latency_result] + endpoint_results
        
        # Calculate summary
        total_tests = len(all_results)
        passed_tests = sum(1 for r in all_results if r.get("status") == "PASS")
        failed_tests = total_tests - passed_tests
        
        total_duration = time.time() - start_time
        
        summary = {
            "test_suite": "tailscale_handshake",
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": round((passed_tests / total_tests) * 100, 2),
            "total_duration_ms": round(total_duration * 1000, 2),
            "results": all_results
        }
        
        logger.info(f"Handshake tests completed: {summary['success_rate']}% success rate")
        return summary

async def main():
    """Main test runner"""
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    logger.info(f"Starting Tailscale handshake tests against {base_url}")
    
    async with TailscaleHandshakeTester(base_url) as tester:
        results = await tester.run_all_tests()
        
        # Print summary
        print("\n" + "="*60)
        print("TAILSCALE HANDSHAKE TEST RESULTS")
        print("="*60)
        print(f"Total Tests: {results['total_tests']}")
        print(f"Passed: {results['passed_tests']}")
        print(f"Failed: {results['failed_tests']}")
        print(f"Success Rate: {results['success_rate']}%")
        print(f"Total Duration: {results['total_duration_ms']}ms")
        print("="*60)
        
        # Print individual results
        for result in results['results']:
            status = result.get('status', 'UNKNOWN')
            test_name = result.get('test', 'unknown')
            duration = result.get('duration_ms', 0)
            print(f"{status:4} | {test_name:20} | {duration:8.2f}ms")
        
        print("="*60)
        
        # Exit with appropriate code
        sys.exit(0 if results['failed_tests'] == 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())
