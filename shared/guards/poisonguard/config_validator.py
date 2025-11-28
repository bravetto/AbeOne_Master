"""
Configuration validation for PoisonGuard.
Provides robust validation for config.yaml and runtime configuration.
"""

import yaml
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, field_validator, Field, ConfigDict
import logging

logger = logging.getLogger(__name__)


class PluginConfig(BaseModel):
    """Configuration for a single plugin."""
    name: str = Field(..., description="Plugin name")
    class_name: str = Field(..., alias="class", description="Plugin class name")
    config: Dict[str, Any] = Field(default_factory=dict, description="Plugin configuration")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("Plugin name must be a non-empty string")
        return v
    
    @field_validator('class_name')
    @classmethod
    def validate_class_name(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("Plugin class must be a non-empty string")
        if '.' not in v:
            raise ValueError("Plugin class must be in format 'module.ClassName'")
        return v


class AnalyzerConfig(BaseModel):
    """Configuration for the analyzer component."""
    plugins: List[PluginConfig] = Field(default_factory=list, description="List of analysis plugins")
    
    @field_validator('plugins')
    @classmethod
    def validate_plugins(cls, v):
        if not v:
            logger.warning("No plugins configured for analyzer")
            return v
        
        # Check for duplicate plugin names
        names = [plugin.name for plugin in v]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate plugin names found")
        
        # Validate each plugin
        for plugin in v:
            if not plugin.name:
                raise ValueError("Plugin name cannot be empty")
            if not plugin.class_name:
                raise ValueError("Plugin class cannot be empty")
        
        return v


class MitigatorConfig(BaseModel):
    """Configuration for the mitigator component."""
    default_action: str = Field(default="flag", description="Default mitigation action")
    sanitize_keywords: List[str] = Field(default_factory=list, description="Keywords to sanitize")
    
    @field_validator('default_action')
    @classmethod
    def validate_default_action(cls, v):
        valid_actions = ['flag', 'sanitize', 'redact', 'none']
        if v not in valid_actions:
            raise ValueError(f"Invalid default action: {v}. Must be one of {valid_actions}")
        return v
    
    @field_validator('sanitize_keywords')
    @classmethod
    def validate_sanitize_keywords(cls, v):
        if not isinstance(v, list):
            raise ValueError("Sanitize keywords must be a list")
        for keyword in v:
            if not isinstance(keyword, str) or not keyword.strip():
                raise ValueError("All sanitize keywords must be non-empty strings")
        return v


class LoggingConfig(BaseModel):
    """Configuration for logging."""
    version: int = Field(default=1, description="Logging configuration version")
    disable_existing_loggers: bool = Field(default=False, description="Disable existing loggers")
    formatters: Dict[str, Any] = Field(default_factory=dict, description="Log formatters")
    handlers: Dict[str, Any] = Field(default_factory=dict, description="Log handlers")
    root: Dict[str, Any] = Field(default_factory=dict, description="Root logger configuration")
    
    @field_validator('version')
    @classmethod
    def validate_version(cls, v):
        if v != 1:
            raise ValueError("Only logging configuration version 1 is supported")
        return v


class DatabaseConfig(BaseModel):
    """Configuration for database."""
    url: str = Field(default="sqlite:///poisonguard.db", description="Database URL")
    echo: bool = Field(default=False, description="Echo SQL queries")
    pool_size: int = Field(default=5, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Maximum overflow connections")
    
    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("Database URL must be a non-empty string")
        return v
    
    @field_validator('pool_size')
    @classmethod
    def validate_pool_size(cls, v):
        if v < 1 or v > 100:
            raise ValueError("Pool size must be between 1 and 100")
        return v


class PoisonGuardConfig(BaseModel):
    """Main configuration model for PoisonGuard."""
    analyzer: AnalyzerConfig = Field(default_factory=AnalyzerConfig, description="Analyzer configuration")
    mitigator: MitigatorConfig = Field(default_factory=MitigatorConfig, description="Mitigator configuration")
    logging: LoggingConfig = Field(default_factory=LoggingConfig, description="Logging configuration")
    database: DatabaseConfig = Field(default_factory=DatabaseConfig, description="Database configuration")
    
    model_config = ConfigDict(extra="forbid")  # Reject extra fields


class ConfigValidator:
    """Configuration validator for PoisonGuard."""
    
    def __init__(self):
        self.config: Optional[PoisonGuardConfig] = None
        self.validation_errors: List[str] = []
    
    def load_and_validate(self, config_path: str = "config.yaml") -> PoisonGuardConfig:
        """Load and validate configuration file."""
        try:
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            
            if not config_data:
                raise ValueError("Configuration file is empty")
            
            # Validate the configuration
            self.config = PoisonGuardConfig(**config_data)
            logger.info("Configuration loaded and validated successfully")
            return self.config
            
        except FileNotFoundError as e:
            logger.error(f"Configuration file not found: {e}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in configuration file: {e}")
            raise ValueError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            self.validation_errors.append(str(e))
            raise ValueError(f"Configuration validation failed: {e}")
    
    def validate_plugin_configs(self) -> List[str]:
        """Validate plugin configurations specifically."""
        errors = []
        
        if not self.config:
            return ["No configuration loaded"]
        
        for plugin in self.config.analyzer.plugins:
            try:
                # Check if plugin class exists
                module_name, class_name = plugin.class_name.rsplit('.', 1)
                
                # Validate keyword plugin config
                if plugin.name == "keyword":
                    if 'keyword_list' not in plugin.config:
                        errors.append(f"Keyword plugin '{plugin.name}' missing 'keyword_list' in config")
                    elif not isinstance(plugin.config['keyword_list'], list):
                        errors.append(f"Keyword plugin '{plugin.name}' keyword_list must be a list")
                
                # Validate length plugin config
                elif plugin.name == "length":
                    required_fields = ['min_length', 'max_length']
                    for field in required_fields:
                        if field not in plugin.config:
                            errors.append(f"Length plugin '{plugin.name}' missing '{field}' in config")
                        elif not isinstance(plugin.config[field], (int, float)):
                            errors.append(f"Length plugin '{plugin.name}' {field} must be a number")
                    
                    if 'min_length' in plugin.config and 'max_length' in plugin.config:
                        if plugin.config['min_length'] >= plugin.config['max_length']:
                            errors.append(f"Length plugin '{plugin.name}' min_length must be less than max_length")
                
                # Validate model plugin config
                elif plugin.name == "model":
                    if 'model_name' not in plugin.config:
                        errors.append(f"Model plugin '{plugin.name}' missing 'model_name' in config")
                    if 'toxicity_threshold' not in plugin.config:
                        errors.append(f"Model plugin '{plugin.name}' missing 'toxicity_threshold' in config")
                    elif not isinstance(plugin.config['toxicity_threshold'], (int, float)):
                        errors.append(f"Model plugin '{plugin.name}' toxicity_threshold must be a number")
                    elif not (0 <= plugin.config['toxicity_threshold'] <= 1):
                        errors.append(f"Model plugin '{plugin.name}' toxicity_threshold must be between 0 and 1")
                        
            except Exception as e:
                errors.append(f"Error validating plugin '{plugin.name}': {e}")
        
        return errors
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary."""
        if not self.config:
            return {
                "valid": False,
                "errors": ["No configuration loaded"],
                "warnings": []
            }
        
        plugin_errors = self.validate_plugin_configs()
        warnings = []
        
        # Check for warnings
        if not self.config.analyzer.plugins:
            warnings.append("No analysis plugins configured")
        
        if self.config.mitigator.default_action == "sanitize" and not self.config.mitigator.sanitize_keywords:
            warnings.append("Sanitize action configured but no sanitize keywords provided")
        
        return {
            "valid": len(plugin_errors) == 0,
            "errors": plugin_errors,
            "warnings": warnings,
            "plugin_count": len(self.config.analyzer.plugins),
            "default_action": self.config.mitigator.default_action
        }


def validate_config(config_path: str = "config.yaml") -> PoisonGuardConfig:
    """Convenience function to validate configuration."""
    validator = ConfigValidator()
    return validator.load_and_validate(config_path)


def get_config_validation_report(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Get detailed configuration validation report."""
    validator = ConfigValidator()
    try:
        validator.load_and_validate(config_path)
        return validator.get_validation_summary()
    except Exception as e:
        return {
            "valid": False,
            "errors": [str(e)],
            "warnings": []
        }
