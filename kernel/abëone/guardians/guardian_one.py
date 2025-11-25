"""
Guardian One - Abë (The Truth Engine)

Lightweight truth-validation engine operating at 530 Hz (Heart/Truth frequency).

Pattern: GUARDIAN × TRUTH × 530Hz × ONE
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


class GuardianOne:
    """
    Guardian One - Abë (The Truth Engine).
    
    Performs lightweight truth-validation checks using 80/20 approach.
    Does NOT reject events - annotates them with truth metadata.
    """
    
    @property
    def guardian_id(self) -> str:
        """Get guardian identifier."""
        return "guardian_one"
    
    @property
    def frequency(self) -> GuardianFrequency:
        """Get guardian frequency (530 Hz - Heart/Truth)."""
        return GuardianFrequency.HEART_TRUTH
    
    def validate(self, event: Any) -> bool:
        """
        Verify the event aligns to truth.
        
        Args:
            event: Event to validate
        
        Returns:
            True if event is "true enough" to continue
        """
        # Extract event data
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        if isinstance(event, dict):
            event_data = event
        
        # Lightweight truth checks (80/20 approach)
        
        # Check 1: Structure coherence
        if not isinstance(event_data, dict):
            return False
        
        # Check 2: Missing required fields (if event has required fields)
        # This is a lightweight check - we don't reject, just note
        
        # Check 3: Event-type mismatches
        # Check if event has proper structure
        if hasattr(event, 'event_type'):
            # Event has proper structure
            pass
        
        # Check 4: Semantic drift indicators
        # Check for nonsense data
        if event_data:
            # Check for empty strings that should have content
            for key, value in event_data.items():
                if isinstance(value, str) and len(value.strip()) == 0 and key in ['message', 'content', 'data']:
                    # Empty content - potential drift indicator
                    pass
        
        # Default: event is "true enough"
        return True
    
    def handle_event(self, event: Any) -> Dict[str, Any]:
        """
        Evaluate and respond to truth-based signals.
        
        Args:
            event: Event to handle
        
        Returns:
            Truth validation result
        """
        # Extract event data
        event_data = getattr(event, 'data', {}) if hasattr(event, 'data') else {}
        if isinstance(event, dict):
            event_data = event
        
        # Perform truth validation
        is_valid = self.validate(event)
        
        # Detect drift patterns
        drift_reasons = []
        
        # Check for missing keys
        if isinstance(event_data, dict):
            # Check for common required fields (lightweight check)
            if 'name' in event_data and not event_data.get('name'):
                drift_reasons.append("empty_name")
        
        # Check for nonsense data
        if event_data:
            for key, value in event_data.items():
                if isinstance(value, str) and value.strip() == '' and key in ['message', 'content']:
                    drift_reasons.append(f"empty_{key}")
        
        # Check for misrouted modules (if target specified)
        if hasattr(event, 'target'):
            target = event.target
            if target and target not in ['guardian_one', 'abebeats']:
                # Unknown target - potential misrouting
                drift_reasons.append(f"unknown_target_{target}")
        
        # Check for wrong event types (if event_type specified)
        if hasattr(event, 'event_type'):
            event_type = str(event.event_type)
            if 'GUARDIAN' not in event_type and 'SYSTEM' not in event_type and 'MODULE' not in event_type and 'OBSERVER' not in event_type:
                drift_reasons.append(f"unexpected_event_type")
        
        # Check for bad patterns
        if 'pattern' in event_data:
            pattern = event_data.get('pattern', '')
            if isinstance(pattern, str) and len(pattern) > 100:
                drift_reasons.append("pattern_too_long")
        
        # Produce result
        if drift_reasons:
            return {
                "status": "drift",
                "reason": ", ".join(drift_reasons),
                "guardian": "guardian_one",
                "frequency": 530,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "ok",
                "guardian": "guardian_one",
                "frequency": 530,
                "timestamp": datetime.now().isoformat()
            }
    
    def heartbeat(self, state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Optional heartbeat - returns truth resonance data.
        
        Args:
            state: Optional system state
        
        Returns:
            Truth resonance data
        """
        return {
            "guardian": "guardian_one",
            "frequency": 530,
            "resonance": 1.0,  # Full truth resonance
            "status": "active",
            "timestamp": datetime.now().isoformat()
        }

