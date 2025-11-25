"""
Error Types - Structured Error Types

Defines structured error types for the AbëONE system.

Pattern: ERROR × TYPES × STRUCTURE × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories."""
    VALIDATION = "validation"
    MODULE = "module"
    PIPELINE = "pipeline"
    NETWORK = "network"
    TIMEOUT = "timeout"
    CONFIGURATION = "configuration"
    SYSTEM = "system"
    UNKNOWN = "unknown"


@dataclass
class AbeoneError(Exception):
    """Base error class for AbëONE system."""
    error_code: str
    message: str
    category: ErrorCategory
    severity: ErrorSeverity
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    context: Optional[Dict[str, Any]] = None
    
    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context
        }


class ValidationError(AbeoneError):
    """Validation error."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="VALIDATION_ERROR",
            message=message,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.MEDIUM,
            details=details or {}
        )


class ModuleError(AbeoneError):
    """Module error."""
    def __init__(self, module_id: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="MODULE_ERROR",
            message=f"[{module_id}] {message}",
            category=ErrorCategory.MODULE,
            severity=ErrorSeverity.HIGH,
            details=details or {},
            context={"module_id": module_id}
        )


class PipelineError(AbeoneError):
    """Pipeline error."""
    def __init__(self, pipeline_id: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="PIPELINE_ERROR",
            message=f"[{pipeline_id}] {message}",
            category=ErrorCategory.PIPELINE,
            severity=ErrorSeverity.HIGH,
            details=details or {},
            context={"pipeline_id": pipeline_id}
        )


class NetworkError(AbeoneError):
    """Network error."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="NETWORK_ERROR",
            message=message,
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.MEDIUM,
            details=details or {}
        )


class TimeoutError(AbeoneError):
    """Timeout error."""
    def __init__(self, operation: str, timeout: float, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="TIMEOUT_ERROR",
            message=f"Operation '{operation}' timed out after {timeout}s",
            category=ErrorCategory.TIMEOUT,
            severity=ErrorSeverity.MEDIUM,
            details=details or {},
            context={"operation": operation, "timeout": timeout}
        )


class ConfigurationError(AbeoneError):
    """Configuration error."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="CONFIGURATION_ERROR",
            message=message,
            category=ErrorCategory.CONFIGURATION,
            severity=ErrorSeverity.HIGH,
            details=details or {}
        )


class SystemError(AbeoneError):
    """System error."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="SYSTEM_ERROR",
            message=message,
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.CRITICAL,
            details=details or {}
        )

