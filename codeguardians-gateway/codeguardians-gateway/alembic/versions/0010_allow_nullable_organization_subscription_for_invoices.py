"""allow_nullable_organization_subscription_for_invoices

Revision ID: df138efe9c17
Revises: 0009_add_record_type
Create Date: 2025-11-03 15:20:14.191301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df138efe9c17'
down_revision = '0009_add_record_type'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Allow nullable organization_id and subscription_id for invoices."""
    # Make organization_id nullable
    op.alter_column('invoices', 'organization_id',
                    existing_type=sa.Integer(),
                    nullable=True,
                    existing_foreign_key_constraint_name='invoices_organization_id_fkey')
    
    # Make subscription_id nullable
    op.alter_column('invoices', 'subscription_id',
                    existing_type=sa.Integer(),
                    nullable=True,
                    existing_foreign_key_constraint_name='invoices_subscription_id_fkey')


def downgrade() -> None:
    """Revert organization_id and subscription_id to not nullable."""
    # First, update any null values to prevent constraint violations
    # We'll need to handle existing nulls - for now, we'll prevent downgrade if nulls exist
    # In production, you'd want to handle this more carefully
    op.alter_column('invoices', 'organization_id',
                    existing_type=sa.Integer(),
                    nullable=False,
                    existing_foreign_key_constraint_name='invoices_organization_id_fkey')
    
    op.alter_column('invoices', 'subscription_id',
                    existing_type=sa.Integer(),
                    nullable=False,
                    existing_foreign_key_constraint_name='invoices_subscription_id_fkey')
