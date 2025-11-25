"""
Protocol Schema Definitions

Defines core data structures and schemas for protocol messages with strict
validation, type checking, and serialization support. All schemas are designed
for network transmission and must be JSON-serializable.

This module provides:
- Base message schema with validation
- Type-safe field definitions
- Serialization/deserialization utilities
- Schema versioning support

Example:
    >>> from protocol.schema import ProtocolMessage
    >>> msg = ProtocolMessage(
    ...     intent="test",
    ...     payload={"key": "value"}
    ... )
    >>> json_str = msg.to_json()
    >>> restored = ProtocolMessage.from_json(json_str)
"""

import json
import time
import uuid
import threading
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """Message type enumeration."""
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    NOTIFICATION = "notification"
    ERROR = "error"


class MessagePriority(str, Enum):
    """Message priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


# Protocol version constant
PROTOCOL_VERSION = "1.0.0"


@dataclass
class ProtocolMessage:
    """
    Core protocol message schema with validation and serialization.
    
    This is the base message structure for all protocol communications.
    All fields are validated on creation and messages can be serialized
    to/from JSON for network transmission.
    
    Attributes:
        id: Unique message identifier (UUID)
        version: Protocol version (default: PROTOCOL_VERSION)
        type: Message type (default: REQUEST)
        priority: Message priority (default: NORMAL)
        intent: Intent or action identifier (required)
        payload: Message payload data (required, must be JSON-serializable)
        metadata: Optional metadata dictionary
        timestamp: Message creation timestamp (Unix timestamp)
        trace: List of processing nodes this message has passed through
        correlation_id: Optional correlation ID for request/response pairing
        source: Optional source identifier
        target: Optional target identifier
    
    Raises:
        ValueError: If required fields are missing or invalid
        TypeError: If field types are incorrect
        
    Example:
        >>> msg = ProtocolMessage(
        ...     intent="process_data",
        ...     payload={"data": "example"}
        ... )
        >>> assert msg.validate()[0] == True
        >>> json_data = msg.to_json()
    """
    
    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    version: str = PROTOCOL_VERSION
    
    # Message classification
    type: MessageType = MessageType.REQUEST
    priority: MessagePriority = MessagePriority.NORMAL
    
    # Semantic fields
    intent: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    
    # Routing fields
    source: Optional[str] = None
    target: Optional[str] = None
    correlation_id: Optional[str] = None
    semantic_vector: Optional[List[float]] = None  # For semantic routing
    capability: Optional[str] = None  # For capability-based routing
    topic: Optional[str] = None  # For event-based routing
    
    # Temporal fields
    timestamp: float = field(default_factory=time.time)
    
    # Processing trace
    trace: List[str] = field(default_factory=list)
    
    # Thread-safe trace modification
    _trace_lock: threading.Lock = field(
        default_factory=threading.Lock,
        init=False,
        repr=False
    )
    
    def __post_init__(self) -> None:
        """
        Post-initialization validation and normalization.
        
        Validates message structure and normalizes fields after creation.
        Raises exceptions if validation fails.
        
        Raises:
            ValueError: If message structure is invalid
        """
        # Validate ID format (UUID)
        if not isinstance(self.id, str) or len(self.id) != 36:
            try:
                uuid.UUID(self.id)
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid message ID format: {self.id}")
        
        # Validate version
        if self.version != PROTOCOL_VERSION:
            raise ValueError(
                f"Protocol version mismatch: expected {PROTOCOL_VERSION}, "
                f"got {self.version}"
            )
        
        # Validate intent is non-empty
        if not isinstance(self.intent, str) or not self.intent.strip():
            raise ValueError("intent must be a non-empty string")
        
        # Normalize intent
        self.intent = self.intent.strip()
        
        # Validate payload is a dictionary
        if not isinstance(self.payload, dict):
            raise TypeError(f"payload must be a dict, got {type(self.payload).__name__}")
        
        # Validate payload is JSON-serializable
        try:
            json.dumps(self.payload)
        except (TypeError, ValueError) as e:
            raise ValueError(f"payload must be JSON-serializable: {e}")
        
        # Validate metadata if provided
        if self.metadata is not None:
            if not isinstance(self.metadata, dict):
                raise TypeError(
                    f"metadata must be a dict, got {type(self.metadata).__name__}"
                )
            try:
                json.dumps(self.metadata)
            except (TypeError, ValueError) as e:
                raise ValueError(f"metadata must be JSON-serializable: {e}")
        
        # Validate timestamp is reasonable (within last 10 years to 1 hour future)
        current_time = time.time()
        min_time = current_time - (10 * 365 * 24 * 60 * 60)  # 10 years ago
        max_time = current_time + (60 * 60)  # 1 hour future
        
        if not isinstance(self.timestamp, (int, float)):
            raise TypeError(f"timestamp must be numeric, got {type(self.timestamp).__name__}")
        
        if self.timestamp < min_time or self.timestamp > max_time:
            raise ValueError(
                f"timestamp out of reasonable range: {self.timestamp}. "
                f"Expected range: {min_time} to {max_time}"
            )
        
        # Validate trace is a list of strings
        if not isinstance(self.trace, list):
            raise TypeError(f"trace must be a list, got {type(self.trace).__name__}")
        
        for item in self.trace:
            if not isinstance(item, str):
                raise TypeError(
                    f"trace items must be strings, got {type(item).__name__}"
                )
        
        # Initialize trace lock if not already initialized
        if not hasattr(self, '_trace_lock'):
            self._trace_lock = threading.Lock()
    
    def add_trace(self, node: str) -> None:
        """
        Add a node to the processing trace (thread-safe).
        
        Appends a node identifier to the trace list, indicating this message
        has been processed by that node. This operation is thread-safe.
        
        Args:
            node: Node identifier to add to trace
            
        Raises:
            ValueError: If node is not a valid string identifier
            
        Example:
            >>> msg = ProtocolMessage(intent="test", payload={})
            >>> msg.add_trace("router-1")
            >>> msg.add_trace("handler-2")
            >>> assert len(msg.trace) == 2
        """
        if not isinstance(node, str) or not node.strip():
            raise ValueError(
                f"Trace node must be non-empty string, got {type(node).__name__}"
            )
        
        with self._trace_lock:
            self.trace.append(node.strip())
    
    def validate(self) -> Tuple[bool, Optional[str]]:
        """
        Validate message structure and constraints.
        
        Performs comprehensive validation of all message fields and returns
        a tuple indicating validity and any error message.
        
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if message is valid, False otherwise
            - error_message: Error description if invalid, None if valid
            
        Example:
            >>> msg = ProtocolMessage(intent="test", payload={})
            >>> is_valid, error = msg.validate()
            >>> assert is_valid == True
        """
        try:
            # Re-run post-init validation checks
            self.__post_init__()
            return True, None
        except (ValueError, TypeError) as e:
            return False, str(e)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert message to dictionary representation.
        
        Excludes internal fields like thread locks and returns a dictionary
        suitable for JSON serialization.
        
        Returns:
            Dictionary representation of message
            
        Example:
            >>> msg = ProtocolMessage(intent="test", payload={"key": "value"})
            >>> data = msg.to_dict()
            >>> assert data["intent"] == "test"
            >>> assert data["payload"]["key"] == "value"
        """
        # Manually build dict to avoid thread lock serialization issues
        data = {
            'id': self.id,
            'version': self.version,
            'type': self.type.value,
            'priority': self.priority.value,
            'intent': self.intent,
            'payload': self.payload.copy() if self.payload else {},
            'metadata': self.metadata.copy() if self.metadata else {},
            'source': self.source,
            'target': self.target,
            'correlation_id': self.correlation_id,
            'semantic_vector': self.semantic_vector,
            'capability': self.capability,
            'topic': self.topic,
            'timestamp': self.timestamp,
            'trace': self.trace.copy() if self.trace else []
        }
        return data
    
    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Serialize message to JSON string.
        
        Validates message before serialization and raises an exception if
        the message is invalid.
        
        Args:
            indent: Optional JSON indentation (for pretty printing)
            
        Returns:
            JSON string representation of message
            
        Raises:
            ValueError: If message validation fails
            
        Example:
            >>> msg = ProtocolMessage(intent="test", payload={})
            >>> json_str = msg.to_json()
            >>> assert isinstance(json_str, str)
        """
        is_valid, error = self.validate()
        if not is_valid:
            raise ValueError(f"Cannot serialize invalid message: {error}")
        
        # Get dict representation (excludes thread locks)
        data = self.to_dict()
        
        # Custom JSON encoder that handles all types safely
        def json_encoder(obj):
            if isinstance(obj, (int, float, str, bool, type(None))):
                return obj
            elif isinstance(obj, dict):
                return {k: json_encoder(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [json_encoder(item) for item in obj]
            elif isinstance(obj, (MessageType, MessagePriority)):
                return obj.value
            else:
                return str(obj)
        
        return json.dumps(json_encoder(data), indent=indent)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ProtocolMessage':
        """
        Deserialize message from JSON string.
        
        Parses JSON string and creates a ProtocolMessage instance. Validates
        the deserialized message and raises an exception if validation fails.
        
        Args:
            json_str: JSON string to deserialize
            
        Returns:
            ProtocolMessage instance
            
        Raises:
            ValueError: If JSON is invalid or message validation fails
            TypeError: If JSON structure doesn't match schema
            
        Example:
            >>> json_str = '{"intent": "test", "payload": {}}'
            >>> msg = ProtocolMessage.from_json(json_str)
            >>> assert msg.intent == "test"
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        
        # Remove _trace_lock if present (shouldn't be in JSON)
        data.pop('_trace_lock', None)
        
        # Convert enum strings back to enum values
        if 'type' in data and isinstance(data['type'], str):
            try:
                data['type'] = MessageType(data['type'])
            except ValueError:
                raise ValueError(f"Invalid message type: {data['type']}")
        
        if 'priority' in data and isinstance(data['priority'], str):
            try:
                data['priority'] = MessagePriority(data['priority'])
            except ValueError:
                raise ValueError(f"Invalid message priority: {data['priority']}")
        
        # Create message instance
        try:
            msg = cls(**data)
        except TypeError as e:
            raise ValueError(f"Invalid message structure: {e}")
        
        # Re-initialize trace lock (not in JSON)
        msg._trace_lock = threading.Lock()
        
        # Validate deserialized message
        is_valid, error = msg.validate()
        if not is_valid:
            raise ValueError(f"Deserialized message invalid: {error}")
        
        return msg
    
    def copy(self, new_id: bool = True) -> 'ProtocolMessage':
        """
        Create a deep copy of the message.
        
        Creates an independent copy of the message. By default, generates
        a new ID and timestamp for the copy.
        
        Args:
            new_id: If True, generate new ID and timestamp for copy
            
        Returns:
            New ProtocolMessage instance
            
        Example:
            >>> msg1 = ProtocolMessage(intent="test", payload={})
            >>> msg2 = msg1.copy()
            >>> assert msg1.id != msg2.id  # Different IDs
            >>> assert msg1.intent == msg2.intent  # Same intent
        """
        data = self.to_dict()
        
        if new_id:
            data['id'] = str(uuid.uuid4())
            data['timestamp'] = time.time()
            data['trace'] = []  # Reset trace for new message
        
        # Convert enum values back to enums
        data['type'] = MessageType(data['type'])
        data['priority'] = MessagePriority(data['priority'])
        
        new_msg = cls(**data)
        new_msg._trace_lock = threading.Lock()
        return new_msg
    
    def __repr__(self) -> str:
        """Human-readable string representation."""
        return (
            f"ProtocolMessage("
            f"id={self.id[:8]}..., "
            f"type={self.type.value}, "
            f"intent={self.intent}, "
            f"priority={self.priority.value}, "
            f"trace_len={len(self.trace)})"
        )


