"""
CodeGuardians Gateway - Guard Services API Routes

This module provides the API endpoints for interacting with guard services
through the unified gateway.
"""

import uuid
import json
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import logging

from app.core.guard_orchestrator import (
    orchestrator,
    OrchestrationRequest,
    OrchestrationResponse,
    GuardServiceType,
    ServiceHealth
)
from app.core.exceptions import GuardServiceError, ServiceUnavailableError
from app.api.dependencies import get_current_user, require_admin_access
from app.middleware.explicit_rate_limiting import public_rate_limit, admin_rate_limit
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/guards", tags=["Guard Services"])

# Payload size limits
MAX_PAYLOAD_SIZE = 10 * 1024 * 1024  # 10MB
MAX_PAYLOAD_SIZE_STRICT = 1 * 1024 * 1024  # 1MB for management endpoints


def validate_service_url(url: str) -> bool:
    """
    Validate service URL is safe and properly formatted.
    
    Args:
        url: Service URL to validate
        
    Returns:
        True if URL is valid, False otherwise
    """
    from urllib.parse import urlparse
    import os
    
    try:
        parsed = urlparse(url)
        
        # Only allow http/https schemes
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Validate URL format
        if not parsed.hostname:
            return False
        
        # In production, block localhost/127.0.0.1 unless explicitly allowed
        is_production = os.getenv('ENVIRONMENT', 'development').lower() == 'production'
        if is_production:
            if parsed.hostname.lower() in ['localhost', '127.0.0.1', '0.0.0.0']:
                # Only allow if explicitly permitted via environment variable
                allow_localhost = os.getenv('ALLOW_LOCALHOST_SERVICES', 'false').lower() == 'true'
                if not allow_localhost:
                    return False
        
        return True
    
    except Exception:
        return False


def sanitize_service_name(name: str) -> str:
    """
    Sanitize service name to prevent injection attacks.
    
    Args:
        name: Service name to sanitize
        
    Returns:
        Sanitized service name (alphanumeric + hyphen/underscore only)
    """
    import re
    # Only allow alphanumeric, hyphen, underscore
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '', name)
    return sanitized


class GuardRequest(BaseModel):
    """Request model for guard service operations."""
    service_type: str = Field(..., description="Type of guard service to use")
    payload: Dict[str, Any] = Field(..., description="Request payload for the guard service")
    user_id: Optional[str] = Field(None, description="User ID for request tracking")
    session_id: Optional[str] = Field(None, description="Session ID for request tracking")
    priority: int = Field(1, description="Request priority (1-10)")
    timeout: Optional[int] = Field(None, description="Request timeout in seconds")
    fallback_enabled: bool = Field(True, description="Enable fallback mechanisms")
    client_type: Optional[str] = Field("web", description="Client type: web, vscode, chrome, api")
    client_version: Optional[str] = Field(None, description="Client version for compatibility")
    request_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional request metadata")


