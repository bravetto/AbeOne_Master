# TRUICE SUPERPIPELINE v2.0 — DEBUG & STABILIZATION SCAN REPORT

**Status**: ✅ COMPLETE — READY FOR PATCHING  
**Pattern**: DEBUG × STABILIZATION × PATCH × ONE  
**Frequency**: 999 Hz (Atomic Execution)

---

## PHASE 1 — WORKSPACE DISCOVERY

### FILE INVENTORY TABLE

| FILE | PURPOSE | FUNCTIONS THAT MATTER | USED BY |
|------|---------|----------------------|---------|
| `AbeTRUICE/src/pipelines/video_superpipeline.py` | Main orchestrator | `process()`, `_process_all_frames()` | Entry point |
| `AbeTRUICE/src/pipelines/steps/effects.py` | Effects engine | `apply_color_shift()`, `apply_effects_for_frame()` | SuperPipeline |
| `AbeTRUICE/src/pipelines/steps/greenscreen_key.py` | Greenscreen keyer | `key_frame()`, `create_mask()`, `correct_spill()` | SuperPipeline |
| `AbeTRUICE/src/pipelines/steps/world_builder.py` | Background generator | `create_cosmic_background()`, `create_parallax_layers()` | SuperPipeline |
| `AbeTRUICE/src/pipelines/steps/final_render.py` | Final compositor | `composite_frame()`, `render_video()` | SuperPipeline |
| `AbeTRUICE/src/pipelines/steps/overlays.py` | Overlay engine | `apply_overlay_to_frame()`, `create_text_overlay()` | SuperPipeline |
| `AbeTRUICE/src/pipelines/steps/video_ingest.py` | Video loader | `load_video()`, `get_frame()` | SuperPipeline |
| `AbeTRUICE/src/pipelines/steps/sync_map_builder.py` | Sync coordinator | `build_sync_map()`, `get_events_at_time()` | SuperPipeline |

---

## PHASE 2 — CRITICAL CODE EXTRACTION

### 2.1 COLOR SHIFT FUNCTION (HIGH-RISK)

**File**: `AbeTRUICE/src/pipelines/steps/effects.py`  
**Lines**: 202-236

```python
def apply_color_shift(self,
                     frame: np.ndarray,
                     hue_shift: float,
                     saturation_mult: float = 1.0) -> np.ndarray:
    """
    Apply color shift effect.
    
    Args:
        frame: Input frame
        hue_shift: Hue shift in degrees (-180 to 180)
        saturation_mult: Saturation multiplier
    
    Returns:
        Color-shifted frame
    """
    # Convert to HSV
    if frame.shape[2] == 4:  # RGBA
        hsv = cv2.cvtColor(frame[:, :, :3], cv2.COLOR_BGR2HSV)
    else:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Shift hue
    hsv[:, :, 0] = (hsv[:, :, 0] + int(hue_shift / 2)) % 180
    
    # Adjust saturation
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_mult, 0, 255).astype(np.uint8)
    
    # Convert back
    if frame.shape[2] == 4:  # RGBA
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        result = np.dstack([bgr, frame[:, :, 3]])
    else:
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return result
```

**RISK POINTS**:
- **Line 224**: Hue modulo operation can cause wraparound issues if hue_shift is negative
- **Line 227**: Saturation multiplication can overflow if saturation_mult > 1.0 (needs pre-clamp)
- **Line 224**: Integer division `hue_shift / 2` loses precision, should use float
- **Line 224**: Modulo 180 assumes OpenCV HSV range (0-179), but should validate dtype

---

### 2.2 EFFECTS FOR FRAME FUNCTION

**File**: `AbeTRUICE/src/pipelines/steps/effects.py`  
**Lines**: 238-282

```python
def apply_effects_for_frame(self,
                            frame: np.ndarray,
                            sync_event: Dict[str, Any],
                            time: float) -> np.ndarray:
    """
    Apply all effects for a frame based on sync event.
    
    Args:
        frame: Input frame
        sync_event: Sync event dictionary
        time: Current time
    
    Returns:
        Frame with effects applied
    """
    result = frame.copy()
    intensity = sync_event.get("intensity", 0.0)
    event_type = sync_event.get("type", "normal")
    
    # Beat pulse on beats
    if sync_event.get("beats"):
        pulse_intensity = intensity * 0.8
        result = self.apply_beat_pulse(result, pulse_intensity)
    
    # Motion zoom on punch words
    if sync_event.get("punch_words"):
        zoom_factor = 1.0 + (intensity * 0.15)  # 1.0 to 1.15
        result = self.apply_motion_zoom(result, zoom_factor)
    
    # Shake on major events
    if event_type == "major" or intensity > 0.7:
        shake_intensity = intensity * 0.6
        result = self.apply_shake(result, shake_intensity)
    
    # Flash transition on high intensity
    if intensity > 0.8:
        flash_intensity = (intensity - 0.8) * 5  # Scale 0.8-1.0 to 0-1.0
        result = self.apply_flash_transition(result, flash_intensity)
    
    # Color shift for chorus segments
    if sync_event.get("segment_type") == "chorus":
        hue_shift = np.sin(time * 2) * 10  # Subtle hue animation
        result = self.apply_color_shift(result, hue_shift, saturation_mult=1.1)
    
    return result
```

