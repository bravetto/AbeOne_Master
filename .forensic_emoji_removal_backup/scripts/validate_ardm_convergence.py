#!/usr/bin/env python3
"""
ARDM Convergence Validation

Validates that ARDM integrations are properly converged with existing systems.

Pattern: AEYON × VALIDATE × CONVERGENCE × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

from unified_validator_base import UnifiedValidatorBase, ValidationStatus


class ARDMConvergenceValidator(UnifiedValidatorBase):
    """
    ARDM Convergence Validator
    
    Validates:
    - Meta Orchestrator integration exists and works
    - Pre-commit hook integration exists
    - Operationalization workflow integration exists
    - Validation infrastructure integration exists
    """
    
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """Define ARDM convergence validation checks"""
        return {
            'convergence_mandates_doc': {
                'name': 'Convergence Mandates Document',
                'func': self._check_convergence_mandates_doc,
                'required': True,
            },
            'meta_orchestrator_integration': {
                'name': 'Meta Orchestrator Integration',
                'func': self._check_meta_orchestrator_integration,
                'required': True,
            },
            'pre_commit_integration': {
                'name': 'Pre-Commit Hook Integration',
                'func': self._check_pre_commit_integration,
                'required': True,
            },
            'operationalization_integration': {
                'name': 'Operationalization Workflow Integration',
                'func': self._check_operationalization_integration,
                'required': True,
            },
            'meta_orchestrator_functional': {
                'name': 'Meta Orchestrator Integration Functional',
                'func': self._check_meta_orchestrator_functional,
                'required': True,
            },
        }
    
    def _check_convergence_mandates_doc(self) -> Tuple[str, List[str]]:
        """Check if convergence mandates document exists"""
        doc_path = self.workspace_root / "ARDM_CONVERGENCE_MANDATES.md"
        return self._check_file(doc_path, "ARDM_CONVERGENCE_MANDATES.md")
    
    def _check_meta_orchestrator_integration(self) -> Tuple[str, List[str]]:
        """Check if Meta Orchestrator integration exists"""
        integration_path = self.workspace_root / "scripts" / "ardm-meta-orchestrator-integration.py"
        return self._check_file(integration_path, "ardm-meta-orchestrator-integration.py")
    
    def _check_pre_commit_integration(self) -> Tuple[str, List[str]]:
        """Check if pre-commit hook integration exists"""
        hook_path = self.workspace_root / "scripts" / "pre-commit-ardm-check.sh"
        return self._check_file(hook_path, "pre-commit-ardm-check.sh")
    
    def _check_operationalization_integration(self) -> Tuple[str, List[str]]:
        """Check if operationalization workflow integration exists"""
        script_path = self.workspace_root / "scripts" / "operationalize-with-ardm.sh"
        return self._check_file(script_path, "operationalize-with-ardm.sh")
    
    def _check_meta_orchestrator_functional(self) -> Tuple[str, List[str]]:
        """Check if Meta Orchestrator integration is functional"""
        integration_path = self.workspace_root / "scripts" / "ardm-meta-orchestrator-integration.py"
        if not integration_path.exists():
            return ValidationStatus.FAIL.value, ["Integration script not found"]
        
        content = self._read_file(integration_path)
        required_patterns = [
            "MetaOrchestratorARDMIntegration",
            "meta_scan",
            "REPLACE_ME",
            "validate_operationalization",
        ]
        
        return self._check_content(content, required_patterns, "Meta Orchestrator Integration", threshold=0.8)


def main():
    """Main validation entry point"""
    validator = ARDMConvergenceValidator()
    validator.run()
    
    # Print summary
    print("\n" + "="*60)
    print("ARDM Convergence Validation Summary")
    print("="*60)
    
    summary = validator.results.get('summary', {})
    total = summary.get('total', 0)
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    warnings = summary.get('warnings', 0)
    
    print(f"\nTotal Checks: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Warnings: {warnings}")
    
    if failed > 0:
        print("\n❌ ARDM convergence validation FAILED")
        sys.exit(1)
    elif warnings > 0:
        print("\n⚠️  ARDM convergence validation PASSED with warnings")
        sys.exit(0)
    else:
        print("\n✅ ARDM convergence validation PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()

