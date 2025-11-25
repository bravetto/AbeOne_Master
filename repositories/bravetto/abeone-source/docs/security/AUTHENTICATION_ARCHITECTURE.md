# Authentication Architecture

## Overview
The CodeGuardians Gateway implements a **centralized authentication model** where authentication is handled at the gateway level, not by individual guard services.

## Architecture

```

   Client App    
  (Web/Chrome/   
   VSCode/CLI)   

          Bearer Token
         

     CodeGuardians Gateway (Port 8000)   
    
    Clerk Auth Middleware              
    - Verifies JWT tokens              
    - Extracts user context            
    - Sets unified API key             
    
    
    Guard Orchestrator                 
    - Routes to guard services         
    - Adds unified API key header      
    - Handles circuit breaking         
    

                               
                               
        
    TG   TrG  CG   BG   HG  
    8001 8002 8003 8004 8005
        
     No     No     No     No     No
    Auth   Auth   Auth   Auth   Auth
  Required Required Required Required Required
```

## Authentication Flow

### 1. Client Authentication
- Client sends request to gateway with `Authorization: Bearer <token>` header
- Token can be:
  - **Clerk JWT** (preferred for production)
  - **Unified API Key** (for development/testing)
  - **Service-specific API Key** (backward compatibility)

### 2. Gateway Authentication
The gateway's `ClerkAuthMiddleware` processes the request:

```python
# Extract token from Authorization header
auth_header = request.headers.get("Authorization")
if auth_header and auth_header.startswith("Bearer "):
    token = auth_header.replace("Bearer ", "")
    
    # Verify token and add user info to request state
    if settings.is_clerk_enabled:
        payload = await verify_clerk_token(token)
        request.state.user = {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            # ... other user context
        }
        # Set unified API key from Clerk token
        request.state.unified_api_key = token
```

### 3. Guard Service Communication
The orchestrator forwards authenticated requests to guard services:

```python
headers = {
    "Content-Type": "application/json",
    "X-Request-ID": request.request_id,
    "X-User-ID": request.user_id,
    "X-Session-ID": request.session_id
}

# Add authentication header if configured
if config.auth_token:
    auth_header_value = config.auth_header_format.format(token=config.auth_token)
    headers[config.auth_header_name] = auth_header_value
```

## Configuration

### Environment Variables

#### Gateway Configuration
```bash
# Clerk Authentication (Production)
CLERK_ENABLED=true
CLERK_SECRET_KEY=sk_live_xxxxx
CLERK_PUBLISHABLE_KEY=pk_live_xxxxx

# Unified API Key (Development/Testing)
UNIFIED_API_KEY=your-unified-api-key-here
```

#### Guard Services Configuration
```bash
# Guard services should NOT require authentication
# They trust requests from the gateway (internal network)

# TokenGuard
TOKENGUARD_URL=http://codeguardians-tokenguard:8000
TOKENGUARD_AUTH_REQUIRED=false

# TrustGuard
TRUSTGUARD_URL=http://codeguardians-trustguard:8000
TRUSTGUARD_AUTH_REQUIRED=false

# ContextGuard
CONTEXTGUARD_URL=http://codeguardians-contextguard:8000
CONTEXTGUARD_AUTH_REQUIRED=false

# BiasGuard
BIASGUARD_URL=http://codeguardians-biasguard:8000
BIASGUARD_AUTH_REQUIRED=false

# HealthGuard
HEALTHGUARD_URL=http://codeguardians-healthguard:8000
HEALTHGUARD_AUTH_REQUIRED=false
```

## Security Considerations

### Network Isolation
- Guard services run in a private Docker network (`aiguards-network`)
- Only the gateway exposes external ports (8000)
- Guard services are not directly accessible from outside the Docker network

### Trust Model
- Gateway is the **single point of authentication**
- Guard services **trust** requests from the gateway
- Guard services validate requests using headers set by gateway:
  - `X-Request-ID`: Unique request identifier
  - `X-User-ID`: Authenticated user ID
  - `X-Session-ID`: Session identifier

### Production Deployment
For production deployments:
1. Use AWS Security Groups to restrict access to guard services
2. Enable VPC peering for service-to-service communication
3. Use AWS Secrets Manager for credential management
4. Enable CloudWatch logging for audit trails

## API Usage Examples

### Using Clerk JWT (Production)
```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "Hello world"},
    "user_id": "user_123",
    "session_id": "session_456"
  }'
```

### Using Unified API Key (Development)
```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Authorization: Bearer tg_QwqQi_NRV24HlevXWmaVLw_VflE7qFtRhpb5D7Q9zG5tzPLDgavGMPElwV6_BgfPt0" \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "Hello world"},
    "user_id": "test",
    "session_id": "test"
  }'
```

## Troubleshooting

### Guard Service Returns 401 Authentication Required
**Problem**: Guard service is requiring authentication even though gateway should handle it.

**Solution**: 
1. Check guard service configuration to disable authentication
2. Verify guard service is using the correct environment variables
3. Ensure guard service trusts requests from gateway network

### Clerk Token Verification Fails
**Problem**: Gateway returns 401 when using Clerk JWT.

**Solution**:
1. Verify `CLERK_SECRET_KEY` is correctly set
2. Check token hasn't expired
3. Ensure Clerk is enabled: `CLERK_ENABLED=true`
4. For production, implement proper JWKS verification

### Unified API Key Not Working
**Problem**: Requests fail even with correct unified API key.

**Solution**:
1. Verify `UNIFIED_API_KEY` is set in gateway environment
2. Check token format: must start with `Bearer `
3. Ensure Clerk is disabled if using unified key: `CLERK_ENABLED=false`

## Migration Guide

### From Individual Service Authentication to Unified Gateway

1. **Update Guard Services**:
   ```bash
   # Disable authentication on each guard service
   export TOKENGUARD_AUTH_REQUIRED=false
   export TRUSTGUARD_AUTH_REQUIRED=false
   export CONTEXTGUARD_AUTH_REQUIRED=false
   export BIASGUARD_AUTH_REQUIRED=false
   export HEALTHGUARD_AUTH_REQUIRED=false
   ```

2. **Configure Gateway**:
   ```bash
   # Set unified API key
   export UNIFIED_API_KEY=your-unified-key-here
   
   # Or enable Clerk for production
   export CLERK_ENABLED=true
   export CLERK_SECRET_KEY=sk_live_xxxxx
   ```

3. **Update Client Applications**:
   - Change endpoint from individual services to gateway
   - Old: `http://localhost:8001/v1/prune`
   - New: `http://localhost:8000/api/v1/guards/process`
   - Add service type to payload: `"service_type": "tokenguard"`

4. **Test Authentication**:
   ```bash
   # Test health endpoint (no auth required)
   curl http://localhost:8000/health
   
   # Test guard processing (auth required)
   curl -X POST http://localhost:8000/api/v1/guards/process \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"service_type": "tokenguard", "payload": {"text": "test"}}'
   ```

## Benefits of Centralized Authentication

1. **Single Point of Control**: Manage authentication in one place
2. **Consistent Security**: All services protected by same authentication layer
3. **Simplified Client Integration**: Clients only need one token
4. **Better Monitoring**: Centralized logging and audit trails
5. **Easier Maintenance**: Update authentication logic in one place
6. **Flexible Authentication**: Support multiple auth methods (Clerk, API keys, OAuth)