# Schema normalization utilities

def normalize_message_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize message data dictionary.
    
    Normalizes a dictionary to match ProtocolMessage schema requirements.
    Handles type conversions, default values, and field name normalization.
    
    Args:
        data: Raw message data dictionary
        
    Returns:
        Normalized dictionary suitable for ProtocolMessage creation
        
    Example:
        >>> raw = {"intent": "  test  ", "payload": None}
        >>> normalized = normalize_message_data(raw)
        >>> assert normalized["intent"] == "test"
        >>> assert normalized["payload"] == {}
    """
    normalized = {}
    
    # Normalize ID
    if 'id' in data:
        normalized['id'] = str(data['id']).strip()
    else:
        normalized['id'] = str(uuid.uuid4())
    
    # Normalize version
    normalized['version'] = str(data.get('version', PROTOCOL_VERSION)).strip()
    
    # Normalize type
    if 'type' in data:
        type_val = data['type']
        if isinstance(type_val, str):
            try:
                normalized['type'] = MessageType(type_val.lower())
            except ValueError:
                normalized['type'] = MessageType.REQUEST
        elif isinstance(type_val, MessageType):
            normalized['type'] = type_val
        else:
            normalized['type'] = MessageType.REQUEST
    else:
        normalized['type'] = MessageType.REQUEST
    
    # Normalize priority
    if 'priority' in data:
        priority_val = data['priority']
        if isinstance(priority_val, str):
            try:
                normalized['priority'] = MessagePriority(priority_val.lower())
            except ValueError:
                normalized['priority'] = MessagePriority.NORMAL
        elif isinstance(priority_val, MessagePriority):
            normalized['priority'] = priority_val
        else:
            normalized['priority'] = MessagePriority.NORMAL
    else:
        normalized['priority'] = MessagePriority.NORMAL
    
    # Normalize intent (required)
    if 'intent' in data:
        intent = str(data['intent']).strip()
        if not intent:
            raise ValueError("intent cannot be empty")
        normalized['intent'] = intent
    else:
        raise ValueError("intent is required")
    
    # Normalize payload (required)
    if 'payload' in data:
        if data['payload'] is None:
            normalized['payload'] = {}
        elif isinstance(data['payload'], dict):
            normalized['payload'] = data['payload']
        else:
            raise TypeError("payload must be a dict")
    else:
        normalized['payload'] = {}
    
    # Normalize metadata (optional)
    if 'metadata' in data:
        if data['metadata'] is None:
            normalized['metadata'] = {}
        elif isinstance(data['metadata'], dict):
            normalized['metadata'] = data['metadata']
        else:
            normalized['metadata'] = {}
    else:
        normalized['metadata'] = {}
    
    # Normalize source/target (optional strings)
    for field_name in ['source', 'target', 'correlation_id', 'capability', 'topic']:
        if field_name in data:
            value = data[field_name]
            if value is not None:
                normalized[field_name] = str(value).strip() or None
            else:
                normalized[field_name] = None
    
    # Normalize semantic_vector (optional list of floats)
    if 'semantic_vector' in data:
        semantic_vector = data['semantic_vector']
        if semantic_vector is None:
            normalized['semantic_vector'] = None
        elif isinstance(semantic_vector, list):
            try:
                normalized['semantic_vector'] = [float(x) for x in semantic_vector]
            except (ValueError, TypeError):
                normalized['semantic_vector'] = None
        else:
            normalized['semantic_vector'] = None
    
    # Normalize timestamp
    if 'timestamp' in data:
        timestamp = data['timestamp']
        if isinstance(timestamp, (int, float)):
            normalized['timestamp'] = float(timestamp)
        elif isinstance(timestamp, str):
            try:
                normalized['timestamp'] = float(timestamp)
            except ValueError:
                normalized['timestamp'] = time.time()
        else:
            normalized['timestamp'] = time.time()
    else:
        normalized['timestamp'] = time.time()
    
    # Normalize trace (list of strings)
    if 'trace' in data:
        trace = data['trace']
        if isinstance(trace, list):
            normalized['trace'] = [
                str(item).strip() for item in trace if str(item).strip()
            ]
        else:
            normalized['trace'] = []
    else:
        normalized['trace'] = []
    
    return normalized

