"""Add last_login column to users table

Revision ID: 0003_add_last_login_column
Revises: 0002_add_user_post_tables
Create Date: 2025-10-21 22:48:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003_add_last_login_column'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add last_login column to users table."""
    # Add last_login column to users table
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Remove last_login column from users table."""
    # Remove last_login column from users table
    op.drop_column('users', 'last_login')
