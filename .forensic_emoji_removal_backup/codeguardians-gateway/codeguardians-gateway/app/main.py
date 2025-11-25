"""
Main FastAPI application entry point.

This module creates and configures the FastAPI application with all
necessary middleware, routes, and error handlers.
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from datetime import datetime

from fastapi import FastAPI, Request, Response, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, generate_latest
import time

from app.core.config import get_settings
from app.core.database import init_db
from app.core.exceptions import (
    BaseAPIException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    InternalServerError,
    StripeError,
    StripeWebhookError,
    ClerkError,
    ClerkTokenError,
    ClerkWebhookError,
    ClerkJWKSFetchError
)
from app.utils.retry import circuit_breaker_registry
from app.api.v1.bias import router as bias_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.guards_integrated import router as guards_integrated_router
from app.api.v1.direct_guards import router as direct_guards_router
from app.api.v1 import auth, users, posts, guards, organizations, subscriptions, enterprise, legal, ab_testing, upload, config, performance
from app.api.v1.guards import GuardRequest
from app.api.webhooks import stripe_webhooks_router, clerk_webhooks_router, stripe_api_router
from app.api.internal import guards as internal_guards
from app.core.guard_orchestrator import orchestrator
from app.utils.logging import setup_logging, get_logger
from app.middleware.usage_tracking import usage_tracking_middleware
from app.middleware.dynamic_rate_limiting import dynamic_rate_limiting_middleware
from app.core.security import security_middleware
from app.core.circuit_breaker import circuit_breaker_manager
from app.core.config_validation import config_validator, validate_configuration
from app.core.health_monitor import health_monitor

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager with graceful shutdown."""
    # Initialize tracing if enabled
    from app.core.tracing import initialize_tracing
    import os
    if os.getenv("OTEL_ENABLED", "false").lower() == "true":
        initialize_tracing(
            service_name="codeguardians-gateway",
            sampling_rate=float(os.getenv("OTEL_SAMPLING_RATE", "1.0"))
        )
        logger.info("✅ Distributed tracing initialized")
    
    # Register graceful shutdown handlers
    from app.core.graceful_shutdown import register_shutdown_handler, get_request_drainer
    
    async def shutdown_orchestrator():
        """Shutdown guard orchestrator."""
        await orchestrator.shutdown()
    
    async def shutdown_job_queue():
        """Shutdown job queue."""
        if 'job_queue' in locals():
            await job_queue.stop_workers()
    
    async def shutdown_database():
        """Close database connections."""
        from app.core.database import get_engine
        engine = get_engine()
        await engine.dispose()
    
    async def shutdown_connection_pools():
        """Close connection pools."""
        from app.core.connection_pool_optimizer import get_connection_optimizer
        optimizer = get_connection_optimizer()
        await optimizer.close_all()
    
    register_shutdown_handler(shutdown_orchestrator)
    register_shutdown_handler(shutdown_job_queue)
    register_shutdown_handler(shutdown_database)
    register_shutdown_handler(shutdown_connection_pools)
    
    # Startup
    logger.info("🚀 Starting CodeGuardians Gateway...")
    
    # Initialize database
    await init_db()
    logger.info("✅ Database initialized")
    
    # Initialize guard orchestrator
    await orchestrator.initialize()
    logger.info("✅ Guard orchestrator initialized")
    
    # Initialize performance optimizers
    from app.core.connection_pool_optimizer import get_connection_optimizer
    from app.core.performance_optimizer import get_performance_optimizer
    connection_optimizer = get_connection_optimizer()
    performance_optimizer = get_performance_optimizer()
    logger.info("✅ Performance optimizers initialized")
    
    # BiasGuard now runs as a separate Node.js service
    logger.info("✅ BiasGuard service will be initialized as separate container")

    # Run database migrations
    from app.core.database import run_migrations
    await run_migrations()
    logger.info("✅ Database migrations completed")
    
    # Initialize guard metrics tables
    from app.core.guard_metrics_migration import run_guard_metrics_migration
    await run_guard_metrics_migration()
    logger.info("✅ Guard metrics tables initialized")

    # Initialize job queue
    from app.core.job_queue import initialize_job_queue, register_job_handler
    job_queue = await initialize_job_queue()

    # Register job handlers
    await _register_job_handlers(job_queue)
    logger.info("✅ Job queue initialized")

    logger.info("✅ CodeGuardians Gateway started successfully")
    
    yield
    
    # Graceful shutdown
    logger.info("🛑 Initiating graceful shutdown...")
    
    # Drain in-flight requests with timeout
    drainer = get_request_drainer()
    if drainer.get_in_flight_count() > 0:
        logger.info(f"Draining {drainer.get_in_flight_count()} in-flight requests...")
        drained = await drainer.drain()
        if not drained:
            logger.warning("Shutdown timeout exceeded, forcing termination")
    
    # Execute shutdown handlers (registered above) with timeout
    from app.core.graceful_shutdown import _execute_shutdown_handlers
    import asyncio
    try:
        await asyncio.wait_for(_execute_shutdown_handlers(), timeout=10.0)
    except asyncio.TimeoutError:
        logger.warning("Shutdown handlers timeout exceeded, forcing termination")
    
    logger.info("✅ CodeGuardians Gateway shutdown complete")


