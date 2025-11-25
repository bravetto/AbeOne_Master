# AIGuardian Developer Guide

**Complete Development Setup • Testing • Contribution Guidelines**

---

##  Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Git
- VS Code (recommended)

### 1. Clone & Setup

```bash
git clone <repository-url>
cd AIGuards-Backend-1
```

### 2. Start Development Environment

```bash
# Navigate to gateway
cd codeguardians-gateway/codeguardians-gateway

# Start all services
docker-compose up -d

# Wait for services to be healthy
sleep 30

# Verify everything is working
curl http://localhost:8000/health/live
```

### 3. Access Development Tools

- **API Gateway**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Checks**: http://localhost:8000/health/live
- **PostgreSQL**: localhost:5433 (user: `codeguardians-gateway`, REPLACE_ME
- **Redis**: localhost:6380 (REPLACE_ME

---

##  System Architecture

### Core Components

```

                    AIGUARDIAN ECOSYSTEM                     
                                                             
               
   TOKEN GUARD    TRUST GUARD    CONTEXT              
   (Port 8001)    (Port 8002)    GUARD                
                                 (Port 8003)          
           
                                                         
                         
                                                           
               
   BIAS GUARD     SECURITY       HEALTH GUARD         
   (Port 8004)    GUARD          (Port 8005)          
                  (Port 8005)                         
               
                                                           
                                                           
     
                   API GATEWAY                            
                   (Port 8000)                            
                                                          
   • Single Endpoint: /api/v1/guards/process             
   • Load Balancing • Rate Limiting • Auth               
     

```

### Guard Services

| Service                 | Port | Purpose                                     | Directory                           |
| ----------------------- | ---- | ------------------------------------------- | ----------------------------------- |
| **TokenGuard**    | 8001 | Token optimization & cost management        | `guards/tokenguard/`              |
| **TrustGuard**    | 8002 | Trust validation & reliability              | `guards/trust-guard/`             |
| **ContextGuard**  | 8003 | Context drift detection & memory management | `guards/contextguard/`            |
| **BiasGuard**     | 8004 | Bias detection & content analysis           | `guards/biasguard-backend/`       |
| **HealthGuard**   | 8005 | Health monitoring & validation              | `guards/healthguard/`             |

---

##  Service Communication Architecture

### Docker Internal Networking
The CodeGuardians system uses Docker's internal networking for secure, efficient service-to-service communication:

#### Network Topology
```
    
   External             Gateway       
   Clients          (Port 8000)   
    
                              
                               Internal Docker Network
                               (No external exposure)
                              

  TokenGuard        TrustGuard      ContextGuard      BiasGuard      
   (8001)            (8002)           (8003)           (8004)        


 SecurityGuard     HealthGuard    
    (8005)           (8005)       

```

#### Communication Flow
1. **External Request** → Gateway (Port 8000)
2. **Gateway Processing** → Authentication, Rate Limiting, Routing
3. **Internal Routing** → Docker Network to Target Service
4. **Service Processing** → Business Logic Execution
5. **Response Flow** → Service → Gateway → Client

### Security Benefits
- **No External Exposure**: Guard services have no public ports
- **Network Isolation**: Services communicate only within Docker network
- **Gateway Security**: Single entry point for all security measures
- **Failover Protection**: Gateway handles service failures gracefully

### Development Considerations
- **Local Testing**: Use `docker-compose` for full network simulation
- **Service Discovery**: Gateway automatically discovers healthy services
- **Health Monitoring**: Continuous health checks via internal endpoints
- **Load Balancing**: Gateway distributes load across service instances

### Configuration
Services are configured with internal network addresses:
```python
# Service discovery (internal addresses)
SERVICE_ENDPOINTS = {
    "tokenguard": "http://tokenguard:8001/api/v1/optimize",
    "trustguard": "http://trustguard:8002/api/v1/trust",
    # ... etc
}
```

---

##  Development Setup

### Environment Configuration

Create `env.unified` file in `codeguardians-gateway/codeguardians-gateway/`:

```bash
# Database
POSTGRES_REPLACE_ME
DATABASE_URL=postgresql+asyncpg://codeguardians-gateway:postgres-password-dev@postgres:5432/codeguardians-gateway_db

# Redis
REDIS_REPLACE_ME
REDIS_URL=REPLACE_MEredis:6379/0

# Security
SECRET_KEY=your-32-char-secret-key-minimum
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

### Key Development Files

```
codeguardians-gateway/codeguardians-gateway/
 app/
    main.py                    # FastAPI application
    api/v1/guards.py          # Unified guard API endpoint
    core/guard_orchestrator.py # Service routing logic
 docker-compose.yml            # Complete system orchestration
 Dockerfile                    # Gateway container
 requirements.txt             # Python dependencies
```

---

##  Testing

### Comprehensive Testing Suite

The test suite has been completely reorganized and enhanced with comprehensive coverage:

#### **Smoke Tests** (`tests/smoke/`) - Quick Validation (< 5s)
- `test_smoke_health.py` - Critical health endpoints validation
- `test_smoke_guards.py` - Guard service connectivity checks
- `test_smoke_api.py` - Core API endpoint validation

#### **Unit Tests** (`tests/unit/`) - Component Testing
- `test_guard_orchestrator.py` - Orchestrator logic and circuit breaker
- `test_models.py` - Database model validation
- `test_payload_transformation.py` - Payload transformation logic

#### **Integration Tests** (`tests/integration/`) - Full Service Testing
- `test_guard_services.py` - Comprehensive guard service testing
- `test_guard_metrics.py` - Metrics validation and statistics
- `test_edge_cases.py` - Edge cases and error handling

#### **Test Environment Configuration**
- **Database**: In-memory SQLite (isolated per test)
- **Redis**: Mocked (no external dependencies)
- **Guard Services**: Live services for integration tests
- **HTTP Client**: Async httpx for all requests

### Quick Health Check

```bash
# Test all services
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready
curl http://localhost:8000/api/v1/guards/services
```

### Running Tests

#### **Smoke Tests** (Quick Validation)
```bash
cd codeguardians-gateway/codeguardians-gateway
pytest -m smoke -v
```

#### **Unit Tests** (Fast, No Dependencies)
```bash
pytest -m unit -v
# Or specific files:
pytest tests/unit/test_guard_orchestrator.py -v
```

#### **Integration Tests** (Requires Running Services)
```bash
# Start services first
docker-compose up -d
sleep 30

# Run integration tests
pytest -m integration -v
# Or specific test files:
pytest tests/integration/test_guard_services.py -v
```

#### **Edge Case Tests** (Error Handling)
```bash
pytest -m edge_case -v
```

#### **Guard Metrics Tests** (Metrics Validation)
```bash
pytest -m guard_metrics -v
```

#### **Full Test Suite** (All Tests)
```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term
```

#### **Test Categories by Marker**
```bash
# Run only smoke tests
pytest -m smoke

# Run smoke and unit tests
pytest -m "smoke or unit"

# Run all except slow tests
pytest -m "not slow"

# Run specific test class
pytest tests/integration/test_guard_services.py::TestTokenGuard -v
```

### API Testing

```bash
# Test unified guard endpoint
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "test content"},
    "user_id": "test-user",
    "session_id": "test-session"
  }'
