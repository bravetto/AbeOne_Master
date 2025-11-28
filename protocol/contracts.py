"""
Protocol Contract Validation

Defines validation contracts and rules for protocol messages beyond basic
schema validation. Provides contract-level enforcement of business rules,
routing constraints, and message integrity requirements.

This module ensures messages meet all contract requirements before processing,
preventing invalid or malformed messages from entering the system.

Example:
    >>> from protocol.schema import ProtocolMessage
    >>> from protocol.contracts import ProtocolContracts
    >>> 
    >>> msg = ProtocolMessage(intent="test", payload={"key": "value"})
    >>> ProtocolContracts.validate(msg)  # Raises if invalid
    >>> normalized = ProtocolContracts.normalize(msg)
"""

from typing import Dict, Any, List, Optional, Set
from enum import Enum

from .schema import ProtocolMessage, MessageType, MessagePriority


class ContractViolationError(Exception):
    """
    Raised when a protocol message violates contract requirements.
    
    This exception is raised for contract-level violations that go beyond
    basic schema validation, such as business rule violations or routing
    constraint violations.
    """
    pass


class RoutingConstraint(str, Enum):
    """Routing constraint types."""
    EXPLICIT = "explicit"  # Must have target
    CAPABILITY = "capability"  # Must have capability hint
    BROADCAST = "broadcast"  # No target required
    SELECTIVE = "selective"  # Target or capability required


