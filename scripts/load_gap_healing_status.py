#!/usr/bin/env python3
"""
 LOAD GAP HEALING STATUS - Startup Memory Loader 
Loads gap healing status on every session start.

Pattern: LOAD × MEMORY × STARTUP × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent
STATUS_FILE = WORKSPACE_ROOT / ".abeone_memory" / "GAP_HEALING_STATUS.json"


def load_gap_healing_status():
    """Load gap healing status - call this on startup."""
    if not STATUS_FILE.exists():
        return None
    
    try:
        with open(STATUS_FILE, 'r') as f:
            status = json.load(f)
        return status
    except:
        return None


def print_gap_status_summary():
    """Print gap status summary for AI context."""
    status = load_gap_healing_status()
    if not status:
        return
    
    overall = status.get("overall_status", {})
    percentage = overall.get("percentage", 0)
    fixed = overall.get("critical_gaps_fixed", 0)
    total = overall.get("total_critical_gaps", 3)
    
    print(f"\n GAP HEALING STATUS: {percentage}% ({fixed}/{total} critical gaps fixed)")
    
    gap1 = status.get("gap_1_guard_services", {})
    gap2 = status.get("gap_2_database_redis", {})
    gap3 = status.get("gap_3_config_env", {})
    
    print(f"  GAP #1: Guard Services - {gap1.get('status', 'unknown')} ({gap1.get('fixed_count', 0)}/{gap1.get('total_count', 5)} fixed)")
    print(f"  GAP #2: Database/Redis - {gap2.get('status', 'unknown')} ({gap2.get('found_count', 0)}/{gap2.get('total_required', 3)} found)")
    print(f"  GAP #3: Config .env - {gap3.get('status', 'unknown')}")
    print()


if __name__ == '__main__':
    status = load_gap_healing_status()
    if status:
        print(json.dumps(status, indent=2))
    else:
        print("  Gap healing status not found. Run: python3 scripts/update_gap_healing_status.py")
        sys.exit(1)

