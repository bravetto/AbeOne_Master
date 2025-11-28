"""Extend subscriptions and invoices tables for Stripe integration

Revision ID: 0007_extend_subscriptions_invoices
Revises: 0006_add_stripe_customers
Create Date: 2025-01-15 03:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0007_stripe_extend'
down_revision = '0006_add_stripe_customers'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Extend subscriptions and invoices tables with Stripe fields."""
    
    # Add new columns to subscriptions table
    op.add_column('subscriptions', sa.Column('stripe_customer_id', sa.String(length=255), nullable=True))
    op.add_column('subscriptions', sa.Column('stripe_price_id', sa.String(length=255), nullable=True))
    op.add_column('subscriptions', sa.Column('billing_cycle_anchor', sa.DateTime(timezone=True), nullable=True))
    op.add_column('subscriptions', sa.Column('collection_method', sa.String(length=50), nullable=True))
    op.add_column('subscriptions', sa.Column('days_until_due', sa.Integer(), nullable=True))
    op.add_column('subscriptions', sa.Column('default_payment_method', sa.String(length=255), nullable=True))
    op.add_column('subscriptions', sa.Column('trial_start', sa.DateTime(timezone=True), nullable=True))
    op.add_column('subscriptions', sa.Column('trial_end', sa.DateTime(timezone=True), nullable=True))
    op.add_column('subscriptions', sa.Column('items', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('subscriptions', sa.Column('stripe_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('subscriptions', sa.Column('cancel_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('subscriptions', sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True))
    
    # Create indexes for subscriptions
    op.create_index('REPLACE_ME', 'subscriptions', ['stripe_customer_id'])
    op.create_index('REPLACE_ME', 'subscriptions', ['stripe_price_id'])
    
    # Add new columns to invoices table
    op.add_column('invoices', sa.Column('stripe_customer_id', sa.String(length=255), nullable=True))
    op.add_column('invoices', sa.Column('stripe_charge_id', sa.String(length=255), nullable=True))
    op.add_column('invoices', sa.Column('currency', sa.String(length=3), nullable=True))
    op.add_column('invoices', sa.Column('subtotal', sa.Integer(), nullable=True))
    op.add_column('invoices', sa.Column('tax', sa.Integer(), nullable=True))
    op.add_column('invoices', sa.Column('total', sa.Integer(), nullable=True))
    op.add_column('invoices', sa.Column('amount_shipping', sa.Integer(), nullable=True))
    op.add_column('invoices', sa.Column('billing_reason', sa.String(length=50), nullable=True))
    op.add_column('invoices', sa.Column('collection_method', sa.String(length=50), nullable=True))
    op.add_column('invoices', sa.Column('customer_email', sa.String(length=255), nullable=True))
    op.add_column('invoices', sa.Column('customer_name', sa.String(length=255), nullable=True))
    op.add_column('invoices', sa.Column('customer_address', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('invoices', sa.Column('customer_shipping', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('invoices', sa.Column('lines', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('invoices', sa.Column('hosted_invoice_url', sa.String(length=500), nullable=True))
    op.add_column('invoices', sa.Column('invoice_pdf', sa.String(length=500), nullable=True))
    op.add_column('invoices', sa.Column('stripe_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    
    # Create indexes for invoices
    op.create_index('ix_invoices_stripe_customer_id', 'invoices', ['stripe_customer_id'])
    op.create_index('ix_invoices_stripe_charge_id', 'invoices', ['stripe_charge_id'])


def downgrade() -> None:
    """Remove Stripe fields from subscriptions and invoices tables."""
    
    # Drop indexes for invoices
    op.drop_index('ix_invoices_stripe_charge_id', table_name='invoices')
    op.drop_index('ix_invoices_stripe_customer_id', table_name='invoices')
    
    # Drop columns from invoices
    op.drop_column('invoices', 'stripe_metadata')
    op.drop_column('invoices', 'invoice_pdf')
    op.drop_column('invoices', 'hosted_invoice_url')
    op.drop_column('invoices', 'lines')
    op.drop_column('invoices', 'customer_shipping')
    op.drop_column('invoices', 'customer_address')
    op.drop_column('invoices', 'customer_name')
    op.drop_column('invoices', 'customer_email')
    op.drop_column('invoices', 'collection_method')
    op.drop_column('invoices', 'billing_reason')
    op.drop_column('invoices', 'amount_shipping')
    op.drop_column('invoices', 'total')
    op.drop_column('invoices', 'tax')
    op.drop_column('invoices', 'subtotal')
    op.drop_column('invoices', 'currency')
    op.drop_column('invoices', 'stripe_charge_id')
    op.drop_column('invoices', 'stripe_customer_id')
    
    # Drop indexes for subscriptions
    op.drop_index('REPLACE_ME', table_name='subscriptions')
    op.drop_index('REPLACE_ME', table_name='subscriptions')
    
    # Drop columns from subscriptions
    op.drop_column('subscriptions', 'ended_at')
    op.drop_column('subscriptions', 'cancel_at')
    op.drop_column('subscriptions', 'stripe_metadata')
    op.drop_column('subscriptions', 'items')
    op.drop_column('subscriptions', 'trial_end')
    op.drop_column('subscriptions', 'trial_start')
    op.drop_column('subscriptions', 'default_payment_method')
    op.drop_column('subscriptions', 'days_until_due')
    op.drop_column('subscriptions', 'collection_method')
    op.drop_column('subscriptions', 'billing_cycle_anchor')
    op.drop_column('subscriptions', 'stripe_price_id')
    op.drop_column('subscriptions', 'stripe_customer_id')

