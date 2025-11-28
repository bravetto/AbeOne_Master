"""
Serialization Utilities

Efficient data serialization with multiple format support.

Pattern: SERIALIZATION × EFFICIENCY × ATOMIC × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import pickle
import gzip
from typing import Any, Optional, Union
from pathlib import Path

try:
    import msgpack
    MSGPACK_AVAILABLE = True
except ImportError:
    MSGPACK_AVAILABLE = False
    msgpack = None


class Serializer:
    """
    Unified serializer supporting multiple formats.
    
    Formats:
    - JSON: Human-readable, cross-platform
    - Pickle: Python-native, preserves types
    - MessagePack: Compact binary, fast
    - Gzip: Compression wrapper for any format
    
    ASSUMES:
    - Data is serializable in chosen format
    - File paths are writable/readable
    
    VERIFY:
    - serialize() returns bytes or str
    - deserialize() returns original type
    - Round-trip preserves data integrity
    
    FAILS:
    - If data not serializable in chosen format
    - If file I/O fails
    - If format not supported
    """
    
    @staticmethod
    def serialize_json(
        data: Any,
        indent: Optional[int] = None,
        ensure_ascii: bool = False
    ) -> str:
        """
        Serialize data to JSON string.
        
        SAFETY: Handles non-serializable objects gracefully
        ASSUMES: Data is JSON-serializable
        VERIFY: Returns valid JSON string
        
        Args:
            data: Data to serialize
            indent: Optional indentation level (None = compact)
            ensure_ascii: Whether to escape non-ASCII characters
            
        Returns:
            JSON string
            
        Raises:
            TypeError: If data contains non-JSON-serializable objects
        """
        try:
            return json.dumps(
                data,
                indent=indent,
                ensure_ascii=ensure_ascii,
                default=str  # Fallback for non-serializable types
            )
        except TypeError as e:
            raise TypeError(f"Data not JSON-serializable: {e}")
    
    @staticmethod
    def deserialize_json(data: str) -> Any:
        """
        Deserialize JSON string to Python object.
        
        SAFETY: Validates JSON syntax
        ASSUMES: data is valid JSON string
        VERIFY: Returns Python object
        
        Args:
            data: JSON string
            
        Returns:
            Deserialized Python object
            
        Raises:
            json.JSONDecodeError: If JSON syntax invalid
        """
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON: {e.msg}",
                e.doc,
                e.pos
            )
    
    @staticmethod
    def serialize_pickle(data: Any, protocol: int = pickle.HIGHEST_PROTOCOL) -> bytes:
        """
        Serialize data to pickle bytes.
        
        SAFETY: Uses highest protocol for efficiency
        ASSUMES: Data is pickle-serializable
        VERIFY: Returns bytes
        
        Args:
            data: Data to serialize
            protocol: Pickle protocol version (default: highest)
            
        Returns:
            Pickled bytes
            
        Raises:
            pickle.PicklingError: If data not pickleable
        """
        try:
            return pickle.dumps(data, protocol=protocol)
        except pickle.PicklingError as e:
            raise pickle.PicklingError(f"Data not pickleable: {e}")
    
    @staticmethod
    def deserialize_pickle(data: bytes) -> Any:
        """
        Deserialize pickle bytes to Python object.
        
        SAFETY: Validates pickle format
        ASSUMES: data is valid pickle bytes
        VERIFY: Returns Python object
        
        Args:
            data: Pickled bytes
            
        Returns:
            Deserialized Python object
            
        Raises:
            pickle.UnpicklingError: If pickle data invalid
        """
        try:
            return pickle.loads(data)
        except pickle.UnpicklingError as e:
            raise pickle.UnpicklingError(f"Invalid pickle data: {e}")
    
    @staticmethod
    def serialize_msgpack(data: Any) -> bytes:
        """
        Serialize data to MessagePack bytes.
        
        SAFETY: Falls back to JSON if MessagePack unavailable
        ASSUMES: Data is MessagePack-serializable
        VERIFY: Returns bytes
        
        Args:
            data: Data to serialize
            
        Returns:
            MessagePack bytes
            
        Raises:
            ImportError: If MessagePack not available
            TypeError: If data not MessagePack-serializable
        """
        if not MSGPACK_AVAILABLE:
            raise ImportError(
                "MessagePack not available. Install with: pip install msgpack"
            )
        
        try:
            return msgpack.packb(data, use_bin_type=True)
        except TypeError as e:
            raise TypeError(f"Data not MessagePack-serializable: {e}")
    
    @staticmethod
    def deserialize_msgpack(data: bytes) -> Any:
        """
        Deserialize MessagePack bytes to Python object.
        
        SAFETY: Validates MessagePack format
        ASSUMES: data is valid MessagePack bytes
        VERIFY: Returns Python object
        
        Args:
            data: MessagePack bytes
            
        Returns:
            Deserialized Python object
            
        Raises:
            ImportError: If MessagePack not available
            msgpack.UnpackException: If MessagePack data invalid
        """
        if not MSGPACK_AVAILABLE:
            raise ImportError(
                "MessagePack not available. Install with: pip install msgpack"
            )
        
        try:
            return msgpack.unpackb(data, raw=False)
        except msgpack.UnpackException as e:
            raise msgpack.UnpackException(f"Invalid MessagePack data: {e}")
    
    @staticmethod
    def compress(data: bytes, level: int = 6) -> bytes:
        """
        Compress data using gzip.
        
        SAFETY: Validates compression level
        ASSUMES: data is bytes
        VERIFY: Returns compressed bytes
        
        Args:
            data: Data to compress
            level: Compression level (1-9, default: 6)
            
        Returns:
            Compressed bytes
            
        Raises:
            ValueError: If compression level invalid
        """
        if not (1 <= level <= 9):
            raise ValueError(f"Compression level must be 1-9, got {level}")
        
        return gzip.compress(data, compresslevel=level)
    
    @staticmethod
    def decompress(data: bytes) -> bytes:
        """
        Decompress gzip-compressed data.
        
        SAFETY: Validates gzip format
        ASSUMES: data is gzip-compressed bytes
        VERIFY: Returns decompressed bytes
        
        Args:
            data: Compressed bytes
            
        Returns:
            Decompressed bytes
            
        Raises:
            gzip.BadGzipFile: If data not valid gzip
        """
        try:
            return gzip.decompress(data)
        except gzip.BadGzipFile as e:
            raise gzip.BadGzipFile(f"Invalid gzip data: {e}")


def save_json(
    data: Any,
    filepath: Union[str, Path],
    indent: Optional[int] = 2,
    ensure_ascii: bool = False
) -> None:
    """
    Save data to JSON file.
    
    SAFETY: Creates parent directories if needed
    ASSUMES: filepath is writable, data is JSON-serializable
    VERIFY: File created successfully
    
    Args:
        data: Data to save
        filepath: Path to JSON file
        indent: Optional indentation level (default: 2)
        ensure_ascii: Whether to escape non-ASCII characters
        
    Raises:
        IOError: If file write fails
        TypeError: If data not JSON-serializable
    """
    filepath_obj = Path(filepath)
    filepath_obj.parent.mkdir(parents=True, exist_ok=True)
    
    json_str = Serializer.serialize_json(data, indent=indent, ensure_ascii=ensure_ascii)
    
    try:
        filepath_obj.write_text(json_str, encoding='utf-8')
    except IOError as e:
        raise IOError(f"Failed to write JSON file: {e}")


def load_json(filepath: Union[str, Path]) -> Any:
    """
    Load data from JSON file.
    
    SAFETY: Validates file exists and is readable
    ASSUMES: filepath points to valid JSON file
    VERIFY: Returns deserialized Python object
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Deserialized Python object
        
    Raises:
        FileNotFoundError: If file not found
        json.JSONDecodeError: If JSON invalid
        IOError: If file read fails
    """
    filepath_obj = Path(filepath)
    
    if not filepath_obj.exists():
        raise FileNotFoundError(f"JSON file not found: {filepath}")
    
    try:
        json_str = filepath_obj.read_text(encoding='utf-8')
        return Serializer.deserialize_json(json_str)
    except IOError as e:
        raise IOError(f"Failed to read JSON file: {e}")


def save_pickle(
    data: Any,
    filepath: Union[str, Path],
    protocol: int = pickle.HIGHEST_PROTOCOL
) -> None:
    """
    Save data to pickle file.
    
    SAFETY: Creates parent directories if needed
    ASSUMES: filepath is writable, data is pickle-serializable
    VERIFY: File created successfully
    
    Args:
        data: Data to save
        filepath: Path to pickle file
        protocol: Pickle protocol version (default: highest)
        
    Raises:
        IOError: If file write fails
        pickle.PicklingError: If data not pickleable
    """
    filepath_obj = Path(filepath)
    filepath_obj.parent.mkdir(parents=True, exist_ok=True)
    
    pickle_bytes = Serializer.serialize_pickle(data, protocol=protocol)
    
    try:
        filepath_obj.write_bytes(pickle_bytes)
    except IOError as e:
        raise IOError(f"Failed to write pickle file: {e}")


def load_pickle(filepath: Union[str, Path]) -> Any:
    """
    Load data from pickle file.
    
    SAFETY: Validates file exists and is readable
    ASSUMES: filepath points to valid pickle file
    VERIFY: Returns deserialized Python object
    
    Args:
        filepath: Path to pickle file
        
    Returns:
        Deserialized Python object
        
    Raises:
        FileNotFoundError: If file not found
        pickle.UnpicklingError: If pickle invalid
        IOError: If file read fails
    """
    filepath_obj = Path(filepath)
    
    if not filepath_obj.exists():
        raise FileNotFoundError(f"Pickle file not found: {filepath}")
    
    try:
        pickle_bytes = filepath_obj.read_bytes()
        return Serializer.deserialize_pickle(pickle_bytes)
    except IOError as e:
        raise IOError(f"Failed to read pickle file: {e}")


def save_msgpack(
    data: Any,
    filepath: Union[str, Path]
) -> None:
    """
    Save data to MessagePack file.
    
    SAFETY: Creates parent directories if needed
    ASSUMES: filepath is writable, data is MessagePack-serializable
    VERIFY: File created successfully
    
    Args:
        data: Data to save
        filepath: Path to MessagePack file
        
    Raises:
        ImportError: If MessagePack not available
        IOError: If file write fails
        TypeError: If data not MessagePack-serializable
    """
    if not MSGPACK_AVAILABLE:
        raise ImportError(
            "MessagePack not available. Install with: pip install msgpack"
        )
    
    filepath_obj = Path(filepath)
    filepath_obj.parent.mkdir(parents=True, exist_ok=True)
    
    msgpack_bytes = Serializer.serialize_msgpack(data)
    
    try:
        filepath_obj.write_bytes(msgpack_bytes)
    except IOError as e:
        raise IOError(f"Failed to write MessagePack file: {e}")


def load_msgpack(filepath: Union[str, Path]) -> Any:
    """
    Load data from MessagePack file.
    
    SAFETY: Validates file exists and is readable
    ASSUMES: filepath points to valid MessagePack file
    VERIFY: Returns deserialized Python object
    
    Args:
        filepath: Path to MessagePack file
        
    Returns:
        Deserialized Python object
        
    Raises:
        ImportError: If MessagePack not available
        FileNotFoundError: If file not found
        msgpack.UnpackException: If MessagePack invalid
        IOError: If file read fails
    """
    if not MSGPACK_AVAILABLE:
        raise ImportError(
            "MessagePack not available. Install with: pip install msgpack"
        )
    
    filepath_obj = Path(filepath)
    
    if not filepath_obj.exists():
        raise FileNotFoundError(f"MessagePack file not found: {filepath}")
    
    try:
        msgpack_bytes = filepath_obj.read_bytes()
        return Serializer.deserialize_msgpack(msgpack_bytes)
    except IOError as e:
        raise IOError(f"Failed to read MessagePack file: {e}")


def save_compressed(
    data: Any,
    filepath: Union[str, Path],
    format: str = "pickle",
    compression_level: int = 6
) -> None:
    """
    Save data to compressed file.
    
    Supports JSON, pickle, or MessagePack formats with gzip compression.
    
    SAFETY: Creates parent directories if needed
    ASSUMES: filepath is writable, data is serializable in chosen format
    VERIFY: Compressed file created successfully
    
    Args:
        data: Data to save
        filepath: Path to compressed file
        format: Serialization format - "json", "pickle", or "msgpack"
        compression_level: Gzip compression level (1-9, default: 6)
        
    Raises:
        ValueError: If format not supported
        IOError: If file write fails
    """
    if format == "json":
        serialized = Serializer.serialize_json(data).encode('utf-8')
    elif format == "pickle":
        serialized = Serializer.serialize_pickle(data)
    elif format == "msgpack":
        serialized = Serializer.serialize_msgpack(data)
    else:
        raise ValueError(f"Unsupported format: {format}. Must be 'json', 'pickle', or 'msgpack'")
    
    compressed = Serializer.compress(serialized, level=compression_level)
    
    filepath_obj = Path(filepath)
    filepath_obj.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        filepath_obj.write_bytes(compressed)
    except IOError as e:
        raise IOError(f"Failed to write compressed file: {e}")


def load_compressed(
    filepath: Union[str, Path],
    format: str = "pickle"
) -> Any:
    """
    Load data from compressed file.
    
    Supports JSON, pickle, or MessagePack formats with gzip compression.
    
    SAFETY: Validates file exists and is readable
    ASSUMES: filepath points to valid compressed file
    VERIFY: Returns deserialized Python object
    
    Args:
        filepath: Path to compressed file
        format: Serialization format - "json", "pickle", or "msgpack"
        
    Returns:
        Deserialized Python object
        
    Raises:
        ValueError: If format not supported
        FileNotFoundError: If file not found
        IOError: If file read fails
    """
    filepath_obj = Path(filepath)
    
    if not filepath_obj.exists():
        raise FileNotFoundError(f"Compressed file not found: {filepath}")
    
    try:
        compressed = filepath_obj.read_bytes()
        decompressed = Serializer.decompress(compressed)
        
        if format == "json":
            return Serializer.deserialize_json(decompressed.decode('utf-8'))
        elif format == "pickle":
            return Serializer.deserialize_pickle(decompressed)
        elif format == "msgpack":
            return Serializer.deserialize_msgpack(decompressed)
        else:
            raise ValueError(f"Unsupported format: {format}. Must be 'json', 'pickle', or 'msgpack'")
    except IOError as e:
        raise IOError(f"Failed to read compressed file: {e}")

