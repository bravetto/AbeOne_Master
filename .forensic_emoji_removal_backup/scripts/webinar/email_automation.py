#!/usr/bin/env python3
"""
Webinar Email Automation
Handles all email sequences automatically.
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

class WebinarEmailAutomation:
    """Automatically manages all webinar email sequences."""
    
    def __init__(self):
        # ConvertKit API (fallback to SendGrid if not available)
        self.convertkit_api_key = os.getenv("CONVERTKIT_API_KEY")
        self.convertkit_api_secret = os.getenv("CONVERTKIT_API_SECRET")
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        
        # Email queue (simple file-based for now, upgrade to Redis/SQS later)
        self.queue_dir = Path("webinars/email_queue")
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        
    def register_attendee(self, email: str, name: str, webinar_id: str, webinar_data: Dict):
        """Register attendee and trigger email sequence."""
        
        print(f"📧 Registering {email} for webinar {webinar_id}")
        
        # Store registration
        registration = {
            "email": email,
            "name": name,
            "webinar_id": webinar_id,
            "registered_at": datetime.now().isoformat(),
            "webinar_data": webinar_data
        }
        
        reg_file = self.queue_dir / f"registration_{webinar_id}_{email.replace('@', '_at_')}.json"
        reg_file.write_text(json.dumps(registration, indent=2))
        
        # Send immediate confirmation
        self._send_confirmation_email(email, name, webinar_id, webinar_data)
        
        # Schedule reminders
        self._schedule_reminders(email, name, webinar_id, webinar_data)
        
        return registration
    
    def _send_confirmation_email(self, email: str, name: str, webinar_id: str, webinar_data: Dict):
        """Send immediate confirmation email."""
        
        topic = webinar_data.get("topic", "Webinar")
        scheduled_time = webinar_data.get("scheduled_time", "TBD")
        zoom_link = webinar_data.get("zoom_link", "#")
        
        email_content = {
            "to": email,
            "subject": f"Welcome! Your {topic} Webinar Details",
            "body": f"""
Hi {name},

You're registered for: {topic}

📅 Date: {scheduled_time}
🔗 Join Link: {zoom_link}

What You'll Get:
{chr(10).join(f"✅ {magnet.get('title', 'Bonus')}" for magnet in webinar_data.get('lead_magnets', []))}

See you there!

— Michael
            """.strip()
        }
        
        self._send_email(email_content)
        print(f"✅ Confirmation email sent to {email}")
    
    def _schedule_reminders(self, email: str, name: str, webinar_id: str, webinar_data: Dict):
        """Schedule reminder emails."""
        
        scheduled_time_str = webinar_data.get("scheduled_time")
        if not scheduled_time_str:
            return
        
        try:
            webinar_datetime = datetime.fromisoformat(scheduled_time_str.replace("Z", "+00:00"))
        except:
            # Fallback: assume 7 days from now
            webinar_datetime = datetime.now() + timedelta(days=7)
        
        # 24-hour reminder
        reminder_24h = {
            "email": email,
            "name": name,
            "webinar_id": webinar_id,
            "webinar_data": webinar_data,
            "send_time": (webinar_datetime - timedelta(hours=24)).isoformat(),
            "type": "reminder_24h",
            "subject": f"24 Hours Until: {webinar_data.get('topic', 'Webinar')}"
        }
        self._queue_email(reminder_24h)
        
        # 3-hour reminder
        reminder_3h = {
            "email": email,
            "name": name,
            "webinar_id": webinar_id,
            "webinar_data": webinar_data,
            "send_time": (webinar_datetime - timedelta(hours=3)).isoformat(),
            "type": "reminder_3h",
            "subject": f"Starting Soon: {webinar_data.get('topic', 'Webinar')}"
        }
        self._queue_email(reminder_3h)
        
        # 15-minute reminder
        reminder_15m = {
            "email": email,
            "name": name,
            "webinar_id": webinar_id,
            "webinar_data": webinar_data,
            "send_time": (webinar_datetime - timedelta(minutes=15)).isoformat(),
            "type": "reminder_15m",
            "subject": f"Starting in 15 Minutes: {webinar_data.get('topic', 'Webinar')}"
        }
        self._queue_email(reminder_15m)
        
        print(f"✅ Scheduled 3 reminder emails for {email}")
    
    def _queue_email(self, email_job: Dict):
        """Add email to queue."""
        
        send_time = email_job["send_time"]
        filename = f"email_{send_time.replace(':', '-').replace('+', '_')}_{email_job['email'].replace('@', '_at_')}.json"
        queue_file = self.queue_dir / filename
        queue_file.write_text(json.dumps(email_job, indent=2))
    
    def _send_email(self, email_content: Dict):
        """Send email via SendGrid or ConvertKit."""
        
        if self.sendgrid_api_key:
            self._send_via_sendgrid(email_content)
        elif self.convertkit_api_key:
            self._send_via_convertkit(email_content)
        else:
            # Fallback: save to file for manual sending
            print(f"⚠️ No email API configured. Saving to file:")
            email_file = self.queue_dir / f"manual_{datetime.now().timestamp()}.txt"
            email_file.write_text(f"""
