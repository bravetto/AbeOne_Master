"""
Pipeline Engine - Safe Pipeline Execution

Executes pipelines only when explicitly triggered by human operator.

Pattern: PIPELINE × ENGINE × EXECUTION × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import threading
from pathlib import Path


class PipelineStatus(Enum):
    """Pipeline execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(Enum):
    """Pipeline step execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PipelineStep:
    """Pipeline step definition."""
    step_id: str
    module_id: str
    action: str
    params: Dict[str, Any] = field(default_factory=dict)
    on_success: Optional[str] = None
    on_error: Optional[str] = None
    timeout: Optional[int] = None
    retry: Optional[int] = None


@dataclass
class Pipeline:
    """Pipeline definition."""
    pipeline_id: str
    version: str
    steps: List[PipelineStep] = field(default_factory=list)
    triggers: Dict[str, Any] = field(default_factory=dict)
    error_handler: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class StepExecutionResult:
    """Pipeline step execution result."""
    step_id: str
    status: StepStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class PipelineExecution:
    """Pipeline execution instance."""
    execution_id: str
    pipeline_id: str
    status: PipelineStatus
    params: Dict[str, Any] = field(default_factory=dict)
    step_results: List[StepExecutionResult] = field(default_factory=list)
    current_step: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class PipelineEngine:
    """
    Pipeline Engine.
    
    Responsibilities:
    - Pipeline registration and management
    - Pipeline execution (human-triggered only)
    - Step execution and error handling
    - Pipeline state management
    """
    
    def __init__(self):
        """Initialize pipeline engine."""
        self.pipelines: Dict[str, Pipeline] = {}
        self.executions: Dict[str, PipelineExecution] = {}
        self.module_registry: Optional[Callable] = None
        self.event_bus: Optional[Callable] = None
        
        # Thread safety
        self._lock = threading.Lock()
    
    def register_module_registry(self, registry: Callable) -> None:
        """Register module registry hook."""
        with self._lock:
            self.module_registry = registry
    
    def register_event_bus(self, bus: Callable) -> None:
        """Register event bus hook."""
        with self._lock:
            self.event_bus = bus
    
    def register_pipeline(self, pipeline: Pipeline) -> bool:
        """
        Register a new pipeline.
        
        Args:
            pipeline: Pipeline definition
        
        Returns:
            True if registration successful
        """
        with self._lock:
            if pipeline.pipeline_id in self.pipelines:
                return False  # Already registered
            
            # Validate pipeline
            if not self._validate_pipeline(pipeline):
                return False
            
            self.pipelines[pipeline.pipeline_id] = pipeline
            return True
    
    def _validate_pipeline(self, pipeline: Pipeline) -> bool:
        """
        Validate pipeline definition.
        
        Args:
            pipeline: Pipeline definition
        
        Returns:
            True if valid
        """
        if not pipeline.pipeline_id:
            print("❌ Pipeline validation error: pipeline_id is required")
            return False
        
        if not pipeline.steps:
            print("❌ Pipeline validation error: pipeline must have at least one step")
            return False
        
        # Validate steps
        step_ids = set()
        for step in pipeline.steps:
            if not step.step_id:
                print(f"❌ Pipeline validation error: step_id is required for step")
                return False
            
            if step.step_id in step_ids:
                print(f"❌ Pipeline validation error: duplicate step_id: {step.step_id}")
                return False
            
            step_ids.add(step.step_id)
            
            if not step.module_id:
                print(f"❌ Pipeline validation error: module_id is required for step {step.step_id}")
                return False
            
            if not step.action:
                print(f"❌ Pipeline validation error: action is required for step {step.step_id}")
                return False
            
            # Validate on_success/on_error references
            if step.on_success and step.on_success not in step_ids and step.on_success != "complete":
                print(f"⚠️ Pipeline validation warning: on_success '{step.on_success}' not found for step {step.step_id}")
            
            if step.on_error and step.on_error not in step_ids and step.on_error != "error_handler":
                print(f"⚠️ Pipeline validation warning: on_error '{step.on_error}' not found for step {step.step_id}")
        
        return True
    
    def get_pipeline(self, pipeline_id: str) -> Optional[Pipeline]:
        """
        Get pipeline by ID.
        
        Args:
            pipeline_id: Pipeline identifier
        
        Returns:
            Pipeline definition or None
        """
        with self._lock:
            return self.pipelines.get(pipeline_id)
    
    def execute_pipeline(self, pipeline_id: str, params: Dict[str, Any], 
                        execution_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute pipeline with given parameters.
        
        **IMPORTANT**: This method only executes when explicitly called by human operator.
        No autonomous execution is performed.
        
        Args:
            pipeline_id: Pipeline identifier
            params: Pipeline parameters
            execution_id: Optional execution ID (auto-generated if not provided)
        
        Returns:
            Execution result dictionary
        """
        # Get pipeline
        pipeline = self.get_pipeline(pipeline_id)
        if not pipeline:
            return {
                "status": "error",
                "error": f"Pipeline '{pipeline_id}' not found"
            }
        
        # Check if pipeline allows manual execution
        if not pipeline.triggers.get("manual", False):
            return {
                "status": "error",
                "error": f"Pipeline '{pipeline_id}' does not allow manual execution"
            }
        
        # Create execution instance
        exec_id = execution_id or f"{pipeline_id}_{datetime.now().isoformat()}"
        execution = PipelineExecution(
            execution_id=exec_id,
            pipeline_id=pipeline_id,
            status=PipelineStatus.RUNNING,
            params=params,
            started_at=datetime.now()
        )
        
        with self._lock:
            self.executions[exec_id] = execution
        
        try:
            # Execute pipeline steps
            result = self._execute_steps(pipeline, execution, params)
            
            # Update execution status
            execution.status = PipelineStatus.COMPLETED
            execution.completed_at = datetime.now()
            
            return {
                "status": "success",
                "execution_id": exec_id,
                "result": result,
                "step_results": [
                    {
                        "step_id": sr.step_id,
                        "status": sr.status.value,
                        "result": sr.result,
                        "error": sr.error,
                        "execution_time": sr.execution_time
                    }
                    for sr in execution.step_results
                ]
            }
            
        except Exception as e:
            # Update execution status
            execution.status = PipelineStatus.FAILED
            execution.error = str(e)
            execution.completed_at = datetime.now()
            
            return {
                "status": "error",
                "execution_id": exec_id,
                "error": str(e),
                "step_results": [
                    {
                        "step_id": sr.step_id,
                        "status": sr.status.value,
                        "result": sr.result,
                        "error": sr.error
                    }
                    for sr in execution.step_results
                ]
            }
    
    def _execute_steps(self, pipeline: Pipeline, execution: PipelineExecution, 
                      params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute pipeline steps.
        
        Args:
            pipeline: Pipeline definition
            execution: Execution instance
            params: Pipeline parameters
        
        Returns:
            Final result dictionary
        """
        step_results: Dict[str, Any] = {}
        current_step_id = pipeline.steps[0].step_id if pipeline.steps else None
        
        while current_step_id:
            # Find step
            step = next((s for s in pipeline.steps if s.step_id == current_step_id), None)
            if not step:
                break
            
            # Execute step
            execution.current_step = current_step_id
            step_result = self._execute_step(step, params, step_results)
            execution.step_results.append(step_result)
            
            # Store result
            step_results[step.step_id] = step_result.result
            
            # Determine next step
            if step_result.status == StepStatus.COMPLETED:
                # Success - go to on_success handler
                if step.on_success:
                    if step.on_success == "complete":
                        break
                    current_step_id = step.on_success
                else:
                    # No on_success - move to next step
                    current_index = next((i for i, s in enumerate(pipeline.steps) 
                                         if s.step_id == current_step_id), -1)
                    if current_index >= 0 and current_index < len(pipeline.steps) - 1:
                        current_step_id = pipeline.steps[current_index + 1].step_id
                    else:
                        break
            elif step_result.status == StepStatus.FAILED:
                # Failure - go to on_error handler
                if step.on_error:
                    if step.on_error == "error_handler":
                        # Use pipeline error handler
                        if pipeline.error_handler:
                            current_step_id = pipeline.error_handler
                        else:
                            break
                    else:
                        current_step_id = step.on_error
                else:
                    # No on_error - fail pipeline
                    raise Exception(f"Step '{step.step_id}' failed: {step_result.error}")
            else:
                # Unexpected status
                break
        
        return step_results
    
    def _execute_step(self, step: PipelineStep, params: Dict[str, Any], 
                     step_results: Dict[str, Any]) -> StepExecutionResult:
        """
        Execute a single pipeline step.
        
        Args:
            step: Step definition
            params: Pipeline parameters
            step_results: Previous step results
        
        Returns:
            Step execution result
        """
        start_time = datetime.now()
        
        try:
            # Resolve step parameters (support ${param} and ${step_id.result} syntax)
            resolved_params = self._resolve_params(step.params, params, step_results)
            
            # Get module from registry
            if not self.module_registry:
                raise Exception("Module registry not registered")
            
            module = self.module_registry.get(step.module_id)
            if not module:
                raise Exception(f"Module '{step.module_id}' not found")
            
            # Create event for module
            if not self.event_bus:
                raise Exception("Event bus not registered")
            
            event = self.event_bus.create_event(
                event_type=self.event_bus.EventType.MODULE_EVENT,
                source="pipeline_engine",
                target=step.module_id,
                data={
                    "name": step.action,
                    "params": resolved_params
                }
            )
            
            # Send event to module
            result = self.module_registry.send_event(step.module_id, event)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return StepExecutionResult(
                step_id=step.step_id,
                status=StepStatus.COMPLETED,
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return StepExecutionResult(
                step_id=step.step_id,
                status=StepStatus.FAILED,
                error=str(e),
                execution_time=execution_time
            )
    
    def _resolve_params(self, step_params: Dict[str, Any], pipeline_params: Dict[str, Any],
                       step_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve step parameters (support ${param} and ${step_id.result} syntax).
        
        Args:
            step_params: Step parameters
            pipeline_params: Pipeline parameters
            step_results: Previous step results
        
        Returns:
            Resolved parameters
        """
        resolved = {}
        
        for key, value in step_params.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                # Resolve parameter reference
                ref = value[2:-1]
                
                if "." in ref:
                    # Step result reference: ${step_id.result}
                    step_id, result_key = ref.split(".", 1)
                    if step_id in step_results:
                        step_result = step_results[step_id]
                        if isinstance(step_result, dict) and result_key in step_result:
                            resolved[key] = step_result[result_key]
                        else:
                            resolved[key] = step_result
                    else:
                        resolved[key] = value  # Keep unresolved
                else:
                    # Pipeline parameter reference: ${param}
                    if ref in pipeline_params:
                        resolved[key] = pipeline_params[ref]
                    else:
                        resolved[key] = value  # Keep unresolved
            elif isinstance(value, dict):
                # Recursively resolve nested dictionaries
                resolved[key] = self._resolve_params(value, pipeline_params, step_results)
            elif isinstance(value, list):
                # Resolve list items
                resolved[key] = [
                    self._resolve_params({"_": item}, pipeline_params, step_results)["_"]
                    if isinstance(item, (str, dict))
                    else item
                    for item in value
                ]
            else:
                resolved[key] = value
        
        return resolved
    
    def get_execution(self, execution_id: str) -> Optional[PipelineExecution]:
        """
        Get execution by ID.
        
        Args:
            execution_id: Execution identifier
        
        Returns:
            Execution instance or None
        """
        with self._lock:
            return self.executions.get(execution_id)
    
    def get_all_pipelines(self) -> List[str]:
        """
        Get list of all pipeline IDs.
        
        Returns:
            List of pipeline IDs
        """
        with self._lock:
            return list(self.pipelines.keys())


# Global pipeline engine instance
_pipeline_engine_instance: Optional[PipelineEngine] = None


def get_pipeline_engine() -> PipelineEngine:
    """Get global pipeline engine instance."""
    global _pipeline_engine_instance
    if _pipeline_engine_instance is None:
        _pipeline_engine_instance = PipelineEngine()
    return _pipeline_engine_instance

