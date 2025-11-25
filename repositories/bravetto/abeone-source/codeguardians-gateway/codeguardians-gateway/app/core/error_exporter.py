"""
Error Exporter - Standardized Error Handling and Export

FULL CAVALRY: Error handling excellence
- Standardized error export
- Comprehensive error logging
- Error tracking and metrics
- Simplified error handling
"""

import traceback
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import json

from app.core.error_response import ErrorResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)


class ErrorExporter:
    """
    Standardized error exporter for all failure points.
    
    FULL CAVALRY: Excellence in error handling
    """
    
    @staticmethod
    def export_error(
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> ErrorResponse:
        """
        Export error in standardized format.
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
            error_code: Specific error code
            request_id: Request ID for tracing
            user_id: User ID if available
            
        Returns:
            Standardized ErrorResponse
        """
        # Extract error code from exception if available
        if not error_code:
            error_code = getattr(error, 'error_code', None) or type(error).__name__.upper()
        
        # Build error message
        error_message = str(error) if str(error) else type(error).__name__
        
        # Get stack trace for logging (not for user)
        stack_trace = traceback.format_exc()
        
        # Log error with full context
        logger.error(
            f"Error exported: {error_code}",
            extra={
                "error_type": type(error).__name__,
                "error_message": error_message,
                "error_code": error_code,
                "request_id": request_id,
                "user_id": user_id,
                "context": context or {},
                "stack_trace": stack_trace
            }
        )
        
        # Build standardized error response
        return ErrorResponse(
            error_code=error_code,
            message=error_message,
            timestamp=datetime.now(timezone.utc).isoformat(),
            request_id=request_id,
            details=context or {}
        )
    
    @staticmethod
    def export_error_dict(
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export error as dictionary.
        
        Returns:
            Dictionary representation of error
        """
        error_response = ErrorExporter.export_error(
            error=error,
            context=context,
            error_code=error_code,
            request_id=request_id,
            user_id=user_id
        )
        
        return {
            "error_code": error_response.error_code,
            "message": error_response.message,
            "timestamp": error_response.timestamp,
            "request_id": error_response.request_id,
            "details": error_response.details
        }
    
    @staticmethod
    def handle_and_export(
        func,
        context: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None,
        default_return: Any = None
    ) -> Any:
        """
        Wrapper to handle and export errors.
        
        Args:
            func: Function to execute
            context: Additional context
            error_code: Error code if function fails
            request_id: Request ID
            user_id: User ID
            default_return: Default return value on error
            
        Returns:
            Function result or default_return on error
        """
        try:
            return func()
        except Exception as e:
            ErrorExporter.export_error(
                error=e,
                context=context,
                error_code=error_code,
                request_id=request_id,
                user_id=user_id
            )
            return default_return
    
    @staticmethod
    async def handle_and_export_async(
        func,
        context: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None,
        default_return: Any = None
    ) -> Any:
        """
        Async wrapper to handle and export errors.
        
        Args:
            func: Async function to execute
            context: Additional context
            error_code: Error code if function fails
            request_id: Request ID
            user_id: User ID
            default_return: Default return value on error
            
        Returns:
            Function result or default_return on error
        """
        try:
            if callable(func):
                return await func()
            else:
                return await func
        except Exception as e:
            ErrorExporter.export_error(
                error=e,
                context=context,
                error_code=error_code,
                request_id=request_id,
                user_id=user_id
            )
            return default_return


# Global error exporter instance
_error_exporter: Optional[ErrorExporter] = None


def get_error_exporter() -> ErrorExporter:
    """Get global error exporter instance."""
    global _error_exporter
    if _error_exporter is None:
        _error_exporter = ErrorExporter()
    return _error_exporter

