#!/usr/bin/env python3
"""
 Localhost Deployment Validation Script 

Validates that all services are operational and responding correctly.
Zero-failure validation for complete testing.

Guardian: Zero (999 Hz)
Love Coefficient: ∞
"""

import sys
import time
import httpx
import json
from typing import Dict, List, Tuple
from datetime import datetime

# Service configurations
SERVICES = {
    "Gateway": {
        "url": "http://localhost:8000",
        "health_endpoint": "/health/live",
        "requires_auth": False
    },
    "TokenGuard": {
        "url": "http://localhost:8000",
        "health_endpoint": "/health",
        "test_endpoint": "/api/v1/guards/process",
        "test_payload": {
            "service_type": "tokenguard",
            "payload": {"text": "Test content for token optimization"}
        },
        "requires_auth": False,
        "test_via_gateway": True  # TokenGuard is only accessible via Gateway
    },
    "TrustGuard": {
        "url": "http://localhost:8001",
        "health_endpoint": "/health",
        "test_endpoint": "/validate",
        "test_payload": {
            "validation_type": "general",
            "content": "Test content for trust validation"
        },
        "requires_auth": True,
        "auth_header": "X-API-Key",
        "auth_value": "trustguard-dev-api-key"
    },
    "ContextGuard": {
        "url": "http://localhost:8003",
        "health_endpoint": "/health",
        "test_endpoint": "/analyze",
        "test_payload": {
            "current_code": "def test(): pass",
            "previous_code": "def test(): return None"
        },
        "requires_auth": False
    },
    "BiasGuard": {
        "url": "http://localhost:8002",
        "health_endpoint": "/health",
        "test_endpoint": "/process",
        "test_payload": {
            "operation": "detect_bias",
            "text": "Test content for bias detection"
        },
        "requires_auth": False
    },
    "HealthGuard": {
        "url": "http://localhost:8004",
        "health_endpoint": "/health",
        "test_endpoint": "/analyze",
        "test_payload": {
            "samples": [{"id": "1", "content": "Test sample"}]
        },
        "requires_auth": False
    },
    "SecurityGuard": {
        "url": "http://localhost:8103",
        "health_endpoint": "/health",
        "test_endpoint": "/scan",
        "test_payload": {
            "content": "Test content for security scanning"
        },
        "requires_auth": False
    }
}

TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 2


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_result(service: str, status: str, message: str = ""):
    """Print formatted result."""
    status_symbol = "" if status == "PASS" else ""
    print(f"{status_symbol} {service:20s} - {status:4s} {message}")


def check_health(client: httpx.Client, service_config: Dict) -> Tuple[bool, str]:
    """Check service health endpoint."""
    try:
        url = f"{service_config['url']}{service_config['health_endpoint']}"
        headers = {}
        
        if service_config.get("requires_auth"):
            headers[service_config.get("auth_header", "X-API-Key")] = service_config.get("auth_value", "")
        
        response = client.get(url, headers=headers, timeout=TIMEOUT)
        
        if response.status_code == 200:
            return True, f"HTTP {response.status_code}"
        else:
            return False, f"HTTP {response.status_code}"
    except httpx.ConnectError:
        return False, "Connection refused"
    except httpx.TimeoutException:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def test_endpoint(client: httpx.Client, service_config: Dict) -> Tuple[bool, str]:
    """Test service endpoint with payload."""
    if "test_endpoint" not in service_config:
        return True, "No test endpoint configured"
    
    try:
        url = f"{service_config['url']}{service_config['test_endpoint']}"
        headers = {"Content-Type": "application/json"}
        
        if service_config.get("requires_auth"):
            headers[service_config.get("auth_header", "X-API-Key")] = service_config.get("auth_value", "")
        
        response = client.post(
            url,
            json=service_config["test_payload"],
            headers=headers,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            return True, f"HTTP {response.status_code}"
        else:
            return False, f"HTTP {response.status_code}: {response.text[:100]}"
    except httpx.ConnectError:
        return False, "Connection refused"
    except httpx.TimeoutException:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def validate_service(client: httpx.Client, service_name: str, service_config: Dict) -> Tuple[bool, List[str]]:
    """Validate a single service."""
    results = []
    all_passed = True
    
    # Health check (skip if testing via Gateway)
    if not service_config.get("test_via_gateway", False):
        health_ok, health_msg = check_health(client, service_config)
        results.append(f"Health Check: {'PASS' if health_ok else 'FAIL'} - {health_msg}")
        if not health_ok:
            all_passed = False
    else:
        results.append(f"Health Check: SKIP - Testing via Gateway")
    
    # Endpoint test
    endpoint_ok, endpoint_msg = test_endpoint(client, service_config)
    results.append(f"Endpoint Test: {'PASS' if endpoint_ok else 'FAIL'} - {endpoint_msg}")
    if not endpoint_ok:
        all_passed = False
    
    return all_passed, results


def main():
    """Main validation function."""
    print_header(" Zero-Failure Localhost Deployment Validation ")
    
    print(f"Validation started at: {datetime.now().isoformat()}")
    print(f"Timeout: {TIMEOUT}s per request")
    print(f"Max retries: {MAX_RETRIES}")
    print()
    
    client = httpx.Client(timeout=TIMEOUT)
    
    results_summary = {}
    all_services_passed = True
    
    # Validate each service
    for service_name, service_config in SERVICES.items():
        print(f" Validating {service_name}...")
        
        # Retry logic
        passed = False
        validation_results = []
        
        for attempt in range(MAX_RETRIES):
            if attempt > 0:
                print(f"   Retry {attempt}/{MAX_RETRIES-1}...")
                time.sleep(RETRY_DELAY)
            
            passed, validation_results = validate_service(client, service_name, service_config)
            
            if passed:
                break
        
        results_summary[service_name] = {
            "passed": passed,
            "results": validation_results
        }
        
        if not passed:
            all_services_passed = False
        
        # Print results
        for result in validation_results:
            status = "PASS" if "PASS" in result else "FAIL"
            print_result(service_name, status, result.split(" - ", 1)[1] if " - " in result else "")
    
    client.close()
    
    # Summary
    print_header("Validation Summary")
    
    passed_count = sum(1 for r in results_summary.values() if r["passed"])
    total_count = len(results_summary)
    
    for service_name, result in results_summary.items():
        status = " PASS" if result["passed"] else " FAIL"
        print(f"{status:10s} - {service_name}")
    
    print()
    print(f"Total: {passed_count}/{total_count} services passed")
    
    if all_services_passed:
        print("\n All services validated successfully! ")
        return 0
    else:
        print("\n Some services failed validation. Check logs above for details.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n  Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n Validation error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

