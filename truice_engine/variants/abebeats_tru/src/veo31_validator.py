"""
Veo 3.1 Prompt Engineering Validator
Epistemic Validation & Pattern Analysis

Validates:
- Prompt structure and constraints
- Character Bible completeness
- Layered Prompt consistency
- Workflow pattern correctness
- Epistemic foundation alignment

Pattern: VALIDATE × EPISTEMIC × PATTERN × ONE
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import logging

from .veo31_prompt_engine import (
    Veo31PromptEngine,
    CharacterBible,
    LayeredPrompt,
    Veo31PromptConfig
)

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Validation result"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    recommendations: List[str]
    score: float  # 0.0 - 1.0


class Veo31Validator:
    """
    Veo 3.1 Prompt Engineering Validator
    
    Validates prompts against:
    - Veo 3.1 API constraints
    - Epistemic foundations
    - Best practices
    - Pattern consistency
    """
    
    def __init__(self):
        """Initialize validator"""
        self.logger = logging.getLogger(f"{__name__}.Veo31Validator")
    
    def validate_character_bible(
        self,
        bible: CharacterBible
    ) -> ValidationResult:
        """
        Validate Character Bible completeness.
        
        Checks:
        - Required fields present
        - Tag format (3-16 chars)
        - Reference images available
        - Physical description provided
        """
        errors = []
        warnings = []
        recommendations = []
        
        # Required fields
        if not bible.name:
            errors.append("Character Bible name is required")
        
        if not bible.tag:
            errors.append("Character Bible tag is required")
        elif len(bible.tag) < 3 or len(bible.tag) > 16:
            errors.append(f"Tag '{bible.tag}' must be 3-16 characters")
        
        if not bible.physical_description:
            warnings.append("Physical description missing - may cause identity drift")
        
        if not bible.reference_images:
            warnings.append("No reference images provided - identity anchoring may be weak")
        elif len(bible.reference_images) < 2:
            recommendations.append("Consider adding 2-3 reference images for better identity anchoring")
        
        if not bible.wardrobe:
            warnings.append("Wardrobe description missing - may cause consistency issues")
        
        # Score calculation
        score = 1.0
        score -= len(errors) * 0.3
        score -= len(warnings) * 0.1
        score = max(0.0, score)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            recommendations=recommendations,
            score=score
        )
    
    def validate_layered_prompt(
        self,
        prompt: LayeredPrompt,
        check_continuity: bool = False,
        previous_prompt: Optional[LayeredPrompt] = None
    ) -> ValidationResult:
        """
        Validate Layered Prompt structure and consistency.
        
        Checks:
        - All layers present
        - Layer content quality
        - Continuity with previous prompt (if provided)
        """
        errors = []
        warnings = []
        recommendations = []
        
        # Check all layers present
        if not prompt.identity:
            errors.append("Identity layer is required (fixed axiom)")
        
        if not prompt.cinematography:
            warnings.append("Cinematography layer missing - visual continuity may suffer")
        
        if not prompt.environment:
            warnings.append("Environment layer missing - spatial consistency may suffer")
        
        if not prompt.performance:
            errors.append("Performance layer is required (variable action)")
        
        # Check layer quality
        if prompt.identity and len(prompt.identity) < 10:
            warnings.append("Identity layer seems too short - may not provide sufficient anchoring")
        
        if prompt.performance and len(prompt.performance) < 10:
            warnings.append("Performance layer seems too short - action may be unclear")
        
        # Check continuity if previous prompt provided
        if check_continuity and previous_prompt:
            if prompt.identity != previous_prompt.identity:
                errors.append("Identity layer changed - violates fixed axiom principle")
            
            if prompt.cinematography != previous_prompt.cinematography:
                warnings.append("Cinematography layer changed - may break visual continuity")
            
            if prompt.environment != previous_prompt.environment:
                warnings.append("Environment layer changed - may break spatial consistency")
        
        # Check prompt length
        full_prompt = prompt.to_prompt_text()
        if len(full_prompt) > 1000:
            errors.append(f"Prompt exceeds 1000 character limit ({len(full_prompt)} chars)")
        
        # Score calculation
        score = 1.0
        score -= len(errors) * 0.3
        score -= len(warnings) * 0.1
        score = max(0.0, score)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            recommendations=recommendations,
            score=score
        )
    
    def validate_prompt_text(
        self,
        prompt: str,
        max_length: int = 1000
    ) -> ValidationResult:
        """
        Validate prompt text against Veo 3.1 constraints.
        
        Checks:
        - Length constraints
        - @tag syntax validity
        - Basic structure
        """
        errors = []
        warnings = []
        recommendations = []
        
        if not prompt or not prompt.strip():
            errors.append("Prompt cannot be empty")
            return ValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                recommendations=recommendations,
                score=0.0
            )
        
        if len(prompt) > max_length:
            errors.append(f"Prompt exceeds {max_length} character limit ({len(prompt)} chars)")
        
        # Check @tag syntax
        import re
        tag_pattern = r'@(\w+)'
        tags = re.findall(tag_pattern, prompt)
        
        for tag in tags:
            if len(tag) < 3:
                errors.append(f"Tag '@{tag}' is too short (minimum 3 characters)")
            elif len(tag) > 16:
                errors.append(f"Tag '@{tag}' is too long (maximum 16 characters)")
        
        if tags and len(tags) > 3:
            warnings.append(f"Using {len(tags)} tags - ensure all Character Bibles are registered")
        
        # Check for Director's Formula elements
        director_elements = ["shot", "camera", "lighting", "angle", "movement"]
        found_elements = [elem for elem in director_elements if elem.lower() in prompt.lower()]
        if not found_elements:
            recommendations.append("Consider adding cinematography elements (camera, lighting, angle)")
        
        # Score calculation
        score = 1.0
        score -= len(errors) * 0.3
        score -= len(warnings) * 0.1
        score = max(0.0, score)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            recommendations=recommendations,
            score=score
        )
    
    def validate_workflow_config(
        self,
        config: Veo31PromptConfig
    ) -> ValidationResult:
        """
        Validate Workflow configuration.
        
        Checks:
        - Multi-subject setup correctness
        - Workflow pattern validity
        - API constraints
        """
        errors = []
        warnings = []
        recommendations = []
        
        if config.use_workflow:
            if not config.primary_subject:
                errors.append("Primary subject required for workflow")
            
            if not config.secondary_subjects:
                warnings.append("No secondary subjects - workflow may be unnecessary")
            
            if config.workflow_pattern not in ["gen4_image_to_veo31", "multi_model_chain"]:
                warnings.append(f"Unknown workflow pattern: {config.workflow_pattern}")
            
            # Validate Character Bibles
            if config.primary_subject:
                primary_validation = self.validate_character_bible(config.primary_subject)
                if not primary_validation.is_valid:
                    errors.extend([f"Primary subject: {e}" for e in primary_validation.errors])
                warnings.extend([f"Primary subject: {w}" for w in primary_validation.warnings])
            
            for i, sec in enumerate(config.secondary_subjects):
                sec_validation = self.validate_character_bible(sec)
                if not sec_validation.is_valid:
                    errors.extend([f"Secondary subject {i+1}: {e}" for e in sec_validation.errors])
                warnings.extend([f"Secondary subject {i+1}: {w}" for w in sec_validation.warnings])
        
        # Validate model selection
        if config.model not in ["veo3", "veo3.1", "veo3.1_fast"]:
            warnings.append(f"Unknown model: {config.model}")
        
        # Validate duration
        if config.duration < 2 or config.duration > 10:
            errors.append(f"Duration {config.duration} is outside valid range (2-10 seconds)")
        
        # Score calculation
        score = 1.0
        score -= len(errors) * 0.3
        score -= len(warnings) * 0.1
        score = max(0.0, score)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            recommendations=recommendations,
            score=score
        )
    
    def validate_multi_shot_sequence(
        self,
        sequence: List[LayeredPrompt]
    ) -> ValidationResult:
        """
        Validate multi-shot sequence for continuity.
        
        Checks:
        - Identity layer consistency
        - Cinematography consistency
        - Environment consistency
        - Performance layer variation
        """
        errors = []
        warnings = []
        recommendations = []
        
        if not sequence:
            errors.append("Sequence cannot be empty")
            return ValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                recommendations=recommendations,
                score=0.0
            )
        
        if len(sequence) < 2:
            warnings.append("Sequence has only one shot - continuity check not applicable")
        
        # Check consistency across shots
        first_prompt = sequence[0]
        identity_changes = 0
        cinematography_changes = 0
        environment_changes = 0
        
        for i, prompt in enumerate(sequence[1:], start=1):
            if prompt.identity != first_prompt.identity:
                errors.append(f"Shot {i+1}: Identity layer changed - violates fixed axiom")
                identity_changes += 1
            
            if prompt.cinematography != first_prompt.cinematography:
                warnings.append(f"Shot {i+1}: Cinematography layer changed - may break visual continuity")
                cinematography_changes += 1
            
            if prompt.environment != first_prompt.environment:
                warnings.append(f"Shot {i+1}: Environment layer changed - may break spatial consistency")
                environment_changes += 1
        
        # Check performance variation
        performances = [p.performance for p in sequence]
        if len(set(performances)) < len(performances) * 0.5:
            warnings.append("Performance layers show limited variation - sequence may be repetitive")
        
        # Score calculation
        score = 1.0
        score -= identity_changes * 0.5  # Identity changes are critical
        score -= cinematography_changes * 0.2
        score -= environment_changes * 0.2
        score = max(0.0, score)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            recommendations=recommendations,
            score=score
        )

