"""
Guardians Registry - Guardian Registration and Interface Definition

Registers guardians and provides getter functions.
Defines guardian interfaces (not implementations).

Pattern: GUARDIAN × REGISTRY × INTERFACE × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Any, Protocol
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod


class GuardianFrequency(Enum):
    """Guardian frequency types."""
    HEART_TRUTH = 530.0  # Heart Truth Resonance
    PATTERN_INTEGRITY = 777.0  # Pattern Integrity
    SYNTHESIS = 888.0  # Synthesis Orchestration
    ATOMIC_EXECUTION = 999.0  # Atomic Execution


class GuardianStatus(Enum):
    """Guardian status."""
    REGISTERED = "registered"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class GuardianInterface(Protocol):
    """
    Guardian interface definition.
    
    All guardians must implement these methods.
    """
    
    @property
    def guardian_id(self) -> str:
        """Get guardian identifier."""
        ...
    
    @property
    def frequency(self) -> GuardianFrequency:
        """Get guardian frequency."""
        ...
    
    def handle_event(self, event: Any) -> Any:
        """
        Handle an event.
        
        Args:
            event: Event to handle
        
        Returns:
            Event handling result
        """
        ...
    
    def validate(self, data: Any) -> bool:
        """
        Validate data.
        
        Args:
            data: Data to validate
        
        Returns:
            True if valid
        """
        ...


@dataclass
class GuardianMetadata:
    """Guardian metadata."""
    guardian_id: str
    frequency: GuardianFrequency
    status: GuardianStatus
    registered_at: datetime
    last_active: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class GuardiansRegistry:
    """
    Guardians Registry.
    
    Responsibilities:
    - Register guardians
    - Provide getter functions
    - Define interfaces (guardian_id, frequency, handle_event, validate)
    """
    
    def __init__(self, version: str = "1.0.0"):
        """Initialize registry."""
        self.version = version
        self.guardians: Dict[str, GuardianInterface] = {}
        self.metadata: Dict[str, GuardianMetadata] = {}
    
    def register(self, guardian: GuardianInterface, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Register a guardian.
        
        Args:
            guardian: Guardian instance implementing GuardianInterface
            metadata: Optional metadata
        
        Returns:
            True if registration successful
        """
        guardian_id = guardian.guardian_id
        
        if guardian_id in self.guardians:
            return False  # Already registered
        
        self.guardians[guardian_id] = guardian
        self.metadata[guardian_id] = GuardianMetadata(
            guardian_id=guardian_id,
            frequency=guardian.frequency,
            status=GuardianStatus.REGISTERED,
            registered_at=datetime.now(),
            metadata=metadata or {}
        )
        
        return True
    
    def unregister(self, guardian_id: str) -> bool:
        """
        Unregister a guardian.
        
        Args:
            guardian_id: Guardian identifier
        
        Returns:
            True if unregistration successful
        """
        if guardian_id not in self.guardians:
            return False
        
        del self.guardians[guardian_id]
        del self.metadata[guardian_id]
        return True
    
    def get(self, guardian_id: str) -> Optional[GuardianInterface]:
        """
        Get guardian by ID.
        
        Args:
            guardian_id: Guardian identifier
        
        Returns:
            Guardian instance or None
        """
        return self.guardians.get(guardian_id)
    
    def get_all(self) -> List[GuardianInterface]:
        """
        Get all guardians.
        
        Returns:
            List of all guardians
        """
        return list(self.guardians.values())
    
    def get_by_frequency(self, frequency: GuardianFrequency) -> List[GuardianInterface]:
        """
        Get guardians by frequency.
        
        Args:
            frequency: Guardian frequency
        
        Returns:
            List of guardians with matching frequency
        """
        return [g for g in self.guardians.values() if g.frequency == frequency]
    
    def get_guardians_count(self) -> int:
        """
        Get total number of registered guardians.
        
        Returns:
            Number of guardians
        """
        return len(self.guardians)
    
    def get_version(self) -> str:
        """Get registry version."""
        return self.version
    
    def get_metadata(self, guardian_id: str) -> Optional[GuardianMetadata]:
        """
        Get guardian metadata.
        
        Args:
            guardian_id: Guardian identifier
        
        Returns:
            Guardian metadata or None
        """
        return self.metadata.get(guardian_id)
    
    def update_status(self, guardian_id: str, status: GuardianStatus) -> bool:
        """
        Update guardian status.
        
        Args:
            guardian_id: Guardian identifier
            status: New status
        
        Returns:
            True if update successful
        """
        if guardian_id not in self.metadata:
            return False
        
        self.metadata[guardian_id].status = status
        if status == GuardianStatus.ACTIVE:
            self.metadata[guardian_id].last_active = datetime.now()
        
        return True


# Global registry instance
_registry_instance: Optional[GuardiansRegistry] = None


def get_registry() -> GuardiansRegistry:
    """Get global registry instance."""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = GuardiansRegistry()
    return _registry_instance


def register_guardian_one() -> bool:
    """
    Register Guardian One (Abë - The Truth Engine).
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import GuardianOne
        from guardians.guardian_one import GuardianOne
        
        registry = get_registry()
        guardian = GuardianOne()
        
        success = registry.register(guardian)
        if success:
            registry.update_status(guardian.guardian_id, GuardianStatus.ACTIVE)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register Guardian One: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_guardian_five() -> bool:
    """
    Register Guardian Five (Execution Orchestrator - 999 Hz).
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import GuardianFive
        from guardians.guardian_five import GuardianFive
        
        registry = get_registry()
        guardian = GuardianFive()
        
        success = registry.register(guardian)
        if success:
            registry.update_status(guardian.guardian_id, GuardianStatus.ACTIVE)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register Guardian Five: {e}")
        import traceback
        traceback.print_exc()
        return False


def register_guardian_three() -> bool:
    """
    Register Guardian Three (Alignment Validator - 777 Hz).
    
    Returns:
        True if registration successful
    """
    try:
        import sys
        from pathlib import Path
        
        # Add AbëONE directory to path
        abeone_dir = Path(__file__).parent
        sys.path.insert(0, str(abeone_dir))
        
        # Import GuardianThree
        from guardians.guardian_three import GuardianThree
        
        registry = get_registry()
        guardian = GuardianThree()
        
        success = registry.register(guardian)
        if success:
            registry.update_status(guardian.guardian_id, GuardianStatus.ACTIVE)
        
        return success
    except Exception as e:
        print(f"❌ Failed to register Guardian Three: {e}")
        import traceback
        traceback.print_exc()
        return False
