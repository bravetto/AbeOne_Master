"""
Unified Pagination - Convergent Emergence

EEAaO: Everything Everywhere All at Once
- Single elegant pagination solution
- Natural flow like water
"""

from typing import Optional, Dict, Any, Callable
from fastapi import Query, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logging import get_logger

logger = get_logger(__name__)


class PaginationParams:
    """Unified pagination parameters - convergent emergence."""
    
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
        sort_by: Optional[str] = Query(None, description="Field to sort by"),
        sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
        search: Optional[str] = Query(None, description="Search query")
    ):
        self.skip = skip
        self.limit = limit
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.search = search


async def apply_pagination(
    query,
    pagination: PaginationParams,
    db: AsyncSession,
    model
) -> Dict[str, Any]:
    """
    Apply pagination to query - elegant convergence.
    
    EEAaO: Single elegant solution for all pagination needs
    """
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    
    # Apply sorting
    if pagination.sort_by and hasattr(model, pagination.sort_by):
        sort_field = getattr(model, pagination.sort_by)
        if pagination.sort_order == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())
    
    # Apply pagination
    query = query.offset(pagination.skip).limit(pagination.limit)
    
    # Execute
    result = await db.execute(query)
    items = result.scalars().all()
    
    return {
        "items": items,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
        "has_more": (pagination.skip + pagination.limit) < total
    }


def get_pagination_dependency() -> PaginationParams:
    """Get pagination dependency - water flow pattern."""
    return PaginationParams()

