# Data Lake Module

Provides safe ingestion envelopes for storage into the central data lake.

**Pattern**: MODULE × DATA_LAKE × INGESTION × ONE  
**Philosophy**: 80/20 → 97.8% Certainty  
**Safety**: No ETL automation. No PII processing unless human-approved.

---

## Purpose

The Data Lake Module provides safe ingestion envelopes for storage into the central data lake. It validates and creates ingestion envelopes but **does not perform any ETL automation** or **PII processing** unless explicitly human-approved.

---

## Envelope Schema

### Ingestion Envelope

```python
{
    "source": str,              # Required: Source identifier
    "timestamp": str,           # Required: ISO8601 timestamp
    "payload": dict,            # Required: Payload dictionary
    "checksum": str             # Required: SHA256 checksum of payload
}
```

### Field Details

- **source** (str, required): The source identifier for the data (e.g., `"analytics"`, `"social"`, `"ctv"`). Must be a non-empty string.
- **timestamp** (str, required): ISO8601 format timestamp when the envelope was created (e.g., `"2024-01-15T10:30:00.123456"`).
- **payload** (dict, required): The data payload dictionary. Structure is not validated - only that it's a dictionary.
- **checksum** (str, required): SHA256 checksum of the JSON-serialized payload (sorted keys) for integrity verification.

---

## Events

### MODULE_EVENT.data.ingest → MODULE_EVENT.data_validated

**Event Flow**:
1. **Request**: Receive `data.ingest` event with payload and source
2. **Validation**: Validate payload schema (structure only, not content)
3. **Envelope Creation**: Create ingestion envelope with source, timestamp, payload, checksum
4. **Storage**: Store envelope record
5. **Publication**: Publish `MODULE_EVENT.data_validated` event
6. **Broadcast**: `data_validated` event broadcast to MODULE_EVENT subscribers

### data.ingest Event

**Event Structure**:
```python
{
    "name": "data.ingest",
    "source": str,              # Source identifier
    "payload": dict             # Payload dictionary
}
```

### data_validated Event

**Event Structure**:
```python
{
    "name": "data_validated",
    "envelope_id": str,         # Checksum-based envelope ID
    "envelope": {
        "source": str,
        "timestamp": str,       # ISO8601 format
        "payload": dict,
        "checksum": str
    }
}
```

---

## Safety Guarantees

 **No ETL Automation**: Module does not perform any Extract, Transform, Load operations  
 **No PII Processing**: Module does not process or detect PII unless human-approved  
 **Structure Validation Only**: Only validates payload structure (is a dict), not content  
 **Integrity Checks**: Provides checksums for data integrity verification  
 **Event-Based**: All output is through event system

---

## Usage

### Public API

```python
from modules.datalake import DataLakeModule

# Initialize module
datalake_module = DataLakeModule()

# Load module
datalake_module.on_load()

# Ingest data
result = datalake_module.ingest(
    payload={
        "user_id": "12345",
        "action": "page_view",
        "page": "/home"
    },
    source="analytics"
)

# Result:
# {
#     "success": True,
#     "envelope_id": "sha256-checksum-here",
#     "status": "validated",
#     "message": "Data ingestion envelope created and validated (no ETL automation, no PII processing)"
# }
```

### Event-Based Usage

```python
from EVENT_BUS import EventBus, EventType, get_bus

event_bus = get_bus()

# Publish data.ingest event
event = event_bus.create_event(
    event_type=EventType.MODULE_EVENT,
    source="your_module",
    target="MODULE_DATA_LAKE",
    data={
        "name": "data.ingest",
        "source": "analytics",
        "payload": {
            "user_id": "12345",
            "action": "page_view",
            "page": "/home"
        }
    }
)

event_bus.publish(event)
```

### Subscribe to data_validated Events

