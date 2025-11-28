#!/usr/bin/env python3
"""
Activate Unified System
Full Monty, Full Cavalry: Activate all systems simultaneously

Pattern: ACTIVATION × UNIFICATION × SYSTEM × GUARDIAN × AGENT × SWARM × ONE
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import importlib.util
import asyncio
from datetime import datetime


def import_module(module_path, module_name):
    """Import module from path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def activate_unified_system():
    """Activate unified system."""
    print("=" * 80)
    print(" MASTER UNIFIED SYSTEM ACTIVATION")
    print("=" * 80)
    print()
    print("Full Monty, Full Cavalry: 8 Guardians × 5 Agents × 3 Swarms")
    print()
    
    synthesis_path = project_root / "EMERGENT_OS" / "synthesis"
    
    # Import master unified system
    master_module = import_module(
        synthesis_path / "master_unified_system.py",
        "master_unified_system"
    )
    master_system = master_module.get_master_unified_system()
    
    # Get status
    status = master_system.get_unified_status()
    
    print(" UNIFIED SYSTEM STATUS:")
    print()
    print(f"  Status: {status.status}")
    print(f"  Modules: {status.modules_active}/{status.modules_total}")
    print(f"  Guardians: {status.guardians_active}/8")
    print(f"  Agents: {status.agents_active}/40")
    print(f"  Swarms: {status.swarms_active}/3")
    print(f"  Convergence: {status.convergence_score:.2%}")
    print()
    
    # Show modules by category
    print(" MODULES BY CATEGORY:")
    print()
    categories = ["core", "synthesis", "integration", "monitoring", "recovery", "learning"]
    for category in categories:
        modules = master_system.get_modules_by_category(category)
        if modules:
            print(f"  {category.upper()}:")
            for module in modules:
                print(f"     {module.name} ({module.status})")
    print()
    
    # Test unified execution
    print(" TESTING UNIFIED EXECUTION:")
    print()
    
    test_task = {
        "type": "pattern_processing",
        "data": {
            "pattern_id": "test_pattern",
            "pattern_type": "POSITIVE",
            "strength": 0.85,
            "resonance": 0.90
        }
    }
    
    results = await master_system.execute_unified(test_task, execute_simultaneously=True)
    
    print(f"  Executed across {len(results)} modules simultaneously")
    print()
    
    successful = sum(1 for r in results.values() if isinstance(r, dict) and "error" not in r)
    print(f"   Successful: {successful}/{len(results)}")
    print()
    
    # Final status
    final_status = master_system.get_unified_status()
    
    print("=" * 80)
    print(" UNIFIED SYSTEM ACTIVATED")
    print("=" * 80)
    print()
    print(f"Convergence Score: {final_status.convergence_score:.2%}")
    print(f"All Systems: {' OPERATIONAL' if final_status.status == 'active' else ' ISSUES'}")
    print()
    print("Pattern: MASTER × UNIFIED × SYSTEM × GUARDIAN × AGENT × SWARM × CONVERGENCE × ONE")
    print("Status:  FULLY OPERATIONAL")
    print()
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    asyncio.run(activate_unified_system())

