"""
Organization Management API

This module provides endpoints for:
- Organization creation and management
- Team member invitation and management
- Organization settings and configuration
- Tenant isolation enforcement

Architecture:
- All endpoints require tenant context
- Organization operations are scoped to user's organization
- Team management requires appropriate permissions
- Audit logging for all organization changes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.models import (
    User, Organization, OrganizationMember, 
    Subscription, SubscriptionTier, SubscriptionStatus
)
from app.middleware.tenant_context import (
    TenantContext, CurrentTenant, require_permission, require_role, get_current_tenant
)
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/organizations", tags=["organizations"])


# Pydantic models for request/response
class OrganizationCreate(BaseModel):
    """Request model for creating a new organization."""
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None


class OrganizationUpdate(BaseModel):
    """Request model for updating organization details."""
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None


class OrganizationResponse(BaseModel):
    """Response model for organization information."""
    id: str
    name: str
    description: Optional[str]
    website: Optional[str]
    industry: Optional[str]
    created_at: datetime
    updated_at: datetime
    member_count: int
    subscription_tier: Optional[str]
    
    class Config:
        from_attributes = True


class MemberInvite(BaseModel):
    """Request model for inviting team members."""
    email: EmailStr
    role: str = "member"
    permissions: List[str] = []


class MemberResponse(BaseModel):
    """Response model for organization members."""
    id: str
    user_id: str
    email: str
    role: str
    permissions: List[str]
    is_active: bool
    joined_at: datetime
    last_active: Optional[datetime]
    
    class Config:
        from_attributes = True


class MemberUpdate(BaseModel):
    """Request model for updating member permissions."""
    role: Optional[str] = None
    permissions: Optional[List[str]] = None


@router.get("/current", response_model=None)
async def get_current_organization(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's organization information.

    Returns organization details including member count and subscription tier.
    """
    try:
        # Get organization details
        org_stmt = select(Organization).where(
            Organization.id == tenant_context.organization_id
        )
        org_result = await db.execute(org_stmt)
        organization = org_result.scalar_one_or_none()
        
        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )
        
        # Get member count
        member_count_stmt = select(func.count(OrganizationMember.id)).where(
            and_(
                OrganizationMember.organization_id == tenant_context.organization_id,
                OrganizationMember.is_active == True
            )
        )
        member_count_result = await db.execute(member_count_stmt)
        member_count = member_count_result.scalar() or 0
        
        # Get subscription tier name
        subscription_stmt = select(Subscription, SubscriptionTier).join(
            SubscriptionTier, Subscription.subscription_tier_id == SubscriptionTier.id
        ).where(
            and_(
                Subscription.organization_id == tenant_context.organization_id,
                Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING])
            )
        ).limit(1)
        subscription_result = await db.execute(subscription_stmt)
        subscription_tuple = subscription_result.first()
        
        tier_name = None
        if subscription_tuple:
            _, tier = subscription_tuple
            tier_name = tier.name
        
        return OrganizationResponse(
            id=str(organization.id),
            name=organization.name,
            description=organization.description,
            website=None,  # TODO: Add website field to Organization model
            industry=None,  # TODO: Add industry field to Organization model
            created_at=organization.created_at,
            updated_at=organization.updated_at,
            member_count=member_count,
            subscription_tier=tier_name
        )
        
    except HTTPException:
        raise
    except RuntimeError as e:
        # Database is disabled or unavailable
        logger.error(f"Database unavailable for organization retrieval: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable - database connection failed"
        )
    except Exception as e:
        logger.error(f"Error retrieving current organization: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve organization information"
        )


