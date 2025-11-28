"""
AbëONE Event Bus Adapter - Master Workspace Integration

Bridges Master Workspace to AbëONE Event Bus.

Pattern: ADAPTER × BUS × WORKSPACE × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Optional, List, Dict, Any, Callable
from pathlib import Path
import sys
from datetime import datetime
from ._logger import get_adapter_logger

logger = get_adapter_logger("BusAdapter")


class BusAdapter:
    """
    Event Bus Adapter for AbëONE Master Workspace.
    
    Provides access to AbëONE event bus functionality.
    """
    
    def __init__(self, kernel_path: Optional[str] = None):
        """
        Initialize bus adapter.
        
        Args:
            kernel_path: Path to kernel (default: abëone)
        
        Raises:
            ValueError: If kernel_path is invalid
        """
        if kernel_path is None:
            repo_root = Path(__file__).parent.parent
            kernel_path_str = str(repo_root / "abëone")
        else:
            kernel_path_str = kernel_path
        
        self.kernel_path = Path(kernel_path_str)
        
        # Validate kernel path exists
        if not self.kernel_path.exists():
            error_msg = f"Kernel path does not exist: {self.kernel_path}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        self._bus = None
        self._initialized = False
        logger.debug(f"BusAdapter initialized with path: {self.kernel_path}")
    
    def _load_bus(self) -> bool:
        """
        Load event bus.
        
        Returns:
            True if loaded successfully
        """
        if self._initialized:
            return True
        
        try:
            kernel_dir = str(self.kernel_path)
            if kernel_dir not in sys.path:
                sys.path.insert(0, kernel_dir)
            
            from EVENT_BUS import get_bus, EventType, Event
            
            self._bus = get_bus()
            self._EventType = EventType
            self._Event = Event
            self._initialized = True
            logger.info("Event bus loaded successfully")
            return True
            
        except ImportError as e:
            logger.error(f"Failed to import EVENT_BUS: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Failed to load event bus: {e}", exc_info=True)
            return False
    
    def get_bus(self) -> Optional[Any]:
        """
        Get event bus instance.
        
        Returns:
            Event bus instance or None
        """
        if not self._load_bus():
            return None
        return self._bus
    
    def subscribe(self, event_type: str, handler: Callable[[Any], None]) -> bool:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Event type ("SYSTEM_EVENT", "MODULE_EVENT", "GUARDIAN_EVENT", "OBSERVER_EVENT")
            handler: Handler function
        
        Returns:
            True if subscription successful
        
        Raises:
            ValueError: If event_type or handler is invalid
        """
        # Input validation
        if not event_type or not isinstance(event_type, str):
            logger.error(f"Invalid event_type: '{event_type}'")
            raise ValueError("Event type must be a non-empty string")
        
        if not callable(handler):
            logger.error("Handler must be callable")
            raise ValueError("Handler must be a callable function")
        
        bus = self.get_bus()
        if bus is None:
            logger.error("Cannot subscribe: event bus not available")
            return False
        
        try:
            event_type_map = {
                "SYSTEM_EVENT": self._EventType.SYSTEM_EVENT,
                "MODULE_EVENT": self._EventType.MODULE_EVENT,
                "GUARDIAN_EVENT": self._EventType.GUARDIAN_EVENT,
                "OBSERVER_EVENT": self._EventType.OBSERVER_EVENT
            }
            
            mapped_type = event_type_map.get(event_type.upper())
            if mapped_type is None:
                logger.error(f"Unknown event type: {event_type}")
                return False
            
            bus.subscribe(mapped_type, handler)
            logger.info(f"Subscribed to event type: {event_type}")
            return True
            
        except AttributeError as e:
            logger.error(f"Event bus missing required attribute: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Failed to subscribe to {event_type}: {e}", exc_info=True)
            return False
    
    def publish(self, event_type: str, payload: Dict[str, Any]) -> bool:
        """
        Publish an event.
        
        Args:
            event_type: Event type string
            payload: Event payload
        
        Returns:
            True if publish successful
        
        Raises:
            ValueError: If event_type or payload is invalid
        """
        # Input validation
        if not event_type or not isinstance(event_type, str):
            logger.error(f"Invalid event_type: '{event_type}'")
            raise ValueError("Event type must be a non-empty string")
        
        if not isinstance(payload, dict):
            logger.error(f"Invalid payload type: {type(payload)}")
            raise ValueError("Payload must be a dictionary")
        
        bus = self.get_bus()
        if bus is None:
            logger.error("Cannot publish: event bus not available")
            return False
        
        try:
            event_type_map = {
                "SYSTEM_EVENT": self._EventType.SYSTEM_EVENT,
                "MODULE_EVENT": self._EventType.MODULE_EVENT,
                "GUARDIAN_EVENT": self._EventType.GUARDIAN_EVENT,
                "OBSERVER_EVENT": self._EventType.OBSERVER_EVENT
            }
            
            mapped_type = event_type_map.get(event_type.upper())
            if mapped_type is None:
                logger.error(f"Unknown event type: {event_type}")
                return False
            
            event = self._Event(
                event_type=mapped_type,
                payload=payload,
                timestamp=datetime.now()
            )
            
            bus.publish(event)
            logger.debug(f"Published event: {event_type}")
            return True
            
        except AttributeError as e:
            logger.error(f"Event bus missing required attribute: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Failed to publish event {event_type}: {e}", exc_info=True)
            return False


# Global adapter instance
_adapter_instance: Optional[BusAdapter] = None


def get_bus_adapter(kernel_path: Optional[str] = None) -> BusAdapter:
    """
    Get global bus adapter instance.
    
    Args:
        kernel_path: Optional kernel path override
    
    Returns:
        BusAdapter instance
    """
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = BusAdapter(kernel_path)
    return _adapter_instance