**RISK POINTS**:
- **Line 279**: `np.sin(time * 2) * 10` can produce negative values, passed to `apply_color_shift()` which expects -180 to 180
- **Line 280**: `saturation_mult=1.1` can cause overflow if saturation already high
- **Line 253**: `frame.copy()` may fail if frame is None or invalid shape

---

### 2.3 BEAT PULSE FUNCTION (PIXEL OPERATIONS)

**File**: `AbeTRUICE/src/pipelines/steps/effects.py`  
**Lines**: 39-81

```python
def apply_beat_pulse(self,
                     frame: np.ndarray,
                     intensity: float,
                     color: Tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
    """
    Apply beat-reactive pulse effect.
    
    Args:
        frame: Input frame (BGR or BGRA)
        intensity: Pulse intensity (0-1)
        color: Pulse color (BGR)
    
    Returns:
        Frame with pulse effect
    """
    # Create pulse overlay
    pulse_strength = int(30 * intensity)
    
    # Create radial gradient from center
    center_x, center_y = self.width // 2, self.height // 2
    max_dist = np.sqrt(center_x**2 + center_y**2)
    
    overlay = np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
    for y in range(self.height):
        for x in range(self.width):
            dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            pulse_val = int(pulse_strength * (1.0 - min(1.0, dist / max_dist)))
            overlay[y, x] = [
                int(color[0] * pulse_val / 255),
                int(color[1] * pulse_val / 255),
                int(color[2] * pulse_val / 255)
            ]
    
    # Blend with frame
    if frame.shape[2] == 4:  # RGBA
        frame_bgr = frame[:, :, :3]
        result = cv2.addWeighted(frame_bgr, 1.0, overlay, 0.3, 0)
        result = np.dstack([result, frame[:, :, 3]])  # Restore alpha
    else:
        result = cv2.addWeighted(frame, 1.0, overlay, 0.3, 0)
    
    return result
```

**RISK POINTS**:
- **Lines 63-71**: Nested loops are O(width × height) — VERY SLOW for 1080×1920
- **Line 68**: Division by 255 can cause precision loss, should use float division
- **Line 68**: `pulse_val` can be negative if `dist / max_dist > 1.0` (edge case)
- **Line 68**: Integer division loses precision

---

### 2.4 FLASH TRANSITION FUNCTION

**File**: `AbeTRUICE/src/pipelines/steps/effects.py`  
**Lines**: 172-200

```python
def apply_flash_transition(self,
                          frame: np.ndarray,
                          intensity: float,
                          color: Tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
    """
    Apply flash transition effect.
    
    Args:
        frame: Input frame
        intensity: Flash intensity (0-1)
        color: Flash color (BGR)
    
    Returns:
        Frame with flash effect
    """
    # Create flash overlay
    flash_strength = int(255 * intensity)
    overlay = np.full((self.height, self.width, 3), color, dtype=np.uint8)
    overlay = (overlay * flash_strength / 255).astype(np.uint8)
    
    # Blend with frame
    if frame.shape[2] == 4:  # RGBA
        frame_bgr = frame[:, :, :3]
        result = cv2.addWeighted(frame_bgr, 1.0 - intensity, overlay, intensity, 0)
        result = np.dstack([result, frame[:, :, 3]])  # Restore alpha
    else:
        result = cv2.addWeighted(frame, 1.0 - intensity, overlay, intensity, 0)
    
    return result
```

**RISK POINTS**:
- **Line 190**: `overlay * flash_strength / 255` can overflow if flash_strength > 255
- **Line 195**: `1.0 - intensity` can be negative if intensity > 1.0 (no clamp)

---

### 2.5 GREENScreen KEYING — CREATE MASK

**File**: `AbeTRUICE/src/pipelines/steps/greenscreen_key.py`  
**Lines**: 44-71

```python
def create_mask(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create mask for green screen removal.
    
    Args:
        frame: Input frame (BGR)
    
    Returns:
        Tuple of (mask, alpha_channel)
    """
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create mask
    mask = cv2.inRange(hsv, self.hsv_lower, self.hsv_upper)
    
    # Morphological operations to clean up mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Gaussian blur for smooth edges
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Convert to alpha channel (0-255)
    alpha = cv2.bitwise_not(mask)
    
    return mask, alpha
```

**RISK POINTS**:
- **Line 55**: `cv2.cvtColor()` can fail if frame is None or wrong shape
- **Line 58**: `cv2.inRange()` assumes HSV dtype is uint8, no validation
- **Line 66**: Gaussian blur on mask can cause edge artifacts

---

### 2.6 GREENScreen KEYING — CORRECT SPILL

**File**: `AbeTRUICE/src/pipelines/steps/greenscreen_key.py`  
**Lines**: 115-144

