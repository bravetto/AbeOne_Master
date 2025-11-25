"""
Internal Guard Services API Routes

This module provides internal API endpoints for individual guard services.
These endpoints are for internal use only and should not be exposed to external clients.
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
from app.utils.logging import get_logger
from app.api.dependencies import require_internal_access

logger = get_logger(__name__)
router = APIRouter(prefix="/internal/guards", tags=["Internal Guard Services"])

# Payload size limits
MAX_PAYLOAD_SIZE = 10 * 1024 * 1024  # 10MB
MAX_PAYLOAD_SIZE_STRICT = 1 * 1024 * 1024  # 1MB for management endpoints


class InternalGuardRequest(BaseModel):
    """Internal request model for guard service operations."""
    service_type: str = Field(..., description="Type of guard service to use")
    payload: Dict[str, Any] = Field(..., description="Request payload for the guard service")
    user_id: Optional[str] = Field(None, description="User ID for request tracking")
    session_id: Optional[str] = Field(None, description="Session ID for request tracking")
    priority: int = Field(1, description="Request priority (1-10)")
    timeout: Optional[int] = Field(None, description="Request timeout in seconds")
    fallback_enabled: bool = Field(True, description="Enable fallback mechanisms")


class InternalGuardResponse(BaseModel):
    """Internal response model for guard service operations."""
    request_id: str
    service_type: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None
    service_used: Optional[str] = None
    fallback_used: bool = False


async def process_internal_guard_request(
    request: InternalGuardRequest,
    background_tasks: BackgroundTasks,
    http_request: Request
) -> InternalGuardResponse:
    """Process an internal guard request."""
    # Generate unique request ID
    request_id = str(uuid.uuid4())

    # Validate payload size
    payload_size = len(json.dumps(request.payload).encode('utf-8'))
    if payload_size > MAX_PAYLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"Payload exceeds maximum size of {MAX_PAYLOAD_SIZE} bytes (got {payload_size} bytes)"
        )

    # Validate service type
    try:
        service_type = GuardServiceType(request.service_type.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid service type: {request.service_type}. "
                   f"Valid types: {[t.value for t in GuardServiceType]}"
        )

    try:
        # Create orchestration request
        orchestration_request = OrchestrationRequest(
            request_id=request_id,
            service_type=service_type,
            payload=request.payload,
            user_id=request.user_id,
            session_id=request.session_id,
            priority=request.priority,
            timeout=request.timeout,
            fallback_enabled=request.fallback_enabled
        )

        # Process request through orchestrator
        response = await orchestrator.orchestrate_request(orchestration_request)

        # Log request for monitoring
        background_tasks.add_task(
            log_internal_guard_request,
            request_id,
            service_type.value,
            request.user_id,
            response.success,
            response.processing_time
        )

        return InternalGuardResponse(
            request_id=response.request_id,
            service_type=response.service_type.value,
            success=response.success,
            data=response.data,
            error=response.error,
            processing_time=response.processing_time,
            service_used=response.service_used,
            fallback_used=response.fallback_used
        )

    except GuardServiceError as e:
        logger.error(f"Internal guard service error: {e}")
        raise HTTPException(status_code=502, detail=str(e))
    except ServiceUnavailableError as e:
        logger.error(f"Internal service unavailable: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in internal guard request processing: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/tokenguard/optimize", response_model=InternalGuardResponse)
async def internal_optimize_tokens(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    http_request: Request,
    _: None = Depends(require_internal_access)
) -> InternalGuardResponse:
    """
    Internal endpoint for TokenGuard token optimization.
    
    This endpoint provides direct access to TokenGuard's token optimization
    capabilities for internal services and testing.
    """
    guard_request = InternalGuardRequest(
        service_type="tokenguard",
        payload=request,
        user_id=http_request.headers.get("X-User-ID"),
        session_id=http_request.headers.get("X-Session-ID")
    )
    
    return await process_internal_guard_request(guard_request, background_tasks, http_request)


@router.post("/trustguard/validate", response_model=InternalGuardResponse)
async def internal_validate_trust(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    http_request: Request,
    _: None = Depends(require_internal_access)
) -> InternalGuardResponse:
    """
    Internal endpoint for TrustGuard validation.
    
    This endpoint provides direct access to TrustGuard's AI failure pattern
    detection and validation capabilities for internal services.
    """
    guard_request = InternalGuardRequest(
        service_type="trustguard",
        payload=request,
        user_id=http_request.headers.get("X-User-ID"),
        session_id=http_request.headers.get("X-Session-ID")
    )
    
    return await process_internal_guard_request(guard_request, background_tasks, http_request)


@router.post("/contextguard/analyze", response_model=InternalGuardResponse)
async def internal_analyze_context(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    http_request: Request,
    _: None = Depends(require_internal_access)
) -> InternalGuardResponse:
    """
    Internal endpoint for ContextGuard analysis.
    
    This endpoint provides direct access to ContextGuard's context drift
    detection and memory management capabilities for internal services.
    """
    guard_request = InternalGuardRequest(
        service_type="contextguard",
        payload=request,
        user_id=http_request.headers.get("X-User-ID"),
        session_id=http_request.headers.get("X-Session-ID")
    )
    
    return await process_internal_guard_request(guard_request, background_tasks, http_request)


@router.post("/biasguard/detect", response_model=InternalGuardResponse)
async def internal_detect_bias(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    http_request: Request,
    _: None = Depends(require_internal_access)
) -> InternalGuardResponse:
    """
    Internal endpoint for BiasGuard detection.
    
    This endpoint provides direct access to BiasGuard's bias detection
    and mitigation capabilities for internal services.
    """
    guard_request = InternalGuardRequest(
        service_type="biasguard",
        payload=request,
        user_id=http_request.headers.get("X-User-ID"),
        session_id=http_request.headers.get("X-Session-ID")
    )
    
    return await process_internal_guard_request(guard_request, background_tasks, http_request)


@router.post("/healthguard/monitor", response_model=InternalGuardResponse)
async def internal_monitor_health(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    http_request: Request,
    _: None = Depends(require_internal_access)
) -> InternalGuardResponse:
    """
    Internal endpoint for HealthGuard monitoring.
    
    This endpoint provides direct access to HealthGuard's system health
    monitoring and poisoning detection capabilities for internal services.
    """
    guard_request = InternalGuardRequest(
        service_type="healthguard",
        payload=request,
        user_id=http_request.headers.get("X-User-ID"),
        session_id=http_request.headers.get("X-Session-ID")
    )
    
    return await process_internal_guard_request(guard_request, background_tasks, http_request)


async def log_internal_guard_request(
    request_id: str,
    service_type: str,
    user_id: Optional[str],
    success: bool,
    processing_time: Optional[float]
):
    """Log internal guard request for monitoring and analytics."""
    logger.info(
        f"Internal guard request processed - "
        f"ID: {request_id}, "
        f"Service: {service_type}, "
        f"User: {user_id}, "
        f"Success: {success}, "
        f"Time: {processing_time:.3f}s"
    )

