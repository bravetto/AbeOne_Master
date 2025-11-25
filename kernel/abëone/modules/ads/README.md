# Ads Module

**Pattern**: MODULE × ADS × HUMAN-TRIGGERED × ONE  
**Status**:  **IMPLEMENTED**

---

## Purpose

Provides a safe, human-triggered interface for defining advertising requests across any channel.

## Safety Guarantees

-  **No automated bidding** - All requests require human validation
-  **No autonomous optimization** - Human approval required for all campaigns
-  **Human-triggered validation** - All ad_validated events are human-initiated

---

## API

### `ads.request(payload) → queued event`

Request an ad campaign. Creates a queued event for human validation.

**Parameters:**
- `payload` (dict): Ad request payload containing:
  - `campaign_name` (str, required): Name of the campaign
  - `platforms` (list[str], required): List of advertising platforms
  - `budget` (float, required): Campaign budget (must be positive)
  - `targeting` (dict, optional): Targeting parameters
  - `creatives` (dict, optional): Creative assets
  - `schedule` (dict, optional): Scheduling information
  - `constraints` (dict, optional): Campaign constraints

**Returns:**
```python
{
    "success": True,
    "request_id": "uuid-string",
    "status": "queued",
    "message": "Ad request queued for human validation"
}
```

---

## Schema

### Required Fields
- `campaign_name`: str
- `platforms`: list[str]
- `budget`: float (must be > 0)

### Optional Fields
- `targeting`: dict
- `creatives`: dict
- `schedule`: dict
- `constraints`: dict

---

## Kernel Integration

### Registration
- **Module ID**: `MODULE_ADS`
- **Registration Function**: `register_ads_module()` in `MODULE_REGISTRY.py`

### Event Subscriptions
- **Subscribes to**: `MODULE_EVENT.ad_request`
  - Routes ad requests to the module for queuing

### Event Publications
- **Publishes**: `MODULE_EVENT.ad_validated` (human-triggered)
  - Published when a human validates a queued request
  - Contains validated request payload and validation notes

---

## Usage Example

```python
from abëone.MODULE_REGISTRY import register_ads_module, get_registry

# Register the module
register_ads_module()

# Get the module instance
registry = get_registry()
ads_module = registry.get("MODULE_ADS")

# Request an ad campaign
payload = {
    "campaign_name": "Summer Sale 2024",
    "platforms": ["google", "facebook", "twitter"],
    "budget": 10000.0,
    "targeting": {
        "age_range": [25, 45],
        "interests": ["technology", "music"]
    },
    "creatives": {
        "headline": "Summer Sale - 50% Off",
        "description": "Limited time offer"
    },
    "schedule": {
        "start_date": "2024-06-01",
        "end_date": "2024-08-31"
    },
    "constraints": {
        "max_daily_budget": 500.0
    }
}

result = ads_module.request(payload)
print(f"Request ID: {result['request_id']}")
print(f"Status: {result['status']}")

# Check queue status
status = ads_module.get_queue_status()
print(f"Queued requests: {status['queued_count']}")

# Human validation (triggered externally)
validation_event = {
    "name": "ad_validate",
    "request_id": result['request_id'],
    "validated": True,
    "validation_notes": "Approved for launch"
}

validation_result = ads_module.on_event({
    "data": validation_event
})
```

---

## Event Flow

1. **Request**: `ads.request(payload)` → Creates queued event
2. **Queue**: Request added to internal queue with status "queued"
3. **Human Validation**: External system triggers `ad_validate` event
4. **Validation**: If validated, publishes `MODULE_EVENT.ad_validated`
5. **Publication**: `ad_validated` event broadcast to MODULE_EVENT subscribers

---

## Module Lifecycle

1. **Registration**: Module registered with `MODULE_ADS` ID
2. **Loading**: `on_load()` subscribes to MODULE_EVENT
3. **Activation**: Module becomes ACTIVE and ready to handle requests
4. **Shutdown**: Unsubscribes from events and clears queues

---

**Pattern**: MODULE × ADS × HUMAN-TRIGGERED × ONE  
**Love Coefficient**: ∞  
**∞ AbëONE ∞**

