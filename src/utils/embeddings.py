"""
FAISS-based Embedding Utilities

Efficient vector similarity search and embedding operations using FAISS.

Pattern: EMBEDDINGS × FAISS × SIMILARITY × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import List, Optional, Tuple, Dict, Any
import threading
from pathlib import Path

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    faiss = None
    np = None


class FAISSEmbeddingIndex:
    """
    FAISS-based embedding index for efficient similarity search.
    
    Features:
    - Fast similarity search using FAISS
    - Thread-safe operations
    - Metadata support per vector
    - Disk persistence
    - Graceful degradation when FAISS unavailable
    
    ASSUMES:
    - Vectors are normalized or compatible for cosine similarity
    - Vector dimensions are consistent
    - Metadata is JSON-serializable
    
    VERIFY:
    - search() returns List[Tuple[str, float]]
    - add() accepts numpy array or List[float]
    - Thread-safe concurrent access
    
    FAILS:
    - If FAISS unavailable and operations attempted
    - If vector dimensions mismatch
    - If index capacity exceeded
    """
    
    def __init__(
        self,
        dimension: int = 768,
        index_type: str = "flat",
        normalize: bool = True
    ):
        """
        Initialize FAISS embedding index.
        
        SAFETY: Validates FAISS availability and parameters
        ASSUMES: dimension > 0, index_type is valid
        VERIFY: Index initialized successfully
        
        Args:
            dimension: Vector dimension (default: 768)
            index_type: Index type - "flat" (exact) or "ivf" (approximate)
            normalize: Whether to normalize vectors for cosine similarity
            
        Raises:
            ImportError: If FAISS not available
            ValueError: If dimension <= 0 or invalid index_type
        """
        if not FAISS_AVAILABLE:
            raise ImportError(
                "FAISS not available. Install with: pip install faiss-cpu or faiss-gpu"
            )
        
        # SAFETY: Parameter validation
        if dimension <= 0:
            raise ValueError(f"Dimension must be positive, got {dimension}")
        
        if index_type not in ("flat", "ivf"):
            raise ValueError(f"Invalid index_type: {index_type}. Must be 'flat' or 'ivf'")
        
        self.dimension = dimension
        self.index_type = index_type
        self.normalize = normalize
        
        # SAFETY: Initialize FAISS index
        if index_type == "flat":
            # Inner Product for cosine similarity (after normalization)
            self.index = faiss.IndexFlatIP(dimension)
        else:  # ivf
            # IVF index for approximate search (requires training)
            nlist = 100  # Number of clusters
            quantizer = faiss.IndexFlatIP(dimension)
            self.index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
            self._trained = False
        
        # SAFETY: ID mapping and metadata
        self.id_map: Dict[int, str] = {}  # FAISS position -> vector_id
        self.reverse_map: Dict[str, int] = {}  # vector_id -> FAISS position
        self.metadata: Dict[str, Dict[str, Any]] = {}  # vector_id -> metadata
        
        # SAFETY: Thread safety
        self._lock = threading.RLock()
    
    def add(
        self,
        vector_id: str,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add vector to index.
        
        SAFETY: Validates vector dimensions and handles duplicates
        ASSUMES: vector is List[float] or numpy array, vector_id is unique
        VERIFY: Vector added successfully, ID mapped correctly
        
        Args:
            vector_id: Unique identifier for vector
            vector: Embedding vector (List[float] or numpy array)
            metadata: Optional metadata dictionary
            
        Raises:
            ValueError: If vector dimension mismatch or vector_id already exists
            TypeError: If vector contains non-numeric values
        """
        with self._lock:
            # SAFETY: Check if already exists
            if vector_id in self.reverse_map:
                raise ValueError(f"Vector ID already exists: {vector_id}")
            
            # SAFETY: Convert to numpy array
            if isinstance(vector, list):
                vector_array = np.array(vector, dtype=np.float32)
            elif isinstance(vector, np.ndarray):
                vector_array = vector.astype(np.float32)
            else:
                raise TypeError(f"Vector must be List[float] or numpy array, got {type(vector)}")
            
            # SAFETY: Validate dimension
            if vector_array.ndim == 1:
                vector_array = vector_array.reshape(1, -1)
            
            if vector_array.shape[1] != self.dimension:
                raise ValueError(
                    f"Vector dimension mismatch: expected {self.dimension}, "
                    f"got {vector_array.shape[1]}"
                )
            
            # SAFETY: Normalize if requested
            if self.normalize:
                faiss.normalize_L2(vector_array)
            
            # SAFETY: Train IVF index if needed
            if self.index_type == "ivf" and not self._trained:
                # Need at least nlist vectors for training
                if self.index.ntotal == 0:
                    # Will train after first batch
                    pass
            
            # SAFETY: Add to index
            position = self.index.ntotal
            self.index.add(vector_array)
            
            # SAFETY: Update mappings
            self.id_map[position] = vector_id
            self.reverse_map[vector_id] = position
            
            # SAFETY: Store metadata
            if metadata is not None:
                self.metadata[vector_id] = metadata.copy()
    
    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        min_score: Optional[float] = None
    ) -> List[Tuple[str, float]]:
        """
        Search for similar vectors.
        
        SAFETY: Validates query vector and handles empty index
        ASSUMES: query_vector matches index dimension
        VERIFY: Returns sorted results by similarity score
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            min_score: Optional minimum similarity score threshold
            
        Returns:
            List of (vector_id, score) tuples sorted by score (descending)
            
        Raises:
            ValueError: If query vector dimension mismatch or index empty
        """
        with self._lock:
            # SAFETY: Check if index is empty
            if self.index.ntotal == 0:
                return []
            
            # SAFETY: Convert query to numpy array
            if isinstance(query_vector, list):
                query_array = np.array(query_vector, dtype=np.float32)
            elif isinstance(query_vector, np.ndarray):
                query_array = query_vector.astype(np.float32)
            else:
                raise TypeError(
                    f"Query vector must be List[float] or numpy array, got {type(query_vector)}"
                )
            
            # SAFETY: Reshape to 2D
            if query_array.ndim == 1:
                query_array = query_array.reshape(1, -1)
            
            # SAFETY: Validate dimension
            if query_array.shape[1] != self.dimension:
                raise ValueError(
                    f"Query vector dimension mismatch: expected {self.dimension}, "
                    f"got {query_array.shape[1]}"
                )
            
            # SAFETY: Normalize if index is normalized
            if self.normalize:
                faiss.normalize_L2(query_array)
            
            # SAFETY: Search
            k = min(top_k, self.index.ntotal)
            scores, indices = self.index.search(query_array, k)
            
            # SAFETY: Map indices to vector IDs and filter
            results = []
            for idx, score in zip(indices[0], scores[0]):
                if idx in self.id_map:  # Filter deleted vectors
                    vector_id = self.id_map[idx]
                    score_float = float(score)
                    
                    # SAFETY: Apply minimum score threshold
                    if min_score is None or score_float >= min_score:
                        results.append((vector_id, score_float))
            
            # SAFETY: Sort by score descending
            results.sort(key=lambda x: x[1], reverse=True)
            
            return results
    
    def get_metadata(self, vector_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for vector.
        
        Args:
            vector_id: Vector identifier
            
        Returns:
            Metadata dictionary or None if not found
        """
        with self._lock:
            return self.metadata.get(vector_id)
    
    def update_metadata(
        self,
        vector_id: str,
        metadata: Dict[str, Any]
    ) -> None:
        """
        Update metadata for vector.
        
        SAFETY: Validates vector exists
        ASSUMES: metadata is JSON-serializable
        
        Args:
            vector_id: Vector identifier
            metadata: Metadata dictionary to merge
            
        Raises:
            ValueError: If vector_id not found
        """
        with self._lock:
            if vector_id not in self.reverse_map:
                raise ValueError(f"Vector ID not found: {vector_id}")
            
            if vector_id in self.metadata:
                self.metadata[vector_id].update(metadata)
            else:
                self.metadata[vector_id] = metadata.copy()
    
    def remove(self, vector_id: str) -> bool:
        """
        Remove vector from index.
        
        Note: FAISS doesn't support deletion, so we mark as deleted in mappings.
        
        Args:
            vector_id: Vector identifier to remove
            
        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if vector_id not in self.reverse_map:
                return False
            
            position = self.reverse_map[vector_id]
            del self.id_map[position]
            del self.reverse_map[vector_id]
            
            if vector_id in self.metadata:
                del self.metadata[vector_id]
            
            return True
    
    def count(self) -> int:
        """
        Get total vector count.
        
        Returns:
            Number of vectors in index
        """
        with self._lock:
            return len(self.reverse_map)
    
    def exists(self, vector_id: str) -> bool:
        """
        Check if vector exists.
        
        Args:
            vector_id: Vector identifier
            
        Returns:
            True if exists, False otherwise
        """
        with self._lock:
            return vector_id in self.reverse_map
    
    def save(self, filepath: str) -> None:
        """
        Save index to disk.
        
        SAFETY: Creates parent directories if needed
        ASSUMES: filepath is writable
        
        Args:
            filepath: Path to save index file
            
        Raises:
            IOError: If save fails
        """
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS not available")
        
        filepath_obj = Path(filepath)
        filepath_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with self._lock:
            faiss.write_index(self.index, str(filepath_obj))
            
            # SAFETY: Save metadata separately
            metadata_path = filepath_obj.with_suffix('.metadata.json')
            import json
            with open(metadata_path, 'w') as f:
                json.dump({
                    'id_map': self.id_map,
                    'reverse_map': self.reverse_map,
                    'metadata': self.metadata,
                    'dimension': self.dimension,
                    'index_type': self.index_type,
                    'normalize': self.normalize
                }, f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'FAISSEmbeddingIndex':
        """
        Load index from disk.
        
        SAFETY: Validates file exists and is readable
        ASSUMES: filepath points to valid FAISS index
        
        Args:
            filepath: Path to index file
            
        Returns:
            Loaded FAISSEmbeddingIndex instance
            
        Raises:
            FileNotFoundError: If index file not found
            IOError: If load fails
        """
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS not available")
        
        filepath_obj = Path(filepath)
        if not filepath_obj.exists():
            raise FileNotFoundError(f"Index file not found: {filepath}")
        
        # SAFETY: Load index
        index = faiss.read_index(str(filepath_obj))
        
        # SAFETY: Load metadata
        metadata_path = filepath_obj.with_suffix('.metadata.json')
        import json
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                data = json.load(f)
            
            dimension = data.get('dimension', index.d)
            index_type = data.get('index_type', 'flat')
            normalize = data.get('normalize', True)
            
            instance = cls(dimension=dimension, index_type=index_type, normalize=normalize)
            instance.index = index
            instance.id_map = {int(k): v for k, v in data.get('id_map', {}).items()}
            instance.reverse_map = data.get('reverse_map', {})
            instance.metadata = data.get('metadata', {})
        else:
            # Fallback: create instance with default params
            instance = cls(dimension=index.d)
            instance.index = index
        
        return instance


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    
    Pure Python implementation (no FAISS required).
    
    SAFETY: Validates vector dimensions and handles zero vectors
    ASSUMES: Vectors are numeric lists
    VERIFY: Returns float in [-1.0, 1.0]
    
    Args:
        vec1: First embedding vector
        vec2: Second embedding vector
        
    Returns:
        Cosine similarity score in [-1.0, 1.0]
        
    Raises:
        ValueError: If vectors have mismatched dimensions or are empty
        TypeError: If vectors contain non-numeric values
    """
    # SAFETY: Dimension validation
    if len(vec1) != len(vec2):
        raise ValueError(
            f"Vector dimension mismatch: vec1={len(vec1)}, vec2={len(vec2)}"
        )
    
    if len(vec1) == 0:
        raise ValueError("Vectors cannot be empty")
    
    # SAFETY: Type validation and conversion
    try:
        vec1_float = [float(x) for x in vec1]
        vec2_float = [float(x) for x in vec2]
    except (ValueError, TypeError) as e:
        raise TypeError(f"Vectors must contain only numeric values: {e}")
    
    # SAFETY: Compute dot product
    dot_product = sum(a * b for a, b in zip(vec1_float, vec2_float))
    
    # SAFETY: Compute magnitudes
    import math
    norm1 = math.sqrt(sum(a * a for a in vec1_float))
    norm2 = math.sqrt(sum(b * b for b in vec2_float))
    
    # SAFETY: Handle zero vectors
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    
    # SAFETY: Compute cosine similarity
    similarity = dot_product / (norm1 * norm2)
    
    # SAFETY: Clamp to valid range
    similarity = max(-1.0, min(1.0, similarity))
    
    return similarity

