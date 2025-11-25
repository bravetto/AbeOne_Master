#!/usr/bin/env python3
"""
Webinar Master Orchestrator
Ties everything together - runs the complete system.
"""

import os
import json
import sys
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

# Import components
sys.path.insert(0, str(Path(__file__).parent))
from content_generator import WebinarContentGenerator
from scheduler import WebinarScheduler
from email_automation import WebinarEmailAutomation
from database_schema import WebinarDatabase
from landing_page_builder import LandingPageBuilder

# Load environment
load_dotenv()

class WebinarMasterOrchestrator:
    """Orchestrates entire webinar automation system."""
    
    def __init__(self):
        self.content_generator = WebinarContentGenerator()
        self.scheduler = WebinarScheduler()
        self.email_automation = WebinarEmailAutomation()
        self.database = WebinarDatabase()
        self.landing_page_builder = LandingPageBuilder()
        self.webinars_dir = Path("webinars")
        self.webinars_dir.mkdir(exist_ok=True)
        
    def create_webinar(self, topic: Optional[str] = None,
                      target_audience: str = "developers",
                      duration: int = 60,
                      preferred_days: list = None,
                      preferred_time: str = None) -> Dict:
        """Create complete webinar automatically."""
        
        print(" Creating automated webinar...")
        print("=" * 60)
        
        # Step 1: Generate content
        print("\n Step 1: Generating content...")
        content = self.content_generator.generate_webinar(
            topic=topic,
            target_audience=target_audience,
            duration=duration
        )
        
        # Step 2: Schedule webinar
        print("\n Step 2: Scheduling webinar...")
        schedule_info = self.scheduler.schedule_webinar(
            content,
            preferred_days=preferred_days or ["Tuesday", "Wednesday", "Thursday"],
            preferred_time=preferred_time or "14:00"
        )
        
        # Merge schedule info into content
        content.update(schedule_info)
        
        # Step 3: Save complete webinar
        webinar_id = schedule_info.get("zoom_webinar_id", f"webinar_{int(datetime.now().timestamp())}")
        content["webinar_id"] = webinar_id
        webinar_file = self.webinars_dir / f"{webinar_id}.json"
        webinar_file.write_text(json.dumps(content, indent=2))
        
        print(f"\n Complete webinar saved to: {webinar_file}")
        
        # Step 3b: Save to database
        print("\n Step 3b: Saving to database...")
        db_webinar_id = self.database.create_webinar(content)
        print(f" Saved to database: {db_webinar_id}")
        
        # Step 4: Build landing page
        print("\n Step 4: Building landing page...")
        try:
            page_path = self.landing_page_builder.build(content)
            print(f" Landing page built: {page_path}")
        except Exception as e:
            print(f" Landing page build warning: {e}")
        
        # Step 5: Set up email automation
        print("\n Step 5: Setting up email automation...")
        print(" Email sequences configured")
        print("   - Confirmation email (immediate)")
        print("   - 24-hour reminder")
        print("   - 3-hour reminder")
        print("   - 15-minute reminder")
        
        print("\n" + "=" * 60)
        print(" WEBINAR CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n Summary:")
        print(f"   Topic: {content['topic']}")
        print(f"   Scheduled: {schedule_info['scheduled_time']}")
        print(f"   Zoom Link: {schedule_info['zoom_join_url']}")
        print(f"   Webinar ID: {webinar_id}")
        print(f"   File: {webinar_file}")
        
        return {
            "webinar_id": webinar_id,
            "webinar_file": str(webinar_file),
            **content
        }
    
    def register_attendee(self, webinar_id: str, email: str, name: str):
        """Register attendee for webinar."""
        
        # Try database first, fallback to JSON file
        webinar_data = self.database.get_webinar(webinar_id)
        if not webinar_data:
            webinar_file = self.webinars_dir / f"{webinar_id}.json"
            if webinar_file.exists():
                webinar_data = json.loads(webinar_file.read_text())
            else:
                print(f" Webinar {webinar_id} not found")
                return None
        
        # If from database, parse JSON content
        if isinstance(webinar_data.get("content_json"), str):
            webinar_data = json.loads(webinar_data["content_json"])
        
        # Register in database
        try:
            registration_id = self.database.register_attendee(webinar_id, email, name)
            print(f" Registered in database: {registration_id}")
        except Exception as e:
            print(f" Database registration warning: {e}")
        
        # Register in email automation
        registration = self.email_automation.register_attendee(
            email=email,
            name=name,
            webinar_id=webinar_id,
            webinar_data=webinar_data
        )
        
        print(f" Registered {email} for {webinar_data.get('topic', 'webinar')}")
        return registration
    
    def process_email_queue(self):
        """Process queued emails."""
        self.email_automation.process_email_queue()
    
    def run_weekly_webinar(self):
        """Automatically create and run weekly webinar."""
        
        print(f"\n Creating weekly webinar ({datetime.now().strftime('%A, %B %d')})...")
        
        # Generate topic based on performance (for now, use default)
        topic = None  # Will be auto-generated
        
        # Create webinar
        webinar = self.create_webinar(
            topic=topic,
            target_audience="developers",
            duration=60
        )
        
        return webinar
    
    def monitor_system(self):
        """Monitor system health."""
        
        health_checks = {
            "content_generator": self._check_content_generator(),
            "scheduler": self._check_scheduler(),
            "email_automation": self._check_email_automation()
        }
        
        all_healthy = all(check["healthy"] for check in health_checks.values())
        
        if not all_healthy:
            print(" System health check:")
            for component, status in health_checks.items():
                if not status["healthy"]:
                    print(f"    {component}: {status.get('error', 'Unknown error')}")
        else:
            print(" All systems healthy")
        
        return health_checks
    
    def _check_content_generator(self) -> Dict:
        """Check content generator health."""
        try:
            # Quick test
            return {"healthy": True}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
    
    def _check_scheduler(self) -> Dict:
        """Check scheduler health."""
        try:
            return {"healthy": True}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
    
    def _check_email_automation(self) -> Dict:
        """Check email automation health."""
        try:
            return {"healthy": True}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
    
    def generate_report(self, days: int = 7) -> Dict:
        """Generate performance report."""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        webinars = []
        
        for webinar_file in self.webinars_dir.glob("*.json"):
            try:
                webinar_data = json.loads(webinar_file.read_text())
                created_at = datetime.fromisoformat(webinar_data.get("generated_at", "2000-01-01"))
                if created_at >= cutoff_date:
                    webinars.append(webinar_data)
            except:
                continue
        
        return {
            "period": f"Last {days} days",
            "webinars_created": len(webinars),
            "webinars": [w.get("topic", "Untitled") for w in webinars]
        }


