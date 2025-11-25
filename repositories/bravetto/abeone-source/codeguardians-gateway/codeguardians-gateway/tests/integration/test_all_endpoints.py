"""
Comprehensive Endpoint Testing Suite

This test suite systematically tests all API endpoints in the codebase.
It covers:
- Health and infrastructure endpoints
- Authentication and authorization
- Guard services (all 5 services)
- User management
- Content management (posts)
- Subscriptions and billing
- Organizations and enterprise features
- Analytics and metrics
- File upload operations
- A/B testing
- Webhooks (Stripe and Clerk)
- Configuration management
- Legal and compliance endpoints

The tests validate:
- Endpoint accessibility
- Response status codes
- Response structure
- Error handling
- Authentication requirements

Note: These tests use TestClient from FastAPI which doesn't require a running server.
For testing against a live server, use test_all_endpoints_live.py
"""

import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any, List
import json
from datetime import datetime


@pytest.mark.integration
class TestHealthEndpoints:
    """Test health check and infrastructure endpoints."""
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_check(self, client: TestClient):
        """Test basic health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_liveness_probe(self, client: TestClient):
        """Test Kubernetes liveness probe."""
        response = client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "alive"
    
    def test_readiness_probe(self, client: TestClient):
        """Test Kubernetes readiness probe."""
        response = client.get("/health/ready")
        assert response.status_code in [200, 503]  # May be 503 if DB not ready
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
    
    def test_comprehensive_health(self, client: TestClient):
        """Test comprehensive health check."""
        response = client.get("/health/comprehensive")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "timestamp" in data
    
    def test_circuit_breaker_status(self, client: TestClient):
        """Test circuit breaker status endpoint."""
        response = client.get("/health/circuit-breakers")
        assert response.status_code == 200
    
    def test_configuration_health(self, client: TestClient):
        """Test configuration health check."""
        response = client.get("/health/configuration")
        assert response.status_code == 200
    
    def test_metrics_endpoint(self, client: TestClient):
        """Test Prometheus metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers.get("content-type", "")


@pytest.mark.integration
class TestAuthenticationEndpoints:
    """Test authentication endpoints."""
    
    def test_login_endpoint_invalid(self, client: TestClient):
        """Test login with invalid data."""
        response = client.post("/api/v1/auth/login", json={"clerk_token": "invalid"})
        # Should return 400 or 422 for invalid token
        assert response.status_code in [400, 401, 422]
    
    def test_register_endpoint_invalid(self, client: TestClient):
        """Test registration with invalid data."""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@test.com", "password": "short"}  # Too short
        )
        assert response.status_code == 422
    
    def test_register_endpoint_missing_fields(self, client: TestClient):
        """Test registration with missing fields."""
        response = client.post("/api/v1/auth/register", json={})
        assert response.status_code == 422
    
    def test_logout_endpoint_unauthorized(self, client: TestClient):
        """Test logout without authentication."""
        response = client.post("/api/v1/auth/logout")
        assert response.status_code in [401, 403]
    
    def test_refresh_token_invalid(self, client: TestClient):
        """Test token refresh with invalid token."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid"}
        )
        assert response.status_code in [400, 401, 422]
    
    def test_password_reset_request(self, client: TestClient):
        """Test password reset request."""
        response = client.post(
            "/api/v1/auth/password-reset",
            json={"email": "test@example.com"}
        )
        # Should accept the request (may return 200 or 422 for invalid email)
        assert response.status_code in [200, 422]
    
    def test_password_reset_confirm_invalid(self, client: TestClient):
        """Test password reset confirmation with invalid token."""
        response = client.post(
            "/api/v1/auth/password-reset/confirm",
            json={"token": "invalid", "new_password": "newpassword123"}
        )
        assert response.status_code in [400, 422]
    
    def test_verify_email_invalid(self, client: TestClient):
        """Test email verification with invalid token."""
        response = client.post(
            "/api/v1/auth/verify-email",
            json={"token": "invalid"}
        )
        assert response.status_code in [400, 422]
    
    def test_get_current_user_unauthorized(self, client: TestClient):
        """Test getting current user without authentication."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code in [401, 403]


