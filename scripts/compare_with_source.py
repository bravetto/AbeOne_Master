#!/usr/bin/env python3
"""
Compare current codebase with AbeONE-Source repository
Generate similarity report
"""

import os
import hashlib
import filecmp
from pathlib import Path
from collections import defaultdict
import json

# Paths
CURRENT_REPO = Path("/Users/michaelmataluni/Documents/AbeOne_Master")
SOURCE_REPO = Path("/tmp/abeone-source-comparison")

# Exclude patterns - more comprehensive
EXCLUDE_PATTERNS = [
    ".git",
    "__pycache__",
    ".pyc",
    "node_modules",
    ".next",
    ".venv",
    "venv",
    "env",
    ".DS_Store",
    "*.log",
    ".cursor",
    ".vscode",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".forensic_emoji_removal_backup",
    "archive",
    "temp_repos",
    "satellites",
    "orbital",
    "download",
    "Downloads",
    "repositories",
    ".abeone_memory",
    "out",
    "_next",
    "CDF",
    "DASHBOARDS",
    "Documents",
]

# Source code file extensions to focus on
SOURCE_EXTENSIONS = {
    '.py', '.ts', '.tsx', '.js', '.jsx', '.json', '.yaml', '.yml',
    '.toml', '.ini', '.cfg', '.conf', '.sh', '.bash', '.zsh',
    '.dockerfile', '.md', '.txt', '.sql', '.graphql', '.gql',
    '.css', '.scss', '.sass', '.less', '.html', '.xml',
    '.go', '.rs', '.java', '.cpp', '.c', '.h', '.hpp',
    '.rb', '.php', '.swift', '.kt', '.scala', '.clj',
    '.vue', '.svelte', '.dart', '.r', '.m', '.mm',
}

# Documentation-only patterns (exclude from source code comparison)
DOC_ONLY_PATTERNS = [
    '/docs/',
    '/documentation/',
    'README.md',
    'CHANGELOG.md',
    'LICENSE',
    '.md',  # Will be handled separately
]

def should_exclude(path_str):
    """Check if path should be excluded"""
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False

