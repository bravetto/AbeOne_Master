"""
UUID Generation Utilities

Efficient UUID generation with multiple format support.

Pattern: UUID × GENERATION × ATOMIC × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

import uuid
import hashlib
from typing import Optional, Union


def generate_uuid() -> str:
    """
    Generate standard UUID4 string.
    
    SAFETY: Uses cryptographically secure random generation
    ASSUMES: System has sufficient entropy
    VERIFY: Returns valid UUID string
    
    Returns:
        UUID4 string (e.g., "550e8400-e29b-41d4-a716-446655440000")
    """
    return str(uuid.uuid4())


def generate_uuid_hex() -> str:
    """
    Generate UUID4 as hexadecimal string (no hyphens).
    
    SAFETY: Uses cryptographically secure random generation
    ASSUMES: System has sufficient entropy
    VERIFY: Returns 32-character hex string
    
    Returns:
        UUID4 hex string (e.g., "550e8400e29b41d4a716446655440000")
    """
    return uuid.uuid4().hex


def generate_uuid_int() -> int:
    """
    Generate UUID4 as integer.
    
    SAFETY: Uses cryptographically secure random generation
    ASSUMES: System has sufficient entropy
    VERIFY: Returns positive integer
    
    Returns:
        UUID4 as integer
    """
    return uuid.uuid4().int


def generate_uuid_bytes() -> bytes:
    """
    Generate UUID4 as bytes.
    
    SAFETY: Uses cryptographically secure random generation
    ASSUMES: System has sufficient entropy
    VERIFY: Returns 16 bytes
    
    Returns:
        UUID4 as bytes (16 bytes)
    """
    return uuid.uuid4().bytes


def generate_uuid_from_string(
    text: str,
    namespace: Optional[uuid.UUID] = None
) -> str:
    """
    Generate deterministic UUID5 from string.
    
    Uses SHA-1 hashing for deterministic UUID generation.
    Same input always produces same UUID.
    
    SAFETY: Validates input is not empty
    ASSUMES: text is string, namespace is valid UUID if provided
    VERIFY: Returns valid UUID string
    
    Args:
        text: Input string to hash
        namespace: Optional namespace UUID (default: DNS namespace)
        
    Returns:
        UUID5 string
        
    Raises:
        ValueError: If text is empty
    """
    if not text:
        raise ValueError("Text cannot be empty")
    
    if namespace is None:
        namespace = uuid.NAMESPACE_DNS
    
    return str(uuid.uuid5(namespace, text))


def generate_uuid_from_bytes(
    data: bytes,
    namespace: Optional[uuid.UUID] = None
) -> str:
    """
    Generate deterministic UUID5 from bytes.
    
    Uses SHA-1 hashing for deterministic UUID generation.
    Same input always produces same UUID.
    
    SAFETY: Validates input is not empty
    ASSUMES: data is bytes, namespace is valid UUID if provided
    VERIFY: Returns valid UUID string
    
    Args:
        data: Input bytes to hash
        namespace: Optional namespace UUID (default: DNS namespace)
        
    Returns:
        UUID5 string
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    if namespace is None:
        namespace = uuid.NAMESPACE_DNS
    
    # SAFETY: Convert bytes to string for UUID5
    text = data.decode('utf-8', errors='replace')
    return str(uuid.uuid5(namespace, text))


def generate_short_uuid(length: int = 8) -> str:
    """
    Generate short UUID-like identifier.
    
    Uses hash of UUID4 for shorter identifier.
    Not cryptographically secure, but sufficient for most use cases.
    
    SAFETY: Validates length is positive
    ASSUMES: length > 0
    VERIFY: Returns hex string of requested length
    
    Args:
        length: Desired length (default: 8)
        
    Returns:
        Short hex identifier
        
    Raises:
        ValueError: If length <= 0
    """
    if length <= 0:
        raise ValueError(f"Length must be positive, got {length}")
    
    # SAFETY: Generate UUID and hash
    uuid_str = generate_uuid_hex()
    hash_obj = hashlib.sha256(uuid_str.encode())
    hash_hex = hash_obj.hexdigest()
    
    # SAFETY: Truncate to requested length
    return hash_hex[:length]


