"""
AI Guardians Legal & Compliance API

Complete legal compliance endpoints for Terms of Service, Privacy Policy, GDPR, and audit logging.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_, func, delete

from app.core.database import get_db
from app.core.models import User, Organization, AuditLog
from app.middleware.tenant_context import TenantContext, CurrentTenant, get_current_tenant
from app.core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Legal & Compliance"])

# Get settings
settings = get_settings()


@router.get("/terms-of-service")
async def get_terms_of_service():
    """
    Get Terms of Service document.
    
    Returns the current Terms of Service document.
    """
    return {
        "version": "1.0",
        "last_updated": "2024-01-01T00:00:00Z",
        "content": """
        AI GUARDIANS TERMS OF SERVICE
        
        1. ACCEPTANCE OF TERMS
        By accessing and using AI Guardians services, you accept and agree to be bound by the terms and provision of this agreement.
        
        2. DESCRIPTION OF SERVICE
        AI Guardians provides AI-powered security and validation services through our API platform.
        
        3. USER ACCOUNTS
        You are responsible for maintaining the confidentiality of your account and password.
        
        4. ACCEPTABLE USE
        You agree not to use the service for any unlawful purpose or any purpose prohibited under this clause.
        
        5. PAYMENT TERMS
        Subscription fees are billed in advance and are non-refundable except as required by law.
        
        6. INTELLECTUAL PROPERTY
        The service and its original content, features, and functionality are owned by AI Guardians.
        
        7. TERMINATION
        We may terminate or suspend your account immediately, without prior notice, for any reason.
        
        8. DISCLAIMER
        The service is provided on an "AS IS" and "AS AVAILABLE" basis.
        
        9. LIMITATION OF LIABILITY
        In no event shall AI Guardians be liable for any indirect, incidental, special, consequential, or punitive damages.
        
        10. GOVERNING LAW
        These terms shall be governed by and construed in accordance with the laws of the United States.
        """,
        "acceptance_required": True
    }


@router.get("/privacy-policy")
async def get_privacy_policy():
    """
    Get Privacy Policy document.
    
    Returns the current Privacy Policy document.
    """
    return {
        "version": "1.0",
        "last_updated": "2024-01-01T00:00:00Z",
        "content": """
        AI GUARDIANS PRIVACY POLICY
        
        1. INFORMATION WE COLLECT
        We collect information you provide directly to us, such as when you create an account, use our services, or contact us.
        
        2. HOW WE USE YOUR INFORMATION
        We use the information we collect to provide, maintain, and improve our services.
        
        3. INFORMATION SHARING
        We do not sell, trade, or otherwise transfer your personal information to third parties without your consent.
        
        4. DATA SECURITY
        We implement appropriate security measures to protect your personal information.
        
        5. DATA RETENTION
        We retain your personal information for as long as necessary to provide our services and comply with legal obligations.
        
        6. YOUR RIGHTS
        You have the right to access, update, or delete your personal information.
        
        7. COOKIES
        We use cookies and similar technologies to enhance your experience on our platform.
        
        8. THIRD-PARTY SERVICES
        Our service may contain links to third-party websites or services.
        
        9. CHILDREN'S PRIVACY
        Our service is not intended for children under 13 years of age.
        
        10. CHANGES TO THIS POLICY
        We may update this privacy policy from time to time.
        """,
        "acceptance_required": True
    }


@router.get("/cookie-policy")
async def get_cookie_policy():
    """
    Get Cookie Policy document.
    
    Returns the current Cookie Policy document.
    """
    return {
        "version": "1.0",
        "last_updated": "2024-01-01T00:00:00Z",
        "content": """
        AI GUARDIANS COOKIE POLICY
        
        1. WHAT ARE COOKIES
        Cookies are small text files that are placed on your device when you visit our website.
        
        2. HOW WE USE COOKIES
        We use cookies to enhance your experience, analyze usage, and provide personalized content.
        
        3. TYPES OF COOKIES
        - Essential cookies: Required for basic website functionality
        - Analytics cookies: Help us understand how visitors use our website
        - Marketing cookies: Used to deliver relevant advertisements
        
        4. COOKIE MANAGEMENT
        You can control and delete cookies through your browser settings.
        
        5. THIRD-PARTY COOKIES
        We may use third-party services that set their own cookies.
        """,
        "acceptance_required": False
    }


@router.post("/accept-tos")
async def accept_terms_of_service(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Accept Terms of Service.

    Records user acceptance of Terms of Service.
    """
    try:
        # Update user's ToS acceptance
        stmt = select(User).where(User.id == tenant_context.user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.tos_accepted_at = datetime.now(timezone.utc)
        user.tos_version = "1.0"
        await db.commit()
        
        # Log acceptance
        audit_log = AuditLog(
            user_id=tenant_context.user_id,
            organization_id=tenant_context.organization_id,
            action="tos_accepted",
            resource_type="legal",
            resource_id="tos_1.0",
            details={"version": "1.0", "accepted_at": datetime.now(timezone.utc).isoformat()}
        )
        db.add(audit_log)
        await db.commit()
        
        logger.info(f"User {tenant_context.user_id} accepted Terms of Service")
        
        return {
            "status": "accepted",
            "version": "1.0",
            "accepted_at": user.tos_accepted_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to accept Terms of Service: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to accept Terms of Service")


@router.get("/gdpr/export")
async def export_user_data(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Export user data (GDPR compliance).
    
    Exports all personal data associated with the user.
    """
    try:
        user_stmt = select(User).where(User.id == tenant_context.user_id)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's organization
        org_stmt = select(Organization).where(Organization.id == tenant_context.organization_id)
        org_result = await db.execute(org_stmt)
        organization = org_result.scalar_one_or_none()
        
        # Get audit logs
        audit_stmt = select(AuditLog).where(
            AuditLog.user_id == tenant_context.user_id
        ).order_by(desc(AuditLog.created_at))
        audit_result = await db.execute(audit_stmt)
        audit_logs = audit_result.scalars().all()
        
        # Compile export data
        export_data = {
            "export_date": datetime.now(timezone.utc).isoformat(),
            "user_data": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat(),
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "tos_accepted_at": user.tos_accepted_at.isoformat() if user.tos_accepted_at else None,
                "tos_version": user.tos_version
            },
            "organization_data": {
                "id": str(organization.id),
                "name": organization.name,
                "created_at": organization.created_at.isoformat(),
                "subscription_status": organization.subscription_status
            } if organization else None,
            "audit_logs": [
                {
                    "id": str(log.id),
                    "action": log.action,
                    "resource_type": log.resource_type,
                    "resource_id": log.resource_id,
                    "details": log.details,
                    "created_at": log.created_at.isoformat()
                }
                for log in audit_logs
            ]
        }
        
        # Log export request
        audit_log = AuditLog(
            user_id=tenant_context.user_id,
            organization_id=tenant_context.organization_id,
            action="data_export_requested",
            resource_type="gdpr",
            resource_id="export",
            details={"export_date": datetime.now(timezone.utc).isoformat()}
        )
        db.add(audit_log)
        await db.commit()
        
        logger.info(f"Data export requested by user {tenant_context.user_id}")
        
        return export_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export user data: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to export user data")


@router.delete("/gdpr/delete")
async def delete_user_data(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete user data (GDPR compliance).
    
    Permanently deletes all personal data associated with the user.
    """
    try:
        user_stmt = select(User).where(User.id == tenant_context.user_id)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Anonymize user data instead of hard delete (for audit purposes)
        user.username = f"deleted_user_{user.id}"
        user.email = f"deleted_{user.id}@example.com"
        user.is_active = False
        user.deleted_at = datetime.now(timezone.utc)
        
        # Delete audit logs
        delete_stmt = delete(AuditLog).where(AuditLog.user_id == tenant_context.user_id)
        await db.execute(delete_stmt)
        await db.commit()
        
        # Log deletion request
        audit_log = AuditLog(
            user_id=tenant_context.user_id,
            organization_id=tenant_context.organization_id,
            action="data_deletion_requested",
            resource_type="gdpr",
            resource_id="delete",
            details={"deleted_at": datetime.now(timezone.utc).isoformat()}
        )
        db.add(audit_log)
        await db.commit()
        
        logger.info(f"Data deletion requested by user {tenant_context.user_id}")
        
        return {
            "status": "deleted",
            "deleted_at": datetime.now(timezone.utc).isoformat(),
            "message": "Your personal data has been anonymized and deleted."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete user data: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete user data")


@router.get("/audit-logs")
async def get_audit_logs(
    tenant_context: TenantContext = Depends(get_current_tenant),
    limit: int = 100,
    offset: int = 0,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get audit logs for the organization.
    
    Returns paginated audit logs with optional filtering.
    """
    try:
        stmt = select(AuditLog).where(
            AuditLog.organization_id == tenant_context.organization_id
        )
        
        # Apply filters
        if action:
            stmt = stmt.where(AuditLog.action == action)
        if resource_type:
            stmt = stmt.where(AuditLog.resource_type == resource_type)
        if start_date:
            stmt = stmt.where(AuditLog.created_at >= start_date)
        if end_date:
            stmt = stmt.where(AuditLog.created_at <= end_date)
        
        # Get total count
        count_stmt = select(func.count(AuditLog.id)).where(
            AuditLog.organization_id == tenant_context.organization_id
        )
        if action:
            count_stmt = count_stmt.where(AuditLog.action == action)
        if resource_type:
            count_stmt = count_stmt.where(AuditLog.resource_type == resource_type)
        if start_date:
            count_stmt = count_stmt.where(AuditLog.created_at >= start_date)
        if end_date:
            count_stmt = count_stmt.where(AuditLog.created_at <= end_date)
        
        total_result = await db.execute(count_stmt)
        total_count = total_result.scalar() or 0
        
        # Get paginated results
        logs_stmt = stmt.order_by(desc(AuditLog.created_at)).offset(offset).limit(limit)
        logs_result = await db.execute(logs_stmt)
        logs = logs_result.scalars().all()
        
        return {
            "logs": [
                {
                    "id": str(log.id),
                    "user_id": str(log.user_id),
                    "action": log.action,
                    "resource_type": log.resource_type,
                    "resource_id": log.resource_id,
                    "details": log.details,
                    "created_at": log.created_at.isoformat()
                }
                for log in logs
            ],
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": offset + limit < total_count
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get audit logs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get audit logs")


@router.get("/compliance-status")
async def get_compliance_status(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get compliance status for the organization.
    
    Returns current compliance status including ToS acceptance, data retention, etc.
    """
    try:
        user_stmt = select(User).where(User.id == tenant_context.user_id)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        org_stmt = select(Organization).where(Organization.id == tenant_context.organization_id)
        org_result = await db.execute(org_stmt)
        organization = org_result.scalar_one_or_none()
        
        # Check ToS acceptance
        tos_accepted = user.tos_accepted_at is not None
        tos_version = user.tos_version
        
        # Check data retention compliance
        data_retention_days = 90  # Example: 90 days
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=data_retention_days)
        
        old_logs_stmt = select(func.count(AuditLog.id)).where(
            and_(
                AuditLog.organization_id == tenant_context.organization_id,
                AuditLog.created_at < cutoff_date
            )
        )
        old_logs_result = await db.execute(old_logs_stmt)
        old_audit_logs = old_logs_result.scalar() or 0
        
        return {
            "organization_id": str(tenant_context.organization_id),
            "compliance_status": {
                "tos_accepted": tos_accepted,
                "tos_version": tos_version,
                "tos_accepted_at": user.tos_accepted_at.isoformat() if user.tos_accepted_at else None,
                "data_retention_compliant": old_audit_logs == 0,
                "old_audit_logs_count": old_audit_logs,
                "data_retention_days": data_retention_days
            },
            "recommendations": [
                "Accept Terms of Service" if not tos_accepted else None,
                "Review data retention policy" if old_audit_logs > 0 else None,
                "Update privacy settings" if not user.privacy_settings else None
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get compliance status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get compliance status")


@router.post("/data-retention/cleanup")
async def cleanup_old_data(
    tenant_context: TenantContext = Depends(get_current_tenant),
    days_to_keep: int = 90,
    db: AsyncSession = Depends(get_db)
):
    """
    Clean up old data for compliance.
    
    Removes data older than specified days to maintain compliance.
    """
    try:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)
        
        # Delete old audit logs
        delete_stmt = delete(AuditLog).where(
            and_(
                AuditLog.organization_id == tenant_context.organization_id,
                AuditLog.created_at < cutoff_date
            )
        )
        result = await db.execute(delete_stmt)
        await db.commit()
        deleted_count = result.rowcount
        
        # Log cleanup action
        audit_log = AuditLog(
            user_id=tenant_context.user_id,
            organization_id=tenant_context.organization_id,
            action="data_cleanup",
            resource_type="compliance",
            resource_id="retention",
            details={
                "days_to_keep": days_to_keep,
                "deleted_count": deleted_count,
                "cutoff_date": cutoff_date.isoformat()
            }
        )
        db.add(audit_log)
        await db.commit()
        
        logger.info(f"Data cleanup completed for organization {tenant_context.organization_id}: {deleted_count} records deleted")
        
        return {
            "status": "completed",
            "deleted_count": deleted_count,
            "days_to_keep": days_to_keep,
            "cutoff_date": cutoff_date.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to cleanup old data: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to cleanup old data")
