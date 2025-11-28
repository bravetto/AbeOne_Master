"""
DOOH/Radio Module - Core Interface

Provides safe, human-triggered request packaging for Digital Out-of-Home, Radio, Podcast buys.

Pattern: MODULE × DOOH × HUMAN-TRIGGERED × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: No placement booking. Sends only validated request objects.
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


class DoohModule(ModuleInterface):
    """
    DOOH/Radio Module.
    
    Provides safe, human-triggered request packaging for DOOH, Radio, Podcast buys.
    
    Safety Guarantees:
    - No placement booking
    - Sends only validated request objects
    - Human-trigger only
    - All requests require human validation
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize DOOH/Radio Module.
        
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
        return "MODULE_DOOH"
    
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
            print("✅ DOOH/Radio Module: Loading...")
            
            # Subscribe to MODULE_EVENT for DOOH events
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print("✅ DOOH/Radio Module: Loaded successfully")
            return True
        except Exception as e:
            print(f"❌ DOOH/Radio Module: Load failed - {e}")
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
        
        # Handle DOOH events
        event_name = event_data.get('name', '')
        
        if event_name == "dooh_request":
            return self._handle_dooh_request(event_data)
        elif event_name == "dooh_validate":
            return self._handle_dooh_validate(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes DOOH events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route dooh_request events to this module
        if event_name == "dooh_request" and (not event.target or event.target == self.module_id):
            self._handle_dooh_request(event_data)
    
    def _handle_dooh_request(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle dooh_request event.
        
        Queues the request for human validation.
        
        SAFETY: No placement booking. Sends only validated request objects.
        
        Args:
            event_data: Event data containing DOOH request payload
            
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
            
            # Add to queue (human-reviewed queue)
            self._request_queue.append(queued_request)
            
            # Publish MODULE_EVENT.dooh_request
            if self._event_bus:
                dooh_event = self._event_bus.create_event(
                    event_type=EventType.MODULE_EVENT,
                    source=self.module_id,
                    target=None,
                    data={
                        "name": "dooh_request",
                        "request_id": request_id,
                        "payload": payload
                    }
                )
                self._event_bus.publish(dooh_event)
            
            return {
                "success": True,
                "request_id": request_id,
                "status": "queued",
                "message": "DOOH/Radio request queued for human validation"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _handle_dooh_validate(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle dooh_validate event (human-triggered).
        
        Validates a queued DOOH/Radio request.
        
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
                
                # Note: No automatic placement booking - human must trigger separately
                # This module only packages validated request objects
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
        Validate DOOH/Radio request payload schema.
        
        Required fields:
        - channel: "dooh"|"radio"|"podcast"
        - spend: float
        - placements: list[str]
        - creative_assets: dict
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        # Validate channel: "dooh"|"radio"|"podcast" (required)
        channel = payload.get('channel')
        if channel is None:
            return {
                "valid": False,
                "error": "Missing required field: channel"
            }
        if not isinstance(channel, str):
            return {
                "valid": False,
                "error": "channel must be a string"
            }
        valid_channels = ["dooh", "radio", "podcast"]
        if channel not in valid_channels:
            return {
                "valid": False,
                "error": f"channel must be one of: {', '.join(valid_channels)}"
            }
        
        # Validate spend: float (required)
        spend = payload.get('spend')
        if spend is None:
            return {
                "valid": False,
                "error": "Missing required field: spend"
            }
        if not isinstance(spend, (int, float)):
            return {
                "valid": False,
                "error": "spend must be a number"
            }
        if spend <= 0:
            return {
                "valid": False,
                "error": "spend must be positive"
            }
        
        # Validate placements: list[str] (required)
        placements = payload.get('placements')
        if placements is None:
            return {
                "valid": False,
                "error": "Missing required field: placements"
            }
        if not isinstance(placements, list):
            return {
                "valid": False,
                "error": "placements must be a list"
            }
        if len(placements) == 0:
            return {
                "valid": False,
                "error": "placements cannot be empty"
            }
        for placement in placements:
            if not isinstance(placement, str):
                return {
                    "valid": False,
                    "error": "placements items must be strings"
                }
            if len(placement.strip()) == 0:
                return {
                    "valid": False,
                    "error": "placements items cannot be empty"
                }
        
        # Validate creative_assets: dict (required)
        creative_assets = payload.get('creative_assets')
        if creative_assets is None:
            return {
                "valid": False,
                "error": "Missing required field: creative_assets"
            }
        if not isinstance(creative_assets, dict):
            return {
                "valid": False,
                "error": "creative_assets must be a dictionary"
            }
        
        return {"valid": True}
    
    def request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Request a DOOH/Radio/Podcast buy.
        
        Creates a queued event for human validation.
        
        SAFETY: No placement booking. Sends only validated request objects.
        
        Args:
            payload: DOOH/Radio request payload containing:
                - channel: "dooh"|"radio"|"podcast"
                - spend: float
                - placements: list[str]
                - creative_assets: dict
        
        Returns:
            Result dictionary with request_id and status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create dooh_request event data
        event_data = {
            "name": "dooh_request",
            "payload": payload
        }
        
        # Handle the request
        return self._handle_dooh_request(event_data)
    
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
                    "channel": req['payload'].get('channel'),
                    "spend": req['payload'].get('spend'),
                    "placements_count": len(req['payload'].get('placements', [])),
                    "status": req['status'],
                    "created_at": req['created_at']
                }
                for req in self._request_queue
            ]
        }
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print("✅ DOOH/Radio Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._request_queue.clear()
        self._validated_requests.clear()
        
        print("✅ DOOH/Radio Module: Shutdown complete")

