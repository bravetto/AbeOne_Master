"""
Module Lifecycle Management - Enhanced Lifecycle Management

Enhanced module lifecycle management with dependency resolution and health checks.

Pattern: MODULE × LIFECYCLE × DEPENDENCIES × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from .MODULE_REGISTRY import ModuleStatus, ModuleHealth, ModuleInterface, ModuleMetadata


class LifecyclePhase(Enum):
    """Lifecycle phase."""
    REGISTRATION = "registration"
    DEPENDENCY_RESOLUTION = "dependency_resolution"
    LOADING = "loading"
    ACTIVATION = "activation"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"


@dataclass
class ModuleDependency:
    """Module dependency definition."""
    module_id: str
    required: bool = True
    min_version: Optional[str] = None
    max_version: Optional[str] = None


@dataclass
class LifecycleState:
    """Module lifecycle state."""
    module_id: str
    phase: LifecyclePhase
    dependencies: List[str] = field(default_factory=list)
    resolved_dependencies: Set[str] = field(default_factory=set)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class ModuleLifecycleManager:
    """
    Module Lifecycle Manager.
    
    Responsibilities:
    - Manage module lifecycle
    - Resolve dependencies
    - Coordinate lifecycle phases
    - Handle lifecycle errors
    """
    
    def __init__(self):
        """Initialize lifecycle manager."""
        self.lifecycle_states: Dict[str, LifecycleState] = {}
        self.dependency_graph: Dict[str, List[ModuleDependency]] = {}
    
    def register_module_dependencies(self, module_id: str, dependencies: List[ModuleDependency]) -> None:
        """
        Register module dependencies.
        
        Args:
            module_id: Module identifier
            dependencies: List of dependencies
        """
        self.dependency_graph[module_id] = dependencies
    
    def resolve_dependencies(self, module_id: str, available_modules: Dict[str, ModuleInterface]) -> Tuple[bool, List[str]]:
        """
        Resolve module dependencies.
        
        Args:
            module_id: Module identifier
            available_modules: Dictionary of available modules
        
        Returns:
            Tuple of (is_resolved, missing_dependencies)
        """
        if module_id not in self.dependency_graph:
            return True, []  # No dependencies
        
        dependencies = self.dependency_graph[module_id]
        missing_dependencies: List[str] = []
        
        for dep in dependencies:
            if dep.module_id not in available_modules:
                if dep.required:
                    missing_dependencies.append(dep.module_id)
                continue
            
            # Check version constraints if specified
            if dep.min_version or dep.max_version:
                module = available_modules[dep.module_id]
                module_version = module.version
                
                # Simple version comparison (can be enhanced)
                if dep.min_version and self._compare_versions(module_version, dep.min_version) < 0:
                    if dep.required:
                        missing_dependencies.append(f"{dep.module_id} (min_version: {dep.min_version})")
                
                if dep.max_version and self._compare_versions(module_version, dep.max_version) > 0:
                    if dep.required:
                        missing_dependencies.append(f"{dep.module_id} (max_version: {dep.max_version})")
        
        return len(missing_dependencies) == 0, missing_dependencies
    
    def _compare_versions(self, version1: str, version2: str) -> int:
        """
        Compare two version strings.
        
        Args:
            version1: First version
            version2: Second version
        
        Returns:
            -1 if version1 < version2, 0 if equal, 1 if version1 > version2
        """
        # Simple version comparison (can be enhanced with semver)
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1_part < v2_part:
                return -1
            elif v1_part > v2_part:
                return 1
        
        return 0
    
    def get_load_order(self, module_ids: List[str], available_modules: Dict[str, ModuleInterface]) -> List[str]:
        """
        Get module load order based on dependencies.
        
        Args:
            module_ids: List of module IDs
            available_modules: Dictionary of available modules
        
        Returns:
            Ordered list of module IDs
        """
        # Build dependency graph
        graph: Dict[str, Set[str]] = {}
        for module_id in module_ids:
            graph[module_id] = set()
            if module_id in self.dependency_graph:
                for dep in self.dependency_graph[module_id]:
                    if dep.module_id in module_ids:
                        graph[module_id].add(dep.module_id)
        
        # Topological sort
        ordered: List[str] = []
        visited: Set[str] = set()
        temp_visited: Set[str] = set()
        
        def visit(node: str) -> bool:
            if node in temp_visited:
                return False  # Cycle detected
            if node in visited:
                return True
            
            temp_visited.add(node)
            
            for dep in graph.get(node, set()):
                if not visit(dep):
                    return False
            
            temp_visited.remove(node)
            visited.add(node)
            ordered.append(node)
            return True
        
        for module_id in module_ids:
            if module_id not in visited:
                if not visit(module_id):
                    return []  # Cycle detected
        
        return ordered
    
    def get_shutdown_order(self, module_ids: List[str]) -> List[str]:
        """
        Get module shutdown order (reverse of load order).
        
        Args:
            module_ids: List of module IDs
        
        Returns:
            Ordered list of module IDs for shutdown
        """
        load_order = self.get_load_order(module_ids, {})
        return list(reversed(load_order))
    
    def set_lifecycle_state(self, module_id: str, phase: LifecyclePhase, error: Optional[str] = None) -> None:
        """
        Set lifecycle state for a module.
        
        Args:
            module_id: Module identifier
            phase: Lifecycle phase
            error: Optional error message
        """
        if module_id not in self.lifecycle_states:
            self.lifecycle_states[module_id] = LifecycleState(
                module_id=module_id,
                phase=phase
            )
        
        state = self.lifecycle_states[module_id]
        state.phase = phase
        
        if phase == LifecyclePhase.RUNNING and not state.started_at:
            state.started_at = datetime.now()
        
        if phase in [LifecyclePhase.SHUTDOWN, LifecyclePhase.SHUTTING_DOWN] and not state.completed_at:
            state.completed_at = datetime.now()
        
        if error:
            state.error = error
    
    def get_lifecycle_state(self, module_id: str) -> Optional[LifecycleState]:
        """
        Get lifecycle state for a module.
        
        Args:
            module_id: Module identifier
        
        Returns:
            Lifecycle state or None
        """
        return self.lifecycle_states.get(module_id)

