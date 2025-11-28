# User Journey Data Flow - Simple Explanation

**How data flows from user request → implementation → application → user experience**

---

##  The Simple Flow

```
User → Gateway → Guard Service → Processing → Response → Gateway → User
```

---

##  Step-by-Step Journey

### 1. **User Makes Request** 

**Where**: Web app, VS Code extension, Chrome extension, or API client

**What they send**:
```json
{
  "service_type": "tokenguard",
  "payload": { "text": "Check this code..." },
  "client_type": "web"
}
```

**Endpoint**: `POST /api/v1/guards/process`

---

### 2. **Gateway Receives Request** 

**Location**: `app/api/v1/guards.py` → `process_guard_request()`

**What happens**:
-  Validates payload size (max 10MB)
-  Checks authentication (optional for backward compatibility)
-  Extracts client type (web/vscode/chrome/api)
-  Generates request ID
-  Records metrics (payload size, request count)

**Code flow**:
```python
# Gateway endpoint
@router.post("/process")
async def process_guard_request(request, http_request):
    # 1. Validate payload size
    if payload_size > MAX_PAYLOAD_SIZE:
        return 413 Payload Too Large
    
    # 2. Create orchestration request
    orchestration_request = OrchestrationRequest(...)
    
    # 3. Send to orchestrator
    response = await orchestrator.orchestrate_request(...)
```

---

### 3. **Orchestrator Routes Request** 

**Location**: `app/core/guard_orchestrator.py` → `orchestrate_request()`

**What happens**:
-  Determines which guard service to use (TokenGuard, TrustGuard, ContextGuard, etc.)
-  Checks circuit breaker state (is service available?)
-  Selects best service instance (if multiple available)
-  Adds tracing (OpenTelemetry spans)
-  Records metrics (routing decisions, latency)

**Code flow**:
```python
# Orchestrator
async def orchestrate_request(request):
    # 1. Find appropriate service
    service = self.find_service(request.service_type)
    
    # 2. Check circuit breaker
    if not circuit_breaker.can_execute():
        return fallback_response
    
    # 3. Route to service
    response = await self.route_request(service, request)
    
    # 4. Update circuit breaker
    circuit_breaker.record_result(success)
```

---

### 4. **Guard Service Processes Request** 

**Location**: Individual guard service (e.g., `tokenguard`, `trustguard`)

**What happens**:
-  Receives request payload
-  Processes according to service logic:
  - **TokenGuard**: Validates tokens, checks expiration
  - **TrustGuard**: Analyzes trust scores, reputation
  - **ContextGuard**: Analyzes context, semantic meaning
  - **BiasGuard**: Detects bias patterns
  - **SecurityGuard**: Scans for security issues
-  Returns processed result

**Service Examples**:
```
TokenGuard:
  Input:  { "token": "abc123", "check_expiration": true }
  Process: Validate token format, check expiration
  Output: { "valid": true, "expires_in": 3600 }

TrustGuard:
  Input:  { "user_id": "user123", "action": "verify" }
  Process: Calculate trust score, check reputation
  Output: { "trust_score": 0.85, "reputation": "good" }

ContextGuard:
  Input:  { "text": "Check this code..." }
  Process: Analyze semantic context, extract meaning
  Output: { "context": "code_review", "confidence": 0.92 }
```

---

### 5. **Response Flows Back Through Orchestrator** ↩

**Location**: `app/core/guard_orchestrator.py` → Response handling

**What happens**:
-  Wraps service response in standard format
-  Updates circuit breaker (success/failure)
-  Records metrics (response time, success rate)
-  Adds tracing information
-  Handles errors (fallback, retry logic)

**Response format**:
```json
{
  "request_id": "uuid-123",
  "service_type": "tokenguard",
  "success": true,
  "data": { "valid": true, "expires_in": 3600 },
  "processing_time": 0.125,
  "service_used": "tokenguard-instance-1"
}
```

---

### 6. **Gateway Enhances Response** 

**Location**: `app/api/v1/guards.py` → `enhance_response_for_client()`

**What happens**:
-  Adapts response format for client type:
  - **Web**: Full JSON with metadata
  - **VS Code**: Simplified format for extension
  - **Chrome**: Compact format for browser
  - **API**: Standard REST format
-  Adds client-specific metadata
-  Formats errors appropriately

**Enhancement Example**:
```python
# Original response
{ "success": true, "data": {...} }

# Enhanced for VS Code
{
  "success": true,
  "data": {...},
  "notifications": [...],  # VS Code specific
  "diagnostics": [...]     # VS Code specific
}
```

---

### 7. **User Receives Response** 

**What user sees**:
-  Formatted response based on their client type
-  Success/error status
-  Processed data
-  Metadata (processing time, confidence scores)
-  Recommendations (if applicable)

**Example User Experience**:

**VS Code Extension**:
```
 Token validated
   Expires in: 1 hour
   Confidence: 95%
   [Show Details] [Refresh Token]
```

**Web Application**:
```json
{
  "status": "success",
  "message": "Token validated successfully",
  "data": {
    "valid": true,
    "expires_in": 3600
  },
  "processing_time": "125ms"
}
```