async def _register_job_handlers(job_queue):
    """Register background job handlers."""
    from app.core.job_queue import Job

    # Example job handlers - these can be expanded based on needs
    async def email_notification_job(job: Job):
        """Send email notifications."""
        try:
            payload = job.payload
            recipient = payload.get("recipient")
            subject = payload.get("subject", "AI Guardian Notification")
            body = payload.get("body", "")

            # Use existing email service
            from app.services.email_service import send_email
            await send_email(recipient, subject, body)

            logger.info(f"Email notification sent to {recipient}")

        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            raise

    async def data_cleanup_job(job: Job):
        """Clean up old data for compliance."""
        try:
            payload = job.payload
            days_to_keep = payload.get("days_to_keep", 90)

            # Use existing legal service cleanup
            from app.api.v1.legal import cleanup_old_data
            # This would need to be adapted to work with job context
            logger.info(f"Data cleanup job completed for {days_to_keep} days retention")

        except Exception as e:
            logger.error(f"Failed to cleanup data: {e}")
            raise

    async def analytics_update_job(job: Job):
        """Update analytics data."""
        try:
            payload = job.payload
            # Update analytics data, refresh caches, etc.
            logger.info("Analytics update job completed")

        except Exception as e:
            logger.error(f"Failed to update analytics: {e}")
            raise

    async def health_check_job(job: Job):
        """Perform comprehensive health checks."""
        try:
            # Trigger health checks for all services
            from app.core.guard_orchestrator import orchestrator
            await orchestrator.refresh_health_status()
            logger.info("Health check job completed")

        except Exception as e:
            logger.error(f"Failed to perform health checks: {e}")
            raise

    # Register handlers
    await job_queue.register_handler("email_notification", email_notification_job)
    await job_queue.register_handler("data_cleanup", data_cleanup_job)
    await job_queue.register_handler("analytics_update", analytics_update_job)
    await job_queue.register_handler("health_check", health_check_job)

    # Start workers
    await job_queue.start_workers(num_workers=2, queues=["default", "analytics", "maintenance"])


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    # Reload settings if TESTING is set
    import os
    if os.getenv("TESTING", "false").lower() in ("true", "1", "yes"):
        from app.core.config import reload_settings
        settings = reload_settings()
    else:
        settings = get_settings()
    
    # Enable Swagger UI only in development environment
    # Security: Documentation endpoints disabled in production
    environment = os.getenv("ENVIRONMENT", settings.ENVIRONMENT).lower()
    is_development = environment == "development"
    
    app = FastAPI(
        title="AI Guardian API",
        description="Unified API for AI Guard Services - TokenGuard, TrustGuard, ContextGuard, and BiasGuard",
        version="1.0.0",
        author="Bravetto",
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/mit"
        },
        servers=[
            {"url": "https://api.aiguardian.ai", "description": "Production API"},
            {"url": "https://api.internal.aiguardian.ai", "description": "Internal API"},
            {"url": f"http://{os.getenv('HOST', 'localhost')}:{int(os.getenv('PORT', os.getenv('GATEWAY_PORT', '8000')))}", "description": "Development API"}
        ],
        docs_url="/docs" if is_development else None,
        redoc_url="/redoc" if is_development else None,
        openapi_url="/openapi.json" if is_development else None,
        lifespan=lifespan
    )
    
    # Add middleware
    _add_middleware(app)
    
    # Add routes
    _add_routes(app)
    
    # Add exception handlers
    _add_exception_handlers(app)
    
    # Add health checks
    _add_health_checks(app)
    
    logger.info("FastAPI application created successfully")
    return app


