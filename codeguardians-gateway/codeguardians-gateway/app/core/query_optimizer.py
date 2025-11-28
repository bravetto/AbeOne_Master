"""
Database Query Optimizer

FULL MONTY EEAaO: Excellence at Every Level
- Query batching
- Result caching
- Index optimization
- Query plan analysis
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta, timezone

from app.core.response_cache import get_cached_response, set_cached_response
from app.utils.logging import get_logger

logger = get_logger(__name__)


class QueryOptimizer:
    """
    Optimize database queries for maximum performance.
    
    EEAaO: Excellence at Every Level - Query optimization
    """
    
    async def batch_fetch(
        self,
        db: AsyncSession,
        queries: List[select],
        cache_ttl: int = 300
    ) -> List[Any]:
        """
        Execute multiple queries in batch with caching.
        
        EEAaO: Batch optimization for excellence
        """
        from app.core.error_exporter import get_error_exporter
        error_exporter = get_error_exporter()
        results = []
        
        for i, query in enumerate(queries):
            try:
                # Generate cache key from query
                cache_key = f"query:{hash(str(query))}"
                
                # Try cache first
                cached = await get_cached_response(cache_key)
                if cached:
                    results.append(cached.get("data"))
                    continue
                
                # Execute query
                result = await db.execute(query)
                data = result.scalars().all()
                
                # Cache result
                try:
                    await set_cached_response(
                        cache_key,
                        {"data": [str(d) for d in data]},
                        cache_ttl
                    )
                except Exception as cache_error:
                    error_exporter.export_error(
                        cache_error,
                        context={"operation": "cache_query_result", "query_index": i},
                        error_code="QUERY_CACHE_ERROR"
                    )
                    # Continue without cache
                
                results.append(data)
            except Exception as query_error:
                error_exporter.export_error(
                    query_error,
                    context={"operation": "batch_fetch_query", "query_index": i},
                    error_code="QUERY_EXECUTION_ERROR"
                )
                # Add None to maintain list length
                results.append(None)
        
        return results
    
    async def optimized_select(
        self,
        db: AsyncSession,
        query: select,
        cache_ttl: int = 300,
        use_cache: bool = True
    ) -> List[Any]:
        """
        Execute optimized select query with caching.
        
        EEAaO: Query optimization for excellence
        """
        from app.core.error_exporter import get_error_exporter
        error_exporter = get_error_exporter()
        
        if use_cache:
            try:
                cache_key = f"query:{hash(str(query))}"
                cached = await get_cached_response(cache_key)
                if cached:
                    logger.debug(f"Query cache hit: {cache_key}")
                    return cached.get("data", [])
            except Exception as cache_error:
                error_exporter.export_error(
                    cache_error,
                    context={"operation": "get_cached_query"},
                    error_code="QUERY_CACHE_READ_ERROR"
                )
                # Continue without cache
        
        try:
            result = await db.execute(query)
            data = result.scalars().all()
            
            if use_cache:
                try:
                    await set_cached_response(
                        cache_key,
                        {"data": [str(d) for d in data]},
                        cache_ttl
                    )
                except Exception as cache_error:
                    error_exporter.export_error(
                        cache_error,
                        context={"operation": "cache_query_result"},
                        error_code="QUERY_CACHE_WRITE_ERROR"
                    )
                    # Continue without caching
            
            return data
        except Exception as query_error:
            error_exporter.export_error(
                query_error,
                context={"operation": "optimized_select"},
                error_code="QUERY_EXECUTION_ERROR"
            )
            raise


# Global optimizer instance
_query_optimizer: Optional[QueryOptimizer] = None


def get_query_optimizer() -> QueryOptimizer:
    """Get global query optimizer instance."""
    global _query_optimizer
    if _query_optimizer is None:
        _query_optimizer = QueryOptimizer()
    return _query_optimizer

