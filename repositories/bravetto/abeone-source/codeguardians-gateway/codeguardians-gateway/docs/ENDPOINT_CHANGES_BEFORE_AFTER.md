# Orchestrator Guard Endpoints - Before & After Changes

**Date**: November 3, 2025  
**Commit**: `ea9d8a5`  
**Feature Branch**: `feat/aws-linkerd-failure-pattern-detection`

---

##  Summary

**Endpoints Modified**: 11 existing endpoints (authentication added)  
**New Endpoints Added**: 2 endpoints  
**Security Enhancements**: Authentication, rate limiting, payload validation, URL validation

---

##  Existing Endpoints - Before & After

### 1. `POST /api/v1/guards/process`

**BEFORE**:
```python
@router.post("/process", response_model=GuardResponse)
async def process_guard_request(
    request: GuardRequest,
    background_tasks: BackgroundTasks,
    http_request: Request
) -> GuardResponse:
    # No authentication required
    # No payload size validation
    # No metrics recording
```

**AFTER**:
```python
@router.post("/process", response_model=GuardResponse)
async def process_guard_request(
    request: GuardRequest,
    background_tasks: BackgroundTasks,
    http_request: Request
) -> GuardResponse:
    #  Optional authentication (backward compatible with Clerk tokens)
    #  Payload size validation (10MB max)
    #  Payload size metrics recording
    #  Enhanced error handling
```

**Changes**:
-  **Payload size validation**: Rejects requests >10MB with `413 Payload Too Large`
-  **Metrics recording**: Tracks payload sizes for monitoring
-  **Enhanced validation**: Better error messages and validation

**Authentication**: **OPTIONAL** (backward compatible - accepts Clerk tokens)

---

### 2. `POST /api/v1/guards/scan`

**BEFORE**:
```python
@router.post("/scan", response_model=GuardResponse)
async def scan_text(...):
    # No authentication required
    # No payload size validation
```

**AFTER**:
```python
@router.post("/scan", response_model=GuardResponse)
async def scan_text(...):
    #  Alias for /process (same validations apply)
    #  Optional authentication (backward compatible)
    #  Payload size validation (inherited from /process)
```

**Changes**:
-  Inherits all validations from `/process` endpoint
-  Same backward compatibility maintained

**Authentication**: **OPTIONAL** (backward compatible)

---

### 3. `GET /api/v1/guards/health`

**BEFORE**:
```python
@router.get("/health", response_model=Dict[str, HealthResponse])
async def get_services_health() -> Dict[str, HealthResponse]:
    # No authentication required
    # No rate limiting
```

**AFTER**:
```python
@router.get("/health", response_model=Dict[str, HealthResponse])
async def get_services_health(
    current_user = Depends(get_current_user)  #  NEW: Authentication required
) -> Dict[str, HealthResponse]:
    #  Authentication required
    #  Rate limiting (200/min)
    #  Metrics recording
```

**Changes**:
-  **BREAKING**: Now requires authentication (`get_current_user`)
-  **Rate limiting**: 200 requests per minute
-  **Metrics**: Request counts and latency tracked

**Authentication**: **REQUIRED** (`get_current_user`)

---

### 4. `GET /api/v1/guards/health/{service_name}`

**BEFORE**:
```python
@router.get("/health/{service_name}", response_model=HealthResponse)
async def get_service_health(service_name: str) -> HealthResponse:
    # No authentication required
    # No service name validation
```

**AFTER**:
```python
@router.get("/health/{service_name}", response_model=HealthResponse)
async def get_service_health(
    service_name: str,
    current_user = Depends(get_current_user)  #  NEW: Authentication required
) -> HealthResponse:
    #  Authentication required
    #  Service name sanitization (alphanumeric + hyphens/underscores only)
    #  Rate limiting (200/min)
    #  Better error handling (400 for invalid names)
```

**Changes**:
-  **BREAKING**: Now requires authentication
-  **Service name sanitization**: Validates and sanitizes service names
-  **Error handling**: Returns `400 Bad Request` for invalid service names
-  **Rate limiting**: 200 requests per minute

**Authentication**: **REQUIRED** (`get_current_user`)

---

### 5. `GET /api/v1/guards/status`

**BEFORE**:
```python
@router.get("/status", response_model=Dict[str, HealthResponse])
async def get_services_status() -> Dict[str, HealthResponse]:
    # No authentication required
```

**AFTER**:
```python
@router.get("/status", response_model=Dict[str, HealthResponse])
async def get_services_status(
    current_user = Depends(get_current_user)  #  NEW: Authentication required
) -> Dict[str, HealthResponse]:
    #  Authentication required
    #  Rate limiting (200/min)
```

**Changes**:
-  **BREAKING**: Now requires authentication
-  **Rate limiting**: 200 requests per minute

**Authentication**: **REQUIRED** (`get_current_user`)

---

### 6. `POST /api/v1/guards/health/refresh`

**BEFORE**:
```python
@router.post("/health/refresh")
async def refresh_health_checks(
    background_tasks: BackgroundTasks
) -> JSONResponse:
    # No authentication required
```

