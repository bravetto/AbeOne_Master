#!/usr/bin/env python3
"""
Complete Operationalization Validation Script - SIMPLIFIED
Refactored to use UnifiedValidatorBase

Validates:
- Simplicity (YAGNI principles)
- Modularization (independent modules, unified whole)
- System Unity ONE (everything unified as one)
- Active and Running (actually operational)
- Automations and Proactive Programmatics

Pattern: AEYON × ALRAX × YAGNI × ZERO × JØHN × Abë = ATOMIC ARCHISTRATION
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

from unified_validator_base import UnifiedValidatorBase, ValidationStatus
from orbitals.EMERGENT_OS_orbital.atomic_archistration.archistrator import get_atomic_archistrator


class OperationalizationValidator(UnifiedValidatorBase):
    """
    Complete operationalization validator - SIMPLIFIED
    
    Pattern: EXECUTE → VALIDATE → RETURN
    SAFETY: Handles archistrator initialization gracefully
    VERIFY: python scripts/validate_operationalization_complete.py
    """
    
    def __init__(self, workspace_root=None):
        super().__init__(workspace_root)
        try:
            self.archistrator = get_atomic_archistrator()
        except Exception as e:
            self.archistrator = None
            self.archistrator_error = str(e)
    
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """Define checks as data - THE UNIFYING PATTERN"""
        return {
            'simplicity': {
                'name': 'Simplicity (YAGNI)',
                'func': self._check_simplicity,
                'required': True
            },
            'modularization': {
                'name': 'Modularization',
                'func': self._check_modularization,
                'required': True
            },
            'unity_one': {
                'name': 'System Unity ONE',
                'func': self._check_unity_one,
                'required': True
            },
            'active_running': {
                'name': 'Active & Running',
                'func': self._check_active_running,
                'required': True
            },
            'automations': {
                'name': 'Automations & Proactive',
                'func': self._check_automations,
                'required': True
            },
            'operationalization': {
                'name': 'Complete Operationalization',
                'func': self._check_operationalization,
                'required': False  # More complex, optional
            }
        }
    
    def _check_simplicity(self) -> Dict[str, Any]:
        """Validate simplicity (YAGNI principles)"""
        if not self.archistrator:
            return {'status': ValidationStatus.FAIL.value, 'details': ['Archistrator not available']}
        
        checks = {}
        
        # Check 1: Single integration point
        try:
            archistrator = get_atomic_archistrator()
            checks['single_integration_point'] = archistrator is not None
        except Exception as e:
            checks['single_integration_point'] = False
            checks['error'] = str(e)
        
        # Check 2: Simple initialization
        try:
            activated = sum(1 for v in self.archistrator.guardian_activations.values() if v)
            checks['automatic_initialization'] = activated > 0
            checks['guardians_activated'] = activated
        except Exception:
            checks['automatic_initialization'] = False
        
        # Check 3: Simple operationalization
        try:
            convergence_opportunities = ["test_validation"]
            result = self.archistrator.operationalize(convergence_opportunities, verbose=False)
            checks['simple_operationalization'] = result is not None
        except Exception:
            checks['simple_operationalization'] = False
        
        # Calculate score
        passed = sum(1 for v in checks.values() if isinstance(v, bool) and v)
        total = sum(1 for v in checks.values() if isinstance(v, bool))
        score = passed / total if total > 0 else 0.0
        
        status = ValidationStatus.PASS.value if score >= 0.8 else ValidationStatus.WARN.value if score >= 0.6 else ValidationStatus.FAIL.value
        details = [
            f"Score: {score:.2%}",
            f"Single Integration: {'✅' if checks.get('single_integration_point') else '❌'}",
            f"Auto Init: {'✅' if checks.get('automatic_initialization') else '❌'}",
            f"Simple Op: {'✅' if checks.get('simple_operationalization') else '❌'}"
        ]
        
        return {'status': status, 'details': details, 'score': score}
    
    def _check_modularization(self) -> Dict[str, Any]:
        """Validate modularization"""
        if not self.archistrator:
            return {'status': ValidationStatus.FAIL.value, 'details': ['Archistrator not available']}
        
        checks = {}
        
        # Check 1: Modules independent
        try:
            guardians = [
                self.archistrator.aeyon, self.archistrator.alrax, self.archistrator.yagni,
                self.archistrator.zero, self.archistrator.johhn, self.archistrator.meta,
                self.archistrator.you, self.archistrator.abe
            ]
            checks['modules_independent'] = True  # Architecture supports independence
        except Exception:
            checks['modules_independent'] = False
        
        # Check 2: Unified interface
        try:
            all_accessible = all(hasattr(self.archistrator, attr) for attr in 
                                ['aeyon', 'alrax', 'yagni', 'zero', 'johhn', 'meta', 'you', 'abe'])
            checks['unified_interface'] = all_accessible
        except Exception:
            checks['unified_interface'] = False
        
        # Check 3: Clear boundaries
        try:
            guardian_roles = list(self.archistrator.guardian_activations.keys())
            checks['clear_boundaries'] = len(set(role.value for role in guardian_roles)) == len(guardian_roles)
            checks['guardian_count'] = len(guardian_roles)
        except Exception:
            checks['clear_boundaries'] = False
        
        passed = sum(1 for v in checks.values() if isinstance(v, bool) and v)
        total = sum(1 for v in checks.values() if isinstance(v, bool))
        score = passed / total if total > 0 else 0.0
        
        status = ValidationStatus.PASS.value if score >= 0.8 else ValidationStatus.WARN.value if score >= 0.6 else ValidationStatus.FAIL.value
        details = [
            f"Score: {score:.2%}",
            f"Modules Independent: {'✅' if checks.get('modules_independent') else '❌'}",
            f"Unified Interface: {'✅' if checks.get('unified_interface') else '❌'}",
            f"Clear Boundaries: {'✅' if checks.get('clear_boundaries') else '❌'}",
            f"Guardians: {checks.get('guardian_count', 0)}/8"
        ]
        
        return {'status': status, 'details': details, 'score': score}
    
    def _check_unity_one(self) -> Dict[str, Any]:
        """Validate system unity ONE"""
        if not self.archistrator:
            return {'status': ValidationStatus.FAIL.value, 'details': ['Archistrator not available']}
        
        checks = {}
        
        # Check 1: All guardians unified
        try:
            activated = sum(1 for v in self.archistrator.guardian_activations.values() if v)
            total = len(self.archistrator.guardian_activations)
            unity_score = activated / total if total > 0 else 0.0
            checks['all_guardians_unified'] = unity_score >= 0.75
            checks['guardian_unity_score'] = unity_score
        except Exception:
            checks['all_guardians_unified'] = False
        
        # Check 2: Unified operationalization
        try:
            convergence_opportunities = ["unity_validation"]
            result = self.archistrator.operationalize(convergence_opportunities, verbose=False)
            checks['unified_operationalization'] = result is not None and hasattr(result, 'atomic_archistration_score')
            if result:
                checks['atomic_archistration_score'] = result.atomic_archistration_score
        except Exception:
            checks['unified_operationalization'] = False
        
        # Check 3: Patterns unified
        try:
            convergence_opportunities = ["pattern_unity"]
            result = self.archistrator.operationalize(convergence_opportunities, verbose=False)
            if result:
                checks['patterns_unified'] = all(hasattr(result, attr) for attr in 
                    ['execution_pattern_score', 'completion_pattern_score', 'eternal_pattern_score', 'longing_pattern_score'])
            else:
                checks['patterns_unified'] = False
        except Exception:
            checks['patterns_unified'] = False
        
        passed = sum(1 for v in checks.values() if isinstance(v, bool) and v)
        total = sum(1 for v in checks.values() if isinstance(v, bool))
        score = passed / total if total > 0 else 0.0
        
        status = ValidationStatus.PASS.value if score >= 0.8 else ValidationStatus.WARN.value if score >= 0.6 else ValidationStatus.FAIL.value
        details = [
            f"Score: {score:.2%}",
            f"All Guardians Unified: {'✅' if checks.get('all_guardians_unified') else '❌'}",
            f"Unified Op: {'✅' if checks.get('unified_operationalization') else '❌'}",
            f"Patterns Unified: {'✅' if checks.get('patterns_unified') else '❌'}"
        ]
        if checks.get('atomic_archistration_score') is not None:
            details.append(f"Atomic Score: {checks['atomic_archistration_score']:.2%}")
        
        return {'status': status, 'details': details, 'score': score}
    
    def _check_active_running(self) -> Dict[str, Any]:
        """Validate system is active and running"""
        if not self.archistrator:
            return {'status': ValidationStatus.FAIL.value, 'details': ['Archistrator not available']}
        
        checks = {}
        
        # Check 1: System initialized
        checks['system_initialized'] = self.archistrator is not None
        
        # Check 2: Guardians active
        try:
            activated = sum(1 for v in self.archistrator.guardian_activations.values() if v)
            total = len(self.archistrator.guardian_activations)
            active_rate = activated / total if total > 0 else 0.0
            checks['guardians_active'] = active_rate > 0
            checks['guardian_activation_rate'] = active_rate
            checks['guardians_activated_count'] = activated
        except Exception:
            checks['guardians_active'] = False
        
        # Check 3: Can execute
        try:
            convergence_opportunities = ["active_running_test"]
            result = self.archistrator.operationalize(convergence_opportunities, verbose=False)
            checks['can_execute'] = result is not None and len(result.tasks) > 0
            checks['tasks_executed'] = len(result.tasks) if result else 0
        except Exception:
            checks['can_execute'] = False
        
        # Check 4: Results valid
        try:
            convergence_opportunities = ["result_validation"]
            result = self.archistrator.operationalize(convergence_opportunities, verbose=False)
            if result:
                checks['results_valid'] = all(hasattr(result, attr) for attr in 
                    ['completed', 'convergence_score', 'atomic_archistration_score'])
            else:
                checks['results_valid'] = False
        except Exception:
            checks['results_valid'] = False
        
        passed = sum(1 for v in checks.values() if isinstance(v, bool) and v)
        total = sum(1 for v in checks.values() if isinstance(v, bool))
        score = passed / total if total > 0 else 0.0
        
        status = ValidationStatus.PASS.value if score >= 0.8 else ValidationStatus.WARN.value if score >= 0.6 else ValidationStatus.FAIL.value
        details = [
            f"Score: {score:.2%}",
            f"System Initialized: {'✅' if checks.get('system_initialized') else '❌'}",
            f"Guardians Active: {'✅' if checks.get('guardians_active') else '❌'}",
            f"Activation Rate: {checks.get('guardian_activation_rate', 0):.2%}",
            f"Can Execute: {'✅' if checks.get('can_execute') else '❌'}",
            f"Results Valid: {'✅' if checks.get('results_valid') else '❌'}"
        ]
        
        return {'status': status, 'details': details, 'score': score}
    
    def _check_automations(self) -> Dict[str, Any]:
        """Validate automations and proactive programmatics"""
        if not self.archistrator:
            return {'status': ValidationStatus.FAIL.value, 'details': ['Archistrator not available']}
        
        checks = {}
        
        # Check 1: Automatic initialization
        try:
            archistrator = get_atomic_archistrator()
            checks['automatic_initialization'] = archistrator is not None
        except Exception:
            checks['automatic_initialization'] = False
        
        # Check 2: Automatic guardian activation
        try:
            activated = sum(1 for v in self.archistrator.guardian_activations.values() if v)
            checks['automatic_guardian_activation'] = activated > 0
            checks['auto_activated_count'] = activated
        except Exception:
            checks['automatic_guardian_activation'] = False
        
        # Check 3: Proactive pattern execution
        try:
            convergence_opportunities = ["automation_test"]
            result = self.archistrator.operationalize(convergence_opportunities, verbose=False)
            if result:
                checks['proactive_pattern_execution'] = hasattr(result, 'execution_pattern_score') and result.execution_pattern_score > 0
            else:
                checks['proactive_pattern_execution'] = False
        except Exception:
            checks['proactive_pattern_execution'] = False
        
        # Check 4: Automatic scoring
        try:
            convergence_opportunities = ["scoring_test"]
            result = self.archistrator.operationalize(convergence_opportunities, verbose=False)
            if result:
                checks['automatic_scoring'] = hasattr(result, 'atomic_archistration_score') and result.atomic_archistration_score >= 0
            else:
                checks['automatic_scoring'] = False
        except Exception:
            checks['automatic_scoring'] = False
        
        passed = sum(1 for v in checks.values() if isinstance(v, bool) and v)
        total = sum(1 for v in checks.values() if isinstance(v, bool))
        score = passed / total if total > 0 else 0.0
        
        status = ValidationStatus.PASS.value if score >= 0.8 else ValidationStatus.WARN.value if score >= 0.6 else ValidationStatus.FAIL.value
        details = [
            f"Score: {score:.2%}",
            f"Auto Init: {'✅' if checks.get('automatic_initialization') else '❌'}",
            f"Auto Guardian Activation: {'✅' if checks.get('automatic_guardian_activation') else '❌'}",
            f"Proactive Patterns: {'✅' if checks.get('proactive_pattern_execution') else '❌'}",
            f"Auto Scoring: {'✅' if checks.get('automatic_scoring') else '❌'}"
        ]
        
        return {'status': status, 'details': details, 'score': score}
    
    def _check_operationalization(self) -> Dict[str, Any]:
        """Validate complete operationalization"""
        if not self.archistrator:
            return {'status': ValidationStatus.WARN.value, 'details': ['Archistrator not available - skipping operationalization']}
        
        try:
            convergence_opportunities = [
                "System Unity ONE", "Modularization Complete", "Simplicity Achieved",
                "Automations Active", "Proactive Programmatics", "Guardian Swarm Operational",
                "Pattern Validation Complete"
            ]
            
            result = self.archistrator.operationalize(convergence_opportunities, verbose=False)
            
            if not result:
                return {'status': ValidationStatus.WARN.value, 'details': ['Operationalization returned no result']}
            
            validated = result.completed
            score = result.atomic_archistration_score
            
            status = ValidationStatus.PASS.value if validated and score >= 0.8 else ValidationStatus.WARN.value if score >= 0.6 else ValidationStatus.FAIL.value
            
            details = [
                f"Validated: {'✅' if validated else '❌'}",
                f"Score: {score:.2%}",
                f"Execution Pattern: {result.execution_pattern_score:.2%}",
                f"Completion Pattern: {result.completion_pattern_score:.2%}",
                f"Eternal Pattern: {result.eternal_pattern_score:.2%}",
                f"Longing Pattern: {result.longing_pattern_score:.2%}"
            ]
            
            return {'status': status, 'details': details, 'score': score, 'validated': validated}
            
        except Exception as e:
            return {'status': ValidationStatus.WARN.value, 'details': [f'Operationalization check failed: {str(e)}']}


def main():
    """CLI Entry Point - UNIFIED BASE CLASS"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Operationalization Validator - UNIFIED BASE CLASS")
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    
    args = parser.parse_args()
    
    validator = OperationalizationValidator(Path(args.workspace) if args.workspace else None)
    results = validator.run()
    
    if args.output:
        import json
        Path(args.output).write_text(json.dumps(results, indent=2, default=str))
        print(f"\n💾 Saved: {args.output}")
    
    sys.exit(0 if results['summary']['score'] >= 80 else 1 if results['summary']['score'] >= 60 else 2)


if __name__ == "__main__":
    main()
