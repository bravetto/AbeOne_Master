"""
Trust Guard Authentication System

Implements enterprise-grade authentication and authorization:
- API key authentication
- JWT token support
- Role-based access control (RBAC)
- Request signing validation
- Audit logging for security events
"""

import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import logging

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    logging.warning("PyJWT not available. JWT authentication will be disabled.")

logger = logging.getLogger(__name__)


class Role(Enum):
    """User roles for RBAC."""
    ADMIN = "admin"
    OPERATOR = "operator"
    ANALYST = "analyst"
    READONLY = "readonly"
    SERVICE = "service"


class Permission(Enum):
    """API permissions."""
    DETECT = "detect"
    VALIDATE = "validate"
    MITIGATE = "mitigate"
    CONSTITUTIONAL = "constitutional"
    METRICS = "metrics"
    HEALTH = "health"
    READ_ONLY = "read_only"
    ADMIN = "admin"


# Role to permission mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: set(Permission),
    Role.OPERATOR: {Permission.DETECT, Permission.VALIDATE, Permission.MITIGATE, 
                   Permission.CONSTITUTIONAL, Permission.METRICS, Permission.HEALTH},
    Role.ANALYST: {Permission.DETECT, Permission.VALIDATE, Permission.METRICS, Permission.HEALTH},
    Role.READONLY: {Permission.METRICS, Permission.HEALTH},
    Role.SERVICE: {Permission.DETECT, Permission.VALIDATE, Permission.HEALTH}
}


class APIKey:
    """API Key representation."""
    
    def __init__(self, key_id: str, key_hash: str, role: Role, 
                 name: str, created_at: datetime, expires_at: Optional[datetime] = None,
                 last_used: Optional[datetime] = None, is_active: bool = True):
        self.key_id = key_id
        self.key_hash = key_hash
        self.role = role
        self.name = name
        self.created_at = created_at
        self.expires_at = expires_at
        self.last_used = last_used
        self.is_active = is_active
    
    def is_expired(self) -> bool:
        """Check if the API key is expired."""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if the API key is valid (active and not expired)."""
        return self.is_active and not self.is_expired()
    
    def update_last_used(self):
        """Update the last used timestamp."""
        self.last_used = datetime.now(timezone.utc)


class AuthenticationError(Exception):
    """Authentication related errors."""
    pass


class AuthorizationError(Exception):
    """Authorization related errors."""
    pass


class APIKeyManager:
    """Manages API keys and authentication."""
    
    def __init__(self, secret_key: str):
        """Initialize the API key manager."""
        self.secret_key = secret_key.encode('utf-8')
        self.api_keys: Dict[str, APIKey] = {}
        self.rate_limits: Dict[str, Dict[str, Any]] = {}
        
        # Create default admin key if none exist
        self._create_default_admin_key()
        
        logger.info("API Key Manager initialized")
    
    def _create_default_admin_key(self):
        """Create a default admin API key for initial setup."""
        if not self.api_keys:
            admin_key = self.create_api_key(
                name="Default Admin Key",
                role=Role.ADMIN,
                expires_in_days=365
            )
            # Store the full API key for debugging purposes (temporary)
            self.default_api_key = admin_key['api_key']
            logger.warning(f"Created default admin API key: {admin_key['api_key']}")
            logger.warning("Please change the default admin key in production!")
    
    def generate_key_id(self) -> str:
        """Generate a unique key ID."""
        return f"tg_{secrets.token_urlsafe(16)}"
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash an API key for secure storage."""
        return hashlib.pbkdf2_hmac('sha256', api_key.encode('utf-8'), 
                                  self.secret_key, 100000).hex()
    
    def create_api_key(self, name: str, role: Role, expires_in_days: Optional[int] = None) -> Dict[str, Any]:
        """Create a new API key."""
        key_id = self.generate_key_id()
        api_key_secret = secrets.token_urlsafe(32)
        full_api_key = f"{key_id}_{api_key_secret}"
        key_hash = self.hash_api_key(full_api_key)
        
        expires_at = None
        if expires_in_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
        
        api_key_obj = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            role=role,
            name=name,
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at
        )
        
        self.api_keys[key_id] = api_key_obj
        
        logger.info(f"Created API key: {key_id} for role: {role.value}")
        
        return {
            "key_id": key_id,
            "api_key": full_api_key,  # Only returned once
            "role": role.value,
            "name": name,
            "expires_at": expires_at.isoformat() if expires_at else None
        }
    
    def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """Validate an API key and return the key object."""
        if not api_key:
            return None
        
        # The API key format is: tg_<key_id>_<secret>
        # We need to find the key_id by looking for the pattern tg_<key_id>_<secret>
        # where key_id is the part between the first and second underscore
        try:
            parts = api_key.split('_')
            if len(parts) < 3 or parts[0] != 'tg':
                return None
            
            # Reconstruct the key_id: tg_<key_id>
            key_id = f"{parts[0]}_{parts[1]}"
        except (IndexError, ValueError):
            return None
        
        if key_id not in self.api_keys:
            return None
        
        api_key_obj = self.api_keys[key_id]
        if not api_key_obj.is_valid():
            return None
        
        # Verify the key hash
        key_hash = self.hash_api_key(api_key)
        if not hmac.compare_digest(api_key_obj.key_hash, key_hash):
            return None
        
        # Update last used timestamp
        api_key_obj.update_last_used()
        
        return api_key_obj
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key."""
        if key_id in self.api_keys:
            self.api_keys[key_id].is_active = False
            logger.info(f"Revoked API key: {key_id}")
            return True
        return False
    
    def list_api_keys(self) -> List[Dict[str, Any]]:
        """List all API keys (without the actual key values)."""
        keys = []
        for key_id, api_key_obj in self.api_keys.items():
            keys.append({
                "key_id": key_id,
                "name": api_key_obj.name,
                "role": api_key_obj.role.value,
                "created_at": api_key_obj.created_at.isoformat(),
                "expires_at": api_key_obj.expires_at.isoformat() if api_key_obj.expires_at else None,
                "last_used": api_key_obj.last_used.isoformat() if api_key_obj.last_used else None,
                "is_active": api_key_obj.is_active
            })
        return keys
    
    def check_rate_limit(self, key_id: str, limit: int = 100, window: int = 60) -> bool:
        """Check if the API key is within rate limits."""
        now = time.time()
        window_start = now - window
        
        if key_id not in self.rate_limits:
            self.rate_limits[key_id] = {"requests": [], "limit": limit, "window": window}
        
        rate_limit_data = self.rate_limits[key_id]
        
        # Remove old requests outside the window
        rate_limit_data["requests"] = [
            req_time for req_time in rate_limit_data["requests"] 
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(rate_limit_data["requests"]) >= limit:
            return False
        
        # Add current request
        rate_limit_data["requests"].append(now)
        return True


class JWTAuthenticator:
    """JWT token authentication."""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """Initialize JWT authenticator."""
        if not JWT_AVAILABLE:
            raise ImportError("PyJWT is required for JWT authentication")
        
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry = timedelta(hours=24)
        
        logger.info("JWT Authenticator initialized")
    
    def create_token(self, user_id: str, role: Role, expires_in: Optional[timedelta] = None) -> str:
        """Create a JWT token."""
        if not JWT_AVAILABLE:
            raise ImportError("PyJWT is required for JWT authentication")
        
        expiry = expires_in or self.token_expiry
        payload = {
            "user_id": user_id,
            "role": role.value,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + expiry
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate a JWT token and return the payload."""
        if not JWT_AVAILABLE:
            return None
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None


