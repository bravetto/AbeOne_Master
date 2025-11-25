# CodeGuardians Gateway API Documentation

## 🌐 Base URL

```
http://localhost:8000
```

## 🔐 Authentication

All endpoints require authentication via JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## 📋 Core Endpoints

### 1. Unified Guard Processing

**Endpoint**: `POST /api/v1/guards/process`
**Description**: Main endpoint for all guard service processing!67


#### Request Format

```json
{
  "service_type": "tokenguard|trustguard|contextguard|biasguard|securityguard|healthguard",
  "payload": {
    "text": "Content to analyze",
    "context_window": 1024,
    "memory_limit": 2048,
    "drift_threshold": 0.1
  },
  "user_id": "user-123",
  "session_id": "session-456"
}
```

#### Response Format

```json
{
  "request_id": "uuid",
  "service_type": "tokenguard",
  "success": true,
  "data": {
    "result": "analysis result",
    "confidence": 0.95,
    "metadata": {}
  },
  "error": null,
  "processing_time": 0.123,
  "service_used": "tokenguard"
}
```

### 2. Service Discovery

**Endpoint**: `GET /api/v1/guards/services`
**Description**: List all available guard services

#### Response

```json
{
  "services": [
    {
      "name": "tokenguard",
      "port": 8001,
      "status": "healthy",
      "description": "Token optimization & cost management"
    },
    {
      "name": "trustguard",
      "port": 8002,
      "status": "healthy",
      "description": "Trust validation & reliability"
    },
    {
      "name": "contextguard",
      "port": 8003,
      "status": "healthy",
      "description": "Context analysis & drift detection"
    },
    {
      "name": "biasguard",
      "port": 8004,
      "status": "healthy",
      "description": "Bias detection & mitigation"
    },
    {
      "name": "securityguard",
      "port": 8005,
      "status": "healthy",
      "description": "Security scanning & threat detection"
    },
    {
      "name": "healthguard",
      "port": 8005,
      "status": "healthy",
      "description": "Health monitoring & validation"
    }
  ],
  "access_pattern": "Use POST /api/v1/guards/process with service_type field"
}
```

## 🛡️ Guard Service Architecture

**⚠️ Important**: Guard services run on internal Docker network ports only. All external access must go through the unified gateway endpoint: `POST /api/v1/guards/process`. Direct access to individual service endpoints is not available.

### Internal Service Endpoints (Reference Only)

### TokenGuard (Port 8001)

**Purpose**: Token optimization and security

#### Endpoint: `POST /api/v1/optimize`

```json
{
  "text": "Your content to optimize",
  "max_tokens": 1000,
  "optimization_level": "aggressive"
}
```

#### Response

```json
{
  "optimized_text": "Optimized content",
  "token_count": 150,
  "reduction_percentage": 25.5,
  "optimization_techniques": ["pruning", "compression"]
}
```

### TrustGuard (Port 8002)

**Purpose**: Trust validation and reliability

#### Endpoint: `POST /api/v1/trust`

```json
{
  "text": "Content to validate",
  "trust_threshold": 0.8,
  "validation_level": "comprehensive"
}
```

#### Response

```json
{
  "trust_score": 0.85,
  "reliability": "high",
  "validation_results": {
    "factual_accuracy": 0.9,
    "source_credibility": 0.8,
    "consistency": 0.85
  }
}
```

### ContextGuard (Port 8003)

**Purpose**: Context analysis and drift detection

#### Endpoint: `POST /api/v1/context`

```json
{
  "text": "Current content",
  "context_window": 1024,
  "memory_limit": 2048,
  "drift_threshold": 0.1
}
```

#### Response

```json
{
  "drift_detected": true,
  "drift_score": 0.85,
  "context_coherence": 0.15,
  "recommended_action": "redirect_to_original_topic",
  "suggested_response": "Let's get back to discussing..."
}
```

### BiasGuard (Port 8004)

**Purpose**: Bias detection and mitigation

#### Endpoint: `POST /api/v1/bias`

```json
{
  "text": "Content to analyze",
  "bias_types": ["demographic", "content", "representation"],
  "mitigation_level": "moderate"
}
```

