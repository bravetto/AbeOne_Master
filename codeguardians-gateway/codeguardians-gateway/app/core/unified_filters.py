"""
Unified Filtering - Convergent Emergence

EEAaO: Everything Everywhere All at Once
- Single elegant filtering solution
- Natural flow like water
"""

from typing import Optional, Dict, Any, List
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logging import get_logger

logger = get_logger(__name__)


class FilterBuilder:
    """
    Unified filter builder - convergent emergence.
    
    EEAaO: Single elegant solution for all filtering needs
    """
    
    def __init__(self, model):
        self.model = model
        self.conditions = []
    
    def equals(self, field: str, value: Any):
        """Add equals filter."""
        if hasattr(self.model, field):
            self.conditions.append(getattr(self.model, field) == value)
        return self
    
    def contains(self, field: str, value: str):
        """Add contains filter (case-insensitive)."""
        if hasattr(self.model, field):
            self.conditions.append(getattr(self.model, field).ilike(f"%{value}%"))
        return self
    
    def in_list(self, field: str, values: List[Any]):
        """Add in-list filter."""
        if hasattr(self.model, field):
            self.conditions.append(getattr(self.model, field).in_(values))
        return self
    
    def greater_than(self, field: str, value: Any):
        """Add greater than filter."""
        if hasattr(self.model, field):
            self.conditions.append(getattr(self.model, field) > value)
        return self
    
    def less_than(self, field: str, value: Any):
        """Add less than filter."""
        if hasattr(self.model, field):
            self.conditions.append(getattr(self.model, field) < value)
        return self
    
    def apply(self, query):
        """Apply filters to query."""
        if self.conditions:
            return query.where(and_(*self.conditions))
        return query


def build_filters(model, filter_dict: Dict[str, Any]) -> FilterBuilder:
    """
    Build filters from dictionary - elegant helper.
    
    EEAaO: Natural flow like water
    """
    builder = FilterBuilder(model)
    
    for field, value in filter_dict.items():
        if value is None:
            continue
        
        if isinstance(value, list):
            builder.in_list(field, value)
        elif isinstance(value, str) and '%' in value:
            builder.contains(field, value.replace('%', ''))
        elif isinstance(value, (int, float)):
            builder.equals(field, value)
        else:
            builder.equals(field, value)
    
    return builder

