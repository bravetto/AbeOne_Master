# Guard Services Overview

**Complete Guide to AIGuardian Guard Services Architecture and Implementation**

---

##  Executive Summary

AIGuardian provides intelligent AI protection through **5 specialized guard services** that work together to ensure AI reliability, security, and performance. This document provides a comprehensive overview of all guard services, their capabilities, and integration patterns.

**Services Overview:**
- **TokenGuard**: Cost optimization and token management
- **TrustGuard**: AI reliability pattern detection
- **ContextGuard**: Context drift detection and memory management
- **BiasGuard**: Bias detection and content analysis
- **HealthGuard**: Health monitoring and validation

---

##  Architecture Overview

### Service Architecture

```

                    AIGUARDIAN ECOSYSTEM                     
                                                             
               
   TOKEN GUARD    TRUST GUARD    CONTEXT              
   (Port 8001)    (Port 8002)    GUARD                
                                 (Port 8003)          
   • Cost Opt.    • Reliability   • Drift Det.         
   • Chunking     • Validation   • Memory            
           
                                                         
                         
                                                           
                               
   BIAS GUARD                       HEALTH GUARD         
   (Port 8004)                      (Port 8006)          
                                                         
   • Detection                      • Monitoring         
   • Mitigation                     • Validation         
                               
                                                           
                                                           
     
                   API GATEWAY                            
                   (Port 8000)                            
                                                          
   • Single Endpoint: /api/v1/guards/process             
   • Load Balancing • Rate Limiting • Auth               
     

```

### Integration Patterns

All guard services integrate through the **unified API gateway** using a consistent interface:

```json
{
  "service_type": "tokenguard|trustguard|contextguard|biasguard|healthguard",
  "payload": {
    // Service-specific payload
  },
  "user_id": "optional-user-identifier",
  "session_id": "optional-session-identifier"
}
```

---

##  Individual Guard Services

### 1. TokenGuard (Port 8001)

**Purpose:** Intelligent token cost optimization and management for AI interactions.

**Key Features:**
- **Cost Optimization**: Multiple strategies to reduce token usage while maintaining quality
- **Intelligent Chunking**: Smart text segmentation for optimal API processing
- **Summarization**: Content compression preserving key information
- **Caching**: Intelligent response caching to avoid redundant processing
- **Rate Limiting**: Built-in rate limiting for API protection
- **Monitoring**: Prometheus metrics integration for performance tracking

**Primary Use Cases:**
- Reducing API costs for high-volume AI applications
- Optimizing token usage for long-form content processing
- Implementing intelligent caching strategies
- Managing rate limits across multiple AI providers

**API Endpoints:**
- `POST /v1/analyze` - Token analysis and optimization
- `POST /v1/cost-estimate` - Cost estimation for content
- `GET /v1/metrics` - Token usage metrics
- `GET /health` - Service health check

**Response Format:**
```json
{
  "optimized_tokens": 150,
  "cost_savings": 0.3,
  "confidence_score": 0.95,
  "processing_time": 0.123
}
```

---

### 2. TrustGuard (Port 8002)

**Purpose:** AI reliability service detecting and mitigating seven critical AI failure patterns.

**Failure Patterns Detected:**
1. **Hallucination**: False information presented as fact
2. **Drift**: Loss of conversational coherence and consistency
3. **Bias**: Systematic prejudices in responses or recommendations
4. **Deception**: Intentional misleading or incomplete information
5. **Security Theater**: False sense of security without real protection
6. **Duplication**: Repetitive or redundant responses
7. **Stub Syndrome**: Inadequate or superficial responses

**Key Features:**
- **Mathematical Validation**: KL divergence, uncertainty quantification, statistical analysis
- **Constitutional Prompting**: Automated mitigation strategies and enhancement techniques
- **Enterprise Security**: API key authentication, JWT tokens, RBAC, audit logging
- **Real-time Monitoring**: Prometheus metrics, health checks, distributed tracing
- **Production Ready**: Comprehensive error handling and observability

**Primary Use Cases:**
- Ensuring AI response reliability in production environments
- Detecting and mitigating AI hallucinations
- Maintaining conversational consistency
- Implementing constitutional AI guidelines

**API Endpoints:**
- `POST /v1/detect` - Pattern detection in AI responses
- `POST /v1/validate` - Comprehensive validation with mathematical analysis
- `POST /v1/mitigate` - Apply mitigation strategies
- `POST /v1/constitutional` - Generate constitutional prompts
- `GET /v1/metrics` - Service metrics and pattern statistics
- `GET /health` - Service health check

**Response Format:**
```json
{
  "patterns_detected": {
    "hallucination": {
      "score": 0.85,
      "confidence": 0.92,
      "evidence": ["overconfidence language", "specific numbers without context"],
      "risk_level": "high"
    }
  },
  "overall_risk": "high",
  "mitigation_suggestions": [
    "Add uncertainty qualifiers",
    "Implement fact-checking protocols"
  ],
  "processing_time": 0.156
}
```

---

### 3. ContextGuard (Port 8003)

