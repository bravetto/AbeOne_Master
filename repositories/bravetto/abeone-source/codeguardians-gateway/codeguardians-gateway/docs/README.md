# CodeGuardians Gateway Documentation

##  Documentation Structure

This documentation is organized for different types of engineers:

###  For Backend Engineers
- **[API Reference](api/README.md)** - Complete API documentation with endpoints, request/response formats
- **[Guard Services](guard-services/README.md)** - Individual guard service documentation
- **[Architecture](architecture/README.md)** - System architecture and design patterns

###  For DevOps Engineers  
- **[DEVOPS_GUIDE.md](../../DEVOPS_GUIDE.md)** - Production deployment, AWS setup, secrets management
- **[Architecture](architecture/README.md)** - Infrastructure and deployment architecture

###  For Frontend Engineers
- **[API Reference](api/README.md)** - API endpoints and integration examples
- **[Guard Services](guard-services/README.md)** - Service capabilities and use cases

###  For QA Engineers
- **[API Reference](api/README.md)** - Testing endpoints and expected responses
- **[Guard Services](guard-services/README.md)** - Service behavior and test scenarios

##  Quick Start

### API Endpoint
```
POST http://localhost:8000/api/v1/guards/process
```

### Basic Request
```json
{
  "service_type": "tokenguard",
  "payload": {"text": "Your content here"},
  "user_id": "user-123",
  "session_id": "session-456"
}
```

### Health Checks
- **Live**: `GET /health/live`
- **Ready**: `GET /health/ready`
- **Services**: `GET /api/v1/guards/services`

##  Available Guard Services

| Service | Port | Purpose | Endpoint |
|---------|------|---------|----------|
| **TokenGuard** | 8001 | Token optimization & security | `/api/v1/optimize` |
| **TrustGuard** | 8002 | Trust validation & reliability | `/api/v1/trust` |
| **ContextGuard** | 8003 | Context analysis & drift detection | `/api/v1/context` |
| **BiasGuard** | 8004 | Bias detection & mitigation | `/api/v1/bias` |
| **SecurityGuard** | 8005 | Security scanning & threat detection | `/api/v1/security` |
| **HealthGuard** | 8005 | Health monitoring & validation | `/api/v1/health` |

##  External Documentation

- **[USER_GUIDE.md](../../USER_GUIDE.md)** - End-user documentation
- **[DEV_HANDOFF.md](../../DEV_HANDOFF.md)** - Developer setup and handoff
- **[DEVOPS_GUIDE.md](../../DEVOPS_GUIDE.md)** - Production deployment guide