```

### Comprehensive Testing

```bash
# Run full test suite
cd codeguardians-gateway/codeguardians-gateway
python scripts/test_all_endpoints.py --base-url http://localhost:8000

# Test individual components
docker exec codeguardians-gateway-postgres psql -U codeguardians-gateway -d codeguardians-gateway_db -c "SELECT version();"
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev ping
```

#### Load Testing

```bash
# Simple load test
ab -n 100 -c 10 http://localhost:8000/health/live
```

### Test Categories Explained

| Test Category | Marker | Duration | Dependencies | Purpose |
|---------------|--------|----------|--------------|---------|
| **Smoke Tests** | `smoke` | < 5s | None | Quick validation of critical functionality |
| **Unit Tests** | `unit` | < 1s each | None | Component-level testing |
| **Integration Tests** | `integration` | 1-30s each | Live Services | Full service integration testing |
| **Edge Case Tests** | `edge_case` | 1-10s each | Live Services | Error handling and unusual inputs |
| **Guard Metrics Tests** | `guard_metrics` | 1-5s each | Live Services | Metrics validation and statistics |
| **Slow Tests** | `slow` | > 1s each | Varies | Performance and load testing |

### Test Files Overview

| File | Category | Tests | Purpose |
|------|----------|-------|---------|
| `tests/smoke/test_smoke_health.py` | Smoke | 10 | Health endpoint validation |
| `tests/smoke/test_smoke_guards.py` | Smoke | 12 | Guard service connectivity |
| `tests/smoke/test_smoke_api.py` | Smoke | 15 | Core API endpoint testing |
| `tests/unit/test_guard_orchestrator.py` | Unit | 20+ | Orchestrator and circuit breaker |
| `tests/integration/test_guard_services.py` | Integration | 25+ | Comprehensive guard testing |
| `tests/integration/test_guard_metrics.py` | Integration | 20+ | Metrics validation |
| `tests/integration/test_edge_cases.py` | Edge Case | 30+ | Error handling and edge cases |

### Test Environment Setup

The test environment automatically configures:
- **Redis Mocking**: All Redis operations are mocked
- **Database Isolation**: Each test gets a fresh in-memory database
- **Cache Disabled**: No external cache dependencies
- **Rate Limiting Mocked**: No Redis required for rate limiting tests

### Troubleshooting Tests

#### **If Tests Fail with Redis Errors**
```bash
# Check if Redis mocking is working
pytest tests/test_payload_transformation.py -v -s
# Should show: "[OK] Redis: MOCKED"
```

#### **If Integration Tests Fail**
```bash
# Ensure services are running
docker-compose ps
curl http://localhost:8000/health/live

