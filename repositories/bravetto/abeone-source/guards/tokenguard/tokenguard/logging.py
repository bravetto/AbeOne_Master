# tokenguard/logging.py
"""
Structured logging configuration for TokenGuard microservice.
"""

import logging
import sys
import json
from datetime import datetime, timezone
from typing import Optional, Any
from .config import config


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self: Any, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)

        return json.dumps(log_entry)


def setup_logging() -> logging.Logger:
    """Configure structured logging for the application with error handling."""
    try:
        # Remove existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)

        if config.log_format.lower() == "json":
            console_handler.setFormatter(JSONFormatter())
        else:
            # Standard format for development
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            console_handler.setFormatter(formatter)

        # Configure root logger
        root_logger.addHandler(console_handler)

        # Validate and set log level
        try:
            log_level = getattr(logging, config.log_level.upper())
            root_logger.setLevel(log_level)
        except AttributeError:
            # Fallback to INFO if invalid log level
            root_logger.setLevel(logging.INFO)
            root_logger.warning(f"Invalid log level '{config.log_level}', falling back to INFO")

        # Configure specific loggers
        logging.getLogger("uvicorn.access").setLevel(logging.INFO)
        logging.getLogger("uvicorn.error").setLevel(logging.INFO)

        # Create tokenguard logger
        tokenguard_logger = logging.getLogger("tokenguard")
        tokenguard_logger.info("Logging system initialized successfully")

        return tokenguard_logger

    except Exception as e:
        # Fallback logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            stream=sys.stdout,
        )
        logger = logging.getLogger("tokenguard")
        logger.error(f"Failed to setup structured logging, using basic configuration: {e}")
        return logger


def log_with_context(logger: logging.Logger, level: str, message: str, **context) -> None:
    """Log message with additional context fields and error handling."""
    try:
        # Validate level
        numeric_level = getattr(logging, level.upper(), None)
        if numeric_level is None:
            logger.warning(f"Invalid log level '{level}', using INFO")
            numeric_level = logging.INFO

        record = logging.LogRecord(
            name=logger.name,
            level=numeric_level,
            pathname="",
            lineno=0,
            msg=message,
            args=(),
            exc_info=None,
        )

        # Safely add context fields
        sanitized_context = {}
        for key, value in context.items():
            try:
                # Ensure context values are JSON serializable
                json.dumps(value)
                sanitized_context[key] = value
            except (TypeError, ValueError):
                sanitized_context[key] = str(value)

        record.extra_fields = sanitized_context  # type: ignore
        logger.handle(record)

    except Exception as e:
        # Fallback to simple logging if context logging fails
        logger.error(f"Context logging failed: {e}")
        logger.log(getattr(logging, level.upper(), logging.INFO), message)


def log_error_with_traceback(
    logger: logging.Logger, message: str, exception: Exception, **context
) -> None:
    """Log error with full traceback and context."""
    try:
        import traceback

        error_context = {
            "error_type": type(exception).__name__,
            "error_message": str(exception),
            "traceback": traceback.format_exc(),
            **context,
        }

        log_with_context(logger, "ERROR", message, **error_context)

    except Exception as e:
        # Ultimate fallback
        logger.error(f"Failed to log error with traceback: {e}")
        logger.error(f"Original error: {message} - {exception}")


def get_request_logger(request_id: Optional[str] = None) -> logging.Logger:
    """Get a logger with request context."""
    logger = logging.getLogger("tokenguard.request")
    if request_id:
        # Add request ID to all subsequent logs from this logger
        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs) -> Any:  # type: ignore
            record = old_factory(*args, **kwargs)
            if not hasattr(record, "extra_fields"):
                record.extra_fields = {}  # type: ignore
            record.extra_fields["request_id"] = request_id  # type: ignore
            return record

        logging.setLogRecordFactory(record_factory)

    return logger
