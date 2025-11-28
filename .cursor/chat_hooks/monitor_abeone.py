#!/usr/bin/env python3
"""
AbëONE Monitoring System
Continuously monitors system health and triggers self-healing.

Pattern: MONITOR × HEALTH × PROTECTION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
MONITOR_LOG = WORKSPACE_ROOT / ".abeone_memory" / "MONITOR_LOG.json"
MEMORY_FILE = WORKSPACE_ROOT / ".abeone_memory" / "ABEONE_CORE_MEMORY.json"


def check_system_health():
    """Check overall system health."""
    health_checks = {
        'memory_exists': MEMORY_FILE.exists(),
        'memory_readable': False,
        'boot_script_exists': False,
        'handlers_exist': False
    }
    
    # Check memory readability
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, 'r') as f:
                json.load(f)
            health_checks['memory_readable'] = True
        except:
            pass
    
    # Check boot script
    boot_script = WORKSPACE_ROOT / ".cursor" / "chat_hooks" / "boot_abeone.py"
    health_checks['boot_script_exists'] = boot_script.exists()
    
    # Check handlers
    handlers = [
        "scripts/abeone-memory-loader.py",
        "scripts/abeone-validator.py"
    ]
    health_checks['handlers_exist'] = all(
        (WORKSPACE_ROOT / handler).exists() for handler in handlers
    )
    
    # Calculate health score
    health_score = sum(health_checks.values()) / len(health_checks) * 100
    
    return health_checks, health_score


def trigger_healing_if_needed(health_score):
    """Trigger self-healing if health score is low."""
    if health_score < 75:
        heal_script = WORKSPACE_ROOT / ".cursor" / "chat_hooks" / "self_heal_abeone.py"
        if heal_script.exists():
            try:
                subprocess.Popen(
                    [sys.executable, str(heal_script)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return True
            except:
                pass
    return False


def log_monitor_event(health_checks, health_score, healing_triggered):
    """Log monitoring event."""
    monitor_data = {
        'timestamp': datetime.now().isoformat(),
        'health_checks': health_checks,
        'health_score': health_score,
        'healing_triggered': healing_triggered,
        'monitor': 'monitor_abeone.py'
    }
    
    if MONITOR_LOG.exists():
        with open(MONITOR_LOG, 'r') as f:
            log = json.load(f)
    else:
        log = {'monitors': []}
    
    log['monitors'].append(monitor_data)
    
    # Keep last 100 monitors
    if len(log['monitors']) > 100:
        log['monitors'] = log['monitors'][-100:]
    
    with open(MONITOR_LOG, 'w') as f:
        json.dump(log, f, indent=2)


def main():
    """Main monitoring execution."""
    # Check health
    health_checks, health_score = check_system_health()
    
    # Trigger healing if needed
    healing_triggered = trigger_healing_if_needed(health_score)
    
    # Log event
    log_monitor_event(health_checks, health_score, healing_triggered)
    
    # Output (for debugging)
    if health_score < 75:
        print(f"⚠️  System health: {health_score:.1f}%")
        if healing_triggered:
            print("  🔧 Self-healing triggered")
    else:
        print(f"✅ System health: {health_score:.1f}%")


if __name__ == '__main__':
    main()

