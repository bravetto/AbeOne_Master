#!/usr/bin/env python3
"""
Simple test runner for CodeGuardians Gateway tests.

This script runs the test suite with proper Python path configuration.
"""

import sys
import os
import subprocess

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def run_tests():
    """Run the test suite."""
    print("Running CodeGuardians Gateway Test Suite")
    print("=" * 50)
    
    # Set environment variables
    env = os.environ.copy()
    env['PYTHONPATH'] = current_dir
    
    # Test categories to run
    test_categories = [
        ("smoke", "Smoke Tests (Quick Validation)"),
        ("unit", "Unit Tests (Component Testing)"),
        ("integration", "Integration Tests (Full Service Testing)"),
        ("edge_case", "Edge Case Tests (Error Handling)"),
        ("guard_metrics", "Guard Metrics Tests (Metrics Validation)")
    ]
    
    total_passed = 0
    total_failed = 0
    
    for marker, description in test_categories:
        print(f"\n{description}")
        print("-" * 40)
        
        try:
            # Run tests with specific marker
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                f"-m", marker, 
                "-v", 
                "--tb=short",
                "--no-header"
            ], 
            cwd=current_dir,
            env=env,
            capture_output=True,
            text=True
            )
            
            if result.returncode == 0:
                print(f"PASSED: {marker} tests")
                # Count passed tests
                passed_count = result.stdout.count("PASSED")
                total_passed += passed_count
                print(f"   {passed_count} tests passed")
            else:
                print(f"FAILED: {marker} tests")
                # Count failed tests
                failed_count = result.stdout.count("FAILED")
                total_failed += failed_count
                print(f"   {failed_count} tests failed")
                if result.stdout:
                    print("   Output:", result.stdout[-500:])  # Last 500 chars
                if result.stderr:
                    print("   Errors:", result.stderr[-500:])  # Last 500 chars
                    
        except Exception as e:
            print(f"ERROR: Error running {marker} tests: {e}")
            total_failed += 1
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print(f"Total Passed: {total_passed}")
    print(f"Total Failed: {total_failed}")
    print(f"Success Rate: {(total_passed / (total_passed + total_failed) * 100):.1f}%" if (total_passed + total_failed) > 0 else "No tests run")
    
    return total_failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
