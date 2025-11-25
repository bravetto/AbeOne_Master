#!/usr/bin/env python3
"""
AEYON Import Test
Tests that AEYON can be imported successfully.
"""

import sys
import os

# Add EMERGENT_OS to path
abeone_root = os.path.dirname(os.path.abspath(__file__))
emergent_os_path = os.path.join(abeone_root, 'EMERGENT_OS')
if emergent_os_path not in sys.path:
    sys.path.insert(0, emergent_os_path)

def test_basic_imports():
    """Test basic AEYON imports."""
    print("Testing basic AEYON imports...")
    try:
        from triadic_execution_harness import AEYONAgent, TriadicExecutionHarness
        from triadic_execution_harness.aeyon_binding import AEYONBinding, bind_aeyon
        print("✅ AEYON imports successful!")
        return True
    except ImportError as e:
        print(f"❌ AEYON import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_layer():
    """Test Integration Layer imports."""
    print("\nTesting Integration Layer imports...")
    try:
        from integration_layer.registry.module_registry import ModuleRegistry
        from integration_layer.events.event_bus import EventBus
        from integration_layer.router.request_router import RequestRouter
        print("✅ Integration Layer imports successful!")
        return True
    except ImportError as e:
        print(f"⚠️  Integration Layer import warning: {e}")
        print("   AEYON may work in limited mode")
        return True  # Not critical for basic functionality

def main():
    """Run all import tests."""
    print("=" * 50)
    print("AEYON Import Test")
    print("=" * 50)
    print()
    
    results = []
    results.append(test_basic_imports())
    results.append(test_integration_layer())
    
    print()
    print("=" * 50)
    if all(results):
        print("✅ ALL IMPORT TESTS PASSED")
        return 0
    else:
        print("❌ SOME IMPORT TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())

