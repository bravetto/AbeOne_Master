"""
Personalization Engine - AI-Powered Identity Formation
Pattern: PERSONALIZATION × AI × IDENTITY × ONE
"""

from typing import Dict, List, Optional, Any
import random
from config.settings import TRAIT_DETECTION_THRESHOLD

class PersonalityType:
    """Identity roles"""
    CREATIVE_WARRIOR = "Creative Warrior"
    SYSTEMS_WIZARD = "Systems Wizard"
    QUIET_ASSASSIN = "Quiet Assassin"
    INFLUENCE_ARCHITECT = "Influence Architect"
    VISION_BUILDER = "Vision Builder"
    MOMENTUM_BEAST = "Momentum Beast"

class PersonalizationEngine:
    """AI-powered personalization engine"""
    
    def __init__(self):
        self.personality_questions = self._initialize_questions()
        self.trait_mappings = self._initialize_trait_mappings()
    
    def _initialize_questions(self) -> List[Dict[str, Any]]:
        """Initialize 5-question Greatness Sprint
        
        Role Assignment Rules:
        - Q1 (Passions) → Archetype
        - Q2 (Talents) → Role
        - Q3 (Vibes) → Color
        - Q4 (Intentions) → Pathway
        """
        return [
            {
                'id': 'q1',
                'question': 'What fuels you?',  # Passions → Archetype
                'options': [
                    {'text': '🔥 Creating', 'archetype': 'creative_warrior', 'roles': {'creative_warrior': 0.9}},
                    {'text': '🧠 Solving', 'archetype': 'systems_wizard', 'roles': {'systems_wizard': 0.9}},
                    {'text': '🤝 Connecting', 'archetype': 'influence_architect', 'roles': {'influence_architect': 0.9}},
                    {'text': '⚔️ Competing', 'archetype': 'quiet_assassin', 'roles': {'quiet_assassin': 0.9}},
                    {'text': '🚀 Building', 'archetype': 'vision_builder', 'roles': {'vision_builder': 0.7, 'momentum_beast': 0.6}},
                ]
            },
            {
                'id': 'q2',
                'question': 'Your natural talent?',  # Talents → Role
                'options': [
                    {'text': '🎨 Creativity', 'role': 'creative_warrior', 'roles': {'creative_warrior': 0.9}},
                    {'text': '🧩 Systems Thinking', 'role': 'systems_wizard', 'roles': {'systems_wizard': 0.9}},
                    {'text': '🐉 Leadership', 'role': 'influence_architect', 'roles': {'influence_architect': 0.9}},
                    {'text': '🔧 Craftsmanship', 'role': 'vision_builder', 'roles': {'vision_builder': 0.9}},
                    {'text': '🌪 Execution Speed', 'role': 'momentum_beast', 'roles': {'momentum_beast': 0.9}},
                ]
            },
            {
                'id': 'q3',
                'question': 'Your social vibe?',  # Vibes → Color
                'options': [
                    {'text': '🌞 Outgoing', 'vibe': 'influence_architect', 'roles': {'influence_architect': 0.9}},
                    {'text': '🌙 Quiet Assassin', 'vibe': 'quiet_assassin', 'roles': {'quiet_assassin': 0.9}},
                    {'text': '⚡ High-Energy', 'vibe': 'momentum_beast', 'roles': {'momentum_beast': 0.9}},
                    {'text': '🍃 Calm Strategist', 'vibe': 'systems_wizard', 'roles': {'systems_wizard': 0.9}},
                ]
            },
            {
                'id': 'q4',
                'question': 'Why are you here?',  # Intentions → Pathway
                'options': [
                    {'text': '👑 Level Up', 'pathway': 'vision_builder', 'roles': {'vision_builder': 0.9}},
                    {'text': '💸 Business', 'pathway': 'momentum_beast', 'roles': {'momentum_beast': 0.9}},
                    {'text': '🧬 Mind Expansion', 'pathway': 'systems_wizard', 'roles': {'systems_wizard': 0.9}},
                    {'text': '⚙️ Tools + Systems', 'pathway': 'systems_wizard', 'roles': {'systems_wizard': 0.9}},
                    {'text': '🎭 Fun + Chaos', 'pathway': 'creative_warrior', 'roles': {'creative_warrior': 0.9}},
                ]
            },
            {
                'id': 'q5',
                'question': 'How do you want to grow?',
                'options': [
                    {'text': '🏆 Mastery', 'roles': {'vision_builder': 0.8, 'quiet_assassin': 0.7}},
                    {'text': '🧗‍♂️ Confidence', 'roles': {'influence_architect': 0.8, 'momentum_beast': 0.7}},
                    {'text': '💡 Creativity', 'roles': {'creative_warrior': 0.9}},
                    {'text': '🧠 Intelligence', 'roles': {'systems_wizard': 0.9}},
                    {'text': '🔥 Discipline', 'roles': {'momentum_beast': 0.8, 'vision_builder': 0.7}},
                    {'text': '💰 Income', 'roles': {'momentum_beast': 0.9, 'influence_architect': 0.6}},
                ]
            },
        ]
    
    def _initialize_trait_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Initialize identity role mappings"""
        return {
            'creative_warrior': {
                'personality': PersonalityType.CREATIVE_WARRIOR,
                'role': 'creative_warrior',
                'color': 0xff5a5a,  # "#ff5a5a"
                'emoji': '🔥',
                'description': 'You create. You express. You innovate. You fight for your vision.',
            },
            'systems_wizard': {
                'personality': PersonalityType.SYSTEMS_WIZARD,
                'role': 'systems_wizard',
                'color': 0x5ac7ff,  # "#5ac7ff"
                'emoji': '⚡',
                'description': 'You think in systems. You see patterns. You optimize everything.',
            },
            'quiet_assassin': {
                'personality': PersonalityType.QUIET_ASSASSIN,
                'role': 'quiet_assassin',
                'color': 0x8a8a8a,  # "#8a8a8a"
                'emoji': '🌙',
                'description': 'You move in silence. You strike with precision. You win quietly.',
            },
            'influence_architect': {
                'personality': PersonalityType.INFLUENCE_ARCHITECT,
                'role': 'influence_architect',
                'color': 0xffcc33,  # "#ffcc33"
                'emoji': '👑',
                'description': 'You build influence. You connect people. You architect networks.',
            },
            'vision_builder': {
                'personality': PersonalityType.VISION_BUILDER,
                'role': 'vision_builder',
                'color': 0x7aff7a,  # "#7aff7a"
                'emoji': '🐉',
                'description': 'You build visions. You craft excellence. You create legacies.',
            },
            'momentum_beast': {
                'personality': PersonalityType.MOMENTUM_BEAST,
                'role': 'momentum_beast',
                'color': 0xff7af5,  # "#ff7af5"
                'emoji': '🚀',
                'description': 'You move fast. You execute hard. You build momentum.',
            },
        }
    
    def get_question(self, question_id: str) -> Optional[Dict[str, Any]]:
        """Get question by ID"""
        for q in self.personality_questions:
            if q['id'] == question_id:
                return q
        return None
    
    def get_next_question(self, answered_questions: List[str]) -> Optional[Dict[str, Any]]:
        """Get next unanswered question"""
        for q in self.personality_questions:
            if q['id'] not in answered_questions:
                return q
        return None
    
    def analyze_responses(self, responses: Dict[str, int]) -> Dict[str, Any]:
        """Analyze user responses using role assignment rules
        
        Rules:
        - Q1 (Passions) → Archetype
        - Q2 (Talents) → Role
        - Q3 (Vibes) → Color
        - Q4 (Intentions) → Pathway
        """
        role_scores = {
            'creative_warrior': 0.0,
            'systems_wizard': 0.0,
            'quiet_assassin': 0.0,
            'influence_architect': 0.0,
            'vision_builder': 0.0,
            'momentum_beast': 0.0,
        }
        
        # Track assignment rules
        archetype = None  # Q1
        role = None  # Q2
        vibe = None  # Q3
        pathway = None  # Q4
        
        # Aggregate role scores from responses
        for question_id, option_index in responses.items():
            question = self.get_question(question_id)
            if question and 0 <= option_index < len(question['options']):
                option = question['options'][option_index]
                
                # Q1: Passions → Archetype
                if question_id == 'q1' and 'archetype' in option:
                    archetype = option['archetype']
                    role_scores[archetype] += 1.0  # Strong weight for archetype
                
                # Q2: Talents → Role
                elif question_id == 'q2' and 'role' in option:
                    role = option['role']
                    role_scores[role] += 1.0  # Strong weight for role
                
                # Q3: Vibes → Color (affects visual, but also role)
                elif question_id == 'q3' and 'vibe' in option:
                    vibe = option['vibe']
                    role_scores[vibe] += 0.7  # Medium weight for vibe
                
                # Q4: Intentions → Pathway
                elif question_id == 'q4' and 'pathway' in option:
                    pathway = option['pathway']
                    role_scores[pathway] += 0.8  # Medium-high weight for pathway
                
                # Q5: Growth goals (supports all roles)
                elif question_id == 'q5' and 'roles' in option:
                    for role_name, value in option['roles'].items():
                        role_scores[role_name] += value * 0.5  # Lower weight for growth
                
                # Fallback: use 'roles' if present
                elif 'roles' in option:
                    for role_name, value in option['roles'].items():
                        role_scores[role_name] += value
        
        # Determine dominant role
        dominant_role = max(role_scores.items(), key=lambda x: x[1])
        
        # Normalize scores
        total = sum(role_scores.values())
        if total > 0:
            role_scores = {k: v / total for k, v in role_scores.items()}
        
        # Get role mapping
        personality_type = self.trait_mappings[dominant_role[0]]
        
        # Determine role stack (top 3 roles)
        sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
        role_stack = [role_name for role_name, score in sorted_roles[:3] if score > 0.1]
        
        return {
            'personality_type': personality_type['personality'],
            'personality_role': personality_type['role'],
            'role_stack': role_stack,  # Multiple roles
            'personality_color': personality_type['color'],
            'personality_emoji': personality_type['emoji'],
            'personality_description': personality_type['description'],
            'trait_scores': role_scores,  # Renamed for consistency
            'confidence': dominant_role[1],
            'archetype': archetype,  # Q1 result
            'role': role,  # Q2 result
            'vibe': vibe,  # Q3 result
            'pathway': pathway,  # Q4 result
        }
    
    def generate_personality_reveal(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personality reveal message"""
        # Build role stack description
        role_stack = analysis.get('role_stack', [])
        role_descriptions = []
        
        # Primary role
        primary_role = self.trait_mappings.get(role_stack[0] if role_stack else analysis['personality_role'], {})
        role_descriptions.append(primary_role.get('personality', analysis['personality_type']))
        
        # Secondary roles (energy/vibes)
        if len(role_stack) > 1:
            for role_name in role_stack[1:]:
                if role_name in self.trait_mappings:
                    role_info = self.trait_mappings[role_name]
                    # Use emoji or short description
                    role_descriptions.append(f"{role_info.get('emoji', '')} {role_info.get('personality', role_name)}")
        
        role_text = " with ".join(role_descriptions[:3]) if len(role_descriptions) > 1 else role_descriptions[0]
        
        return {
            'title': f"{analysis['personality_emoji']} **ROLE DROP**",
            'description': f"Ohhhhhh SHIT.\n\nYou're a {role_text}.\n\nThis server has been waiting for someone like you.",
            'color': analysis['personality_color'],
        }
    
    def recommend_quest(self, personality_type: str, completed_quests: List[str]) -> Optional[str]:
        """Recommend quest based on personality"""
        # Simple recommendation logic
        # In production, this would be more sophisticated
        if 'welcome_001' not in completed_quests:
            return 'welcome_001'
        elif 'personality_001' not in completed_quests:
            return 'personality_001'
        elif 'exploration_001' not in completed_quests:
            return 'exploration_001'
        return None
    
    def generate_welcome_message(self, username: str) -> Dict[str, Any]:
        """Generate personalized welcome message"""
        return {
            'title': "🔥 **WELCOME TO THE GREATNESSZONE 🔥**",
            'description': "You're 1 click away from discovering your inner archetype.",
            'color': 0xff00ff,
        }
    
    def generate_energy_scan_message(self, username: str) -> Dict[str, Any]:
        """Generate energy scan message"""
        return {
            'title': "⚡ **Energy Scan**",
            'description': "Initializing scan…\n\nCalibrating greatness…\n\nHold tight… this might tingle 👀",
            'color': 0x00ffff,
        }
    
    def generate_ai_profile(self, username: str, analysis: Dict[str, Any], role_stack: List[str]) -> Dict[str, Any]:
        """Generate AI-powered personal profile"""
        # Generate profile based on roles
        top_role = max(analysis['trait_scores'].items(), key=lambda x: x[1])
        
        profile_texts = {
            'creative_warrior': f"**{username}** is a **Creative Warrior** 🔥 - You create, express, and innovate. "
                               f"You fight for your vision and bring beauty into the world. "
                               f"Your strength lies in creative expression and artistic innovation.",
            'systems_wizard': f"**{username}** is a **Systems Wizard** ⚡ - You think in systems and see patterns. "
                            f"You optimize everything and understand complex structures. "
                            f"Your strength lies in analytical thinking and systematic optimization.",
            'quiet_assassin': f"**{username}** is a **Quiet Assassin** 🌙 - You move in silence and strike with precision. "
                            f"You win quietly and execute flawlessly. "
                            f"Your strength lies in strategic execution and quiet excellence.",
            'influence_architect': f"**{username}** is an **Influence Architect** 👑 - You build influence and connect people. "
                                  f"You architect networks and create impact through relationships. "
                                  f"Your strength lies in building connections and creating influence.",
            'vision_builder': f"**{username}** is a **Vision Builder** 🐉 - You build visions and craft excellence. "
                            f"You create legacies and turn dreams into reality. "
                            f"Your strength lies in long-term thinking and masterful execution.",
            'momentum_beast': f"**{username}** is a **Momentum Beast** 🚀 - You move fast and execute hard. "
                            f"You build momentum and get things done at incredible speed. "
                            f"Your strength lies in rapid execution and unstoppable momentum.",
        }
        
        role_names = [self.trait_mappings[r]['personality'] for r in role_stack[:3] if r in self.trait_mappings]
        
        return {
            'title': f"📊 **{username}'s AI-Generated Profile**",
            'description': profile_texts.get(top_role[0], f"**{username}** is unique and powerful!"),
            'color': analysis['personality_color'],
            'fields': [
                {
                    'name': 'Role Stack',
                    'value': ' → '.join(role_names) if role_names else analysis['personality_type'],
                    'inline': False
                },
                {
                    'name': 'Top Roles',
                    'value': '\n'.join([
                        f"{self.trait_mappings[t]['emoji']} {self.trait_mappings[t]['personality']}: {int(s * 100)}%"
                        for t, s in sorted(analysis['trait_scores'].items(), key=lambda x: x[1], reverse=True)[:3]
                        if t in self.trait_mappings
                    ]),
                    'inline': False
                }
            ]
        }

# Global instance
personalization_engine = PersonalizationEngine()

