"""
User Profile Management
Pattern: MEMORY × PROFILES × ONE
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from .storage import Storage

class UserProfile:
    """User profile manager"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def get_or_create(self, discord_id: str, username: str) -> Dict[str, Any]:
        """Get existing profile or create new one"""
        profile = self.storage.get_user_profile(discord_id)
        if not profile:
            profile = self.storage.create_user_profile(discord_id, username)
        return profile
    
    def get_profile_template(self, discord_id: str) -> Dict[str, Any]:
        """Get user profile in template format"""
        profile = self.storage.get_user_profile(discord_id)
        if not profile:
            return None
        
        # Get decisions to extract answers
        decisions = self.storage.get_decisions(discord_id)
        
        # Extract answers from decisions
        passions = ""
        talents = ""
        vibe = ""
        intention = ""
        growth = ""
        
        for decision in decisions:
            if decision['decision_type'] == 'personality':
                decision_data = decision.get('decision_data', {})
                if isinstance(decision_data, str):
                    import json
                    try:
                        decision_data = json.loads(decision_data)
                    except:
                        decision_data = {}
                
                # Extract from decision data
                passions = decision_data.get('archetype', '')
                talents = decision_data.get('role', '')
                vibe = decision_data.get('vibe', '')
                intention = decision_data.get('pathway', '')
                growth = decision_data.get('growth', '')
        
        # Get role stack for archetype and role
        role_stack = self.storage.get_roles(discord_id)
        archetype = role_stack[0] if role_stack else ""
        role = role_stack[1] if len(role_stack) > 1 else archetype
        
        # Get artifact
        artifacts = self.storage.get_artifacts(discord_id)
        artifact = artifacts[0].get('artifact_name', '') if artifacts else ""
        
        # Get unlocked channels
        channels_unlocked = []
        profile_data = profile.get('profile_data', {})
        if isinstance(profile_data, dict):
            channels_unlocked = profile_data.get('channels_unlocked', [])
        
        return {
            'userId': discord_id,
            'passions': passions,
            'talents': talents,
            'vibe': vibe,
            'intention': intention,
            'growth': growth,
            'archetype': archetype,
            'role': role,
            'artifact': artifact,
            'channelsUnlocked': channels_unlocked,
            'createdAt': profile.get('created_at', datetime.utcnow()).isoformat() if profile.get('created_at') else datetime.utcnow().isoformat(),
        }
    
    def get_profile_summary(self, discord_id: str) -> Dict[str, Any]:
        """Get complete profile summary"""
        profile = self.storage.get_user_profile(discord_id)
        if not profile:
            return None
        
        return {
            'profile': profile,
            'traits': self.storage.get_traits(discord_id),
            'roles': self.storage.get_roles(discord_id),
            'level': profile.get('level', 1),
            'points': profile.get('total_points', 0),
            'onboarding_complete': profile.get('onboarding_complete', False),
            'template': self.get_profile_template(discord_id),
        }
    
    def update_traits(self, discord_id: str, traits: Dict[str, float]):
        """Update user traits"""
        for trait_name, trait_value in traits.items():
            self.storage.add_trait(discord_id, trait_name, trait_value)
    
    def assign_role(self, discord_id: str, role_name: str, role_type: str = 'personality'):
        """Assign role to user"""
        self.storage.add_role(discord_id, role_name, role_type)
    
    def record_decision(self, discord_id: str, decision_type: str, decision_value: str, decision_data: Optional[Dict] = None):
        """Record user decision"""
        self.storage.add_decision(discord_id, decision_type, decision_value, decision_data)
    
    def update_profile_from_onboarding(self, discord_id: str, onboarding_data: Dict[str, Any]):
        """Update profile with onboarding data"""
        session = onboarding_data.get('session', {})
        responses = session.get('responses', {})
        personality = session.get('personality', {})
        role_stack = session.get('role_stack', [])
        selected_artifact = session.get('selected_artifact', '')
        channels_unlocked = session.get('channels_unlocked', [])
        
        # Extract answers from responses
        from specialist_layer.personalization_engine import personalization_engine
        
        passions = ""
        talents = ""
        vibe = ""
        intention = ""
        growth = ""
        
        # Q1: Passions
        if 'q1' in responses:
            q1 = personalization_engine.get_question('q1')
            if q1 and 0 <= responses['q1'] < len(q1['options']):
                passions = q1['options'][responses['q1']].get('text', '')
        
        # Q2: Talents
        if 'q2' in responses:
            q2 = personalization_engine.get_question('q2')
            if q2 and 0 <= responses['q2'] < len(q2['options']):
                talents = q2['options'][responses['q2']].get('text', '')
        
        # Q3: Vibe
        if 'q3' in responses:
            q3 = personalization_engine.get_question('q3')
            if q3 and 0 <= responses['q3'] < len(q3['options']):
                vibe = q3['options'][responses['q3']].get('text', '')
        
        # Q4: Intention
        if 'q4' in responses:
            q4 = personalization_engine.get_question('q4')
            if q4 and 0 <= responses['q4'] < len(q4['options']):
                intention = q4['options'][responses['q4']].get('text', '')
        
        # Q5: Growth
        if 'q5' in responses:
            q5 = personalization_engine.get_question('q5')
            if q5 and 0 <= responses['q5'] < len(q5['options']):
                growth = q5['options'][responses['q5']].get('text', '')
        
        # Update profile data
        profile_data = {
            'passions': passions,
            'talents': talents,
            'vibe': vibe,
            'intention': intention,
            'growth': growth,
            'archetype': personality.get('archetype', role_stack[0] if role_stack else ''),
            'role': personality.get('role', role_stack[1] if len(role_stack) > 1 else role_stack[0] if role_stack else ''),
            'artifact': selected_artifact,
            'channels_unlocked': channels_unlocked,
        }
        
        self.storage.update_user_profile(discord_id, profile_data=profile_data)
    
    def complete_onboarding(self, discord_id: str):
        """Mark onboarding as complete"""
        self.storage.update_user_profile(
            discord_id,
            onboarding_complete=True,
            onboarding_completed_at=datetime.utcnow()
        )

