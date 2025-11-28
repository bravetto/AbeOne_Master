#!/usr/bin/env python3
"""
Docker Network Endpoint Testing Script

This script simulates gateway requests to guard services using Docker network.
It tests the actual endpoints and verifies URL construction, routing, and responses.
"""

import asyncio
import httpx
import json
import sys
from typing import Dict, Any, List, Tuple
from datetime import datetime
import os

# Service configurations from docker-compose.yml
SERVICES = {
    "tokenguard": {
        "url": "http://tokenguard:8000",
        "endpoint": "/scan",
        "health": "/health",
        "test_payload": {"content": "Test content for token scanning", "confidence": 0.7}
    },
    "trustguard": {
        "url": "http://trustguard:8000",
        "endpoint": "/v1/validate",
        "health": "/health",
        "test_payload": {
            "input_text": "This is input text for validation",
            "output_text": "This is output text for validation"
        }
    },
    "contextguard": {
        "url": "http://contextguard:8000",
        "endpoint": "/analyze",
        "health": "/health",
        "test_payload": {
            "current_code": "def new_function():\n    return True",
            "previous_code": "def old_function():\n    return False"
        }
    },
    "biasguard": {
        "url": "http://biasguard:8000",
        "endpoint": "/analyze",
        "health": "/health",
        "test_payload": {
            "samples": [
                {"id": "1", "content": "Test sample for bias detection"}
            ]
        }
    },
    "healthguard": {
        "url": "http://healthguard:8000",
        "endpoint": "/analyze",
        "health": "/health",
        "test_payload": {
            "samples": [
                {"id": "1", "content": "Test sample for health monitoring"}
            ]
        }
    },
    "securityguard": {
        "url": "http://securityguard:8000",
        "endpoint": "/scan",
        "health": "/health",
        "test_payload": {"content": "Test content for security scanning"}
    }
}

# Gateway URL (for testing through gateway)
GATEWAY_URL = os.getenv("GATEWAY_URL", "http://codeguardians-gateway:8000")


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")


def print_result(test_name: str, success: bool, details: str = "", extra: Dict[str, Any] = None):
    """Print test result with formatting."""
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if success else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} {test_name}")
    if details:
        print(f"     {details}")
    if extra:
        for key, value in extra.items():
            print(f"     {Colors.BLUE}{key}:{Colors.RESET} {value}")


