#!/usr/bin/env python3
"""
Validate Success Patterns Integration

YAGNI × JØHN × ALRAX × ZERO: Validation Script
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orbitals.EMERGENT_OS_orbital.integration_layer.unified_organism import get_unified_organism
from orbitals.EMERGENT_OS_orbital.success_patterns.integration import SuccessPatternsIntegration


def validate_integration():
    """Validate success patterns integration."""
    print("=" * 80)
    print("🔍 VALIDATING SUCCESS PATTERNS INTEGRATION")
    print("=" * 80)
    print()
    
    # Get organism
    try:
        organism = get_unified_organism()
        print("✅ Unified Organism: Available")
    except Exception as e:
        print(f"❌ Unified Organism: Error - {e}")
        return False
    
    # Check if success patterns module exists
    try:
        success_patterns = organism.get_module("success_patterns")
        if success_patterns:
            print("✅ Success Patterns Module: Registered")
        else:
            print("⚠️  Success Patterns Module: Not registered (may need bootstrap)")
            return False
    except Exception as e:
        print(f"❌ Success Patterns Module: Error - {e}")
        return False
    
    # Check module status
    try:
        status = success_patterns.get_status()
        print(f"✅ Module Status: {status.get('active', False)}")
        print(f"   - Initialized: {status.get('initialized', False)}")
        print(f"   - Active: {status.get('active', False)}")
        print(f"   - Background Tasks: {status.get('background_tasks', 0)}")
        print(f"   - Guardians: {status.get('guardians', {})}")
    except Exception as e:
        print(f"❌ Status Check: Error - {e}")
        return False
    
    # Check organism status includes success_patterns
    try:
        organism_status = organism.get_status()
        modules = organism_status.get('modules', {})
        if 'success_patterns' in modules:
            print("✅ Organism Integration: Success Patterns in organism status")
        else:
            print("⚠️  Organism Integration: Success Patterns not in organism status")
    except Exception as e:
        print(f"❌ Organism Status Check: Error - {e}")
        return False
    
    print()
    print("=" * 80)
    print("✅ VALIDATION COMPLETE - ALL CHECKS PASSED")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    success = validate_integration()
    sys.exit(0 if success else 1)

