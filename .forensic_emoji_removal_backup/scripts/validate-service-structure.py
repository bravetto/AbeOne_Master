#!/usr/bin/env python3
"""
Service Structure Validation Script

Validates that services follow the standard structure specification.

Pattern: VALIDATION × STRUCTURE × COMPLIANCE × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import sys
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json

# Project root
PROJECT_ROOT = Path(__file__).parent.parent


# Required files and directories
REQUIRED_FILES = {
    'main.py': True,
    'requirements.txt': True,
    'Dockerfile': True,
    'README.md': True,
    'core/config.py': True,
    'core/logging.py': True,
    'core/metrics.py': True,
    'core/security.py': True,
    'core/exceptions.py': True,
    'api/v1/router.py': True,
    'api/v1/endpoints/health.py': True,
    'models/requests.py': True,
    'models/responses.py': True,
    'services/': False,  # Directory, not file
    'tests/conftest.py': True,
}

# Required patterns in main.py
REQUIRED_PATTERNS = {
    'create_app': 'create_app() function',
    'lifespan': 'lifespan() context manager',
    'FastAPI': 'FastAPI import',
}


def check_file_exists(service_path: Path, file_path: str, is_file: bool = True) -> bool:
    """Check if a file or directory exists."""
    full_path = service_path / file_path
    if is_file:
        return full_path.is_file()
    else:
        return full_path.is_dir()


def check_pattern_in_file(service_path: Path, file_path: str, patterns: Dict[str, str]) -> Dict[str, bool]:
    """Check if patterns exist in a file."""
    file_full_path = service_path / file_path
    
    if not file_full_path.exists():
        return {pattern: False for pattern in patterns}
    
    try:
        with open(file_full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {}
        for pattern, description in patterns.items():
            # Check for function definitions
            if pattern == 'create_app':
                results[pattern] = 'def create_app' in content or 'async def create_app' in content
            elif pattern == 'lifespan':
                results[pattern] = 'def lifespan' in content or 'async def lifespan' in content or '@asynccontextmanager' in content
            elif pattern == 'FastAPI':
                results[pattern] = 'FastAPI' in content or 'from fastapi import' in content
            else:
                results[pattern] = pattern in content
        
        return results
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}", file=sys.stderr)
        return {pattern: False for pattern in patterns}


def validate_service(service_path: Path) -> Dict:
    """Validate a single service structure."""
    service_name = service_path.name
    
    validation_results = {
        'service': service_name,
        'path': str(service_path.relative_to(PROJECT_ROOT)),
        'files': {},
        'patterns': {},
        'compliance': {
            'files_passed': 0,
            'files_total': 0,
            'patterns_passed': 0,
            'patterns_total': 0,
            'is_compliant': False
        }
    }
    
    # Check required files
    for file_path, is_file in REQUIRED_FILES.items():
        exists = check_file_exists(service_path, file_path, is_file)
        validation_results['files'][file_path] = exists
        validation_results['compliance']['files_total'] += 1
        if exists:
            validation_results['compliance']['files_passed'] += 1
    
    # Check patterns in main.py
    if (service_path / 'main.py').exists():
        patterns = check_pattern_in_file(service_path, 'main.py', REQUIRED_PATTERNS)
        validation_results['patterns'] = patterns
        validation_results['compliance']['patterns_total'] = len(patterns)
        validation_results['compliance']['patterns_passed'] = sum(patterns.values())
    
    # Calculate compliance
    files_compliant = validation_results['compliance']['files_passed'] == validation_results['compliance']['files_total']
    patterns_compliant = validation_results['compliance']['patterns_passed'] == validation_results['compliance']['patterns_total']
    validation_results['compliance']['is_compliant'] = files_compliant and patterns_compliant
    
    return validation_results


def find_services(root: Path) -> List[Path]:
    """Find all service directories."""
    services = []
    
    # Exclude certain directories
    exclude_dirs = {
        '.git', 'node_modules', '__pycache__', '.venv', 'venv',
        'env', '.env', 'dist', 'build', '.next', 'temp_repos',
        'repositories', 'BryanSatellite', 'AbeONESourceSatellite',
        '_ARCHIVE', 'dependencies', 'scripts', 'docs'
    }
    
    # Look for services with main.py
    for main_file in root.rglob('main.py'):
        # Skip if in excluded directory
        if any(excluded in main_file.parts for excluded in exclude_dirs):
            continue
        
        # Check if it's a FastAPI service (has FastAPI import or create_app)
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'FastAPI' in content or 'create_app' in content:
                    services.append(main_file.parent)
        except Exception:
            pass
    
    return services


def print_report(results: List[Dict]):
    """Print validation report."""
    print("\n" + "=" * 80)
    print("📊 SERVICE STRUCTURE VALIDATION REPORT")
    print("=" * 80)
    
    total_services = len(results)
    compliant_services = sum(1 for r in results if r['compliance']['is_compliant'])
    
    print(f"\nTotal services: {total_services}")
    print(f"Compliant services: {compliant_services}")
    print(f"Non-compliant services: {total_services - compliant_services}")
    
    # Print compliant services
    compliant = [r for r in results if r['compliance']['is_compliant']]
    if compliant:
        print("\n" + "=" * 80)
        print("✅ COMPLIANT SERVICES")
        print("=" * 80)
        for result in compliant:
            print(f"  ✅ {result['service']}")
    
    # Print non-compliant services
    non_compliant = [r for r in results if not r['compliance']['is_compliant']]
    if non_compliant:
        print("\n" + "=" * 80)
        print("❌ NON-COMPLIANT SERVICES")
        print("=" * 80)
        
        for result in non_compliant[:10]:  # Top 10
            print(f"\n📦 {result['service']}")
            print(f"   Path: {result['path']}")
            
            # Missing files
            missing_files = [f for f, exists in result['files'].items() if not exists]
            if missing_files:
                print(f"   Missing files: {', '.join(missing_files[:5])}")
                if len(missing_files) > 5:
                    print(f"   ... and {len(missing_files) - 5} more")
            
            # Missing patterns
            if result['patterns']:
                missing_patterns = [p for p, exists in result['patterns'].items() if not exists]
                if missing_patterns:
                    print(f"   Missing patterns: {', '.join(missing_patterns)}")
            
            # Compliance score
            files_score = result['compliance']['files_passed'] / result['compliance']['files_total'] * 100
            patterns_score = result['compliance']['patterns_passed'] / result['compliance']['patterns_total'] * 100 if result['compliance']['patterns_total'] > 0 else 100
            print(f"   Compliance: {files_score:.0f}% files, {patterns_score:.0f}% patterns")


def main():
    """Main entry point."""
    print("🚀 Starting Service Structure Validation")
    print("=" * 80)
    
    # Find all services
    services = find_services(PROJECT_ROOT)
    print(f"Found {len(services)} services")
    
    # Validate each service
    results = []
    for service_path in services:
        result = validate_service(service_path)
        results.append(result)
    
    # Print report
    print_report(results)
    
    # Save report
    report_file = PROJECT_ROOT / 'dependencies' / 'service-structure-validation-report.json'
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump({
            'total_services': len(results),
            'compliant_services': sum(1 for r in results if r['compliance']['is_compliant']),
            'results': results
        }, f, indent=2)
    
    print(f"\n✅ Report saved to: {report_file}")
    
    # Exit with error code if any services are non-compliant
    if any(not r['compliance']['is_compliant'] for r in results):
        sys.exit(1)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