class ProtocolContracts:
    """
    Protocol contract validation and enforcement.
    
    Defines and enforces contract-level validation rules for protocol messages.
    Contracts go beyond schema validation to enforce business rules, routing
    constraints, and message integrity requirements.
    
    Contract Rules:
    1. Required fields must be present and non-empty
    2. Routing constraints must be satisfied
    3. Message type-specific rules must be followed
    4. Payload structure must match intent requirements
    5. Correlation IDs must be valid for request/response pairs
    
    Example:
        >>> msg = ProtocolMessage(intent="test", payload={})
        >>> ProtocolContracts.validate(msg)  # Validates contract rules
    """
    
    # Required fields for all messages
    REQUIRED_FIELDS: Set[str] = {"intent", "payload"}
    
    # Fields required for request messages
    REQUEST_REQUIRED_FIELDS: Set[str] = {"intent", "payload"}
    
    # Fields required for response messages
    RESPONSE_REQUIRED_FIELDS: Set[str] = {"intent", "payload", "correlation_id"}
    
    # Fields required for error messages
    ERROR_REQUIRED_FIELDS: Set[str] = {"intent", "payload"}
    
    # Maximum payload size (10MB)
    MAX_PAYLOAD_SIZE: int = 10 * 1024 * 1024
    
    # Maximum trace length
    MAX_TRACE_LENGTH: int = 100
    
    # Maximum intent length
    MAX_INTENT_LENGTH: int = 255
    
    @staticmethod
    def validate(msg: ProtocolMessage) -> None:
        """
        Validate message against all contract rules.
        
        Performs comprehensive contract validation including:
        - Required field validation
        - Message type-specific rules
        - Routing constraint validation
        - Payload size validation
        - Trace length validation
        
        Args:
            msg: ProtocolMessage instance to validate
            
        Raises:
            ContractViolationError: If message violates contract rules
            TypeError: If msg is not a ProtocolMessage instance
            
        Example:
            >>> msg = ProtocolMessage(intent="test", payload={})
            >>> ProtocolContracts.validate(msg)  # No exception if valid
        """
        # Type check
        if not isinstance(msg, ProtocolMessage):
            raise TypeError(
                f"Expected ProtocolMessage instance, got {type(msg).__name__}"
            )
        
        # Validate required fields
        ProtocolContracts._validate_required_fields(msg)
        
        # Validate field constraints
        ProtocolContracts._validate_field_constraints(msg)
        
        # Validate message type-specific rules
        ProtocolContracts._validate_type_specific_rules(msg)
        
        # Validate routing constraints
        ProtocolContracts._validate_routing_constraints(msg)
        
        # Validate payload constraints
        ProtocolContracts._validate_payload_constraints(msg)
    
    @staticmethod
    def _validate_required_fields(msg: ProtocolMessage) -> None:
        """
        Validate required fields are present and non-empty.
        
        Args:
            msg: Message to validate
            
        Raises:
            ContractViolationError: If required fields are missing or empty
        """
        missing_fields = []
        
        # Check base required fields
        for field_name in ProtocolContracts.REQUIRED_FIELDS:
            value = getattr(msg, field_name, None)
            
            if value is None:
                missing_fields.append(f"{field_name} (None)")
                continue
            
            if field_name == "intent":
                if not isinstance(value, str) or not value.strip():
                    missing_fields.append(f"{field_name} (empty or not string)")
            
            elif field_name == "payload":
                if not isinstance(value, dict):
                    missing_fields.append(f"{field_name} (not a dict)")
                # Empty payload is allowed for all message types (may contain metadata elsewhere)
        
        # Check type-specific required fields
        if msg.type == MessageType.RESPONSE:
            if not msg.correlation_id:
                missing_fields.append("correlation_id (required for response)")
        
        if missing_fields:
            raise ContractViolationError(
                f"Missing or invalid required fields: {missing_fields}"
            )
    
    @staticmethod
    def _validate_field_constraints(msg: ProtocolMessage) -> None:
        """
        Validate field value constraints (length, format, etc.).
        
        Args:
            msg: Message to validate
            
        Raises:
            ContractViolationError: If field constraints are violated
        """
        # Validate intent length
        if len(msg.intent) > ProtocolContracts.MAX_INTENT_LENGTH:
            raise ContractViolationError(
                f"intent exceeds maximum length of {ProtocolContracts.MAX_INTENT_LENGTH} "
                f"characters: {len(msg.intent)}"
            )
        
        # Validate trace length
        if len(msg.trace) > ProtocolContracts.MAX_TRACE_LENGTH:
            raise ContractViolationError(
                f"trace exceeds maximum length of {ProtocolContracts.MAX_TRACE_LENGTH} "
                f"entries: {len(msg.trace)}"
            )
        
        # Validate source/target format (if provided)
        for field_name in ['source', 'target']:
            value = getattr(msg, field_name, None)
            if value is not None:
                if not isinstance(value, str) or not value.strip():
                    raise ContractViolationError(
                        f"{field_name} must be non-empty string if provided"
                    )
                
                # Basic identifier format validation (alphanumeric, dash, underscore)
                import re
                if not re.match(r'^[a-zA-Z0-9_-]+$', value):
                    raise ContractViolationError(
                        f"{field_name} contains invalid characters. "
                        "Allowed: alphanumeric, dash, underscore"
                    )
        
        # Validate correlation_id format (if provided)
        if msg.correlation_id is not None:
            if not isinstance(msg.correlation_id, str) or not msg.correlation_id.strip():
                raise ContractViolationError(
                    "correlation_id must be non-empty string if provided"
                )
            
            # UUID format validation
            import uuid
            try:
                uuid.UUID(msg.correlation_id)
            except ValueError:
                raise ContractViolationError(
                    f"correlation_id must be valid UUID format: {msg.correlation_id}"
                )
    
    @staticmethod
    def _validate_type_specific_rules(msg: ProtocolMessage) -> None:
        """
        Validate message type-specific business rules.
        
        Args:
            msg: Message to validate
            
        Raises:
            ContractViolationError: If type-specific rules are violated
        """
        if msg.type == MessageType.RESPONSE:
            # Response messages must have correlation_id
            if not msg.correlation_id:
                raise ContractViolationError(
                    "Response messages must include correlation_id"
                )
            
            # Response messages should not have empty payloads (unless error)
            if not msg.payload and msg.priority != MessagePriority.CRITICAL:
                raise ContractViolationError(
                    "Response messages must include non-empty payload"
                )
        
        elif msg.type == MessageType.ERROR:
            # Error messages should have error information in payload
            if 'error' not in msg.payload and 'message' not in msg.payload:
                raise ContractViolationError(
                    "Error messages must include 'error' or 'message' in payload"
                )
        
        elif msg.type == MessageType.EVENT:
            # Event messages should have topic or target
            if not msg.target and 'topic' not in msg.payload:
                raise ContractViolationError(
                    "Event messages must include 'target' or 'topic' in payload"
                )
    
    @staticmethod
    def _validate_routing_constraints(msg: ProtocolMessage) -> None:
        """
        Validate routing constraint rules.
        
        Ensures routing fields are consistent and valid for the message type.
        
        Args:
            msg: Message to validate
            
        Raises:
            ContractViolationError: If routing constraints are violated
        """
        # Request messages should have either target or be broadcast
        if msg.type == MessageType.REQUEST:
            # Target is optional for requests (can be broadcast)
            # But if provided, must be valid
            pass
        
        # Response messages must have source (implicit from correlation)
        # This is handled by correlation_id validation
        
        # Event messages should have target or topic
        if msg.type == MessageType.EVENT:
            if not msg.target and 'topic' not in msg.payload:
                raise ContractViolationError(
                    "Event messages require either 'target' or 'topic' in payload"
                )
    
    @staticmethod
    def _validate_payload_constraints(msg: ProtocolMessage) -> None:
        """
        Validate payload size and structure constraints.
        
        Args:
            msg: Message to validate
            
        Raises:
            ContractViolationError: If payload constraints are violated
        """
        import json
        
        # Check payload size
        try:
            payload_json = json.dumps(msg.payload)
            payload_size = len(payload_json.encode('utf-8'))
            
            if payload_size > ProtocolContracts.MAX_PAYLOAD_SIZE:
                raise ContractViolationError(
                    f"Payload size ({payload_size} bytes) exceeds maximum "
                    f"({ProtocolContracts.MAX_PAYLOAD_SIZE} bytes)"
                )
        except (TypeError, ValueError) as e:
            raise ContractViolationError(
                f"Payload size validation failed: {e}"
            )
        
        # Validate payload depth (prevent deeply nested structures)
        max_depth = ProtocolContracts._get_payload_depth(msg.payload)
        if max_depth > 10:
            raise ContractViolationError(
                f"Payload nesting depth ({max_depth}) exceeds maximum (10 levels)"
            )
    
    @staticmethod
    def _get_payload_depth(obj: Any, current_depth: int = 0) -> int:
        """
        Calculate maximum nesting depth of payload structure.
        
        Args:
            obj: Object to analyze
            current_depth: Current recursion depth
            
        Returns:
            Maximum nesting depth
        """
        if current_depth > 10:
            return current_depth
        
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(
                ProtocolContracts._get_payload_depth(v, current_depth + 1)
                for v in obj.values()
            )
        elif isinstance(obj, list):
            if not obj:
                return current_depth
            return max(
                ProtocolContracts._get_payload_depth(item, current_depth + 1)
                for item in obj
            )
        else:
            return current_depth
    
    @staticmethod
    def normalize(msg: ProtocolMessage) -> Dict[str, Any]:
        """
        Normalize message to clean dictionary representation.
        
        Creates a normalized dictionary representation of the message,
        excluding None values and internal fields, suitable for logging
        or external transmission.
        
        Args:
            msg: ProtocolMessage instance to normalize
            
        Returns:
            Normalized dictionary representation
            
        Example:
            >>> msg = ProtocolMessage(intent="test", payload={})
            >>> normalized = ProtocolContracts.normalize(msg)
            >>> assert "intent" in normalized
            >>> assert "_trace_lock" not in normalized
        """
        # Get base dictionary
        normalized = msg.to_dict()
        
        # Remove None values for cleaner output (optional)
        # Keep them for protocol compatibility
        cleaned = {}
        for key, value in normalized.items():
            # Keep all fields for protocol compatibility
            # Only exclude internal fields
            if not key.startswith('_'):
                cleaned[key] = value
        
        return cleaned
    
    @staticmethod
    def validate_routing(msg: ProtocolMessage, constraint: RoutingConstraint) -> None:
        """
        Validate message against specific routing constraint.
        
        Args:
            msg: Message to validate
            constraint: Routing constraint to enforce
            
        Raises:
            ContractViolationError: If routing constraint is violated
            
        Example:
            >>> msg = ProtocolMessage(intent="test", payload={}, target="service-1")
            >>> ProtocolContracts.validate_routing(msg, RoutingConstraint.EXPLICIT)
        """
        if constraint == RoutingConstraint.EXPLICIT:
            if not msg.target:
                raise ContractViolationError(
                    "Message requires explicit target for routing"
                )
        
        elif constraint == RoutingConstraint.CAPABILITY:
            if 'capability' not in msg.payload and 'capability' not in msg.metadata:
                raise ContractViolationError(
                    "Message requires capability hint for routing"
                )
        
        elif constraint == RoutingConstraint.SELECTIVE:
            if not msg.target and 'capability' not in msg.payload:
                raise ContractViolationError(
                    "Message requires either target or capability for selective routing"
                )
        
        # BROADCAST constraint allows any routing configuration
    
    @staticmethod
    def get_required_fields_for_type(msg_type: MessageType) -> Set[str]:
        """
        Get required fields for a specific message type.
        
        Args:
            msg_type: Message type to get requirements for
            
        Returns:
            Set of required field names
            
        Example:
            >>> required = ProtocolContracts.get_required_fields_for_type(MessageType.RESPONSE)
            >>> assert "correlation_id" in required
        """
        base_fields = ProtocolContracts.REQUIRED_FIELDS.copy()
        
        if msg_type == MessageType.RESPONSE:
            base_fields.update(ProtocolContracts.RESPONSE_REQUIRED_FIELDS)
        elif msg_type == MessageType.ERROR:
            base_fields.update(ProtocolContracts.ERROR_REQUIRED_FIELDS)
        elif msg_type == MessageType.REQUEST:
            base_fields.update(ProtocolContracts.REQUEST_REQUIRED_FIELDS)
        
        return base_fields

