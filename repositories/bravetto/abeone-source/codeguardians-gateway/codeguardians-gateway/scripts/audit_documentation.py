"""
Documentation Audit Script for AI Guardians

This script audits all documentation for accuracy, completeness, and consistency.
It checks for outdated references, broken links, and missing information.
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class DocumentationIssue:
    """Represents a documentation issue."""
    file_path: str
    line_number: int
    issue_type: str
    description: str
    severity: str  # "high", "medium", "low"
    suggested_fix: str = ""

@dataclass
class CodeReference:
    """Represents a code reference in documentation."""
    file_path: str
    line_number: int
    reference: str
    context: str

class DocumentationAuditor:
    """Audits documentation for issues and inconsistencies."""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.issues: List[DocumentationIssue] = []
        self.code_references: List[CodeReference] = []
        self.api_endpoints: Set[str] = set()
        self.service_names: Set[str] = set()
        self.file_references: Set[str] = set()
        
    def audit_all(self) -> Dict[str, Any]:
        """Run comprehensive documentation audit."""
        logger.info("Starting documentation audit...")
        
        # Find all documentation files
        doc_files = self._find_documentation_files()
        logger.info(f"Found {len(doc_files)} documentation files")
        
        # Find all code files
        code_files = self._find_code_files()
        logger.info(f"Found {len(code_files)} code files")
        
        # Extract API endpoints from code
        self._extract_api_endpoints(code_files)
        
        # Extract service names from code
        self._extract_service_names(code_files)
        
        # Audit each documentation file
        for doc_file in doc_files:
            self._audit_documentation_file(doc_file)
        
        # Check for orphaned files
        self._check_orphaned_files()
        
        # Check for missing documentation
        self._check_missing_documentation(code_files)
        
        # Generate report
        return self._generate_audit_report()
    
    def _find_documentation_files(self) -> List[Path]:
        """Find all documentation files."""
        doc_extensions = {'.md', '.rst', '.txt', '.yml', '.yaml', '.json'}
        doc_files = []
        
        for ext in doc_extensions:
            doc_files.extend(self.root_path.rglob(f"*{ext}"))
        
        # Filter out certain directories
        filtered_files = []
        for file_path in doc_files:
            if any(part.startswith('.') for part in file_path.parts):
                continue
            if 'node_modules' in str(file_path):
                continue
            if '__pycache__' in str(file_path):
                continue
            filtered_files.append(file_path)
        
        return filtered_files
    
    def _find_code_files(self) -> List[Path]:
        """Find all code files."""
        code_extensions = {'.py', '.ts', '.js', '.json', '.yaml', '.yml'}
        code_files = []
        
        for ext in code_extensions:
            code_files.extend(self.root_path.rglob(f"*{ext}"))
        
        # Filter out certain directories
        filtered_files = []
        for file_path in code_files:
            if any(part.startswith('.') for part in file_path.parts):
                continue
            if 'node_modules' in str(file_path):
                continue
            if '__pycache__' in str(file_path):
                continue
            if 'test' in str(file_path).lower() and file_path.suffix == '.py':
                continue  # Skip test files for now
            filtered_files.append(file_path)
        
        return filtered_files
    
    def _extract_api_endpoints(self, code_files: List[Path]) -> None:
        """Extract API endpoints from code files."""
        endpoint_patterns = [
            r'@router\.(get|post|put|delete)\("([^"]+)"',
            r'@app\.(get|post|put|delete)\("([^"]+)"',
            r'router\.(get|post|put|delete)\("([^"]+)"',
            r'app\.(get|post|put|delete)\("([^"]+)"',
        ]
        
        for file_path in code_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern in endpoint_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        self.api_endpoints.add(match[1])
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
    
    def _extract_service_names(self, code_files: List[Path]) -> None:
        """Extract service names from code files."""
        service_patterns = [
            r'GuardServiceType\.(\w+)',
            r'"(\w+guard)"',
            r'service_type.*=.*"(\w+)"',
        ]
        
        for file_path in code_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern in service_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        self.service_names.add(match.lower())
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
    
    def _audit_documentation_file(self, file_path: Path) -> None:
        """Audit a single documentation file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            self.issues.append(DocumentationIssue(
                file_path=str(file_path),
                line_number=0,
                issue_type="file_read_error",
                description=f"Could not read file: {e}",
                severity="high"
            ))
            return
        
        # Check for TODO/FIXME comments
        self._check_todo_comments(file_path, lines)
        
        # Check for broken links
        self._check_broken_links(file_path, lines)
        
        # Check for outdated references
        self._check_outdated_references(file_path, lines)
        
        # Check for missing API documentation
        self._check_api_documentation(file_path, lines)
        
        # Check for inconsistent service names
        self._check_service_names(file_path, lines)
        
        # Check for code references
        self._check_code_references(file_path, lines)
    
    def _check_todo_comments(self, file_path: Path, lines: List[str]) -> None:
        """Check for TODO/FIXME comments in documentation."""
        for i, line in enumerate(lines, 1):
            if 'TODO' in line.upper() or 'FIXME' in line.upper():
                self.issues.append(DocumentationIssue(
                    file_path=str(file_path),
                    line_number=i,
                    issue_type="todo_comment",
                    description=f"TODO/FIXME comment found: {line.strip()}",
                    severity="medium",
                    suggested_fix="Complete the TODO item or remove the comment"
                ))
    
    def _check_broken_links(self, file_path: Path, lines: List[str]) -> None:
        """Check for broken links in documentation."""
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        for i, line in enumerate(lines, 1):
            matches = re.findall(link_pattern, line)
            for text, url in matches:
                if url.startswith('http'):
                    # External link - could check if it's accessible
                    continue
                elif url.startswith('#'):
                    # Anchor link - check if anchor exists
                    anchor = url[1:]
                    if not any(anchor in l for l in lines):
                        self.issues.append(DocumentationIssue(
                            file_path=str(file_path),
                            line_number=i,
                            issue_type="broken_anchor_link",
                            description=f"Broken anchor link: {url}",
                            severity="medium",
                            suggested_fix=f"Add anchor '{anchor}' or fix the link"
                        ))
                else:
                    # File link - check if file exists
                    target_path = file_path.parent / url
                    if not target_path.exists():
                        self.issues.append(DocumentationIssue(
                            file_path=str(file_path),
                            line_number=i,
                            issue_type="broken_file_link",
                            description=f"Broken file link: {url}",
                            severity="high",
                            suggested_fix=f"Fix the file path or create the missing file"
                        ))
    
    def _check_outdated_references(self, file_path: Path, lines: List[str]) -> None:
        """Check for outdated references in documentation."""
        outdated_patterns = [
            (r'securityguard', "SecurityGuard has been removed"),
            (r'healthguard.*mock', "HealthGuard mock has been replaced with real implementation"),
            (r'localhost:800[5-9]', "Port numbers may be outdated"),
            (r'v0\.\d+', "Version numbers may be outdated"),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, message in outdated_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(DocumentationIssue(
                        file_path=str(file_path),
                        line_number=i,
                        issue_type="outdated_reference",
                        description=f"Potentially outdated reference: {message}",
                        severity="medium",
                        suggested_fix="Update the reference to current implementation"
                    ))
    
    def _check_api_documentation(self, file_path: Path, lines: List[str]) -> None:
        """Check if API endpoints are properly documented."""
        if 'api' in str(file_path).lower() or 'endpoint' in str(file_path).lower():
            content = '\n'.join(lines)
            
            for endpoint in self.api_endpoints:
                if endpoint not in content:
                    self.issues.append(DocumentationIssue(
                        file_path=str(file_path),
                        line_number=0,
                        issue_type="missing_api_documentation",
                        description=f"API endpoint '{endpoint}' not documented",
                        severity="medium",
                        suggested_fix=f"Add documentation for endpoint '{endpoint}'"
                    ))
    
    def _check_service_names(self, file_path: Path, lines: List[str]) -> None:
        """Check for inconsistent service names."""
        content = '\n'.join(lines)
        
        # Check for old service names
        old_services = ['securityguard', 'healthguard_mock']
        for old_service in old_services:
            if old_service in content.lower():
                self.issues.append(DocumentationIssue(
                    file_path=str(file_path),
                    line_number=0,
                    issue_type="outdated_service_name",
                    description=f"References to old service '{old_service}' found",
                    severity="high",
                    suggested_fix=f"Update references to current service names"
                ))
    
    def _check_code_references(self, file_path: Path, lines: List[str]) -> None:
        """Check for code references in documentation."""
        code_pattern = r'`([^`]+)`'
        
        for i, line in enumerate(lines, 1):
            matches = re.findall(code_pattern, line)
            for match in matches:
                if '.' in match and not match.startswith('http'):
                    # Potential code reference
                    self.code_references.append(CodeReference(
                        file_path=str(file_path),
                        line_number=i,
                        reference=match,
                        context=line.strip()
                    ))
    
    def _check_orphaned_files(self) -> None:
        """Check for orphaned files."""
        # This would require more complex analysis
        # For now, just check for files that might be orphaned
        pass
    
    def _check_missing_documentation(self, code_files: List[Path]) -> None:
        """Check for missing documentation."""
        # Check if main modules have documentation
        main_modules = ['app/main.py', 'app/core/guard_orchestrator.py']
        
        for module in main_modules:
            module_path = self.root_path / module
            if module_path.exists():
                # Check if there's corresponding documentation
                doc_paths = [
                    self.root_path / f"docs/{module.replace('/', '_')}.md",
                    self.root_path / f"docs/{module.replace('/', '/')}.md",
                ]
                
                if not any(p.exists() for p in doc_paths):
                    self.issues.append(DocumentationIssue(
                        file_path=str(module_path),
                        line_number=0,
                        issue_type="missing_documentation",
                        description=f"Module {module} lacks documentation",
                        severity="medium",
                        suggested_fix=f"Create documentation for {module}"
                    ))
    
    def _generate_audit_report(self) -> Dict[str, Any]:
        """Generate comprehensive audit report."""
        # Categorize issues by severity
        high_issues = [i for i in self.issues if i.severity == "high"]
        medium_issues = [i for i in self.issues if i.severity == "medium"]
        low_issues = [i for i in self.issues if i.severity == "low"]
        
        # Categorize issues by type
        issue_types = {}
        for issue in self.issues:
            if issue.issue_type not in issue_types:
                issue_types[issue.issue_type] = 0
            issue_types[issue.issue_type] += 1
        
        # Generate summary
        summary = {
            "total_issues": len(self.issues),
            "high_severity": len(high_issues),
            "medium_severity": len(medium_issues),
            "low_severity": len(low_issues),
            "issue_types": issue_types,
            "api_endpoints_found": len(self.api_endpoints),
            "service_names_found": len(self.service_names),
            "code_references_found": len(self.code_references)
        }
        
        return {
            "summary": summary,
            "issues": [
                {
                    "file": issue.file_path,
                    "line": issue.line_number,
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "description": issue.description,
                    "suggested_fix": issue.suggested_fix
                }
                for issue in self.issues
            ],
            "api_endpoints": list(self.api_endpoints),
            "service_names": list(self.service_names),
            "code_references": [
                {
                    "file": ref.file_path,
                    "line": ref.line_number,
                    "reference": ref.reference,
                    "context": ref.context
                }
                for ref in self.code_references
            ]
        }


def main():
    """Run documentation audit."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Audit AI Guardians documentation")
    parser.add_argument("--path", default=".", help="Root path to audit")
    parser.add_argument("--output", default="documentation_audit.json", help="Output file")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    auditor = DocumentationAuditor(args.path)
    results = auditor.audit_all()
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    summary = results["summary"]
    print(f"\nDocumentation Audit Complete!")
    print(f"Total Issues: {summary['total_issues']}")
    print(f"High Severity: {summary['high_severity']}")
    print(f"Medium Severity: {summary['medium_severity']}")
    print(f"Low Severity: {summary['low_severity']}")
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()