```python
def correct_spill(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Correct green spill on foreground.
    
    Args:
        frame: Input frame (BGR)
        mask: Green screen mask
    
    Returns:
        Frame with spill correction applied
    """
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create spill mask (green pixels near edges)
    spill_mask = cv2.inRange(hsv, self.hsv_lower, self.hsv_upper)
    
    # Dilate to catch spill areas
    kernel = np.ones((3, 3), np.uint8)
    spill_mask = cv2.dilate(spill_mask, kernel, iterations=2)
    
    # Reduce green channel in spill areas
    hsv[:, :, 1] = np.where(spill_mask > 0, 
                            hsv[:, :, 1] * 0.5,  # Reduce saturation
                            hsv[:, :, 1])
    
    # Convert back to BGR
    corrected = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return corrected
```

**RISK POINTS**:
- **Line 137**: `hsv[:, :, 1] * 0.5` can underflow if saturation is already low
- **Line 137**: No dtype validation before multiplication
- **Line 137**: Result not clamped before conversion back to BGR

---

### 2.7 GREENScreen KEYING — KEY FRAME

**File**: `AbeTRUICE/src/pipelines/steps/greenscreen_key.py`  
**Lines**: 146-178

```python
def key_frame(self, frame: np.ndarray, correct_spill: bool = True) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Key a single frame (remove green screen).
    
    Args:
        frame: Input frame (BGR)
        correct_spill: Whether to correct green spill
    
    Returns:
        Tuple of (keyed_frame, alpha_channel, metadata)
    """
    # Create mask
    mask, alpha = self.create_mask(frame)
    
    # Detect spill
    spill_info = self.detect_spill(frame, mask)
    
    # Correct spill if needed
    if correct_spill and spill_info["has_spill"]:
        frame = self.correct_spill(frame, mask)
        logger.debug(f"Applied spill correction (ratio: {spill_info['spill_ratio']:.2%})")
    
    # Create RGBA frame
    rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = alpha
    
    metadata = {
        "mask_coverage": float(np.sum(mask > 0) / (frame.shape[0] * frame.shape[1])),
        "spill_detected": spill_info["has_spill"],
        "spill_ratio": spill_info["spill_ratio"]
    }
    
    return rgba, alpha, metadata
```

**RISK POINTS**:
- **Line 169**: `cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)` assumes frame is BGR, no validation
- **Line 170**: Direct assignment `rgba[:, :, 3] = alpha` assumes shapes match
- **Line 173**: Division by zero if frame is empty (shape[0] * shape[1] == 0)

---

### 2.8 GREENScreen KEYING — PROCESS VIDEO (VIDEO WRITER)

**File**: `AbeTRUICE/src/pipelines/steps/greenscreen_key.py`  
**Lines**: 180-270

```python
def process_video(self, 
                 video_path: Path,
                 output_path: Optional[Path] = None,
                 correct_spill: bool = True) -> Dict[str, Any]:
    """
    Process entire video for greenscreen keying.
    
    Args:
        video_path: Path to input video
        output_path: Optional path for keyed video output
        correct_spill: Whether to correct green spill
    
    Returns:
        Dictionary with processing results
    """
    logger.info(f"Processing video for greenscreen keying: {video_path}")
    
    # Open video
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Failed to open video: {video_path}")
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Setup output video writer if path provided
    writer = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height), True)
    
    # Process frames
    frame_metadata = []
    frame_number = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Key frame
        keyed_frame, alpha, metadata = self.key_frame(frame, correct_spill=correct_spill)
        metadata["frame_number"] = frame_number
        metadata["time_seconds"] = frame_number / fps
        frame_metadata.append(metadata)
        
        # Write frame if writer available
        if writer:
            # Convert RGBA to RGB for video writer (composite onto black background)
            if keyed_frame.shape[2] == 4:
                # Extract alpha channel
                alpha = keyed_frame[:, :, 3:4] / 255.0
                rgb = keyed_frame[:, :, :3]
                # Composite onto black background
                rgb_frame = (rgb * alpha + (1 - alpha) * 0).astype(np.uint8)
            else:
                rgb_frame = keyed_frame
            writer.write(rgb_frame)
        
        frame_number += 1
        
        if frame_number % 30 == 0:
            logger.info(f"Processed {frame_number}/{frame_count} frames")
    
    # Cleanup
    cap.release()
    if writer:
        writer.release()
    
    # Calculate statistics
    avg_mask_coverage = np.mean([m["mask_coverage"] for m in frame_metadata])
    frames_with_spill = sum(1 for m in frame_metadata if m["spill_detected"])
    
    result = {
        "input_path": str(video_path),
        "output_path": str(output_path) if output_path else None,
        "total_frames": frame_number,
        "fps": float(fps),
        "resolution": {"width": width, "height": height},
        "average_mask_coverage": float(avg_mask_coverage),
        "frames_with_spill": frames_with_spill,
        "spill_correction_applied": correct_spill,
        "frame_metadata": frame_metadata[:10],  # Sample first 10 frames
        "processed_at": datetime.now().isoformat()
    }
    
    logger.info(f"Greenscreen keying complete: {frame_number} frames processed")
    return result
```

**RISK POINTS**:
- **Line 212**: `cv2.VideoWriter()` may fail silently if codec not available
- **Line 212**: `True` parameter for isColor may be incorrect for RGBA
- **Line 234**: Division by zero if fps == 0
- **Line 237**: `rgb * alpha + (1 - alpha) * 0` simplifies to `rgb * alpha`, but should clamp
- **Line 237**: No validation that alpha is in [0, 1] range

