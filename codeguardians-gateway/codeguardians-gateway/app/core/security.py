"""
AI Guardians Security Module

Comprehensive security validation and protection for the AI Guardians platform.
"""

import re
import html
import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, validator
import logging
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, Query
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.models import User

logger = logging.getLogger(__name__)


class SecurityThreat(BaseModel):
    """Security threat detection result."""
    threat_type: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    description: str
    pattern: str
    confidence: float


class BiasGuardPolicy(BaseModel):
    """BiasGuard policy enforcement model."""
    policy_id: str
    policy_name: str
    enforcement_type: str  # "attribute_based", "fairness_check", "compliance", "audit"
    rules: List[Dict[str, Any]]
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "policy_id": "BIAS_001",
                "policy_name": "Demographic Parity",
                "enforcement_type": "fairness_check",
                "rules": [
                    {"field": "age", "operator": "!=", "threshold": 0.1},
                    {"field": "gender", "operator": "<=", "threshold": 0.05}
                ]
            }
        }


class BiasGuardValidator:
    """
    BiasGuard integration for policy-based fairness and attribution tracking.
    
    Enforces codified bias prevention and compliance through rule-based
    authentication and authorization guardrails.
    """
    
    def __init__(self):
        """Initialize BiasGuard validator with default policies."""
        self.policies: Dict[str, BiasGuardPolicy] = {}
        self.audit_log: List[Dict[str, Any]] = []
        self.enforcement_rules = self._initialize_enforcement_rules()
        self._load_default_policies()
        
    def _initialize_enforcement_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize policy enforcement rules."""
        return {
            "fairness": [
                {
                    "rule_id": "FAIRNESS_001",
                    "name": "Equal Opportunity",
                    "description": "Ensures equal opportunity across demographic groups",
                    "metric": "demographic_parity",
                    "threshold": 0.1,
                    "enabled": True
                },
                {
                    "rule_id": "FAIRNESS_002",
                    "name": "Equalized Odds",
                    "description": "Ensures equalized false positive and negative rates",
                    "metric": "equalized_odds",
                    "threshold": 0.15,
                    "enabled": True
                }
            ],
            "attribution": [
                {
                    "rule_id": "ATTR_001",
                    "name": "Decision Attribution",
                    "description": "Tracks and logs all authorization decisions",
                    "requires_audit": True,
                    "enabled": True
                },
                {
                    "rule_id": "ATTR_002",
                    "name": "Policy Version Tracking",
                    "description": "Records which policy version was applied",
                    "requires_version": True,
                    "enabled": True
                }
            ],
            "compliance": [
                {
                    "rule_id": "COMP_001",
                    "name": "Audit Trail",
                    "description": "Maintains comprehensive audit trail for all auth operations",
                    "retention_days": 90,
                    "enabled": True
                }
            ]
        }
    
    def _load_default_policies(self) -> None:
        """Load default BiasGuard policies."""
        default_policies = [
            BiasGuardPolicy(
                policy_id="BIAS_FAIRNESS_001",
                policy_name="Equal Opportunity Policy",
                enforcement_type="fairness_check",
                rules=[
                    {"field": "demographic_groups", "metric": "parity", "threshold": 0.1},
                    {"field": "access_patterns", "metric": "disparity", "threshold": 0.05}
                ]
            ),
            BiasGuardPolicy(
                policy_id="BIAS_ATTR_001",
                policy_name="Attribution Tracking Policy",
                enforcement_type="attribute_based",
                rules=[
                    {"audit_level": "full", "track_decisions": True, "track_changes": True}
                ]
            ),
            BiasGuardPolicy(
                policy_id="BIAS_COMPLIANCE_001",
                policy_name="Compliance & Audit Policy",
                enforcement_type="compliance",
                rules=[
                    {"audit_retention": 90, "audit_format": "json", "audit_encryption": True}
                ]
            )
        ]
        
        for policy in default_policies:
            self.policies[policy.policy_id] = policy
            logger.info(f"Loaded BiasGuard policy: {policy.policy_id}")
    
    def register_policy(self, policy: BiasGuardPolicy) -> bool:
        """
        Register a new BiasGuard policy.
        
        Args:
            policy: BiasGuardPolicy to register
            
        Returns:
            bool: True if registered successfully
        """
        try:
            self.policies[policy.policy_id] = policy
            self._audit_log(
                event="policy_registered",
                policy_id=policy.policy_id,
                status="success"
            )
            logger.info(f"BiasGuard policy registered: {policy.policy_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to register BiasGuard policy: {e}")
            self._audit_log(
                event="policy_registration_failed",
                policy_id=policy.policy_id,
                error=str(e)
            )
            return False
    
    def enforce_policy(
        self,
        policy_id: str,
        user_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enforce a BiasGuard policy on user data.
        
        Args:
            policy_id: ID of policy to enforce
            user_data: User data to validate
            context: Additional context for enforcement
            
        Returns:
            Dict with enforcement result and audit information
        """
        result = {
            "enforced": False,
            "policy_id": policy_id,
            "violations": [],
            "warnings": [],
            "audit_id": self._generate_audit_id(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        if policy_id not in self.policies:
            result["violations"].append(f"Policy not found: {policy_id}")
            self._audit_log(event="policy_not_found", policy_id=policy_id)
            return result
        
        policy = self.policies[policy_id]
        
        if not policy.is_active:
            result["violations"].append(f"Policy is inactive: {policy_id}")
            return result
        
        try:
            # Apply policy rules
            for rule in policy.rules:
                violation = self._check_rule(rule, user_data, context)
                if violation:
                    result["violations"].append(violation)
            
            # Enforce based on policy type
            if policy.enforcement_type == "fairness_check":
                fairness_result = self._enforce_fairness(user_data, policy)
                result["violations"].extend(fairness_result.get("violations", []))
                result["warnings"].extend(fairness_result.get("warnings", []))
            
            elif policy.enforcement_type == "attribute_based":
                attr_result = self._enforce_attribution(user_data, policy)
                result["attribution_data"] = attr_result
            
            elif policy.enforcement_type == "compliance":
                compliance_result = self._enforce_compliance(user_data, policy)
                result["compliance_data"] = compliance_result
            
            result["enforced"] = len(result["violations"]) == 0
            
            # Log audit trail
            self._audit_log(
                event="policy_enforced",
                policy_id=policy_id,
                enforced=result["enforced"],
                violation_count=len(result["violations"])
            )
            
            logger.info(f"Policy {policy_id} enforced: {result['enforced']}")
            return result
            
        except Exception as e:
            logger.error(f"Error enforcing policy {policy_id}: {e}")
            result["violations"].append(f"Enforcement error: {str(e)}")
            result["enforced"] = False
            return result
    
    def _check_rule(
        self,
        rule: Dict[str, Any],
        user_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Check a single rule against user data.
        
        Args:
            rule: Rule to check
            user_data: User data to validate
            context: Additional context
            
        Returns:
            Violation message if rule violated, None otherwise
        """
        field = rule.get("field")
        operator = rule.get("operator", "==")
        threshold = rule.get("threshold")
        
        if not field or field not in user_data:
            return None
        
        value = user_data.get(field)
        
        # Simple rule checking
        if operator == "==" and value != threshold:
            return f"Rule violation: {field} != {threshold}"
        elif operator == "!=" and value == threshold:
            return f"Rule violation: {field} == {threshold}"
        elif operator == "<" and not (value < threshold):
            return f"Rule violation: {field} >= {threshold}"
        elif operator == ">" and not (value > threshold):
            return f"Rule violation: {field} <= {threshold}"
        elif operator == "<=" and not (value <= threshold):
            return f"Rule violation: {field} > {threshold}"
        elif operator == ">=" and not (value >= threshold):
            return f"Rule violation: {field} < {threshold}"
        
        return None
    
    def _enforce_fairness(
        self,
        user_data: Dict[str, Any],
        policy: BiasGuardPolicy
    ) -> Dict[str, Any]:
        """
        Enforce fairness policy rules.
        
        Args:
            user_data: User data to validate
            policy: Policy to enforce
            
        Returns:
            Dict with fairness enforcement results
        """
        result = {"violations": [], "warnings": [], "fairness_metrics": {}}
        
        # Check for demographic parity
        if "demographic_groups" in user_data:
            metrics = self._calculate_demographic_parity(user_data)
            result["fairness_metrics"]["demographic_parity"] = metrics
            
            if metrics.get("disparity", 0) > 0.1:
                result["warnings"].append(
                    f"Demographic parity disparity: {metrics['disparity']:.2%}"
                )
        
        logger.debug(f"Fairness enforcement result: {result}")
        return result
    
    def _enforce_attribution(
        self,
        user_data: Dict[str, Any],
        policy: BiasGuardPolicy
    ) -> Dict[str, Any]:
        """
        Enforce attribution tracking policy.
        
        Args:
            user_data: User data to track
            policy: Policy to enforce
            
        Returns:
            Dict with attribution tracking data
        """
        attribution_data = {
            "user_id": user_data.get("id"),
            "email": user_data.get("email"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "policy_id": policy.policy_id,
            "tracked_fields": list(user_data.keys())
        }
        
        self._audit_log(
            event="attribution_tracked",
            **attribution_data
        )
        
        logger.debug(f"Attribution tracked: {user_data.get('id')}")
        return attribution_data
    
    def _enforce_compliance(
        self,
        user_data: Dict[str, Any],
        policy: BiasGuardPolicy
    ) -> Dict[str, Any]:
        """
        Enforce compliance policy rules.
        
        Args:
            user_data: User data to validate
            policy: Policy to enforce
            
        Returns:
            Dict with compliance enforcement data
        """
        compliance_data = {
            "compliance_check_id": self._generate_audit_id(),
            "user_id": user_data.get("id"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "compliance_status": "verified",
            "audit_trail_created": True
        }
        
        self._audit_log(
            event="compliance_check",
            **compliance_data
        )
        
        logger.debug(f"Compliance check completed: {compliance_data['compliance_check_id']}")
        return compliance_data
    
    def _calculate_demographic_parity(
        self,
        user_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Calculate demographic parity metrics.
        
        Args:
            user_data: User data to analyze
            
        Returns:
            Dict with demographic parity metrics
        """
        metrics = {
            "groups_identified": 0,
            "parity_score": 0.0,
            "disparity": 0.0
        }
        
        # Placeholder for actual demographic parity calculation
        # In production, this would use statistical methods
        demographic_fields = ["age", "gender", "race", "ethnicity"]
        identified_groups = sum(1 for field in demographic_fields if field in user_data)
        
        metrics["groups_identified"] = identified_groups
        metrics["parity_score"] = 1.0 - (identified_groups * 0.05)
        metrics["disparity"] = 1.0 - metrics["parity_score"]
        
        return metrics
    
    def _audit_log(self, **kwargs) -> None:
        """
        Create an audit log entry.
        
        Args:
            **kwargs: Audit data to log
        """
        log_entry = {
            **kwargs,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "audit_id": self._generate_audit_id()
        }
        self.audit_log.append(log_entry)
        logger.debug(f"Audit log: {log_entry}")
    
    @staticmethod
    def _generate_audit_id() -> str:
        """Generate unique audit ID."""
        import uuid
        return f"AUD-{uuid.uuid4().hex[:12].upper()}"


# Global BiasGuard validator instance
_biasguard_validator: Optional[BiasGuardValidator] = None


def get_biasguard_validator() -> BiasGuardValidator:
    """
    Get or create global BiasGuard validator instance.
    
    Returns:
        BiasGuardValidator: Global validator instance
    """
    global _biasguard_validator
    if _biasguard_validator is None:
        _biasguard_validator = BiasGuardValidator()
        logger.info("BiasGuard validator initialized")
    return _biasguard_validator


class SecurityValidator:
    """Comprehensive security validation for AI Guardians."""
    
    def __init__(self):
        """Initialize security validator with threat patterns."""
        self.threat_patterns = self._initialize_threat_patterns()
        self.rate_limits = {}
        
    def _initialize_threat_patterns(self) -> Dict[str, List[str]]:
        """Initialize comprehensive threat detection patterns."""
        return {
            "sql_injection": [
                r"';?\s*DROP\s+TABLE",
                r"UNION\s+SELECT",
                r"OR\s+1\s*=\s*1",
                r"AND\s+1\s*=\s*1",
                r"';?\s*INSERT\s+INTO",
                r"';?\s*UPDATE\s+",
                r"';?\s*DELETE\s+FROM",
                r"';?\s*EXEC\s*\(",
                r"';?\s*EXECUTE\s*\(",
                r"';?\s*ALTER\s+TABLE",
                r"';?\s*CREATE\s+TABLE",
                r"';?\s*TRUNCATE\s+TABLE"
            ],
            "xss": [
                r"<script[^>]*>",
                r"javascript:",
                r"onload\s*=",
                r"onerror\s*=",
                r"onclick\s*=",
                r"onmouseover\s*=",
                r"alert\s*\(",
                r"document\.cookie",
                r"window\.location",
                r"eval\s*\(",
                r"exec\s*\(",
                r"<iframe[^>]*>",
                r"<object[^>]*>",
                r"<embed[^>]*>",
                r"<form[^>]*>"
            ],
            "path_traversal": [
                r"\.\./",
                r"\.\.\\",
                r"/etc/passwd",
                r"C:\\Windows\\System32",
                r"/proc/self/environ",
                r"file://",
                r"ftp://",
                r"gopher://",
                r"data:",
                r"javascript:"
            ],
            "command_injection": [
                r"[|&;`$]",
                r"system\s*\(",
                r"shell_exec\s*\(",
                r"passthru\s*\(",
                r"exec\s*\(",
                r"popen\s*\(",
                r"proc_open\s*\(",
                r"cmd\s*/",
                r"powershell\s*",
                r"bash\s*-"
            ],
            "ldap_injection": [
                r"\)\s*\(\s*&",
                r"\)\s*\(\s*\|",
                r"\)\s*\(\s*!",
                r"\*\)\s*\(\s*uid\s*=\s*\*",
                r"admin\*",
                r"\)\s*\(\s*objectClass\s*=\s*\*"
            ],
            "xml_injection": [
                r"<!DOCTYPE",
                r"<!ENTITY",
                r"SYSTEM\s+",
                r"file://",
                r"http://",
                r"ftp://",
                r"<!\[CDATA\[",
                r"\]\]>"
            ],
            "no_sql_injection": [
                r"\$where",
                r"\$ne\s*:",
                r"\$gt\s*:",
                r"\$lt\s*:",
                r"\$regex",
                r"\$exists",
                r"__proto__",
                r"constructor"
            ],
            "prototype_pollution": [
                r"__proto__",
                r"constructor",
                r"prototype",
                r"\.__proto__",
                r"\.constructor",
                r"\.prototype"
            ],
            "template_injection": [
                r"\{\{.*\}\}",
                r"\{%.*%\}",
                r"#\{.*\}",
                r"\$\{.*\}",
                r"<%.*%>",
                r"\{\{.*\|\s*.*\}\}"
            ]
        }
    
    async def validate_input(self, data: Any, input_type: str = "general") -> List[SecurityThreat]:
        """
        Validate input data for security threats.
        
        Args:
            data: Input data to validate
            input_type: Type of input (json, text, url, etc.)
            
        Returns:
            List of detected security threats
        """
        threats = []
        
        if isinstance(data, str):
            threats.extend(await self._validate_string(data, input_type))
        elif isinstance(data, dict):
            threats.extend(await self._validate_dict(data, input_type))
        elif isinstance(data, list):
            for item in data:
                threats.extend(await self.validate_input(item, input_type))
        
        return threats
    
    async def _validate_string(self, text: str, input_type: str) -> List[SecurityThreat]:
        """Validate string input for threats."""
        threats = []
        text_lower = text.lower()
        
        for threat_type, patterns in self.threat_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    threat = SecurityThreat(
                        threat_type=threat_type,
                        severity=self._get_threat_severity(threat_type),
                        description=f"{threat_type.replace('_', ' ').title()} pattern detected",
                        pattern=pattern,
                        confidence=0.8
                    )
                    threats.append(threat)
                    logger.warning(f"Security threat detected: {threat_type} - {pattern}")
        
        return threats
    
    async def _validate_dict(self, data: Dict[str, Any], input_type: str) -> List[SecurityThreat]:
        """Validate dictionary input for threats."""
        threats = []
        
        for key, value in data.items():
            # Validate key
            threats.extend(await self._validate_string(str(key), input_type))
            
            # Validate value
            threats.extend(await self.validate_input(value, input_type))
        
        return threats
    
    def _get_threat_severity(self, threat_type: str) -> str:
        """Get severity level for threat type."""
        severity_map = {
            "sql_injection": "HIGH",
            "command_injection": "CRITICAL",
            "path_traversal": "HIGH",
            "xss": "MEDIUM",
            "ldap_injection": "HIGH",
            "xml_injection": "HIGH",
            "no_sql_injection": "MEDIUM",
            "prototype_pollution": "HIGH",
            "template_injection": "MEDIUM"
        }
        return severity_map.get(threat_type, "LOW")
    
    async def sanitize_input(self, data: Any) -> Any:
        """Sanitize input data to remove potential threats."""
        if isinstance(data, str):
            # HTML escape
            data = html.escape(data)
            # Remove null bytes
            data = data.replace('\x00', '')
            # Remove control characters
            data = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', data)
        elif isinstance(data, dict):
            return {k: await self.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [await self.sanitize_input(item) for item in data]
        
        return data
    
    async def check_rate_limit(self, identifier: str, limit: int = 100, window: int = 3600) -> bool:
        """Check if request is within rate limit."""
        import time
        current_time = time.time()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Clean old entries
        self.rate_limits[identifier] = [
            timestamp for timestamp in self.rate_limits[identifier]
            if current_time - timestamp < window
        ]
        
        # Check limit
        if len(self.rate_limits[identifier]) >= limit:
            return False
        
        # Add current request
        self.rate_limits[identifier].append(current_time)
        return True
    
    async def validate_json_input(self, json_data: Union[str, dict]) -> Dict[str, Any]:
        """Validate and sanitize JSON input."""
        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format")
        
        # Validate structure
        if not isinstance(json_data, dict):
            raise ValueError("JSON data must be an object")
        
        # Check for dangerous keys
        dangerous_keys = ['__proto__', 'constructor', 'prototype']
        for key in json_data.keys():
            if key in dangerous_keys:
                raise ValueError(f"Dangerous key detected: {key}")
        
        # Sanitize data
        sanitized_data = await self.sanitize_input(json_data)
        
        return sanitized_data


class SecurityMiddleware:
    """Security middleware for request validation."""
    
    def __init__(self):
        self.validator = SecurityValidator()
    
    async def validate_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate incoming request for security threats."""
        # Check for threats
        threats = await self.validator.validate_input(request_data)
        
        if threats:
            high_severity_threats = [t for t in threats if t.severity in ["HIGH", "CRITICAL"]]
            if high_severity_threats:
                raise SecurityError("High severity security threat detected", threats)
        
        # Sanitize input
        sanitized_data = await self.validator.sanitize_input(request_data)
        
        return sanitized_data


class SecurityError(Exception):
    """Security validation error."""
    
    def __init__(self, message: str, threats: List[SecurityThreat] = None):
        super().__init__(message)
        self.threats = threats or []


# Password hashing context
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    from app.core.config import get_settings
    settings = get_settings()
    secret_key = getattr(settings, 'JWT_SECRET_KEY', 'secret')
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token."""
    from app.core.config import get_settings
    settings = get_settings()
    secret_key = getattr(settings, 'JWT_SECRET_KEY', 'secret')
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token."""
    try:
        from app.core.config import get_settings
        settings = get_settings()
        secret_key = getattr(settings, 'JWT_SECRET_KEY', 'secret')
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(HTTPBearer())) -> Optional[dict]:
    """Get current user from JWT token."""
    try:
        payload = verify_token(token.credentials)
        if payload is None:
            return None
        return payload
    except Exception:
        return None


def get_optional_current_user(token: Optional[str] = Depends(HTTPBearer(auto_error=False))) -> Optional[dict]:
    """Get current user from JWT token, returns None if no token provided."""
    if token is None:
        return None
    try:
        payload = verify_token(token.credentials)
        if payload is None:
            return None
        return payload
    except Exception:
        return None




async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    """Get user by ID from database."""
    from sqlalchemy import select
    from app.core.models import User
    from app.core.exceptions import NotFoundError

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise NotFoundError(f"User with ID {user_id} not found")

    return user


async def get_current_user_from_db(token: Optional[str] = Depends(HTTPBearer(auto_error=False)), db: AsyncSession = Depends(get_db)) -> Optional[User]:
    """Get current user as User object from database, returns None on authentication failure."""
    try:
        if token is None:
            logger.warning("No authorization token provided")
            return None

        payload = verify_token(token.credentials)
        logger.info(f"Token payload: {payload}")
        if payload is None:
            logger.warning("Token verification failed")
            return None

        # Get user ID from payload
        user_id = payload.get("user_id")
        logger.info(f"User ID from token: {user_id}")
        if not user_id:
            logger.warning("No user_id in token payload")
            return None

        from sqlalchemy import select
        from app.core.models import User

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        logger.info(f"Found user: {user}")

        return user
    except Exception as e:
        logger.error(f"Error getting current user from database: {e}")
        return None


async def get_current_superuser(current_user: Optional[User] = Depends(get_current_user_from_db)) -> User:
    """Get current superuser from database."""
    if current_user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Authentication required")

    if not current_user.is_superuser:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Superuser access required")

    return current_user


async def get_optional_current_user_from_db(token: Optional[str] = Depends(HTTPBearer(auto_error=False)), db: AsyncSession = Depends(get_db)) -> Optional[User]:
    """Get current user as User object from database, returns None if no token provided."""
    if token is None:
        return None
    try:
        payload = verify_token(token.credentials)
        if payload is None:
            return None

        # Get user ID from payload
        user_id = payload.get("user_id")
        if not user_id:
            return None

        from sqlalchemy import select
        from app.core.models import User

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return user
    except Exception as e:
        logger.error(f"Error getting optional current user from database: {e}")
        return None


def get_pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
) -> dict:
    """Get pagination parameters."""
    return {
        "skip": skip,
        "limit": limit
    }

def verify_api_key(api_key: str) -> bool:
    """Verify API key."""
    # For development, accept any non-empty API key
    # In production, this would check against a database or environment variable
    return api_key and len(api_key) > 10

def generate_password_reset_token(email: str) -> str:
    """Generate password reset token for email"""
    payload = {"email": email, "type": "password_reset", "exp": datetime.now(timezone.utc) + timedelta(hours=1)}
    return jwt.encode(payload, "secret", algorithm="HS256")

def verify_password_reset_token(token: str) -> str:
    """Verify password reset token and return email"""
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        if payload.get("type") == "password_reset":
            return payload.get("email")
    except JWTError:
        pass
    raise ValueError("Invalid or expired reset token")

def generate_email_verification_token(email: str) -> str:
    """Generate email verification token"""
    from app.core.config import get_settings
    settings = get_settings()
    secret_key = getattr(settings, 'JWT_SECRET_KEY', 'secret')
    payload = {"email": email, "type": "email_verification", "exp": datetime.now(timezone.utc) + timedelta(days=7)}
    return jwt.encode(payload, secret_key, algorithm="HS256")

def verify_email_verification_token(token: str) -> str:
    """Verify email verification token and return email"""
    try:
        from app.core.config import get_settings
        settings = get_settings()
        secret_key = getattr(settings, 'JWT_SECRET_KEY', 'secret')
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        if payload.get("type") == "email_verification":
            return payload.get("email")
    except JWTError:
        pass
    raise ValueError("Invalid or expired verification token")

def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """Validate password strength and return (is_valid, errors)"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit")
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, errors

# Global security validator instance
security_validator = SecurityValidator()
security_middleware = SecurityMiddleware()