# Check service logs
docker-compose logs codeguardians-gateway
```

#### **If Enterprise/SaaS Tests Run (They Shouldn't)**
```bash
# These should be skipped by default
pytest tests/test_enterprise_api.py -v
# Should show: "SKIPPED - Enterprise features under development"
```

---

##  API Development

### Adding New Guard Service

1. **Create Service Structure**

```bash
mkdir new-guard-service
cd new-guard-service
touch main.py Dockerfile requirements.txt
```

2. **Service Template** (`main.py`)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NewGuard Service")

class ProcessRequest(BaseModel):
    text: str
    user_id: str
    session_id: str

@app.post("/api/v1/process")
async def process(request: ProcessRequest):
    # Your guard logic here
    return {
        "status": "success",
        "result": "processed",
        "confidence": 0.95
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

3. **Add to Docker Compose**

```yaml
# Add to docker-compose.yml
newguard-service:
  build: ./new-guard-service
  ports:
    - "8007:8007"
  environment:
    - PORT=8007
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8007/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

4. **Update Guard Orchestrator**

```python
# Add to app/core/guard_orchestrator.py
SERVICE_ENDPOINTS = {
    # ... existing services
    "newguard": "/api/v1/process"
}
```

---

##  Debugging & Troubleshooting

### Common Issues

#### Services Not Starting

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs codeguardians-gateway
docker-compose logs tokenguard

# Restart specific service
docker-compose restart tokenguard
```

#### Database Connection Issues

```bash
# Check PostgreSQL
docker exec codeguardians-gateway-postgres psql -U codeguardians-gateway -d codeguardians-gateway_db -c "SELECT 1;"