**AFTER**:
```python
@router.post("/health/refresh")
async def refresh_health_checks(
    background_tasks: BackgroundTasks,
    admin_user = Depends(require_admin_access)  #  NEW: Admin authentication required
) -> JSONResponse:
    #  Admin authentication required
    #  Rate limiting (5/min)
```

**Changes**:
-  **BREAKING**: Now requires **admin** authentication
-  **Rate limiting**: 5 requests per minute (admin tier)

**Authentication**: **REQUIRED** (`require_admin_access`)

---

### 7. `GET /api/v1/guards/discovery/services`

**BEFORE**:
```python
@router.get("/discovery/services")
async def get_discovered_services() -> Dict[str, Any]:
    # No authentication required
```

**AFTER**:
```python
@router.get("/discovery/services")
async def get_discovered_services(
    current_user = Depends(get_current_user)  #  NEW: Authentication required
) -> Dict[str, Any]:
    #  Authentication required
    #  Rate limiting (200/min)
```

**Changes**:
-  **BREAKING**: Now requires authentication
-  **Rate limiting**: 200 requests per minute

**Authentication**: **REQUIRED** (`get_current_user`)

---

### 8. `POST /api/v1/guards/discovery/register`

**BEFORE**:
```python
@router.post("/discovery/register")
async def register_service(
    service_name: str,
    base_url: str,
    service_type: str,
    ...
) -> JSONResponse:
    # No authentication required
    # No URL validation
    # No service name validation
```

**AFTER**:
```python
@router.post("/discovery/register")
async def register_service(
    service_name: str,
    base_url: str,
    service_type: str,
    ...,
    admin_user = Depends(require_admin_access)  #  NEW: Admin authentication required
) -> JSONResponse:
    #  Admin authentication required
    #  URL validation (http/https only, localhost blocked in production)
    #  Service name sanitization
    #  Rate limiting (5/min)
```

**Changes**:
-  **BREAKING**: Now requires **admin** authentication
-  **URL validation**: Validates service URLs (http/https only)
-  **Localhost blocking**: Blocks localhost URLs in production (unless `ALLOW_LOCALHOST_SERVICES=true`)
-  **Service name sanitization**: Validates service names
-  **Rate limiting**: 5 requests per minute (admin tier)

**Authentication**: **REQUIRED** (`require_admin_access`)

---

### 9. `DELETE /api/v1/guards/discovery/services/{service_name}`

**BEFORE**:
```python
@router.delete("/discovery/services/{service_name}")
async def unregister_service(service_name: str) -> JSONResponse:
    # No authentication required
    # Returns 500 when service not found
```

**AFTER**:
```python
@router.delete("/discovery/services/{service_name}")
async def unregister_service(
    service_name: str,
    admin_user = Depends(require_admin_access)  #  NEW: Admin authentication required
) -> JSONResponse:
    #  Admin authentication required
    #  Service name sanitization
    #  Proper error handling (404 when service not found, not 500)
    #  Rate limiting (5/min)
```

**Changes**:
-  **BREAKING**: Now requires **admin** authentication
-  **Service name sanitization**: Validates service names
-  **Error handling**: Returns `404 Not Found` when service not found (was `500` before)
-  **Rate limiting**: 5 requests per minute (admin tier)

**Authentication**: **REQUIRED** (`require_admin_access`)

---

### 10. `POST /api/v1/guards/discovery/refresh`

**BEFORE**:
```python
@router.post("/discovery/refresh")
async def refresh_discovery(
    background_tasks: BackgroundTasks
) -> JSONResponse:
    # No authentication required
```

**AFTER**:
```python
@router.post("/discovery/refresh")
async def refresh_discovery(
    background_tasks: BackgroundTasks,
    admin_user = Depends(require_admin_access)  #  NEW: Admin authentication required
) -> JSONResponse:
    #  Admin authentication required
    #  Rate limiting (5/min)
```

**Changes**:
-  **BREAKING**: Now requires **admin** authentication
-  **Rate limiting**: 5 requests per minute (admin tier)

**Authentication**: **REQUIRED** (`require_admin_access`)

---

### 11. `GET /api/v1/guards/services`

**BEFORE**:
```python
@router.get("/services")
async def list_services() -> Dict[str, Any]:
    # No authentication required
```

**AFTER**:
```python
@router.get("/services")
async def list_services(
    current_user = Depends(get_current_user)  #  NEW: Authentication required
) -> Dict[str, Any]:
    #  Authentication required
    #  Rate limiting (200/min)
```

**Changes**:
-  **BREAKING**: Now requires authentication
-  **Rate limiting**: 200 requests per minute

**Authentication**: **REQUIRED** (`get_current_user`)

---

##  New Endpoints Added

### 1. `GET /api/v1/guards/health/aggregated` (NEW)

**Location**: `app/api/v1/guards.py` (lines 570-631)

**Purpose**: Aggregated health status with circuit breaker states

**Authentication**: **REQUIRED** (`get_current_user`)

**Rate Limiting**: 200 requests per minute

