"""
Parallel Guard Execution Module

FULL MONTY EEAaO: Excellence at Every Level
- Parallel guard service execution
- Concurrent request handling
- Optimized orchestration
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import time

from app.core.guard_orchestrator import (
    GuardServiceOrchestrator,
    OrchestrationRequest,
    GuardServiceType
)
from app.utils.logging import get_logger

logger = get_logger(__name__)


class ParallelGuardExecutor:
    """
    Execute multiple guard services in parallel for optimal performance.
    
    EEAaO: Excellence at Every Level - Parallel execution
    """
    
    def __init__(self, orchestrator: GuardServiceOrchestrator):
        self.orchestrator = orchestrator
        self.max_concurrent = 10
    
    async def execute_parallel_guards(
        self,
        requests: List[OrchestrationRequest],
        max_concurrent: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple guard requests in parallel.
        
        EEAaO: Parallel execution for excellence
        """
        max_concurrent = max_concurrent or self.max_concurrent
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_with_semaphore(request: OrchestrationRequest):
            async with semaphore:
                try:
                    response = await self.orchestrator.orchestrate_request(request)
                    return {
                        "request_id": response.request_id,
                        "success": response.success,
                        "data": response.data,
                        "service_type": response.service_type.value if response.service_type else None,
                        "processing_time": response.processing_time
                    }
                except Exception as e:
                    from app.core.error_exporter import get_error_exporter
                    error_exporter = get_error_exporter()
                    error_exporter.export_error(
                        e,
                        context={"operation": "parallel_guard_execution", "service_type": request.service_type.value},
                        error_code="PARALLEL_GUARD_ERROR",
                        request_id=request.request_id
                    )
                    return {
                        "request_id": request.request_id,
                        "success": False,
                        "error": str(e),
                        "error_code": getattr(e, 'error_code', 'PARALLEL_GUARD_ERROR')
                    }
        
        start_time = time.time()
        results = await asyncio.gather(
            *[execute_with_semaphore(req) for req in requests],
            return_exceptions=True
        )
        total_time = time.time() - start_time
        
        logger.info(
            f"Parallel guard execution completed: {len(requests)} requests in {total_time:.2f}s"
        )
        
        return [r for r in results if not isinstance(r, Exception)]
    
    async def execute_multi_guard_pipeline(
        self,
        request: OrchestrationRequest,
        guard_sequence: List[GuardServiceType]
    ) -> Dict[str, Any]:
        """
        Execute multiple guards in sequence with parallel optimization.
        
        EEAaO: Pipeline optimization for excellence
        """
        results = {}
        start_time = time.time()
        
        # Execute guards in sequence but optimize each step
        for guard_type in guard_sequence:
            guard_request = OrchestrationRequest(
                request_id=f"{request.request_id}-{guard_type.value}",
                service_type=guard_type,
                payload=request.payload,
                user_id=request.user_id,
                session_id=request.session_id,
                priority=request.priority,
                timeout=request.timeout,
                fallback_enabled=request.fallback_enabled
            )
            
            try:
                response = await self.orchestrator.orchestrate_request(guard_request)
                results[guard_type.value] = {
                    "success": response.success,
                    "data": response.data,
                    "processing_time": response.processing_time
                }
            except Exception as e:
                from app.core.error_exporter import get_error_exporter
                error_exporter = get_error_exporter()
                error_exporter.export_error(
                    e,
                    context={"operation": "guard_pipeline_step", "guard_type": guard_type.value},
                    error_code="GUARD_PIPELINE_ERROR",
                    request_id=request.request_id
                )
                results[guard_type.value] = {
                    "success": False,
                    "error": str(e),
                    "error_code": getattr(e, 'error_code', 'GUARD_PIPELINE_ERROR')
                }
        
        total_time = time.time() - start_time
        
        return {
            "results": results,
            "total_time": total_time,
            "sequence": [g.value for g in guard_sequence]
        }