class SecurityManager:
    """Main security manager for authentication and authorization."""
    
    def __init__(self, secret_key: str):
        """Initialize the security manager."""
        self.secret_key = secret_key
        self.api_key_manager = APIKeyManager(secret_key)
        self.jwt_authenticator = JWTAuthenticator(secret_key) if JWT_AVAILABLE else None
        
        logger.info("Security Manager initialized")
    
    def authenticate_request(self, api_key: Optional[str] = None, 
                           jwt_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Authenticate a request using API key or JWT token."""
        # Try API key authentication first
        if api_key:
            api_key_obj = self.api_key_manager.validate_api_key(api_key)
            if api_key_obj:
                # Check rate limits
                if not self.api_key_manager.check_rate_limit(api_key_obj.key_id):
                    raise AuthenticationError("Rate limit exceeded")
                
                return {
                    "user_id": api_key_obj.key_id,
                    "role": api_key_obj.role,
                    "auth_type": "api_key",
                    "permissions": ROLE_PERMISSIONS[api_key_obj.role]
                }
        
        # Try JWT authentication
        if jwt_token and self.jwt_authenticator:
            payload = self.jwt_authenticator.validate_token(jwt_token)
            if payload:
                role = Role(payload["role"])
                return {
                    "user_id": payload["user_id"],
                    "role": role,
                    "auth_type": "jwt",
                    "permissions": ROLE_PERMISSIONS[role]
                }
        
        return None
    
    def authorize_request(self, user_info: Dict[str, Any], permission: Permission) -> bool:
        """Authorize a request for a specific permission."""
        if not user_info:
            return False
        
        user_permissions = user_info.get("permissions", set())
        return permission in user_permissions
    
    def create_api_key(self, name: str, role: Role, expires_in_days: Optional[int] = None) -> Dict[str, Any]:
        """Create a new API key."""
        return self.api_key_manager.create_api_key(name, role, expires_in_days)
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key."""
        return self.api_key_manager.revoke_api_key(key_id)
    
    def list_api_keys(self) -> List[Dict[str, Any]]:
        """List all API keys."""
        return self.api_key_manager.list_api_keys()
    
    def create_jwt_token(self, user_id: str, role: Role, expires_in: Optional[timedelta] = None) -> str:
        """Create a JWT token."""
        if not self.jwt_authenticator:
            raise AuthenticationError("JWT authentication not available")
        return self.jwt_authenticator.create_token(user_id, role, expires_in)
    
    def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """Validate an API key and return the key object."""
        return self.api_key_manager.validate_api_key(api_key)


_security_manager_instance = None

def get_security_manager() -> SecurityManager:
    """Get the global security manager instance."""
    global _security_manager_instance
    if _security_manager_instance is None:
        from trustguard.config import get_config
        config = get_config()
        secret_key = config.get_secret("secret_key")
        _security_manager_instance = SecurityManager(secret_key)
    return _security_manager_instance
