# Creative Genome Module

Defines the schema for creative assets, metadata, performance markers.

**Pattern**: MODULE × CREATIVE_GENOME × SCHEMA × ONE  
**Philosophy**: 80/20 → 97.8% Certainty  
**Safety**: No automated creative scoring. No mutation. Schema only.

---

## Purpose

The Creative Genome Module defines the schema for creative assets, metadata, and performance markers. It provides schema validation and registration but **does not perform any automated creative scoring** or **mutation** of assets.

---

## Schema

### Creative Asset Schema

```python
{
    "asset_id": str,                    # Required: Unique asset identifier
    "format": str,                      # Required: Asset format (e.g., "image", "video", "audio")
    "dimensions": tuple[int, int],      # Required: Asset dimensions (width, height)
    "duration": float,                  # Required: Asset duration in seconds
    "tags": list[str],                 # Optional: List of tags (defaults to [])
    "performance_markers": dict         # Optional: Performance markers dictionary (defaults to {})
}
```

### Field Details

- **asset_id** (str, required): Unique identifier for the creative asset. Must be a non-empty string.
- **format** (str, required): The format/type of the asset (e.g., `"image"`, `"video"`, `"audio"`, `"text"`). Must be a non-empty string.
- **dimensions** (tuple[int, int], required): Asset dimensions as a tuple of two integers `(width, height)`. Both values must be non-negative integers.
- **duration** (float, required): Asset duration in seconds. Must be a non-negative number (int or float).
- **tags** (list[str], optional): List of string tags associated with the asset. Defaults to empty list `[]` if not provided.
- **performance_markers** (dict, optional): Dictionary of performance markers/metrics. Defaults to empty dictionary `{}` if not provided.

---

## Safety Guarantees

### ✅ What This Module Does

- **Schema Definition**: Defines the structure for creative assets
- **Schema Validation**: Validates that asset data conforms to the schema
- **Asset Registration**: Registers validated assets with schema-only storage
- **Asset Retrieval**: Provides read-only access to registered assets

### 🚫 What This Module Does NOT Do

- **No Automated Creative Scoring**: Does not analyze or score creative quality
- **No Mutation**: Does not modify or transform asset data
- **No Performance Analysis**: Does not automatically analyze performance markers
- **No Content Processing**: Does not process or analyze asset content

---

## Events

### MODULE_EVENT.creative.register → MODULE_EVENT.creative_registered

**Event Flow**:
1. **Request**: Receive `creative.register` event with asset data
2. **Validation**: Validate asset schema (structure only, no scoring)
3. **Registration**: Register asset with schema-only storage
4. **Publication**: Publish `MODULE_EVENT.creative_registered` event
5. **Broadcast**: `creative_registered` event broadcast to MODULE_EVENT subscribers

**Event Data**:
```python
{
    "name": "creative.register",
    "asset": {
        "asset_id": "asset_123",
        "format": "video",
        "dimensions": (1920, 1080),
        "duration": 30.5,
        "tags": ["promo", "summer"],
        "performance_markers": {"views": 1000, "clicks": 50}
    }
}
```

**Response**:
```python
{
    "success": True,
    "asset_id": "asset_123",
    "status": "registered",
    "message": "Creative asset registered (schema only, no scoring, no mutation)"
}
```

### MODULE_EVENT.creative.validate

**Event Flow**:
1. **Request**: Receive `creative.validate` event with asset data
2. **Validation**: Validate asset schema (structure only, no scoring)
3. **Response**: Return validation result

**Event Data**:
```python
{
    "name": "creative.validate",
    "asset": {
        "asset_id": "asset_123",
        "format": "video",
        "dimensions": (1920, 1080),
        "duration": 30.5,
        "tags": ["promo", "summer"],
        "performance_markers": {"views": 1000, "clicks": 50}
    }
}
```

**Response**:
```python
{
    "success": True,
    "valid": True,
    "message": "Schema validation complete (no scoring, no mutation)"
}
```

### MODULE_EVENT.creative.get

**Event Flow**:
1. **Request**: Receive `creative.get` event with asset_id
2. **Retrieval**: Retrieve registered asset by asset_id
3. **Response**: Return asset schema or error

**Event Data**:
```python
{
    "name": "creative.get",
    "asset_id": "asset_123"
}
```

**Response**:
```python
{
    "success": True,
    "asset": {
        "asset_id": "asset_123",
        "format": "video",
        "dimensions": [1920, 1080],
        "duration": 30.5,
        "tags": ["promo", "summer"],
        "performance_markers": {"views": 1000, "clicks": 50}
    }
}
```

---

## Public API

### `register(asset_data: Dict[str, Any]) -> Dict[str, Any]`

Register a creative asset with schema validation.

**Args**:
- `asset_data`: Asset data dictionary with schema fields

**Returns**:
- Result dictionary with registration status

**Example**:
```python
from abëone.modules.creative_genome import CreativeGenomeModule

module = CreativeGenomeModule()
module.on_load()

result = module.register({
    "asset_id": "asset_123",
    "format": "video",
    "dimensions": (1920, 1080),
    "duration": 30.5,
    "tags": ["promo", "summer"],
    "performance_markers": {"views": 1000, "clicks": 50}
})

print(result)
# {
#     "success": True,
#     "asset_id": "asset_123",
#     "status": "registered",
#     "message": "Creative asset registered (schema only, no scoring, no mutation)"
# }
```

### `validate(asset_data: Dict[str, Any]) -> Dict[str, Any]`