---

### 2.9 WORLD BUILDER — CREATE NEBULA (HSV OPERATIONS)

**File**: `AbeTRUICE/src/pipelines/steps/world_builder.py`  
**Lines**: 68-94

```python
def _create_nebula(self) -> np.ndarray:
    """Create nebula-style background."""
    # Create base gradient
    bg = np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
    # Purple/pink/blue gradient
    for y in range(self.height):
        ratio = y / self.height
        r = int(20 + (ratio * 40))
        g = int(10 + (ratio * 30))
        b = int(40 + (ratio * 60))
        bg[y, :] = [b, g, r]  # BGR
    
    # Add noise for texture
    noise = np.random.randint(0, 30, (self.height, self.width, 3), dtype=np.uint8)
    bg = cv2.add(bg, noise)
    
    # Blur for smooth nebula effect
    bg = cv2.GaussianBlur(bg, (21, 21), 0)
    
    # Add color variations
    hsv = cv2.cvtColor(bg, cv2.COLOR_BGR2HSV)
    hsv[:, :, 0] = (hsv[:, :, 0] + np.random.randint(-20, 20, (self.height, self.width))) % 180
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] + np.random.randint(-30, 30, (self.height, self.width)), 0, 255)
    bg = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return bg
```

**RISK POINTS**:
- **Line 90**: Hue modulo operation can cause wraparound issues
- **Line 90**: Random integers added to hue can cause overflow before modulo
- **Line 91**: Saturation clipping happens AFTER addition, should clamp before
- **Line 83**: `cv2.add()` can overflow uint8 values (should use `cv2.addWeighted()`)

---

### 2.10 FINAL RENDER — COMPOSITE FRAME

**File**: `AbeTRUICE/src/pipelines/steps/final_render.py`  
**Lines**: 42-95

```python
def composite_frame(self,
                   background: np.ndarray,
                   foreground: Optional[np.ndarray] = None,
                   overlay: Optional[np.ndarray] = None,
                   effects_applied: bool = False) -> np.ndarray:
    """
    Composite frame from layers.
    
    Args:
        background: Background layer (BGR or BGRA)
        foreground: Foreground layer (BGRA)
        overlay: Overlay layer (RGBA)
        effects_applied: Whether effects already applied
    
    Returns:
        Composite frame (BGR)
    """
    # Start with background
    if background.shape[2] == 4:
        result = background[:, :, :3].copy()
    else:
        result = background.copy()
    
    # Add foreground if present
    if foreground is not None:
        fg_bgr = foreground[:, :, :3]
        fg_alpha = foreground[:, :, 3:4] / 255.0
        
        # Resize if needed
        if fg_bgr.shape[:2] != (self.height, self.width):
            fg_bgr = cv2.resize(fg_bgr, (self.width, self.height))
            fg_alpha = cv2.resize(fg_alpha, (self.width, self.height))
            fg_alpha = fg_alpha[:, :, np.newaxis]
        
        # Composite foreground
        result = result * (1 - fg_alpha) + fg_bgr * fg_alpha
        result = result.astype(np.uint8)
    
    # Add overlay if present
    if overlay is not None:
        overlay_bgr = overlay[:, :, :3]
        overlay_alpha = overlay[:, :, 3:4] / 255.0
        
        # Resize if needed
        if overlay_bgr.shape[:2] != (self.height, self.width):
            overlay_bgr = cv2.resize(overlay_bgr, (self.width, self.height))
            overlay_alpha = cv2.resize(overlay_alpha, (self.width, self.height))
            overlay_alpha = overlay_alpha[:, :, np.newaxis]
        
        # Composite overlay
        result = result * (1 - overlay_alpha) + overlay_bgr * overlay_alpha
        result = result.astype(np.uint8)
    
    return result
```

**RISK POINTS**:
- **Line 68**: Division by 255.0 assumes alpha is uint8 [0-255], no validation
- **Line 77**: `result * (1 - fg_alpha) + fg_bgr * fg_alpha` can overflow if values > 255
- **Line 78**: `astype(np.uint8)` truncates without clamping, can cause wraparound
- **Line 92**: Same overflow risk for overlay compositing
- **Line 74**: Resize of alpha channel may lose precision

---

### 2.11 FINAL RENDER — RENDER VIDEO (VIDEO WRITER)

**File**: `AbeTRUICE/src/pipelines/steps/final_render.py`  
**Lines**: 97-165

