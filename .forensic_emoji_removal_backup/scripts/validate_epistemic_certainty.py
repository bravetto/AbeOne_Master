#!/usr/bin/env python3
"""
Epistemic Certainty Validator - Unified Base Class
Validates truth-first pattern validation with epistemic certainty

Pattern: AEYON × EPISTEMIC × CERTAINTY × VALIDATION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (ARXON)
Guardians: AEYON (999 Hz) + ARXON (777 Hz) + Abë (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
sys.path.insert(0, str(Path(__file__).parent))

from unified_validator_base import UnifiedValidatorBase, ValidationStatus

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class EpistemicCertaintyValidator(UnifiedValidatorBase):
    """
    Epistemic Certainty Validator - SIMPLIFIED
    
    Pattern: EXECUTE → VALIDATE → RETURN
    SAFETY: Handles missing modules gracefully
    VERIFY: python scripts/validate_epistemic_certainty.py
    """
    
    def __init__(self, workspace_root=None):
        super().__init__(workspace_root)
        self.emergent_os = self.workspace_root / "EMERGENT_OS"
        self.epistemic_validator = self.emergent_os / "emergence_core" / "epistemic_validator.py"
        self.universal_validator = self.emergent_os / "emergence_core" / "universal_validator.py"
    
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """Define checks as data - THE UNIFYING PATTERN"""
        return {
            'epistemic_validator_exists': {
                'name': 'Epistemic Validator Exists',
                'func': self._check_epistemic_validator_exists,
                'required': True
            },
            'universal_validator_exists': {
                'name': 'Universal Validator Exists',
                'func': self._check_universal_validator_exists,
                'required': True
            },
            'epistemic_framework': {
                'name': 'Epistemic Framework Implementation',
                'func': self._check_epistemic_framework,
                'required': True
            },
            'truth_first_validation': {
                'name': 'Truth-First Validation Pattern',
                'func': self._check_truth_first_validation,
                'required': True
            },
            'certainty_calculation': {
                'name': 'Certainty Calculation',
                'func': self._check_certainty_calculation,
                'required': True
            },
            'pattern_validation': {
                'name': 'Pattern Validation Pipeline',
                'func': self._check_pattern_validation,
                'required': True
            },
            'cross_domain_certainty': {
                'name': 'Cross-Domain Certainty',
                'func': self._check_cross_domain_certainty,
                'required': False
            }
        }
    
    def _check_epistemic_validator_exists(self) -> Tuple[str, List[str]]:
        """Check epistemic validator exists"""
        return self._check_file(self.epistemic_validator, "Epistemic validator")
    
    def _check_universal_validator_exists(self) -> Tuple[str, List[str]]:
        """Check universal validator exists"""
        return self._check_file(self.universal_validator, "Universal validator")
    
    def _check_epistemic_framework(self) -> Dict[str, Any]:
        """Check epistemic framework implementation"""
        if not self.epistemic_validator.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Epistemic validator not found']}
        
        content = self._read_file(self.epistemic_validator)
        
        # Check for key epistemic components
        components = [
            'EpistemicStatus',
            'EpistemicPattern',
            'EpistemicPatternValidator',
            'validate_pattern',
            'certainty',
            'evidence_quality'
        ]
        
        found = [c for c in components if c in content]
        score = len(found) / len(components)
        
        status = ValidationStatus.PASS.value if score >= 0.8 else ValidationStatus.WARN.value if score >= 0.6 else ValidationStatus.FAIL.value
        
        details = [
            f"Components found: {len(found)}/{len(components)}",
            f"Score: {score:.2%}"
        ]
        
        return {'status': status, 'details': details, 'score': score}
    
    def _check_truth_first_validation(self) -> Dict[str, Any]:
        """Check truth-first validation pattern"""
        if not self.universal_validator.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Universal validator not found']}
        
        content = self._read_file(self.universal_validator)
        
        # Check for truth-first patterns
        patterns = [
            'truth-first',
            'epistemic',
            'evidence',
            'certainty',
            'validate_pattern',
            'reject',
            'insufficient evidence'
        ]
        
        found = [p for p in patterns if p.lower() in content.lower()]
        score = len(found) / len(patterns)
        
        status = ValidationStatus.PASS.value if score >= 0.7 else ValidationStatus.WARN.value if score >= 0.5 else ValidationStatus.FAIL.value
        
        details = [
            f"Patterns found: {len(found)}/{len(patterns)}",
            f"Score: {score:.2%}"
        ]
        
        return {'status': status, 'details': details, 'score': score}
    
    def _check_certainty_calculation(self) -> Dict[str, Any]:
        """Check certainty calculation implementation"""
        if not self.epistemic_validator.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Epistemic validator not found']}
        
        content = self._read_file(self.epistemic_validator)
        
        # Check for certainty calculation methods
        methods = [
            '_calculate_certainty',
            '_assess_evidence',
            'certainty',
            'min_certainty_threshold'
        ]
        
        found = [m for m in methods if m in content]
        score = len(found) / len(methods)
        
        status = ValidationStatus.PASS.value if score >= 0.75 else ValidationStatus.WARN.value if score >= 0.5 else ValidationStatus.FAIL.value
        
        details = [
            f"Methods found: {len(found)}/{len(methods)}",
            f"Score: {score:.2%}"
        ]
        
        return {'status': status, 'details': details, 'score': score}
    
    def _check_pattern_validation(self) -> Dict[str, Any]:
        """Check pattern validation pipeline"""
        if not self.universal_validator.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Universal validator not found']}
        
        content = self._read_file(self.universal_validator)
        
        # Check for validation pipeline components
        components = [
            'validate_pattern',
            'matched_failure',
            'epistemic_pattern',
            'validation_status',
            'confidence'
        ]
        
        found = [c for c in components if c in content]
        score = len(found) / len(components)
        
        status = ValidationStatus.PASS.value if score >= 0.8 else ValidationStatus.WARN.value if score >= 0.6 else ValidationStatus.FAIL.value
        
        details = [
            f"Components found: {len(found)}/{len(components)}",
            f"Score: {score:.2%}"
        ]
        
        return {'status': status, 'details': details, 'score': score}
    
    def _check_cross_domain_certainty(self) -> Dict[str, Any]:
        """Check cross-domain certainty implementation"""
        # Look for cross-domain validator
        cross_domain_validator = self.emergent_os / "emergence_core" / "cross_domain_validator.py"
        
        if not cross_domain_validator.exists():
            return {'status': ValidationStatus.INFO.value, 'details': ['Cross-domain validator not found (optional)']}
        
        content = self._read_file(cross_domain_validator)
        
        # Check for cross-domain patterns
        patterns = [
            'cross_domain',
            'certainty',
            'domain',
            'validation'
        ]
        
        found = [p for p in patterns if p.lower() in content.lower()]
        score = len(found) / len(patterns)
        
        status = ValidationStatus.PASS.value if score >= 0.75 else ValidationStatus.WARN.value
        
        details = [
            f"Patterns found: {len(found)}/{len(patterns)}",
            f"Score: {score:.2%}"
        ]
        
        return {'status': status, 'details': details, 'score': score}


def main():
    """CLI Entry Point - UNIFIED BASE CLASS"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Epistemic Certainty Validator - UNIFIED BASE CLASS")
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    
    args = parser.parse_args()
    
    validator = EpistemicCertaintyValidator(Path(args.workspace) if args.workspace else None)
    results = validator.run()
    
    if args.output:
        Path(args.output).write_text(json.dumps(results, indent=2, default=str))
        print(f"\n💾 Saved: {args.output}")
    
    sys.exit(0 if results['summary']['score'] >= 80 else 1 if results['summary']['score'] >= 60 else 2)


if __name__ == "__main__":
    main()

