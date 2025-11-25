# Trust Guard API Documentation

## Overview

Trust Guard provides a comprehensive REST API for AI reliability monitoring, pattern detection, and mitigation. All endpoints require authentication via API key or JWT token.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication

Trust Guard supports two authentication methods:

### API Key Authentication

Include your API key in the request header:

```bash
curl -H "X-API-Key: your-api-key" \
     -H "Content-Type: application/json" \
     http://localhost:8000/v1/detect
```

### JWT Token Authentication

Include your JWT token in the Authorization header:

```bash
curl -H "Authorization: Bearer your-jwt-token" \
     -H "Content-Type: application/json" \
     http://localhost:8000/v1/detect
```

## API Endpoints

### AI Pattern Detection

#### POST /v1/detect

Detect AI failure patterns in text.

**Request Body:**
```json
{
  "text": "The AI system is 100% certain that this is correct.",
  "context": "Optional context information",
  "metadata": {
    "source": "chatbot",
    "timestamp": "2025-01-13T00:00:00Z"
  }
}
```

**Response:**
```json
{
  "detections": {
    "hallucination": {
      "score": 0.75,
      "confidence": 0.85,
      "description": "High overconfidence detected",
      "evidence": ["100% certain", "overconfidence indicators"],
      "risk_level": "high"
    },
    "drift": {
      "score": 0.0,
      "confidence": 1.0,
      "description": "No topic drift detected",
      "evidence": [],
      "risk_level": "low"
    }
  },
  "overall_risk_score": 0.75,
  "processing_time_ms": 45.2,
  "timestamp": "2025-01-13T00:00:00Z"
}
```

#### POST /v1/validate

Perform comprehensive mathematical validation.

**Request Body:**
```json
{
  "input_text": "Original input text",
  "output_text": "AI-generated output text",
  "context": "Optional context"
}
```

**Response:**
```json
{
  "overall_score": 0.65,
  "kl_divergence": 0.23,
  "uncertainty_score": 0.15,
  "consistency_score": 0.78,
  "statistical_analysis": {
    "word_count": 25,
    "readability_score": 0.82,
    "complexity_metrics": {...}
  },
  "confidence_intervals": {
    "lower_bound": 0.45,
    "upper_bound": 0.85,
    "confidence_level": 0.95
  },
  "risk_assessment": {
    "level": "medium",
    "description": "Moderate risk detected",
    "recommendations": ["Review output for accuracy"]
  }
}
```

#### POST /v1/mitigate

Apply constitutional prompting and mitigation strategies.

**Request Body:**
```json
{
  "text": "Text to mitigate",
  "detected_patterns": ["hallucination", "bias"],
  "risk_level": "high"
}
```

**Response:**
```json
{
  "original_text": "Original text",
  "mitigated_text": "Enhanced and mitigated text",
  "applied_techniques": ["constitutional_prompting", "uncertainty_injection"],
  "risk_reduction": 0.4,
  "confidence_improvement": 0.25,
  "prompts_used": ["Be honest about uncertainty", "Avoid overconfident claims"]
}
```

#### POST /v1/constitutional

Generate constitutional prompts for specific patterns.

**Request Body:**
```json
{
  "patterns": ["hallucination", "bias"],
  "severity": "high"
}
```

**Response:**
```json
{
  "prompts": [
    "Be honest about uncertainty and limitations",
    "Avoid making claims you cannot verify",
    "Present balanced perspectives without bias"
  ],
  "techniques": ["uncertainty_injection", "constitutional_prompting"],
  "severity": "high"
}
```

### Security & Authentication

#### POST /v1/auth/keys

Create a new API key.

**Request Body:**
```json
{
  "name": "My API Key",
  "role": "developer",
  "expires_in_days": 90
}
```

**Response:**
```json
{
  "key_id": "tg_abc123",
  "api_key": "tg_abc123_secret_key_here",
  "role": "developer",
  "name": "My API Key",
  "created_at": "2025-01-13T00:00:00Z",
  "expires_at": "2025-04-13T00:00:00Z"
}
```

#### GET /v1/auth/keys

List all API keys (admin only).

**Response:**
```json
{
  "keys": [
    {
      "key_id": "tg_abc123",
      "name": "My API Key",
      "role": "developer",
      "created_at": "2025-01-13T00:00:00Z",
      "expires_at": "2025-04-13T00:00:00Z",
      "last_used": "2025-01-13T12:00:00Z",
      "is_active": true
    }
  ]
}
```

#### DELETE /v1/auth/keys/{key_id}

Revoke an API key.

**Response:**
```json
{
  "message": "API key revoked successfully",
  "key_id": "tg_abc123"
}
```

#### POST /v1/auth/jwt

Generate a JWT token.

**Request Body:**
```json
{
  "user_id": "user123",
  "role": "analyst",
  "expires_in_minutes": 60
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-01-13T01:00:00Z",
  "user_id": "user123",
  "role": "analyst"
}
```

### Monitoring & Health

#### GET /health

