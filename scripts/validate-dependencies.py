#!/usr/bin/env python3
"""
Dependency Validation Script

Validates that all requirements.txt files comply with shared dependency manifest.
Checks for version conflicts and missing dependencies.

Pattern: VALIDATION × DEPENDENCIES × COMPLIANCE × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import json

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
SHARED_REQUIREMENTS = PROJECT_ROOT / 'dependencies' / 'shared-requirements.txt'


def parse_version_spec(version_spec: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Parse version specification into (min_version, max_version, exact_version).
    
    Examples:
        ">=2.12.0" -> (2.12.0, None, None)
        "==2.5.0" -> (None, None, 2.5.0)
        ">=2.0.0,<3.0.0" -> (2.0.0, 3.0.0, None)
    """
    min_version = None
    max_version = None
    exact_version = None
    
    # Remove comments
    version_spec = version_spec.split('#')[0].strip()
    
    if not version_spec or version_spec == "unspecified":
        return (None, None, None)
    
    # Parse comma-separated constraints
    constraints = [c.strip() for c in version_spec.split(',')]
    
    for constraint in constraints:
        if constraint.startswith('>='):
            min_version = constraint[2:].strip()
        elif constraint.startswith('<='):
            max_version = constraint[2:].strip()
        elif constraint.startswith('>'):
            # >x.y.z means >=x.y.z+1 (approximate)
            min_version = constraint[1:].strip()
        elif constraint.startswith('<'):
            # <x.y.z means <=x.y.z-1 (approximate)
            max_version = constraint[1:].strip()
        elif constraint.startswith('=='):
            exact_version = constraint[2:].strip()
        elif constraint.startswith('~='):
            # Compatible release: ~=2.2.0 means >=2.2.0,<3.0.0
            base_version = constraint[2:].strip()
            parts = base_version.split('.')
            if len(parts) >= 2:
                min_version = base_version
                max_version = f"{int(parts[0]) + 1}.0.0"
    
    return (min_version, max_version, exact_version)


def parse_requirements_file(file_path: Path) -> Dict[str, str]:
    """Parse requirements.txt and return {package: version_spec} dict."""
    dependencies = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse package specification
                match = re.match(r'^([a-zA-Z0-9_-]+[a-zA-Z0-9_.-]*)\s*([=<>!~]+.*)?$', line)
                if match:
                    package_name = match.group(1).lower()
                    version_spec = match.group(2).strip() if match.group(2) else "unspecified"
                    dependencies[package_name] = version_spec
    except Exception as e:
        print(f"  Error parsing {file_path}: {e}", file=sys.stderr)
    
    return dependencies


def load_shared_requirements() -> Dict[str, str]:
    """Load shared requirements manifest."""
    if not SHARED_REQUIREMENTS.exists():
        print(f"  Shared requirements not found: {SHARED_REQUIREMENTS}")
        return {}
    
    return parse_requirements_file(SHARED_REQUIREMENTS)


def check_version_compatibility(shared_spec: str, file_spec: str) -> Tuple[bool, str]:
    """
    Check if file version spec is compatible with shared spec.
    
    Returns:
        (is_compatible, reason)
    """
    if file_spec == "unspecified" or not file_spec:
        return (True, "No version specified")
    
    shared_min, shared_max, shared_exact = parse_version_spec(shared_spec)
    file_min, file_max, file_exact = parse_version_spec(file_spec)
    
    # If shared has exact version, file must match or be compatible
    if shared_exact:
        if file_exact:
            if file_exact == shared_exact:
                return (True, "Exact match")
            else:
                return (False, f"Exact version mismatch: {file_exact} != {shared_exact}")
        elif file_min:
            # Check if file_min is >= shared_exact
            if compare_versions(file_min, shared_exact) >= 0:
                return (True, f"File min {file_min} >= shared exact {shared_exact}")
            else:
                return (False, f"File min {file_min} < shared exact {shared_exact}")
    
    # If file has exact version, check compatibility
    if file_exact:
        if shared_min and compare_versions(file_exact, shared_min) < 0:
            return (False, f"File exact {file_exact} < shared min {shared_min}")
        if shared_max and compare_versions(file_exact, shared_max) >= 0:
            return (False, f"File exact {file_exact} >= shared max {shared_max}")
        return (True, f"File exact {file_exact} within shared range")
    
    # Check min/max compatibility
    if file_min and shared_max:
        if compare_versions(file_min, shared_max) >= 0:
            return (False, f"File min {file_min} >= shared max {shared_max}")
    
    if file_max and shared_min:
        if compare_versions(file_max, shared_min) < 0:
            return (False, f"File max {file_max} < shared min {shared_min}")
    
    return (True, "Compatible")


def compare_versions(v1: str, v2: str) -> int:
    """
    Compare two version strings.
    
    Returns:
        -1 if v1 < v2
        0 if v1 == v2
        1 if v1 > v2
    """
    def normalize_version(v: str) -> List[int]:
        # Remove any non-numeric suffixes
        parts = re.split(r'[^0-9]', v.split('+')[0])
        return [int(p) if p.isdigit() else 0 for p in parts if p]
    
    v1_parts = normalize_version(v1)
    v2_parts = normalize_version(v2)
    
    # Pad with zeros
    max_len = max(len(v1_parts), len(v2_parts))
    v1_parts.extend([0] * (max_len - len(v1_parts)))
    v2_parts.extend([0] * (max_len - len(v2_parts)))
    
    for p1, p2 in zip(v1_parts, v2_parts):
        if p1 < p2:
            return -1
        elif p1 > p2:
            return 1
    
    return 0


