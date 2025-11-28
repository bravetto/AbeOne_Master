"""
Admin API endpoints for Guard Services Orchestrator.

These endpoints require admin authentication and provide administrative
functionality for managing the orchestrator.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.api.dependencies import require_admin_access
from app.core.guard_orchestrator import orchestrator
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/admin/guards", tags=["Guard Admin"])


@router.get("/circuit-breakers", response_model=Dict[str, Any])
async def get_circuit_breakers(
    admin_user = Depends(require_admin_access)
) -> Dict[str, Any]:
    """
    Get circuit breaker states for all services.
    
    Admin-only endpoint that exposes detailed circuit breaker information
    including state, failure counts, and last failure timestamps.
    """
    try:
        circuit_breaker_data = {}
        
        for service_name, breaker in orchestrator.circuit_breakers.items():
            circuit_breaker_data[service_name] = {
                "state": breaker.state,
                "failure_count": breaker.failure_count,
                "threshold": breaker.threshold,
                "timeout": breaker.timeout,
                "last_failure_time": breaker.last_failure_time.isoformat() if breaker.last_failure_time else None,
                "can_execute": breaker.can_execute()
            }
        
        return {
            "total_breakers": len(circuit_breaker_data),
            "breakers": circuit_breaker_data
        }
        
    except Exception as e:
        logger.error(f"Error getting circuit breaker states: {e}")
        raise HTTPException(status_code=500, detail="Failed to get circuit breaker states")

