"""
Comprehensive Audit Logging Module

Provides audit logging for all sensitive operations.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.models import AuditLog
from app.core.database import get_db
from app.utils.logging import get_logger

logger = get_logger(__name__)


async def log_audit_event(
    db: AsyncSession,
    user_id: Optional[int],
    organization_id: Optional[str],
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    request: Optional[Any] = None
) -> None:
    """
    Log an audit event.
    
    Args:
        db: Database session
        user_id: User ID performing the action
        organization_id: Organization ID
        action: Action performed (e.g., 'create', 'update', 'delete')
        resource_type: Type of resource (e.g., 'user', 'file', 'subscription')
        resource_id: ID of the resource
        details: Additional details about the action
        ip_address: IP address of the requester (can be extracted from request if provided)
        user_agent: User agent string (can be extracted from request if provided)
        request: Optional FastAPI Request object to extract IP and user agent
    """
    # Extract IP and user agent from request if not provided
    if request and not ip_address:
        ip_address = request.client.host if request.client else None
    if request and not user_agent:
        user_agent = request.headers.get("user-agent")
    
    try:
        audit_log = AuditLog(
            user_id=user_id,
            organization_id=organization_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.now(timezone.utc)
        )
        
        db.add(audit_log)
        await db.commit()
        
        logger.info(
            f"Audit log: {action} {resource_type} "
            f"(user={user_id}, org={organization_id})"
        )
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to log audit event: {e}")


async def log_user_deactivation(
    db: AsyncSession,
    admin_user_id: int,
    target_user_id: int,
    organization_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    request: Optional[Any] = None
) -> None:
    """Log user deactivation."""
    await log_audit_event(
        db=db,
        user_id=admin_user_id,
        organization_id=organization_id,
        action="deactivate",
        resource_type="user",
        resource_id=str(target_user_id),
        details={"target_user_id": target_user_id},
        ip_address=ip_address,
        request=request
    )


async def log_file_deletion(
    db: AsyncSession,
    user_id: int,
    file_id: str,
    organization_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    request: Optional[Any] = None
) -> None:
    """Log file deletion."""
    await log_audit_event(
        db=db,
        user_id=user_id,
        organization_id=organization_id,
        action="delete",
        resource_type="file",
        resource_id=file_id,
        details={"file_id": file_id},
        ip_address=ip_address,
        request=request
    )


async def log_configuration_change(
    db: AsyncSession,
    user_id: int,
    config_key: str,
    old_value: Any,
    new_value: Any,
    organization_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    request: Optional[Any] = None
) -> None:
    """Log configuration change."""
    await log_audit_event(
        db=db,
        user_id=user_id,
        organization_id=organization_id,
        action="update",
        resource_type="configuration",
        resource_id=config_key,
        details={
            "config_key": config_key,
            "old_value": str(old_value),
            "new_value": str(new_value)
        },
        ip_address=ip_address,
        request=request
    )


async def log_subscription_change(
    db: AsyncSession,
    user_id: int,
    subscription_id: str,
    action: str,
    details: Dict[str, Any],
    organization_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    request: Optional[Any] = None
) -> None:
    """Log subscription change."""
    await log_audit_event(
        db=db,
        user_id=user_id,
        organization_id=organization_id,
        action=action,
        resource_type="subscription",
        resource_id=subscription_id,
        details=details,
        ip_address=ip_address,
        request=request
    )

