"""
Security Hardening - Production Security Measures

Additional security measures for production deployment.
"""

import logging
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib
import hmac

from app.utils.logging import get_logger
from prometheus_client import Counter

logger = get_logger(__name__)

# Security metrics
SECURITY_VIOLATIONS = Counter(
    'REPLACE_ME',
    'Total security violations detected',
    ['violation_type']
)

RATE_LIMIT_EXCEEDED = Counter(
    'REPLACE_ME',
    'Total rate limit violations',
    ['identifier']
)


class SecurityHardener:
    """
    Security hardening component.
    
    PRODUCTION HARDENED:
    - Input validation
    - Rate limiting
    - Request signing
    - IP whitelisting
    - Payload sanitization
    """
    
    def __init__(self):
        """Initialize security hardener."""
        self.rate_limits: Dict[str, List[datetime]] = {}
        self.allowed_ips: Optional[List[str]] = None
        self.secret_key: Optional[str] = None
        
        # Production hardening: Configurable limits
        self.max_requests_per_minute = 100
        self.max_payload_size = 10 * 1024 * 1024  # 10MB
        self.rate_limit_window = timedelta(minutes=1)
    
    def validate_request_id(self, request_id: str) -> bool:
        """
        Validate request ID format.
        
        PRODUCTION: Prevents injection attacks
        """
        if not request_id:
            return False
        
        # Must be alphanumeric with hyphens/underscores, max 100 chars
        if not re.match(r'^[a-zA-Z0-9_-]{1,100}$', request_id):
            SECURITY_VIOLATIONS.labels(violation_type="invalid_request_id").inc()
            return False
        
        return True
    
    def validate_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Validate payload for security issues.
        
        PRODUCTION: Prevents injection, size limits, content validation
        """
        import json
        
        # Check payload size
        payload_str = json.dumps(payload)
        payload_size = len(payload_str.encode('utf-8'))
        
        if payload_size > self.max_payload_size:
            SECURITY_VIOLATIONS.labels(violation_type="payload_too_large").inc()
            logger.warning(f"Payload size {payload_size} exceeds maximum {self.max_payload_size}")
            return False
        
        # Check for dangerous patterns
        payload_lower = payload_str.lower()
        dangerous_patterns = [
            r'<script[^>]*>',
            r'javascript:',
            r'on\w+\s*=',
            r'eval\s*\(',
            r'exec\s*\(',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, payload_lower):
                SECURITY_VIOLATIONS.labels(violation_type="dangerous_pattern").inc()
                logger.warning(f"Dangerous pattern detected: {pattern}")
                return False
        
        return True
    
    def check_rate_limit(self, identifier: str) -> bool:
        """
        Check rate limit for identifier.
        
        PRODUCTION: Per-identifier rate limiting
        """
        now = datetime.now()
        
        # Clean old entries
        if identifier in self.rate_limits:
            self.rate_limits[identifier] = [
                timestamp for timestamp in self.rate_limits[identifier]
                if now - timestamp < self.rate_limit_window
            ]
        else:
            self.rate_limits[identifier] = []
        
        # Check limit
        if len(self.rate_limits[identifier]) >= self.max_requests_per_minute:
            RATE_LIMIT_EXCEEDED.labels(identifier=identifier).inc()
            SECURITY_VIOLATIONS.labels(violation_type="rate_limit_exceeded").inc()
            return False
        
        # Add current request
        self.rate_limits[identifier].append(now)
        return True
    
    def validate_ip(self, ip_address: str) -> bool:
        """
        Validate IP address against whitelist.
        
        PRODUCTION: IP whitelisting if configured
        """
        if self.allowed_ips is None:
            # No whitelist configured, allow all
            return True
        
        if ip_address in self.allowed_ips:
            return True
        
        SECURITY_VIOLATIONS.labels(violation_type="ip_not_whitelisted").inc()
        logger.warning(f"IP {ip_address} not in whitelist")
        return False
    
    def sanitize_input(self, data: Any) -> Any:
        """
        Sanitize input data.
        
        PRODUCTION: Remove dangerous content
        """
        if isinstance(data, str):
            # Remove null bytes
            data = data.replace('\x00', '')
            # Limit length
            if len(data) > 100000:  # 100KB max
                data = data[:100000]
            return data
        
        elif isinstance(data, dict):
            return {k: self.sanitize_input(v) for k, v in data.items()}
        
        elif isinstance(data, list):
            return [self.sanitize_input(item) for item in data]
        
        return data
    
    def verify_request_signature(self, payload: str, signature: str) -> bool:
        """
        Verify request signature.
        
        PRODUCTION: HMAC signature verification
        """
        if not self.secret_key:
            # No secret key configured, skip verification
            return True
        
        try:
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(expected_signature, signature)
        except Exception as e:
            logger.error(f"Signature verification error: {e}")
            return False
    
    def configure(
        self,
        allowed_ips: Optional[List[str]] = None,
        secret_key: Optional[str] = None,
        max_requests_per_minute: int = 100
    ):
        """
        Configure security settings.
        
        Args:
            allowed_ips: List of allowed IP addresses (None = allow all)
            secret_key: Secret key for request signing
            max_requests_per_minute: Maximum requests per minute per identifier
        """
        self.allowed_ips = allowed_ips
        self.secret_key = secret_key
        self.max_requests_per_minute = max_requests_per_minute
        logger.info("Security hardener configured")


# Global security hardener instance
_security_hardener: Optional[SecurityHardener] = None


def get_security_hardener() -> SecurityHardener:
    """Get global security hardener instance."""
    global _security_hardener
    if _security_hardener is None:
        _security_hardener = SecurityHardener()
    return _security_hardener

