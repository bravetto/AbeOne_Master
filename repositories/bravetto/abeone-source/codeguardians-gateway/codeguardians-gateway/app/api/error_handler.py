"""
Standardized Error Response Handler

PRODUCTION HARDENING:
- Consistent error response format (error_code, timestamp, request_id)
- Request ID correlation
- Sensitive data masking
- Error logging with context

SAFETY: All errors follow consistent format
ASSUMES: Request ID available in request state
VERIFY: All error responses include required fields
"""

import time
import uuid
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import BaseAPIException
from app.core.error_sanitizer import sanitize_error_response
from app.utils.logging import get_logger

logger = get_logger(__name__)


def create_error_response(
    error_code: str,
    message: str,
    status_code: int = 500,
    request_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    timestamp: Optional[float] = None
) -> Dict[str, Any]:
    """
    Create standardized error response.
    
    Args:
        error_code: Error code identifier
        message: Human-readable error message
        status_code: HTTP status code
        request_id: Request ID for correlation
        details: Additional error details
        timestamp: Error timestamp (defaults to now)
    
    Returns:
        Standardized error response dict
    """
    if timestamp is None:
        timestamp = time.time()
    
    response = {
        "error": {
            "error_code": error_code,
            "message": message,
            "timestamp": timestamp,
            "request_id": request_id or str(uuid.uuid4())
        }
    }
    
    if details:
        # Mask sensitive data in details
        response["error"]["details"] = mask_sensitive_data(details)
    
    return response


def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mask sensitive data in error details.
    
    SAFETY: Prevents exposure of secrets in error responses
    """
    sensitive_keys = [
        "password", "secret", "token", "api_key", "access_key",
        "secret_key", "private_key", "credit_card", "ssn"
    ]
    
    masked = {}
    for key, value in data.items():
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in sensitive_keys):
            masked[key] = "***MASKED***"
        elif isinstance(value, dict):
            masked[key] = mask_sensitive_data(value)
        elif isinstance(value, list):
            masked[key] = [
                mask_sensitive_data(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            masked[key] = value
    
    return masked


async def handle_base_api_exception(
    request: Request,
    exc: BaseAPIException
) -> JSONResponse:
    """Handle BaseAPIException with standardized format."""
    request_id = getattr(request.state, "request_id", None)
    
    error_response = create_error_response(
        error_code=exc.error_code or "API_ERROR",
        message=exc.message,
        status_code=exc.status_code,
        request_id=request_id,
        details=exc.details
    )
    
    logger.error(
        f"API Error: {exc.error_code} - {exc.message}",
        extra={
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "request_id": request_id,
            "details": exc.details
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def handle_http_exception(
    request: Request,
    exc: HTTPException
) -> JSONResponse:
    """Handle HTTPException with standardized format."""
    request_id = getattr(request.state, "request_id", None)
    
    error_response = create_error_response(
        error_code=f"HTTP_{exc.status_code}",
        message=exc.detail,
        status_code=exc.status_code,
        request_id=request_id
    )
    
    logger.warning(
        f"HTTP Exception: {exc.status_code} - {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "request_id": request_id
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def handle_validation_error(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors with standardized format."""
    request_id = getattr(request.state, "request_id", None)
    
    error_response = create_error_response(
        error_code="VALIDATION_ERROR",
        message="Request validation failed",
        status_code=422,
        request_id=request_id,
        details={"errors": exc.errors()}
    )
    
    logger.warning(
        f"Validation Error: {exc.errors()}",
        extra={
            "request_id": request_id,
            "errors": exc.errors()
        }
    )
    
    return JSONResponse(
        status_code=422,
        content=error_response
    )


async def handle_generic_exception(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Handle unexpected exceptions with standardized format.
    
    Sanitizes error messages in production to prevent information disclosure.
    """
    request_id = getattr(request.state, "request_id", None)
    
    # Sanitize error response for production
    sanitized = sanitize_error_response(exc, detail="An unexpected error occurred")
    
    error_response = create_error_response(
        error_code="INTERNAL_ERROR",
        message=sanitized["error"],
        status_code=500,
        request_id=request_id
    )
    
    logger.exception(
        f"Unexpected error: {exc}",
        extra={
            "request_id": request_id,
            "exception_type": type(exc).__name__
        }
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response
    )

