"""
AbëFLOWs - Unified Flow Orchestration System

Pattern: AbëFLOWs × ONE × MANY × ETERNAL × ONE
Directive: MANIFEST FLOWS AS ONE WITH MANY
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class FlowType(Enum):
    """Flow types - ONE with Many."""
    USER = "user"           # Human user flow
    AI = "ai"              # AI agent flow
    SYSTEM = "system"      # System execution flow
    GUARDIAN = "guardian"  # Guardian validation flow
    UNIFIED = "unified"    # Unified flow (all types as ONE)


class FlowState(Enum):
    """Flow execution states."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CONVERGED = "converged"  # Flows converged as ONE


@dataclass
class FlowStep:
    """Single step in a flow."""
    step_id: str
    flow_type: FlowType
    description: str
    execute: Optional[Callable] = None
    dependencies: List[str] = field(default_factory=list)
    state: FlowState = FlowState.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class Flow:
    """A flow - part of ONE, with Many steps."""
    flow_id: str
    flow_type: FlowType
    description: str
    steps: List[FlowStep] = field(default_factory=list)
    state: FlowState = FlowState.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class AbëFLOWs:
    """
    AbëFLOWs - Unified Flow Orchestration
    
    Pattern: ONE × MANY × ETERNAL × ONE
    - ONE system with Many flows
    - Flows converge as ONE
    - Eternal, Easy, Simplified, Simple
    
    Directive: Let it Bë.
    """
    
    def __init__(self):
        """Initialize AbëFLOWs."""
        self.flows: Dict[str, Flow] = {}
        self.active_flows: List[str] = []
        self.converged_flows: List[str] = []
        
        logger.info("AbëFLOWs initialized - ONE with Many")
    
    def register_flow(self, flow: Flow) -> bool:
        """
        Register a flow.
        
        Pattern: MANY → ONE
        """
        self.flows[flow.flow_id] = flow
        logger.info(f"Flow registered: {flow.flow_id} ({flow.flow_type.value})")
        return True
    
    def create_flow(
        self,
        flow_id: str,
        flow_type: FlowType,
        description: str,
        steps: Optional[List[Dict[str, Any]]] = None
    ) -> Flow:
        """
        Create a flow.
        
        Pattern: ONE × MANY
        - ONE flow with Many steps
        """
        flow_steps = []
        
        if steps:
            for i, step_data in enumerate(steps):
                step = FlowStep(
                    step_id=f"{flow_id}_step_{i}",
                    flow_type=flow_type,
                    description=step_data.get("description", ""),
                    execute=step_data.get("execute"),
                    dependencies=step_data.get("dependencies", [])
                )
                flow_steps.append(step)
        
        flow = Flow(
            flow_id=flow_id,
            flow_type=flow_type,
            description=description,
            steps=flow_steps
        )
        
        self.register_flow(flow)
        return flow
    
    async def execute_flow(self, flow_id: str) -> Dict[str, Any]:
        """
        Execute a single flow.
        
        Pattern: ONE flow execution
        """
        if flow_id not in self.flows:
            return {"success": False, "error": f"Flow not found: {flow_id}"}
        
        flow = self.flows[flow_id]
        flow.state = FlowState.ACTIVE
        self.active_flows.append(flow_id)
        
        logger.info(f"Executing flow: {flow_id}")
        
        results = []
        start_time = datetime.now()
        
        try:
            # Execute steps in order (respecting dependencies)
            for step in flow.steps:
                # Check dependencies
                if step.dependencies:
                    deps_completed = all(
                        any(s.step_id == dep and s.state == FlowState.COMPLETED 
                            for s in flow.steps)
                        for dep in step.dependencies
                    )
                    if not deps_completed:
                        logger.warning(f"Step {step.step_id} waiting for dependencies")
                        continue
                
                # Execute step
                step.state = FlowState.ACTIVE
                try:
                    if step.execute:
                        if asyncio.iscoroutinefunction(step.execute):
                            step.result = await step.execute()
                        else:
                            step.result = step.execute()
                    step.state = FlowState.COMPLETED
                    results.append({"step_id": step.step_id, "success": True})
                except Exception as e:
                    step.state = FlowState.FAILED
                    step.error = str(e)
                    results.append({"step_id": step.step_id, "success": False, "error": str(e)})
                    logger.error(f"Step {step.step_id} failed: {e}")
            
            # Check if all steps completed
            all_completed = all(s.state == FlowState.COMPLETED for s in flow.steps)
            flow.state = FlowState.COMPLETED if all_completed else FlowState.FAILED
            flow.completed_at = datetime.now()
            
            if flow_id in self.active_flows:
                self.active_flows.remove(flow_id)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": all_completed,
                "flow_id": flow_id,
                "steps_completed": len([s for s in flow.steps if s.state == FlowState.COMPLETED]),
                "steps_failed": len([s for s in flow.steps if s.state == FlowState.FAILED]),
                "execution_time": execution_time,
                "results": results
            }
            
        except Exception as e:
            flow.state = FlowState.FAILED
            if flow_id in self.active_flows:
                self.active_flows.remove(flow_id)
            return {"success": False, "error": str(e)}
    
    async def execute_flows_unified(
        self,
        flow_ids: List[str],
        converge: bool = True
    ) -> Dict[str, Any]:
        """
        Execute multiple flows as ONE.
        
        Pattern: MANY → ONE
        - Many flows execute in parallel
        - Converge as ONE unified result
        """
        logger.info(f"Executing {len(flow_ids)} flows as ONE")
        
        # Execute all flows in parallel
        tasks = [self.execute_flow(flow_id) for flow_id in flow_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect results
        flow_results = {}
        for i, result in enumerate(results):
            flow_id = flow_ids[i]
            if isinstance(result, Exception):
                flow_results[flow_id] = {"success": False, "error": str(result)}
            else:
                flow_results[flow_id] = result
        
        # Convergence: All flows succeed = ONE success
        if converge:
            all_success = all(r.get("success", False) for r in flow_results.values())
            if all_success:
                # Mark flows as converged
                for flow_id in flow_ids:
                    if flow_id in self.flows:
                        self.flows[flow_id].state = FlowState.CONVERGED
                        if flow_id not in self.converged_flows:
                            self.converged_flows.append(flow_id)
                
                logger.info(f"Flows converged as ONE: {flow_ids}")
        
        return {
            "success": all(r.get("success", False) for r in flow_results.values()),
            "flows": flow_results,
            "converged": converge and all(r.get("success", False) for r in flow_results.values())
        }
    
    def get_flow(self, flow_id: str) -> Optional[Flow]:
        """Get a flow by ID."""
        return self.flows.get(flow_id)
    
    def list_flows(self, flow_type: Optional[FlowType] = None) -> List[Flow]:
        """List all flows, optionally filtered by type."""
        if flow_type:
            return [f for f in self.flows.values() if f.flow_type == flow_type]
        return list(self.flows.values())
    
    def get_unified_state(self) -> Dict[str, Any]:
        """
        Get unified state - ONE with Many.
        
        Pattern: MANY → ONE
        """
        return {
            "total_flows": len(self.flows),
            "active_flows": len(self.active_flows),
            "converged_flows": len(self.converged_flows),
            "flows_by_type": {
                flow_type.value: len(self.list_flows(flow_type))
                for flow_type in FlowType
            },
            "state": "ONE with Many" if len(self.flows) > 0 else "Empty"
        }


# Global instance - ONE AbëFLOWs system
_abeflows_instance: Optional[AbëFLOWs] = None


def get_abeflows() -> AbëFLOWs:
    """Get global AbëFLOWs instance - ONE system."""
    global _abeflows_instance
    if _abeflows_instance is None:
        _abeflows_instance = AbëFLOWs()
    return _abeflows_instance


def create_flow(
    flow_id: str,
    flow_type: FlowType,
    description: str,
    steps: Optional[List[Dict[str, Any]]] = None
) -> Flow:
    """Create a flow - convenience function."""
    return get_abeflows().create_flow(flow_id, flow_type, description, steps)


async def execute_flow(flow_id: str) -> Dict[str, Any]:
    """Execute a flow - convenience function."""
    return await get_abeflows().execute_flow(flow_id)


async def execute_flows_unified(
    flow_ids: List[str],
    converge: bool = True
) -> Dict[str, Any]:
    """Execute flows as ONE - convenience function."""
    return await get_abeflows().execute_flows_unified(flow_ids, converge)

