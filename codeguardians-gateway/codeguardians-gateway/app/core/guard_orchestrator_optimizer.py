"""
Guard Orchestrator Performance Optimizer

FULL MONTY EEAaO: Excellence at Every Level
- Optimized HTTP client integration
- Connection pooling
- Parallel request execution
"""

from typing import Optional
import httpx
from app.core.connection_pool_optimizer import get_connection_optimizer
from app.utils.logging import get_logger

logger = get_logger(__name__)


def get_optimized_http_client_for_orchestrator() -> httpx.AsyncClient:
    """
    Get optimized HTTP client for guard orchestrator.
    
    EEAaO: Excellence at Every Level - Optimized connections
    """
    optimizer = get_connection_optimizer()
    return optimizer.get_optimized_http_client()

