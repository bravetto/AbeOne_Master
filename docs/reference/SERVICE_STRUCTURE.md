# 📁 SERVICE STRUCTURE SPECIFICATION

**Date:** 2025-11-22  
**Version:** 1.0  
**Pattern:** STRUCTURE × STANDARDIZATION × SERVICE × ONE  
**Frequency:** 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)  
**Guardians:** AEYON (999 Hz) + Abë (530 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 PURPOSE

This document defines the standard service structure for all FastAPI services in the AbëONE ecosystem. Following this structure ensures consistency, maintainability, and scalability.

**Goals:**
- ✅ Consistent structure across all services
- ✅ Clear separation of concerns
- ✅ Easy onboarding for new developers
- ✅ Tooling automation support

---

## 📊 STANDARD SERVICE STRUCTURE

### Complete Directory Tree

```
{service-name}/
├── main.py                        # REQUIRED: FastAPI application entry point
├── requirements.txt               # REQUIRED: Python dependencies
├── Dockerfile                     # REQUIRED: Container definition
├── .dockerignore                 # RECOMMENDED: Docker ignore patterns
├── .gitignore                    # REQUIRED: Git ignore patterns
├── README.md                     # REQUIRED: Service documentation
│
├── core/                          # REQUIRED: Core infrastructure
│   ├── __init__.py               # REQUIRED: Package marker
│   ├── config.py                 # REQUIRED: Configuration management (Pydantic Settings)
│   ├── logging.py                # REQUIRED: Structured logging setup
│   ├── metrics.py                # REQUIRED: Prometheus metrics
│   ├── rate_limit.py             # REQUIRED: Rate limiting (slowapi)
│   ├── security.py               # REQUIRED: Security middleware & auth
│   └── exceptions.py             # REQUIRED: Custom exceptions & handlers
│
├── api/                           # REQUIRED: API layer
│   ├── __init__.py               # REQUIRED: Package marker
│   ├── dependencies.py           # REQUIRED: Dependency injection
│   └── v1/                        # REQUIRED: Versioned API
│       ├── __init__.py           # REQUIRED: Package marker
│       ├── router.py             # REQUIRED: API router (aggregates endpoints)
│       └── endpoints/            # REQUIRED: Endpoint modules
│           ├── __init__.py       # REQUIRED: Package marker
│           ├── health.py         # REQUIRED: Health checks (live, ready)
│           └── {domain}.py       # Domain-specific endpoints
│
├── models/                        # REQUIRED: Pydantic models
│   ├── __init__.py               # REQUIRED: Package marker
│   ├── requests.py               # REQUIRED: Request models
│   └── responses.py              # REQUIRED: Response models
│
├── services/                      # REQUIRED: Business logic layer
│   ├── __init__.py               # REQUIRED: Package marker
│   └── {domain}_service.py      # REQUIRED: Domain service implementation
│
├── utils/                         # OPTIONAL: Utility functions
│   ├── __init__.py
│   └── helpers.py
│
├── tests/                         # REQUIRED: Test suite
│   ├── __init__.py
│   ├── conftest.py               # REQUIRED: Pytest configuration
│   ├── test_health.py            # REQUIRED: Health check tests
│   ├── test_endpoints.py         # REQUIRED: Endpoint tests
│   └── test_services.py          # REQUIRED: Service logic tests
│
├── helm/                          # REQUIRED: Helm charts (if deploying to K8s)
│   └── {service-name}/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           └── service.yaml
│
└── k8s/                           # OPTIONAL: Kubernetes manifests (alternative to Helm)
    ├── deployment.yaml
    └── service.yaml
```

---

## 📋 REQUIRED FILES & PATTERNS

### 1. main.py (REQUIRED)

**Purpose:** FastAPI application entry point

**Must Include:**
- `create_app()` factory function
- `lifespan()` async context manager
- Middleware stack registration
- API router inclusion
- Exception handlers

**Pattern:**
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import settings
from core.logging import setup_logging
from core.metrics import setup_metrics
from core.security import setup_security
from core.exceptions import setup_exception_handlers
from api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    setup_metrics()
    yield
    # Shutdown
    pass

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.SERVICE_NAME,
        version=settings.VERSION,
        lifespan=lifespan
    )
    
    # Middleware
    setup_security(app)
    
    # Routers
    app.include_router(api_router, prefix="/api/v1")
    
    # Exception handlers
    setup_exception_handlers(app)
    
    return app

