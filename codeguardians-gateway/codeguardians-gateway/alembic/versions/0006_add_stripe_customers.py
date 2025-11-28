"""Add Stripe customers table

Revision ID: 0006_add_stripe_customers
Revises: 0005_add_stripe_products_prices
Create Date: 2025-01-15 02:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0006_add_stripe_customers'
down_revision = '0005_add_stripe_products_prices'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add Stripe customers table."""
    
    # Create stripe_customers table
    op.create_table('stripe_customers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stripe_customer_id', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('balance', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('currency', sa.String(length=3), nullable=True),
        sa.Column('delinquent', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('invoice_prefix', sa.String(length=50), nullable=True),
        sa.Column('default_source', sa.String(length=255), nullable=True),
        sa.Column('address', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('shipping', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('invoice_settings', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('preferred_locales', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('tax_exempt', sa.String(length=20), nullable=True),
        sa.Column('stripe_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('livemode', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('stripe_customer_id', name='uq_stripe_customers_stripe_id')
    )
    
    # Create indexes for stripe_customers
    op.create_index('ix_stripe_customers_id', 'stripe_customers', ['id'])
    op.create_index('ix_stripe_customers_stripe_id', 'stripe_customers', ['stripe_customer_id'], unique=True)
    op.create_index('ix_stripe_customers_email', 'stripe_customers', ['email'])
    
    # Create trigger for updated_at
    op.execute("""
        CREATE TRIGGER update_stripe_customers_updated_at 
        BEFORE UPDATE ON stripe_customers 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    """Remove Stripe customers table."""
    
    # Drop trigger
    op.execute("DROP TRIGGER IF EXISTS update_stripe_customers_updated_at ON stripe_customers;")
    
    # Drop table
    op.drop_table('stripe_customers')

