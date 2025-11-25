"""
Badge System
Pattern: GAMIFICATION × BADGES × ONE
"""

from typing import Dict, List, Optional
from config.settings import BADGE_EMOJIS

class Badge:
    """Badge definition"""
    
    def __init__(
        self,
        badge_id: str,
        name: str,
        description: str,
        emoji: str,
        rarity: str = 'common'  # common, rare, epic, legendary
    ):
        self.badge_id = badge_id
        self.name = name
        self.description = description
        self.emoji = emoji
        self.rarity = rarity
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'badge_id': self.badge_id,
            'name': self.name,
            'description': self.description,
            'emoji': self.emoji,
            'rarity': self.rarity,
        }

class BadgeManager:
    """Badge manager"""
    
    def __init__(self):
        self.badges = self._initialize_badges()
    
    def _initialize_badges(self) -> Dict[str, Badge]:
        """Initialize all badges"""
        badges = {}
        
        # Onboarding Badges
        badges['first_quest'] = Badge(
            badge_id='first_quest',
            name='First Quest',
            description='Completed your first quest!',
            emoji=BADGE_EMOJIS.get('first_quest', ''),
            rarity='common'
        )
        
        badges['identity_discovered'] = Badge(
            badge_id='identity_discovered',
            name='Identity Discovered',
            description='Unlocked your true personality!',
            emoji='',
            rarity='rare'
        )
        
        badges['first_badge'] = Badge(
            badge_id='first_badge',
            name='First Badge',
            description='Earned your first badge!',
            emoji=BADGE_EMOJIS.get('first_badge', ''),
            rarity='common'
        )
        
        # Level Badges
        badges['level_10'] = Badge(
            badge_id='level_10',
            name='Level 10',
            description='Reached level 10!',
            emoji=BADGE_EMOJIS.get('level_10', ''),
            rarity='rare'
        )
        
        # Quest Badges
        badges['quest_master'] = Badge(
            badge_id='quest_master',
            name='Quest Master',
            description='Completed 10 quests!',
            emoji=BADGE_EMOJIS.get('quest_master', ''),
            rarity='epic'
        )
        
        # Social Badges
        badges['social_butterfly'] = Badge(
            badge_id='social_butterfly',
            name='Social Butterfly',
            description='Made 50 reactions!',
            emoji=BADGE_EMOJIS.get('social_butterfly', ''),
            rarity='rare'
        )
        
        # Time-based Badges
        badges['night_owl'] = Badge(
            badge_id='night_owl',
            name='Night Owl',
            description='Active after midnight!',
            emoji=BADGE_EMOJIS.get('night_owl', ''),
            rarity='common'
        )
        
        badges['early_bird'] = Badge(
            badge_id='early_bird',
            name='Early Bird',
            description='Active before 6 AM!',
            emoji=BADGE_EMOJIS.get('early_bird', ''),
            rarity='common'
        )
        
        return badges
    
    def get_badge(self, badge_id: str) -> Optional[Badge]:
        """Get badge by ID"""
        return self.badges.get(badge_id)
    
    def get_all_badges(self) -> List[Badge]:
        """Get all badges"""
        return list(self.badges.values())
    
    def check_badge_unlock(self, badge_id: str, user_stats: Dict) -> bool:
        """Check if badge should be unlocked"""
        badge = self.get_badge(badge_id)
        if not badge:
            return False
        
        # Badge-specific unlock logic
        if badge_id == 'level_10':
            return user_stats.get('level', 0) >= 10
        elif badge_id == 'quest_master':
            return user_stats.get('completed_quests', 0) >= 10
        elif badge_id == 'social_butterfly':
            return user_stats.get('reactions', 0) >= 50
        
        return False

# Global instance
badge_manager = BadgeManager()

