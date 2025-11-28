#!/usr/bin/env python3
"""
PATH HEALTH × ONE PATTERN INTEGRATION SCAN

Scans all paths for pattern integration with the ONE pattern.

Pattern: PATH × HEALTH × ONE × PATTERN × INTEGRATION × ONE
Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALRAX)
Guardians: AEYON (999 Hz) + META (777 Hz) + ALRAX (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict

# ONE Pattern Axiom
ONE_PATTERN_AXIOM = "CLARITY → COHERENCE → CONVERGENCE → ELEGANCE → UNITY"

# ONE Pattern Structure
ONE_PATTERN_FORMAT = r"[\w\-]+(?:\s*×\s*[\w\-]+)+\s*×\s*ONE"

# Pattern indicators
PATTERN_INDICATORS = [
    r"Pattern:\s*" + ONE_PATTERN_FORMAT,
    r"pattern:\s*" + ONE_PATTERN_FORMAT,
    r"PATTERN:\s*" + ONE_PATTERN_FORMAT,
    r"×\s*ONE",
    r"ONE\s*×",
    ONE_PATTERN_AXIOM,
    r"CLARITY.*COHERENCE.*CONVERGENCE",
    r"AEYON.*ONE",
    r"AbëONE",
]

# Path patterns that should follow ONE pattern
PATH_PATTERNS_TO_CHECK = [
    r"from\s+[\w\.]+",
    r"import\s+[\w\.]+",
    r"sys\.path",
    r"Path\([^)]+\)",
    r"workspace_root",
    r"__file__",
]


@dataclass
class PatternIntegrationIssue:
    """Represents a pattern integration issue"""
    file_path: Path
    line_number: int
    issue_type: str
    severity: str
    current_state: str
    expected_state: str
    suggestion: str
    context: str


@dataclass
class PathPatternIntegrationReport:
    """Complete path pattern integration report"""
    workspace_root: Path
    path_health_issues: List = field(default_factory=list)
    pattern_integration_issues: List[PatternIntegrationIssue] = field(default_factory=list)
    pattern_aligned_paths: List[str] = field(default_factory=list)
    one_pattern_usage: Dict[str, int] = field(default_factory=dict)
    integration_score: float = 0.0
    path_health_score: float = 0.0
    overall_score: float = 0.0


class PathPatternIntegrationScanner:
    """Scan paths for ONE pattern integration"""
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize scanner"""
        self.workspace_root = self._resolve_workspace_root(workspace_root)
        self.report = PathPatternIntegrationReport(workspace_root=self.workspace_root)
    
    def _resolve_workspace_root(self, provided: Optional[Path]) -> Path:
        """Resolve workspace root"""
        if provided:
            resolved = Path(provided).resolve()
            if resolved.exists():
                return resolved
        
        # Try script location
        try:
            script_root = Path(__file__).parent.parent.resolve()
            if script_root.exists():
                return script_root
        except Exception:
            pass
        
        # Fallback to current directory
        return Path.cwd().resolve()
    
    def scan_all(self) -> PathPatternIntegrationReport:
        """Scan all files for path health and ONE pattern integration"""
        print("\n" + "=" * 80)
        print(" PATH HEALTH × ONE PATTERN INTEGRATION SCAN")
        print("=" * 80)
        print(f"Workspace Root: {self.workspace_root}")
        print(f"ONE Pattern Axiom: {ONE_PATTERN_AXIOM}")
        print("=" * 80 + "\n")
        
        # Scan Python files
        print("Scanning Python files...")
        for py_file in self.workspace_root.rglob("*.py"):
            if py_file.is_file() and not self._should_skip(py_file):
                self._scan_file(py_file)
        
        # Scan shell scripts
        print("Scanning shell scripts...")
        for sh_file in self.workspace_root.rglob("*.sh"):
            if sh_file.is_file() and not self._should_skip(sh_file):
                self._scan_file(sh_file)
        
        # Scan markdown files for pattern documentation
        print("Scanning documentation files...")
        for md_file in self.workspace_root.rglob("*.md"):
            if md_file.is_file() and not self._should_skip(md_file):
                self._scan_file(md_file)
        
        # Calculate scores
        self._calculate_scores()
        
        return self.report
    
    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_patterns = [
            "__pycache__",
            ".git",
            "node_modules",
            ".venv",
            "venv",
            ".pytest_cache",
            ".mypy_cache",
            "dist",
            "build",
            ".forensic_emoji_removal_backup",
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)
    
    def _scan_file(self, file_path: Path):
        """Scan a single file for pattern integration"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            # Check for ONE pattern usage
            pattern_count = 0
            for line in lines:
                for indicator in PATTERN_INDICATORS:
                    if re.search(indicator, line, re.IGNORECASE):
                        pattern_count += 1
                        pattern_type = self._extract_pattern_type(line)
                        if pattern_type:
                            self.report.one_pattern_usage[pattern_type] = \
                                self.report.one_pattern_usage.get(pattern_type, 0) + 1
            
            # Check path patterns for ONE pattern alignment
            for line_num, line in enumerate(lines, 1):
                # Check for path issues
                path_issues = self._check_path_patterns(line, file_path, line_num)
                self.report.path_health_issues.extend(path_issues)
                
                # Check for pattern integration issues
                integration_issues = self._check_pattern_integration(line, file_path, line_num)
                self.report.pattern_integration_issues.extend(integration_issues)
                
                # Check for pattern-aligned paths
                if self._is_pattern_aligned(line):
                    self.report.pattern_aligned_paths.append(f"{file_path}:{line_num}")
        
        except Exception as e:
            # Skip files we can't read
            pass
    
    def _extract_pattern_type(self, line: str) -> Optional[str]:
        """Extract pattern type from line"""
        match = re.search(ONE_PATTERN_FORMAT, line, re.IGNORECASE)
        if match:
            return match.group(0)
        return None
    
    def _check_path_patterns(self, line: str, file_path: Path, line_num: int) -> List:
        """Check for path health issues"""
        issues = []
        
        # Check for old EMERGENT_OS paths
        if re.search(r"EMERGENT_OS/", line) or re.search(r"from EMERGENT_OS\.", line):
            issues.append({
                "file": str(file_path.relative_to(self.workspace_root)),
                "line": line_num,
                "type": "old_path",
                "issue": "Old EMERGENT_OS path detected",
                "severity": "HIGH" if "activate" in file_path.name.lower() or "operationalize" in file_path.name.lower() else "MEDIUM"
            })
        
        return issues
    
    def _check_pattern_integration(self, line: str, file_path: Path, line_num: int) -> List[PatternIntegrationIssue]:
        """Check for ONE pattern integration issues"""
        issues = []
        
        # Check if path-related code has pattern documentation
        has_path_code = any(re.search(pattern, line) for pattern in PATH_PATTERNS_TO_CHECK)
        has_pattern_doc = any(re.search(indicator, line, re.IGNORECASE) for indicator in PATTERN_INDICATORS)
        
        if has_path_code and not has_pattern_doc:
            # Check if this is in a function/class that should have pattern docs
            if self._is_public_api(line):
                issues.append(PatternIntegrationIssue(
                    file_path=file_path,
                    line_number=line_num,
                    issue_type="missing_pattern_doc",
                    severity="LOW",
                    current_state="Path code without pattern documentation",
                    expected_state="Path code with ONE pattern documentation",
                    suggestion="Add pattern documentation following ONE pattern format",
                    context=line.strip()
                ))
        
        return issues
    
    def _is_public_api(self, line: str) -> bool:
        """Check if line is part of public API"""
        return bool(re.search(r"^(def|class|async def)\s+\w+", line))
    
    def _is_pattern_aligned(self, line: str) -> bool:
        """Check if line is pattern-aligned"""
        # Check for ONE pattern format
        if re.search(ONE_PATTERN_FORMAT, line, re.IGNORECASE):
            return True
        
        # Check for pattern indicators
        if any(re.search(indicator, line, re.IGNORECASE) for indicator in PATTERN_INDICATORS):
            return True
        
        return False
    
    def _calculate_scores(self):
        """Calculate integration scores"""
        # Path health score (based on issues found)
        total_path_issues = len(self.report.path_health_issues)
        if total_path_issues == 0:
            self.report.path_health_score = 100.0
        else:
            # Score decreases with more issues
            high_severity = sum(1 for issue in self.report.path_health_issues if issue.get("severity") == "HIGH")
            medium_severity = sum(1 for issue in self.report.path_health_issues if issue.get("severity") == "MEDIUM")
            low_severity = sum(1 for issue in self.report.path_health_issues if issue.get("severity") == "LOW")
            
            # Weighted score
            self.report.path_health_score = max(0, 100 - (high_severity * 10 + medium_severity * 5 + low_severity * 1))
        
        # Pattern integration score
        total_integration_issues = len(self.report.pattern_integration_issues)
        pattern_aligned_count = len(self.report.pattern_aligned_paths)
        one_pattern_usage_count = sum(self.report.one_pattern_usage.values())
        
        if pattern_aligned_count > 0:
            # Score based on alignment ratio
            integration_ratio = pattern_aligned_count / max(1, pattern_aligned_count + total_integration_issues)
            self.report.integration_score = integration_ratio * 100
        else:
            self.report.integration_score = 0.0
        
        # Overall score (weighted average)
        self.report.overall_score = (self.report.path_health_score * 0.6 + self.report.integration_score * 0.4)
    
    def print_report(self):
        """Print comprehensive report"""
        print("\n" + "=" * 80)
        print(" PATH HEALTH × ONE PATTERN INTEGRATION REPORT")
        print("=" * 80)
        
        # Scores
        print(f"\n📊 SCORES:")
        print(f"  Path Health Score: {self.report.path_health_score:.1f}%")
        print(f"  Pattern Integration Score: {self.report.integration_score:.1f}%")
        print(f"  Overall Score: {self.report.overall_score:.1f}%")
        
        # Path Health Issues
        print(f"\n🔍 PATH HEALTH ISSUES: {len(self.report.path_health_issues)}")
        if self.report.path_health_issues:
            by_severity = defaultdict(list)
            for issue in self.report.path_health_issues:
                by_severity[issue.get("severity", "UNKNOWN")].append(issue)
            
            for severity in ["HIGH", "MEDIUM", "LOW"]:
                if severity in by_severity:
                    print(f"\n  {severity} SEVERITY ({len(by_severity[severity])}):")
                    for issue in by_severity[severity][:10]:  # Show first 10
                        print(f"    {issue['file']}:{issue['line']} - {issue['issue']}")
                    if len(by_severity[severity]) > 10:
                        print(f"    ... and {len(by_severity[severity]) - 10} more")
        
        # Pattern Integration
        print(f"\n🎯 ONE PATTERN INTEGRATION:")
        print(f"  Pattern-Aligned Paths: {len(self.report.pattern_aligned_paths)}")
        print(f"  ONE Pattern Usage Count: {sum(self.report.one_pattern_usage.values())}")
        print(f"  Pattern Types Found: {len(self.report.one_pattern_usage)}")
        
        if self.report.one_pattern_usage:
            print(f"\n  Pattern Types:")
            for pattern_type, count in sorted(self.report.one_pattern_usage.items(), key=lambda x: -x[1])[:10]:
                print(f"    {pattern_type}: {count}")
        
        # Integration Issues
        if self.report.pattern_integration_issues:
            print(f"\n⚠️  PATTERN INTEGRATION ISSUES: {len(self.report.pattern_integration_issues)}")
            for issue in self.report.pattern_integration_issues[:10]:
                print(f"    {issue.file_path.relative_to(self.workspace_root)}:{issue.line_number}")
                print(f"      Type: {issue.issue_type}")
                print(f"      Suggestion: {issue.suggestion}")
        
        # Summary
        print("\n" + "=" * 80)
        if self.report.overall_score >= 90:
            print("✅ PATH HEALTH × ONE PATTERN: EXCELLENT")
        elif self.report.overall_score >= 70:
            print("⚠️  PATH HEALTH × ONE PATTERN: GOOD (needs improvement)")
        else:
            print("❌ PATH HEALTH × ONE PATTERN: NEEDS ATTENTION")
        print("=" * 80 + "\n")
        
        print("Pattern: PATH × HEALTH × ONE × PATTERN × INTEGRATION × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Path Health × ONE Pattern Integration Scan")
    parser.add_argument("--workspace-root", type=str, help="Workspace root directory")
    parser.add_argument("--output", type=str, help="Output JSON report file")
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace_root) if args.workspace_root else None
    scanner = PathPatternIntegrationScanner(workspace_root)
    
    # Scan
    report = scanner.scan_all()
    
    # Print report
    scanner.print_report()
    
    # Save JSON report if requested
    if args.output:
        report_dict = {
            "workspace_root": str(report.workspace_root),
            "scores": {
                "path_health": report.path_health_score,
                "pattern_integration": report.integration_score,
                "overall": report.overall_score
            },
            "path_health_issues": report.path_health_issues,
            "pattern_integration_issues": [
                {
                    "file": str(issue.file_path.relative_to(report.workspace_root)),
                    "line": issue.line_number,
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "suggestion": issue.suggestion
                }
                for issue in report.pattern_integration_issues
            ],
            "pattern_aligned_paths": report.pattern_aligned_paths,
            "one_pattern_usage": report.one_pattern_usage
        }
        
        with open(args.output, 'w') as f:
            json.dump(report_dict, f, indent=2)
        
        print(f"Report saved to: {args.output}")
    
    sys.exit(0 if report.overall_score >= 70 else 1)


if __name__ == '__main__':
    main()