class GuardResponse(BaseModel):
    """Response model for guard service operations."""
    request_id: str
    service_type: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None
    service_used: Optional[str] = None
    fallback_used: bool = False
    client_type: Optional[str] = None
    confidence_score: Optional[float] = None
    warnings: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Response model for service health checks."""
    service_name: str
    status: str
    last_check: str
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = {}


@router.post("/process", response_model=GuardResponse)
@public_rate_limit(requests_per_minute=100)
async def process_guard_request(
    request: GuardRequest,
    background_tasks: BackgroundTasks,
    http_request: Request
) -> GuardResponse:
    """
    Process a request through the appropriate guard service.
    
    This unified endpoint handles requests from all client types:
    - Web applications
    - VS Code extensions
    - Chrome extensions
    - API clients
    
    The endpoint automatically adapts responses based on client type and
    provides appropriate formatting and metadata for each client.
    """
    # Extract request ID from request state (set by middleware) or generate new one
    request_id = getattr(http_request.state, "request_id", None) or http_request.headers.get("X-Request-ID") or str(uuid.uuid4())

    # Enhanced input validation
    from app.core.input_validation import get_input_validator
    validator = get_input_validator()
    validator.clear_threats()
    
    # Validate payload size
    payload_size = len(json.dumps(request.payload).encode('utf-8'))
    if not validator.validate_payload_size(request.payload):
        # Record payload size metric before rejecting
        try:
            from app.core.orchestrator_metrics import record_payload_size
            record_payload_size(http_request.url.path if hasattr(http_request, 'url') else '/process', payload_size)
        except Exception:
            pass
        
        raise HTTPException(
            status_code=413,
            detail=f"Payload exceeds maximum size of {MAX_PAYLOAD_SIZE} bytes (got {payload_size} bytes)"
        )
    
    # Validate payload content for security threats
    payload_str = json.dumps(request.payload)
    if validator.detect_sql_injection(payload_str):
        raise HTTPException(
            status_code=400,
            detail="SQL injection pattern detected in payload"
        )
    if validator.detect_xss(payload_str):
        raise HTTPException(
            status_code=400,
            detail="XSS pattern detected in payload"
        )
    if validator.detect_command_injection(payload_str):
        raise HTTPException(
            status_code=400,
            detail="Command injection pattern detected in payload"
        )
    
    # Validate JSON structure depth
    if not validator.validate_json_structure(request.payload):
        raise HTTPException(
            status_code=400,
            detail="JSON structure exceeds maximum depth"
        )
    
    # Record payload size metrics (for valid requests)
    try:
        from app.core.orchestrator_metrics import record_payload_size
        record_payload_size(http_request.url.path if hasattr(http_request, 'url') else '/process', payload_size)
    except Exception:
        pass

    # Validate service type
    try:
        service_type = GuardServiceType(request.service_type.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid service type: {request.service_type}. "
                   f"Valid types: {[t.value for t in GuardServiceType]}"
        )

    # Validate client type
    valid_client_types = ["web", "vscode", "chrome", "api"]
    client_type = request.client_type or "web"
    if client_type not in valid_client_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid client type: {client_type}. "
                   f"Valid types: {valid_client_types}"
        )

    try:
        # Extract Clerk token from request if available (for unified API key)
        from app.core.clerk_auth import get_unified_api_key_from_request
        clerk_token = get_unified_api_key_from_request(http_request)
        
        # Validate payload
        if not isinstance(request.payload, dict):
            raise HTTPException(
                status_code=400,
                detail="Payload must be a dictionary/object"
            )
        
        if not request.payload:
            raise HTTPException(
                status_code=400,
                detail="Payload cannot be empty"
            )
        
        # Enhance payload with client-specific metadata
        enhanced_payload = request.payload.copy()
        enhanced_payload.update({
            "client_type": client_type,
            "client_version": request.client_version,
            "request_metadata": request.request_metadata or {},
            "user_agent": http_request.headers.get("user-agent", ""),
            "ip_address": http_request.client.host if http_request.client else None
        })

        # Create orchestration request
        orchestration_request = OrchestrationRequest(
            request_id=request_id,
            service_type=service_type,
            payload=enhanced_payload,
            user_id=request.user_id,
            session_id=request.session_id,
            priority=request.priority,
            timeout=request.timeout,
            fallback_enabled=request.fallback_enabled
        )
        
        # If Clerk token is available, use it as unified API key for all services
        original_configs = {}
        if clerk_token:
            # Temporarily override auth tokens for this request
            for service_name, config in orchestrator.services.items():
                original_configs[service_name] = config.auth_token
                # Use Clerk token as unified API key
                config.auth_token = clerk_token

        try:
            # Process request through orchestrator
            response = await orchestrator.orchestrate_request(orchestration_request)
            
            # Enhance response based on client type
            enhanced_response = await enhance_response_for_client(
                response, client_type, request.client_version
            )

            # Log request for monitoring
            background_tasks.add_task(
                log_guard_request,
                request_id,
                service_type.value,
                request.user_id,
                response.success,
                response.processing_time,
                client_type,
                response.data  # Pass response data for metrics tracking
            )

            return GuardResponse(
                request_id=enhanced_response.request_id,
                service_type=enhanced_response.service_type.value,
                success=enhanced_response.success,
                data=enhanced_response.data,
                error=enhanced_response.error,
                processing_time=enhanced_response.processing_time,
                service_used=enhanced_response.service_used,
                fallback_used=enhanced_response.fallback_used,
                client_type=client_type,
                confidence_score=enhanced_response.data.get("confidence") if enhanced_response.data else None,
                warnings=enhanced_response.data.get("warnings") if enhanced_response.data else None,
                recommendations=enhanced_response.data.get("recommendations") if enhanced_response.data else None,
                metadata=enhanced_response.data.get("metadata") if enhanced_response.data else None
            )
        finally:
            # Always restore original auth tokens if Clerk token was used
            if clerk_token and original_configs:
                for service_name, original_token in original_configs.items():
                    if service_name in orchestrator.services:
                        orchestrator.services[service_name].auth_token = original_token

    except GuardServiceError as e:
        logger.error(f"Guard service error: {e}")
        raise HTTPException(status_code=502, detail=str(e))
    except ServiceUnavailableError as e:
        logger.error(f"Service unavailable: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except HTTPException:
        # Re-raise HTTPExceptions (validation errors, etc.)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in guard request processing: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Individual guard service endpoints have been moved to /internal/guards
# for internal use only. External clients should use the unified /process endpoint.


@router.get("/status", response_model=Dict[str, HealthResponse])
async def get_services_status(
    current_user = Depends(get_current_user)
) -> Dict[str, HealthResponse]:
    """
    Get status of all guard services (alias for /health).
    
    Returns the current health status, response times, and metadata
    for all registered guard services.
    """
    return await get_services_health()


@router.post("/scan", response_model=GuardResponse)
async def scan_text(
    request: GuardRequest,
    background_tasks: BackgroundTasks,
    http_request: Request
) -> GuardResponse:
    """
    Scan text using the appropriate guard service.
    
    This is an alias for the /process endpoint for backward compatibility.
    """
    return await process_guard_request(request, background_tasks, http_request)


@router.get("/health", response_model=Dict[str, HealthResponse])
async def get_services_health(
    current_user = Depends(get_current_user)
) -> Dict[str, HealthResponse]:
    """
    Get health status of all guard services.
    
    Returns the current health status, response times, and metadata
    for all registered guard services.
    """
    try:
        health_data = await orchestrator.get_service_health()
        
        response = {}
        for service_name, health in health_data.items():
            response[service_name] = HealthResponse(
                service_name=health.service_name,
                status=health.status.value,
                last_check=health.last_check.isoformat(),
                response_time=health.response_time,
                error_message=health.error_message,
                metadata=health.metadata
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting service health: {e}")
        raise HTTPException(status_code=500, detail="Failed to get service health")


@router.get("/health/{service_name}", response_model=HealthResponse)
async def get_service_health(
    service_name: str,
    current_user = Depends(get_current_user)
) -> HealthResponse:
    """
    Get health status of a specific guard service.
    
    Returns the current health status, response time, and metadata
    for the specified guard service.
    """
    # Sanitize service name
    sanitized_name = sanitize_service_name(service_name)
    if sanitized_name != service_name:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid service name: {service_name}. Only alphanumeric characters, hyphens, and underscores allowed."
        )
    
    try:
        health = await orchestrator.get_service_health(sanitized_name)
        
        return HealthResponse(
            service_name=health.service_name,
            status=health.status.value,
            last_check=health.last_check.isoformat(),
            response_time=health.response_time,
            error_message=health.error_message,
            metadata=health.metadata
        )
        
    except Exception as e:
        logger.error(f"Error getting health for service {sanitized_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get health for {sanitized_name}")


@router.post("/health/refresh")
async def refresh_health_checks(
    background_tasks: BackgroundTasks,
    admin_user = Depends(require_admin_access)
) -> JSONResponse:
    """
    Refresh health checks for all guard services.
    
    Triggers immediate health checks for all registered services
    and updates their status.
    """
    try:
        background_tasks.add_task(orchestrator.refresh_health_checks)
        
        return JSONResponse(
            status_code=202,
            content={"message": "Health checks refresh initiated"}
        )
        
    except Exception as e:
        logger.error(f"Error refreshing health checks: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh health checks")


@router.get("/discovery/services")
async def get_discovered_services(
    current_user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get information about all discovered guard services.
    
    Returns detailed information about all services discovered
    through auto-discovery or manual registration.
    """
    try:
        discovered_services = orchestrator.get_discovered_services()
        
        return {
            "total_services": len(discovered_services),
            "auto_discovery_enabled": orchestrator.auto_discovery_enabled,
            "discovery_interval": orchestrator.discovery_interval,
            "services": discovered_services
        }
        
    except Exception as e:
        logger.error(f"Error getting discovered services: {e}")
        raise HTTPException(status_code=500, detail="Failed to get discovered services")


