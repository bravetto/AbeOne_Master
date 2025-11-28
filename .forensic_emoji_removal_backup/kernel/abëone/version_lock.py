"""
Version Lock Mechanism - Prevent Architectural Drift

Implements version locking mechanism to prevent architectural drift.

Pattern: VERSION × LOCK × VALIDATION × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
from pathlib import Path


@dataclass
class VersionLock:
    """Version lock metadata to prevent drift."""
    kernel_version: str
    guardians_version: str
    modules_version: str
    event_bus_version: str
    locked_at: datetime = field(default_factory=datetime.now)
    checksum: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "kernel_version": self.kernel_version,
            "guardians_version": self.guardians_version,
            "modules_version": self.modules_version,
            "event_bus_version": self.event_bus_version,
            "locked_at": self.locked_at.isoformat(),
            "checksum": self.checksum,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VersionLock':
        """Create from dictionary."""
        locked_at = datetime.fromisoformat(data["locked_at"]) if isinstance(data.get("locked_at"), str) else datetime.now()
        return cls(
            kernel_version=data["kernel_version"],
            guardians_version=data["guardians_version"],
            modules_version=data["modules_version"],
            event_bus_version=data["event_bus_version"],
            locked_at=locked_at,
            checksum=data.get("checksum"),
            metadata=data.get("metadata", {})
        )
    
    def calculate_checksum(self) -> str:
        """Calculate checksum for version lock."""
        data = {
            "kernel_version": self.kernel_version,
            "guardians_version": self.guardians_version,
            "modules_version": self.modules_version,
            "event_bus_version": self.event_bus_version
        }
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def update_checksum(self) -> None:
        """Update checksum."""
        self.checksum = self.calculate_checksum()


class VersionLockManager:
    """
    Version Lock Manager.
    
    Responsibilities:
    - Manage version locks
    - Persist version locks
    - Validate version locks
    - Detect version mismatches
    """
    
    def __init__(self, lock_file: Optional[str] = None):
        """Initialize version lock manager."""
        self.lock_file = lock_file or "config/version_lock.json"
        self.current_lock: Optional[VersionLock] = None
    
    def create_lock(self, kernel_version: str, guardians_version: str,
                   modules_version: str, event_bus_version: str,
                   metadata: Optional[Dict[str, Any]] = None) -> VersionLock:
        """
        Create a new version lock.
        
        Args:
            kernel_version: Kernel version
            guardians_version: Guardians version
            modules_version: Modules version
            event_bus_version: Event bus version
            metadata: Optional metadata
        
        Returns:
            Created version lock
        """
        lock = VersionLock(
            kernel_version=kernel_version,
            guardians_version=guardians_version,
            modules_version=modules_version,
            event_bus_version=event_bus_version,
            metadata=metadata or {}
        )
        lock.update_checksum()
        self.current_lock = lock
        return lock
    
    def save_lock(self, lock: VersionLock) -> bool:
        """
        Save version lock to file.
        
        Args:
            lock: Version lock to save
        
        Returns:
            True if save successful
        """
        try:
            lock_file = Path(self.lock_file)
            lock_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(lock_file, 'w') as f:
                json.dump(lock.to_dict(), f, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Failed to save version lock: {e}")
            return False
    
    def load_lock(self) -> Optional[VersionLock]:
        """
        Load version lock from file.
        
        Returns:
            Version lock or None
        """
        try:
            lock_file = Path(self.lock_file)
            if not lock_file.exists():
                return None
            
            with open(lock_file, 'r') as f:
                data = json.load(f)
            
            lock = VersionLock.from_dict(data)
            self.current_lock = lock
            return lock
        except Exception as e:
            print(f"❌ Failed to load version lock: {e}")
            return None
    
    def validate_lock(self, lock: VersionLock) -> bool:
        """
        Validate version lock checksum.
        
        Args:
            lock: Version lock to validate
        
        Returns:
            True if valid
        """
        expected_checksum = lock.calculate_checksum()
        return lock.checksum == expected_checksum
    
    def compare_locks(self, lock1: VersionLock, lock2: VersionLock) -> Dict[str, Any]:
        """
        Compare two version locks.
        
        Args:
            lock1: First version lock
            lock2: Second version lock
        
        Returns:
            Comparison result dictionary
        """
        mismatches = []
        
        if lock1.kernel_version != lock2.kernel_version:
            mismatches.append({
                "component": "kernel",
                "expected": lock1.kernel_version,
                "actual": lock2.kernel_version
            })
        
        if lock1.guardians_version != lock2.guardians_version:
            mismatches.append({
                "component": "guardians",
                "expected": lock1.guardians_version,
                "actual": lock2.guardians_version
            })
        
        if lock1.modules_version != lock2.modules_version:
            mismatches.append({
                "component": "modules",
                "expected": lock1.modules_version,
                "actual": lock2.modules_version
            })
        
        if lock1.event_bus_version != lock2.event_bus_version:
            mismatches.append({
                "component": "event_bus",
                "expected": lock1.event_bus_version,
                "actual": lock2.event_bus_version
            })
        
        return {
            "matches": len(mismatches) == 0,
            "mismatches": mismatches
        }

