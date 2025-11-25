# Guard Services Documentation

##  Guard Services Overview

The CodeGuardians Gateway orchestrates 6 specialized AI guard services, each providing specific protection capabilities.

##  Service Matrix

| Service | Internal Port | Directory | Purpose | Access Method |
|---------|---------------|-----------|---------|---------------|
| **TokenGuard** | 8001 | `security-guard/` | Token optimization & security | Via Gateway |
| **TrustGuard** | 8002 | `validation-systems/` | Trust validation & reliability | Via Gateway |
| **ContextGuard** | 8003 | `consciousness-core/` | Context analysis & drift detection | Via Gateway |
| **BiasGuard** | 8004 | `neuromorphic-integration/` | Bias detection & mitigation | Via Gateway |
| **SecurityGuard** | 8005 | `security-guard/` | Security scanning & threat detection | Via Gateway |
| **HealthGuard** | 8005 | `guardians/validation-framework/` | Health monitoring & validation | Via Gateway |

** Important**: Ports are internal Docker network only. All services are accessed via the unified gateway at `POST /api/v1/guards/process`.

##  Service Architecture

### Common Service Structure
```
service-directory/
 main.py              # FastAPI application
 Dockerfile           # Container definition
 requirements.txt     # Python dependencies
 service-module/      # Service-specific code
     __init__.py
     core.py          # Core service logic
     models.py        # Data models
```

### Service Communication
- **Internal Network**: Services communicate via Docker internal network
- **Health Checks**: Each service exposes `/health` endpoint
- **API Gateway**: All external requests go through the gateway
- **Load Balancing**: Gateway handles service discovery and load balancing

##  Individual Service Documentation

### 1. TokenGuard (Port 8001)
**Purpose**: AI token cost optimization and intelligent pruning

:warning: **Internal Service - Access via Gateway Only** \\
Direct access not available (no exposed ports). Use `POST /api/v1/guards/process` with `service_type: "tokenguard"`

#### Capabilities
- **Token Pruning**: Remove unnecessary tokens while preserving meaning
- **Cost Optimization**: Reduce API costs by up to 40%
- **Security Scanning**: Detect and remove sensitive information
- **Compression**: Intelligent text compression

#### Gateway Request Format
```json
{
  "service_type": "tokenguard",
  "payload": {
    "text": "Your content to optimize",
    "max_tokens": 1000,
    "optimization_level": "aggressive"
  },
  "user_id": "user-123",
  "session_id": "session-456"
}
```


#### Response Format
```json
{
  "optimized_text": "Optimized content",
  "original_token_count": 200,
  "optimized_token_count": 150,
  "reduction_percentage": 25.0,
  "optimization_techniques": ["pruning", "compression", "summarization"],
  "confidence_score": 0.95
}
```

#### Use Cases
- **Content Optimization**: Reduce token usage for API calls
- **Cost Management**: Lower AI API costs
- **Security**: Remove sensitive information before processing

### 2. TrustGuard (Port 8002)
**Purpose**: AI reliability service with 7 failure pattern detection

:warning: **Internal Service - Access via Gateway Only** \\
Direct access not available (no exposed ports). Use `POST /api/v1/guards/process` with `service_type: "trustguard"`

#### Capabilities
- **Factual Accuracy**: Verify factual claims
- **Source Credibility**: Assess information sources
- **Consistency Checking**: Detect contradictions
- **Reliability Scoring**: Overall trustworthiness assessment

#### Gateway Request Format
```json
{
  "service_type": "trustguard",
  "payload": {
    "text": "Content to validate",
    "trust_threshold": 0.8,
    "validation_level": "basic"
  },
  "user_id": "user-123",
  "session_id": "session-456"
}
```

#### Response Format
```json
{
  "trust_score": 0.85,
  "reliability": "high|medium|low",
  "validation_results": {
    "factual_accuracy": 0.9,
    "source_credibility": 0.8,
    "consistency": 0.85,
    "bias_detection": 0.2
  },
  "failure_patterns": ["unverified_claims", "contradictions"],
  "confidence_interval": [0.8, 0.9]
}
```

#### Use Cases
- **Content Verification**: Validate information accuracy
- **Source Assessment**: Evaluate information sources
- **Quality Control**: Ensure content reliability