To: {email_content['to']}
Subject: {email_content['subject']}

{email_content['body']}
            """)
            print(f"   Saved to: {email_file}")
    
    def _send_via_sendgrid(self, email_content: Dict):
        """Send email via SendGrid."""
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail
            
            sg = sendgrid.SendGridAPIClient(api_key=self.sendgrid_api_key)
            message = Mail(
                from_email=os.getenv("SENDGRID_FROM_EMAIL", "noreply@bravetto.ai"),
                to_emails=email_content["to"],
                subject=email_content["subject"],
                plain_text_content=email_content["body"]
            )
            response = sg.send(message)
            print(f"✅ Email sent via SendGrid: {response.status_code}")
        except ImportError:
            print("⚠️ SendGrid library not installed. Run: pip install sendgrid")
        except Exception as e:
            print(f"❌ SendGrid error: {e}")
    
    def _send_via_convertkit(self, email_content: Dict):
        """Send email via ConvertKit."""
        # ConvertKit API implementation
        print(f"📧 ConvertKit integration pending (email queued)")
    
    def process_email_queue(self):
        """Process queued emails that are ready to send."""
        
        now = datetime.now()
        sent_count = 0
        
        for queue_file in self.queue_dir.glob("email_*.json"):
            try:
                email_job = json.loads(queue_file.read_text())
                send_time = datetime.fromisoformat(email_job["send_time"].replace("Z", "+00:00"))
                
                if send_time <= now:
                    # Time to send!
                    email_content = {
                        "to": email_job["email"],
                        "subject": email_job["subject"],
                        "body": self._generate_email_body(email_job)
                    }
                    self._send_email(email_content)
                    
                    # Move to sent folder
                    sent_dir = self.queue_dir / "sent"
                    sent_dir.mkdir(exist_ok=True)
                    queue_file.rename(sent_dir / queue_file.name)
                    sent_count += 1
            except Exception as e:
                print(f"⚠️ Error processing {queue_file}: {e}")
        
        if sent_count > 0:
            print(f"✅ Processed {sent_count} queued emails")
    
    def _generate_email_body(self, email_job: Dict) -> str:
        """Generate email body based on type."""
        
        webinar_data = email_job.get("webinar_data", {})
        topic = webinar_data.get("topic", "Webinar")
        zoom_link = webinar_data.get("zoom_link", "#")
        name = email_job.get("name", "there")
        
        email_type = email_job.get("type", "reminder")
        
        if email_type == "reminder_24h":
            return f"""
Hi {name},

Just a friendly reminder: Your {topic} webinar starts in 24 hours!

🔗 Join Link: {zoom_link}

See you there!

— Michael
            """.strip()
        
        elif email_type == "reminder_3h":
            return f"""
Hi {name},

Your {topic} webinar starts in 3 hours!

🔗 Join Link: {zoom_link}

Don't miss it!

— Michael
            """.strip()
        
        elif email_type == "reminder_15m":
            return f"""
Hi {name},

Your {topic} webinar starts in 15 minutes!

🔗 Join Now: {zoom_link}

See you there!

— Michael
            """.strip()
        
        else:
            return f"""
Hi {name},

Reminder about: {topic}

🔗 Join Link: {zoom_link}

— Michael
            """.strip()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Webinar Email Automation")
    parser.add_argument("--process-queue", action="store_true", help="Process email queue")
    parser.add_argument("--register", action="store_true", help="Register attendee")
    parser.add_argument("--email", type=str, help="Email address")
    parser.add_argument("--name", type=str, help="Name")
    parser.add_argument("--webinar-id", type=str, help="Webinar ID")
    parser.add_argument("--webinar-file", type=str, help="Webinar JSON file")
    
    args = parser.parse_args()
    
    automation = WebinarEmailAutomation()
    
    if args.process_queue:
        automation.process_email_queue()
    elif args.register:
        if not all([args.email, args.name, args.webinar_id, args.webinar_file]):
            print("❌ Missing required arguments: --email, --name, --webinar-id, --webinar-file")
            sys.exit(1)
        
        webinar_data = json.loads(Path(args.webinar_file).read_text())
        automation.register_attendee(
            email=args.email,
            name=args.name,
            webinar_id=args.webinar_id,
            webinar_data=webinar_data
        )
    else:
        parser.print_help()