@pytest.mark.asyncio
@pytest.mark.integration
class TestUserEndpoints:
    """Test user management endpoints."""
    
    async def test_get_current_user_unauthorized(self, async_client: AsyncClient):
        """Test getting current user profile without auth."""
        response = await async_client.get("/api/v1/users/me")
        assert response.status_code in [401, 403]
    
    async def test_update_current_user_unauthorized(self, async_client: AsyncClient):
        """Test updating current user without auth."""
        response = await async_client.put(
            "/api/v1/users/me",
            json={"full_name": "Updated Name"}
        )
        assert response.status_code in [401, 403]
    
    async def test_delete_current_user_unauthorized(self, async_client: AsyncClient):
        """Test deleting current user without auth."""
        response = await async_client.delete("/api/v1/users/me")
        assert response.status_code in [401, 403]
    
    async def test_list_users_unauthorized(self, async_client: AsyncClient):
        """Test listing users without admin auth."""
        response = await async_client.get("/api/v1/users/")
        assert response.status_code in [401, 403]
    
    async def test_get_user_by_id_unauthorized(self, async_client: AsyncClient):
        """Test getting user by ID without admin auth."""
        response = await async_client.get("/api/v1/users/123")
        assert response.status_code in [401, 403, 404]
    
    async def test_create_user_unauthorized(self, async_client: AsyncClient):
        """Test creating user without admin auth."""
        response = await async_client.post(
            "/api/v1/users/",
            json={"email": "new@example.com", "password": "password123", "full_name": "New User"}
        )
        assert response.status_code in [401, 403]
    
    async def test_update_user_unauthorized(self, async_client: AsyncClient):
        """Test updating user without admin auth."""
        response = await async_client.put(
            "/api/v1/users/123",
            json={"full_name": "Updated"}
        )
        assert response.status_code in [401, 403, 404]
    
    async def test_delete_user_unauthorized(self, async_client: AsyncClient):
        """Test deleting user without admin auth."""
        response = await async_client.delete("/api/v1/users/123")
        assert response.status_code in [401, 403, 404]
    
    async def test_activate_user_unauthorized(self, async_client: AsyncClient):
        """Test activating user without admin auth."""
        response = await async_client.post("/api/v1/users/123/activate")
        assert response.status_code in [401, 403, 404]
    
    async def test_deactivate_user_unauthorized(self, async_client: AsyncClient):
        """Test deactivating user without admin auth."""
        response = await async_client.post("/api/v1/users/123/deactivate")
        assert response.status_code in [401, 403, 404]


