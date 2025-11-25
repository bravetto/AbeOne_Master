"""
Usage Tracking Middleware

This middleware tracks API usage for quota enforcement and billing:
1. Records API calls per organization
2. Tracks usage metrics in real-time
3. Enforces subscription limits
4. Provides usage analytics

Architecture:
- Real-time tracking in Redis for performance
- Persistent storage in PostgreSQL for history
- Quota enforcement before request processing
- Usage analytics and reporting
"""

from typing import Dict, Any, Optional, List
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta, timezone
import json
import redis
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.database import get_session_factory
from app.core.models import UsageRecord, Subscription, SubscriptionTier
from app.middleware.tenant_context import TenantContext
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Redis connection for real-time usage tracking
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)


class UsageTracker:
    """
    Usage tracking service for API calls and resource consumption.
    
    Provides real-time usage tracking with Redis and persistent
    storage with PostgreSQL for analytics and billing.
    """
    
    def __init__(self):
        self.redis_client = redis_client
        self.usage_prefix = "usage:org:"
        self.quota_prefix = "quota:org:"
    
    def get_usage_key(self, organization_id: str, period: str = "current") -> str:
        """Generate Redis key for usage tracking."""
        return f"{self.usage_prefix}{organization_id}:{period}"
    
    def get_quota_key(self, organization_id: str) -> str:
        """Generate Redis key for quota limits."""
        return f"{self.quota_prefix}{organization_id}"
    
    async def track_api_call(
        self, 
        organization_id: str, 
        endpoint: str, 
        method: str,
        response_time: float,
        status_code: int
    ) -> Dict[str, Any]:
        """
        Track API call usage for an organization.
        
        Args:
            organization_id: Organization identifier
            endpoint: API endpoint called
            method: HTTP method
            response_time: Response time in seconds
            status_code: HTTP status code
            
        Returns:
            Current usage statistics
        """
        try:
            # Get current usage from Redis
            usage_key = self.get_usage_key(organization_id)
            current_usage = self.redis_client.hgetall(usage_key)
            
            # Increment API call count
            api_calls = int(current_usage.get("api_calls", 0)) + 1
            total_response_time = float(current_usage.get("total_response_time", 0)) + response_time
            
            # Update usage in Redis
            usage_data = {
                "api_calls": str(api_calls),
                "total_response_time": str(total_response_time),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "endpoints": json.dumps(
                    json.loads(current_usage.get("endpoints", "{}")) | 
                    {f"{method}:{endpoint}": json.loads(current_usage.get("endpoints", "{}")).get(f"{method}:{endpoint}", 0) + 1}
                )
            }
            
            self.redis_client.hset(usage_key, mapping=usage_data)
            
            # Set expiration to end of current month
            self.redis_client.expire(usage_key, self._get_seconds_until_month_end())
            
            # Store detailed record in PostgreSQL (async)
            await self._store_usage_record(
                organization_id, endpoint, method, response_time, status_code
            )
            
            logger.debug(f"Tracked API call for organization: {organization_id}")
            
            return {
                "api_calls": api_calls,
                "avg_response_time": total_response_time / api_calls,
                "last_updated": usage_data["last_updated"]
            }
            
        except Exception as e:
            logger.error(f"Error tracking API call: {e}")
            return {}
    
    async def get_current_usage(self, organization_id: str) -> Dict[str, Any]:
        """
        Get current usage statistics for an organization.
        
        Args:
            organization_id: Organization identifier
            
        Returns:
            Current usage statistics
        """
        try:
            usage_key = self.get_usage_key(organization_id)
            usage_data = self.redis_client.hgetall(usage_key)
            
            if not usage_data:
                return {
                    "api_calls": 0,
                    "avg_response_time": 0,
                    "endpoints": {},
                    "last_updated": None
                }
            
            api_calls = int(usage_data.get("api_calls", 0))
            total_response_time = float(usage_data.get("total_response_time", 0))
            
            return {
                "api_calls": api_calls,
                "avg_response_time": total_response_time / api_calls if api_calls > 0 else 0,
                "endpoints": json.loads(usage_data.get("endpoints", "{}")),
                "last_updated": usage_data.get("last_updated")
            }
            
        except Exception as e:
            logger.error(f"Error getting current usage: {e}")
            return {}
    
    async def get_quota_limits(self, organization_id: str, db: AsyncSession) -> Dict[str, Any]:
        """
        Get quota limits for an organization based on subscription.
        
        Args:
            organization_id: Organization identifier
            db: Database session
            
        Returns:
            Quota limits and current usage
        """
        try:
            # Get active subscription
            stmt = select(Subscription).options(selectinload(Subscription.subscription_tier)).where(
                and_(
                    Subscription.organization_id == organization_id,
                    Subscription.status == "active"
                )
            )
            result = await db.execute(stmt)
            subscription = result.scalar_one_or_none()
            
            if not subscription or not subscription.subscription_tier:
                # Default limits for free tier
                return {
                    "api_calls_limit": 1000,
                    "storage_limit": 100,  # MB
                    "tier": "free"
                }
            
            tier = subscription.subscription_tier
            
            # Get current usage
            current_usage = await self.get_current_usage(organization_id)
            
            # Get limits from JSON field
            api_calls_limit = tier.limits.get("api_calls_limit", 0) if tier.limits else 0
            storage_limit = tier.limits.get("storage_limit", 0) if tier.limits else 0
            
            return {
                "api_calls_limit": api_calls_limit,
                "storage_limit": storage_limit,
                "api_calls_used": current_usage.get("api_calls", 0),
                "tier": tier.name,
                "usage_percentage": (current_usage.get("api_calls", 0) / api_calls_limit * 100) if api_calls_limit > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting quota limits: {e}", exc_info=True)
            return {}
    
    async def check_quota_exceeded(self, organization_id: str, db: AsyncSession) -> bool:
        """
        Check if organization has exceeded quota limits.
        
        Args:
            organization_id: Organization identifier
            db: Database session
            
        Returns:
            True if quota exceeded, False otherwise
        """
        try:
            quota_info = await self.get_quota_limits(organization_id, db)
            
            if quota_info.get("api_calls_used", 0) >= quota_info.get("api_calls_limit", 0):
                logger.warning(f"Quota exceeded for organization: {organization_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking quota: {e}", exc_info=True)
            return False
    
    async def _store_usage_record(
        self,
        organization_id: str,
        endpoint: str,
        method: str,
        response_time: float,
        status_code: int
    ):
        """Store detailed usage record in PostgreSQL."""
        try:
            # This would be called asynchronously to avoid blocking the request
            # For now, we'll just log it
            logger.debug(
                f"Storing usage record: {organization_id} - {method} {endpoint} - "
                f"{response_time}s - {status_code}"
            )
            
            # TODO: Implement actual database storage
            # This would be done in a background task or separate service
            
        except Exception as e:
            logger.error(f"Error storing usage record: {e}")
    
    def _get_seconds_until_month_end(self) -> int:
        """Calculate seconds until end of current month."""
        now = datetime.now(timezone.utc)
        if now.month == 12:
            next_month = now.replace(year=now.year + 1, month=1, day=1)
        else:
            next_month = now.replace(month=now.month + 1, day=1)
        
        return int((next_month - now).total_seconds())


# Global usage tracker instance
usage_tracker = UsageTracker()


async def usage_tracking_middleware(request: Request, call_next):
    """
    Middleware to track API usage and enforce quotas.
    
    This middleware:
    1. Checks quota limits before processing request
    2. Tracks API usage in real-time
    3. Records usage metrics for billing
    4. Enforces subscription limits
    """
    start_time = datetime.now(timezone.utc)
    
    try:
        # Skip usage tracking for webhook endpoints
        if request.url.path.startswith("/webhooks/"):
            response = await call_next(request)
            return response
        
        # Get tenant context from request state
        if not hasattr(request.state, 'tenant_context'):
            # If no tenant context, skip usage tracking
            response = await call_next(request)
            return response
        
        tenant_context: TenantContext = request.state.tenant_context
        organization_id = tenant_context.organization_id
        
        # Get database session factory and create async session for quota checking
        session_factory = get_session_factory()
        if not session_factory:
            logger.warning("Database session factory not available, skipping quota check")
            response = await call_next(request)
            return response
        
        async with session_factory() as db:
            try:
                # Check if quota exceeded
                quota_exceeded = await usage_tracker.check_quota_exceeded(organization_id, db)
                
                if quota_exceeded:
                    logger.warning(f"Quota exceeded for organization: {organization_id}")
                    return JSONResponse(
                        status_code=429,
                        content={
                            "error": "Quota exceeded",
                            "message": "You have reached your API call limit for this billing period",
                            "upgrade_url": "/dashboard/billing"
                        }
                    )
                
                # Process request
                response = await call_next(request)
                
                # Calculate response time
                response_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                
                # Track usage
                await usage_tracker.track_api_call(
                    organization_id=organization_id,
                    endpoint=request.url.path,
                    method=request.method,
                    response_time=response_time,
                    status_code=response.status_code
                )
                
                # Add usage headers to response
                current_usage = await usage_tracker.get_current_usage(organization_id)
                quota_info = await usage_tracker.get_quota_limits(organization_id, db)
                
                response.headers["X-Usage-Calls"] = str(current_usage.get("api_calls", 0))
                response.headers["X-Usage-Limit"] = str(quota_info.get("api_calls_limit", 0))
                response.headers["X-Usage-Remaining"] = str(
                    quota_info.get("api_calls_limit", 0) - current_usage.get("api_calls", 0)
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Error in usage tracking middleware: {e}", exc_info=True)
                # Continue with request even if tracking fails
                response = await call_next(request)
                return response
                
    except Exception as e:
        logger.error(f"Error in usage tracking middleware (outer): {e}", exc_info=True)
        # Continue with request even if tracking fails
        response = await call_next(request)
        return response


async def get_usage_analytics(organization_id: str, db: AsyncSession) -> Dict[str, Any]:
    """
    Get detailed usage analytics for an organization.
    
    Args:
        organization_id: Organization identifier
        db: Database session
        
    Returns:
        Usage analytics including trends and breakdowns
    """
    try:
        # Get current period usage
        current_usage = await usage_tracker.get_current_usage(organization_id)
        quota_info = await usage_tracker.get_quota_limits(organization_id, db)
        
        # Get historical usage (last 30 days)
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        
        # TODO: Implement historical usage query
        # This would query UsageRecord table for historical data
        
        return {
            "current_period": {
                "api_calls": current_usage.get("api_calls", 0),
                "avg_response_time": current_usage.get("avg_response_time", 0),
                "endpoints": current_usage.get("endpoints", {}),
                "last_updated": current_usage.get("last_updated")
            },
            "quota": quota_info,
            "historical": {
                "last_30_days": {
                    "total_calls": 0,  # TODO: Calculate from historical data
                    "avg_daily_calls": 0,
                    "peak_usage_day": None
                }
            },
            "recommendations": _generate_usage_recommendations(current_usage, quota_info)
        }
        
    except Exception as e:
        logger.error(f"Error getting usage analytics: {e}")
        return {}


def _generate_usage_recommendations(current_usage: Dict[str, Any], quota_info: Dict[str, Any]) -> List[str]:
    """Generate usage recommendations based on current usage patterns."""
    recommendations = []
    
    usage_percentage = quota_info.get("usage_percentage", 0)
    
    if usage_percentage > 90:
        recommendations.append("You're approaching your API limit. Consider upgrading your plan.")
    elif usage_percentage > 75:
        recommendations.append("You've used 75% of your API calls. Monitor your usage closely.")
    
    avg_response_time = current_usage.get("avg_response_time", 0)
    if avg_response_time > 2.0:
        recommendations.append("Your API response times are high. Consider optimizing your requests.")
    
    return recommendations
