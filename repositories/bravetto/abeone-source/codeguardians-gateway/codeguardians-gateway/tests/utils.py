"""
Shared test utilities for CodeGuardians Gateway testing suite.

This module provides common utilities for testing guard services,
validating responses, and generating test data.
"""

import asyncio
import time
from typing import Dict, Any, Optional, List
import httpx
import logging

logger = logging.getLogger(__name__)


async def wait_for_service(url: str, timeout: int = 30) -> bool:
    """
    Wait for a service to become available.
    
    Args:
        url: Service URL to check
        timeout: Maximum time to wait in seconds
        
    Returns:
        True if service becomes available, False otherwise
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{url}/health", timeout=5.0)
                if response.status_code == 200:
                    logger.info(f"Service at {url} is available")
                    return True
        except Exception as e:
            logger.debug(f"Service at {url} not yet available: {e}")
        
        await asyncio.sleep(1)
    
    logger.warning(f"Service at {url} did not become available within {timeout}s")
    return False


async def assert_guard_response_valid(response: dict, service_type: str) -> None:
    """
    Validate guard response structure.
    
    Args:
        response: Response dictionary to validate
        service_type: Expected service type
        
    Raises:
        AssertionError: If response structure is invalid
    """
    # Required fields for all guard responses
    required_fields = [
        'request_id', 'service_type', 'success', 'processing_time', 
        'service_used', 'fallback_used'
    ]
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    # Validate service type
    assert response['service_type'] == service_type, \
        f"Expected service_type '{service_type}', got '{response['service_type']}'"
    
    # Validate success field
    assert isinstance(response['success'], bool), \
        "Field 'success' must be boolean"
    
    # Validate processing time
    assert isinstance(response['processing_time'], (int, float)), \
        "Field 'processing_time' must be numeric"
    assert response['processing_time'] >= 0, \
        "Field 'processing_time' must be non-negative"
    
    # Validate service_used
    assert isinstance(response['service_used'], str), \
        "Field 'service_used' must be string"
    
    # Validate fallback_used
    assert isinstance(response['fallback_used'], bool), \
        "Field 'fallback_used' must be boolean"
    
    # Validate data or error presence
    if response['success']:
        assert 'data' in response, "Successful response must contain 'data' field"
        assert response['data'] is not None, "Data field cannot be null"
    else:
        assert 'error' in response, "Failed response must contain 'error' field"
        assert response['error'] is not None, "Error field cannot be null"


def generate_test_payload(service_type: str, scenario: str) -> Dict[str, Any]:
    """
    Generate test payloads for different scenarios.
    
    Args:
        service_type: Type of guard service
        scenario: Test scenario (e.g., 'normal', 'malicious', 'edge_case')
        
    Returns:
        Dictionary containing test payload
    """
    base_payloads = {
        'securityguard': {
            'normal': {
                'content': 'This is normal content for security scanning',
                'content_type': 'text',
                'scan_level': 'standard'
            },
            'malicious': {
                'content': 'This is malicious content with potential threats and vulnerabilities',
                'content_type': 'text',
                'scan_level': 'deep'
            },
            'edge_case': {
                'content': '',
                'content_type': 'text',
                'scan_level': 'standard'
            }
        },
        'contextguard': {
            'normal': {
                'operation': 'set',
                'data': {
                    'key': 'test_key',
                    'value': 'test_value'
                },
                'consciousness_context': {
                    'context': 'test context'
                }
            },
            'malicious': {
                'operation': 'set',
                'data': {
                    'key': 'malicious_key',
                    'value': 'malicious_value'
                },
                'consciousness_context': {
                    'context': 'malicious context'
                }
            },
            'edge_case': {
                'operation': 'set',
                'data': {},
                'consciousness_context': {}
            }
        },
        'trustguard': {
            'normal': {
                'validation_type': 'general',
                'content': 'This is content for trust validation',
                'validation_level': 'standard'
            },
            'malicious': {
                'validation_type': 'general',
                'content': 'This is untrustworthy content',
                'validation_level': 'strict'
            },
            'edge_case': {
                'validation_type': 'general',
                'content': '',
                'validation_level': 'standard'
            }
        },
        'biasguard': {
            'normal': {
                'operation': 'detect_bias',
                'data': {
                    'text': 'This is neutral content for bias detection'
                },
                'context': {
                    'context': 'neutral context'
                }
            },
            'malicious': {
                'operation': 'detect_bias',
                'data': {
                    'text': 'This is biased content with unfair language'
                },
                'context': {
                    'context': 'biased context'
                }
            },
            'edge_case': {
                'operation': 'detect_bias',
                'data': {},
                'context': {}
            }
        }
    }
    
    if service_type not in base_payloads:
        raise ValueError(f"Unknown service type: {service_type}")
    
    if scenario not in base_payloads[service_type]:
        raise ValueError(f"Unknown scenario '{scenario}' for service '{service_type}'")
    
    return base_payloads[service_type][scenario].copy()


def generate_large_payload(size_kb: int = 100) -> Dict[str, Any]:
    """
    Generate a large payload for stress testing.
    
    Args:
        size_kb: Size of payload in KB
        
    Returns:
        Dictionary containing large payload
    """
    large_content = "x" * (size_kb * 1024)
    
    return {
        'content': large_content,
        'content_type': 'text',
        'scan_level': 'standard'
    }


def generate_malformed_payload() -> Dict[str, Any]:
    """
    Generate a malformed payload for error testing.
    
    Returns:
        Dictionary containing malformed payload
    """
    return {
        'content': None,
        'content_type': 123,  # Should be string
        'scan_level': None
    }


async def make_guard_request(
    client: httpx.AsyncClient,
    base_url: str,
    service_type: str,
    payload: Dict[str, Any],
    user_id: Optional[str] = None,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Make a request to the guard service through the orchestrator.
    
    Args:
        client: HTTP client
        base_url: Base URL of the gateway
        service_type: Type of guard service
        payload: Request payload
        user_id: Optional user ID
        session_id: Optional session ID
        
    Returns:
        Response dictionary
    """
    request_data = {
        'service_type': service_type,
        'payload': payload
    }
    
    if user_id:
        request_data['user_id'] = user_id
    if session_id:
        request_data['session_id'] = session_id
    
    response = await client.post(
        f"{base_url}/api/v1/guards/process",
        json=request_data,
        timeout=30.0
    )
    
    response.raise_for_status()
    return response.json()


