# HyperVector API Documentation

**Status:**  **COMPLETE**  
**Version:** 1.0.0

---

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### Health Check

#### `GET /api/v1/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### Add Vector

#### `POST /api/v1/vectors`

Add a new vector to storage.

**Request Body:**
```json
{
  "vector": [0.1, 0.2, ...],
  "metadata": {
    "name": "test_vector",
    "category": "test"
  },
  "vector_id": "optional-custom-id"
}
```

**Response:** `201 Created`
```json
{
  "vector_id": "uuid-here",
  "vector": [0.1, 0.2, ...],
  "metadata": {...},
  "created_at": "2025-01-27T12:00:00",
  "updated_at": "2025-01-27T12:00:00"
}
```

**Errors:**
- `400 Bad Request` - Invalid vector dimension or format
- `507 Insufficient Storage` - Storage at capacity

---

### Get Vector

#### `GET /api/v1/vectors/{vector_id}`

Get vector by ID.

**Response:** `200 OK`
```json
{
  "vector_id": "uuid-here",
  "vector": [0.1, 0.2, ...],
  "metadata": {...},
  "created_at": "2025-01-27T12:00:00",
  "updated_at": "2025-01-27T12:00:00"
}
```

**Errors:**
- `404 Not Found` - Vector not found

---

### Update Vector

#### `PUT /api/v1/vectors/{vector_id}`

Update vector and/or metadata.

**Request Body:**
```json
{
  "vector": [0.1, 0.2, ...],
  "metadata": {
    "new_field": "value"
  }
}
```

**Response:** `200 OK`
```json
{
  "vector_id": "uuid-here",
  "vector": [0.1, 0.2, ...],
  "metadata": {...},
  "created_at": "2025-01-27T12:00:00",
  "updated_at": "2025-01-27T12:00:00"
}
```

**Errors:**
- `404 Not Found` - Vector not found
- `400 Bad Request` - Invalid vector dimension

---

### Delete Vector

#### `DELETE /api/v1/vectors/{vector_id}`

Delete vector by ID.

**Response:** `204 No Content`

**Errors:**
- `404 Not Found` - Vector not found

---

### Search Vectors

#### `POST /api/v1/vectors/search`

Search for similar vectors.

**Request Body:**
```json
{
  "query_vector": [0.1, 0.2, ...],
  "top_k": 10,
  "min_score": 0.0
}
```

**Response:** `200 OK`
```json
{
  "results": [
    {
      "vector_id": "uuid-1",
      "score": 0.95,
      "metadata": {...}
    },
    {
      "vector_id": "uuid-2",
      "score": 0.92,
      "metadata": {...}
    }
  ],
  "count": 2
}
```

**Errors:**
- `400 Bad Request` - Invalid query vector dimension

---

### List Vectors

#### `GET /api/v1/vectors?limit=100`

List all vector IDs.

**Query Parameters:**
- `limit` (optional) - Maximum number of IDs to return (default: 100)

**Response:** `200 OK`
```json
[
  "uuid-1",
  "uuid-2",
  "uuid-3"
]
```

---

### Get Statistics

#### `GET /api/v1/vectors/stats`

Get system statistics.

**Response:** `200 OK`
```json
{
  "count": 1000,
  "capacity": 10000,
  "dimension": 1024,
  "storage_path": ".hypervector",
  "faiss_available": true
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Status Codes:**
- `400` - Bad Request (validation error)
- `404` - Not Found
- `507` - Insufficient Storage
- `503` - Service Unavailable

---

## Examples

### cURL Examples

```bash
# Add vector
curl -X POST http://localhost:8000/api/v1/vectors \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, 0.3],
    "metadata": {"name": "test"}
  }'

# Search vectors
curl -X POST http://localhost:8000/api/v1/vectors/search \
  -H "Content-Type: application/json" \
  -d '{
    "query_vector": [0.1, 0.2, 0.3],
    "top_k": 10
  }'

# Get vector
curl http://localhost:8000/api/v1/vectors/{vector_id}

# Delete vector
curl -X DELETE http://localhost:8000/api/v1/vectors/{vector_id}
```

---

**Pattern:** AEYON × API × DOCUMENTATION × ONE  
**Status:**  **COMPLETE**

