"""
Configuration Management API

This module provides endpoints for managing system configuration including:
- Configuration CRUD operations
- Rate limit configuration
- Feature flags management
- Cache configuration
- Configuration export and reload
"""

import logging
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from app.core.database import get_db
from app.middleware.tenant_context import TenantContext, get_current_tenant
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/config", tags=["Configuration"])


# Pydantic models for config management
class ConfigResponse(BaseModel):
    """Response model for configuration."""
    config: Dict[str, Any]
    last_updated: Optional[datetime] = None
    version: str = "1.0"


class RateLimitsRequest(BaseModel):
    """Request model for updating rate limits."""
    limit: Optional[int] = Field(None, description="Rate limit per minute")
    burst: Optional[int] = Field(None, description="Burst limit")
    per_endpoint: Optional[Dict[str, int]] = Field(None, description="Per-endpoint limits")


class RateLimitsResponse(BaseModel):
    """Response model for rate limits."""
    limit: int
    burst: int
    per_endpoint: Dict[str, int]
    updated_at: datetime


class FeatureFlagsRequest(BaseModel):
    """Request model for updating feature flags."""
    flag: str = Field(..., description="Feature flag name")
    enabled: bool = Field(..., description="Whether the feature is enabled")
    value: Optional[Any] = Field(None, description="Optional feature flag value")


class FeatureFlagsResponse(BaseModel):
    """Response model for feature flags."""
    flags: Dict[str, Any]
    updated_at: datetime


class CacheConfigRequest(BaseModel):
    """Request model for cache configuration."""
    ttl: Optional[int] = Field(None, description="Time to live in seconds")
    max_size: Optional[int] = Field(None, description="Maximum cache size")
    eviction_policy: Optional[str] = Field(None, description="Cache eviction policy")


class CacheConfigResponse(BaseModel):
    """Response model for cache configuration."""
    ttl: int
    max_size: int
    eviction_policy: str
    updated_at: datetime


class ConfigStatusResponse(BaseModel):
    """Response model for config status."""
    status: str
    last_updated: datetime
    version: str
    features_enabled: int
    rate_limits_active: bool


@router.get("/config", response_model=ConfigResponse)
async def get_config(
    tenant_context: TenantContext = Depends(get_current_tenant)
):
    """
    Get current configuration.
    
    Returns the current system configuration.
    """
    try:
        # In a real implementation, this would fetch from database or config service
        # For now, return a basic config structure
        config = {
            "api_version": "1.0",
            "features": {
                "rate_limiting": True,
                "caching": True,
                "monitoring": True
            },
            "organization_id": tenant_context.organization_id
        }
        
        return ConfigResponse(
            config=config,
            last_updated=datetime.now(timezone.utc),
            version="1.0"
        )
        
    except Exception as e:
        logger.error(f"Error retrieving config: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve configuration"
        )


@router.get("/config/rate-limits", response_model=RateLimitsResponse)
async def get_rate_limits(
    tenant_context: TenantContext = Depends(get_current_tenant)
):
    """
    Get current rate limit configuration.
    
    Returns the current rate limit settings.
    """
    try:
        # In a real implementation, fetch from database
        return RateLimitsResponse(
            limit=100,
            burst=150,
            per_endpoint={
                "/api/v1/guards/process": 200,
                "/api/v1/guards/tokenguard": 300
            },
            updated_at=datetime.now(timezone.utc)
        )
        
    except Exception as e:
        logger.error(f"Error retrieving rate limits: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve rate limits"
        )


