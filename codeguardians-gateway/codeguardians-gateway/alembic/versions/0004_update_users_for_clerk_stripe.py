"""Update users table for Clerk authentication and Stripe integration

Revision ID: 0004_update_users_for_clerk_stripe
Revises: 0003_add_last_login_column
Create Date: 2025-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0004_clerk_stripe'
down_revision = '0003_add_last_login_column'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Update users table for Clerk and Stripe integration."""
    
    # Add new columns for Clerk and Stripe integration
    op.add_column('users', sa.Column('clerk_user_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('stripe_customer_id', sa.String(length=255), nullable=True))
    
    # Create indexes for the new columns
    op.create_index('ix_users_clerk_user_id', 'users', ['clerk_user_id'], unique=True)
    op.create_index('ix_users_stripe_customer_id', 'users', ['stripe_customer_id'], unique=True)
    
    # Note: hashed_password column was never created in the users table,
    # so we don't need to drop it since we're using Clerk authentication


def downgrade() -> None:
    """Revert changes to users table."""
    
    # Drop the new indexes
    op.drop_index('ix_users_stripe_customer_id', table_name='users')
    op.drop_index('ix_users_clerk_user_id', table_name='users')
    
    # Drop the new columns
    op.drop_column('users', 'stripe_customer_id')
    op.drop_column('users', 'clerk_user_id')

