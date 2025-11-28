"""
Veo 3.1 Prompt Engineering Engine
Epistemic Foundation: Chain-of-Frames (CoF) Reasoning

Implements:
- Character Bible Methodology (Identity Anchors)
- Layered Prompting Framework (Identity/Cinematography/Environment/Performance)
- Runway API Orchestration Patterns
- Multi-Subject Integration via Workflows

Pattern: EPISTEMIC × PROMPT × ORCHESTRATION × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PromptLayer(Enum):
    """Layered Prompting Framework Layers"""
    IDENTITY = "identity"  # Fixed axiom - who
    CINEMATOGRAPHY = "cinematography"  # Fixed grammar - how
    ENVIRONMENT = "environment"  # Fixed context - where
    PERFORMANCE = "performance"  # Variable - what


@dataclass
class CharacterBible:
    """
    Character Bible / Identity Anchors
    
    Provides fixed axioms for Veo 3.1's CoF reasoning to prevent identity drift.
    """
    name: str
    reference_images: List[str] = field(default_factory=list)  # URLs or paths
    wardrobe: str = ""  # Consistent wardrobe description
    physical_description: str = ""  # Age, hair, features
    tag: str = ""  # Tag for @tag syntax (3-16 chars)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_reference_dict(self) -> Dict[str, Any]:
        """Convert to Runway API referenceImages format"""
        return {
            "uri": self.reference_images[0] if self.reference_images else "",
            "tag": self.tag or self.name[:16]
        }
    
    def to_identity_layer(self) -> str:
        """Generate Identity Layer prompt text"""
        parts = []
        if self.physical_description:
            parts.append(self.physical_description)
        if self.wardrobe:
            parts.append(f"wearing {self.wardrobe}")
        return ", ".join(parts)


@dataclass
class LayeredPrompt:
    """
    Layered Prompting Framework
    
    Manually anchors CoF reasoning across multi-shot sequences.
    """
    identity: str  # Fixed - must not change between shots
    cinematography: str  # Fixed - maintains visual continuity
    environment: str  # Fixed - maintains context
    performance: str  # Variable - changes per shot
    
    def to_prompt_text(self) -> str:
        """Generate full prompt text"""
        return f"{self.identity}. {self.cinematography}. {self.environment}. {self.performance}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict"""
        return {
            "identity": self.identity,
            "cinematography": self.cinematography,
            "environment": self.environment,
            "performance": self.performance,
            "full_prompt": self.to_prompt_text()
        }


@dataclass
class Veo31PromptConfig:
    """Configuration for Veo 3.1 prompt generation"""
    # Model selection
    model: str = "veo3.1"  # veo3, veo3.1, veo3.1_fast
    duration: int = 5  # 2-10 seconds
    
    # Character Bibles
    primary_subject: Optional[CharacterBible] = None
    secondary_subjects: List[CharacterBible] = field(default_factory=list)
    
    # Layered Prompt
    layered_prompt: Optional[LayeredPrompt] = None
    
    # Audio/Dialogue
    dialogue: Optional[str] = None
    sound_design: Optional[str] = None
    
    # Runway API specific
    use_workflow: bool = True  # Use Runway Workflows for multi-subject
    workflow_pattern: str = "gen4_image_to_veo31"  # gen4_image -> veo3.1
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


