"""
Memory Layer - Database Storage
Pattern: MEMORY × STORAGE × ONE
"""

import sqlite3
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

class Storage:
    """Database storage for user profiles, traits, roles, artifacts, decisions"""
    
    def __init__(self, db_path: str = "onboarding.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User Profiles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                discord_id TEXT UNIQUE NOT NULL,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                onboarding_complete BOOLEAN DEFAULT FALSE,
                onboarding_started_at TIMESTAMP,
                onboarding_completed_at TIMESTAMP,
                current_quest_id TEXT,
                level INTEGER DEFAULT 1,
                total_points INTEGER DEFAULT 0,
                profile_data TEXT  -- JSON blob
            )
        """)
        
        # Traits
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_traits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                trait_name TEXT NOT NULL,
                trait_value REAL NOT NULL,
                confidence REAL DEFAULT 1.0,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles(user_id),
                UNIQUE(user_id, trait_name)
            )
        """)
        
        # Roles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_name TEXT NOT NULL,
                role_type TEXT NOT NULL,  -- 'personality', 'achievement', 'custom'
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles(user_id),
                UNIQUE(user_id, role_name)
            )
        """)
        
        # Artifacts (items, badges, achievements)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_artifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                artifact_type TEXT NOT NULL,  -- 'badge', 'item', 'achievement'
                artifact_name TEXT NOT NULL,
                artifact_data TEXT,  -- JSON blob
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles(user_id),
                UNIQUE(user_id, artifact_type, artifact_name)
            )
        """)
        
        # Decisions (user choices during onboarding)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                decision_type TEXT NOT NULL,  -- 'personality', 'quest_choice', 'role_choice'
                decision_value TEXT NOT NULL,
                decision_data TEXT,  -- JSON blob
                made_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
            )
        """)
        
        # Quests
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                quest_id TEXT NOT NULL,
                quest_name TEXT NOT NULL,
                status TEXT DEFAULT 'assigned',  -- 'assigned', 'in_progress', 'completed', 'failed'
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                quest_data TEXT,  -- JSON blob
                FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
            )
        """)
        
        # Points History
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS points_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                points INTEGER NOT NULL,
                reason TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_user_profile(self, discord_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by Discord ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_profiles WHERE discord_id = ?", (discord_id,))
        row = cursor.fetchone()
        
        if row:
            profile = dict(row)
            if profile.get('profile_data'):
                try:
                    profile['profile_data'] = json.loads(profile['profile_data'])
                except (json.JSONDecodeError, TypeError):
                    profile['profile_data'] = {}
            conn.close()
            return profile
        conn.close()
        return None
    
    def create_user_profile(self, discord_id: str, username: str) -> Dict[str, Any]:
        """Create new user profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user_profiles (discord_id, username, onboarding_started_at)
            VALUES (?, ?, ?)
        """, (discord_id, username, datetime.utcnow()))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return self.get_user_profile(discord_id)
    
    def update_user_profile(self, discord_id: str, **updates):
        """Update user profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Handle profile_data as JSON
        if 'profile_data' in updates and isinstance(updates['profile_data'], dict):
            updates['profile_data'] = json.dumps(updates['profile_data'])
        
        updates['updated_at'] = datetime.utcnow()
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [discord_id]
        
        cursor.execute(f"UPDATE user_profiles SET {set_clause} WHERE discord_id = ?", values)
        conn.commit()
        conn.close()
    
    def add_trait(self, discord_id: str, trait_name: str, trait_value: float, confidence: float = 1.0):
        """Add or update user trait"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO user_traits (user_id, trait_name, trait_value, confidence, detected_at)
            VALUES (?, ?, ?, ?, ?)
        """, (profile['user_id'], trait_name, trait_value, confidence, datetime.utcnow()))
        
        conn.commit()
        conn.close()
    
    def get_traits(self, discord_id: str) -> List[Dict[str, Any]]:
        """Get all user traits"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return []
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_traits WHERE user_id = ?", (profile['user_id'],))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def add_role(self, discord_id: str, role_name: str, role_type: str):
        """Add role to user"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO user_roles (user_id, role_name, role_type, assigned_at)
            VALUES (?, ?, ?, ?)
        """, (profile['user_id'], role_name, role_type, datetime.utcnow()))
        
        conn.commit()
        conn.close()
    
    def get_roles(self, discord_id: str) -> List[str]:
        """Get all user roles"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT role_name FROM user_roles WHERE user_id = ?", (profile['user_id'],))
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]
    
    def add_artifact(self, discord_id: str, artifact_type: str, artifact_name: str, artifact_data: Optional[Dict] = None):
        """Add artifact (badge, item, achievement)"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        artifact_data_json = json.dumps(artifact_data) if artifact_data else None
        
        cursor.execute("""
            INSERT OR IGNORE INTO user_artifacts (user_id, artifact_type, artifact_name, artifact_data, unlocked_at)
            VALUES (?, ?, ?, ?, ?)
        """, (profile['user_id'], artifact_type, artifact_name, artifact_data_json, datetime.utcnow()))
        
        conn.commit()
        conn.close()
    
    def add_decision(self, discord_id: str, decision_type: str, decision_value: str, decision_data: Optional[Dict] = None):
        """Record user decision"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        decision_data_json = json.dumps(decision_data) if decision_data else None
        
        cursor.execute("""
            INSERT INTO user_decisions (user_id, decision_type, decision_value, decision_data, made_at)
            VALUES (?, ?, ?, ?, ?)
        """, (profile['user_id'], decision_type, decision_value, decision_data_json, datetime.utcnow()))
        
        conn.commit()
        conn.close()
    
    def assign_quest(self, discord_id: str, quest_id: str, quest_name: str, quest_data: Optional[Dict] = None):
        """Assign quest to user"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        quest_data_json = json.dumps(quest_data) if quest_data else None
        
        cursor.execute("""
            INSERT INTO user_quests (user_id, quest_id, quest_name, status, quest_data, assigned_at)
            VALUES (?, ?, ?, 'assigned', ?, ?)
        """, (profile['user_id'], quest_id, quest_name, quest_data_json, datetime.utcnow()))
        
        # Update user profile
        cursor.execute("""
            UPDATE user_profiles SET current_quest_id = ? WHERE user_id = ?
        """, (quest_id, profile['user_id']))
        
        conn.commit()
        conn.close()
    
    def complete_quest(self, discord_id: str, quest_id: str):
        """Mark quest as completed"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE user_quests 
            SET status = 'completed', completed_at = ?
            WHERE user_id = ? AND quest_id = ?
        """, (datetime.utcnow(), profile['user_id'], quest_id))
        
        conn.commit()
        conn.close()
    
    def add_points(self, discord_id: str, points: int, reason: str):
        """Add points to user"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Add to history
        cursor.execute("""
            INSERT INTO points_history (user_id, points, reason, timestamp)
            VALUES (?, ?, ?, ?)
        """, (profile['user_id'], points, reason, datetime.utcnow()))
        
        # Update total
        cursor.execute("""
            UPDATE user_profiles SET total_points = total_points + ? WHERE user_id = ?
        """, (points, profile['user_id']))
        
        conn.commit()
        conn.close()
        
        return self.get_user_profile(discord_id)['total_points']
    
    def get_decisions(self, discord_id: str) -> List[Dict[str, Any]]:
        """Get all user decisions"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return []
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_decisions WHERE user_id = ? ORDER BY made_at DESC", (profile['user_id'],))
        rows = cursor.fetchall()
        conn.close()
        
        decisions = []
        for row in rows:
            decision = dict(row)
            if decision.get('decision_data'):
                try:
                    decision['decision_data'] = json.loads(decision['decision_data'])
                except (json.JSONDecodeError, TypeError):
                    decision['decision_data'] = {}
            decisions.append(decision)
        
        return decisions
    
    def get_artifacts(self, discord_id: str, artifact_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get user artifacts"""
        profile = self.get_user_profile(discord_id)
        if not profile:
            return []
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if artifact_type:
            cursor.execute("""
                SELECT * FROM user_artifacts 
                WHERE user_id = ? AND artifact_type = ?
                ORDER BY unlocked_at DESC
            """, (profile['user_id'], artifact_type))
        else:
            cursor.execute("""
                SELECT * FROM user_artifacts 
                WHERE user_id = ?
                ORDER BY unlocked_at DESC
            """, (profile['user_id'],))
        
        rows = cursor.fetchall()
        conn.close()
        
        artifacts = []
        for row in rows:
            artifact = dict(row)
            if artifact.get('artifact_data'):
                try:
                    artifact['artifact_data'] = json.loads(artifact['artifact_data'])
                except (json.JSONDecodeError, TypeError):
                    artifact['artifact_data'] = {}
            artifacts.append(artifact)
        
        return artifacts

