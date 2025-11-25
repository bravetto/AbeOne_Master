#!/usr/bin/env python3
"""
Test script to verify multi-container network communication
between the CodeGuardians Gateway and guard services.
"""

import asyncio
import httpx
import time
import json
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiContainerNetworkTester:
    """Test multi-container network connectivity."""

    def __init__(self, gateway_url: str = "http://localhost:8000"):
        self.gateway_url = gateway_url
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def test_gateway_health(self) -> Dict[str, Any]:
        """Test gateway health endpoints."""
        logger.info("Testing gateway health endpoints...")

        results = {}

        # Test gateway liveness
        try:
            response = await self.http_client.get(f"{self.gateway_url}/health/live")
            results["gateway_liveness"] = {
                "status": response.status_code,
                "response": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            results["gateway_liveness"] = {"error": str(e)}

        # Test gateway readiness
        try:
            response = await self.http_client.get(f"{self.gateway_url}/health/ready")
            results["gateway_readiness"] = {
                "status": response.status_code,
                "response": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            results["gateway_readiness"] = {"error": str(e)}

        # Test gateway comprehensive health
        try:
            response = await self.http_client.get(f"{self.gateway_url}/health/comprehensive")
            results["gateway_comprehensive"] = {
                "status": response.status_code,
                "response": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            results["gateway_comprehensive"] = {"error": str(e)}

        return results

    async def test_guard_services_health(self) -> Dict[str, Any]:
        """Test guard services health through gateway."""
        logger.info("Testing guard services health through gateway...")

        results = {}

        # Test all guard services health
        try:
            response = await self.http_client.get(f"{self.gateway_url}/api/v1/guards/health")
            results["all_guards_health"] = {
                "status": response.status_code,
                "response": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            results["all_guards_health"] = {"error": str(e)}

        # Test individual guard services
        guards = ["tokenguard", "trustguard", "contextguard", "biasguard", "healthguard"]

        for guard in guards:
            try:
                response = await self.http_client.get(f"{self.gateway_url}/api/v1/guards/health/{guard}")
                results[f"{guard}_health"] = {
                    "status": response.status_code,
                    "response": response.json() if response.status_code == 200 else None
                }
            except Exception as e:
                results[f"{guard}_health"] = {"error": str(e)}

        return results

    async def test_unified_processing(self) -> Dict[str, Any]:
        """Test unified guard processing endpoint."""
        logger.info("Testing unified guard processing...")

        results = {}

        test_payloads = {
            "tokenguard": {
                "service_type": "tokenguard",
                "payload": {
                    "content": "This is a test for token optimization",
                    "content_type": "text",
                    "scan_level": "standard"
                },
                "user_id": "test-user",
                "client_type": "api"
            },
            "trustguard": {
                "service_type": "trustguard",
                "payload": {
                    "validation_type": "general",
                    "content": "This is accurate information for testing",
                    "validation_level": "standard"
                },
                "user_id": "test-user",
                "client_type": "api"
            },
            "contextguard": {
                "service_type": "contextguard",
                "payload": {
                    "operation": "set",
                    "data": {
                        "context": "Test conversation context",
                        "conversation_history": ["Previous message"]
                    },
                    "consciousness_context": "maintain_context"
                },
                "user_id": "test-user",
                "client_type": "api"
            },
            "biasguard": {
                "service_type": "biasguard",
                "payload": {
                    "operation": "detect_bias",
                    "data": {
                        "text": "This is a test for bias detection"
                    }
                },
                "user_id": "test-user",
                "client_type": "api"
            },
            "healthguard": {
                "service_type": "healthguard",
                "payload": {
                    "content": "Test system health check",
                    "content_type": "system_log",
                    "scan_level": "standard"
                },
                "user_id": "test-user",
                "client_type": "api"
            }
        }

        for guard_name, payload in test_payloads.items():
            try:
                response = await self.http_client.post(
                    f"{self.gateway_url}/api/v1/guards/process",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                results[f"{guard_name}_processing"] = {
                    "status": response.status_code,
                    "response": response.json() if response.status_code in [200, 400, 500] else None
                }
            except Exception as e:
                results[f"{guard_name}_processing"] = {"error": str(e)}

        return results

    async def test_service_discovery(self) -> Dict[str, Any]:
        """Test service discovery endpoints."""
        logger.info("Testing service discovery...")

        results = {}

        # Test service listing
        try:
            response = await self.http_client.get(f"{self.gateway_url}/api/v1/guards/services")
            results["service_listing"] = {
                "status": response.status_code,
                "response": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            results["service_listing"] = {"error": str(e)}

        # Test discovered services
        try:
            response = await self.http_client.get(f"{self.gateway_url}/api/v1/guards/discovery/services")
            results["discovered_services"] = {
                "status": response.status_code,
                "response": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            results["discovered_services"] = {"error": str(e)}

        return results

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all network connectivity tests."""
        logger.info("Starting multi-container network tests...")

        results = {}

        # Wait a bit for services to be ready
        logger.info("Waiting 30 seconds for services to initialize...")
        await asyncio.sleep(30)

        # Run all test suites
        results["gateway_health"] = await self.test_gateway_health()
        results["guard_services_health"] = await self.test_guard_services_health()
        results["unified_processing"] = await self.test_unified_processing()
        results["service_discovery"] = await self.test_service_discovery()

        await self.http_client.aclose()

        return results

    def print_results(self, results: Dict[str, Any]):
        """Print test results in a readable format."""
        print("\n" + "="*80)
        print("MULTI-CONTAINER NETWORK TEST RESULTS")
        print("="*80)

        for test_suite, suite_results in results.items():
            print(f"\n[*] {test_suite.upper().replace('_', ' ')}")
            print("-" * 50)

            for test_name, test_result in suite_results.items():
                if "error" in test_result:
                    print(f"[ERROR] {test_name}: {test_result['error']}")
                elif test_result.get("status") == 200:
                    print(f"[OK] {test_name}: SUCCESS")
                else:
                    print(f"[WARN] {test_name}: STATUS {test_result.get('status', 'UNKNOWN')}")

        # Summary
        total_tests = 0
        successful_tests = 0

        for suite_results in results.values():
            for test_result in suite_results.values():
                total_tests += 1
                if "error" not in test_result and test_result.get("status") == 200:
                    successful_tests += 1

        print("\n" + "="*80)
        print(f"SUMMARY: {successful_tests}/{total_tests} tests passed")
        print("="*80)

        if successful_tests == total_tests:
            print("[SUCCESS] All tests passed! Multi-container network is working correctly.")
        elif successful_tests > total_tests * 0.8:
            print("[WARNING] Most tests passed. Some services may need attention.")
        else:
            print("[FAILURE] Many tests failed. Check service configurations and network connectivity.")


async def main():
    """Main test function."""
    tester = MultiContainerNetworkTester()

    try:
        results = await tester.run_all_tests()
        tester.print_results(results)
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        print(f"\n[ERROR] Test execution failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
