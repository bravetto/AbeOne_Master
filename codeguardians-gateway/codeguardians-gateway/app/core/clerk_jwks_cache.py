"""
Clerk JWKS Caching Module

Caches JWKS (JSON Web Key Set) responses from Clerk to improve performance
and reduce API calls. Includes retry logic for resilience.
"""

import time
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import httpx
from app.core.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# In-memory cache for JWKS
_jwks_cache: Optional[Dict[str, Any]] = None
_jwks_cache_time: float = 0.0
_jwks_cache_ttl: float = 3600.0  # 1 hour default TTL


async def get_cached_jwks(jwks_url: str, ttl: float = 3600.0) -> Optional[Dict[str, Any]]:
    """
    Get JWKS from cache or fetch from Clerk.
    
    Args:
        jwks_url: Clerk JWKS endpoint URL
        ttl: Time to live in seconds (default: 1 hour)
        
    Returns:
        JWKS dictionary or None if fetch fails
    """
    global _jwks_cache, _jwks_cache_time, _jwks_cache_ttl
    
    current_time = time.time()
    
    # Check if cache is valid
    if _jwks_cache and (current_time - _jwks_cache_time) < ttl:
        logger.debug("JWKS cache hit")
        return _jwks_cache
    
    # Cache expired or missing, fetch from Clerk
    logger.debug("JWKS cache miss, fetching from Clerk")
    
    max_retries = 3
    retry_delay = 1.0
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(jwks_url)
                response.raise_for_status()
                
                jwks_data = response.json()
                
                # Update cache
                _jwks_cache = jwks_data
                _jwks_cache_time = current_time
                _jwks_cache_ttl = ttl
                
                logger.info("JWKS fetched and cached successfully")
                return jwks_data
                
        except httpx.TimeoutException:
            logger.warning(f"JWKS fetch timeout (attempt {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay * (attempt + 1))
        except httpx.HTTPStatusError as e:
            logger.error(f"JWKS fetch failed: HTTP {e.response.status_code}")
            if e.response.status_code >= 500 and attempt < max_retries - 1:
                await asyncio.sleep(retry_delay * (attempt + 1))
            else:
                break
        except Exception as e:
            logger.error(f"JWKS fetch failed: {e}")
            break
    
    # If we have stale cache, return it
    if _jwks_cache:
        logger.warning("Using stale JWKS cache due to fetch failure")
        return _jwks_cache
    
    logger.error("JWKS fetch failed and no cache available")
    return None


def invalidate_jwks_cache() -> None:
    """Invalidate JWKS cache to force refresh."""
    global _jwks_cache, _jwks_cache_time
    _jwks_cache = None
    _jwks_cache_time = 0.0
    logger.info("JWKS cache invalidated")