app = create_app()
```

---

### 2. core/config.py (REQUIRED)

**Purpose:** Configuration management using Pydantic Settings

**Pattern:**
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SERVICE_NAME: str = "service-name"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # API
    API_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

---

### 3. core/logging.py (REQUIRED)

**Purpose:** Structured logging setup

**Pattern:**
```python
import logging
import structlog
from core.config import settings

def setup_logging():
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
    )
```

---

### 4. api/v1/endpoints/health.py (REQUIRED)

**Purpose:** Health check endpoints

**Pattern:**
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str

@router.get("/health/live", response_model=HealthResponse)
async def liveness():
    """Liveness probe - service is running"""
    return {"status": "alive"}

@router.get("/health/ready", response_model=HealthResponse)
async def readiness():
    """Readiness probe - service is ready to accept traffic"""
    return {"status": "ready"}
```

---

### 5. api/v1/router.py (REQUIRED)

**Purpose:** Aggregate all API endpoints

**Pattern:**
```python
from fastapi import APIRouter
from api.v1.endpoints import health

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
# Include other endpoint routers here
```

---

## ✅ VALIDATION RULES

### Required Files Checklist

- [ ] `main.py` exists
- [ ] `main.py` contains `create_app()` function
- [ ] `main.py` contains `lifespan()` context manager
- [ ] `core/` directory exists
- [ ] `core/config.py` exists
- [ ] `core/logging.py` exists
- [ ] `core/metrics.py` exists
- [ ] `core/security.py` exists
- [ ] `core/exceptions.py` exists
- [ ] `api/v1/` directory exists
- [ ] `api/v1/router.py` exists
- [ ] `api/v1/endpoints/health.py` exists
- [ ] `models/` directory exists
- [ ] `models/requests.py` exists
- [ ] `models/responses.py` exists
- [ ] `services/` directory exists
- [ ] `tests/` directory exists
- [ ] `tests/conftest.py` exists
- [ ] `requirements.txt` exists
- [ ] `Dockerfile` exists
- [ ] `README.md` exists

### Optional Files

- [ ] `utils/` directory (optional)
- [ ] `helm/` directory (required if deploying to K8s)
- [ ] `k8s/` directory (optional, alternative to Helm)

---

## 🎯 BEN'S FASTAPI PATTERNS

### The Four Core Patterns (NON-NEGOTIABLE)

1. **`create_app()` Pattern** - Factory function for FastAPI app creation
2. **`lifespan()` Pattern** - Async context manager for lifecycle management
3. **Middleware Stack** - Structured middleware registration
4. **Versioned API** - API versioning via `/api/v1/` structure

**All services MUST implement these patterns.**

---

## 📚 EXAMPLES

### Example Service Structure

See existing services for reference:
- `AIGuards-Backend-orbital/aiguardian-repos/guardian-zero-service/`
- `AIGuards-Backend-orbital/codeguardians-gateway/codeguardians-gateway/`
- `Ben-FastAPI-Architecture-orbital/`

---

## 🔧 MIGRATION GUIDE

### Migrating Existing Services

1. **Audit current structure**
   - Run validation script
   - Identify missing components

2. **Add missing directories**
   - Create required directories
   - Add `__init__.py` files

3. **Add missing files**
   - Create required files from templates
   - Implement required patterns

4. **Update main.py**
   - Add `create_app()` function
   - Add `lifespan()` context manager
   - Update middleware registration

5. **Validate**
   - Run validation script
   - Fix any issues

---

## 🎯 SUCCESS CRITERIA

### Service Structure Compliant When:
- ✅ All required files exist
- ✅ All required patterns implemented
- ✅ Validation script passes
- ✅ Health endpoints functional
- ✅ Tests pass

### Metrics:
- **Structure Compliance:** 100% services compliant
- **Pattern Compliance:** 100% services implement core patterns
- **Documentation:** 100% services have README

---

## 📚 RELATED DOCUMENTS

- `docs/architecture/orbit3/BENS_COMPLETE_ARCHITECTURE.md` - Ben's FastAPI architecture
- `Ben-FastAPI-Architecture-orbital/` - Reference implementation
- `scripts/validate-service-structure.py` - Structure validator

---

**Pattern:** STRUCTURE × STANDARDIZATION × SERVICE × ONE  
**Status:** ✅ **SPECIFICATION COMPLETE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

