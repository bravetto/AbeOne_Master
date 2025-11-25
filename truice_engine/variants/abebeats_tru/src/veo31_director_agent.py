"""
Veo 3.1 LLM Director Agent
Auto-Generate Layered Prompts from High-Level Concepts

Uses SystemPromptBuilder pattern for LLM integration.

Pattern: LLM × DIRECTOR × PROMPT × ONE
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging
import json

from .veo31_prompt_engine import LayeredPrompt, CharacterBible

logger = logging.getLogger(__name__)


@dataclass
class DirectorAgentConfig:
    """Configuration for Director Agent"""
    llm_client: Any  # LLM client (must have chat method)
    system_prompt_builder: Optional[Any] = None  # SystemPromptBuilder instance
    model: str = "gpt-4"  # LLM model to use
    temperature: float = 0.7


class Veo31DirectorAgent:
    """
    LLM Director Agent for Veo 3.1
    
    Automatically generates Layered Prompts from high-level concepts.
    Acts as a "film director" that decomposes concepts into structured prompts.
    
    Pattern: CONCEPT → DECOMPOSE → LAYERED_PROMPT
    """
    
    DIRECTOR_SYSTEM_PROMPT = """You are a professional film director specializing in AI video generation with Veo 3.1.

Your role is to decompose high-level creative concepts into structured, layered prompts that ensure visual consistency and creative control.

## Your Methodology

You use the "Layered Prompting Framework" which divides prompts into four layers:

1. **Identity Layer** (Fixed Axiom - WHO)
   - Defines the subject(s) with precise physical descriptions
   - Must remain consistent across all shots in a sequence
   - Example: "Same female protagonist, early 30s, shoulder-length black hair, wearing a red scarf"

2. **Cinematography Layer** (Fixed Grammar - HOW)
   - Defines camera work, lighting, and visual style
   - Must remain consistent for visual continuity
   - Example: "35mm handheld tracking; golden-hour warm key with soft backlight; shallow depth of field"

3. **Environment Layer** (Fixed Context - WHERE)
   - Defines the setting and spatial context
   - Must remain consistent for spatial coherence
   - Example: "Rain-soaked street, neon signage reflections; maintain teal–orange palette with magenta highlights"

4. **Performance Layer** (Variable - WHAT)
   - Defines the action/performance that changes per shot
   - This is the ONLY layer that should vary significantly between shots
   - Example: "She urgently glances over her shoulder, a single tear tracing her cheek"

## Your Process

When given a high-level concept:
1. Extract the core subject(s) and create Identity Layer
2. Determine appropriate cinematography style and create Cinematography Layer
3. Define the environment/setting and create Environment Layer
4. Specify the action/performance and create Performance Layer

## Output Format

Always output a JSON object with this structure:
{
  "identity": "Precise subject description (fixed axiom)",
  "cinematography": "Camera, lighting, visual style (fixed grammar)",
  "environment": "Setting, spatial context (fixed context)",
  "performance": "Action, performance (variable)"
}

## Important Rules

