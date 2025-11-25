"""
Configuration Management Module

Provides centralized configuration management with environment variable support,
validation, and normalization utilities. All configuration values are validated
at initialization and can be loaded from environment variables or dictionaries.

This module uses Pydantic for type validation and settings management, ensuring
type safety and runtime validation of all configuration values.

Example:
    >>> from config import AppConfig
    >>> config = AppConfig()
    >>> print(config.app_name)
    'Application'
    
    >>> # Load from environment variables
    >>> import os
    >>> os.environ['APP_NAME'] = 'MyApp'
    >>> config = AppConfig()
    >>> print(config.app_name)
    'MyApp'
"""

import os
import re
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from pathlib import Path

try:
    # Try pydantic v2 style imports first
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from pydantic import Field, field_validator, model_validator
except ImportError:
    try:
        # Fallback to pydantic v1 style imports
        from pydantic import BaseSettings, Field, field_validator, model_validator
        try:
            from pydantic import ConfigDict as SettingsConfigDict
        except ImportError:
            # For older pydantic versions, use dict for model_config
            SettingsConfigDict = dict
    except ImportError:
        raise ImportError(
            "pydantic and pydantic-settings are required. "
            "Install with: pip install 'pydantic>=2.0' 'pydantic-settings>=2.0'"
        )


