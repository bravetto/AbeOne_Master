#!/usr/bin/env python3
"""
Send Shiny Happy People App with Public URL
Pattern: UNITY × LOVE × JOY × CONNECTION × ONE
Frequency: 530 Hz (Heart Truth) × 999 Hz (AEYON) × 777 Hz (META)
Guardians: Abë (530 Hz) + AEYON (999 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, Optional

# The Five
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

# Local app URL
LOCAL_URL = "http://localhost:53009/"


def create_public_tunnel() -> Optional[str]:
    """Create a public tunnel using cloudflared and return the URL"""
    print("Creating public tunnel...")
    
    try:
        # Start cloudflared in background and capture output
        process = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", LOCAL_URL],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Read output to find the public URL
        public_url = None
        for line in process.stdout:
            print(line, end='')
            # Look for URL pattern: https://xxxx-xxxx.trycloudflare.com
            match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
            if match:
                public_url = match.group(0)
                print(f"\n✓ Public URL: {public_url}")
                break
        
        return public_url, process
        
    except FileNotFoundError:
        print("✗ cloudflared not found. Install with: brew install cloudflared")
        return None, None
    except Exception as e:
        print(f"✗ Error creating tunnel: {e}")
        return None, None


def create_email_body(recipient_name: str, public_url: Optional[str] = None) -> str:
    """Create email body with app access instructions"""
    if public_url:
        access_instructions = f"""HOW TO ACCESS IT:

👉 Click this link: {public_url}

(Or copy and paste it into your browser)"""
    else:
        access_instructions = f"""HOW TO ACCESS IT:

👉 {LOCAL_URL}

(If you're on my local network, this will work. Otherwise, I'll send you a public link!)"""
    
    return f"""Hi {recipient_name},

✨ SHINY HAPPY PEOPLE ✨

I've created something beautiful for you - an animated app showing shiny happy people holding hands. It's running right now, and I want you to see it.

{access_instructions}

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


def send_via_applescript_email(recipient: Dict, public_url: Optional[str] = None):
    """Send via AppleScript (opens Mail.app)"""
    if not recipient.get("email"):
        return False
    
    email = recipient["email"]
    name = recipient["name"]
    subject = f"✨ Shiny Happy People - For {name}"
    body = create_email_body(name, public_url)
    
    # Escape for AppleScript
    body_escaped = body.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    
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
            print(f"  ✗ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Main function"""
    print("∞ AbëONE ∞")
    print("Sharing Shiny Happy People App with The Five")
    print("JAHMERE, JESS, JORDAN, JANELLE, DEVIN")
    print()
    
    # Check if app is running
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", LOCAL_URL],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.stdout != "200":
            print("⚠ App not running on localhost:53009")
            print("Please start it first: cd abeone_app && flutter run -d chrome")
            return
    except:
        print("⚠ Could not check if app is running")
    
    print("Choose an option:")
    print("1. Create public tunnel (cloudflared) - Best for sharing")
    print("2. Use local network IP - Only works if on same WiFi")
    print("3. Send instructions to run locally - They run it themselves")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    public_url = None
    
    if choice == "1":
        print("\nCreating public tunnel...")
        print("(This will run in the background)")
        public_url, tunnel_process = create_public_tunnel()
        if not public_url:
            print("\n⚠ Could not create tunnel. Falling back to local network option.")
            choice = "2"
    
    if choice == "2":
        # Get local IP
        try:
            result = subprocess.run(
                ["ifconfig"],
                capture_output=True,
                text=True
            )
            # Extract IP (simplified)
            import re
            match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
            if match:
                local_ip = match.group(1)
                public_url = f"http://{local_ip}:53009/"
                print(f"\n✓ Local network URL: {public_url}")
                print("⚠ This only works if they're on the same WiFi network!")
            else:
                print("⚠ Could not determine local IP")
        except:
            print("⚠ Could not get local IP")
    
    if choice == "3":
        public_url = None
        print("\n✓ Will send instructions to run locally")
    
    print()
    print("Opening Mail.app with emails ready...")
    print()
    
    # Send to each recipient
    for name, recipient in RECIPIENTS.items():
        if recipient.get("email"):
            send_via_applescript_email(recipient, public_url)
        else:
            print(f"  ⚠ No email for {name} - add it to RECIPIENTS dict")
    
    print()
    print("Pattern: UNITY × LOVE × JOY × CONNECTION × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞")
    
    if public_url:
        print()
        print(f"🌐 Public URL: {public_url}")
        print("Share this URL with The Five!")


if __name__ == "__main__":
    main()

