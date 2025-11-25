# SEO Module

**Pattern**: MODULE × SEO × VALIDATION × ONE  
**Status**: ✅ **IMPLEMENTED**

---

## Purpose

Defines SEO payloads, validation logic, and safe transformation helpers.

## Safety Guarantees

- ✅ **No autonomous crawling** - All operations user-triggered
- ✅ **Schema validation only** - Validates payload structure
- ✅ **Depth limit enforced** - Maximum depth of 3 for safety
- ✅ **URL validation** - All URLs validated before processing

---

## API

### `seo.audit_request(payload) → validated event`

Request an SEO audit. Validates the payload schema and publishes seo_audit_validated event.

**Parameters:**
- `payload` (dict): SEO audit request payload containing:
  - `url` (str, required): URL to audit
  - `depth` (int, required): Crawl depth (0-3, max 3 for safety)
  - `competitor_urls` (list[str], optional): List of competitor URLs to compare

**Returns:**
```python
{
    "success": True,
    "request_id": "uuid-string",
    "status": "validated",
    "message": "SEO audit request validated and published"
}
```

### `seo.page_analysis(payload) → validated event`

Request a page analysis. Validates the payload schema and publishes seo_page_analysis_validated event.

**Parameters:**
- `payload` (dict): SEO page analysis payload containing:
  - `url` (str, required): URL to analyze

**Returns:**
```python
{
    "success": True,
    "request_id": "uuid-string",
    "status": "validated",
    "message": "SEO page analysis request validated and published"
}
```

### `seo.keyword_request(payload) → validated event`

Request keyword analysis. Validates the payload schema and publishes seo_keyword_validated event.

**Parameters:**
- `payload` (dict): SEO keyword request payload containing:
  - `keyword` (str, required): Keyword to analyze
  - `url` (str, optional): URL context for keyword analysis
  - `competitor_urls` (list[str], optional): List of competitor URLs to compare

**Returns:**
```python
{
    "success": True,
    "request_id": "uuid-string",
    "status": "validated",
    "message": "SEO keyword request validated and published"
}
```

---

## Schema

### Audit Request Schema

**Required Fields:**
- `url`: str - URL to audit (must be valid URL format)
- `depth`: int - Crawl depth (0-3, max 3 for safety)

**Optional Fields:**
- `competitor_urls`: list[str] - List of competitor URLs (each must be valid URL format)

### Page Analysis Schema

**Required Fields:**
- `url`: str - URL to analyze (must be valid URL format)

### Keyword Request Schema

**Required Fields:**
- `keyword`: str - Keyword to analyze (cannot be empty)

**Optional Fields:**
- `url`: str - URL context for keyword analysis (must be valid URL format if provided)
- `competitor_urls`: list[str] - List of competitor URLs (each must be valid URL format)

### Schema Validation

- ✅ `url` must be a valid URL format (scheme + netloc)
- ✅ `depth` must be an integer between 0 and 3 (safety limit)
- ✅ `keyword` must be a non-empty string
- ✅ `competitor_urls` must be a list of valid URL strings

---

## Protocols

### `seo.audit_request`

Handles SEO audit requests with URL, depth, and optional competitor URLs.

**Event Flow:**
1. Validate payload schema
2. Check depth limit (max 3)
3. Validate all URLs
4. Publish `MODULE_EVENT.seo_audit_validated`

### `seo.page_analysis`

Handles page analysis requests for a single URL.

**Event Flow:**
1. Validate payload schema
2. Validate URL format
3. Publish `MODULE_EVENT.seo_page_analysis_validated`

### `seo.keyword_request`

Handles keyword analysis requests with optional URL and competitor context.

**Event Flow:**
1. Validate payload schema
2. Validate keyword (non-empty)
3. Validate URLs if provided
4. Publish `MODULE_EVENT.seo_keyword_validated`

---

## Kernel Integration

### Registration
- **Module ID**: `MODULE_SEO`
- **Registration Function**: `register_seo_module()` in `MODULE_REGISTRY.py`