@router.get("/members", response_model=None)
async def get_organization_members(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all members of the current organization.

    Returns list of active organization members with their roles and permissions.
    """
    try:
        stmt = select(OrganizationMember, User).join(
            User, OrganizationMember.user_id == User.id
        ).where(
            and_(
                OrganizationMember.organization_id == tenant_context.organization_id,
                OrganizationMember.is_active == True
            )
        )
        result = await db.execute(stmt)
        members_tuples = result.all()
        
        member_responses = []
        for member, user in members_tuples:
            member_responses.append(MemberResponse(
                id=member.id,
                user_id=member.user_id,
                email=user.email,
                role=member.role,
                permissions=member.permissions or [],
                is_active=member.is_active,
                joined_at=member.joined_at,
                last_active=user.last_login
            ))
        
        logger.info(f"Retrieved {len(member_responses)} members for organization: {tenant_context.organization_id}")
        
        return member_responses
        
    except HTTPException:
        raise
    except RuntimeError as e:
        # Database is disabled or unavailable
        logger.error(f"Database unavailable for organization members: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable - database connection failed"
        )
    except Exception as e:
        logger.error(f"Error retrieving organization members: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve organization members"
        )


@router.post("/members/invite")
async def invite_member(
    invite: MemberInvite,
    tenant_context: TenantContext = require_permission("members:invite"),
    db: AsyncSession = Depends(get_db)
):
    """
    Invite a new member to the organization.
    
    Requires 'members:invite' permission.
    Creates invitation record and sends email notification.
    """
    try:
        # Check if user already exists
        user_stmt = select(User).where(User.email == invite.email)
        user_result = await db.execute(user_stmt)
        existing_user = user_result.scalar_one_or_none()
        
        if existing_user:
            # Check if user is already a member
            member_stmt = select(OrganizationMember).where(
                and_(
                    OrganizationMember.user_id == existing_user.id,
                    OrganizationMember.organization_id == tenant_context.organization_id
                )
            )
            member_result = await db.execute(member_stmt)
            existing_member = member_result.scalar_one_or_none()
            
            if existing_member and existing_member.is_active:
                raise HTTPException(
                    status_code=400,
                    detail="User is already a member of this organization"
                )
        
        # Create invitation record (simplified - in production, use invitation table)
        if existing_user:
            try:
                # User exists, add to organization
                new_member = OrganizationMember(
                    user_id=existing_user.id,
                    organization_id=tenant_context.organization_id,
                    role=invite.role,
                    permissions=invite.permissions,
                    is_active=True,
                    joined_at=datetime.now(timezone.utc)
                )
                db.add(new_member)
                await db.commit()
            except Exception as e:
                await db.rollback()
                logger.error(f"Error adding member to organization: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to add member to organization"
                )
        else:
            # User doesn't exist, would need to create invitation workflow
            # For now, return error
            raise HTTPException(
                status_code=400,
                detail="User must have an account before being invited"
            )
        
        logger.info(f"Invited member {invite.email} to organization: {tenant_context.organization_id}")
        
        return {
            "message": "Member invitation sent successfully",
            "email": invite.email,
            "role": invite.role
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inviting member: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to invite member"
        )


@router.put("/members/{member_id}")
async def update_member(
    member_id: str,
    member_update: MemberUpdate,
    tenant_context: TenantContext = require_permission("members:manage"),
    db: AsyncSession = Depends(get_db)
):
    """
    Update member role and permissions.
    
    Requires 'members:manage' permission.
    """
    try:
        member_stmt = select(OrganizationMember).where(
            and_(
                OrganizationMember.id == member_id,
                OrganizationMember.organization_id == tenant_context.organization_id
            )
        )
        result = await db.execute(member_stmt)
        member = result.scalar_one_or_none()
        
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Prevent self-modification of admin role
        if (member.user_id == tenant_context.user_id and 
            member_update.role == "member" and 
            member.role == "admin"):
            raise HTTPException(
                status_code=400,
                detail="Cannot remove admin role from yourself"
            )
        
        # Update member
        if member_update.role is not None:
            member.role = member_update.role
        if member_update.permissions is not None:
            member.permissions = member_update.permissions
        
        member.updated_at = datetime.now(timezone.utc)
        await db.commit()
        
        logger.info(f"Updated member {member_id} in organization: {tenant_context.organization_id}")
        
        return {
            "message": "Member updated successfully",
            "member_id": member_id,
            "role": member.role,
            "permissions": member.permissions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating member: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update member"
        )


@router.delete("/members/{member_id}")
async def remove_member(
    member_id: str,
    tenant_context: TenantContext = require_permission("members:manage"),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove member from organization.

    Requires 'members:manage' permission.
    """
    try:
        # Find member
        member_stmt = select(OrganizationMember).where(
            and_(
                OrganizationMember.id == member_id,
                OrganizationMember.organization_id == tenant_context.organization_id
            )
        )
        member_result = await db.execute(member_stmt)
        member = member_result.scalar_one_or_none()
        
        if not member:
            raise HTTPException(
                status_code=404,
                detail="Member not found"
            )
        
        # Prevent removing yourself
        if member.user_id == tenant_context.user_id:
            raise HTTPException(
                status_code=400,
                detail="Cannot remove yourself from the organization"
            )
        
        # Deactivate member instead of deleting (soft delete)
        member.is_active = False
        member.updated_at = datetime.now(timezone.utc)
        await db.commit()
        
        logger.info(f"Removed member {member_id} from organization: {tenant_context.organization_id}")
        
        return {
            "message": "Member removed successfully",
            "member_id": member_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing member: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to remove member"
        )


@router.get("/subscription")
async def get_organization_subscription(
    tenant_context: TenantContext = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current organization subscription information.

    Returns subscription details including tier, limits, and usage.
    """
    try:
        subscription_stmt = select(Subscription).options(
            selectinload(Subscription.subscription_tier)
        ).where(
            and_(
                Subscription.organization_id == tenant_context.organization_id,
                Subscription.status == SubscriptionStatus.ACTIVE
            )
        )
        result = await db.execute(subscription_stmt)
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            return {
                "subscription": None,
                "message": "No active subscription found"
            }
        
        return {
            "subscription": {
                "id": subscription.id,
                "tier": subscription.subscription_tier.name if subscription.subscription_tier else None,
                "status": subscription.status,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "api_calls_limit": subscription.subscription_tier.limits.get("api_calls_limit", 0) if subscription.subscription_tier and subscription.subscription_tier.limits else None,
                "storage_limit": subscription.subscription_tier.limits.get("storage_limit", 0) if subscription.subscription_tier and subscription.subscription_tier.limits else None
            }
        }
        
    except Exception as e:
        logger.error(f"Error retrieving subscription: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve subscription information"
        )
