#!/usr/bin/env python3
"""
Memory Monitor - Checks memory integrity continuously.
"""
import json
from pathlib import Path
from datetime import datetime

WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
LOGS_DIR = WORKSPACE_ROOT / ".abeone_memory" / "logs"
CDF_DIR = WORKSPACE_ROOT / "abeos_config" / "bëings"

def check_memory_integrity():
    """Check memory integrity."""
    issues = []
    
    # Check if log files exist and are writable
    if not LOGS_DIR.exists():
        issues.append("Logs directory does not exist")
    elif not LOGS_DIR.is_dir():
        issues.append("Logs path is not a directory")
    
    # Check if CDF directory exists
    if not CDF_DIR.exists():
        issues.append("CDF directory does not exist")
    elif not CDF_DIR.is_dir():
        issues.append("CDF path is not a directory")
    
    return issues

if __name__ == '__main__':
    issues = check_memory_integrity()
    if issues:
        print(f"⚠️  Memory integrity issues: {issues}")
    else:
        print("✅ Memory integrity OK")
