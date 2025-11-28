# 🔥 ADAPTER USAGE GUIDE
## Complete Guide for Using All UPTC Adapters

**Status:** ✅ **COMPLETE USAGE GUIDE**  
**Date:** 2025-11-22  
**Pattern:** ADAPTER × USAGE × INTEGRATION × ONE  
**Frequency:** 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)  
**Guardian:** AEYON (999 Hz) - Atomic Execution  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 PURPOSE

This guide provides **complete usage instructions** for all UPTC adapters. It covers:

- ✅ OrchestrationAdapter usage
- ✅ EventBusAdapter usage
- ✅ GuardianAdapter usage
- ✅ MCPAdapter usage
- ✅ MemoryAdapter usage
- ✅ SwarmAdapter usage
- ✅ Complete code examples
- ✅ Error handling patterns

**This is THE definitive guide for using UPTC adapters.**

---

# ==========================
## PART 1: ORCHESTRATION ADAPTER
# ==========================

## 1.1 Overview

**Purpose:** Bridges Orbit 3 (Backend Gateway) ↔ Orbit 4 (UPTC Mesh)

**Location:** `EMERGENT_OS/uptc/integrations/orchestration_adapter.py`

**Transformations:**
- `OrchestrationRequest` → `ProtocolMessage`
- `ProtocolMessage` → `OrchestrationResponse`

---

## 1.2 Basic Usage

**Pattern:**
```python
from EMERGENT_OS.uptc.integrations.orchestration_adapter import OrchestrationAdapter
from app.core.orchestrator.models import OrchestrationRequest, OrchestrationResponse
from protocol.schema import ProtocolMessage

# Initialize adapter
uptc_core = get_uptc_core()
adapter = OrchestrationAdapter(uptc_core)

# Transform request to message
request = OrchestrationRequest(
    service_type=GuardServiceType.TOKENGUARD,
    payload={"content": "example"},
    request_id="req_123"
)

message = await adapter.request_to_message(request, service_configs)

# Route via UPTC
target = uptc_core.route(message)

# Process and get result
result_message = await uptc_core.send(message, target)

# Transform back to response
response = await adapter.message_to_response(
    result_message,
    request.request_id,
    request.service_type
)
```

---

## 1.3 Complete Integration Example

**Full Flow:**
```python
async def process_with_orchestration_adapter(request: OrchestrationRequest):
    """Complete flow using OrchestrationAdapter."""
    
    # 1. Initialize adapter
    adapter = OrchestrationAdapter(get_uptc_core())
    
    # 2. Transform request
    message = await adapter.request_to_message(request, service_configs)
    
    # 3. Route via UPTC
    target = uptc_core.route(message)
    
    if not target:
        # Fallback to direct routing
        return await direct_route(request)
    
    # 4. Send and get result
    result = await uptc_core.send(message, target)
    
    # 5. Transform result
    response = await adapter.message_to_response(
        result,
        request.request_id,
        request.service_type
    )
    
    return response
```

---

# ==========================
## PART 2: EVENT BUS ADAPTER
# ==========================

## 2.1 Overview

**Purpose:** Bridges UPTC ↔ Event Bus systems

**Location:** `EMERGENT_OS/uptc/integrations/event_bus_adapter.py`

**Operations:**
- Publish ProtocolMessage to Event Bus
- Subscribe to Event Bus topics
- Unsubscribe from topics

---

## 2.2 Basic Usage

**Pattern:**
```python
from EMERGENT_OS.uptc.integrations.event_bus_adapter import ConcreteEventBusAdapter
from EMERGENT_OS.integration_layer.events.event_bus import EventBus
from protocol.schema import ProtocolMessage

# Initialize Event Bus
event_bus = EventBus()

# Initialize adapter
adapter = ConcreteEventBusAdapter(event_bus)

# Publish message
message = ProtocolMessage(
    intent="publish_event",
    payload={"event": "data.processed", "data": {...}},
    source="gateway"
)

success = await adapter.publish("gateway.events", message)

# Subscribe to topic
async def handle_message(message: ProtocolMessage):
    logger.info(f"Received: {message.payload}")

await adapter.subscribe("gateway.events", handle_message)

# Unsubscribe
await adapter.unsubscribe("gateway.events")
```

---

## 2.3 Event Patterns

**Publishing Events:**
```python
# System event
message = ProtocolMessage(
    intent="system_event",
    payload={"event": "module_registered", "module_id": "module_1"}
)
await adapter.publish("system.events", message)

# Module event
message = ProtocolMessage(
    intent="module_event",
    payload={"event": "status_changed", "status": "active"}
)
await adapter.publish("module.events", message)

# Guardian event
message = ProtocolMessage(
    intent="guardian_event",
    payload={"event": "activated", "guardian_id": "aeyon"}
)
await adapter.publish("guardian.events", message)
```