def find_all_requirements_files(root: Path) -> List[Path]:
    """Find all requirements.txt files."""
    exclude_dirs = {
        '.git', 'node_modules', '__pycache__', '.venv', 'venv',
        'env', '.env', 'dist', 'build', '.next', 'temp_repos',
        'repositories', 'BryanSatellite', 'AbeONESourceSatellite',
        '_ARCHIVE', 'dependencies'
    }
    
    requirements_files = []
    for file_path in root.rglob('requirements.txt'):
        if any(excluded in file_path.parts for excluded in exclude_dirs):
            continue
        requirements_files.append(file_path)
    
    return requirements_files


def validate_dependencies() -> Dict:
    """Validate all dependencies against shared manifest."""
    print(" Validating dependencies...")
    
    shared_deps = load_shared_requirements()
    requirements_files = find_all_requirements_files(PROJECT_ROOT)
    
    conflicts = []
    warnings = []
    stats = {
        'total_files': len(requirements_files),
        'files_with_conflicts': 0,
        'total_conflicts': 0,
        'total_warnings': 0
    }
    
    for req_file in requirements_files:
        rel_path = req_file.relative_to(PROJECT_ROOT)
        file_deps = parse_requirements_file(req_file)
        
        file_conflicts = []
        file_warnings = []
        
        for package, file_spec in file_deps.items():
            if package in shared_deps:
                shared_spec = shared_deps[package]
                is_compatible, reason = check_version_compatibility(shared_spec, file_spec)
                
                if not is_compatible:
                    file_conflicts.append({
                        'package': package,
                        'shared_spec': shared_spec,
                        'file_spec': file_spec,
                        'reason': reason
                    })
                elif file_spec != shared_spec and file_spec != "unspecified":
                    file_warnings.append({
                        'package': package,
                        'shared_spec': shared_spec,
                        'file_spec': file_spec,
                        'reason': reason
                    })
        
        if file_conflicts:
            conflicts.append({
                'file': str(rel_path),
                'conflicts': file_conflicts
            })
            stats['files_with_conflicts'] += 1
            stats['total_conflicts'] += len(file_conflicts)
        
        if file_warnings:
            warnings.append({
                'file': str(rel_path),
                'warnings': file_warnings
            })
            stats['total_warnings'] += len(file_warnings)
    
    return {
        'stats': stats,
        'conflicts': conflicts,
        'warnings': warnings,
        'shared_packages': len(shared_deps)
    }


def print_report(report: Dict):
    """Print validation report."""
    print("\n" + "=" * 80)
    print(" DEPENDENCY VALIDATION REPORT")
    print("=" * 80)
    
    stats = report['stats']
    print(f"\nTotal requirements.txt files: {stats['total_files']}")
    print(f"Shared packages in manifest: {report['shared_packages']}")
    print(f"Files with conflicts: {stats['files_with_conflicts']}")
    print(f"Total conflicts: {stats['total_conflicts']}")
    print(f"Total warnings: {stats['total_warnings']}")
    
    if report['conflicts']:
        print("\n" + "=" * 80)
        print(" VERSION CONFLICTS")
        print("=" * 80)
        
        for conflict_group in report['conflicts'][:10]:  # Top 10
            print(f"\n {conflict_group['file']}")
            for conflict in conflict_group['conflicts']:
                print(f"    {conflict['package']}")
                print(f"      Shared: {conflict['shared_spec']}")
                print(f"      File:   {conflict['file_spec']}")
                print(f"      Reason: {conflict['reason']}")
    
    if report['warnings']:
        print("\n" + "=" * 80)
        print("  WARNINGS (Non-conflicting but different versions)")
        print("=" * 80)
        
        for warning_group in report['warnings'][:5]:  # Top 5
            print(f"\n {warning_group['file']}")
            for warning in warning_group['warnings'][:3]:  # Top 3 per file
                print(f"     {warning['package']}: {warning['file_spec']} (shared: {warning['shared_spec']})")
    
    # Summary
    print("\n" + "=" * 80)
    if stats['total_conflicts'] == 0:
        print(" NO CONFLICTS FOUND - All dependencies are compatible!")
    else:
        print(f"  {stats['total_conflicts']} conflicts found - Review and update requirements.txt files")
    print("=" * 80)


def main():
    """Main entry point."""
    print(" Starting Dependency Validation")
    print("=" * 80)
    
    if not SHARED_REQUIREMENTS.exists():
        print(f" Shared requirements file not found: {SHARED_REQUIREMENTS}")
        print("   Create it first: dependencies/shared-requirements.txt")
        sys.exit(1)
    
    report = validate_dependencies()
    print_report(report)
    
    # Save report
    report_file = PROJECT_ROOT / 'dependencies' / 'validation-report.json'
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n Report saved to: {report_file}")
    
    # Exit with error code if conflicts found
    if report['stats']['total_conflicts'] > 0:
        sys.exit(1)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

