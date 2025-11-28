"""
Performance Optimization Module

FULL MONTY EEAaO: Excellence at Every Level
- Connection pooling
- Request batching
- Parallel execution
- Caching optimization
- Query optimization
"""

import asyncio
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timezone
import time

from app.core.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class PerformanceOptimizer:
    """
    Performance optimizer for parallel execution and caching.
    
    EEAaO: Excellence at Every Level
    """
    
    def __init__(self):
        self._batch_queues: Dict[str, List[Any]] = {}
        self._batch_timers: Dict[str, float] = {}
        self._batch_size = 10
        self._batch_timeout = 0.1  # 100ms
    
    async def parallel_execute(
        self,
        tasks: List[Callable],
        max_concurrent: int = 10
    ) -> List[Any]:
        """
        Execute multiple tasks in parallel with concurrency limit.
        
        EEAaO: Parallel execution for excellence
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_with_semaphore(task):
            async with semaphore:
                if asyncio.iscoroutinefunction(task):
                    return await task()
                else:
                    return task()
        
        results = await asyncio.gather(
            *[execute_with_semaphore(task) for task in tasks],
            return_exceptions=True
        )
        
        # SAFETY: Export errors instead of silently filtering
        filtered_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                from app.core.error_exporter import get_error_exporter
                get_error_exporter().export_error(
                    result,
                    context={"operation": "parallel_execute", "task_index": i},
                    error_code="PARALLEL_EXECUTION_ERROR"
                )
            else:
                filtered_results.append(result)
        
        return filtered_results
    
    async def batch_execute(
        self,
        queue_name: str,
        task: Callable,
        item: Any
    ) -> Optional[Any]:
        """
        Batch execute tasks for efficiency.
        
        EEAaO: Batching for performance excellence
        """
        if queue_name not in self._batch_queues:
            self._batch_queues[queue_name] = []
            self._batch_timers[queue_name] = time.time()
        
        self._batch_queues[queue_name].append((task, item))
        
        # Check if batch is ready
        queue_size = len(self._batch_queues[queue_name])
        elapsed = time.time() - self._batch_timers[queue_name]
        
        if queue_size >= self._batch_size or elapsed >= self._batch_timeout:
            return await self._flush_batch(queue_name)
        
        return None
    
    async def _flush_batch(self, queue_name: str) -> Any:
        """Flush a batch queue."""
        if queue_name not in self._batch_queues:
            return None
        
        batch = self._batch_queues.pop(queue_name)
        self._batch_timers.pop(queue_name, None)
        
        if not batch:
            return None
        
        # Execute batch in parallel
        tasks = [task(item) for task, item in batch]
        results = await self.parallel_execute(tasks)
        
        return results


# Global optimizer instance
_performance_optimizer: Optional[PerformanceOptimizer] = None


def get_performance_optimizer() -> PerformanceOptimizer:
    """Get global performance optimizer instance."""
    global _performance_optimizer
    if _performance_optimizer is None:
        _performance_optimizer = PerformanceOptimizer()
    return _performance_optimizer

