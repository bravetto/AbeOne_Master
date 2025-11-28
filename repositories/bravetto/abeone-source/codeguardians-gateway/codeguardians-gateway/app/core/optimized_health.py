"""
Optimized Health Checks for Kubernetes Probes

PRODUCTION HARDENING:
- Lightweight health checks for K8s probes (<50ms for TrustGuard)
- Dependency checks (database, Redis) with timeouts
- Separate endpoints for liveness vs readiness
- Minimal resource usage

SAFETY: Fast health checks prevent probe timeouts
ASSUMES: Dependencies available within timeout
VERIFY: Health checks complete within SLA
"""

import asyncio
import time
from typing import Dict, Any, Optional
from fastapi import Response
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.response_cache import get_cached_health_check, set_cached_health_check
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class OptimizedHealthChecker:
    """
    Optimized health checker for Kubernetes probes.
    
    Separate lightweight checks for liveness vs readiness.
    """
    
    def __init__(self):
        """Initialize health checker."""
        self._liveness_cache: Optional[Dict[str, Any]] = None
        self._liveness_cache_ttl = 5.0  # Cache liveness for 5 seconds
        self._liveness_cache_time = 0.0
    
    async def liveness_check(self) -> JSONResponse:
        """
        Lightweight liveness check.
        
        K8s uses this to determine if container should be restarted.
        Should be fast (<50ms) and not check dependencies.
        Uses caching for optimal performance.
        
        VERIFY: Returns 200 if process is alive
        """
        start_time = time.time()
        
        # Try to get from cache first
        cached = await get_cached_health_check()
        if cached:
            cached["response_time_ms"] = round((time.time() - start_time) * 1000, 2)
            return JSONResponse(
                content=cached,
                status_code=200,
                headers={"Cache-Control": "no-cache"}
            )
        
        # Very lightweight check - just verify process is running
        health_data = {
            "status": "alive",
            "timestamp": time.time(),
            "service": "codeguardians-gateway"
        }
        
        # Add response time
        response_time = (time.time() - start_time) * 1000  # ms
        health_data["response_time_ms"] = round(response_time, 2)
        
        # Cache result
        await set_cached_health_check(health_data, ttl=5)
        
        return JSONResponse(
            content=health_data,
            status_code=200,
            headers={"Cache-Control": "no-cache"}
        )
    
    async def readiness_check(self, check_dependencies: bool = True) -> JSONResponse:
        """
        Readiness check with optional dependency checks.
        
        K8s uses this to determine if container can receive traffic.
        Can check dependencies but should timeout quickly.
        
        Args:
            check_dependencies: Whether to check database/Redis (default: True)
        
        VERIFY: Returns 200 if ready, 503 if not ready
        """
        start_time = time.time()
        health_data = {
            "status": "ready",
            "timestamp": time.time(),
            "service": "codeguardians-gateway",
            "checks": {}
        }
        
        is_ready = True
        
        # Check dependencies with timeouts
        if check_dependencies:
            # Database check (with timeout)
            db_check = await self._check_database(timeout=2.0)
            health_data["checks"]["database"] = db_check
            if not db_check["healthy"]:
                is_ready = False
            
            # Redis check (with timeout)
            redis_check = await self._check_redis(timeout=2.0)
            health_data["checks"]["redis"] = redis_check
            if not redis_check["healthy"]:
                is_ready = False
        
        # Add response time
        response_time = (time.time() - start_time) * 1000  # ms
        health_data["response_time_ms"] = round(response_time, 2)
        
        status_code = 200 if is_ready else 503
        health_data["status"] = "ready" if is_ready else "not_ready"
        
        return JSONResponse(
            content=health_data,
            status_code=status_code,
            headers={"Cache-Control": "no-cache"}
        )
    
    async def _check_database(self, timeout: float = 2.0) -> Dict[str, Any]:
        """
        Check database connectivity with timeout.
        
        Args:
            timeout: Maximum time to wait for check (seconds)
        
        Returns:
            Dict with 'healthy' boolean and optional 'error'
        """
        try:
            # Use asyncio.wait_for to enforce timeout
            result = await asyncio.wait_for(
                self._ping_database(),
                timeout=timeout
            )
            return {"healthy": True, "response_time_ms": result}
        except asyncio.TimeoutError:
            logger.warning("Database health check timed out")
            return {"healthy": False, "error": "timeout"}
        except Exception as e:
            logger.warning(f"Database health check failed: {e}")
            return {"healthy": False, "error": str(e)}
    
    async def _ping_database(self) -> float:
        """Ping database and return response time in ms."""
        start_time = time.time()
        
        try:
            from sqlalchemy import text
            from app.core.database import get_engine
            engine = get_engine()
            
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            
            return (time.time() - start_time) * 1000
        except Exception as e:
            logger.error(f"Database ping failed: {e}")
            raise
    
    async def _check_redis(self, timeout: float = 2.0) -> Dict[str, Any]:
        """
        Check Redis connectivity with timeout.
        
        Args:
            timeout: Maximum time to wait for check (seconds)
        
        Returns:
            Dict with 'healthy' boolean and optional 'error'
        """
        try:
            result = await asyncio.wait_for(
                self._ping_redis(),
                timeout=timeout
            )
            return {"healthy": True, "response_time_ms": result}
        except asyncio.TimeoutError:
            logger.warning("Redis health check timed out")
            return {"healthy": False, "error": "timeout"}
        except Exception as e:
            logger.warning(f"Redis health check failed: {e}")
            return {"healthy": False, "error": str(e)}
    
    async def _ping_redis(self) -> float:
        """Ping Redis and return response time in ms."""
        start_time = time.time()
        
        try:
            import redis.asyncio as redis
            from app.core.config import get_settings
            settings = get_settings()
            
            client = redis.from_url(
                settings.REDIS_URL,
                socket_connect_timeout=1.0,
                socket_timeout=1.0
            )
            
            await client.ping()
            await client.close()
            
            return (time.time() - start_time) * 1000
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            raise


# Global health checker instance
_health_checker: Optional[OptimizedHealthChecker] = None


def get_health_checker() -> OptimizedHealthChecker:
    """Get global health checker instance."""
    global _health_checker
    if _health_checker is None:
        _health_checker = OptimizedHealthChecker()
    return _health_checker