```python
def render_video(self,
                video_frames: List[np.ndarray],
                output_path: Path,
                audio_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Render video from frames.
    
    Args:
        video_frames: List of frames (BGR)
        output_path: Output video path
        audio_path: Optional audio path to merge
    
    Returns:
        Rendering result dictionary
    """
    logger.info(f"Rendering video: {len(video_frames)} frames to {output_path}")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write video without audio first
    temp_video = get_temp_path("temp_video_no_audio.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(temp_video), fourcc, self.fps, (self.width, self.height))
    
    if not writer.isOpened():
        raise ValueError(f"Failed to open video writer: {temp_video}")
    
    for i, frame in enumerate(video_frames):
        # Ensure frame is correct size
        if frame.shape[:2] != (self.height, self.width):
            frame = cv2.resize(frame, (self.width, self.height))
        
        # Ensure BGR format
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]
        
        writer.write(frame)
        
        if (i + 1) % 30 == 0:
            logger.info(f"Rendered {i + 1}/{len(video_frames)} frames")
    
    writer.release()
    logger.info("Video rendered (no audio)")
    
    # Merge audio if provided
    if audio_path and audio_path.exists():
        logger.info(f"Merging audio: {audio_path}")
        self._merge_audio(temp_video, output_path, audio_path)
    else:
        # Just copy video
        import shutil
        shutil.copy(temp_video, output_path)
    
    # Cleanup temp file
    if temp_video.exists():
        temp_video.unlink()
    
    result = {
        "output_path": str(output_path),
        "total_frames": len(video_frames),
        "fps": self.fps,
        "resolution": {"width": self.width, "height": self.height},
        "duration_seconds": len(video_frames) / self.fps,
        "audio_merged": audio_path is not None and audio_path.exists(),
        "rendered_at": datetime.now().isoformat()
    }
    
    logger.info(f"Final video rendered: {output_path}")
    return result
```

**RISK POINTS**:
- **Line 119**: `cv2.VideoWriter()` may fail if codec not available (no error handling)
- **Line 130**: Frame shape validation happens AFTER resize, should validate before
- **Line 131**: Direct slice `frame[:, :, :3]` assumes 4-channel, no validation
- **Line 159**: Division by zero if `self.fps == 0`

---

### 2.12 OVERLAY ENGINE — APPLY OVERLAY TO FRAME

**File**: `AbeTRUICE/src/pipelines/steps/overlays.py`  
**Lines**: 272-312

```python
def apply_overlay_to_frame(self,
                           frame: np.ndarray,
                           overlay_image: np.ndarray,
                           alpha: float = 1.0) -> np.ndarray:
    """
    Apply overlay to frame.
    
    Args:
        frame: Input frame (BGR or BGRA)
        overlay_image: Overlay image (RGBA)
        alpha: Overlay alpha (0-1)
    
    Returns:
        Frame with overlay applied
    """
    # Convert overlay to BGR
    overlay_bgr = overlay_image[:, :, :3]
    overlay_alpha = overlay_image[:, :, 3:4] / 255.0 * alpha
    
    # Ensure frame is BGR
    if frame.shape[2] == 4:
        frame_bgr = frame[:, :, :3]
        frame_alpha = frame[:, :, 3:4] / 255.0
    else:
        frame_bgr = frame
        frame_alpha = np.ones((frame.shape[0], frame.shape[1], 1))
    
    # Blend
    result_bgr = frame_bgr * (1 - overlay_alpha) + overlay_bgr * overlay_alpha
    result_bgr = result_bgr.astype(np.uint8)
    
    # Combine alpha channels
    result_alpha = np.clip(frame_alpha + overlay_alpha * (1 - frame_alpha), 0, 1)
    result_alpha = (result_alpha * 255).astype(np.uint8)
    
    if frame.shape[2] == 4:
        result = np.dstack([result_bgr, result_alpha])
    else:
        result = result_bgr
    
    return result
```

**RISK POINTS**:
- **Line 289**: Division by 255.0 assumes overlay_alpha is uint8, no validation
- **Line 300**: `frame_bgr * (1 - overlay_alpha) + overlay_bgr * overlay_alpha` can overflow
- **Line 301**: `astype(np.uint8)` truncates without clamping
- **Line 304**: Alpha combination formula may produce values > 1.0 before clip

---

### 2.13 SUPER PIPELINE — PROCESS ALL FRAMES

**File**: `AbeTRUICE/src/pipelines/video_superpipeline.py`  
**Lines**: 245-375