Basic health check.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-13T00:00:00Z",
  "version": "1.0.0"
}
```

#### GET /health/live

Kubernetes liveness probe.

**Response:**
```json
{
  "status": "alive"
}
```

#### GET /health/ready

Kubernetes readiness probe.

**Response:**
```json
{
  "status": "ready"
}
```

#### GET /health/detailed

Comprehensive health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-13T00:00:00Z",
  "uptime_seconds": 3600,
  "check_duration_ms": 15.2,
  "components": [
    {
      "name": "Detector",
      "status": "healthy",
      "message": "AI Detector is operational",
      "timestamp": "2025-01-13T00:00:00Z"
    },
    {
      "name": "System Resources",
      "status": "healthy",
      "message": "System resources are optimal",
      "details": {
        "cpu_percent": 25.5,
        "memory_percent": 45.2
      }
    }
  ],
  "summary": {
    "total_components": 8,
    "healthy_components": 8,
    "degraded_components": 0,
    "unhealthy_components": 0
  }
}
```

#### GET /metrics

Prometheus metrics.

**Response:**
```
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{endpoint="/v1/detect",method="POST",status_code="200"} 150

# HELP pattern_detections_total Total number of AI pattern detections
# TYPE pattern_detections_total counter
pattern_detections_total{pattern="hallucination",risk_level="high"} 25
```

#### GET /v1/observability/summary

Observability system summary.

**Response:**
```json
{
  "status": "active",
  "service_info": {
    "name": "TrustGuard",
    "version": "1.0.0",
    "tracing_enabled": true,
    "metrics_enabled": true
  },
  "performance": {
    "total_requests": 1250,
    "endpoints": {
      "/v1/detect": {
        "count": 500,
        "avg_response_time_ms": 45.2,
        "max_response_time_ms": 120.5,
        "min_response_time_ms": 12.3,
        "error_count": 2,
        "error_rate": 0.4
      }
    }
  },
  "timestamp": "2025-01-13T00:00:00Z"
}
```

### Tracer Bullets (Debugging)

#### GET /v1/tracer/bullets

Get tracer bullets for debugging.

**Query Parameters:**
- `count` (optional): Number of bullets to return (default: 100)

**Response:**
```json
{
  "bullets": [
    {
      "id": "bullet_123",
      "timestamp": "2025-01-13T00:00:00Z",
      "level": "info",
      "message": "Pattern detection completed",
      "data": {
        "pattern": "hallucination",
        "score": 0.75
      },
      "trace_id": "trace_456"
    }
  ],
  "total_count": 150,
  "returned_count": 100
}
```

#### GET /v1/tracer/performance

Get performance metrics from tracer bullets.

**Response:**
```json
{
  "performance_metrics": {
    "avg_processing_time_ms": 45.2,
    "max_processing_time_ms": 120.5,
    "min_processing_time_ms": 12.3,
    "total_requests": 500,
    "error_rate": 0.02
  },
  "timestamp": "2025-01-13T00:00:00Z"
}
```

#### GET /v1/tracer/health

Get tracer system health.

**Response:**
```json
{
  "status": "healthy",
  "total_bullets": 150,
  "max_bullets": 10000,
  "performance_tracking": true,
  "last_cleanup": "2025-01-13T00:00:00Z"
}
```

#### DELETE /v1/tracer/bullets

Clear all tracer bullets.

**Response:**
```json
{
  "message": "Tracer bullets cleared successfully",
  "cleared_count": 150
}
```

## Error Responses

All endpoints return consistent error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request format",
  "error_code": "INVALID_REQUEST"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication required",
  "error_code": "AUTHENTICATION_REQUIRED"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions",
  "error_code": "INSUFFICIENT_PERMISSIONS"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded",
  "error_code": "RATE_LIMIT_EXCEEDED"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error_code": "INTERNAL_ERROR"
}
```

## Rate Limiting

- **Default Limit**: 100 requests per minute per API key
- **Headers**: Rate limit information is included in response headers:
  - `X-RateLimit-Limit`: Maximum requests per minute
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time when the rate limit resets

## Usage Examples

### Python

```python
import requests

# Set up authentication
headers = {
    "X-API-Key": "your-api-key",
    "Content-Type": "application/json"
}

# Detect AI patterns
response = requests.post(
    "http://localhost:8000/v1/detect",
    headers=headers,
    json={
        "text": "The AI is 100% certain this is correct.",
        "context": "Customer service chatbot"
    }
)

result = response.json()
print(f"Hallucination score: {result['detections']['hallucination']['score']}")
```

### JavaScript

```javascript
const response = await fetch('http://localhost:8000/v1/detect', {
  method: 'POST',
  headers: {
    'X-API-Key': 'your-api-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: 'The AI is 100% certain this is correct.',
    context: 'Customer service chatbot'
  })
});

const result = await response.json();
console.log(`Hallucination score: ${result.detections.hallucination.score}`);
```

### cURL

```bash
# Detect patterns
curl -X POST "http://localhost:8000/v1/detect" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The AI is 100% certain this is correct.",
    "context": "Customer service chatbot"
  }'

# Get health status
curl -H "X-API-Key: your-api-key" \
  "http://localhost:8000/health/detailed"

# Get metrics
curl -H "X-API-Key: your-api-key" \
  "http://localhost:8000/metrics"
```

## SDKs and Libraries

Trust Guard provides official SDKs for:

- **Python**: `pip install trust-guard-sdk`
- **JavaScript/Node.js**: `npm install trust-guard-sdk`
- **Go**: `go get github.com/trust-guard/sdk-go`

## Support

For API support and questions:

- **Documentation**: [https://docs.trust-guard.com](https://docs.trust-guard.com)
- **Interactive API**: [https://api.trust-guard.com/docs](https://api.trust-guard.com/docs)
- **Support Email**: support@trust-guard.com
- **Status Page**: [https://status.trust-guard.com](https://status.trust-guard.com)