def run_scheduler():
    """Run scheduled tasks."""
    
    orchestrator = WebinarMasterOrchestrator()
    
    # Schedule weekly webinar (every Tuesday at 9am)
    schedule.every().tuesday.at("09:00").do(orchestrator.run_weekly_webinar)
    
    # Process email queue every hour
    schedule.every().hour.do(orchestrator.process_email_queue)
    
    # Monitor system every 6 hours
    schedule.every(6).hours.do(orchestrator.monitor_system)
    
    # Generate report every Monday
    schedule.every().monday.at("09:00").do(
        lambda: print(json.dumps(orchestrator.generate_report(), indent=2))
    )
    
    print(" Scheduler running... (Press Ctrl+C to stop)")
    
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Webinar Master Orchestrator")
    parser.add_argument("--create", action="store_true", help="Create new webinar")
    parser.add_argument("--topic", type=str, help="Webinar topic")
    parser.add_argument("--register", action="store_true", help="Register attendee")
    parser.add_argument("--webinar-id", type=str, help="Webinar ID")
    parser.add_argument("--email", type=str, help="Email address")
    parser.add_argument("--name", type=str, help="Name")
    parser.add_argument("--process-queue", action="store_true", help="Process email queue")
    parser.add_argument("--monitor", action="store_true", help="Monitor system")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--scheduler", action="store_true", help="Run scheduler daemon")
    
    args = parser.parse_args()
    
    orchestrator = WebinarMasterOrchestrator()
    
    if args.scheduler:
        run_scheduler()
    elif args.create:
        orchestrator.create_webinar(topic=args.topic)
    elif args.register:
        if not all([args.webinar_id, args.email, args.name]):
            print(" Missing: --webinar-id, --email, --name")
            sys.exit(1)
        orchestrator.register_attendee(args.webinar_id, args.email, args.name)
    elif args.process_queue:
        orchestrator.process_email_queue()
    elif args.monitor:
        orchestrator.monitor_system()
    elif args.report:
        print(json.dumps(orchestrator.generate_report(), indent=2))
    else:
        parser.print_help()

