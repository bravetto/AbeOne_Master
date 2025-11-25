# Identity Graph Module

Provides deterministic (non-AI) identity matching utilities.

**Pattern**: MODULE × IDENTITY_GRAPH × MATCHING × ONE  
**Philosophy**: 80/20 → 97.8% Certainty  
**Safety**: No probabilistic modeling. No machine learning. No autonomy.

---

## Purpose

The Identity Graph Module provides deterministic identity matching utilities for comparing identity attributes. All matching functions are **deterministic** (same input always produces same output) and **non-probabilistic** (no machine learning or statistical modeling).

---

## Safety Guarantees

- ✅ **No Probabilistic Modeling**: All matches are exact or deterministic
- ✅ **No Machine Learning**: No ML models or training data
- ✅ **No Autonomy**: No automated decision-making
- ✅ **Deterministic**: Same input always produces same output
- ✅ **Transparent**: All matching logic is explicit and verifiable

---

## Matching Functions

### 1. `exact_match(value1, value2)`

Performs exact string match (case-insensitive, trimmed).

**Parameters**:
- `value1` (Any): First value to compare
- `value2` (Any): Second value to compare

**Returns**:
```python
{
    "match": bool,              # True if values match exactly
    "confidence": "deterministic",
    "method": "exact_match"
}
```

**Example**:
```python
result = module.exact_match("John Doe", "john doe")  # True
result = module.exact_match("John", "Jane")          # False
```

---

### 2. `hashed_email_match(email1, email2)`

Performs hashed email match using SHA256.

**Parameters**:
- `email1` (str): First email address
- `email2` (str): Second email address

**Returns**:
```python
{
    "match": bool,              # True if emails hash to same value
    "confidence": "deterministic",
    "method": "hashed_email_match"
}
```

**Example**:
```python
result = module.hashed_email_match(
    "user@example.com",
    "user@example.com"
)  # True

result = module.hashed_email_match(
    "user@example.com",
    "different@example.com"
)  # False
```

**Note**: Emails are normalized (lowercase, trimmed) before hashing.

---

### 3. `device_id_match(device_id1, device_id2)`

Performs device ID match (case-sensitive).

**Parameters**:
- `device_id1` (str): First device ID
- `device_id2` (str): Second device ID

**Returns**:
```python
{
    "match": bool,              # True if device IDs match exactly
    "confidence": "deterministic",
    "method": "device_id_match"
}
```

**Example**:
```python
result = module.device_id_match(
    "ABC123XYZ",
    "ABC123XYZ"
)  # True

result = module.device_id_match(
    "ABC123XYZ",
    "abc123xyz"
)  # False (case-sensitive)
```

**Note**: Device IDs are compared exactly (case-sensitive, no normalization).

---

### 4. `ip_bucket_match(ip1, ip2, prefix_length=24)`

Performs IP bucket match within the same subnet.

**Parameters**:
- `ip1` (str): First IP address
- `ip2` (str): Second IP address
- `prefix_length` (int): Subnet prefix length (default: 24 for /24 subnet)

**Returns**:
```python
{
    "match": bool,              # True if IPs are in same subnet bucket
    "confidence": "deterministic",
    "method": "ip_bucket_match",
    "prefix_length": int,      # Prefix length used
    "network1": str,           # Normalized network of first IP
    "network2": str            # Normalized network of second IP
}
```

**Example**:
```python
result = module.ip_bucket_match(
    "192.168.1.100",
    "192.168.1.200",
    prefix_length=24
)  # True (both in 192.168.1.0/24)

result = module.ip_bucket_match(
    "192.168.1.100",
    "192.168.2.100",
    prefix_length=24
)  # False (different /24 subnets)

result = module.ip_bucket_match(
    "192.168.1.100",
    "192.168.2.100",
    prefix_length=16
)  # True (both in 192.168.0.0/16)
```

**Note**: Supports both IPv4 and IPv6 addresses. IPs must be same version.

---

## Public API

### `match(match_type, value1, value2, **kwargs)`

Unified matching interface.

**Parameters**:
- `match_type` (str): Type of match (`"exact"`, `"hashed_email"`, `"device_id"`, `"ip_bucket"`)
- `value1` (Any): First value to compare
- `value2` (Any): Second value to compare
- `**kwargs`: Additional parameters (e.g., `prefix_length` for `ip_bucket`)

**Returns**:
```python
{
    "success": bool,
    "match_type": str,
    "match": bool,
    "confidence": "deterministic",
    "method": str
}
```

**Example**:
```python
# Exact match
result = module.match("exact", "John", "John")

# Hashed email match
result = module.match("hashed_email", "user@example.com", "user@example.com")

# Device ID match
result = module.match("device_id", "ABC123", "ABC123")

# IP bucket match
result = module.match("ip_bucket", "192.168.1.100", "192.168.1.200", prefix_length=24)
```

