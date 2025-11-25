"""
Standardized Error Response Format

PRODUCTION HARDENING:
- Consistent error response structure
- error_code, timestamp, request_id in all responses
- Backward compatible with existing exceptions

SAFETY: All errors follow consistent format
VERIFY: All error responses include required fields
"""

import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from app.core.exceptions import BaseAPIException


def format_error_response(
    error_code: str,
    message: str,
    status_code: int = 500,
    request_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    timestamp: Optional[float] = None
) -> Dict[str, Any]:
    """
    Format standardized error response.
    
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
    
    return {
        "error": {
            "error_code": error_code,
            "message": message,
            "timestamp": timestamp,
            "request_id": request_id or str(uuid.uuid4())
        },
        "details": details or {}
    }


def format_exception_response(
    exc: BaseAPIException,
    request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Format BaseAPIException as standardized error response.
    
    Args:
        exc: BaseAPIException instance
        request_id: Request ID for correlation
    
    Returns:
        Standardized error response dict
    """
    return format_error_response(
        error_code=exc.error_code or "API_ERROR",
        message=exc.message,
        status_code=exc.status_code,
        request_id=request_id,
        details=exc.details
    )

