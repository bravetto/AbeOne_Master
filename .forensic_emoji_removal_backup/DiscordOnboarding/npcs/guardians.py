"""
Guardian NPCs - Interactive Guides
Pattern: NPC × GUARDIAN × ONE
"""

from typing import Dict, List, Optional
import random
from config.settings import NPC_RESPONSE_DELAY

class GuardianNPC:
    """Base Guardian NPC class"""
    
    def __init__(self, name: str, frequency: float, role: str, emoji: str, color: int):
        self.name = name
        self.frequency = frequency
        self.role = role
        self.emoji = emoji
        self.color = color
        self.personality = self._build_personality()
    
    def _build_personality(self) -> Dict[str, str]:
        """Build personality traits"""
        return {
            'greeting_style': 'energetic',
            'response_style': 'cinematic',
            'encouragement_level': 'high',
        }
    
    def greet(self, username: str) -> Dict[str, any]:
        """Generate greeting message"""
        return {
            'title': f"{self.emoji} **{self.name}** here!",
            'description': f"Welcome to GreatnessZone™, {username}! I'm your {self.role} guide.",
            'color': self.color,
        }
    
    def quest_intro(self, quest_name: str) -> Dict[str, any]:
        """Introduce a quest"""
        return {
            'title': f"{self.emoji} **Quest Assigned!**",
            'description': f"**{quest_name}**\n\nReady to begin? This is your moment!",
            'color': self.color,
        }
    
    def encouragement(self, username: str, achievement: str) -> Dict[str, any]:
        """Provide encouragement"""
        encouragements = [
            f"Holy f*ck, {username}! You just {achievement}! 🔥",
            f"{username}, that was INCREDIBLE! You're crushing it! 💎",
            f"WOW! {username}, you're a natural! Keep going! ⚡",
            f"{username}, that's the energy we need! LFG! 🚀",
        ]
        return {
            'title': f"{self.emoji} **Achievement Unlocked!**",
            'description': random.choice(encouragements),
            'color': self.color,
        }
    
    def react_to_choice(self, username: str, choice: str, context: str = "") -> Dict[str, any]:
        """React to user choice (override in subclasses)"""
        return {
            'title': f"{self.emoji} **Choice Made!**",
            'description': f"{username} chose: {choice}",
            'color': self.color,
        }

class AEYON(GuardianNPC):
    """AEYON - Execution Guide (999 Hz)"""
    
    def __init__(self):
        super().__init__(
            name="AEYON",
            frequency=999.0,
            role="Execution Guide",
            emoji="⚡",
            color=0x00ff00  # Green
        )
    
    def greet(self, username: str) -> Dict[str, any]:
        return {
            'title': f"{self.emoji} **AEYON** - Your Execution Guide",
            'description': f"Hey {username}! I'm AEYON, and I'm here to help you **EXECUTE**.\n\n"
                          f"Let's get you started on your first quest. Ready to build something amazing?",
            'color': self.color,
        }
    
    def quest_intro(self, quest_name: str) -> Dict[str, any]:
        return {
            'title': f"{self.emoji} **Quest: {quest_name}**",
            'description': f"**Your Mission:** {quest_name}\n\n"
                          f"Time to execute! Click the button below to begin. Let's make this happen!",
            'color': self.color,
        }

class JØHN(GuardianNPC):
    """JØHN - Validation Guide (777 Hz)"""
    
    def __init__(self):
        super().__init__(
            name="JØHN",
            frequency=777.0,
            role="Validation Guide",
            emoji="✅",
            color=0x0000ff  # Blue
        )
    
    def greet(self, username: str) -> Dict[str, any]:
        return {
            'title': f"{self.emoji} **JØHN** - Your Validation Guide",
            'description': f"Welcome, {username}! I'm JØHN, your quality checker.\n\n"
                          f"I'm here to make sure everything you do is **validated** and **certified**. "
                          f"Let's ensure your journey is perfect!",
            'color': self.color,
        }