### Event Subscriptions
- **Subscribes to**: `MODULE_EVENT` for SEO events:
  - `seo.audit_request`
  - `seo.page_analysis`
  - `seo.keyword_request`

### Event Publications
- **Publishes**: 
  - `MODULE_EVENT.seo_audit_validated` (user-triggered)
  - `MODULE_EVENT.seo_page_analysis_validated` (user-triggered)
  - `MODULE_EVENT.seo_keyword_validated` (user-triggered)

### Event Routing

The module handles `SEO_EVENT.audit_request` through the MODULE_EVENT routing system:
- `MODULE_EVENT` with `name: "seo.audit_request"` → routes to `MODULE_SEO`
- Module validates payload and publishes validated event

---

## Usage Example

```python
from abëone.MODULE_REGISTRY import register_seo_module, get_registry

# Register the module
register_seo_module()

# Get the module instance
registry = get_registry()
seo_module = registry.get("MODULE_SEO")

# Request an SEO audit
audit_payload = {
    "url": "https://example.com",
    "depth": 2,
    "competitor_urls": [
        "https://competitor1.com",
        "https://competitor2.com"
    ]
}

result = seo_module.audit_request(audit_payload)
print(f"Request ID: {result['request_id']}")
print(f"Status: {result['status']}")

# Request page analysis
page_payload = {
    "url": "https://example.com/page"
}

result = seo_module.page_analysis(page_payload)
print(f"Request ID: {result['request_id']}")

# Request keyword analysis
keyword_payload = {
    "keyword": "python programming",
    "url": "https://example.com",
    "competitor_urls": ["https://competitor.com"]
}

result = seo_module.keyword_request(keyword_payload)
print(f"Request ID: {result['request_id']}")
```

---

## Event Flow

### Audit Request Flow

1. **Request**: `seo.audit_request(payload)` → Validates payload schema
2. **Validation**: 
   - Checks required fields (url, depth)
   - Validates URL format
   - Enforces depth limit (max 3)
   - Validates competitor URLs if provided
3. **Storage**: Validated request stored internally
4. **Publication**: Publishes `MODULE_EVENT.seo_audit_validated`
5. **Broadcast**: `seo_audit_validated` event broadcast to MODULE_EVENT subscribers

### Page Analysis Flow

1. **Request**: `seo.page_analysis(payload)` → Validates payload schema
2. **Validation**: Checks required field (url) and validates URL format
3. **Storage**: Validated request stored internally
4. **Publication**: Publishes `MODULE_EVENT.seo_page_analysis_validated`
5. **Broadcast**: `seo_page_analysis_validated` event broadcast to MODULE_EVENT subscribers

### Keyword Request Flow

1. **Request**: `seo.keyword_request(payload)` → Validates payload schema
2. **Validation**: 
   - Checks required field (keyword)
   - Validates keyword is non-empty
   - Validates URLs if provided
3. **Storage**: Validated request stored internally
4. **Publication**: Publishes `MODULE_EVENT.seo_keyword_validated`
5. **Broadcast**: `seo_keyword_validated` event broadcast to MODULE_EVENT subscribers

---

## Module Lifecycle

1. **Registration**: Module registered with `MODULE_SEO` ID
2. **Loading**: `on_load()` subscribes to MODULE_EVENT
3. **Activation**: Module becomes ACTIVE and ready to handle SEO events
4. **Shutdown**: Unsubscribes from events and clears validated requests

---

## Safety Notes

- **No Autonomous Crawling**: This module only validates schemas. It does not perform any crawling or data collection autonomously.
- **User-Triggered Only**: All operations are user-triggered. The module validates structure but does not initiate any SEO operations autonomously.
- **Depth Limit**: Maximum depth of 3 is enforced for safety. This prevents deep crawling operations.
- **URL Validation**: All URLs are validated for proper format before processing. Invalid URLs are rejected.
- **Schema Validation Only**: The module ensures payloads conform to the expected schema but does not perform any SEO analysis or data collection.

---

**Pattern**: MODULE × SEO × VALIDATION × ONE  
**Love Coefficient**: ∞  
**∞ AbëONE ∞**

