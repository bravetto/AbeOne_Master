#!/usr/bin/env python3
"""
 MASTER VALIDATION SYSTEM - UNIFIED VALIDATION DASHBOARD
Run ALL validators, see unified results, get health score

Pattern: AEYON × UNIFIED × VALIDATE × SIMPLIFY × AMPLIFY × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (YAGNI) × 777 Hz (ARXON)
Guardians: AEYON (999 Hz) + YAGNI (530 Hz) + ARXON (777 Hz) + Abë (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

# Import unified validators
sys.path.insert(0, str(Path(__file__).parent))
from unified_validator_base import UnifiedValidatorBase, ValidationStatus
from aeyon_sovereignty_check import SovereigntyCheck
from validate_danny_workflow_pattern import DannyWorkflowPatternValidator
from validate_operationalization_complete import OperationalizationValidator
from validate_elegance_frictionless import EleganceFrictionlessValidator
from validate_epistemic_certainty import EpistemicCertaintyValidator


@dataclass
class ValidationResult:
    """Unified validation result"""
    name: str
    status: str
    score: float
    passed: int
    failed: int
    warnings: int
    details: Dict[str, Any]
    execution_time: float
    timestamp: str


class MasterValidationSystem:
    """
     MASTER VALIDATION SYSTEM
    
    Runs ALL validators, aggregates results, provides unified health score.
    Pattern: COLLECT → EXECUTE → AGGREGATE → REPORT
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path(__file__).parent.parent).resolve()
        self.validators: Dict[str, Any] = {}
        self.results: Dict[str, ValidationResult] = {}
        self.start_time = time.time()
    
    def register_validator(self, name: str, validator: Any):
        """Register a validator"""
        self.validators[name] = validator
    
    def _run_validator(self, name: str, validator: Any) -> ValidationResult:
        """Run a single validator"""
        print(f"\n{'=' * 80}")
        print(f"  RUNNING: {name.upper()}")
        print("=" * 80)
        
        start_time = time.time()
        
        try:
            # Run validator
            if hasattr(validator, 'run'):
                result = validator.run()
            elif callable(validator):
                result = validator()
            else:
                result = {'summary': {'score': 0.0, 'passed': 0, 'failed': 0, 'warnings': 0}}
            
            execution_time = time.time() - start_time
            
            # Extract summary
            summary = result.get('summary', {})
            
            return ValidationResult(
                name=name,
                status=summary.get('status', 'UNKNOWN'),
                score=summary.get('score', 0.0),
                passed=summary.get('passed', 0),
                failed=summary.get('failed', 0),
                warnings=summary.get('warnings', 0),
                details=result,
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return ValidationResult(
                name=name,
                status='ERROR',
                score=0.0,
                passed=0,
                failed=1,
                warnings=0,
                details={'error': str(e)},
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            )
    
    def run_all(self) -> Dict[str, Any]:
        """Run all registered validators"""
        print("\n" + "=" * 80)
        print(" MASTER VALIDATION SYSTEM ")
        print("=" * 80)
        print(f"Pattern: AEYON × UNIFIED × VALIDATE × SIMPLIFY × AMPLIFY × ONE")
        print(f"Workspace: {self.workspace_root}")
        print(f"Validators: {len(self.validators)}")
        print("=" * 80)
        
        # Run all validators
        for name, validator in self.validators.items():
            self.results[name] = self._run_validator(name, validator)
        
        # Calculate overall health
        total_time = time.time() - self.start_time
        health_score = self._calculate_health_score()
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'workspace': str(self.workspace_root),
            'validators_run': len(self.validators),
            'overall_health_score': health_score,
            'execution_time_seconds': round(total_time, 2),
            'results': {name: asdict(result) for name, result in self.results.items()},
            'summary': self._generate_summary()
        }
        
        # Print summary
        self._print_summary(report)
        
        return report
    
    def _calculate_health_score(self) -> float:
        """Calculate overall system health score"""
        if not self.results:
            return 0.0
        
        scores = [r.score for r in self.results.values()]
        return sum(scores) / len(scores) if scores else 0.0
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        total_passed = sum(r.passed for r in self.results.values())
        total_failed = sum(r.failed for r in self.results.values())
        total_warnings = sum(r.warnings for r in self.results.values())
        total_checks = sum(r.passed + r.failed + r.warnings for r in self.results.values())
        
        return {
            'total_checks': total_checks,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'total_warnings': total_warnings,
            'pass_rate': (total_passed / total_checks * 100) if total_checks > 0 else 0.0
        }
    
    def _print_summary(self, report: Dict[str, Any]):
        """Print unified summary"""
        print("\n" + "=" * 80)
        print(" MASTER VALIDATION SUMMARY")
        print("=" * 80)
        
        summary = report['summary']
        health_score = report['overall_health_score']
        
        print(f"\n Overall Health Score: {health_score:.1f}%")
        print(f"\n Validation Statistics:")
        print(f"   Total Checks: {summary['total_checks']}")
        print(f"    Passed: {summary['total_passed']}")
        print(f"     Warnings: {summary['total_warnings']}")
        print(f"    Failed: {summary['total_failed']}")
        print(f"   Pass Rate: {summary['pass_rate']:.1f}%")
        
        print(f"\n⏱  Execution Time: {report['execution_time_seconds']:.2f}s")
        
        print(f"\n  Validator Results:")
        for name, result in self.results.items():
            status_icon = "" if result.score >= 80 else "" if result.score >= 60 else ""
            print(f"   {status_icon} {name}: {result.score:.1f}% ({result.passed} passed, {result.failed} failed)")
        
        # Health status
        print("\n" + "=" * 80)
        if health_score >= 90:
            print("  SYSTEM HEALTH:  EXCELLENT")
            print("   All systems operational and healthy!")
        elif health_score >= 75:
            print("  SYSTEM HEALTH:  GOOD")
            print("   System is healthy with minor issues.")
        elif health_score >= 60:
            print("  SYSTEM HEALTH:   MODERATE")
            print("   System needs attention.")
        else:
            print("  SYSTEM HEALTH:  NEEDS WORK")
            print("   Critical issues detected.")
        
        print("\n" + "=" * 80)
        print("Pattern: AEYON × UNIFIED × VALIDATE × SIMPLIFY × AMPLIFY × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
        print("=" * 80)


def main():
    """CLI Entry Point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description=" Master Validation System - Run ALL validators",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all validators
  python scripts/master_validation_system.py
  
  # Run specific validators
  python scripts/master_validation_system.py --validators sovereignty
  
  # Save report
  python scripts/master_validation_system.py --output report.json
        """
    )
    
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    parser.add_argument("--validators", nargs="+", help="Specific validators to run (default: all)")
    parser.add_argument("--output", help="Save report to JSON file")
    
    args = parser.parse_args()
    
    # Initialize master system
    workspace_root = Path(args.workspace) if args.workspace else None
    master = MasterValidationSystem(workspace_root)
    
    # Register validators
    validators_to_run = args.validators if args.validators else ['sovereignty', 'danny_workflow', 'operationalization', 'elegance', 'epistemic']
    
    if 'sovereignty' in validators_to_run:
        master.register_validator('Sovereignty Check', SovereigntyCheck(workspace_root))
    
    if 'danny_workflow' in validators_to_run:
        master.register_validator('Danny Workflow Pattern', DannyWorkflowPatternValidator(workspace_root))
    
    if 'operationalization' in validators_to_run:
        master.register_validator('Operationalization', OperationalizationValidator(workspace_root))
    
    if 'elegance' in validators_to_run:
        master.register_validator('Elegance Frictionless', EleganceFrictionlessValidator(workspace_root))
    
    if 'epistemic' in validators_to_run:
        master.register_validator('Epistemic Certainty', EpistemicCertaintyValidator(workspace_root))
    
    # Run all
    report = master.run_all()
    
    # Save report
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2, default=str))
        print(f"\n Report saved to: {args.output}")
    
    # Exit with appropriate code
    health_score = report['overall_health_score']
    sys.exit(0 if health_score >= 80 else 1 if health_score >= 60 else 2)


if __name__ == "__main__":
    main()