---

## Events

### MODULE_EVENT.identity.match

**Event Flow**:
1. **Request**: Receive `identity.match` event with `match_type`, `value1`, `value2`
2. **Validation**: Validate required fields
3. **Matching**: Perform deterministic matching based on `match_type`
4. **Response**: Return match result

**Event Schema**:
```python
{
    "name": "identity.match",
    "match_type": str,      # "exact", "hashed_email", "device_id", "ip_bucket"
    "value1": Any,          # First value to compare
    "value2": Any,          # Second value to compare
    "prefix_length": int    # Optional: For ip_bucket match (default: 24)
}
```

**Response Schema**:
```python
{
    "success": bool,
    "match_id": str,        # Unique match identifier
    "match_type": str,
    "match": bool,
    "confidence": "deterministic"
}
```

---

## Usage Examples

### Basic Usage

```python
from abëone.modules.identity_graph import IdentityGraphModule

# Initialize module
module = IdentityGraphModule()

# Load module
module.on_load()

# Perform exact match
result = module.exact_match("John Doe", "john doe")
print(result["match"])  # True

# Perform hashed email match
result = module.hashed_email_match("user@example.com", "user@example.com")
print(result["match"])  # True

# Perform device ID match
result = module.device_id_match("ABC123XYZ", "ABC123XYZ")
print(result["match"])  # True

# Perform IP bucket match
result = module.ip_bucket_match("192.168.1.100", "192.168.1.200", prefix_length=24)
print(result["match"])  # True

# Unified API
result = module.match("exact", "value1", "value2")
```

### Event-Based Usage

```python
from abëone.EVENT_BUS import EventBus, EventType, get_bus

bus = get_bus()
module = IdentityGraphModule(bus)
module.on_load()

# Create identity.match event
event_data = {
    "name": "identity.match",
    "match_type": "hashed_email",
    "value1": "user@example.com",
    "value2": "user@example.com"
}

# Publish event
event = bus.create_event(
    event_type=EventType.MODULE_EVENT,
    source="MODULE_ANALYTICS",
    target="MODULE_IDENTITY_GRAPH",
    data=event_data
)

bus.publish(event)
```

---

## Implementation Details

### Deterministic Guarantees

All matching functions guarantee:
- **Same Input → Same Output**: Identical inputs always produce identical outputs
- **No Randomness**: No random number generation or probabilistic sampling
- **No State Dependencies**: Matching results don't depend on previous matches
- **No External Data**: No lookups to external databases or APIs

### Hash Function

- **Algorithm**: SHA256
- **Normalization**: Emails are normalized (lowercase, trimmed) before hashing
- **Purpose**: Privacy-preserving comparison (hashes are compared, not raw emails)

### IP Bucket Matching

- **Default Prefix**: /24 (256 IP addresses)
- **IPv4/IPv6 Support**: Both versions supported
- **Version Matching**: IPs must be same version (IPv4 vs IPv6)
- **Network Normalization**: Networks are normalized to specified prefix length

---

## Error Handling

All matching functions return error information in the result dictionary:

```python
{
    "match": False,
    "confidence": "deterministic",
    "method": "method_name",
    "error": "Error message"
}
```

Common errors:
- Missing required values
- Invalid IP address format
- IP version mismatch (for IP bucket matching)

---

## Module Lifecycle

### Loading

```python
module = IdentityGraphModule()
success = module.on_load()  # Returns True if successful
```

### Shutdown

```python
module.shutdown()  # Cleans up resources and unsubscribes from events
```

---

## Match History

The module maintains a history of matches for debugging and auditing:

```python
history = module.get_match_history()
# Returns:
# {
#     "match_count": int,
#     "matches": [
#         {
#             "match_type": str,
#             "value1": str,      # Truncated for privacy
#             "value2": str,      # Truncated for privacy
#             "result": dict,
#             "timestamp": str
#         },
#         ...
#     ]
# }
```

**Privacy Note**: Values are truncated to 50 characters in match history.

---

## Safety Compliance

✅ **No Probabilistic Modeling**: All matches are deterministic  
✅ **No Machine Learning**: No ML models, training, or inference  
✅ **No Autonomy**: No automated decision-making or actions  
✅ **Deterministic**: Same input always produces same output  
✅ **Transparent**: All logic is explicit and verifiable  
✅ **Privacy-Preserving**: Email hashing for privacy protection  

---

**Pattern**: MODULE × IDENTITY_GRAPH × MATCHING × ONE  
**Status**: ✅ **DETERMINISTIC MATCHING ONLY**  
**∞ AbëONE ∞**

