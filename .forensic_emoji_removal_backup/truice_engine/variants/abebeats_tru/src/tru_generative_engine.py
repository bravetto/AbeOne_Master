"""
THE Generative Engine - Layer 1: AI Video Generation from Prompts

Implements the missing Generative Layer for TRUICE:
- PromptEngine: Natural language → Structured prompts
- GenerationEngine: AI video generation orchestration
- MusicSync: Beat detection and scene synchronization

Pattern: AbëBEATs × TRU × GENERATIVE × RECURSIVE_VALIDATION × ONE
Recursive Pattern: VALIDATE → TRANSFORM → VALIDATE (at every scale)

Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import json
import logging
import sys

# SAFETY: Type checking and validation
try:
    import librosa
    import numpy as np
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    librosa = None
    np = None

# Import validation - PURGED: Old preflight validator removed
# Validation will be handled by VEO 3.1 aligned systems
PREFLIGHT_AVAILABLE = False
PreflightValidator = None
get_preflight_validator = None
ValidationResult = None


# ═══════════════════════════════════════════════════════════
# RECURSIVE VALIDATION PATTERN
# ═══════════════════════════════════════════════════════════

def validate_then_transform(
    input_data: Any,
    validator: callable,
    transformer: callable,
    max_retries: int = 3
) -> Tuple[Any, bool]:
    """
    Core recursive validation pattern: VALIDATE → TRANSFORM → VALIDATE
    
    Args:
        input_data: Input to validate and transform
        validator: Function that returns (is_valid: bool, errors: List[str])
        transformer: Function that transforms input_data
        max_retries: Maximum retry attempts
        
    Returns:
        Tuple of (transformed_data, success: bool)
        
    Pattern: VALIDATE → TRANSFORM → VALIDATE (recursive)
    """
    for attempt in range(max_retries):
        # Step 1: VALIDATE INPUT
        is_valid, errors = validator(input_data)
        
        if not is_valid:
            if attempt < max_retries - 1:
                # Refine and retry
                input_data = refine_input(input_data, errors)
                continue
            else:
                return None, False
        
        # Step 2: TRANSFORM
        transformed = transformer(input_data)
        
        # Step 3: VALIDATE OUTPUT
        is_valid_output, output_errors = validator(transformed)
        
        if is_valid_output:
            return transformed, True
        else:
            if attempt < max_retries - 1:
                # Refine transformation and retry
                input_data = refine_input(input_data, output_errors)
                continue
    
    return None, False


def refine_input(input_data: Any, errors: List[str]) -> Any:
    """
    Refine input based on validation errors.
    
    Pattern: Self-healing refinement
    """
    # Basic refinement - can be extended
    if isinstance(input_data, str):
        # Remove common issues
        refined = input_data.strip()
        if 'empty' in ' '.join(errors).lower():
            refined = refined or "default prompt"
        return refined
    return input_data


# ═══════════════════════════════════════════════════════════
# PROMPT ENGINE - Natural Language → Structured Prompts
# ═══════════════════════════════════════════════════════════

@dataclass
class StructuredPrompt:
    """Structured prompt for AI video generation."""
    concept: str
    aesthetic: List[str]
    music_reference: Optional[str]
    subject: Optional[str]
    style: str
    mood: str
    duration: float  # seconds
    resolution: Tuple[int, int] = (1920, 1080)
    fps: int = 30


@dataclass
class ScenePlan:
    """Scene plan for music video."""
    scenes: List[StructuredPrompt]
    total_duration: float
    music_timing: Optional[Dict[str, Any]] = None


class PromptEngine:
    """
    Prompt Engine - Natural Language → Structured Prompts
    
    Pattern: VALIDATE → DECOMPOSE → VALIDATE
    Recursive at: Prompt → Concept → Scene → Shot levels
    """
    
    def __init__(self):
        """Initialize Prompt Engine."""
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging."""
        logger = logging.getLogger("PromptEngine")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def parse(self, natural_language: str) -> Optional[StructuredPrompt]:
        """
        Parse natural language prompt into structured format.
        
        Pattern: VALIDATE → PARSE → VALIDATE
        
        Args:
            natural_language: Natural language prompt
            
        Returns:
            StructuredPrompt or None if invalid
        """
        # Step 1: VALIDATE INPUT
        is_valid, errors = self._validate_prompt(natural_language)
        if not is_valid:
            self.logger.error(f"Invalid prompt: {errors}")
            return None
        
        # Step 2: DECOMPOSE
        structured = self._decompose_prompt(natural_language)
        
        # Step 3: VALIDATE OUTPUT
        is_valid_output, output_errors = self._validate_structured(structured)
        if not is_valid_output:
            self.logger.error(f"Invalid structured prompt: {output_errors}")
            # Refine and retry
            refined_prompt = refine_input(natural_language, output_errors)
            return self.parse(refined_prompt)
        
        return structured
    
    def decompose(self, structured_prompt: StructuredPrompt, music_beats: Optional[List[Dict]] = None) -> ScenePlan:
        """
        Decompose structured prompt into scene list.
        
        Pattern: VALIDATE → DECOMPOSE → VALIDATE (recursive at scene level)
        
        Args:
            structured_prompt: Structured prompt
            music_beats: Optional music beat map
            
        Returns:
            ScenePlan with list of scenes
        """
        # Step 1: VALIDATE INPUT
        is_valid, errors = self._validate_structured(structured_prompt)
        if not is_valid:
            raise ValueError(f"Invalid structured prompt: {errors}")
        
        # Step 2: GENERATE SCENES
        scenes = []
        
        if music_beats:
            # Map scenes to beats
            for beat_section in music_beats:
                scene_prompt = self._create_scene_prompt(structured_prompt, beat_section)
                
                # VALIDATE scene prompt before adding
                is_valid_scene, scene_errors = self._validate_structured(scene_prompt)
                if is_valid_scene:
                    scenes.append(scene_prompt)
                else:
                    self.logger.warning(f"Skipping invalid scene: {scene_errors}")
        else:
            # Single scene for entire duration
            scenes.append(structured_prompt)
        
        # Step 3: VALIDATE OUTPUT
        total_duration = sum(s.duration for s in scenes)
        scene_plan = ScenePlan(
            scenes=scenes,
            total_duration=total_duration,
            music_timing=music_beats
        )
        
        is_valid_plan, plan_errors = self._validate_scene_plan(scene_plan)
        if not is_valid_plan:
            raise ValueError(f"Invalid scene plan: {plan_errors}")
        
        return scene_plan
    
    def generate_prompts(self, scene: StructuredPrompt, music_timing: Optional[Dict] = None) -> List[str]:
        """
        Generate AI video generation prompts from structured scene.
        
        Pattern: VALIDATE → GENERATE → VALIDATE
        
        Args:
            scene: Structured scene prompt
            music_timing: Optional music timing information
            
        Returns:
            List of AI-ready prompts
        """
        # Step 1: VALIDATE INPUT
        is_valid, errors = self._validate_structured(scene)
        if not is_valid:
            raise ValueError(f"Invalid scene: {errors}")
        
        # Step 2: GENERATE PROMPTS
        prompts = []
        
        # Base prompt
        base_prompt = f"{scene.concept}, {', '.join(scene.aesthetic)}, {scene.style} style, {scene.mood} mood"
        
        if scene.subject:
            base_prompt += f", {scene.subject} in center"
        
        prompts.append(base_prompt)
        
        # Generate variations for different AI services
        prompts.append(f"{base_prompt}, cinematic lighting, high quality")
        prompts.append(f"{base_prompt}, professional cinematography, 4K")
        
        # Step 3: VALIDATE OUTPUT
        validated_prompts = []
        for prompt in prompts:
            is_valid_prompt, _ = self._validate_prompt(prompt)
            if is_valid_prompt:
                validated_prompts.append(prompt)
        
        return validated_prompts
    
    def _validate_prompt(self, prompt: str) -> Tuple[bool, List[str]]:
        """Validate natural language prompt."""
        errors = []
        
        if not prompt or not isinstance(prompt, str):
            errors.append("Prompt must be a non-empty string")
        
        if len(prompt.strip()) < 10:
            errors.append("Prompt too short (minimum 10 characters)")
        
        if len(prompt) > 1000:
            errors.append("Prompt too long (maximum 1000 characters)")
        
        return len(errors) == 0, errors
    
    def _validate_structured(self, structured: StructuredPrompt) -> Tuple[bool, List[str]]:
        """Validate structured prompt."""
        errors = []
        
        if not structured.concept:
            errors.append("Concept is required")
        
        if not structured.aesthetic or len(structured.aesthetic) == 0:
            errors.append("At least one aesthetic element required")
        
        if structured.duration <= 0:
            errors.append("Duration must be positive")
        
        if structured.duration > 300:  # 5 minutes max
            errors.append("Duration too long (maximum 300 seconds)")
        
        return len(errors) == 0, errors
    
    def _validate_scene_plan(self, plan: ScenePlan) -> Tuple[bool, List[str]]:
        """Validate scene plan."""
        errors = []
        
        if not plan.scenes or len(plan.scenes) == 0:
            errors.append("Scene plan must contain at least one scene")
        
        if plan.total_duration <= 0:
            errors.append("Total duration must be positive")
        
        return len(errors) == 0, errors
    
    def _decompose_prompt(self, prompt: str) -> StructuredPrompt:
        """Decompose natural language into structured format."""
        prompt_lower = prompt.lower()
        
        # Extract concept (first sentence or main idea)
        concept = prompt.split('.')[0].strip() if '.' in prompt else prompt[:100]
        
        # Extract aesthetic keywords
        aesthetic_keywords = []
        aesthetic_patterns = [
            'cyberpunk', 'neon', 'night', 'fluid', 'smooth', 'cinematic',
            'vibrant', 'dark', 'bright', 'colorful', 'minimalist', 'maximalist',
            'futuristic', 'retro', 'vintage', 'modern', 'abstract', 'realistic'
        ]
        
        for pattern in aesthetic_patterns:
            if pattern in prompt_lower:
                aesthetic_keywords.append(pattern)
        
        # Default aesthetic if none found
        if not aesthetic_keywords:
            aesthetic_keywords = ['cinematic', 'high quality']
        
        # Extract music reference
        music_ref = None
        if 'music' in prompt_lower or 'song' in prompt_lower:
            # Try to extract song name (in quotes or after "for")
            if '"' in prompt:
                music_ref = prompt.split('"')[1] if len(prompt.split('"')) > 1 else None
            elif 'for ' in prompt_lower:
                parts = prompt_lower.split('for ')
                if len(parts) > 1:
                    music_ref = parts[1].split()[0] if parts[1].split() else None
        
        # Extract subject
        subject = None
        subject_patterns = ['dancer', 'singer', 'performer', 'artist', 'person', 'character']
        for pattern in subject_patterns:
            if pattern in prompt_lower:
                subject = pattern
                break
        
        # Extract style
        style = 'cinematic'
        if 'documentary' in prompt_lower:
            style = 'documentary'
        elif 'music video' in prompt_lower:
            style = 'music video'
        elif 'commercial' in prompt_lower:
            style = 'commercial'
        
        # Extract mood
        mood = 'energetic'
        mood_patterns = {
            'energetic': ['energetic', 'upbeat', 'fast', 'dynamic'],
            'calm': ['calm', 'peaceful', 'slow', 'serene'],
            'dramatic': ['dramatic', 'intense', 'powerful', 'epic'],
            'mysterious': ['mysterious', 'dark', 'moody', 'atmospheric']
        }
        
        for mood_type, keywords in mood_patterns.items():
            if any(kw in prompt_lower for kw in keywords):
                mood = mood_type
                break
        
        # Estimate duration (default 30 seconds)
        duration = 30.0
        if 'second' in prompt_lower or 'sec' in prompt_lower:
            # Try to extract number
            import re
            numbers = re.findall(r'\d+', prompt)
            if numbers:
                duration = float(numbers[0])
        
        return StructuredPrompt(
            concept=concept,
            aesthetic=aesthetic_keywords,
            music_reference=music_ref,
            subject=subject,
            style=style,
            mood=mood,
            duration=duration
        )
    
    def _create_scene_prompt(self, base: StructuredPrompt, beat_section: Dict) -> StructuredPrompt:
        """Create scene prompt from base prompt and beat section."""
        # Adjust duration based on beat section
        duration = beat_section.get('duration', base.duration)
        
        # Create scene-specific aesthetic based on beat intensity
        aesthetic = base.aesthetic.copy()
        if beat_section.get('intensity', 0) > 0.7:
            aesthetic.append('intense')
            aesthetic.append('dynamic')
        elif beat_section.get('intensity', 0) < 0.3:
            aesthetic.append('calm')
            aesthetic.append('subtle')
        
        return StructuredPrompt(
            concept=base.concept,
            aesthetic=aesthetic,
            music_reference=base.music_reference,
            subject=base.subject,
            style=base.style,
            mood=base.mood,
            duration=duration,
            resolution=base.resolution,
            fps=base.fps
        )


