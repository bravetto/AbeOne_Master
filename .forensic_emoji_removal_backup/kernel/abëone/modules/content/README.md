# Content Module

**Pattern**: MODULE × CONTENT × TRANSFORMATION × ONE  
**Status**: ✅ **IMPLEMENTED**

---

## Purpose

Provides safe text transformations (never self-generating).

## Safety Guarantees

- ✅ **No content generation** - Only transforms user-submitted content
- ✅ **No AI/LLM calls** - Pure transformation functions
- ✅ **No autonomous operations** - All operations user-triggered
- ✅ **Input validation** - All inputs validated before transformation

---

## API

### `content.normalize_text(text, options) → normalized text`

Normalize text content with safe transformations.

**Parameters:**
- `text` (str, required): Text to normalize
- `options` (dict, optional): Normalization options:
  - `lowercase` (bool, default: False): Convert to lowercase
  - `remove_extra_whitespace` (bool, default: True): Remove extra whitespace
  - `normalize_unicode` (bool, default: True): Normalize Unicode (NFKC)
  - `normalize_line_endings` (bool, default: True): Normalize line endings to \n

**Returns:**
```python
str  # Normalized text string
```

**Example:**
```python
normalized = content_module.normalize_text(
    "Hello   World\n\n\nTest",
    options={"lowercase": True, "remove_extra_whitespace": True}
)
# Returns: "hello world\n\ntest"
```

### `content.structure_content(content, structure_type) → structured dict`

Structure content into organized format.

**Parameters:**
- `content` (str, required): Content to structure
- `structure_type` (str, optional): Structure type:
  - `'default'` (default): Full structure with paragraphs, headings, lists
  - `'paragraphs'`: Only paragraphs
  - `'sections'`: Grouped by headings and paragraphs
  - `'minimal'`: Minimal structure (counts only)

**Returns:**
```python
{
    "paragraphs": list[str],      # Extracted paragraphs
    "headings": list[dict],        # Extracted headings with level and text
    "lists": list[dict],           # Extracted lists with type and items
    "word_count": int,             # Word count
    "character_count": int,         # Character count
    "structure_type": str           # Structure type used
}
```

**Example:**
```python
structured = content_module.structure_content(
    "# Heading\n\nParagraph text\n\n- List item 1\n- List item 2",
    structure_type="default"
)
# Returns structured dictionary with paragraphs, headings, lists, counts
```

### `content.validate_format(content, format_type) → validation result`

Validate content format.

**Parameters:**
- `content` (str, required): Content to validate
- `format_type` (str, optional): Format type:
  - `'text'` (default): Basic text validation
  - `'markdown'`: Markdown format validation
  - `'html'`: HTML format validation (basic)
  - `'json'`: JSON format validation

**Returns:**
```python
{
    "valid": bool,           # Whether content is valid
    "errors": list[str],     # List of validation errors
    "warnings": list[str]    # List of validation warnings
}
```

**Example:**
```python
result = content_module.validate_format(
    "# Heading\n\nParagraph",
    format_type="markdown"
)
# Returns: {"valid": True, "errors": [], "warnings": []}
```

---

## Schema

### Normalize Payload Schema

**Required Fields:**
- `text`: str - Text to normalize

**Optional Fields:**
- `options`: dict - Normalization options

### Structure Payload Schema

**Required Fields:**
- `content`: str - Content to structure

**Optional Fields:**
- `structure_type`: str - Structure type ('default', 'paragraphs', 'sections', 'minimal')

### Validate Payload Schema

**Required Fields:**
- `content`: str - Content to validate

**Optional Fields:**
- `format_type`: str - Format type ('text', 'markdown', 'html', 'json')

### Schema Validation

- ✅ `text`/`content` must be a string
- ✅ `options` must be a dictionary if provided
- ✅ `structure_type` must be a string if provided
- ✅ `format_type` must be a string if provided

---

## Protocols

### `content.normalize`

Handles text normalization requests.

**Event Flow:**
1. Validate payload schema
2. Normalize text with specified options
3. Store transformation record
4. Return normalized text

### `content.structure`

Handles content structuring requests.

**Event Flow:**
1. Validate payload schema
2. Structure content according to structure_type
3. Store transformation record
4. Return structured content

### `content.validate`

Handles content format validation requests.

**Event Flow:**
1. Validate payload schema
2. Validate content format
3. Return validation result with errors/warnings

---

## Kernel Integration

