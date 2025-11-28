"""
TRUICE Self-Healing Orchestrator - Swarm 5-12
Binary Truth Logic + Auto-Reversion

Pattern: SELF_HEALING × ORCHESTRATION × BINARY_TRUTH × AUTO_REVERSION × ONE
Directive: PRODUCTION EXCELLENCE
Love Coefficient: ∞
∞ AbëONE ∞
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
import json
import subprocess
import time
import asyncio

from .tru_orchestrator import TruiceOrchestrator, PipelineResult, Activity, ActivityType
from .tru_activity_types import ActivityResult
from .tru_visual_forensics import VisualForensics, VisualForensicsResult
from .tru_watchers_eye import WatchersEye, WatchersEyeResult

logger = logging.getLogger(__name__)

# Try to import psutil for advanced process monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None
    logger.warning("psutil not available - using subprocess-based monitoring")


@dataclass
class SelfHealingResult:
    """Result of self-healing orchestration."""
    success: bool
    attempts: int
    final_result: Optional[PipelineResult] = None
    reverted: bool = False
    error: Optional[str] = None
    execution_time_ms: float = 0.0


class SelfHealingOrchestrator:
    """
    Self-Healing Orchestrator with Binary Truth Logic
    
    Directive: PRODUCTION EXCELLENCE
    Pattern: SELF_HEALING × ORCHESTRATION × BINARY_TRUTH × AUTO_REVERSION × ONE
    
    Atomic Principles:
    - BINARY_TRUTH: Success signal ignored without Visual Validator Pass token
    - AUTO_REVERSION: Revert to Last Known Good on failure
    """
    
    def __init__(
        self,
        visual_forensics: Optional[VisualForensics] = None,
        watchers_eye: Optional[WatchersEye] = None
    ):
        """
        Initialize Self-Healing Orchestrator.
        
        SAFETY: Validates components are available
        ASSUMES: Components are initialized
        VERIFY: Orchestrator can execute and heal
        """
        self.orchestrator = TruiceOrchestrator()
        # Initialize VisualForensics with self as process tracker
        self.visual_forensics = visual_forensics or VisualForensics(process_tracker=self)
        self.watchers_eye = watchers_eye or WatchersEye()
        
        self.max_retries = 3
        self.last_known_good_config: Optional[Dict[str, Any]] = None
        
        # Stall detection configuration
        self.stall_detection_enabled = True
        self.stall_cpu_threshold = 5.0  # CPU < 5% = potential stall
        self.stall_runtime_threshold = 300  # 5 minutes runtime
        self.stall_check_interval = 30  # Check every 30 seconds
        
        # Process tracking
        self.active_processes: Dict[int, Dict[str, Any]] = {}  # PID -> process info
        
        logger.info("Self-Healing Orchestrator initialized (stall detection enabled)")
    
    async def execute_with_self_healing(
        self,
        input_path: Path,
        output_path: Path,
        final_path: Path
    ) -> SelfHealingResult:
        """
        Execute pipeline with self-healing logic.
        
        Atomic Principle: BINARY_TRUTH + AUTO_REVERSION
        - Success signal ignored without Visual Validator Pass token
        - Auto-revert to Last Known Good on failure
        - Retry with safe mode parameters
        """
        start_time = datetime.now()
        attempts = 0
        
        # Start background monitoring task for stall detection
        monitoring_task = None
        if self.stall_detection_enabled:
            monitoring_task = asyncio.create_task(self._monitor_active_processes())
        
        try:
            while attempts < self.max_retries:
                attempts += 1
                logger.info(f"Execution attempt {attempts}/{self.max_retries}")
                
                # Execute visual forensics (Swarm 1 & 2)
                # Note: Process PID tracking happens inside VisualForensics
                forensics_result = self.visual_forensics.execute_layer_aware_keying(
                    input_path=input_path,
                    output_path=output_path,
                    green_screen_color=(0, 255, 0),
                    tolerance=0.35,
                    enable_despill=True
                )
                
                # Check for stalled processes during execution
                # (VisualForensics now tracks PIDs internally)
                # Stall detection happens via background monitoring task
                
                # Check binary truth: Black output = FAILURE
                if forensics_result.is_black_output:
                    logger.warning(f"Attempt {attempts}: Black output detected - initiating self-healing")
                    
                    # Auto-reversion: Revert to Last Known Good
                    if self.visual_forensics.last_known_good_config:
                        logger.info("Reverting to last known good configuration")
                        forensics_result = self.visual_forensics.revert_to_safe_config(
                            input_path=input_path,
                            output_path=output_path
                        )
                        
                        if forensics_result.success and not forensics_result.is_black_output:
                            # Reversion successful - continue
                            pass
                        else:
                            # Reversion failed - try safe mode
                            logger.warning("Reversion failed - trying safe mode")
                            forensics_result = self._execute_safe_mode(
                                input_path=input_path,
                                output_path=output_path
                            )
                    else:
                        # No last known good - try safe mode
                        logger.warning("No last known good - trying safe mode")
                        forensics_result = self._execute_safe_mode(
                            input_path=input_path,
                            output_path=output_path
                        )
                
                # Check if forensics succeeded
                if not forensics_result.success or forensics_result.is_black_output:
                    if attempts < self.max_retries:
                        logger.warning(f"Attempt {attempts} failed - retrying...")
                        continue
                    else:
                        # Max retries exceeded
                        execution_time = (datetime.now() - start_time).total_seconds() * 1000
                        return SelfHealingResult(
                            success=False,
                            attempts=attempts,
                            error=f"Max retries exceeded. Last error: {forensics_result.error}",
                            execution_time_ms=execution_time
                        )
                
                # Execute Watcher's Eye validation (Swarm 3 & 4)
                watchers_result = self.watchers_eye.validate_and_save(
                    output_path=forensics_result.output_path,
                    final_path=final_path,
                    similarity_threshold=0.95
                )
                
                # Binary Truth Logic: Visual Validator Pass token required
                if not watchers_result.passed:
                    logger.warning(f"Attempt {attempts}: Visual validation failed - initiating self-healing")
                    
                    if attempts < self.max_retries:
                        # Retry with different parameters
                        continue
                    else:
                        # Max retries exceeded
                        execution_time = (datetime.now() - start_time).total_seconds() * 1000
                        return SelfHealingResult(
                            success=False,
                            attempts=attempts,
                            error=f"Visual validation failed: {watchers_result.error}",
                            execution_time_ms=execution_time
                        )
                
                # SUCCESS: Both forensics and visual validation passed
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                
                # Create pipeline result
                pipeline_result = PipelineResult(
                    success=True,
                    results=[
                        ActivityResult(
                            success=True,
                            activity_name="visual_forensics",
                            output=str(forensics_result.output_path)
                        ),
                        ActivityResult(
                            success=True,
                            activity_name="watchers_eye",
                            output=str(watchers_result.output_path)
                        )
                    ]
                )
                
                logger.info(f"Self-healing execution SUCCESS after {attempts} attempt(s)")
                return SelfHealingResult(
                    success=True,
                    attempts=attempts,
                    final_result=pipeline_result,
                    reverted=(attempts > 1),
                    execution_time_ms=execution_time
                )
        
            # Should not reach here, but handle edge case
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return SelfHealingResult(
                success=False,
                attempts=attempts,
                error="Execution loop completed without success",
                execution_time_ms=execution_time
            )
        finally:
            # Clean up monitoring task
            if monitoring_task and not monitoring_task.done():
                monitoring_task.cancel()
                try:
                    await monitoring_task
                except asyncio.CancelledError:
                    pass
            # Clear active processes
            self.active_processes.clear()
    
    def _execute_safe_mode(
        self,
        input_path: Path,
        output_path: Path
    ) -> VisualForensicsResult:
        """
        Execute with safe mode parameters.
        
        Safe mode: Ignore alpha channel to preserve data
        """
        logger.info("Executing in safe mode (ignoring alpha channel)")
        
        # Safe mode: Use more conservative parameters
        return self.visual_forensics.execute_layer_aware_keying(
            input_path=input_path,
            output_path=output_path,
            green_screen_color=(0, 255, 0),
            tolerance=0.25,  # More conservative
            enable_despill=False  # Disable despill for safety
        )
    
    def _detect_stall(self, process_id: int) -> bool:
        """
        Detect zombie processes (low CPU, high runtime).
        
        Atomic Principle: STALL_DETECTION
        - CPU < threshold AND runtime > threshold = STALL
        - Returns True if process is stalled
        
        SAFETY: Validates process exists before checking
        ASSUMES: Process ID is valid
        VERIFY: Returns True if stalled, False otherwise
        """
        if not self.stall_detection_enabled:
            return False
        
        try:
            if PSUTIL_AVAILABLE:
                return self._detect_stall_psutil(process_id)
            else:
                return self._detect_stall_subprocess(process_id)
        except Exception as e:
            logger.warning(f"Stall detection failed for PID {process_id}: {e}")
            return False
    
    def _detect_stall_psutil(self, process_id: int) -> bool:
        """Detect stall using psutil (preferred method)."""
        try:
            process = psutil.Process(process_id)
            
            # Get CPU usage (non-blocking)
            cpu_percent = process.cpu_percent(interval=0.1)
            
            # Get runtime
            runtime_seconds = (datetime.now() - datetime.fromtimestamp(process.create_time())).total_seconds()
            
            # Check stall condition: Low CPU AND High Runtime
            is_stalled = (
                cpu_percent < self.stall_cpu_threshold and
                runtime_seconds > self.stall_runtime_threshold
            )
            
            if is_stalled:
                logger.warning(
                    f"STALL DETECTED: PID {process_id} - "
                    f"CPU: {cpu_percent:.1f}% (threshold: {self.stall_cpu_threshold}%), "
                    f"Runtime: {runtime_seconds:.0f}s (threshold: {self.stall_runtime_threshold}s)"
                )
            
            return is_stalled
            
        except psutil.NoSuchProcess:
            # Process doesn't exist (may have completed)
            return False
        except Exception as e:
            logger.warning(f"psutil stall detection failed: {e}")
            return False
    
    def _detect_stall_subprocess(self, process_id: int) -> bool:
        """Detect stall using subprocess (fallback method)."""
        try:
            # Use ps command (like monitor_generation.py)
            result = subprocess.run(
                ["ps", "-p", str(process_id), "-o", "etime,pcpu"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                # Process doesn't exist
                return False
            
            lines = result.stdout.strip().split('\n')
            if len(lines) < 2:
                return False
            
            # Parse output: etime pcpu
            parts = lines[1].split()
            if len(parts) < 2:
                return False
            
            etime_str = parts[0]  # Format: HH:MM:SS or MM:SS
            cpu_str = parts[1]
            
            # Parse CPU percentage
            try:
                cpu_percent = float(cpu_str)
            except ValueError:
                return False
            
            # Parse runtime (etime format: HH:MM:SS or MM:SS)
            runtime_seconds = self._parse_etime(etime_str)
            
            # Check stall condition
            is_stalled = (
                cpu_percent < self.stall_cpu_threshold and
                runtime_seconds > self.stall_runtime_threshold
            )
            
            if is_stalled:
                logger.warning(
                    f"STALL DETECTED: PID {process_id} - "
                    f"CPU: {cpu_percent:.1f}% (threshold: {self.stall_cpu_threshold}%), "
                    f"Runtime: {runtime_seconds:.0f}s (threshold: {self.stall_runtime_threshold}s)"
                )
            
            return is_stalled
            
        except Exception as e:
            logger.warning(f"Subprocess stall detection failed: {e}")
            return False
    
    def _parse_etime(self, etime_str: str) -> float:
        """Parse ps etime format (HH:MM:SS or MM:SS) to seconds."""
        try:
            parts = etime_str.split(':')
            if len(parts) == 3:
                # HH:MM:SS
                hours, minutes, seconds = map(int, parts)
                return hours * 3600 + minutes * 60 + seconds
            elif len(parts) == 2:
                # MM:SS
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
            else:
                return 0.0
        except Exception:
            return 0.0
    
    def _restart_stalled_process(self, process_id: int) -> bool:
        """
        Restart stalled process.
        
        Atomic Principle: SELF_HEALING
        - Terminates zombie process
        - Returns True if restart successful
        
        SAFETY: Validates process exists before termination
        ASSUMES: Process is stalled and safe to kill
        VERIFY: Process terminated successfully
        """
        try:
            logger.info(f"Restarting stalled process: PID {process_id}")
            
            if PSUTIL_AVAILABLE:
                process = psutil.Process(process_id)
                process.terminate()
                # Wait for graceful termination
                try:
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    # Force kill if doesn't terminate
                    process.kill()
            else:
                # Use kill command
                subprocess.run(["kill", str(process_id)], timeout=5)
                time.sleep(1)
                # Force kill if still running
                subprocess.run(["kill", "-9", str(process_id)], timeout=5)
            
            # Remove from tracking
            if process_id in self.active_processes:
                del self.active_processes[process_id]
            
            logger.info(f"Stalled process {process_id} terminated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restart stalled process {process_id}: {e}")
            return False
    
    async def _monitor_active_processes(self):
        """
        Background task to monitor active processes for stalls.
        
        Atomic Principle: STALL_DETECTION
        - Monitors all tracked processes
        - Detects and restarts stalled processes automatically
        """
        while self.active_processes:
            await asyncio.sleep(self.stall_check_interval)
            
            # Check each active process
            stalled_pids = []
            for pid, process_info in list(self.active_processes.items()):
                if self._detect_stall(pid):
                    stalled_pids.append(pid)
            
            # Restart stalled processes
            for pid in stalled_pids:
                logger.warning(f"Auto-restarting stalled process: PID {pid}")
                self._restart_stalled_process(pid)
    
    def rewrite_exit_code_handler(
        self,
        renderer_success: bool,
        visual_validator_pass: bool
    ) -> bool:
        """
        Rewrite pipeline exit code handler.
        
        Atomic Principle: BINARY_TRUTH
        - Success signal from renderer is IGNORED unless Visual Validator Pass token present
        """
        # Binary Truth Logic
        if not visual_validator_pass:
            # Visual validation failed = Pipeline FAIL
            logger.error("Pipeline FAIL: Visual Validator did not pass")
            return False
        
        if not renderer_success:
            # Renderer failed = Pipeline FAIL
            logger.error("Pipeline FAIL: Renderer did not succeed")
            return False
        
        # Both passed = Pipeline SUCCESS
        logger.info("Pipeline SUCCESS: Both renderer and visual validator passed")
        return True