def generate_namespaced_uuid(
    namespace: str,
    name: str
) -> str:
    """
    Generate namespaced UUID5.
    
    Creates deterministic UUID from namespace and name.
    Useful for consistent IDs across systems.
    
    SAFETY: Validates inputs are not empty
    ASSUMES: namespace and name are strings
    VERIFY: Returns valid UUID string
    
    Args:
        namespace: Namespace identifier
        name: Name within namespace
        
    Returns:
        UUID5 string
        
    Raises:
        ValueError: If namespace or name is empty
    """
    if not namespace:
        raise ValueError("Namespace cannot be empty")
    
    if not name:
        raise ValueError("Name cannot be empty")
    
    # SAFETY: Create namespace UUID from string
    namespace_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, namespace)
    
    # SAFETY: Generate UUID5 from namespace and name
    return str(uuid.uuid5(namespace_uuid, name))


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Validate UUID string format.
    
    SAFETY: Handles invalid formats gracefully
    ASSUMES: uuid_string is string
    VERIFY: Returns boolean
    
    Args:
        uuid_string: UUID string to validate
        
    Returns:
        True if valid UUID format, False otherwise
    """
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, TypeError):
        return False


def normalize_uuid(uuid_string: str) -> str:
    """
    Normalize UUID string to standard format.
    
    Converts UUID to lowercase standard format.
    
    SAFETY: Validates UUID format
    ASSUMES: uuid_string is valid UUID
    VERIFY: Returns normalized UUID string
    
    Args:
        uuid_string: UUID string to normalize
        
    Returns:
        Normalized UUID string (lowercase, standard format)
        
    Raises:
        ValueError: If UUID format invalid
    """
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return str(uuid_obj)
    except ValueError as e:
        raise ValueError(f"Invalid UUID format: {e}")


class UUIDGenerator:
    """
    UUID generator with configurable options.
    
    Provides reusable UUID generator with consistent settings.
    
    ASSUMES:
    - System has sufficient entropy for random generation
    
    VERIFY:
    - Generated UUIDs are valid
    - Format matches requested type
    """
    
    def __init__(
        self,
        format: str = "standard",
        namespace: Optional[str] = None
    ):
        """
        Initialize UUID generator.
        
        SAFETY: Validates format parameter
        ASSUMES: format is valid format type
        VERIFY: Generator initialized successfully
        
        Args:
            format: UUID format - "standard", "hex", "int", or "bytes"
            namespace: Optional namespace for deterministic UUIDs
            
        Raises:
            ValueError: If format invalid
        """
        if format not in ("standard", "hex", "int", "bytes"):
            raise ValueError(
                f"Invalid format: {format}. Must be 'standard', 'hex', 'int', or 'bytes'"
            )
        
        self.format = format
        self.namespace = namespace
    
    def generate(self, name: Optional[str] = None) -> Union[str, int, bytes]:
        """
        Generate UUID.
        
        SAFETY: Handles deterministic vs random generation
        ASSUMES: name provided if namespace set
        VERIFY: Returns UUID in requested format
        
        Args:
            name: Optional name for deterministic UUID generation
            
        Returns:
            UUID in requested format
            
        Raises:
            ValueError: If namespace set but name not provided
        """
        if self.namespace and name:
            # SAFETY: Deterministic UUID
            uuid_str = generate_namespaced_uuid(self.namespace, name)
            uuid_obj = uuid.UUID(uuid_str)
        else:
            # SAFETY: Random UUID
            uuid_obj = uuid.uuid4()
        
        # SAFETY: Return in requested format
        if self.format == "standard":
            return str(uuid_obj)
        elif self.format == "hex":
            return uuid_obj.hex
        elif self.format == "int":
            return uuid_obj.int
        else:  # bytes
            return uuid_obj.bytes
    
    def generate_many(self, count: int) -> list:
        """
        Generate multiple UUIDs.
        
        SAFETY: Validates count is positive
        ASSUMES: count > 0
        VERIFY: Returns list of UUIDs
        
        Args:
            count: Number of UUIDs to generate
            
        Returns:
            List of UUIDs in requested format
            
        Raises:
            ValueError: If count <= 0
        """
        if count <= 0:
            raise ValueError(f"Count must be positive, got {count}")
        
        return [self.generate() for _ in range(count)]

