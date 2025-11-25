"""Add Stripe products and prices tables

Revision ID: 0005_add_stripe_products_prices
Revises: 0004_update_users_for_clerk_stripe
Create Date: 2025-01-15 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0005_add_stripe_products_prices'
down_revision = '0004_clerk_stripe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add Stripe products and prices tables."""
    
    # Create stripe_products table
    op.create_table('stripe_products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stripe_product_id', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('unit_label', sa.String(length=100), nullable=True),
        sa.Column('statement_descriptor', sa.String(length=22), nullable=True),
        sa.Column('tax_code', sa.String(length=100), nullable=True),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('shippable', sa.Boolean(), nullable=True),
        sa.Column('package_dimensions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('images', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('attributes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('marketing_features', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('stripe_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('livemode', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('stripe_product_id', name='uq_stripe_products_stripe_id')
    )
    
    # Create indexes for stripe_products
    op.create_index('ix_stripe_products_id', 'stripe_products', ['id'])
    op.create_index('ix_stripe_products_stripe_id', 'stripe_products', ['stripe_product_id'], unique=True)
    op.create_index('ix_stripe_products_active', 'stripe_products', ['active'])
    
    # Create stripe_prices table
    op.create_table('stripe_prices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stripe_price_id', sa.String(length=255), nullable=False),
        sa.Column('stripe_product_id', sa.String(length=255), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('unit_amount', sa.Integer(), nullable=False),
        sa.Column('unit_amount_decimal', sa.String(length=20), nullable=True),
        sa.Column('billing_scheme', sa.String(length=20), nullable=False),
        sa.Column('tiers_mode', sa.String(length=20), nullable=True),
        sa.Column('nickname', sa.String(length=100), nullable=True),
        sa.Column('lookup_key', sa.String(length=100), nullable=True),
        sa.Column('tax_behavior', sa.String(length=20), nullable=False),
        sa.Column('custom_unit_amount', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('transform_quantity', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('recurring', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('stripe_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('livemode', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['stripe_product_id'], ['stripe_products.stripe_product_id'], ondelete='CASCADE'),
        sa.UniqueConstraint('stripe_price_id', name='uq_stripe_prices_stripe_id')
    )
    
    # Create indexes for stripe_prices
    op.create_index('ix_stripe_prices_id', 'stripe_prices', ['id'])
    op.create_index('ix_stripe_prices_stripe_id', 'stripe_prices', ['stripe_price_id'], unique=True)
    op.create_index('ix_stripe_prices_product_id', 'stripe_prices', ['stripe_product_id'])
    op.create_index('ix_stripe_prices_active', 'stripe_prices', ['active'])
    
    # Create trigger for updated_at on stripe_products
    op.execute("""
        CREATE TRIGGER update_stripe_products_updated_at 
        BEFORE UPDATE ON stripe_products 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create trigger for updated_at on stripe_prices
    op.execute("""
        CREATE TRIGGER update_stripe_prices_updated_at 
        BEFORE UPDATE ON stripe_prices 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    """Remove Stripe products and prices tables."""
    
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS update_stripe_prices_updated_at ON stripe_prices;")
    op.execute("DROP TRIGGER IF EXISTS update_stripe_products_updated_at ON stripe_products;")
    
    # Drop tables in reverse order
    op.drop_table('stripe_prices')
    op.drop_table('stripe_products')

