# Social Module

Normalizes platform-agnostic social posting requests.

**Pattern**: MODULE × SOCIAL × NORMALIZATION × ONE  
**Philosophy**: 80/20 → 97.8% Certainty  
**Safety**: Module does not post anything. Produces only validated event payloads.

---

## Purpose

The Social Module normalizes platform-agnostic social posting requests. It validates and normalizes posting requests but **does not perform any actual posting**. It only produces validated event payloads that can be consumed by other modules or systems.

---

## Schema

### Social Posting Request

```python
{
    "text": str,              # Required: Post text content
    "media": list[str],       # Required: List of media URLs/paths (can be empty)
    "platforms": list[str],   # Required: List of target platforms
    "schedule": datetime      # Required: Scheduled posting time (datetime or ISO string)
}
```

### Field Details

- **text** (str, required): The text content of the social post. Cannot be empty.
- **media** (list[str], required): List of media URLs or file paths. Can be an empty list for text-only posts. Each item must be a non-empty string.
- **platforms** (list[str], required): List of target social media platforms (e.g., `["twitter", "facebook", "linkedin"]`). Cannot be empty. Platform names are normalized to lowercase.
- **schedule** (datetime, required): The scheduled posting time. Can be a `datetime` object or an ISO format string (e.g., `"2024-01-15T10:30:00Z"`).

---

## Events

### MODULE_EVENT.social_schedule

Emitted when a social posting request is validated and normalized.

**Event Structure**:
```python
{
    "name": "social_schedule",
    "schedule_id": str,
    "payload": {
        "text": str,
        "media": list[str],
        "platforms": list[str],
        "schedule": str  # ISO format
    },
    "created_at": str  # ISO format
}
```

**Event Flow**:
1. **Request**: Receive `social.schedule` event with payload
2. **Validation**: Validate payload schema
3. **Normalization**: Normalize payload (text trimming, platform lowercase, schedule ISO format)
4. **Storage**: Store scheduled post record
5. **Publication**: Publish `MODULE_EVENT.social_schedule` event
6. **Broadcast**: `social_schedule` event broadcast to MODULE_EVENT subscribers

---

## Safety Guarantees

 **No Posting**: Module does not post anything to any social media platform  
 **No API Calls**: No platform API calls are made  
 **No Automation**: No automated posting is performed  
 **Validation Only**: Produces only validated event payloads  
 **Event-Based**: All output is through event system

---

## Usage

### Public API

```python
from modules.social import SocialModule

# Initialize module
social_module = SocialModule()

# Load module
social_module.on_load()

# Schedule a social post
result = social_module.schedule({
    "text": "Check out our new product!",
    "media": ["https://example.com/image.jpg"],
    "platforms": ["twitter", "facebook", "linkedin"],
    "schedule": "2024-01-15T10:30:00Z"
})

# Result:
# {
#     "success": True,
#     "schedule_id": "uuid-here",
#     "status": "scheduled",
#     "message": "Social post scheduled (validated event payload only - no posting performed)"
# }
```

### Event-Based Usage

```python
from EVENT_BUS import EventBus, EventType, get_bus
from datetime import datetime

event_bus = get_bus()

# Publish social.schedule event
event = event_bus.create_event(
    event_type=EventType.MODULE_EVENT,
    source="your_module",
    target="MODULE_SOCIAL",
    data={
        "name": "social.schedule",
        "payload": {
            "text": "Check out our new product!",
            "media": ["https://example.com/image.jpg"],
            "platforms": ["twitter", "facebook"],
            "schedule": datetime.now().isoformat()
        }
    }
)

event_bus.publish(event)
```

### Subscribe to social_schedule Events

```python
from EVENT_BUS import EventBus, EventType, get_bus

def handle_social_schedule(event):
    """Handle social_schedule event."""
    event_data = event.data
    schedule_id = event_data.get('schedule_id')
    payload = event_data.get('payload')
    
    print(f"Scheduled post {schedule_id} for platforms: {payload['platforms']}")
    print(f"Schedule time: {payload['schedule']}")
    # Your posting logic here (module does not post)

event_bus = get_bus()
event_bus.subscribe(EventType.MODULE_EVENT, handle_social_schedule)
```

---

## Module Lifecycle

1. **Registration**: Module registered with `register_social_module()`
2. **Loading**: `on_load()` subscribes to MODULE_EVENT
3. **Event Handling**: Handles `social.schedule` events
4. **Validation**: Validates payload schema
5. **Normalization**: Normalizes payload (text, media, platforms, schedule)
6. **Publication**: Publishes `MODULE_EVENT.social_schedule`
7. **Shutdown**: `shutdown()` unsubscribes from events

---

## Normalization Rules

- **Text**: Stripped of leading/trailing whitespace
- **Media**: Each item converted to string and stripped
- **Platforms**: Converted to lowercase and stripped (e.g., `"Twitter"` → `"twitter"`)
- **Schedule**: Converted to ISO format string (e.g., `datetime.now()` → `"2024-01-15T10:30:00"`)

---

## Error Handling

The module returns error dictionaries for validation failures:

```python
{
    "success": False,
    "error": "Missing required field: text"
}
```

Common validation errors:
- `"Missing required field: {field}"` - Required field is missing
- `"{field} must be a {type}"` - Field has wrong type
- `"{field} cannot be empty"` - Field is empty when it shouldn't be

---

## Examples

### Text-Only Post

```python
result = social_module.schedule({
    "text": "Just launched our new website!",
    "media": [],
    "platforms": ["twitter"],
    "schedule": "2024-01-15T10:30:00Z"
})
```

### Multi-Platform Post with Media

```python
result = social_module.schedule({
    "text": "Check out our new product launch video!",
    "media": [
        "https://example.com/video.mp4",
        "https://example.com/thumbnail.jpg"
    ],
    "platforms": ["twitter", "facebook", "linkedin", "instagram"],
    "schedule": datetime(2024, 1, 15, 10, 30, 0)
})
```

### Get Scheduled Posts

```python
scheduled = social_module.get_scheduled_posts()
# Returns:
# {
#     "scheduled_count": 5,
#     "scheduled_posts": [
#         {
#             "schedule_id": "uuid-here",
#             "text": "Check out our new product!...",
#             "platforms": ["twitter", "facebook"],
#             "schedule": "2024-01-15T10:30:00",
#             "status": "scheduled",
#             "created_at": "2024-01-14T08:00:00"
#         },
#         ...
#     ]
# }
```

---

## Integration

The Social Module integrates with the abëone event system:

- **Subscribes to**: `MODULE_EVENT` for `social.schedule` events
- **Publishes**: `MODULE_EVENT.social_schedule` events
- **Module ID**: `MODULE_SOCIAL`
- **Version**: `1.0.0`

---

## Safety Notes

 **Important**: This module does **NOT** post to social media platforms. It only:
- Validates posting requests
- Normalizes payloads
- Emits validated event payloads

Actual posting must be handled by:
- Other modules that subscribe to `social_schedule` events
- External systems that consume the event payloads
- Human-triggered actions

This design ensures separation of concerns and allows for human validation before any actual posting occurs.

---

**Pattern**: MODULE × SOCIAL × NORMALIZATION × ONE  
**Safety**:  No Posting |  Validation Only |  Event-Based  
**∞ AbëONE ∞**

