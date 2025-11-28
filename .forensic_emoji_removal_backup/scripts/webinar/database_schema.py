#!/usr/bin/env python3
"""
Webinar Database Schema
SQLite database schema for webinar system.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class WebinarDatabase:
    """Database for webinar system."""
    
    def __init__(self, db_path: str = "webinars/webinars.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables."""
        
        cursor = self.conn.cursor()
        
        # Webinars table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS webinars (
                id TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                scheduled_time TEXT NOT NULL,
                duration INTEGER DEFAULT 60,
                zoom_webinar_id TEXT,
                zoom_join_url TEXT,
                zoom_password TEXT,
                calendar_event_id TEXT,
                calendar_link TEXT,
                content_json TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Registrations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                webinar_id TEXT NOT NULL,
                email TEXT NOT NULL,
                name TEXT NOT NULL,
                registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                attended INTEGER DEFAULT 0,
                converted INTEGER DEFAULT 0,
                FOREIGN KEY (webinar_id) REFERENCES webinars(id)
            )
        """)
        
        # Email sequences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_sequences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                registration_id INTEGER NOT NULL,
                sequence_number INTEGER NOT NULL,
                email_type TEXT NOT NULL,
                sent_at TEXT,
                opened_at TEXT,
                clicked_at TEXT,
                FOREIGN KEY (registration_id) REFERENCES registrations(id)
            )
        """)
        
        # Analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                webinar_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (webinar_id) REFERENCES webinars(id)
            )
        """)
        
        self.conn.commit()
        print("✅ Database tables created")
    
    def create_webinar(self, webinar_data: Dict) -> str:
        """Create webinar record."""
        
        webinar_id = webinar_data.get("webinar_id") or f"webinar_{int(datetime.now().timestamp())}"
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO webinars 
            (id, topic, scheduled_time, duration, zoom_webinar_id, zoom_join_url, 
             zoom_password, calendar_event_id, calendar_link, content_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            webinar_id,
            webinar_data.get("topic", ""),
            webinar_data.get("scheduled_time", ""),
            webinar_data.get("duration", 60),
            webinar_data.get("zoom_webinar_id", ""),
            webinar_data.get("zoom_join_url", ""),
            webinar_data.get("zoom_password", ""),
            webinar_data.get("calendar_event_id", ""),
            webinar_data.get("calendar_link", ""),
            json.dumps(webinar_data)
        ))
        
        self.conn.commit()
        return webinar_id
    
    def register_attendee(self, webinar_id: str, email: str, name: str) -> int:
        """Register attendee."""
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO registrations (webinar_id, email, name)
            VALUES (?, ?, ?)
        """, (webinar_id, email, name))
        
        registration_id = cursor.lastrowid
        self.conn.commit()
        return registration_id
    
    def get_webinar(self, webinar_id: str) -> Optional[Dict]:
        """Get webinar by ID."""
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM webinars WHERE id = ?", (webinar_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def get_registrations(self, webinar_id: str) -> List[Dict]:
        """Get all registrations for webinar."""
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM registrations WHERE webinar_id = ?", (webinar_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def mark_attended(self, registration_id: int):
        """Mark registration as attended."""
        
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE registrations SET attended = 1 WHERE id = ?
        """, (registration_id,))
        self.conn.commit()
    
    def mark_converted(self, registration_id: int):
        """Mark registration as converted."""
        
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE registrations SET converted = 1 WHERE id = ?
        """, (registration_id,))
        self.conn.commit()
    
    def get_analytics(self, webinar_id: str) -> Dict:
        """Get analytics for webinar."""
        
        registrations = self.get_registrations(webinar_id)
        total = len(registrations)
        attended = sum(1 for r in registrations if r.get("attended"))
        converted = sum(1 for r in registrations if r.get("converted"))
        
        return {
            "total_registrations": total,
            "attended": attended,
            "attendance_rate": attended / total if total > 0 else 0,
            "converted": converted,
            "conversion_rate": converted / total if total > 0 else 0
        }


if __name__ == "__main__":
    # Test database
    db = WebinarDatabase()
    
    # Create test webinar
    test_webinar = {
        "webinar_id": "test_123",
        "topic": "Test Webinar",
        "scheduled_time": datetime.now().isoformat(),
        "duration": 60
    }
    
    webinar_id = db.create_webinar(test_webinar)
    print(f"✅ Created webinar: {webinar_id}")
    
    # Register test attendee
    reg_id = db.register_attendee(webinar_id, "test@example.com", "Test User")
    print(f"✅ Registered attendee: {reg_id}")
    
    # Get analytics
    analytics = db.get_analytics(webinar_id)
    print(f"📊 Analytics: {analytics}")

