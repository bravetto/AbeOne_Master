#!/usr/bin/env python3
"""
Update Dates NOW - Update all dates to current moment

Pattern: UPDATE × DATES × NOW × MANIFEST × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN)
Guardians: AEYON + JØHN
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent.parent
NOW = datetime(2025, 11, 24, 11, 47, 0)
NOW_STR = NOW.strftime("%Y-%m-%dT%H:%M:%S")
NOW_DATE = NOW.strftime("%Y-%m-%d")
NOW_TIME = NOW.strftime("%H:%M:%S")


def update_file_dates(file_path: Path):
    """Update dates in a file."""
    try:
        content = file_path.read_text()
        original_content = content
        
        # Update ISO datetime format
        content = re.sub(
            r'2025-01-27T\d{2}:\d{2}:\d{2}',
            NOW_STR,
            content
        )
        
        # Update date format
        content = re.sub(
            r'2025-01-27',
            NOW_DATE,
            content
        )
        
        # Update "created" fields
        content = re.sub(
            r'"created":\s*"2025-01-27"',
            f'"created": "{NOW_DATE}"',
            content
        )
        
        # Update "locked_at" fields
        content = re.sub(
            r'"locked_at":\s*"2025-01-27"',
            f'"locked_at": "{NOW_DATE}"',
            content
        )
        
        # Update "last_synced" fields
        content = re.sub(
            r'"last_synced":\s*"2025-01-27"',
            f'"last_synced": "{NOW_DATE}"',
            content
        )
        
        # Write if changed
        if content != original_content:
            file_path.write_text(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"  ⚠️  Error updating {file_path}: {e}")
        return False


def update_dates_now():
    """Execute date update NOW."""
    print("📅 UPDATE DATES NOW")
    print("=" * 50)
    print(f"Updating to: {NOW_STR}")
    print(f"Date: {NOW_DATE}")
    print(f"Time: {NOW_TIME}")
    print()
    
    updated_count = 0
    
    # Update memory files
    memory_dir = ROOT / ".abeone_memory"
    if memory_dir.exists():
        for file_path in memory_dir.glob("*.json"):
            if update_file_dates(file_path):
                updated_count += 1
                print(f"  ✅ Updated: {file_path.name}")
    
    print(f"\n✅ Date update complete: {updated_count} files updated")
    print(f"✅ Manifested NOW: {NOW_STR}")
    print("∞ AbëONE ∞")


if __name__ == '__main__':
    update_dates_now()