### 3. ContextGuard (Port 8003)
**Purpose**: Advanced context drift detection and management

:warning: **Internal Service - Access via Gateway Only** \\
Direct access not available (no exposed ports). Use `POST /api/v1/guards/process` with `service_type: "contextguard"`

#### Capabilities
- **Context Drift Detection**: Identify when conversation drifts
- **Memory Management**: Manage context windows efficiently
- **Coherence Analysis**: Assess context coherence
- **Drift Mitigation**: Provide corrective suggestions

#### Gateway Request Format
```json
{
  "service_type": "contextguard",
  "payload": {
    "text": "Current content",
    "context_window": 1024,
    "drift_threshold": 0.1
  },
  "user_id": "user-123",
  "session_id": "session-456"
}
```

#### Response Format
```json
{
  "drift_detected": true,
  "drift_score": 0.85,
  "context_coherence": 0.15,
  "drift_type": "topic_shift|semantic_drift|temporal_drift",
  "recommended_action": "redirect_to_original_topic|continue|clarify",
  "suggested_response": "Let's get back to discussing...",
  "context_preservation": 0.3
}
```

#### Use Cases
- **Conversation Management**: Maintain conversation focus
- **Context Preservation**: Keep relevant context
- **Drift Prevention**: Prevent off-topic discussions

### 4. BiasGuard (Port 8004)
**Purpose**: Bias detection and mitigation

:warning: **Internal Service - Access via Gateway Only** \\
Direct access not available (no exposed ports). Use `POST /api/v1/guards/process` with `service_type: "biasguard"`

#### Capabilities
- **Demographic Bias**: Detect demographic bias
- **Content Bias**: Identify biased content
- **Representation Analysis**: Assess representation fairness
- **Mitigation Suggestions**: Provide bias reduction recommendations

#### Gateway Request Format
```json
{
  "service_type": "biasguard",
  "payload": {
    "text": "Content to analyze",
    "bias_types": ["demographic", "content"],
    "mitigation_level": "moderate"
  },
  "user_id": "user-123",
  "session_id": "session-456"
}
```

#### Response Format
```json
{
  "bias_detected": true,
  "bias_score": 0.7,
  "bias_types": ["demographic", "content"],
  "bias_details": {
    "demographic_bias": 0.8,
    "content_bias": 0.6,
    "representation_bias": 0.3
  },
  "mitigation_suggestions": [
    "Use inclusive language",
    "Add diverse examples",
    "Remove gender-specific terms"
  ],
  "fairness_score": 0.3
}
```

#### Use Cases
- **Content Review**: Ensure unbiased content
- **Diversity Training**: Promote inclusive language
- **Fairness Assessment**: Evaluate content fairness

### 5. SecurityGuard (Port 8005)
**Purpose**: Security scanning and threat detection

:warning: **Internal Service - Access via Gateway Only** \\
Direct access not available (no exposed ports). Use `POST /api/v1/guards/process` with `service_type: "securityguard"`

#### Capabilities
- **Malware Detection**: Identify malicious content
- **Phishing Prevention**: Detect phishing attempts
- **Injection Scanning**: Find code injection attempts
- **Threat Assessment**: Overall security risk evaluation

#### Gateway Request Format
```json
{
  "service_type": "securityguard",
  "payload": {
    "text": "Content to scan",
    "scan_types": ["malware", "phishing"],
    "threat_level": "high"
  },
  "user_id": "user-123",
  "session_id": "session-456"
}
```

#### Response Format
```json
{
  "threats_detected": true,
  "threat_score": 0.8,
  "threat_types": ["phishing", "social_engineering"],
  "threat_details": {
    "malware_indicators": 0.2,
    "phishing_indicators": 0.9,
    "injection_attempts": 0.1,
    "social_engineering": 0.7
  },
  "recommendations": [
    "Remove suspicious links",
    "Verify sender identity",
    "Report to security team"
  ],
  "risk_level": "high"
}
```

#### Use Cases
- **Content Security**: Scan for malicious content
- **Threat Prevention**: Prevent security breaches
- **Risk Assessment**: Evaluate security risks

### 6. HealthGuard (Port 8005)
**Purpose**: Health monitoring and validation

