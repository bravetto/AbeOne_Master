"""
Configuration Validation Module

This module provides configuration validation capabilities
for the CodeGuardians Gateway system.
"""

import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """A configuration validation result."""
    field: str
    severity: ValidationSeverity
    message: str
    current_value: Any = None
    suggested_value: Any = None
    rule: Optional[str] = None


class ConfigValidator:
    """Configuration validator."""
    
    def __init__(self):
        self._rules: Dict[str, Dict[str, Any]] = {}
        self._custom_validators: Dict[str, callable] = {}
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default validation rules."""
        self._rules = {
            "debug": {
                "type": bool,
                "description": "Debug mode flag"
            },
            "log_level": {
                "type": str,
                "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                "description": "Logging level"
            },
            "max_request_size": {
                "type": int,
                "min": 1024,  # 1KB
                "max": 104857600,  # 100MB
                "description": "Maximum request size in bytes"
            },
            "request_timeout": {
                "type": int,
                "min": 1,
                "max": 300,  # 5 minutes
                "description": "Request timeout in seconds"
            },
            "rate_limit_enabled": {
                "type": bool,
                "description": "Rate limiting enabled flag"
            },
            "rate_limit_requests_per_minute": {
                "type": int,
                "min": 1,
                "max": 10000,
                "description": "Rate limit requests per minute"
            },
            "cors_enabled": {
                "type": bool,
                "description": "CORS enabled flag"
            },
            "cors_origins": {
                "type": list,
                "description": "CORS allowed origins"
            },
            "health_check_interval": {
                "type": int,
                "min": 5,
                "max": 300,
                "description": "Health check interval in seconds"
            },
            "metrics_enabled": {
                "type": bool,
                "description": "Metrics collection enabled flag"
            },
            "metrics_port": {
                "type": int,
                "min": 1024,
                "max": 65535,
                "description": "Metrics server port"
            },
            "circuit_breaker_enabled": {
                "type": bool,
                "description": "Circuit breaker enabled flag"
            },
            "circuit_breaker_threshold": {
                "type": int,
                "min": 1,
                "max": 100,
                "description": "Circuit breaker failure threshold"
            },
            "circuit_breaker_timeout": {
                "type": int,
                "min": 10,
                "max": 3600,  # 1 hour
                "description": "Circuit breaker timeout in seconds"
            },
            "database_url": {
                "type": str,
                "pattern": r"^postgresql://.*",
                "description": "Database connection URL"
            },
            "redis_url": {
                "type": str,
                "pattern": r"^redis://.*",
                "description": "Redis connection URL"
            },
            "secret_key": {
                "type": str,
                "min_length": 32,
                "description": "Application secret key"
            },
            "jwt_secret_key": {
                "type": str,
                "min_length": 32,
                "description": "JWT secret key"
            },
            "jwt_algorithm": {
                "type": str,
                "choices": ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"],
                "description": "JWT algorithm"
            },
            "jwt_access_token_expire_minutes": {
                "type": int,
                "min": 1,
                "max": 1440,  # 24 hours
                "description": "JWT access token expiration in minutes"
            },
            "allowed_hosts": {
                "type": list,
                "description": "Allowed hostnames"
            },
            "guard_services_enabled": {
                "type": bool,
                "description": "Guard services enabled flag"
            },
            "bias_detection_enabled": {
                "type": bool,
                "description": "Bias detection enabled flag"
            },
            "token_optimization_enabled": {
                "type": bool,
                "description": "Token optimization enabled flag"
            },
            "context_management_enabled": {
                "type": bool,
                "description": "Context management enabled flag"
            },
            "trust_validation_enabled": {
                "type": bool,
                "description": "Trust validation enabled flag"
            },
            "health_monitoring_enabled": {
                "type": bool,
                "description": "Health monitoring enabled flag"
            }
        }
    
    def add_rule(self, field: str, rule: Dict[str, Any]) -> None:
        """Add a validation rule for a field."""
        self._rules[field] = rule
    
    def add_custom_validator(self, field: str, validator: callable) -> None:
        """Add a custom validator for a field."""
        self._custom_validators[field] = validator
    
    def validate_field(self, field: str, value: Any) -> List[ValidationResult]:
        """Validate a single field."""
        results = []
        
        if field not in self._rules:
            return results
        
        rule = self._rules[field]
        
        # Type validation
        if "type" in rule:
            if not isinstance(value, rule["type"]):
                results.append(ValidationResult(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Expected type {rule['type'].__name__}, got {type(value).__name__}",
                    current_value=value,
                    rule="type"
                ))
                return results  # Stop validation if type is wrong
        
        # Skip further validation if type is wrong
        if not isinstance(value, rule.get("type", type(value))):
            return results
        
        # Range validation for numbers
        if isinstance(value, (int, float)):
            if "min" in rule and value < rule["min"]:
                results.append(ValidationResult(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Value {value} is below minimum {rule['min']}",
                    current_value=value,
                    suggested_value=rule["min"],
                    rule="min"
                ))
            
            if "max" in rule and value > rule["max"]:
                results.append(ValidationResult(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Value {value} is above maximum {rule['max']}",
                    current_value=value,
                    suggested_value=rule["max"],
                    rule="max"
                ))
        
        # String length validation
        if isinstance(value, str):
            if "min_length" in rule and len(value) < rule["min_length"]:
                results.append(ValidationResult(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"String length {len(value)} is below minimum {rule['min_length']}",
                    current_value=value,
                    rule="min_length"
                ))
            
            if "max_length" in rule and len(value) > rule["max_length"]:
                results.append(ValidationResult(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"String length {len(value)} is above maximum {rule['max_length']}",
                    current_value=value,
                    rule="max_length"
                ))
            
            # Pattern validation
            if "pattern" in rule:
                import re
                if not re.match(rule["pattern"], value):
                    results.append(ValidationResult(
                        field=field,
                        severity=ValidationSeverity.ERROR,
                        message=f"Value does not match required pattern",
                        current_value=value,
                        rule="pattern"
                    ))
        
        # Enum/choices validation
        if "choices" in rule:
            if value not in rule["choices"]:
                results.append(ValidationResult(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Value {value} is not in allowed choices {rule['choices']}",
                    current_value=value,
                    suggested_value=rule["choices"][0] if rule["choices"] else None,
                    rule="choices"
                ))
        
        # Custom validator
        if field in self._custom_validators:
            try:
                custom_result = self._custom_validators[field](value)
                if custom_result:
                    if isinstance(custom_result, ValidationResult):
                        results.append(custom_result)
                    elif isinstance(custom_result, list):
                        results.extend(custom_result)
            except Exception as e:
                results.append(ValidationResult(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Custom validation failed: {str(e)}",
                    current_value=value,
                    rule="custom"
                ))
        
        return results
    
    def validate_config(self, config: Dict[str, Any]) -> List[ValidationResult]:
        """Validate an entire configuration."""
        results = []
        
        for field, value in config.items():
            field_results = self.validate_field(field, value)
            results.extend(field_results)
        
        return results
    
    def validate_required_fields(self, config: Dict[str, Any], 
                                required_fields: List[str]) -> List[ValidationResult]:
        """Validate that required fields are present."""
        results = []
        
        for field in required_fields:
            if field not in config or config[field] is None:
                results.append(ValidationResult(
                    field=field,
                    severity=ValidationSeverity.ERROR,
                    message=f"Required field '{field}' is missing",
                    rule="required"
                ))
        
        return results
    
    def get_validation_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Get a summary of validation results."""
        summary = {
            "total_issues": len(results),
            "by_severity": {},
            "by_field": {},
            "critical_issues": [],
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        for severity in ValidationSeverity:
            summary["by_severity"][severity.value] = 0
        
        for result in results:
            # Count by severity
            summary["by_severity"][result.severity.value] += 1
            
            # Count by field
            if result.field not in summary["by_field"]:
                summary["by_field"][result.field] = 0
            summary["by_field"][result.field] += 1
            
            # Categorize by severity
            if result.severity == ValidationSeverity.CRITICAL:
                summary["critical_issues"].append(result)
            elif result.severity == ValidationSeverity.ERROR:
                summary["errors"].append(result)
            elif result.severity == ValidationSeverity.WARNING:
                summary["warnings"].append(result)
            elif result.severity == ValidationSeverity.INFO:
                summary["info"].append(result)
        
        return summary
    
    def is_valid(self, results: List[ValidationResult]) -> bool:
        """Check if validation results indicate a valid configuration."""
        return not any(result.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] 
                      for result in results)