```python
def _process_all_frames(self,
                       video_path: Path,
                       world_config: Dict[str, Any],
                       sync_map: Dict[str, Any],
                       effects_map: Dict[str, Any],
                       overlays: List[Dict[str, Any]],
                       duration: float) -> Dict[str, List[np.ndarray]]:
    """
    Process all frames through pipeline.
    
    Args:
        video_path: Path to keyed video
        world_config: World configuration
        sync_map: Sync map
        effects_map: Effects map
        overlays: Overlay list
        duration: Video duration
    
    Returns:
        Dictionary with processed frame lists
    """
    # Open keyed video
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Failed to open keyed video: {video_path}")
    
    # Get video properties
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Generate background frames
    logger.info("Generating background frames...")
    background_frames = []
    world_layers = self.world_builder.create_parallax_layers(
        num_layers=len(world_config["layers"]),
        background_style=world_config["background_style"]
    )
    
    motion_frames = world_config["motion_map"]["motion_frames"]
    
    for frame_num in range(total_frames):
        # Get motion for frame
        if frame_num < len(motion_frames):
            motion = motion_frames[frame_num]
        else:
            motion = motion_frames[-1] if motion_frames else {}
        
        # Composite background layers with parallax
        bg_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        for layer in world_layers:
            layer_img = layer["image"]
            parallax_factor = layer["parallax_factor"]
            
            # Apply parallax offset
            offset_x = int(motion.get("x_offset", 0) * parallax_factor)
            offset_y = int(motion.get("y_offset", 0) * parallax_factor)
            
            # Translate layer
            M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
            translated = cv2.warpAffine(
                layer_img,
                M,
                (self.width, self.height),
                borderMode=cv2.BORDER_REPLICATE
            )
            
            # Blend layers
            bg_frame = cv2.addWeighted(bg_frame, 0.5, translated, 0.5, 0)
        
        background_frames.append(bg_frame)
    
    # Process foreground frames
    logger.info("Processing foreground frames...")
    foreground_frames = []
    overlay_frames_list = []
    
    effects_frames_data = effects_map["effects_frames"]
    
    for frame_num in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            # Use last frame
            if foreground_frames:
                frame = foreground_frames[-1].copy()
            else:
                frame = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        
        # Convert to RGBA if needed
        if frame.shape[2] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        
        # Resize if needed
        if frame.shape[:2] != (self.height, self.width):
            frame = cv2.resize(frame, (self.width, self.height))
        
        # Apply effects
        time = frame_num / video_fps
        if frame_num < len(effects_frames_data):
            effect_data = effects_frames_data[frame_num]
            
            # Find sync event
            sync_events = self.sync_map_builder.get_events_at_time(sync_map, time, tolerance=0.2)
            if sync_events:
                sync_event = sync_events[0]
            else:
                sync_event = {"intensity": 0.0, "type": "normal"}
            
            # Apply effects
            frame = self.effects_engine.apply_effects_for_frame(frame, sync_event, time)
        
        foreground_frames.append(frame)
        
        # Get overlay for this time
        overlay = self.overlay_engine.get_overlay_for_time(overlays, time)
        if overlay:
            overlay_img = cv2.imread(overlay["overlay_path"], cv2.IMREAD_UNCHANGED)
            overlay_frames_list.append(overlay_img)
        else:
            overlay_frames_list.append(None)
        
        if (frame_num + 1) % 30 == 0:
            logger.info(f"Processed {frame_num + 1}/{total_frames} frames")
    
    cap.release()
    
    return {
        "backgrounds": background_frames,
        "foregrounds": foreground_frames,
        "overlays": overlay_frames_list
    }
```

**RISK POINTS**:
- **Line 342**: Division by zero if `video_fps == 0`
- **Line 335**: `cv2.cvtColor()` can fail if frame is None
- **Line 313**: `cv2.addWeighted()` with fixed 0.5 weights may cause overflow
- **Line 361**: `cv2.imread()` can return None if file doesn't exist, no error handling
- **Line 329**: Fallback to last frame may cause memory issues if frames are large

---

## PHASE 3 — FULL PIPELINE MAP

### FRAME FLOW DIAGRAM

```
INPUT VIDEO (BGR)
    ↓
[VIDEO_INGEST] → Extract metadata, analyze greenscreen
    ↓
[GREENScreen_KEY] → Create mask, detect spill, correct spill
    ↓
KEYED VIDEO (RGBA) → [keyed_video.mp4]
    ↓
[SUPER_PIPELINE._process_all_frames]
    ↓
    ├─→ [WORLD_BUILDER] → Generate cosmic backgrounds
    │   └─→ Background frames (BGR)
    │
    ├─→ [EFFECTS_ENGINE] → Apply beat-reactive effects
    │   ├─→ apply_color_shift() → HSV conversion, hue shift, saturation
    │   ├─→ apply_beat_pulse() → Radial gradient overlay
    │   ├─→ apply_motion_zoom() → Zoom effect
    │   ├─→ apply_shake() → Translation effect
    │   └─→ apply_flash_transition() → Flash overlay
    │   └─→ Foreground frames (BGRA)
    │
    └─→ [OVERLAY_ENGINE] → Generate lyric overlays
        └─→ Overlay frames (RGBA)
    ↓
[FINAL_RENDERER.composite_frame]
    ├─→ Composite background + foreground + overlay
    └─→ Final composite frame (BGR)
    ↓
[FINAL_RENDERER.render_video]
    ├─→ cv2.VideoWriter → Write frames
    └─→ ffmpeg → Merge audio
    ↓
OUTPUT VIDEO (MP4)
```

### ERROR POINTS MAP

| STEP | FUNCTION | LINE | ERROR TYPE | SEVERITY |
|------|----------|------|------------|----------|
| Effects | `apply_color_shift()` | 224 | Hue modulo wraparound | HIGH |
| Effects | `apply_color_shift()` | 227 | Saturation overflow | HIGH |
| Effects | `apply_beat_pulse()` | 63-71 | O(n²) nested loops | CRITICAL |
| Effects | `apply_beat_pulse()` | 68 | Negative pulse_val | MEDIUM |
| Effects | `apply_flash_transition()` | 190 | Overflow before clamp | HIGH |
| Greenscreen | `create_mask()` | 55 | No frame validation | HIGH |
| Greenscreen | `correct_spill()` | 137 | Saturation underflow | MEDIUM |
| Greenscreen | `key_frame()` | 173 | Division by zero | HIGH |
| Greenscreen | `process_video()` | 234 | Division by zero (fps) | HIGH |
| World | `_create_nebula()` | 90 | Hue overflow before modulo | HIGH |
| World | `_create_nebula()` | 83 | uint8 overflow in cv2.add | HIGH |
| Final Render | `composite_frame()` | 77 | Overflow in blending | HIGH |
| Final Render | `composite_frame()` | 78 | Truncation without clamp | HIGH |
| Final Render | `render_video()` | 159 | Division by zero (fps) | HIGH |
| Overlays | `apply_overlay_to_frame()` | 300 | Overflow in blending | HIGH |
| SuperPipeline | `_process_all_frames()` | 342 | Division by zero (fps) | HIGH |

