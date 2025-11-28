# tokenguard/config.py
"""
Configuration management for TokenGuard microservice.
"""

import logging
from typing import Optional, Any
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, model_validator, ValidationError, ValidationInfo

logger = logging.getLogger(__name__)


class TokenGuardConfig(BaseSettings):
    """Configuration settings for TokenGuard microservice."""

    # Core pruning parameters
    confidence_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum confidence required to keep response (0.0-1.0)",
    )

    max_length: int = Field(
        default=800,
        ge=100,
        le=50000,
        description="Maximum response length before pruning (100-50000)",
    )

    min_length: int = Field(
        default=200,
        ge=50,
        le=5000,
        description="Minimum length threshold for pruning decisions (50-5000)",
    )

    uncertainty_threshold: float = Field(
        default=0.25, ge=0.0, le=1.0, description="Threshold for uncertainty scoring (0.0-1.0)"
    )

    check_interval_tokens: int = Field(
        default=5, ge=1, le=100, description="How often to check confidence in tokens (1-100)"
    )

    trailing_tokens_window: int = Field(
        default=5, ge=1, le=50, description="Number of recent tokens to analyze (1-50)"
    )

    # Server configuration
    host: str = Field(default="0.0.0.0", description="Host address to bind the server")

    port: int = Field(
        default=8000, ge=1024, le=65535, description="Port number for the server (1024-65535)"
    )

    # Logging configuration
    log_level: str = Field(
        default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    log_format: str = Field(default="json", description="Log format (json or text)")

    # Performance settings
    enable_metrics: bool = Field(default=True, description="Enable performance metrics collection")

    rate_limit_requests: int = Field(
        default=10000, ge=1, le=10000, description="Maximum requests per rate limit window (1-10000)"
    )

    rate_limit_window: int = Field(
        default=60, ge=1, le=3600, description="Rate limit window in seconds (1-3600)"
    )

    # Security settings
    api_key: Optional[str] = Field(default=None, description="Primary API key for authentication")

    cors_origins: str = Field(default="*", description="CORS allowed origins (comma-separated)")

    # LLM Client Settings
    llm_api_key: Optional[str] = Field(
        default=None,
        description="API key for the LLM provider (e.g., OpenAI). If not set, it will try the OPENAI_API_KEY environment variable."
    )
    llm_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="Base URL for the LLM provider API"
    )

    # Service Mode Configuration
    service_mode: str = Field(
        default="standard",
        description="Operating mode: 'standard' (original), 'tool_call' (LLM tool calling), 'mcp' (Model Context Protocol)"
    )

    mcp_server_name: str = Field(
        default="TokenGuard",
        description="Name for MCP server when in MCP mode"
    )

    mcp_server_version: str = Field(
        default="1.0.0",
        description="Version for MCP server when in MCP mode"
    )

    @field_validator("min_length")
    @classmethod
    def validate_min_length_relationship(cls: Any, min_length: int, info: ValidationInfo) -> int:
        """Ensure min_length meets minimum requirements."""
        # Field validators in pydantic v2 validate individual fields
        # Cross-field validation (min_length < max_length) should use model_validator
        if min_length < 50:
            raise ValueError(f"min_length must be at least 50, got {min_length}")
        return min_length

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls: Any, log_level: str) -> str:
        """Validate log level is supported."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if log_level.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of: {', '.join(valid_levels)}")
        return log_level.upper()

    @field_validator("log_format")
    @classmethod
    def validate_log_format(cls: Any, log_format: str) -> str:
        """Validate log format is supported."""
        valid_formats = {"json", "text"}
        if log_format.lower() not in valid_formats:
            raise ValueError(f"log_format must be one of: {', '.join(valid_formats)}")
        return log_format.lower()

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls: Any, api_key: Optional[str]) -> Optional[str]:
        """Validate API key format and security."""
        if api_key is not None:
            if len(api_key) < 16:
                raise ValueError("API key must be at least 16 characters long")
            if not api_key.replace("-", "").replace("_", "").isalnum():
                raise ValueError(
                    "API key must contain only alphanumeric characters, hyphens, and underscores"
                )
        return api_key

    @field_validator("service_mode")
    @classmethod
    def validate_service_mode(cls: Any, service_mode: str) -> str:
        """Validate service mode is supported."""
        valid_modes = {"standard", "tool_call", "mcp"}
        if service_mode.lower() not in valid_modes:
            raise ValueError(f"service_mode must be one of: {', '.join(valid_modes)}")
        return service_mode.lower()

    @model_validator(mode="after")
    def validate_length_relationship(self: Any) -> "TokenGuardConfig":
        """Validate that min_length is less than max_length."""
        if self.min_length >= self.max_length:
            raise ValueError(
                f"min_length ({self.min_length}) must be less than max_length ({self.max_length})"
            )
        return self

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "env_prefix": "TOKENGUARD_",
        "extra": "ignore",
    }


def get_config() -> TokenGuardConfig:
    """Get validated configuration instance with error handling."""
    try:
        return TokenGuardConfig()
    except ValidationError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Configuration initialization failed: {e}")
        raise


# Global configuration instance
try:
    config = get_config()
    logger.info("Configuration loaded successfully")
except Exception as e:
    logger.critical(f"Failed to initialize configuration: {e}")
    raise
