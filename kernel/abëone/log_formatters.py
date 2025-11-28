"""
Log Formatters - Log Formatting Utilities

Implements log formatters for different log formats.

Pattern: LOG × FORMATTERS × UTILITIES × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, Any, Optional
from datetime import datetime
import json


class LogFormatter:
    """Base log formatter."""
    
    def format(self, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Format a log message.
        
        Args:
            level: Log level
            message: Log message
            context: Optional context
        
        Returns:
            Formatted log message
        """
        raise NotImplementedError


class SimpleFormatter(LogFormatter):
    """Simple log formatter."""
    
    def format(self, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Format log message in simple format."""
        timestamp = datetime.now().isoformat()
        context_str = f" {json.dumps(context)}" if context else ""
        return f"[{timestamp}] [{level}] {message}{context_str}"


class DetailedFormatter(LogFormatter):
    """Detailed log formatter."""
    
    def format(self, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Format log message in detailed format."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        
        if context:
            log_entry["context"] = context
        
        return json.dumps(log_entry, indent=2)


class CompactFormatter(LogFormatter):
    """Compact log formatter."""
    
    def format(self, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Format log message in compact format."""
        level_short = level[:1].upper()
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"{timestamp} {level_short} {message}"