**Purpose:** Context drift detection and memory management for AI conversations.

**Key Features:**
- **Context Drift Detection**: Monitors conversation coherence and topic consistency
- **Memory Management**: Intelligent memory allocation and cleanup
- **Session Tracking**: Maintains conversation state across interactions
- **Drift Mitigation**: Automatic correction of context drift issues
- **Performance Monitoring**: Memory usage and processing efficiency tracking

**Primary Use Cases:**
- Maintaining conversation coherence in chat applications
- Preventing context drift in long-form AI interactions
- Optimizing memory usage for scalable AI services
- Ensuring consistent AI behavior across sessions

**API Endpoints:**
- `POST /gateway` - Context processing and drift detection
- `POST /analyze` - Context analysis and memory management
- `GET /health` - Service health check

**Response Format:**
```json
{
  "action": "processed",
  "key": "session123",
  "value": "context_data",
  "drift_detected": false,
  "memory_usage": 0.75,
  "processing_time": 0.089
}
```

---

### 4. BiasGuard (Port 8004)

**Purpose:** Bias detection and mitigation in AI-generated content.

**Key Features:**
- **Multi-layered Detection**: Statistical analysis, machine learning, and signature-based methods
- **Advanced Mitigation**: Flagging, sanitizing, and redacting biased content
- **Pluggable Architecture**: Custom plugins for specialized bias detection
- **Structured Logging**: Detailed auditing of all analysis and mitigation actions
- **Comprehensive Reporting**: Security incidents, performance, and model health reports
- **Configurable Analysis**: Keyword lists, content limits, and detection model customization

**Primary Use Cases:**
- Detecting biased content in AI-generated responses
- Implementing content moderation for AI applications
- Ensuring fairness and inclusivity in AI outputs
- Compliance with content standards and regulations

**API Endpoints:**
- `POST /v1/process` - Bias detection and analysis
- `GET /health` - Service health check

**Response Format:**
```json
{
  "operation": "detect_bias",
  "result": {
    "bias_detected": true,
    "bias_types": ["political", "cultural"],
    "confidence": 0.87,
    "mitigation_applied": "content_filtered"
  },
  "processing_time": 0.145
}
```

---

### 5. HealthGuard (Port 8006)

**Purpose:** Health monitoring and validation for AI services and infrastructure.

**Key Features:**
- **Service Health Monitoring**: Continuous health checks for all AI services
- **Performance Validation**: Response time and throughput monitoring
- **Resource Monitoring**: CPU, memory, and system resource tracking
- **Automated Alerts**: Health degradation and failure notifications
- **Historical Analysis**: Trend analysis and predictive health monitoring
- **Integration Validation**: Cross-service dependency checking

**Primary Use Cases:**
- Monitoring AI service health and performance
- Detecting service degradation before failures
- Ensuring high availability of AI infrastructure
- Performance optimization and capacity planning

**API Endpoints:**
- `POST /analyze` - Health analysis and monitoring
- `GET /health` - Service health check
- `GET /metrics` - Health and performance metrics

**Response Format:**
```json
{
  "samples": [
    {
      "id": "sample1",
      "content": "health_check_data",
      "metadata": {
        "response_time": 0.123,
        "cpu_usage": 0.45,
        "memory_usage": 0.67
      }
    }
  ],
  "overall_health": "healthy",
  "processing_time": 0.056
}
```

---

##  Service Integration

### Unified API Gateway

All guard services integrate through a single API gateway endpoint:

```bash
POST http://localhost:8000/api/v1/guards/process
```

**Request Format:**
```json
{
  "service_type": "tokenguard|trustguard|contextguard|biasguard|healthguard",
  "payload": {
    // Service-specific payload structure
  },
  "user_id": "optional-user-id",
  "session_id": "optional-session-id"
}
```

**Response Format:**
```json
{
  "status": "success|error",
  "service": "service_name",
  "result": {
    // Service-specific response data
  },
  "processing_time": 0.123,
  "timestamp": "2025-11-01T12:00:00Z"
}
```

### Service Discovery

The gateway provides automatic service discovery:

```bash
GET http://localhost:8000/api/v1/guards/services
```

**Response:**
```json
{
  "services": {
    "tokenguard": {
      "port": 8001,
      "status": "healthy",
      "version": "1.0.0",
      "endpoints": ["/v1/analyze", "/v1/cost-estimate", "/health"]
    },
    "trustguard": {
      "port": 8002,
      "status": "healthy",
      "version": "2.1.0",
      "endpoints": ["/v1/detect", "/v1/validate", "/v1/mitigate", "/health"]
    }
    // ... other services
  }
}
```

---

##  Development and Deployment

### Local Development

1. **Clone Repository:**
```bash
git clone <repository-url>
cd AIGuards-Backend-1
```

2. **Start Services:**
```bash
# Start all services
docker-compose up -d

# Or start individual services
docker-compose up tokenguard trustguard contextguard biasguard healthguard -d
```

3. **Verify Health:**
```bash
# Check all services
curl http://localhost:8000/api/v1/guards/services

# Test individual services
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8006/health
```

