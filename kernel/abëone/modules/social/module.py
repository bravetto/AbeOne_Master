"""
Social Module - Core Interface

Normalizes platform-agnostic social posting requests.

Pattern: MODULE × SOCIAL × NORMALIZATION × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: Module does not post anything. Produces only validated event payloads.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

# Import kernel components
import sys
from pathlib import Path

# Add abëone directory to path
abeone_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(abeone_dir))

from EVENT_BUS import EventBus, Event, EventType, get_bus
from MODULE_REGISTRY import ModuleInterface


class SocialModule(ModuleInterface):
    """
    Social Module.
    
    Normalizes platform-agnostic social posting requests.
    
    Safety Guarantees:
    - Does not post anything
    - Produces only validated event payloads
    - No platform API calls
    - No automated posting
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize Social Module.
        
        Args:
            event_bus: Optional event bus instance (defaults to global instance)
        """
        self._event_bus = event_bus or get_bus()
        self._loaded = False
        self._scheduled_posts: Dict[str, Dict[str, Any]] = {}
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        return "MODULE_SOCIAL"
    
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
            print(" Social Module: Loading...")
            
            # Subscribe to MODULE_EVENT for social events
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print(" Social Module: Loaded successfully")
            return True
        except Exception as e:
            print(f" Social Module: Load failed - {e}")
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
        
        # Handle social events
        event_name = event_data.get('name', '')
        
        if event_name == "social.schedule":
            return self._handle_schedule(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes social events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route social.schedule events to this module
        if event_name == "social.schedule" and (not event.target or event.target == self.module_id):
            self._handle_schedule(event_data)
    
    def _handle_schedule(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle social.schedule event.
        
        Normalizes and validates social posting request, then emits social_schedule event.
        
        SAFETY: Does not post anything. Produces only validated event payloads.
        
        Args:
            event_data: Event data containing social posting request payload
            
        Returns:
            Result dictionary with schedule_id and status
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
            
            # Normalize payload
            normalized_payload = self._normalize_payload(payload)
            
            # Generate schedule ID
            schedule_id = str(uuid.uuid4())
            
            # Create scheduled post record
            scheduled_post = {
                "schedule_id": schedule_id,
                "text": normalized_payload['text'],
                "media": normalized_payload['media'],
                "platforms": normalized_payload['platforms'],
                "schedule": normalized_payload['schedule'],
                "created_at": datetime.now().isoformat(),
                "status": "scheduled"
            }
            
            # Store scheduled post
            self._scheduled_posts[schedule_id] = scheduled_post
            
            # Publish MODULE_EVENT.social_schedule
            self._publish_social_schedule(scheduled_post)
            
            return {
                "success": True,
                "schedule_id": schedule_id,
                "status": "scheduled",
                "message": "Social post scheduled (validated event payload only - no posting performed)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate social posting request payload schema.
        
        Required fields:
        - text: str
        - media: list[str]
        - platforms: list[str]
        - schedule: datetime (ISO format string or datetime object)
        
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
        if len(text.strip()) == 0:
            return {
                "valid": False,
                "error": "text cannot be empty"
            }
        
        # Validate media: list[str] (required)
        media = payload.get('media')
        if media is None:
            return {
                "valid": False,
                "error": "Missing required field: media"
            }
        if not isinstance(media, list):
            return {
                "valid": False,
                "error": "media must be a list"
            }
        # Media can be empty list (text-only post)
        for media_item in media:
            if not isinstance(media_item, str):
                return {
                    "valid": False,
                    "error": "media items must be strings"
                }
            if len(media_item.strip()) == 0:
                return {
                    "valid": False,
                    "error": "media items cannot be empty strings"
                }
        
        # Validate platforms: list[str] (required)
        platforms = payload.get('platforms')
        if platforms is None:
            return {
                "valid": False,
                "error": "Missing required field: platforms"
            }
        if not isinstance(platforms, list):
            return {
                "valid": False,
                "error": "platforms must be a list"
            }
        if len(platforms) == 0:
            return {
                "valid": False,
                "error": "platforms cannot be empty"
            }
        for platform in platforms:
            if not isinstance(platform, str):
                return {
                    "valid": False,
                    "error": "platform items must be strings"
                }
            if len(platform.strip()) == 0:
                return {
                    "valid": False,
                    "error": "platform items cannot be empty"
                }
        
        # Validate schedule: datetime (required)
        schedule = payload.get('schedule')
        if schedule is None:
            return {
                "valid": False,
                "error": "Missing required field: schedule"
            }
        
        # Accept datetime object or ISO format string
        if isinstance(schedule, datetime):
            # Valid datetime object
            pass
        elif isinstance(schedule, str):
            # Try to parse ISO format string
            try:
                datetime.fromisoformat(schedule.replace('Z', '+00:00'))
            except ValueError:
                return {
                    "valid": False,
                    "error": "schedule must be a datetime object or ISO format string"
                }
        else:
            return {
                "valid": False,
                "error": "schedule must be a datetime object or ISO format string"
            }
        
        return {"valid": True}
    
    def _normalize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize social posting request payload.
        
        Normalizes:
        - text: strips whitespace
        - media: ensures list of strings
        - platforms: normalizes platform names (lowercase)
        - schedule: converts to ISO format string
        
        Args:
            payload: Payload to normalize
            
        Returns:
            Normalized payload dictionary
        """
        normalized = {}
        
        # Normalize text
        normalized['text'] = payload['text'].strip()
        
        # Normalize media (ensure list of strings)
        normalized['media'] = [str(item).strip() for item in payload['media']]
        
        # Normalize platforms (lowercase, strip)
        normalized['platforms'] = [str(platform).lower().strip() for platform in payload['platforms']]
        
        # Normalize schedule (convert to ISO format string)
        schedule = payload['schedule']
        if isinstance(schedule, datetime):
            normalized['schedule'] = schedule.isoformat()
        elif isinstance(schedule, str):
            # Parse and re-format to ensure consistency
            try:
                dt = datetime.fromisoformat(schedule.replace('Z', '+00:00'))
                normalized['schedule'] = dt.isoformat()
            except ValueError:
                # If parsing fails, use as-is (validation should have caught this)
                normalized['schedule'] = schedule
        else:
            normalized['schedule'] = schedule
        
        return normalized
    
    def _publish_social_schedule(self, scheduled_post: Dict[str, Any]) -> None:
        """
        Publish MODULE_EVENT.social_schedule.
        
        Emits validated event payload for social posting.
        
        SAFETY: Does not post anything. Produces only validated event payloads.
        
        Args:
            scheduled_post: Scheduled post dictionary
        """
        if not self._event_bus:
            return
        
        try:
            event = self._event_bus.create_event(
                event_type=EventType.MODULE_EVENT,
                source=self.module_id,
                target=None,  # Broadcast to MODULE_EVENT subscribers
                data={
                    "name": "social_schedule",
                    "schedule_id": scheduled_post['schedule_id'],
                    "payload": {
                        "text": scheduled_post['text'],
                        "media": scheduled_post['media'],
                        "platforms": scheduled_post['platforms'],
                        "schedule": scheduled_post['schedule']
                    },
                    "created_at": scheduled_post['created_at']
                }
            )
            
            self._event_bus.publish(event)
        except Exception as e:
            print(f"  Social Module: Failed to publish social_schedule event: {e}")
    
    def schedule(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Schedule a social post.
        
        Normalizes and validates social posting request, then emits social_schedule event.
        
        SAFETY: Does not post anything. Produces only validated event payloads.
        
        Args:
            payload: Social posting request payload containing:
                - text: str (required)
                - media: list[str] (required, can be empty)
                - platforms: list[str] (required)
                - schedule: datetime (required, ISO format string or datetime object)
        
        Returns:
            Result dictionary with schedule_id and status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create social.schedule event data
        event_data = {
            "name": "social.schedule",
            "payload": payload
        }
        
        # Handle the schedule request
        return self._handle_schedule(event_data)
    
    def get_scheduled_posts(self) -> Dict[str, Any]:
        """
        Get all scheduled posts.
        
        Returns:
            Dictionary with scheduled posts information
        """
        return {
            "scheduled_count": len(self._scheduled_posts),
            "scheduled_posts": [
                {
                    "schedule_id": post['schedule_id'],
                    "text": post['text'][:50] + "..." if len(post['text']) > 50 else post['text'],
                    "platforms": post['platforms'],
                    "schedule": post['schedule'],
                    "status": post['status'],
                    "created_at": post['created_at']
                }
                for post in self._scheduled_posts.values()
            ]
        }
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print(" Social Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._scheduled_posts.clear()
        
        print(" Social Module: Shutdown complete")

