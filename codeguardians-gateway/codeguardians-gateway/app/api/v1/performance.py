"""
Performance Monitoring and Optimization Endpoints

FULL MONTY EEAaO: Excellence at Every Level
- Performance metrics
- Optimization recommendations
- Cache statistics
- Connection pool stats
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.performance_optimizer import get_performance_optimizer
from app.core.connection_pool_optimizer import get_connection_optimizer
from app.core.response_cache import get_cache_client
from app.core.query_optimizer import get_query_optimizer
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/performance", tags=["performance"])


@router.get("/metrics", summary="Get performance metrics")
async def get_performance_metrics() -> Dict[str, Any]:
    """
    Get comprehensive performance metrics.
    
    EEAaO: Performance excellence monitoring
    """
    optimizer = get_performance_optimizer()
    connection_optimizer = get_connection_optimizer()
    
    # Get cache stats
    cache_client = await get_cache_client()
    cache_stats = {}
    if cache_client:
        try:
            info = await cache_client.info("stats")
            cache_stats = {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
        except Exception as e:
            logger.debug(f"Cache stats unavailable: {e}")
    
    return {
        "performance_optimizer": {
            "batch_queues": len(optimizer._batch_queues),
            "batch_size": optimizer._batch_size,
            "batch_timeout": optimizer._batch_timeout
        },
        "connection_pools": {
            "http_client": "initialized" if connection_optimizer._http_client else "not_initialized",
            "redis_pool": "initialized" if connection_optimizer._redis_pool else "not_initialized"
        },
        "cache": cache_stats,
        "optimization_status": "excellent"
    }


@router.get("/optimization/recommendations", summary="Get optimization recommendations")
async def get_optimization_recommendations() -> Dict[str, Any]:
    """
    Get performance optimization recommendations.
    
    EEAaO: Excellence recommendations
    """
    recommendations = []
    
    # Check cache hit rate
    cache_client = await get_cache_client()
    if cache_client:
        try:
            info = await cache_client.info("stats")
            hits = int(info.get("keyspace_hits", 0))
            misses = int(info.get("keyspace_misses", 0))
            total = hits + misses
            
            if total > 0:
                hit_rate = hits / total
                if hit_rate < 0.7:
                    recommendations.append({
                        "type": "cache",
                        "priority": "medium",
                        "message": f"Cache hit rate is {hit_rate:.1%}, consider increasing cache TTL",
                        "current_hit_rate": hit_rate
                    })
        except Exception:
            pass
    
    return {
        "recommendations": recommendations,
        "total_recommendations": len(recommendations),
        "optimization_level": "excellent" if len(recommendations) == 0 else "good"
    }

