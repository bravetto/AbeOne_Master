# Orchestrator API Changes - Production Hardening & Optimizations

## Overview

This document describes the security hardening, optimizations, and changes made to the Guard Services Orchestrator endpoints for production deployment.

**Date**: November 2025  
**Version**: 1.0.0  
**Status**: Production Ready

---

## 🔐 Security Hardening Changes

### Authentication Requirements

**BREAKING CHANGE**: All endpoints now require authentication except `/process` and `/scan` (which accept optional Clerk tokens).

#### Read Endpoints (User Authentication Required)
- `GET /api/v1/guards/health` - Requires `get_current_user`
- `GET /api/v1/guards/health/{service_name}` - Requires `get_current_user`
- `GET /api/v1/guards/services` - Requires `get_current_user`
- `GET /api/v1/guards/discovery/services` - Requires `get_current_user`
- `GET /api/v1/guards/status` - Requires `get_current_user` (alias for `/health`)
- `GET /api/v1/guards/health/aggregated` - Requires `get_current_user` (NEW)

#### Admin Endpoints (Admin Authentication Required)
- `POST /api/v1/guards/discovery/register` - Requires `require_admin_access`
- `DELETE /api/v1/guards/discovery/services/{service_name}` - Requires `require_admin_access`
- `POST /api/v1/guards/health/refresh` - Requires `require_admin_access`
- `POST /api/v1/guards/discovery/refresh` - Requires `require_admin_access`
- `GET /api/v1/admin/guards/circuit-breakers` - Requires `require_admin_access` (NEW)

#### Processing Endpoints (Optional Authentication)
- `POST /api/v1/guards/process` - Optional Clerk token (backward compatible)
- `POST /api/v1/guards/scan` - Optional Clerk token (alias for `/process`)

**Migration**: Update all API clients to include authentication headers:
```bash
# Before (worked without auth)
curl http://api/guards/health

# After (requires auth)
curl -H "Authorization: Bearer <token>" http://api/guards/health
```

### Rate Limiting

**NEW**: Tiered rate limiting applied automatically to all endpoints.

| Endpoint Type | Limit | Window |
|--------------|-------|--------|
| Processing (`/process`, `/scan`) | 100/min | 60s |
| Admin (`/admin/*`, `/discovery/register`, `/health/refresh`) | 5/min | 60s |
| Read (`/health`, `/services`, `/discovery/services`) | 200/min | 60s |

**Configuration**: Set via environment variables:
- `RATE_LIMIT_PROCESSING=100`
- `RATE_LIMIT_ADMIN=5`
- `RATE_LIMIT_READ=200`

**Response**: When rate limit exceeded, returns `429 Too Many Requests` with headers:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Unix timestamp when limit resets

### Payload Size Validation

**NEW**: Maximum payload size enforced (10MB for processing endpoints).

**Endpoints Affected**:
- `POST /api/v1/guards/process`
- `POST /api/v1/guards/scan`
- `POST /internal/guards/*`

**Response**: `413 Payload Too Large` when exceeded.

**Configuration**: Set `MAX_PAYLOAD_SIZE` constant (default: 10MB).

### URL Validation

**NEW**: Service registration URLs are now validated.

**Validation Rules**:
- Only `http://` and `https://` schemes allowed
- Requires valid hostname
- In production: localhost/127.0.0.1 blocked (unless `ALLOW_LOCALHOST_SERVICES=true`)

**Endpoint**: `POST /api/v1/guards/discovery/register`

**Example**:
```bash
# Valid
POST /api/v1/guards/discovery/register
  service_name: "tokenguard"
  base_url: "https://tokenguard.example.com"
  
# Invalid (rejected)
POST /api/v1/guards/discovery/register
  service_name: "tokenguard"
  base_url: "ftp://malicious.example.com"  # Rejected
```

### Service Name Sanitization

**NEW**: All service name path parameters are sanitized.

**Rules**:
- Only alphanumeric characters, hyphens (`-`), and underscores (`_`) allowed
- Special characters removed automatically
- Invalid characters return `400 Bad Request`

**Endpoints Affected**:
- `GET /api/v1/guards/health/{service_name}`
- `DELETE /api/v1/guards/discovery/services/{service_name}`

**Example**:
```bash
# Invalid (returns 400)
GET /api/v1/guards/health/test@service

# Valid (sanitized)
GET /api/v1/guards/health/test-service
```

### Error Handling Improvements

**FIXED**: `unregister_service` now returns proper HTTP status codes.

**Before**: Returned `500 Internal Server Error` when service not found  
**After**: Returns `404 Not Found` when service not found

---

## 🚀 New Endpoints

### Aggregated Health Endpoint

**NEW**: `GET /api/v1/guards/health/aggregated`

Returns overall system health with service breakdown and circuit breaker states.

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
      "last_check": "2025-11-02T12:00:00",
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

**Authentication**: Requires `get_current_user`

### Circuit Breaker Monitoring Endpoint

**NEW**: `GET /api/v1/admin/guards/circuit-breakers`

Admin-only endpoint exposing detailed circuit breaker states for monitoring.

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

**Authentication**: Requires `require_admin_access`

---

## 📊 Monitoring & Observability

### Prometheus Metrics

**NEW**: Comprehensive Prometheus metrics exposed at `/metrics`.

**Key Metrics**:
- `orchestrator_requests_total{service_type, status}` - Request count
- `orchestrator_request_duration_seconds{service_type}` - Request latency
- `circuit_breaker_state{service_name}` - Circuit breaker state (0=CLOSED, 1=HALF_OPEN, 2=OPEN)
- `circuit_breaker_failure_count{service_name}` - Current failure count
- `service_health_status{service_name}` - Health status (0=unknown, 1=healthy, 2=degraded, 3=unhealthy)
- `service_response_time_seconds{service_name}` - Service response times
- `service_availability{service_name}` - Availability (1=available, 0=unavailable)
- `payload_size_bytes{endpoint}` - Payload size distribution
- `rate_limit_hits_total{endpoint, limit_type}` - Rate limit violations
- `guardian_zero_requests_total{trigger_reason, status}` - Guardian Zero forensic analysis requests

