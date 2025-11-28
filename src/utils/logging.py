"""
Logging Utilities

Consistent logging configuration and utilities across modules.

Pattern: LOGGING × CONSISTENCY × ATOMIC × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

import logging
import sys
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime


class LoggerConfig:
    """
    Logger configuration manager.
    
    Provides consistent logging setup across modules with:
    - Standardized format
    - Multiple handlers (console, file)
    - Configurable levels
    - Structured logging support
    
    ASSUMES:
    - Log directory is writable (if file logging enabled)
    - Logger names follow module hierarchy
    
    VERIFY:
    - Logger created successfully
    - Handlers configured correctly
    - Log levels set appropriately
    
    FAILS:
    - If log directory not writable
    - If invalid log level specified
    """
    
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    @staticmethod
    def get_logger(
        name: str,
        level: Optional[int] = None,
        format_string: Optional[str] = None,
        filepath: Optional[Path] = None,
        file_level: Optional[int] = None
    ) -> logging.Logger:
        """
        Get or create logger with configuration.
        
        SAFETY: Prevents duplicate handlers
        ASSUMES: name is valid logger name, level is valid log level
        VERIFY: Logger configured with requested handlers
        
        Args:
            name: Logger name (typically __name__)
            level: Console log level (default: INFO)
            format_string: Custom format string (default: standard format)
            filepath: Optional file path for file handler
            file_level: Optional file log level (default: same as console)
            
        Returns:
            Configured Logger instance
        """
        logger = logging.getLogger(name)
        
        # SAFETY: Prevent duplicate handlers
        if logger.handlers:
            return logger
        
        # SAFETY: Set log level
        if level is None:
            level = logging.INFO
        
        logger.setLevel(level)
        
        # SAFETY: Configure format
        if format_string is None:
            format_string = LoggerConfig.DEFAULT_FORMAT
        
        formatter = logging.Formatter(
            format_string,
            datefmt=LoggerConfig.DEFAULT_DATE_FORMAT
        )
        
        # SAFETY: Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # SAFETY: File handler (if specified)
        if filepath is not None:
            file_level = file_level or level
            
            # SAFETY: Create parent directories
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(filepath, encoding='utf-8')
            file_handler.setLevel(file_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    @staticmethod
    def setup_module_logger(
        module_name: str,
        level: Optional[int] = None,
        log_dir: Optional[Path] = None
    ) -> logging.Logger:
        """
        Setup logger for a module with standard configuration.
        
        SAFETY: Creates log directory if needed
        ASSUMES: module_name is valid module path
        VERIFY: Logger configured with console and optional file handler
        
        Args:
            module_name: Module name (typically __name__)
            level: Log level (default: INFO)
            log_dir: Optional directory for log files
            
        Returns:
            Configured Logger instance
        """
        filepath = None
        if log_dir is not None:
            # SAFETY: Create log file path
            log_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d')
            log_filename = f"{module_name.replace('.', '_')}_{timestamp}.log"
            filepath = log_dir / log_filename
        
        return LoggerConfig.get_logger(
            name=module_name,
            level=level,
            filepath=filepath
        )


def get_logger(
    name: str,
    level: Optional[int] = None
) -> logging.Logger:
    """
    Get logger instance with default configuration.
    
    Convenience function for quick logger setup.
    
    SAFETY: Prevents duplicate handlers
    ASSUMES: name is valid logger name
    VERIFY: Logger configured with console handler
    
    Args:
        name: Logger name (typically __name__)
        level: Log level (default: INFO)
        
    Returns:
        Logger instance
    """
    return LoggerConfig.get_logger(name=name, level=level)


def setup_logger(
    name: str,
    level: Optional[int] = None,
    format_string: Optional[str] = None,
    filepath: Optional[Path] = None
) -> logging.Logger:
    """
    Setup logger with custom configuration.
    
    SAFETY: Creates parent directories for file handler
    ASSUMES: name is valid logger name, filepath is writable
    VERIFY: Logger configured successfully
    
    Args:
        name: Logger name (typically __name__)
        level: Log level (default: INFO)
        format_string: Custom format string
        filepath: Optional file path for file handler
        
    Returns:
        Logger instance
    """
    return LoggerConfig.get_logger(
        name=name,
        level=level,
        format_string=format_string,
        filepath=filepath
    )


class StructuredLogger:
    """
    Structured logging wrapper for consistent log formatting.
    
    Provides structured logging with context support:
    - Contextual fields
    - Consistent formatting
    - Easy context propagation
    
    ASSUMES:
    - Logger is properly configured
    - Context data is JSON-serializable
    
    VERIFY:
    - Structured logs include context
    - Context propagated correctly
    """
    
    def __init__(self, logger: logging.Logger):
        """
        Initialize structured logger.
        
        Args:
            logger: Base logger instance
        """
        self.logger = logger
        self.context: Dict[str, Any] = {}
    
    def add_context(self, **kwargs: Any) -> None:
        """
        Add context fields to logger.
        
        Args:
            **kwargs: Context key-value pairs
        """
        self.context.update(kwargs)
    
    def clear_context(self) -> None:
        """Clear all context fields."""
        self.context.clear()
    
    def _format_message(self, message: str, **kwargs: Any) -> str:
        """
        Format message with context.
        
        SAFETY: Handles non-serializable context values
        ASSUMES: message is string, kwargs are serializable
        VERIFY: Returns formatted string
        
        Args:
            message: Log message
            **kwargs: Additional context
            
        Returns:
            Formatted message with context
        """
        import json
        
        # SAFETY: Merge context
        full_context = {**self.context, **kwargs}
        
        # SAFETY: Serialize context
        try:
            context_str = json.dumps(full_context, default=str)
        except TypeError:
            context_str = str(full_context)
        
        return f"{message} | Context: {context_str}"
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with context."""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message with context."""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with context."""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with context."""
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message with context."""
        self.logger.critical(self._format_message(message, **kwargs))
    
    def exception(self, message: str, **kwargs: Any) -> None:
        """Log exception with context."""
        self.logger.exception(self._format_message(message, **kwargs))


def create_structured_logger(
    name: str,
    level: Optional[int] = None
) -> StructuredLogger:
    """
    Create structured logger instance.
    
    Convenience function for creating structured logger.
    
    Args:
        name: Logger name (typically __name__)
        level: Log level (default: INFO)
        
    Returns:
        StructuredLogger instance
    """
    logger = get_logger(name=name, level=level)
    return StructuredLogger(logger)


class LogContext:
    """
    Context manager for temporary log context.
    
    Usage:
        with LogContext(logger, key="value"):
            logger.info("Message")  # Includes context
    """
    
    def __init__(
        self,
        logger: StructuredLogger,
        **kwargs: Any
    ):
        """
        Initialize log context.
        
        Args:
            logger: Structured logger instance
            **kwargs: Context fields to add
        """
        self.logger = logger
        self.context = kwargs
        self.original_context: Dict[str, Any] = {}
    
    def __enter__(self) -> 'LogContext':
        """Enter context manager."""
        self.original_context = self.logger.context.copy()
        self.logger.add_context(**self.context)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.logger.context = self.original_context

