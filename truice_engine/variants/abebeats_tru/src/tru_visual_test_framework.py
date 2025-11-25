"""
TRUICE Visual Test Framework

MVP Visual Test Framework for validating video outputs.

Pattern: VISUAL_TEST × BASELINE × COMPARISON × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Try to import OpenCV
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None
    np = None
    logger.warning("OpenCV not available - visual testing will be limited")


@dataclass
class VisualTestResult:
    """Result of visual test comparison."""
    passed: bool
    similarity: float
    error: Optional[str] = None
    frame_differences: Optional[List[dict]] = None


class TruVisualTestFramework:
    """
    MVP Visual Test Framework for TRUICE video outputs.
    
    Pattern: VISUAL_TEST × BASELINE × COMPARISON × ONE
    """
    
    def __init__(self, baseline_path: Optional[Path] = None):
        """
        Initialize with optional baseline.
        
        SAFETY: Validates baseline exists if provided
        ASSUMES: Baseline is correct output
        VERIFY: Baseline is valid video file if provided
        """
        if not CV2_AVAILABLE:
            raise RuntimeError("OpenCV required for visual testing")
        
        self.baseline_path = baseline_path
        self.baseline_frames = None
        
        if baseline_path and baseline_path.exists():
            self.baseline_frames = self._load_baseline_frames()
            logger.info(f"Loaded baseline: {len(self.baseline_frames)} frames")
    
    def _load_baseline_frames(self) -> List:
        """Load baseline video frames."""
        if not CV2_AVAILABLE:
            return []
        
        cap = cv2.VideoCapture(str(self.baseline_path))
        frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        return frames
    
    def validate_output(
        self,
        output_path: Path,
        similarity_threshold: float = 0.95,
        check_black_output: bool = True
    ) -> VisualTestResult:
        """
        Validate output video.
        
        SAFETY: Validates output exists before validation
        ASSUMES: Output is valid video file
        VERIFY: Output is not black and matches baseline if provided
        """
        if not CV2_AVAILABLE:
            return VisualTestResult(
                passed=False,
                similarity=0.0,
                error="OpenCV not available"
            )
        
        if not output_path.exists():
            return VisualTestResult(
                passed=False,
                similarity=0.0,
                error=f"Output file not found: {output_path}"
            )
        
        # Check for black output (critical failure)
        if check_black_output:
            is_black = self._check_black_output(output_path)
            if is_black:
                return VisualTestResult(
                    passed=False,
                    similarity=0.0,
                    error="Output is black (critical failure)"
                )
        
        # Compare against baseline if available
        if self.baseline_frames:
            return self._compare_against_baseline(output_path, similarity_threshold)
        
        # If no baseline, just check that output is valid (not black)
        return VisualTestResult(
            passed=True,
            similarity=1.0
        )
    
    def _check_black_output(self, output_path: Path) -> bool:
        """
        Check if output is all black.
        
        VERIFY: Returns True if output is black (critical failure)
        """
        cap = cv2.VideoCapture(str(output_path))
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return True  # Can't read = failure
        
        # Check if frame is all black (or nearly all black)
        non_black_pixels = np.sum(np.any(frame > 10, axis=2))
        total_pixels = frame.shape[0] * frame.shape[1]
        non_black_percentage = (non_black_pixels / total_pixels) * 100
        
        # If less than 1% non-black, consider it black output
        return non_black_percentage < 1.0
    
    def _compare_against_baseline(
        self,
        output_path: Path,
        similarity_threshold: float
    ) -> VisualTestResult:
        """Compare output against baseline."""
        # Load output frames
        cap = cv2.VideoCapture(str(output_path))
        output_frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            output_frames.append(frame)
        
        cap.release()
        
        # Compare frame counts
        if len(output_frames) != len(self.baseline_frames):
            return VisualTestResult(
                passed=False,
                similarity=0.0,
                error=f"Frame count mismatch: {len(output_frames)} vs {len(self.baseline_frames)}"
            )
        
        # Frame-by-frame comparison
        similarities = []
        frame_differences = []
        
        for i, (baseline_frame, output_frame) in enumerate(
            zip(self.baseline_frames, output_frames)
        ):
            similarity = self._compare_frames(baseline_frame, output_frame)
            similarities.append(similarity)
            
            if similarity < similarity_threshold:
                frame_differences.append({
                    'frame': i,
                    'similarity': similarity
                })
        
        avg_similarity = np.mean(similarities)
        
        if avg_similarity >= similarity_threshold:
            return VisualTestResult(
                passed=True,
                similarity=avg_similarity,
                frame_differences=None
            )
        else:
            return VisualTestResult(
                passed=False,
                similarity=avg_similarity,
                error=f"Output differs from baseline (similarity: {avg_similarity:.2f})",
                frame_differences=frame_differences
            )
    
    def _compare_frames(
        self,
        baseline: np.ndarray,
        output: np.ndarray
    ) -> float:
        """
        Compare two frames using simple difference.
        
        VERIFY: Returns similarity score 0.0-1.0
        """
        # Resize if dimensions differ
        if baseline.shape != output.shape:
            output = cv2.resize(output, (baseline.shape[1], baseline.shape[0]))
        
        # Convert to grayscale for comparison
        if len(baseline.shape) == 3:
            baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
        else:
            baseline_gray = baseline
        
        if len(output.shape) == 3:
            output_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        else:
            output_gray = output
        
        # Calculate simple difference
        diff = np.abs(baseline_gray.astype(float) - output_gray.astype(float))
        similarity = 1.0 - (np.mean(diff) / 255.0)
        
        return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]