:warning: **Internal Service - Access via Gateway Only** \\
Direct access not available (no exposed ports). Use `POST /api/v1/guards/process` with `service_type: "healthguard"`

#### Capabilities
- **Toxicity Detection**: Identify toxic content
- **Safety Validation**: Ensure content safety
- **Appropriateness**: Assess content appropriateness
- **Wellness Monitoring**: Monitor mental health indicators

#### Gateway Request Format
```json
{
  "service_type": "healthguard",
  "payload": {
    "text": "Content to monitor",
    "health_metrics": ["toxicity", "safety"],
    "monitoring_level": "comprehensive"
  },
  "user_id": "user-123",
  "session_id": "session-456"
}
```

#### Response Format
```json
{
  "health_score": 0.9,
  "toxicity_level": "low|medium|high",
  "safety_status": "safe|caution|unsafe",
  "appropriateness": "appropriate|questionable|inappropriate",
  "wellness_indicators": {
    "stress_indicators": 0.1,
    "anxiety_indicators": 0.2,
    "depression_indicators": 0.1
  },
  "recommendations": [
    "Content is appropriate for all audiences",
    "Consider adding trigger warnings",
    "Monitor for mental health concerns"
  ]
}
```

#### Use Cases
- **Content Moderation**: Ensure appropriate content
- **Safety Monitoring**: Protect users from harmful content
- **Wellness Support**: Monitor mental health indicators

##  Service Integration

### Service Discovery
The gateway automatically discovers services via health checks:
```python
# Service discovery logic
SERVICE_ENDPOINTS = {
    "tokenguard": "http://tokenguard:8001/api/v1/optimize",
    "trustguard": "http://trustguard:8002/api/v1/trust",
    "contextguard": "http://contextguard:8003/api/v1/context",
    "biasguard": "http://biasguard:8004/api/v1/bias",
    "securityguard": "http://securityguard:8005/api/v1/security",
    "healthguard": "http://healthguard:8005/api/v1/health"
}
```

### Health Monitoring
Each service exposes health endpoints:
- **Liveness**: `GET /health/live`
- **Readiness**: `GET /health/ready`
- **Metrics**: `GET /metrics`

### Circuit Breaker
Services implement circuit breaker pattern for fault tolerance:
- **Failure Threshold**: 5 consecutive failures
- **Recovery Timeout**: 30 seconds
- **Fallback**: Graceful degradation

##  Testing Services

### Health Check Commands
```bash
# Check individual services via gateway
curl http://localhost:8000/api/v1/guards/health/tokenguard
curl http://localhost:8000/api/v1/guards/health/trustguard
curl http://localhost:8000/api/v1/guards/health/contextguard
curl http://localhost:8000/api/v1/guards/health/biasguard
curl http://localhost:8000/api/v1/guards/health/securityguard
curl http://localhost:8000/api/v1/guards/health/healthguard
```

### Service Testing
```bash
# Test TokenGuard
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "test content"},
    "user_id": "test",
    "session_id": "test"
  }'
```

##  Service Metrics

### Performance Metrics
- **Response Time**: Average processing time per service
- **Throughput**: Requests per second
- **Error Rate**: Percentage of failed requests
- **Availability**: Service uptime percentage

### Business Metrics
- **Usage**: Service utilization rates
- **Cost**: Resource consumption
- **Quality**: Accuracy and reliability scores
- **User Satisfaction**: Feedback and ratings

##  Service Configuration

### Environment Variables
Each service can be configured via environment variables:
```bash
# Common variables
PORT=8001
LOG_LEVEL=INFO
DEBUG=false
MAX_WORKERS=4

# Service-specific variables
TOKEN_OPTIMIZATION_LEVEL=moderate
TRUST_THRESHOLD=0.8
CONTEXT_WINDOW_SIZE=1024
BIAS_DETECTION_SENSITIVITY=0.7
SECURITY_SCAN_DEPTH=comprehensive
HEALTH_MONITORING_LEVEL=basic
```

### Service Scaling
Services can be scaled independently:
```yaml
# Docker Compose scaling
services:
  tokenguard:
    deploy:
      replicas: 3
  trustguard:
    deploy:
      replicas: 2
  contextguard:
    deploy:
      replicas: 1
```

This documentation provides comprehensive information about each guard service, their capabilities, and how to integrate with them.
