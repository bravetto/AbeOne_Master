#!/usr/bin/env python3
"""
Verify All Infrastructure - Master Verification Script

Runs all infrastructure verification scripts.

Pattern: VERIFY × ALL × INFRASTRUCTURE × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN)
Guardians: AEYON (999 Hz) + JØHN (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, List

def run_verification(script_name: str) -> Dict[str, Any]:
    """Run a verification script"""
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        return {
            "success": False,
            "message": f"Script not found: {script_name}",
            "script": script_name
        }
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "success": result.returncode == 0,
            "message": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "script": script_name
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error running script: {e}",
            "script": script_name
        }


def main():
    """Main execution"""
    print("\n⚡ VERIFY ALL INFRASTRUCTURE")
    print("=" * 70)
    print("\nRunning all infrastructure verification scripts...\n")
    
    verification_scripts = [
        "verify_database_connection.py",
        "verify_job_queue.py",
        "verify_rate_limiting.py",
        "verify_realtime_features.py"
    ]
    
    results = []
    for script in verification_scripts:
        print(f"Running {script}...")
        result = run_verification(script)
        results.append(result)
        
        if result["success"]:
            print(f"✅ {script}: PASSED\n")
        else:
            print(f"❌ {script}: FAILED")
            if result.get("error"):
                print(f"   Error: {result['error']}\n")
    
    # Summary
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL INFRASTRUCTURE VERIFIED!")
        print("\nNext steps:")
        print("1. cd products/apps/web && npx prisma migrate dev")
        print("2. cd products/apps/web && npm run webinar:worker")
        print("3. cd products/apps/web && npm run dev")
    else:
        print("\n⚠️  SOME VERIFICATIONS FAILED")
        print("\nPlease fix the issues above before proceeding.")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("Pattern: VERIFY × ALL × INFRASTRUCTURE × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞\n")


if __name__ == "__main__":
    main()

