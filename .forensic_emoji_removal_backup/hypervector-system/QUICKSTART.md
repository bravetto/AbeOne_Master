# 🔥 HyperVector System - Quick Start Guide

**Status:** ✅ **READY TO USE**  
**Pattern:** AEYON × QUICKSTART × ONE

---

## Installation

```bash
# Navigate to directory
cd hypervector-system

# Install dependencies
pip install -r requirements.txt
```

---

## Initialize Storage

```bash
# Initialize with default settings (1024 dims, 10000 capacity)
python scripts/init_store.py

# Or customize
python scripts/init_store.py --dimension 2048 --capacity 50000
```

---

## Start API Server

```bash
# Start server
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Or with reload for development
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Server will be available at: `http://localhost:8000`

---

## Test with SDK

```python
from SDK.client import HyperVectorClient

# Initialize client
client = HyperVectorClient(api_url="http://localhost:8000")

# Add a vector
vector_id = client.add_vector(
    vector=[0.1] * 1024,
    metadata={"name": "test", "category": "example"}
)
print(f"Added vector: {vector_id}")

# Search
results = client.search([0.1] * 1024, top_k=5)
for result in results:
    print(f"ID: {result['vector_id']}, Score: {result['score']}")

# Get stats
stats = client.get_stats()
print(f"Total vectors: {stats['count']}")
```

---

## Test with cURL

```bash
# Add vector
curl -X POST http://localhost:8000/api/v1/vectors \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, 0.3],
    "metadata": {"name": "test"}
  }'

# Search
curl -X POST http://localhost:8000/api/v1/vectors/search \
  -H "Content-Type: application/json" \
  -d '{
    "query_vector": [0.1, 0.2, 0.3],
    "top_k": 10
  }'

# Health check
curl http://localhost:8000/api/v1/health
```

---

## Populate Test Data

```bash
# Generate 100 test vectors
python scripts/populate_test_data.py --count 100

# Or customize
python scripts/populate_test_data.py --count 1000 --dimension 2048
```

---

## Environment Variables

```bash
# Set custom configuration
export VECTOR_DIMENSION=2048
export VECTOR_CAPACITY=50000
export STORAGE_PATH=.hypervector

# Start server
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

---

## Next Steps

1. **Read Documentation:**
   - [API Documentation](docs/API.md)
   - [SDK Documentation](docs/SDK.md)
   - [Architecture](docs/ARCHITECTURE.md)

2. **Explore Examples:**
   - Check `tests/` directory for examples
   - See `scripts/` for utility scripts

3. **Integrate:**
   - Use SDK in your Python projects
   - Call API from any language
   - Build on top of the storage engine

---

**Pattern:** AEYON × QUICKSTART × ONE  
**Status:** ✅ **READY**

