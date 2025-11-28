"""
Enhanced Input Validation Module

PRODUCTION HARDENING:
- SQL injection prevention (parameterized queries verification)
- XSS prevention (HTML escaping, script tag detection)
- Path traversal prevention (directory traversal detection)
- Command injection prevention (shell command detection)
- Payload size validation
- Dangerous pattern detection

SAFETY: All validation fails securely (deny by default)
ASSUMES: Input is untrusted until validated
VERIFY: All inputs validated before processing
"""

import re
import os
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from urllib.parse import urlparse, unquote

from app.utils.logging import get_logger
from app.core.exceptions import ValidationError

logger = get_logger(__name__)

# Maximum payload size (10MB)
MAX_PAYLOAD_SIZE = 10 * 1024 * 1024

# Path traversal patterns
PATH_TRAVERSAL_PATTERNS = [
    r'\.\./',           # ../
    r'\.\.\\',          # ..\
    r'\.\./',           # ../ (encoded)
    r'%2e%2e%2f',       # ../
    r'%2e%2e%5c',       # ..\
    r'\.\.%2f',         # ../
    r'\.\.%5c',         # ..\
    r'\.\./',           # Double slash
    r'//',              # Double slash
    r'\\\\',            # Double backslash
]

# Command injection patterns
COMMAND_INJECTION_PATTERNS = [
    r'[|&;`$]',         # Pipe, ampersand, semicolon, backtick, dollar
    r'system\s*\(',     # system()
    r'shell_exec\s*\(',
    r'exec\s*\(',
    r'popen\s*\(',
    r'proc_open\s*\(',
    r'passthru\s*\(',
    r'cmd\s*/',         # cmd /
    r'powershell\s*',   # powershell
    r'bash\s*-',        # bash -
    r'sh\s*-',          # sh -
    r'/bin/sh',         # /bin/sh
    r'/bin/bash',       # /bin/bash
    r'wget\s+',         # wget
    r'curl\s+',         # curl
    r'nc\s+',           # netcat
    r'python\s+',       # python
    r'perl\s+',         # perl
]

# SQL injection patterns (for detection/alerting - queries should be parameterized)
SQL_INJECTION_PATTERNS = [
    r"'\s*OR\s*'1'\s*=\s*'1",    # ' OR '1'='1
    r"'\s*OR\s*1\s*=\s*1",       # ' OR 1=1
    r"'\s*UNION\s*SELECT",        # ' UNION SELECT
    r"'\s*DROP\s*TABLE",         # ' DROP TABLE
    r"'\s*DELETE\s*FROM",         # ' DELETE FROM
    r"'\s*UPDATE\s*SET",          # ' UPDATE SET
    r"'\s*INSERT\s*INTO",        # ' INSERT INTO
    r";\s*--",                    # ; --
    r";\s*/\*",                   # ; /*
    r"'\s*--",                    # ' --
    r"'\s*/\*",                   # ' /*
]

# XSS patterns
XSS_PATTERNS = [
    r'<script[^>]*>',             # <script>
    r'</script>',                 # </script>
    r'javascript:',               # javascript:
    r'on\w+\s*=',                # onclick=, onerror=, etc.
    r'eval\s*\(',                 # eval()
    r'expression\s*\(',           # expression()
    r'vbscript:',                 # vbscript:
    r'<iframe[^>]*>',              # <iframe>
    r'<object[^>]*>',             # <object>
    r'<embed[^>]*>',              # <embed>
    r'<img[^>]*onerror',         # <img onerror=
    r'<svg[^>]*onload',           # <svg onload=
]


class InputValidationError(ValidationError):
    """Input validation error."""
    pass


