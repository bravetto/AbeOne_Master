"""
Shared response models to eliminate duplication across the API.

This module provides standardized response models that can be reused across
different API endpoints, following DRY principles.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


# Standard API Response Models
class StandardResponse(BaseModel):
    """Standard response model for API operations."""
    success: bool = Field(..., description="Whether the operation was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if operation failed")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class GuardResponse(StandardResponse):
    """Standard response model for guard service operations."""
    request_id: str = Field(..., description="Unique request identifier")
    service_type: str = Field(..., description="Type of guard service used")
    service_used: Optional[str] = Field(None, description="Actual service implementation used")
    fallback_used: bool = Field(False, description="Whether fallback mechanism was used")
    client_type: Optional[str] = Field(None, description="Client type that made the request")
    confidence_score: Optional[float] = Field(None, description="Overall confidence score")
    warnings: Optional[List[str]] = Field(default_factory=list, description="Warning messages")
    recommendations: Optional[List[str]] = Field(default_factory=list, description="Action recommendations")


class HealthResponse(BaseModel):
    """Standard response model for health check operations."""
    service_name: str = Field(..., description="Name of the service")
    status: str = Field(..., description="Health status: healthy, degraded, unhealthy")
    last_check: Optional[str] = Field(None, description="ISO timestamp of last health check")
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    version: Optional[str] = Field(None, description="Service version")
    uptime: Optional[float] = Field(None, description="Service uptime in seconds")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Health check metadata")


class ListResponse(BaseModel):
    """Standard response model for list operations with pagination."""
    items: List[Dict[str, Any]] = Field(default_factory=list, description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(1, description="Current page number")
    size: int = Field(20, description="Items per page")
    pages: int = Field(0, description="Total number of pages")
    has_next: bool = Field(False, description="Whether there are more pages")
    has_prev: bool = Field(False, description="Whether there are previous pages")


class UserResponse(BaseModel):
    """Standard user response model."""
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, description="User's full name")
    is_active: bool = Field(True, description="Whether user account is active")
    is_superuser: bool = Field(False, description="Whether user has superuser privileges")
    created_at: str = Field(..., description="Account creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    last_login: Optional[str] = Field(None, description="Last login timestamp")

    @classmethod
    def from_orm(cls, user) -> "UserResponse":
        """Create response from ORM user object."""
        return cls(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at.isoformat() if user.created_at else None,
            updated_at=user.updated_at.isoformat() if user.updated_at else None,
            last_login=user.last_login.isoformat() if user.last_login else None,
        )


class PostResponse(BaseModel):
    """Standard post response model."""
    id: int = Field(..., description="Post ID")
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content")
    summary: Optional[str] = Field(None, description="Post summary")
    slug: Optional[str] = Field(None, description="URL-friendly slug")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    is_published: bool = Field(False, description="Whether post is published")
    is_featured: bool = Field(False, description="Whether post is featured")
    view_count: int = Field(0, description="Number of views")
    author_id: int = Field(..., description="Author user ID")
    author_name: str = Field(..., description="Author's full name")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    published_at: Optional[str] = Field(None, description="Publication timestamp")


class OrganizationResponse(BaseModel):
    """Standard organization response model."""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    description: Optional[str] = Field(None, description="Organization description")
    owner_id: int = Field(..., description="Owner user ID")
    is_active: bool = Field(True, description="Whether organization is active")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    member_count: int = Field(0, description="Number of members")


class SubscriptionResponse(BaseModel):
    """Standard subscription response model."""
    id: int = Field(..., description="Subscription ID")
    user_id: int = Field(..., description="User ID")
    tier_id: int = Field(..., description="Subscription tier ID")
    status: str = Field(..., description="Subscription status")
    current_period_start: str = Field(..., description="Current billing period start")
    current_period_end: str = Field(..., description="Current billing period end")
    cancel_at_period_end: bool = Field(False, description="Whether subscription cancels at period end")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")


# Specialized Response Models
class BiasDetectionResponse(BaseModel):
    """Response model for bias detection operations."""
    bias_detected: bool = Field(..., description="Whether bias was detected")
    bias_score: float = Field(..., description="Overall bias score (0.0-1.0)")
    bias_types: List[str] = Field(default_factory=list, description="Types of bias detected")
    bias_details: Dict[str, float] = Field(default_factory=dict, description="Detailed bias scores by category")
    mitigation_suggestions: List[str] = Field(default_factory=list, description="Suggested mitigation actions")
    fairness_score: float = Field(..., description="Fairness score (0.0-1.0, higher is better)")
    confidence: float = Field(..., description="Confidence in detection results")
    processing_time: float = Field(..., description="Processing time in seconds")


class AnalyticsResponse(BaseModel):
    """Response model for analytics operations."""
    total_requests: int = Field(..., description="Total number of requests")
    cost_savings_usd: float = Field(..., description="Total cost savings in USD")
    tokens_saved: int = Field(..., description="Total tokens saved")
    violations_blocked: int = Field(..., description="Number of violations blocked")
    productivity_increase_percent: float = Field(..., description="Productivity increase percentage")
    risk_reduction_percent: float = Field(..., description="Risk reduction percentage")
    uptime_percent: float = Field(..., description="System uptime percentage")
    last_updated: str = Field(..., description="Last update timestamp")
    guards_active: int = Field(..., description="Number of active guards")
    data_source: str = Field(..., description="Source of analytics data")


class UploadResponse(BaseModel):
    """Response model for file upload operations."""
    filename: str = Field(..., description="Uploaded file name")
    file_id: str = Field(..., description="Unique file identifier")
    file_size: int = Field(..., description="File size in bytes")
    content_type: str = Field(..., description="File MIME type")
    upload_url: Optional[str] = Field(None, description="Direct access URL")
    expires_at: Optional[str] = Field(None, description="URL expiration timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="File metadata")


class PresignedUploadResponse(BaseModel):
    """Response model for presigned upload URLs."""
    upload_url: str = Field(..., description="Presigned upload URL")
    file_key: str = Field(..., description="File key/path")
    fields: Optional[Dict[str, str]] = Field(None, description="Additional form fields")
    expires_in: int = Field(..., description="URL expiration time in seconds")
    max_size: int = Field(..., description="Maximum allowed file size")
    allowed_types: List[str] = Field(default_factory=list, description="Allowed MIME types")


class FileMetadataResponse(BaseModel):
    """Response model for file metadata operations."""
    file_id: str = Field(..., description="File identifier")
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., description="File size in bytes")
    content_type: str = Field(..., description="MIME type")
    uploaded_at: str = Field(..., description="Upload timestamp")
    uploaded_by: int = Field(..., description="User ID who uploaded the file")
    checksum: Optional[str] = Field(None, description="File checksum")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


# Utility functions for consistent response creation
def create_success_response(
    data: Optional[Dict[str, Any]] = None,
    processing_time: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> StandardResponse:
    """Create a standard success response."""
    return StandardResponse(
        success=True,
        data=data or {},
        processing_time=processing_time,
        metadata=metadata or {}
    )


def create_error_response(
    error: str,
    processing_time: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> StandardResponse:
    """Create a standard error response."""
    return StandardResponse(
        success=False,
        error=error,
        processing_time=processing_time,
        metadata=metadata or {}
    )


def create_guard_response(
    request_id: str,
    service_type: str,
    data: Optional[Dict[str, Any]] = None,
    service_used: Optional[str] = None,
    processing_time: Optional[float] = None,
    confidence_score: Optional[float] = None,
    warnings: Optional[List[str]] = None,
    recommendations: Optional[List[str]] = None,
    error: Optional[str] = None
) -> GuardResponse:
    """Create a standard guard service response."""
    return GuardResponse(
        request_id=request_id,
        service_type=service_type,
        success=error is None,
        data=data or {},
        error=error,
        processing_time=processing_time,
        service_used=service_used,
        confidence_score=confidence_score,
        warnings=warnings or [],
        recommendations=recommendations or []
    )