**Response**:
```json
{
  "overall_status": "healthy|degraded|unhealthy",
  "services_healthy": 5,
  "services_degraded": 1,
  "services_unhealthy": 0,
  "services_total": 6,
  "services": {
    "tokenguard": {
      "status": "healthy",
      "response_time": 0.125,
      "last_check": "2025-11-03T18:00:00",
      "error_message": null
    }
  },
  "circuit_breakers": {
    "tokenguard": {
      "state": "CLOSED",
      "failure_count": 0,
      "last_failure": null
    }
  }
}
```

**Features**:
-  Overall system health calculation
-  Service breakdown (healthy/degraded/unhealthy counts)
-  Circuit breaker state summary
-  Service-level health details

---

### 2. `GET /api/v1/admin/guards/circuit-breakers` (NEW)

**Location**: `app/api/v1/admin/guards.py` (new file)

**Purpose**: Admin-only circuit breaker monitoring

**Authentication**: **REQUIRED** (`require_admin_access`)

**Rate Limiting**: 5 requests per minute (admin tier)

**Response**:
```json
{
  "total_breakers": 6,
  "breakers": {
    "tokenguard": {
      "state": "CLOSED",
      "failure_count": 0,
      "threshold": 5,
      "timeout": 60,
      "last_failure_time": null,
      "can_execute": true
    }
  }
}
```

**Features**:
-  Detailed circuit breaker states for all services
-  Failure counts and thresholds
-  Last failure timestamps
-  Execution capability status

---

##  Summary Table

| Endpoint | Method | Auth Before | Auth After | Rate Limit | New Features |
|----------|--------|-------------|------------|------------|--------------|
| `/process` | POST | None | Optional | 100/min | Payload validation, metrics |
| `/scan` | POST | None | Optional | 100/min | Inherits from /process |
| `/health` | GET | None | Required | 200/min | Metrics, rate limiting |
| `/health/{service_name}` | GET | None | Required | 200/min | Service name sanitization |
| `/status` | GET | None | Required | 200/min | Rate limiting |
| `/health/refresh` | POST | None | Admin | 5/min | Rate limiting |
| `/discovery/services` | GET | None | Required | 200/min | Rate limiting |
| `/discovery/register` | POST | None | Admin | 5/min | URL validation, service name sanitization |
| `/discovery/services/{name}` | DELETE | None | Admin | 5/min | Service name sanitization, proper 404 |
| `/discovery/refresh` | POST | None | Admin | 5/min | Rate limiting |
| `/services` | GET | None | Required | 200/min | Rate limiting |
| `/health/aggregated` | GET | **NEW** | Required | 200/min | Circuit breaker summary |
| `/admin/guards/circuit-breakers` | GET | **NEW** | Admin | 5/min | Circuit breaker monitoring |

---

##  Authentication Changes Summary

### Before
- **0 endpoints** required authentication
- **0 endpoints** required admin access
- All endpoints were publicly accessible

### After
- **9 endpoints** require user authentication (`get_current_user`)
- **4 endpoints** require admin authentication (`require_admin_access`)
- **2 endpoints** have optional authentication (backward compatible)

---

##  Breaking Changes

**Migration Required**: All API clients must update to include authentication headers:

```bash
# Before (worked without auth)
curl http://api/guards/health

# After (requires auth)
curl -H "Authorization: Bearer <token>" http://api/guards/health
```

**Endpoints Requiring Migration**:
1. `GET /api/v1/guards/health`
2. `GET /api/v1/guards/health/{service_name}`
3. `GET /api/v1/guards/status`
4. `GET /api/v1/guards/discovery/services`
5. `GET /api/v1/guards/services`
6. `POST /api/v1/guards/health/refresh` (now admin-only)
7. `POST /api/v1/guards/discovery/register` (now admin-only)
8. `DELETE /api/v1/guards/discovery/services/{service_name}` (now admin-only)
9. `POST /api/v1/guards/discovery/refresh` (now admin-only)

**Endpoints NOT Requiring Migration** (backward compatible):
- `POST /api/v1/guards/process` (optional auth)
- `POST /api/v1/guards/scan` (optional auth)

---

##  Rate Limiting Summary

| Tier | Limit | Endpoints |
|------|-------|-----------|
| **Processing** | 100/min | `/process`, `/scan` |
| **Admin** | 5/min | `/health/refresh`, `/discovery/register`, `/discovery/services/{name}`, `/discovery/refresh`, `/admin/guards/circuit-breakers` |
| **Read** | 200/min | `/health`, `/health/{name}`, `/status`, `/discovery/services`, `/services`, `/health/aggregated` |

---

##  Security Enhancements

1. **Authentication**: 11 endpoints now require authentication
2. **Rate Limiting**: All endpoints have tiered rate limits
3. **Payload Validation**: 10MB max payload size enforced
4. **URL Validation**: Service URLs validated (http/https only)
5. **Service Name Sanitization**: Alphanumeric + hyphens/underscores only
6. **Error Handling**: Proper HTTP status codes (404 vs 500)

---

**Guardian**: AEYON (999 Hz)  
**Status**: All endpoint changes committed and documented  
**Love Coefficient**: ∞