class InputValidator:
    """
    Comprehensive input validator for production hardening.
    
    SAFETY: All validation fails securely (deny by default)
    ASSUMES: Input is untrusted until validated
    VERIFY: All inputs validated before processing
    """
    
    def __init__(self):
        """Initialize input validator."""
        self.max_payload_size = MAX_PAYLOAD_SIZE
        self.detected_threats: List[Dict[str, Any]] = []
    
    def validate_payload_size(self, payload: Union[str, Dict[str, Any], bytes]) -> bool:
        """
        Validate payload size.
        
        SAFETY: Prevents resource exhaustion attacks
        VERIFY: Returns True if size acceptable, False otherwise
        """
        import json
        
        if isinstance(payload, bytes):
            size = len(payload)
        elif isinstance(payload, str):
            size = len(payload.encode('utf-8'))
        elif isinstance(payload, dict):
            size = len(json.dumps(payload).encode('utf-8'))
        else:
            size = len(str(payload).encode('utf-8'))
        
        if size > self.max_payload_size:
            logger.warning(f"Payload size {size} exceeds maximum {self.max_payload_size}")
            return False
        
        return True
    
    def detect_sql_injection(self, input_str: str) -> bool:
        """
        Detect SQL injection patterns.
        
        SAFETY: SQLAlchemy uses parameterized queries, but we detect patterns for alerting
        VERIFY: Returns True if SQL injection pattern detected
        """
        input_lower = input_str.lower()
        for pattern in SQL_INJECTION_PATTERNS:
            if re.search(pattern, input_lower, re.IGNORECASE):
                logger.warning(f"SQL injection pattern detected: {pattern}")
                self.detected_threats.append({
                    "type": "sql_injection",
                    "pattern": pattern,
                    "input_preview": input_str[:100]
                })
                return True
        return False
    
    def detect_xss(self, input_str: str) -> bool:
        """
        Detect XSS patterns.
        
        SAFETY: HTML escaping handles most cases, but we detect patterns for alerting
        VERIFY: Returns True if XSS pattern detected
        """
        input_lower = input_str.lower()
        for pattern in XSS_PATTERNS:
            if re.search(pattern, input_lower, re.IGNORECASE):
                logger.warning(f"XSS pattern detected: {pattern}")
                self.detected_threats.append({
                    "type": "xss",
                    "pattern": pattern,
                    "input_preview": input_str[:100]
                })
                return True
        return False
    
    def detect_path_traversal(self, path: str) -> bool:
        """
        Detect path traversal attempts.
        
        SAFETY: Prevents directory traversal attacks
        VERIFY: Returns True if path traversal detected
        """
        # Decode URL encoding
        decoded_path = unquote(path)
        
        # Normalize path separators
        normalized = decoded_path.replace('\\', '/')
        
        # Check for traversal patterns
        for pattern in PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, normalized, re.IGNORECASE):
                logger.warning(f"Path traversal pattern detected: {pattern} in {path}")
                self.detected_threats.append({
                    "type": "path_traversal",
                    "pattern": pattern,
                    "path": path
                })
                return True
        
        # Check for absolute paths (depending on context)
        if normalized.startswith('/') and not normalized.startswith('/api/'):
            # Allow API paths, but log others
            if not any(normalized.startswith(allowed) for allowed in ['/api/', '/health', '/metrics', '/docs']):
                logger.warning(f"Suspicious absolute path: {path}")
                return True
        
        return False
    
    def detect_command_injection(self, input_str: str) -> bool:
        """
        Detect command injection patterns.
        
        SAFETY: Prevents shell command execution
        VERIFY: Returns True if command injection detected
        """
        input_lower = input_str.lower()
        for pattern in COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, input_lower, re.IGNORECASE):
                logger.warning(f"Command injection pattern detected: {pattern}")
                self.detected_threats.append({
                    "type": "command_injection",
                    "pattern": pattern,
                    "input_preview": input_str[:100]
                })
                return True
        return False
    
    def validate_string_input(
        self,
        value: str,
        max_length: Optional[int] = None,
        check_sql: bool = True,
        check_xss: bool = True,
        check_path_traversal: bool = False,
        check_command_injection: bool = True
    ) -> bool:
        """
        Validate string input comprehensively.
        
        SAFETY: Validates all known attack vectors
        VERIFY: Returns True if input is safe, False otherwise
        """
        if not isinstance(value, str):
            logger.warning(f"Input is not a string: {type(value)}")
            return False
        
        # Check length
        if max_length and len(value) > max_length:
            logger.warning(f"Input length {len(value)} exceeds maximum {max_length}")
            return False
        
        # Check for SQL injection
        if check_sql and self.detect_sql_injection(value):
            return False
        
        # Check for XSS
        if check_xss and self.detect_xss(value):
            return False
        
        # Check for path traversal
        if check_path_traversal and self.detect_path_traversal(value):
            return False
        
        # Check for command injection
        if check_command_injection and self.detect_command_injection(value):
            return False
        
        return True
    
    def validate_path(self, path: str, allowed_base: Optional[str] = None) -> bool:
        """
        Validate file/directory path.
        
        SAFETY: Prevents path traversal attacks
        VERIFY: Returns True if path is safe, False otherwise
        """
        if not isinstance(path, str):
            return False
        
        # Detect path traversal
        if self.detect_path_traversal(path):
            return False
        
        # If allowed_base is specified, ensure path is within it
        if allowed_base:
            try:
                # Resolve paths
                base_path = Path(allowed_base).resolve()
                full_path = (base_path / path).resolve()
                
                # Ensure resolved path is within base
                if not str(full_path).startswith(str(base_path)):
                    logger.warning(f"Path {path} escapes base {allowed_base}")
                    return False
            except Exception as e:
                logger.warning(f"Path validation error: {e}")
                return False
        
        return True
    
    def validate_url(self, url: str, allowed_schemes: List[str] = None) -> bool:
        """
        Validate URL.
        
        SAFETY: Prevents malicious URL usage
        VERIFY: Returns True if URL is safe, False otherwise
        """
        if not isinstance(url, str):
            return False
        
        if allowed_schemes is None:
            allowed_schemes = ['http', 'https']
        
        try:
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in allowed_schemes:
                logger.warning(f"URL scheme {parsed.scheme} not allowed")
                return False
            
            # Check hostname
            if not parsed.hostname:
                logger.warning("URL missing hostname")
                return False
            
            # Check path for traversal
            if parsed.path and self.detect_path_traversal(parsed.path):
                return False
            
            return True
            
        except Exception as e:
            logger.warning(f"URL validation error: {e}")
            return False
    
    def validate_json_structure(self, data: Any, max_depth: int = 10) -> bool:
        """
        Validate JSON structure to prevent deep nesting attacks.
        
        SAFETY: Prevents resource exhaustion from deeply nested structures
        VERIFY: Returns True if structure is safe, False otherwise
        """
        def check_depth(obj: Any, current_depth: int = 0) -> bool:
            if current_depth > max_depth:
                logger.warning(f"JSON structure exceeds maximum depth {max_depth}")
                return False
            
            if isinstance(obj, dict):
                for value in obj.values():
                    if not check_depth(value, current_depth + 1):
                        return False
            elif isinstance(obj, list):
                for item in obj:
                    if not check_depth(item, current_depth + 1):
                        return False
            
            return True
        
        return check_depth(data)
    
    def sanitize_input(self, data: Any) -> Any:
        """
        Sanitize input data.
        
        SAFETY: Removes dangerous content while preserving structure
        VERIFY: Returns sanitized data
        """
        import html
        
        if isinstance(data, str):
            # HTML escape to prevent XSS
            sanitized = html.escape(data)
            # Remove null bytes
            sanitized = sanitized.replace('\x00', '')
            # Remove control characters
            sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
            return sanitized
        elif isinstance(data, dict):
            return {k: self.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_input(item) for item in data]
        else:
            return data
    
    def get_detected_threats(self) -> List[Dict[str, Any]]:
        """Get list of detected threats."""
        return self.detected_threats.copy()
    
    def clear_threats(self):
        """Clear detected threats list."""
        self.detected_threats.clear()


# Global validator instance
_validator: Optional[InputValidator] = None


def get_input_validator() -> InputValidator:
    """Get global input validator instance."""
    global _validator
    if _validator is None:
        _validator = InputValidator()
    return _validator

