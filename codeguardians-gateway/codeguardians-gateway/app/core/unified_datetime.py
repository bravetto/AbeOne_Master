"""
Unified DateTime Utilities - Convergent Emergence

EEAaO: Everything Everywhere All at Once
- Single source of truth for datetime operations
- Elegant convergence of datetime patterns
- Natural flow like water
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Union


def now_utc() -> datetime:
    """
    Get current UTC datetime - single source of truth.
    
    EEAaO: All datetime.now(timezone.utc) calls converge here
    Water flow: Simple, natural, powerful
    """
    return datetime.now(timezone.utc)


def to_iso_string(dt: Optional[datetime]) -> Optional[str]:
    """
    Convert datetime to ISO format string - elegant transformation.
    
    EEAaO: All .isoformat() calls converge here
    Water flow: Natural conversion
    """
    if dt is None:
        return None
    return dt.isoformat()


def to_formatted_string(dt: Optional[datetime], format_str: str = '%Y-%m-%d %H:%M:%S UTC') -> Optional[str]:
    """
    Convert datetime to formatted string - flexible formatting.
    
    EEAaO: All .strftime() calls converge here
    Water flow: Natural formatting
    """
    if dt is None:
        return None
    return dt.strftime(format_str)


def from_iso_string(iso_str: Optional[str]) -> Optional[datetime]:
    """
    Parse ISO format string to datetime - elegant parsing.
    
    EEAaO: All datetime parsing converges here
    Water flow: Natural parsing
    """
    if iso_str is None:
        return None
    try:
        return datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return None


def add_days(dt: datetime, days: int) -> datetime:
    """
    Add days to datetime - elegant arithmetic.
    
    EEAaO: All timedelta operations converge here
    Water flow: Natural addition
    """
    return dt + timedelta(days=days)


def days_until(target: Optional[datetime], from_dt: Optional[datetime] = None) -> int:
    """
    Calculate days until target datetime - elegant calculation.
    
    EEAaO: All date difference calculations converge here
    Water flow: Natural calculation
    """
    if target is None:
        return 0
    if from_dt is None:
        from_dt = now_utc()
    delta = target - from_dt
    return delta.days if delta.days > 0 else 0


def format_datetime_fields(data: dict, fields: list[str]) -> dict:
    """
    Format datetime fields in a dictionary - elegant batch formatting.
    
    EEAaO: All datetime field formatting converges here
    Water flow: Natural batch transformation
    
    Example:
        data = {"created_at": datetime.now(), "updated_at": datetime.now()}
        formatted = format_datetime_fields(data, ["created_at", "updated_at"])
    """
    result = data.copy()
    for field in fields:
        if field in result and isinstance(result[field], datetime):
            result[field] = to_iso_string(result[field])
    return result