@pytest.mark.asyncio
@pytest.mark.integration
class TestPostsEndpoints:
    """Test posts/content management endpoints."""
    
    async def test_list_posts(self, async_client: AsyncClient):
        """Test listing posts (public endpoint)."""
        response = await async_client.get("/api/v1/posts/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or isinstance(data, list)
    
    async def test_get_post_by_id_not_found(self, async_client: AsyncClient):
        """Test getting non-existent post."""
        response = await async_client.get("/api/v1/posts/99999")
        assert response.status_code == 404
    
    async def test_get_post_by_slug_not_found(self, async_client: AsyncClient):
        """Test getting post by slug that doesn't exist."""
        response = await async_client.get("/api/v1/posts/slug/non-existent-slug")
        assert response.status_code == 404
    
    async def test_create_post_unauthorized(self, async_client: AsyncClient):
        """Test creating post without authentication."""
        response = await async_client.post(
            "/api/v1/posts/",
            json={"title": "Test Post", "content": "Test content"}
        )
        assert response.status_code in [401, 403]
    
    async def test_update_post_unauthorized(self, async_client: AsyncClient):
        """Test updating post without authentication."""
        response = await async_client.put(
            "/api/v1/posts/123",
            json={"title": "Updated"}
        )
        assert response.status_code in [401, 403, 404]
    
    async def test_delete_post_unauthorized(self, async_client: AsyncClient):
        """Test deleting post without authentication."""
        response = await async_client.delete("/api/v1/posts/123")
        assert response.status_code in [401, 403, 404]
    
    async def test_publish_post_unauthorized(self, async_client: AsyncClient):
        """Test publishing post without authentication."""
        response = await async_client.post("/api/v1/posts/123/publish")
        assert response.status_code in [401, 403, 404]
    
    async def test_unpublish_post_unauthorized(self, async_client: AsyncClient):
        """Test unpublishing post without authentication."""
        response = await async_client.post("/api/v1/posts/123/unpublish")
        assert response.status_code in [401, 403, 404]


@pytest.mark.asyncio
@pytest.mark.integration
class TestGuardServiceEndpoints:
    """Test guard service endpoints."""
    
    async def test_process_guard_request_tokenguard(self, async_client: AsyncClient):
        """Test processing request through TokenGuard."""
        payload = {
            "service_type": "tokenguard",
            "payload": {
                "text": "This is a test message for token optimization",
                "max_tokens": 100
            }
        }
        response = await async_client.post("/api/v1/guards/process", json=payload)
        # Should return 200 or 422 if validation fails
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            data = response.json()
            assert "request_id" in data or "success" in data
    
    async def test_process_guard_request_trustguard(self, async_client: AsyncClient):
        """Test processing request through TrustGuard."""
        payload = {
            "service_type": "trustguard",
            "payload": {
                "content": "This is test content for trust validation"
            }
        }
        response = await async_client.post("/api/v1/guards/process", json=payload)
        assert response.status_code in [200, 422]
    
    async def test_process_guard_request_contextguard(self, async_client: AsyncClient):
        """Test processing request through ContextGuard."""
        payload = {
            "service_type": "contextguard",
            "payload": {
                "context": "Test context",
                "conversation_history": []
            }
        }
        response = await async_client.post("/api/v1/guards/process", json=payload)
        assert response.status_code in [200, 422]
    
    async def test_process_guard_request_biasguard(self, async_client: AsyncClient):
        """Test processing request through BiasGuard."""
        payload = {
            "service_type": "biasguard",
            "payload": {
                "text": "This is test text for bias detection"
            }
        }
        response = await async_client.post("/api/v1/guards/process", json=payload)
        assert response.status_code in [200, 422]
    
    async def test_process_guard_request_healthguard(self, async_client: AsyncClient):
        """Test processing request through HealthGuard."""
        payload = {
            "service_type": "healthguard",
            "payload": {
                "text": "Health check request"
            }
        }
        response = await async_client.post("/api/v1/guards/process", json=payload)
        assert response.status_code in [200, 422]
    
    async def test_process_guard_request_invalid_service(self, async_client: AsyncClient):
        """Test processing request with invalid service type."""
        payload = {
            "service_type": "invalid_service",
            "payload": {"text": "test"}
        }
        response = await async_client.post("/api/v1/guards/process", json=payload)
        assert response.status_code == 400
    
    async def test_guard_status(self, async_client: AsyncClient):
        """Test guard service status endpoint."""
        response = await async_client.get("/api/v1/guards/status")
        assert response.status_code == 200
    
    async def test_guard_health(self, async_client: AsyncClient):
        """Test guard service health endpoint."""
        response = await async_client.get("/api/v1/guards/health")
        assert response.status_code == 200
    
    async def test_specific_guard_health(self, async_client: AsyncClient):
        """Test specific guard service health."""
        response = await async_client.get("/api/v1/guards/health/tokenguard")
        assert response.status_code in [200, 404]
    
    async def test_refresh_guard_health(self, async_client: AsyncClient):
        """Test refreshing guard health status."""
        response = await async_client.post("/api/v1/guards/health/refresh")
        assert response.status_code == 200
    
    async def test_discovery_services(self, async_client: AsyncClient):
        """Test service discovery endpoint."""
        response = await async_client.get("/api/v1/guards/discovery/services")
        assert response.status_code == 200
    
    async def test_list_guard_services(self, async_client: AsyncClient):
        """Test listing guard services."""
        response = await async_client.get("/api/v1/guards/services")
        assert response.status_code == 200
    
    async def test_scan_endpoint_alias(self, async_client: AsyncClient):
        """Test scan endpoint alias."""
        payload = {
            "service_type": "tokenguard",
            "payload": {"text": "test"}
        }
        response = await async_client.post("/api/v1/scan", json=payload)
        assert response.status_code in [200, 422]
    
    async def test_analyze_endpoint_alias(self, async_client: AsyncClient):
        """Test analyze endpoint alias."""
        payload = {
            "service_type": "tokenguard",
            "payload": {"text": "test"}
        }
        response = await async_client.post("/api/v1/analyze", json=payload)
        assert response.status_code in [200, 422]


@pytest.mark.asyncio
@pytest.mark.integration
class TestDirectGuardEndpoints:
    """Test direct guard service endpoints."""
    
    async def test_direct_tokenguard(self, async_client: AsyncClient):
        """Test direct TokenGuard endpoint."""
        response = await async_client.post(
            "/tokenguard",
            json={"text": "Test text for token optimization"}
        )
        assert response.status_code in [200, 422]
    
    async def test_direct_trustguard(self, async_client: AsyncClient):
        """Test direct TrustGuard endpoint."""
        response = await async_client.post(
            "/trustguard",
            json={"text": "Test content for trust validation"}
        )
        assert response.status_code in [200, 422]
    
    async def test_direct_contextguard(self, async_client: AsyncClient):
        """Test direct ContextGuard endpoint."""
        response = await async_client.post(
            "/contextguard",
            json={"text": "Test context"}
        )
        assert response.status_code in [200, 422]
    
    async def test_direct_biasguard(self, async_client: AsyncClient):
        """Test direct BiasGuard endpoint."""
        response = await async_client.post(
            "/biasguard",
            json={"text": "Test text for bias detection"}
        )
        assert response.status_code in [200, 422]
    
    async def test_direct_healthguard(self, async_client: AsyncClient):
        """Test direct HealthGuard endpoint."""
        response = await async_client.post(
            "/healthguard",
            json={"text": "Health check"}
        )
        assert response.status_code in [200, 422]


@pytest.mark.asyncio
@pytest.mark.integration
class TestIntegratedGuardEndpoints:
    """Test integrated guard service endpoints."""
    
    async def test_integrated_tokenguard(self, async_client: AsyncClient):
        """Test integrated TokenGuard endpoint."""
        response = await async_client.post(
            "/tokenguard",
            json={"text": "Test text"}
        )
        assert response.status_code in [200, 422]
    
    async def test_integrated_trustguard(self, async_client: AsyncClient):
        """Test integrated TrustGuard endpoint."""
        response = await async_client.post(
            "/trustguard",
            json={"text": "Test content"}
        )
        assert response.status_code in [200, 422]
    
    async def test_integrated_contextguard(self, async_client: AsyncClient):
        """Test integrated ContextGuard endpoint."""
        response = await async_client.post(
            "/contextguard",
            json={"text": "Test context"}
        )
        assert response.status_code in [200, 422]
    
    async def test_integrated_biasguard(self, async_client: AsyncClient):
        """Test integrated BiasGuard endpoint."""
        response = await async_client.post(
            "/biasguard",
            json={"text": "Test text"}
        )
        assert response.status_code in [200, 422]
    
    async def test_integrated_healthguard(self, async_client: AsyncClient):
        """Test integrated HealthGuard endpoint."""
        response = await async_client.post(
            "/healthguard",
            json={"text": "Test"}
        )
        assert response.status_code in [200, 422]
    
    async def test_guard_metrics(self, async_client: AsyncClient):
        """Test guard service metrics endpoint."""
        response = await async_client.get("/metrics")
        assert response.status_code == 200
    
    async def test_guard_health_check(self, async_client: AsyncClient):
        """Test guard services health check."""
        response = await async_client.get("/health")
        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
class TestBiasEndpoints:
    """Test BiasGuard specific endpoints."""
    
    async def test_bias_detect(self, async_client: AsyncClient):
        """Test bias detection endpoint."""
        response = await async_client.post(
            "/biasguard/detect",
            json={"text": "Test text for bias detection"}
        )
        assert response.status_code in [200, 422]
    
    async def test_bias_analyze(self, async_client: AsyncClient):
        """Test bias analysis endpoint."""
        response = await async_client.post(
            "/biasguard/analyze",
            json={"text": "Test text for bias analysis"}
        )
        assert response.status_code in [200, 422]
    
    async def test_bias_health(self, async_client: AsyncClient):
        """Test BiasGuard health endpoint."""
        response = await async_client.get("/biasguard/health")
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
@pytest.mark.integration
class TestSubscriptionEndpoints:
    """Test subscription management endpoints."""
    
    async def test_get_subscription_tiers(self, async_client: AsyncClient):
        """Test getting subscription tiers (public)."""
        response = await async_client.get("/api/v1/subscriptions/tiers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list) or "items" in data
    
    async def test_get_current_subscription_unauthorized(self, async_client: AsyncClient):
        """Test getting current subscription without auth."""
        response = await async_client.get("/api/v1/subscriptions/current")
        assert response.status_code in [401, 403]
    
    async def test_create_checkout_session_unauthorized(self, async_client: AsyncClient):
        """Test creating checkout session without auth."""
        response = await async_client.post(
            "/api/v1/subscriptions/checkout",
            json={
                "tier_id": "1",
                "billing_cycle": "monthly",
                "success_url": "http://example.com/success",
                "cancel_url": "http://example.com/cancel"
            }
        )
        assert response.status_code in [401, 403]
    
    async def test_cancel_subscription_unauthorized(self, async_client: AsyncClient):
        """Test canceling subscription without auth."""
        response = await async_client.post("/api/v1/subscriptions/cancel")
        assert response.status_code in [401, 403]
    
    async def test_reactivate_subscription_unauthorized(self, async_client: AsyncClient):
        """Test reactivating subscription without auth."""
        response = await async_client.post("/api/v1/subscriptions/reactivate")
        assert response.status_code in [401, 403]
    
    async def test_get_subscription_usage_unauthorized(self, async_client: AsyncClient):
        """Test getting subscription usage without auth."""
        response = await async_client.get("/api/v1/subscriptions/usage")
        assert response.status_code in [401, 403]
    
    async def test_get_subscription_history_unauthorized(self, async_client: AsyncClient):
        """Test getting subscription history without auth."""
        response = await async_client.get("/api/v1/subscriptions/history")
        assert response.status_code in [401, 403]
    
    async def test_stripe_webhook_invalid(self, async_client: AsyncClient):
        """Test Stripe webhook without valid signature."""
        response = await async_client.post(
            "/api/v1/subscriptions/webhook/stripe",
            json={"type": "payment_intent.succeeded"}
        )
        # Should reject without valid signature
        assert response.status_code in [400, 401, 403, 500]


@pytest.mark.asyncio
@pytest.mark.integration
class TestOrganizationEndpoints:
    """Test organization management endpoints."""
    
    async def test_get_current_organization_unauthorized(self, async_client: AsyncClient):
        """Test getting current organization without auth."""
        response = await async_client.get("/api/v1/organizations/current")
        assert response.status_code in [401, 403]
    
    async def test_list_organization_members_unauthorized(self, async_client: AsyncClient):
        """Test listing organization members without auth."""
        response = await async_client.get("/api/v1/organizations/members")
        assert response.status_code in [401, 403]
    
    async def test_invite_member_unauthorized(self, async_client: AsyncClient):
        """Test inviting member without auth."""
        response = await async_client.post(
            "/api/v1/organizations/members/invite",
            json={"email": "newmember@example.com", "role": "member"}
        )
        assert response.status_code in [401, 403]
    
    async def test_update_member_unauthorized(self, async_client: AsyncClient):
        """Test updating member without auth."""
        response = await async_client.put(
            "/api/v1/organizations/members/123",
            json={"role": "admin"}
        )
        assert response.status_code in [401, 403, 404]
    
    async def test_delete_member_unauthorized(self, async_client: AsyncClient):
        """Test deleting member without auth."""
        response = await async_client.delete("/api/v1/organizations/members/123")
        assert response.status_code in [401, 403, 404]
    
    async def test_get_organization_subscription_unauthorized(self, async_client: AsyncClient):
        """Test getting organization subscription without auth."""
        response = await async_client.get("/api/v1/organizations/subscription")
        assert response.status_code in [401, 403]


@pytest.mark.asyncio
@pytest.mark.integration
class TestEnterpriseEndpoints:
    """Test enterprise setup endpoints."""
    
    async def test_enterprise_setup_unauthorized(self, async_client: AsyncClient):
        """Test enterprise setup without auth."""
        response = await async_client.post(
            "/api/v1/enterprise/setup",
            json={"org_name": "Test Org"}
        )
        assert response.status_code in [401, 403]
    
    async def test_enterprise_status_unauthorized(self, async_client: AsyncClient):
        """Test getting enterprise status without auth."""
        response = await async_client.get("/api/v1/enterprise/status")
        assert response.status_code in [401, 403]
    
    async def test_get_enterprise_config_unauthorized(self, async_client: AsyncClient):
        """Test getting enterprise config without auth."""
        response = await async_client.get("/api/v1/enterprise/config")
        assert response.status_code in [401, 403]
    
    async def test_update_enterprise_config_unauthorized(self, async_client: AsyncClient):
        """Test updating enterprise config without auth."""
        response = await async_client.put(
            "/api/v1/enterprise/config",
            json={"setting": "value"}
        )
        assert response.status_code in [401, 403]
    
    async def test_list_enterprise_services_unauthorized(self, async_client: AsyncClient):
        """Test listing enterprise services without auth."""
        response = await async_client.get("/api/v1/enterprise/services")
        assert response.status_code in [401, 403]
    
    async def test_restart_enterprise_service_unauthorized(self, async_client: AsyncClient):
        """Test restarting enterprise service without auth."""
        response = await async_client.post(
            "/api/v1/enterprise/services/restart",
            json={"service": "test"}
        )
        assert response.status_code in [401, 403]


@pytest.mark.asyncio
@pytest.mark.integration
class TestLegalEndpoints:
    """Test legal and compliance endpoints."""
    
    async def test_get_terms_of_service(self, async_client: AsyncClient):
        """Test getting terms of service (public)."""
        response = await async_client.get("/api/v1/legal/terms-of-service")
        assert response.status_code == 200
    
    async def test_get_privacy_policy(self, async_client: AsyncClient):
        """Test getting privacy policy (public)."""
        response = await async_client.get("/api/v1/legal/privacy-policy")
        assert response.status_code == 200
    
    async def test_get_cookie_policy(self, async_client: AsyncClient):
        """Test getting cookie policy (public)."""
        response = await async_client.get("/api/v1/legal/cookie-policy")
        assert response.status_code == 200
    
    async def test_accept_tos_unauthorized(self, async_client: AsyncClient):
        """Test accepting terms of service without auth."""
        response = await async_client.post(
            "/api/v1/legal/accept-tos",
            json={"accepted": True}
        )
        assert response.status_code in [401, 403]
    
    async def test_gdpr_export_unauthorized(self, async_client: AsyncClient):
        """Test GDPR data export without auth."""
        response = await async_client.get("/api/v1/legal/gdpr/export")
        assert response.status_code in [401, 403]
    
    async def test_gdpr_delete_unauthorized(self, async_client: AsyncClient):
        """Test GDPR data deletion without auth."""
        response = await async_client.delete("/api/v1/legal/gdpr/delete")
        assert response.status_code in [401, 403]
    
    async def test_get_audit_logs_unauthorized(self, async_client: AsyncClient):
        """Test getting audit logs without auth."""
        response = await async_client.get("/api/v1/legal/audit-logs")
        assert response.status_code in [401, 403]
    
    async def test_get_compliance_status_unauthorized(self, async_client: AsyncClient):
        """Test getting compliance status without auth."""
        response = await async_client.get("/api/v1/legal/compliance-status")
        assert response.status_code in [401, 403]
    
    async def test_data_retention_cleanup_unauthorized(self, async_client: AsyncClient):
        """Test data retention cleanup without auth."""
        response = await async_client.post("/api/v1/legal/data-retention/cleanup")
        assert response.status_code in [401, 403]


@pytest.mark.asyncio
@pytest.mark.integration
class TestConfigEndpoints:
    """Test configuration management endpoints."""
    
    async def test_get_config_unauthorized(self, async_client: AsyncClient):
        """Test getting config without auth."""
        response = await async_client.get("/api/v1/config/config")
        assert response.status_code in [401, 403]
    
    async def test_get_rate_limits_unauthorized(self, async_client: AsyncClient):
        """Test getting rate limits without auth."""
        response = await async_client.get("/api/v1/config/config/rate-limits")
        assert response.status_code in [401, 403]
    
    async def test_update_rate_limits_unauthorized(self, async_client: AsyncClient):
        """Test updating rate limits without auth."""
        response = await async_client.put(
            "/api/v1/config/config/rate-limits",
            json={"limit": 100}
        )
        assert response.status_code in [401, 403]
    
    async def test_get_feature_flags_unauthorized(self, async_client: AsyncClient):
        """Test getting feature flags without auth."""
        response = await async_client.get("/api/v1/config/config/feature-flags")
        assert response.status_code in [401, 403]
    
    async def test_update_feature_flags_unauthorized(self, async_client: AsyncClient):
        """Test updating feature flags without auth."""
        response = await async_client.put(
            "/api/v1/config/config/feature-flags",
            json={"flag": "test"}
        )
        assert response.status_code in [401, 403]
    
    async def test_update_cache_config_unauthorized(self, async_client: AsyncClient):
        """Test updating cache config without auth."""
        response = await async_client.put(
            "/api/v1/config/config/cache",
            json={"ttl": 3600}
        )
        assert response.status_code in [401, 403]
    
    async def test_get_config_status_unauthorized(self, async_client: AsyncClient):
        """Test getting config status without auth."""
        response = await async_client.get("/api/v1/config/config/status")
        assert response.status_code in [401, 403]
    
    async def test_reload_config_unauthorized(self, async_client: AsyncClient):
        """Test reloading config without auth."""
        response = await async_client.post("/api/v1/config/config/reload")
        assert response.status_code in [401, 403]
    
    async def test_export_config_unauthorized(self, async_client: AsyncClient):
        """Test exporting config without auth."""
        response = await async_client.get("/api/v1/config/config/export")
        assert response.status_code in [401, 403]


@pytest.mark.asyncio
@pytest.mark.integration
class TestAnalyticsEndpoints:
    """Test analytics endpoints."""
    
    async def test_get_benefits_overview(self, async_client: AsyncClient):
        """Test getting benefits overview."""
        response = await async_client.get("/api/v1/analytics/benefits/overview")
        assert response.status_code == 200
    
    async def test_get_benefits_detailed(self, async_client: AsyncClient):
        """Test getting detailed benefits."""
        response = await async_client.get("/api/v1/analytics/benefits/detailed")
        assert response.status_code == 200
    
    async def test_get_performance_dashboard(self, async_client: AsyncClient):
        """Test getting performance dashboard."""
        response = await async_client.get("/api/v1/analytics/performance/dashboard")
        assert response.status_code == 200
    
    async def test_get_guard_metrics(self, async_client: AsyncClient):
        """Test getting specific guard metrics."""
        response = await async_client.get("REPLACE_ME")
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
@pytest.mark.integration
class TestUploadEndpoints:
    """Test file upload endpoints."""
    
    async def test_direct_upload_unauthorized(self, async_client: AsyncClient):
        """Test direct upload without auth."""
        files = {"file": ("test.txt", b"test content", "text/plain")}
        response = await async_client.post("/api/v1/upload/direct", files=files)
        assert response.status_code in [401, 403]
    
    async def test_presigned_upload_unauthorized(self, async_client: AsyncClient):
        """Test presigned upload without auth."""
        response = await async_client.post(
            "/api/v1/upload/presigned",
            json={"filename": "test.txt", "content_type": "text/plain"}
        )
        assert response.status_code in [401, 403]
    
    async def test_download_file_not_found(self, async_client: AsyncClient):
        """Test downloading non-existent file."""
        response = await async_client.get("/api/v1/upload/download/99999")
        assert response.status_code in [404, 401, 403]
    
    async def test_get_download_url_not_found(self, async_client: AsyncClient):
        """Test getting download URL for non-existent file."""
        response = await async_client.get("/api/v1/upload/download/99999/url")
        assert response.status_code in [404, 401, 403]
    
    async def test_get_file_metadata_not_found(self, async_client: AsyncClient):
        """Test getting metadata for non-existent file."""
        response = await async_client.get("/api/v1/upload/metadata/99999")
        assert response.status_code in [404, 401, 403]
    
    async def test_delete_file_unauthorized(self, async_client: AsyncClient):
        """Test deleting file without auth."""
        response = await async_client.delete("/api/v1/upload/123")
        assert response.status_code in [401, 403, 404]
    
    async def test_list_files_unauthorized(self, async_client: AsyncClient):
        """Test listing files without auth."""
        response = await async_client.get("/api/v1/upload/list")
        assert response.status_code in [401, 403]
    
    async def test_upload_health(self, async_client: AsyncClient):
        """Test upload service health."""
        response = await async_client.get("/api/v1/upload/health")
        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
class TestABTestingEndpoints:
    """Test A/B testing endpoints."""
    
    async def test_create_experiment_unauthorized(self, async_client: AsyncClient):
        """Test creating experiment without auth."""
        response = await async_client.post(
            "/experiments",
            json={"name": "test_experiment"}
        )
        assert response.status_code in [401, 403, 404]
    
    async def test_list_experiments_unauthorized(self, async_client: AsyncClient):
        """Test listing experiments without auth."""
        response = await async_client.get("/experiments")
        assert response.status_code in [401, 403, 404]
    
    async def test_get_experiment_unauthorized(self, async_client: AsyncClient):
        """Test getting experiment without auth."""
        response = await async_client.get("/experiments/123")
        assert response.status_code in [401, 403, 404]
    
    async def test_update_experiment_unauthorized(self, async_client: AsyncClient):
        """Test updating experiment without auth."""
        response = await async_client.put(
            "/experiments/123",
            json={"name": "updated"}
        )
        assert response.status_code in [401, 403, 404]
    
    async def test_start_experiment_unauthorized(self, async_client: AsyncClient):
        """Test starting experiment without auth."""
        response = await async_client.post("/experiments/123/start")
        assert response.status_code in [401, 403, 404]
    
    async def test_stop_experiment_unauthorized(self, async_client: AsyncClient):
        """Test stopping experiment without auth."""
        response = await async_client.post("/experiments/123/stop")
        assert response.status_code in [401, 403, 404]
    
    async def test_assign_user_unauthorized(self, async_client: AsyncClient):
        """Test assigning user to experiment without auth."""
        response = await async_client.post(
            "/assign-user",
            json={"user_id": "123", "experiment_id": "456"}
        )
        assert response.status_code in [401, 403, 404]
    
    async def test_get_user_variants_unauthorized(self, async_client: AsyncClient):
        """Test getting user variants without auth."""
        response = await async_client.get("/users/123/variants")
        assert response.status_code in [401, 403, 404]
    
    async def test_submit_results_unauthorized(self, async_client: AsyncClient):
        """Test submitting results without auth."""
        response = await async_client.post(
            "/results",
            json={"experiment_id": "123"}
        )
        assert response.status_code in [401, 403, 404]
    
    async def test_get_experiment_analysis_unauthorized(self, async_client: AsyncClient):
        """Test getting experiment analysis without auth."""
        response = await async_client.get("/experiments/123/analysis")
        assert response.status_code in [401, 403, 404]
    
    async def test_analyze_experiment_unauthorized(self, async_client: AsyncClient):
        """Test analyzing experiment without auth."""
        response = await async_client.post("/experiments/123/analyze")
        assert response.status_code in [401, 403, 404]
    
    async def test_get_experiment_metrics_unauthorized(self, async_client: AsyncClient):
        """Test getting experiment metrics without auth."""
        response = await async_client.get("/experiments/123/metrics")
        assert response.status_code in [401, 403, 404]
    
    async def test_get_experiment_status_unauthorized(self, async_client: AsyncClient):
        """Test getting experiment status without auth."""
        response = await async_client.get("/experiments/123/status")
        assert response.status_code in [401, 403, 404]


@pytest.mark.asyncio
@pytest.mark.integration
class TestWebhookEndpoints:
    """Test webhook endpoints."""
    
    async def test_stripe_webhook_invalid(self, async_client: AsyncClient):
        """Test Stripe webhook without valid signature."""
        response = await async_client.post(
            "/webhooks/stripe",
            json={"type": "payment_intent.succeeded", "data": {}}
        )
        # Should reject without valid signature
        assert response.status_code in [400, 401, 403, 500]
    
    async def test_list_stripe_products(self, async_client: AsyncClient):
        """Test listing Stripe products."""
        response = await async_client.get("/webhooks/stripe/products")
        assert response.status_code in [200, 401, 403]
    
    async def test_get_stripe_price(self, async_client: AsyncClient):
        """Test getting Stripe price."""
        response = await async_client.get("/webhooks/stripe/prices/123")
        assert response.status_code in [404, 401, 403]
    
    async def test_get_stripe_customer(self, async_client: AsyncClient):
        """Test getting Stripe customer."""
        response = await async_client.get("/webhooks/stripe/customers/test@test.com")
        assert response.status_code in [200, 404, 401, 403]
    
    async def test_get_stripe_subscriptions(self, async_client: AsyncClient):
        """Test getting Stripe subscriptions."""
        response = await async_client.get("/webhooks/stripe/subscriptions/123")
        assert response.status_code in [200, 404, 401, 403]
    
    async def test_get_stripe_invoices(self, async_client: AsyncClient):
        """Test getting Stripe invoices."""
        response = await async_client.get("/webhooks/stripe/invoices/123")
        assert response.status_code in [200, 404, 401, 403]
    
    async def test_clerk_webhook_invalid(self, async_client: AsyncClient):
        """Test Clerk webhook without valid signature."""
        response = await async_client.post(
            "/webhooks/clerk",
            json={"type": "user.created", "data": {}}
        )
        # Should reject without valid signature
        assert response.status_code in [400, 401, 403, 500]
    
    async def test_get_clerk_user(self, async_client: AsyncClient):
        """Test getting Clerk user."""
        response = await async_client.get("/webhooks/clerk/users/123")
        assert response.status_code in [404, 401, 403]
    
    async def test_get_clerk_user_by_email(self, async_client: AsyncClient):
        """Test getting Clerk user by email."""
        response = await async_client.get("/webhooks/clerk/users/email/test@test.com")
        assert response.status_code in [404, 401, 403]


@pytest.mark.asyncio
@pytest.mark.integration
class TestInternalEndpoints:
    """Test internal guard service endpoints."""
    
    async def test_internal_tokenguard_optimize(self, async_client: AsyncClient):
        """Test internal TokenGuard optimize endpoint."""
        response = await async_client.post(
            "/tokenguard/optimize",
            json={"text": "test"}
        )
        assert response.status_code in [200, 422, 404]
    
    async def test_internal_trustguard_validate(self, async_client: AsyncClient):
        """Test internal TrustGuard validate endpoint."""
        response = await async_client.post(
            "/trustguard/validate",
            json={"text": "test"}
        )
        assert response.status_code in [200, 422, 404]
    
    async def test_internal_contextguard_analyze(self, async_client: AsyncClient):
        """Test internal ContextGuard analyze endpoint."""
        response = await async_client.post(
            "/contextguard/analyze",
            json={"text": "test"}
        )
        assert response.status_code in [200, 422, 404]
    
    async def test_internal_biasguard_detect(self, async_client: AsyncClient):
        """Test internal BiasGuard detect endpoint."""
        response = await async_client.post(
            "/biasguard/detect",
            json={"text": "test"}
        )
        assert response.status_code in [200, 422, 404]
    
    async def test_internal_healthguard_monitor(self, async_client: AsyncClient):
        """Test internal HealthGuard monitor endpoint."""
        response = await async_client.post(
            "/healthguard/monitor",
            json={"text": "test"}
        )
        assert response.status_code in [200, 422, 404]
    
    async def test_internal_testing_token(self, async_client: AsyncClient):
        """Test internal testing token endpoint."""
        response = await async_client.get("/api/v1/internal-testing/token")
        # May be 404 if internal testing is disabled
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
@pytest.mark.integration
class TestServiceDiscoveryEndpoints:
    """Test service discovery endpoints."""
    
    async def test_register_service_invalid(self, async_client: AsyncClient):
        """Test registering service with invalid data."""
        response = await async_client.post(
            "/api/v1/guards/discovery/register",
            json={"name": "test", "url": "http://test"}
        )
        assert response.status_code in [200, 400, 422]
    
    async def test_delete_service_not_found(self, async_client: AsyncClient):
        """Test deleting non-existent service."""
        response = await async_client.delete("/api/v1/guards/discovery/services/non-existent")
        assert response.status_code in [404, 400]
    
    async def test_refresh_discovery(self, async_client: AsyncClient):
        """Test refreshing service discovery."""
        response = await async_client.post("/api/v1/guards/discovery/refresh")
        assert response.status_code in [200, 401, 403]