@router.put("/config/rate-limits", response_model=RateLimitsResponse)
async def update_rate_limits(
    rate_limits: RateLimitsRequest,
    request: Request,
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Update rate limit configuration.
    
    Updates rate limit settings for the organization.
    """
    try:
        # Get old values for audit log
        old_limit = 100  # Default, would come from database
        old_burst = 150  # Default, would come from database
        
        # In a real implementation, save to database
        # For now, return the updated values
        updated_limits = {
            "limit": rate_limits.limit or 100,
            "burst": rate_limits.burst or 150,
            "per_endpoint": rate_limits.per_endpoint or {}
        }
        
        # Audit log
        from app.core.audit_logger import log_configuration_change
        await log_configuration_change(
            db=db,
            user_id=tenant_context.user_id,
            config_key="rate_limits",
            old_value={"limit": old_limit, "burst": old_burst},
            new_value=updated_limits,
            organization_id=tenant_context.organization_id,
            request=request
        )
        
        logger.info(f"Updated rate limits for organization: {tenant_context.organization_id}")
        
        return RateLimitsResponse(
            limit=updated_limits["limit"],
            burst=updated_limits["burst"],
            per_endpoint=updated_limits["per_endpoint"],
            updated_at=datetime.now(timezone.utc)
        )
        
    except Exception as e:
        logger.error(f"Error updating rate limits: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to update rate limits"
        )


@router.get("/config/feature-flags", response_model=FeatureFlagsResponse)
async def get_feature_flags(
    tenant_context: TenantContext = Depends(get_current_tenant)
):
    """
    Get current feature flags.
    
    Returns all feature flags and their status.
    """
    try:
        # In a real implementation, fetch from database
        flags = {
            "experimental_features": False,
            "new_ui": True,
            "beta_api": False
        }
        
        return FeatureFlagsResponse(
            flags=flags,
            updated_at=datetime.now(timezone.utc)
        )
        
    except Exception as e:
        logger.error(f"Error retrieving feature flags: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve feature flags"
        )


@router.put("/config/feature-flags", response_model=FeatureFlagsResponse)
async def update_feature_flags(
    feature_flag: FeatureFlagsRequest,
    tenant_context: TenantContext = Depends(get_current_tenant)
):
    """
    Update feature flag.
    
    Updates a specific feature flag.
    """
    try:
        # In a real implementation, save to database
        # For now, return updated flags
        flags = {
            "experimental_features": False,
            "new_ui": True,
            "beta_api": False,
            feature_flag.flag: feature_flag.enabled
        }
        
        logger.info(f"Updated feature flag {feature_flag.flag} for organization: {tenant_context.organization_id}")
        
        return FeatureFlagsResponse(
            flags=flags,
            updated_at=datetime.now(timezone.utc)
        )
        
    except Exception as e:
        logger.error(f"Error updating feature flags: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to update feature flags"
        )


@router.put("/config/cache", response_model=CacheConfigResponse)
async def update_cache_config(
    cache_config: CacheConfigRequest,
    tenant_context: TenantContext = Depends(get_current_tenant)
):
    """
    Update cache configuration.
    
    Updates cache settings including TTL and eviction policy.
    """
    try:
        # In a real implementation, save to database or cache service
        logger.info(f"Updated cache config for organization: {tenant_context.organization_id}")
        
        return CacheConfigResponse(
            ttl=cache_config.ttl or 3600,
            max_size=cache_config.max_size or 1000,
            eviction_policy=cache_config.eviction_policy or "lru",
            updated_at=datetime.now(timezone.utc)
        )
        
    except Exception as e:
        logger.error(f"Error updating cache config: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to update cache configuration"
        )


@router.get("/config/status", response_model=ConfigStatusResponse)
async def get_config_status(
    tenant_context: TenantContext = Depends(get_current_tenant)
):
    """
    Get configuration status.
    
    Returns the current status of configuration including last update time.
    """
    try:
        # In a real implementation, fetch from database
        flags = {
            "experimental_features": False,
            "new_ui": True,
            "beta_api": False
        }
        
        enabled_count = sum(1 for v in flags.values() if v)
        
        return ConfigStatusResponse(
            status="active",
            last_updated=datetime.now(timezone.utc),
            version="1.0",
            features_enabled=enabled_count,
            rate_limits_active=True
        )
        
    except Exception as e:
        logger.error(f"Error retrieving config status: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve configuration status"
        )


@router.post("/config/reload")
async def reload_config(
    tenant_context: TenantContext = Depends(get_current_tenant)
):
    """
    Reload configuration.
    
    Reloads configuration from the database or config service.
    """
    try:
        # In a real implementation, reload from database or config service
        logger.info(f"Reloaded config for organization: {tenant_context.organization_id}")
        
        return {
            "status": "success",
            "message": "Configuration reloaded successfully",
            "reloaded_at": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error reloading config: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to reload configuration"
        )


@router.get("/config/export")
async def export_config(
    tenant_context: TenantContext = Depends(get_current_tenant)
):
    """
    Export configuration.
    
    Exports the current configuration as JSON.
    """
    try:
        # In a real implementation, fetch all config from database
        export_data = {
            "organization_id": tenant_context.organization_id,
            "export_date": datetime.now(timezone.utc).isoformat(),
            "config": {
                "api_version": "1.0",
                "features": {
                    "rate_limiting": True,
                    "caching": True,
                    "monitoring": True
                }
            },
            "rate_limits": {
                "limit": 100,
                "burst": 150
            },
            "feature_flags": {
                "experimental_features": False,
                "new_ui": True,
                "beta_api": False
            },
            "cache": {
                "ttl": 3600,
                "max_size": 1000,
                "eviction_policy": "lru"
            }
        }
        
        return export_data
        
    except Exception as e:
        logger.error(f"Error exporting config: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to export configuration"
        )