def _add_middleware(app: FastAPI) -> None:
    """Add middleware to the application."""
    
    # Clerk authentication middleware (if enabled)
    if settings.is_clerk_enabled:
        from app.core.clerk_auth import ClerkAuthMiddleware
        app.add_middleware(ClerkAuthMiddleware)
        logger.info("Clerk authentication middleware enabled")
    
    # CORS middleware - Configured for VS Code and Chrome extension compatibility
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],  # Expose all headers for extension access
    )

    # Tenant context middleware - extracts tenant context from requests
    from app.middleware.tenant_context import TenantContextMiddleware
    app.add_middleware(TenantContextMiddleware)
    logger.info("Tenant context middleware enabled")

    # NOTE: Host validation middleware removed - network security handled at cloud/infrastructure level (AWS EKS)
    # Danny's infrastructure (EKS, Linkerd, network policies) provides network security
    # Application-level host validation is redundant and causes issues with Kubernetes internal services
    logger.info("Host validation middleware disabled - relying on cloud infrastructure security")
    
    # Request logging and metrics middleware with request ID correlation
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        """Log requests and collect metrics with request ID correlation."""
        import uuid
        start_time = time.time()
        
        # Extract or generate request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Store request ID in request state for use throughout request lifecycle
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add request ID to response headers for correlation
        response.headers["X-Request-ID"] = request_id
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Update metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        # Add request ID to tracing span if tracing enabled
        try:
            from app.core.tracing import set_span_request_id
            set_span_request_id(request_id)
        except Exception:
            pass  # Tracing not critical, continue if unavailable
        
        # Track in-flight requests for graceful shutdown
        try:
            from app.core.graceful_shutdown import get_request_drainer
            drainer = get_request_drainer()
            await drainer.add_request()
        except Exception:
            pass  # Graceful shutdown not critical, continue if unavailable
        
        # Log request with correlation ID
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.3f}s - "
            f"Request-ID: {request_id}"
        )
        
        # Remove request from drainer after completion
        try:
            if 'drainer' in locals():
                await drainer.remove_request()
        except Exception:
            pass
        
        return response
    
    # Security headers middleware
    @app.middleware("http")
    async def security_headers_middleware(request: Request, call_next):
        """Add security headers to responses."""
        response = await call_next(request)
        
        # Determine if this is a documentation endpoint
        is_docs_endpoint = request.url.path in ["/docs", "/redoc", "/openapi.json"]
        
        # Security headers
        response.headers["X-Frame-Options"] = "SAMEORIGIN" if is_docs_endpoint else "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # More permissive CSP for documentation endpoints to allow Swagger UI CDN resources
        if is_docs_endpoint:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self'"
            )
        else:
            response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response
    
    # Usage tracking middleware
    app.middleware("http")(usage_tracking_middleware)
    
    # Dynamic rate limiting middleware
    app.middleware("http")(dynamic_rate_limiting_middleware)


