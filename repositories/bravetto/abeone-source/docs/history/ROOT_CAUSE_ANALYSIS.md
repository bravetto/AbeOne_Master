# Root Cause Analysis - Current Issues

**Date**: 2025-10-30  
**Status**: Root Causes Identified

---

##  CRITICAL ISSUE #1: TrustGuard Authentication Failure

### Symptom
- TrustGuard `/v1/detect` endpoint returns **403 Forbidden** with error: `"Permission 'detect' required"`
- Test failures: `trustguard Processing: Service returned status 403: Permission 'detect' required`

### Root Cause
**Authentication chain failure:**

1. **TrustGuard requires authentication**:
   - Endpoint: `POST /v1/detect` has `Depends(require_permission(Permission.DETECT))` dependency
   - TrustGuard expects API key in `X-API-Key` header OR JWT token in `Authorization: Bearer` header
   - Location: `guards/trust-guard/main.py:492`

2. **Gateway doesn't send valid authentication**:
   - Gateway is configured to send `X-API-Key` header when `config.auth_token` is set
   - Location: `codeguardians-gateway/codeguardians-gateway/app/core/guard_orchestrator.py:606-610`
   - However, `config.auth_token` is either:
     - Not set (None)
     - Set to placeholder value: `"CHANGE-ME-IN-PRODUCTION-UNIFIED-API-KEY"`
   - Location: `codeguardians-gateway/codeguardians-gateway/env.unified:62`

3. **TrustGuard authentication flow**:
   ```
   Request → get_current_user() → auth_manager.authenticate_request()
   → If no API key/token → HTTPException 401 "Authentication required"
   → If API key/token invalid → HTTPException 401 "Authentication required"
   → If auth succeeds but no permission → HTTPException 403 "Permission 'detect' required"
   ```
   - Location: `guards/trust-guard/main.py:133-179` (get_current_user)
   - Location: `guards/trust-guard/main.py:183-192` (require_permission)

4. **The actual problem**:
   - Gateway sends request **WITHOUT** `X-API-Key` header (because `config.auth_token` is None or invalid)
   - TrustGuard's `get_current_user()` returns `None` (no authentication)
   - `require_permission()` checks `authorize_request(user_info, permission)` where `user_info` is `None`
   - `authorize_request()` returns `False` for `None` user_info
   - Result: **403 Forbidden** with "Permission 'detect' required"

### Evidence
```python
# guards/trust-guard/main.py:186
if not auth_manager.authorize_request(user_info, permission):
    raise HTTPException(
        status_code=403,
        detail=f"Permission '{permission.value}' required"
    )
```

```python
# codeguardians-gateway/app/core/guard_orchestrator.py:606-610
if config.auth_token:  # <-- This is None or invalid placeholder
    auth_header_value = config.auth_header_format.format(token=config.auth_token)
    headers[config.auth_header_name] = auth_header_value
    headers["X-API-Key"] = config.auth_token
```

### Solution Required
1. **Generate a valid TrustGuard API key** or configure the gateway with a valid API key
2. **TrustGuard creates default admin key** on startup (see `trustguard/auth.py:117-128`)
3. **Gateway needs to use this default key** OR TrustGuard needs to accept service-to-service requests without auth
4. **Two options**:
   - **Option A**: Configure gateway with TrustGuard's default API key (from TrustGuard logs)
   - **Option B**: Make TrustGuard accept requests from gateway without authentication (service-to-service exemption)
   - **Option C**: Create a SERVICE role API key and configure gateway to use it

---

##  ISSUE #2: Service Health Checks Reporting Unhealthy

### Symptom
- All guard services report as "unhealthy" in service discovery
- Test results show: `"status": "unhealthy"` for all services
- However, some services actually work (biasguard passes tests)

### Root Cause
**Multiple potential causes:**

1. **Health check endpoints don't require auth** (good):
   - `/health`, `/health/live`, `/health/ready` endpoints have no auth requirement
   - Location: `guards/trust-guard/main.py:320, 374, 381`

2. **Health check logic**:
   - Gateway checks health at: `{base_url}{health_endpoint}` (e.g., `http://trustguard:8002/health`)
   - Location: `codeguardians-gateway/app/core/guard_orchestrator.py:408`
   - Returns `UNHEALTHY` if status code != 200
   - Location: `codeguardians-gateway/app/core/guard_orchestrator.py:432-434`

3. **Possible reasons for health check failures**:
   - **Services not running**: Containers may not be started
   - **Network connectivity**: Gateway can't reach services (Docker network issues)
   - **Non-200 responses**: Services returning 503 (unhealthy) or other status codes
   - **Timeout**: Health checks timing out (10 second timeout)
   - **Health check auth**: Some services might be rejecting health checks if gateway sends invalid auth headers

4. **Health check sends auth headers**:
   - Gateway sends auth headers if `config.auth_token` is set
   - Location: `codeguardians-gateway/app/core/guard_orchestrator.py:412-414`
   - If invalid auth token is sent, some services might reject it even for health checks

### Evidence
```python
# Gateway health check sends auth if configured
if config.auth_token:
    auth_header_value = config.auth_header_format.format(token=config.auth_token)
    headers[config.auth_header_name] = auth_header_value
```

