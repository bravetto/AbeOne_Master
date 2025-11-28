"""
SDK Exceptions

Custom exceptions for SDK operations.
"""


class HyperVectorError(Exception):
    """Base exception for HyperVector SDK."""
    pass


class HyperVectorAPIError(HyperVectorError):
    """API error exception."""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


class HyperVectorNotFoundError(HyperVectorAPIError):
    """Vector not found exception."""
    pass


class HyperVectorValidationError(HyperVectorError):
    """Validation error exception."""
    pass

