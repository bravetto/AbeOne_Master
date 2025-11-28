"""
SQLAlchemy models for the application.

This module defines the database models using SQLAlchemy ORM with
proper relationships, constraints, and validation.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, 
    ForeignKey, Index, UniqueConstraint, CheckConstraint,
    Numeric, JSON, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
import re
import enum

Base = declarative_base()


# Enums for SaaS business logic
class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"
    TRIALING = "trialing"


class OrganizationRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    REFUNDED = "refunded"


class User(Base):
    """User model for authentication and user management."""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # User information
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    
    # Clerk integration
    clerk_user_id = Column(String(255), unique=True, index=True, nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    username = Column(String(255), unique=True, nullable=True)
    locale = Column(String(10), nullable=True)
    last_active_at = Column(DateTime(timezone=True), nullable=True)
    last_sign_in_at = Column(DateTime(timezone=True), nullable=True)
    password_enabled = Column(Boolean, default=True, nullable=True)
    two_factor_enabled = Column(Boolean, default=False, nullable=True)
    totp_enabled = Column(Boolean, default=False, nullable=True)
    backup_code_enabled = Column(Boolean, default=False, nullable=True)
    banned = Column(Boolean, default=False, nullable=True)
    locked = Column(Boolean, default=False, nullable=True)
    verification_attempts_remaining = Column(Integer, default=100, nullable=True)
    primary_email_address_id = Column(String(255), nullable=True)
    primary_phone_number_id = Column(String(255), nullable=True)
    primary_web3_wallet_id = Column(String(255), nullable=True)
    external_id = Column(String(255), nullable=True)
    clerk_created_at = Column(DateTime(timezone=True), nullable=True)
    clerk_updated_at = Column(DateTime(timezone=True), nullable=True)
    clerk_private_metadata = Column(JSON, nullable=True)
    clerk_public_metadata = Column(JSON, nullable=True)
    clerk_unsafe_metadata = Column(JSON, nullable=True)
    
    # Stripe integration
    stripe_customer_id = Column(String(255), unique=True, index=True, nullable=True)
    
    # User status
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    organization_memberships = relationship("OrganizationMember", back_populates="user", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        Index('ix_users_email_active', 'email', 'is_active'),
        Index('ix_users_first_name', 'first_name'),
        Index('ix_users_last_name', 'last_name'),
        Index('ix_users_username', 'username', unique=True),
        Index('ix_users_external_id', 'external_id'),
        Index('REPLACE_ME', 'primary_email_address_id'),
        CheckConstraint('length(email) >= 5', name='ck_users_email_length'),
        CheckConstraint('length(full_name) >= 1', name='ck_users_full_name_length'),
    )
    
    @validates('email')
    def validate_email(self, key, email):
        """Validate email format."""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('Invalid email format')
        return email.lower()
    
    @validates('full_name')
    def validate_full_name(self, key, full_name):
        """Validate full name."""
        if not full_name or len(full_name.strip()) < 1:
            raise ValueError('Full name cannot be empty')
        return full_name.strip()
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
    
    def __str__(self):
        return f"User(id={self.id}, email={self.email})"


class Post(Base):
    """Post model for content management."""
    
    __tablename__ = "posts"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Post content
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(String(500), nullable=True)
    
    # Post status
    is_published = Column(Boolean, default=False, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # Metadata
    slug = Column(String(255), unique=True, index=True, nullable=True)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    view_count = Column(Integer, default=0, nullable=False)
    
    # Relationships
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="posts")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Constraints
    __table_args__ = (
        Index('ix_posts_author_created', 'author_id', 'created_at'),
        Index('ix_posts_published_created', 'is_published', 'created_at'),
        Index('ix_posts_slug', 'slug'),
        CheckConstraint('length(title) >= 1', name='ck_posts_title_length'),
        CheckConstraint('length(content) >= 10', name='ck_posts_content_length'),
        CheckConstraint('view_count >= 0', name='ck_posts_view_count_positive'),
    )
    
    @validates('title')
    def validate_title(self, key, title):
        """Validate post title."""
        if not title or len(title.strip()) < 1:
            raise ValueError('Post title cannot be empty')
        return title.strip()
    
    @validates('content')
    def validate_content(self, key, content):
        """Validate post content."""
        if not content or len(content.strip()) < 10:
            raise ValueError('Post content must be at least 10 characters')
        return content.strip()
    
    @validates('slug')
    def validate_slug(self, key, slug):
        """Validate and generate slug."""
        if slug:
            # Ensure slug is URL-safe
            slug = re.sub(r'[^a-zA-Z0-9\-_]', '-', slug.lower())
            slug = re.sub(r'-+', '-', slug).strip('-')
        return slug
    
    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title})>"
    
    def __str__(self):
        return f"Post(id={self.id}, title={self.title})"


class AuditLog(Base):
    """Audit log for tracking changes and actions."""
    
    __tablename__ = "audit_logs"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Audit information
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(100), nullable=True)
    
    # Change details
    old_values = Column(Text, nullable=True)  # JSON string
    new_values = Column(Text, nullable=True)  # JSON string
    
    # Request context
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(String(500), nullable=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Constraints
    __table_args__ = (
        Index('ix_audit_logs_user_created', 'user_id', 'created_at'),
        Index('ix_audit_logs_resource', 'resource_type', 'resource_id'),
        Index('ix_audit_logs_action', 'action', 'created_at'),
    )
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, user_id={self.user_id})>"


class Session(Base):
    """User session management."""
    
    __tablename__ = "sessions"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Session information
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Session data
    data = Column(Text, nullable=True)  # JSON string
    
    # Session metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # Constraints
    __table_args__ = (
        Index('ix_sessions_user_active', 'user_id', 'is_active'),
        Index('ix_sessions_expires', 'expires_at'),
    )
    
    def __repr__(self):
        return f"<Session(id={self.id}, session_id={self.session_id}, user_id={self.user_id})>"


class APIKey(Base):
    """API key management for external integrations."""
    
    __tablename__ = "api_keys"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # API key information
    key_name = Column(String(255), nullable=False)
    key_hash = Column(String(255), unique=True, index=True, nullable=False)
    key_prefix = Column(String(10), nullable=False)  # First few chars for identification
    
    # Ownership and permissions
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permissions = Column(Text, nullable=True)  # JSON string of permissions
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    last_used = Column(DateTime(timezone=True), nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Constraints
    __table_args__ = (
        Index('ix_api_keys_user_active', 'user_id', 'is_active'),
        Index('ix_api_keys_prefix', 'key_prefix'),
        CheckConstraint('usage_count >= 0', name='REPLACE_ME'),
    )
    
    def __repr__(self):
        return f"<APIKey(id={self.id}, key_name={self.key_name}, user_id={self.user_id})>"


# ===========================================
# SAAS BUSINESS MODELS
# ===========================================

class Organization(Base):
    """Organization model for multi-tenancy."""
    
    __tablename__ = "organizations"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Organization information
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Organization status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Subscription information
    subscription_tier_id = Column(Integer, ForeignKey("subscription_tiers.id"), nullable=True)
    subscription_tier = relationship("SubscriptionTier", back_populates="organizations")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    members = relationship("OrganizationMember", back_populates="organization", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="organization", cascade="all, delete-orphan")
    usage_records = relationship("UsageRecord", back_populates="organization", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        Index('ix_organizations_slug', 'slug'),
        CheckConstraint('length(name) >= 1', name='ck_organizations_name_length'),
    )
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name={self.name}, slug={self.slug})>"


class OrganizationMember(Base):
    """Organization membership model."""
    
    __tablename__ = "organization_members"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Member information
    role = Column(Enum(OrganizationRole), default=OrganizationRole.MEMBER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="organization_memberships")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('organization_id', 'user_id', name='uq_org_members_org_user'),
        Index('ix_org_members_org_user', 'organization_id', 'user_id'),
    )
    
    def __repr__(self):
        return f"<OrganizationMember(id={self.id}, org_id={self.organization_id}, user_id={self.user_id})>"


class SubscriptionTier(Base):
    """Subscription tier model."""
    
    __tablename__ = "subscription_tiers"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Tier information
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Pricing
    price_monthly = Column(Numeric(10, 2), nullable=False, default=0)
    price_yearly = Column(Numeric(10, 2), nullable=False, default=0)
    
    # Features and limits
    features = Column(JSON, nullable=True)  # List of features
    limits = Column(JSON, nullable=True)    # Usage limits
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    organizations = relationship("Organization", back_populates="subscription_tier")
    subscriptions = relationship("Subscription", back_populates="subscription_tier")
    
    def __repr__(self):
        return f"<SubscriptionTier(id={self.id}, name={self.name})>"


class Subscription(Base):
    """Subscription model."""
    
    __tablename__ = "subscriptions"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    subscription_tier_id = Column(Integer, ForeignKey("subscription_tiers.id"), nullable=False)
    
    # Subscription information
    stripe_subscription_id = Column(String(255), unique=True, index=True, nullable=True)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False)
    
    # Billing information
    current_period_start = Column(DateTime(timezone=True), nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)
    cancel_at_period_end = Column(Boolean, default=False, nullable=False)
    canceled_at = Column(DateTime(timezone=True), nullable=True)
    
    # Stripe integration fields
    stripe_customer_id = Column(String(255), index=True, nullable=True)
    stripe_price_id = Column(String(255), index=True, nullable=True)
    billing_cycle_anchor = Column(DateTime(timezone=True), nullable=True)
    collection_method = Column(String(50), nullable=True)
    days_until_due = Column(Integer, nullable=True)
    default_payment_method = Column(String(255), nullable=True)
    trial_start = Column(DateTime(timezone=True), nullable=True)
    trial_end = Column(DateTime(timezone=True), nullable=True)
    items = Column(JSON, nullable=True)  # Subscription items as JSON
    stripe_metadata = Column(JSON, nullable=True)
    cancel_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="subscriptions")
    subscription_tier = relationship("SubscriptionTier", back_populates="subscriptions")
    invoices = relationship("Invoice", back_populates="subscription", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        Index('ix_subscriptions_org', 'organization_id'),
        Index('ix_subscriptions_status', 'status'),
    )
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, org_id={self.organization_id}, status={self.status})>"


class PaymentMethod(Base):
    """Payment method model."""
    
    __tablename__ = "payment_methods"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Payment method information
    stripe_payment_method_id = Column(String(255), unique=True, index=True, nullable=False)
    type = Column(String(50), nullable=False)  # card, bank_account, etc.
    is_default = Column(Boolean, default=False, nullable=False)
    
    # Card information (if applicable)
    brand = Column(String(50), nullable=True)  # visa, mastercard, etc.
    last4 = Column(String(4), nullable=True)
    exp_month = Column(Integer, nullable=True)
    exp_year = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    organization = relationship("Organization")
    
    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, org_id={self.organization_id}, type={self.type})>"


class Invoice(Base):
    """Invoice model."""
    
    __tablename__ = "invoices"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)  # Allow null for orphaned invoices
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)  # Allow null for orphaned invoices
    
    # Invoice information
    stripe_invoice_id = Column(String(255), unique=True, index=True, nullable=True)
    invoice_number = Column(String(100), unique=True, index=True, nullable=False)
    
    # Amounts
    amount_due = Column(Numeric(10, 2), nullable=False)
    amount_paid = Column(Numeric(10, 2), nullable=False, default=0)
    amount_remaining = Column(Numeric(10, 2), nullable=False)
    
    # Status
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    
    # Dates
    due_date = Column(DateTime(timezone=True), nullable=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    
    # Stripe integration fields
    stripe_customer_id = Column(String(255), index=True, nullable=True)
    stripe_charge_id = Column(String(255), nullable=True)
    currency = Column(String(3), nullable=True)
    subtotal = Column(Integer, nullable=True)  # Amount in cents
    tax = Column(Integer, nullable=True)  # Amount in cents
    total = Column(Integer, nullable=True)  # Amount in cents
    amount_shipping = Column(Integer, nullable=True)  # Amount in cents
    billing_reason = Column(String(50), nullable=True)
    collection_method = Column(String(50), nullable=True)
    customer_email = Column(String(255), nullable=True)
    customer_name = Column(String(255), nullable=True)
    customer_address = Column(JSON, nullable=True)
    customer_shipping = Column(JSON, nullable=True)
    lines = Column(JSON, nullable=True)  # Invoice line items as JSON
    hosted_invoice_url = Column(String(500), nullable=True)
    invoice_pdf = Column(String(500), nullable=True)
    stripe_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    organization = relationship("Organization")
    subscription = relationship("Subscription", back_populates="invoices")
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, org_id={self.organization_id}, amount={self.amount_due})>"


class UsageRecord(Base):
    """Usage tracking model."""
    
    __tablename__ = "usage_records"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Usage information
    endpoint = Column(String(255), nullable=False)
    request_count = Column(Integer, nullable=False, default=1)
    response_time_ms = Column(Integer, nullable=True)
    status_code = Column(Integer, nullable=True)
    record_type = Column(String(50), nullable=False, default="api_call")  # api_call, storage, etc.
    
    # Timestamps
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="usage_records")
    
    # Constraints
    __table_args__ = (
        Index('ix_usage_records_org_date', 'organization_id', 'recorded_at'),
        Index('ix_usage_records_endpoint', 'endpoint'),
    )
    
    def __repr__(self):
        return f"<UsageRecord(id={self.id}, org_id={self.organization_id}, endpoint={self.endpoint})>"


# =============================================================================
# BIASGUARD MODELS - Policy Enforcement and Compliance Tracking
# =============================================================================


class BiasGuardEnforcementType(str, enum.Enum):
    """BiasGuard policy enforcement types."""
    FAIRNESS_CHECK = "fairness_check"
    ATTRIBUTE_BASED = "attribute_based"
    COMPLIANCE = "compliance"
    AUDIT = "audit"


class BiasGuardPolicy(Base):
    """BiasGuard policy model for fairness and compliance enforcement."""
    
    __tablename__ = "biasguard_policies"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Policy identification
    policy_id = Column(String(100), unique=True, index=True, nullable=False)
    policy_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Policy configuration
    enforcement_type = Column(
        String(50),
        default=BiasGuardEnforcementType.FAIRNESS_CHECK,
        nullable=False
    )
    rules = Column(JSON, nullable=False)  # Policy rules as JSON
    
    # Policy status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    priority = Column(Integer, default=100, nullable=False)  # Lower number = higher priority
    
    # Metadata
    created_by = Column(String(255), nullable=True)
    last_modified_by = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    audit_events = relationship(
        "BiasGuardAuditLog",
        back_populates="policy",
        cascade="all, delete-orphan"
    )
    
    # Constraints
    __table_args__ = (
        Index('ix_biasguard_policies_active', 'is_active'),
        Index('ix_biasguard_policies_type', 'enforcement_type'),
        Index('ix_biasguard_policies_priority', 'priority'),
        CheckConstraint('priority >= 0', name='REPLACE_ME'),
    )
    
    def __repr__(self):
        return f"<BiasGuardPolicy(id={self.id}, policy_id={self.policy_id}, type={self.enforcement_type})>"


class BiasGuardAuditLog(Base):
    """
    BiasGuard audit log model for tracking policy enforcement events,
    decisions, and compliance.
    
    Ensures attribution and auditability of all fairness and compliance
    decisions made by the system.
    """
    
    __tablename__ = "biasguard_audit_logs"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Audit identification
    audit_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Related entities
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    policy_id = Column(Integer, ForeignKey("biasguard_policies.id"), nullable=True)
    
    # Event details
    event_type = Column(String(100), nullable=False, index=True)  # e.g., policy_enforced, violation_detected
    event_status = Column(String(50), nullable=False)  # success, violation, warning, error
    
    # Policy enforcement details
    enforcement_type = Column(String(50), nullable=True)
    policy_name = Column(String(255), nullable=True)
    
    # Decision details
    decision = Column(String(50), nullable=True)  # allow, deny, review_required
    enforcement_passed = Column(Boolean, nullable=True)
    
    # Violations and warnings
    violations = Column(JSON, nullable=True)  # List of violations
    warnings = Column(JSON, nullable=True)  # List of warnings
    
    # Fairness metrics
    fairness_metrics = Column(JSON, nullable=True)
    compliance_metrics = Column(JSON, nullable=True)
    
    # User context (for attribution)
    user_email = Column(String(255), nullable=True, index=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Additional context
    context_data = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    policy = relationship("BiasGuardPolicy", back_populates="audit_events")
    user = relationship("User")
    
    # Constraints
    __table_args__ = (
        Index('REPLACE_ME', 'event_type'),
        Index('REPLACE_ME', 'event_status'),
        Index('ix_biasguard_audit_logs_user_id', 'user_id'),
        Index('REPLACE_ME', 'created_at'),
        Index('REPLACE_ME', 'enforcement_passed'),
        UniqueConstraint('audit_id', name='REPLACE_ME'),
        CheckConstraint('length(audit_id) > 0', name='REPLACE_ME'),
    )
    
    def __repr__(self):
        return f"<BiasGuardAuditLog(id={self.id}, audit_id={self.audit_id}, event={self.event_type})>"


class BiasGuardPolicyViolation(Base):
    """
    BiasGuard policy violation model for detailed violation tracking
    and compliance monitoring.
    """
    
    __tablename__ = "biasguard_policy_violations"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Related entities
    audit_log_id = Column(Integer, ForeignKey("biasguard_audit_logs.id"), nullable=False, index=True)
    policy_id = Column(Integer, ForeignKey("biasguard_policies.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    
    # Violation details
    violation_type = Column(String(100), nullable=False)  # fairness_violation, compliance_breach, etc.
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    description = Column(Text, nullable=True)
    
    # Resolution
    is_resolved = Column(Boolean, default=False, nullable=False, index=True)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(String(255), nullable=True)
    
    # Metrics
    impact_score = Column(Numeric(precision=5, scale=2), nullable=True)
    remediation_required = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    audit_log = relationship("BiasGuardAuditLog")
    policy = relationship("BiasGuardPolicy")
    user = relationship("User")
    
    # Constraints
    __table_args__ = (
        Index('REPLACE_ME', 'audit_log_id'),
        Index('ix_biasguard_violations_policy', 'policy_id'),
        Index('ix_biasguard_violations_user', 'user_id'),
        Index('ix_biasguard_violations_type', 'violation_type'),
        Index('REPLACE_ME', 'severity'),
        Index('REPLACE_ME', 'is_resolved'),
        CheckConstraint("severity IN ('low', 'medium', 'high', 'critical')", name='REPLACE_ME'),
    )
    
    def __repr__(self):
        return f"<BiasGuardPolicyViolation(id={self.id}, type={self.violation_type}, severity={self.severity})>"


class BiasGuardComplianceReport(Base):
    """
    BiasGuard compliance report model for generating compliance and
    audit reports.
    """
    
    __tablename__ = "biasguard_compliance_reports"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Report identification
    report_id = Column(String(100), unique=True, index=True, nullable=False)
    report_name = Column(String(255), nullable=False)
    report_type = Column(String(50), nullable=False)  # audit, compliance, fairness
    
    # Date range
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Report data
    total_events = Column(Integer, default=0, nullable=False)
    total_violations = Column(Integer, default=0, nullable=False)
    total_warnings = Column(Integer, default=0, nullable=False)
    policies_enforced = Column(JSON, nullable=True)  # List of policies
    
    # Metrics
    compliance_score = Column(Numeric(precision=5, scale=2), nullable=True)
    fairness_score = Column(Numeric(precision=5, scale=2), nullable=True)
    audit_coverage = Column(Numeric(precision=5, scale=2), nullable=True)
    
    # Report details
    summary = Column(Text, nullable=True)
    findings = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    
    # Status
    status = Column(String(50), default="pending", nullable=False)  # pending, completed, reviewed
    reviewed_by = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Constraints
    __table_args__ = (
        Index('REPLACE_ME', 'report_type'),
        Index('REPLACE_ME', 'status'),
        Index('REPLACE_ME', 'start_date', 'end_date'),
    )
    
    def __repr__(self):
        return f"<BiasGuardComplianceReport(id={self.id}, report_id={self.report_id}, type={self.report_type})>"


# =============================================================================
# STRIPE INTEGRATION MODELS - Webhook Event Handling
# =============================================================================

class StripeProduct(Base):
    """Stripe product model for subscription plans."""
    
    __tablename__ = "stripe_products"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Stripe product information
    stripe_product_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Product details
    type = Column(String(50), nullable=False)  # service, good
    unit_label = Column(String(100), nullable=True)
    statement_descriptor = Column(String(22), nullable=True)
    tax_code = Column(String(100), nullable=True)
    url = Column(String(500), nullable=True)
    
    # Physical product details
    shippable = Column(Boolean, nullable=True)
    package_dimensions = Column(JSON, nullable=True)
    
    # Media and features
    images = Column(JSON, nullable=True)
    attributes = Column(JSON, nullable=True)
    marketing_features = Column(JSON, nullable=True)
    stripe_metadata = Column(JSON, nullable=True)
    
    # Stripe metadata
    livemode = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    prices = relationship("StripePrice", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<StripeProduct(id={self.id}, stripe_id={self.stripe_product_id}, name={self.name})>"


class StripePrice(Base):
    """Stripe price model for subscription pricing."""
    
    __tablename__ = "stripe_prices"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Stripe price information
    stripe_price_id = Column(String(255), unique=True, index=True, nullable=False)
    stripe_product_id = Column(String(255), ForeignKey("stripe_products.stripe_product_id"), nullable=False)
    active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Pricing details
    currency = Column(String(3), nullable=False)
    type = Column(String(20), nullable=False)  # one_time, recurring
    unit_amount = Column(Integer, nullable=False)  # Amount in cents
    unit_amount_decimal = Column(String(20), nullable=True)
    
    # Billing details
    billing_scheme = Column(String(20), nullable=False)  # per_unit, tiered
    tiers_mode = Column(String(20), nullable=True)  # graduated, volume
    nickname = Column(String(100), nullable=True)
    lookup_key = Column(String(100), nullable=True)
    
    # Tax and custom pricing
    tax_behavior = Column(String(20), nullable=False)  # unspecified, inclusive, exclusive
    custom_unit_amount = Column(JSON, nullable=True)
    transform_quantity = Column(JSON, nullable=True)
    
    # Recurring details
    recurring = Column(JSON, nullable=True)  # Recurring details as JSON
    stripe_metadata = Column(JSON, nullable=True)
    
    # Stripe metadata
    livemode = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    product = relationship("StripeProduct", back_populates="prices")
    
    def __repr__(self):
        return f"<StripePrice(id={self.id}, stripe_id={self.stripe_price_id}, amount={self.unit_amount})>"


class StripeCustomer(Base):
    """Stripe customer model for customer management."""
    
    __tablename__ = "stripe_customers"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Stripe customer information
    stripe_customer_id = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), index=True, nullable=True)
    name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    
    # Customer details
    balance = Column(Integer, default=0, nullable=False)  # Balance in cents
    currency = Column(String(3), nullable=True)
    delinquent = Column(Boolean, default=False, nullable=False)
    invoice_prefix = Column(String(50), nullable=True)
    default_source = Column(String(255), nullable=True)
    
    # Address and shipping
    address = Column(JSON, nullable=True)  # city, country, line1, line2, postal_code, state
    shipping = Column(JSON, nullable=True)
    
    # Settings
    invoice_settings = Column(JSON, nullable=True)
    preferred_locales = Column(JSON, nullable=True)
    tax_exempt = Column(String(20), nullable=True)
    stripe_metadata = Column(JSON, nullable=True)
    
    # Stripe metadata
    livemode = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<StripeCustomer(id={self.id}, stripe_id={self.stripe_customer_id}, email={self.email})>"