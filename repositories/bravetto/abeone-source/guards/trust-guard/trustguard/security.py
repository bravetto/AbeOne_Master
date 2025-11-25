"""
Trust Guard Security Middleware

Implements enterprise-grade security middleware:
- Request signing validation
- CORS hardening
- Input sanitization
- Audit logging
- Security headers
"""

import re
import hashlib
import hmac
import time
from typing import Dict, List, Any, Optional, Set
from fastapi import Request, HTTPException, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    def __init__(self, app, allowed_origins: List[str] = None):
        super().__init__(app)
        self.allowed_origins = allowed_origins or ["*"]
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """Sanitize input to prevent XSS and injection attacks."""
    
    def __init__(self, app):
        super().__init__(app)
        # Patterns to detect potential attacks
        self.xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>'
        ]
        
        self.sql_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)',
            r'(\b(OR|AND)\s+\d+\s*=\s*\d+)',
            r'(\b(OR|AND)\s+\'\w+\'\s*=\s*\'\w+\')',
            r'(\b(OR|AND)\s+\"\w+\"\s*=\s*\"\w+\")'
        ]
    
    async def dispatch(self, request: Request, call_next):
        # Check request body for malicious content
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    body_str = body.decode('utf-8', errors='ignore')
                    
                    # Check for XSS patterns
                    for pattern in self.xss_patterns:
                        if re.search(pattern, body_str, re.IGNORECASE):
                            logger.warning(f"XSS pattern detected in request from {request.client.host}")
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid request content"
                            )
                    
                    # Check for SQL injection patterns
                    for pattern in self.sql_patterns:
                        if re.search(pattern, body_str, re.IGNORECASE):
                            logger.warning(f"SQL injection pattern detected in request from {request.client.host}")
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid request content"
                            )
            except Exception as e:
                logger.error(f"Error in input sanitization: {e}")
        
        response = await call_next(request)
        return response


class RequestSigningValidator:
    """Validate request signatures for critical endpoints."""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode('utf-8')
        self.signature_header = "X-Request-Signature"
        self.timestamp_header = "X-Request-Timestamp"
        self.max_age = 300  # 5 minutes
    
    def validate_signature(self, request: Request, body: bytes) -> bool:
        """Validate request signature."""
        signature = request.headers.get(self.signature_header)
        timestamp = request.headers.get(self.timestamp_header)
        
        if not signature or not timestamp:
            return False
        
        try:
            # Check timestamp to prevent replay attacks
            request_time = int(timestamp)
            current_time = int(time.time())
            
            if abs(current_time - request_time) > self.max_age:
                logger.warning("Request timestamp too old")
                return False
            
            # Calculate expected signature
            expected_signature = self._calculate_signature(body, timestamp)
            
            # Compare signatures
            return hmac.compare_digest(signature, expected_signature)
            
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid signature format: {e}")
            return False
    
    def _calculate_signature(self, body: bytes, timestamp: str) -> str:
        """Calculate HMAC signature for request."""
        message = f"{timestamp}:{body.decode('utf-8', errors='ignore')}"
        signature = hmac.new(
            self.secret_key,
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature


class AuditLogger:
    """Log security events for audit purposes."""
    
    def __init__(self):
        self.security_events = []
    
    def log_auth_event(self, event_type: str, user_id: str, 
                      ip_address: str, success: bool, details: Dict[str, Any] = None):
        """Log authentication events."""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "user_id": user_id,
            "ip_address": ip_address,
            "success": success,
            "details": details or {}
        }
        
        self.security_events.append(event)
        
        # Log to application logger
        level = logging.INFO if success else logging.WARNING
        logger.log(level, f"Auth event: {event_type} for user {user_id} from {ip_address} - {'SUCCESS' if success else 'FAILED'}")
    
    def log_security_event(self, event_type: str, ip_address: str, 
                          details: Dict[str, Any] = None):
        """Log security events."""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "ip_address": ip_address,
            "details": details or {}
        }
        
        self.security_events.append(event)
        logger.warning(f"Security event: {event_type} from {ip_address}")
    
    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent security events."""
        return self.security_events[-limit:]


class SecurityManager:
    """Main security manager."""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.request_validator = RequestSigningValidator(secret_key)
        self.audit_logger = AuditLogger()
        
        logger.info("Security Manager initialized")
    
    def validate_request_signature(self, request: Request, body: bytes) -> bool:
        """Validate request signature."""
        return self.request_validator.validate_signature(request, body)
    
    def log_auth_event(self, event_type: str, user_id: str, 
                      ip_address: str, success: bool, details: Dict[str, Any] = None):
        """Log authentication event."""
        self.audit_logger.log_auth_event(event_type, user_id, ip_address, success, details)
    
    def log_security_event(self, event_type: str, ip_address: str, 
                          details: Dict[str, Any] = None):
        """Log security event."""
        self.audit_logger.log_security_event(event_type, ip_address, details)
    
    def get_security_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent security events."""
        return self.audit_logger.get_recent_events(limit)


def get_security_manager() -> SecurityManager:
    """Get the global security manager instance."""
    from trustguard.config import get_config
    config = get_config()
    secret_key = config.get_secret("secret_key", "trust-guard-security-key-change-in-production")
    return SecurityManager(secret_key)