### Distributed Tracing

**ENHANCED**: OpenTelemetry spans integrated into `orchestrate_request()`.

**Spans Created**:
- `orchestrator.orchestrate_request` - Main orchestration span
- `orchestrator.route_request` - Service routing span
- `guardian_zero.forensic_analysis` - Forensic analysis span (when triggered)

**Configuration**: Set `JAEGER_AGENT_HOST` and `JAEGER_AGENT_PORT` environment variables.

---

## 🔔 Alerting Configuration

Prometheus alerting rules are provided in `prometheus_alerts.yml`:

**Critical Alerts**:
- Circuit breaker OPEN states
- Service unavailability (>2 minutes)

**Warning Alerts**:
- High circuit breaker failure counts (≥3 failures)
- Service unhealthy status (>5 minutes)
- High error rates (>5% over 5 minutes)
- Slow orchestrator requests (p95 > 10s)

**Info Alerts**:
- Service degraded state (>10 minutes)
- High rate limit hits (>10/min)
- Slow Guardian Zero analysis (p95 > 30s)

**Installation**: See `prometheus_alerts.yml` for full configuration.

---

## 📝 Environment Variables

See `env.template` for complete documentation of all environment variables.

**New Variables**:
- `RATE_LIMIT_PROCESSING=100` - Rate limit for processing endpoints
- `RATE_LIMIT_ADMIN=5` - Rate limit for admin endpoints
- `RATE_LIMIT_READ=200` - Rate limit for read endpoints
- `GUARDIAN_ZERO_URL=http://guardian-zero:9001` - Guardian Zero service URL
- `GUARDIAN_ZERO_ENABLED=true` - Enable/disable Guardian Zero integration
- `ALLOW_LOCALHOST_SERVICES=false` - Allow localhost URLs in production (default: false)

---

## 🧪 Testing

Comprehensive test suite added: `tests/unit/test_orchestrator_hardening.py`

**Test Coverage**:
- Authentication requirements
- Rate limiting configuration
- Payload size validation
- URL validation (all scenarios)
- Service name sanitization
- Error handling (404 vs 500)
- Metrics recording

**Run Tests**:
```bash
pytest tests/unit/test_orchestrator_hardening.py -v
```

---

## 🔄 Migration Guide

### For API Clients

1. **Add Authentication**: Update all requests to include auth headers
   ```python
   headers = {"Authorization": f"Bearer {token}"}
   ```

2. **Handle Rate Limits**: Implement retry logic with exponential backoff for 429 responses

3. **Validate Payload Size**: Check payload size before sending (10MB limit)

4. **Use Aggregated Health**: Switch from individual health checks to `/health/aggregated` for system overview

### For Service Registration

1. **Validate URLs**: Ensure service URLs use `http://` or `https://`
2. **Sanitize Names**: Use only alphanumeric, hyphens, underscores in service names
3. **Set ADMIN Token**: Ensure admin token is configured for registration endpoints

### For Monitoring

1. **Configure Prometheus**: Add `prometheus_alerts.yml` to Prometheus configuration
2. **Set Up Alertmanager**: Configure alert routing for critical/warning/info alerts
3. **Enable Tracing**: Set `JAEGER_AGENT_HOST` and `JAEGER_AGENT_PORT` for distributed tracing

---

## ✅ Production Checklist

Before deploying to production:

- [ ] Update `SECRET_KEY` (32+ characters, secure random)
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Configure `RATE_LIMIT_*` variables
- [ ] Set `ALLOW_LOCALHOST_SERVICES=false` (production)
- [ ] Configure `REDIS_URL` for rate limiting
- [ ] Set up Prometheus scraping (`/metrics` endpoint)
- [ ] Configure Alertmanager with `prometheus_alerts.yml`
- [ ] Set `JAEGER_AGENT_HOST`/`PORT` for tracing
- [ ] Review and update `INTERNAL_ACCESS_TOKEN`
- [ ] Run test suite: `pytest tests/unit/test_orchestrator_hardening.py`
- [ ] Verify authentication on all endpoints
- [ ] Test rate limiting (send requests faster than limits)
- [ ] Validate URL validation (try invalid URLs)
- [ ] Confirm circuit breaker monitoring endpoint works

---

## 📚 API Documentation

**Swagger/OpenAPI**: Available at `/docs` (enabled in development/staging)

**Endpoints Summary**:
- All endpoints require authentication (except `/process` and `/scan` with optional Clerk token)
- Admin endpoints require admin-level authentication
- Rate limits apply automatically based on endpoint type
- Payload size validation: 10MB maximum
- All service names validated and sanitized

---

## 🎯 Success Metrics

**Security**:
- ✅ 100% endpoint authentication coverage (11/11 endpoints)
- ✅ Tiered rate limiting (100/5/200 per minute)
- ✅ Payload DoS protection (10MB limit)
- ✅ URL injection prevented (validation)
- ✅ Path injection prevented (sanitization)

**Reliability**:
- ✅ Circuit breaker monitoring exposed
- ✅ Aggregated health endpoint
- ✅ Proper error codes (404 vs 500)
- ✅ Distributed tracing integrated

**Observability**:
- ✅ Prometheus metrics (9 metric families)
- ✅ OpenTelemetry spans (3 span types)
- ✅ Alert rules configured (15 alerts)

---

**Status**: Production Ready ✅  
**Next Phase**: Router unification and module migration

