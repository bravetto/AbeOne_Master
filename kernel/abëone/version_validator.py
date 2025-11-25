"""
Version Validator - Validate Version Compatibility

Validates version compatibility and detects mismatches.

Pattern: VERSION × VALIDATION × COMPATIBILITY × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .version_lock import VersionLock, VersionLockManager


@dataclass
class VersionMismatch:
    """Version mismatch information."""
    component: str
    expected_version: str
    actual_version: str
    severity: str  # "error", "warning", "info"
    message: str


class VersionValidator:
    """
    Version Validator.
    
    Responsibilities:
    - Validate version compatibility
    - Detect version mismatches
    - Provide version mismatch details
    """
    
    def __init__(self, lock_manager: Optional[VersionLockManager] = None):
        """Initialize version validator."""
        self.lock_manager = lock_manager or VersionLockManager()
        self.required_versions: Dict[str, str] = {}
    
    def set_required_version(self, component: str, version: str) -> None:
        """
        Set required version for a component.
        
        Args:
            component: Component name
            version: Required version
        """
        self.required_versions[component] = version
    
    def validate_version(self, component: str, version: str) -> Tuple[bool, Optional[VersionMismatch]]:
        """
        Validate component version against required version.
        
        Args:
            component: Component name
            version: Actual version
        
        Returns:
            Tuple of (is_valid, mismatch_info)
        """
        if component not in self.required_versions:
            return True, None
        
        required_version = self.required_versions[component]
        
        if version != required_version:
            mismatch = VersionMismatch(
                component=component,
                expected_version=required_version,
                actual_version=version,
                severity="error",
                message=f"Version mismatch for {component}: expected {required_version}, got {version}"
            )
            return False, mismatch
        
        return True, None
    
    def validate_lock(self, lock: VersionLock) -> Tuple[bool, List[VersionMismatch]]:
        """
        Validate version lock against required versions.
        
        Args:
            lock: Version lock to validate
        
        Returns:
            Tuple of (is_valid, list_of_mismatches)
        """
        mismatches: List[VersionMismatch] = []
        
        # Validate kernel version
        is_valid, mismatch = self.validate_version("kernel", lock.kernel_version)
        if not is_valid and mismatch:
            mismatches.append(mismatch)
        
        # Validate guardians version
        is_valid, mismatch = self.validate_version("guardians", lock.guardians_version)
        if not is_valid and mismatch:
            mismatches.append(mismatch)
        
        # Validate modules version
        is_valid, mismatch = self.validate_version("modules", lock.modules_version)
        if not is_valid and mismatch:
            mismatches.append(mismatch)
        
        # Validate event bus version
        is_valid, mismatch = self.validate_version("event_bus", lock.event_bus_version)
        if not is_valid and mismatch:
            mismatches.append(mismatch)
        
        return len(mismatches) == 0, mismatches
    
    def check_compatibility(self, lock1: VersionLock, lock2: VersionLock) -> Tuple[bool, List[VersionMismatch]]:
        """
        Check compatibility between two version locks.
        
        Args:
            lock1: First version lock
            lock2: Second version lock
        
        Returns:
            Tuple of (is_compatible, list_of_mismatches)
        """
        mismatches: List[VersionMismatch] = []
        
        if lock1.kernel_version != lock2.kernel_version:
            mismatches.append(VersionMismatch(
                component="kernel",
                expected_version=lock1.kernel_version,
                actual_version=lock2.kernel_version,
                severity="error",
                message=f"Kernel version mismatch: {lock1.kernel_version} vs {lock2.kernel_version}"
            ))
        
        if lock1.guardians_version != lock2.guardians_version:
            mismatches.append(VersionMismatch(
                component="guardians",
                expected_version=lock1.guardians_version,
                actual_version=lock2.guardians_version,
                severity="warning",
                message=f"Guardians version mismatch: {lock1.guardians_version} vs {lock2.guardians_version}"
            ))
        
        if lock1.modules_version != lock2.modules_version:
            mismatches.append(VersionMismatch(
                component="modules",
                expected_version=lock1.modules_version,
                actual_version=lock2.modules_version,
                severity="warning",
                message=f"Modules version mismatch: {lock1.modules_version} vs {lock2.modules_version}"
            ))
        
        if lock1.event_bus_version != lock2.event_bus_version:
            mismatches.append(VersionMismatch(
                component="event_bus",
                expected_version=lock1.event_bus_version,
                actual_version=lock2.event_bus_version,
                severity="error",
                message=f"Event bus version mismatch: {lock1.event_bus_version} vs {lock2.event_bus_version}"
            ))
        
        return len(mismatches) == 0, mismatches

