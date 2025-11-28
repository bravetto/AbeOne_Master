"""
Configuration Settings
Pattern: CONFIG × SETTINGS × ONE
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', '0'))  # Optional: specific guild

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///onboarding.db')

# Onboarding Configuration
ONBOARDING_TIMEOUT = 60  # 60 seconds hook target
QUEST_TIMEOUT = 300  # 5 minutes for quest completion

# Gamification Configuration
POINTS_WELCOME = 10
POINTS_QUEST_COMPLETE = 50
POINTS_BADGE_UNLOCK = 25
POINTS_DAILY_LOGIN = 5

# NPC Configuration
NPC_RESPONSE_DELAY = 1.5  # Seconds between NPC messages (for cinematic effect)

# Personalization Configuration
TRAIT_DETECTION_THRESHOLD = 0.7  # Confidence threshold for trait detection

# Role Configuration - Identity Engine Colors
ROLE_COLORS = {
    'creative_warrior': 0xff5a5a,      # "#ff5a5a" - Red/Pink
    'systems_wizard': 0x5ac7ff,        # "#5ac7ff" - Blue/Cyan
    'quiet_assassin': 0x8a8a8a,        # "#8a8a8a" - Gray
    'influence_architect': 0xffcc33,   # "#ffcc33" - Yellow/Gold
    'vision_builder': 0x7aff7a,        # "#7aff7a" - Green
    'momentum_beast': 0xff7af5,        # "#ff7af5" - Magenta/Pink
    'novice': 0x808080,                # Gray
    'veteran': 0xffd700,               # Gold
}

# Badge Emojis
BADGE_EMOJIS = {
    'first_quest': '',
    'first_badge': '',
    'level_10': '',
    'quest_master': '',
    'social_butterfly': '',
    'night_owl': '',
    'early_bird': '',
}

