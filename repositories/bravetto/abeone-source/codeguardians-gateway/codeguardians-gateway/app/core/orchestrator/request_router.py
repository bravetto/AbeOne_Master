"""
Request Router Component - Production Hardened

Handles request routing and payload transformation with:
- Service-specific routing
- Payload transformation
- Request validation
- Production-ready error handling
"""

import logging
from typing import Dict, Any, Optional
import httpx

from app.core.guard_orchestrator import (
    OrchestrationRequest,
    GuardServiceType,
    GuardServiceConfig
)
from app.core.config import get_settings
from app.core.exceptions import (
    GuardServiceError,
    ServiceUnavailableError,
    ConfigurationError
)
from app.utils.logging import get_logger
from prometheus_client import Counter, Histogram

logger = get_logger(__name__)
settings = get_settings()

# Prometheus metrics
ROUTING_COUNTER = Counter(
    'orchestrator_routing_total',
    'Total routing operations',
    ['service_name', 'status']
)

ROUTING_DURATION = Histogram(
    'REPLACE_ME',
    'Request routing duration',
    ['service_name']
)

PAYLOAD_SIZE = Histogram(
    'orchestrator_payload_size_bytes',
    'Payload size in bytes',
    ['service_name']
)


class RequestRouter:
    """
    Request routing component for guard services.
    
    PRODUCTION HARDENED:
    - Comprehensive metrics
    - Payload size limits
    - Timeout protection
    - Error resilience
    """
    
    def __init__(self, http_client: httpx.AsyncClient):
        """
        Initialize request router.
        
        Args:
            http_client: HTTP client for routing requests
        """
        self.http_client = http_client
        
        # Production hardening: Resource limits
        self.max_payload_size = 10 * 1024 * 1024  # 10MB
        self.max_timeout = 300  # 5 minutes
        self.default_timeout = 30  # seconds
    
    def determine_endpoint(self, request: OrchestrationRequest) -> str:
        """
        Determine the appropriate endpoint for a request.
        
        PRODUCTION: Validates service type, returns safe defaults
        """
        if not isinstance(request, OrchestrationRequest):
            raise ValueError("Invalid request type")
        
        service_type = request.service_type
        
        if not isinstance(service_type, GuardServiceType):
            raise ValueError(f"Invalid service type: {service_type}")
        
        # Default endpoints for each service type
        # These must match the actual endpoints exposed by each guard service
        endpoints = {
            GuardServiceType.TOKEN_GUARD: "/scan",
            GuardServiceType.TRUST_GUARD: "/validate",  # Updated to match actual TrustGuard endpoint
            GuardServiceType.CONTEXT_GUARD: "/analyze",
            GuardServiceType.BIAS_GUARD: "/process",  # Updated to match actual BiasGuard endpoint
            GuardServiceType.HEALTH_GUARD: "/analyze",
            GuardServiceType.SECURITY_GUARD: "/scan",  # Updated to match actual SecurityGuard endpoint
        }
        
        endpoint = endpoints.get(service_type, "/api/v1/process")
        
        # Validate endpoint format
        if not isinstance(endpoint, str) or not endpoint.startswith('/'):
            logger.warning(f"Invalid endpoint format for {service_type}: {endpoint}, using default")
            endpoint = "/api/v1/process"
        
        return endpoint
    
    def transform_payload(self, request: OrchestrationRequest) -> Dict[str, Any]:
        """
        Transform the generic payload to match service-specific schema.
        
        PRODUCTION: Validates payload, handles edge cases, tracks metrics
        """
        if not isinstance(request, OrchestrationRequest):
            raise ValueError("Invalid request type")
        
        service_type = request.service_type
        
        if not isinstance(service_type, GuardServiceType):
            raise ValueError(f"Invalid service type: {service_type}")
        
        # Ensure payload is a dict
        if not isinstance(request.payload, dict):
            logger.warning(f"Invalid payload type: {type(request.payload)}, using empty dict")
            payload = {}
        else:
            payload = request.payload.copy()
        
        # Validate payload size
        import json
        payload_size = len(json.dumps(payload).encode('utf-8'))
        PAYLOAD_SIZE.labels(service_name=service_type.value).observe(payload_size)
        
        if payload_size > self.max_payload_size:
            raise ValueError(f"Payload size {payload_size} exceeds maximum {self.max_payload_size}")
        
        # Add request metadata
        if request.user_id and 'user_id' not in payload:
            payload['user_id'] = request.user_id
        if request.session_id and 'session_id' not in payload:
            payload['session_id'] = request.session_id
        if request.request_id and 'request_id' not in payload:
            payload['request_id'] = request.request_id
        
        # Service-specific transformations
        if service_type == GuardServiceType.TOKEN_GUARD:
            return {
                "content": payload.get("content", payload.get("text", "")),
                "confidence": payload.get("confidence", 0.7),
                "logprobs_stream": payload.get("logprobs_stream"),
                "user_id": payload.get("user_id", request.user_id),
                "session_id": payload.get("session_id", request.session_id),
                "request_id": payload.get("request_id", request.request_id)
            }
        
        elif service_type == GuardServiceType.TRUST_GUARD:
            # TrustGuard expects: input_text, output_text, context (optional)
            context = payload.get("context")
            if isinstance(context, dict):
                import json
                context = json.dumps(context)
            
            return {
                "input_text": payload.get("input_text", payload.get("text", "")),
                "output_text": payload.get("output_text", payload.get("output", "")),
                "context": context,
                "user_id": payload.get("user_id", request.user_id),
                "session_id": payload.get("session_id", request.session_id),
                "request_id": payload.get("request_id", request.request_id)
            }
        
        elif service_type == GuardServiceType.CONTEXT_GUARD:
            return {
                "current_code": payload.get("current_code", payload.get("text", "")),
                "previous_code": payload.get("previous_code", ""),
                "context": payload.get("context", {}),
                "user_id": payload.get("user_id", request.user_id),
                "session_id": payload.get("session_id", request.session_id),
                "request_id": payload.get("request_id", request.request_id)
            }
        
        elif service_type == GuardServiceType.BIAS_GUARD:
            # BiasGuard expects: text, context (optional), detailed_analysis (optional)
            text = payload.get("text", "")
            
            # Handle various input formats
            if not text:
                if "samples" in payload and isinstance(payload["samples"], list) and len(payload["samples"]) > 0:
                    sample = payload["samples"][0]
                    if isinstance(sample, dict):
                        text = sample.get("content") or sample.get("text", "")
                    else:
                        text = str(sample)
                elif "content" in payload:
                    text = payload["content"]
                elif "data" in payload and isinstance(payload["data"], dict):
                    text = payload["data"].get("text", "")
            
            return {
                "text": text,
                "context": payload.get("context", {}),
                "detailed_analysis": payload.get("detailed_analysis", False),
                "user_id": payload.get("user_id", request.user_id),
                "session_id": payload.get("session_id", request.session_id),
                "request_id": payload.get("request_id", request.request_id)
            }
        
        elif service_type == GuardServiceType.HEALTH_GUARD:
            return {
                "samples": payload.get("samples", []),
                "user_id": payload.get("user_id", request.user_id),
                "session_id": payload.get("session_id", request.session_id),
                "request_id": payload.get("request_id", request.request_id)
            }
        
        elif service_type == GuardServiceType.SECURITY_GUARD:
            return {
                "content": payload.get("content", payload.get("text", "")),
                "context": payload.get("context", {}),
                "strict_mode": payload.get("strict_mode", False),
                "user_id": payload.get("user_id", request.user_id),
                "session_id": payload.get("session_id", request.session_id),
                "request_id": payload.get("request_id", request.request_id)
            }
        
        # Default: return payload as-is
        return payload
    
    async def route_request(
        self,
        request: OrchestrationRequest,
        config: GuardServiceConfig
    ) -> Dict[str, Any]:
        """
        Route a request to the appropriate service.
        
        PRODUCTION: Comprehensive validation, timeout protection, metrics
        """
        import time
        start_time = time.time()
        service_name = request.service_type.value
        
        try:
            # Validate inputs
            if not isinstance(request, OrchestrationRequest):
                raise ValueError("Invalid request type")
            
            if not config:
                raise ServiceUnavailableError(f"Service configuration not found for {service_name}")
            
            if not isinstance(config, GuardServiceConfig):
                raise ConfigurationError(f"Invalid configuration type for {service_name}")
            
            if not self.http_client:
                raise ServiceUnavailableError("HTTP client not initialized")
            
            if not isinstance(self.http_client, httpx.AsyncClient):
                raise ServiceUnavailableError("HTTP client is not a valid AsyncClient instance")
            
            if not config.base_url:
                raise ConfigurationError(f"Base URL not configured for {service_name}")
            
            # Determine endpoint
            endpoint = self.determine_endpoint(request)
            
            # Construct URL
            base_url = config.base_url.rstrip('/')
            url = f"{base_url}{endpoint}"
            
            if not url.startswith(('http://', 'https://')):
                raise ConfigurationError(f"Invalid URL format: {url}")
            
            # Transform payload
            transformed_payload = self.transform_payload(request)
            
            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "X-Request-ID": request.request_id,
                "X-Gateway-Request": "true"
            }
            
            # Add internal access token for internal services
            if self._is_internal_service(config.base_url):
                headers["X-Internal-Token"] = settings.INTERNAL_ACCESS_TOKEN
            
            if request.user_id:
                headers["X-User-ID"] = request.user_id
            
            if request.session_id:
                headers["X-Session-ID"] = request.session_id
            
            # Add authentication headers
            if config.auth_token:
                try:
                    if isinstance(config.auth_token, str):
                        auth_header_value = config.auth_header_format.format(token=config.auth_token)
                        headers[config.auth_header_name] = auth_header_value
                        headers["X-API-Key"] = config.auth_token
                except Exception as auth_error:
                    logger.warning(f"Failed to add auth headers for {service_name}: {auth_error}")
            
            # Validate and set timeout
            timeout_seconds = request.timeout if request.timeout and request.timeout > 0 else config.timeout
            if timeout_seconds <= 0:
                timeout_seconds = self.default_timeout
            
            if timeout_seconds > self.max_timeout:
                timeout_seconds = self.max_timeout
            
            timeout = httpx.Timeout(timeout_seconds)
            
            # Make request
            response = await self.http_client.post(
                url,
                json=transformed_payload,
                headers=headers,
                timeout=timeout
            )
            
            duration = time.time() - start_time
            ROUTING_DURATION.labels(service_name=service_name).observe(duration)
            
            # Handle response
            if response.status_code == 200:
                ROUTING_COUNTER.labels(service_name=service_name, status="success").inc()
                try:
                    if not response.content:
                        return {"status": "success", "message": "Empty response"}
                    return response.json()
                except Exception as json_error:
                    logger.warning(f"Failed to parse JSON response from {service_name}: {json_error}")
                    return {"status": "success", "raw_response": response.text[:500]}
            
            elif response.status_code == 401:
                ROUTING_COUNTER.labels(service_name=service_name, status="auth_error").inc()
                error_msg = f"Authentication failed for {service_name}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg = error_data["detail"]
                except Exception as json_error:
                    logger.debug(f"Failed to parse auth error JSON: {json_error}")
                raise GuardServiceError(error_msg)
            
            elif response.status_code == 403:
                ROUTING_COUNTER.labels(service_name=service_name, status="forbidden").inc()
                error_msg = f"Permission denied for {service_name}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg = error_data["detail"]
                except Exception as json_error:
                    logger.debug(f"Failed to parse permission error JSON: {json_error}")
                raise GuardServiceError(error_msg)
            
            elif response.status_code == 404:
                ROUTING_COUNTER.labels(service_name=service_name, status="not_found").inc()
                raise GuardServiceError(f"Endpoint not found for {service_name}: {endpoint}")
            
            else:
                ROUTING_COUNTER.labels(service_name=service_name, status="error").inc()
                error_msg = f"Service returned status {response.status_code}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg = error_data["detail"]
                    elif "error" in error_data:
                        error_msg = error_data["error"]
                except:
                    if response.text:
                        error_msg = response.text[:200]
                raise GuardServiceError(error_msg)
        
        except httpx.TimeoutException as e:
            duration = time.time() - start_time
            ROUTING_DURATION.labels(service_name=service_name).observe(duration)
            ROUTING_COUNTER.labels(service_name=service_name, status="timeout").inc()
            raise GuardServiceError(f"Request timeout for {service_name}: {str(e)}")
        
        except httpx.ConnectError as e:
            duration = time.time() - start_time
            ROUTING_DURATION.labels(service_name=service_name).observe(duration)
            ROUTING_COUNTER.labels(service_name=service_name, status="connection_error").inc()
            raise GuardServiceError(f"Connection failed for {service_name}: {str(e)}")
        
        except Exception as e:
            duration = time.time() - start_time
            ROUTING_DURATION.labels(service_name=service_name).observe(duration)
            ROUTING_COUNTER.labels(service_name=service_name, status="exception").inc()
            raise
    
    def _is_internal_service(self, base_url: str) -> bool:
        """Check if service is internal."""
        internal_hosts = ["localhost", "127.0.0.1", "0.0.0.0"]
        return any(host in base_url for host in internal_hosts)