@router.post("/discovery/register")
async def register_service(
    service_name: str,
    base_url: str,
    service_type: str,
    health_endpoint: str = "/health",
    priority: int = 1,
    tags: List[str] = None,
    admin_user = Depends(require_admin_access)
) -> JSONResponse:
    """
    Manually register a guard service.
    
    Allows manual registration of guard services that may not be
    discovered automatically.
    """
    try:
        # Sanitize and validate service name
        sanitized_name = sanitize_service_name(service_name)
        if sanitized_name != service_name:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid service name: {service_name}. Only alphanumeric characters, hyphens, and underscores allowed."
            )
        
        # Validate service URL
        if not validate_service_url(base_url):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid service URL: {base_url}. Must be http/https and valid format."
            )
        
        # Convert string to enum
        from app.core.guard_orchestrator import GuardServiceType
        service_type_enum = GuardServiceType(service_type.lower())
        
        success = await orchestrator.register_service(
            service_name=sanitized_name,
            base_url=base_url,
            service_type=service_type_enum,
            health_endpoint=health_endpoint,
            priority=priority,
            tags=tags or []
        )
        
        if success:
            return JSONResponse(
                status_code=201,
                content={"message": f"Service {service_name} registered successfully"}
            )
        else:
            raise HTTPException(status_code=400, detail=f"Failed to register service {service_name}")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid service type: {service_type}")
    except Exception as e:
        logger.error(f"Error registering service {service_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to register service {service_name}")