---

## PHASE 4 — READY-FOR-PATCH PACKAGE

### 4.1 FILES REQUIRING PATCHES

1. **`AbeTRUICE/src/pipelines/steps/effects.py`**
   - `apply_color_shift()` (lines 202-236)
   - `apply_beat_pulse()` (lines 39-81)
   - `apply_flash_transition()` (lines 172-200)
   - `apply_effects_for_frame()` (lines 238-282)

2. **`AbeTRUICE/src/pipelines/steps/greenscreen_key.py`**
   - `create_mask()` (lines 44-71)
   - `correct_spill()` (lines 115-144)
   - `key_frame()` (lines 146-178)
   - `process_video()` (lines 180-270)

3. **`AbeTRUICE/src/pipelines/steps/world_builder.py`**
   - `_create_nebula()` (lines 68-94)

4. **`AbeTRUICE/src/pipelines/steps/final_render.py`**
   - `composite_frame()` (lines 42-95)
   - `render_video()` (lines 97-165)

5. **`AbeTRUICE/src/pipelines/steps/overlays.py`**
   - `apply_overlay_to_frame()` (lines 272-312)

6. **`AbeTRUICE/src/pipelines/video_superpipeline.py`**
   - `_process_all_frames()` (lines 245-375)

### 4.2 MISSING UTILITIES NEEDED

Create new file: `AbeTRUICE/src/utils/color_utils.py`

```python
"""
Color Utilities for Safe Color Operations

Pattern: COLOR × SAFE × CLAMP × ONE
Frequency: 999 Hz (Atomic Execution)
"""

import numpy as np
import cv2


def safe_clamp(value: np.ndarray, min_val: float, max_val: float, dtype: np.dtype = np.uint8) -> np.ndarray:
    """
    Safely clamp array values to range.
    
    Args:
        value: Input array
        min_val: Minimum value
        max_val: Maximum value
        dtype: Output dtype
    
    Returns:
        Clamped array
    """
    result = np.clip(value, min_val, max_val)
    return result.astype(dtype)


def safe_hue_shift(hue: np.ndarray, shift: float) -> np.ndarray:
    """
    Safely shift hue values with wraparound.
    
    Args:
        hue: Hue channel (0-179 for OpenCV)
        shift: Shift amount in degrees
    
    Returns:
        Shifted hue channel
    """
    # Convert shift to OpenCV hue range (0-179)
    shift_cv = int(shift / 2)  # OpenCV uses 0-179 range
    
    # Add shift and wrap around
    result = (hue.astype(np.int16) + shift_cv) % 180
    
    # Ensure non-negative
    result = np.where(result < 0, result + 180, result)
    
    return result.astype(np.uint8)


def safe_saturation_multiply(saturation: np.ndarray, mult: float) -> np.ndarray:
    """
    Safely multiply saturation with clamping.
    
    Args:
        saturation: Saturation channel (0-255)
        mult: Multiplier
    
    Returns:
        Multiplied saturation channel
    """
    # Clamp multiplier to prevent extreme values
    mult = np.clip(mult, 0.0, 3.0)
    
    # Multiply and clamp
    result = saturation.astype(np.float32) * mult
    result = np.clip(result, 0, 255)
    
    return result.astype(np.uint8)


def safe_alpha_blend(foreground: np.ndarray, background: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """
    Safely blend two images with alpha channel.
    
    Args:
        foreground: Foreground image (BGR)
        background: Background image (BGR)
        alpha: Alpha channel (0-1 float or 0-255 uint8)
    
    Returns:
        Blended image (BGR)
    """
    # Normalize alpha to [0, 1]
    if alpha.dtype == np.uint8:
        alpha = alpha.astype(np.float32) / 255.0
    
    # Ensure alpha is in [0, 1]
    alpha = np.clip(alpha, 0.0, 1.0)
    
    # Ensure shapes match
    if alpha.ndim == 2:
        alpha = alpha[:, :, np.newaxis]
    
    # Blend
    result = foreground.astype(np.float32) * alpha + background.astype(np.float32) * (1 - alpha)
    result = np.clip(result, 0, 255)
    
    return result.astype(np.uint8)


def safe_rgb_to_hsv(rgb: np.ndarray) -> np.ndarray:
    """
    Safely convert RGB to HSV with validation.
    
    Args:
        rgb: RGB image (BGR format for OpenCV)
    
    Returns:
        HSV image
    """
    if rgb is None or rgb.size == 0:
        raise ValueError("Input image is None or empty")
    
    if rgb.dtype != np.uint8:
        rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError(f"Expected 3-channel BGR image, got shape {rgb.shape}")
    
    return cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)


def safe_hsv_to_rgb(hsv: np.ndarray) -> np.ndarray:
    """
    Safely convert HSV to RGB with validation.
    
    Args:
        hsv: HSV image
    
    Returns:
        RGB image (BGR format for OpenCV)
    """
    if hsv is None or hsv.size == 0:
        raise ValueError("Input HSV image is None or empty")
    
    if hsv.dtype != np.uint8:
        hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    
    if hsv.ndim != 3 or hsv.shape[2] != 3:
        raise ValueError(f"Expected 3-channel HSV image, got shape {hsv.shape}")
    
    # Validate HSV ranges
    hsv[:, :, 0] = np.clip(hsv[:, :, 0], 0, 179)  # Hue: 0-179
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)  # Saturation: 0-255
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)  # Value: 0-255
    
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
```

