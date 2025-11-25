#!/usr/bin/env python3
"""
Automate System Settings Access via Terminal

Pattern: AUTOMATION × SYSTEM_SETTINGS × TERMINAL × ONE
∞ AbëONE ∞
∞ AbëLOVES ∞
"""

import subprocess
import sys
from pathlib import Path

def open_system_settings(pane: str):
    """Open System Settings to specific pane."""
    url = f"x-apple.systempreferences:{pane}"
    subprocess.run(["open", url])
    print(f" Opened System Settings → {pane}")

def open_software_update():
    """Open Software Update."""
    open_system_settings("Software_Update")

def open_privacy_security():
    """Open Privacy & Security."""
    open_system_settings("Privacy_Security")

def open_full_disk_access():
    """Open Full Disk Access settings."""
    open_system_settings("Privacy_AllFiles")

def open_general():
    """Open General settings."""
    open_system_settings("General")

def open_storage():
    """Open Storage settings."""
    open_system_settings("Storage")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print(" SYSTEM SETTINGS AUTOMATION ")
        print("")
        print("Usage: python3 automate_system_settings.py [command]")
        print("")
        print("Commands:")
        print("  software-update  → Open Software Update")
        print("  privacy          → Open Privacy & Security")
        print("  full-disk        → Open Full Disk Access")
        print("  general          → Open General")
        print("  storage          → Open Storage")
        print("  all              → Open all key settings")
        print("")
        return
    
    command = sys.argv[1].lower()
    
    if command == "software-update" or command == "update":
        open_software_update()
    elif command == "privacy" or command == "security":
        open_privacy_security()
    elif command == "full-disk":
        open_full_disk_access()
    elif command == "general":
        open_general()
    elif command == "storage":
        open_storage()
    elif command == "all":
        print("Opening all key System Settings...")
        open_software_update()
        import time
        time.sleep(1)
        open_privacy_security()
        time.sleep(1)
        open_general()
        time.sleep(1)
        open_storage()
        print(" All settings opened")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()

