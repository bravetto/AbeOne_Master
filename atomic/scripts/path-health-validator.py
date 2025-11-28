#!/usr/bin/env python3
"""
Path Health Validator - Analyze and validate paths across codebase

Pattern: PATH × HEALTH × VALIDATION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (ALRAX) × 530 Hz (YAGNI)
Guardians: AEYON + ALRAX + YAGNI
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

ROOT = Path(__file__).parent.parent.parent


@dataclass
class PathIssue:
    """Path health issue"""
    file_path: str
    line_number: int
    issue_type: str  # "broken", "deprecated", "relative", "absolute"
    path: str
    severity: str  # "high", "medium", "low"
    suggestion: Optional[str] = None


class PathHealthValidator:
    """Validate path health across codebase"""
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or self._detect_workspace_root()
        self.issues: List[PathIssue] = []
        
    def _detect_workspace_root(self) -> Path:
        """Detect workspace root using git"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                cwd=ROOT
            )
            if result.returncode == 0:
                return Path(result.stdout.strip())
        except Exception:
            pass
        
        # Fallback to script location
        return ROOT
    
    def scan_scripts(self) -> List[PathIssue]:
        """Scan all scripts for path issues"""
        issues = []
        
        # Focus on atomic directory and key scripts
        scan_dirs = [
            self.workspace_root / "atomic",
            self.workspace_root / "products" / "apps" / "web",
        ]
        
        for scan_dir in scan_dirs:
            if not scan_dir.exists():
                continue
                
            # Scan Python scripts
            for py_file in scan_dir.rglob("*.py"):
                if any(skip in str(py_file) for skip in ["node_modules", ".git", "__pycache__", ".venv"]):
                    continue
                try:
                    issues.extend(self._scan_file(py_file))
                except Exception:
                    continue
            
            # Scan shell scripts
            for sh_file in scan_dir.rglob("*.sh"):
                if any(skip in str(sh_file) for skip in ["node_modules", ".git"]):
                    continue
                try:
                    issues.extend(self._scan_file(sh_file))
                except Exception:
                    continue
            
            # Scan JavaScript/TypeScript
            for js_file in scan_dir.rglob("*.{js,jsx,ts,tsx}"):
                if any(skip in str(js_file) for skip in ["node_modules", ".git", ".next", "dist"]):
                    continue
                try:
                    issues.extend(self._scan_file(js_file))
                except Exception:
                    continue
        
        self.issues = issues
        return issues
    
    def _scan_file(self, file_path: Path) -> List[PathIssue]:
        """Scan a single file for path issues"""
        issues = []
        
        try:
            content = file_path.read_text()
            lines = content.split("\n")
            
            # Patterns to check
            patterns = [
                (r'["\']([^"\']*EMERGENT_OS[^"\']*)["\']', "deprecated"),
                (r'["\']([^"\']*\.\.\/\.\.\/[^"\']*)["\']', "relative"),
                (r'["\'](/[^"\']*)["\']', "absolute"),
                (r'Path\(["\']([^"\']+)["\']\)', "path_constructor"),
                (r'import.*from\s+["\']([^"\']+)["\']', "import"),
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern, issue_type in patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        path_str = match.group(1)
                        
                        # Skip if it's a URL or special path
                        if any(skip in path_str for skip in ["http://", "https://", "npm:", "node:", "@"]):
                            continue
                        
                        # Check if path exists
                        if issue_type == "deprecated":
                            issues.append(PathIssue(
                                file_path=str(file_path.relative_to(self.workspace_root)),
                                line_number=line_num,
                                issue_type=issue_type,
                                path=path_str,
                                severity="high",
                                suggestion=f"Update to use orbital path: {self._suggest_new_path(path_str)}"
                            ))
                        elif issue_type == "relative":
                            # Validate relative path
                            resolved = (file_path.parent / path_str).resolve()
                            if not resolved.exists():
                                issues.append(PathIssue(
                                    file_path=str(file_path.relative_to(self.workspace_root)),
                                    line_number=line_num,
                                    issue_type="broken",
                                    path=path_str,
                                    severity="high",
                                    suggestion="Path does not exist"
                                ))
                        elif issue_type == "absolute":
                            # Check if absolute path is within workspace
                            abs_path = Path(path_str)
                            try:
                                abs_path.resolve()
                                if not str(abs_path.resolve()).startswith(str(self.workspace_root.resolve())):
                                    issues.append(PathIssue(
                                        file_path=str(file_path.relative_to(self.workspace_root)),
                                        line_number=line_num,
                                        issue_type="absolute",
                                        path=path_str,
                                        severity="medium",
                                        suggestion="Use relative path instead"
                                    ))
                            except Exception:
                                pass
        
        except Exception as e:
            # Skip files that can't be read
            pass
        
        return issues
    
    def _suggest_new_path(self, old_path: str) -> str:
        """Suggest new path for deprecated paths"""
        # Map old paths to new paths
        if "EMERGENT_OS" in old_path:
            return old_path.replace("EMERGENT_OS", "orbital/EMERGENT_OS-orbital")
        return old_path
    
    def validate_paths(self) -> Dict:
        """Validate all paths and generate report"""
        issues = self.scan_scripts()
        
        # Group by severity
        high_severity = [i for i in issues if i.severity == "high"]
        medium_severity = [i for i in issues if i.severity == "medium"]
        low_severity = [i for i in issues if i.severity == "low"]
        
        # Calculate health score
        total_files_scanned = len(set(i.file_path for i in issues))
        total_issues = len(issues)
        health_score = max(0, 100 - (total_issues * 2))  # Simple scoring
        
        return {
            "status": "complete",
            "pattern": "PATH × HEALTH × VALIDATION × ONE",
            "workspace_root": str(self.workspace_root),
            "metrics": {
                "total_issues": total_issues,
                "high_severity": len(high_severity),
                "medium_severity": len(medium_severity),
                "low_severity": len(low_severity),
                "health_score": health_score,
                "files_scanned": total_files_scanned
            },
            "issues": {
                "high": [asdict(i) for i in high_severity],
                "medium": [asdict(i) for i in medium_severity],
                "low": [asdict(i) for i in low_severity]
            },
            "guardian_signatures": {
                "AEYON": "999 Hz - Path health validated atomically",
                "ALRAX": "530 Hz - Path issues identified forensically",
                "YAGNI": "530 Hz - Only necessary paths validated"
            }
        }


def main():
    """Main execution"""
    import sys
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "scan"
    
    print(" Path Health Validator")
    print("Pattern: PATH × HEALTH × VALIDATION × ONE")
    print("∞ AbëONE ∞\n")
    
    validator = PathHealthValidator()
    
    if mode == "scan" or mode == "report":
        report = validator.validate_paths()
        
        print(" Path Health Report:")
        print(f"  Workspace Root: {report['workspace_root']}")
        print(f"  Files Scanned: {report['metrics']['files_scanned']}")
        print(f"  Total Issues: {report['metrics']['total_issues']}")
        print(f"  High Severity: {report['metrics']['high_severity']}")
        print(f"  Medium Severity: {report['metrics']['medium_severity']}")
        print(f"  Low Severity: {report['metrics']['low_severity']}")
        print(f"  Health Score: {report['metrics']['health_score']}%")
        
        if report['metrics']['high_severity'] > 0:
            print(f"\n  High Severity Issues:")
            for issue in report['issues']['high'][:10]:  # Show first 10
                print(f"    {issue['file_path']}:{issue['line_number']} - {issue['issue_type']}")
                print(f"      Path: {issue['path']}")
                if issue['suggestion']:
                    print(f"      Suggestion: {issue['suggestion']}")
        
        # Save report
        report_path = ROOT / "atomic" / "PATH_HEALTH_REPORT.json"
        import json
        report_path.write_text(json.dumps(report, indent=2))
        print(f"\n Report saved to {report_path}")
        
    elif mode == "pythonpath":
        print(" PYTHONPATH Configuration:")
        pythonpath = os.environ.get("PYTHONPATH", "Not set")
        print(f"  PYTHONPATH: {pythonpath}")
        print(f"  Workspace Root: {validator.workspace_root}")
        print(f"  Recommended: export PYTHONPATH={validator.workspace_root}")
    
    print("\n Path health validation complete!")
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    main()