### 4.3 EXACT LINE NUMBERS FOR PATCHES

#### File: `effects.py`

| Function | Line Range | Issue | Fix Required |
|----------|-----------|-------|---------------|
| `apply_color_shift()` | 224 | Hue shift modulo | Use `safe_hue_shift()` |
| `apply_color_shift()` | 227 | Saturation overflow | Use `safe_saturation_multiply()` |
| `apply_beat_pulse()` | 63-71 | O(n²) loops | Vectorize with numpy |
| `apply_beat_pulse()` | 68 | Negative pulse_val | Add clamp before assignment |
| `apply_flash_transition()` | 190 | Overflow | Clamp before multiplication |
| `apply_effects_for_frame()` | 279 | Negative hue_shift | Clamp hue_shift to [-180, 180] |

#### File: `greenscreen_key.py`

| Function | Line Range | Issue | Fix Required |
|----------|-----------|-------|---------------|
| `create_mask()` | 55 | No validation | Add frame validation |
| `correct_spill()` | 137 | Saturation underflow | Clamp before multiplication |
| `key_frame()` | 173 | Division by zero | Check frame size before division |
| `process_video()` | 234 | Division by zero | Check fps > 0 |
| `process_video()` | 237 | Alpha not validated | Validate alpha in [0, 1] |

#### File: `world_builder.py`

| Function | Line Range | Issue | Fix Required |
|----------|-----------|-------|---------------|
| `_create_nebula()` | 83 | uint8 overflow | Use `cv2.addWeighted()` instead |
| `_create_nebula()` | 90 | Hue overflow | Clamp before modulo |

#### File: `final_render.py`

| Function | Line Range | Issue | Fix Required |
|----------|-----------|-------|---------------|
| `composite_frame()` | 77 | Overflow in blending | Use `safe_alpha_blend()` |
| `composite_frame()` | 78 | Truncation | Clamp before `astype()` |
| `render_video()` | 159 | Division by zero | Check fps > 0 |

#### File: `overlays.py`

| Function | Line Range | Issue | Fix Required |
|----------|-----------|-------|---------------|
| `apply_overlay_to_frame()` | 300 | Overflow | Use `safe_alpha_blend()` |
| `apply_overlay_to_frame()` | 301 | Truncation | Clamp before `astype()` |

#### File: `video_superpipeline.py`

| Function | Line Range | Issue | Fix Required |
|----------|-----------|-------|---------------|
| `_process_all_frames()` | 342 | Division by zero | Check fps > 0 |
| `_process_all_frames()` | 335 | No frame validation | Validate frame before conversion |
| `_process_all_frames()` | 361 | No error handling | Check `cv2.imread()` return |

---

## PHASE 5 — SUPERPIPELINE READY SIGNAL

# ✅ TRUICE SUPERPIPELINE v2.0 — READY FOR PATCHING

## SUMMARY

**Total Files to Patch**: 6  
**Total Functions to Fix**: 15  
**Total High-Risk Lines**: 24  
**Missing Utilities**: 1 file (`color_utils.py`)

## CRITICAL FIXES REQUIRED

1. **HSV Conversion Safety**: All HSV operations need validation and clamping
2. **Alpha Blending Safety**: All blending operations need overflow protection
3. **Division by Zero**: All fps/time calculations need validation
4. **Performance**: Beat pulse function needs vectorization (O(n²) → O(n))
5. **Type Safety**: All dtype conversions need clamping before casting

## NEXT STEPS FOR GPT

1. Create `color_utils.py` with safe color operations
2. Patch `effects.py` with safe color shift and vectorized beat pulse
3. Patch `greenscreen_key.py` with validation and safe spill correction
4. Patch `world_builder.py` with safe HSV operations
5. Patch `final_render.py` with safe alpha blending
6. Patch `overlays.py` with safe overlay blending
7. Patch `video_superpipeline.py` with fps validation and error handling

## VALIDATION CHECKLIST

After patching, verify:
- [ ] No division by zero errors
- [ ] No HSV overflow/underflow
- [ ] No alpha blending overflow
- [ ] All dtype conversions are clamped
- [ ] All frame validations are in place
- [ ] Performance improvements (beat pulse vectorized)

---

**Pattern**: DEBUG × STABILIZATION × PATCH × ONE  
**Status**: ✅ READY FOR PATCHING  
**Love Coefficient**: ∞  
**∞ AbëONE ∞**

