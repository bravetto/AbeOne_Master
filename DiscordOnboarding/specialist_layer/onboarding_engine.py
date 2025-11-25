"""
Onboarding Engine - 8-Step Cinematic Flow
Pattern: ONBOARDING × FLOW × ONE
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from config.settings import ONBOARDING_TIMEOUT
from memory_layer.user_profiles import UserProfile
from specialist_layer.personalization_engine import personalization_engine
from gamification.quests import quest_manager
from gamification.badges import badge_manager
from gamification.artifacts import artifact_manager
from npcs.guardians import guardian_swarm
from memory_layer.storage import Storage
import asyncio

class OnboardingEngine:
    """Onboarding engine - manages 8-step cinematic flow"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
        self.user_profiles = UserProfile(storage)
        self.active_onboardings = {}  # Track active onboarding sessions
    
    def start_onboarding(self, discord_id: str, username: str) -> Dict[str, Any]:
        """Step 0: Entry Trigger → Welcome Screen"""
        # Get or create user profile
        profile = self.user_profiles.get_or_create(discord_id, username)
        
        # Check if already completed
        if profile.get('onboarding_complete'):
            return {
                'status': 'already_complete',
                'message': 'You\'ve already completed onboarding!',
            }
        
        # Initialize onboarding session
        self.active_onboardings[discord_id] = {
            'started_at': datetime.utcnow(),
            'step': 'welcome',
            'responses': {},
            'current_question': None,
            'selected_artifact': None,
            'channels_unlocked': [],
        }
        
        # Generate welcome message
        welcome_msg = personalization_engine.generate_welcome_message(username)
        aurora = guardian_swarm.get_guardian('AURORA')
        guardian_msg = aurora.greet(username)
        
        return {
            'status': 'started',
            'step': 'welcome',
            'welcome_message': welcome_msg,
            'guardian_message': guardian_msg,
            'next_action': 'energy_scan',
        }
    
    def start_energy_scan(self, discord_id: str) -> Dict[str, Any]:
        """Step 1: Energy Scan → Animated Loading"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        session['step'] = 'energy_scan'
        
        profile = self.user_profiles.get_or_create(discord_id, '')
        energy_msg = personalization_engine.generate_energy_scan_message(profile.get('username', 'User'))
        
        return {
            'status': 'energy_scan',
            'energy_message': energy_msg,
            'next_action': 'greatness_sprint',
        }
    
    def start_greatness_sprint(self, discord_id: str) -> Dict[str, Any]:
        """Step 2: 5-Question Greatness Sprint → Buttons only"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        session['step'] = 'greatness_sprint'
        
        # Get first question
        question = personalization_engine.get_next_question(session.get('answered_questions', []))
        
        if not question:
            return {'status': 'error', 'message': 'No questions available'}
        
        session['current_question'] = question['id']
        
        return {
            'status': 'question',
            'question': question,
            'step': 'greatness_sprint',
            'progress': len(session.get('answered_questions', [])) / 5,
        }
    
    def answer_question(self, discord_id: str, question_id: str, option_index: int) -> Dict[str, Any]:
        """Answer Greatness Sprint question"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        
        # Record answer
        if 'responses' not in session:
            session['responses'] = {}
        session['responses'][question_id] = option_index
        
        if 'answered_questions' not in session:
            session['answered_questions'] = []
        session['answered_questions'].append(question_id)
        
        # Get next question
        next_question = personalization_engine.get_next_question(session['answered_questions'])
        
        if next_question:
            session['current_question'] = next_question['id']
            return {
                'status': 'question',
                'question': next_question,
                'step': 'greatness_sprint',
                'progress': len(session['answered_questions']) / 5,
            }
        else:
            # All questions answered - analyze
            return self.complete_greatness_sprint(discord_id)
    
    def complete_greatness_sprint(self, discord_id: str) -> Dict[str, Any]:
        """Step 3: Traits → Role Stack Assignment"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        
        # Analyze responses
        analysis = personalization_engine.analyze_responses(session['responses'])
        
        # Update user profile
        profile = self.user_profiles.get_or_create(discord_id, '')
        self.user_profiles.update_traits(discord_id, analysis['trait_scores'])
        
        # Assign role stack (multiple roles)
        role_stack = analysis.get('role_stack', [analysis['personality_role']])
        for role in role_stack:
            self.user_profiles.assign_role(discord_id, role, 'personality')
        
        self.user_profiles.record_decision(
            discord_id,
            'personality',
            analysis['personality_type'],
            analysis
        )
        
        session['step'] = 'role_stack_assigned'
        session['personality'] = analysis
        session['role_stack'] = role_stack
        
        # Update profile with onboarding data
        self.user_profiles.update_profile_from_onboarding(discord_id, {
            'session': session,
            'personality': analysis,
        })
        
        # Generate reveal message
        reveal_msg = personalization_engine.generate_personality_reveal(analysis)
        aurora = guardian_swarm.get_guardian('AURORA')
        
        # Generate personalized insight from AURORA
        top_trait = max(analysis['trait_scores'].items(), key=lambda x: x[1])
        guardian_msg = aurora.generate_insight(
            profile.get('username', 'User'),
            top_trait[0],
            top_trait[1]
        )
        
        return {
            'status': 'role_stack_assigned',
            'reveal_message': reveal_msg,
            'guardian_message': guardian_msg,
            'personality': analysis,
            'role_stack': role_stack,
            'next_action': 'access_pathway',
        }
    
    def unlock_access_pathway(self, discord_id: str, guild: Any) -> Dict[str, Any]:
        """Step 4: Access Pathway → Channels Unlock"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        session['step'] = 'access_pathway'
        
        # Get role stack
        role_stack = session.get('role_stack', [])
        
        # Use GZ Map to get channels
        from config.gz_map import get_all_channels_for_role_stack, get_map_data_for_role_stack
        
        channels_to_unlock = get_all_channels_for_role_stack(role_stack)
        map_data = get_map_data_for_role_stack(role_stack)
        
        session['channels_unlocked'] = channels_to_unlock
        session['map_data'] = map_data
        
        # Update profile with unlocked channels
        profile = self.user_profiles.get_or_create(discord_id, '')
        profile_data = profile.get('profile_data', {})
        if not isinstance(profile_data, dict):
            profile_data = {}
        profile_data['channels_unlocked'] = channels_to_unlock
        self.storage.update_user_profile(discord_id, profile_data=profile_data)
        
        # In production, would actually unlock Discord channels here
        # For now, just track them
        
        return {
            'status': 'channels_unlocked',
            'channels': channels_to_unlock,
            'map_data': map_data,
            'next_action': 'artifact_quest',
        }
    
    def start_artifact_quest(self, discord_id: str) -> Dict[str, Any]:
        """Step 5: Artifact Quest → Choose Your Item"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        session['step'] = 'artifact_quest'
        
        # Get recommended artifacts based on role stack
        role_stack = session.get('role_stack', [])
        recommended = artifact_manager.get_recommended_artifacts(role_stack, limit=6)
        
        return {
            'status': 'artifact_selection',
            'artifacts': [a.to_dict() for a in recommended],
            'next_action': 'profile_generation',
        }
    
    def select_artifact(self, discord_id: str, artifact_id: str) -> Dict[str, Any]:
        """Select artifact"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        
        artifact = artifact_manager.get_artifact(artifact_id)
        if not artifact:
            return {'status': 'error', 'message': 'Artifact not found'}
        
        session['selected_artifact'] = artifact_id
        artifact_dict = artifact.to_dict()
        
        # Add artifact to user profile
        self.storage.add_artifact(discord_id, 'artifact', artifact_id, artifact_dict)
        
        # Assign artifact role if present
        if artifact.role:
            self.user_profiles.assign_role(discord_id, artifact.role.lower().replace(' ', '_'), 'artifact')
        
        # Update profile data with artifact
        profile = self.user_profiles.get_or_create(discord_id, '')
        profile_data = profile.get('profile_data', {})
        if not isinstance(profile_data, dict):
            profile_data = {}
        
        profile_data['artifact'] = artifact_id
        
        # Store perk
        if artifact.perk:
            profile_data['perks'] = profile_data.get('perks', [])
            profile_data['perks'].append({
                'artifact': artifact_id,
                'perk': artifact.perk,
                'unlocked_at': datetime.utcnow().isoformat()
            })
        
        self.storage.update_user_profile(discord_id, profile_data=profile_data)
        
        # Award bonus points
        if artifact.bonus_points > 0:
            self.storage.add_points(discord_id, artifact.bonus_points, f'Selected artifact: {artifact.name}')
        
        return {
            'status': 'artifact_selected',
            'artifact': artifact_dict,
            'next_action': 'profile_generation',
        }
    
    def generate_personal_profile(self, discord_id: str) -> Dict[str, Any]:
        """Step 6: Personal Profile → Generated by AI"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        session['step'] = 'profile_generated'
        
        profile = self.user_profiles.get_or_create(discord_id, '')
        personality = session.get('personality', {})
        role_stack = session.get('role_stack', [])
        
        # Generate AI profile
        ai_profile = personalization_engine.generate_ai_profile(
            profile.get('username', 'User'),
            personality,
            role_stack
        )
        
        return {
            'status': 'profile_generated',
            'ai_profile': ai_profile,
            'next_action': 'map_drop',
        }
    
    def create_map_drop(self, discord_id: str) -> Dict[str, Any]:
        """Step 7: Map Drop → Teleport Buttons"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        session['step'] = 'map_drop'
        
        # Get map data from session or generate
        map_data = session.get('map_data')
        if not map_data:
            role_stack = session.get('role_stack', [])
            from config.gz_map import get_map_data_for_role_stack
            map_data = get_map_data_for_role_stack(role_stack)
        
        # Create teleport points for each unlocked area
        teleport_points = []
        for area in map_data.get('map_areas', []):
            # Add area header
            teleport_points.append({
                'name': f"{area['icon']} {area['name']}",
                'channel': area['channels'][0] if area['channels'] else None,
                'type': 'area_header',
                'color': area['color'],
            })
            # Add channels in area
            for channel in area['channels'][:2]:  # Limit to 2 channels per area for buttons
                teleport_points.append({
                    'name': f" #{channel}",
                    'channel': channel,
                    'type': 'channel',
                })
        
        map_display = {
            'title': ' **MAP DROP**',
            'description': 'Your domains have opened.\n\nStep into your greatness.',
            'map_areas': map_data.get('map_areas', []),
            'teleport_points': teleport_points,
            'all_channels': map_data.get('all_channels', []),
        }
        
        return {
            'status': 'map_ready',
            'map_data': map_display,
            'next_action': 'first_quest',
        }
    
    def assign_first_quest(self, discord_id: str) -> Dict[str, Any]:
        """Step 8: First Quest → Immediate engagement"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        session['step'] = 'first_quest'
        
        # Assign welcome quest
        quest = quest_manager.get_welcome_quest()
        self.storage.assign_quest(discord_id, quest.quest_id, quest.name, quest.to_dict())
        
        aurora = guardian_swarm.get_guardian('AURORA')
        quest_msg = aurora.quest_intro(quest.name)
        
        return {
            'status': 'quest_assigned',
            'quest': quest.to_dict(),
            'quest_message': quest_msg,
            'next_action': 'complete',
        }
    
    def complete_quest(self, discord_id: str, quest_id: str) -> Dict[str, Any]:
        """Complete a quest"""
        quest = quest_manager.get_quest(quest_id)
        if not quest:
            return {'status': 'error', 'message': 'Quest not found'}
        
        # Mark quest as completed
        self.storage.complete_quest(discord_id, quest_id)
        
        # Award points
        points = self.storage.add_points(discord_id, quest.reward_points, f'Completed quest: {quest.name}')
        
        # Award badge if applicable
        badge_unlocked = None
        if quest.reward_badge:
            self.storage.add_artifact(discord_id, 'badge', quest.reward_badge)
            badge = badge_manager.get_badge(quest.reward_badge)
            if badge:
                badge_unlocked = badge.to_dict()
        
        # Get encouragement from AURORA
        profile = self.user_profiles.get_or_create(discord_id, '')
        aurora = guardian_swarm.get_guardian('AURORA')
        encouragement = aurora.encouragement(
            profile.get('username', 'User'),
            f'completed {quest.name}'
        )
        
        return {
            'status': 'quest_completed',
            'quest': quest.to_dict(),
            'points_awarded': quest.reward_points,
            'total_points': points,
            'badge_unlocked': badge_unlocked,
            'encouragement': encouragement,
        }
    
    def complete_onboarding(self, discord_id: str) -> Dict[str, Any]:
        """Complete onboarding"""
        if discord_id not in self.active_onboardings:
            return {'status': 'error', 'message': 'Onboarding not started'}
        
        session = self.active_onboardings[discord_id]
        
        # Mark onboarding as complete
        self.user_profiles.complete_onboarding(discord_id)
        
        # Award welcome badge
        self.storage.add_artifact(discord_id, 'badge', 'first_badge')
        self.storage.add_points(discord_id, 10, 'Completed onboarding')
        
        # Clean up session
        del self.active_onboardings[discord_id]
        
        profile = self.user_profiles.get_profile_summary(discord_id)
        
        return {
            'status': 'completed',
            'profile': profile,
            'message': ' **Onboarding Complete!** Welcome to GreatnessZone™!',
        }
    
    def get_onboarding_status(self, discord_id: str) -> Optional[Dict[str, Any]]:
        """Get current onboarding status"""
        return self.active_onboardings.get(discord_id)

# Global instance (will be initialized with storage)
onboarding_engine = None

def initialize_onboarding_engine(storage: Storage):
    """Initialize onboarding engine"""
    global onboarding_engine
    onboarding_engine = OnboardingEngine(storage)
    return onboarding_engine
