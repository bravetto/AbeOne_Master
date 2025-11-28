#!/usr/bin/env python3
"""
Dependency Analysis Script

Analyzes all requirements.txt files to identify:
- Common dependencies across projects
- Version conflicts
- Duplicate dependencies
- Missing version specifications

Pattern: ANALYSIS × DEPENDENCIES × UNIFICATION × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import json

# Project root
PROJECT_ROOT = Path(__file__).parent.parent


def parse_requirements_file(file_path: Path) -> List[Tuple[str, str]]:
    """
    Parse a requirements.txt file and extract package names and versions.
    
    Returns:
        List of (package_name, version_spec) tuples
    """
    dependencies = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse package specification
                # Format: package==version, package>=version, package~=version, etc.
                match = re.match(r'^([a-zA-Z0-9_-]+[a-zA-Z0-9_.-]*)\s*([=<>!~]+.*)?$', line)
                if match:
                    package_name = match.group(1).lower()
                    version_spec = match.group(2).strip() if match.group(2) else "unspecified"
                    dependencies.append((package_name, version_spec))
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return dependencies


def find_all_requirements_files(root: Path) -> List[Path]:
    """Find all requirements.txt files in the project."""
    requirements_files = []
    
    # Exclude certain directories
    exclude_dirs = {
        '.git', 'node_modules', '__pycache__', '.venv', 'venv',
        'env', '.env', 'dist', 'build', '.next', 'temp_repos',
        'repositories', 'BryanSatellite', 'AbeONESourceSatellite'
    }
    
    for file_path in root.rglob('requirements.txt'):
        # Skip excluded directories
        if any(excluded in file_path.parts for excluded in exclude_dirs):
            continue
        requirements_files.append(file_path)
    
    return requirements_files


def analyze_dependencies() -> Dict:
    """Analyze all dependencies and return analysis results."""
    print(" Analyzing dependencies...")
    
    requirements_files = find_all_requirements_files(PROJECT_ROOT)
    print(f"Found {len(requirements_files)} requirements.txt files")
    
    # Track dependencies across all files
    package_versions: Dict[str, Set[str]] = defaultdict(set)
    package_files: Dict[str, List[str]] = defaultdict(list)
    all_dependencies: List[Tuple[str, str, str]] = []  # (package, version, file)
    
    # Parse all requirements files
    for req_file in requirements_files:
        rel_path = req_file.relative_to(PROJECT_ROOT)
        dependencies = parse_requirements_file(req_file)
        
        for package, version in dependencies:
            package_versions[package].add(version)
            package_files[package].append(str(rel_path))
            all_dependencies.append((package, version, str(rel_path)))
    
    # Identify conflicts (packages with multiple different versions)
    conflicts = {}
    common_packages = {}
    
    for package, versions in package_versions.items():
        # Remove "unspecified" from version set for conflict detection
        specified_versions = {v for v in versions if v != "unspecified"}
        
        if len(specified_versions) > 1:
            conflicts[package] = {
                'versions': list(specified_versions),
                'files': package_files[package],
                'count': len(package_files[package])
            }
        
        # Common packages (used in 3+ files)
        if len(package_files[package]) >= 3:
            common_packages[package] = {
                'versions': list(versions),
                'files': package_files[package],
                'count': len(package_files[package])
            }
    
    # Generate report
    report = {
        'total_files': len(requirements_files),
        'total_packages': len(package_versions),
        'conflicts': conflicts,
        'common_packages': common_packages,
        'summary': {
            'conflict_count': len(conflicts),
            'common_package_count': len(common_packages),
            'files_with_conflicts': len(set(
                file for conflict in conflicts.values() for file in conflict['files']
            ))
        }
    }
    
    return report


def print_report(report: Dict):
    """Print analysis report."""
    print("\n" + "=" * 80)
    print(" DEPENDENCY ANALYSIS REPORT")
    print("=" * 80)
    
    print(f"\nTotal requirements.txt files: {report['total_files']}")
    print(f"Total unique packages: {report['total_packages']}")
    print(f"Version conflicts: {report['summary']['conflict_count']}")
    print(f"Common packages (3+ files): {report['summary']['common_package_count']}")
    
    # Print conflicts
    if report['conflicts']:
        print("\n" + "=" * 80)
        print("  VERSION CONFLICTS")
        print("=" * 80)
        
        # Sort by conflict count
        sorted_conflicts = sorted(
            report['conflicts'].items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        for package, info in sorted_conflicts[:20]:  # Top 20 conflicts
            print(f"\n {package}")
            print(f"   Versions: {', '.join(info['versions'])}")
            print(f"   Used in {info['count']} files")
            print(f"   Example files: {', '.join(info['files'][:3])}")
    
    # Print common packages
    if report['common_packages']:
        print("\n" + "=" * 80)
        print(" COMMON PACKAGES (3+ files)")
        print("=" * 80)
        
        # Sort by usage count
        sorted_common = sorted(
            report['common_packages'].items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        for package, info in sorted_common[:30]:  # Top 30 common packages
            versions_str = ', '.join(info['versions'][:3])
            if len(info['versions']) > 3:
                versions_str += f" (+{len(info['versions']) - 3} more)"
            print(f"{package:30} | {versions_str:40} | {info['count']:3} files")


def main():
    """Main entry point."""
    print(" Starting Dependency Analysis")
    print("=" * 80)
    
    # Analyze dependencies
    report = analyze_dependencies()
    
    # Print report
    print_report(report)
    
    # Save report to JSON
    report_file = PROJECT_ROOT / 'dependencies' / 'dependency-analysis-report.json'
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n Report saved to: {report_file}")
    
    return report


if __name__ == "__main__":
    main()

