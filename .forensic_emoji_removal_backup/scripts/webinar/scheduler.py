#!/usr/bin/env python3
"""
Webinar Scheduler
Auto-schedules webinars at optimal times.
"""

import os
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

class WebinarScheduler:
    """Automatically schedules webinars at optimal times."""
    
    def __init__(self):
        self.zoom_api_key = os.getenv("ZOOM_API_KEY")
        self.zoom_api_secret = os.getenv("ZOOM_API_SECRET")
        self.calendar_credentials = os.getenv("GOOGLE_CALENDAR_CREDENTIALS")
        
        # Default settings
        self.default_days = ["Tuesday", "Wednesday", "Thursday"]
        self.default_time = "14:00"  # 2pm EST
        self.default_timezone = "America/New_York"
        
    def schedule_webinar(self, webinar_content: Dict, 
                        preferred_days: List[str] = None,
                        preferred_time: str = None) -> Dict:
        """Schedule webinar at optimal time."""
        
        print(f"📅 Scheduling webinar: {webinar_content.get('topic', 'Untitled')}")
        
        # Find optimal time slot
        optimal_time = self._find_optimal_time(
            webinar_content, 
            preferred_days or self.default_days,
            preferred_time or self.default_time
        )
        
        print(f"✅ Optimal time: {optimal_time.isoformat()}")
        
        # Create Zoom webinar (mock for now, implement API later)
        zoom_webinar = self._create_zoom_webinar(
            topic=webinar_content.get("topic", "Webinar"),
            start_time=optimal_time,
            duration=webinar_content.get("duration", 60)
        )
        
        # Create calendar event (mock for now)
        calendar_event = self._create_calendar_event(
            topic=webinar_content.get("topic", "Webinar"),
            start_time=optimal_time,
            zoom_link=zoom_webinar.get("join_url", "#")
        )
        
        schedule_info = {
            "scheduled_time": optimal_time.isoformat(),
            "zoom_webinar_id": zoom_webinar.get("id", "mock_123"),
            "zoom_join_url": zoom_webinar.get("join_url", "https://zoom.us/j/mock"),
            "zoom_password": zoom_webinar.get("password", ""),
            "calendar_event_id": calendar_event.get("id", "mock_cal_123"),
            "calendar_link": calendar_event.get("htmlLink", "#")
        }
        
        # Save schedule info
        schedule_file = Path(f"webinars/schedule_{optimal_time.strftime('%Y%m%d_%H%M')}.json")
        schedule_file.write_text(json.dumps(schedule_info, indent=2))
        print(f"💾 Schedule saved to: {schedule_file}")
        
        return schedule_info
    
    def _find_optimal_time(self, webinar_content: Dict, 
                          preferred_days: List[str],
                          preferred_time: str) -> datetime:
        """Find optimal webinar time."""
        
        # Parse preferred time
        hour, minute = map(int, preferred_time.split(":"))
        
        # Start from today
        now = datetime.now()
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Find next preferred day
        days_ahead = 0
        max_days = 14  # Look ahead 2 weeks
        
        while days_ahead < max_days:
            day_name = candidate.strftime("%A")
            if day_name in preferred_days:
                # Check if time is in the future
                if candidate > now:
                    return candidate
            candidate += timedelta(days=1)
            days_ahead += 1
        
        # Fallback: next Tuesday at 2pm
        days_until_tuesday = (1 - now.weekday()) % 7
        if days_until_tuesday == 0:
            days_until_tuesday = 7
        return now + timedelta(days=days_until_tuesday)
    
    def _create_zoom_webinar(self, topic: str, start_time: datetime, duration: int) -> Dict:
        """Create Zoom webinar."""
        
        if not self.zoom_api_key:
            print("⚠️ Zoom API not configured. Using mock webinar.")
            return {
                "id": f"mock_{int(start_time.timestamp())}",
                "join_url": "https://zoom.us/j/mock",
                "password": "123456",
                "topic": topic,
                "start_time": start_time.isoformat(),
                "duration": duration
            }
        
        # TODO: Implement actual Zoom API call
        # from zoomus import ZoomClient
        # zoom = ZoomClient(self.zoom_api_key, self.zoom_api_secret)
        # webinar = zoom.webinar.create(...)
        
        print(f"✅ Zoom webinar created (mock)")
        return {
            "id": f"zoom_{int(start_time.timestamp())}",
            "join_url": f"https://zoom.us/j/{int(start_time.timestamp())}",
            "password": "123456",
            "topic": topic,
            "start_time": start_time.isoformat(),
            "duration": duration
        }
    
    def _create_calendar_event(self, topic: str, start_time: datetime, zoom_link: str) -> Dict:
        """Create Google Calendar event."""
        
        if not self.calendar_credentials:
            print("⚠️ Google Calendar not configured. Using mock event.")
            return {
                "id": f"cal_{int(start_time.timestamp())}",
                "htmlLink": "#",
                "summary": f"Webinar: {topic}",
                "start": start_time.isoformat(),
                "end": (start_time + timedelta(hours=1)).isoformat()
            }
        
        # TODO: Implement actual Google Calendar API call
        # from google.oauth2.credentials import Credentials
        # from googleapiclient.discovery import build
        # service = build('calendar', 'v3', credentials=creds)
        # event = service.events().insert(calendarId='primary', body=event_body).execute()
        
        print(f"✅ Calendar event created (mock)")
        return {
            "id": f"cal_{int(start_time.timestamp())}",
            "htmlLink": f"https://calendar.google.com/event?eid={int(start_time.timestamp())}",
            "summary": f"Webinar: {topic}",
            "start": start_time.isoformat(),
            "end": (start_time + timedelta(hours=1)).isoformat()
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Schedule webinar")
    parser.add_argument("--webinar-file", type=str, required=True, help="Webinar JSON file")
    parser.add_argument("--days", type=str, nargs="+", help="Preferred days (e.g., Tuesday Wednesday)")
    parser.add_argument("--time", type=str, help="Preferred time (e.g., 14:00)")
    
    args = parser.parse_args()
    
    scheduler = WebinarScheduler()
    
    webinar_content = json.loads(Path(args.webinar_file).read_text())
    schedule_info = scheduler.schedule_webinar(
        webinar_content,
        preferred_days=args.days,
        preferred_time=args.time
    )
    
    print(f"\n✅ Webinar scheduled!")
    print(f"📅 Time: {schedule_info['scheduled_time']}")
    print(f"🔗 Zoom: {schedule_info['zoom_join_url']}")
    print(f"📆 Calendar: {schedule_info['calendar_link']}")

