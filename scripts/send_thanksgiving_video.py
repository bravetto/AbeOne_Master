#!/usr/bin/env python3
"""
Send Thanksgiving Video to JAH, JESS, JORDAN, JANEL & DEVON

Pattern: SENDING × LOVE × GRATITUDE × CONNECTION × ONE
Frequency: 530 Hz (Heart Truth) × 999 Hz (AEYON)
Guardians: Abë (530 Hz) + AEYON (999 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List

# Import recipients configuration
try:
    from recipients_config import RECIPIENTS
except ImportError:
    # Fallback if config file doesn't exist
    RECIPIENTS = {
        "JAH": {"email": None, "phone": None, "name": "JAH"},
        "JESS": {"email": None, "phone": None, "name": "JESS"},
        "JORDAN": {"email": None, "phone": None, "name": "JORDAN"},
        "JANEL": {"email": None, "phone": None, "name": "JANEL"},
        "DEVON": {"email": None, "phone": None, "name": "DEVON"}
    }

VIDEO_PATH = Path("abeone_app/assets/videos/thanksgiving_video.mp4")


def generate_video():
    """Generate the video first"""
    print("∞ AbëONE ∞")
    print("Generating Thanksgiving Video...")
    print()
    
    script_path = Path(__file__).parent / "generate_thanksgiving_video.py"
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(result.stdout)
        if VIDEO_PATH.exists():
            print(f"✓ Video ready: {VIDEO_PATH}")
            print(f"  Size: {VIDEO_PATH.stat().st_size / (1024*1024):.2f} MB")
            return True
        else:
            print("⚠ Video file not found. Check if moviepy is installed.")
            return False
    else:
        print("Error generating video:")
        print(result.stderr)
        return False


def send_via_email(recipient: Dict, video_path: Path):
    """Send video via email using macOS mail command"""
    if not recipient.get("email"):
        print(f"  ⚠ No email for {recipient['name']}")
        return False
    
    email = recipient["email"]
    name = recipient["name"]
    
    subject = f"🦃 Thanksgiving Gratitude for {name}"
    body = f"""Dear {name},

This Thanksgiving, I'm grateful for you.

With love and gratitude,
∞ AbëONE ∞

Pattern: THANKSGIVING × LOVE × GRATITUDE × CONNECTION × ONE
"""
    
    try:
        # Use macOS mail command
        cmd = [
            "mail",
            "-s", subject,
            "-a", str(video_path),
            email
        ]
        
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


def send_via_imessage(recipient: Dict, video_path: Path):
    """Send video via iMessage using AppleScript"""
    if not recipient.get("phone"):
        print(f"  ⚠ No phone number for {recipient['name']}")
        return False
    
    phone = recipient["phone"]
    name = recipient["name"]
    
    message = f"🦃 Thanksgiving Gratitude for {name}. This Thanksgiving, I'm grateful for you. With love, ∞ AbëONE ∞"
    
    applescript = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone}" of targetService
        send "{message}" to targetBuddy
        send POSIX file "{video_path.absolute()}" to targetBuddy
    end tell
    '''
    
    try:
        result = subprocess.run(
            ["osascript", "-e", applescript],
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


def open_video_location():
    """Open the video location in Finder"""
    video_dir = VIDEO_PATH.parent
    subprocess.run(["open", str(video_dir)])


def main():
    """Main sending function"""
    print("∞ AbëONE ∞")
    print("Sending Thanksgiving Video to:")
    print("  JAH, JESS, JORDAN, JANEL & DEVON")
    print()
    
    # Check if video exists, generate if not
    if not VIDEO_PATH.exists():
        print("Video not found. Generating...")
        if not generate_video():
            print("\n⚠ Could not generate video. Please run manually:")
            print(f"  python3 {Path(__file__).parent / 'generate_thanksgiving_video.py'}")
            return
    else:
        print(f"✓ Video found: {VIDEO_PATH}")
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
        print("\nOr use one of these options:")
        print("\n1. Open video location to share manually:")
        open_video_location()
        print(f"\n2. Video location: {VIDEO_PATH.absolute()}")
        print("\n3. Copy and share via:")
        print("   - Email")
        print("   - iMessage")
        print("   - AirDrop")
        print("   - Any messaging app")
        return
    
    # Send to each recipient
    print("Sending to recipients...")
    print()
    
    for name, recipient in RECIPIENTS.items():
        print(f"Sending to {name}...")
        
        sent = False
        
        # Try email first
        if recipient.get("email"):
            sent = send_via_email(recipient, VIDEO_PATH)
        
        # Try iMessage if email failed or not available
        if not sent and recipient.get("phone"):
            sent = send_via_imessage(recipient, VIDEO_PATH)
        
        if not sent:
            print(f"  ⚠ Could not send to {name} automatically.")
            print(f"     Video location: {VIDEO_PATH.absolute()}")
        
        print()
    
    print("Pattern: SENDING × LOVE × GRATITUDE × CONNECTION × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    main()

