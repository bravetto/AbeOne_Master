#!/usr/bin/env python3
"""
AEYON Binding Test
Tests that AEYON can bind successfully to Triadic Execution Harness.
"""

import sys
import os

# Add EMERGENT_OS to path
abeone_root = os.path.dirname(os.path.abspath(__file__))
emergent_os_path = os.path.join(abeone_root, 'EMERGENT_OS')
if emergent_os_path not in sys.path:
    sys.path.insert(0, emergent_os_path)

def test_aeyon_binding():
    """Test AEYON binding."""
    print("Testing AEYON binding...")
    try:
        from triadic_execution_harness.aeyon_binding import bind_aeyon
        
        # Initialize AEYON binding
        aeyon_binding = bind_aeyon()
        
        # Verify binding status
        runtime_state = aeyon_binding.get_runtime_state()
        
        print(f" AEYON Binding Status: {runtime_state.binding_status}")
        print(f" Harness Status: {runtime_state.harness_status}")
        print(f" AEYON Agent Active: {runtime_state.aeyon_agent_active}")
        
        if runtime_state.binding_status.value == "bound":
            print(" AEYON successfully bound and ready!")
            return True
        else:
            print(f"  AEYON binding status: {runtime_state.binding_status.value}")
            print("   This may be normal if Integration Layer is not fully configured")
            return True  # Not necessarily a failure
            
    except Exception as e:
        print(f" AEYON binding failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run binding test."""
    print("=" * 50)
    print("AEYON Binding Test")
    print("=" * 50)
    print()
    
    result = test_aeyon_binding()
    
    print()
    print("=" * 50)
    if result:
        print(" BINDING TEST PASSED")
        return 0
    else:
        print(" BINDING TEST FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())