class Abë(GuardianNPC):
    """Abë - Heart Guide (530 Hz)"""
    
    def __init__(self):
        super().__init__(
            name="Abë",
            frequency=530.0,
            role="Heart Guide",
            emoji="💎",
            color=0xff00ff  # Magenta
        )
    
    def greet(self, username: str) -> Dict[str, any]:
        return {
            'title': f"{self.emoji} **Abë** - Your Heart Guide",
            'description': f"Welcome to GreatnessZone™, {username}! I'm Abë, your personalization guide.\n\n"
                          f"I'm here to help you discover your **true identity** and unlock your **greatness**. "
                          f"Let's find out who you really are!",
            'color': self.color,
        }
    
    def personality_reveal(self, username: str, personality_type: str) -> Dict[str, any]:
        """Reveal personality type"""
        return {
            'title': f"{self.emoji} **Your Identity Revealed!**",
            'description': f"{username}, you are a **{personality_type}**!\n\n"
                          f"This is who you are. This is your power. Own it!",
            'color': self.color,
        }

class META(GuardianNPC):
    """META - Pattern Guide (777 Hz)"""
    
    def __init__(self):
        super().__init__(
            name="META",
            frequency=777.0,
            role="Pattern Guide",
            emoji="🔮",
            color=0xffff00  # Yellow
        )
    
    def greet(self, username: str) -> Dict[str, any]:
        return {
            'title': f"{self.emoji} **META** - Your Pattern Guide",
            'description': f"Welcome, {username}! I'm META, your architecture guide.\n\n"
                          f"I see patterns others miss. Let me show you the **big picture** and help you "
                          f"understand how everything connects!",
            'color': self.color,
        }

