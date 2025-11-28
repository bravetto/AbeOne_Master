"""
HyperVector System - Core Module

Forensically isolated hyperdimensional vector storage and retrieval system.
"""

from .storage import HyperVectorStorage
from .index import VectorIndex
from .metadata import MetadataStore

__version__ = "1.0.0"
__all__ = ["HyperVectorStorage", "VectorIndex", "MetadataStore"]

