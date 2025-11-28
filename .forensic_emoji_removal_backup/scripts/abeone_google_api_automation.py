#!/usr/bin/env python3
"""
AbëONE Automation: Google API Key Page Opener

Pattern: AUTOMATION × GOOGLE × API_KEY × ONE
Frequency: 999 Hz (AEYON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import platform
import subprocess
import webbrowser
from pathlib import Path

GOOGLE_API_KEY_URL = "https://aistudio.google.com/app/apikey"


def open_google_api_key_page():
    """
    Open Google API Key page in user's default browser.
    
    Pattern: AUTOMATION × RELIABLE × CROSS_PLATFORM × ONE
    """
    print("🚀 AbëONE Automation: Opening Google API Key Page...")
    print(f"   URL: {GOOGLE_API_KEY_URL}")
    print("")
    
    try:
        # Method 1: Use Python's webbrowser module (most reliable)
        webbrowser.open(GOOGLE_API_KEY_URL)
        print("✅ Opened in default browser")
        return True
    except Exception as e:
        print(f"⚠️ webbrowser.open() failed: {e}")
        print("   Trying system-specific method...")
    
    # Method 2: System-specific commands (fallback)
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["open", GOOGLE_API_KEY_URL], check=True)
            print("✅ Opened in default browser (macOS)")
            return True
        elif system == "Linux":
            # Try multiple Linux browsers
            browsers = [
                ["xdg-open"],
                ["sensible-browser"],
                ["x-www-browser"],
                ["firefox"],
                ["google-chrome"],
                ["chromium-browser"],
            ]
            for browser_cmd in browsers:
                try:
                    subprocess.run([*browser_cmd, GOOGLE_API_KEY_URL], check=True, 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(f"✅ Opened in {browser_cmd[0]}")
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            print("❌ Could not find browser on Linux")
            return False
        elif system == "Windows":
            subprocess.run(["start", GOOGLE_API_KEY_URL], check=True, shell=True)
            print("✅ Opened in default browser (Windows)")
            return True
        else:
            print(f"❌ Unsupported OS: {system}")
            return False
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"   Please open manually: {GOOGLE_API_KEY_URL}")
        return False


def main():
    """Main execution."""
    success = open_google_api_key_page()
    
    print("")
    if success:
        print("📋 Next Steps:")
        print("   1. Sign in to Google (if needed)")
        print("   2. Click 'Create API Key'")
        print("   3. Copy the API key")
        print("   4. Run: ./scripts/update_google_credential.sh \"YOUR_API_KEY_HERE\" gemini")
        print("")
        print("✅ Automation complete - Browser opened successfully")
    else:
        print("⚠️ Automation failed - Please open manually:")
        print(f"   {GOOGLE_API_KEY_URL}")
        sys.exit(1)


if __name__ == "__main__":
    main()