@router.delete("/discovery/services/{service_name}")
async def unregister_service(
    service_name: str,
    admin_user = Depends(require_admin_access)
) -> JSONResponse:
    """
    Unregister a guard service.
    
    Removes a service from the orchestrator and stops monitoring it.
    """
    # Sanitize service name
    sanitized_name = sanitize_service_name(service_name)
    if sanitized_name != service_name:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid service name: {service_name}. Only alphanumeric characters, hyphens, and underscores allowed."
        )
    try:
        success = await orchestrator.unregister_service(sanitized_name)

        if success:
            return JSONResponse(
                status_code=200,
                content={"message": f"Service {sanitized_name} unregistered successfully"}
            )
        else:
            # Service not found - return 404 as expected by test
            logger.info(f"Service {sanitized_name} not found for unregistration")
            raise HTTPException(status_code=404, detail=f"Service {sanitized_name} not found")

    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # Log the error and return a more specific error message
        logger.error(f"Unexpected error unregistering service {sanitized_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to unregister service {sanitized_name}: {str(e)}")


@router.post("/discovery/refresh")
async def refresh_discovery(
    background_tasks: BackgroundTasks,
    admin_user = Depends(require_admin_access)
) -> JSONResponse:
    """
    Trigger immediate service discovery.
    
    Forces an immediate discovery scan for new services
    without waiting for the next discovery interval.
    """
    try:
        background_tasks.add_task(orchestrator._discover_services)
        
        return JSONResponse(
            status_code=202,
            content={"message": "Service discovery refresh initiated"}
        )
        
    except Exception as e:
        logger.error(f"Error refreshing discovery: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh discovery")