```python
from EVENT_BUS import EventBus, EventType, get_bus

def handle_data_validated(event):
    """Handle data_validated event."""
    event_data = event.data
    envelope_id = event_data.get('envelope_id')
    envelope = event_data.get('envelope')
    
    print(f"Validated envelope {envelope_id} from source: {envelope['source']}")
    print(f"Timestamp: {envelope['timestamp']}")
    print(f"Checksum: {envelope['checksum']}")
    # Your storage logic here (module does not store)

event_bus = get_bus()
event_bus.subscribe(EventType.MODULE_EVENT, handle_data_validated)
```

---

## Module Lifecycle

1. **Registration**: Module registered with `register_datalake_module()`
2. **Loading**: `on_load()` subscribes to MODULE_EVENT
3. **Event Handling**: Handles `data.ingest` events
4. **Validation**: Validates payload schema (structure only)
5. **Envelope Creation**: Creates ingestion envelope with source, timestamp, payload, checksum
6. **Publication**: Publishes `MODULE_EVENT.data_validated`
7. **Shutdown**: `shutdown()` unsubscribes from events

---

## Validation Rules

- **Payload**: Must be a dictionary (required)
- **Source**: Must be a non-empty string (required)
- **Content**: Not validated (no PII detection, no content validation)
- **Checksum**: Calculated from JSON-serialized payload (sorted keys) using SHA256

---

## Error Handling

The module returns error dictionaries for validation failures:

```python
{
    "success": False,
    "error": "Missing required field: payload"
}
```

Common validation errors:
- `"Missing required field: payload"` - Payload is missing
- `"payload must be a dictionary"` - Payload is not a dictionary
- `"source must be a non-empty string"` - Source is missing or invalid

---

## Examples

### Analytics Data Ingestion

```python
result = datalake_module.ingest(
    payload={
        "user_id": "12345",
        "session_id": "abc123",
        "event": "page_view",
        "page": "/products",
        "timestamp": "2024-01-15T10:30:00Z"
    },
    source="analytics"
)
```

### Social Media Data Ingestion

```python
result = datalake_module.ingest(
    payload={
        "platform": "twitter",
        "post_id": "123456789",
        "content": "Check out our new product!",
        "engagement": {
            "likes": 42,
            "retweets": 10,
            "replies": 5
        }
    },
    source="social"
)
```

### CTV Data Ingestion

```python
result = datalake_module.ingest(
    payload={
        "campaign_id": "ctv_2024_q1",
        "impressions": 1000000,
        "completion_rate": 0.85,
        "device_type": "smart_tv"
    },
    source="ctv"
)
```

### Get Ingested Envelopes

```python
envelopes = datalake_module.get_ingested_envelopes()
# Returns:
# {
#     "ingested_count": 10,
#     "envelopes": [
#         {
#             "envelope_id": "sha256-checksum-here",
#             "source": "analytics",
#             "timestamp": "2024-01-15T10:30:00.123456",
#             "checksum": "sha256-checksum-here",
#             "payload_keys": ["user_id", "action", "page"]
#         },
#         ...
#     ]
# }
```

---

## Integration

The Data Lake Module integrates with the abëone event system:

- **Subscribes to**: `MODULE_EVENT` for `data.ingest` events
- **Publishes**: `MODULE_EVENT.data_validated` events
- **Module ID**: `MODULE_DATA_LAKE`
- **Version**: `1.0.0`

---

## Safety Notes

 **Important**: This module does **NOT**:
- Perform ETL automation
- Process or detect PII
- Transform data automatically
- Store data directly (only creates envelopes)

This module only:
- Validates payload structure (is a dict)
- Creates ingestion envelopes
- Emits validated event payloads

Actual storage and processing must be handled by:
- Other modules that subscribe to `data_validated` events
- External systems that consume the event payloads
- Human-approved processes for PII handling

This design ensures separation of concerns and allows for human validation before any PII processing occurs.

---

**Pattern**: MODULE × DATA_LAKE × INGESTION × ONE  
**Safety**:  No ETL Automation |  No PII Processing |  Structure Validation Only  
**∞ AbëONE ∞**

