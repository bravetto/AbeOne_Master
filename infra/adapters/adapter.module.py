"""
AbëONE Module Adapter - Master Workspace Integration

Bridges Master Workspace to AbëONE Module Registry.

Pattern: ADAPTER × MODULE × WORKSPACE × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import sys
from ._logger import get_adapter_logger

logger = get_adapter_logger("ModuleAdapter")


class ModuleAdapter:
    """
    Module Adapter for AbëONE Master Workspace.
    
    Provides access to AbëONE module registry functionality.
    """
    
    def __init__(self, kernel_path: Optional[str] = None):
        """
        Initialize module adapter.
        
        Args:
            kernel_path: Path to kernel (default: abëone)
        
        Raises:
            ValueError: If kernel_path is invalid
        """
        if kernel_path is None:
            repo_root = Path(__file__).parent.parent
            kernel_path = repo_root / "abëone"
        
        self.kernel_path = Path(kernel_path)
        
        # Validate kernel path exists
        if not self.kernel_path.exists():
            error_msg = f"Kernel path does not exist: {self.kernel_path}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        self._registry = None
        self._initialized = False
        logger.debug(f"ModuleAdapter initialized with path: {self.kernel_path}")
    
    def _load_registry(self) -> bool:
        """
        Load module registry.
        
        Returns:
            True if loaded successfully
        """
        if self._initialized:
            return True
        
        try:
            kernel_dir = str(self.kernel_path)
            if kernel_dir not in sys.path:
                sys.path.insert(0, kernel_dir)
            
            from MODULE_REGISTRY import get_registry
            
            self._registry = get_registry()
            self._initialized = True
            logger.info("Module registry loaded successfully")
            return True
            
        except ImportError as e:
            logger.error(f"Failed to import MODULE_REGISTRY: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Failed to load registry: {e}", exc_info=True)
            return False
    
    def get_registry(self) -> Optional[Any]:
        """
        Get module registry instance.
        
        Returns:
            Registry instance or None
        """
        if not self._load_registry():
            return None
        return self._registry
    
    def register_module(self, module: Any, name: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Register module via MODULE_REGISTRY.register_module().
        
        Contract: adapter.module.py MUST register module via MODULE_REGISTRY.register_module().
        
        Args:
            module: Module instance implementing ModuleInterface
            name: Module name
            metadata: Optional metadata
        
        Returns:
            True if registration successful
        
        Raises:
            ValueError: If module or name is invalid
        """
        # Input validation
        if module is None:
            logger.error("Cannot register module: module is None")
            raise ValueError("Module cannot be None")
        
        if not name or not isinstance(name, str) or not name.strip():
            logger.error(f"Cannot register module: invalid name '{name}'")
            raise ValueError("Module name must be a non-empty string")
        
        registry = self.get_registry()
        if registry is None:
            logger.error("Cannot register module: registry not available")
            return False
        
        try:
            result = registry.register(module, name, metadata)
            if result:
                logger.info(f"Module '{name}' registered successfully")
            else:
                logger.warning(f"Module '{name}' registration returned False")
            return result
        except AttributeError as e:
            logger.error(f"Module '{name}' missing required interface: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Failed to register module '{name}': {e}", exc_info=True)
            return False
    
    def get_module(self, module_id: str) -> Optional[Any]:
        """
        Get module by ID.
        
        Args:
            module_id: Module identifier
        
        Returns:
            Module instance or None
        
        Raises:
            ValueError: If module_id is invalid
        """
        # Input validation
        if not module_id or not isinstance(module_id, str) or not module_id.strip():
            logger.error(f"Invalid module_id: '{module_id}'")
            raise ValueError("Module ID must be a non-empty string")
        
        registry = self.get_registry()
        if registry is None:
            logger.warning("Cannot get module: registry not available")
            return None
        
        try:
            module = registry.get(module_id)
            if module is None:
                logger.debug(f"Module '{module_id}' not found in registry")
            else:
                logger.debug(f"Module '{module_id}' retrieved successfully")
            return module
        except Exception as e:
            logger.error(f"Failed to get module '{module_id}': {e}", exc_info=True)
            return None
    
    def get_all_modules(self) -> List[Any]:
        """
        Get all modules.
        
        Returns:
            List of module instances
        """
        registry = self.get_registry()
        if registry is None:
            return []
        
        try:
            modules = registry.get_all()
            logger.debug(f"Retrieved {len(modules)} modules from registry")
            return modules
        except Exception as e:
            logger.error(f"Failed to get all modules: {e}", exc_info=True)
            return []


# Global adapter instance
_adapter_instance: Optional[ModuleAdapter] = None


def get_module_adapter(kernel_path: Optional[str] = None) -> ModuleAdapter:
    """
    Get global module adapter instance.
    
    Args:
        kernel_path: Optional kernel path override
    
    Returns:
        ModuleAdapter instance
    """
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = ModuleAdapter(kernel_path)
    return _adapter_instance


def register_abeone_master(metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    Register AbeOne_Master module via MODULE_REGISTRY.register().
    
    Contract: adapter.module.py MUST register module via MODULE_REGISTRY.register().
    Module registration at import-time.
    
    Args:
        metadata: Optional metadata dict
    
    Returns:
        True if registration successful
    """
    try:
        adapter = get_module_adapter()
        
        # Load module manifest for registration metadata
        repo_root = Path(__file__).parent.parent
        manifest_path = repo_root / "module_manifest.json"
        
        if manifest_path.exists():
            import json
            with open(manifest_path) as f:
                manifest = json.load(f)
            
            # Create module metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                "module_id": manifest.get("module_id", "abeone_master"),
                "name": manifest.get("name", "AbëONE Multi-Orbit Workspace"),
                "version": manifest.get("version", "1.0.0"),
                "description": manifest.get("description", ""),
                "kernelVersion": manifest.get("kernelVersion", "v0.9.0-stable"),
                "frequency": manifest.get("frequency", 999.0),
                "pattern": manifest.get("pattern", "ABEONE_MASTER × WORKSPACE × ORCHESTRATOR × MULTI_ORBIT × ONE"),
                "status": manifest.get("status", "operational"),
                "capabilities": manifest.get("capabilities", []),
            })
        
        # For workspace orchestrator, we register a workspace module object
        # Create a simple module-like object for registration
        class WorkspaceModule:
            def __init__(self, module_id: str, metadata: Dict[str, Any]):
                self.module_id = module_id
                self.metadata = metadata
            
            def __repr__(self):
                return f"WorkspaceModule(module_id='{self.module_id}')"
        
        module = WorkspaceModule("abeone_master", metadata)
        result = adapter.register_module(module, "abeone_master", metadata)
        
        if result:
            logger.info("AbeOne_Master module registered successfully")
        else:
            logger.warning("AbeOne_Master module registration returned False")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to register AbeOne_Master module: {e}", exc_info=True)
        return False


# Auto-register on import (if kernel is available)
try:
    register_abeone_master()
except Exception as e:
    # Don't fail import if registration fails (kernel might not be available)
    logger.debug(f"Auto-registration skipped: {e}")

