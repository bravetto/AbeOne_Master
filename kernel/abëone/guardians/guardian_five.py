"""
Guardian Five - Execution Orchestrator (999 Hz)

Prime mover that transforms INTENT into EXECUTION.
Never blocks execution - delegates work through EventBus.

Pattern: GUARDIAN × EXECUTION × 999Hz × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, Any, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add AbëONE directory to path for imports
abeone_dir = Path(__file__).parent.parent
sys.path.insert(0, str(abeone_dir))

from GUARDIANS_REGISTRY import GuardianFrequency
from EVENT_BUS import EventType, Event


class GuardianFive:
    """
    Guardian Five - Execution Orchestrator (999 Hz).
    
    PRIME MOVER: Takes INTENT and transforms it into EXECUTION.
    Never blocks execution - delegates work through EventBus.
    """
    
    def __init__(self):
        """Initialize Guardian Five."""
        self.queue_length = 0  # Internal queue size (lightweight tracking)
    
    @property
    def guardian_id(self) -> str:
        """Get guardian identifier."""
        return "guardian_five"
    
    @property
    def frequency(self) -> GuardianFrequency:
        """Get guardian frequency (999 Hz - Atomic Execution)."""
        return GuardianFrequency.ATOMIC_EXECUTION
    
    def validate(self, event: Any) -> bool:
        """
        Optional validation - always returns True.
        
        Execution engine does not judge truth; it executes intent.
        
        Args:
            event: Event to validate
        
        Returns:
            Always True
        """
        return True
    
    def handle_event(self, event: Any) -> Event:
        """
        Handle event - transform INTENT into EXECUTION.
        
        Args:
            event: Event to handle
        
        Returns:
            New SYSTEM_EVENT for execution
        """
        # Extract event data
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        if isinstance(event, dict):
            event_data = event
        
        # Read task from event data
        task = event_data.get("task", "")
        
        # Determine event type based on task
        # If task is a module operation, use MODULE_EVENT
        # Otherwise, use SYSTEM_EVENT
        if task in ["generate_beats", "generate_beat"]:
            execution_event_type = EventType.MODULE_EVENT
            target = "abebeats"
        else:
            execution_event_type = EventType.SYSTEM_EVENT
            target = None
        
        # Create execution event
        execution_event = Event(
            event_type=execution_event_type,
            event_id=f"execution_{datetime.now().isoformat()}",
            timestamp=datetime.now(),
            source="guardian_five",
            target=target,
            data={
                "task": task,
                "original_event": event_data,
                "executed_by": "guardian_five",
                "status": "queued"
            },
            context={
                "guardian": "guardian_five",
                "frequency": 999
            }
        )
        
        # Emit EXECUTION_TICK SYSTEM_EVENT
        tick_event = Event(
            event_type=EventType.SYSTEM_EVENT,
            event_id=f"execution_tick_{datetime.now().isoformat()}",
            timestamp=datetime.now(),
            source="guardian_five",
            target=None,
            data={
                "tick_type": "EXECUTION_TICK",
                "task": task,
                "executed_by": "guardian_five"
            }
        )
        
        # Update queue length (lightweight tracking)
        self.queue_length += 1
        
        # Return the execution event (tick event will be published separately)
        # Store tick event for later publishing
        execution_event.tick_event = tick_event
        
        return execution_event
    
    def heartbeat(self, state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Return executor status.
        
        Args:
            state: Optional system state
        
        Returns:
            Executor status data
        """
        return {
            "executor_ready": True,
            "queue_length": self.queue_length,
            "guardian": "guardian_five",
            "frequency": 999,
            "timestamp": datetime.now().isoformat()
        }

