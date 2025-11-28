# AIGuardian User Guide

**Simple API Usage • Quick Start • Examples**

---

## 🚀 Quick Start

### 1. Start the System
```bash
cd codeguardians-gateway/codeguardians-gateway
docker-compose up -d
```

### 2. Test the System
```bash
curl -X GET http://localhost:8000/health/live
```

### 3. Use the API
```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "Your content here"},
    "user_id": "user-123",
    "session_id": "session-456"
  }'
```

## 🌐 API Endpoint

**Single endpoint for everything:**
```
POST http://localhost:8000/api/v1/guards/process
```

## 🛡️ Available Guard Services

- **tokenguard** - Token optimization & security
- **trustguard** - Trust validation & reliability  
- **contextguard** - Context analysis & drift detection
- **biasguard** - Bias detection & mitigation
- **securityguard** - Security scanning & threat detection
- **healthguard** - Health monitoring & validation

## 📋 Request Format

```json
{
  "service_type": "tokenguard|trustguard|contextguard|biasguard|securityguard|healthguard",
  "payload": {
    "text": "Your content to analyze"
  },
  "user_id": "your-user-id",
  "session_id": "your-session-id"
}
```

## 📊 Response Format

```json
{
  "request_id": "uuid",
  "service_type": "tokenguard",
  "success": true,
  "data": {
    "result": "analysis result"
  },
  "error": null,
  "processing_time": 0.123,
  "service_used": "tokenguard"
}
```

## 🔧 Health Endpoints

- **Live**: `GET http://localhost:8000/health/live`
- **Ready**: `GET http://localhost:8000/health/ready`
- **Services**: `GET http://localhost:8000/api/v1/guards/services`
- **Docs**: `GET http://localhost:8000/docs`

## 🛑 Stop the System

```bash
cd codeguardians-gateway/codeguardians-gateway
docker-compose down
```

## 🧠 Context Drift Handling

AIGuardian automatically handles context drift through the ContextGuard service:

```json
{
  "service_type": "contextguard",
  "payload": {
    "text": "Your content",
    "context_window": 1024,
    "memory_limit": 2048,
    "drift_threshold": 0.1
  },
  "user_id": "user-123",
  "session_id": "session-456"
}
```

**Context Drift Response:**
```json
{
  "data": {
    "drift_detected": true,
    "drift_score": 0.85,
    "context_coherence": 0.15,
    "recommended_action": "redirect_to_original_topic",
    "suggested_response": "Let's get back to discussing..."
  }
}
```

That's it! AIGuardian provides intelligent AI protection through a single, simple API endpoint.
