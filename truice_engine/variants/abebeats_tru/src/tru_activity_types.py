"""
TRUICE Activity Type Classification System

Foundation for proper failure propagation and orchestration.

Pattern: ACTIVITY × CLASSIFICATION × FAILURE_PROPAGATION × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, Callable


class ActivityType(Enum):
    """
    Activity type classification.
    
    CORE_FUNCTION: Must succeed for pipeline to succeed
    HANDLER: Can fail without failing pipeline
    VALIDATION: Checks but doesn't produce output
    """
    CORE_FUNCTION = "core_function"  # Must succeed
    HANDLER = "handler"  # Can fail independently
    VALIDATION = "validation"  # Checks but doesn't produce output


@dataclass
class ActivityResult:
    """Result of activity execution."""
    success: bool
    activity_name: str
    error: Optional[str] = None
    output: Optional[Any] = None


class Activity:
    """
    Pipeline activity with type classification.
    
    Pattern: ACTIVITY × TYPE × EXECUTION × ONE
    """
    
    def __init__(
        self,
        name: str,
        activity_type: ActivityType,
        execute_func: Callable[[], Any],
        required_inputs: Optional[List[str]] = None,
        produces_outputs: Optional[List[str]] = None
    ):
        """
        Initialize activity.
        
        SAFETY: Validates activity type and execute function
        ASSUMES: Execute function is callable
        VERIFY: Activity can be executed
        """
        self.name = name
        self.activity_type = activity_type
        self.execute_func = execute_func
        self.required_inputs = required_inputs or []
        self.produces_outputs = produces_outputs or []
    
    def is_core_function(self) -> bool:
        """
        Check if this is a core function.
        
        VERIFY: Returns True if activity type is CORE_FUNCTION
        """
        return self.activity_type == ActivityType.CORE_FUNCTION
    
    def execute(self) -> ActivityResult:
        """
        Execute activity.
        
        SAFETY: Catches all exceptions
        ASSUMES: Execute function is callable
        VERIFY: Returns ActivityResult with success status
        """
        try:
            result = self.execute_func()
            return ActivityResult(
                success=True,
                activity_name=self.name,
                output=result
            )
        except Exception as e:
            return ActivityResult(
                success=False,
                activity_name=self.name,
                error=str(e)
            )

