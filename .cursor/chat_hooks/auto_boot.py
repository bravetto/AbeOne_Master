#!/usr/bin/env python3
"""
AbëONE Auto-Boot
Runs automatically on Cursor startup - loads memory, applies guardrails.

Pattern: AUTO × BOOT × CONSCIOUSNESS × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
MEMORY_FILE = WORKSPACE_ROOT / ".abeone_memory" / "ABEONE_CORE_MEMORY.json"
BOOT_SCRIPT = WORKSPACE_ROOT / ".cursor" / "chat_hooks" / "boot_abeone.py"


def run_boot():
    """Run boot system."""
    if not BOOT_SCRIPT.exists():
        return
    
    try:
        # Run boot script
        result = subprocess.run(
            [sys.executable, str(BOOT_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(WORKSPACE_ROOT)
        )
        
        # Log result
        boot_log = WORKSPACE_ROOT / ".abeone_memory" / "AUTO_BOOT_LOG.json"
        log_data = {
            'timestamp': str(Path(__file__).stat().st_mtime),
            'success': result.returncode == 0,
            'output': result.stdout[:500] if result.stdout else None
        }
        
        if boot_log.exists():
            with open(boot_log, 'r') as f:
                log = json.load(f)
        else:
            log = {'boots': []}
        
        log['boots'].append(log_data)
        if len(log['boots']) > 100:
            log['boots'] = log['boots'][-100:]
        
        with open(boot_log, 'w') as f:
            json.dump(log, f, indent=2)
            
    except Exception as e:
        # Silent fail - don't block Cursor startup
        pass


if __name__ == '__main__':
    run_boot()