# Global validator instance
config_validator = ConfigValidator()


def validate_configuration(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Validate configuration and return results."""
    if config is None:
        # Try to get config from environment or default
        config = {}
        import os
        for key in config_validator._rules.keys():
            env_value = os.getenv(key.upper())
            if env_value is not None:
                # Convert string to appropriate type
                rule = config_validator._rules[key]
                expected_type = rule.get("type", str)
                if expected_type == bool:
                    config[key] = env_value.lower() in ('true', '1', 'yes', 'on')
                elif expected_type == int:
                    try:
                        config[key] = int(env_value)
                    except ValueError:
                        config[key] = env_value
                elif expected_type == list:
                    config[key] = [item.strip() for item in env_value.split(',')]
                else:
                    config[key] = env_value
            else:
                # Use default value if available
                if "default" in rule:
                    config[key] = rule["default"]
    
    # Validate the configuration
    results = config_validator.validate_config(config)
    summary = config_validator.get_validation_summary(results)
    
    return {
        "valid": config_validator.is_valid(results),
        "results": results,
        "summary": summary,
        "config": config
    }


def validate_field(field: str, value: Any) -> List[ValidationResult]:
    """Validate a single field."""
    return config_validator.validate_field(field, value)


def add_validation_rule(field: str, rule: Dict[str, Any]) -> None:
    """Add a validation rule."""
    config_validator.add_rule(field, rule)


def add_custom_validator(field: str, validator: callable) -> None:
    """Add a custom validator."""
    config_validator.add_custom_validator(field, validator)
