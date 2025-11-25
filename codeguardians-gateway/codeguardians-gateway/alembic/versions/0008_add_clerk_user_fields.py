"""Add Clerk user fields to users table

Revision ID: 0008_add_clerk_user_fields
Revises: 0007_extend_subscriptions_invoices
Create Date: 2024-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0008_add_clerk_user_fields'
down_revision = '0007_stripe_extend'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add Clerk user fields to users table."""
    
    # Add Clerk-specific user fields
    op.add_column('users', sa.Column('first_name', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('image_url', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('profile_image_url', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('username', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('locale', sa.String(length=10), nullable=True))
    op.add_column('users', sa.Column('last_active_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('last_sign_in_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('password_enabled', sa.Boolean(), default=True, nullable=True))
    op.add_column('users', sa.Column('two_factor_enabled', sa.Boolean(), default=False, nullable=True))
    op.add_column('users', sa.Column('totp_enabled', sa.Boolean(), default=False, nullable=True))
    op.add_column('users', sa.Column('backup_code_enabled', sa.Boolean(), default=False, nullable=True))
    op.add_column('users', sa.Column('banned', sa.Boolean(), default=False, nullable=True))
    op.add_column('users', sa.Column('locked', sa.Boolean(), default=False, nullable=True))
    op.add_column('users', sa.Column('verification_attempts_remaining', sa.Integer(), default=100, nullable=True))
    op.add_column('users', sa.Column('primary_email_address_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('primary_phone_number_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('primary_web3_wallet_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('external_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('clerk_created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('clerk_updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('clerk_private_metadata', sa.JSON(), nullable=True))
    op.add_column('users', sa.Column('clerk_public_metadata', sa.JSON(), nullable=True))
    op.add_column('users', sa.Column('clerk_unsafe_metadata', sa.JSON(), nullable=True))
    
    # Create indexes for the new columns
    op.create_index('ix_users_first_name', 'users', ['first_name'])
    op.create_index('ix_users_last_name', 'users', ['last_name'])
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_external_id', 'users', ['external_id'])
    op.create_index('REPLACE_ME', 'users', ['primary_email_address_id'])


def downgrade() -> None:
    """Remove Clerk user fields from users table."""
    
    # Drop the indexes
    op.drop_index('REPLACE_ME', table_name='users')
    op.drop_index('ix_users_external_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    op.drop_index('ix_users_first_name', table_name='users')
    
    # Drop the columns
    op.drop_column('users', 'clerk_unsafe_metadata')
    op.drop_column('users', 'clerk_public_metadata')
    op.drop_column('users', 'clerk_private_metadata')
    op.drop_column('users', 'clerk_updated_at')
    op.drop_column('users', 'clerk_created_at')
    op.drop_column('users', 'external_id')
    op.drop_column('users', 'primary_web3_wallet_id')
    op.drop_column('users', 'primary_phone_number_id')
    op.drop_column('users', 'primary_email_address_id')
    op.drop_column('users', 'verification_attempts_remaining')
    op.drop_column('users', 'locked')
    op.drop_column('users', 'banned')
    op.drop_column('users', 'backup_code_enabled')
    op.drop_column('users', 'totp_enabled')
    op.drop_column('users', 'two_factor_enabled')
    op.drop_column('users', 'password_enabled')
    op.drop_column('users', 'last_sign_in_at')
    op.drop_column('users', 'last_active_at')
    op.drop_column('users', 'locale')
    op.drop_column('users', 'username')
    op.drop_column('users', 'profile_image_url')
    op.drop_column('users', 'image_url')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
