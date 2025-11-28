"""
Trust Guard Logging Configuration

Structured logging for Trust Guard service with context tracking, trace context, and performance data
"""

import logging
import logging.config
import sys
import time
import uuid
from typing import Any, Dict, Optional, Union
from contextvars import ContextVar
from pythonjsonlogger import jsonlogger

# Context variables for trace context
trace_id_var: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
span_id_var: ContextVar[Optional[str]] = ContextVar('span_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)


def setup_logging(
    level: str = "INFO",
    format_type: str = "json",
    log_to_file: bool = False
) -> logging.Logger:
    """
    Set up structured logging for Trust Guard service.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        format_type: Log format ('json' or 'text')
        log_to_file: Whether to log to file in addition to console

    Returns:
        Configured logger instance for Trust Guard
    """

    # Configure log level
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Base configuration
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {},
        'handlers': {},
        'root': {
            'level': numeric_level,
            'handlers': ['console']
        },
        'loggers': {
            'trustguard': {
                'level': numeric_level,
                'handlers': ['console'],
                'propagate': False
            }
        }
    }

    # Configure formatters
    if format_type == 'json':
        config['formatters']['json'] = {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s %(trace_id)s %(span_id)s %(user_id)s %(request_id)s'
        }
        formatter_name = 'json'
        formatter_class = 'pythonjsonlogger.jsonlogger.JsonFormatter'
    else:
        config['formatters']['text'] = {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s [trace_id=%(trace_id)s span_id=%(span_id)s user_id=%(user_id)s request_id=%(request_id)s]'
        }
        formatter_name = 'text'
        formatter_class = 'logging.Formatter'

    # Console handler
    config['handlers']['console'] = {
        'class': 'logging.StreamHandler',
        'level': numeric_level,
        'formatter': formatter_name,
        'stream': sys.stdout
    }

    # File handler (optional)
    if log_to_file:
        config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'level': numeric_level,
            'formatter': formatter_name,
            'filename': 'trustguard.log',
            'mode': 'a'
        }
        config['root']['handlers'].append('file')
        config['loggers']['trustguard']['handlers'].append('file')

    # Apply configuration
    logging.config.dictConfig(config)

    # Create and return Trust Guard logger
    logger = logging.getLogger('trustguard')
    logger.info("Trust Guard logging initialized",
                extra={'level': level, 'format': format_type, 'file_logging': log_to_file})

    return logger


def set_trace_context(
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None
) -> None:
    """Set trace context variables."""
    # Always set the values - None will clear the context
    trace_id_var.set(trace_id)
    span_id_var.set(span_id)
    user_id_var.set(user_id)
    request_id_var.set(request_id)


def get_trace_context() -> Dict[str, Optional[str]]:
    """Get current trace context."""
    return {
        'trace_id': trace_id_var.get(),
        'span_id': span_id_var.get(),
        'user_id': user_id_var.get(),
        'request_id': request_id_var.get()
    }


def generate_trace_id() -> str:
    """Generate a new trace ID."""
    return str(uuid.uuid4())


def generate_span_id() -> str:
    """Generate a new span ID."""
    return str(uuid.uuid4())[:8]


def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    **context
) -> None:
    """
    Log a message with additional context information.

    Args:
        logger: Logger instance to use
        level: Log level (debug, info, warning, error)
        message: Log message
        **context: Additional key-value pairs to include in log
    """
    log_method = getattr(logger, level.lower(), logger.info)
    
    # Get trace context
    trace_context = get_trace_context()
    
    # Merge with additional context
    full_context = {**trace_context, **context}
    
    # Add performance data if available
    if 'duration' not in full_context and 'start_time' in full_context:
        full_context['duration'] = time.time() - full_context['start_time']
    
    log_method(message, extra=full_context)


def log_performance(
    logger: logging.Logger,
    operation: str,
    duration: float,
    **metrics
) -> None:
    """
    Log performance metrics for an operation.

    Args:
        logger: Logger instance to use
        operation: Operation name
        duration: Operation duration in seconds
        **metrics: Additional performance metrics
    """
    performance_data = {
        'operation': operation,
        'duration_seconds': duration,
        'duration_ms': duration * 1000,
        'timestamp': time.time(),
        **metrics
    }
    
    log_with_context(logger, 'info', f"Performance: {operation}", **performance_data)


def log_security_event(
    logger: logging.Logger,
    event_type: str,
    severity: str = "medium",
    **details
) -> None:
    """
    Log security-related events.

    Args:
        logger: Logger instance to use
        event_type: Type of security event
        severity: Event severity (low, medium, high, critical)
        **details: Additional event details
    """
    security_data = {
        'event_type': event_type,
        'severity': severity,
        'timestamp': time.time(),
        **details
    }
    
    log_level = 'warning' if severity in ['high', 'critical'] else 'info'
    log_with_context(logger, log_level, f"Security event: {event_type}", **security_data)


def log_business_event(
    logger: logging.Logger,
    event_type: str,
    **details
) -> None:
    """
    Log business-related events.

    Args:
        logger: Logger instance to use
        event_type: Type of business event
        **details: Additional event details
    """
    business_data = {
        'event_type': event_type,
        'timestamp': time.time(),
        **details
    }
    
    log_with_context(logger, 'info', f"Business event: {event_type}", **business_data)


class PerformanceLogger:
    """Context manager for logging operation performance."""
    
    def __init__(self, logger: logging.Logger, operation: str, **metrics):
        self.logger = logger
        self.operation = operation
        self.metrics = metrics
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        
        performance_data = {
            'duration_seconds': duration,
            'duration_ms': duration * 1000,
            'success': exc_type is None,
            **self.metrics
        }
        
        if exc_type:
            performance_data['error_type'] = exc_type.__name__
            performance_data['error_message'] = str(exc_val) if exc_val else None
        
        log_performance(self.logger, self.operation, duration, **performance_data)
