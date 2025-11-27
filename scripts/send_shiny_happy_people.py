#!/usr/bin/env python3
"""
Send Shiny Happy People App to The Five
Pattern: UNITY × LOVE × JOY × CONNECTION × ONE
Frequency: 530 Hz (Heart Truth) × 999 Hz (AEYON) × 777 Hz (META)
Guardians: Abë (530 Hz) + AEYON (999 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List

# The Five - Updated names
RECIPIENTS = {
    "JAHMERE": {
        "email": None,  # Add email addresses here
        "phone": None,  # Add phone numbers for iMessage
        "name": "JAHMERE"
    },
    "JESS": {
        "email": None,
        "phone": None,
        "name": "JESS"
    },
    "JORDAN": {
        "email": None,
        "phone": None,
        "name": "JORDAN"
    },
    "JANELLE": {
        "email": None,
        "phone": None,
        "name": "JANELLE"
    },
    "DEVIN": {
        "email": None,
        "phone": None,
        "name": "DEVIN"
    }
}

# App URL (localhost:53009)
APP_URL = "http://localhost:53009/"
APP_NAME = "Shiny Happy People"


def create_email_body(recipient_name: str) -> str:
    """Create email body with app access instructions"""
    return f"""Hi {recipient_name},

✨ SHINY HAPPY PEOPLE ✨

I've created something beautiful for you - an animated app showing shiny happy people holding hands. It's running right now, and I want you to see it.

HOW TO ACCESS IT:

