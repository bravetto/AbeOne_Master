"""
Metadata Storage

JSON-based metadata storage for vectors.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import threading


class MetadataStore:
    """
    Thread-safe JSON-based metadata storage.
    """
    
    def __init__(self, storage_path: Path):
        """
        Initialize metadata store.
        
        Args:
            storage_path: Path to JSON file
        """
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._data: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        
        # Load existing data
        self._load()
    
    def get(self, vector_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for vector.
        
        Args:
            vector_id: Vector ID
        
        Returns:
            Metadata dict or None
        """
        with self._lock:
            return self._data.get(vector_id)
    
    def set(self, vector_id: str, metadata: Dict[str, Any]):
        """
        Set metadata for vector.
        
        Args:
            vector_id: Vector ID
            metadata: Metadata dict
        """
        with self._lock:
            self._data[vector_id] = metadata
            self._save()
    
    def delete(self, vector_id: str) -> bool:
        """
        Delete metadata for vector.
        
        Args:
            vector_id: Vector ID
        
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if vector_id not in self._data:
                return False
            
            del self._data[vector_id]
            self._save()
            return True
    
    def clear(self):
        """Clear all metadata."""
        with self._lock:
            self._data.clear()
            self._save()
    
    def _load(self):
        """Load metadata from disk."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._data = {}
        else:
            self._data = {}
    
    def _save(self):
        """Save metadata to disk."""
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self._data, f, indent=2)
        except IOError:
            pass  # Fail silently if can't save