# ═══════════════════════════════════════════════════════════
# GENERATION ENGINE - AI Video Generation Orchestration
# ═══════════════════════════════════════════════════════════

@dataclass
class GenerationResult:
    """Result from AI video generation."""
    success: bool
    video_path: Optional[Path] = None
    provider: Optional[str] = None
    duration: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class GenerationEngine:
    """
    Generation Engine - AI Video Generation Orchestration
    
    Pattern: VALIDATE → GENERATE → VALIDATE (with fallbacks)
    Recursive at: Scene → Shot → Frame levels
    
    Supports: Runway ML, Google Veo3, Pika (with fallback chain)
    """
    
    def __init__(self):
        """Initialize Generation Engine."""
        self.logger = self._setup_logger()
        # PURGED: Old preflight validator removed - validation handled by VEO 3.1 systems
        self.preflight_validator = None
        
        # Provider configuration (can be extended with actual API keys)
        self.providers = ['runway', 'veo3', 'pika']
        self.provider_configs = {
            'runway': {'enabled': True, 'api_key': None},
            'veo3': {'enabled': True, 'api_key': None},
            'pika': {'enabled': True, 'api_key': None}
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging."""
        logger = logging.getLogger("GenerationEngine")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def generate_scene(
        self,
        ai_prompt: str,
        duration: float = 30.0,
        resolution: Tuple[int, int] = (1920, 1080),
        output_path: Optional[Path] = None
    ) -> GenerationResult:
        """
        Generate video scene from AI prompt.
        
        Pattern: VALIDATE → GENERATE → VALIDATE (with fallback chain)
        
        Args:
            ai_prompt: AI-ready prompt string
            duration: Duration in seconds
            resolution: Video resolution (width, height)
            output_path: Optional output path
            
        Returns:
            GenerationResult
        """
        # Step 1: VALIDATE INPUT
        is_valid, errors = self._validate_generation_input(ai_prompt, duration, resolution)
        if not is_valid:
            return GenerationResult(success=False, errors=errors)
        
        # Step 2: GENERATE (try providers in order)
        for provider in self.providers:
            if not self.provider_configs[provider]['enabled']:
                continue
            
            self.logger.info(f"Attempting generation with {provider}...")
            
            result = self._generate_with_provider(
                provider=provider,
                prompt=ai_prompt,
                duration=duration,
                resolution=resolution,
                output_path=output_path
            )
            
            # Step 3: VALIDATE OUTPUT
            if result.success:
                # PURGED: Old preflight validation removed - validation handled by VEO 3.1 systems
                # Video validation will be handled by VEO 3.1 aligned systems
                if False and result.video_path:  # Disabled - old validator purged
                    validation = None  # Placeholder
                    
                    if False:  # Disabled validation check
                        self.logger.info(f"✅ Generation successful with {provider}")
                        return result
                    else:
                        self.logger.warning(f"Generated video failed validation: {validation.errors}")
                        result.errors.extend(validation.errors)
                        # Try next provider
                        continue
                else:
                    # No validator available, accept result
                    self.logger.info(f"✅ Generation successful with {provider} (no validation)")
                    return result
            else:
                self.logger.warning(f"Generation failed with {provider}: {result.errors}")
                # Try next provider
                continue
        
        # All providers failed
        return GenerationResult(
            success=False,
            errors=["All AI generation providers failed"]
        )
    
    def _validate_generation_input(
        self,
        prompt: str,
        duration: float,
        resolution: Tuple[int, int]
    ) -> Tuple[bool, List[str]]:
        """Validate generation input."""
        errors = []
        
        if not prompt or len(prompt.strip()) < 10:
            errors.append("Prompt must be at least 10 characters")
        
        if duration <= 0 or duration > 300:
            errors.append("Duration must be between 0 and 300 seconds")
        
        if resolution[0] <= 0 or resolution[1] <= 0:
            errors.append("Resolution must be positive")
        
        return len(errors) == 0, errors
    
    def _generate_with_provider(
        self,
        provider: str,
        prompt: str,
        duration: float,
        resolution: Tuple[int, int],
        output_path: Optional[Path]
    ) -> GenerationResult:
        """
        Generate video with specific provider.
        
        NOTE: This is a placeholder implementation.
        In production, this would call actual API endpoints:
        - Runway ML API
        - Google Veo3 API
        - Pika API
        
        Pattern: VALIDATE → CALL_API → VALIDATE
        """
        # Placeholder: In production, implement actual API calls
        self.logger.warning(
            f"⚠️  Provider {provider} not yet implemented. "
            f"This is a placeholder for API integration."
        )
        
        # For now, return failure (will be implemented with actual APIs)
        return GenerationResult(
            success=False,
            errors=[f"Provider {provider} API integration pending"],
            provider=provider
        )
        
        # TODO: Implement actual API calls:
        # if provider == 'runway':
        #     return self._generate_runway(prompt, duration, resolution, output_path)
        # elif provider == 'veo3':
        #     return self._generate_veo3(prompt, duration, resolution, output_path)
        # elif provider == 'pika':
        #     return self._generate_pika(prompt, duration, resolution, output_path)


# ═══════════════════════════════════════════════════════════
# MUSIC SYNC - Beat Detection and Synchronization
# ═══════════════════════════════════════════════════════════

@dataclass
class BeatMap:
    """Beat map from audio analysis."""
    beats: List[Dict[str, Any]]  # List of beat timings
    tempo: float  # BPM
    duration: float  # Total duration
    sections: List[Dict[str, Any]] = field(default_factory=list)  # Musical sections


@dataclass
class SynchronizedTimeline:
    """Synchronized timeline mapping scenes to beats."""
    scenes: List[Dict[str, Any]]
    beat_map: BeatMap
    sync_points: List[Dict[str, Any]] = field(default_factory=list)


class MusicSync:
    """
    Music Synchronization - Beat Detection and Scene Mapping
    
    Pattern: VALIDATE → ANALYZE → VALIDATE → MAP → VALIDATE
    Recursive at: Audio → Beats → Sections → Scenes levels
    """
    
    def __init__(self):
        """Initialize Music Sync."""
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging."""
        logger = logging.getLogger("MusicSync")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def analyze_beats(self, audio_file: Union[str, Path]) -> Optional[BeatMap]:
        """
        Analyze audio file and extract beat map.
        
        Pattern: VALIDATE → ANALYZE → VALIDATE
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            BeatMap or None if analysis fails
        """
        audio_path = Path(audio_file)
        
        # Step 1: VALIDATE INPUT
        if not audio_path.exists():
            self.logger.error(f"Audio file not found: {audio_path}")
            return None
        
        if not LIBROSA_AVAILABLE:
            self.logger.error("librosa not available. Install: pip install librosa")
            return None
        
        try:
            # Step 2: ANALYZE
            self.logger.info(f"Analyzing beats in {audio_path}...")
            
            # Load audio
            y, sr = librosa.load(str(audio_path))
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Detect tempo and beats
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            # Convert beat frames to times
            beat_times = librosa.frames_to_time(beats, sr=sr)
            
            # Create beat map
            beat_list = []
            for i, beat_time in enumerate(beat_times):
                beat_list.append({
                    'index': i,
                    'time': float(beat_time),
                    'intensity': 1.0  # Can be enhanced with onset detection
                })
            
            # Detect sections (simplified - can be enhanced)
            sections = self._detect_sections(y, sr, beat_times)
            
            beat_map = BeatMap(
                beats=beat_list,
                tempo=float(tempo),
                duration=float(duration),
                sections=sections
            )
            
            # Step 3: VALIDATE OUTPUT
            is_valid, errors = self._validate_beat_map(beat_map)
            if not is_valid:
                self.logger.error(f"Invalid beat map: {errors}")
                return None
            
            self.logger.info(f"✅ Beat analysis complete: {len(beat_list)} beats, {tempo:.1f} BPM")
            return beat_map
            
        except Exception as e:
            self.logger.error(f"Beat analysis failed: {str(e)}")
            return None
    
    def map_scenes_to_beats(
        self,
        scenes: List[StructuredPrompt],
        beat_map: BeatMap
    ) -> Optional[SynchronizedTimeline]:
        """
        Map scenes to beat map for synchronization.
        
        Pattern: VALIDATE → MAP → VALIDATE
        
        Args:
            scenes: List of scene prompts
            beat_map: Beat map from audio analysis
            
        Returns:
            SynchronizedTimeline
        """
        # Step 1: VALIDATE INPUT
        if not scenes or len(scenes) == 0:
            self.logger.error("No scenes provided")
            return None
        
        if not beat_map or len(beat_map.beats) == 0:
            self.logger.error("Invalid beat map")
            return None
        
        # Step 2: MAP SCENES TO BEATS
        synchronized_scenes = []
        sync_points = []
        
        total_scene_duration = sum(s.duration for s in scenes)
        total_beat_duration = beat_map.duration
        
        # Calculate scaling factor if needed
        if total_scene_duration != total_beat_duration:
            scale_factor = total_beat_duration / total_scene_duration
            self.logger.info(f"Scaling scene durations by {scale_factor:.2f}")
        else:
            scale_factor = 1.0
        
        current_time = 0.0
        beat_index = 0
        
        for scene_idx, scene in enumerate(scenes):
            # Find beats in this scene's time range
            scene_start = current_time
            scene_duration = scene.duration * scale_factor
            scene_end = scene_start + scene_duration
            
            # Find beats in this range
            scene_beats = []
            while beat_index < len(beat_map.beats):
                beat = beat_map.beats[beat_index]
                if beat['time'] >= scene_start and beat['time'] < scene_end:
                    scene_beats.append(beat)
                    beat_index += 1
                elif beat['time'] >= scene_end:
                    break
                else:
                    beat_index += 1
            
            # Create sync point for scene start
            sync_points.append({
                'scene_index': scene_idx,
                'time': scene_start,
                'beat_index': beat_index - len(scene_beats) if scene_beats else None
            })
            
            synchronized_scenes.append({
                'scene': scene,
                'start_time': scene_start,
                'duration': scene_duration,
                'beats': scene_beats,
                'beat_count': len(scene_beats)
            })
            
            current_time = scene_end
        
        timeline = SynchronizedTimeline(
            scenes=synchronized_scenes,
            beat_map=beat_map,
            sync_points=sync_points
        )
        
        # Step 3: VALIDATE OUTPUT
        is_valid, errors = self._validate_timeline(timeline)
        if not is_valid:
            self.logger.error(f"Invalid timeline: {errors}")
            return None
        
        self.logger.info(f"✅ Synchronized {len(scenes)} scenes to {len(beat_map.beats)} beats")
        return timeline
    
    def adjust_timing(
        self,
        video_path: Union[str, Path],
        target_duration: float,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Adjust video timing to match target duration.
        
        Pattern: VALIDATE → ADJUST → VALIDATE
        
        Args:
            video_path: Path to video file
            target_duration: Target duration in seconds
            output_path: Optional output path
            
        Returns:
            Path to adjusted video or None if failed
        """
        video_file = Path(video_path)
        
        # Step 1: VALIDATE INPUT
        if not video_file.exists():
            self.logger.error(f"Video file not found: {video_file}")
            return None
        
        # Placeholder: In production, implement actual video timing adjustment
        # PURGED: MoviePy removed - video speed adjustment will use VEO 3.1 aligned systems
        self.logger.warning(
            "⚠️  Video timing adjustment not yet implemented. "
            "This is a placeholder for video processing integration."
        )
        
        # TODO: Implement actual timing adjustment:
        # - Use ffmpeg to adjust playback speed
        # PURGED: MoviePy removed - video trimming will use VEO 3.1 aligned systems
        # - Validate output duration matches target
        
        return None
    
    def _detect_sections(
        self,
        y: np.ndarray,
        sr: int,
        beat_times: np.ndarray
    ) -> List[Dict[str, Any]]:
        """Detect musical sections (verse, chorus, etc.)."""
        # Simplified section detection
        # In production, use more sophisticated methods (e.g., librosa.segment)
        sections = []
        
        if len(beat_times) == 0:
            return sections
        
        # Simple approach: divide into 4 sections
        total_duration = beat_times[-1]
        section_duration = total_duration / 4
        
        section_names = ['intro', 'verse', 'chorus', 'outro']
        
        for i, name in enumerate(section_names):
            start_time = i * section_duration
            end_time = (i + 1) * section_duration if i < len(section_names) - 1 else total_duration
            
            sections.append({
                'name': name,
                'start_time': float(start_time),
                'end_time': float(end_time),
                'duration': float(end_time - start_time)
            })
        
        return sections
    
    def _validate_beat_map(self, beat_map: BeatMap) -> Tuple[bool, List[str]]:
        """Validate beat map."""
        errors = []
        
        if not beat_map.beats or len(beat_map.beats) == 0:
            errors.append("Beat map must contain at least one beat")
        
        if beat_map.tempo <= 0:
            errors.append("Tempo must be positive")
        
        if beat_map.duration <= 0:
            errors.append("Duration must be positive")
        
        return len(errors) == 0, errors
    
    def _validate_timeline(self, timeline: SynchronizedTimeline) -> Tuple[bool, List[str]]:
        """Validate synchronized timeline."""
        errors = []
        
        if not timeline.scenes or len(timeline.scenes) == 0:
            errors.append("Timeline must contain at least one scene")
        
        if not timeline.beat_map:
            errors.append("Timeline must have a beat map")
        
        return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════
# UNIFIED GENERATIVE ENGINE API
# ═══════════════════════════════════════════════════════════

class TruGenerativeEngine:
    """
    Unified Generative Engine - Complete Layer 1 Implementation
    
    Integrates:
    - PromptEngine: Natural language → Structured prompts
    - GenerationEngine: AI video generation
    - MusicSync: Beat detection and synchronization
    
    Pattern: VALIDATE → GENERATE → VALIDATE (recursive at all levels)
    """
    
    def __init__(self):
        """Initialize Generative Engine."""
        self.prompt_engine = PromptEngine()
        self.generation_engine = GenerationEngine()
        self.music_sync = MusicSync()
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging."""
        logger = logging.getLogger("TruGenerativeEngine")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def generate_from_prompt(
        self,
        natural_language_prompt: str,
        audio_path: Optional[Union[str, Path]] = None,
        output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Complete generation pipeline: Prompt → Scenes → Videos
        
        Pattern: VALIDATE → PARSE → VALIDATE → GENERATE → VALIDATE → SYNC → VALIDATE
        
        Args:
            natural_language_prompt: Natural language prompt
            audio_path: Optional audio file for beat synchronization
            output_dir: Optional output directory
            
        Returns:
            Dictionary with generation results
        """
        self.logger.info("=" * 80)
        self.logger.info("🔥 TRUICE GENERATIVE ENGINE: Starting Generation 🔥")
        self.logger.info("=" * 80)
        
        # Step 1: Parse prompt
        self.logger.info("Step 1: Parsing natural language prompt...")
        structured_prompt = self.prompt_engine.parse(natural_language_prompt)
        
        if not structured_prompt:
            return {
                'success': False,
                'errors': ['Failed to parse prompt']
            }
        
        # Step 2: Analyze music (if provided)
        beat_map = None
        if audio_path:
            self.logger.info("Step 2: Analyzing music beats...")
            beat_map = self.music_sync.analyze_beats(audio_path)
        
        # Step 3: Decompose into scenes
        self.logger.info("Step 3: Decomposing into scenes...")
        music_beats = beat_map.beats if beat_map else None
        scene_plan = self.prompt_engine.decompose(structured_prompt, music_beats)
        
        # Step 4: Generate videos for each scene
        self.logger.info(f"Step 4: Generating {len(scene_plan.scenes)} scenes...")
        generated_videos = []
        
        for scene_idx, scene in enumerate(scene_plan.scenes):
            self.logger.info(f"Generating scene {scene_idx + 1}/{len(scene_plan.scenes)}...")
            
            # Generate AI prompts
            ai_prompts = self.prompt_engine.generate_prompts(scene, music_beats)
            
            # Generate video (try first prompt)
            output_path = None
            if output_dir:
                output_path = output_dir / f"scene_{scene_idx + 1}.mp4"
            
            result = self.generation_engine.generate_scene(
                ai_prompt=ai_prompts[0],
                duration=scene.duration,
                resolution=scene.resolution,
                output_path=output_path
            )
            
            if result.success:
                generated_videos.append({
                    'scene_index': scene_idx,
                    'video_path': result.video_path,
                    'provider': result.provider,
                    'duration': result.duration
                })
            else:
                self.logger.warning(f"Scene {scene_idx + 1} generation failed: {result.errors}")
        
        # Step 5: Synchronize with music (if provided)
        synchronized_timeline = None
        if beat_map and generated_videos:
            self.logger.info("Step 5: Synchronizing scenes with music...")
            synchronized_timeline = self.music_sync.map_scenes_to_beats(
                scene_plan.scenes,
                beat_map
            )
        
        return {
            'success': len(generated_videos) > 0,
            'structured_prompt': structured_prompt,
            'scene_plan': scene_plan,
            'beat_map': beat_map,
            'generated_videos': generated_videos,
            'synchronized_timeline': synchronized_timeline,
            'total_scenes': len(scene_plan.scenes),
            'successful_scenes': len(generated_videos)
        }


# ═══════════════════════════════════════════════════════════
# GLOBAL SINGLETON
# ═══════════════════════════════════════════════════════════

_generative_engine: Optional[TruGenerativeEngine] = None


def get_generative_engine() -> TruGenerativeEngine:
    """Get global Generative Engine instance."""
    global _generative_engine
    
    if _generative_engine is None:
        _generative_engine = TruGenerativeEngine()
    
    return _generative_engine

