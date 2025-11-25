"""
Logging System - Comprehensive Logging System

Implements comprehensive logging system with multiple log levels, formatters, and handlers.

Pattern: LOGGING × SYSTEM × HANDLERS × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import sys
from pathlib import Path
from .log_formatters import LogFormatter, SimpleFormatter


class LogLevel(Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogHandler:
    """Base log handler."""
    
    def handle(self, level: LogLevel, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Handle a log message."""
        raise NotImplementedError


class ConsoleHandler(LogHandler):
    """Console log handler."""
    
    def __init__(self, formatter: Optional[LogFormatter] = None):
        """Initialize console handler."""
        self.formatter = formatter or SimpleFormatter()
        self.stream = sys.stdout
    
    def handle(self, level: LogLevel, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Handle log message to console."""
        formatted = self.formatter.format(level.value, message, context)
        print(formatted, file=self.stream)


class FileHandler(LogHandler):
    """File log handler."""
    
    def __init__(self, log_file: str, formatter: Optional[LogFormatter] = None):
        """Initialize file handler."""
        self.log_file = Path(log_file)
        self.formatter = formatter or SimpleFormatter()
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def handle(self, level: LogLevel, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Handle log message to file."""
        formatted = self.formatter.format(level.value, message, context)
        with open(self.log_file, 'a') as f:
            f.write(formatted + '\n')


@dataclass
class LoggerConfig:
    """Logger configuration."""
    level: LogLevel = LogLevel.INFO
    handlers: List[LogHandler] = field(default_factory=list)
    enable_context: bool = True


class Logger:
    """
    Logger.
    
    Responsibilities:
    - Log messages at different levels
    - Route logs to handlers
    - Manage log context
    """
    
    def __init__(self, name: str, config: Optional[LoggerConfig] = None):
        """Initialize logger."""
        self.name = name
        self.config = config or LoggerConfig()
        self.context: Dict[str, Any] = {}
    
    def set_level(self, level: LogLevel) -> None:
        """Set log level."""
        self.config.level = level
    
    def add_handler(self, handler: LogHandler) -> None:
        """Add log handler."""
        self.config.handlers.append(handler)
    
    def set_context(self, key: str, value: Any) -> None:
        """Set context value."""
        self.context[key] = value
    
    def clear_context(self) -> None:
        """Clear context."""
        self.context.clear()
    
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged."""
        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 4
        }
        return level_order[level] >= level_order[self.config.level]
    
    def _log(self, level: LogLevel, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Internal log method."""
        if not self._should_log(level):
            return
        
        # Merge context
        log_context = {}
        if self.config.enable_context:
            log_context.update(self.context)
        if context:
            log_context.update(context)
        
        # Send to handlers
        for handler in self.config.handlers:
            try:
                handler.handle(level, message, log_context if log_context else None)
            except Exception as e:
                print(f"⚠️ Log handler failed: {e}", file=sys.stderr)
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log debug message."""
        self._log(LogLevel.DEBUG, message, context)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log info message."""
        self._log(LogLevel.INFO, message, context)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log warning message."""
        self._log(LogLevel.WARNING, message, context)
    
    def error(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log error message."""
        self._log(LogLevel.ERROR, message, context)
    
    def critical(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log critical message."""
        self._log(LogLevel.CRITICAL, message, context)


class LoggingSystem:
    """
    Logging System.
    
    Responsibilities:
    - Manage loggers
    - Provide default logger
    - Configure logging system
    """
    
    def __init__(self):
        """Initialize logging system."""
        self.loggers: Dict[str, Logger] = {}
        self.default_logger: Optional[Logger] = None
        self._setup_default_logger()
    
    def _setup_default_logger(self) -> None:
        """Setup default logger."""
        config = LoggerConfig(
            level=LogLevel.INFO,
            handlers=[ConsoleHandler()]
        )
        self.default_logger = Logger("abeone", config)
        self.loggers["abeone"] = self.default_logger
    
    def get_logger(self, name: str) -> Logger:
        """
        Get or create a logger.
        
        Args:
            name: Logger name
        
        Returns:
            Logger instance
        """
        if name not in self.loggers:
            config = LoggerConfig(
                level=LogLevel.INFO,
                handlers=[ConsoleHandler()]
            )
            self.loggers[name] = Logger(name, config)
        
        return self.loggers[name]
    
    def get_default_logger(self) -> Logger:
        """Get default logger."""
        return self.default_logger or self.get_logger("abeone")


# Global logging system instance
_logging_system_instance: Optional[LoggingSystem] = None


def get_logging_system() -> LoggingSystem:
    """Get global logging system instance."""
    global _logging_system_instance
    if _logging_system_instance is None:
        _logging_system_instance = LoggingSystem()
    return _logging_system_instance


def get_logger(name: str = "abeone") -> Logger:
    """Get a logger."""
    return get_logging_system().get_logger(name)

