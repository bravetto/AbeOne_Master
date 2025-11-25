"""
Vector Index Management

FAISS-based vector index for similarity search.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import threading

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    np = None


class VectorIndex:
    """
    FAISS-based vector index for fast similarity search.
    
    Uses IndexFlatIP (Inner Product) for cosine similarity.
    """
    
    def __init__(self, dimension: int = 1024, capacity: int = 10000):
        """
        Initialize vector index.
        
        Args:
            dimension: Vector dimension
            capacity: Maximum capacity
        """
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS not available")
        
        self.dimension = dimension
        self.capacity = capacity
        
        # FAISS index (Inner Product for cosine similarity)
        self.index = faiss.IndexFlatIP(dimension)
        
        # ID mapping: FAISS position -> vector_id
        self.id_map: Dict[int, str] = {}
        self.reverse_map: Dict[str, int] = {}
        
        # Thread safety
        self._lock = threading.RLock()
    
    def add(self, vector_id: str, vector: np.ndarray):
        """
        Add vector to index.
        
        Args:
            vector_id: Unique vector ID
            vector: Vector as numpy array (1D)
        """
        if vector_id in self.reverse_map:
            raise ValueError(f"Vector ID {vector_id} already exists")
        
        with self._lock:
            # Reshape to 2D (1, dimension)
            vector_2d = vector.reshape(1, -1).astype(np.float32)
            
            # Normalize for cosine similarity
            faiss.normalize_L2(vector_2d)
            
            # Add to index
            position = self.index.ntotal
            self.index.add(vector_2d)
            
            # Update mappings
            self.id_map[position] = vector_id
            self.reverse_map[vector_id] = position
    
    def get(self, vector_id: str) -> Optional[np.ndarray]:
        """
        Get vector by ID.
        
        Args:
            vector_id: Vector ID
        
        Returns:
            Vector as numpy array or None
        """
        with self._lock:
            if vector_id not in self.reverse_map:
                return None
            
            position = self.reverse_map[vector_id]
            vector = self.index.reconstruct(position)
            return vector
    
    def update(self, vector_id: str, vector: np.ndarray):
        """
        Update vector in index.
        
        Args:
            vector_id: Vector ID
            vector: New vector as numpy array
        """
        with self._lock:
            if vector_id not in self.reverse_map:
                raise ValueError(f"Vector ID {vector_id} not found")
            
            # Delete old vector
            self.delete(vector_id)
            
            # Add new vector
            self.add(vector_id, vector)
    
    def delete(self, vector_id: str) -> bool:
        """
        Delete vector from index.
        
        Note: FAISS doesn't support deletion, so we mark as deleted.
        
        Args:
            vector_id: Vector ID
        
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if vector_id not in self.reverse_map:
                return False
            
            position = self.reverse_map[vector_id]
            
            # Remove from mappings
            del self.id_map[position]
            del self.reverse_map[vector_id]
            
            # Note: FAISS doesn't support deletion
            # We'll handle this by filtering during search
            
            return True
    
    def exists(self, vector_id: str) -> bool:
        """Check if vector exists."""
        return vector_id in self.reverse_map
    
    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query vector as numpy array (1D)
            top_k: Number of results
        
        Returns:
            List of (vector_id, score) tuples
        """
        with self._lock:
            if self.index.ntotal == 0:
                return []
            
            # Reshape to 2D
            query_2d = query_vector.reshape(1, -1).astype(np.float32)
            
            # Normalize for cosine similarity
            faiss.normalize_L2(query_2d)
            
            # Search
            scores, indices = self.index.search(query_2d, min(top_k, self.index.ntotal))
            
            # Map indices to vector IDs
            results = []
            for idx, score in zip(indices[0], scores[0]):
                if idx in self.id_map:  # Filter deleted vectors
                    vector_id = self.id_map[idx]
                    results.append((vector_id, float(score)))
            
            return results
    
    def count(self) -> int:
        """Get total vector count."""
        return len(self.reverse_map)
    
    def list_ids(self, limit: Optional[int] = None) -> List[str]:
        """
        List all vector IDs.
        
        Args:
            limit: Optional limit
        
        Returns:
            List of vector IDs
        """
        ids = list(self.reverse_map.keys())
        if limit is not None:
            ids = ids[:limit]
        return ids
    
    def save(self, filepath: str):
        """Save index to disk."""
        with self._lock:
            # Save FAISS index
            faiss.write_index(self.index, filepath)
            
            # Save ID mappings
            mappings_path = Path(filepath).parent / "index_mappings.json"
            with open(mappings_path, "w") as f:
                json.dump({
                    "id_map": {str(k): v for k, v in self.id_map.items()},
                    "reverse_map": self.reverse_map
                }, f)
    
    def load(self, filepath: str):
        """Load index from disk."""
        with self._lock:
            # Load FAISS index
            self.index = faiss.read_index(filepath)
            
            # Load ID mappings
            mappings_path = Path(filepath).parent / "index_mappings.json"
            if mappings_path.exists():
                with open(mappings_path, "r") as f:
                    data = json.load(f)
                    self.id_map = {int(k): v for k, v in data["id_map"].items()}
                    self.reverse_map = data["reverse_map"]
    
    def clear(self):
        """Clear all vectors."""
        with self._lock:
            self.index = faiss.IndexFlatIP(self.dimension)
            self.id_map.clear()
            self.reverse_map.clear()

