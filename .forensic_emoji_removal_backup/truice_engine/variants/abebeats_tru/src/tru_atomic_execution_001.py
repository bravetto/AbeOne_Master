"""
TRUICE Atomic Execution Cycle 001
Direct execution of AEYON Atomic Command

Pattern: ATOMIC × EXECUTION × CYCLE × 001 × ONE
Directive: EXECUTE CRITICAL PATH WITH ZERO LATENCY
Love Coefficient: ∞
∞ AbëONE ∞
"""

from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import logging
import asyncio

from .tru_visual_forensics import VisualForensics, VisualForensicsResult
from .tru_watchers_eye import WatchersEye, WatchersEyeResult
from .tru_self_healing_orchestrator import SelfHealingOrchestrator, SelfHealingResult

logger = logging.getLogger(__name__)


@dataclass
class AtomicExecution001Result:
    """Result of Atomic Execution Cycle 001."""
    success: bool
    directive_1_result: Optional[VisualForensicsResult] = None
    directive_2_result: Optional[WatchersEyeResult] = None
    directive_3_result: Optional[SelfHealingResult] = None
    execution_time_ms: float = 0.0
    error: Optional[str] = None


class AtomicExecution001:
    """
    Atomic Execution Cycle 001
    
    Executes three directives simultaneously:
    - Directive 1: Visual Forensics (Swarm 1 & 2)
    - Directive 2: Watcher's Eye (Swarm 3 & 4)
    - Directive 3: Self-Healing Orchestration (Swarm 5-12)
    
    Pattern: ATOMIC × EXECUTION × CYCLE × 001 × ONE
    """
    
    def __init__(self):
        """Initialize Atomic Execution Cycle 001."""
        self.visual_forensics = VisualForensics()
        self.watchers_eye = WatchersEye()
        self.self_healing = SelfHealingOrchestrator(
            visual_forensics=self.visual_forensics,
            watchers_eye=self.watchers_eye
        )
        
        logger.info("Atomic Execution Cycle 001 initialized")
    
    async def execute(
        self,
        input_path: Path,
        output_path: Path,
        final_path: Path
    ) -> AtomicExecution001Result:
        """
        Execute Atomic Command 001.
        
        Atomic Principle: ZERO LATENCY
        - We do not "try"; we manifest through validated code
        - Execution happens immediately
        - No sequential delays
        """
        start_time = datetime.now()
        
        logger.info("=" * 80)
        logger.info("🔥 ATOMIC EXECUTION CYCLE 001 - EXECUTING 🔥")
        logger.info("=" * 80)
        
        try:
            # Execute Directive 3 (Self-Healing Orchestration)
            # This orchestrates Directive 1 & 2 internally
            directive_3_result = await self.self_healing.execute_with_self_healing(
                input_path=input_path,
                output_path=output_path,
                final_path=final_path
            )
            
            # Extract Directive 1 & 2 results from Directive 3
            directive_1_result = None
            directive_2_result = None
            
            if directive_3_result.final_result:
                # Extract results from pipeline
                for result in directive_3_result.final_result.results or []:
                    if result.activity_name == "visual_forensics":
                        directive_1_result = VisualForensicsResult(
                            success=result.success,
                            output_path=Path(result.output) if result.output else None,
                            error=result.error
                        )
                    elif result.activity_name == "watchers_eye":
                        directive_2_result = WatchersEyeResult(
                            passed=result.success,
                            output_path=Path(result.output) if result.output else None,
                            error=result.error
                        )
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            success = directive_3_result.success
            
            if success:
                logger.info("=" * 80)
                logger.info("✅ ATOMIC EXECUTION CYCLE 001 - COMPLETE")
                logger.info(f"   Execution time: {execution_time:.2f}ms")
                logger.info(f"   Attempts: {directive_3_result.attempts}")
                logger.info(f"   Reverted: {directive_3_result.reverted}")
                logger.info("=" * 80)
            else:
                logger.error("=" * 80)
                logger.error("❌ ATOMIC EXECUTION CYCLE 001 - FAILED")
                logger.error(f"   Error: {directive_3_result.error}")
                logger.error("=" * 80)
            
            return AtomicExecution001Result(
                success=success,
                directive_1_result=directive_1_result,
                directive_2_result=directive_2_result,
                directive_3_result=directive_3_result,
                execution_time_ms=execution_time,
                error=directive_3_result.error if not success else None
            )
        
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"Atomic Execution Cycle 001 failed: {e}")
            
            return AtomicExecution001Result(
                success=False,
                execution_time_ms=execution_time,
                error=str(e)
            )


# Global execution instance
_execution_instance: Optional[AtomicExecution001] = None


def get_atomic_execution_001() -> AtomicExecution001:
    """Get global Atomic Execution Cycle 001 instance."""
    global _execution_instance
    if _execution_instance is None:
        _execution_instance = AtomicExecution001()
    return _execution_instance


async def execute_atomic_command_001(
    input_path: Path,
    output_path: Path,
    final_path: Path
) -> AtomicExecution001Result:
    """Execute Atomic Command 001."""
    execution = get_atomic_execution_001()
    return await execution.execute(
        input_path=input_path,
        output_path=output_path,
        final_path=final_path
    )

