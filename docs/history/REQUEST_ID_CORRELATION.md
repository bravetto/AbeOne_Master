# Request-ID Correlation Implementation Summary

## Overview
Implemented comprehensive request-ID correlation across Gateway and all Guard services to enable end-to-end request tracing and debugging.

## Implementation Details

### Gateway (`codeguardians-gateway`)

**1. Request ID Middleware** (`app/main.py`)
- Extracts `X-Request-ID` from incoming requests
- Generates new UUID if not present
- Stores request ID in `request.state.request_id`
- Adds `X-Request-ID` to all response headers
- Logs request ID in all log entries

**2. Guards Endpoint** (`app/api/v1/guards.py`)
- Extracts request ID from `request.state` (set by middleware)
- Falls back to header or generates new one
- Passes request ID to orchestrator
- Includes request ID in response

**3. Guard Orchestrator** (`app/core/guard_orchestrator.py`)
- Already sends `X-Request-ID` header to guard services
- Includes `X-Gateway-Request: true` header

### BiasGuard (`guards/biasguard-backend`)

**1. Request Logging Middleware** (`src/app.ts`)
- Extracts `X-Request-ID` from incoming headers
- Generates new request ID if not present
- Stores in `req.requestId` for use throughout request lifecycle
- Adds `X-Request-ID` to response headers
- Logs request ID with correlation ID in all log entries
- Includes gateway request indicator, user ID, and session ID in logs

### TrustGuard (`guards/trust-guard`)

**Already Implemented:**
- Extracts `X-Request-ID` header (line 169)
- Uses request ID in logging context
- Supports request ID in trace context

## Request Flow

```
Client Request
  ↓ (may include X-Request-ID header)
Gateway Middleware
  ↓ (extracts or generates request ID)
Gateway Guards Endpoint
  ↓ (uses request ID from state)
Gateway Orchestrator
  ↓ (sends X-Request-ID header)
Guard Service
  ↓ (extracts X-Request-ID, uses in logs)
Response
  ↓ (includes X-Request-ID in headers)
Client
```

## Benefits

1. **End-to-End Tracing**: Track requests across all services using single request ID
2. **Debugging**: Easily correlate logs across gateway and guards
3. **Monitoring**: Filter metrics and logs by request ID
4. **Client Integration**: Clients can provide request IDs for their own correlation

## Usage

**Client-provided Request ID:**
```bash
curl -H "X-Request-ID: my-custom-id-123" \
     http://localhost:8000/api/v1/guards/process \
     -d '{"service_type": "tokenguard", "payload": {...}}'
```

**Response includes Request ID:**
```json
{
  "request_id": "REPLACE_ME",
  "success": true,
  ...
}
```

**Response Headers:**
```
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
```

## Log Correlation

All logs now include request ID, enabling easy filtering:

```bash
# Filter logs by request ID
docker logs codeguardians-gateway-development | grep "Request-ID: abc-123"
docker logs codeguardians-biasguard | grep "requestId: abc-123"
```

## Next Steps

1.  Request-ID correlation implemented
2. ⏳ Add request ID to Prometheus metrics labels
3. ⏳ Add request ID to OpenTelemetry traces
4. ⏳ Create Grafana dashboard with request ID filtering

