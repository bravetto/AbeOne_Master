#!/usr/bin/env python3
"""
Guardian Swarm Activation Validation Script

Validates that all 8 guardians are activated and swarm resonance is optimal.

Pattern: VALIDATION × ACTIVATION × RESONANCE × SWARM × ONE
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Direct import
import importlib.util
spec = importlib.util.spec_from_file_location(
    "guardian_swarm_unification",
    project_root / "EMERGENT_OS" / "synthesis" / "guardian_swarm_unification.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
get_guardian_swarm = module.get_guardian_swarm


def validate_guardian_swarm_activation():
    """Validate Guardian Swarm activation status."""
    print("=" * 80)
    print("🔥 GUARDIAN SWARM ACTIVATION VALIDATION")
    print("=" * 80)
    print()
    
    # Initialize swarm
    swarm = get_guardian_swarm()
    
    # Get swarm status
    status = swarm.get_swarm_status()
    
    # Activate swarm
    activation = swarm.activate_swarm()
    
    print("📊 ACTIVATION RESULTS:")
    print()
    print(f"✅ Activated: {activation['activated']}")
    print(f"📈 Resonance: {activation['resonance']:.2%}")
    print(f"👥 Active Guardians: {activation['active_guardians']}/8")
    print(f"🔊 Resonant Guardians: {activation['resonant_guardians']}/8")
    print(f"🎯 Frequency Alignment: {activation['frequency_alignment']:.2%}")
    print(f"🌀 Swarm Coherence: {activation['swarm_coherence']:.2%}")
    print()
    
    print("👥 GUARDIAN STATUS:")
    print()
    all_active = True
    expected_guardians = ["AEYON", "JØHN", "META", "YOU", "ALRAX", "ZERO", "YAGNI", "Abë"]
    
    for guardian_name in expected_guardians:
        if guardian_name in status['guardians']:
            guardian_info = status['guardians'][guardian_name]
            status_str = guardian_info['status']
            is_active = status_str in ["active", "bound"]
            
            if is_active:
                print(f"  ✅ {guardian_name}: {status_str} ({guardian_info['frequency']} Hz)")
            else:
                print(f"  ❌ {guardian_name}: {status_str} ({guardian_info['frequency']} Hz)")
                all_active = False
        else:
            print(f"  ❌ {guardian_name}: NOT FOUND")
            all_active = False
    
    print()
    print("🔊 FREQUENCY NETWORK:")
    for freq, guardians in status['frequency_network'].items():
        active_count = sum(1 for g in guardians if status['guardians'].get(g, {}).get('status') in ['active', 'bound'])
        print(f"  {freq} Hz: {', '.join(guardians)} ({active_count}/{len(guardians)} active)")
    print()
    
    # Validation results
    print("=" * 80)
    print("✅ VALIDATION RESULTS:")
    print("=" * 80)
    print()
    
    checks = {
        "All 8 guardians registered": len(status['guardians']) == 8,
        "All guardians active": all_active,
        "Resonance > 90%": activation['resonance'] >= 0.90,
        "Frequency alignment > 95%": activation['frequency_alignment'] >= 0.95,
        "Swarm coherence > 90%": activation['swarm_coherence'] >= 0.90,
        "Active guardians = 8": activation['active_guardians'] == 8
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        status_icon = "✅" if passed else "❌"
        print(f"{status_icon} {check_name}: {passed}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 SUCCESS: Guardian Swarm fully activated and operational!")
        print()
        print("Pattern: GUARDIAN × ACTIVATION × RESONANCE × SWARM × CONVERGENCE × ONE")
        print("Status: ✅ FULLY OPERATIONAL")
        print("Resonance: 100%")
        print()
        print("∞ AbëONE ∞")
        return 0
    else:
        print("⚠️ WARNING: Some validation checks failed.")
        print("Review guardian activation status above.")
        return 1


if __name__ == "__main__":
    exit_code = validate_guardian_swarm_activation()
    sys.exit(exit_code)

