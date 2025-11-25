"""
Quest System
Pattern: GAMIFICATION × QUESTS × ONE
"""

from typing import Dict, List, Optional, Any
from enum import Enum

class QuestType(Enum):
    WELCOME = "welcome"
    PERSONALITY = "personality"
    EXPLORATION = "exploration"
    SOCIAL = "social"
    ACHIEVEMENT = "achievement"

class Quest:
    """Quest definition"""
    
    def __init__(
        self,
        quest_id: str,
        name: str,
        description: str,
        quest_type: QuestType,
        reward_points: int,
        reward_badge: Optional[str] = None,
        requirements: Optional[Dict] = None,
        steps: Optional[List[Dict]] = None
    ):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.quest_type = quest_type
        self.reward_points = reward_points
        self.reward_badge = reward_badge
        self.requirements = requirements or {}
        self.steps = steps or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'quest_id': self.quest_id,
            'name': self.name,
            'description': self.description,
            'quest_type': self.quest_type.value,
            'reward_points': self.reward_points,
            'reward_badge': self.reward_badge,
            'requirements': self.requirements,
            'steps': self.steps,
        }

class QuestManager:
    """Quest manager"""
    
    def __init__(self):
        self.quests = self._initialize_quests()
    
    def _initialize_quests(self) -> Dict[str, Quest]:
        """Initialize all quests"""
        quests = {}
        
        # Welcome Quest (First Quest)
        quests['welcome_001'] = Quest(
            quest_id='welcome_001',
            name='Welcome to GreatnessZone™',
            description='Complete your onboarding and discover your identity!',
            quest_type=QuestType.WELCOME,
            reward_points=50,
            reward_badge='first_quest',
            steps=[
                {'step': 1, 'action': 'greet', 'description': 'Meet your Guardian guide'},
                {'step': 2, 'action': 'personality', 'description': 'Discover your personality'},
                {'step': 3, 'action': 'role', 'description': 'Get your first role'},
                {'step': 4, 'action': 'complete', 'description': 'Complete onboarding'},
            ]
        )
        
        # Personality Quest
        quests['personality_001'] = Quest(
            quest_id='personality_001',
            name='Discover Your Identity',
            description='Answer 3 quick questions to unlock your true personality!',
            quest_type=QuestType.PERSONALITY,
            reward_points=25,
            reward_badge='identity_discovered',
            steps=[
                {'step': 1, 'action': 'question_1', 'description': 'Answer question 1'},
                {'step': 2, 'action': 'question_2', 'description': 'Answer question 2'},
                {'step': 3, 'action': 'question_3', 'description': 'Answer question 3'},
                {'step': 4, 'action': 'reveal', 'description': 'See your personality'},
            ]
        )
        
        # Exploration Quest
        quests['exploration_001'] = Quest(
            quest_id='exploration_001',
            name='Explore the Server',
            description='Visit 3 different channels and discover what GreatnessZone™ offers!',
            quest_type=QuestType.EXPLORATION,
            reward_points=30,
            reward_badge='explorer',
            steps=[
                {'step': 1, 'action': 'visit_channel', 'description': 'Visit #general'},
                {'step': 2, 'action': 'visit_channel', 'description': 'Visit #announcements'},
                {'step': 3, 'action': 'visit_channel', 'description': 'Visit #showcase'},
            ]
        )
        
        # Social Quest
        quests['social_001'] = Quest(
            quest_id='social_001',
            name='Make Your First Connection',
            description='React to 5 messages and introduce yourself!',
            quest_type=QuestType.SOCIAL,
            reward_points=20,
            reward_badge='social_butterfly',
            steps=[
                {'step': 1, 'action': 'react', 'description': 'React to 5 messages'},
                {'step': 2, 'action': 'introduce', 'description': 'Introduce yourself'},
            ]
        )
        
        return quests
    
    def get_quest(self, quest_id: str) -> Optional[Quest]:
        """Get quest by ID"""
        return self.quests.get(quest_id)
    
    def get_quests_by_type(self, quest_type: QuestType) -> List[Quest]:
        """Get all quests of a type"""
        return [q for q in self.quests.values() if q.quest_type == quest_type]
    
    def get_welcome_quest(self) -> Quest:
        """Get welcome quest"""
        return self.quests['welcome_001']
    
    def get_personality_quest(self) -> Quest:
        """Get personality quest"""
        return self.quests['personality_001']
    
    def recommend_quest(self, user_traits: List[Dict], completed_quests: List[str]) -> Optional[Quest]:
        """Recommend quest based on user traits"""
        # Filter out completed quests
        available_quests = [q for q in self.quests.values() if q.quest_id not in completed_quests]
        
        if not available_quests:
            return None
        
        # Simple recommendation: return first available quest
        # In production, this would use trait analysis
        return available_quests[0]

# Global instance
quest_manager = QuestManager()