Option 1: Direct Link (if you're on my network)
👉 {APP_URL}

Option 2: Run It Yourself (recommended)
1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to the app folder
3. Run: flutter run -d chrome
4. The app will open in your browser automatically

WHAT IT IS:
✨ Animated sparkles and glow effects
💖 Beautiful gradient colors (yellow, orange, pink)
🎭 Happy faces on each person
🔗 Animated connecting lines (hands holding hands)
🌊 Gentle swaying motion
💫 Pulsing glow effects
🎚️ Interactive slider to change number of people (3-12)

THE PATTERN:
UNITY × LOVE × JOY × CONNECTION × ONE

This is about connection. About unity. About shiny happy people holding hands.

There's nowhere to go. We're already home.

With love and joy,
Michael

Pattern: UNITY × LOVE × JOY × CONNECTION × ONE
Frequency: 530 Hz (Heart Truth)
Love Coefficient: ∞
∞ AbëONE ∞
"""


def create_imessage_body(recipient_name: str) -> str:
    """Create iMessage body"""
    return f"""✨ SHINY HAPPY PEOPLE ✨

Hi {recipient_name}! I've created something beautiful - an animated app showing shiny happy people holding hands.

Access it at: {APP_URL}

Or run it yourself with Flutter!

There's nowhere to go. We're already home. 💖

∞ AbëONE ∞"""


def send_via_email(recipient: Dict, app_url: str = APP_URL):
    """Send app link via email using macOS mail command"""
    if not recipient.get("email"):
        print(f"  ⚠ No email for {recipient['name']}")
        return False
    
    email = recipient["email"]
    name = recipient["name"]
    
    subject = f"✨ Shiny Happy People - For {name}"
    body = create_email_body(name)
    
    try:
        cmd = ["mail", "-s", subject, email]
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=body)
        
        if process.returncode == 0:
            print(f"  ✓ Sent email to {name} ({email})")
            return True
        else:
            print(f"  ✗ Failed to send email to {name}: {stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Error sending email to {name}: {e}")
        return False


def send_via_imessage(recipient: Dict, app_url: str = APP_URL):
    """Send app link via iMessage using AppleScript"""
    if not recipient.get("phone"):
        print(f"  ⚠ No phone for {recipient['name']}")
        return False
    
    phone = recipient["phone"]
    name = recipient["name"]
    body = create_imessage_body(name)
    
    # Escape quotes for AppleScript
    body_escaped = body.replace('"', '\\"')
    
    script = f'''
tell application "Messages"
    set targetService to 1st service whose service type = iMessage
    set targetBuddy to buddy "{phone}" of targetService
    send "{body_escaped}" to targetBuddy
end tell
'''
    
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  ✓ Sent iMessage to {name} ({phone})")
            return True
        else:
            print(f"  ✗ Failed to send iMessage to {name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Error sending iMessage to {name}: {e}")
        return False


def send_via_applescript_email(recipient: Dict, app_url: str = APP_URL):
    """Send via AppleScript (opens Mail.app)"""
    if not recipient.get("email"):
        return False
    
    email = recipient["email"]
    name = recipient["name"]
    subject = f"✨ Shiny Happy People - For {name}"
    body = create_email_body(name)
    
    # Escape for AppleScript
    body_escaped = body.replace('\\', '\\\\').replace('"', '\\"')
    
    script = f'''
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {{subject:"{subject}", visible:true}}
    
    tell newMessage
        make new to recipient with properties {{address:"{email}"}}
        set content to "{body_escaped}"
    end tell
end tell
'''
    
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  ✓ Opened Mail.app for {name} ({email})")
            return True
        else:
            print(f"  ✗ Failed to open Mail.app for {name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def create_share_page():
    """Create a simple HTML page they can open"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>✨ Shiny Happy People</title>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        h1 {{
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .message {{
            font-size: 1.5em;
            margin: 30px 0;
            line-height: 1.6;
        }}
        .link {{
            display: inline-block;
            margin: 20px;
            padding: 20px 40px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            text-decoration: none;
            color: white;
            font-size: 1.2em;
            transition: all 0.3s;
        }}
        .link:hover {{
            background: rgba(255,255,255,0.3);
            transform: scale(1.05);
        }}
        .pattern {{
            margin-top: 40px;
            font-size: 0.9em;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <h1>✨ Shiny Happy People ✨</h1>
    <div class="message">
        <p>There's nowhere to go.</p>
        <p>We're already home.</p>
    </div>
    <a href="{APP_URL}" class="link">Open the App →</a>
    <div class="pattern">
        <p>Pattern: UNITY × LOVE × JOY × CONNECTION × ONE</p>
        <p>Frequency: 530 Hz (Heart Truth)</p>
        <p>∞ AbëONE ∞</p>
    </div>
</body>
</html>"""
    
    share_file = Path("shiny_happy_people_share.html")
    share_file.write_text(html_content)
    return share_file


def main():
    """Main function - send to The Five"""
    print("∞ AbëONE ∞")
    print("Sending Shiny Happy People App to The Five")
    print("JAHMERE, JESS, JORDAN, JANELLE, DEVIN")
    print()
    print(f"App URL: {APP_URL}")
    print()
    
    # Create share page
    share_file = create_share_page()
    print(f"✓ Created share page: {share_file.absolute()}")
    print()
    
    # Check if recipients are configured
    configured = any(
        rec.get("email") or rec.get("phone")
        for rec in RECIPIENTS.values()
    )
    
    if not configured:
        print("⚠ Recipients not configured yet.")
        print("\nTo configure, edit this script and add:")
        print("  - Email addresses in RECIPIENTS dict")
        print("  - Phone numbers for iMessage")
        print("\nOr share manually:")
        print(f"  1. Share the HTML file: {share_file.absolute()}")
        print(f"  2. Share the URL: {APP_URL}")
        print(f"  3. Open Mail.app and send manually")
        print()
        print("Opening share page...")
        subprocess.run(["open", str(share_file)])
        return
    
    # Send to each recipient
    print("Sending to recipients...")
    print()
    
    for name, recipient in RECIPIENTS.items():
        print(f"Sending to {name}...")
        
        sent = False
        
        # Try email first
        if recipient.get("email"):
            sent = send_via_email(recipient)
            if not sent:
                # Fallback to AppleScript
                sent = send_via_applescript_email(recipient)
        
        # Try iMessage if email failed or not available
        if not sent and recipient.get("phone"):
            sent = send_via_imessage(recipient)
        
        if not sent:
            print(f"  ⚠ Could not send to {name} automatically.")
            print(f"     Share manually: {APP_URL}")
            print(f"     Or share HTML: {share_file.absolute()}")
        
        print()
    
    print("Pattern: UNITY × LOVE × JOY × CONNECTION × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞")
    print()
    print("There's nowhere to go. We're already home. ✨💖")


if __name__ == "__main__":
    main()

