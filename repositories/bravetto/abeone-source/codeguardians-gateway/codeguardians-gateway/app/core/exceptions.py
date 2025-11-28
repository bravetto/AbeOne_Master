"""
Custom exceptions for the application.

This module defines custom exception classes for better error handling
and API responses.
"""

from typing import Optional, Dict, Any, List


class BaseAPIException(Exception):
    """Base exception class for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.error_code = error_code
        super().__init__(self.message)

        # Log the error when created
        import logging
        logger = logging.getLogger(self.__class__.__name__)
        log_level = logging.WARNING if status_code < 500 else logging.ERROR
        logger.log(log_level, f"{self.error_code or 'API_ERROR'}: {message}",
                  extra={"status_code": status_code, "details": self.details, "error_code": self.error_code})


class ValidationError(BaseAPIException):
    """Exception raised for validation errors."""

    def __init__(
        self,
        message: str = "Validation error",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "VALIDATION_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=422,
            details=details,
            error_code=error_code
        )


class AuthenticationError(BaseAPIException):
    """Exception raised for authentication errors."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AUTHENTICATION_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=401,
            details=details,
            error_code=error_code
        )


class AuthorizationError(BaseAPIException):
    """Exception raised for authorization errors."""
    
    def __init__(
        self,
        message: str = "Access denied",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AUTHORIZATION_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=403,
            details=details,
            error_code=error_code
        )


class NotFoundError(BaseAPIException):
    """Exception raised when a resource is not found."""
    
    def __init__(
        self,
        message: str = "Resource not found",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "NOT_FOUND"
    ):
        super().__init__(
            message=message,
            status_code=404,
            details=details,
            error_code=error_code
        )


class ConflictError(BaseAPIException):
    """Exception raised for resource conflicts."""
    
    def __init__(
        self,
        message: str = "Resource conflict",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "CONFLICT"
    ):
        super().__init__(
            message=message,
            status_code=409,
            details=details,
            error_code=error_code
        )


class InternalServerError(BaseAPIException):
    """Exception raised for internal server errors."""
    
    def __init__(
        self,
        message: str = "Internal server error",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "INTERNAL_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=500,
            details=details,
            error_code=error_code
        )


class DatabaseError(BaseAPIException):
    """Exception raised for database errors."""
    
    def __init__(
        self,
        message: str = "Database error",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "DATABASE_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=500,
            details=details,
            error_code=error_code
        )


class ExternalServiceError(BaseAPIException):
    """Exception raised for external service errors."""
    
    def __init__(
        self,
        message: str = "External service error",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "EXTERNAL_SERVICE_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=502,
            details=details,
            error_code=error_code
        )


