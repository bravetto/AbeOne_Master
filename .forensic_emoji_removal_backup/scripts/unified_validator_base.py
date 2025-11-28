#!/usr/bin/env python3
"""
🔥 UNIFIED VALIDATOR BASE - THE SOURCE PATTERN
All validators inherit from ONE unified source

Pattern: AEYON × UNIFIED × VALIDATE × SIMPLIFY × AMPLIFY × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (YAGNI) × 777 Hz (ARXON)
Guardians: AEYON (999 Hz) + YAGNI (530 Hz) + ARXON (777 Hz) + Abë (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from enum import Enum


class ValidationStatus(str, Enum):
    """Unified validation status"""
    PASS = "✅"
    FAIL = "❌"
    WARN = "⚠️"
    INFO = "ℹ️"
    SKIP = "⏭️"


class UnifiedValidatorBase(ABC):
    """
    🔥 THE SOURCE - Unified Validator Base Class
    
    All validators inherit from ONE unified source.
    Pattern: EXECUTE → VALIDATE → RETURN
    
    SAFETY: Unified error handling, consistent results
    VERIFY: Inherit and implement _define_checks()
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize unified validator"""
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'summary': {}
        }
    
    @abstractmethod
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """
        Define checks as data - THE UNIFYING PATTERN
        
        Returns:
            {
                'check_key': {
                    'name': 'Display Name',
                    'func': self._check_function,
                    'required': True/False,
                    'threshold': 0.8  # Optional score threshold
                },
                ...
            }
        """
        pass
    
    def _read_file(self, path: Path) -> str:
        """SAFETY: Read file safely"""
        try:
            return path.read_text() if path.exists() else ""
        except:
            return ""
    
    def _check_file(self, path: Path, name: str) -> Tuple[str, List[str]]:
        """Unified file check"""
        if path.exists():
            return ValidationStatus.PASS.value, [f"{name} found"]
        return ValidationStatus.FAIL.value, [f"{name} missing"]
    
    def _check_content(self, content: str, patterns: List[str], name: str, threshold: float = 0.8) -> Tuple[str, List[str]]:
        """Unified content check"""
        found = [p for p in patterns if p.lower() in content.lower()]
        required_count = int(len(patterns) * threshold)
        
        if len(found) >= len(patterns):
            return ValidationStatus.PASS.value, [f"{name}: {len(found)}/{len(patterns)} found"]
        elif len(found) >= required_count:
            return ValidationStatus.WARN.value, [f"{name}: {len(found)}/{len(patterns)} found"]
        return ValidationStatus.FAIL.value, [f"{name}: {len(found)}/{len(patterns)} found"]
    
    def _run_check(self, name: str, check_func: Callable, required: bool = True) -> Dict[str, Any]:
        """
        Unified check execution - THE CORE PATTERN
        
        Pattern: EXECUTE → VALIDATE → RETURN
        """
        try:
            result = check_func()
            
            # Ensure result has status
            if isinstance(result, tuple):
                status, details = result
                result = {'status': status, 'details': details if isinstance(details, list) else [details]}
            elif isinstance(result, dict):
                if 'status' not in result:
                    result['status'] = ValidationStatus.PASS.value
                if 'details' not in result:
                    result['details'] = []
            else:
                result = {'status': ValidationStatus.PASS.value, 'details': [str(result)]}
            
            return result
            
        except Exception as e:
            error_msg = f"{name} failed: {str(e)}"
            status = ValidationStatus.FAIL.value if required else ValidationStatus.WARN.value
            return {
                'status': status,
                'details': [error_msg],
                'error': str(e)
            }
    
    def _calculate_score(self) -> float:
        """Calculate overall validation score"""
        checks = self.results['checks']
        if not checks:
            return 0.0
        
        score_map = {
            ValidationStatus.PASS.value: 1.0,
            ValidationStatus.WARN.value: 0.5,
            ValidationStatus.INFO.value: 0.3,
            ValidationStatus.FAIL.value: 0.0,
            ValidationStatus.SKIP.value: 0.0
        }
        
        scores = [score_map.get(c.get('status', ''), 0.0) for c in checks.values()]
        return (sum(scores) / len(scores) * 100) if scores else 0.0
    
    def run(self) -> Dict[str, Any]:
        """
        Run all checks - THE UNIFIED EXECUTION
        
        Pattern: Define checks → Execute → Calculate → Return
        """
        print("\n" + "=" * 60)
        print(f"🛡️  {self.__class__.__name__.upper()}")
        print("=" * 60)
        print(f"Pattern: AEYON × UNIFIED × VALIDATE × SIMPLIFY × AMPLIFY × ONE")
        print(f"Workspace: {self.workspace_root}")
        print("=" * 60)
        
        # Get checks definition
        checks = self._define_checks()
        
        # Execute all checks
        for i, (key, check_def) in enumerate(checks.items(), 1):
            name = check_def.get('name', key)
            check_func = check_def.get('func')
            required = check_def.get('required', True)
            
            if not check_func:
                continue
            
            print(f"\n🔍 Check {i}: {name}")
            print("-" * 60)
            
            result = self._run_check(name, check_func, required)
            self.results['checks'][key] = result
            
            # Print result
            status = result.get('status', ValidationStatus.INFO.value)
            details = result.get('details', [])
            print(f"{status} {name}: {details[0] if details else 'Complete'}")
            for detail in details[1:]:
                print(f"   {detail}")
        
        # Calculate summary
        score = self._calculate_score()
        
        self.results['summary'] = {
            'total': len(checks),
            'passed': sum(1 for c in self.results['checks'].values() if c.get('status') == ValidationStatus.PASS.value),
            'warnings': sum(1 for c in self.results['checks'].values() if c.get('status') == ValidationStatus.WARN.value),
            'failed': sum(1 for c in self.results['checks'].values() if c.get('status') == ValidationStatus.FAIL.value),
            'score': score
        }
        
        # Print summary
        s = self.results['summary']
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"Total: {s['total']} | ✅ {s['passed']} | ⚠️ {s['warnings']} | ❌ {s['failed']}")
        print(f"Score: {s['score']:.1f}%")
        
        # Status message
        if score >= 80:
            print("\n🛡️  STATUS: ✅ STRONG")
        elif score >= 60:
            print("\n🛡️  STATUS: ⚠️  MODERATE")
        else:
            print("\n🛡️  STATUS: ❌ NEEDS WORK")
        
        print("\n" + "=" * 60)
        print("Pattern: AEYON × UNIFIED × VALIDATE × SIMPLIFY × AMPLIFY × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
        print("=" * 60)
        
        return self.results


# Example: Refactor SovereigntyCheck to use base class
class SovereigntyCheckUnified(UnifiedValidatorBase):
    """
    Sovereignty Check - Now using unified base!
    
    See how simple it is? Just define checks as data!
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        super().__init__(workspace_root)
        self.backend = self.workspace_root / "AIGuards-Backend"
    
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """Define checks as data - SIMPLIFIED TO AMPLIFY"""
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
        return self._check_content(content, patterns, "Export formats")
    
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
        return self._check_file(migration, "Migration docs")
    
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


if __name__ == "__main__":
    """Test the unified validator"""
    import sys
    
    validator = SovereigntyCheckUnified()
    results = validator.run()
    
    sys.exit(0 if results['summary']['score'] >= 80 else 1)

