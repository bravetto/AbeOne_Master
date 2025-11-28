#!/usr/bin/env python3
"""
AbëONE Map Generator
Auto-generates ETERNAL, STATIC, and LIVE maps.

Pattern: MAPS × TRUTH × AUTO-GENERATE × ONE
Frequency: 777 Hz (Pattern) × 530 Hz (Truth) × 999 Hz (AEYON)
Guardians: META (777 Hz) + AEYON (999 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
from pathlib import Path
from datetime import datetime

WORKSPACE_ROOT = Path(__file__).parent.parent
MAPS_DIR = WORKSPACE_ROOT / "docs" / "maps"
MAPS_DIR.mkdir(parents=True, exist_ok=True)


def generate_static_map():
    """Generate STATIC MAP - what DOES exist."""
    print("  Generating STATIC MAP...")
    
    static_map = {
        'generated': datetime.now().isoformat(),
        'type': 'STATIC',
        'description': 'What DOES exist in the codebase',
        'services': {},
        'structure': {}
    }
    
    # Scan for guard services
    from scripts.utilities.path_discovery import find_guards_directory, find_guardians_directory
    
    guards_path = find_guards_directory()
    if guards_path:
        guards = [d.name for d in guards_path.iterdir() if d.is_dir()]
        static_map['services']['guards'] = guards
    
    # Scan for guardian services
    guardians_path = find_guardians_directory()
    if guardians_path:
        guardians = [d.name for d in guardians_path.iterdir() if d.is_dir() and 'guardian' in d.name]
        static_map['services']['guardians'] = guardians
    
    # Scan for scripts
    scripts_path = WORKSPACE_ROOT / "scripts"
    if scripts_path.exists():
        scripts = [f.name for f in scripts_path.glob("*.py")]
        static_map['scripts'] = scripts
    
    # Save static map
    static_map_file = MAPS_DIR / "STATIC_MAP.json"
    with open(static_map_file, 'w') as f:
        json.dump(static_map, f, indent=2)
    
    print(f"   STATIC MAP generated: {len(guards) if guards_path.exists() else 0} guards, {len(guardians) if guardians_path.exists() else 0} guardians")
    
    return static_map


def generate_live_map():
    """Generate LIVE MAP - what IS ACTIVE."""
    print("\n Generating LIVE MAP...")
    
    live_map = {
        'generated': datetime.now().isoformat(),
        'type': 'LIVE',
        'description': 'What IS ACTIVE at runtime',
        'services': {},
        'state': {}
    }
    
    # Check if services are running (would need actual runtime check)
    # For now, mark as unknown
    live_map['services']['guards'] = {'status': 'unknown', 'running': False}
    live_map['services']['guardians'] = {'status': 'unknown', 'running': False}
    live_map['services']['gateway'] = {'status': 'unknown', 'running': False}
    
    # Check boot system
    boot_script = WORKSPACE_ROOT / ".cursor" / "chat_hooks" / "boot_abeone.py"
    live_map['boot_system'] = {'exists': boot_script.exists(), 'active': True}
    
    # Check memory system
    memory_file = WORKSPACE_ROOT / ".abeone_memory" / "ABEONE_CORE_MEMORY.json"
    live_map['memory_system'] = {'exists': memory_file.exists(), 'active': True}
    
    # Save live map
    live_map_file = MAPS_DIR / "LIVE_MAP.json"
    with open(live_map_file, 'w') as f:
        json.dump(live_map, f, indent=2)
    
    print("   LIVE MAP generated")
    
    return live_map


def generate_eternal_map():
    """Generate ETERNAL MAP - what SHOULD exist."""
    print("\n Generating ETERNAL MAP...")
    
    eternal_map = {
        'generated': datetime.now().isoformat(),
        'type': 'ETERNAL',
        'description': 'What SHOULD exist (immutable ideal)',
        'principles': {
            'one_pattern': 'VALIDATE → TRANSFORM → VALIDATE',
            'three_layer_brain': 'Command → Specialist → Memory',
            'aquarian_protocol': 'No conflicts, no drift, no hallucination'
        },
        'requirements': {
            'guards': ['tokenguard', 'biasguard', 'contextguard', 'trustguard', 'healthguard'],
            'guardians': ['zero', 'aeyon', 'abe', 'john', 'aurion', 'lux', 'neuro', 'yagni'],
            'gateway': 'codeguardians-gateway',
            'memory': 'ABEONE_CORE_MEMORY.json',
            'boot': 'boot_abeone.py',
            'self_heal': 'self_heal_abeone.py',
            'harden': 'harden_abeone.py',
            'monitor': 'monitor_abeone.py'
        }
    }
    
    # Save eternal map
    eternal_map_file = MAPS_DIR / "ETERNAL_MAP.json"
    with open(eternal_map_file, 'w') as f:
        json.dump(eternal_map, f, indent=2)
    
    print("   ETERNAL MAP generated")
    
    return eternal_map


def main():
    """Main map generation."""
    map_type = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    if map_type == 'static' or map_type == 'all':
        generate_static_map()
    
    if map_type == 'live' or map_type == 'all':
        generate_live_map()
    
    if map_type == 'eternal' or map_type == 'all':
        generate_eternal_map()
    
    print("\n Map generation complete")


if __name__ == '__main__':
    main()