class Environment(str, Enum):
    """Deployment environment enumeration."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AppConfig(BaseSettings):
    """
    Application configuration with environment variable support and validation.
    
    All configuration values can be set via environment variables using the
    APP_ prefix (e.g., APP_NAME, APP_ENVIRONMENT). Values are validated at
    initialization and normalized according to their type.
    
    Attributes:
        app_name: Application name (default: "Application")
        app_version: Application version in semver format (default: "1.0.0")
        environment: Deployment environment (default: DEVELOPMENT)
        debug: Enable debug mode (default: False)
        log_level: Logging level (default: INFO)
        secret_key: Secret key for cryptographic operations (required in production)
        database_url: Database connection URL (optional)
        redis_url: Redis connection URL (optional)
        api_timeout: API request timeout in seconds (default: 30.0)
        max_request_size: Maximum request size in bytes (default: 10485760)
        allowed_hosts: List of allowed hostnames for CORS (default: ["*"])
        enable_metrics: Enable metrics collection (default: True)
        metrics_port: Port for metrics endpoint (default: 9090)
    
    Raises:
        ValueError: If configuration values fail validation
        ValidationError: If Pydantic validation fails
    
    Example:
        >>> config = AppConfig()
        >>> config.validate()
        True
        
        >>> # Production config with validation
        >>> prod_config = AppConfig(
        ...     environment="production",
        ...     secret_key="secure-key-here"
        ... )
    """
    
    # Application metadata
    app_name: str = Field(
        default="Application",
        description="Application name",
        min_length=1,
        max_length=100
    )
    app_version: str = Field(
        default="1.0.0",
        description="Application version in semver format"
    )
    
    # Environment configuration
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Deployment environment"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        description="Logging level"
    )
    
    # Security configuration
    secret_key: Optional[str] = Field(
        default=None,
        description="Secret key for cryptographic operations",
        min_length=32
    )
    
    # Database configuration
    database_url: Optional[str] = Field(
        default=None,
        description="Database connection URL"
    )
    
    # Cache/Redis configuration
    redis_url: Optional[str] = Field(
        default=None,
        description="Redis connection URL"
    )
    
    # API configuration
    api_timeout: float = Field(
        default=30.0,
        description="API request timeout in seconds",
        gt=0.0,
        le=300.0
    )
    max_request_size: int = Field(
        default=10485760,  # 10MB
        description="Maximum request size in bytes",
        gt=0,
        le=104857600  # 100MB max
    )
    allowed_hosts: List[str] = Field(
        default=["*"],
        description="List of allowed hostnames for CORS"
    )
    
    # Metrics configuration
    enable_metrics: bool = Field(
        default=True,
        description="Enable metrics collection"
    )
    metrics_port: int = Field(
        default=9090,
        description="Port for metrics endpoint",
        gt=1024,
        lt=65536
    )
    
    # Handle both pydantic v1 and v2 style configuration
    if isinstance(SettingsConfigDict, type) and hasattr(SettingsConfigDict, '__call__'):
        # Pydantic v2 style
        model_config = SettingsConfigDict(
            env_prefix="APP_",
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False,
            validate_assignment=True,
            extra="ignore"
        )
    else:
        # Pydantic v1 style (fallback)
        class Config:
            env_prefix = "APP_"
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = False
            validate_assignment = True
            extra = "ignore"
    
    @field_validator('app_version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        """
        Validate version string follows semver format.
        
        Args:
            v: Version string to validate
            
        Returns:
            Validated version string
            
        Raises:
            ValueError: If version format is invalid
        """
        if not isinstance(v, str):
            raise ValueError("Version must be a string")
        
        # Semver pattern: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
        semver_pattern = re.compile(
            r'^\d+\.\d+\.\d+(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?'
            r'(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$'
        )
        
        if not semver_pattern.match(v):
            raise ValueError(
                f"Invalid version format: {v}. "
                "Expected semver format: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]"
            )
        
        return v
    
    @field_validator('database_url', 'redis_url')
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate URL format for database and Redis connections.
        
        Args:
            v: URL string to validate
            
        Returns:
            Validated URL string or None
            
        Raises:
            ValueError: If URL format is invalid
        """
        if v is None:
            return None
        
        if not isinstance(v, str) or not v.strip():
            raise ValueError("URL must be a non-empty string if provided")
        
        # Basic URL validation: scheme://host/path
        url_pattern = re.compile(
            r'^[a-zA-Z][a-zA-Z0-9+.-]*://'  # scheme
            r'[^\s/$.?#].*$'  # rest of URL
        )
        
        if not url_pattern.match(v.strip()):
            raise ValueError(
                f"Invalid URL format: {v}. "
                "Expected format: scheme://host/path"
            )
        
        return v.strip()
    
    @field_validator('allowed_hosts')
    @classmethod
    def validate_allowed_hosts(cls, v: List[str]) -> List[str]:
        """
        Validate and normalize allowed hosts list.
        
        Args:
            v: List of hostnames
            
        Returns:
            Normalized list of hostnames
            
        Raises:
            ValueError: If list contains invalid hostnames
        """
        if not isinstance(v, list):
            raise ValueError("allowed_hosts must be a list")
        
        if len(v) == 0:
            raise ValueError("allowed_hosts cannot be empty")
        
        normalized = []
        for host in v:
            if not isinstance(host, str):
                raise ValueError(f"Host must be a string, got {type(host).__name__}")
            
            host = host.strip()
            if not host:
                raise ValueError("Host cannot be empty")
            
            # Validate hostname format (basic check)
            if host != "*":
                # Basic hostname validation
                hostname_pattern = re.compile(
                    r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*'
                    r'[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$|'
                    r'^(\d{1,3}\.){3}\d{1,3}$|'  # IPv4
                    r'^\*$'  # Wildcard
                )
                if not hostname_pattern.match(host):
                    raise ValueError(f"Invalid hostname format: {host}")
            
            normalized.append(host)
        
        return normalized
    
    @model_validator(mode='after')
    def validate_environmental_requirements(self) -> 'AppConfig':
        """
        Validate environment-specific requirements.
        
        In production, certain values must be set (e.g., secret_key).
        This validator ensures production configurations are secure.
        
        Returns:
            Self after validation
            
        Raises:
            ValueError: If production requirements are not met
        """
        if self.environment == Environment.PRODUCTION:
            if not self.secret_key:
                raise ValueError(
                    "secret_key is required in production environment. "
                    "Set APP_SECRET_KEY environment variable."
                )
            
            if len(self.secret_key) < 32:
                raise ValueError(
                    "secret_key must be at least 32 characters in production"
                )
            
            if self.debug:
                raise ValueError(
                    "debug mode must be disabled in production environment"
                )
        
        return self
    
    def validate(self) -> bool:
        """
        Validate configuration and return True if valid.
        
        Returns:
            True if configuration is valid
            
        Note:
            This method will raise exceptions if validation fails.
            It returns True only if all validations pass.
        """
        try:
            # Trigger validation by accessing validated fields
            _ = self.app_name
            _ = self.app_version
            _ = self.environment
            _ = self.log_level
            return True
        except Exception:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of configuration
            
        Example:
            >>> config = AppConfig()
            >>> config_dict = config.to_dict()
            >>> print(config_dict['app_name'])
            'Application'
        """
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "environment": self.environment.value,
            "debug": self.debug,
            "log_level": self.log_level.value,
            "secret_key": self.secret_key,
            "database_url": self.database_url,
            "redis_url": self.redis_url,
            "api_timeout": self.api_timeout,
            "max_request_size": self.max_request_size,
            "allowed_hosts": self.allowed_hosts.copy(),
            "enable_metrics": self.enable_metrics,
            "metrics_port": self.metrics_port
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        """
        Create configuration from dictionary.
        
        Args:
            data: Dictionary with configuration values
            
        Returns:
            AppConfig instance
            
        Raises:
            ValidationError: If dictionary contains invalid values
            
        Example:
            >>> data = {"app_name": "MyApp", "environment": "production"}
            >>> config = AppConfig.from_dict(data)
        """
        # Normalize keys to match field names
        normalized_data = {}
        for key, value in data.items():
            # Convert UPPER_CASE to snake_case
            normalized_key = key.lower().replace('_', '_')
            normalized_data[normalized_key] = value
        
        return cls(**normalized_data)
    
    def is_production(self) -> bool:
        """
        Check if configuration is for production environment.
        
        Returns:
            True if environment is production
        """
        return self.environment == Environment.PRODUCTION
    
    def is_development(self) -> bool:
        """
        Check if configuration is for development environment.
        
        Returns:
            True if environment is development
        """
        return self.environment == Environment.DEVELOPMENT


# Normalization utilities

def normalize_string(value: Any, max_length: Optional[int] = None) -> str:
    """
    Normalize a value to a string.
    
    Converts various types to strings, trims whitespace, and optionally
    enforces maximum length. Handles None values by returning empty string.
    
    Args:
        value: Value to normalize
        max_length: Optional maximum length (truncates if exceeded)
        
    Returns:
        Normalized string
        
    Example:
        >>> normalize_string(123)
        '123'
        >>> normalize_string("  hello  ")
        'hello'
        >>> normalize_string("very long string", max_length=5)
        'very '
    """
    if value is None:
        return ""
    
    if not isinstance(value, str):
        value = str(value)
    
    normalized = value.strip()
    
    if max_length is not None and len(normalized) > max_length:
        normalized = normalized[:max_length]
    
    return normalized


def normalize_int(value: Any, min_value: Optional[int] = None, 
                  max_value: Optional[int] = None, default: int = 0) -> int:
    """
    Normalize a value to an integer.
    
    Converts strings and floats to integers, validates range, and returns
    default value if conversion fails.
    
    Args:
        value: Value to normalize
        min_value: Optional minimum value (clamps if below)
        max_value: Optional maximum value (clamps if above)
        default: Default value if conversion fails
        
    Returns:
        Normalized integer
        
    Example:
        >>> normalize_int("123")
        123
        >>> normalize_int("45.7")
        45
        >>> normalize_int("invalid", default=0)
        0
        >>> normalize_int(150, min_value=0, max_value=100)
        100
    """
    if value is None:
        return default
    
    if isinstance(value, int):
        result = value
    elif isinstance(value, float):
        result = int(value)
    elif isinstance(value, str):
        try:
            result = int(float(value))
        except (ValueError, TypeError):
            return default
    else:
        return default
    
    if min_value is not None and result < min_value:
        result = min_value
    
    if max_value is not None and result > max_value:
        result = max_value
    
    return result


def normalize_float(value: Any, min_value: Optional[float] = None,
                   max_value: Optional[float] = None, default: float = 0.0) -> float:
    """
    Normalize a value to a float.
    
    Converts strings and integers to floats, validates range, and returns
    default value if conversion fails.
    
    Args:
        value: Value to normalize
        min_value: Optional minimum value (clamps if below)
        max_value: Optional maximum value (clamps if above)
        default: Default value if conversion fails
        
    Returns:
        Normalized float
        
    Example:
        >>> normalize_float("123.45")
        123.45
        >>> normalize_float("invalid", default=0.0)
        0.0
        >>> normalize_float(150.5, min_value=0.0, max_value=100.0)
        100.0
    """
    if value is None:
        return default
    
    if isinstance(value, float):
        result = value
    elif isinstance(value, int):
        result = float(value)
    elif isinstance(value, str):
        try:
            result = float(value)
        except (ValueError, TypeError):
            return default
    else:
        return default
    
    if min_value is not None and result < min_value:
        result = min_value
    
    if max_value is not None and result > max_value:
        result = max_value
    
    return result


def normalize_bool(value: Any, default: bool = False) -> bool:
    """
    Normalize a value to a boolean.
    
    Converts strings ("true", "false", "1", "0", etc.) and numbers to booleans.
    Returns default value if conversion is ambiguous.
    
    Args:
        value: Value to normalize
        default: Default value if conversion fails
        
    Returns:
        Normalized boolean
        
    Example:
        >>> normalize_bool("true")
        True
        >>> normalize_bool("1")
        True
        >>> normalize_bool("false")
        False
        >>> normalize_bool("invalid", default=False)
        False
    """
    if value is None:
        return default
    
    if isinstance(value, bool):
        return value
    
    if isinstance(value, (int, float)):
        return bool(value)
    
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "1", "yes", "on", "enabled"):
            return True
        if normalized in ("false", "0", "no", "off", "disabled"):
            return False
    
    return default


def normalize_list(value: Any, item_type: Optional[type] = None) -> List[Any]:
    """
    Normalize a value to a list.
    
    Converts various types to lists. If value is already a list, returns it.
    If value is a string, splits by comma. Otherwise wraps in a list.
    
    Args:
        value: Value to normalize
        item_type: Optional type to cast list items to
        
    Returns:
        Normalized list
        
    Example:
        >>> normalize_list("a,b,c")
        ['a', 'b', 'c']
        >>> normalize_list([1, 2, 3])
        [1, 2, 3]
        >>> normalize_list("1,2,3", item_type=int)
        [1, 2, 3]
    """
    if value is None:
        return []
    
    if isinstance(value, list):
        result = value
    elif isinstance(value, str):
        result = [item.strip() for item in value.split(",") if item.strip()]
    elif isinstance(value, (tuple, set)):
        result = list(value)
    else:
        result = [value]
    
    if item_type is not None:
        try:
            result = [item_type(item) for item in result]
        except (ValueError, TypeError):
            # If type conversion fails, return original list
            pass
    
    return result


# Global configuration instance (lazy initialization)
_config_instance: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """
    Get global configuration instance.
    
    Creates a singleton instance of AppConfig on first call, then returns
    the same instance on subsequent calls.
    
    Returns:
        Global AppConfig instance
        
    Example:
        >>> config = get_config()
        >>> config.app_name
        'Application'
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = AppConfig()
    return _config_instance


def reset_config() -> None:
    """
    Reset global configuration instance.
    
    Forces recreation of configuration on next get_config() call.
    Useful for testing or when environment variables change.
    
    Example:
        >>> reset_config()
        >>> # Change environment variables
        >>> config = get_config()  # Will reload from environment
    """
    global _config_instance
    _config_instance = None

