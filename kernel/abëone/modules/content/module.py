"""
Content Module - Core Interface

Provides safe text transformations (never self-generating).

Pattern: MODULE × CONTENT × TRANSFORMATION × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: No content generation. Only transforms user-submitted content.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import re
import unicodedata

# Import kernel components
import sys
from pathlib import Path

# Add abëone directory to path
abeone_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(abeone_dir))

from EVENT_BUS import EventBus, Event, EventType, get_bus
from MODULE_REGISTRY import ModuleInterface


class ContentModule(ModuleInterface):
    """
    Content Module.
    
    Provides safe text transformations (never self-generating).
    
    Safety Guarantees:
    - No content generation
    - Only transforms user-submitted content
    - No AI/LLM calls
    - Pure transformation functions
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize Content Module.
        
        Args:
            event_bus: Optional event bus instance (defaults to global instance)
        """
        self._event_bus = event_bus or get_bus()
        self._loaded = False
        self._transformations: Dict[str, Dict[str, Any]] = {}
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        return "MODULE_CONTENT"
    
    @property
    def version(self) -> str:
        """Get module version."""
        return "1.0.0"
    
    def on_load(self) -> bool:
        """
        Called when module is loaded.
        
        Sets up event subscriptions and initializes the module.
        
        Returns:
            True if load successful
        """
        try:
            print(" Content Module: Loading...")
            
            # Subscribe to MODULE_EVENT for content events
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print(" Content Module: Loaded successfully")
            return True
        except Exception as e:
            print(f" Content Module: Load failed - {e}")
            return False
    
    def on_event(self, event: Any) -> Any:
        """
        Called when module receives an event.
        
        Args:
            event: Event to handle
            
        Returns:
            Event handling result
        """
        if not self._loaded:
            return {"error": "Module not loaded"}
        
        # Extract event data
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        if isinstance(event, dict):
            event_data = event
        
        # Handle content events
        event_name = event_data.get('name', '')
        
        if event_name == "content.normalize":
            return self._handle_normalize(event_data)
        elif event_name == "content.structure":
            return self._handle_structure(event_data)
        elif event_name == "content.validate":
            return self._handle_validate(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes content events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route content events to this module
        content_events = ["content.normalize", "content.structure", "content.validate"]
        if event_name in content_events and (not event.target or event.target == self.module_id):
            self.on_event(event)
    
    def _handle_normalize(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle content.normalize event.
        
        Normalizes user-submitted text content.
        
        Args:
            event_data: Event data containing normalization request
            
        Returns:
            Result dictionary with normalized content
        """
        try:
            # Extract payload
            payload = event_data.get('payload', event_data)
            
            # Validate payload
            validation_result = self._validate_normalize_payload(payload)
            if not validation_result['valid']:
                return {
                    "success": False,
                    "error": validation_result['error']
                }
            
            # Normalize text
            text = payload.get('text')
            options = payload.get('options', {})
            normalized = self.normalize_text(text, options)
            
            # Generate transformation ID
            transformation_id = str(uuid.uuid4())
            
            # Store transformation
            self._transformations[transformation_id] = {
                "transformation_id": transformation_id,
                "type": "normalize",
                "input": text,
                "output": normalized,
                "options": options,
                "created_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "transformation_id": transformation_id,
                "normalized": normalized
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _handle_structure(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle content.structure event.
        
        Structures user-submitted content.
        
        Args:
            event_data: Event data containing structure request
            
        Returns:
            Result dictionary with structured content
        """
        try:
            # Extract payload
            payload = event_data.get('payload', event_data)
            
            # Validate payload
            validation_result = self._validate_structure_payload(payload)
            if not validation_result['valid']:
                return {
                    "success": False,
                    "error": validation_result['error']
                }
            
            # Structure content
            content = payload.get('content')
            structure_type = payload.get('structure_type', 'default')
            structured = self.structure_content(content, structure_type)
            
            # Generate transformation ID
            transformation_id = str(uuid.uuid4())
            
            # Store transformation
            self._transformations[transformation_id] = {
                "transformation_id": transformation_id,
                "type": "structure",
                "input": content,
                "output": structured,
                "structure_type": structure_type,
                "created_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "transformation_id": transformation_id,
                "structured": structured
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _handle_validate(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle content.validate event.
        
        Validates content format.
        
        Args:
            event_data: Event data containing validation request
            
        Returns:
            Result dictionary with validation result
        """
        try:
            # Extract payload
            payload = event_data.get('payload', event_data)
            
            # Validate payload
            validation_result = self._validate_validate_payload(payload)
            if not validation_result['valid']:
                return {
                    "success": False,
                    "error": validation_result['error']
                }
            
            # Validate format
            content = payload.get('content')
            format_type = payload.get('format_type', 'text')
            validation_result = self.validate_format(content, format_type)
            
            return {
                "success": True,
                "valid": validation_result['valid'],
                "errors": validation_result.get('errors', []),
                "warnings": validation_result.get('warnings', [])
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_normalize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate normalize payload schema.
        
        Required fields:
        - text: str
        
        Optional fields:
        - options: dict
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        # Validate text: str (required)
        text = payload.get('text')
        if text is None:
            return {
                "valid": False,
                "error": "Missing required field: text"
            }
        if not isinstance(text, str):
            return {
                "valid": False,
                "error": "text must be a string"
            }
        
        # Validate options: dict (optional)
        options = payload.get('options')
        if options is not None and not isinstance(options, dict):
            return {
                "valid": False,
                "error": "options must be a dictionary"
            }
        
        return {"valid": True}
    
    def _validate_structure_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate structure payload schema.
        
        Required fields:
        - content: str
        
        Optional fields:
        - structure_type: str
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        # Validate content: str (required)
        content = payload.get('content')
        if content is None:
            return {
                "valid": False,
                "error": "Missing required field: content"
            }
        if not isinstance(content, str):
            return {
                "valid": False,
                "error": "content must be a string"
            }
        
        # Validate structure_type: str (optional)
        structure_type = payload.get('structure_type')
        if structure_type is not None and not isinstance(structure_type, str):
            return {
                "valid": False,
                "error": "structure_type must be a string"
            }
        
        return {"valid": True}
    
    def _validate_validate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate validate payload schema.
        
        Required fields:
        - content: str
        
        Optional fields:
        - format_type: str
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        # Validate content: str (required)
        content = payload.get('content')
        if content is None:
            return {
                "valid": False,
                "error": "Missing required field: content"
            }
        if not isinstance(content, str):
            return {
                "valid": False,
                "error": "content must be a string"
            }
        
        # Validate format_type: str (optional)
        format_type = payload.get('format_type')
        if format_type is not None and not isinstance(format_type, str):
            return {
                "valid": False,
                "error": "format_type must be a string"
            }
        
        return {"valid": True}
    
    def normalize_text(self, text: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Normalize text content.
        
        Performs safe text transformations:
        - Unicode normalization (NFKC)
        - Whitespace normalization
        - Line ending normalization
        - Optional: lowercase conversion
        - Optional: remove extra whitespace
        
        SAFETY: Only transforms user-submitted content. Never generates new content.
        
        Args:
            text: Text to normalize
            options: Optional normalization options:
                - lowercase: bool (default: False)
                - remove_extra_whitespace: bool (default: True)
                - normalize_unicode: bool (default: True)
                - normalize_line_endings: bool (default: True)
        
        Returns:
            Normalized text string
        """
        if not isinstance(text, str):
            raise ValueError("text must be a string")
        
        options = options or {}
        lowercase = options.get('lowercase', False)
        remove_extra_whitespace = options.get('remove_extra_whitespace', True)
        normalize_unicode = options.get('normalize_unicode', True)
        normalize_line_endings = options.get('normalize_line_endings', True)
        
        normalized = text
        
        # Unicode normalization (NFKC - compatibility decomposition + composition)
        if normalize_unicode:
            normalized = unicodedata.normalize('NFKC', normalized)
        
        # Line ending normalization (convert all to \n)
        if normalize_line_endings:
            normalized = normalized.replace('\r\n', '\n').replace('\r', '\n')
        
        # Lowercase conversion
        if lowercase:
            normalized = normalized.lower()
        
        # Remove extra whitespace
        if remove_extra_whitespace:
            # Replace multiple spaces with single space
            normalized = re.sub(r' +', ' ', normalized)
            # Replace multiple newlines with single newline (max 2 consecutive)
            normalized = re.sub(r'\n{3,}', '\n\n', normalized)
            # Trim leading/trailing whitespace
            normalized = normalized.strip()
        
        return normalized
    
    def structure_content(self, content: str, structure_type: str = 'default') -> Dict[str, Any]:
        """
        Structure content into organized format.
        
        Analyzes and structures user-submitted content:
        - Extracts paragraphs
        - Identifies headings
        - Extracts lists
        - Counts words/characters
        - Identifies structure patterns
        
        SAFETY: Only transforms user-submitted content. Never generates new content.
        
        Args:
            content: Content to structure
            structure_type: Structure type ('default', 'paragraphs', 'sections', 'minimal')
        
        Returns:
            Dictionary with structured content:
                - paragraphs: list[str]
                - headings: list[dict] (with level and text)
                - lists: list[dict] (with type and items)
                - word_count: int
                - character_count: int
                - structure_type: str
        """
        if not isinstance(content, str):
            raise ValueError("content must be a string")
        
        structured = {
            "paragraphs": [],
            "headings": [],
            "lists": [],
            "word_count": 0,
            "character_count": len(content),
            "structure_type": structure_type
        }
        
        # Split into lines for analysis
        lines = content.split('\n')
        
        # Extract paragraphs (non-empty lines that aren't headings or list items)
        current_paragraph = []
        in_list = False
        
        for line in lines:
            line_stripped = line.strip()
            
            if not line_stripped:
                # Empty line - end current paragraph
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        structured["paragraphs"].append(paragraph_text)
                    current_paragraph = []
                in_list = False
                continue
            
            # Check for heading (starts with #)
            if line_stripped.startswith('#'):
                # End current paragraph
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        structured["paragraphs"].append(paragraph_text)
                    current_paragraph = []
                
                # Extract heading level and text
                heading_match = re.match(r'^(#{1,6})\s+(.+)$', line_stripped)
                if heading_match:
                    level = len(heading_match.group(1))
                    text = heading_match.group(2).strip()
                    structured["headings"].append({
                        "level": level,
                        "text": text
                    })
                in_list = False
                continue
            
            # Check for list item (starts with -, *, +, or number)
            list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.+)$', line_stripped)
            if list_match:
                # End current paragraph
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        structured["paragraphs"].append(paragraph_text)
                    current_paragraph = []
                
                # Extract list item
                list_type = 'unordered' if list_match.group(2) in ['-', '*', '+'] else 'ordered'
                item_text = list_match.group(3).strip()
                
                # Add to appropriate list
                if not structured["lists"] or structured["lists"][-1]["type"] != list_type:
                    structured["lists"].append({
                        "type": list_type,
                        "items": []
                    })
                
                structured["lists"][-1]["items"].append(item_text)
                in_list = True
                continue
            
            # Regular text line
            if in_list:
                # End list context
                in_list = False
            
            current_paragraph.append(line_stripped)
        
        # Add final paragraph
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph).strip()
            if paragraph_text:
                structured["paragraphs"].append(paragraph_text)
        
        # Calculate word count
        words = re.findall(r'\b\w+\b', content)
        structured["word_count"] = len(words)
        
        # Apply structure type filter
        if structure_type == 'paragraphs':
            # Return only paragraphs
            return {
                "paragraphs": structured["paragraphs"],
                "word_count": structured["word_count"],
                "character_count": structured["character_count"]
            }
        elif structure_type == 'sections':
            # Return headings and paragraphs grouped
            sections = []
            current_section = None
            
            for item in structured["headings"] + [{"type": "paragraph", "text": p} for p in structured["paragraphs"]]:
                if "level" in item:
                    # New heading - start new section
                    if current_section:
                        sections.append(current_section)
                    current_section = {
                        "heading": item,
                        "paragraphs": []
                    }
                elif current_section:
                    current_section["paragraphs"].append(item["text"])
                else:
                    # Paragraph before first heading
                    if not sections or sections[-1].get("heading") is None:
                        sections.append({
                            "heading": None,
                            "paragraphs": [item["text"]]
                        })
                    else:
                        sections[-1]["paragraphs"].append(item["text"])
            
            if current_section:
                sections.append(current_section)
            
            return {
                "sections": sections,
                "word_count": structured["word_count"],
                "character_count": structured["character_count"]
            }
        elif structure_type == 'minimal':
            # Return minimal structure
            return {
                "word_count": structured["word_count"],
                "character_count": structured["character_count"],
                "has_headings": len(structured["headings"]) > 0,
                "has_lists": len(structured["lists"]) > 0,
                "paragraph_count": len(structured["paragraphs"])
            }
        
        # Default: return full structure
        return structured
    
    def validate_format(self, content: str, format_type: str = 'text') -> Dict[str, Any]:
        """
        Validate content format.
        
        Validates user-submitted content against format requirements:
        - Text format validation
        - Markdown format validation
        - HTML format validation (basic)
        - JSON format validation
        
        SAFETY: Only validates user-submitted content. Never generates new content.
        
        Args:
            content: Content to validate
            format_type: Format type ('text', 'markdown', 'html', 'json')
        
        Returns:
            Dictionary with validation result:
                - valid: bool
                - errors: list[str]
                - warnings: list[str]
        """
        if not isinstance(content, str):
            return {
                "valid": False,
                "errors": ["content must be a string"],
                "warnings": []
            }
        
        errors = []
        warnings = []
        
        if format_type == 'text':
            # Basic text validation
            if len(content.strip()) == 0:
                errors.append("Content is empty")
            
            # Check for null bytes
            if '\x00' in content:
                errors.append("Content contains null bytes")
            
            # Check for extremely long lines (potential issues)
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if len(line) > 10000:
                    warnings.append(f"Line {i} is extremely long ({len(line)} characters)")
        
        elif format_type == 'markdown':
            # Basic markdown validation
            if len(content.strip()) == 0:
                errors.append("Content is empty")
            
            # Check for balanced code blocks
            code_block_count = content.count('```')
            if code_block_count % 2 != 0:
                errors.append("Unbalanced code blocks (```)")
            
            # Check for balanced inline code
            inline_code_count = content.count('`')
            if inline_code_count % 2 != 0:
                warnings.append("Unbalanced inline code markers (`)")
            
            # Check for balanced brackets in links/images
            link_pattern = r'\[([^\]]*)\]\(([^\)]*)\)'
            image_pattern = r'!\[([^\]]*)\]\(([^\)]*)\)'
            
            # Count opening/closing brackets
            open_brackets = content.count('[')
            close_brackets = content.count(']')
            open_parens = content.count('(')
            close_parens = content.count(')')
            
            # Check for potential unclosed links/images
            if open_brackets != close_brackets:
                warnings.append("Unbalanced square brackets (potential unclosed links/images)")
            if open_parens != close_parens:
                warnings.append("Unbalanced parentheses (potential unclosed links/images)")
        
        elif format_type == 'html':
            # Basic HTML validation
            if len(content.strip()) == 0:
                errors.append("Content is empty")
            
            # Check for balanced tags (basic)
            open_tags = len(re.findall(r'<[^/][^>]*>', content))
            close_tags = len(re.findall(r'</[^>]+>', content))
            
            # Self-closing tags don't count
            self_closing_tags = len(re.findall(r'<[^>]+/>', content))
            open_tags -= self_closing_tags
            
            if open_tags != close_tags:
                warnings.append(f"Potentially unbalanced HTML tags (open: {open_tags}, close: {close_tags})")
            
            # Check for null bytes
            if '\x00' in content:
                errors.append("Content contains null bytes")
        
        elif format_type == 'json':
            # JSON validation
            if len(content.strip()) == 0:
                errors.append("Content is empty")
            
            try:
                import json
                json.loads(content)
            except json.JSONDecodeError as e:
                errors.append(f"Invalid JSON: {str(e)}")
        
        else:
            errors.append(f"Unknown format_type: {format_type}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_transformation_count(self) -> int:
        """
        Get count of transformations performed.
        
        Returns:
            Number of transformations
        """
        return len(self._transformations)
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print(" Content Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._transformations.clear()
        
        print(" Content Module: Shutdown complete")

