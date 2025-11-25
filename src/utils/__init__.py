"""
AbëONE Master Workspace Utilities

Efficient, atomic utility modules for common operations.

Pattern: UTILS × WORKSPACE × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

# Embeddings utilities
from .embeddings import (
    FAISSEmbeddingIndex,
    cosine_similarity,
    FAISS_AVAILABLE
)

# Serialization utilities
from .serialization import (
    Serializer,
    save_json,
    load_json,
    save_pickle,
    load_pickle,
    save_msgpack,
    load_msgpack,
    save_compressed,
    load_compressed,
    MSGPACK_AVAILABLE
)

# Logging utilities
from .logging import (
    LoggerConfig,
    get_logger,
    setup_logger,
    StructuredLogger,
    create_structured_logger,
    LogContext
)

# UUID utilities
from .uuid import (
    generate_uuid,
    generate_uuid_hex,
    generate_uuid_int,
    generate_uuid_bytes,
    generate_uuid_from_string,
    generate_uuid_from_bytes,
    generate_short_uuid,
    generate_namespaced_uuid,
    is_valid_uuid,
    normalize_uuid,
    UUIDGenerator
)

# Path utilities (existing)
from .paths import (
    resolve_project_root,
    get_data_path,
    get_input_path,
    get_output_path,
    get_sub_orbit_path
)

__all__ = [
    # Embeddings
    'FAISSEmbeddingIndex',
    'cosine_similarity',
    'FAISS_AVAILABLE',
    # Serialization
    'Serializer',
    'save_json',
    'load_json',
    'save_pickle',
    'load_pickle',
    'save_msgpack',
    'load_msgpack',
    'save_compressed',
    'load_compressed',
    'MSGPACK_AVAILABLE',
    # Logging
    'LoggerConfig',
    'get_logger',
    'setup_logger',
    'StructuredLogger',
    'create_structured_logger',
    'LogContext',
    # UUID
    'generate_uuid',
    'generate_uuid_hex',
    'generate_uuid_int',
    'generate_uuid_bytes',
    'generate_uuid_from_string',
    'generate_uuid_from_bytes',
    'generate_short_uuid',
    'generate_namespaced_uuid',
    'is_valid_uuid',
    'normalize_uuid',
    'UUIDGenerator',
    # Paths
    'resolve_project_root',
    'get_data_path',
    'get_input_path',
    'get_output_path',
    'get_sub_orbit_path',
]

