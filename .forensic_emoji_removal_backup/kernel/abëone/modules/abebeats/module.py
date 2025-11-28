"""
AbëBEATs Module - Product Module Implementation

Integrates AbëBEATs pipeline into AbëONE organism.

Pattern: MODULE × ABEBEATS × 530Hz × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, Any, Optional
import sys
import os
from pathlib import Path

# Add module directory to path
module_dir = Path(__file__).parent
sys.path.insert(0, str(module_dir))

# Import pipeline
from pipeline import get_abebeats_pipeline, generate_abebeat, AbeBeat


class AbeBeatsModule:
    """
    AbëBEATs Module.
    
    Implements ModuleInterface for AbëONE organism.
    """
    
    def __init__(self):
        """Initialize AbëBEATs Module."""
        self._pipeline = None
        self._loaded = False
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        return "abebeats"
    
    @property
    def version(self) -> str:
        """Get module version."""
        return "1.0.0"
    
    def on_load(self) -> bool:
        """
        Called when module is loaded.
        
        Returns:
            True if load successful
        """
        try:
            print("✅ AbëBEATs Module: Loading...")
            self._pipeline = get_abebeats_pipeline()
            self._loaded = True
            print("✅ AbëBEATs Module: Loaded successfully")
            return True
        except Exception as e:
            print(f"❌ AbëBEATs Module: Load failed - {e}")
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
        
        # Handle BEAT_REQUEST events
        event_name = event_data.get('name', '')
        
        if event_name == "generate_beats":
            return self._handle_generate_beats(event_data)
        elif event_name == "generate_beat":
            return self._handle_generate_beat(event_data)
        else:
            return {"error": f"Unknown event: {event_name}"}
    
    def _handle_generate_beats(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle generate_beats event.
        
        Args:
            event_data: Event data
        
        Returns:
            Result dictionary
        """
        try:
            input_audio = event_data.get('input_audio')
            pattern = event_data.get('pattern')
            content = event_data.get('content')
            
            # Generate beat using pipeline
            beat = self.generate_beats(input_audio=input_audio, pattern=pattern, content=content)
            
            return {
                "success": True,
                "beat": {
                    "beat_id": beat.beat_id,
                    "frequency": beat.frequency,
                    "resonance_strength": beat.resonance_strength,
                    "consciousness_score": beat.consciousness_score,
                    "pattern": beat.pattern
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _handle_generate_beat(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle generate_beat event (alias for generate_beats).
        
        Args:
            event_data: Event data
        
        Returns:
            Result dictionary
        """
        return self._handle_generate_beats(event_data)
    
    def generate_beats(self, input_audio: Optional[str] = None, pattern: Optional[str] = None,
                       content: Optional[str] = None) -> AbeBeat:
        """
        Generate beats using the pipeline.
        
        Args:
            input_audio: Optional input audio path (not used yet, for future expansion)
            pattern: Optional pattern for beat
            content: Optional content for resonance calculation
        
        Returns:
            Generated AbeBeat
        """
        if not self._loaded:
            raise RuntimeError("Module not loaded")
        
        return generate_abebeat(pattern=pattern, content=content)
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        print("✅ AbëBEATs Module: Shutting down...")
        self._pipeline = None
        self._loaded = False
        print("✅ AbëBEATs Module: Shutdown complete")