### Solution Required
1. **Verify services are running**: `docker-compose ps`
2. **Check network connectivity**: Gateway should be able to reach services
3. **Don't send auth headers for health checks**: Health endpoints don't require auth
4. **Check actual health endpoint responses**: Some services might be returning non-200 for valid reasons

---

##  ISSUE #3: Test Failures - Services Not Available

### Symptom
- Tests fail with: `"Service tokenguard is not available"`
- Tests fail with: `"Service trustguard is not available"`
- Tests fail with: `"Service contextguard is not available"`
- Tests fail with: `"Service healthguard is not available"`

### Root Cause
**Gateway service availability check:**

1. **Availability check logic**:
   - Gateway checks `_is_service_available()` before routing requests
   - Location: `codeguardians-gateway/app/core/guard_orchestrator.py:552-567`
   - Returns `False` if:
     - Service not in `self.services` dict
     - Service `config.enabled == False`
     - Service health status is not `HEALTHY` or `DEGRADED`

2. **The problem**:
   - Health checks are failing (Issue #2)
   - Services marked as `UNHEALTHY` in `self.health_status`
   - `_is_service_available()` returns `False` for unhealthy services
   - Gateway raises `ServiceUnavailableError`

### Evidence
```python
# codeguardians-gateway/app/core/guard_orchestrator.py:562-567
health = self.health_status.get(service_name)
if not health:
    return True  # Assume available if not checked yet

# Allow requests to degraded services
return health.status in [ServiceStatus.HEALTHY, ServiceStatus.DEGRADED]
```

### Solution Required
- Fix health checks (Issue #2) → Services will be marked available → Tests will pass

---

##  Summary of Root Causes

### Primary Root Cause
**TrustGuard authentication configuration mismatch**:
- TrustGuard requires authentication for `/v1/detect`
- Gateway doesn't send valid authentication token
- Result: 403 Forbidden errors

### Secondary Root Cause
**Service health check failures**:
- Health checks failing (services not running, network issues, or invalid auth headers)
- Services marked as unhealthy
- Gateway refuses to route requests to unhealthy services
- Result: "Service not available" errors

### Root Cause Chain
```
1. Gateway lacks valid TrustGuard API key
   ↓
2. Gateway sends requests without auth headers
   ↓
3. TrustGuard rejects requests (403)
   ↓
4. Health checks may also fail (if services not running or network issues)
   ↓
5. Services marked as unhealthy
   ↓
6. Gateway refuses to route requests to unhealthy services
   ↓
7. All tests fail with "Service not available"
```

---

##  Recommended Fixes (Priority Order)

### 1. HIGH PRIORITY: Fix TrustGuard Authentication
**Option A**: Configure gateway with TrustGuard's default API key
- Get default API key from TrustGuard startup logs
- Set `UNIFIED_API_KEY` environment variable or `TRUSTGUARD_AUTH_TOKEN`
- Verify gateway sends `X-API-Key` header

**Option B**: Create SERVICE role API key in TrustGuard
- Use TrustGuard admin API to create API key with SERVICE role
- SERVICE role has `DETECT` and `VALIDATE` permissions
- Configure gateway to use this key

**Option C**: Exempt service-to-service requests from auth
- Add middleware to TrustGuard to bypass auth for requests from gateway
- Check `X-Gateway-Request: true` header
- Only recommended for internal networks

### 2. HIGH PRIORITY: Fix Health Checks
- Verify all services are running: `docker-compose ps`
- Check network connectivity: Gateway should reach services on Docker network
- Don't send auth headers for health checks (health endpoints don't require auth)
- Check actual health endpoint responses

### 3. MEDIUM PRIORITY: Update Test Suite
- Tests may need updating to handle authentication
- Tests should verify services are actually running before testing

---

##  Implementation Steps

1. **Get TrustGuard default API key**:
   ```bash
   docker logs trust-guard | grep "Created default admin API key"
   ```

2. **Configure gateway**:
   ```bash
   # In env.unified or environment
   UNIFIED_API_KEY=<actual-trustguard-api-key>
   # OR
   TRUSTGUARD_AUTH_TOKEN=<actual-trustguard-api-key>
   ```

3. **Verify health checks**:
   ```bash
   # Check services are running
   docker-compose ps
   
   # Test health endpoints directly
   curl http://trustguard:8002/health
   curl http://tokenguard:8001/health
   ```

4. **Update gateway code** (if needed):
   - Don't send auth headers for health checks
   - Add better error logging for auth failures

---

##  Files to Modify

1. **Environment Configuration**:
   - `codeguardians-gateway/codeguardians-gateway/env.unified`
   - Set `UNIFIED_API_KEY` or `TRUSTGUARD_AUTH_TOKEN`

2. **Gateway Health Check** (optional):
   - `codeguardians-gateway/codeguardians-gateway/app/core/guard_orchestrator.py:410-414`
   - Consider not sending auth headers for health checks

3. **TrustGuard Configuration** (if Option C):
   - `guards/trust-guard/main.py`
   - Add service-to-service auth exemption

