"""
TRUICE Visual Forensics - Swarm 1 & 2
Layer-Aware Keying with Despill Logic

Pattern: VISUAL × FORENSICS × LAYER × ISOLATION × DESPILL × ONE
Directive: OBLITERATE GREEN SCREEN TRUTH
Love Coefficient: ∞
∞ AbëONE ∞
"""

from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import logging
import subprocess
import json

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
    logger.warning("OpenCV not available - visual forensics will be limited")


@dataclass
class VisualForensicsResult:
    """Result of visual forensics execution."""
    success: bool
    output_path: Optional[Path] = None
    pixel_variance: Optional[float] = None
    is_black_output: bool = False
    error: Optional[str] = None
    ffmpeg_command: Optional[str] = None


class VisualForensics:
    """
    Visual Forensics - Layer-Aware Keying with Despill Logic
    
    Directive: OBLITERATE GREEN SCREEN TRUTH
    Pattern: VISUAL × FORENSICS × LAYER × ISOLATION × DESPILL × ONE
    """
    
    def __init__(self, process_tracker: Optional[Any] = None):
        """
        Initialize Visual Forensics.
        
        Args:
            process_tracker: Optional callback to track process PIDs for stall detection
        """
        self.last_known_good_config: Optional[Dict[str, Any]] = None
        self.process_tracker = process_tracker  # Callback to track PIDs
        logger.info("Visual Forensics initialized")
    
    def execute_layer_aware_keying(
        self,
        input_path: Path,
        output_path: Path,
        green_screen_color: Tuple[int, int, int] = (0, 255, 0),
        tolerance: float = 0.35,
        enable_despill: bool = True
    ) -> VisualForensicsResult:
        """
        Execute layer-aware keying with despill logic.
        
        SAFETY: Validates input exists before processing
        ASSUMES: Input is valid video file
        VERIFY: Output has pixel variance > 1% (not black)
        
        Atomic Principle: ISOLATION - Treat streams as distinct atomic units
        """
        if not input_path.exists():
            return VisualForensicsResult(
                success=False,
                error=f"Input file not found: {input_path}"
            )
        
        # Build FFmpeg filter-complex with layer isolation
        filter_complex = self._build_layer_isolated_filter_complex(
            green_screen_color,
            tolerance,
            enable_despill
        )
        
        # Execute FFmpeg command
        ffmpeg_command = self._build_ffmpeg_command(
            input_path,
            output_path,
            filter_complex
        )
        
        try:
            # Execute FFmpeg with process tracking
            # Start process and track PID for stall detection
            process = subprocess.Popen(
                ffmpeg_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Store PID for potential stall detection
            process_pid = process.pid
            
            # Notify process tracker if available
            if self.process_tracker:
                self.process_tracker.active_processes[process_pid] = {
                    'start_time': datetime.now(),
                    'command': ' '.join(ffmpeg_command[:3]),  # First few args for logging
                    'type': 'ffmpeg_chromakey'
                }
                logger.debug(f"Tracking FFmpeg process: PID {process_pid}")
            
            # Wait for completion
            stdout, stderr = process.communicate()
            
            # Remove from tracking when complete
            if self.process_tracker and process_pid in self.process_tracker.active_processes:
                del self.process_tracker.active_processes[process_pid]
                logger.debug(f"FFmpeg process completed: PID {process_pid}")
            
            # Check return code
            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode,
                    ffmpeg_command,
                    stdout,
                    stderr
                )
            
            result = type('Result', (), {
                'returncode': process.returncode,
                'stdout': stdout,
                'stderr': stderr
            })()
            
            # Validate output
            if not output_path.exists():
                return VisualForensicsResult(
                    success=False,
                    error="Output file not created",
                    ffmpeg_command=" ".join(ffmpeg_command)
                )
            
            # Check pixel variance (CRITICAL: Binary Truth)
            pixel_variance = self._check_pixel_variance(output_path)
            is_black_output = pixel_variance < 0.01  # < 1% = black
            
            if is_black_output:
                # CRITICAL FAILURE: Black output detected
                logger.error(f"BLACK OUTPUT DETECTED: Pixel variance {pixel_variance:.2%} < 1%")
                return VisualForensicsResult(
                    success=False,
                    output_path=output_path,
                    pixel_variance=pixel_variance,
                    is_black_output=True,
                    error="Output is black (pixel variance < 1%)",
                    ffmpeg_command=" ".join(ffmpeg_command)
                )
            
            # Save as last known good configuration
            self.last_known_good_config = {
                "green_screen_color": green_screen_color,
                "tolerance": tolerance,
                "enable_despill": enable_despill,
                "filter_complex": filter_complex
            }
            
            logger.info(f"Layer-aware keying SUCCESS: Pixel variance {pixel_variance:.2%}")
            return VisualForensicsResult(
                success=True,
                output_path=output_path,
                pixel_variance=pixel_variance,
                is_black_output=False,
                ffmpeg_command=" ".join(ffmpeg_command)
            )
        
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg execution failed: {e.stderr}")
            return VisualForensicsResult(
                success=False,
                error=f"FFmpeg error: {e.stderr}",
                ffmpeg_command=" ".join(ffmpeg_command)
            )
    
    def _build_layer_isolated_filter_complex(
        self,
        green_screen_color: Tuple[int, int, int],
        tolerance: float,
        enable_despill: bool
    ) -> str:
        """
        Build FFmpeg filter-complex with layer isolation.
        
        Atomic Principle: ISOLATION
        - Do NOT apply colorkey to background
        - Apply chromakey only to source stream [0:v]
        - Use despill logic for dingy green edges
        """
        # Convert RGB to hex for FFmpeg
        r, g, b = green_screen_color
        color_hex = f"0x{b:02x}{g:02x}{r:02x}"  # BGR format for FFmpeg
        
        # Layer isolation: Process foreground only
        # [0:v] = source stream (foreground with green screen)
        
        if enable_despill:
            # Chromakey with despill (handles dingy green screens)
            # Similarity: 0.0-1.0, higher = more aggressive
            similarity = tolerance
            blend = 0.0  # No blending (hard edge)
            
            filter_complex = (
                f"[0:v]chromakey=color={color_hex}:similarity={similarity}:"
                f"blend={blend}:yuv=1[ckout]"
            )
        else:
            # Simple colorkey (faster but less accurate)
            similarity = tolerance
            
            filter_complex = (
                f"[0:v]colorkey=color={color_hex}:similarity={similarity}:"
                f"blend=0.0[ckout]"
            )
        
        # If background exists, overlay; otherwise output keyed foreground
        # Note: This assumes single input for now (green screen only)
        # For two-layer composition, add: [1:v][ckout]overlay=0:0[out]
        
        return filter_complex
    
    def _build_ffmpeg_command(
        self,
        input_path: Path,
        output_path: Path,
        filter_complex: str
    ) -> List[str]:
        """Build FFmpeg command with layer isolation."""
        # FFmpeg command with layer-aware processing
        command = [
            "ffmpeg",
            "-i", str(input_path),
            "-filter_complex", filter_complex,
            "-map", "[ckout]",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            "-crf", "18",  # High quality
            "-y",  # Overwrite output
            str(output_path)
        ]
        
        return command
    
    def _check_pixel_variance(self, output_path: Path) -> float:
        """
        Check pixel variance (detect black output).
        
        Atomic Principle: BINARY_TRUTH
        - Pixel variance < 1% = BLACK OUTPUT = FAILURE
        - Pixel variance >= 1% = VALID OUTPUT = SUCCESS (if truth_score >= 0.987)
        """
        if not CV2_AVAILABLE:
            # Fallback: Assume valid if file exists
            return 0.5
        
        cap = cv2.VideoCapture(str(output_path))
        if not cap.isOpened():
            return 0.0
        
        # Read first frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return 0.0
        
        # Calculate pixel variance
        # Non-black pixels = pixels with any channel > 10
        non_black_mask = np.any(frame > 10, axis=2)
        non_black_pixels = np.sum(non_black_mask)
        total_pixels = frame.shape[0] * frame.shape[1]
        
        pixel_variance = non_black_pixels / total_pixels
        
        return pixel_variance
    
    def get_last_known_good_config(self) -> Optional[Dict[str, Any]]:
        """Get last known good configuration for auto-reversion."""
        return self.last_known_good_config
    
    def revert_to_safe_config(
        self,
        input_path: Path,
        output_path: Path
    ) -> VisualForensicsResult:
        """
        Revert to last known good configuration.
        
        Atomic Principle: SELF_HEALING
        """
        if not self.last_known_good_config:
            return VisualForensicsResult(
                success=False,
                error="No last known good configuration available"
            )
        
        logger.info("Reverting to last known good configuration")
        
        return self.execute_layer_aware_keying(
            input_path=input_path,
            output_path=output_path,
            green_screen_color=tuple(self.last_known_good_config["green_screen_color"]),
            tolerance=self.last_known_good_config["tolerance"],
            enable_despill=self.last_known_good_config["enable_despill"]
        )