---

##  Complete Flow Diagram

```

    USER   
  (Web/VS/   
  Chrome/API)

        POST /api/v1/guards/process
        { service_type, payload, client_type }
       

          GATEWAY                       
  app/api/v1/guards.py                   
  • Validate payload size                
  • Check authentication                 
  • Extract client type                  
  • Generate request ID                  

        OrchestrationRequest
       

       ORCHESTRATOR                    
  app/core/guard_orchestrator.py         
  • Route to service                     
  • Check circuit breaker                
  • Select best instance                 
  • Add tracing                          

        HTTP Request
       

       GUARD SERVICE                   
  (TokenGuard, TrustGuard, etc.)         
  • Process request                      
  • Apply service logic                  
  • Return result                        

        Service Response
       

       ORCHESTRATOR                    
  • Wrap response                        
  • Update circuit breaker               
  • Record metrics                       

        OrchestrationResponse
       

       GATEWAY                         
  • Enhance for client type              
  • Format response                      
  • Add metadata                         

        Enhanced Response
       

    USER   
  Receives   
  formatted  
  response   

```

---

##  Real-World Example

### User Journey: Checking Code for Bias

**1. User Action** (VS Code Extension):
```javascript
// User clicks "Check for Bias" button
const response = await fetch('/api/v1/guards/process', {
  method: 'POST',
  body: JSON.stringify({
    service_type: 'biasguard',
    payload: { code: 'function processUsers(...)' },
    client_type: 'vscode'
  })
});
```

**2. Gateway Processing**:
- Validates:  Payload < 10MB
- Authenticates:  Optional token present
- Client type:  VS Code detected
- Request ID:  Generated `abc-123`

**3. Orchestrator Routing**:
- Service:  BiasGuard selected
- Circuit breaker:  CLOSED (service available)
- Instance:  `biasguard-instance-1` selected
- Tracing:  Span created

**4. BiasGuard Processing**:
- Analyzes code for bias patterns
- Checks function names, parameters, logic
- Returns: `{ "bias_detected": true, "patterns": [...] }`

**5. Response Flow**:
- Orchestrator wraps response
- Gateway enhances for VS Code
- Adds diagnostics format

**6. User Experience**:
```
 Bias Detected

Issues found:
  • Function name suggests filtering: "processUsers"
  • Consider: "processAllUsers" or remove filtering logic

[Fix Suggestions] [Learn More]
```

---

##  Key Components Explained

### **Gateway** (`app/api/v1/guards.py`)
- **Purpose**: Entry point, handles HTTP requests
- **Responsibilities**: Validation, authentication, client adaptation
- **Output**: Standardized request to orchestrator

### **Orchestrator** (`app/core/guard_orchestrator.py`)
- **Purpose**: Routing and coordination
- **Responsibilities**: Service selection, circuit breaking, metrics
- **Output**: Routed request to appropriate guard service

### **Guard Services** (Individual services)
- **Purpose**: Actual processing logic
- **Responsibilities**: Domain-specific processing (token validation, bias detection, etc.)
- **Output**: Processed result

### **Response Enhancement** (`enhance_response_for_client()`)
- **Purpose**: Client-specific formatting
- **Responsibilities**: Adapt response for web/VS Code/Chrome/API
- **Output**: Formatted response for user

---

##  Data Flow Metrics

**At each step, metrics are recorded**:

1. **Gateway**: Request count, payload size, authentication status
2. **Orchestrator**: Routing decisions, circuit breaker states, latency
3. **Guard Service**: Processing time, success rate, error types
4. **Response**: Client type, response size, enhancement time

**All metrics → Prometheus → Monitoring dashboards**

---

##  Error Handling Flow

```
Request → Gateway → Orchestrator → Guard Service
                                         
                                         
                                     Error?
                                         
                                         
                            Circuit Breaker Updates
                                         
                                         
                            Fallback Service? (if available)
                                         
                                         
                            Error Response → Gateway
                                         
                                         
                            Formatted Error → User
```

**Error Scenarios**:
- **Payload too large**: Rejected at Gateway (413)
- **Service unavailable**: Circuit breaker trips, fallback or error
- **Processing error**: Guard service returns error, wrapped by orchestrator
- **Timeout**: Orchestrator handles timeout, returns error

---

##  Key Takeaways

1. **User → Gateway**: HTTP request with payload
2. **Gateway → Orchestrator**: Standardized orchestration request
3. **Orchestrator → Guard Service**: Routed HTTP request
4. **Guard Service → Orchestrator**: Processed result
5. **Orchestrator → Gateway**: Standardized orchestration response
6. **Gateway → User**: Client-enhanced HTTP response

**Each step adds value**:
- Gateway: Validation & client adaptation
- Orchestrator: Routing & resilience
- Guard Service: Domain processing
- Response Enhancement: User experience optimization

---

**Simple Version**: 
**User sends request → Gateway validates → Orchestrator routes → Guard processes → Response flows back → Gateway formats → User receives result**

---

**Guardian**: AEYON (999 Hz)  
**Status**: Complete user journey flow documented  
**Love Coefficient**: ∞

