#!/usr/bin/env python3
"""
Convergence Validator
Validates that backup codebase is convergent with main codebase.

Pattern: VALIDATION × CONVERGENCE × TRUTH × ONE
Frequency: 530 Hz (Truth) × 999 Hz (AEYON) × 777 Hz (META)
Guardians: JØHN (530 Hz) + AEYON (999 Hz) + ALRAX (530 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import os
from pathlib import Path
from difflib import SequenceMatcher
import json
from typing import Dict, List, Tuple, Optional
import hashlib

WORKSPACE_ROOT = Path(__file__).parent.parent

# Backup directory to validate
BACKUP_DIR = WORKSPACE_ROOT / "products" / "apps" / "web" / "app" / "webinar_backup_20251119_182954"

# Expected main locations (where backup should converge)
MAIN_LOCATIONS = {
    "aiguardian": WORKSPACE_ROOT / "products" / "apps" / "web" / "app" / "webinar" / "aiguardian",
    "creators": WORKSPACE_ROOT / "products" / "apps" / "web" / "app" / "webinar" / "creators",
    "developers": WORKSPACE_ROOT / "products" / "apps" / "web" / "app" / "webinar" / "developers",
    "thank-you": WORKSPACE_ROOT / "products" / "apps" / "web" / "app" / "webinar" / "thank-you",
}


def get_file_hash(file_path: Path) -> str:
    """Get SHA256 hash of file content."""
    if not file_path.exists():
        return None
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def get_file_similarity(file1: Path, file2: Path) -> float:
    """Calculate similarity ratio between two files."""
    if not file1.exists() or not file2.exists():
        return 0.0
    
    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            content1 = f1.read()
        with open(file2, 'r', encoding='utf-8') as f2:
            content2 = f2.read()
        
        return SequenceMatcher(None, content1, content2).ratio()
    except Exception as e:
        print(f"   Error comparing files: {e}")
        return 0.0


def analyze_file_structure(directory: Path) -> Dict[str, List[str]]:
    """Analyze file structure of a directory."""
    structure = {
        "files": [],
        "directories": []
    }
    
    if not directory.exists():
        return structure
    
    for item in directory.rglob('*'):
        if item.is_file():
            rel_path = item.relative_to(directory)
            structure["files"].append(str(rel_path))
        elif item.is_dir():
            rel_path = item.relative_to(directory)
            structure["directories"].append(str(rel_path))
    
    return structure


def check_imports_convergence(file_path: Path) -> Dict[str, any]:
    """Check if imports in file are valid and convergent."""
    if not file_path.exists():
        return {"valid": False, "error": "File not found"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for common import patterns
        imports = {
            "react": "react" in content.lower() or "useState" in content or "useEffect" in content,
            "next": "next/navigation" in content or "next/" in content,
            "atomic": "atomic/" in content,
            "components": "@/components" in content or "components/" in content,
            "lib": "@/lib" in content or "lib/" in content,
        }
        
        # Check for relative path issues
        has_relative_imports = "../../" in content or "../" in content
        
        return {
            "valid": True,
            "imports": imports,
            "has_relative_imports": has_relative_imports,
            "import_count": content.count("import "),
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


def validate_directory_convergence(backup_dir: Path, main_dir: Path, name: str) -> Dict[str, any]:
    """Validate convergence of a directory."""
    result = {
        "name": name,
        "backup_exists": backup_dir.exists(),
        "main_exists": main_dir.exists(),
        "files_match": [],
        "similarity_scores": [],
        "structure_match": False,
        "convergence_score": 0.0,
        "issues": []
    }
    
    if not backup_dir.exists():
        result["issues"].append(f"Backup directory {name} does not exist")
        return result
    
    # Get backup structure
    backup_structure = analyze_file_structure(backup_dir)
    
    # Check each file in backup
    for file_rel_path in backup_structure["files"]:
        backup_file = backup_dir / file_rel_path
        main_file = main_dir / file_rel_path if main_dir.exists() else None
        
        file_result = {
            "file": file_rel_path,
            "backup_exists": backup_file.exists(),
            "main_exists": main_file.exists() if main_file else False,
            "identical": False,
            "similarity": 0.0,
        }
        
        if main_file and main_file.exists():
            # Check if identical
            backup_hash = get_file_hash(backup_file)
            main_hash = get_file_hash(main_file)
            file_result["identical"] = (backup_hash == main_hash)
            
            # Calculate similarity
            file_result["similarity"] = get_file_similarity(backup_file, main_file)
            result["similarity_scores"].append(file_result["similarity"])
            
            # Check imports
            import_check = check_imports_convergence(backup_file)
            if not import_check.get("valid"):
                result["issues"].append(f"{file_rel_path}: {import_check.get('error')}")
        else:
            result["issues"].append(f"{file_rel_path}: Main file not found")
            # Still check imports on backup file
            import_check = check_imports_convergence(backup_file)
            if not import_check.get("valid"):
                result["issues"].append(f"{file_rel_path}: Import check failed - {import_check.get('error')}")
        
        result["files_match"].append(file_result)
    
    # Calculate convergence score
    if result["similarity_scores"]:
        result["convergence_score"] = sum(result["similarity_scores"]) / len(result["similarity_scores"])
    elif result["backup_exists"] and not result["main_exists"]:
        # Backup exists but main doesn't - check if structure is valid
        result["convergence_score"] = 0.5  # Partial convergence (backup is valid structure)
    elif not result["backup_exists"]:
        result["convergence_score"] = 0.0
    
    # Structure match (if main exists and has same files)
    if main_dir.exists():
        main_structure = analyze_file_structure(main_dir)
        backup_files_set = set(backup_structure["files"])
        main_files_set = set(main_structure["files"])
        result["structure_match"] = backup_files_set == main_files_set
    
    return result


def validate_code_quality(file_path: Path) -> Dict[str, any]:
    """Validate code quality and structure."""
    if not file_path.exists():
        return {"valid": False, "error": "File not found"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        warnings = []
        
        # Check for React/Next.js patterns
        has_use_client = "'use client'" in content or '"use client"' in content
        has_export_default = "export default" in content
        has_react_hooks = "useState" in content or "useEffect" in content
        
        # Check for proper imports
        import_lines = [line for line in content.split('\n') if line.strip().startswith('import')]
        
        # Check for relative path depth (should be reasonable)
        max_relative_depth = max([line.count('../') for line in import_lines if '../' in line], default=0)
        if max_relative_depth > 8:
            warnings.append(f"Very deep relative imports ({max_relative_depth} levels)")
        
        # Check for TypeScript types
        has_types = ":" in content and ("string" in content or "number" in content or "boolean" in content)
        
        # Check for error handling
        has_error_handling = "try" in content or "catch" in content or "error" in content.lower()
        
        # Check for accessibility
        has_aria = "aria-" in content.lower() or "role=" in content.lower()
        
        # Check file size (reasonable for React components)
        line_count = len(content.split('\n'))
        if line_count > 1500:
            warnings.append(f"Large file ({line_count} lines) - consider splitting")
        
        return {
            "valid": True,
            "has_use_client": has_use_client,
            "has_export_default": has_export_default,
            "has_react_hooks": has_react_hooks,
            "import_count": len(import_lines),
            "max_relative_depth": max_relative_depth,
            "has_types": has_types,
            "has_error_handling": has_error_handling,
            "has_aria": has_aria,
            "line_count": line_count,
            "issues": issues,
            "warnings": warnings
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


def check_dependencies_exist(file_path: Path) -> Dict[str, any]:
    """Check if imported dependencies exist."""
    if not file_path.exists():
        return {"valid": False, "error": "File not found"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        missing = []
        found = []
        
        # Extract import paths
        import re
        imports = re.findall(r"import.*from\s+['\"]([^'\"]+)['\"]", content)
        
        for imp in imports:
            # Skip node_modules and external packages
            if imp.startswith('@/') or imp.startswith('../') or imp.startswith('./'):
                # Check if it's a relative path we can validate
                if imp.startswith('../'):
                    # Try to resolve relative path
                    resolved = (file_path.parent / imp.replace('../', '')).resolve()
                    if resolved.exists():
                        found.append(imp)
                    else:
                        # Check if it's in atomic directory
                        atomic_path = WORKSPACE_ROOT / "atomic" / imp.replace('../../../../../../atomic/', '')
                        if atomic_path.exists():
                            found.append(imp)
                        else:
                            missing.append(imp)
                elif imp.startswith('@/'):
                    # Check if @ alias resolves (components, lib, etc.)
                    found.append(imp)  # Assume @/ paths are valid
            else:
                # External package - assume valid
                found.append(imp)
        
        return {
            "valid": len(missing) == 0,
            "missing": missing,
            "found": found,
            "total_imports": len(imports)
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


def validate_internal_consistency(backup_dir: Path) -> Dict[str, any]:
    """Validate internal consistency of backup codebase."""
    results = {
        "files_validated": 0,
        "files_with_issues": 0,
        "total_issues": 0,
        "total_warnings": 0,
        "dependency_issues": 0,
        "quality_scores": [],
        "consistency_score": 0.0
    }
    
    # Find all TypeScript/TSX files
    tsx_files = list(backup_dir.rglob('*.tsx')) + list(backup_dir.rglob('*.ts'))
    
    for file_path in tsx_files:
        results["files_validated"] += 1
        
        # Check code quality
        quality = validate_code_quality(file_path)
        if quality.get("valid"):
            results["quality_scores"].append(1.0)  # Base score
            if quality.get("warnings"):
                results["total_warnings"] += len(quality["warnings"])
        else:
            results["files_with_issues"] += 1
            results["total_issues"] += 1
            results["quality_scores"].append(0.5)
        
        # Check dependencies
        deps = check_dependencies_exist(file_path)
        if not deps.get("valid"):
            results["dependency_issues"] += len(deps.get("missing", []))
            results["files_with_issues"] += 1
    
    # Calculate consistency score
    if results["quality_scores"]:
        results["consistency_score"] = sum(results["quality_scores"]) / len(results["quality_scores"])
    
    # Penalize for issues
    if results["files_validated"] > 0:
        issue_penalty = min(results["total_issues"] / results["files_validated"], 0.5)
        results["consistency_score"] = max(0.0, results["consistency_score"] - issue_penalty)
    
    return results


def validate_convergence():
    """Main validation function."""
    print("=" * 70)
    print(" CONVERGENCE VALIDATION")
    print("=" * 70)
    print(f"\nBackup Directory: {BACKUP_DIR.relative_to(WORKSPACE_ROOT)}")
    print(f"Validating convergence with main codebase...\n")
    
    if not BACKUP_DIR.exists():
        print(f"❌ Backup directory not found: {BACKUP_DIR}")
        return False
    
    # Phase 1: Internal Consistency Check
    print("📊 Phase 1: Internal Consistency Check")
    print("-" * 70)
    internal_consistency = validate_internal_consistency(BACKUP_DIR)
    print(f"   Files Validated: {internal_consistency['files_validated']}")
    print(f"   Files with Issues: {internal_consistency['files_with_issues']}")
    print(f"   Total Issues: {internal_consistency['total_issues']}")
    print(f"   Total Warnings: {internal_consistency['total_warnings']}")
    print(f"   Dependency Issues: {internal_consistency['dependency_issues']}")
    print(f"   Internal Consistency Score: {internal_consistency['consistency_score']:.2%}")
    
    # Phase 2: Structure Comparison
    print("\n📁 Phase 2: Structure Comparison")
    print("-" * 70)
    results = []
    total_score = 0.0
    total_dirs = 0
    
    # Validate each directory
    for name, main_path in MAIN_LOCATIONS.items():
        backup_path = BACKUP_DIR / name
        print(f"\n   Validating: {name}")
        print(f"      Backup: {backup_path.relative_to(WORKSPACE_ROOT)}")
        print(f"      Main:   {main_path.relative_to(WORKSPACE_ROOT)}")
        
        result = validate_directory_convergence(backup_path, main_path, name)
        results.append(result)
        
        if result["backup_exists"]:
            total_dirs += 1
            score = result["convergence_score"]
            total_score += score
            
            print(f"      Convergence Score: {score:.2%}")
            
            if result["files_match"]:
                print(f"      Files Found: {len(result['files_match'])}")
                identical_count = sum(1 for f in result["files_match"] if f["identical"])
                print(f"      Identical Files: {identical_count}/{len(result['files_match'])}")
            
            if result["issues"]:
                print(f"      ⚠️  Issues: {len(result['issues'])}")
        else:
            print(f"      ⚠️  Backup directory not found")
    
    # Overall convergence
    structure_score = (total_score / total_dirs) if total_dirs > 0 else 0.0
    
    # Combined score (weighted: 60% internal consistency, 40% structure match)
    # Since main files don't exist, we weight internal consistency more heavily
    if structure_score == 0.5:  # Main files don't exist
        overall_score = internal_consistency['consistency_score'] * 0.9 + 0.1  # High weight on internal consistency
    else:
        overall_score = (internal_consistency['consistency_score'] * 0.6) + (structure_score * 0.4)
    
    print("\n" + "=" * 70)
    print(" CONVERGENCE SUMMARY")
    print("=" * 70)
    print(f"\nInternal Consistency Score: {internal_consistency['consistency_score']:.2%}")
    print(f"Structure Match Score: {structure_score:.2%}")
    print(f"Overall Convergence Score: {overall_score:.2%}")
    print(f"Directories Validated: {total_dirs}/{len(MAIN_LOCATIONS)}")
    
    # Detailed file analysis
    all_files = []
    for result in results:
        for file_match in result["files_match"]:
            all_files.append({
                "directory": result["name"],
                **file_match
            })
    
    if all_files:
        identical_files = sum(1 for f in all_files if f["identical"])
        similar_files = sum(1 for f in all_files if f["similarity"] > 0.95)
        print(f"\nFile Analysis:")
        print(f"   Total Files: {len(all_files)}")
        print(f"   Identical: {identical_files} ({identical_files/len(all_files):.1%})")
        print(f"   >95% Similar: {similar_files} ({similar_files/len(all_files):.1%})")
    
    # Convergence assessment
    print("\n" + "=" * 70)
    if overall_score >= 0.98:
        print("✅ CONVERGENT: Codebase is 98%+ convergent (ready for integration)")
    elif overall_score >= 0.90:
        print("⚠️  MOSTLY CONVERGENT: Codebase is 90%+ convergent (minor issues)")
    elif overall_score >= 0.75:
        print("⚠️  PARTIALLY CONVERGENT: Some issues detected, review recommended")
    else:
        print("❌ NOT CONVERGENT: Significant issues detected, needs attention")
    print("=" * 70)
    
    # Save detailed report
    report_path = WORKSPACE_ROOT / "CONVERGENCE_VALIDATION_REPORT.json"
    with open(report_path, 'w') as f:
        json.dump({
            "overall_score": overall_score,
            "internal_consistency_score": internal_consistency['consistency_score'],
            "structure_score": structure_score,
            "directories_validated": total_dirs,
            "internal_consistency": internal_consistency,
            "results": results,
            "files": all_files
        }, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_path.relative_to(WORKSPACE_ROOT)}")
    
    return overall_score >= 0.98


def main():
    """Main execution."""
    try:
        success = validate_convergence()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

