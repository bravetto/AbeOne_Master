"""
AbëBEATs Module - Unified Organism Integration

Complete integration of AbëBEATs with Unified Organism.

Pattern: AbëBEATs × MODULE × UNIFIED × ORGANISM × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

# Import Unified Organism components
import sys
from pathlib import Path

# Add EMERGENT_OS to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "EMERGENT_OS"))

from integration_layer.registry.module_registry import (
    ModuleRegistry,
    ModuleCapability,
    ModuleStatus
)
from integration_layer.events.event_bus import EventBus
from integration_layer.state.system_state import SystemState

# Import AbëBEATs pipeline
# SAFETY: Handle both relative and absolute imports
try:
    from .src.pipeline import (
        AbeBeatsPipeline,
        AbeBeat,
        AbeBeatSequence,
        get_abebeats_pipeline
    )
except ImportError:
    # Fallback to absolute import
    import sys
    from pathlib import Path
    abebeats_path = Path(__file__).parent
    if str(abebeats_path) not in sys.path:
        sys.path.insert(0, str(abebeats_path))
    from src.pipeline import (
        AbeBeatsPipeline,
        AbeBeat,
        AbeBeatSequence,
        get_abebeats_pipeline
    )

logger = logging.getLogger(__name__)


class AbebeatsModule:
    """
    AbëBEATs Module - Unified Organism Integration
    
    Integrates AbëBEATs with Unified Organism:
    - Module Registry registration
    - Event Bus integration
    - System State tracking
    - Guardian synchronization
    - Lifecycle management
    
    Pattern: AbëBEATs × MODULE × UNIFIED × ORGANISM × ONE
    """
    
    def __init__(
        self,
        module_registry: Optional[ModuleRegistry] = None,
        event_bus: Optional[EventBus] = None,
        system_state: Optional[SystemState] = None
    ):
        """
        Initialize AbëBEATs Module.
        
        Args:
            module_registry: Module Registry instance
            event_bus: Event Bus instance
            system_state: System State instance
        """
        self.module_registry = module_registry
        self.event_bus = event_bus
        self.system_state = system_state
        
        # AbëBEATs Pipeline
        self.pipeline = get_abebeats_pipeline()
        
        # Module state
        self._registered = False
        self._active = False
        self._initialized = False
        
        # Module metadata
        self.module_id = "abebeats"
        self.module_name = "AbëBEATs"
        self.module_version = "1.0.0"
    
    def _publish_event(self, event_type_str: str, data: Dict[str, Any]) -> None:
        """
        Helper to publish events safely.
        
        Args:
            event_type_str: Event type string
            data: Event data
        """
        if not self.event_bus:
            return
        
        try:
            from integration_layer.events.event_bus import Event, EventType
            import uuid
            
            # Map string to EventType
            event_type_map = {
                "module_registered": EventType.MODULE_REGISTERED,
                "module_initialized": EventType.MODULE_STATUS_CHANGED,
                "module_activated": EventType.MODULE_STATUS_CHANGED,
                "module_shutdown": EventType.MODULE_STATUS_CHANGED,
            }
            
            event_type = event_type_map.get(event_type_str, EventType.MODULE_STATUS_CHANGED)
            
            event = Event(
                event_type=event_type,
                event_id=str(uuid.uuid4()),
                timestamp=datetime.utcnow(),
                source_module=self.module_id,
                data=data
            )
            
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self.event_bus.publish(event))
                else:
                    loop.run_until_complete(self.event_bus.publish(event))
            except RuntimeError:
                pass  # No event loop, skip
        except Exception:
            pass  # Non-critical: event publishing failure doesn't break operations
        
    def register(self) -> bool:
        """
        Register module with Module Registry.
        
        Returns:
            True if registration successful
        """
        if self._registered:
            return True
            
        if not self.module_registry:
            logger.warning("Module Registry not available, skipping registration")
            return False
            
        try:
            # Define capabilities
            capabilities = [
                ModuleCapability(
                    name="beat_generation",
                    description="Generate 530 Hz frequency beats",
                    endpoints=["generate_beat", "generate_beat_sequence"]
                ),
                ModuleCapability(
                    name="guardian_beats",
                    description="Process beats through all Guardians",
                    endpoints=["process_guardian_beats"]
                ),
                ModuleCapability(
                    name="sequence_generation",
                    description="Generate complete beat sequences",
                    endpoints=["generate_complete_sequence"]
                ),
                ModuleCapability(
                    name="statistics",
                    description="Get pipeline statistics",
                    endpoints=["get_pipeline_stats"]
                )
            ]
            
            # Register module
            # SAFETY: Check if dependencies exist, only include if they do
            available_deps = []
            for dep in ["triadic_execution_harness", "consciousness"]:
                if self.module_registry.is_module_registered(dep):
                    available_deps.append(dep)
            
            success = self.module_registry.register_module(
                module_id=self.module_id,
                name=self.module_name,
                version=self.module_version,
                capabilities=capabilities,
                dependencies=available_deps  # Only include registered dependencies
            )
            
            if success:
                self._registered = True
                logger.info(f"✅ {self.module_name} module registered")
                
                # Publish registration event
                self._publish_event("module_registered", {
                    "module_id": self.module_id,
                    "module_name": self.module_name,
                    "version": self.module_version
                })
                    
                return True
            else:
                logger.error(f"Failed to register {self.module_name} module")
                return False
                
        except Exception as e:
            logger.error(f"Error registering {self.module_name} module: {e}", exc_info=True)
            return False
    
    def initialize(self) -> bool:
        """
        Initialize module.
        
        Returns:
            True if initialization successful
        """
        if self._initialized:
            return True
            
        try:
            # Initialize pipeline
            # Pipeline is already initialized via singleton
            
            # Update module status
            if self.module_registry:
                self.module_registry.update_module_status(
                    self.module_id,
                    ModuleStatus.INITIALIZING
                )
            
            self._initialized = True
            
            logger.info(f"✅ {self.module_name} module initialized")
            
            # Publish initialization event
            self._publish_event("module_initialized", {
                "module_id": self.module_id,
                "status": "initialized"
            })
                
            return True
            
        except Exception as e:
            logger.error(f"Error initializing {self.module_name} module: {e}", exc_info=True)
            return False
    
    def activate(self) -> bool:
        """
        Activate module.
        
        Returns:
            True if activation successful
        """
        if not self._initialized:
            if not self.initialize():
                return False
                
        if self._active:
            return True
            
        try:
            # Update module status
            if self.module_registry:
                self.module_registry.update_module_status(
                    self.module_id,
                    ModuleStatus.ACTIVE
                )
            
            self._active = True
            
            logger.info(f"✅ {self.module_name} module activated")
            
            # Publish activation event
            self._publish_event("module_activated", {
                "module_id": self.module_id,
                "status": "activated"
            })
                
            return True
            
        except Exception as e:
            logger.error(f"Error activating {self.module_name} module: {e}", exc_info=True)
            return False
    
    def shutdown(self) -> bool:
        """
        Shutdown module.
        
        Returns:
            True if shutdown successful
        """
        if not self._active:
            return True
            
        try:
            # Update module status
            if self.module_registry:
                self.module_registry.update_module_status(
                    self.module_id,
                    ModuleStatus.SHUTTING_DOWN
                )
            
            self._active = False
            
            logger.info(f"✅ {self.module_name} module shut down")
            
            # Publish shutdown event
            self._publish_event("module_shutdown", {
                "module_id": self.module_id,
                "status": "shutdown"
            })
            
            # Update final status
            if self.module_registry:
                self.module_registry.update_module_status(
                    self.module_id,
                    ModuleStatus.SHUTDOWN
                )
                
            return True
            
        except Exception as e:
            logger.error(f"Error shutting down {self.module_name} module: {e}", exc_info=True)
            return False
    
    def generate_beat(
        self,
        pattern: Optional[str] = None,
        content: Optional[str] = None
    ) -> Optional[AbeBeat]:
        """
        Generate an AbëBEAT.
        
        Args:
            pattern: Optional pattern
            content: Optional content
            
        Returns:
            AbëBEAT or None if error
        """
        if not self._active:
            logger.warning("Module not active, cannot generate beat")
            return None
            
        try:
            beat = self.pipeline.generate_beat(pattern=pattern, content=content)
            
            # Publish beat generation event
            self._publish_event("beat_generated", {
                "beat_id": beat.beat_id,
                "pattern": pattern,
                "frequency": beat.frequency,
                "resonance": beat.resonance_strength
            })
            
            return beat
            
        except Exception as e:
            logger.error(f"Error generating beat: {e}", exc_info=True)
            return None
    
    def generate_beat_sequence(
        self,
        patterns: List[str],
        content_list: Optional[List[str]] = None
    ) -> Optional[AbeBeatSequence]:
        """
        Generate a sequence of AbëBEATs.
        
        Args:
            patterns: List of patterns
            content_list: Optional list of content
            
        Returns:
            AbëBeatSequence or None if error
        """
        if not self._active:
            logger.warning("Module not active, cannot generate sequence")
            return None
            
        try:
            sequence = self.pipeline.generate_beat_sequence(
                patterns=patterns,
                content_list=content_list
            )
            
            # Publish sequence generation event
            self._publish_event("sequence_generated", {
                "sequence_id": sequence.sequence_id,
                "total_beats": sequence.total_beats,
                "average_resonance": sequence.average_resonance
            })
            
            return sequence
            
        except Exception as e:
            logger.error(f"Error generating sequence: {e}", exc_info=True)
            return None
    
    def process_guardian_beats(self) -> Optional[Dict[str, Any]]:
        """
        Process beats through all Guardians.
        
        Returns:
            Guardian beat processing results or None if error
        """
        if not self._active:
            logger.warning("Module not active, cannot process Guardian beats")
            return None
            
        try:
            results = self.pipeline.process_guardian_beats()
            
            # Publish Guardian beats event
            self._publish_event("guardian_beats_processed", {
                "total_beats": results.get("total_beats", 0),
                "guardian_beats": results.get("guardian_beats", {})
            })
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing Guardian beats: {e}", exc_info=True)
            return None
    
    def generate_complete_sequence(self) -> Optional[AbeBeatSequence]:
        """
        Generate complete AbëBEATs sequence.
        
        Returns:
            Complete AbëBeatSequence or None if error
        """
        if not self._active:
            logger.warning("Module not active, cannot generate complete sequence")
            return None
            
        try:
            sequence = self.pipeline.generate_complete_sequence()
            
            # Publish complete sequence event
            self._publish_event("complete_sequence_generated", {
                "sequence_id": sequence.sequence_id,
                "total_beats": sequence.total_beats,
                "average_resonance": sequence.average_resonance,
                "coherence_score": sequence.coherence_score
            })
            
            return sequence
            
        except Exception as e:
            logger.error(f"Error generating complete sequence: {e}", exc_info=True)
            return None
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """
        Get pipeline statistics.
        
        Returns:
            Pipeline statistics dictionary
        """
        if not self._active:
            return {
                "error": "Module not active",
                "total_beats": 0,
                "total_sequences": 0
            }
            
        try:
            return self.pipeline.get_pipeline_stats()
        except Exception as e:
            logger.error(f"Error getting pipeline stats: {e}", exc_info=True)
            return {
                "error": str(e),
                "total_beats": 0,
                "total_sequences": 0
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get module status.
        
        Returns:
            Status dictionary
        """
        module_info = None
        if self.module_registry:
            module_info = self.module_registry.get_module(self.module_id)
        
        return {
            "module_id": self.module_id,
            "module_name": self.module_name,
            "module_version": self.module_version,
            "registered": self._registered,
            "initialized": self._initialized,
            "active": self._active,
            "registry_status": module_info.status.value if module_info else "unknown",
            "health_score": module_info.health_score if module_info else 0.0,
            "pipeline_stats": self.get_pipeline_stats()
        }


# Global module instance
_abebeats_module: Optional[AbebeatsModule] = None


def get_abebeats_module(
    module_registry: Optional[ModuleRegistry] = None,
    event_bus: Optional[EventBus] = None,
    system_state: Optional[SystemState] = None
) -> AbebeatsModule:
    """
    Get global AbëBEATs Module instance.
    
    Args:
        module_registry: Optional Module Registry
        event_bus: Optional Event Bus
        system_state: Optional System State
        
    Returns:
        AbebeatsModule instance
    """
    global _abebeats_module
    
    if _abebeats_module is None:
        _abebeats_module = AbebeatsModule(
            module_registry=module_registry,
            event_bus=event_bus,
            system_state=system_state
        )
    
    return _abebeats_module

