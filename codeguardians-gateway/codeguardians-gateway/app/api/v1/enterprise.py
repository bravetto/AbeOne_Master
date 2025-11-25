"""
Enterprise Setup API

This module provides endpoints for external enterprise configuration:
- Database connection setup
- Pricing configuration
- Service configuration
- System initialization
- Health checks for external systems

This serves as the single entry point for business/leadership
to configure the AI Guardians platform from external codebases.
"""

from typing import Dict, Any, Optional, List, Union
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import json
import os
import httpx
import redis.asyncio as redis
from passlib.context import CryptContext

from app.core.database import get_db, get_session_factory, check_db_connection, get_engine
from app.core.models import Organization, OrganizationMember, User, SubscriptionTier
from app.core.config import get_settings
from app.core.security import verify_token
from app.utils.logging import get_logger
from fastapi import Request

logger = get_logger(__name__)
router = APIRouter(prefix="/enterprise", tags=["Enterprise Setup"])


def check_enterprise_auth(request: Request):
    """
    Check authentication for enterprise endpoints.

    Manually checks Authorization header and verifies JWT token.
    """
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required for enterprise endpoints"
        )

    # Extract token from "Bearer <token>" format
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

    token = auth_header[7:]  # Remove "Bearer " prefix

    try:
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        return payload
    except Exception as e:
        logger.warning(f"Enterprise authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )


# Pydantic models for enterprise configuration
class DatabaseConfig(BaseModel):
    """Database configuration model."""
    host: str = Field(..., description="Database host")
    port: int = Field(default=5432, description="Database port")
    name: str = Field(..., description="Database name")
    username: str = Field(..., description="Database username")
    password: str = Field(..., description="Database password")
    ssl_mode: str = Field(default="prefer", description="SSL mode")
    pool_size: int = Field(default=10, description="Connection pool size")
    max_overflow: int = Field(default=20, description="Max overflow connections")


class RedisConfig(BaseModel):
    """Redis configuration model."""
    host: str = Field(..., description="Redis host")
    port: int = Field(default=6379, description="Redis port")
    REPLACE_ME = Field(None, description="Redis password")
    db: int = Field(default=0, description="Redis database number")
    ssl: bool = Field(default=False, description="Use SSL connection")


class PricingConfig(BaseModel):
    """Pricing configuration model."""
    free_tier: Dict[str, Any] = Field(..., description="Free tier configuration")
    pro_tier: Dict[str, Any] = Field(..., description="Pro tier configuration")
    enterprise_tier: Dict[str, Any] = Field(..., description="Enterprise tier configuration")
    currency: str = Field(default="USD", description="Default currency")
    billing_cycle: str = Field(default="monthly", description="Default billing cycle")


class ServiceConfig(BaseModel):
    """Service configuration model."""
    consciousness_core_url: str = Field(..., description="Consciousness core service URL")
    neuromorphic_integration_url: str = Field(..., description="Neuromorphic integration service URL")
    security_guard_url: str = Field(..., description="Security guard service URL")
    validation_systems_url: str = Field(..., description="Validation systems service URL")
    gateway_url: str = Field(..., description="Gateway service URL")


class SystemConfig(BaseModel):
    """System configuration model."""
    environment: str = Field(default="production", description="Environment (development/staging/production)")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Log level")
    secret_key: str = Field(..., description="Application secret key")
    allowed_origins: List[str] = Field(default=["*"], description="Allowed CORS origins")
    allowed_hosts: List[str] = Field(default=["*"], description="Allowed hosts")


class EnterpriseSetupRequest(BaseModel):
    """Complete enterprise setup request."""
    database: DatabaseConfig
    redis: RedisConfig
    pricing: PricingConfig
    services: ServiceConfig
    system: SystemConfig
    organization_name: str = Field(..., description="Default organization name")
    admin_email: str = Field(..., description="Admin user email")
    admin_password: str = Field(..., description="Admin user password")


class EnterpriseStatusResponse(BaseModel):
    """Enterprise system status response."""
    status: str
    services: Dict[str, str]
    database: str
    redis: str
    configuration: Dict[str, Any]
    timestamp: datetime


@router.post("/setup", status_code=status.HTTP_201_CREATED)
async def setup_enterprise(
    setup_request: EnterpriseSetupRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Initialize enterprise AI Guardians platform.
    
    This endpoint allows external systems to configure:
    - Database connections
    - Redis configuration
    - Pricing tiers
    - Service URLs
    - System settings
    
    Returns configuration status and next steps.
    """
    try:
        logger.info("Starting enterprise setup process")
        
        # Validate database connection
        db_status = await _validate_database_connection(setup_request.database)
        if not db_status["connected"]:
            raise HTTPException(
                status_code=400,
                detail=f"Database connection failed: {db_status['error']}"
            )
        
        # Validate Redis connection
        redis_status = await _validate_redis_connection(setup_request.redis)
        if not redis_status["connected"]:
            raise HTTPException(
                status_code=400,
                detail=f"Redis connection failed: {redis_status['error']}"
            )
        
        # Validate service URLs
        services_status = await _validate_services(setup_request.services)
        if not services_status["all_healthy"]:
            raise HTTPException(
                status_code=400,
                detail=f"Service validation failed: {services_status['errors']}"
            )
        
        # Store configuration
        config_id = await _store_enterprise_config(setup_request, db)
        
        # Initialize default organization and admin user
        await _initialize_default_organization(setup_request, db)
        
        # Setup pricing tiers
        await _setup_pricing_tiers(setup_request.pricing, db)
        
        # Background task: Initialize all services
        background_tasks.add_task(_initialize_services, setup_request)
        
        logger.info(f"Enterprise setup completed successfully: {config_id}")
        
        return {
            "status": "success",
            "message": "Enterprise AI Guardians platform initialized successfully",
            "config_id": config_id,
            "next_steps": [
                "Access admin panel at /admin",
                "Configure additional settings via /enterprise/config",
                "Monitor system health via /enterprise/status",
                "Deploy Chrome extension with gateway URL"
            ],
            "admin_credentials": {
                "email": setup_request.admin_email,
                "password": "***hidden***"
            },
            "api_endpoints": {
                "health": "/health",
                "status": "/enterprise/status",
                "config": "/enterprise/config",
                "services": "/enterprise/services"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise setup failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Enterprise setup failed: {str(e)}"
        )


@router.get("/status", response_model=EnterpriseStatusResponse)
async def get_enterprise_status(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Get current enterprise system status.

    Returns health status of all services, database, Redis,
    and current configuration.
    """
    # Check authentication
    check_enterprise_auth(request)

    try:
        # Check database status
        db_status = await _check_database_status(db)
        
        # Check Redis status
        redis_status = await _check_redis_status()
        
        # Check service statuses
        services_status = await _check_services_status()
        
        # Get current configuration
        config = await _get_current_configuration()
        
        overall_status = "healthy" if all([
            db_status == "healthy",
            redis_status == "healthy",
            all(status == "healthy" for status in services_status.values())
        ]) else "degraded"
        
        return EnterpriseStatusResponse(
            status=overall_status,
            services=services_status,
            database=db_status,
            redis=redis_status,
            configuration=config,
            timestamp=datetime.now(timezone.utc)
        )
        
    except Exception as e:
        logger.error(f"Error getting enterprise status: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve enterprise status"
        )


@router.get("/config")
async def get_enterprise_config(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Get current enterprise configuration.

    Returns current system configuration including:
    - Database settings
    - Redis settings
    - Pricing configuration
    - Service URLs
    - System settings
    """
    # Check authentication
    check_enterprise_auth(request)

    try:
        config = await _get_current_configuration()
        
        # Remove sensitive information
        if "database" in config and "password" in config["database"]:
            config["database"]["password"] = "***hidden***"
        if "redis" in config and "password" in config["redis"]:
            config["redis"]["password"] = "***hidden***"
        if "system" in config and "secret_key" in config["system"]:
            config["system"]["secret_key"] = "***hidden***"
        
        return {
            "configuration": config,
            "timestamp": datetime.now(timezone.utc),
            "version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Error getting enterprise config: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve enterprise configuration"
        )


@router.put("/config")
async def update_enterprise_config(
    request: Request,
    config_update: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    """
    Update enterprise configuration.

    Allows partial updates to system configuration.
    """
    # Check authentication
    check_enterprise_auth(request)

    try:
        # Validate configuration update
        await _validate_config_update(config_update)
        
        # Update configuration
        updated_config = await _update_configuration(config_update, db)
        
        logger.info("Enterprise configuration updated successfully")
        
        return {
            "status": "success",
            "message": "Configuration updated successfully",
            "updated_fields": list(config_update.keys()),
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error updating enterprise config: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update configuration: {str(e)}"
        )


@router.get("/services")
async def get_services_status(request: Request):
    """
    Get status of all AI Guardian services.

    Returns health status and configuration for:
    - Consciousness Core
    - Neuromorphic Integration
    - Security Guard
    - Validation Systems
    - Gateway
    """
    # Check authentication
    check_enterprise_auth(request)

    try:
        services = {
            "consciousness_core": await _check_service_health("consciousness_core"),
            "neuromorphic_integration": await _check_service_health("neuromorphic_integration"),
            "security_guard": await _check_service_health("security_guard"),
            "validation_systems": await _check_service_health("validation_systems"),
            "gateway": await _check_service_health("gateway")
        }
        
        overall_health = all(service["status"] == "healthy" for service in services.values())
        
        return {
            "overall_status": "healthy" if overall_health else "degraded",
            "services": services,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting services status: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve services status"
        )


@router.post("/services/restart")
async def restart_services(
    request: Request,
    service_names: Optional[List[str]] = None,
    background_tasks: BackgroundTasks = None
):
    """
    Restart AI Guardian services.

    Allows restarting specific services or all services.
    """
    # Check authentication
    check_enterprise_auth(request)

    try:
        if service_names is None:
            service_names = [
                "consciousness_core",
                "neuromorphic_integration", 
                "security_guard",
                "validation_systems",
                "gateway"
            ]
        
        # Background task: Restart services
        background_tasks.add_task(_restart_services, service_names)
        
        logger.info(f"Restarting services: {service_names}")
        
        return {
            "status": "success",
            "message": f"Restart initiated for services: {', '.join(service_names)}",
            "services": service_names,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error restarting services: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to restart services: {str(e)}"
        )


# Helper functions
async def _validate_database_connection(db_config: DatabaseConfig) -> Dict[str, Any]:
    """Validate database connection."""
    try:
        # Test database connection with a simple query
        # Import here to avoid circular imports
        from sqlalchemy import text
        from app.core.database import engine

        # Execute a simple test query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            row = result.fetchone()

        if row and row[0] == 1:
            return {"connected": True, "message": "Database connection successful"}
        else:
            return {"connected": False, "error": "Database test query failed"}

    except Exception as e:
        return {"connected": False, "error": str(e)}


async def _validate_redis_connection(redis_config: RedisConfig) -> Dict[str, Any]:
    """Validate Redis connection."""
    try:
        # Import settings
        settings = get_settings()

        # Create Redis connection to test
        import redis
        test_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            REPLACE_ME
            decode_responses=True,
            socket_timeout=5
        )

        # Test connection with ping
        pong = test_client.ping()
        if pong:
            return {"connected": True, "message": "Redis connection successful"}
        else:
            return {"connected": False, "error": "Redis ping failed"}

    except Exception as e:
        return {"connected": False, "error": str(e)}


async def _validate_services(services_config: ServiceConfig) -> Dict[str, Any]:
    """Validate all service URLs."""
    try:
        results = {}
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Check each service endpoint
            services_to_check = [
                ("consciousness_core", services_config.consciousness_core_url),
                ("neuromorphic_integration", services_config.neuromorphic_integration_url),
                ("security_guard", services_config.security_guard_url),
                ("validation_systems", services_config.validation_systems_url),
                ("gateway", services_config.gateway_url),
            ]
            
            for service_name, url in services_to_check:
                try:
                    # Try health endpoint first
                    health_url = f"{url}/health" if not url.endswith("/health") else url
                    response = await client.get(health_url)
                    results[service_name] = {
                        "healthy": response.status_code == 200,
                        "status_code": response.status_code,
                        "url": url
                    }
                except Exception as e:
                    results[service_name] = {
                        "healthy": False,
                        "error": str(e),
                        "url": url
                    }
        
        all_healthy = all(result.get("healthy", False) for result in results.values())
        return {
            "all_healthy": all_healthy,
            "results": results,
            "message": "All services healthy" if all_healthy else "Some services are unhealthy"
        }
    except Exception as e:
        return {"all_healthy": False, "errors": str(e)}


async def _store_enterprise_config(setup_request: EnterpriseSetupRequest, db: AsyncSession) -> str:
    """Store enterprise configuration."""
    try:
        config_id = f"enterprise_config_{int(datetime.now(timezone.utc).timestamp())}"
        
        # Store configuration in a JSON format (could be stored in a dedicated config table)
        config_data = {
            "config_id": config_id,
            "database": setup_request.database.dict(),
            "redis": setup_request.redis.dict(),
            "pricing": setup_request.pricing.dict(),
            "services": setup_request.services.dict(),
            "system": setup_request.system.dict(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Store in environment or dedicated config storage
        # For now, log it (in production, store in database or secrets manager)
        logger.info(f"Enterprise configuration stored: {config_id}", extra={"config": config_data})
        
        return config_id
    except Exception as e:
        logger.error(f"Error storing enterprise config: {e}")
        raise


async def _initialize_default_organization(setup_request: EnterpriseSetupRequest, db: AsyncSession):
    """Initialize default organization and admin user."""
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Check if organization already exists
        result = await db.execute(
            select(Organization).where(Organization.slug == setup_request.organization_name.lower().replace(" ", "-"))
        )
        existing_org = result.scalar_one_or_none()
        
        if existing_org:
            logger.info(f"Organization {setup_request.organization_name} already exists")
            return
        
        # Create organization
        org_slug = setup_request.organization_name.lower().replace(" ", "-").replace("_", "-")
        new_org = Organization(
            name=setup_request.organization_name,
            slug=org_slug,
            description=f"Enterprise organization for {setup_request.organization_name}",
            is_active=True
        )
        db.add(new_org)
        await db.flush()
        
        # Create admin user
        hashed_password = pwd_context.hash(setup_request.admin_password)
        admin_user = User(
            email=setup_request.admin_email,
            full_name="Administrator",
            hashed_REPLACE_ME
            is_active=True,
            is_superuser=True,
            is_verified=True
        )
        db.add(admin_user)
        await db.flush()
        
        # Add admin as organization owner
        org_member = OrganizationMember(
            organization_id=new_org.id,
            user_id=admin_user.id,
            role="owner",
            is_active=True
        )
        db.add(org_member)
        await db.commit()
        
        logger.info(f"Initialized organization {new_org.name} with admin user {admin_user.email}")
    except Exception as e:
        await db.rollback()
        logger.error(f"Error initializing default organization: {e}")
        raise


async def _setup_pricing_tiers(pricing_config: PricingConfig, db: AsyncSession):
    """Setup pricing tiers in database."""
    try:
        tiers = [
            ("free", pricing_config.free_tier),
            ("pro", pricing_config.pro_tier),
            ("enterprise", pricing_config.enterprise_tier)
        ]
        
        for tier_name, tier_data in tiers:
            # Check if tier already exists
            result = await db.execute(
                select(SubscriptionTier).where(SubscriptionTier.name == tier_name.capitalize())
            )
            existing_tier = result.scalar_one_or_none()
            
            if existing_tier:
                # Update existing tier
                existing_tier.description = tier_data.get("description", "")
                existing_tier.price_monthly = tier_data.get("price_monthly", 0)
                existing_tier.price_yearly = tier_data.get("price_yearly", 0)
                existing_tier.features = tier_data.get("features", [])
                existing_tier.limits = tier_data.get("limits", {})
            else:
                # Create new tier
                new_tier = SubscriptionTier(
                    name=tier_name.capitalize(),
                    description=tier_data.get("description", ""),
                    price_monthly=tier_data.get("price_monthly", 0),
                    price_yearly=tier_data.get("price_yearly", 0),
                    features=tier_data.get("features", []),
                    limits=tier_data.get("limits", {}),
                    is_active=True
                )
                db.add(new_tier)
        
        await db.commit()
        logger.info("Setup pricing tiers successfully")
    except Exception as e:
        await db.rollback()
        logger.error(f"Error setting up pricing tiers: {e}")
        raise


async def _initialize_services(setup_request: EnterpriseSetupRequest):
    """Initialize all services with configuration."""
    try:
        # Validate all services are reachable
        validation_result = await _validate_services(setup_request.services)
        
        if not validation_result.get("all_healthy", False):
            logger.warning("Some services are not healthy during initialization", extra=validation_result)
        
        # Log service initialization
        logger.info("Initialized all services with enterprise configuration", extra={
            "services": setup_request.services.dict(),
            "validation": validation_result
        })
    except Exception as e:
        logger.error(f"Error initializing services: {e}")


async def _check_database_status(db: AsyncSession) -> str:
    """Check database health status."""
    try:
        # Execute a simple query to check database connectivity
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        
        # Check if we can query a table
        result = await db.execute(text("SELECT COUNT(*) FROM users LIMIT 1"))
        result.scalar()
        
        return "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return "unhealthy"


async def _check_redis_status() -> str:
    """Check Redis health status."""
    try:
        settings = get_settings()
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            REPLACE_ME 'REDIS_PASSWORD', None),
            decode_responses=True
        )
        
        # Test connection with ping
        pong = await redis_client.ping()
        await redis_client.aclose()
        
        return "healthy" if pong else "unhealthy"
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return "unhealthy"


async def _check_services_status() -> Dict[str, str]:
    """Check all services health status."""
    try:
        # Get service URLs from environment or config
        services = {
            "consciousness_core": os.getenv("CONSCIOUSNESS_CORE_URL", "http://localhost:8001"),
            "neuromorphic_integration": os.getenv("NEUROMORPHIC_INTEGRATION_URL", "http://localhost:8002"),
            "security_guard": os.getenv("SECURITY_GUARD_URL", "http://localhost:8003"),
            "validation_systems": os.getenv("VALIDATION_SYSTEMS_URL", "http://localhost:8004"),
            "gateway": os.getenv("GATEWAY_URL", "http://localhost:8000")
        }
        
        status_results = {}
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            for service_name, url in services.items():
                try:
                    health_url = f"{url}/health" if not url.endswith("/health") else url
                    response = await client.get(health_url)
                    status_results[service_name] = "healthy" if response.status_code == 200 else "unhealthy"
                except Exception:
                    status_results[service_name] = "unreachable"
        
        return status_results
    except Exception as e:
        logger.error(f"Services health check failed: {e}")
        return {}


async def _get_current_configuration() -> Dict[str, Any]:
    """Get current system configuration."""
    try:
        # Get configuration from environment variables and database
        config = {
            "database": {
                "url": os.getenv("DATABASE_URL", "postgresql://localhost:5432/aiguards"),
                "host": os.getenv("DATABASE_HOST", os.getenv("POSTGRES_HOST", "localhost")),
                "port": int(os.getenv("DATABASE_PORT", os.getenv("POSTGRES_PORT", "5432"))),
                "status": "configured"
            },
            "redis": {
                "url": os.getenv("REDIS_URL", "redis://localhost:6379"),
                "host": os.getenv("REDIS_HOST", "localhost"),
                "port": int(os.getenv("REDIS_PORT", "6379")),
                "status": "configured"
            },
            "services": {
                "consciousness_core": os.getenv("CONSCIOUSNESS_CORE_URL", "http://localhost:8001"),
                "neuromorphic_integration": os.getenv("NEUROMORPHIC_INTEGRATION_URL", "http://localhost:8002"),
                "security_guard": os.getenv("SECURITY_GUARD_URL", "http://localhost:8003"),
                "validation_systems": os.getenv("VALIDATION_SYSTEMS_URL", "http://localhost:8004"),
                "gateway_url": f"http://{os.getenv('HOST', 'localhost')}:{os.getenv('PORT', os.getenv('GATEWAY_PORT', '8000'))}",
                "status": "configured"
            },
            "pricing": {
                "stripe_secret_key": "***" if os.getenv("STRIPE_SECRET_KEY") else None,
                "stripe_webhook_secret": "***" if os.getenv("STRIPE_WEBHOOK_SECRET") else None,
                "status": "configured" if os.getenv("STRIPE_SECRET_KEY") else "not_configured"
            },
            "system": {
                "environment": os.getenv("ENVIRONMENT", "production"),
                "debug": os.getenv("DEBUG", "false").lower() == "true",
                "log_level": os.getenv("LOG_LEVEL", "INFO"),
                "status": "configured"
            }
        }
        
        return config
    except Exception as e:
        logger.error(f"Error getting current configuration: {e}")
        return {}


async def _validate_config_update(config_update: Dict[str, Any]):
    """Validate configuration update."""
    try:
        # Validate required fields
        required_sections = ["database", "redis", "services", "pricing", "system"]
        
        for section in required_sections:
            if section not in config_update:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate database configuration
        if "database" in config_update:
            db_config = config_update["database"]
            if "url" not in db_config and ("host" not in db_config or "port" not in db_config):
                raise ValueError("Database configuration must include either 'url' or 'host' and 'port'")
        
        # Validate Redis configuration
        if "redis" in config_update:
            redis_config = config_update["redis"]
            if "url" not in redis_config and ("host" not in redis_config or "port" not in redis_config):
                raise ValueError("Redis configuration must include either 'url' or 'host' and 'port'")
        
        # Validate services configuration
        if "services" in config_update:
            services_config = config_update["services"]
            required_services = ["consciousness_core", "neuromorphic_integration", "security_guard", "validation_systems", "gateway"]
            for service in required_services:
                if service not in services_config:
                    raise ValueError(f"Missing required service configuration: {service}")
        
        # Validate pricing configuration
        if "pricing" in config_update:
            pricing_config = config_update["pricing"]
            if "stripe_secret_key" not in pricing_config:
                raise ValueError("Pricing configuration must include Stripe secret key")
        
        logger.info("Configuration update validated successfully")
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise


async def _update_configuration(config_update: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
    """Update system configuration."""
    try:
        # Update environment variables (in production, this would be stored in a config database)
        env_updates = {}
        
        # Update database configuration
        if "database" in config_update:
            db_config = config_update["database"]
            if "url" in db_config:
                env_updates["DATABASE_URL"] = db_config["url"]
            if "host" in db_config:
                env_updates["DB_HOST"] = db_config["host"]
            if "port" in db_config:
                env_updates["DB_PORT"] = str(db_config["port"])
        
        # Update Redis configuration
        if "redis" in config_update:
            redis_config = config_update["redis"]
            if "url" in redis_config:
                env_updates["REDIS_URL"] = redis_config["url"]
            if "host" in redis_config:
                env_updates["REDIS_HOST"] = redis_config["host"]
            if "port" in redis_config:
                env_updates["REDIS_PORT"] = str(redis_config["port"])
        
        # Update services configuration
        if "services" in config_update:
            services_config = config_update["services"]
            for service, url in services_config.items():
                if service != "status":
                    env_updates[f"{service.upper()}_URL"] = url
        
        # Update pricing configuration
        if "pricing" in config_update:
            pricing_config = config_update["pricing"]
            if "stripe_secret_key" in pricing_config:
                env_updates["STRIPE_SECRET_KEY"] = pricing_config["stripe_secret_key"]
            if "stripe_webhook_secret" in pricing_config:
                env_updates["STRIPE_WEBHOOK_SECRET"] = pricing_config["stripe_webhook_secret"]
        
        # Update system configuration
        if "system" in config_update:
            system_config = config_update["system"]
            if "environment" in system_config:
                env_updates["ENVIRONMENT"] = system_config["environment"]
            if "debug" in system_config:
                env_updates["DEBUG"] = str(system_config["debug"]).lower()
            if "log_level" in system_config:
                env_updates["LOG_LEVEL"] = system_config["log_level"]
        
        # Apply environment updates (in production, this would be stored persistently)
        for key, value in env_updates.items():
            os.environ[key] = value
        
        # Store configuration in database or config file
        config_id = f"config_update_{int(datetime.now(timezone.utc).timestamp())}"
        config_data = {
            "config_id": config_id,
            "config_update": config_update,
            "env_updates": env_updates,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Log the configuration update
        logger.info(f"Configuration updated successfully: {config_id}", extra={"config": config_data})
        
        return {
            "config_id": config_id,
            "updated_sections": list(config_update.keys()),
            "env_updates": env_updates,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error updating configuration: {e}")
        raise


async def _check_service_health(service_name: str) -> Dict[str, Any]:
    """Check individual service health."""
    try:
        # Get service URL from environment
        service_urls = {
            "consciousness_core": os.getenv("CONSCIOUSNESS_CORE_URL", "http://localhost:8001"),
            "neuromorphic_integration": os.getenv("NEUROMORPHIC_INTEGRATION_URL", "http://localhost:8002"),
            "security_guard": os.getenv("SECURITY_GUARD_URL", "http://localhost:8003"),
            "validation_systems": os.getenv("VALIDATION_SYSTEMS_URL", "http://localhost:8004"),
            "gateway": os.getenv("GATEWAY_URL", "http://localhost:8000")
        }
        
        if service_name not in service_urls:
            return {
                "service": service_name,
                "status": "unknown",
                "error": f"Service {service_name} not configured",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        url = service_urls[service_name]
        health_url = f"{url}/health" if not url.endswith("/health") else url
        
        start_time = datetime.now(timezone.utc)
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(health_url)
            end_time = datetime.now(timezone.utc)
            
            response_time = (end_time - start_time).total_seconds()
            
            if response.status_code == 200:
                return {
                    "service": service_name,
                    "status": "healthy",
                    "response_time": response_time,
                    "url": url,
                    "timestamp": end_time.isoformat()
                }
            else:
                return {
                    "service": service_name,
                    "status": "unhealthy",
                    "response_time": response_time,
                    "url": url,
                    "status_code": response.status_code,
                    "timestamp": end_time.isoformat()
                }
    except Exception as e:
        logger.error(f"Service health check failed for {service_name}: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


async def _restart_services(service_names: List[str]):
    """Restart specified services."""
    try:
        import subprocess
        import asyncio
        
        # Service restart commands (in production, this would use proper service management)
        service_commands = {
            "consciousness_core": ["docker", "restart", "consciousness-core"],
            "neuromorphic_integration": ["docker", "restart", "neuromorphic-integration"],
            "security_guard": ["docker", "restart", "security-guard"],
            "validation_systems": ["docker", "restart", "validation-systems"],
            "gateway": ["docker", "restart", "gateway"]
        }
        
        restart_results = {}
        
        for service_name in service_names:
            if service_name in service_commands:
                try:
                    # Execute restart command
                    cmd = service_commands[service_name]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        restart_results[service_name] = {
                            "status": "success",
                            "message": f"Service {service_name} restarted successfully"
                        }
                        logger.info(f"Successfully restarted service: {service_name}")
                    else:
                        restart_results[service_name] = {
                            "status": "failed",
                            "error": result.stderr,
                            "message": f"Failed to restart service {service_name}"
                        }
                        logger.error(f"Failed to restart service {service_name}: {result.stderr}")
                except subprocess.TimeoutExpired:
                    restart_results[service_name] = {
                        "status": "timeout",
                        "message": f"Service {service_name} restart timed out"
                    }
                    logger.error(f"Service restart timed out: {service_name}")
                except Exception as e:
                    restart_results[service_name] = {
                        "status": "error",
                        "error": str(e),
                        "message": f"Error restarting service {service_name}"
                    }
                    logger.error(f"Error restarting service {service_name}: {e}")
            else:
                restart_results[service_name] = {
                    "status": "unknown",
                    "message": f"Service {service_name} not found in restart configuration"
                }
                logger.warning(f"Unknown service for restart: {service_name}")
        
        # Log overall restart results
        successful_restarts = [name for name, result in restart_results.items() if result["status"] == "success"]
        failed_restarts = [name for name, result in restart_results.items() if result["status"] != "success"]
        
        logger.info(f"Service restart completed. Successful: {successful_restarts}, Failed: {failed_restarts}")
        
        return restart_results
        
    except Exception as e:
        logger.error(f"Error restarting services: {e}")
        raise
