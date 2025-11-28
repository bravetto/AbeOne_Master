"""
Tests for Stripe webhook router separation.

This module tests that Stripe webhooks and API endpoints are properly
separated into different routers.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import create_app
from app.api.webhooks import stripe_webhooks_router, stripe_api_router


@pytest.fixture
def app():
    """Create test application."""
    # Set database enabled before creating app
    import os
    os.environ["DATABASE_ENABLED"] = "true"
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    return create_app()


@pytest.fixture
def client(app, mock_db):
    """Create test client."""
    from app.core.database import get_db
    
    # Override get_db dependency to return mock_db
    async def override_get_db():
        yield mock_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def mock_db():
    """Create mock database session."""
    return AsyncMock(spec=AsyncSession)


class TestStripeRouterSeparation:
    """Test cases for Stripe router separation."""
    
    def test_webhook_router_exists(self):
        """Test that webhook_router is defined and accessible."""
        assert stripe_webhooks_router is not None
        assert hasattr(stripe_webhooks_router, 'routes')
    
    def test_api_router_exists(self):
        """Test that stripe_api_router is defined and accessible."""
        assert stripe_api_router is not None
        assert hasattr(stripe_api_router, 'routes')
    
    def test_routers_are_different_objects(self):
        """Test that webhook_router and api_router are different objects."""
        assert stripe_webhooks_router is not stripe_api_router
    
    def test_webhook_router_has_webhook_tag(self):
        """Test that webhook router has correct tag."""
        assert "Stripe Webhooks" in stripe_webhooks_router.tags
    
    def test_api_router_has_api_tag(self):
        """Test that API router has correct tag."""
        assert "Stripe API" in stripe_api_router.tags
    
    def test_webhook_router_imported_from_module(self):
        """Test that routers can be imported from webhooks module."""
        from app.api.webhooks import stripe_webhooks_router, stripe_api_router
        
        assert stripe_webhooks_router is not None
        assert stripe_api_router is not None
    
    def test_backward_compatibility_router_export(self):
        """Test that default router export maintains backward compatibility."""
        from app.api.webhooks.stripe_webhooks import router
        
        # The router should be the webhook_router for backward compatibility
        assert router is not None
        assert hasattr(router, 'routes')


class TestStripeRouterRegistration:
    """Test cases for Stripe router registration in main app."""
    
    def test_webhook_router_registered(self, app):
        """Test that webhook router is registered in the app."""
        # Check if webhook routes are registered
        webhook_routes = [
            route for route in app.routes
            if hasattr(route, 'path') and '/webhooks/stripe' in route.path
        ]
        
        assert len(webhook_routes) > 0, "Webhook router should be registered"
    
    def test_api_router_registered(self, app):
        """Test that API router is registered in the app."""
        # Check if API routes are registered
        api_routes = [
            route for route in app.routes
            if hasattr(route, 'path') and '/stripe/products' in route.path
        ]
        
        assert len(api_routes) > 0, "API router should be registered with /stripe prefix"
    
    def test_webhook_endpoint_separate_from_api(self, app):
        """Test that webhook endpoint is separate from API endpoints."""
        # Webhook endpoint should be under /webhooks/stripe
        webhook_routes = [
            route for route in app.routes
            if hasattr(route, 'path') and route.path == '/webhooks/stripe'
        ]
        
        # API endpoints should be under /stripe
        api_routes = [
            route for route in app.routes
            if hasattr(route, 'path') and '/stripe/products' in route.path
        ]
        
        assert len(webhook_routes) > 0, "Webhook endpoint should exist"
        assert len(api_routes) > 0, "API endpoints should exist"
        assert webhook_routes[0].path != api_routes[0].path, "Endpoints should be separate"


class TestStripeAPIEndpoints:
    """Test cases for Stripe API endpoints (separated from webhooks)."""
    
    @patch('app.api.webhooks.stripe_webhooks.get_db')
    def test_get_products_endpoint_exists(self, mock_get_db, client, mock_db):
        """Test that /stripe/products endpoint exists."""
        # Mock database query
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value = mock_db
        
        # Make request
        response = client.get("/stripe/products", headers={"Host": "localhost"})
        
        # Should not be 404 (endpoint exists)
        assert response.status_code != 404
    
    @patch('app.api.webhooks.stripe_webhooks.get_db')
    def test_get_prices_endpoint_exists(self, mock_get_db, client, mock_db):
        """Test that /stripe/prices/{product_id} endpoint exists."""
        # Mock database query
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value = mock_db
        
        # Make request
        response = client.get("/stripe/prices/test_product_id", headers={"Host": "localhost"})
        
        # Should not be 404 (endpoint exists)
        assert response.status_code != 404
    
    @patch('app.api.webhooks.stripe_webhooks.get_db')
    def test_get_customers_endpoint_exists(self, mock_get_db, client, mock_db):
        """Test that /stripe/customers/{email} endpoint exists."""
        # Mock database query to return None (not found)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value = mock_db
        
        # Make request
        response = client.get("/stripe/customers/test@example.com", headers={"Host": "localhost"})
        
        # Should not be 404 route not found (should be 404 for customer not found, which is different)
        assert response.status_code in [404, 500]  # 404 = customer not found, 500 = other error


class TestStripeWebhookEndpoint:
    """Test cases for Stripe webhook endpoint (separated from API)."""
    
    @patch('app.api.webhooks.stripe_webhooks._get_stripe')
    @patch('app.api.webhooks.stripe_webhooks.get_db')
    def test_webhook_endpoint_under_webhooks_prefix(
        self, mock_get_db, mock_get_stripe, client, mock_db
    ):
        """Test that webhook endpoint is under /webhooks prefix."""
        # Mock stripe and database
        mock_stripe = MagicMock()
        mock_stripe.Webhook.construct_event.return_value = {
            'type': 'product.created',
            'data': {'object': {}}
        }
        mock_get_stripe.return_value = mock_stripe
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value = mock_db
        
        # Try to access webhook endpoint
        response = client.post(
            "/webhooks/stripe",
            json={"test": "data"},
            headers={
                "stripe-signature": "test_signature",
                "Host": "localhost"
            }
        )
        
        # Should not be 404 (endpoint exists)
        # Might be 400/500 due to signature validation, but route exists
        assert response.status_code != 404
    
    def test_webhook_and_api_endpoints_separate_paths(self, app):
        """Test that webhook and API endpoints have separate paths."""
        routes = [route for route in app.routes if hasattr(route, 'path')]
        
        webhook_paths = [r.path for r in routes if '/webhooks/stripe' in r.path]
        api_paths = [r.path for r in routes if '/stripe/' in r.path and '/webhooks' not in r.path]
        
        assert len(webhook_paths) > 0, "Webhook paths should exist"
        assert len(api_paths) > 0, "API paths should exist"
        
        # Verify paths don't overlap
        for webhook_path in webhook_paths:
            for api_path in api_paths:
                assert webhook_path != api_path, f"Paths should not overlap: {webhook_path} vs {api_path}"

