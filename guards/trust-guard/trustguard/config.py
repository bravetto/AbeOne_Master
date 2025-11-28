"""
Trust Guard Configuration

Environment-based configuration for Trust Guard service with secrets management
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)


class TrustGuardConfig(BaseSettings):
    """
    Configuration settings for Trust Guard AI reliability service.
    """

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    # Service settings
    service_mode: str = "standard"  # standard, mcp, tool_call
    log_level: str = "INFO"
    enable_metrics: bool = True
    rate_limit: int = 100  # requests per minute

    # CORS settings
    cors_origins: Optional[str] = "*"

    # API settings
    api_key: Optional[str] = None

    # Security settings
    secret_key: Optional[str] = None
    jwt_secret: Optional[str] = None
    encryption_key: Optional[str] = None
    
    # Secrets rotation settings
    secret_rotation_interval: int = 30  # days
    max_secret_age: int = 90  # days
    
    # Trust Guard specific
    confidence_threshold: float = 0.7
    max_length: int = 800
    min_length: int = 10

    model_config = {
        "env_file": ".env",
        "env_prefix": "TRUSTGUARD_"
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._secrets_cache: Dict[str, Any] = {}
        self._secrets_rotation: Dict[str, datetime] = {}
        self._initialize_secrets()
    
    def _initialize_secrets(self):
        """Initialize secrets with secure defaults if not provided."""
        if not self.secret_key:
            self.secret_key = self._generate_secret_key()
            self._secrets_cache["secret_key"] = self.secret_key
            self._secrets_rotation["secret_key"] = datetime.now(timezone.utc)
            logger.warning("Generated default secret key. Change in production!")
        
        if not self.jwt_secret:
            self.jwt_secret = self._generate_secret_key()
            self._secrets_cache["jwt_secret"] = self.jwt_secret
            self._secrets_rotation["jwt_secret"] = datetime.now(timezone.utc)
            logger.warning("Generated default JWT secret. Change in production!")
        
        if not self.encryption_key:
            self.encryption_key = self._generate_secret_key()
            self._secrets_cache["encryption_key"] = self.encryption_key
            self._secrets_rotation["encryption_key"] = datetime.now(timezone.utc)
            logger.warning("Generated default encryption key. Change in production!")
    
    def _generate_secret_key(self) -> str:
        """Generate a secure random secret key."""
        return secrets.token_urlsafe(32)
    
    def get_secret(self, secret_name: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret value with caching and rotation support."""
        try:
            if secret_name in self._secrets_cache:
                # Check if secret needs rotation
                if self._should_rotate_secret(secret_name):
                    self._rotate_secret(secret_name)
                return self._secrets_cache[secret_name]
            
            # Try to get from environment
            env_var = f"TRUSTGUARD_{secret_name.upper()}"
            secret_value = os.getenv(env_var, default)
            
            if secret_value:
                self._secrets_cache[secret_name] = secret_value
                self._secrets_rotation[secret_name] = datetime.now(timezone.utc)
            
            return secret_value
        except Exception as e:
            logger.error(f"Error getting secret {secret_name}: {e}")
            return default
    
    def _should_rotate_secret(self, secret_name: str) -> bool:
        """Check if a secret should be rotated."""
        if secret_name not in self._secrets_rotation:
            return False
        
        last_rotation = self._secrets_rotation[secret_name]
        rotation_interval = timedelta(days=self.secret_rotation_interval)
        
        return datetime.now(timezone.utc) - last_rotation > rotation_interval
    
    def _rotate_secret(self, secret_name: str):
        """Rotate a secret."""
        logger.info(f"Rotating secret: {secret_name}")
        
        # Generate new secret
        new_secret = self._generate_secret_key()
        
        # Update cache
        self._secrets_cache[secret_name] = new_secret
        self._secrets_rotation[secret_name] = datetime.now(timezone.utc)
        
        # Log rotation (but not the actual secret)
        logger.info(f"Secret rotated: {secret_name}")
    
    def validate_secrets(self) -> bool:
        """Validate that all required secrets are available."""
        required_secrets = ["secret_key", "jwt_secret", "encryption_key"]
        
        for secret_name in required_secrets:
            if not self.get_secret(secret_name):
                logger.error(f"Required secret missing: {secret_name}")
                return False
        
        return True
    
    def get_secrets_summary(self) -> Dict[str, Any]:
        """Get a summary of secrets status (without actual values)."""
        summary = {}
        
        for secret_name in ["secret_key", "jwt_secret", "encryption_key"]:
            has_secret = secret_name in self._secrets_cache
            last_rotation = self._secrets_rotation.get(secret_name)
            needs_rotation = self._should_rotate_secret(secret_name) if has_secret else False
            
            summary[secret_name] = {
                "available": has_secret,
                "last_rotation": last_rotation.isoformat() if last_rotation else None,
                "needs_rotation": needs_rotation
            }
        
        return summary


_config_instance = None

def get_config() -> TrustGuardConfig:
    """Get validated configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = TrustGuardConfig()
    return _config_instance