def _add_routes(app: FastAPI) -> None:
    """Add API routes to the application."""
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        env = os.getenv("ENVIRONMENT", settings.ENVIRONMENT).lower()
        return {
            "service": "codeguardians-gateway",
            "version": "0.1.0",
            "status": "running",
            "docs": "/docs" if env == "development" else "disabled (development only)",
            "health": "/health",
            "api": "/api/v1"
        }
    
    # Include API routers
    app.include_router(bias_router)
    app.include_router(analytics_router)
    app.include_router(guards_integrated_router, tags=["Integrated Guard Services"])
    app.include_router(direct_guards_router, tags=["Direct Guard Access"])
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(posts.router, prefix="/api/v1/posts", tags=["Posts"])
    app.include_router(guards.router, tags=["Guard Services"])
    # Admin router for guard services management
    from app.api.v1.admin import guards as admin_guards
    app.include_router(admin_guards.router, tags=["Guard Admin"])
    app.include_router(organizations.router, prefix="/api/v1", tags=["Organizations"])
    app.include_router(subscriptions.router, prefix="/api/v1", tags=["Subscriptions"])
    app.include_router(enterprise.router, prefix="/api/v1", tags=["Enterprise Setup"])
    app.include_router(legal.router, prefix="/api/v1/legal", tags=["Legal & Compliance"])
    app.include_router(config.router, prefix="/api/v1", tags=["Configuration"])
    app.include_router(performance.router)
    app.include_router(ab_testing.router, tags=["A/B Testing"])
    app.include_router(ab_testing.legacy_router, tags=["A/B Testing (Legacy)"])
    app.include_router(upload.router, prefix="/api/v1", tags=["File Upload"])
    app.include_router(stripe_webhooks_router, prefix="/webhooks", tags=["Stripe Webhooks"])
    app.include_router(stripe_api_router, prefix="/stripe", tags=["Stripe API"])
    app.include_router(clerk_webhooks_router, prefix="/webhooks", tags=["Clerk Webhooks"])
    
    # Expose webhook endpoints for testing (ngrok/public access)
    @app.get("/webhooks/health", tags=["Webhooks"])
    async def webhooks_health():
        """Health check endpoint for webhook services."""
        return {
            "status": "healthy",
            "webhooks": {
                "stripe": "/api/v1/webhooks/stripe",
                "clerk": "/api/v1/webhooks/clerk"
            },
            "timestamp": datetime.now().isoformat()
        }
    
    @app.get("/webhooks", tags=["Webhooks"])
    async def list_webhook_endpoints():
        """List all available webhook endpoints for testing."""
        base_url = settings.BASE_URL or "http://localhost:8000"
        return {
            "webhooks": {
                "stripe": {
                    "url": f"{base_url}/api/v1/webhooks/stripe",
                    "method": "POST",
                    "description": "Stripe payment webhook events"
                },
                "clerk": {
                    "url": f"{base_url}/api/v1/webhooks/clerk",
                    "method": "POST",
                    "description": "Clerk authentication webhook events"
                }
            },
            "health": f"{base_url}/webhooks/health"
        }
    
    # Include internal routers (for internal services only)
    app.include_router(internal_guards.router, tags=["Internal Guard Services"])
    
    # Add scan endpoint as alias for guards/process
    @app.post("/api/v1/scan")
    async def scan_text_alias(request: GuardRequest, http_request: Request, background_tasks: BackgroundTasks):
        """Scan text endpoint - alias for guards/process."""
        from app.api.v1.guards import process_guard_request
        
        return await process_guard_request(request, background_tasks, http_request)
    
    # Add analyze endpoint as alias for guards/process
    @app.post("/api/v1/analyze")
    async def analyze_alias(request: GuardRequest, http_request: Request, background_tasks: BackgroundTasks):
        """Analyze endpoint - alias for guards/process."""
        from app.api.v1.guards import process_guard_request
        
        return await process_guard_request(request, background_tasks, http_request)
    
    # Metrics endpoint
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint."""
        return Response(
            generate_latest(),
            media_type="text/plain"
        )
    
    # Internal Testing endpoint
    @app.get("/api/v1/internal-testing/token")
    async def get_internal_testing_token():
        """Get internal testing JWT token for extension development."""
        if not settings.is_internal_testing_enabled:
            raise HTTPException(
                status_code=404, 
                detail="Internal testing not enabled"
            )
        
        host = os.getenv("HOST", "localhost")
        port = os.getenv("PORT", os.getenv("GATEWAY_PORT", "8000"))
        api_url = f"http://{host}:{port}"
        
        return {
            "jwt_token": settings.INTERNAL_TESTING_JWT_TOKEN,
            "api_url": api_url,
            "expires_at": "Never (internal testing token)",
            "usage_instructions": {
                "chrome_extension": "Use as Authorization: Bearer <token> header",
                "vscode_extension": "Use as Authorization: Bearer <token> header",
                "curl_example": f"curl -H 'Authorization: Bearer <token>' {api_url}/api/v1/guards/process"
            }
        }


def _add_exception_handlers(app: FastAPI) -> None:
    """Add global exception handlers with standardized format."""
    from app.api.error_handler import (
        handle_base_api_exception,
        handle_http_exception,
        handle_validation_error as handle_validation_error_std,
        handle_generic_exception
    )
    from fastapi.exceptions import RequestValidationError
    
    # Standardized handlers for BaseAPIException
    @app.exception_handler(BaseAPIException)
    async def base_api_exception_handler(request: Request, exc: BaseAPIException):
        """Handle BaseAPIException with standardized format."""
        return await handle_base_api_exception(request, exc)
    
    # Request validation errors (FastAPI built-in)
    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors with standardized format."""
        return await handle_validation_error_std(request, exc)
    
    # Legacy handlers for backward compatibility (now use standardized format)
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        """Handle validation errors (uses standardized format)."""
        return await handle_base_api_exception(request, exc)
    
    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(request: Request, exc: AuthenticationError):
        """Handle authentication errors."""
        return JSONResponse(
            status_code=401,
            content={
                "error": "Authentication Error",
                "message": str(exc)
            }
        )
    
    @app.exception_handler(AuthorizationError)
    async def authorization_error_handler(request: Request, exc: AuthorizationError):
        """Handle authorization errors."""
        return JSONResponse(
            status_code=403,
            content={
                "error": "Authorization Error",
                "message": str(exc)
            }
        )
    
    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError):
        """Handle not found errors."""
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "message": str(exc)
            }
        )
    
    @app.exception_handler(ConflictError)
    async def conflict_error_handler(request: Request, exc: ConflictError):
        """Handle conflict errors."""
        return JSONResponse(
            status_code=409,
            content={
                "error": "Conflict",
                "message": str(exc)
            }
        )
    
    @app.exception_handler(InternalServerError)
    async def internal_server_error_handler(request: Request, exc: InternalServerError):
        """Handle internal server errors."""
        logger.error(f"Internal server error: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred"
            }
        )

    # Stripe-specific exception handlers
    @app.exception_handler(StripeError)
    async def stripe_error_handler(request: Request, exc: StripeError):
        """Handle Stripe API errors."""
        logger.error(f"Stripe API error: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Stripe API Error",
                "error_code": exc.error_code,
                "message": str(exc),
                "details": exc.details
            }
        )

    @app.exception_handler(StripeWebhookError)
    async def stripe_webhook_error_handler(request: Request, exc: StripeWebhookError):
        """Handle Stripe webhook processing errors."""
        logger.error(f"Stripe webhook processing error: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Stripe Webhook Error",
                "error_code": exc.error_code,
                "message": str(exc),
                "details": exc.details
            }
        )

    # Clerk-specific exception handlers
    @app.exception_handler(ClerkError)
    async def clerk_error_handler(request: Request, exc: ClerkError):
        """Handle Clerk API errors."""
        logger.error(f"Clerk API error: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Clerk API Error",
                "error_code": exc.error_code,
                "message": str(exc),
                "details": exc.details
            }
        )

    @app.exception_handler(ClerkTokenError)
    async def clerk_token_error_handler(request: Request, exc: ClerkTokenError):
        """Handle Clerk token validation errors."""
        logger.warning(f"Clerk token validation error: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Authentication Error",
                "error_code": exc.error_code,
                "message": str(exc),
                "details": exc.details
            }
        )

    @app.exception_handler(ClerkWebhookError)
    async def clerk_webhook_error_handler(request: Request, exc: ClerkWebhookError):
        """Handle Clerk webhook processing errors."""
        logger.error(f"Clerk webhook processing error: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Clerk Webhook Error",
                "error_code": exc.error_code,
                "message": str(exc),
                "details": exc.details
            }
        )

    @app.exception_handler(ClerkJWKSFetchError)
    async def clerk_jwks_fetch_error_handler(request: Request, exc: ClerkJWKSFetchError):
        """Handle Clerk JWKS fetch errors."""
        logger.error(f"Clerk JWKS fetch error: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Service Unavailable",
                "error_code": exc.error_code,
                "message": str(exc),
                "details": exc.details
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions with standardized format."""
        return await handle_http_exception(request, exc)
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions with standardized format."""
        # Don't catch HTTPException or our custom exceptions - let specific handlers deal with them
        if isinstance(exc, (HTTPException, BaseAPIException, ValidationError, AuthenticationError, AuthorizationError, NotFoundError, ConflictError, InternalServerError, StripeError, StripeWebhookError, ClerkError, ClerkWebhookError, ClerkJWKSFetchError)):
            raise exc

        return await handle_generic_exception(request, exc)


def _add_health_checks(app: FastAPI) -> None:
    """Add health check endpoints."""
    
    @app.get("/health")
    async def health_check():
        """Simple health check endpoint."""
        return {
            "status": "healthy",
            "service": "codeguardians-gateway",
            "version": "0.1.0",
            "timestamp": time.time(),
            "circuit_breakers": circuit_breaker_registry.get_all_states()
        }
    
    @app.get("/health/live")
    async def liveness_check():
        """Liveness probe for Kubernetes (optimized <50ms)."""
        from app.core.optimized_health import get_health_checker
        return await get_health_checker().liveness_check()
    
    @app.get("/health/ready")
    async def readiness_check(check_dependencies: bool = True):
        """Readiness probe for Kubernetes with dependency checks."""
        from app.core.optimized_health import get_health_checker
        return await get_health_checker().readiness_check(check_dependencies=check_dependencies)
    
    @app.get("/health/comprehensive")
    async def comprehensive_health_check():
        """Comprehensive health check with all services and system metrics."""
        try:
            health_data = await health_monitor.get_comprehensive_health()
            return health_data
        except Exception as e:
            logger.error(f"Comprehensive health check failed: {e}")
            return {
                "status": "error",
                "timestamp": time.time(),
                "error": str(e)
            }
    
    @app.get("/health/circuit-breakers")
    async def circuit_breaker_status():
        """Get circuit breaker status for all services."""
        try:
            return circuit_breaker_manager.get_all_states()
        except Exception as e:
            logger.error(f"Circuit breaker status check failed: {e}")
            return {"error": str(e)}
    
    @app.get("/health/configuration")
    async def configuration_health():
        """Check configuration validity."""
        try:
            config_report = validate_configuration()
            return config_report
        except Exception as e:
            logger.error(f"Configuration health check failed: {e}")
            return {"error": str(e)}


# Create the application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT or GATEWAY_PORT environment variable, default to 8000
    port = int(os.getenv("PORT", os.getenv("GATEWAY_PORT", "8000")))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=settings.ENVIRONMENT == "development",
        log_level=(settings.LOG_LEVEL or "INFO").lower()
    )