### Production Deployment

1. **Configure Environment:**
```bash
# Set required environment variables
export TRUSTGUARD_API_KEY="your-api-key"
export AWS_REGION="us-east-1"
# ... other service configurations
```

2. **Deploy Services:**
```bash
# Using docker-compose for production
docker-compose -f docker-compose.prod.yml up -d

# Or use deployment scripts
./scripts/deploy.sh prod
```

3. **Health Monitoring:**
```bash
# Enable monitoring
curl http://localhost:8000/api/v1/guards/health

# Check service metrics
curl http://localhost:8000/metrics
```

---

##  Performance Characteristics

### Response Times (Typical)
- **TokenGuard**: < 50ms for optimization analysis
- **TrustGuard**: < 200ms for pattern detection
- **ContextGuard**: < 100ms for context processing
- **BiasGuard**: < 150ms for bias analysis
- **HealthGuard**: < 50ms for health checks

### Resource Requirements
- **CPU**: 0.5-1.0 vCPU per service
- **Memory**: 512MB-1GB per service
- **Storage**: 20GB base + variable for logs/metrics
- **Network**: < 10Mbps typical usage

### Scalability
- **Concurrent Requests**: Support for 1000+ concurrent users
- **Auto-scaling**: Configurable based on CPU/memory metrics
- **Load Balancing**: Built-in through API gateway
- **High Availability**: Multi-instance deployment support

---

##  Security and Compliance

### Authentication
- **Service-to-Service**: Automatic authentication via gateway
- **API Keys**: Configurable authentication for direct access
- **JWT Tokens**: Support for user-based authentication
- **Rate Limiting**: Configurable request throttling

### Data Protection
- **Encryption**: TLS/SSL for all service communications
- **Input Validation**: Comprehensive payload validation
- **Audit Logging**: Detailed request/response logging
- **Compliance**: GDPR, SOC2 compliance support

### Access Control
- **RBAC**: Role-based access control for enterprise features
- **API Permissions**: Granular permission management
- **Network Security**: VPC and security group configurations
- **Monitoring**: Security event logging and alerting

---

##  Troubleshooting

### Common Issues

**Service Unavailable:**
```bash
# Check service status
docker-compose ps

# View service logs
docker-compose logs tokenguard

# Restart service
docker-compose restart tokenguard
```

**High Latency:**
```bash
# Check resource usage
docker stats

# Review metrics
curl http://localhost:8000/metrics

# Optimize configuration
# Adjust rate limits, timeouts, resource allocation
```

**Authentication Errors:**
```bash
# Verify API keys
echo $TRUSTGUARD_API_KEY

# Check gateway configuration
curl http://localhost:8000/api/v1/guards/services

# Review service logs for auth failures
```

### Health Checks

**Automated Monitoring:**
```bash
# Enable health monitoring
curl http://localhost:8000/api/v1/guards/health

# Individual service health
curl http://localhost:8001/health
curl http://localhost:8002/health
# ... etc
```

**Manual Testing:**
```bash
# Test unified endpoint
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "test content"}
  }'
```

---

##  Documentation Resources

### Service-Specific Documentation
- **[TokenGuard Details](guards/tokenguard/README.md)** - Complete TokenGuard documentation
- **[TrustGuard Architecture](guards/trust-guard/README.md)** - TrustGuard implementation guide
- **[ContextGuard Guide](guards/contextguard/)** - ContextGuard usage documentation
- **[BiasGuard Manual](guards/biasguard-backend/README.md)** - BiasGuard configuration guide
- **[HealthGuard Reference](guards/healthguard/README.md)** - HealthGuard monitoring guide

### Integration Guides
- **[API Reference](api/README.md)** - Complete API endpoint documentation
- **[Integration Guide](docs/INTEGRATION_GUIDE.md)** - Service integration patterns
- **[Deployment Guide](docs/DEVOPS_GUIDE.md)** - Production deployment instructions

### Development Resources
- **[Testing Report](docs/TESTING_REPORT.md)** - Comprehensive testing documentation
- **[Fixes and Changes](docs/FIXES_AND_CHANGES.md)** - Change history and fixes
- **[Root Cause Analysis](docs/ROOT_CAUSE_ANALYSIS.md)** - Technical issue analysis

---

##  Next Steps

### For Users
1. **Quick Start**: Follow the [Getting Started Guide](docs/GETTING_STARTED.md)
2. **API Integration**: Use the unified gateway endpoint
3. **Monitoring**: Set up health monitoring and alerting

### For Developers
1. **Service Development**: Follow individual service documentation
2. **Integration Testing**: Use the comprehensive test suite
3. **Performance Optimization**: Monitor and tune service configurations

### For DevOps
1. **Production Deployment**: Use provided deployment scripts
2. **Monitoring Setup**: Configure Prometheus and Grafana
3. **Security Configuration**: Implement proper authentication and access control

---

**This overview provides the foundation for understanding and working with AIGuardian's guard services. Each service has extensive documentation available in its respective directory for detailed implementation guidance.**

*Last Updated: November 2025*