@router.get("/health/aggregated", response_model=Dict[str, Any])
async def get_aggregated_health(
    current_user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get aggregated health status of all guard services.
    
    Returns overall status, healthy/total counts, and service breakdown
    with circuit breaker states summary.
    """
    try:
        health_data = await orchestrator.get_service_health()
        
        # Calculate overall status
        healthy_count = sum(
            1 for h in health_data.values() 
            if h.status.value == "healthy"
        )
        degraded_count = sum(
            1 for h in health_data.values()
            if h.status.value == "degraded"
        )
        total_count = len(health_data)
        
        # Determine overall status
        if healthy_count == total_count:
            overall_status = "healthy"
        elif healthy_count + degraded_count == total_count:
            overall_status = "degraded"
        else:
            overall_status = "unhealthy"
        
        # Get circuit breaker states summary
        circuit_breaker_summary = {}
        for service_name, breaker in orchestrator.circuit_breakers.items():
            circuit_breaker_summary[service_name] = {
                "state": breaker.state,
                "failure_count": breaker.failure_count,
                "last_failure": breaker.last_failure_time.isoformat() if breaker.last_failure_time else None
            }
        
        return {
            "overall_status": overall_status,
            "services_healthy": healthy_count,
            "services_degraded": degraded_count,
            "services_unhealthy": total_count - healthy_count - degraded_count,
            "services_total": total_count,
            "services": {
                name: {
                    "status": health.status.value,
                    "response_time": health.response_time,
                    "last_check": health.last_check.isoformat(),
                    "error_message": health.error_message
                }
                for name, health in health_data.items()
            },
            "circuit_breakers": circuit_breaker_summary
        }
        
    except Exception as e:
        logger.error(f"Error getting aggregated health: {e}")
        raise HTTPException(status_code=500, detail="Failed to get aggregated health")


@router.get("/services")
async def list_services(
    current_user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    List all available guard services and their configurations.
    
    Returns information about all registered guard services including
    their types, endpoints, and current status.
    """
    try:
        services_info = {}
        
        for service_name, config in orchestrator.services.items():
            health = orchestrator.health_status.get(service_name)
            
            services_info[service_name] = {
                "name": config.name,
                "service_type": config.service_type.value,
                "base_url": config.base_url,
                "enabled": config.enabled,
                "priority": config.priority,
                "tags": config.tags,
                "status": health.status.value if health else "unknown",
                "last_check": health.last_check.isoformat() if health else None
            }
        
        return {
            "services": services_info,
            "total_services": len(services_info),
            "healthy_services": len([s for s in services_info.values() if s["status"] == "healthy"])
        }
        
    except Exception as e:
        logger.error(f"Error listing services: {e}")
        raise HTTPException(status_code=500, detail="Failed to list services")


async def enhance_response_for_client(
    response: OrchestrationResponse,
    client_type: str,
    client_version: Optional[str]
) -> OrchestrationResponse:
    """
    Enhance response based on client type and version.
    
    Args:
        response: Original orchestration response
        client_type: Type of client (web, vscode, chrome, api)
        client_version: Version of the client
        
    Returns:
        Enhanced orchestration response
    """
    if not response.data:
        return response
    
    # Handle list responses (e.g., from HealthGuard)
    if isinstance(response.data, list):
        # Wrap list responses in a dict for consistent handling
        enhanced_data = {
            "results": response.data,
            "count": len(response.data)
        }
    else:
        enhanced_data = response.data.copy() if isinstance(response.data, dict) else {"data": response.data}
    
    # Add client-specific enhancements
    if client_type == "vscode":
        # VS Code specific enhancements
        enhanced_data.update({
            "vscode_compatible": True,
            "notifications": _format_vscode_notifications(enhanced_data),
            "quick_fixes": _extract_quick_fixes(enhanced_data),
            "diagnostics": _format_diagnostics(enhanced_data)
        })
    elif client_type == "chrome":
        # Chrome extension specific enhancements
        enhanced_data.update({
            "chrome_compatible": True,
            "badge_text": _generate_badge_text(enhanced_data),
            "popup_data": _format_popup_data(enhanced_data),
            "content_script_data": _format_content_script_data(enhanced_data)
        })
    elif client_type == "web":
        # Web application specific enhancements
        enhanced_data.update({
            "web_compatible": True,
            "ui_components": _format_ui_components(enhanced_data),
            "user_feedback": _format_user_feedback(enhanced_data)
        })
    elif client_type == "api":
        # API client specific enhancements
        enhanced_data.update({
            "api_compatible": True,
            "raw_data": enhanced_data.get("raw_data", {}),
            "structured_output": _format_structured_output(enhanced_data)
        })
    
    # Add version-specific enhancements
    if client_version:
        enhanced_data["client_version"] = client_version
        enhanced_data["version_compatibility"] = _check_version_compatibility(client_version)
    
    # Create enhanced response
    enhanced_response = OrchestrationResponse(
        request_id=response.request_id,
        service_type=response.service_type,
        success=response.success,
        data=enhanced_data,
        error=response.error,
        processing_time=response.processing_time,
        service_used=response.service_used,
        fallback_used=response.fallback_used
    )
    
    return enhanced_response


def _format_vscode_notifications(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Format data for VS Code notifications."""
    notifications = []
    
    if data.get("warnings"):
        for warning in data["warnings"]:
            notifications.append({
                "type": "warning",
                "message": warning,
                "severity": "warning"
            })
    
    if data.get("recommendations"):
        for rec in data["recommendations"]:
            notifications.append({
                "type": "info",
                "message": rec,
                "severity": "information"
            })
    
    return notifications


def _extract_quick_fixes(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract quick fixes for VS Code."""
    fixes = []
    
    if data.get("suggestions"):
        for suggestion in data["suggestions"]:
            fixes.append({
                "title": suggestion.get("title", "Apply suggestion"),
                "description": suggestion.get("description", ""),
                "action": suggestion.get("action", "replace"),
                "range": suggestion.get("range", {}),
                "newText": suggestion.get("newText", "")
            })
    
    return fixes


def _format_diagnostics(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Format diagnostics for VS Code."""
    diagnostics = []
    
    if data.get("issues"):
        for issue in data["issues"]:
            diagnostics.append({
                "range": issue.get("range", {}),
                "severity": issue.get("severity", "warning"),
                "message": issue.get("message", ""),
                "source": "AI Guardian"
            })
    
    return diagnostics


def _generate_badge_text(data: Dict[str, Any]) -> str:
    """Generate badge text for Chrome extension."""
    if data.get("issues_count", 0) > 0:
        return str(data["issues_count"])
    elif data.get("warnings_count", 0) > 0:
        return "!"
    else:
        return "✓"


def _format_popup_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format data for Chrome extension popup."""
    return {
        "summary": data.get("summary", "Analysis complete"),
        "issues": data.get("issues", []),
        "recommendations": data.get("recommendations", []),
        "confidence": data.get("confidence", 0.0)
    }


def _format_content_script_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format data for Chrome extension content script."""
    return {
        "highlights": data.get("highlights", []),
        "tooltips": data.get("tooltips", []),
        "overlay_data": data.get("overlay_data", {})
    }


def _format_ui_components(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format UI components for web application."""
    return {
        "alerts": data.get("alerts", []),
        "cards": data.get("cards", []),
        "charts": data.get("charts", []),
        "tables": data.get("tables", [])
    }


def _format_user_feedback(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format user feedback data for web application."""
    return {
        "rating_prompt": data.get("rating_prompt", "How helpful was this analysis?"),
        "feedback_fields": data.get("feedback_fields", []),
        "suggestions": data.get("suggestions", [])
    }


def _format_structured_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format structured output for API clients."""
    return {
        "analysis": data.get("analysis", {}),
        "metrics": data.get("metrics", {}),
        "raw_results": data.get("raw_results", {}),
        "confidence_scores": data.get("confidence_scores", {})
    }


def _check_version_compatibility(client_version: str) -> Dict[str, Any]:
    """Check client version compatibility."""
    # This would implement actual version checking logic
    return {
        "compatible": True,
        "min_required": "1.0.0",
        "recommended": "1.2.0",
        "deprecated": False
    }


async def log_guard_request(
    request_id: str,
    service_type: str,
    user_id: Optional[str],
    success: bool,
    processing_time: Optional[float],
    client_type: str = "unknown",
    response_data: Optional[Dict[str, Any]] = None
):
    """Log guard request for monitoring and analytics."""
    logger.info(
        f"Guard request processed - "
        f"ID: {request_id}, "
        f"Service: {service_type}, "
        f"User: {user_id}, "
        f"Success: {success}, "
        f"Time: {processing_time:.3f}s, "
        f"Client: {client_type}"
    )
    
    # Record real metrics if response data is available
    if success and response_data:
        try:
            from app.core.real_metrics_tracker import real_metrics_tracker
            await real_metrics_tracker.record_guard_operation(
                guard_name=service_type,
                response_data=response_data,
                processing_time=processing_time or 0.0,
                success=success,
                user_id=user_id,
                session_id=None  # Could extract from request if needed
            )
        except Exception as e:
            logger.error(f"Error recording real metrics: {e}")