async def check_service_health(
    client: httpx.AsyncClient,
    service_url: str,
    timeout: float = 10.0
) -> Dict[str, Any]:
    """
    Check the health of a guard service.
    
    Args:
        client: HTTP client
        service_url: URL of the service
        timeout: Request timeout
        
    Returns:
        Health check response
    """
    response = await client.get(
        f"{service_url}/health",
        timeout=timeout
    )
    
    response.raise_for_status()
    return response.json()


def validate_security_metrics(response_data: Dict[str, Any]) -> None:
    """
    Validate security guard metrics.
    
    Args:
        response_data: Response data from security guard
        
    Raises:
        AssertionError: If metrics are invalid
    """
    if 'threats_detected' in response_data:
        assert isinstance(response_data['threats_detected'], list), \
            "threats_detected must be a list"
    
    if 'security_score' in response_data:
        score = response_data['security_score']
        assert isinstance(score, (int, float)), \
            "security_score must be numeric"
        assert 0 <= score <= 1, \
            "security_score must be between 0 and 1"
    
    if 'recommendations' in response_data:
        assert isinstance(response_data['recommendations'], list), \
            "recommendations must be a list"


def validate_trust_metrics(response_data: Dict[str, Any]) -> None:
    """
    Validate trust guard metrics.
    
    Args:
        response_data: Response data from trust guard
        
    Raises:
        AssertionError: If metrics are invalid
    """
    if 'validation_results' in response_data:
        assert isinstance(response_data['validation_results'], list), \
            "validation_results must be a list"
    
    if 'overall_score' in response_data:
        score = response_data['overall_score']
        assert isinstance(score, (int, float)), \
            "overall_score must be numeric"
        assert 0 <= score <= 1, \
            "overall_score must be between 0 and 1"


def validate_context_metrics(response_data: Dict[str, Any]) -> None:
    """
    Validate context guard metrics.
    
    Args:
        response_data: Response data from context guard
        
    Raises:
        AssertionError: If metrics are invalid
    """
    if 'consciousness_validated' in response_data:
        assert isinstance(response_data['consciousness_validated'], bool), \
            "consciousness_validated must be boolean"


def validate_bias_metrics(response_data: Dict[str, Any]) -> None:
    """
    Validate bias guard metrics.
    
    Args:
        response_data: Response data from bias guard
        
    Raises:
        AssertionError: If metrics are invalid
    """
    if 'bias_detected' in response_data:
        assert isinstance(response_data['bias_detected'], bool), \
            "bias_detected must be boolean"
    
    if 'confidence' in response_data:
        confidence = response_data['confidence']
        assert isinstance(confidence, (int, float)), \
            "confidence must be numeric"
        assert 0 <= confidence <= 1, \
            "confidence must be between 0 and 1"


def get_guard_service_urls() -> Dict[str, str]:
    """
    Get URLs for all guard services.
    
    Returns:
        Dictionary mapping service names to URLs
    """
    return {
        'securityguard': 'http://localhost:8005',
        'contextguard': 'http://localhost:8003',
        'trustguard': 'http://localhost:8002',
        'biasguard': 'http://localhost:8004'
    }


def get_gateway_url() -> str:
    """
    Get the gateway URL.
    
    Returns:
        Gateway URL
    """
    return 'http://localhost:8000'
