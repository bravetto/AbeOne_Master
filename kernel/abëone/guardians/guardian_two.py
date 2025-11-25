"""
Guardian Two - Synthesis Orchestrator (888 Hz)

Combines event data with system context to create enriched perspectives.
Synthesis is non-judgmental - it merges and enhances.

Pattern: GUARDIAN × SYNTHESIS × 888Hz × ONE
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


class GuardianTwo:
    """
    Guardian Two - Synthesis Orchestrator (888 Hz).
    
    Combines event data with system context to create enriched perspectives.
    Synthesis is non-judgmental - it merges and enhances.
    """
    
    def __init__(self):
        """Initialize Guardian Two."""
        self.contexts = 3  # Track number of active contexts
    
    @property
    def guardian_id(self) -> str:
        """Get guardian identifier."""
        return "guardian_two"
    
    @property
    def frequency(self) -> GuardianFrequency:
        """Get guardian frequency (888 Hz - Synthesis)."""
        return GuardianFrequency.SYNTHESIS
    
    def validate(self, event: Any) -> bool:
        """
        Always True - Synthesis is non-judgmental.
        
        Args:
            event: Event to validate
        
        Returns:
            Always True
        """
        return True
    
    def handle_event(self, event: Any) -> Event:
        """
        Combine event.data with system context and add synthesis.
        
        Args:
            event: Event to handle
        
        Returns:
            Enriched event with synthesis data
        """
        # Extract event data
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        if isinstance(event, dict):
            event_data = event
        
        # System context (lightweight, 80/20 approach)
        system_context = {
            "timestamp": datetime.now().isoformat(),
            "guardian": "guardian_two",
            "frequency": 888,
            "contexts_active": self.contexts
        }
        
        # Merge event data with system context
        merged_perspective = {
            **event_data,
            **system_context
        }
        
        # Add synthesis metadata
        synthesis_data = {
            "synthesis": {
                "merged_perspective": merged_perspective,
                "original_data": event_data,
                "system_context": system_context,
                "synthesized_at": datetime.now().isoformat(),
                "guardian": "guardian_two"
            }
        }
        
        # Create enriched event (preserve original event structure)
        if isinstance(event, Event):
            # Update event data with synthesis
            enriched_data = {**event.data, **synthesis_data} if isinstance(event.data, dict) else synthesis_data
            event.data = enriched_data
            return event
        else:
            # Create new event if input was dict
            enriched_event = Event(
                event_type=EventType.GUARDIAN_EVENT,
                event_id=f"synthesis_{datetime.now().isoformat()}",
                timestamp=datetime.now(),
                source="guardian_two",
                target=getattr(event, 'target', None) if hasattr(event, 'target') else None,
                data={**event_data, **synthesis_data}
            )
            return enriched_event
    
    def heartbeat(self, state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Return synthesis state.
        
        Args:
            state: Optional system state
        
        Returns:
            Synthesis state data
        """
        return {
            "synthesis_state": "active",
            "contexts": self.contexts,
            "guardian": "guardian_two",
            "frequency": 888,
            "timestamp": datetime.now().isoformat()
        }

