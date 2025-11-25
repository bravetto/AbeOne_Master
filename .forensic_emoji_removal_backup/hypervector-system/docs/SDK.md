# HyperVector SDK Documentation

**Status:** ✅ **COMPLETE**  
**Version:** 1.0.0

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Quick Start

```python
from SDK.client import HyperVectorClient

# Initialize client
client = HyperVectorClient(api_url="http://localhost:8000")

# Add a vector
vector_id = client.add_vector(
    vector=[0.1] * 1024,
    metadata={"name": "test_vector", "category": "test"}
)

# Search similar vectors
results = client.search(
    query_vector=[0.1] * 1024,
    top_k=10
)

# Get vector by ID
vector = client.get_vector(vector_id)
```

---

## API Reference

### `HyperVectorClient`

Main client class for interacting with HyperVector API.

#### Constructor

```python
HyperVectorClient(
    api_url: str = "http://localhost:8000",
    timeout: int = 30
)
```

**Parameters:**
- `api_url` - API base URL (default: "http://localhost:8000")
- `timeout` - Request timeout in seconds (default: 30)

---

### Methods

#### `add_vector(vector, metadata=None, vector_id=None) -> str`

Add a new vector to storage.

**Parameters:**
- `vector` (List[float]) - Vector as list of floats
- `metadata` (Optional[Dict[str, Any]]) - Optional metadata dictionary
- `vector_id` (Optional[str]) - Optional custom vector ID

**Returns:**
- `str` - Vector ID

**Raises:**
- `HyperVectorValidationError` - On validation error
- `HyperVectorAPIError` - On API error

**Example:**
```python
vector_id = client.add_vector(
    vector=[0.1] * 1024,
    metadata={"name": "test", "category": "example"}
)
```

---

#### `get_vector(vector_id) -> Dict[str, Any]`

Get vector by ID.

**Parameters:**
- `vector_id` (str) - Vector ID

**Returns:**
- `Dict[str, Any]` - Vector record with metadata

**Raises:**
- `HyperVectorNotFoundError` - If vector not found
- `HyperVectorAPIError` - On API error

**Example:**
```python
vector = client.get_vector("uuid-here")
print(vector["metadata"])
```

---

#### `update_vector(vector_id, vector=None, metadata=None) -> Dict[str, Any]`

Update vector and/or metadata.

**Parameters:**
- `vector_id` (str) - Vector ID
- `vector` (Optional[List[float]]) - Optional new vector
- `metadata` (Optional[Dict[str, Any]]) - Optional new metadata (merged)

**Returns:**
- `Dict[str, Any]` - Updated vector record

**Raises:**
- `HyperVectorNotFoundError` - If vector not found
- `HyperVectorAPIError` - On API error

**Example:**
```python
client.update_vector(
    vector_id="uuid-here",
    metadata={"new_field": "value"}
)
```

---

#### `delete_vector(vector_id) -> bool`

Delete vector by ID.

**Parameters:**
- `vector_id` (str) - Vector ID

**Returns:**
- `bool` - True if deleted

**Raises:**
- `HyperVectorAPIError` - On API error

**Example:**
```python
client.delete_vector("uuid-here")
```

---

#### `search(query_vector, top_k=10, min_score=0.0) -> List[Dict[str, Any]]`

Search for similar vectors.

**Parameters:**
- `query_vector` (List[float]) - Query vector
- `top_k` (int) - Number of results (default: 10)
- `min_score` (float) - Minimum similarity score (default: 0.0)

**Returns:**
- `List[Dict[str, Any]]` - List of search results with vector_id, score, and metadata

**Raises:**
- `HyperVectorValidationError` - On validation error
- `HyperVectorAPIError` - On API error

**Example:**
```python
results = client.search(
    query_vector=[0.1] * 1024,
    top_k=10,
    min_score=0.8
)

for result in results:
    print(f"ID: {result['vector_id']}, Score: {result['score']}")
```

---

#### `list_vectors(limit=None) -> List[str]`

List all vector IDs.

**Parameters:**
- `limit` (Optional[int]) - Optional limit on number of IDs

**Returns:**
- `List[str]` - List of vector IDs

**Raises:**
- `HyperVectorAPIError` - On API error

**Example:**
```python
vector_ids = client.list_vectors(limit=100)
```

---

#### `get_stats() -> Dict[str, Any]`

Get system statistics.

**Returns:**
- `Dict[str, Any]` - Statistics dictionary

**Raises:**
- `HyperVectorAPIError` - On API error

**Example:**
```python
stats = client.get_stats()
print(f"Count: {stats['count']}, Capacity: {stats['capacity']}")
```

---

#### `health_check() -> Dict[str, str]`

Check API health.

**Returns:**
- `Dict[str, str]` - Health status dictionary

**Raises:**
- `HyperVectorAPIError` - On API error

**Example:**
```python
health = client.health_check()
print(health["status"])
```

---

#### `batch_add_vectors(vectors) -> List[str]`

Add multiple vectors in batch.

**Parameters:**
- `vectors` (List[Tuple[List[float], Optional[Dict[str, Any]]]]) - List of (vector, metadata) tuples

**Returns:**
- `List[str]` - List of vector IDs

**Raises:**
- `HyperVectorAPIError` - On API error

**Example:**
```python
vectors = [
    ([0.1] * 1024, {"name": "vector_1"}),
    ([0.2] * 1024, {"name": "vector_2"}),
]
vector_ids = client.batch_add_vectors(vectors)
```

---

## Exceptions

### `HyperVectorError`

Base exception for all HyperVector SDK errors.

### `HyperVectorAPIError`

API error exception.

**Attributes:**
- `status_code` - HTTP status code

### `HyperVectorNotFoundError`

Vector not found exception (extends `HyperVectorAPIError`).

### `HyperVectorValidationError`

Validation error exception.

---

## Complete Example

```python
from SDK.client import HyperVectorClient
from SDK.exceptions import HyperVectorError

# Initialize client
client = HyperVectorClient(api_url="http://localhost:8000")

try:
    # Add vectors
    vector_ids = []
    for i in range(10):
        vector = [0.1 * i] * 1024
        metadata = {"index": i, "name": f"vector_{i}"}
        vector_id = client.add_vector(vector, metadata)
        vector_ids.append(vector_id)
    
    # Search
    query = [0.1] * 1024
    results = client.search(query, top_k=5)
    
    for result in results:
        print(f"ID: {result['vector_id']}, Score: {result['score']}")
    
    # Get stats
    stats = client.get_stats()
    print(f"Total vectors: {stats['count']}")
    
except HyperVectorError as e:
    print(f"Error: {e}")
```

---

**Pattern:** AEYON × SDK × DOCUMENTATION × ONE  
**Status:** ✅ **COMPLETE**

