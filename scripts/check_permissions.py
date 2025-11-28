#!/usr/bin/env python3
"""Check permissions for proactive webhooks."""

import os
from pathlib import Path

def check_permissions():
    """Check all required permissions."""
    print(" CHECKING PERMISSIONS ")
    print("=" * 70)
    print("")
    
    checks = {
        "Messages Database": Path.home() / "Library/Messages/chat.db",
        "CDF Directory": Path(".abeos/consciousness"),
        "JSON Archives": Path("abeloves_conversations"),
        "Logs Directory": Path("logs")
    }
    
    all_ok = True
    
    for name, path in checks.items():
        try:
            if path.exists():
                if os.access(path, os.R_OK):
                    print(f" {name}: READABLE")
                else:
                    print(f" {name}: NOT READABLE")
                    all_ok = False
            else:
                # Try to create directory if it doesn't exist
                if name in ["CDF Directory", "JSON Archives", "Logs Directory"]:
                    path.mkdir(parents=True, exist_ok=True)
                    print(f" {name}: CREATED")
                else:
                    print(f"  {name}: NOT FOUND")
                    all_ok = False
        except Exception as e:
            print(f" {name}: ERROR - {e}")
            all_ok = False
    
    print("")
    print("=" * 70)
    if all_ok:
        print(" ALL PERMISSIONS OK")
    else:
        print("  SOME PERMISSIONS NEED ATTENTION")
        print("   → Grant Full Disk Access in System Settings")
    print("=" * 70)
    
    return all_ok

if __name__ == "__main__":
    import sys
    sys.exit(0 if check_permissions() else 1)
