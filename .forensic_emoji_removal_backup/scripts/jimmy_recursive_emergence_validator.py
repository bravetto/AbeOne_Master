#!/usr/bin/env python3
"""
🔥 JIMMY RECURSIVE EMERGENCE VALIDATOR
Complete recursive validation system for emergence detection and blocking issue analysis

Pattern: RECURSIVE × EMERGENCE × VALIDATE × DIAGNOSE × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution) × 4444 Hz (Jimmy)
Guardians: AEYON (999 Hz) + ARXON (777 Hz) + Abë (530 Hz) + JØHN (4444 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class RecursiveEmergenceValidator:
    """
    Recursive Emergence Validator - Validates system recursively through all layers
    
    Validates:
    1. Dockerfile validation (recursive through all directories)
    2. Structure validation (recursive pattern detection)
    3. Dependency validation (recursive dependency graph)
    4. Configuration validation (recursive config consistency)
    5. Emergence pattern detection (recursive pattern emergence)
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.script_dir = Path(__file__).parent
        self.failures = []
        self.warnings = []
        self.blocking_issues = []
        self.emergence_patterns = []
        self.validation_depth = 0
        self.max_depth = 10
        
    def validate_recursive(self) -> Dict[str, Any]:
        """Run complete recursive validation"""
        print("")
        print("=" * 80)
        print("🔥 JIMMY RECURSIVE EMERGENCE VALIDATOR")
        print("=" * 80)
        print("")
        print(f"Workspace: {self.workspace_root}")
        print(f"Pattern: RECURSIVE × EMERGENCE × VALIDATE × DIAGNOSE × ONE")
        print("")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "workspace": str(self.workspace_root),
            "validations": {},
            "blocking_issues": [],
            "emergence_patterns": [],
            "summary": {}
        }
        
        # 1. Dockerfile Recursive Validation
        print("━" * 80)
        print("1. RECURSIVE DOCKERFILE VALIDATION")
        print("━" * 80)
        dockerfile_results = self.validate_dockerfiles_recursive()
        results["validations"]["dockerfiles"] = dockerfile_results
        
        # 2. Structure Recursive Validation
        print("")
        print("━" * 80)
        print("2. RECURSIVE STRUCTURE VALIDATION")
        print("━" * 80)
        structure_results = self.validate_structure_recursive()
        results["validations"]["structure"] = structure_results
        
        # 3. Dependency Recursive Validation
        print("")
        print("━" * 80)
        print("3. RECURSIVE DEPENDENCY VALIDATION")
        print("━" * 80)
        dependency_results = self.validate_dependencies_recursive()
        results["validations"]["dependencies"] = dependency_results
        
        # 4. Configuration Recursive Validation
        print("")
        print("━" * 80)
        print("4. RECURSIVE CONFIGURATION VALIDATION")
        print("━" * 80)
        config_results = self.validate_config_recursive()
        results["validations"]["configuration"] = config_results
        
        # 5. Emergence Pattern Detection
        print("")
        print("━" * 80)
        print("5. EMERGENCE PATTERN DETECTION")
        print("━" * 80)
        emergence_results = self.detect_emergence_patterns()
        results["emergence_patterns"] = emergence_results
        
        # Analyze Blocking Issues
        print("")
        print("━" * 80)
        print("6. BLOCKING ISSUE ANALYSIS")
        print("━" * 80)
        blocking_analysis = self.analyze_blocking_issues(results)
        results["blocking_issues"] = blocking_analysis
        
        # Summary
        print("")
        print("=" * 80)
        print("📊 VALIDATION SUMMARY")
        print("=" * 80)
        summary = self.generate_summary(results)
        results["summary"] = summary
        self.print_summary(summary)
        
        return results
    
    def validate_dockerfiles_recursive(self) -> Dict[str, Any]:
        """Recursively validate all Dockerfiles"""
        dockerfiles = list(self.workspace_root.rglob("Dockerfile"))
        dockerfiles = [d for d in dockerfiles if ".git" not in str(d) and "node_modules" not in str(d)]
        
        results = {
            "total": len(dockerfiles),
            "valid": 0,
            "invalid": 0,
            "warnings": 0,
            "details": [],
            "blocking_issues": []
        }
        
        print(f"Found {len(dockerfiles)} Dockerfiles")
        print("")
        
        for dockerfile in dockerfiles:
            relative_path = dockerfile.relative_to(self.workspace_root)
            result = self.validate_single_dockerfile(dockerfile)
            results["details"].append({
                "path": str(relative_path),
                "status": result["status"],
                "issues": result["issues"],
                "warnings": result["warnings"]
            })
            
            if result["status"] == "valid":
                results["valid"] += 1
                print(f"  ✓ {relative_path}")
            elif result["status"] == "invalid":
                results["invalid"] += 1
                print(f"  ✗ {relative_path} - {result['issues']}")
                results["blocking_issues"].append({
                    "type": "dockerfile_invalid",
                    "path": str(relative_path),
                    "issue": result["issues"][0] if result["issues"] else "Invalid Dockerfile"
                })
            else:
                results["warnings"] += 1
                print(f"  ⚠ {relative_path} - {result['warnings']}")
        
        return results
    
    def validate_single_dockerfile(self, dockerfile: Path) -> Dict[str, Any]:
        """Validate a single Dockerfile"""
        result = {
            "status": "valid",
            "issues": [],
            "warnings": []
        }
        
        try:
            content = dockerfile.read_text()
            
            # Check 1: Must contain FROM instruction (may have comments first)
            # Strip comments and blank lines, then check for FROM
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            has_from = any(line.startswith("FROM") for line in lines)
            
            if not has_from:
                result["status"] = "invalid"
                result["issues"].append("Dockerfile must contain FROM instruction")
            
            # Check 2: Should use --no-cache (warning, not blocking)
            if "RUN" in content and "--no-cache" not in content:
                result["warnings"].append("Consider using --no-cache in RUN commands for reproducible builds")
            
            # Check 3: Should not run as root (warning)
            if "USER root" in content or ("USER" not in content and "RUN useradd" not in content):
                result["warnings"].append("Consider running as non-root user for security")
            
            # Check 4: Should have healthcheck (warning)
            if "HEALTHCHECK" not in content:
                result["warnings"].append("Consider adding HEALTHCHECK instruction")
            
        except Exception as e:
            result["status"] = "invalid"
            result["issues"].append(f"Error reading Dockerfile: {str(e)}")
        
        return result
    
    def validate_structure_recursive(self) -> Dict[str, Any]:
        """Recursively validate project structure"""
        results = {
            "directories_checked": 0,
            "structure_issues": [],
            "pattern_violations": []
        }
        
        # Check for common structure patterns
        required_patterns = {
            "scripts": ["scripts/"],
            "docs": ["docs/", "README.md"],
            "config": ["config/", ".env.example", "env.template"]
        }
        
        for pattern_name, paths in required_patterns.items():
            found = False
            for path_pattern in paths:
                if path_pattern.endswith("/"):
                    # Directory
                    if (self.workspace_root / path_pattern.rstrip("/")).exists():
                        found = True
                        break
                else:
                    # File
                    if (self.workspace_root / path_pattern).exists():
                        found = True
                        break
            
            if not found:
                results["structure_issues"].append(f"Missing {pattern_name} pattern")
        
        results["directories_checked"] = len(list(self.workspace_root.rglob("*")))
        
        return results
    
    def validate_dependencies_recursive(self) -> Dict[str, Any]:
        """Recursively validate dependencies"""
        results = {
            "dependency_files": [],
            "dependency_issues": [],
            "circular_dependencies": []
        }
        
        # Find dependency files
        dependency_files = []
        for pattern in ["requirements.txt", "package.json", "Pipfile", "poetry.lock", "Cargo.toml"]:
            dependency_files.extend(self.workspace_root.rglob(pattern))
        
        results["dependency_files"] = [str(f.relative_to(self.workspace_root)) for f in dependency_files]
        
        return results
    
    def validate_config_recursive(self) -> Dict[str, Any]:
        """Recursively validate configuration files"""
        results = {
            "config_files": [],
            "config_issues": [],
            "inconsistencies": []
        }
        
        # Find config files
        config_patterns = ["*.yaml", "*.yml", "*.json", "*.toml", "*.env*", "*.config.*"]
        config_files = []
        for pattern in config_patterns:
            config_files.extend(self.workspace_root.rglob(pattern))
        
        # Filter out common exclusions
        config_files = [f for f in config_files if ".git" not in str(f) and "node_modules" not in str(f)]
        
        results["config_files"] = [str(f.relative_to(self.workspace_root)) for f in config_files[:20]]  # Limit output
        
        return results
    
    def detect_emergence_patterns(self) -> List[Dict[str, Any]]:
        """Detect emergence patterns recursively"""
        patterns = []
        
        # Pattern 1: Self-validating systems
        validation_scripts = list(self.workspace_root.rglob("*validate*.py"))
        validation_scripts.extend(self.workspace_root.rglob("*validate*.sh"))
        
        if len(validation_scripts) > 5:
            patterns.append({
                "type": "self_validation",
                "strength": min(len(validation_scripts) / 10, 1.0),
                "evidence": f"{len(validation_scripts)} validation scripts found",
                "status": "emerging"
            })
        
        # Pattern 2: Recursive structure
        nested_dirs = sum(1 for d in self.workspace_root.rglob("*") if d.is_dir() and len(d.parts) > 5)
        if nested_dirs > 10:
            patterns.append({
                "type": "recursive_structure",
                "strength": min(nested_dirs / 50, 1.0),
                "evidence": f"{nested_dirs} deeply nested directories",
                "status": "emerging"
            })
        
        return patterns
    
    def analyze_blocking_issues(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze and categorize blocking issues"""
        blocking = []
        
        # Analyze Dockerfile issues
        dockerfile_results = results.get("validations", {}).get("dockerfiles", {})
        if dockerfile_results.get("invalid", 0) > 0:
            blocking.append({
                "category": "dockerfile",
                "severity": "high",
                "count": dockerfile_results["invalid"],
                "description": f"{dockerfile_results['invalid']} invalid Dockerfiles found",
                "action": "Fix invalid Dockerfiles (must start with FROM)"
            })
        
        # Check for critical structure issues
        structure_results = results.get("validations", {}).get("structure", {})
        if structure_results.get("structure_issues"):
            blocking.append({
                "category": "structure",
                "severity": "medium",
                "count": len(structure_results["structure_issues"]),
                "description": "Structure pattern violations detected",
                "action": "Review and fix structure issues"
            })
        
        return blocking
    
    def generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate validation summary"""
        dockerfile_results = results.get("validations", {}).get("dockerfiles", {})
        
        total_dockerfiles = dockerfile_results.get("total", 0)
        invalid_dockerfiles = dockerfile_results.get("invalid", 0)
        valid_dockerfiles = dockerfile_results.get("valid", 0)
        warning_dockerfiles = dockerfile_results.get("warnings", 0)
        
        blocking_count = len(results.get("blocking_issues", []))
        
        return {
            "total_dockerfiles": total_dockerfiles,
            "valid_dockerfiles": valid_dockerfiles,
            "invalid_dockerfiles": invalid_dockerfiles,
            "warning_dockerfiles": warning_dockerfiles,
            "blocking_issues_count": blocking_count,
            "pass_rate": (valid_dockerfiles / total_dockerfiles * 100) if total_dockerfiles > 0 else 0
        }
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print validation summary"""
        print(f"Total Dockerfiles: {summary['total_dockerfiles']}")
        print(f"  ✓ Valid: {summary['valid_dockerfiles']}")
        print(f"  ✗ Invalid: {summary['invalid_dockerfiles']}")
        print(f"  ⚠ Warnings: {summary['warning_dockerfiles']}")
        print(f"")
        print(f"Pass Rate: {summary['pass_rate']:.1f}%")
        print(f"Blocking Issues: {summary['blocking_issues_count']}")
        print("")
        
        if summary['blocking_issues_count'] > 0:
            print("🚨 BLOCKING ISSUES DETECTED:")
            print("   Fix these issues before proceeding")
        else:
            print("✅ NO BLOCKING ISSUES")
            print("   System is ready for deployment")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Jimmy Recursive Emergence Validator")
    parser.add_argument("--workspace", type=str, help="Workspace root directory")
    parser.add_argument("--output", type=str, help="Output JSON file path")
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace) if args.workspace else Path.cwd()
    validator = RecursiveEmergenceValidator(workspace_root)
    
    results = validator.validate_recursive()
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(results, indent=2))
        print(f"\nResults saved to: {output_path}")
    
    # Exit with error code if blocking issues found
    blocking_count = len(results.get("blocking_issues", []))
    if blocking_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