class Veo31PromptEngine:
    """
    Veo 3.1 Prompt Engineering Engine
    
    Implements epistemic foundations:
    - Chain-of-Frames (CoF) reasoning support
    - Character Bible identity anchoring
    - Layered Prompting framework
    - Runway API orchestration patterns
    """
    
    def __init__(self):
        """Initialize prompt engine"""
        self.logger = logging.getLogger(f"{__name__}.Veo31PromptEngine")
        self.character_bibles: Dict[str, CharacterBible] = {}
        self.prompt_history: List[Dict[str, Any]] = []
    
    def register_character_bible(self, bible: CharacterBible) -> None:
        """Register a Character Bible for identity anchoring"""
        self.character_bibles[bible.name] = bible
        self.logger.info(f"Registered Character Bible: {bible.name} (tag: {bible.tag})")
    
    def create_layered_prompt(
        self,
        identity: str,
        cinematography: str,
        environment: str,
        performance: str
    ) -> LayeredPrompt:
        """
        Create a Layered Prompt following the framework.
        
        Pattern: IDENTITY (fixed) + CINEMATOGRAPHY (fixed) + ENVIRONMENT (fixed) + PERFORMANCE (variable)
        """
        return LayeredPrompt(
            identity=identity,
            cinematography=cinematography,
            environment=environment,
            performance=performance
        )
    
    def generate_character_bible_identity(
        self,
        character_name: str
    ) -> Optional[str]:
        """Generate Identity Layer from Character Bible"""
        bible = self.character_bibles.get(character_name)
        if not bible:
            self.logger.warning(f"Character Bible not found: {character_name}")
            return None
        return bible.to_identity_layer()
    
    def generate_multi_subject_prompt(
        self,
        primary_name: str,
        secondary_names: List[str],
        relationship: str,
        performance: str
    ) -> str:
        """
        Generate multi-subject prompt using Character Bibles.
        
        Example: "A shot of @person holding @product in a cinematic style."
        """
        primary_bible = self.character_bibles.get(primary_name)
        if not primary_bible:
            raise ValueError(f"Primary Character Bible not found: {primary_name}")
        
        # Build prompt with @tag syntax
        prompt_parts = [f"@{primary_bible.tag}"]
        
        for sec_name in secondary_names:
            sec_bible = self.character_bibles.get(sec_name)
            if sec_bible:
                prompt_parts.append(f"@{sec_bible.tag}")
            else:
                self.logger.warning(f"Secondary Character Bible not found: {sec_name}")
        
        prompt_parts.append(relationship)
        prompt_parts.append(performance)
        
        return " ".join(prompt_parts)
    
    def generate_runway_workflow_payload(
        self,
        config: Veo31PromptConfig
    ) -> Dict[str, Any]:
        """
        Generate Runway Workflow payload for multi-subject integration.
        
        Pattern: gen4_image (composition) -> veo3.1 (animation)
        """
        if not config.use_workflow:
            # Direct veo3.1 API call (single subject only)
            return self._generate_direct_veo31_payload(config)
        
        # Workflow pattern: gen4_image -> veo3.1
        workflow_payload = {
            "workflow_type": config.workflow_pattern,
            "nodes": []
        }
        
        # Node 1: gen4_image (Composition Agent)
        if config.primary_subject and config.secondary_subjects:
            gen4_payload = {
                "node_type": "media_model",
                "model": "gen4_image",
                "promptText": self._generate_gen4_composition_prompt(config),
                "referenceImages": self._collect_reference_images(config)
            }
            workflow_payload["nodes"].append({
                "id": "gen4_composition",
                "type": "gen4_image",
                "config": gen4_payload
            })
        
        # Node 2: veo3.1 (Animation Agent)
        veo31_payload = {
            "node_type": "media_model",
            "model": config.model,
            "promptImage": "{{gen4_composition.output}}",  # Pipe from gen4
            "promptText": config.layered_prompt.performance if config.layered_prompt else "",
            "duration": config.duration
        }
        workflow_payload["nodes"].append({
            "id": "veo31_animation",
            "type": "veo31",
            "config": veo31_payload
        })
        
        return workflow_payload
    
    def _generate_direct_veo31_payload(
        self,
        config: Veo31PromptConfig
    ) -> Dict[str, Any]:
        """Generate direct veo3.1 API payload (single image reference)"""
        payload = {
            "model": config.model,
            "promptText": config.layered_prompt.to_prompt_text() if config.layered_prompt else "",
            "duration": config.duration
        }
        
        # Add single image reference if available
        if config.primary_subject and config.primary_subject.reference_images:
            payload["promptImage"] = config.primary_subject.reference_images[0]
        
        return payload
    
    def _generate_gen4_composition_prompt(
        self,
        config: Veo31PromptConfig
    ) -> str:
        """Generate gen4_image composition prompt with @tag syntax"""
        if not config.primary_subject:
            return ""
        
        tags = [f"@{config.primary_subject.tag}"]
        for sec in config.secondary_subjects:
            tags.append(f"@{sec.tag}")
        
        # Build composition prompt
        composition = f"A medium shot of {' and '.join(tags)}"
        
        if config.layered_prompt:
            composition += f" in a {config.layered_prompt.cinematography} style"
            composition += f", {config.layered_prompt.environment}"
        
        return composition
    
    def _collect_reference_images(
        self,
        config: Veo31PromptConfig
    ) -> List[Dict[str, Any]]:
        """Collect reference images for gen4_image API"""
        references = []
        
        if config.primary_subject:
            references.append(config.primary_subject.to_reference_dict())
        
        for sec in config.secondary_subjects:
            references.append(sec.to_reference_dict())
        
        return references
    
    def generate_multi_shot_sequence(
        self,
        base_layered_prompt: LayeredPrompt,
        performance_variations: List[str],
        maintain_continuity: bool = True
    ) -> List[LayeredPrompt]:
        """
        Generate multi-shot sequence maintaining continuity.
        
        Pattern: Lock Identity/Cinematography/Environment, vary Performance
        """
        sequence = []
        
        for performance in performance_variations:
            shot_prompt = LayeredPrompt(
                identity=base_layered_prompt.identity,  # Fixed
                cinematography=base_layered_prompt.cinematography,  # Fixed
                environment=base_layered_prompt.environment,  # Fixed
                performance=performance  # Variable
            )
            sequence.append(shot_prompt)
        
        return sequence
    
    def validate_prompt(
        self,
        prompt: str,
        max_length: int = 1000
    ) -> Tuple[bool, List[str]]:
        """
        Validate prompt according to Veo 3.1 constraints.
        
        Returns:
            (is_valid, errors)
        """
        errors = []
        
        if not prompt or not prompt.strip():
            errors.append("Prompt cannot be empty")
        
        if len(prompt) > max_length:
            errors.append(f"Prompt exceeds {max_length} character limit")
        
        # Check for @tag syntax validity
        import re
        tag_pattern = r'@(\w+)'
        tags = re.findall(tag_pattern, prompt)
        for tag in tags:
            if len(tag) < 3 or len(tag) > 16:
                errors.append(f"Tag '{tag}' must be 3-16 characters")
        
        return (len(errors) == 0, errors)
    
    def log_prompt(
        self,
        prompt: str,
        config: Veo31PromptConfig,
        result: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log prompt generation for analysis"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "config": {
                "model": config.model,
                "duration": config.duration,
                "use_workflow": config.use_workflow,
                "workflow_pattern": config.workflow_pattern
            },
            "result": result
        }
        self.prompt_history.append(log_entry)
    
    def export_cdf_format(self) -> Dict[str, Any]:
        """
        Export prompt engine state in CDF (Contextual Data Framework) format.
        
        Pattern: EPISTEMIC × PROMPT × ORCHESTRATION × ONE
        """
        return {
            "metadata": {
                "type": "veo31_prompt_engine",
                "version": "1.0.0",
                "pattern": "EPISTEMIC × PROMPT × ORCHESTRATION × ONE",
                "timestamp": datetime.now().isoformat()
            },
            "character_bibles": {
                name: {
                    "name": bible.name,
                    "tag": bible.tag,
                    "wardrobe": bible.wardrobe,
                    "physical_description": bible.physical_description,
                    "reference_images": bible.reference_images,
                    "metadata": bible.metadata
                }
                for name, bible in self.character_bibles.items()
            },
            "prompt_history": self.prompt_history[-100:],  # Last 100 entries
            "epistemic_foundations": {
                "cof_reasoning": "Chain-of-Frames visual reasoning",
                "identity_anchoring": "Character Bible methodology",
                "layered_prompting": "REPLACE_ME",
                "orchestration": "Runway Workflows for multi-subject integration"
            }
        }


# Factory functions for common patterns

def create_character_bible(
    name: str,
    tag: str,
    physical_description: str,
    wardrobe: str = "",
    reference_images: List[str] = None
) -> CharacterBible:
    """Factory: Create Character Bible"""
    return CharacterBible(
        name=name,
        tag=tag,
        physical_description=physical_description,
        wardrobe=wardrobe,
        reference_images=reference_images or []
    )


def create_directors_prompt(
    identity: str,
    cinematography: str,
    environment: str,
    performance: str
) -> LayeredPrompt:
    """Factory: Create Director's Formula prompt"""
    return LayeredPrompt(
        identity=identity,
        cinematography=cinematography,
        environment=environment,
        performance=performance
    )


def create_multi_subject_config(
    primary: CharacterBible,
    secondaries: List[CharacterBible],
    layered_prompt: LayeredPrompt,
    model: str = "veo3.1",
    duration: int = 5
) -> Veo31PromptConfig:
    """Factory: Create multi-subject configuration"""
    return Veo31PromptConfig(
        model=model,
        duration=duration,
        primary_subject=primary,
        secondary_subjects=secondaries,
        layered_prompt=layered_prompt,
        use_workflow=True,
        workflow_pattern="gen4_image_to_veo31"
    )

