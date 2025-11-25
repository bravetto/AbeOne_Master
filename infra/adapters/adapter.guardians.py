"""
AbëONE Guardians Adapter - Master Workspace Integration

Bridges Master Workspace to AbëONE Guardians Registry.

Pattern: ADAPTER × GUARDIANS × WORKSPACE × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import sys
from ._logger import get_adapter_logger

logger = get_adapter_logger("GuardiansAdapter")


class GuardiansAdapter:
    """
    Guardians Adapter for AbëONE Master Workspace.
    
    Provides access to AbëONE guardians functionality.
    """
    
    def __init__(self, kernel_path: Optional[str] = None):
        """
        Initialize guardians adapter.
        
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
        
        self._registry = None
        self._initialized = False
        logger.debug(f"GuardiansAdapter initialized with path: {self.kernel_path}")
    
    def _load_registry(self) -> bool:
        """
        Load guardians registry.
        
        Returns:
            True if loaded successfully
        """
        if self._initialized:
            return True
        
        try:
            kernel_dir = str(self.kernel_path)
            if kernel_dir not in sys.path:
                sys.path.insert(0, kernel_dir)
            
            from GUARDIANS_REGISTRY import get_registry
            
            self._registry = get_registry()
            self._initialized = True
            logger.info("Guardians registry loaded successfully")
            return True
            
        except ImportError as e:
            logger.error(f"Failed to import GUARDIANS_REGISTRY: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Failed to load registry: {e}", exc_info=True)
            return False
    
    def get_registry(self) -> Optional[Any]:
        """
        Get guardians registry instance.
        
        Returns:
            Registry instance or None
        """
        if not self._load_registry():
            return None
        return self._registry
    
    def get_guardian(self, guardian_id: str) -> Optional[Any]:
        """
        Get guardian by ID.
        
        Args:
            guardian_id: Guardian identifier
        
        Returns:
            Guardian instance or None
        
        Raises:
            ValueError: If guardian_id is invalid
        """
        # Input validation
        if not guardian_id or not isinstance(guardian_id, str) or not guardian_id.strip():
            logger.error(f"Invalid guardian_id: '{guardian_id}'")
            raise ValueError("Guardian ID must be a non-empty string")
        
        registry = self.get_registry()
        if registry is None:
            logger.warning("Cannot get guardian: registry not available")
            return None
        
        try:
            guardian = registry.get(guardian_id)
            if guardian is None:
                logger.debug(f"Guardian '{guardian_id}' not found in registry")
            else:
                logger.debug(f"Guardian '{guardian_id}' retrieved successfully")
            return guardian
        except Exception as e:
            logger.error(f"Failed to get guardian '{guardian_id}': {e}", exc_info=True)
            return None
    
    def get_all_guardians(self) -> List[Any]:
        """
        Get all guardians.
        
        Returns:
            List of guardian instances
        """
        registry = self.get_registry()
        if registry is None:
            return []
        
        try:
            guardians = registry.get_all()
            logger.debug(f"Retrieved {len(guardians)} guardians from registry")
            return guardians
        except Exception as e:
            logger.error(f"Failed to get all guardians: {e}", exc_info=True)
            return []
    
    def register_guardian(self, guardian: Any, guardian_id: str) -> bool:
        """
        Register guardian.
        
        Args:
            guardian: Guardian instance
            guardian_id: Guardian identifier
        
        Returns:
            True if registration successful
        
        Raises:
            ValueError: If guardian or guardian_id is invalid
        """
        # Input validation
        if guardian is None:
            logger.error("Cannot register guardian: guardian is None")
            raise ValueError("Guardian cannot be None")
        
        if not guardian_id or not isinstance(guardian_id, str) or not guardian_id.strip():
            logger.error(f"Cannot register guardian: invalid guardian_id '{guardian_id}'")
            raise ValueError("Guardian ID must be a non-empty string")
        
        registry = self.get_registry()
        if registry is None:
            logger.error("Cannot register guardian: registry not available")
            return False
        
        try:
            result = registry.register(guardian, guardian_id)
            if result:
                logger.info(f"Guardian '{guardian_id}' registered successfully")
            else:
                logger.warning(f"Guardian '{guardian_id}' registration returned False")
            return result
        except AttributeError as e:
            logger.error(f"Guardian '{guardian_id}' missing required interface: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Failed to register guardian '{guardian_id}': {e}", exc_info=True)
            return False


# Global adapter instance
_adapter_instance: Optional[GuardiansAdapter] = None


def get_guardians_adapter(kernel_path: Optional[str] = None) -> GuardiansAdapter:
    """
    Get global guardians adapter instance.
    
    Args:
        kernel_path: Optional kernel path override
    
    Returns:
        GuardiansAdapter instance
    """
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = GuardiansAdapter(kernel_path)
    return _adapter_instance

