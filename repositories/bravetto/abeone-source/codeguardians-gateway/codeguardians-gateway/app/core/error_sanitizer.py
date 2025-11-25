"""
Error Message Sanitization Module

Sanitizes error messages in production to prevent information disclosure.
"""

import os
from typing import Any, Dict
from app.core.config import get_settings

settings = get_settings()


def sanitize_error_message(error: Exception, message: str) -> str:
    """
    Sanitize error message for production.
    
    Args:
        error: The exception that occurred
        message: The error message to sanitize
        
    Returns:
        Sanitized error message
    """
    # In production, return generic messages
    if settings.ENVIRONMENT == "production" and not settings.DEBUG:
        # Generic error messages for production
        error_type = type(error).__name__
        
        # Map specific errors to generic messages
        generic_messages = {
            "DatabaseError": "Database operation failed",
            "ConnectionError": "Service temporarily unavailable",
            "TimeoutError": "Request timeout",
            "ValidationError": "Invalid input provided",
            "AuthenticationError": "Authentication failed",
            "AuthorizationError": "Access denied",
            "NotFoundError": "Resource not found",
            "RateLimitError": "Rate limit exceeded",
        }
        
        return generic_messages.get(error_type, "An error occurred")
    
    # In development/debug mode, return full message
    return str(message)


def sanitize_stack_trace(traceback: Any) -> str:
    """
    Sanitize stack trace for production.
    
    Args:
        traceback: Stack trace object
        
    Returns:
        Sanitized stack trace or empty string
    """
    if settings.ENVIRONMENT == "production" and not settings.DEBUG:
        # Don't expose stack traces in production
        return ""
    
    # In development, return full stack trace
    import traceback as tb
    return "".join(tb.format_exception(type(traceback), traceback, traceback.__traceback__))


def sanitize_error_response(error: Exception, detail: str = None) -> Dict[str, Any]:
    """
    Create sanitized error response.
    
    Args:
        error: The exception
        detail: Optional detail message
        
    Returns:
        Sanitized error response dictionary
    """
    message = detail or str(error)
    sanitized_message = sanitize_error_message(error, message)
    
    response = {
        "error": sanitized_message,
        "error_type": type(error).__name__ if settings.DEBUG else "Error"
    }
    
    # Only include stack trace in debug mode
    if settings.DEBUG:
        import traceback
        response["traceback"] = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    
    return response

