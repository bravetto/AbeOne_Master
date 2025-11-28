"""
ONE-Kernel - Core Organism Kernel

Maintains global system state, provides registration hooks,
and prevents drift through version-lock metadata.

Pattern: KERNEL × STATE × REGISTRATION × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading


class SystemState(Enum):
    """System state enumeration."""
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    DEGRADED = "degraded"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"


@dataclass
class VersionLock:
    """Version lock metadata to prevent drift."""
    kernel_version: str
    guardians_version: str
    modules_version: str
    event_bus_version: str
    locked_at: datetime = field(default_factory=datetime.now)
    checksum: Optional[str] = None


@dataclass
class SystemInfo:
    """System information structure."""
    state: SystemState
    uptime: float
    guardians_count: int
    modules_count: int
    events_processed: int
    version_lock: VersionLock
    initialized_at: Optional[datetime] = None
    last_heartbeat: Optional[datetime] = None


class OneKernel:
    """
    Core organism kernel.
    
    Responsibilities:
    - Maintain global system state
    - Provide registration hooks for Guardians and Modules
    - Provide initialization and heartbeat
    - Prevent drift through version-lock metadata
    """
    
    def __init__(self, kernel_version: str = "1.0.0"):
        """Initialize kernel."""
        self.kernel_version = kernel_version
        self.state = SystemState.UNINITIALIZED
        self.initialized_at: Optional[datetime] = None
        self.last_heartbeat: Optional[datetime] = None
        self.start_time: Optional[datetime] = None
        
        # Registration hooks
        self.guardian_registry: Optional[Callable] = None
        self.module_registry: Optional[Callable] = None
        self.event_bus: Optional[Callable] = None
        
        # State tracking
        self.guardians_count = 0
        self.modules_count = 0
        self.events_processed = 0
        
        # Version lock
        self.version_lock = VersionLock(
            kernel_version=kernel_version,
            guardians_version="0.0.0",
            modules_version="0.0.0",
            event_bus_version="0.0.0"
        )
        
        # Thread safety
        self._lock = threading.Lock()
    
    def register_guardian_registry(self, registry: Callable) -> None:
        """Register Guardian registry hook."""
        with self._lock:
            self.guardian_registry = registry
            if hasattr(registry, 'get_guardians_count'):
                self.guardians_count = registry.get_guardians_count()
    
    def register_module_registry(self, registry: Callable) -> None:
        """Register Module registry hook."""
        with self._lock:
            self.module_registry = registry
            if hasattr(registry, 'get_modules_count'):
                self.modules_count = registry.get_modules_count()
    
    def register_event_bus(self, bus: Callable) -> None:
        """Register Event Bus hook."""
        with self._lock:
            self.event_bus = bus
    
    def initialize(self) -> bool:
        """
        Initialize kernel.
        
        Returns:
            True if initialization successful
        """
        with self._lock:
            if self.state != SystemState.UNINITIALIZED:
                return False
            
            self.state = SystemState.INITIALIZING
            
            try:
                # Validate registries are connected
                if not self.guardian_registry:
                    raise ValueError("Guardian registry not registered")
                if not self.module_registry:
                    raise ValueError("Module registry not registered")
                if not self.event_bus:
                    raise ValueError("Event bus not registered")
                
                # Update version lock
                if hasattr(self.guardian_registry, 'get_version'):
                    self.version_lock.guardians_version = self.guardian_registry.get_version()
                if hasattr(self.module_registry, 'get_version'):
                    self.version_lock.modules_version = self.module_registry.get_version()
                if hasattr(self.event_bus, 'get_version'):
                    self.version_lock.event_bus_version = self.event_bus.get_version()
                
                # Register Guardian One (Abë - The Truth Engine)
                try:
                    from GUARDIANS_REGISTRY import register_guardian_one
                    register_guardian_one()
                    print(" Guardian 1 (Abë) online at 530 Hz")
                except Exception as e:
                    print(f" Warning: Failed to register Guardian One: {e}")
                
                # Register Guardian Two (Synthesis Orchestrator - 888 Hz)
                try:
                    from GUARDIANS_REGISTRY import register_guardian_two
                    register_guardian_two()
                    print(" Guardian 2 (Synthesis Orchestrator) online at 888 Hz")
                except Exception as e:
                    print(f" Warning: Failed to register Guardian Two: {e}")
                
                # Register Guardian Three (Alignment Validator - 777 Hz)
                try:
                    from GUARDIANS_REGISTRY import register_guardian_three
                    register_guardian_three()
                    print(" Guardian 3 (Alignment Validator) online at 777 Hz")
                except Exception as e:
                    print(f" Warning: Failed to register Guardian Three: {e}")
                
                # Register Guardian Five (Execution Orchestrator - 999 Hz)
                try:
                    from GUARDIANS_REGISTRY import register_guardian_five
                    register_guardian_five()
                    print(" Guardian 5 (Execution Orchestrator) online at 999 Hz")
                except Exception as e:
                    print(f" Warning: Failed to register Guardian Five: {e}")
                
                # Initialize state
                self.initialized_at = datetime.now()
                self.start_time = datetime.now()
                self.state = SystemState.READY
                
                return True
                
            except Exception as e:
                self.state = SystemState.DEGRADED
                raise e
    
    def start(self) -> bool:
        """
        Start kernel (transition to RUNNING state).
        
        Returns:
            True if start successful
        """
        with self._lock:
            if self.state != SystemState.READY:
                return False
            
            self.state = SystemState.RUNNING
            self.last_heartbeat = datetime.now()
            return True
        
    def heartbeat(self) -> None:
        """Update heartbeat timestamp."""
        with self._lock:
            self.last_heartbeat = datetime.now()
            
            # Update counts from registries
            if self.guardian_registry and hasattr(self.guardian_registry, 'get_guardians_count'):
                self.guardians_count = self.guardian_registry.get_guardians_count()
            
            if self.module_registry and hasattr(self.module_registry, 'get_modules_count'):
                self.modules_count = self.module_registry.get_modules_count()
            
            if self.event_bus and hasattr(self.event_bus, 'get_events_processed'):
                self.events_processed = self.event_bus.get_events_processed()
    
    def shutdown(self) -> None:
        """Shutdown kernel gracefully."""
        with self._lock:
            if self.state == SystemState.SHUTDOWN:
                return
            
            self.state = SystemState.SHUTTING_DOWN
            
            # Shutdown registries
            if self.module_registry and hasattr(self.module_registry, 'shutdown'):
                self.module_registry.shutdown()
            
            self.state = SystemState.SHUTDOWN
    
    def kernel_ready(self) -> bool:
        """
        Check if kernel is ready.
        
        Returns:
            True if kernel is ready
        """
        with self._lock:
            return self.state == SystemState.READY or self.state == SystemState.RUNNING
    
    def system_info(self) -> SystemInfo:
        """
        Get system information.
        
        Returns:
            SystemInfo structure
        """
        with self._lock:
            uptime = 0.0
            if self.start_time:
                uptime = (datetime.now() - self.start_time).total_seconds()
            
            return SystemInfo(
                state=self.state,
                uptime=uptime,
                guardians_count=self.guardians_count,
                modules_count=self.modules_count,
                events_processed=self.events_processed,
                version_lock=self.version_lock,
                initialized_at=self.initialized_at,
                last_heartbeat=self.last_heartbeat
            )
    
    def get_version_lock(self) -> VersionLock:
        """Get version lock metadata."""
        with self._lock:
            return self.version_lock


# Global kernel instance
_kernel_instance: Optional[OneKernel] = None


def get_kernel() -> OneKernel:
    """Get global kernel instance."""
    global _kernel_instance
    if _kernel_instance is None:
        _kernel_instance = OneKernel()
    return _kernel_instance
