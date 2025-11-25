"""
Unified Response Models - Convergent Emergence

EEAaO: Everything Everywhere All at Once
- Single source of truth for response patterns
- Elegant convergence of all response structures
- Natural flow like water
"""

from typing import List, Optional, Generic, TypeVar, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime

from app.core.unified_datetime import now_utc, to_iso_string

T = TypeVar('T')


class BaseResponse(BaseModel):
    """Base response model - convergent emergence."""
    success: bool = True
    timestamp: datetime = Field(default_factory=now_utc)
    request_id: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Unified paginated response - elegant convergence."""
    items: List[T]
    total: int
    skip: int = 0
    limit: int = 100
    has_more: bool = Field(False, computed=True)
    
    def __init__(self, **data):
        super().__init__(**data)
        self.has_more = (self.skip + self.limit) < self.total


class StandardResponse(BaseModel, Generic[T]):
    """Standard response wrapper - water flow pattern."""
    data: T
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ErrorResponseDetail(BaseModel):
    """Unified error detail structure."""
    error_code: str
    message: str
    field: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class StandardErrorResponse(BaseResponse):
    """Standard error response - convergent emergence."""
    success: bool = False
    error: ErrorResponseDetail
    details: Optional[Dict[str, Any]] = None


def create_response(data: Any, message: Optional[str] = None, request_id: Optional[str] = None) -> Dict[str, Any]:
    """Create standard response - elegant helper."""
    return {
        "success": True,
        "data": data,
        "message": message,
        "timestamp": to_iso_string(now_utc()),
        "request_id": request_id
    }


def create_paginated_response(
    items: List[Any],
    total: int,
    skip: int = 0,
    limit: int = 100
) -> Dict[str, Any]:
    """Create paginated response - water flow pattern."""
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total
    }