Validate creative asset schema without registration.

**Args**:
- `asset_data`: Asset data dictionary to validate

**Returns**:
- Validation result dictionary

**Example**:
```python
result = module.validate({
    "asset_id": "asset_123",
    "format": "video",
    "dimensions": (1920, 1080),
    "duration": 30.5
})

print(result)
# {
#     "success": True,
#     "valid": True,
#     "message": "Schema validation complete (no scoring, no mutation)"
# }
```

### `get(asset_id: str) -> Dict[str, Any]`

Get creative asset by asset_id.

**Args**:
- `asset_id`: Asset identifier

**Returns**:
- Asset schema dictionary or error

**Example**:
```python
result = module.get("asset_123")

print(result)
# {
#     "success": True,
#     "asset": {
#         "asset_id": "asset_123",
#         "format": "video",
#         "dimensions": [1920, 1080],
#         "duration": 30.5,
#         "tags": ["promo", "summer"],
#         "performance_markers": {"views": 1000, "clicks": 50}
#     }
# }
```

### `get_all_assets() -> Dict[str, Any]`

Get all registered creative assets.

**Returns**:
- Dictionary with all registered assets

**Example**:
```python
result = module.get_all_assets()

print(result)
# {
#     "asset_count": 1,
#     "assets": [
#         {
#             "asset_id": "asset_123",
#             "format": "video",
#             "dimensions": [1920, 1080],
#             "duration": 30.5,
#             "tags": ["promo", "summer"],
#             "performance_markers": {"views": 1000, "clicks": 50}
#         }
#     ]
# }
```

---

## Usage Examples

### Basic Registration

```python
from abëone.modules.creative_genome import CreativeGenomeModule

module = CreativeGenomeModule()
module.on_load()

# Register a video asset
result = module.register({
    "asset_id": "summer_promo_video_001",
    "format": "video",
    "dimensions": (1920, 1080),
    "duration": 30.0,
    "tags": ["promo", "summer", "2024"],
    "performance_markers": {
        "views": 5000,
        "clicks": 250,
        "conversions": 10
    }
})

print(result["success"])  # True
```

### Image Asset

```python
# Register an image asset
result = module.register({
    "asset_id": "banner_image_001",
    "format": "image",
    "dimensions": (1200, 628),
    "duration": 0.0,  # Images have no duration
    "tags": ["banner", "social"],
    "performance_markers": {
        "impressions": 10000,
        "clicks": 150
    }
})
```

### Audio Asset

```python
# Register an audio asset
result = module.register({
    "asset_id": "jingle_audio_001",
    "format": "audio",
    "dimensions": (0, 0),  # Audio has no visual dimensions
    "duration": 15.5,
    "tags": ["jingle", "brand"],
    "performance_markers": {
        "plays": 2000,
        "completions": 1800
    }
})
```

### Validation Only

```python
# Validate without registering
validation_result = module.validate({
    "asset_id": "test_asset",
    "format": "video",
    "dimensions": (1920, 1080),
    "duration": 30.0
})

if validation_result["valid"]:
    print("Schema is valid!")
else:
    print(f"Validation error: {validation_result['error']}")
```

---

## Error Handling

### Missing Required Fields

```python
result = module.register({
    "format": "video",
    "dimensions": (1920, 1080),
    "duration": 30.0
    # Missing asset_id
})

print(result)
# {
#     "success": False,
#     "error": "Missing required field: asset_id"
# }
```

### Invalid Field Types

```python
result = module.register({
    "asset_id": "asset_123",
    "format": "video",
    "dimensions": "1920x1080",  # Invalid: should be tuple
    "duration": 30.0
})

print(result)
# {
#     "success": False,
#     "error": "dimensions must be a tuple of two integers"
# }
```

### Invalid Values

```python
result = module.register({
    "asset_id": "asset_123",
    "format": "video",
    "dimensions": (-1920, 1080),  # Invalid: negative width
    "duration": 30.0
})

print(result)
# {
#     "success": False,
#     "error": "dimensions must be non-negative integers"
# }
```

---

## Integration

### Event Bus Integration

The module subscribes to `MODULE_EVENT` and handles:
- `creative.register` → Registers asset and publishes `creative_registered`
- `creative.validate` → Validates asset schema
- `creative.get` → Retrieves asset by asset_id

### Module Registry Integration

The module implements `ModuleInterface` and can be registered with the Module Registry:

```python
from abëone.MODULE_REGISTRY import ModuleRegistry
from abëone.modules.creative_genome import CreativeGenomeModule

registry = ModuleRegistry()
module = CreativeGenomeModule()

registry.register_module(module)
registry.load_module(module.module_id)
```

---

## Safety Notes

### Schema-Only Operations

All operations are schema-only:
- ✅ Validation checks structure and types
- ✅ Registration stores schema data
- ✅ Retrieval returns schema data
- ❌ No content analysis
- ❌ No quality scoring
- ❌ No automatic mutation

### Performance Markers

The `performance_markers` field is stored as-is:
- ✅ Accepts any dictionary structure
- ✅ No validation of marker values
- ✅ No automatic analysis
- ✅ No mutation or transformation

### Tags

The `tags` field is stored as-is:
- ✅ Accepts any list of strings
- ✅ No validation of tag content
- ✅ No automatic tagging
- ✅ No tag normalization

---

**Pattern**: MODULE × CREATIVE_GENOME × SCHEMA × ONE  
**Safety**: No automated creative scoring. No mutation. Schema only.  
**∞ AbëONE ∞**

