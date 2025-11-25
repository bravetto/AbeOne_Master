"""Add BiasGuard policy and audit tables

Revision ID: 0002
Revises: 0001
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""
    
    # ===========================================
    # BIASGUARD POLICIES TABLE
    # ===========================================
    op.create_table('biasguard_policies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('policy_id', sa.String(length=100), nullable=False),
        sa.Column('policy_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('enforcement_type', sa.String(length=50), nullable=False),
        sa.Column('rules', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('last_modified_by', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('policy_id', name='uq_biasguard_policies_policy_id'),
        sa.CheckConstraint('priority >= 0', name='REPLACE_ME'),
    )
    op.create_index('ix_biasguard_policies_id', 'biasguard_policies', ['id'], unique=False)
    op.create_index('ix_biasguard_policies_active', 'biasguard_policies', ['is_active'], unique=False)
    op.create_index('ix_biasguard_policies_type', 'biasguard_policies', ['enforcement_type'], unique=False)
    op.create_index('ix_biasguard_policies_priority', 'biasguard_policies', ['priority'], unique=False)
    
    # ===========================================
    # BIASGUARD AUDIT LOGS TABLE
    # ===========================================
    op.create_table('biasguard_audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('audit_id', sa.String(length=50), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('policy_id', sa.Integer(), nullable=True),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('event_status', sa.String(length=50), nullable=False),
        sa.Column('enforcement_type', sa.String(length=50), nullable=True),
        sa.Column('policy_name', sa.String(length=255), nullable=True),
        sa.Column('decision', sa.String(length=50), nullable=True),
        sa.Column('enforcement_passed', sa.Boolean(), nullable=True),
        sa.Column('violations', sa.JSON(), nullable=True),
        sa.Column('warnings', sa.JSON(), nullable=True),
        sa.Column('fairness_metrics', sa.JSON(), nullable=True),
        sa.Column('compliance_metrics', sa.JSON(), nullable=True),
        sa.Column('user_email', sa.String(length=255), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('context_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['policy_id'], ['biasguard_policies.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('audit_id', name='REPLACE_ME'),
        sa.CheckConstraint('length(audit_id) > 0', name='REPLACE_ME'),
    )
    op.create_index('ix_biasguard_audit_logs_id', 'biasguard_audit_logs', ['id'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_audit_logs', ['audit_id'], unique=True)
    op.create_index('REPLACE_ME', 'biasguard_audit_logs', ['event_type'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_audit_logs', ['event_status'], unique=False)
    op.create_index('ix_biasguard_audit_logs_user_id', 'biasguard_audit_logs', ['user_id'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_audit_logs', ['created_at'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_audit_logs', ['enforcement_passed'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_audit_logs', ['user_email'], unique=False)
    
    # ===========================================
    # BIASGUARD POLICY VIOLATIONS TABLE
    # ===========================================
    op.create_table('biasguard_policy_violations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('audit_log_id', sa.Integer(), nullable=False),
        sa.Column('policy_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('violation_type', sa.String(length=100), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_resolved', sa.Boolean(), nullable=False),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('resolved_by', sa.String(length=255), nullable=True),
        sa.Column('impact_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('remediation_required', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['audit_log_id'], ['biasguard_audit_logs.id'], ),
        sa.ForeignKeyConstraint(['policy_id'], ['biasguard_policies.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("severity IN ('low', 'medium', 'high', 'critical')", name='REPLACE_ME'),
    )
    op.create_index('ix_biasguard_violations_id', 'biasguard_policy_violations', ['id'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_policy_violations', ['audit_log_id'], unique=False)
    op.create_index('ix_biasguard_violations_policy', 'biasguard_policy_violations', ['policy_id'], unique=False)
    op.create_index('ix_biasguard_violations_user', 'biasguard_policy_violations', ['user_id'], unique=False)
    op.create_index('ix_biasguard_violations_type', 'biasguard_policy_violations', ['violation_type'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_policy_violations', ['severity'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_policy_violations', ['is_resolved'], unique=False)
    
    # ===========================================
    # BIASGUARD COMPLIANCE REPORTS TABLE
    # ===========================================
    op.create_table('biasguard_compliance_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('report_id', sa.String(length=100), nullable=False),
        sa.Column('report_name', sa.String(length=255), nullable=False),
        sa.Column('report_type', sa.String(length=50), nullable=False),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('total_events', sa.Integer(), nullable=False),
        sa.Column('total_violations', sa.Integer(), nullable=False),
        sa.Column('total_warnings', sa.Integer(), nullable=False),
        sa.Column('policies_enforced', sa.JSON(), nullable=True),
        sa.Column('compliance_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('fairness_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('audit_coverage', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('findings', sa.JSON(), nullable=True),
        sa.Column('recommendations', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('reviewed_by', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('report_id', name='REPLACE_ME'),
    )
    op.create_index('REPLACE_ME', 'biasguard_compliance_reports', ['id'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_compliance_reports', ['report_id'], unique=True)
    op.create_index('REPLACE_ME', 'biasguard_compliance_reports', ['report_type'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_compliance_reports', ['status'], unique=False)
    op.create_index('REPLACE_ME', 'biasguard_compliance_reports', ['start_date', 'end_date'], unique=False)


def downgrade() -> None:
    """Downgrade database schema."""
    
    # Drop tables in reverse order
    op.drop_table('biasguard_compliance_reports')
    op.drop_table('biasguard_policy_violations')
    op.drop_table('biasguard_audit_logs')
    op.drop_table('biasguard_policies')