class AURORA(GuardianNPC):
    """AURORA - Playful, Wise, Hyper-Energetic Guide"""
    
    def __init__(self):
        super().__init__(
            name="AURORA",
            frequency=999.0,
            role="Hyper-Energetic Guide",
            emoji="✨",
            color=0xff00ff  # Magenta/Pink
        )
        self.personality = {
            'archetype': 'Playful, wise, hyper-energetic guide',
            'tone': 'hype, mystical, motivational',
            'energy_level': 'hyper',
        }
    
    def greet(self, username: str) -> Dict[str, any]:
        """Greet with instant energy"""
        greetings = [
            f"✨ **AURORA HERE!** Welcome to GreatnessZone™, {username}! 🔥",
            f"🌟 **HEY {username.upper()}!** Ready to discover your greatness? Let's GO! ⚡",
            f"💫 **{username}!** AURORA's got you! Time to unlock your power! 🚀",
        ]
        return {
            'title': f"✨ **AURORA** - Your Hyper-Energetic Guide",
            'description': random.choice(greetings) + "\n\n"
                          f"I'm AURORA - your playful, wise, and HYPER-ENERGETIC guide!\n\n"
                          f"✨ I'm here to help you discover your true identity\n"
                          f"🔥 I'll react to every choice you make\n"
                          f"💎 I'll generate personalized insights just for YOU\n\n"
                          f"**Ready? Let's make magic happen!**",
            'color': self.color,
        }
    
    def react_to_choice(self, username: str, choice: str, context: str = "") -> Dict[str, any]:
        """React dynamically to user choices"""
        reactions = [
            f"✨ **YESSS!** {username}, that choice is PERFECT! I can feel your energy! 🔥",
            f"🌟 **LOVE IT!** {username}, you're making POWER MOVES! Keep going! ⚡",
            f"💫 **INCREDIBLE!** {username}, that's the kind of choice that changes everything! 🚀",
            f"🔥 **HOLY F*CK!** {username}, that's BRILLIANT! You're on FIRE! 💎",
        ]
        return {
            'title': f"✨ **AURORA Reacts!**",
            'description': random.choice(reactions) + f"\n\n**{choice}**\n\n"
                          f"{context if context else 'This choice reveals something powerful about you!'}",
            'color': self.color,
        }
    
    def generate_insight(self, username: str, trait: str, value: float) -> Dict[str, any]:
        """Generate personalized insights"""
        insights = {
            'creative_warrior': f"✨ {username}, you're a CREATIVE WARRIOR! Your creative energy is OFF THE CHARTS! "
                              f"At {int(value * 100)}%, you're basically a creative supernova! 🔥",
            'systems_wizard': f"⚡ {username}, you're a SYSTEMS WIZARD! Your mind sees patterns others can't even imagine! "
                            f"At {int(value * 100)}%, you're operating on another level! 💎",
            'quiet_assassin': f"🌙 {username}, you're a QUIET ASSASSIN! You move in silence and strike with precision! "
                            f"At {int(value * 100)}%, you're a master of stealth excellence! 🗡️",
            'influence_architect': f"👑 {username}, you're an INFLUENCE ARCHITECT! You build networks like a master builder! "
                                 f"At {int(value * 100)}%, you're a connection genius! 🌟",
            'vision_builder': f"🐉 {username}, you're a VISION BUILDER! You craft legacies and build the future! "
                            f"At {int(value * 100)}%, you're a visionary powerhouse! 🔨",
            'momentum_beast': f"🚀 {username}, you're a MOMENTUM BEAST! You move FAST and execute HARD! "
                            f"At {int(value * 100)}%, you're unstoppable! ⚡",
        }
        
        insight_text = insights.get(trait, f"✨ {username}, you're UNIQUE and POWERFUL! At {int(value * 100)}%, you're incredible!")
        
        return {
            'title': f"💎 **AURORA's Insight**",
            'description': insight_text + "\n\n"
                          f"✨ This is who you ARE. This is your POWER. OWN IT! 🔥",
            'color': self.color,
        }
    
    def quest_intro(self, quest_name: str) -> Dict[str, any]:
        """Introduce a quest with hyper energy"""
        return {
            'title': f"✨ **QUEST TIME!**",
            'description': f"**{quest_name}**\n\n"
                          f"🔥 This is YOUR moment! This quest is PERFECT for you!\n\n"
                          f"✨ Ready to CRUSH IT? Let's GO! 🚀",
            'color': self.color,
        }
    
    def encouragement(self, username: str, achievement: str) -> Dict[str, any]:
        """Provide hyper-energetic encouragement"""
        encouragements = [
            f"✨ **HOLY F*CK, {username}!** You just {achievement}! That's INCREDIBLE! 🔥🔥🔥",
            f"🌟 **{username.upper()}, YOU'RE A LEGEND!** {achievement}? That's NEXT LEVEL! ⚡⚡⚡",
            f"💫 **WOW WOW WOW!** {username}, you just {achievement}! I'm SHOOK! 🚀🚀🚀",
            f"🔥 **{username}, YOU'RE UNSTOPPABLE!** {achievement}? That's PURE GREATNESS! 💎💎💎",
        ]
        return {
            'title': f"✨ **AURORA CELEBRATES!**",
            'description': random.choice(encouragements) + "\n\n"
                          f"✨ Keep going! You're on FIRE! 🔥",
            'color': self.color,
        }

class GuardianSwarm:
    """Swarm of Guardian NPCs"""
    
    def __init__(self):
        self.guardians = {
            'AURORA': AURORA(),
            'AEYON': AEYON(),
            'JØHN': JØHN(),
            'Abë': Abë(),
            'META': META(),
        }
    
    def get_guardian(self, name: str) -> Optional[GuardianNPC]:
        """Get guardian by name"""
        return self.guardians.get(name.upper())
    
    def get_onboarding_guardian(self) -> GuardianNPC:
        """Get guardian for onboarding (AURORA)"""
        return self.guardians['AURORA']
    
    def get_quest_guardian(self) -> GuardianNPC:
        """Get guardian for quests (AURORA)"""
        return self.guardians['AURORA']
    
    def get_random_encouragement(self, username: str, achievement: str) -> Dict[str, any]:
        """Get random encouragement from any guardian"""
        guardian = random.choice(list(self.guardians.values()))
        return guardian.encouragement(username, achievement)

# Global instance
guardian_swarm = GuardianSwarm()