#### Response

```json
{
  "bias_detected": true,
  "bias_score": 0.7,
  "bias_types": ["demographic"],
  "mitigation_suggestions": ["Use inclusive language", "Add diverse examples"]
}
```

### SecurityGuard (Port 8005)

**Purpose**: Security scanning and threat detection

#### Endpoint: `POST /api/v1/security`

```json
{
  "text": "Content to scan",
  "scan_types": ["malware", "phishing", "injection"],
  "threat_level": "high"
}
```

#### Response

```json
{
  "threats_detected": true,
  "threat_score": 0.8,
  "threat_types": ["phishing"],
  "recommendations": ["Remove suspicious links", "Verify sender identity"]
}
```

### HealthGuard (Port 8005)

**Purpose**: Health monitoring and validation

#### Endpoint: `POST /api/v1/health`

```json
{
  "text": "Content to monitor",
  "health_metrics": ["toxicity", "safety", "appropriateness"],
  "monitoring_level": "comprehensive"
}
```

#### Response

```json
{
  "health_score": 0.9,
  "toxicity_level": "low",
  "safety_status": "safe",
  "recommendations": ["Content is appropriate for all audiences"]
}
```

## 🏥 Health Endpoints

### Liveness Check

**Endpoint**: `GET /health/live`
**Description**: Basic service availability

#### Response

```json
{
  "status": "alive",
  "service": "codeguardians-gateway",
  "version": "1.0.0",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Readiness Check

**Endpoint**: `GET /health/ready`
**Description**: Service readiness with dependencies

#### Response

```json
{
  "status": "ready",
  "dependencies": {
    "database": "connected",
    "redis": "connected",
    "guard_services": "healthy"
  },
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## 🔐 Authentication Endpoints

### Login

**Endpoint**: `POST /api/v1/auth/login`
**Description**: User authentication

#### Request

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Response

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "role": "user"
  }
}
```

### Register

**Endpoint**: `POST /api/v1/auth/register`
**Description**: User registration

#### Request

```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

#### Response

```json
{
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user"
  },
  "message": "User created successfully"
}
```

## 📊 Monitoring Endpoints

### Metrics

**Endpoint**: `GET /metrics`
**Description**: Prometheus metrics

#### Response

```
# HELP requests_total Total number of requests
# TYPE requests_total counter
requests_total{service="tokenguard"} 150
requests_total{service="trustguard"} 120

# HELP request_duration_seconds Request duration
# TYPE request_duration_seconds histogram
request_duration_seconds_bucket{le="0.1"} 100
request_duration_seconds_bucket{le="0.5"} 200
```

## 🚨 Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid service_type provided",
    "details": {
      "field": "service_type",
      "expected": "tokenguard|trustguard|contextguard|biasguard|securityguard|healthguard",
      "received": "invalid_service"
    }
  },
  "request_id": "uuid",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Common Error Codes

- `VALIDATION_ERROR` - Request validation failed
- `SERVICE_UNAVAILABLE` - Guard service not available
- `AUTHENTICATION_ERROR` - Invalid or missing authentication
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `INTERNAL_ERROR` - Server internal error

## 🔄 Rate Limiting

### Limits

- **Per User**: 100 requests/minute
- **Per IP**: 1000 requests/minute
- **Per Service**: 500 requests/minute

### Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248600
```

## 📝 Examples

### Complete Integration Example

```javascript
// Frontend integration example
const response = await fetch('http://localhost:8000/api/v1/guards/process', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    service_type: 'tokenguard',
    payload: {
      text: 'Your content here',
      max_tokens: 1000
    },
    user_id: 'user-123',
    session_id: 'session-456'
  })
});

const result = await response.json();
console.log(result.data.result);
```

### Python Integration Example

```python
import requests

# API call
response = requests.post(
    'http://localhost:8000/api/v1/guards/process',
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    },
    json={
        'service_type': 'trustguard',
        'payload': {
            'text': 'Content to validate',
            'trust_threshold': 0.8
        },
        'user_id': 'user-123',
        'session_id': 'session-456'
    }
)

result = response.json()
print(result['data']['trust_score'])
```
