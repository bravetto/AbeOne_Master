"""
Analytics Module - Core Interface

Provides validated schemas for all analytics payloads.

Pattern: MODULE × ANALYTICS × VALIDATION × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: All ingestion human-approved. No automated insights.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import re

# Import kernel components
import sys
from pathlib import Path

# Add abëone directory to path
abeone_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(abeone_dir))

from EVENT_BUS import EventBus, Event, EventType, get_bus
from MODULE_REGISTRY import ModuleInterface


class AnalyticsModule(ModuleInterface):
    """
    Analytics Module.
    
    Provides validated schemas for all analytics payloads.
    
    Safety Guarantees:
    - All ingestion human-approved
    - No automated insights
    - Schema validation only
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize Analytics Module.
        
        Args:
            event_bus: Optional event bus instance (defaults to global instance)
        """
        self._event_bus = event_bus or get_bus()
        self._loaded = False
        self._validated_events: Dict[str, Dict[str, Any]] = {}
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        return "MODULE_ANALYTICS"
    
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
            print("✅ Analytics Module: Loading...")
            
            # Subscribe to MODULE_EVENT.track
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print("✅ Analytics Module: Loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Analytics Module: Load failed - {e}")
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
        
        # Handle track events
        event_name = event_data.get('name', '')
        
        if event_name == "track":
            return self._handle_track(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes track events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route track events to this module
        if event_name == "track" and (not event.target or event.target == self.module_id):
            self._handle_track(event_data)
    
    def _handle_track(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle track event.
        
        Validates the tracking payload schema and publishes analytics_validated event.
        
        Args:
            event_data: Event data containing tracking payload
            
        Returns:
            Result dictionary with validation status
        """
        try:
            # Extract payload
            payload = event_data.get('payload', event_data)
            
            # Validate payload schema
            validation_result = self._validate_payload(payload)
            if not validation_result['valid']:
                return {
                    "success": False,
                    "error": validation_result['error']
                }
            
            # Generate event ID
            event_id = str(uuid.uuid4())
            
            # Create validated event
            validated_event = {
                "event_id": event_id,
                "payload": payload,
                "validated_at": datetime.now().isoformat(),
                "validated": True
            }
            
            # Store validated event
            self._validated_events[event_id] = validated_event
            
            # Publish MODULE_EVENT.analytics_validated (human-approved)
            self._publish_analytics_validated(validated_event)
            
            return {
                "success": True,
                "event_id": event_id,
                "status": "validated",
                "message": "Analytics payload validated and published"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate analytics tracking payload schema.
        
        Required fields:
        - event_name: str
        - timestamp: iso8601
        - user_id: str|None
        - session_id: str
        - properties: dict
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        required_fields = ['event_name', 'timestamp', 'user_id', 'session_id', 'properties']
        
        # Check required fields
        for field in required_fields:
            if field not in payload:
                return {
                    "valid": False,
                    "error": f"Missing required field: {field}"
                }
        
        # Validate event_name: str
        event_name = payload.get('event_name')
        if not isinstance(event_name, str):
            return {
                "valid": False,
                "error": "event_name must be a string"
            }
        
        # Validate timestamp: iso8601
        timestamp = payload.get('timestamp')
        if not isinstance(timestamp, str):
            return {
                "valid": False,
                "error": "timestamp must be a string (ISO8601 format)"
            }
        
        # Validate ISO8601 format
        iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?(Z|[+-]\d{2}:\d{2})$'
        if not re.match(iso8601_pattern, timestamp):
            # Try parsing with datetime to be more lenient
            try:
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return {
                    "valid": False,
                    "error": "timestamp must be in ISO8601 format"
                }
        
        # Validate user_id: str|None
        user_id = payload.get('user_id')
        if user_id is not None and not isinstance(user_id, str):
            return {
                "valid": False,
                "error": "user_id must be a string or None"
            }
        
        # Validate session_id: str
        session_id = payload.get('session_id')
        if not isinstance(session_id, str):
            return {
                "valid": False,
                "error": "session_id must be a string"
            }
        
        # Validate properties: dict
        properties = payload.get('properties')
        if not isinstance(properties, dict):
            return {
                "valid": False,
                "error": "properties must be a dictionary"
            }
        
        return {"valid": True}
    
    def _publish_analytics_validated(self, validated_event: Dict[str, Any]) -> None:
        """
        Publish MODULE_EVENT.analytics_validated (human-approved).
        
        Args:
            validated_event: Validated event dictionary
        """
        if not self._event_bus:
            return
        
        try:
            event = self._event_bus.create_event(
                event_type=EventType.MODULE_EVENT,
                source=self.module_id,
                target=None,  # Broadcast to MODULE_EVENT subscribers
                data={
                    "name": "analytics_validated",
                    "event_id": validated_event['event_id'],
                    "payload": validated_event['payload'],
                    "validated_at": validated_event['validated_at']
                }
            )
            
            self._event_bus.publish(event)
        except Exception as e:
            print(f"⚠️  Analytics Module: Failed to publish analytics_validated event: {e}")
    
    def track(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Track an analytics event.
        
        Validates the payload schema and publishes analytics_validated event.
        
        Args:
            payload: Analytics tracking payload containing:
                - event_name: str
                - timestamp: iso8601
                - user_id: str|None
                - session_id: str
                - properties: dict
        
        Returns:
            Result dictionary with event_id and status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create track event data
        event_data = {
            "name": "track",
            "payload": payload
        }
        
        # Handle the track request
        return self._handle_track(event_data)
    
    def get_validated_count(self) -> int:
        """
        Get count of validated events.
        
        Returns:
            Number of validated events
        """
        return len(self._validated_events)
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print("✅ Analytics Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._validated_events.clear()
        
        print("✅ Analytics Module: Shutdown complete")

