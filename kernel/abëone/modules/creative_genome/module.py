"""
Creative Genome Module - Core Interface

Defines the schema for creative assets, metadata, performance markers.

Pattern: MODULE × CREATIVE_GENOME × SCHEMA × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: No automated creative scoring. No mutation. Schema only.
"""

from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass, field
from datetime import datetime

# Import kernel components
import sys
from pathlib import Path

# Add abëone directory to path
abeone_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(abeone_dir))

from EVENT_BUS import EventBus, Event, EventType, get_bus
from MODULE_REGISTRY import ModuleInterface


@dataclass
class CreativeAssetSchema:
    """
    Creative Asset Schema.
    
    Defines the structure for creative assets, metadata, and performance markers.
    
    Safety Guarantees:
    - No automated creative scoring
    - No mutation
    - Schema validation only
    """
    asset_id: str
    format: str
    dimensions: Tuple[int, int]
    duration: float
    tags: List[str] = field(default_factory=list)
    performance_markers: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert schema to dictionary."""
        return {
            "asset_id": self.asset_id,
            "format": self.format,
            "dimensions": list(self.dimensions),  # Convert tuple to list for JSON serialization
            "duration": self.duration,
            "tags": self.tags,
            "performance_markers": self.performance_markers
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreativeAssetSchema':
        """Create schema from dictionary."""
        # Convert dimensions list back to tuple
        dimensions = data.get('dimensions', (0, 0))
        if isinstance(dimensions, list):
            dimensions = tuple(dimensions)
        
        return cls(
            asset_id=data['asset_id'],
            format=data['format'],
            dimensions=dimensions,
            duration=data['duration'],
            tags=data.get('tags', []),
            performance_markers=data.get('performance_markers', {})
        )


class CreativeGenomeModule(ModuleInterface):
    """
    Creative Genome Module.
    
    Defines the schema for creative assets, metadata, performance markers.
    
    Safety Guarantees:
    - No automated creative scoring
    - No mutation
    - Schema validation only
    - No automatic performance analysis
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize Creative Genome Module.
        
        Args:
            event_bus: Optional event bus instance (defaults to global instance)
        """
        self._event_bus = event_bus or get_bus()
        self._loaded = False
        self._assets: Dict[str, CreativeAssetSchema] = {}
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        return "MODULE_CREATIVE_GENOME"
    
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
            print(" Creative Genome Module: Loading...")
            
            # Subscribe to MODULE_EVENT for creative asset events
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print(" Creative Genome Module: Loaded successfully")
            return True
        except Exception as e:
            print(f" Creative Genome Module: Load failed - {e}")
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
        
        # Handle creative asset events
        event_name = event_data.get('name', '')
        
        if event_name == "creative.register":
            return self._handle_register(event_data)
        elif event_name == "creative.validate":
            return self._handle_validate(event_data)
        elif event_name == "creative.get":
            return self._handle_get(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes creative asset events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route creative.* events to this module
        if event_name.startswith("creative.") and (not event.target or event.target == self.module_id):
            if event_name == "creative.register":
                self._handle_register(event_data)
            elif event_name == "creative.validate":
                self._handle_validate(event_data)
            elif event_name == "creative.get":
                self._handle_get(event_data)
    
    def _handle_register(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle creative.register event.
        
        Registers a creative asset with schema validation.
        
        SAFETY: No automated creative scoring. No mutation. Schema only.
        
        Args:
            event_data: Event data containing asset schema
            
        Returns:
            Result dictionary with registration status
        """
        try:
            # Extract asset data
            asset_data = event_data.get('asset', event_data)
            
            # Validate schema
            validation_result = self._validate_schema(asset_data)
            if not validation_result['valid']:
                return {
                    "success": False,
                    "error": validation_result['error']
                }
            
            # Create schema instance
            asset_schema = CreativeAssetSchema.from_dict(asset_data)
            
            # Store asset (schema only, no mutation)
            self._assets[asset_schema.asset_id] = asset_schema
            
            # Publish MODULE_EVENT.creative_registered
            self._publish_creative_registered(asset_schema)
            
            return {
                "success": True,
                "asset_id": asset_schema.asset_id,
                "status": "registered",
                "message": "Creative asset registered (schema only, no scoring, no mutation)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _handle_validate(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle creative.validate event.
        
        Validates creative asset schema without registration.
        
        SAFETY: No automated creative scoring. No mutation. Schema validation only.
        
        Args:
            event_data: Event data containing asset schema to validate
            
        Returns:
            Validation result dictionary
        """
        try:
            # Extract asset data
            asset_data = event_data.get('asset', event_data)
            
            # Validate schema
            validation_result = self._validate_schema(asset_data)
            
            return {
                "success": validation_result['valid'],
                "valid": validation_result['valid'],
                "error": validation_result.get('error'),
                "message": "Schema validation complete (no scoring, no mutation)"
            }
        except Exception as e:
            return {
                "success": False,
                "valid": False,
                "error": str(e)
            }
    
    def _handle_get(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle creative.get event.
        
        Retrieves a registered creative asset by asset_id.
        
        SAFETY: Read-only operation. No mutation.
        
        Args:
            event_data: Event data containing asset_id
            
        Returns:
            Asset schema dictionary or error
        """
        try:
            asset_id = event_data.get('asset_id', '')
            
            if not asset_id:
                return {
                    "success": False,
                    "error": "Missing required field: asset_id"
                }
            
            if asset_id not in self._assets:
                return {
                    "success": False,
                    "error": f"Asset not found: {asset_id}"
                }
            
            asset_schema = self._assets[asset_id]
            
            return {
                "success": True,
                "asset": asset_schema.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_schema(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate creative asset schema.
        
        Validates that asset_data conforms to CreativeAssetSchema.
        
        SAFETY: Schema validation only. No automated creative scoring. No mutation.
        
        Args:
            asset_data: Asset data dictionary to validate
            
        Returns:
            Validation result dictionary
        """
        # Validate asset_id: str (required)
        if 'asset_id' not in asset_data:
            return {
                "valid": False,
                "error": "Missing required field: asset_id"
            }
        if not isinstance(asset_data['asset_id'], str) or not asset_data['asset_id']:
            return {
                "valid": False,
                "error": "asset_id must be a non-empty string"
            }
        
        # Validate format: str (required)
        if 'format' not in asset_data:
            return {
                "valid": False,
                "error": "Missing required field: format"
            }
        if not isinstance(asset_data['format'], str) or not asset_data['format']:
            return {
                "valid": False,
                "error": "format must be a non-empty string"
            }
        
        # Validate dimensions: tuple[int, int] (required)
        if 'dimensions' not in asset_data:
            return {
                "valid": False,
                "error": "Missing required field: dimensions"
            }
        dimensions = asset_data['dimensions']
        if isinstance(dimensions, list):
            dimensions = tuple(dimensions)
        if not isinstance(dimensions, tuple) or len(dimensions) != 2:
            return {
                "valid": False,
                "error": "dimensions must be a tuple of two integers"
            }
        if not isinstance(dimensions[0], int) or not isinstance(dimensions[1], int):
            return {
                "valid": False,
                "error": "dimensions must be a tuple of two integers"
            }
        if dimensions[0] < 0 or dimensions[1] < 0:
            return {
                "valid": False,
                "error": "dimensions must be non-negative integers"
            }
        
        # Validate duration: float (required)
        if 'duration' not in asset_data:
            return {
                "valid": False,
                "error": "Missing required field: duration"
            }
        if not isinstance(asset_data['duration'], (int, float)):
            return {
                "valid": False,
                "error": "duration must be a number (int or float)"
            }
        if asset_data['duration'] < 0:
            return {
                "valid": False,
                "error": "duration must be non-negative"
            }
        
        # Validate tags: list[str] (optional, defaults to empty list)
        if 'tags' in asset_data:
            if not isinstance(asset_data['tags'], list):
                return {
                    "valid": False,
                    "error": "tags must be a list"
                }
            if not all(isinstance(tag, str) for tag in asset_data['tags']):
                return {
                    "valid": False,
                    "error": "tags must be a list of strings"
                }
        
        # Validate performance_markers: dict (optional, defaults to empty dict)
        if 'performance_markers' in asset_data:
            if not isinstance(asset_data['performance_markers'], dict):
                return {
                    "valid": False,
                    "error": "performance_markers must be a dictionary"
                }
        
        # SAFETY: No automated creative scoring
        # SAFETY: No mutation
        # Schema validation only
        
        return {"valid": True}
    
    def _publish_creative_registered(self, asset_schema: CreativeAssetSchema) -> None:
        """
        Publish MODULE_EVENT.creative_registered.
        
        Emits registered creative asset schema.
        
        SAFETY: No automated creative scoring. No mutation. Schema only.
        
        Args:
            asset_schema: Creative asset schema instance
        """
        if not self._event_bus:
            return
        
        try:
            event = self._event_bus.create_event(
                event_type=EventType.MODULE_EVENT,
                source=self.module_id,
                target=None,  # Broadcast to MODULE_EVENT subscribers
                data={
                    "name": "creative_registered",
                    "asset_id": asset_schema.asset_id,
                    "asset": asset_schema.to_dict()
                }
            )
            
            self._event_bus.publish(event)
        except Exception as e:
            print(f"  Creative Genome Module: Failed to publish creative_registered event: {e}")
    
    def register(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Register a creative asset.
        
        Validates and registers a creative asset schema.
        
        SAFETY: No automated creative scoring. No mutation. Schema only.
        
        Args:
            asset_data: Asset data dictionary with schema fields:
                - asset_id: str (required)
                - format: str (required)
                - dimensions: tuple[int, int] (required)
                - duration: float (required)
                - tags: list[str] (optional, defaults to [])
                - performance_markers: dict (optional, defaults to {})
        
        Returns:
            Result dictionary with registration status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create creative.register event data
        event_data = {
            "name": "creative.register",
            "asset": asset_data
        }
        
        # Handle the register request
        return self._handle_register(event_data)
    
    def validate(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Validate creative asset schema.
        
        Validates asset schema without registration.
        
        SAFETY: No automated creative scoring. No mutation. Schema validation only.
        
        Args:
            asset_data: Asset data dictionary to validate
        
        Returns:
            Validation result dictionary
        """
        if not self._loaded:
            return {
                "success": False,
                "valid": False,
                "error": "Module not loaded"
            }
        
        # Create creative.validate event data
        event_data = {
            "name": "creative.validate",
            "asset": asset_data
        }
        
        # Handle the validate request
        return self._handle_validate(event_data)
    
    def get(self, asset_id: str) -> Dict[str, Any]:
        """
        Public API: Get creative asset by asset_id.
        
        Retrieves registered creative asset schema.
        
        SAFETY: Read-only operation. No mutation.
        
        Args:
            asset_id: Asset identifier
        
        Returns:
            Asset schema dictionary or error
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create creative.get event data
        event_data = {
            "name": "creative.get",
            "asset_id": asset_id
        }
        
        # Handle the get request
        return self._handle_get(event_data)
    
    def get_all_assets(self) -> Dict[str, Any]:
        """
        Get all registered creative assets.
        
        Returns:
            Dictionary with all registered assets
        """
        return {
            "asset_count": len(self._assets),
            "assets": [
                asset.to_dict()
                for asset in self._assets.values()
            ]
        }
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print(" Creative Genome Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._assets.clear()
        
        print(" Creative Genome Module: Shutdown complete")