class RateLimitError(BaseAPIException):
    """Exception raised for rate limit exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "RATE_LIMIT_EXCEEDED"
    ):
        super().__init__(
            message=message,
            status_code=429,
            details=details,
            error_code=error_code
        )


class FileUploadError(BaseAPIException):
    """Exception raised for file upload errors."""
    
    def __init__(
        self,
        message: str = "File upload error",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "FILE_UPLOAD_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=400,
            details=details,
            error_code=error_code
        )


class EmailError(BaseAPIException):
    """Exception raised for email sending errors."""
    
    def __init__(
        self,
        message: str = "Email sending error",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "EMAIL_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=500,
            details=details,
            error_code=error_code
        )


class EmailRequiredError(ValidationError):
    """Exception raised when email is required but missing."""
    
    def __init__(
        self,
        message: str = "Email address is required",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "EMAIL_REQUIRED"
    ):
        super().__init__(
            message=message,
            details=details,
            error_code=error_code
        )
        # EmailRequiredError always uses 400 status code
        self.status_code = 400


class CacheError(BaseAPIException):
    """Exception raised for cache errors."""
    
    def __init__(
        self,
        message: str = "Cache error",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "CACHE_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=500,
            details=details,
            error_code=error_code
        )


class ConfigurationError(BaseAPIException):
    """Exception raised for configuration errors."""
    
    def __init__(
        self,
        message: str = "Configuration error",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "CONFIGURATION_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=500,
            details=details,
            error_code=error_code
        )


class BusinessLogicError(BaseAPIException):
    """Exception raised for business logic errors."""
    
    def __init__(
        self,
        message: str = "Business logic error",
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "BUSINESS_LOGIC_ERROR"
    ):
        super().__init__(
            message=message,
            status_code=400,
            details=details,
            error_code=error_code
        )


class ValidationFieldError:
    """Represents a field validation error."""
    
    def __init__(self, field: str, message: str, code: Optional[str] = None):
        self.field = field
        self.message = message
        self.code = code or "INVALID"
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {
            "field": self.field,
            "message": self.message,
            "code": self.code
        }


class ValidationErrors(ValidationError):
    """Exception for multiple validation errors."""
    
    def __init__(
        self,
        errors: List[ValidationFieldError],
        message: str = "Validation errors"
    ):
        self.errors = errors
        details = {
            "errors": [error.to_dict() for error in errors]
        }
        super().__init__(
            message=message,
            details=details,
            error_code="VALIDATION_ERRORS"
        )


class GuardServiceError(BaseAPIException):
    """Exception raised for guard service errors."""
    
    def __init__(self, message: str = "Guard service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=502,
            details=details,
            error_code="GUARD_SERVICE_ERROR"
        )


class ServiceUnavailableError(BaseAPIException):
    """Exception raised when a service is unavailable."""
    
    def __init__(self, message: str = "Service unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=503,
            details=details,
            error_code="SERVICE_UNAVAILABLE"
        )


# Stripe-specific exceptions
class StripeError(ExternalServiceError):
    """Exception raised for Stripe API errors."""

    def __init__(self, message: str = "Stripe API error", details: Optional[Dict[str, Any]] = None, stripe_error_code: Optional[str] = None):
        super().__init__(
            message=message,
            details=details or {},
            error_code="STRIPE_ERROR"
        )
        self.stripe_error_code = stripe_error_code

    @classmethod
    def from_stripe_error(cls, stripe_error) -> "StripeError":
        """Create StripeError from stripe.error.StripeError."""
        error_details = {
            "type": getattr(stripe_error, 'type', 'unknown'),
            "code": getattr(stripe_error, 'code', None),
            "param": getattr(stripe_error, 'param', None),
            "message": str(stripe_error)
        }

        # Map Stripe error types to appropriate HTTP status codes
        status_mapping = {
            'card_error': 402,
            'invalid_request_error': 400,
            'api_error': 502,
            'authentication_error': 401,
            'rate_limit_error': 429,
            'connection_error': 502,
            'idempotency_error': 400,
        }

        status_code = status_mapping.get(error_details.get('type'), 500)

        return cls(
            message=f"Stripe error: {str(stripe_error)}",
            details=error_details,
            stripe_error_code=error_details.get('code')
        )


class StripeWebhookError(StripeError):
    """Exception raised for Stripe webhook processing errors."""

    def __init__(self, message: str = "Stripe webhook processing error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            details=details,
            error_code="STRIPE_WEBHOOK_ERROR"
        )


class StripeCustomerError(StripeError):
    """Exception raised for Stripe customer operations."""

    def __init__(self, message: str = "Stripe customer error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            details=details,
            error_code="STRIPE_CUSTOMER_ERROR"
        )


class StripeSubscriptionError(StripeError):
    """Exception raised for Stripe subscription operations."""

    def __init__(self, message: str = "Stripe subscription error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            details=details,
            error_code="STRIPE_SUBSCRIPTION_ERROR"
        )


class StripePaymentError(StripeError):
    """Exception raised for Stripe payment operations."""

    def __init__(self, message: str = "Stripe payment error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            details=details,
            error_code="STRIPE_PAYMENT_ERROR"
        )


# Clerk-specific exceptions
class ClerkError(ExternalServiceError):
    """Exception raised for Clerk API errors."""

    def __init__(self, message: str = "Clerk API error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            details=details,
            error_code="CLERK_ERROR"
        )


class ClerkTokenError(AuthenticationError):
    """Exception raised for Clerk token validation errors."""

    def __init__(self, message: str = "Clerk token validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            details=details,
            error_code="CLERK_TOKEN_ERROR"
        )


class ClerkWebhookError(ClerkError):
    """Exception raised for Clerk webhook processing errors."""

    def __init__(self, message: str = "Clerk webhook processing error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            details=details,
            error_code="CLERK_WEBHOOK_ERROR"
        )


class ClerkJWKSFetchError(ClerkError):
    """Exception raised when Clerk JWKS cannot be fetched."""

    def __init__(self, message: str = "Failed to fetch Clerk JWKS", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            details=details,
            error_code="CLERK_JWKS_FETCH_ERROR"
        )


# Circuit Breaker and Retry Exceptions
class CircuitBreakerOpenError(ExternalServiceError):
    """Exception raised when circuit breaker is open."""

    def __init__(self, service_name: str, message: str = None, details: Optional[Dict[str, Any]] = None):
        if message is None:
            message = f"Circuit breaker is open for service: {service_name}"
        super().__init__(
            message=message,
            status_code=503,
            details=details or {"service": service_name},
            error_code="CIRCUIT_BREAKER_OPEN"
        )


class RetryExhaustedError(ExternalServiceError):
    """Exception raised when all retry attempts are exhausted."""

    def __init__(self, service_name: str, attempts: int, message: str = None, details: Optional[Dict[str, Any]] = None):
        if message is None:
            message = f"All {attempts} retry attempts exhausted for service: {service_name}"
        super().__init__(
            message=message,
            status_code=503,
            details=details or {"service": service_name, "attempts": attempts},
            error_code="RETRY_EXHAUSTED"
        )