"""
HyperVector Storage Engine

FAISS-backed storage for 10K hyperdimensional vectors with metadata support.
"""

import json
import uuid
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    np = None

from .index import VectorIndex
from .metadata import MetadataStore


@dataclass
class VectorRecord:
    """Single vector record with metadata."""
    vector_id: str
    vector: List[float]
    metadata: Dict[str, Any]
    created_at: str
    updated_at: str


class HyperVectorStorage:
    """
    Forensically isolated hyperdimensional vector storage.
    
    Features:
    - FAISS-backed vector index
    - Metadata storage per vector
    - Thread-safe operations
    - Disk persistence
    - 10K capacity support
    """
    
    def __init__(
        self,
        dimension: int = 1024,
        capacity: int = 10000,
        storage_path: str = ".hypervector"
    ):
        """
        Initialize hypervector storage.
        
        Args:
            dimension: Vector dimension (default: 1024)
            capacity: Maximum capacity (default: 10000)
            storage_path: Storage directory path
        """
        if not FAISS_AVAILABLE:
            raise ImportError(
                "FAISS not available. Install with: pip install faiss-cpu"
            )
        
        self.dimension = dimension
        self.capacity = capacity
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.index = VectorIndex(dimension=dimension, capacity=capacity)
        self.metadata_store = MetadataStore(
            storage_path=self.storage_path / "metadata.json"
        )
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Load existing data
        self._load_from_disk()
    
    def add_vector(
        self,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None,
        vector_id: Optional[str] = None
    ) -> str:
        """
        Add a vector to storage.
        
        Args:
            vector: Vector as list of floats
            metadata: Optional metadata dict
            vector_id: Optional custom ID (auto-generated if not provided)
        
        Returns:
            Vector ID
        """
        if len(vector) != self.dimension:
            raise ValueError(
                f"Vector dimension {len(vector)} != {self.dimension}"
            )
        
        if self.count() >= self.capacity:
            raise RuntimeError(f"Storage at capacity ({self.capacity})")
        
        with self._lock:
            # Generate ID if not provided
            if vector_id is None:
                vector_id = str(uuid.uuid4())
            
            # Convert to numpy array
            vector_array = np.array(vector, dtype=np.float32)
            
            # Add to index
            self.index.add(vector_id, vector_array)
            
            # Store metadata
            self.metadata_store.set(
                vector_id,
                {
                    "vector_id": vector_id,
                    "metadata": metadata or {},
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            )
            
            # Persist to disk
            self._save_to_disk()
            
            return vector_id
    
    def get_vector(self, vector_id: str) -> Optional[VectorRecord]:
        """
        Get vector by ID.
        
        Args:
            vector_id: Vector ID
        
        Returns:
            VectorRecord or None if not found
        """
        with self._lock:
            vector = self.index.get(vector_id)
            if vector is None:
                return None
            
            metadata = self.metadata_store.get(vector_id)
            if metadata is None:
                metadata = {}
            
            return VectorRecord(
                vector_id=vector_id,
                vector=vector.tolist(),
                metadata=metadata.get("metadata", {}),
                created_at=metadata.get("created_at", ""),
                updated_at=metadata.get("updated_at", "")
            )
    
    def update_vector(
        self,
        vector_id: str,
        vector: Optional[List[float]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update vector and/or metadata.
        
        Args:
            vector_id: Vector ID
            vector: Optional new vector
            metadata: Optional new metadata (merged with existing)
        
        Returns:
            True if updated, False if not found
        """
        with self._lock:
            if not self.index.exists(vector_id):
                return False
            
            # Update vector if provided
            if vector is not None:
                if len(vector) != self.dimension:
                    raise ValueError(
                        f"Vector dimension {len(vector)} != {self.dimension}"
                    )
                vector_array = np.array(vector, dtype=np.float32)
                self.index.update(vector_id, vector_array)
            
            # Update metadata if provided
            if metadata is not None:
                existing_metadata = self.metadata_store.get(vector_id) or {}
                existing_metadata["metadata"] = {
                    **existing_metadata.get("metadata", {}),
                    **metadata
                }
                existing_metadata["updated_at"] = datetime.utcnow().isoformat()
                self.metadata_store.set(vector_id, existing_metadata)
            
            # Persist to disk
            self._save_to_disk()
            
            return True
    
    def delete_vector(self, vector_id: str) -> bool:
        """
        Delete vector by ID.
        
        Args:
            vector_id: Vector ID
        
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if not self.index.exists(vector_id):
                return False
            
            self.index.delete(vector_id)
            self.metadata_store.delete(vector_id)
            self._save_to_disk()
            
            return True
    
    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        min_score: float = 0.0
    ) -> List[Tuple[str, float]]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query vector
            top_k: Number of results to return
            min_score: Minimum similarity score
        
        Returns:
            List of (vector_id, score) tuples
        """
        if len(query_vector) != self.dimension:
            raise ValueError(
                f"Query vector dimension {len(query_vector)} != {self.dimension}"
            )
        
        with self._lock:
            query_array = np.array(query_vector, dtype=np.float32)
            results = self.index.search(query_array, top_k=top_k)
            
            # Filter by min_score
            filtered = [
                (vector_id, score)
                for vector_id, score in results
                if score >= min_score
            ]
            
            return filtered
    
    def count(self) -> int:
        """Get total vector count."""
        return self.index.count()
    
    def list_vectors(self, limit: Optional[int] = None) -> List[str]:
        """
        List all vector IDs.
        
        Args:
            limit: Optional limit on number of IDs
        
        Returns:
            List of vector IDs
        """
        return self.index.list_ids(limit=limit)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        return {
            "count": self.count(),
            "capacity": self.capacity,
            "dimension": self.dimension,
            "storage_path": str(self.storage_path),
            "faiss_available": FAISS_AVAILABLE
        }
    
    def _save_to_disk(self):
        """Save index to disk."""
        index_path = self.storage_path / "index.faiss"
        self.index.save(str(index_path))
    
    def _load_from_disk(self):
        """Load index from disk."""
        index_path = self.storage_path / "index.faiss"
        if index_path.exists():
            self.index.load(str(index_path))
    
    def clear(self):
        """Clear all vectors (use with caution)."""
        with self._lock:
            self.index.clear()
            self.metadata_store.clear()
            self._save_to_disk()

