from typing import Any
#!/usr/bin/env python3
"""
Test Runner for TokenGuard Microservice

Convenient script to run different types of tests.
"""

import sys
import subprocess
import argparse
import os

def run_command(cmd: Any, description) -> Any:
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
        print(f" {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f" {description} - FAILED (exit code: {e.returncode})")
        return False

def main() -> Any:
    parser = argparse.ArgumentParser(description="TokenGuard Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--errors", action="store_true", help="Run error scenario tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--validation", action="store_true", help="Run production validation")
    parser.add_argument("--generate", action="store_true", help="Run generate endpoint tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--coverage", action="store_true", help="Include coverage reporting")
    
    args = parser.parse_args()
    
    # Default to running all tests if no specific option selected
    if not any([args.unit, args.integration, args.errors, args.performance, args.validation, args.generate]):
        args.all = True
    
    print(" TokenGuard Test Runner")
    print("=" * 40)
    
    results = []
    base_cmd = "python -m pytest"
    
    if args.unit or args.all:
        if args.coverage:
            cmd = f"{base_cmd} tests/test_tokenguard.py --cov=tokenguard --cov-report=term-missing"
        else:
            cmd = f"{base_cmd} tests/test_tokenguard.py"
        results.append(run_command(cmd, "Unit Tests"))
    
    if args.integration or args.all:
        cmd = f"{base_cmd} tests/test_service.py"
        results.append(run_command(cmd, "Integration Tests"))
    
    if args.errors or args.all:
        cmd = f"{base_cmd} tests/test_error_scenarios.py"
        results.append(run_command(cmd, "Error Scenario Tests"))
    
    if args.performance or args.all:
        # benchmark.py is a script, not a pytest suite
        cmd = "python tests/benchmark.py"
        results.append(run_command(cmd, "Performance Benchmarks"))
    
    if args.validation or args.all:
        # validation_final.py is a script, not a pytest suite
        cmd = "python tests/validation_final.py"
        results.append(run_command(cmd, "Production Validation"))
    
    if args.generate or args.all:
        cmd = f"{base_cmd} tests/test_generate.py"
        results.append(run_command(cmd, "Generate Endpoint Tests"))

    # Summary
    print(f"\n{'='*60}")
    print("TEST RESULTS SUMMARY")
    print('='*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print(" All tests passed!")
        sys.exit(0)
    else:
        print(" Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()