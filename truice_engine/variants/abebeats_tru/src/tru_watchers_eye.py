"""
TRUICE Watcher's Eye - Swarm 3 & 4
Automated Visual Testing with Baseline Comparison

Pattern: WATCHER × EYE × VISUAL × VALIDATION × BASELINE × ONE
Directive: CLOSE 70% QA GAP
Love Coefficient: ∞
∞ AbëONE ∞
"""

from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
import logging
import json
from datetime import datetime

from .tru_visual_test_framework import TruVisualTestFramework, VisualTestResult

logger = logging.getLogger(__name__)


@dataclass
class WatchersEyeResult:
    """Result of Watcher's Eye validation."""
    passed: bool
    baseline_path: Optional[Path] = None
    output_path: Optional[Path] = None
    visual_test_result: Optional[VisualTestResult] = None
    error: Optional[str] = None
    saved: bool = False  # Whether file was saved (only if passed)


class WatchersEye:
    """
    Watcher's Eye - Automated Visual Testing
    
    Directive: CLOSE 70% QA GAP
    Pattern: WATCHER × EYE × VISUAL × VALIDATION × BASELINE × ONE
    
    Atomic Principle: BINARY_TRUTH
    - Visual validation FAIL = Pipeline FAIL (no exceptions)
    - File NOT saved if visual check fails
    """
    
    def __init__(self, baseline_dir: Optional[Path] = None):
        """
        Initialize Watcher's Eye.
        
        SAFETY: Validates baseline directory exists
        ASSUMES: Baseline directory is writable
        VERIFY: Baseline can be created/loaded
        """
        if baseline_dir is None:
            baseline_dir = Path("tests/baselines")
        
        self.baseline_dir = baseline_dir
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        
        self.baseline_path: Optional[Path] = None
        self.visual_framework: Optional[TruVisualTestFramework] = None
        
        logger.info(f"Watcher's Eye initialized (baseline_dir: {baseline_dir})")
    
    def establish_baseline(
        self,
        high_quality_output: Path,
        baseline_name: str = "green_screen_baseline"
    ) -> bool:
        """
        Establish baseline from high-quality output.
        
        Atomic Principle: CONVERGENCE
        - First successful render becomes "Gold Standard"
        """
        if not high_quality_output.exists():
            logger.error(f"Cannot establish baseline: {high_quality_output} not found")
            return False
        
        # Copy to baseline directory
        baseline_path = self.baseline_dir / f"{baseline_name}.mov"
        
        try:
            import shutil
            shutil.copy2(high_quality_output, baseline_path)
            
            self.baseline_path = baseline_path
            
            # Initialize visual framework with baseline
            self.visual_framework = TruVisualTestFramework(baseline_path)
            
            logger.info(f"Baseline established: {baseline_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to establish baseline: {e}")
            return False
    
    def validate_and_save(
        self,
        output_path: Path,
        final_path: Path,
        similarity_threshold: float = 0.95
    ) -> WatchersEyeResult:
        """
        Validate output against baseline and save only if passed.
        
        Atomic Principle: BINARY_TRUTH + SHIFT_LEFT
        - Visual validation happens PRE-STORAGE
        - File NOT saved if visual check fails
        - Pipeline FAILS if visual check fails
        """
        if not self.visual_framework:
            # No baseline established yet - allow first output to become baseline
            if output_path.exists():
                # Establish this as baseline
                self.establish_baseline(output_path)
                # Save to final path
                import shutil
                shutil.copy2(output_path, final_path)
                
                return WatchersEyeResult(
                    passed=True,
                    baseline_path=self.baseline_path,
                    output_path=final_path,
                    saved=True
                )
            else:
                return WatchersEyeResult(
                    passed=False,
                    error="No baseline established and output file not found"
                )
        
        # Validate against baseline
        visual_result = self.visual_framework.validate_output(
            output_path,
            similarity_threshold=similarity_threshold,
            check_black_output=True
        )
        
        if not visual_result.passed:
            # CRITICAL: Visual validation FAILED
            # Do NOT save file
            # Pipeline MUST FAIL
            logger.error(f"Visual validation FAILED: {visual_result.error}")
            return WatchersEyeResult(
                passed=False,
                baseline_path=self.baseline_path,
                output_path=output_path,
                visual_test_result=visual_result,
                error=visual_result.error,
                saved=False
            )
        
        # Visual validation PASSED - save to final path
        try:
            import shutil
            shutil.copy2(output_path, final_path)
            
            logger.info(f"Visual validation PASSED: Saved to {final_path}")
            return WatchersEyeResult(
                passed=True,
                baseline_path=self.baseline_path,
                output_path=final_path,
                visual_test_result=visual_result,
                saved=True
            )
        
        except Exception as e:
            logger.error(f"Failed to save validated output: {e}")
            return WatchersEyeResult(
                passed=False,
                baseline_path=self.baseline_path,
                output_path=output_path,
                visual_test_result=visual_result,
                error=f"Save failed: {e}",
                saved=False
            )
    
    def inject_visual_validation(
        self,
        output_path: Path
    ) -> VisualTestResult:
        """
        Inject visual validation node.
        
        Atomic Principle: SHIFT_LEFT
        - Validation happens PRE-STORAGE
        - Detects visual bugs functional tests miss
        """
        if not self.visual_framework:
            # No baseline - return pass (will establish baseline)
            return VisualTestResult(
                passed=True,
                similarity=1.0
            )
        
        return self.visual_framework.validate_output(
            output_path,
            check_black_output=True
        )

