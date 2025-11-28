"""
Application configuration management.

This module provides configuration management using Pydantic settings
with environment variable support and validation.
"""

import os
from typing import List, Optional, Union
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "codeguardians-gateway"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "A gold-standard project"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # AWS Secrets Manager Configuration
    AWS_SECRETS_ENABLED: bool = Field(default=True, env="AWS_SECRETS_ENABLED")
    AWS_SECRETS_NAME: str = Field(default="codeguardians-gateway/production", env="AWS_SECRETS_NAME")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    
    # Security
    SECRET_KEY: str = Field(default="change-me-in-production-min-32-chars", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")

    # Clerk Authentication (Optional - for future integration)
    CLERK_SECRET_KEY: Optional[str] = Field(default=None, env="CLERK_SECRET_KEY")
    CLERK_PUBLISHABLE_KEY: Optional[str] = Field(default=None, env="CLERK_PUBLISHABLE_KEY")
    CLERK_WEBHOOK_SECRET: Optional[str] = Field(default=None, env="CLERK_WEBHOOK_SECRET")
    CLERK_ENABLED: bool = Field(default=False, env="CLERK_ENABLED")

    # Stripe Payment (Optional - for future integration)
    STRIPE_SECRET_KEY: Optional[str] = Field(default=None, env="STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY: Optional[str] = Field(default=None, env="STRIPE_PUBLISHABLE_KEY")
    STRIPE_WEBHOOK_SECRET: Optional[str] = Field(default=None, env="STRIPE_WEBHOOK_SECRET")
    STRIPE_ENABLED: bool = Field(default=False, env="STRIPE_ENABLED")

    # Database (Optional - can run without database for stateless API)
    DATABASE_URL: Optional[str] = Field(default=None, env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    DATABASE_POOL_RECYCLE: int = Field(default=3600, env="DATABASE_POOL_RECYCLE")
    DATABASE_ENABLED: bool = Field(default=True, env="DATABASE_ENABLED")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    REDIS_REPLACE_ME = Field(default=None, env="REDIS_PASSWORD")
    
    # CORS - Using Union to allow both string and list from env vars
    ALLOWED_ORIGINS: Union[str, List[str]] = Field(
        default=["http://localhost:3000", "http://localhost:8080", "https://aiguardian.ai"],
        env="ALLOWED_ORIGINS"
    )
    ALLOWED_HOSTS: Union[str, List[str]] = Field(
        default="localhost,127.0.0.1,aiguardian.ai,api.aiguardian.ai,dashboard.aiguardian.ai",
        env="ALLOWED_HOSTS"
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")
    
    # Email
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    SMTP_REPLACE_ME = Field(default=None, env="SMTP_PASSWORD")
    SMTP_TLS: bool = Field(default=True, env="SMTP_TLS")
    
    # S3 File Storage
    S3_ENABLED: bool = Field(default=False, env="S3_ENABLED")
    S3_BUCKET_NAME: Optional[str] = Field(default=None, env="S3_BUCKET_NAME")
    S3_REGION: str = Field(default="us-east-1", env="S3_REGION")
    S3_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="S3_ACCESS_KEY_ID")
    S3_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="S3_SECRET_ACCESS_KEY")
    S3_SESSION_TOKEN: Optional[str] = Field(default=None, env="S3_SESSION_TOKEN")
    S3_ENDPOINT_URL: Optional[str] = Field(default=None, env="S3_ENDPOINT_URL")  # For local testing with MinIO
    
    # File Upload Settings
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_FILE_TYPES: Union[str, List[str]] = Field(
        default="image/jpeg,image/png,image/gif,application/pdf",
        env="ALLOWED_FILE_TYPES"
    )
    UPLOAD_EXPIRY_MINUTES: int = Field(default=60, env="UPLOAD_EXPIRY_MINUTES")  # Presigned URL expiry
    FILE_CLEANUP_DAYS: int = Field(default=30, env="FILE_CLEANUP_DAYS")  # Auto-cleanup after days
    
    # Session Management
    SESSION_TTL: int = Field(default=3600, env="SESSION_TTL")  # Session TTL in seconds (1 hour)
    SESSION_CLEANUP_INTERVAL: int = Field(default=300, env="SESSION_CLEANUP_INTERVAL")  # Cleanup interval in seconds (5 minutes)
    SESSION_STORAGE_TYPE: str = Field(default="redis", env="SESSION_STORAGE_TYPE")  # "redis" or "database"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # seconds
    
    # Endpoint-specific rate limits (for dynamic_rate_limiting middleware)
    RATE_LIMIT_PROCESSING: int = Field(default=100, env="RATE_LIMIT_PROCESSING")  # requests per minute for /process
    RATE_LIMIT_ADMIN: int = Field(default=5, env="RATE_LIMIT_ADMIN")  # requests per minute for admin endpoints
    RATE_LIMIT_READ: int = Field(default=200, env="RATE_LIMIT_READ")  # requests per minute for read endpoints
    
    # Cache
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    CACHE_ENABLED: bool = Field(default=True, env="CACHE_ENABLED")
    
    # Testing
    TESTING: bool = Field(default=False, env="TESTING")
    TEST_DATABASE_URL: Optional[str] = Field(default=None, env="TEST_DATABASE_URL")
    
    # Internal Testing
    INTERNAL_TESTING_ENABLED: bool = Field(default=False, env="INTERNAL_TESTING_ENABLED")
    INTERNAL_TESTING_JWT_TOKEN: Optional[str] = Field(default=None, env="INTERNAL_TESTING_JWT_TOKEN")

    # Internal Access Token for service-to-service communication
    INTERNAL_ACCESS_TOKEN: str = Field(
        default="aiguardian-internal-token-2024",
        env="INTERNAL_ACCESS_TOKEN"
    )

    # BiasGuard Configuration
    BIASGUARD_ENABLED: bool = Field(default=True, env="BIASGUARD_ENABLED")
    BIASGUARD_ENFORCE_FAIRNESS: bool = Field(default=True, env="BIASGUARD_ENFORCE_FAIRNESS")
    BIASGUARD_ENFORCE_COMPLIANCE: bool = Field(default=True, env="BIASGUARD_ENFORCE_COMPLIANCE")
    BIASGUARD_ENFORCE_ATTRIBUTION: bool = Field(default=True, env="BIASGUARD_ENFORCE_ATTRIBUTION")
    BIASGUARD_AUDIT_RETENTION_DAYS: int = Field(default=90, env="BIASGUARD_AUDIT_RETENTION_DAYS")
    BIASGUARD_MAX_AUDIT_RECORDS: int = Field(default=1000000, env="BIASGUARD_MAX_AUDIT_RECORDS")
    BIASGUARD_LOG_LEVEL: str = Field(default="INFO", env="BIASGUARD_LOG_LEVEL")
    
    @field_validator("ALLOWED_ORIGINS", "ALLOWED_HOSTS", "ALLOWED_FILE_TYPES", mode="before")
    @classmethod
    def parse_string_list(cls, v):
        """Parse comma-separated string into list."""
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v
    
    @model_validator(mode="after")
    def validate_cors_origins(self):
        """Validate CORS origins - ensure production doesn't use wildcard."""
        if self.ENVIRONMENT == "production":
            origins = self.ALLOWED_ORIGINS
            if isinstance(origins, str) and origins == "*":
                raise ValueError("CORS wildcard (*) not allowed in production. Use specific origins.")
            if isinstance(origins, list) and "*" in origins:
                raise ValueError("CORS wildcard (*) not allowed in production. Use specific origins.")
        return self

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v):
        """Validate environment setting."""
        allowed_envs = ["development", "staging", "production", "test"]
        if v not in allowed_envs:
            raise ValueError(f"ENVIRONMENT must be one of: {allowed_envs}")
        return v
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level setting."""
        if v is None:
            return "INFO"  # Default log level
        if not isinstance(v, str):
            v = str(v)
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"LOG_LEVEL must be one of: {allowed_levels}")
        return v.upper()
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v):
        """Validate secret key strength."""
        if v and len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @field_validator("S3_BUCKET_NAME")
    @classmethod
    def validate_s3_bucket_name(cls, v, info):
        """Validate S3 bucket name if S3 is enabled."""
        if info.data.get('S3_ENABLED', False) and not v:
            raise ValueError("S3_BUCKET_NAME is required when S3_ENABLED is True")
        return v
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.ENVIRONMENT == "test" or self.TESTING
    
    @property
    def database_url(self) -> Optional[str]:
        """Get database URL for current environment."""
        if self.is_testing and self.TEST_DATABASE_URL:
            return self.TEST_DATABASE_URL
        return self.DATABASE_URL

    @property
    def is_clerk_enabled(self) -> bool:
        """Check if Clerk authentication is enabled."""
        return self.CLERK_ENABLED and self.CLERK_SECRET_KEY is not None

    @property
    def is_stripe_enabled(self) -> bool:
        """Check if Stripe payments are enabled."""
        return self.STRIPE_ENABLED and self.STRIPE_SECRET_KEY is not None
    
    @property
    def is_biasguard_enabled(self) -> bool:
        """Check if BiasGuard is enabled."""
        return self.BIASGUARD_ENABLED
    
    @property
    def is_internal_testing_enabled(self) -> bool:
        """Check if internal testing is enabled."""
        return self.INTERNAL_TESTING_ENABLED and self.INTERNAL_TESTING_JWT_TOKEN is not None
    
    @property
    def is_s3_enabled(self) -> bool:
        """Check if S3 file storage is enabled and properly configured."""
        return (
            self.S3_ENABLED and 
            self.S3_BUCKET_NAME is not None and 
            self.S3_REGION is not None
        )
    
    def _load_aws_secrets(self) -> None:
        """Load secrets from AWS Secrets Manager if enabled."""
        # Check if AWS secrets are enabled via environment variable
        aws_secrets_enabled = os.getenv('AWS_SECRETS_ENABLED', 'true').lower() == 'true'
        if not aws_secrets_enabled:
            return
        
        try:
            # Import AWS secrets module dynamically to avoid circular imports
            from app.core.aws_secrets import (
                initialize_aws_secrets, 
                validate_aws_secrets_available,
                get_aws_secrets_for_environment
            )
            
            # Get AWS configuration from environment
            aws_region = os.getenv('AWS_REGION', 'us-east-1')
            aws_secrets_name = os.getenv('AWS_SECRETS_NAME', 'codeguardians-gateway/production')
            
            # Initialize AWS Secrets Manager
            aws_secrets_manager = initialize_aws_secrets(
                region=aws_region,
                secret_name=aws_secrets_name
            )
            
            # Check if AWS Secrets Manager is available
            if not validate_aws_secrets_available():
                logger.warning("AWS Secrets Manager not available, using environment variables")
                return
            
            # Get secrets from AWS
            aws_secrets = get_aws_secrets_for_environment(
                region=aws_region,
                secret_name=aws_secrets_name
            )
            
            if not aws_secrets:
                logger.warning("No secrets retrieved from AWS Secrets Manager")
                return
            
            # Override environment variables with AWS secrets
            for key, value in aws_secrets.items():
                if value:  # Only override if value is not empty
                    os.environ[key] = value
                    logger.debug(f"Loaded secret from AWS: {key}")
            
            logger.info(f"Successfully loaded {len(aws_secrets)} secrets from AWS Secrets Manager")
            
        except Exception as e:
            logger.error(f"Failed to load AWS secrets: {e}")
            logger.warning("Falling back to environment variables")
    
    def __init__(self, **kwargs):
        """Initialize settings with AWS secrets integration."""
        # Load AWS secrets before initializing settings
        self._load_aws_secrets()
        super().__init__(**kwargs)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_parse_none_str="",
        env_ignore_empty=True,
        extra="ignore"  # Ignore extra environment variables
    )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment."""
    global _settings
    _settings = Settings()
    return _settings
