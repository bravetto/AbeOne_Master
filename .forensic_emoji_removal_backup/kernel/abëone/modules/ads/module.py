"""
Ads Module - Core Interface

Provides a safe, human-triggered interface for defining advertising requests across any channel.

Pattern: MODULE × ADS × HUMAN-TRIGGERED × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: No automated bidding, no autonomous optimization
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
from collections import deque

# Import kernel components
import sys
from pathlib import Path

# Add abëone directory to path
abeone_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(abeone_dir))

from EVENT_BUS import EventBus, Event, EventType, get_bus
from MODULE_REGISTRY import ModuleInterface


class AdsModule(ModuleInterface):
    """
    Ads Module.
    
    Provides safe, human-triggered interface for advertising requests.
    
    Safety Guarantees:
    - No automated bidding
    - No autonomous optimization
    - All requests require human validation
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize Ads Module.
        
        Args:
            event_bus: Optional event bus instance (defaults to global instance)
        """
        self._event_bus = event_bus or get_bus()
        self._loaded = False
        self._request_queue: deque = deque()
        self._validated_requests: Dict[str, Dict[str, Any]] = {}
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        return "MODULE_ADS"
    
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
            print("✅ Ads Module: Loading...")
            
            # Subscribe to MODULE_EVENT.ad_request
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print("✅ Ads Module: Loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Ads Module: Load failed - {e}")
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
        
        # Handle ad_request events
        event_name = event_data.get('name', '')
        
        if event_name == "ad_request":
            return self._handle_ad_request(event_data)
        elif event_name == "ad_validate":
            return self._handle_ad_validate(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes ad_request events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route ad_request events to this module
        if event_name == "ad_request" and (not event.target or event.target == self.module_id):
            self._handle_ad_request(event_data)
    
    def _handle_ad_request(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle ad_request event.
        
        Queues the request for human validation.
        
        Args:
            event_data: Event data containing ad request payload
            
        Returns:
            Result dictionary with request_id
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
            
            # Generate request ID
            request_id = str(uuid.uuid4())
            
            # Create queued request
            queued_request = {
                "request_id": request_id,
                "payload": payload,
                "status": "queued",
                "created_at": datetime.now().isoformat(),
                "validated": False
            }
            
            # Add to queue
            self._request_queue.append(queued_request)
            
            return {
                "success": True,
                "request_id": request_id,
                "status": "queued",
                "message": "Ad request queued for human validation"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _handle_ad_validate(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle ad_validate event (human-triggered).
        
        Validates a queued ad request and publishes ad_validated event.
        
        Args:
            event_data: Event data containing validation info
            
        Returns:
            Result dictionary
        """
        try:
            request_id = event_data.get('request_id')
            validated = event_data.get('validated', False)
            validation_notes = event_data.get('validation_notes', '')
            
            if not request_id:
                return {
                    "success": False,
                    "error": "request_id required"
                }
            
            # Find request in queue
            request = None
            for queued_request in self._request_queue:
                if queued_request.get('request_id') == request_id:
                    request = queued_request
                    break
            
            if not request:
                return {
                    "success": False,
                    "error": f"Request {request_id} not found in queue"
                }
            
            # Update request status
            request['validated'] = validated
            request['validation_notes'] = validation_notes
            request['validated_at'] = datetime.now().isoformat()
            
            if validated:
                request['status'] = "validated"
                # Move to validated requests
                self._request_queue.remove(request)
                self._validated_requests[request_id] = request
                
                # Publish MODULE_EVENT.ad_validated (human-triggered)
                self._publish_ad_validated(request)
            else:
                request['status'] = "rejected"
            
            return {
                "success": True,
                "request_id": request_id,
                "status": request['status']
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate ad request payload schema.
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        required_fields = ['campaign_name', 'platforms', 'budget']
        
        for field in required_fields:
            if field not in payload:
                return {
                    "valid": False,
                    "error": f"Missing required field: {field}"
                }
        
        # Validate types
        if not isinstance(payload.get('campaign_name'), str):
            return {
                "valid": False,
                "error": "campaign_name must be a string"
            }
        
        if not isinstance(payload.get('platforms'), list):
            return {
                "valid": False,
                "error": "platforms must be a list"
            }
        
        budget = payload.get('budget')
        if not isinstance(budget, (int, float)) or budget <= 0:
            return {
                "valid": False,
                "error": "budget must be a positive number"
            }
        
        # Optional fields validation
        if 'targeting' in payload and not isinstance(payload['targeting'], dict):
            return {
                "valid": False,
                "error": "targeting must be a dictionary"
            }
        
        if 'creatives' in payload and not isinstance(payload['creatives'], dict):
            return {
                "valid": False,
                "error": "creatives must be a dictionary"
            }
        
        if 'schedule' in payload and not isinstance(payload['schedule'], dict):
            return {
                "valid": False,
                "error": "schedule must be a dictionary"
            }
        
        if 'constraints' in payload and not isinstance(payload['constraints'], dict):
            return {
                "valid": False,
                "error": "constraints must be a dictionary"
            }
        
        return {"valid": True}
    
    def _publish_ad_validated(self, request: Dict[str, Any]) -> None:
        """
        Publish MODULE_EVENT.ad_validated (human-triggered).
        
        Args:
            request: Validated request dictionary
        """
        if not self._event_bus:
            return
        
        try:
            event = self._event_bus.create_event(
                event_type=EventType.MODULE_EVENT,
                source=self.module_id,
                target=None,  # Broadcast to MODULE_EVENT subscribers
                data={
                    "name": "ad_validated",
                    "request_id": request['request_id'],
                    "payload": request['payload'],
                    "validated_at": request['validated_at'],
                    "validation_notes": request.get('validation_notes', '')
                }
            )
            
            self._event_bus.publish(event)
        except Exception as e:
            print(f"⚠️  Ads Module: Failed to publish ad_validated event: {e}")
    
    def request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Request an ad campaign.
        
        Creates a queued event for human validation.
        
        Args:
            payload: Ad request payload containing:
                - campaign_name: str
                - platforms: list[str]
                - budget: float
                - targeting: dict (optional)
                - creatives: dict (optional)
                - schedule: dict (optional)
                - constraints: dict (optional)
        
        Returns:
            Result dictionary with request_id and status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create ad_request event data
        event_data = {
            "name": "ad_request",
            "payload": payload
        }
        
        # Handle the request
        return self._handle_ad_request(event_data)
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Get current queue status.
        
        Returns:
            Dictionary with queue information
        """
        return {
            "queued_count": len(self._request_queue),
            "validated_count": len(self._validated_requests),
            "queued_requests": [
                {
                    "request_id": req['request_id'],
                    "campaign_name": req['payload'].get('campaign_name'),
                    "status": req['status'],
                    "created_at": req['created_at']
                }
                for req in self._request_queue
            ]
        }
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print("✅ Ads Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._request_queue.clear()
        self._validated_requests.clear()
        
        print("✅ Ads Module: Shutdown complete")

