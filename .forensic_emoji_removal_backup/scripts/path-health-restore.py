#!/usr/bin/env python3
"""
🔥 PATH HEALTH & RESTORE - Converged Success Patterns

Analyzes path issues and restores correct paths based on validated success patterns.

Pattern: PATH × HEALTH × RESTORE × CONVERGENCE × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)
Guardians: AEYON (999 Hz) + ALRAX (530 Hz) + YAGNI (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import subprocess


class PathStatus(str, Enum):
    """Path validation status"""
    VALID = "✅"
    INVALID = "❌"
    MISSING = "⚠️"
    NEEDS_UPDATE = "🔄"


@dataclass
class PathIssue:
    """Represents a path issue"""
    file_path: Path
    line_number: int
    old_path: str
    new_path: Optional[str] = None
    issue_type: str = ""
    severity: str = "MEDIUM"
    fix_suggestion: str = ""
    context: str = ""


@dataclass
class PathHealthReport:
    """Complete path health report"""
    workspace_root: Path
    issues: List[PathIssue] = field(default_factory=list)
    valid_paths: List[str] = field(default_factory=list)
    path_mappings: Dict[str, str] = field(default_factory=dict)
    pythonpath_needed: List[str] = field(default_factory=list)
    score: float = 0.0
    fixed_count: int = 0


class PathHealthRestorer:
    """
    Converged Path Health & Restore System
    
    Based on validated success patterns:
    1. git rev-parse --show-toplevel (most reliable repo root)
    2. Path(__file__).parent.parent (Python project root)
    3. Dynamic path resolution (check both old and new paths)
    4. Substrate-first validation (verify paths exist)
    """
    
    # Path migration mappings (old → new)
    PATH_MIGRATIONS = {
        "EMERGENT_OS/": "orbital/EMERGENT_OS-orbital/",
        "EMERGENT_OS": "orbital/EMERGENT_OS-orbital",
        "from EMERGENT_OS": "from orbital.EMERGENT_OS_orbital",
        "import EMERGENT_OS": "import orbital.EMERGENT_OS_orbital",
    }
    
    # Patterns that indicate path issues
    PATH_ISSUE_PATTERNS = [
        (r"EMERGENT_OS/", "Old EMERGENT_OS path detected"),
        (r"from EMERGENT_OS\.", "Old EMERGENT_OS import detected"),
        (r"import EMERGENT_OS", "Old EMERGENT_OS import detected"),
        (r"sys\.path\.insert\(0,\s*['\"]EMERGENT_OS", "Old EMERGENT_OS sys.path detected"),
        (r"cd.*EMERGENT_OS", "Old EMERGENT_OS cd command detected"),
        (r"EMERGENT_OS/synthesis", "Old EMERGENT_OS synthesis path"),
    ]
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize path health restorer"""
        self.workspace_root = self._resolve_workspace_root(workspace_root)
        self.report = PathHealthReport(workspace_root=self.workspace_root)
        self._detect_path_mappings()
    
    def _resolve_workspace_root(self, provided: Optional[Path]) -> Path:
        """
        Resolve workspace root using validated success patterns.
        
        Pattern Priority:
        1. Provided workspace_root (explicit)
        2. Path(__file__).parent.parent (from script location - most reliable for this workspace)
        3. Path.cwd() with module_manifest.json check
        4. git rev-parse --show-toplevel (fallback)
        """
        # Pattern 1: Provided workspace_root (explicit)
        if provided:
            resolved = Path(provided).resolve()
            if resolved.exists():
                return resolved
        
        # Pattern 2: Path(__file__).parent.parent (from script location - most reliable)
        try:
            script_root = Path(__file__).parent.parent.resolve()
            if script_root.exists() and (script_root / "module_manifest.json").exists():
                return script_root
        except Exception:
            pass
        
        # Pattern 3: Path.cwd() with module_manifest.json check
        cwd = Path.cwd().resolve()
        if (cwd / "module_manifest.json").exists():
            return cwd
        
        # Pattern 4: git rev-parse (fallback - may return parent repo)
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=str(cwd)
            )
            if result.returncode == 0:
                git_root = Path(result.stdout.strip()).resolve()
                # Check if git root has module_manifest.json or is the actual workspace
                if git_root.exists():
                    # If git root has module_manifest.json, use it
                    if (git_root / "module_manifest.json").exists():
                        return git_root
                    # Otherwise, check if current dir is a subdirectory
                    try:
                        cwd.relative_to(git_root)
                        # Current dir is under git root, check for module_manifest.json in cwd
                        if (cwd / "module_manifest.json").exists():
                            return cwd
                    except ValueError:
                        pass
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        
        # Fallback: Use current working directory
        return Path.cwd().resolve()
    
    def _detect_path_mappings(self):
        """Detect actual path mappings by checking what exists"""
        # Check for orbital structure
        orbital_dir = self.workspace_root / "orbital"
        if orbital_dir.exists():
            # Map old paths to new orbital paths
            for orbital in orbital_dir.iterdir():
                if orbital.is_dir() and orbital.name.endswith("-orbital"):
                    old_name = orbital.name.replace("-orbital", "")
                    self.report.path_mappings[f"{old_name}/"] = f"orbital/{orbital.name}/"
                    self.report.path_mappings[old_name] = f"orbital/{orbital.name}"
    
    def scan_scripts(self) -> PathHealthReport:
        """Scan all scripts for path issues"""
        scripts_dir = self.workspace_root / "scripts"
        if not scripts_dir.exists():
            return self.report
        
        # Scan Python scripts
        for py_file in scripts_dir.rglob("*.py"):
            if py_file.is_file():
                self._scan_file(py_file)
        
        # Scan shell scripts
        for sh_file in scripts_dir.rglob("*.sh"):
            if sh_file.is_file():
                self._scan_file(sh_file)
        
        # Scan JavaScript files
        for js_file in scripts_dir.rglob("*.js"):
            if js_file.is_file():
                self._scan_file(js_file)
        
        # Calculate health score
        self._calculate_health_score()
        
        return self.report
    
    def _scan_file(self, file_path: Path):
        """Scan a single file for path issues"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern, issue_type in self.PATH_ISSUE_PATTERNS:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        old_path = match.group(0)
                        new_path = self._resolve_new_path(old_path, file_path)
                        
                        # Get context (surrounding lines)
                        context_start = max(0, line_num - 2)
                        context_end = min(len(lines), line_num + 2)
                        context = "\n".join(lines[context_start:context_end])
                        
                        issue = PathIssue(
                            file_path=file_path,
                            line_number=line_num,
                            old_path=old_path,
                            new_path=new_path,
                            issue_type=issue_type,
                            severity=self._assess_severity(old_path, file_path),
                            fix_suggestion=self._generate_fix_suggestion(old_path, new_path, file_path),
                            context=context
                        )
                        
                        self.report.issues.append(issue)
        except Exception as e:
            # Skip files we can't read
            pass
    
    def _resolve_new_path(self, old_path: str, file_path: Path) -> Optional[str]:
        """Resolve new path for old path"""
        # Check if it's an import statement
        if "import" in old_path or "from" in old_path:
            # Handle Python imports
            if "EMERGENT_OS" in old_path:
                # Convert to orbital import
                new_import = old_path.replace("EMERGENT_OS", "orbitals.EMERGENT_OS_orbital")
                # Fix module name (replace hyphens with underscores)
                new_import = new_import.replace("EMERGENT_OS-orbital", "EMERGENT_OS_orbital")
                return new_import
        
        # Check for directory paths
        if "EMERGENT_OS/" in old_path or old_path == "EMERGENT_OS":
            # Check if orbital exists
            orbital_path = self.workspace_root / "orbitals" / "EMERGENT_OS-orbital"
            if orbital_path.exists():
                relative_path = orbital_path.relative_to(self.workspace_root)
                return str(relative_path)
        
        # Use mapping if available
        for old, new in self.report.path_mappings.items():
            if old in old_path:
                return old_path.replace(old, new)
        
        return None
    
    def _assess_severity(self, old_path: str, file_path: Path) -> str:
        """Assess severity of path issue"""
        # Check if the old path exists (low severity if it does)
        old_full_path = self.workspace_root / old_path.replace("'", "").replace('"', "")
        if old_full_path.exists():
            return "LOW"
        
        # Check if it's in a critical file
        critical_files = ["activate", "operationalize", "validate", "pre-commit"]
        if any(crit in file_path.name.lower() for crit in critical_files):
            return "HIGH"
        
        return "MEDIUM"
    
    def _generate_fix_suggestion(self, old_path: str, new_path: Optional[str], file_path: Path) -> str:
        """Generate fix suggestion for path issue"""
        if not new_path:
            return f"Check if path exists: {old_path}"
        
        file_ext = file_path.suffix
        
        if file_ext == ".py":
            # Python file - suggest import fix
            if "import" in old_path or "from" in old_path:
                return f"Replace: {old_path} → {new_path}"
            elif "sys.path" in old_path:
                return f"Use: sys.path.insert(0, str(workspace_root / '{new_path}'))"
            else:
                return f"Replace: {old_path} → {new_path}"
        
        elif file_ext == ".sh":
            # Shell script - suggest path fix
            return f"Replace: {old_path} → {new_path}"
        
        elif file_ext == ".js":
            # JavaScript - suggest require/import fix
            return f"Replace: {old_path} → {new_path}"
        
        return f"Update path: {old_path} → {new_path}"
    
    def _calculate_health_score(self):
        """Calculate overall path health score"""
        total_issues = len(self.report.issues)
        if total_issues == 0:
            self.report.score = 100.0
            return
        
        # Weight by severity
        high_severity = sum(1 for issue in self.report.issues if issue.severity == "HIGH")
        medium_severity = sum(1 for issue in self.report.issues if issue.severity == "MEDIUM")
        low_severity = sum(1 for issue in self.report.issues if issue.severity == "LOW")
        
        # Calculate score (penalize high severity more)
        penalty = (high_severity * 10) + (medium_severity * 5) + (low_severity * 2)
        self.report.score = max(0.0, 100.0 - penalty)
    
    def fix_issues(self, severity_filter: Optional[str] = None, dry_run: bool = False) -> int:
        """Fix path issues in files"""
        fixed_count = 0
        
        # Filter issues by severity
        issues_to_fix = self.report.issues
        if severity_filter:
            issues_to_fix = [i for i in issues_to_fix if i.severity.upper() == severity_filter.upper()]
        
        # Group by file
        files_to_fix = {}
        for issue in issues_to_fix:
            if issue.file_path not in files_to_fix:
                files_to_fix[issue.file_path] = []
            files_to_fix[issue.file_path].append(issue)
        
        # Fix each file
        for file_path, issues in files_to_fix.items():
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                modified = False
                
                for issue in sorted(issues, key=lambda x: x.line_number, reverse=True):
                    line_idx = issue.line_number - 1
                    if 0 <= line_idx < len(lines):
                        old_line = lines[line_idx]
                        if issue.new_path and issue.old_path in old_line:
                            new_line = old_line.replace(issue.old_path, issue.new_path)
                            lines[line_idx] = new_line
                            modified = True
                            fixed_count += 1
                
                if modified and not dry_run:
                    file_path.write_text('\n'.join(lines), encoding='utf-8')
                    print(f"✅ Fixed {len(issues)} issue(s) in {file_path.relative_to(self.workspace_root)}")
                elif modified and dry_run:
                    print(f"🔍 Would fix {len(issues)} issue(s) in {file_path.relative_to(self.workspace_root)}")
                    
            except Exception as e:
                print(f"⚠️  Error fixing {file_path}: {e}")
        
        self.report.fixed_count = fixed_count
        return fixed_count
    
    def generate_pythonpath_config(self) -> str:
        """Generate PYTHONPATH configuration"""
        pythonpath_dirs = []
        
        # Add orbitals directory
        orbitals_dir = self.workspace_root / "orbitals"
        if orbitals_dir.exists():
            pythonpath_dirs.append(str(orbitals_dir))
        
        # Add EMERGENT_OS-orbital if it exists
        emergent_orbital = self.workspace_root / "orbitals" / "EMERGENT_OS-orbital"
        if emergent_orbital.exists():
            pythonpath_dirs.append(str(emergent_orbital))
        
        # Add workspace root
        pythonpath_dirs.append(str(self.workspace_root))
        
        self.report.pythonpath_needed = pythonpath_dirs
        
        # Generate export command
        pythonpath_str = ":".join(pythonpath_dirs)
        return f"export PYTHONPATH=\"{pythonpath_str}:$PYTHONPATH\""
    
    def print_report(self, severity_filter: Optional[str] = None, verbose: bool = False):
        """Print path health report"""
        print("\n" + "=" * 80)
        print("🔥 PATH HEALTH & RESTORE REPORT")
        print("=" * 80)
        print(f"Workspace Root: {self.workspace_root}")
        print(f"Health Score: {self.report.score:.1f}%")
        print("=" * 80)
        print()
        
        # Filter issues by severity
        issues_to_show = self.report.issues
        if severity_filter:
            issues_to_show = [i for i in issues_to_show if i.severity.upper() == severity_filter.upper()]
        
        # Group issues by severity
        high_issues = [i for i in issues_to_show if i.severity == "HIGH"]
        medium_issues = [i for i in issues_to_show if i.severity == "MEDIUM"]
        low_issues = [i for i in issues_to_show if i.severity == "LOW"]
        
        if high_issues:
            print(f"❌ HIGH SEVERITY ISSUES ({len(high_issues)}):")
            print("-" * 80)
            for issue in high_issues:
                rel_path = issue.file_path.relative_to(self.workspace_root)
                print(f"  {rel_path}:{issue.line_number}")
                print(f"    Issue: {issue.issue_type}")
                print(f"    Old Path: {issue.old_path}")
                if issue.new_path:
                    print(f"    New Path: {issue.new_path}")
                print(f"    Fix: {issue.fix_suggestion}")
                if verbose:
                    print(f"    Context:\n{issue.context}")
                print()
        
        if medium_issues:
            print(f"⚠️  MEDIUM SEVERITY ISSUES ({len(medium_issues)}):")
            print("-" * 80)
            for issue in medium_issues[:10]:  # Show first 10
                rel_path = issue.file_path.relative_to(self.workspace_root)
                print(f"  {rel_path}:{issue.line_number} - {issue.old_path}")
                if verbose and issue.new_path:
                    print(f"    → {issue.new_path}")
            if len(medium_issues) > 10:
                print(f"  ... and {len(medium_issues) - 10} more")
            print()
        
        if low_issues:
            print(f"ℹ️  LOW SEVERITY ISSUES ({len(low_issues)}):")
            print(f"  {len(low_issues)} issues detected (non-critical)")
            print()
        
        # PYTHONPATH configuration
        if self.report.pythonpath_needed:
            print("🔧 PYTHONPATH CONFIGURATION:")
            print("-" * 80)
            print(self.generate_pythonpath_config())
            print()
            print("Add to your shell profile (.zshrc, .bashrc, etc.)")
            print()
        
        # Summary
        print("=" * 80)
        print("📊 SUMMARY")
        print("=" * 80)
        print(f"Total Issues: {len(self.report.issues)}")
        print(f"  High: {len(high_issues)}")
        print(f"  Medium: {len(medium_issues)}")
        print(f"  Low: {len(low_issues)}")
        print(f"Health Score: {self.report.score:.1f}%")
        if self.report.fixed_count > 0:
            print(f"Fixed: {self.report.fixed_count}")
        print()
        
        if self.report.score >= 90:
            print("✅ PATH HEALTH: EXCELLENT")
        elif self.report.score >= 70:
            print("⚠️  PATH HEALTH: GOOD (some issues detected)")
        else:
            print("❌ PATH HEALTH: NEEDS ATTENTION")
        print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Path Health & Restore")
    parser.add_argument("mode", nargs="?", default="scan", choices=["scan", "report", "fix", "pythonpath", "validate"],
                       help="Operation mode")
    parser.add_argument("--workspace-root", type=str, help="Workspace root directory")
    parser.add_argument("--severity", choices=["high", "medium", "low", "all"], default="all",
                       help="Filter by severity")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without making changes")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace_root) if args.workspace_root else None
    restorer = PathHealthRestorer(workspace_root)
    
    # Scan scripts
    report = restorer.scan_scripts()
    
    # Execute mode
    if args.mode == "scan":
        restorer.print_report(severity_filter=args.severity if args.severity != "all" else None, verbose=args.verbose)
    elif args.mode == "report":
        restorer.print_report(severity_filter=None, verbose=True)
    elif args.mode == "fix":
        severity = args.severity if args.severity != "all" else None
        fixed = restorer.fix_issues(severity_filter=severity, dry_run=args.dry_run)
        restorer.print_report(severity_filter=severity, verbose=args.verbose)
    elif args.mode == "pythonpath":
        print("\n" + "=" * 80)
        print("🔧 PYTHONPATH CONFIGURATION")
        print("=" * 80)
        print(restorer.generate_pythonpath_config())
        print()
    elif args.mode == "validate":
        restorer.scan_scripts()
        if report.score >= 90:
            print("✅ All paths validated successfully")
            sys.exit(0)
        else:
            print("❌ Path validation failed")
            sys.exit(1)
    
    # Exit with appropriate code
    sys.exit(0 if report.score >= 70 else 1)


if __name__ == "__main__":
    main()

