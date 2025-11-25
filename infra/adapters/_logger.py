"""
Shared logging utility for adapters.

Provides consistent logging across all Orbit-Spec adapters.

Pattern: LOGGING × ADAPTERS × ONE
"""

import logging
from typing import Optional


def get_adapter_logger(name: str) -> logging.Logger:
    """
    Get logger for adapter.
    
    Args:
        name: Adapter name (e.g., 'KernelAdapter', 'BusAdapter')
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(f"abeone.adapters.{name}")
    
    # Only configure if no handlers exist (avoid duplicate handlers)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger

