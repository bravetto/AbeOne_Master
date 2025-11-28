"""
Module Registry - Product Module Registration and Lifecycle Management

Registers product modules (AbëBEATs, TRUICE) and provides lifecycle hooks.

Pattern: MODULE × REGISTRY × LIFECYCLE × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Any, Protocol, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod


class ModuleStatus(Enum):
    """Module status."""
    UNREGISTERED = "unregistered"
    REGISTERED = "registered"
    LOADING = "loading"
    LOADED = "loaded"
    ACTIVE = "active"
    DEGRADED = "degraded"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"
    ERROR = "error"


class ModuleHealth(Enum):
    """Module health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class ModuleInterface(Protocol):
    """
    Module interface definition.
    
    All modules must implement these lifecycle hooks.
    """
    
    @property
    def module_id(self) -> str:
        """Get module identifier."""
        ...
    
    @property
    def version(self) -> str:
        """Get module version."""
        ...
    
    def on_load(self) -> bool:
        """
        Called when module is loaded.
        
        Returns:
            True if load successful
        """
        ...
    
    def on_event(self, event: Any) -> Any:
        """
        Called when module receives an event.
        
        Args:
            event: Event to handle
        
        Returns:
            Event handling result
        """
        ...
    
    def shutdown(self) -> None:
        """Called when module is shutting down."""
        ...


@dataclass
class ModuleMetadata:
    """Module metadata."""
    module_id: str
    name: str
    version: str
    status: ModuleStatus
    health: ModuleHealth
    registered_at: datetime
    loaded_at: Optional[datetime] = None
    last_heartbeat: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ModuleRegistry:
    """
    Module Registry.
    
    Responsibilities:
    - Register product modules (AbëBEATs, TRUICE)
    - Provide lifecycle hooks (on_load, on_event, shutdown)
    - Track module health and version
    """
    
    def __init__(self, version: str = "1.0.0"):
        """Initialize registry."""
        self.version = version
        self.modules: Dict[str, ModuleInterface] = {}
        self.metadata: Dict[str, ModuleMetadata] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
    
    def register(self, module: ModuleInterface, name: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Register a module.
        
        Args:
            module: Module instance implementing ModuleInterface
            name: Module name
            metadata: Optional metadata
        
        Returns:
            True if registration successful
        """
        module_id = module.module_id
        
        if module_id in self.modules:
            return False  # Already registered
        
        self.modules[module_id] = module
        self.metadata[module_id] = ModuleMetadata(
            module_id=module_id,
            name=name,
            version=module.version,
            status=ModuleStatus.REGISTERED,
            health=ModuleHealth.UNKNOWN,
            registered_at=datetime.now(),
            metadata=metadata or {}
        )
        
        return True
    
    def unregister(self, module_id: str) -> bool:
        """
        Unregister a module.
        
        Args:
            module_id: Module identifier
        
        Returns:
            True if unregistration successful
        """
        if module_id not in self.modules:
            return False
        
        # Shutdown module before unregistering
        module = self.modules[module_id]
        if hasattr(module, 'shutdown'):
            module.shutdown()
        
        del self.modules[module_id]
        del self.metadata[module_id]
        
        if module_id in self.event_handlers:
            del self.event_handlers[module_id]
        
        return True
    
    def load(self, module_id: str) -> bool:
        """
        Load a module (call on_load hook).
        
        Args:
            module_id: Module identifier
        
        Returns:
            True if load successful
        """
        if module_id not in self.modules:
            return False
        
        module = self.modules[module_id]
        metadata = self.metadata[module_id]
        
        metadata.status = ModuleStatus.LOADING
        
        try:
            success = module.on_load()
            
            if success:
                metadata.status = ModuleStatus.LOADED
                metadata.loaded_at = datetime.now()
                return True
            else:
                metadata.status = ModuleStatus.ERROR
                return False
                
        except Exception as e:
            metadata.status = ModuleStatus.ERROR
            metadata.metadata['error'] = str(e)
            return False
    
    def activate(self, module_id: str) -> bool:
        """
        Activate a module (transition to ACTIVE status).
        
        Args:
            module_id: Module identifier
        
        Returns:
            True if activation successful
        """
        if module_id not in self.modules:
            return False
        
        metadata = self.metadata[module_id]
        
        if metadata.status != ModuleStatus.LOADED:
            return False
        
        metadata.status = ModuleStatus.ACTIVE
        metadata.health = ModuleHealth.HEALTHY
        return True
    
    def send_event(self, module_id: str, event: Any) -> Any:
        """
        Send event to module (call on_event hook).
        
        Args:
            module_id: Module identifier
            event: Event to send
        
        Returns:
            Event handling result
        """
        if module_id not in self.modules:
            return None
        
        module = self.modules[module_id]
        metadata = self.metadata[module_id]
        
        if metadata.status != ModuleStatus.ACTIVE:
            return None
        
        try:
            metadata.last_heartbeat = datetime.now()
            return module.on_event(event)
        except Exception as e:
            metadata.status = ModuleStatus.DEGRADED
            metadata.health = ModuleHealth.UNHEALTHY
            metadata.metadata['error'] = str(e)
            return None
    
    def shutdown(self) -> None:
        """Shutdown all modules."""
        for module_id in list(self.modules.keys()):
            self.shutdown_module(module_id)
    
    def shutdown_module(self, module_id: str) -> bool:
        """
        Shutdown a module (call shutdown hook).
        
        Args:
            module_id: Module identifier
        
        Returns:
            True if shutdown successful
        """
        if module_id not in self.modules:
            return False
        
        module = self.modules[module_id]
        metadata = self.metadata[module_id]
        
        metadata.status = ModuleStatus.SHUTTING_DOWN
        
        try:
            module.shutdown()
            metadata.status = ModuleStatus.SHUTDOWN
            return True
        except Exception as e:
            metadata.status = ModuleStatus.ERROR
            metadata.metadata['error'] = str(e)
            return False
    
    def get(self, module_id: str) -> Optional[ModuleInterface]:
        """
        Get module by ID.
        
        Args:
            module_id: Module identifier
        
        Returns:
            Module instance or None
        """
        return self.modules.get(module_id)
    
    def get_all(self) -> List[ModuleInterface]:
        """
        Get all modules.
        
        Returns:
            List of all modules
        """
        return list(self.modules.values())
    
    def get_modules_count(self) -> int:
        """
        Get total number of registered modules.
        
        Returns:
            Number of modules
        """
        return len(self.modules)
    
    def get_version(self) -> str:
        """Get registry version."""
        return self.version
    
    def get_metadata(self, module_id: str) -> Optional[ModuleMetadata]:
        """
        Get module metadata.
        
        Args:
            module_id: Module identifier
        
        Returns:
            Module metadata or None
        """
        return self.metadata.get(module_id)
    
    def update_health(self, module_id: str, health: ModuleHealth) -> bool:
        """
        Update module health.
        
        Args:
            module_id: Module identifier
            health: New health status
        
        Returns:
            True if update successful
        """
        if module_id not in self.metadata:
            return False
        
        self.metadata[module_id].health = health
        
        if health == ModuleHealth.UNHEALTHY:
            self.metadata[module_id].status = ModuleStatus.DEGRADED
        
        return True


# Global registry instance
_registry_instance: Optional[ModuleRegistry] = None


def get_registry() -> ModuleRegistry:
    """Get global registry instance."""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = ModuleRegistry()
    return _registry_instance


def register_abebeats_module() -> bool:
    """
    Register AbëBEATs module.
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import module
        from modules.abebeats.module import AbeBeatsModule
        
        registry = get_registry()
        module = AbeBeatsModule()
        
        success = registry.register(module, name="AbëBEATs")
        if success:
            registry.load(module.module_id)
            registry.activate(module.module_id)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register AbëBEATs module: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_ads_module() -> bool:
    """
    Register Ads module.
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import module
        from modules.ads.module import AdsModule
        
        registry = get_registry()
        module = AdsModule()
        
        success = registry.register(module, name="Ads")
        if success:
            registry.load(module.module_id)
            registry.activate(module.module_id)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register Ads module: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_analytics_module() -> bool:
    """
    Register Analytics module.
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import module
        from modules.analytics.module import AnalyticsModule
        
        registry = get_registry()
        module = AnalyticsModule()
        
        success = registry.register(module, name="Analytics")
        if success:
            registry.load(module.module_id)
            registry.activate(module.module_id)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register Analytics module: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_seo_module() -> bool:
    """
    Register SEO module.
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import module
        from modules.seo.module import SeoModule
        
        registry = get_registry()
        module = SeoModule()
        
        success = registry.register(module, name="SEO")
        if success:
            registry.load(module.module_id)
            registry.activate(module.module_id)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register SEO module: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_content_module() -> bool:
    """
    Register Content module.
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import module
        from modules.content.module import ContentModule
        
        registry = get_registry()
        module = ContentModule()
        
        success = registry.register(module, name="Content")
        if success:
            registry.load(module.module_id)
            registry.activate(module.module_id)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register Content module: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_ctv_module() -> bool:
    """
    Register CTV module.
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import module
        from modules.ctv.module import CtvModule
        
        registry = get_registry()
        module = CtvModule()
        
        success = registry.register(module, name="CTV")
        if success:
            registry.load(module.module_id)
            registry.activate(module.module_id)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register CTV module: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_dooh_module() -> bool:
    """
    Register DOOH/Radio module.
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import module
        from modules.dooh.module import DoohModule
        
        registry = get_registry()
        module = DoohModule()
        
        success = registry.register(module, name="DOOH/Radio")
        if success:
            registry.load(module.module_id)
            registry.activate(module.module_id)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register DOOH/Radio module: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_social_module() -> bool:
    """
    Register Social module.
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import module
        from modules.social.module import SocialModule
        
        registry = get_registry()
        module = SocialModule()
        
        success = registry.register(module, name="Social")
        if success:
            registry.load(module.module_id)
            registry.activate(module.module_id)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register Social module: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_datalake_module() -> bool:
    """
    Register Data Lake module.
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import module
        from modules.datalake.module import DataLakeModule
        
        registry = get_registry()
        module = DataLakeModule()
        
        success = registry.register(module, name="Data Lake")
        if success:
            registry.load(module.module_id)
            registry.activate(module.module_id)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register Data Lake module: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_orbit_repo_module(orbit_repo_path: str, module_id: str) -> bool:
    """
    Register an Orbit Repo module dynamically.
    
    This function allows Orbit Repos to register themselves with the kernel
    by providing their path and module registration function.
    
    Args:
        orbit_repo_path: Path to Orbit Repo root directory
        module_id: Module identifier
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        import importlib.util
        from pathlib import Path
        
        orbit_path = Path(orbit_repo_path)
        if not orbit_path.exists():
            print(f"❌ Orbit Repo path does not exist: {orbit_repo_path}")
            return False
        
        # Try to load register_module.py from Orbit Repo
        register_script = orbit_path / "register_module.py"
        if register_script.exists():
            # Execute registration script
            spec = importlib.util.spec_from_file_location("orbit_register", register_script)
            if spec is None or spec.loader is None:
                print(f"❌ Failed to load registration script: {register_script}")
                return False
            
            module = importlib.util.module_from_spec(spec)
            sys.path.insert(0, str(orbit_path))
            spec.loader.exec_module(module)
            
            # Call register function if it exists
            if hasattr(module, 'register_abebeats_module'):
                return module.register_abebeats_module()
            elif hasattr(module, 'register_module'):
                return module.register_module()
            else:
                print(f"❌ Registration script does not export register function: {register_script}")
                return False
        
        # Fallback: Try to use adapter.module
        adapters_dir = orbit_path / "adapters"
        if adapters_dir.exists():
            sys.path.insert(0, str(adapters_dir))
            
            # Try to import adapter.module
            try:
                adapter_module_spec = importlib.util.spec_from_file_location(
                    "adapter.module", adapters_dir / "adapter.module.py"
                )
                if adapter_module_spec and adapter_module_spec.loader:
                    adapter_module = importlib.util.module_from_spec(adapter_module_spec)
                    adapter_module_spec.loader.exec_module(adapter_module)
                    
                    # Get kernel path (should be orbit_repo_path/kernel/abeone)
                    kernel_path = orbit_path / "kernel" / "abeone"
                    
                    if hasattr(adapter_module, 'get_module_adapter'):
                        adapter = adapter_module.get_module_adapter(str(kernel_path))
                        if hasattr(adapter, 'register_abebeats'):
                            return adapter.register_abebeats()
            
            except Exception as e:
                print(f"⚠️  Adapter registration failed: {e}")
        
        print(f"❌ Could not find registration method for Orbit Repo: {orbit_repo_path}")
        return False
        
    except Exception as e:
        print(f"❌ Failed to register Orbit Repo module: {e}")
        import traceback
        traceback.print_exc()
        return False
