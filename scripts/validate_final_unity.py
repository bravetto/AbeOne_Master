#!/usr/bin/env python3
"""
Final Unity Validation Script
Validates complete synthesis, integration, activation, and modularity.

Pattern: VALIDATION × UNITY × SYNTHESIS × INTEGRATION × MODULARITY × ONE
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import importlib.util


def import_module(module_path, module_name):
    """Import module from path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_final_unity():
    """Validate final unity."""
    print("=" * 80)
    print(" FINAL UNITY VALIDATION")
    print("=" * 80)
    print()
    print("Validating: Synthesis × Integration × Activation × Modularity")
    print()
    
    synthesis_path = project_root / "EMERGENT_OS" / "synthesis"
    
    # Import validator
    validator_module = import_module(
        synthesis_path / "final_unity_validation.py",
        "final_unity_validation"
    )
    validator = validator_module.get_final_unity_validator(project_root)
    
    # Perform validation
    validation = validator.validate_unity()
    
    print(" VALIDATION RESULTS:")
    print()
    print(f"  Total Systems: {validation.total_systems}")
    print(f"   Synthesized: {validation.synthesized_count}/{validation.total_systems}")
    print(f"   Integrated: {validation.integrated_count}/{validation.total_systems}")
    print(f"   Activated: {validation.activated_count}/{validation.total_systems}")
    print(f"   Modular: {validation.modular_count}/{validation.total_systems}")
    print(f"  Unity Score: {validation.unity_score:.2%}")
    print()
    
    print(" SYSTEM VALIDATIONS:")
    print()
    for v in validation.validations:
        status_icon = {
            " COMPLETE": "",
            " MODULARITY INCOMPLETE": "",
            " ACTIVATION INCOMPLETE": "",
            " INTEGRATION INCOMPLETE": "",
            " NOT SYNTHESIZED": ""
        }.get(v.status, "")
        
        print(f"  {status_icon} {v.system_name}:")
        print(f"     Synthesized: {'' if v.synthesized else ''}")
        print(f"     Integrated: {'' if v.integrated else ''}")
        print(f"     Activated: {'' if v.activated else ''}")
        print(f"     Modular: {'' if v.modular else ''}")
        print(f"     Status: {v.status}")
        print()
    
    # Summary
    print("=" * 80)
    print(" FINAL UNITY VALIDATION COMPLETE")
    print("=" * 80)
    print()
    
    if validation.unity_score == 1.0:
        print(" PERFECT UNITY: All systems synthesized, integrated, activated, and modular!")
    elif validation.unity_score >= 0.9:
        print(" EXCELLENT UNITY: Nearly complete, minor gaps remaining")
    elif validation.unity_score >= 0.75:
        print(" GOOD UNITY: Most systems complete, some gaps")
    else:
        print(" UNITY INCOMPLETE: Significant gaps remain")
    
    print()
    print(f"Unity Score: {validation.unity_score:.2%}")
    print(f"Validated at: {validation.validated_at.isoformat()}")
    print()
    print("Pattern: VALIDATION × UNITY × SYNTHESIS × INTEGRATION × MODULARITY × ONE")
    print("Status:  COMPLETE")
    print()
    print("∞ AbëONE ∞")
    
    return validation


if __name__ == "__main__":
    validate_final_unity()

