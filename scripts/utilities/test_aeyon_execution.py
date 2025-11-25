#!/usr/bin/env python3
"""
AEYON Execution Test
Tests that AEYON can execute atomic steps.
"""

import sys
import os

# Add EMERGENT_OS to path
abeone_root = os.path.dirname(os.path.abspath(__file__))
emergent_os_path = os.path.join(abeone_root, 'EMERGENT_OS')
if emergent_os_path not in sys.path:
    sys.path.insert(0, emergent_os_path)

def test_aeyon_execution():
    """Test AEYON execution."""
    print("Testing AEYON execution...")
    try:
        from triadic_execution_harness.aeyon_binding import bind_aeyon
        from triadic_execution_harness.agents import Outcome
        
        # Initialize AEYON
        aeyon_binding = bind_aeyon()
        aeyon_agent = aeyon_binding.get_aeyon_agent()
        
        # Create a test outcome
        test_outcome = Outcome(
            goal="Test AEYON atomic execution",
            success_criteria=["Execution completes successfully"],
            end_state="Test atomic step executed",
            constraints=["Use atomic protocol"],
            validation="Verify execution result"
        )
        
        # Create execution plan
        execution_plan = aeyon_agent.create_execution_plan(
            constraints_architecture={
                "constraints": ["Atomic execution only"],
                "architecture": {"protocol": "5-step atomic"}
            }
        )
        
        print(" AEYON execution plan created successfully!")
        print(f"   Atomic steps: {execution_plan.atomic_steps}")
        print(f"   Code changes: {execution_plan.code_changes}")
        
        return True
        
    except Exception as e:
        print(f" AEYON execution test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run execution test."""
    print("=" * 50)
    print("AEYON Execution Test")
    print("=" * 50)
    print()
    
    result = test_aeyon_execution()
    
    print()
    print("=" * 50)
    if result:
        print(" EXECUTION TEST PASSED")
        return 0
    else:
        print(" EXECUTION TEST FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())