# Check Redis
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev ping
```

#### Port Conflicts

```bash
# Check what's using ports 8000-8005
netstat -tulpn | grep :8000
netstat -tulpn | grep :8001
# ... etc
```

### Debug Commands

```bash
# View live logs
docker-compose logs -f

# Check resource usage
docker stats

# Execute commands in containers
docker exec -it codeguardians-gateway-production bash
docker exec -it codeguardians-gateway-postgres psql -U codeguardians-gateway -d codeguardians-gateway_db
```

---

##  Configuration

### Development Override

Create `docker-compose.override.yml`:



```yaml
services:
  codeguardians-gateway:
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    volumes:
      - .:/app:ro  # Mount source for hot reload
```

### Service Configuration

Each guard service can be configured via environment variables:

- `PORT` - Service port (8001-8005)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `DEBUG` - Debug mode (true/false)

---

##  Monitoring & Logs

### Health Endpoints

- Gateway: `http://localhost:8000/health/live`
- Services: `http://localhost:8000/api/v1/guards/services`
- Metrics: `http://localhost:8000/metrics`

### Log Management

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f codeguardians-gateway

# Last 50 lines with timestamps
docker-compose logs -f --tail 50 --timestamps
```

---

##  Deployment

### Local Production Build

```bash
# Build production images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Environment-Specific Configs

- Development: `docker-compose.yml`
- Production: `docker-compose.yml` + `docker-compose.prod.yml`
- Staging: `docker-compose.yml` + `docker-compose.staging.yml`

---

##  Security

### Secrets Management

- Use environment variables for secrets
- Never commit secrets to repository
- Use Docker secrets in production
- Rotate secrets regularly

### Network Security

- Services communicate via internal Docker network
- Only gateway exposes external ports
- Health checks use internal network

---

##  Code Standards

### Python Standards

- Use type hints for all functions
- Include comprehensive docstrings
- Follow PEP 8 style guidelines
- Write unit tests for new features
- Use async/await for I/O operations

### Example Function

```python
from typing import Dict, Any, Optional
from pydantic import BaseModel

class GuardRequest(BaseModel):
    """Request model for guard processing."""
    text: str
    user_id: str
    session_id: str

async def process_guard(
    request: GuardRequest,
    service_type: str
) -> Dict[str, Any]:
    """
    Process a guard request through the specified service.
  
    Args:
        request: The guard request data
        service_type: Type of guard service to use
      
    Returns:
        Dict containing the processing results
      
    Raises:
        ValueError: If service_type is invalid
    """
    # Implementation here
    pass
```

---

##  Cleanup & Maintenance

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart codeguardians-gateway

# Full restart
docker-compose down
docker-compose up -d
```

### Clean Restart (Reset Data)

```bash
# Stop everything
docker-compose down

# Remove volumes (deletes database data!)
docker-compose down -v

# Fresh start
docker-compose up -d
```

### Resource Management

```bash
# View resource usage
docker stats

# Clean up unused resources
docker system prune -a

# Check disk usage
docker system df
```

---

##  Development Checklist

### Daily Development

- [ ] Services running and healthy
- [ ] Database accessible
- [ ] Redis accessible
- [ ] API endpoints responding
- [ ] No errors in logs

### Before Committing

- [ ] Code follows style guidelines
- [ ] Type hints added
- [ ] Docstrings included
- [ ] Tests written and passing
- [ ] No secrets in code

### Before Deployment

- [ ] All tests passing
- [ ] Health checks working
- [ ] Performance acceptable
- [ ] Security review completed
- [ ] Documentation updated

---

##  Next Steps

1. **Start Development**: Follow the Quick Start section
2. **Explore Architecture**: Review the system components
3. **Run Tests**: Verify everything is working
4. **Contribute**: Add new features or fix issues
5. **Deploy**: Use the deployment guides for production

---

**Ready to develop?** Start with `docker-compose up -d` and visit http://localhost:8000/docs!