def get_file_hash(filepath):
    """Get SHA256 hash of file"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def is_source_file(filepath_str):
    """Check if file is source code (not just documentation)"""
    path_lower = filepath_str.lower()
    
    # Exclude pure documentation directories
    for pattern in DOC_ONLY_PATTERNS:
        if pattern in path_lower and pattern != '.md':
            return False
    
    # Check extension
    ext = Path(filepath_str).suffix.lower()
    if ext in SOURCE_EXTENSIONS:
        return True
    
    # Include files without extension if they're in source directories
    if not ext:
        # Check if it's a config file or script
        if any(x in filepath_str.lower() for x in ['dockerfile', 'makefile', '.env', 'requirements', 'package.json', 'tsconfig', 'pyproject']):
            return True
    
    return False

def get_all_files(root_dir, relative_to=None, source_only=False):
    """Get all files in directory tree"""
    files = {}
    root = Path(root_dir)
    
    if not root.exists():
        return files
    
    for filepath in root.rglob('*'):
        if filepath.is_file():
            rel_path = filepath.relative_to(root)
            rel_str = str(rel_path)
            
            if not should_exclude(rel_str):
                # If source_only, filter to source files
                if source_only and not is_source_file(rel_str):
                    continue
                    
                if relative_to:
                    files[rel_str] = filepath
                else:
                    files[rel_str] = filepath
    
    return files

def compare_files(current_files, source_files):
    """Compare files between two repositories"""
    results = {
        'identical': [],
        'different': [],
        'only_current': [],
        'only_source': [],
        'total_current': len(current_files),
        'total_source': len(source_files),
    }
    
    # Find common files
    common_files = set(current_files.keys()) & set(source_files.keys())
    
    for rel_path in common_files:
        current_file = current_files[rel_path]
        source_file = source_files[rel_path]
        
        current_hash = get_file_hash(current_file)
        source_hash = get_file_hash(source_file)
        
        if current_hash and source_hash:
            if current_hash == source_hash:
                results['identical'].append(rel_path)
            else:
                results['different'].append(rel_path)
        else:
            # If we can't hash, try filecmp
            try:
                if filecmp.cmp(str(current_file), str(source_file), shallow=False):
                    results['identical'].append(rel_path)
                else:
                    results['different'].append(rel_path)
            except Exception:
                results['different'].append(rel_path)
    
    # Files only in current
    results['only_current'] = list(set(current_files.keys()) - set(source_files.keys()))
    
    # Files only in source
    results['only_source'] = list(set(source_files.keys()) - set(current_files.keys()))
    
    return results

def calculate_similarity(results):
    """Calculate similarity percentage"""
    total_common = len(results['identical']) + len(results['different'])
    
    if total_common == 0:
        return 0.0
    
    # Primary metric: How many files are identical vs different
    identical_count = len(results['identical'])
    different_count = len(results['different'])
    
    # Similarity based on identical files vs total common files
    if total_common > 0:
        content_similarity = (identical_count / total_common) * 100
    else:
        content_similarity = 0.0
    
    # Secondary metric: Coverage (how much of source repo is in current)
    source_total = results['total_source']
    if source_total > 0:
        coverage = (total_common / source_total) * 100
    else:
        coverage = 0.0
    
    # If all source files are present and identical, that's 100%
    if identical_count == source_total and different_count == 0:
        return 100.0
    
    # Weighted combination: 80% content similarity, 20% coverage
    final_similarity = (content_similarity * 0.8 + coverage * 0.2)
    
    return min(100.0, max(0.0, final_similarity))

def generate_report(results, similarity):
    """Generate detailed report"""
    report = []
    report.append("=" * 80)
    report.append("ABEONE SOURCE COMPARISON REPORT")
    report.append("=" * 80)
    report.append("")
    report.append(f"Current Repository: {CURRENT_REPO}")
    report.append(f"Source Repository:  {SOURCE_REPO}")
    report.append("")
    report.append("-" * 80)
    report.append("SIMILARITY METRICS")
    report.append("-" * 80)
    report.append(f"Overall Similarity: {similarity:.2f}%")
    report.append(f"Target: 98.00%")
    report.append(f"Status: {'✅ PASS' if similarity >= 98.0 else '❌ FAIL'}")
    report.append("")
    
    report.append("-" * 80)
    report.append("FILE STATISTICS")
    report.append("-" * 80)
    report.append(f"Total files in current repo: {results['total_current']}")
    report.append(f"Total files in source repo:  {results['total_source']}")
    report.append(f"Identical files:             {len(results['identical'])}")
    report.append(f"Different files:              {len(results['different'])}")
    report.append(f"Only in current repo:        {len(results['only_current'])}")
    report.append(f"Only in source repo:          {len(results['only_source'])}")
    report.append("")
    
    # Calculate percentages
    total_common = len(results['identical']) + len(results['different'])
    if total_common > 0:
        identical_pct = (len(results['identical']) / total_common) * 100
        different_pct = (len(results['different']) / total_common) * 100
        report.append(f"Identical files: {identical_pct:.2f}% of common files")
        report.append(f"Different files: {different_pct:.2f}% of common files")
    report.append("")
    
    # Show sample differences
    if results['different']:
        report.append("-" * 80)
        report.append("SAMPLE DIFFERENT FILES (first 20)")
        report.append("-" * 80)
        for file_path in sorted(results['different'])[:20]:
            report.append(f"  - {file_path}")
        if len(results['different']) > 20:
            report.append(f"  ... and {len(results['different']) - 20} more")
        report.append("")
    
    if results['only_current']:
        report.append("-" * 80)
        report.append("FILES ONLY IN CURRENT REPO (first 20)")
        report.append("-" * 80)
        for file_path in sorted(results['only_current'])[:20]:
            report.append(f"  - {file_path}")
        if len(results['only_current']) > 20:
            report.append(f"  ... and {len(results['only_current']) - 20} more")
        report.append("")
    
    if results['only_source']:
        report.append("-" * 80)
        report.append("FILES ONLY IN SOURCE REPO (first 20)")
        report.append("-" * 80)
        for file_path in sorted(results['only_source'])[:20]:
            report.append(f"  - {file_path}")
        if len(results['only_source']) > 20:
            report.append(f"  ... and {len(results['only_source']) - 20} more")
        report.append("")
    
    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)
    
    return "\n".join(report)

def main():
    print("🔍 Scanning current repository (all files)...")
    current_files_all = get_all_files(CURRENT_REPO, source_only=False)
    print(f"   Found {len(current_files_all)} total files")
    
    print("🔍 Scanning current repository (source code only)...")
    current_files_source = get_all_files(CURRENT_REPO, source_only=True)
    print(f"   Found {len(current_files_source)} source code files")
    
    print("🔍 Scanning source repository...")
    source_files = get_all_files(SOURCE_REPO, source_only=False)
    print(f"   Found {len(source_files)} files")
    
    print("🔍 Comparing files...")
    results = compare_files(current_files_all, source_files)
    
    print("🔍 Calculating similarity...")
    similarity = calculate_similarity(results)
    
    print("🔍 Generating report...")
    report = generate_report(results, similarity)
    
    print("\n" + report)
    
    # Save detailed results to JSON
    results_json = {
        'similarity_percentage': similarity,
        'target_percentage': 98.0,
        'status': 'PASS' if similarity >= 98.0 else 'FAIL',
        'statistics': {
            'total_current': results['total_current'],
            'total_source': results['total_source'],
            'identical': len(results['identical']),
            'different': len(results['different']),
            'only_current': len(results['only_current']),
            'only_source': len(results['only_source']),
        },
        'different_files': results['different'][:50],  # First 50
        'only_current_files': results['only_current'][:50],
        'only_source_files': results['only_source'][:50],
    }
    
    json_path = CURRENT_REPO / "comparison_results.json"
    with open(json_path, 'w') as f:
        json.dump(results_json, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {json_path}")
    
    return similarity >= 98.0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

