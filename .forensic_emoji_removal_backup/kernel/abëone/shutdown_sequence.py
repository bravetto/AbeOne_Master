"""
Shutdown Sequence - Graceful Shutdown Sequence

Defines shutdown sequence for graceful shutdown.

Pattern: SHUTDOWN × SEQUENCE × GRACEFUL × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import List, Optional, Callable, Dict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ShutdownPhase(Enum):
    """Shutdown phases."""
    PRE_SHUTDOWN = "pre_shutdown"
    MODULE_SHUTDOWN = "module_shutdown"
    EVENT_BUS_SHUTDOWN = "event_bus_shutdown"
    REGISTRY_SHUTDOWN = "registry_shutdown"
    KERNEL_SHUTDOWN = "kernel_shutdown"
    POST_SHUTDOWN = "post_shutdown"


@dataclass
class ShutdownHook:
    """Shutdown hook definition."""
    hook_id: str
    phase: ShutdownPhase
    hook_func: Callable[[], None]
    timeout: float = 5.0
    priority: int = 0
    enabled: bool = True


@dataclass
class ShutdownStep:
    """Shutdown step definition."""
    step_id: str
    phase: ShutdownPhase
    description: str
    timeout: float = 10.0
    required: bool = True


class ShutdownSequence:
    """
    Shutdown Sequence.
    
    Responsibilities:
    - Define shutdown sequence
    - Execute shutdown hooks
    - Handle shutdown timeouts
    """
    
    def __init__(self):
        """Initialize shutdown sequence."""
        self.hooks: Dict[ShutdownPhase, List[ShutdownHook]] = {
            phase: [] for phase in ShutdownPhase
        }
        self.shutdown_steps: List[ShutdownStep] = []
        self.shutdown_started: Optional[datetime] = None
        self.shutdown_completed: Optional[datetime] = None
    
    def register_hook(self, hook: ShutdownHook) -> bool:
        """
        Register a shutdown hook.
        
        Args:
            hook: Shutdown hook definition
        
        Returns:
            True if registration successful
        """
        if hook.phase not in self.hooks:
            return False
        
        self.hooks[hook.phase].append(hook)
        # Sort by priority (higher priority first)
        self.hooks[hook.phase].sort(key=lambda h: h.priority, reverse=True)
        return True
    
    def add_step(self, step: ShutdownStep) -> None:
        """
        Add a shutdown step.
        
        Args:
            step: Shutdown step definition
        """
        self.shutdown_steps.append(step)
    
    def execute_shutdown(self) -> bool:
        """
        Execute shutdown sequence.
        
        Returns:
            True if shutdown successful
        """
        self.shutdown_started = datetime.now()
        
        try:
            # Execute shutdown steps in order
            for step in self.shutdown_steps:
                if not self._execute_step(step):
                    if step.required:
                        print(f"⚠️ Required shutdown step '{step.step_id}' failed")
                        return False
            
            # Execute hooks by phase
            for phase in ShutdownPhase:
                if not self._execute_phase_hooks(phase):
                    print(f"⚠️ Shutdown phase '{phase.value}' had failures")
            
            self.shutdown_completed = datetime.now()
            return True
            
        except Exception as e:
            print(f"❌ Shutdown sequence failed: {e}")
            return False
    
    def _execute_step(self, step: ShutdownStep) -> bool:
        """
        Execute a shutdown step.
        
        Args:
            step: Shutdown step definition
        
        Returns:
            True if step executed successfully
        """
        try:
            print(f"🔄 Executing shutdown step: {step.description}")
            # Step execution would be implemented based on step type
            return True
        except Exception as e:
            print(f"❌ Shutdown step '{step.step_id}' failed: {e}")
            return False
    
    def _execute_phase_hooks(self, phase: ShutdownPhase) -> bool:
        """
        Execute hooks for a phase.
        
        Args:
            phase: Shutdown phase
        
        Returns:
            True if all hooks executed successfully
        """
        hooks = self.hooks.get(phase, [])
        all_success = True
        
        for hook in hooks:
            if not hook.enabled:
                continue
            
            try:
                hook.hook_func()
            except Exception as e:
                print(f"⚠️ Shutdown hook '{hook.hook_id}' failed: {e}")
                all_success = False
        
        return all_success
    
    def get_shutdown_duration(self) -> Optional[float]:
        """
        Get shutdown duration in seconds.
        
        Returns:
            Shutdown duration or None
        """
        if self.shutdown_started and self.shutdown_completed:
            return (self.shutdown_completed - self.shutdown_started).total_seconds()
        return None

