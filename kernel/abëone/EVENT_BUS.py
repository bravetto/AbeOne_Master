"""
Event Bus - Decentralized Event Routing

Publish/subscribe mechanism for routing events to Guardians and Modules.

Pattern: EVENT × BUS × ROUTING × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
import threading


class EventType(Enum):
    """Event types."""
    SYSTEM_EVENT = "system_event"
    MODULE_EVENT = "module_event"
    GUARDIAN_EVENT = "guardian_event"
    OBSERVER_EVENT = "observer_event"


@dataclass
class Event:
    """Event structure."""
    event_type: EventType
    event_id: str
    timestamp: datetime
    source: str
    target: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    context: Optional[Dict[str, Any]] = None


class EventBus:
    """
    Event Bus.
    
    Responsibilities:
    - Publish/subscribe mechanism
    - Route events to Guardians and Modules
    - Provide 4 event types (SYSTEM, MODULE, GUARDIAN, OBSERVER)
    """
    
    def __init__(self, version: str = "1.0.0"):
        """Initialize event bus."""
        self.version = version
        self.subscribers: Dict[EventType, List[Callable[[Event], None]]] = {
            EventType.SYSTEM_EVENT: [],
            EventType.MODULE_EVENT: [],
            EventType.GUARDIAN_EVENT: [],
            EventType.OBSERVER_EVENT: []
        }
        self.event_history: List[Event] = []
        self.max_history: int = 1000
        self.events_processed = 0
        
        # Registry hooks
        self.guardian_registry: Optional[Callable] = None
        self.module_registry: Optional[Callable] = None
        
        # Thread safety
        self._lock = threading.Lock()
    
    def register_guardian_registry(self, registry: Callable) -> None:
        """Register Guardian registry hook."""
        with self._lock:
            self.guardian_registry = registry
    
    def register_module_registry(self, registry: Callable) -> None:
        """Register Module registry hook."""
        with self._lock:
            self.module_registry = registry
    
    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Event type to subscribe to
            handler: Handler function
        """
        with self._lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: EventType, handler: Callable[[Event], None]) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Event type to unsubscribe from
            handler: Handler function to remove
        """
        with self._lock:
            if event_type in self.subscribers:
                if handler in self.subscribers[event_type]:
                    self.subscribers[event_type].remove(handler)
    
    def publish(self, event: Event) -> bool:
        """
        Publish an event.
        
        Args:
            event: Event to publish
        
        Returns:
            True if published successfully
        """
        with self._lock:
            # Add to history
            self.event_history.append(event)
            if len(self.event_history) > self.max_history:
                self.event_history.pop(0)
            
            self.events_processed += 1
        
        # Route to subscribers
        handlers = self.subscribers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                # Log error but continue processing
                print(f"Error in event handler: {e}")
        
        # Handle MODULE_EVENT with special routing
        if event.event_type == EventType.MODULE_EVENT:
            self._handle_module_event(event)
        # Handle GUARDIAN_EVENT with special routing
        elif event.event_type == EventType.GUARDIAN_EVENT:
            self._handle_guardian_event(event)
        # Route to target if specified
        elif event.target:
            self._route_to_target(event)
        
        return True
    
    def _route_to_target(self, event: Event) -> None:
        """
        Route event to specific target (Guardian or Module).
        
        Args:
            event: Event to route
        """
        target = event.target
        
        if not target:
            return
        
        # Try routing to module first
        if self.module_registry:
            module = self.module_registry.get(target)
            if module:
                self.module_registry.send_event(target, event)
                return
        
        # Try routing to guardian
        if self.guardian_registry:
            guardian = self.guardian_registry.get(target)
            if guardian:
                guardian.handle_event(event)
                return
    
    def _handle_module_event(self, event: Event) -> None:
        """
        Handle MODULE_EVENT - route to appropriate module based on event name.
        
        Args:
            event: Event to handle
        """
        event_data = event.data
        event_name = event_data.get('name', '')
        
        # Route "generate_beats" events to abebeats module
        if event_name == "generate_beats" or event_name == "generate_beat":
            if self.module_registry:
                abebeats_module = self.module_registry.get("abebeats")
                if abebeats_module:
                    self.module_registry.send_event("abebeats", event)
                    return
        
        # Route "track" events to analytics module
        if event_name == "track":
            if self.module_registry:
                analytics_module = self.module_registry.get("MODULE_ANALYTICS")
                if analytics_module:
                    self.module_registry.send_event("MODULE_ANALYTICS", event)
                    return
        
        # Route SEO events to SEO module
        seo_events = ["seo.audit_request", "seo.page_analysis", "seo.keyword_request"]
        if event_name in seo_events:
            if self.module_registry:
                seo_module = self.module_registry.get("MODULE_SEO")
                if seo_module:
                    self.module_registry.send_event("MODULE_SEO", event)
                    return
        
        # Route CTV events to CTV module
        if event_name == "ctv_request":
            if self.module_registry:
                ctv_module = self.module_registry.get("MODULE_CTV")
                if ctv_module:
                    self.module_registry.send_event("MODULE_CTV", event)
                    return
        
        # Route DOOH events to DOOH module
        if event_name == "dooh_request":
            if self.module_registry:
                dooh_module = self.module_registry.get("MODULE_DOOH")
                if dooh_module:
                    self.module_registry.send_event("MODULE_DOOH", event)
                    return
        
        # Route Social events to Social module
        if event_name == "social.schedule":
            if self.module_registry:
                social_module = self.module_registry.get("MODULE_SOCIAL")
                if social_module:
                    self.module_registry.send_event("MODULE_SOCIAL", event)
                    return
        
        # Route Data Lake events to Data Lake module
        if event_name == "data.ingest":
            if self.module_registry:
                datalake_module = self.module_registry.get("MODULE_DATA_LAKE")
                if datalake_module:
                    self.module_registry.send_event("MODULE_DATA_LAKE", event)
                    return
        
        # Default: route to target if specified
        if event.target:
            self._route_to_target(event)
    
    def _handle_guardian_event(self, event: Event) -> None:
        """
        Handle GUARDIAN_EVENT - route to appropriate guardian.
        
        Args:
            event: Event to handle
        """
        if not self.guardian_registry:
            return
        
        # Get guardian by target ID
        guardian_id = event.target or "guardian_one"  # Default to guardian_one
        
        guardian = self.guardian_registry.get(guardian_id)
        if guardian:
            # Special handling for Guardian Five (Execution Orchestrator)
            if guardian_id == "guardian_five":
                # GuardianFive.handle_event() returns a new SYSTEM_EVENT
                execution_event = guardian.handle_event(event)
                
                # Publish the execution event internally
                self.publish(execution_event)
                
                # Also publish EXECUTION_TICK if it exists
                if hasattr(execution_event, 'tick_event'):
                    self.publish(execution_event.tick_event)
                
                # Attach response to original event
                if hasattr(event, 'data'):
                    event_data = dict(event.data) if isinstance(event.data, dict) else {}
                    event_data['guardian_response'] = {
                        "executed_by": "guardian_five",
                        "status": "queued",
                        "execution_event_id": execution_event.event_id
                    }
                    event.data = event_data
            # Special handling for Guardian Two (Synthesis Orchestrator)
            elif guardian_id == "guardian_two":
                # GuardianTwo.handle_event() returns enriched event with synthesis
                enriched_event = guardian.handle_event(event)
                
                # Update original event with synthesis data
                if isinstance(enriched_event, Event):
                    if hasattr(event, 'data'):
                        event.data = enriched_event.data
                    # Forward enriched event if it's a new event
                    if enriched_event.event_id != event.event_id:
                        self.publish(enriched_event)
            # Special handling for Guardian Two (Synthesis Orchestrator)
            elif guardian_id == "guardian_two":
                # GuardianTwo.handle_event() returns enriched event with synthesis
                enriched_event = guardian.handle_event(event)
                
                # Update original event with synthesis data
                if isinstance(enriched_event, Event):
                    if hasattr(event, 'data'):
                        event.data = enriched_event.data
                    # Forward enriched event if it's a new event
                    if enriched_event.event_id != event.event_id:
                        self.publish(enriched_event)
            # Special handling for Guardian Three (Alignment Validator)
            elif guardian_id == "guardian_three":
                # GuardianThree.handle_event() returns event (transformed or original)
                result_event = guardian.handle_event(event)
                
                # If misalignment detected, publish SYSTEM_EVENT("MISALIGNMENT_DETECTED")
                if isinstance(result_event, Event) and result_event.event_type == EventType.SYSTEM_EVENT:
                    misalignment_data = result_event.data
                    if misalignment_data.get("tick_type") == "MISALIGNMENT_DETECTED":
                        self.publish(result_event)
                
                # Attach alignment score to original event
                if hasattr(result_event, 'data'):
                    alignment_info = result_event.data.get("alignment", {})
                    if hasattr(event, 'data'):
                        event_data = dict(event.data) if isinstance(event.data, dict) else {}
                        event_data['alignment'] = alignment_info
                        event.data = event_data
            else:
                # Standard guardian handling
                result = guardian.handle_event(event)
                
                # Attach truth results to event.response (if event supports it)
                if hasattr(event, 'response'):
                    event.response = result
                elif hasattr(event, 'data'):
                    # Store in event data
                    if not hasattr(event.data, '__setitem__'):
                        # Convert to dict if needed
                        event_data = dict(event.data) if hasattr(event.data, '__dict__') else {}
                    else:
                        event_data = event.data
                    event_data['guardian_response'] = result
                    event.data = event_data
    
    def create_event(self, event_type: EventType, source: str, target: Optional[str] = None,
                    data: Optional[Dict[str, Any]] = None, context: Optional[Dict[str, Any]] = None) -> Event:
        """
        Create a new event.
        
        Args:
            event_type: Event type
            source: Source identifier
            target: Target identifier (optional)
            data: Event data
            context: Event context
        
        Returns:
            Created event
        """
        event_id = f"{event_type.value}_{datetime.now().isoformat()}"
        return Event(
            event_type=event_type,
            event_id=event_id,
            timestamp=datetime.now(),
            source=source,
            target=target,
            data=data or {},
            context=context
        )
    
    def get_events_processed(self) -> int:
        """
        Get total number of events processed.
        
        Returns:
            Number of events processed
        """
        with self._lock:
            return self.events_processed
    
    def get_version(self) -> str:
        """Get event bus version."""
        return self.version
    
    def get_event_history(self, limit: int = 100) -> List[Event]:
        """
        Get event history.
        
        Args:
            limit: Maximum number of events to return
        
        Returns:
            List of recent events
        """
        with self._lock:
            return self.event_history[-limit:]


# Global event bus instance
_bus_instance: Optional[EventBus] = None


def get_bus() -> EventBus:
    """Get global event bus instance."""
    global _bus_instance
    if _bus_instance is None:
        _bus_instance = EventBus()
    return _bus_instance
