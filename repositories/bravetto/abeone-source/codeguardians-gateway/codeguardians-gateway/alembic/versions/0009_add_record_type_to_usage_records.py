"""Add record_type to usage_records table

Revision ID: 0009_add_record_type
Revises: 0008_add_clerk_user_fields
Create Date: 2024-01-16 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0009_add_record_type'
down_revision = '0008_add_clerk_user_fields'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add record_type column to usage_records table."""
    op.add_column('usage_records', sa.Column('record_type', sa.String(length=50), nullable=False, server_default='api_call'))
    op.create_index('ix_usage_records_record_type', 'usage_records', ['record_type'])


def downgrade() -> None:
    """Remove record_type column from usage_records table."""
    op.drop_index('ix_usage_records_record_type', table_name='usage_records')
    op.drop_column('usage_records', 'record_type')

