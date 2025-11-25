"""
CTV Module - Core Interface

Provides safe, human-triggered request packaging for CTV, Programmatic TV, Mountain, Roku, Hulu DSP.

Pattern: MODULE × CTV × HUMAN-TRIGGERED × ONE
Philosophy: 80/20 → 97.8% Certainty
Safety: No DSP communication. No automated bidding. Human-trigger only.
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


class CtvModule(ModuleInterface):
    """
    CTV Module.
    
    Provides safe, human-triggered request packaging for CTV platforms.
    
    Safety Guarantees:
    - No DSP communication
    - No automated bidding
    - Human-trigger only
    - All requests require human validation
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Initialize CTV Module.
        
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
        return "MODULE_CTV"
    
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
            print(" CTV Module: Loading...")
            
            # Subscribe to MODULE_EVENT for CTV events
            if self._event_bus:
                self._event_bus.subscribe(EventType.MODULE_EVENT, self._handle_module_event)
            
            self._loaded = True
            print(" CTV Module: Loaded successfully")
            return True
        except Exception as e:
            print(f" CTV Module: Load failed - {e}")
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
        
        # Handle CTV events
        event_name = event_data.get('name', '')
        
        if event_name == "ctv_request":
            return self._handle_ctv_request(event_data)
        elif event_name == "ctv_validate":
            return self._handle_ctv_validate(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT subscription.
        
        Routes CTV events to the module.
        
        Args:
            event: Event to handle
        """
        if not self._loaded:
            return
        
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        event_name = event_data.get('name', '')
        
        # Route ctv_request events to this module
        if event_name == "ctv_request" and (not event.target or event.target == self.module_id):
            self._handle_ctv_request(event_data)
    
    def _handle_ctv_request(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle ctv_request event.
        
        Queues the request for human validation.
        
        SAFETY: No DSP communication. No automated bidding. Human-trigger only.
        
        Args:
            event_data: Event data containing CTV request payload
            
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
            
            return {
                "success": True,
                "request_id": request_id,
                "status": "queued",
                "message": "CTV request queued for human validation"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _handle_ctv_validate(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle ctv_validate event (human-triggered).
        
        Validates a queued CTV request.
        
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
                
                # Note: No automatic DSP communication - human must trigger separately
                # This module only packages requests for human review
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
        Validate CTV request payload schema.
        
        Required fields:
        - brand: str
        - objective: str
        - budget: float
        - geo: list[str]
        - constraints: dict (with brand_safety: bool)
        
        Args:
            payload: Payload to validate
            
        Returns:
            Validation result dictionary
        """
        # Validate brand: str (required)
        brand = payload.get('brand')
        if brand is None:
            return {
                "valid": False,
                "error": "Missing required field: brand"
            }
        if not isinstance(brand, str):
            return {
                "valid": False,
                "error": "brand must be a string"
            }
        if len(brand.strip()) == 0:
            return {
                "valid": False,
                "error": "brand cannot be empty"
            }
        
        # Validate objective: str (required)
        objective = payload.get('objective')
        if objective is None:
            return {
                "valid": False,
                "error": "Missing required field: objective"
            }
        if not isinstance(objective, str):
            return {
                "valid": False,
                "error": "objective must be a string"
            }
        if len(objective.strip()) == 0:
            return {
                "valid": False,
                "error": "objective cannot be empty"
            }
        
        # Validate budget: float (required)
        budget = payload.get('budget')
        if budget is None:
            return {
                "valid": False,
                "error": "Missing required field: budget"
            }
        if not isinstance(budget, (int, float)):
            return {
                "valid": False,
                "error": "budget must be a number"
            }
        if budget <= 0:
            return {
                "valid": False,
                "error": "budget must be positive"
            }
        
        # Validate geo: list[str] (required)
        geo = payload.get('geo')
        if geo is None:
            return {
                "valid": False,
                "error": "Missing required field: geo"
            }
        if not isinstance(geo, list):
            return {
                "valid": False,
                "error": "geo must be a list"
            }
        if len(geo) == 0:
            return {
                "valid": False,
                "error": "geo cannot be empty"
            }
        for geo_item in geo:
            if not isinstance(geo_item, str):
                return {
                    "valid": False,
                    "error": "geo items must be strings"
                }
            if len(geo_item.strip()) == 0:
                return {
                    "valid": False,
                    "error": "geo items cannot be empty"
                }
        
        # Validate constraints: dict (required)
        constraints = payload.get('constraints')
        if constraints is None:
            return {
                "valid": False,
                "error": "Missing required field: constraints"
            }
        if not isinstance(constraints, dict):
            return {
                "valid": False,
                "error": "constraints must be a dictionary"
            }
        
        # Validate brand_safety: bool (required in constraints)
        brand_safety = constraints.get('brand_safety')
        if brand_safety is None:
            return {
                "valid": False,
                "error": "Missing required field: constraints.brand_safety"
            }
        if not isinstance(brand_safety, bool):
            return {
                "valid": False,
                "error": "constraints.brand_safety must be a boolean"
            }
        
        return {"valid": True}
    
    def request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API: Request a CTV campaign.
        
        Creates a queued event for human validation.
        
        SAFETY: No DSP communication. No automated bidding. Human-trigger only.
        
        Args:
            payload: CTV request payload containing:
                - brand: str
                - objective: str
                - budget: float
                - geo: list[str]
                - constraints: dict (with brand_safety: bool)
        
        Returns:
            Result dictionary with request_id and status
        """
        if not self._loaded:
            return {
                "success": False,
                "error": "Module not loaded"
            }
        
        # Create ctv_request event data
        event_data = {
            "name": "ctv_request",
            "payload": payload
        }
        
        # Handle the request
        return self._handle_ctv_request(event_data)
    
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
                    "brand": req['payload'].get('brand'),
                    "objective": req['payload'].get('objective'),
                    "budget": req['payload'].get('budget'),
                    "status": req['status'],
                    "created_at": req['created_at']
                }
                for req in self._request_queue
            ]
        }
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print(" CTV Module: Shutting down...")
        
        # Unsubscribe from events
        if self._event_bus:
            try:
                self._event_bus.unsubscribe(EventType.MODULE_EVENT, self._handle_module_event)
            except Exception:
                pass  # Non-critical
        
        self._loaded = False
        self._request_queue.clear()
        self._validated_requests.clear()
        
        print(" CTV Module: Shutdown complete")