async def test_service_health(client: httpx.AsyncClient, service_name: str, config: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """Test service health endpoint."""
    health_url = f"{config['url']}{config['health']}"
    try:
        response = await client.get(health_url, timeout=5.0)
        if response.status_code == 200:
            return True, {"status_code": 200, "response": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text[:200]}
        else:
            return False, {"status_code": response.status_code, "response": response.text[:200]}
    except httpx.TimeoutException:
        return False, {"error": "Timeout after 5 seconds"}
    except httpx.ConnectError as e:
        return False, {"error": f"Connection error: {str(e)}"}
    except Exception as e:
        return False, {"error": f"Unexpected error: {str(e)}"}


async def test_service_endpoint(client: httpx.AsyncClient, service_name: str, config: Dict[str, Any], use_gateway_header: bool = True) -> Tuple[bool, Dict[str, Any]]:
    """Test service endpoint directly (simulating gateway call)."""
    endpoint_url = f"{config['url']}{config['endpoint']}"
    
    # Prepare headers (simulating gateway)
    headers = {
        "Content-Type": "application/json",
        "X-Request-ID": f"test-{datetime.now().isoformat()}",
    }
    
    if use_gateway_header:
        headers["X-Gateway-Request"] = "true"
    
    # For TrustGuard, also try with authentication if needed
    if service_name == "trustguard" and use_gateway_header:
        # TrustGuard should accept X-Gateway-Request header
        pass
    
    try:
        response = await client.post(
            endpoint_url,
            json=config['test_payload'],
            headers=headers,
            timeout=10.0
        )
        
        result = {
            "status_code": response.status_code,
            "url": endpoint_url,
            "endpoint": config['endpoint'],
            "base_url": config['url']
        }
        
        if response.status_code == 200:
            try:
                result["response"] = response.json()
            except:
                result["response_preview"] = response.text[:500]
            return True, result
        elif response.status_code == 404:
            result["error"] = "404 Not Found"
            result["response_preview"] = response.text[:200] if response.text else "No response body"
            return False, result
        elif response.status_code in [401, 403]:
            result["error"] = f"Authentication/Authorization issue: {response.status_code}"
            try:
                result["response"] = response.json()
            except:
                result["response_preview"] = response.text[:200]
            return False, result
        else:
            result["error"] = f"Unexpected status: {response.status_code}"
            result["response_preview"] = response.text[:200] if response.text else "No response body"
            return False, result
            
    except httpx.TimeoutException:
        return False, {"error": "Timeout after 10 seconds", "url": endpoint_url}
    except httpx.ConnectError as e:
        return False, {"error": f"Connection error: {str(e)}", "url": endpoint_url}
    except Exception as e:
        return False, {"error": f"Unexpected error: {str(e)}", "url": endpoint_url}


async def test_gateway_endpoint(client: httpx.AsyncClient, service_name: str, config: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """Test service through gateway."""
    gateway_endpoint = f"{GATEWAY_URL}/api/v1/guards/process"
    
    payload = {
        "service_type": service_name,
        "payload": config['test_payload'],
        "user_id": "test-user",
        "session_id": "test-session"
    }
    
    try:
        response = await client.post(
            gateway_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15.0
        )
        
        result = {
            "status_code": response.status_code,
            "gateway_url": gateway_endpoint,
            "service_type": service_name
        }
        
        if response.status_code == 200:
            try:
                result["response"] = response.json()
                return True, result
            except:
                result["response_preview"] = response.text[:500]
                return True, result
        else:
            result["error"] = f"Gateway returned status {response.status_code}"
            try:
                result["response"] = response.json()
            except:
                result["response_preview"] = response.text[:200]
            return False, result
            
    except httpx.TimeoutException:
        return False, {"error": "Gateway timeout", "gateway_url": gateway_endpoint}
    except httpx.ConnectError as e:
        return False, {"error": f"Gateway connection error: {str(e)}", "gateway_url": gateway_endpoint}
    except Exception as e:
        return False, {"error": f"Unexpected error: {str(e)}", "gateway_url": gateway_endpoint}


async def test_url_construction():
    """Test URL construction logic (simulating gateway behavior)."""
    print_header("URL Construction Testing")
    
    test_cases = [
        ("http://trustguard:8000", "/v1/validate", "http://trustguard:8000/v1/validate"),
        ("http://trustguard:8000/", "/v1/validate", "http://trustguard:8000/v1/validate"),  # Trailing slash
        ("http://contextguard:8000", "/analyze", "http://contextguard:8000/analyze"),
        ("http://contextguard:8000/", "/analyze", "http://contextguard:8000/analyze"),  # Trailing slash
    ]
    
    results = []
    for base_url, endpoint, expected in test_cases:
        # Simulate gateway URL construction
        sanitized_base = base_url.rstrip('/')
        constructed_url = f"{sanitized_base}{endpoint}"
        success = constructed_url == expected
        results.append((success, base_url, endpoint, expected, constructed_url))
        
        status = Colors.GREEN + "✓" if success else Colors.RED + "✗"
        print(f"{status}{Colors.RESET} Base: {base_url}, Endpoint: {endpoint}")
        print(f"     Expected: {expected}")
        print(f"     Got:      {constructed_url}")
        if not success:
            print(f"     {Colors.RED}MISMATCH!{Colors.RESET}")
        print()
    
    return all(r[0] for r in results)


async def run_all_tests():
    """Run all tests."""
    print_header("Docker Network Endpoint Testing")
    print(f"{Colors.BOLD}Testing guard services via Docker network{Colors.RESET}\n")
    
    # Create HTTP client with extended timeout
    timeout = httpx.Timeout(30.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        
        # Test URL construction
        url_test_passed = await test_url_construction()
        
        print_header("Service Health Checks")
        health_results = {}
        
        for service_name, config in SERVICES.items():
            success, details = await test_service_health(client, service_name, config)
            health_results[service_name] = (success, details)
            print_result(
                f"{service_name} health check",
                success,
                f"URL: {config['url']}{config['health']}",
                details if not success else {"status": "healthy"}
            )
        
        print_header("Direct Service Endpoint Testing")
        endpoint_results = {}
        
        for service_name, config in SERVICES.items():
            # First check if service is healthy
            if not health_results.get(service_name, (False, {}))[0]:
                print_result(
                    f"{service_name} endpoint test",
                    False,
                    f"Skipped - service health check failed"
                )
                endpoint_results[service_name] = (False, {"skipped": "health_check_failed"})
                continue
            
            success, details = await test_service_endpoint(client, service_name, config)
            endpoint_results[service_name] = (success, details)
            
            if success:
                print_result(
                    f"{service_name} endpoint test",
                    True,
                    f"URL: {details.get('url', 'N/A')}",
                    {"status_code": details.get('status_code')}
                )
            else:
                error_msg = details.get('error', 'Unknown error')
                print_result(
                    f"{service_name} endpoint test",
                    False,
                    f"URL: {details.get('url', 'N/A')}",
                    {"error": error_msg, "status_code": details.get('status_code')}
                )
                if details.get('response_preview'):
                    print(f"     {Colors.YELLOW}Response:{Colors.RESET} {details['response_preview']}")
        
        print_header("Gateway Endpoint Testing")
        gateway_results = {}
        
        for service_name, config in SERVICES.items():
            # Skip if direct endpoint test failed
            if not endpoint_results.get(service_name, (False, {}))[0]:
                print_result(
                    f"{service_name} via gateway",
                    False,
                    f"Skipped - direct endpoint test failed"
                )
                gateway_results[service_name] = (False, {"skipped": "direct_endpoint_failed"})
                continue
            
            success, details = await test_gateway_endpoint(client, service_name, config)
            gateway_results[service_name] = (success, details)
            
            if success:
                print_result(
                    f"{service_name} via gateway",
                    True,
                    f"Gateway URL: {GATEWAY_URL}/api/v1/guards/process",
                    {"status_code": details.get('status_code')}
                )
            else:
                error_msg = details.get('error', 'Unknown error')
                print_result(
                    f"{service_name} via gateway",
                    False,
                    f"Gateway URL: {GATEWAY_URL}/api/v1/guards/process",
                    {"error": error_msg, "status_code": details.get('status_code')}
                )
        
        # Summary
        print_header("Test Summary")
        
        total_services = len(SERVICES)
        health_passed = sum(1 for r in health_results.values() if r[0])
        endpoint_passed = sum(1 for r in endpoint_results.values() if r[0] and not r[1].get('skipped'))
        gateway_passed = sum(1 for r in gateway_results.values() if r[0] and not r[1].get('skipped'))
        
        print(f"{Colors.BOLD}Total Services:{Colors.RESET} {total_services}")
        print(f"{Colors.BOLD}Health Checks:{Colors.RESET} {health_passed}/{total_services} passed")
        print(f"{Colors.BOLD}Direct Endpoints:{Colors.RESET} {endpoint_passed}/{total_services} passed")
        print(f"{Colors.BOLD}Gateway Endpoints:{Colors.RESET} {gateway_passed}/{total_services} passed")
        print(f"{Colors.BOLD}URL Construction:{Colors.RESET} {'✓ PASS' if url_test_passed else '✗ FAIL'}")
        
        # Detailed failures
        print(f"\n{Colors.BOLD}Failures:{Colors.RESET}")
        for service_name in SERVICES:
            health_ok, _ = health_results.get(service_name, (False, {}))
            endpoint_ok, endpoint_details = endpoint_results.get(service_name, (False, {}))
            gateway_ok, gateway_details = gateway_results.get(service_name, (False, {}))
            
            if not health_ok:
                print(f"  {Colors.RED}✗{Colors.RESET} {service_name}: Health check failed")
            elif not endpoint_ok and not endpoint_details.get('skipped'):
                print(f"  {Colors.RED}✗{Colors.RESET} {service_name}: Direct endpoint failed")
                print(f"    URL: {endpoint_details.get('url', 'N/A')}")
                print(f"    Error: {endpoint_details.get('error', 'Unknown')}")
            elif not gateway_ok and not gateway_details.get('skipped'):
                print(f"  {Colors.RED}✗{Colors.RESET} {service_name}: Gateway endpoint failed")
                print(f"    Error: {gateway_details.get('error', 'Unknown')}")
        
        # Overall status
        all_passed = (
            url_test_passed and
            health_passed == total_services and
            endpoint_passed == total_services and
            gateway_passed == total_services
        )
        
        print(f"\n{Colors.BOLD}Overall Status:{Colors.RESET} ", end="")
        if all_passed:
            print(f"{Colors.GREEN}✓ ALL TESTS PASSED{Colors.RESET}")
            return 0
        else:
            print(f"{Colors.RED}✗ SOME TESTS FAILED{Colors.RESET}")
            return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(run_all_tests())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
