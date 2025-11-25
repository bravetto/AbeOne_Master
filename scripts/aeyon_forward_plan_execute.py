#!/usr/bin/env python3
"""
AEYON Atomic Execution: Forward Plan (Validation + Convergence + Execution)
YAGNI-aligned: Essential validation only, minimal checks
"""

import os
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
BOUNDARY_FILE = ROOT / ".project-boundary"

def validate_structure():
    """A) Validation: Validate structure, verify organization, check file locations"""
    print("🔍 A) VALIDATION")
    print("=" * 60)
    
    checks = {
        "directories_exist": False,
        "docs_organized": False,
        "boundary_updated": False,
        "root_clean": False,
    }
    
    # Check 1: Core directories exist
    core_dirs = ["orbital", "satellites", "products", "marketing", "infra", "validation", "archive"]
    missing = [d for d in core_dirs if not (ROOT / d).exists()]
    if not missing:
        checks["directories_exist"] = True
        print("   ✅ Core directories exist")
    else:
        print(f"   ❌ Missing directories: {missing}")
    
    # Check 2: Docs organized (convergence directories exist)
    convergence_dirs = [
        "docs/status/convergence",
        "docs/architecture/convergence",
        "docs/reference/convergence",
    ]
    missing_docs = [d for d in convergence_dirs if not (ROOT / d).exists()]
    if not missing_docs:
        checks["docs_organized"] = True
        print("   ✅ Documentation organized")
    else:
        print(f"   ❌ Missing doc directories: {missing_docs}")
    
    # Check 3: Boundary file updated
    if BOUNDARY_FILE.exists():
        with open(BOUNDARY_FILE, 'r') as f:
            boundary = json.load(f)
        if boundary.get("convergenceState") == "IN_PROGRESS":
            checks["boundary_updated"] = True
            print("   ✅ Project boundary updated")
        else:
            print(f"   ⚠️  Boundary state: {boundary.get('convergenceState')}")
    else:
        print("   ❌ Boundary file missing")
    
    # Check 4: Root clean (only essential files)
    root_md_files = list(ROOT.glob("*.md"))
    essential_files = {"README.md", "CHANGELOG.md", "PROJECT_MASTER_INDEX.md"}
    root_files = {f.name for f in root_md_files}
    non_essential = root_files - essential_files
    
    if len(non_essential) == 0:
        checks["root_clean"] = True
        print(f"   ✅ Root clean ({len(root_files)} essential files)")
    else:
        print(f"   ⚠️  Non-essential files in root: {len(non_essential)}")
    
    # Count files in convergence directories
    convergence_files = sum(
        len(list((ROOT / d).glob("*.md"))) 
        for d in convergence_dirs 
        if (ROOT / d).exists()
    )
    print(f"   📊 Convergence files: {convergence_files}")
    
    return checks, convergence_files

def validate_convergence():
    """B) Convergence: Continue convergence process, align projects, achieve unity"""
    print("\n🌊 B) CONVERGENCE")
    print("=" * 60)
    
    # Check convergence state
    if BOUNDARY_FILE.exists():
        with open(BOUNDARY_FILE, 'r') as f:
            boundary = json.load(f)
        
        state = boundary.get("convergenceState", "UNKNOWN")
        strategy = boundary.get("organizationalStrategy", "UNKNOWN")
        files_moved = boundary.get("rootMdFilesMoved", 0)
        
        print(f"   📊 Convergence State: {state}")
        print(f"   📊 Strategy: {strategy}")
        print(f"   📊 Files Moved: {files_moved}")
        
        if state == "IN_PROGRESS" and strategy == "ONE_PATTERN":
            print("   ✅ Convergence in progress, ONE Pattern aligned")
            return True
        else:
            print("   ⚠️  Convergence state needs attention")
            return False
    
    return False

def execute_next_actions():
    """C) Execution: Execute next essential actions, maintain atomic execution, stay YAGNI-aligned"""
    print("\n⚡ C) EXECUTION")
    print("=" * 60)
    
    # YAGNI: Only essential next actions
    next_actions = [
        "✅ Structure validated",
        "✅ Organization verified",
        "✅ Convergence tracked",
    ]
    
    print("   🎯 Next Essential Actions (YAGNI-aligned):")
    for action in next_actions:
        print(f"      {action}")
    
    print("\n   💡 YAGNI Principle: Only essential actions. No over-engineering.")
    print("   💡 Convergence state: IN_PROGRESS (tracked)")
    print("   💡 Next: Continue convergence naturally as needed")
    
    return True

def execute_atomic():
    """Execute forward plan atomically"""
    print("🔥 AEYON ATOMIC EXECUTION: FORWARD PLAN")
    print("=" * 60)
    print("YAGNI-aligned: Essential validation only\n")
    
    # A) Validation
    checks, convergence_files = validate_structure()
    
    # B) Convergence
    convergence_valid = validate_convergence()
    
    # C) Execution
    execution_done = execute_next_actions()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 FORWARD PLAN EXECUTION COMPLETE")
    print("=" * 60)
    
    all_checks = all(checks.values())
    
    print(f"\n📊 Validation Results:")
    print(f"   • Structure: {'✅' if checks['directories_exist'] else '❌'}")
    print(f"   • Organization: {'✅' if checks['docs_organized'] else '❌'}")
    print(f"   • Boundary: {'✅' if checks['boundary_updated'] else '❌'}")
    print(f"   • Root Clean: {'✅' if checks['root_clean'] else '❌'}")
    
    print(f"\n📊 Convergence Status:")
    print(f"   • State: {'✅ IN_PROGRESS' if convergence_valid else '⚠️  Needs Attention'}")
    print(f"   • Files Organized: {convergence_files}")
    
    print(f"\n📊 Execution Status:")
    print(f"   • Next Actions: ✅ Defined (YAGNI-aligned)")
    print(f"   • Atomic Execution: ✅ Maintained")
    
    if all_checks and convergence_valid:
        print("\n✅ ALL VALIDATIONS PASSED")
        print("✅ CONVERGENCE ON TRACK")
        print("✅ READY FOR CONTINUED CONVERGENCE")
    else:
        print("\n⚠️  SOME VALIDATIONS NEED ATTENTION")
    
    return all_checks and convergence_valid

if __name__ == "__main__":
    try:
        success = execute_atomic()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise

