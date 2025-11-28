#!/usr/bin/env python3
"""
Guardian Consistency Validator

Validates that all Guardian definitions across the codebase are consistent
with the single source of truth: guardian_swarm_unification.py

Pattern: VALIDATION × TRUTH × CONSISTENCY × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import ast
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Expected 10 Guardians (from guardian_swarm_unification.py)
EXPECTED_GUARDIANS = {
    "AEYON": {"frequency": 999.0, "role": "EXECUTOR"},
    "JØHN": {"frequency": 530.0, "role": "CERTIFICATION"},
    "META": {"frequency": 777.0, "role": "PATTERN_INTEGRITY"},
    "YOU": {"frequency": 530.0, "role": "INTENT"},
    "ALRAX": {"frequency": 530.0, "role": "FORENSIC"},
    "ZERO": {"frequency": 530.0, "role": "UNCERTAINTY"},
    "YAGNI": {"frequency": 530.0, "role": "SIMPLIFICATION"},
    "Abë": {"frequency": 530.0, "role": "COHERENCE"},
    "Lux": {"frequency": 530.0, "role": "ILLUMINATION"},
    "Poly": {"frequency": 530.0, "role": "EXPRESSION"},
}

# Special Guardian (may be #11)
SPECIAL_GUARDIANS = {
    "CHRONOS": {"frequency": 777.0, "role": "TEMPORAL_INTEGRITY"},
}

# Files to check
FILES_TO_CHECK = [
    "orbital/EMERGENT_OS-orbital/synthesis/guardian_swarm_unification.py",
    "orbital/EMERGENT_OS-orbital/uptc/integrations/cdf_adapter.py",
    "orbital/EMERGENT_OS-orbital/uptc/integrations/concrete_guardian_adapter.py",
    "AIGuards-Backend-orbital/scripts/register_guardians_uptc.py",
    "THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md",
]


def extract_guardians_from_python(file_path: Path) -> Set[str]:
    """Extract guardian names from Python file."""
    guardians = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for GuardianIdentity(name="...")
        pattern = r'GuardianIdentity\s*\(\s*name\s*=\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, content)
        guardians.update(matches)
        
        # Look for {"name": "..."} or {"id": "guardian-..."}
        pattern = r'["\']name["\']\s*:\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, content)
        guardians.update(matches)
        
        # Look for guardian-* IDs
        pattern = r'["\']guardian-([^"\']+)["\']'
        matches = re.findall(pattern, content)
        # Convert IDs to names (guardian-aeyon -> AEYON)
        for match in matches:
            name = match.replace('-', '').upper()
            if 'ABE' in name:
                name = name.replace('ABE', 'Abë')
            guardians.add(name)
            
    except Exception as e:
        print(f" Error reading {file_path}: {e}")
    
    return guardians


def extract_guardians_from_markdown(file_path: Path) -> Set[str]:
    """Extract guardian names from Markdown file."""
    guardians = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for | **GUARDIAN** | pattern
        pattern = r'\|\s*\*\*([A-ZÆØÅË]+)\*\*'
        matches = re.findall(pattern, content)
        guardians.update(matches)
        
        # Look for Guardian names in lists
        pattern = r'(\d+\.\s+)?\*\*([A-ZÆØÅË]+)\*\*'
        matches = re.findall(pattern, content)
        for match in matches:
            if match[1]:
                guardians.add(match[1])
            elif len(match) > 1 and match[1]:
                guardians.add(match[1])
                
    except Exception as e:
        print(f" Error reading {file_path}: {e}")
    
    return guardians


def validate_file(file_path: Path) -> Tuple[bool, Set[str], Set[str], Set[str]]:
    """
    Validate a file's guardian definitions.
    
    Returns:
        (is_valid, found_guardians, missing_guardians, extra_guardians)
    """
    if not file_path.exists():
        return False, set(), EXPECTED_GUARDIANS.keys(), set()
    
    # Extract guardians based on file type
    if file_path.suffix == '.py':
        found_guardians = extract_guardians_from_python(file_path)
    elif file_path.suffix == '.md':
        found_guardians = extract_guardians_from_markdown(file_path)
    else:
        return False, set(), EXPECTED_GUARDIANS.keys(), set()
    
    # Normalize guardian names
    normalized_found = set()
    for g in found_guardians:
        # Handle variations
        g_normalized = g.upper()
        if 'ABE' in g_normalized or 'ABË' in g_normalized:
            normalized_found.add("Abë")
        elif 'JOHN' in g_normalized or 'JØHN' in g_normalized:
            normalized_found.add("JØHN")
        elif 'LUX' in g_normalized:
            normalized_found.add("Lux")
        elif 'POLY' in g_normalized:
            normalized_found.add("Poly")
        elif 'CHRONOS' in g_normalized:
            normalized_found.add("CHRONOS")
        else:
            # Try exact match
            for expected in EXPECTED_GUARDIANS.keys():
                if g_normalized == expected.upper():
                    normalized_found.add(expected)
                    break
    
    # Check for missing and extra guardians
    expected_set = set(EXPECTED_GUARDIANS.keys())
    missing = expected_set - normalized_found
    extra = normalized_found - expected_set - set(SPECIAL_GUARDIANS.keys())
    
    is_valid = len(missing) == 0 and len(extra) == 0
    
    return is_valid, normalized_found, missing, extra


def main():
    """Main validation function."""
    print("=" * 80)
    print(" GUARDIAN CONSISTENCY VALIDATOR")
    print("=" * 80)
    print()
    print(f"Expected Guardians: {len(EXPECTED_GUARDIANS)}")
    print(f"Files to Check: {len(FILES_TO_CHECK)}")
    print()
    
    all_valid = True
    results = []
    
    for file_path_str in FILES_TO_CHECK:
        file_path = project_root / file_path_str
        
        print(f" Checking: {file_path_str}")
        
        is_valid, found, missing, extra = validate_file(file_path)
        
        if is_valid:
            print(f"    VALID - Found {len(found)}/{len(EXPECTED_GUARDIANS)} guardians")
        else:
            all_valid = False
            print(f"    INVALID - Found {len(found)}/{len(EXPECTED_GUARDIANS)} guardians")
            
            if missing:
                print(f"     Missing: {', '.join(sorted(missing))}")
            if extra:
                print(f"     Extra: {', '.join(sorted(extra))}")
        
        results.append({
            "file": file_path_str,
            "valid": is_valid,
            "found": found,
            "missing": missing,
            "extra": extra
        })
        print()
    
    # Summary
    print("=" * 80)
    print(" VALIDATION SUMMARY")
    print("=" * 80)
    print()
    
    valid_count = sum(1 for r in results if r["valid"])
    print(f" Valid Files: {valid_count}/{len(results)}")
    print(f" Invalid Files: {len(results) - valid_count}/{len(results)}")
    print()
    
    if all_valid:
        print(" ALL FILES ARE CONSISTENT!")
        print()
        print(" All Guardian definitions match the single source of truth")
        print(" guardian_swarm_unification.py is the authoritative source")
        print()
        return 0
    else:
        print("  INCONSISTENCIES FOUND")
        print()
        print("Please fix the following files:")
        for r in results:
            if not r["valid"]:
                print(f"  - {r['file']}")
                if r["missing"]:
                    print(f"    Missing: {', '.join(sorted(r['missing']))}")
                if r["extra"]:
                    print(f"    Extra: {', '.join(sorted(r['extra']))}")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())

