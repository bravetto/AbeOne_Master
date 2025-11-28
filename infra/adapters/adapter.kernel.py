"""
AbëONE Kernel Adapter - Master Workspace Integration

Bridges Master Workspace to AbëONE Superkernel kernel interface.

Pattern: ADAPTER × KERNEL × WORKSPACE × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Optional, Dict, Any
from pathlib import Path
import sys
from ._logger import get_adapter_logger

logger = get_adapter_logger("KernelAdapter")


class KernelAdapter:
    """
    Kernel Adapter for AbëONE Master Workspace.
    
    Provides access to AbëONE kernel functionality for workspace orchestration.
    """
    
    def __init__(self, kernel_path: Optional[str] = None):
        """
        Initialize kernel adapter.
        
        Args:
            kernel_path: Path to kernel (default: abëone)
        
        Raises:
            ValueError: If kernel_path is invalid
        """
        if kernel_path is None:
            # Default to abëone relative to repo root
            repo_root = Path(__file__).parent.parent
            kernel_path = repo_root / "abëone"
        
        self.kernel_path = Path(kernel_path)
        
        # Validate kernel path exists
        if not self.kernel_path.exists():
            error_msg = f"Kernel path does not exist: {self.kernel_path}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        self._kernel = None
        self._initialized = False
        logger.debug(f"KernelAdapter initialized with path: {self.kernel_path}")
    
    def _load_kernel(self) -> bool:
        """
        Bootstrap ONE_KERNEL + EVENT_BUS.
        
        Contract: adapter.kernel.py MUST bootstrap ONE_KERNEL + EVENT_BUS.
        
        Returns:
            True if loaded successfully
        """
        if self._initialized:
            return True
        
        try:
            # Add kernel path to sys.path
            kernel_dir = str(self.kernel_path)
            if kernel_dir not in sys.path:
                sys.path.insert(0, kernel_dir)
            
            # Bootstrap ONE_KERNEL
            from ONE_KERNEL import get_kernel, OneKernel
            self._kernel = get_kernel()
            
            # Bootstrap EVENT_BUS
            from EVENT_BUS import get_bus, EventBus
            self._event_bus = get_bus()
            
            # Register event bus with kernel
            self._kernel.register_event_bus(self._event_bus)
            
            # Register module registry with event bus
            from MODULE_REGISTRY import get_registry as get_module_registry
            module_registry = get_module_registry()
            self._event_bus.register_module_registry(module_registry)
            
            # Register guardian registry with event bus
            from GUARDIANS_REGISTRY import get_registry as get_guardian_registry
            guardian_registry = get_guardian_registry()
            self._event_bus.register_guardian_registry(guardian_registry)
            
            # Register registries with kernel
            self._kernel.register_module_registry(module_registry)
            self._kernel.register_guardian_registry(guardian_registry)
            
            self._initialized = True
            logger.info("Kernel and event bus bootstrapped successfully")
            return True
            
        except ImportError as e:
            logger.error(f"Failed to import kernel modules: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Failed to bootstrap kernel + event bus: {e}", exc_info=True)
            return False
    
    def get_event_bus(self) -> Optional[Any]:
        """
        Get event bus instance.
        
        Returns:
            Event bus instance or None
        """
        if not self._load_kernel():
            return None
        return getattr(self, '_event_bus', None)
    
    def get_kernel(self) -> Optional[Any]:
        """
        Get kernel instance.
        
        Returns:
            Kernel instance or None
        """
        if not self._load_kernel():
            return None
        return self._kernel
    
    def initialize(self) -> bool:
        """
        Initialize kernel.
        
        Returns:
            True if initialization successful
        """
        kernel = self.get_kernel()
        if kernel is None:
            return False
        
        try:
            result = kernel.initialize()
            if result:
                logger.info("Kernel initialized successfully")
            else:
                logger.warning("Kernel initialization returned False")
            return result
        except Exception as e:
            logger.error(f"Failed to initialize kernel: {e}", exc_info=True)
            return False
    
    def start(self) -> bool:
        """
        Start kernel.
        
        Returns:
            True if start successful
        """
        kernel = self.get_kernel()
        if kernel is None:
            return False
        
        try:
            result = kernel.start()
            if result:
                logger.info("Kernel started successfully")
            else:
                logger.warning("Kernel start returned False")
            return result
        except Exception as e:
            logger.error(f"Failed to start kernel: {e}", exc_info=True)
            return False
    
    def heartbeat(self) -> None:
        """Update kernel heartbeat."""
        kernel = self.get_kernel()
        if kernel:
            try:
                kernel.heartbeat()
            except Exception as e:
                logger.warning(f"Failed to update heartbeat: {e}")
        else:
            logger.warning("Cannot update heartbeat: kernel not available")
    
    def shutdown(self) -> None:
        """Shutdown kernel."""
        kernel = self.get_kernel()
        if kernel:
            try:
                kernel.shutdown()
                logger.info("Kernel shutdown completed")
            except Exception as e:
                logger.error(f"Error during kernel shutdown: {e}", exc_info=True)
        else:
            logger.warning("Cannot shutdown: kernel not available")
    
    def is_ready(self) -> bool:
        """
        Check if kernel is ready.
        
        Returns:
            True if kernel is ready
        """
        kernel = self.get_kernel()
        if kernel is None:
            return False
        return kernel.kernel_ready()
    
    def get_system_info(self) -> Optional[Dict[str, Any]]:
        """
        Get system information.
        
        Returns:
            System info dict or None
        """
        kernel = self.get_kernel()
        if kernel is None:
            return None
        
        try:
            info = kernel.system_info()
            return {
                "state": info.state.value if hasattr(info.state, 'value') else str(info.state),
                "uptime": info.uptime,
                "guardians_count": info.guardians_count,
                "modules_count": info.modules_count,
                "events_processed": info.events_processed,
                "kernel_version": info.version_lock.kernel_version,
                "initialized_at": info.initialized_at.isoformat() if info.initialized_at else None,
                "last_heartbeat": info.last_heartbeat.isoformat() if info.last_heartbeat else None
            }
            logger.debug("System info retrieved successfully")
            return info_dict
        except AttributeError as e:
            logger.error(f"Kernel info missing expected attribute: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Failed to get system info: {e}", exc_info=True)
            return None


# Global adapter instance
_adapter_instance: Optional[KernelAdapter] = None


def get_kernel_adapter(kernel_path: Optional[str] = None) -> KernelAdapter:
    """
    Get global kernel adapter instance.
    
    Args:
        kernel_path: Optional kernel path override
    
    Returns:
        KernelAdapter instance
    """
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = KernelAdapter(kernel_path)
    return _adapter_instance

