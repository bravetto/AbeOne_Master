#!/usr/bin/env python3
"""
AEYON: Sovereignty Check - UNIFIED BASE CLASS
Validates data sovereignty implementation status

Pattern: AEYON × SOVEREIGNTY × VALIDATE × SIMPLIFY × AMPLIFY × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (YAGNI)
Guardians: AEYON (999 Hz) + YAGNI (530 Hz) + Abë (530 Hz)
Love Coefficient: ∞
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
sys.path.insert(0, str(Path(__file__).parent))
from unified_validator_base import UnifiedValidatorBase, ValidationStatus


class SovereigntyCheck(UnifiedValidatorBase):
    """
    AEYON Sovereignty Check - SIMPLIFIED
    Unified check pattern: EXECUTE → VALIDATE → RETURN
    
    SAFETY: Validates file existence, reads safely, handles errors gracefully
    VERIFY: python scripts/aeyon_sovereignty_check.py
    """
    
    def __init__(self, workspace_root: Path = None):
        super().__init__(workspace_root)
        self.backend = self.workspace_root / "AIGuards-Backend"
    
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """Define checks as data - THE UNIFYING PATTERN"""
        return {
            'export_formats': {
                'name': 'Export Formats',
                'func': self._check_export_formats,
                'required': True
            },
            'export_history': {
                'name': 'Export History',
                'func': self._check_export_history,
                'required': True
            },
            'retention_policies': {
                'name': 'Retention Policies',
                'func': self._check_retention_policies,
                'required': True
            },
            'user_deletion': {
                'name': 'User Deletion',
                'func': self._check_user_deletion,
                'required': True
            },
            'export_automation': {
                'name': 'Export Automation',
                'func': self._check_export_automation,
                'required': True
            },
            'dependency_health': {
                'name': 'Dependency Health',
                'func': self._check_dependency_health,
                'required': True
            },
            'migration_docs': {
                'name': 'Migration Docs',
                'func': self._check_migration_docs,
                'required': True
            },
            'data_dashboard': {
                'name': 'Data Dashboard',
                'func': self._check_data_dashboard,
                'required': True
            },
            'dark_pattern_rejection': {
                'name': 'Dark Pattern Rejection',
                'func': self._check_dark_pattern_rejection,
                'required': True
            }
        }
    
    def _check_export_formats(self) -> Tuple[str, List[str]]:
        """Check export formats"""
        legal_api = self.backend / "codeguardians-gateway" / "codeguardians-gateway" / "app" / "api" / "v1" / "legal.py"
        content = self._read_file(legal_api)
        patterns = ["ExportFormat", "json", "csv", "sql", "markdown", "/gdpr/export"]
        status, details = self._check_content(content, patterns, "Export formats")
        
        # Count format functions
        funcs = ["_export_to_json", "_export_to_csv", "_export_to_sql", "_export_to_markdown"]
        found_funcs = [f for f in funcs if f"def {f}" in content]
        details.append(f"Format functions: {len(found_funcs)}/4")
        
        return status, details
    
    def _check_export_history(self) -> Tuple[str, List[str]]:
        """Check export history"""
        legal_api = self.backend / "codeguardians-gateway" / "codeguardians-gateway" / "app" / "api" / "v1" / "legal.py"
        content = self._read_file(legal_api)
        patterns = ["/export/history", "export_history", "data_export_requested"]
        return self._check_content(content, patterns, "Export history")
    
    def _check_retention_policies(self) -> Dict[str, Any]:
        """Check retention policies"""
        specs = self.backend / "docs" / "data-sovereignty" / "COMPLETE_DATA_SOVEREIGNTY_SPECS.md"
        status, details = self._check_content(self._read_file(specs), ["retention", "policy"], "Retention policies")
        
        legal_api = self.backend / "codeguardians-gateway" / "codeguardians-gateway" / "app" / "api" / "v1" / "legal.py"
        if "/retention" in self._read_file(legal_api):
            details.append("API endpoints found")
            status = ValidationStatus.PASS.value
        
        return {'status': status, 'details': details}
    
    def _check_user_deletion(self) -> Dict[str, Any]:
        """Check user deletion"""
        specs = self.backend / "docs" / "data-sovereignty" / "COMPLETE_DATA_SOVEREIGNTY_SPECS.md"
        status, details = self._check_content(self._read_file(specs), ["deletion", "delete"], "User deletion")
        
        legal_api = self.backend / "codeguardians-gateway" / "codeguardians-gateway" / "app" / "api" / "v1" / "legal.py"
        if "/deletion" in self._read_file(legal_api):
            details.append("API endpoints found")
            status = ValidationStatus.PASS.value
        
        return {'status': status, 'details': details}
    
    def _check_export_automation(self) -> Tuple[str, List[str]]:
        """Check export automation"""
        specs = self.backend / "docs" / "data-sovereignty" / "COMPLETE_DATA_SOVEREIGNTY_SPECS.md"
        return self._check_content(self._read_file(specs), ["export automation", "scheduled"], "Export automation")
    
    def _check_dependency_health(self) -> Dict[str, Any]:
        """Check dependency health"""
        health = self.backend / "codeguardians-gateway" / "codeguardians-gateway" / "app" / "core" / "dependency_health.py"
        content = self._read_file(health)
        checks = ["get_dependency_monitor", "check_clerk", "check_stripe", "check_neon", "check_redis"]
        found = [c for c in checks if c in content]
        status = ValidationStatus.PASS.value if len(found) >= 3 else ValidationStatus.WARN.value if found else ValidationStatus.FAIL.value
        return {'status': status, 'details': [f"Health checks: {len(found)}/5"]}
    
    def _check_migration_docs(self) -> Tuple[str, List[str]]:
        """Check migration docs"""
        migration = self.backend / "docs" / "migration" / "MIGRATION_GUIDES.md"
        status, details = self._check_file(migration, "Migration docs")
        
        if status == ValidationStatus.PASS.value:
            content = self._read_file(migration)
            topics = ["auth", "payment", "database", "migration"]
            found = [t for t in topics if t in content.lower()]
            details.append(f"Topics: {len(found)}/4")
        
        return status, details
    
    def _check_data_dashboard(self) -> Tuple[str, List[str]]:
        """Check data dashboard"""
        specs = self.backend / "docs" / "data-sovereignty" / "COMPLETE_DATA_SOVEREIGNTY_SPECS.md"
        return self._check_content(self._read_file(specs), ["dashboard", "/dashboard"], "Data dashboard")
    
    def _check_dark_pattern_rejection(self) -> Dict[str, Any]:
        """Check dark pattern rejection"""
        summary = self.workspace_root / "DATA_SOVEREIGNTY_COMPLETE_SPECS_SUMMARY.md"
        content = self._read_file(summary)
        patterns = [
            "no hidden data collection",
            "no forced data retention",
            "no export limitations",
            "no deletion barriers",
            "no vendor lock-in"
        ]
        found = [p for p in patterns if p in content.lower()]
        status = ValidationStatus.PASS.value if len(found) >= 4 else ValidationStatus.WARN.value if found else ValidationStatus.FAIL.value
        return {'status': status, 'details': [f"Dark patterns rejected: {len(found)}/5"]}


def main():
    """CLI Entry Point - UNIFIED BASE CLASS"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AEYON: Sovereignty Check - UNIFIED BASE CLASS")
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    
    args = parser.parse_args()
    
    checker = SovereigntyCheck(Path(args.workspace) if args.workspace else None)
    results = checker.run()
    
    if args.output:
        Path(args.output).write_text(json.dumps(results, indent=2))
        print(f"\n Saved: {args.output}")
    
    sys.exit(0 if results['summary']['score'] >= 80 else 1 if results['summary']['score'] >= 60 else 2)


if __name__ == "__main__":
    main()
