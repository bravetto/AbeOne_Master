"""
Storage Tests

Basic tests for storage functionality.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from src.hypervector.storage import HyperVectorStorage
from src.hypervector.utils import generate_random_vector


@pytest.fixture
def temp_storage():
    """Create temporary storage for testing."""
    temp_dir = tempfile.mkdtemp()
    storage = HyperVectorStorage(
        dimension=128,  # Smaller for testing
        capacity=1000,
        storage_path=temp_dir
    )
    yield storage
    shutil.rmtree(temp_dir)


def test_storage_initialization(temp_storage):
    """Test storage initialization."""
    assert temp_storage.count() == 0
    assert temp_storage.dimension == 128
    assert temp_storage.capacity == 1000


def test_add_vector(temp_storage):
    """Test adding a vector."""
    vector = generate_random_vector(128)
    vector_id = temp_storage.add_vector(vector, {"name": "test"})
    
    assert vector_id is not None
    assert temp_storage.count() == 1


def test_get_vector(temp_storage):
    """Test getting a vector."""
    vector = generate_random_vector(128)
    vector_id = temp_storage.add_vector(vector, {"name": "test"})
    
    record = temp_storage.get_vector(vector_id)
    assert record is not None
    assert record.vector_id == vector_id
    assert len(record.vector) == 128
    assert record.metadata["name"] == "test"


def test_search_vectors(temp_storage):
    """Test vector search."""
    # Add multiple vectors
    query_vector = generate_random_vector(128)
    for i in range(5):
        vector = generate_random_vector(128)
        temp_storage.add_vector(vector, {"index": i})
    
    # Search
    results = temp_storage.search(query_vector, top_k=3)
    assert len(results) <= 3
    assert all(isinstance(r, tuple) and len(r) == 2 for r in results)


def test_delete_vector(temp_storage):
    """Test deleting a vector."""
    vector = generate_random_vector(128)
    vector_id = temp_storage.add_vector(vector)
    
    assert temp_storage.count() == 1
    
    success = temp_storage.delete_vector(vector_id)
    assert success is True
    assert temp_storage.count() == 0
    
    record = temp_storage.get_vector(vector_id)
    assert record is None


def test_update_vector(temp_storage):
    """Test updating a vector."""
    vector = generate_random_vector(128)
    vector_id = temp_storage.add_vector(vector, {"name": "old"})
    
    new_metadata = {"name": "new", "category": "test"}
    success = temp_storage.update_vector(vector_id, metadata=new_metadata)
    
    assert success is True
    record = temp_storage.get_vector(vector_id)
    assert record.metadata["name"] == "new"
    assert record.metadata["category"] == "test"


def test_get_stats(temp_storage):
    """Test getting statistics."""
    stats = temp_storage.get_stats()
    assert "count" in stats
    assert "capacity" in stats
    assert "dimension" in stats
    assert stats["count"] == 0


# Run with: pytest tests/test_storage.py -v