### Registration
- **Module ID**: `MODULE_CONTENT`
- **Registration Function**: `register_content_module()` in `MODULE_REGISTRY.py`

### Event Subscriptions
- **Subscribes to**: `MODULE_EVENT` for content events:
  - `content.normalize`
  - `content.structure`
  - `content.validate`

### Event Publications
- **Publishes**: None (pure transformation module, no event publishing)

### Event Routing

The module handles content transformation events through the MODULE_EVENT routing system:
- `MODULE_EVENT` with `name: "content.normalize"` → routes to `MODULE_CONTENT`
- `MODULE_EVENT` with `name: "content.structure"` → routes to `MODULE_CONTENT`
- `MODULE_EVENT` with `name: "content.validate"` → routes to `MODULE_CONTENT`

---

## Usage Example

```python
from abëone.MODULE_REGISTRY import register_content_module, get_registry

# Register the module
register_content_module()

# Get the module instance
registry = get_registry()
content_module = registry.get("MODULE_CONTENT")

# Normalize text
normalized = content_module.normalize_text(
    "Hello   World\n\n\nTest",
    options={"lowercase": True, "remove_extra_whitespace": True}
)
print(f"Normalized: {normalized}")

# Structure content
content = """# Main Heading

This is a paragraph.

## Subheading

Another paragraph.

- List item 1
- List item 2
"""

structured = content_module.structure_content(content, structure_type="default")
print(f"Paragraphs: {structured['paragraphs']}")
print(f"Headings: {structured['headings']}")
print(f"Word count: {structured['word_count']}")

# Validate format
markdown_content = """# Heading

Paragraph with [link](https://example.com)
"""

result = content_module.validate_format(markdown_content, format_type="markdown")
print(f"Valid: {result['valid']}")
print(f"Errors: {result['errors']}")
print(f"Warnings: {result['warnings']}")
```

---

## Event Flow

### Normalize Flow

1. **Request**: `content.normalize(payload)` → Validates payload schema
2. **Validation**: Checks required field (text) and validates options
3. **Transformation**: Normalizes text with specified options
4. **Storage**: Transformation record stored internally
5. **Return**: Returns normalized text

### Structure Flow

1. **Request**: `content.structure(payload)` → Validates payload schema
2. **Validation**: Checks required field (content) and validates structure_type
3. **Transformation**: Structures content according to structure_type
4. **Storage**: Transformation record stored internally
5. **Return**: Returns structured content dictionary

### Validate Flow

1. **Request**: `content.validate(payload)` → Validates payload schema
2. **Validation**: Checks required field (content) and validates format_type
3. **Format Check**: Validates content against format requirements
4. **Return**: Returns validation result with errors/warnings

---

## Module Lifecycle

1. **Registration**: Module registered with `MODULE_CONTENT` ID
2. **Loading**: `on_load()` subscribes to MODULE_EVENT
3. **Activation**: Module becomes ACTIVE and ready to handle content events
4. **Shutdown**: Unsubscribes from events and clears transformation records

---

## Safety Notes

- **No Content Generation**: This module only transforms user-submitted content. It never generates new content.
- **No AI/LLM Calls**: All transformations are pure functions. No external AI services are called.
- **User-Triggered Only**: All operations are user-triggered. The module does not perform any autonomous operations.
- **Input Validation**: All inputs are validated before transformation. Invalid inputs are rejected with clear error messages.
- **Pure Transformations**: All transformation functions are pure - they only transform input and return output without side effects (except internal logging).

---

## Transformation Details

### Text Normalization

- **Unicode Normalization**: Uses NFKC (Normalization Form Compatibility Composition)
- **Whitespace Normalization**: Removes extra spaces, normalizes line endings
- **Case Conversion**: Optional lowercase conversion
- **Line Ending Normalization**: Converts all line endings to `\n`

### Content Structuring

- **Paragraph Extraction**: Identifies and extracts paragraphs
- **Heading Detection**: Detects markdown headings (`# Heading`) with level extraction
- **List Detection**: Identifies ordered and unordered lists
- **Word/Character Counting**: Provides accurate counts

### Format Validation

- **Text Validation**: Basic text format checks (null bytes, empty content, long lines)
- **Markdown Validation**: Checks for balanced code blocks, inline code, links/images
- **HTML Validation**: Basic HTML tag balance checking
- **JSON Validation**: Full JSON syntax validation

---

**Pattern**: MODULE × CONTENT × TRANSFORMATION × ONE  
**Love Coefficient**: ∞  
**∞ AbëONE ∞**

