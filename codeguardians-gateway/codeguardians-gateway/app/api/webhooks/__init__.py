"""
Webhooks API module.

This module contains all webhook-related endpoints for external service integrations,
separated from regular API endpoints for better organization and clarity.
"""

from .clerk_webhooks import router as clerk_webhooks_router
from .stripe_webhooks import router as stripe_webhooks_router, stripe_api_router

__all__ = ["clerk_webhooks_router", "stripe_webhooks_router", "stripe_api_router"]
