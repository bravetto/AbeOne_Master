"""
Artifact System - Choose Your Item
Pattern: GAMIFICATION × ARTIFACTS × ONE
"""

from typing import Dict, List, Optional
from enum import Enum

class ArtifactType(Enum):
    WEAPON = "weapon"
    TOOL = "tool"
    COMPANION = "companion"
    POWER = "power"

class Artifact:
    """Artifact definition"""
    
    def __init__(
        self,
        artifact_id: str,
        name: str,
        description: str,
        emoji: str,
        artifact_type: ArtifactType,
        role: Optional[str] = None,
        role_emoji: Optional[str] = None,
        perk: Optional[str] = None,
        bonus_trait: Optional[str] = None,
        bonus_points: int = 0
    ):
        self.artifact_id = artifact_id
        self.name = name
        self.description = description
        self.emoji = emoji
        self.artifact_type = artifact_type
        self.role = role  # Associated role name
        self.role_emoji = role_emoji  # Role emoji
        self.perk = perk  # Perk description
        self.bonus_trait = bonus_trait
        self.bonus_points = bonus_points
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'artifact_id': self.artifact_id,
            'name': self.name,
            'description': self.description,
            'emoji': self.emoji,
            'artifact_type': self.artifact_type.value,
            'role': self.role,
            'role_emoji': self.role_emoji,
            'perk': self.perk,
            'bonus_trait': self.bonus_trait,
            'bonus_points': self.bonus_points,
        }

class ArtifactManager:
    """Artifact manager"""
    
    def __init__(self):
        self.artifacts = self._initialize_artifacts()
    
    def _initialize_artifacts(self) -> Dict[str, Artifact]:
        """Initialize all artifacts"""
        artifacts = {}
        
        # Core Artifacts with Roles and Perks
        artifacts['sword_of_progress'] = Artifact(
            artifact_id='sword_of_progress',
            name='Sword of Progress',
            description='Cut through obstacles. Build daily discipline. Progress Knight power!',
            emoji='🗡️',
            artifact_type=ArtifactType.WEAPON,
            role='Progress Knight',
            role_emoji='🗡',
            perk='+Daily Discipline',
            bonus_trait='vision_builder',  # Maps to Vision Builder
            bonus_points=15
        )
        
        artifacts['compass_of_purpose'] = Artifact(
            artifact_id='compass_of_purpose',
            name='Compass of Purpose',
            description='Find your true path. Gain clarity. Pathfinder wisdom!',
            emoji='🧭',
            artifact_type=ArtifactType.TOOL,
            role='Pathfinder',
            role_emoji='🧭',
            perk='+Clarity Drops',
            bonus_trait='influence_architect',  # Maps to Influence Architect
            bonus_points=15
        )
        
        artifacts['gem_of_genius'] = Artifact(
            artifact_id='gem_of_genius',
            name='Gem of Genius',
            description='Unlock AI insights. Expand your mind. Mindsmith mastery!',
            emoji='💎',
            artifact_type=ArtifactType.POWER,
            role='Mindsmith',
            role_emoji='💎',
            perk='+AI Insights',
            bonus_trait='systems_wizard',  # Maps to Systems Wizard
            bonus_points=15
        )
        
        artifacts['torch_of_momentum'] = Artifact(
            artifact_id='torch_of_momentum',
            name='Torch of Momentum',
            description='Keep the fire burning. Fuel your drive. Momentum Keeper energy!',
            emoji='🔥',
            artifact_type=ArtifactType.POWER,
            role='Momentum Keeper',
            role_emoji='🔥',
            perk='+Motivation Bursts',
            bonus_trait='momentum_beast',  # Maps to Momentum Beast
            bonus_points=15
        )
        
        # Additional Artifacts for variety
        artifacts['brush_of_creation'] = Artifact(
            artifact_id='brush_of_creation',
            name='Brush of Creation',
            description='Channel your creativity. Bring ideas to life!',
            emoji='🖌️',
            artifact_type=ArtifactType.WEAPON,
            bonus_trait='creative_warrior',
            bonus_points=10
        )
        
        artifacts['shadow_blade'] = Artifact(
            artifact_id='shadow_blade',
            name='Shadow Blade',
            description='Strike with precision. Move in silence. Win quietly.',
            emoji='🗡️',
            artifact_type=ArtifactType.WEAPON,
            bonus_trait='quiet_assassin',
            bonus_points=10
        )
        
        return artifacts
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact by ID"""
        return self.artifacts.get(artifact_id)
    
    def get_artifacts_by_trait(self, trait: str) -> List[Artifact]:
        """Get artifacts matching a trait"""
        return [a for a in self.artifacts.values() if a.bonus_trait == trait or a.bonus_trait is None]
    
    def get_recommended_artifacts(self, role_stack: List[str], limit: int = 4) -> List[Artifact]:
        """Get recommended artifacts based on role stack
        
        Prioritizes core artifacts (Sword, Compass, Gem, Torch) based on role stack
        """
        recommended = []
        
        # Core artifacts mapping to roles
        core_artifacts = {
            'vision_builder': 'sword_of_progress',
            'influence_architect': 'compass_of_purpose',
            'systems_wizard': 'gem_of_genius',
            'momentum_beast': 'torch_of_momentum',
            'creative_warrior': 'brush_of_creation',
            'quiet_assassin': 'shadow_blade',
        }
        
        # Get core artifact for primary role
        if role_stack and role_stack[0] in core_artifacts:
            artifact_id = core_artifacts[role_stack[0]]
            if artifact_id in self.artifacts:
                recommended.append(self.artifacts[artifact_id])
        
        # Get core artifact for secondary role if different
        if len(role_stack) > 1 and role_stack[1] in core_artifacts:
            artifact_id = core_artifacts[role_stack[1]]
            if artifact_id in self.artifacts and artifact_id not in [a.artifact_id for a in recommended]:
                recommended.append(self.artifacts[artifact_id])
        
        # Fill remaining slots with other core artifacts
        all_core = ['sword_of_progress', 'compass_of_purpose', 'gem_of_genius', 'torch_of_momentum']
        for artifact_id in all_core:
            if len(recommended) >= limit:
                break
            if artifact_id in self.artifacts:
                if artifact_id not in [a.artifact_id for a in recommended]:
                    recommended.append(self.artifacts[artifact_id])
        
        return recommended[:limit]

# Global instance
artifact_manager = ArtifactManager()

