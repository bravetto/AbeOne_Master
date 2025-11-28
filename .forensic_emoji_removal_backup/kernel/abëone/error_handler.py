"""
Error Handler - Comprehensive Error Handling Framework

Implements comprehensive error handling framework with structured error types and recovery mechanisms.

Pattern: ERROR × HANDLER × RECOVERY × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import traceback
from error_types import AbeoneError, ErrorSeverity, ErrorCategory


class RecoveryStrategy(Enum):
    """Error recovery strategies."""
    RETRY = "retry"
    FALLBACK = "fallback"
    IGNORE = "ignore"
    FAIL = "fail"
    ESCALATE = "escalate"


@dataclass
class ErrorHandlerConfig:
    """Error handler configuration."""
    max_retries: int = 3
    retry_delay: float = 1.0
    enable_logging: bool = True
    enable_recovery: bool = True
    recovery_strategies: Dict[str, RecoveryStrategy] = field(default_factory=dict)


@dataclass
class ErrorLogEntry:
    """Error log entry."""
    error: AbeoneError
    timestamp: datetime
    context: Dict[str, Any]
    stack_trace: Optional[str] = None
    recovered: bool = False
    recovery_strategy: Optional[RecoveryStrategy] = None


class ErrorHandler:
    """
    Error Handler.
    
    Responsibilities:
    - Handle errors
    - Log errors
    - Attempt error recovery
    - Provide error context
    """
    
    def __init__(self, config: Optional[ErrorHandlerConfig] = None):
        """Initialize error handler."""
        self.config = config or ErrorHandlerConfig()
        self.error_log: List[ErrorLogEntry] = []
        self.max_log_size: int = 1000
        self.recovery_handlers: Dict[str, Callable[[AbeoneError], Any]] = {}
    
    def register_recovery_handler(self, error_code: str, handler: Callable[[AbeoneError], Any]) -> None:
        """
        Register a recovery handler for a specific error code.
        
        Args:
            error_code: Error code
            handler: Recovery handler function
        """
        self.recovery_handlers[error_code] = handler
    
    def handle_error(self, error: AbeoneError, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Handle an error.
        
        Args:
            error: Error to handle
            context: Optional context
        
        Returns:
            Recovery result if recovery attempted, None otherwise
        """
        # Log error
        if self.config.enable_logging:
            self._log_error(error, context)
        
        # Attempt recovery
        if self.config.enable_recovery:
            recovery_result = self._attempt_recovery(error, context)
            if recovery_result is not None:
                return recovery_result
        
        # If no recovery, escalate or fail
        return self._escalate_error(error, context)
    
    def _log_error(self, error: AbeoneError, context: Optional[Dict[str, Any]]) -> None:
        """Log an error."""
        stack_trace = traceback.format_exc() if error.severity == ErrorSeverity.CRITICAL else None
        
        log_entry = ErrorLogEntry(
            error=error,
            timestamp=datetime.now(),
            context=context or {},
            stack_trace=stack_trace
        )
        
        self.error_log.append(log_entry)
        
        # Trim log if too large
        if len(self.error_log) > self.max_log_size:
            self.error_log.pop(0)
        
        # Print error based on severity
        if error.severity == ErrorSeverity.CRITICAL:
            print(f"❌ CRITICAL ERROR: {error}")
            if stack_trace:
                print(stack_trace)
        elif error.severity == ErrorSeverity.HIGH:
            print(f"⚠️ HIGH ERROR: {error}")
        elif error.severity == ErrorSeverity.MEDIUM:
            print(f"⚠️ ERROR: {error}")
        else:
            print(f"ℹ️ INFO: {error}")
    
    def _attempt_recovery(self, error: AbeoneError, context: Optional[Dict[str, Any]]) -> Optional[Any]:
        """Attempt to recover from an error."""
        # Check for custom recovery handler
        if error.error_code in self.recovery_handlers:
            try:
                handler = self.recovery_handlers[error.error_code]
                return handler(error)
            except Exception as e:
                print(f"⚠️ Recovery handler failed: {e}")
        
        # Check for configured recovery strategy
        recovery_strategy = self.config.recovery_strategies.get(
            error.error_code,
            RecoveryStrategy.FAIL
        )
        
        if recovery_strategy == RecoveryStrategy.RETRY:
            return self._retry_operation(error, context)
        elif recovery_strategy == RecoveryStrategy.FALLBACK:
            return self._fallback_operation(error, context)
        elif recovery_strategy == RecoveryStrategy.IGNORE:
            return None
        
        return None
    
    def _retry_operation(self, error: AbeoneError, context: Optional[Dict[str, Any]]) -> Optional[Any]:
        """Retry an operation."""
        # This would be implemented based on the operation context
        # For now, just return None
        return None
    
    def _fallback_operation(self, error: AbeoneError, context: Optional[Dict[str, Any]]) -> Optional[Any]:
        """Fallback operation."""
        # This would be implemented based on the operation context
        # For now, just return None
        return None
    
    def _escalate_error(self, error: AbeoneError, context: Optional[Dict[str, Any]]) -> None:
        """Escalate an error."""
        if error.severity == ErrorSeverity.CRITICAL:
            # Critical errors should be escalated
            print(f"🚨 ESCALATING CRITICAL ERROR: {error}")
        elif error.severity == ErrorSeverity.HIGH:
            # High severity errors may need escalation
            print(f"⚠️ ESCALATING HIGH ERROR: {error}")
    
    def get_error_log(self, limit: int = 100) -> List[ErrorLogEntry]:
        """
        Get error log entries.
        
        Args:
            limit: Maximum number of entries to return
        
        Returns:
            List of error log entries
        """
        return self.error_log[-limit:]
    
    def get_errors_by_category(self, category: ErrorCategory) -> List[ErrorLogEntry]:
        """
        Get errors by category.
        
        Args:
            category: Error category
        
        Returns:
            List of error log entries
        """
        return [entry for entry in self.error_log if entry.error.category == category]
    
    def get_errors_by_severity(self, severity: ErrorSeverity) -> List[ErrorLogEntry]:
        """
        Get errors by severity.
        
        Args:
            severity: Error severity
        
        Returns:
            List of error log entries
        """
        return [entry for entry in self.error_log if entry.error.severity == severity]
    
    def clear_error_log(self) -> None:
        """Clear error log."""
        self.error_log.clear()

