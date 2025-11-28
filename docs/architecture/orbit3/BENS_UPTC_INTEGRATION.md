# 🔥 BEN'S UPTC INTEGRATION GUIDE
## Orbit 3: Integrating FastAPI Services with UPTC

**Status:** ✅ **COMPLETE INTEGRATION GUIDE**  
**Date:** 2025-11-22  
**Pattern:** BEN × UPTC × INTEGRATION × ONE  
**Frequency:** 999 Hz (AEYON) × 444 Hz (Ben) × 530 Hz (UPTC)  
**Guardian:** AEYON (999 Hz) + Ben (444 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 PURPOSE

This guide shows **exactly how** to integrate Ben's FastAPI services with UPTC (Orbit 4). It provides:

- ✅ Step-by-step integration instructions
- ✅ UPTC Router Adapter usage
- ✅ OrchestrationAdapter patterns
- ✅ ProtocolMessage transformation examples
- ✅ Complete code examples
- ✅ Troubleshooting guide

**This is THE definitive guide for Orbit 3 ↔ Orbit 4 integration.**

---

# ==========================
## PART 1: INTEGRATION OVERVIEW
# ==========================

## 1.1 Why Integrate with UPTC?

**Benefits:**
- ✅ **Intelligent Routing** - UPTC selects best routing strategy automatically
- ✅ **Multi-Strategy Routing** - Event, Graph, Semantic, Unified routing
- ✅ **Service Discovery** - Automatic agent discovery via capability matching
- ✅ **Unified Protocol** - Single protocol for all inter-service communication
- ✅ **Fallback Mechanisms** - Graceful degradation if UPTC unavailable

---

## 1.2 Integration Architecture

**Flow:**
```
FastAPI Gateway → UPTC Router Adapter → UPTC Core → Target Service
     (Orbit 3)         (Adapter)          (Orbit 4)      (Any Orbit)
```

**Components:**
- **UPTCRouterAdapter** - Bridges FastAPI Gateway to UPTC
- **OrchestrationAdapter** - Transforms OrchestrationRequest ↔ ProtocolMessage
- **UPTC Core** - Intelligent routing engine
- **ProtocolMessage** - Standardized message format

---

# ==========================
## PART 2: UPTC ROUTER ADAPTER INTEGRATION
# ==========================

## 2.1 Initialization

**Location:** `app/core/orchestrator/uptc_adapter.py`

**Setup:**
```python
from app.core.orchestrator.uptc_adapter import UPTCRouterAdapter
from app.core.orchestrator.request_router import RequestRouter
import httpx

# Initialize HTTP client
http_client = httpx.AsyncClient(timeout=30.0)

# Create fallback router (direct routing)
request_router = RequestRouter(http_client)

# Create UPTC Router Adapter
uptc_adapter = UPTCRouterAdapter(
    fallback_router=request_router,
    enable_uptc=True  # Enable UPTC routing
)

# Check if UPTC is enabled
if uptc_adapter.is_uptc_enabled():
    logger.info("✅ UPTC Router Adapter enabled")
else:
    logger.warning("⚠️ UPTC Router Adapter disabled, using fallback")
```

---

## 2.2 Integration in Guard Orchestrator

**Location:** `app/core/guard_orchestrator.py`

**Pattern:**
```python
class GuardServiceOrchestrator:
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.uptc_adapter = None  # Initialized in initialize()
    
    async def initialize(self):
        """Initialize orchestrator with UPTC integration."""
        try:
            from app.core.orchestrator.uptc_adapter import UPTCRouterAdapter
            from app.core.orchestrator.request_router import RequestRouter
            
            # Create RequestRouter for fallback
            request_router = RequestRouter(self.http_client)
            
            # Wrap with UPTC adapter
            enable_uptc = os.getenv('ENABLE_UPTC_ROUTING', 'true').lower() == 'true'
            self.uptc_adapter = UPTCRouterAdapter(
                fallback_router=request_router,
                enable_uptc=enable_uptc
            )
            
            if self.uptc_adapter.is_uptc_enabled():
                logger.info("✅ UPTC Router Adapter initialized and enabled")
        except Exception as e:
            logger.warning(f"Failed to initialize UPTC Router Adapter: {e}")
            self.uptc_adapter = None
    
    async def _route_request(self, request: OrchestrationRequest) -> Dict[str, Any]:
        """Route request via UPTC or fallback."""
        # Try UPTC Router Adapter first (if available)
        if self.uptc_adapter and self.uptc_adapter.is_uptc_enabled():
            try:
                # Convert services dict to format expected by adapter
                service_configs = {
                    service_type: config_obj 
                    for service_type, config_obj in self.services.items()
                }
                
                # Route via UPTC adapter (falls back to RequestRouter if UPTC fails)
                response = await self.uptc_adapter.route_and_process(
                    request=request,
                    service_configs=service_configs
                )
                return response
            except Exception as e:
                # SAFETY: Log error but continue to direct routing fallback
                logger.warning(f"UPTC routing failed, falling back to direct routing: {e}")
                # Continue to direct routing below
        
        # Fallback to direct routing
        return await self._direct_route(request)
```

---

## 2.3 Environment Configuration

**Environment Variables:**
```bash
# Enable/disable UPTC routing
ENABLE_UPTC_ROUTING=true

# UPTC Core configuration (if needed)
UPTC_PROTOCOL_VERSION=1.0.0
UPTC_RESONANCE_FREQUENCY=530.0
UPTC_PHI_RATIO_THRESHOLD=0.8
```

---

# ==========================
## PART 3: ORCHESTRATION ADAPTER USAGE
# ==========================

## 3.1 OrchestrationAdapter Overview

**Purpose:** Transforms between FastAPI Gateway format and UPTC ProtocolMessage format

**Location:** `EMERGENT_OS/uptc/integrations/orchestration_adapter.py`

**Transformations:**
- `OrchestrationRequest` → `ProtocolMessage`
- `ProtocolMessage` → `OrchestrationResponse`

---

## 3.2 Request to Message Transformation

**Pattern:**
```python
from EMERGENT_OS.uptc.integrations.orchestration_adapter import OrchestrationAdapter
from app.core.orchestrator.models import OrchestrationRequest
from protocol.schema import ProtocolMessage

# Initialize adapter
uptc_core = get_uptc_core()  # Get UPTC Core instance
adapter = OrchestrationAdapter(uptc_core)

# Transform OrchestrationRequest to ProtocolMessage
message = await adapter.request_to_message(
    request=orchestration_request,
    service_configs=service_configs
)

# Message structure:
# - intent: service_type.value (e.g., "tokenguard")
# - action: "process" or request.action
# - payload: request.payload
# - source: "gateway"
# - target: None (let UPTC route)
# - metadata: request metadata
```

---

## 3.3 Message to Response Transformation

**Pattern:**
```python
# After UPTC routes and processes message
result_message = ProtocolMessage(...)

# Transform ProtocolMessage back to OrchestrationResponse
response = await adapter.message_to_response(
    message=result_message,
    request_id=request.request_id,
    service_type=request.service_type
)

# Response structure:
# - request_id: Original request ID
# - service_type: Original service type
# - success: True if message indicates success
# - data: message.payload
# - error: message.payload.get("error") if error
```

---

## 3.4 Complete Request-Response Flow

**End-to-End Pattern:**
```python
async def process_with_uptc(request: OrchestrationRequest):
    """Process request via UPTC with transformation."""
    
    # 1. Transform request to ProtocolMessage
    message = await adapter.request_to_message(request, service_configs)
    
    # 2. Route via UPTC
    target = uptc_core.route(message)
    
    if not target:
        # Fallback to direct routing
        return await direct_route(request)
    
    # 3. Send message to target
    result = await uptc_core.send(message, target)
    
    # 4. Transform result back to OrchestrationResponse
    response = await adapter.message_to_response(
        result, 
        request.request_id, 
        request.service_type
    )
    
    return response
```

---

# ==========================
## PART 4: PROTOCOL MESSAGE PATTERNS
# ==========================

## 4.1 Creating ProtocolMessages

**Basic Pattern:**
```python
from protocol.schema import ProtocolMessage

# Create message for UPTC routing
message = ProtocolMessage(
    intent="tokenguard",  # Service type or capability
    action="process",      # Action to perform
    payload={
        "content": "...",
        "confidence": 0.8
    },
    source="gateway",
    target=None,  # Let UPTC route automatically
    metadata={
        "request_id": "req_123",
        "user_id": "user_456"
    }
)
```

---

## 4.2 Service-Specific Patterns

**TokenGuard Pattern:**
```python
message = ProtocolMessage(
    intent="tokenguard",
    action="optimize",
    payload={
        "content": text_content,
        "max_tokens": 1000,
        "confidence_threshold": 0.8
    }
)
```

**TrustGuard Pattern:**
```python
message = ProtocolMessage(
    intent="trustguard",
    action="validate",
    payload={
        "input_text": input_text,
        "output_text": output_text,
        "context": context_data
    }
)
```

**ContextGuard Pattern:**
```python
message = ProtocolMessage(
    intent="contextguard",
    action="detect_drift",
    payload={
        "current_code": current_code,
        "previous_code": previous_code,
        "session_id": session_id
    }
)
```

---

# ==========================
## PART 5: ROUTING STRATEGIES
# ==========================

## 5.1 Automatic Strategy Selection

**UPTC Router Adapter automatically selects best strategy:**

1. **Direct Routing** - If target specified in message
2. **Event Routing** - If message has topic/event pattern
3. **Graph Routing** - If message intent matches capability
4. **Semantic Routing** - If semantic similarity needed
5. **Unified Routing** - Master router selects best

---

## 5.2 Forcing Specific Strategy

**Pattern:**
```python
# If you need specific routing strategy, set message metadata
message = ProtocolMessage(
    intent="process",
    action="execute",
    payload={...},
    metadata={
        "routing_strategy": "graph"  # Force graph routing
    }
)
```

---

## 5.3 Fallback Chain

**UPTC Router Adapter fallback:**
```
1. Try UPTC routing
   ├─ Success → Return response
   └─ Failure → Continue to fallback
2. Try RequestRouter (direct routing)
   ├─ Success → Return response
   └─ Failure → Return error
```

---

# ==========================
## PART 6: ERROR HANDLING
# ==========================

## 6.1 UPTC Unavailable

**Pattern:**
```python
try:
    if uptc_adapter.is_uptc_enabled():
        response = await uptc_adapter.route_and_process(request, service_configs)
    else:
        # UPTC disabled, use fallback
        response = await request_router.route(request)
except Exception as e:
    logger.error(f"UPTC routing failed: {e}")
    # Fallback to direct routing
    response = await request_router.route(request)
```

---

## 6.2 Routing Failures

**Pattern:**
```python
# UPTC routing returns None if no target found
target = uptc_core.route(message)

if target is None:
    logger.warning("UPTC routing returned no target, using fallback")
    # Fallback to direct routing
    response = await direct_route(request)
else:
    # Use UPTC routing
    response = await uptc_core.send(message, target)
```

---

## 6.3 Transformation Errors

**Pattern:**
```python
try:
    message = await adapter.request_to_message(request, service_configs)
except Exception as e:
    logger.error(f"Request transformation failed: {e}")
    # Fallback to direct routing without transformation
    response = await direct_route(request)
```

---

# ==========================
## PART 7: TESTING INTEGRATION
# ==========================

## 7.1 Unit Testing

**Pattern:**
```python
import pytest
from unittest.mock import Mock, AsyncMock

async def test_uptc_adapter_integration():
    # Mock UPTC Core
    mock_uptc_core = Mock()
    mock_uptc_core.route = Mock(return_value="target_agent")
    
    # Mock adapter
    adapter = OrchestrationAdapter(mock_uptc_core)
    
    # Test transformation
    request = OrchestrationRequest(...)
    message = await adapter.request_to_message(request, {})
    
    assert message.intent == request.service_type.value
    assert message.payload == request.payload
```

---

## 7.2 Integration Testing

**Pattern:**
```python
async def test_uptc_routing_integration():
    # Initialize real UPTC Core
    uptc_core = UPTCCore(config=UPTCConfig())
    uptc_core.activate()
    
    # Register test service
    uptc_core.registry.register_agent(
        agent_id="test_service",
        capabilities=["test"]
    )
    
    # Create adapter
    adapter = OrchestrationAdapter(uptc_core)
    
    # Test routing
    request = OrchestrationRequest(service_type=GuardServiceType.TOKENGUARD, ...)
    message = await adapter.request_to_message(request, {})
    
    target = uptc_core.route(message)
    assert target is not None
```

---

# ==========================
## PART 8: PERFORMANCE OPTIMIZATION
# ==========================

## 8.1 Caching UPTC Core

**Pattern:**
```python
# Cache UPTC Core instance (singleton)
_uptc_core = None

def get_uptc_core():
    global _uptc_core
    if _uptc_core is None:
        _uptc_core = UPTCCore(config=UPTCConfig())
        _uptc_core.activate()
    return _uptc_core
```

---

## 8.2 Connection Pooling

**Pattern:**
```python
# Reuse HTTP client
http_client = httpx.AsyncClient(
    timeout=30.0,
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
)
```

---

## 8.3 Async Operations

**Pattern:**
```python
# Always use async/await for UPTC operations
async def route_request(request):
    # Async routing
    target = await asyncio.to_thread(uptc_core.route, message)
    
    # Async sending
    result = await uptc_core.send_async(message, target)
    
    return result
```

---

# ==========================
## PART 9: TROUBLESHOOTING
# ==========================

## 9.1 Common Issues

### **Issue: UPTC Adapter Not Initializing**

**Symptoms:**
- `uptc_adapter` is `None`
- UPTC routing not working

**Solutions:**
```python
# 1. Check imports
from app.core.orchestrator.uptc_adapter import UPTCRouterAdapter

# 2. Check UPTC Core availability
try:
    from EMERGENT_OS.uptc.uptc_core import UPTCCore
    uptc_available = True
except ImportError:
    uptc_available = False

# 3. Check environment variable
enable_uptc = os.getenv('ENABLE_UPTC_ROUTING', 'true').lower() == 'true'
```

---

### **Issue: Routing Returns None**

**Symptoms:**
- `uptc_core.route(message)` returns `None`
- No service found

**Solutions:**
```python
# 1. Check agent registration
uptc_core.registry.list_agents()  # Should show registered agents

# 2. Check capability matching
capabilities = uptc_core.registry.capability_graph.find_capabilities("tokenguard")
assert len(capabilities) > 0

# 3. Check message intent matches capability
assert message.intent in capabilities
```

---

### **Issue: Transformation Fails**

**Symptoms:**
- `request_to_message()` raises exception
- Message structure incorrect

**Solutions:**
```python
# 1. Validate request structure
assert isinstance(request, OrchestrationRequest)
assert request.service_type is not None
assert request.payload is not None

# 2. Validate service configs
assert request.service_type in service_configs

# 3. Check ProtocolMessage creation
message = ProtocolMessage(...)
is_valid, errors = message.validate()
assert is_valid, f"Message validation failed: {errors}"
```

---

# ==========================
## PART 10: COMPLETE EXAMPLE
# ==========================

## 10.1 Full Integration Example

**Complete FastAPI Service with UPTC Integration:**
```python
from fastapi import FastAPI
from app.core.orchestrator.uptc_adapter import UPTCRouterAdapter
from app.core.orchestrator.request_router import RequestRouter
from app.core.orchestrator.models import OrchestrationRequest
import httpx
import os

app = FastAPI()

# Initialize HTTP client
http_client = httpx.AsyncClient(timeout=30.0)

# Initialize routers
request_router = RequestRouter(http_client)
uptc_adapter = UPTCRouterAdapter(
    fallback_router=request_router,
    enable_uptc=os.getenv('ENABLE_UPTC_ROUTING', 'true').lower() == 'true'
)

@app.post("/api/v1/guards/process")
async def process_guard(request: OrchestrationRequest):
    """Process guard request via UPTC."""
    # Get service configs
    service_configs = get_service_configs()
    
    # Route via UPTC (with fallback)
    response = await uptc_adapter.route_and_process(
        request=request,
        service_configs=service_configs
    )
    
    return response
```

---

**Pattern:** BEN × UPTC × INTEGRATION × ONE  
**Status:** ✅ **COMPLETE INTEGRATION GUIDE**  
**Next Steps:** Use this guide for all Orbit 3 ↔ Orbit 4 integrations  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

