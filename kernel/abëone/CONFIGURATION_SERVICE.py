"""
Configuration Service - Centralized Configuration and Secrets Management

Provides configuration loading, validation, and secrets management.

Pattern: CONFIG × SERVICE × SECRETS × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import json
import os
import threading
from pathlib import Path


@dataclass
class ConfigValidationError(Exception):
    """Configuration validation error."""
    message: str
    key: Optional[str] = None


class ConfigurationService:
    """
    Configuration Service.
    
    Responsibilities:
    - Configuration loading and validation
    - Secrets management
    - Environment variable management
    - Configuration versioning
    - Configuration hot-reloading (optional)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration service."""
        self.config_path = config_path or "config/abeone.config.json"
        self.config: Dict[str, Any] = {}
        self.secrets: Dict[str, str] = {}
        self.env_vars: Dict[str, str] = {}
        self.version: str = "1.0.0"
        self.last_reload: Optional[datetime] = None
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Load configuration on initialization
        self.load_config(self.config_path)
    
    def load_config(self, config_path: str) -> bool:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
        
        Returns:
            True if load successful
        """
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                # Create default configuration
                self.config = self._create_default_config()
                self._save_config(config_path)
                return True
            
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            with self._lock:
                self.config = config_data
                self.config_path = config_path
                self.last_reload = datetime.now()
            
            # Validate configuration
            if not self.validate_config(self.config):
                raise ConfigValidationError("Configuration validation failed")
            
            # Load secrets if configured
            if "secrets" in self.config:
                self._load_secrets()
            
            return True
            
        except Exception as e:
            print(f" Failed to load configuration: {e}")
            # Use default configuration
            with self._lock:
                self.config = self._create_default_config()
            return False
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration."""
        return {
            "kernel": {
                "version": "1.0.0",
                "state": "ready"
            },
            "modules": {},
            "event_bus": {
                "max_history": 1000,
                "routing_rules": {}
            },
            "secrets": {
                "encrypted": False,
                "provider": "env"
            },
            "pipelines": {},
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    
    def _save_config(self, config_path: str) -> None:
        """Save configuration to file."""
        try:
            config_file = Path(config_path)
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f" Failed to save configuration: {e}")
    
    def _load_secrets(self) -> None:
        """Load secrets from configured provider."""
        secrets_config = self.config.get("secrets", {})
        provider = secrets_config.get("provider", "env")
        
        if provider == "env":
            # Load from environment variables
            # Secrets are prefixed with ABEONE_SECRET_
            for key, value in os.environ.items():
                if key.startswith("ABEONE_SECRET_"):
                    secret_key = key.replace("ABEONE_SECRET_", "").lower()
                    self.secrets[secret_key] = value
        elif provider == "file":
            # Load from secrets file
            secrets_file = secrets_config.get("file", "config/secrets.json")
            secrets_path = Path(secrets_file)
            if secrets_path.exists():
                with open(secrets_path, 'r') as f:
                    self.secrets = json.load(f)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports dot notation).
        
        Args:
            key: Configuration key (e.g., "kernel.version" or "modules.ads_engine.enabled")
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        with self._lock:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
    
    def set_config(self, key: str, value: Any) -> None:
        """
        Set configuration value by key (supports dot notation).
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        with self._lock:
            keys = key.split('.')
            config = self.config
            
            # Navigate to parent dict
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Set value
            config[keys[-1]] = value
            
            # Save configuration
            self._save_config(self.config_path)
    
    def get_secret(self, key: str) -> Optional[str]:
        """
        Get secret by key.
        
        Args:
            key: Secret key
        
        Returns:
            Secret value or None
        """
        with self._lock:
            return self.secrets.get(key)
    
    def set_secret(self, key: str, value: str) -> None:
        """
        Set secret by key.
        
        Args:
            key: Secret key
            value: Secret value
        """
        with self._lock:
            self.secrets[key] = value
            
            # Save secrets if file provider
            secrets_config = self.config.get("secrets", {})
            provider = secrets_config.get("provider", "env")
            
            if provider == "file":
                secrets_file = secrets_config.get("file", "config/secrets.json")
                secrets_path = Path(secrets_file)
                secrets_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(secrets_path, 'w') as f:
                    json.dump(self.secrets, f, indent=2)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate configuration structure.
        
        Args:
            config: Configuration dictionary
        
        Returns:
            True if valid
        """
        try:
            # Validate kernel section
            if "kernel" not in config:
                raise ConfigValidationError("Missing 'kernel' section", "kernel")
            
            kernel = config["kernel"]
            if "version" not in kernel:
                raise ConfigValidationError("Missing 'kernel.version'", "kernel.version")
            
            # Validate modules section
            if "modules" not in config:
                raise ConfigValidationError("Missing 'modules' section", "modules")
            
            if not isinstance(config["modules"], dict):
                raise ConfigValidationError("'modules' must be a dictionary", "modules")
            
            # Validate event_bus section
            if "event_bus" not in config:
                raise ConfigValidationError("Missing 'event_bus' section", "event_bus")
            
            event_bus = config["event_bus"]
            if "max_history" not in event_bus:
                raise ConfigValidationError("Missing 'event_bus.max_history'", "event_bus.max_history")
            
            return True
            
        except ConfigValidationError as e:
            print(f" Configuration validation error: {e.message} (key: {e.key})")
            return False
        except Exception as e:
            print(f" Configuration validation error: {e}")
            return False
    
    def reload_config(self) -> bool:
        """
        Reload configuration from file.
        
        Returns:
            True if reload successful
        """
        return self.load_config(self.config_path)
    
    def get_module_config(self, module_id: str) -> Dict[str, Any]:
        """
        Get module-specific configuration.
        
        Args:
            module_id: Module identifier
        
        Returns:
            Module configuration dictionary
        """
        module_config = self.get_config(f"modules.{module_id}", {})
        return module_config if isinstance(module_config, dict) else {}
    
    def is_module_enabled(self, module_id: str) -> bool:
        """
        Check if module is enabled.
        
        Args:
            module_id: Module identifier
        
        Returns:
            True if module is enabled
        """
        module_config = self.get_module_config(module_id)
        return module_config.get("enabled", True)
    
    def get_all_modules(self) -> List[str]:
        """
        Get list of all configured modules.
        
        Returns:
            List of module IDs
        """
        modules = self.get_config("modules", {})
        return list(modules.keys()) if isinstance(modules, dict) else []


# Global configuration service instance
_config_service_instance: Optional[ConfigurationService] = None


def get_config_service() -> ConfigurationService:
    """Get global configuration service instance."""
    global _config_service_instance
    if _config_service_instance is None:
        _config_service_instance = ConfigurationService()
    return _config_service_instance