- Identity, Cinematography, and Environment layers MUST be fixed and reusable across shots
- Only Performance layer should change between shots
- Be specific and detailed - vague descriptions cause identity drift
- Include technical cinematography terms when appropriate
- Consider audio/dialogue if mentioned in the concept
"""

    def __init__(self, config: DirectorAgentConfig):
        """
        Initialize Director Agent.
        
        Args:
            config: DirectorAgentConfig with LLM client
        """
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.Veo31DirectorAgent")
    
    async def generate_layered_prompt(
        self,
        concept: str,
        character_bibles: Optional[List[CharacterBible]] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Optional[LayeredPrompt]:
        """
        Generate Layered Prompt from high-level concept.
        
        Args:
            concept: High-level creative concept
            character_bibles: Optional Character Bibles to reference
            additional_context: Additional context for generation
        
        Returns:
            LayeredPrompt or None if generation failed
        """
        try:
            # Build system prompt
            system_prompt = self.DIRECTOR_SYSTEM_PROMPT
            
            # Add Character Bible context if provided
            if character_bibles:
                bible_context = "\n## Available Character Bibles:\n"
                for bible in character_bibles:
                    bible_context += f"- {bible.name} ({bible.tag}): {bible.physical_description}\n"
                    if bible.wardrobe:
                        bible_context += f"  Wardrobe: {bible.wardrobe}\n"
                system_prompt += bible_context
            
            # Build user prompt
            user_prompt = f"Generate a layered prompt for this concept:\n\n{concept}\n\n"
            
            if additional_context:
                user_prompt += "\nAdditional Context:\n"
                for key, value in additional_context.items():
                    user_prompt += f"- {key}: {value}\n"
            
            user_prompt += "\nOutput the layered prompt as JSON."
            
            # Call LLM
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Use SystemPromptBuilder if available
            if self.config.system_prompt_builder:
                try:
                    enhanced_system = await self.config.system_prompt_builder.build_system_prompt(
                        include_constitution=True,
                        include_rules=True,
                        include_instructions=True
                    )
                    messages[0]["content"] = f"{enhanced_system}\n\n{system_prompt}"
                except Exception as e:
                    self.logger.warning(f"Could not enhance system prompt: {e}")
            
            # Call LLM
            response = await self.config.llm_client.chat(
                messages=messages,
                model=self.config.model,
                temperature=self.config.temperature
            )
            
            # Parse response
            content = response.get("content", "") if isinstance(response, dict) else str(response)
            
            # Extract JSON from response
            json_str = self._extract_json(content)
            if not json_str:
                self.logger.error("Could not extract JSON from LLM response")
                return None
            
            prompt_data = json.loads(json_str)
            
            # Create LayeredPrompt
            return LayeredPrompt(
                identity=prompt_data.get("identity", ""),
                cinematography=prompt_data.get("cinematography", ""),
                environment=prompt_data.get("environment", ""),
                performance=prompt_data.get("performance", "")
            )
        
        except Exception as e:
            self.logger.error(f"Failed to generate layered prompt: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return None
    
    async def generate_multi_shot_sequence(
        self,
        base_concept: str,
        shot_descriptions: List[str],
        character_bibles: Optional[List[CharacterBible]] = None
    ) -> List[LayeredPrompt]:
        """
        Generate multi-shot sequence maintaining continuity.
        
        Args:
            base_concept: Base concept for the sequence
            shot_descriptions: List of shot-specific actions
            character_bibles: Optional Character Bibles
        
        Returns:
            List of LayeredPrompts with fixed Identity/Cinematography/Environment
        """
        # Generate base layered prompt
        base_prompt = await self.generate_layered_prompt(
            base_concept,
            character_bibles
        )
        
        if not base_prompt:
            return []
        
        # Generate sequence with fixed layers
        sequence = []
        for shot_desc in shot_descriptions:
            # Generate performance layer for this shot
            performance_prompt = await self.generate_layered_prompt(
                f"{base_concept}. Shot action: {shot_desc}",
                character_bibles
            )
            
            if performance_prompt:
                # Use base layers, new performance
                shot_prompt = LayeredPrompt(
                    identity=base_prompt.identity,  # Fixed
                    cinematography=base_prompt.cinematography,  # Fixed
                    environment=base_prompt.environment,  # Fixed
                    performance=performance_prompt.performance  # Variable
                )
                sequence.append(shot_prompt)
        
        return sequence
    
    def _extract_json(self, text: str) -> Optional[str]:
        """Extract JSON from LLM response"""
        # Try to find JSON block
        import re
        
        # Look for ```json blocks
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Look for ``` blocks
        code_match = re.search(r'```\s*(\{.*?\})\s*```', text, re.DOTALL)
        if code_match:
            return code_match.group(1)
        
        # Look for JSON object directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        return None

