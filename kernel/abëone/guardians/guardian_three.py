"""
Guardian Three - Alignment Validator (777 Hz)

Validator of intent that ensures EVERY event has valid structure.
Acts as bridge between 777 Hz (Pattern Integrity) and 530 Hz (Heart Truth).

Pattern: GUARDIAN × ALIGNMENT × 777Hz × ONE
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


class GuardianThree:
    """
    Guardian Three - Alignment Validator (777 Hz).
    
    Validator of intent that ensures EVERY event entering the organism
    has a valid structure. Enhances neuromorphic coherence through alignment scoring.
    """
    
    def __init__(self):
        """Initialize Guardian Three."""
        self.last_score = 1.0  # Track last alignment score
    
    @property
    def guardian_id(self) -> str:
        """Get guardian identifier."""
        return "guardian_three"
    
    @property
    def frequency(self) -> GuardianFrequency:
        """Get guardian frequency (777 Hz - Pattern Integrity)."""
        return GuardianFrequency.PATTERN_INTEGRITY
    
    def validate(self, event: Any) -> Dict[str, Any]:
        """
        Ensure event.data is well-formed.
        
        Args:
            event: Event to validate
        
        Returns:
            {"aligned": bool, "score": float}
        """
        # Extract event data
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        if isinstance(event, dict):
            event_data = event
        
        # Ensure event.data is well-formed
        if not isinstance(event_data, dict):
            return {"aligned": False, "score": 0.0}
        
        # Check for required fields: "task" or "message"
        has_task = "task" in event_data and event_data.get("task")
        has_message = "message" in event_data and event_data.get("message")
        
        if not (has_task or has_message):
            return {"aligned": False, "score": 0.0}
        
        # Check for malformed or missing fields
        # Ensure values are not None or empty strings (if they exist)
        for key, value in event_data.items():
            if value is None:
                return {"aligned": False, "score": 0.0}
            if isinstance(value, str) and len(value.strip()) == 0 and key in ["task", "message"]:
                return {"aligned": False, "score": 0.0}
        
        # Event is well-formed
        return {"aligned": True, "score": 1.0}
    
    def handle_event(self, event: Any) -> Event:
        """
        Revalidate event and attach alignment score.
        
        Args:
            event: Event to handle
        
        Returns:
            Event (transformed or original)
        """
        # Revalidate event using validate()
        validation_result = self.validate(event)
        aligned = validation_result["aligned"]
        score = validation_result["score"]
        
        # Update last score
        self.last_score = score
        
        # Extract event data
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        if isinstance(event, dict):
            event_data = event
        
        # Attach alignment score to event.data["alignment"]
        if not isinstance(event_data, dict):
            event_data = {}
        
        event_data["alignment"] = {
            "aligned": aligned,
            "score": score,
            "guardian": "guardian_three",
            "frequency": 777,
            "timestamp": datetime.now().isoformat()
        }
        
        # If misaligned: transform into SYSTEM_EVENT("MISALIGNMENT_DETECTED")
        if not aligned:
            misalignment_event = Event(
                event_type=EventType.SYSTEM_EVENT,
                event_id=f"misalignment_{datetime.now().isoformat()}",
                timestamp=datetime.now(),
                source="guardian_three",
                target=None,
                data={
                    "tick_type": "MISALIGNMENT_DETECTED",
                    "original_event": event_data,
                    "alignment_score": score,
                    "guardian": "guardian_three"
                }
            )
            
            # Store original event and misalignment event
            misalignment_event.original_event = event
            return misalignment_event
        
        # If aligned: forward event unchanged (but with alignment metadata)
        # Update event data with alignment info
        if hasattr(event, 'data'):
            event.data = event_data
        elif isinstance(event, dict):
            event = event_data
        
        return event
    
    def heartbeat(self, state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Return alignment state.
        
        Args:
            state: Optional system state
        
        Returns:
            Alignment state data
        """
        return {
            "alignment_state": "stable" if self.last_score >= 0.5 else "unstable",
            "last_score": self.last_score,
            "guardian": "guardian_three",
            "frequency": 777,
            "timestamp": datetime.now().isoformat()
        }

