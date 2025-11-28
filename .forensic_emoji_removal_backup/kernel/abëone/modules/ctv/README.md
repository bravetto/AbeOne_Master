# CTV Module

## Overview

The CTV Module provides safe, human-triggered request packaging for CTV (Connected TV), Programmatic TV, Mountain, Roku, and Hulu DSP platforms.

**Pattern**: MODULE × CTV × HUMAN-TRIGGERED × ONE  
**Philosophy**: 80/20 → 97.8% Certainty  
**Safety**: No DSP communication. No automated bidding. Human-trigger only.

## Purpose

Defines fully safe and human-triggered request packaging for:
- CTV (Connected TV)
- Programmatic TV
- Mountain
- Roku
- Hulu DSP

## Safety Guarantees

✅ **No DSP Communication** - Module never communicates with DSP platforms  
✅ **No Automated Bidding** - No automated bidding logic  
✅ **Human-Trigger Only** - All requests require human validation  
✅ **Request Packaging Only** - Module only packages requests for human review

## Schema

### CTV Request Payload

```python
{
    "brand": str,              # Brand name (required)
    "objective": str,          # Campaign objective (required)
    "budget": float,           # Budget amount (required, must be > 0)
    "geo": list[str],          # Geographic targeting (required, non-empty)
    "constraints": {           # Constraints (required)
        "brand_safety": bool   # Brand safety requirement (required)
    }
}
```

### Example Request

```python
{
    "brand": "Example Brand",
    "objective": "Brand awareness campaign for Q4",
    "budget": 50000.0,
    "geo": ["US", "CA", "MX"],
    "constraints": {
        "brand_safety": True
    }
}
```

## Events

### MODULE_EVENT.ctv_request

Routed to human-reviewed queue.

**Event Structure**:
```python
{
    "name": "ctv_request",
    "payload": {
        "brand": str,
        "objective": str,
        "budget": float,
        "geo": list[str],
        "constraints": {
            "brand_safety": bool
        }
    }
}
```

**Response**:
```python
{
    "success": True,
    "request_id": str,  # UUID
    "status": "queued",
    "message": "CTV request queued for human validation"
}
```

### MODULE_EVENT.ctv_validate

Human-triggered validation of queued requests.

**Event Structure**:
```python
{
    "name": "ctv_validate",
    "request_id": str,
    "validated": bool,
    "validation_notes": str  # Optional
}
```

**Response**:
```python
{
    "success": True,
    "request_id": str,
    "status": "validated" | "rejected"
}
```

## Usage

### Python API

```python
from modules.ctv import CtvModule

# Initialize module
ctv_module = CtvModule()

# Load module
ctv_module.on_load()

# Create CTV request
payload = {
    "brand": "Example Brand",
    "objective": "Brand awareness campaign",
    "budget": 50000.0,
    "geo": ["US", "CA"],
    "constraints": {
        "brand_safety": True
    }
}

result = ctv_module.request(payload)
# Returns: {"success": True, "request_id": "...", "status": "queued"}

# Check queue status
status = ctv_module.get_queue_status()
# Returns: {"queued_count": 1, "validated_count": 0, "queued_requests": [...]}
```

### Event Bus API

```python
from EVENT_BUS import EventBus, EventType, get_bus

bus = get_bus()

# Create ctv_request event
event = bus.create_event(
    event_type=EventType.MODULE_EVENT,
    source="your_module",
    data={
        "name": "ctv_request",
        "payload": {
            "brand": "Example Brand",
            "objective": "Brand awareness campaign",
            "budget": 50000.0,
            "geo": ["US", "CA"],
            "constraints": {
                "brand_safety": True
            }
        }
    }
)

# Publish event
bus.publish(event)
```

## Module Interface

### Module ID
`MODULE_CTV`

### Version
`1.0.0`

### Lifecycle Hooks

- `on_load()` - Initialize module and subscribe to events
- `on_event(event)` - Handle incoming events
- `shutdown()` - Clean up resources

## Validation

The module validates all incoming requests against the schema:

- ✅ `brand`: Non-empty string
- ✅ `objective`: Non-empty string
- ✅ `budget`: Positive number (int or float)
- ✅ `geo`: Non-empty list of non-empty strings
- ✅ `constraints`: Dictionary
- ✅ `constraints.brand_safety`: Boolean

Invalid requests are rejected with detailed error messages.

## Queue Management

The module maintains two internal data structures:

1. **Request Queue** (`_request_queue`) - Queued requests awaiting human validation
2. **Validated Requests** (`_validated_requests`) - Requests that have been validated

### Queue Status

```python
{
    "queued_count": int,
    "validated_count": int,
    "queued_requests": [
        {
            "request_id": str,
            "brand": str,
            "objective": str,
            "budget": float,
            "status": str,
            "created_at": str
        }
    ]
}
```

## Safety Architecture

### No DSP Communication

The module **never** communicates with DSP platforms directly. It only:
1. Validates request schemas
2. Queues requests for human review
3. Packages requests for human validation

### No Automated Bidding

The module contains **no bidding logic**. It only packages requests.

### Human-Trigger Only

All requests must be:
1. Submitted via `ctv_request` event
2. Validated via `ctv_validate` event (human-triggered)
3. Manually processed after validation

## Error Handling

The module returns structured error responses:

```python
{
    "success": False,
    "error": "Error message describing the issue"
}
```

Common errors:
- `"Module not loaded"` - Module not initialized
- `"Missing required field: <field>"` - Schema validation failure
- `"<field> must be a <type>"` - Type validation failure
- `"Request <request_id> not found in queue"` - Request not found

## Integration

### Module Registry

Register the module:

```python
from MODULE_REGISTRY import register_ctv_module

register_ctv_module()
```

### Event Bus Routing

The Event Bus automatically routes `ctv_request` events to `MODULE_CTV`:

```python
# In EVENT_BUS._handle_module_event()
if event_name == "ctv_request":
    if self.module_registry:
        ctv_module = self.module_registry.get("MODULE_CTV")
        if ctv_module:
            self.module_registry.send_event("MODULE_CTV", event)
```

## Examples

### Basic Request

```python
from modules.ctv import CtvModule

ctv = CtvModule()
ctv.on_load()

result = ctv.request({
    "brand": "TechCorp",
    "objective": "Drive app installs",
    "budget": 100000.0,
    "geo": ["US"],
    "constraints": {
        "brand_safety": True
    }
})

print(result["request_id"])  # UUID of queued request
```

### Validate Request

```python
# Human validates request
validation_result = ctv.on_event({
    "name": "ctv_validate",
    "request_id": "<request_id>",
    "validated": True,
    "validation_notes": "Approved for Q4 campaign"
})
```

### Check Queue

```python
status = ctv.get_queue_status()
print(f"Queued: {status['queued_count']}")
print(f"Validated: {status['validated_count']}")
```

## Notes

- The module is **stateless** between requests (queue is in-memory)
- For production use, consider persisting the queue to a database
- Human validation is required before any DSP communication
- The module does **not** handle DSP API calls - that must be done separately after validation