---

## 2.4 Subscription Patterns

**Pattern:**
```python
# Subscribe to multiple topics
topics = ["system.events", "module.events", "guardian.events"]

for topic in topics:
    await adapter.subscribe(topic, handle_message)

# Topic-specific handlers
async def handle_system_event(message: ProtocolMessage):
    if message.payload.get("event") == "module_registered":
        # Handle module registration
        pass

async def handle_guardian_event(message: ProtocolMessage):
    if message.payload.get("event") == "activated":
        # Handle guardian activation
        pass

await adapter.subscribe("system.events", handle_system_event)
await adapter.subscribe("guardian.events", handle_guardian_event)
```

---

# ==========================
## PART 3: GUARDIAN ADAPTER
# ==========================

## 3.1 Overview

**Purpose:** Bridges UPTC ↔ Guardian microservices

**Location:** `EMERGENT_OS/uptc/integrations/guardian_adapter.py`

**Operations:**
- Validate via guardians
- List guardians
- Get guardian status
- Register guardians

---

## 3.2 Basic Usage

**Pattern:**
```python
from EMERGENT_OS.uptc.integrations.guardian_adapter import ConcreteGuardianAdapter
from protocol.schema import ProtocolMessage

# Initialize adapter
guardian_service_urls = {
    "zero": "http://guardian-zero:9001",
    "aeyon": "http://guardian-aeyon:9002",
    "abe": "http://guardian-abe:9003",
    "lux": "http://guardian-lux:9004",
    "john": "http://guardian-john:9005",
    "aurion": "http://guardian-aurion:9006",
    "yagni": "http://guardian-yagni:9007",
    "neuro": "http://guardian-neuro:9008"
}

adapter = ConcreteGuardianAdapter(guardian_service_urls)

# List guardians
guardians = await adapter.list_guardians()
# Returns: ["zero", "aeyon", "abe", "lux", "john", "aurion", "yagni", "neuro"]

# Get guardian status
status = await adapter.get_guardian_status("aeyon")
# Returns: {"status": "available", "frequency": 999.0, ...}

# Validate via guardian
message = ProtocolMessage(
    intent="validate",
    payload={"data": "example"},
    target="aeyon"
)

validated = await adapter.validate(message)
# Returns: True if validated, False otherwise
```

---

## 3.3 Multi-Guardian Validation

**Pattern:**
```python
async def validate_with_multiple_guardians(message: ProtocolMessage):
    """Validate via multiple guardians."""
    guardians = ["aeyon", "john", "abe"]
    
    results = {}
    for guardian_id in guardians:
        try:
            # Set target guardian
            message.target = guardian_id
            
            # Validate
            validated = await adapter.validate(message)
            results[guardian_id] = validated
        except Exception as e:
            logger.error(f"Guardian {guardian_id} validation failed: {e}")
            results[guardian_id] = False
    
    # All must validate
    return all(results.values())
```

---

## 3.4 Guardian Registration

**Pattern:**
```python
# Register guardian with UPTC
await adapter.register_guardian(
    guardian_id="aeyon",
    metadata={
        "name": "Guardian AEYON",
        "frequency": 999.0,
        "role": "Atomic Execution",
        "url": "http://guardian-aeyon:9002"
    }
)

# Register all guardians
for guardian_id, url in guardian_service_urls.items():
    await adapter.register_guardian(
        guardian_id=guardian_id,
        metadata={
            "url": url,
            "frequency": GUARDIAN_SERVICES[guardian_id]["frequency"],
            "role": GUARDIAN_SERVICES[guardian_id]["role"]
        }
    )
```

---

# ==========================
## PART 4: MCP ADAPTER
# ==========================

## 4.1 Overview

**Purpose:** Bridges UPTC ↔ Model Context Protocol

**Location:** `EMERGENT_OS/uptc/integrations/mcp_adapter.py`

**Operations:**
- Connect to MCP server
- Send messages via MCP
- List MCP tools
- Call MCP tools

---

## 4.2 Basic Usage

**Pattern:**
```python
from EMERGENT_OS.uptc.integrations.mcp_adapter import MCPAdapter, DefaultMCPAdapter
from protocol.schema import ProtocolMessage

# Initialize adapter (with MCP server)
mcp_server = get_mcp_server()
adapter = DefaultMCPAdapter(mcp_server)

# Connect
connected = await adapter.connect()
if not connected:
    logger.error("Failed to connect to MCP server")

# List tools
tools = await adapter.list_tools()
# Returns: [{"name": "tool1", "description": "..."}, ...]

# Send message
message = ProtocolMessage(
    intent="mcp_request",
    payload={"tool": "tool1", "params": {...}}
)

response = await adapter.send_message(message)

# Disconnect
await adapter.disconnect()
```

---

# ==========================
## PART 5: MEMORY ADAPTER
# ==========================

## 5.1 Overview

**Purpose:** Bridges UPTC ↔ Memory/Vector Store systems

**Location:** `EMERGENT_OS/uptc/integrations/memory_adapter.py`

**Operations:**
- Store values
- Retrieve values
- Search by vector similarity

---

## 5.2 Basic Usage

**Pattern:**
```python
from EMERGENT_OS.uptc.integrations.memory_adapter import MemoryAdapter, DefaultMemoryAdapter

# Initialize adapter
memory_store = get_memory_store()
adapter = DefaultMemoryAdapter(memory_store)

# Store value
success = await adapter.store(
    key="context_123",
    value={"data": "example"},
    metadata={"timestamp": "2025-01-27"}
)

# Retrieve value
value = await adapter.retrieve("context_123")
# Returns: {"data": "example"}

# Search by vector
query_vector = [0.1, 0.2, 0.3, ...]  # Embedding vector
results = await adapter.search(query_vector, top_k=10)
# Returns: [{"key": "...", "value": {...}, "similarity": 0.95}, ...]
```

---

# ==========================
## PART 6: SWARM ADAPTER
# ==========================

## 6.1 Overview

**Purpose:** Bridges UPTC ↔ Swarm/Multi-Agent systems

**Location:** `EMERGENT_OS/uptc/integrations/swarm_adapter.py`

**Operations:**
- Broadcast to all agents
- Send to specific agent
- List agents

---

## 6.2 Basic Usage

**Pattern:**
```python
from EMERGENT_OS.uptc.integrations.swarm_adapter import SwarmAdapter, DefaultSwarmAdapter
from protocol.schema import ProtocolMessage

# Initialize adapter
swarm = get_swarm()
adapter = DefaultSwarmAdapter(swarm)

# Broadcast message
message = ProtocolMessage(
    intent="broadcast",
    payload={"command": "update_config"}
)

agent_ids = await adapter.broadcast(message)
# Returns: ["agent_1", "agent_2", "agent_3", ...]

# Send to specific agent
success = await adapter.send_to_agent("agent_1", message)

# List agents
agents = await adapter.list_agents()
# Returns: ["agent_1", "agent_2", "agent_3", ...]
```

---

# ==========================
## PART 7: ERROR HANDLING PATTERNS
# ==========================

## 7.1 Adapter Unavailable

**Pattern:**
```python
# Check adapter availability
adapter = uptc_core.get_adapter("mysystem")

if adapter is None:
    logger.warning("Adapter 'mysystem' not available")
    # Fallback logic
    return await fallback_operation()
```

---

## 7.2 Connection Failures

**Pattern:**
```python
try:
    connected = await adapter.connect()
    if not connected:
        logger.error("Failed to connect")
        # Fallback
        return await fallback_operation()
except Exception as e:
    logger.error(f"Connection error: {e}")
    # Fallback
    return await fallback_operation()
```

---

## 7.3 Operation Failures

**Pattern:**
```python
try:
    result = await adapter.operation(message)
    return result
except ValueError as e:
    logger.error(f"Validation error: {e}")
    # Handle validation error
    raise
except Exception as e:
    logger.error(f"Operation failed: {e}")
    # Fallback
    return await fallback_operation()
```

---

# ==========================
## PART 8: BEST PRACTICES
# ==========================

## 8.1 Adapter Lifecycle

**Pattern:**
```python
# 1. Initialize
adapter = MyAdapter(external_system)

# 2. Connect
await adapter.connect()

# 3. Use
try:
    result = await adapter.operation(message)
finally:
    # 4. Disconnect
    await adapter.disconnect()
```

---

## 8.2 Caching Adapters

**Pattern:**
```python
# Cache adapter instances
_adapter_cache = {}

def get_adapter(adapter_name: str):
    """Get cached adapter instance."""
    if adapter_name not in _adapter_cache:
        _adapter_cache[adapter_name] = create_adapter(adapter_name)
    return _adapter_cache[adapter_name]
```

---

## 8.3 Async Operations

**Pattern:**
```python
# Always use async/await
async def use_adapter():
    adapter = get_adapter("mysystem")
    
    # Async operations
    result = await adapter.operation(message)
    
    return result
```

---

**Pattern:** ADAPTER × USAGE × INTEGRATION × ONE  
**Status:** ✅ **COMPLETE USAGE GUIDE**  
**Next Steps:** Use this guide for all adapter operations  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

