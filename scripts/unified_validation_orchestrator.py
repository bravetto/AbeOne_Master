#!/usr/bin/env python3
"""
 UNIFIED VALIDATION ORCHESTRATOR
Single entry point for ALL validation systems

Coordinates:
- Master Validation System (Python validators)
- AbëONE Preflight ΩMega (comprehensive validation)
- Recursive Emergence Validator (recursive validation)
- Shell validators (Dockerfile, Helm, etc.)

Pattern: UNIFIED × ORCHESTRATION × VALIDATION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (YAGNI) × 777 Hz (ARXON)
Guardians: AEYON (999 Hz) + YAGNI (530 Hz) + ARXON (777 Hz) + Abë (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class ValidationResult:
    """Unified validation result"""
    name: str
    status: str  # "PASS", "FAIL", "WARN", "SKIP"
    score: float
    passed: int
    failed: int
    warnings: int
    details: Dict[str, Any]
    execution_time: float
    timestamp: str


class UnifiedValidationOrchestrator:
    """
     UNIFIED VALIDATION ORCHESTRATOR
    
    Single entry point that coordinates ALL validation systems:
    1. Master Validation System (Python validators)
    2. AbëONE Preflight ΩMega (comprehensive)
    3. Recursive Emergence Validator (recursive)
    4. Shell validators (Dockerfile, Helm, etc.)
    
    Pattern: COLLECT → COORDINATE → EXECUTE → AGGREGATE → REPORT
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path(__file__).parent.parent).resolve()
        self.script_dir = Path(__file__).parent
        self.results: List[ValidationResult] = []
        self.start_time = time.time()
    
    def run_all(self) -> Dict[str, Any]:
        """
        Run all validation systems and aggregate results.
        
        Returns:
            Unified validation report
        """
        print("=" * 80)
        print(" UNIFIED VALIDATION ORCHESTRATOR")
        print("=" * 80)
        print(f"Workspace: {self.workspace_root}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()
        
        # 1. Run Master Validation System (Python validators)
        print(" Step 1: Running Master Validation System...")
        master_result = self._run_master_validation()
        self.results.append(master_result)
        
        # 2. Run AbëONE Preflight ΩMega (comprehensive)
        print("\n Step 2: Running AbëONE Preflight ΩMega...")
        preflight_result = self._run_preflight_omega()
        self.results.append(preflight_result)
        
        # 3. Run Recursive Emergence Validator (if available)
        print("\n Step 3: Running Recursive Emergence Validator...")
        recursive_result = self._run_recursive_validator()
        if recursive_result:
            self.results.append(recursive_result)
        
        # 4. Run Shell Validators (Dockerfile, Helm, etc.)
        print("\n Step 4: Running Shell Validators...")
        shell_results = self._run_shell_validators()
        self.results.extend(shell_results)
        
        # Aggregate results
        return self._aggregate_results()
    
    def _run_master_validation(self) -> ValidationResult:
        """Run Master Validation System"""
        try:
            master_script = self.script_dir / "master_validation_system.py"
            if not master_script.exists():
                return ValidationResult(
                    name="Master Validation System",
                    status="SKIP",
                    score=0.0,
                    passed=0,
                    failed=0,
                    warnings=1,
                    details={"error": "master_validation_system.py not found"},
                    execution_time=0.0,
                    timestamp=datetime.now().isoformat()
                )
            
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, str(master_script), "--workspace", str(self.workspace_root)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            execution_time = time.time() - start_time
            
            # Parse output
            if result.returncode == 0:
                status = "PASS"
                score = 100.0
            else:
                status = "WARN" if result.returncode == 1 else "FAIL"
                score = 0.0
            
            return ValidationResult(
                name="Master Validation System",
                status=status,
                score=score,
                passed=1 if status == "PASS" else 0,
                failed=1 if status == "FAIL" else 0,
                warnings=1 if status == "WARN" else 0,
                details={"stdout": result.stdout, "stderr": result.stderr},
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            return ValidationResult(
                name="Master Validation System",
                status="FAIL",
                score=0.0,
                passed=0,
                failed=1,
                warnings=0,
                details={"error": str(e)},
                execution_time=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    def _run_preflight_omega(self) -> ValidationResult:
        """Run AbëONE Preflight ΩMega"""
        try:
            preflight_script = self.script_dir / "abeone_preflight_omega.py"
            if not preflight_script.exists():
                return ValidationResult(
                    name="AbëONE Preflight ΩMega",
                    status="SKIP",
                    score=0.0,
                    passed=0,
                    failed=0,
                    warnings=1,
                    details={"error": "abeone_preflight_omega.py not found"},
                    execution_time=0.0,
                    timestamp=datetime.now().isoformat()
                )
            
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, str(preflight_script), "--workspace", str(self.workspace_root)],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            execution_time = time.time() - start_time
            
            # Parse exit code (0=pass, 1=warn, 2=fail)
            if result.returncode == 0:
                status = "PASS"
                score = 100.0
            elif result.returncode == 1:
                status = "WARN"
                score = 70.0
            else:
                status = "FAIL"
                score = 0.0
            
            return ValidationResult(
                name="AbëONE Preflight ΩMega",
                status=status,
                score=score,
                passed=1 if status == "PASS" else 0,
                failed=1 if status == "FAIL" else 0,
                warnings=1 if status == "WARN" else 0,
                details={"stdout": result.stdout, "stderr": result.stderr},
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            return ValidationResult(
                name="AbëONE Preflight ΩMega",
                status="FAIL",
                score=0.0,
                passed=0,
                failed=1,
                warnings=0,
                details={"error": str(e)},
                execution_time=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    def _run_recursive_validator(self) -> Optional[ValidationResult]:
        """Run Recursive Emergence Validator (if available)"""
        try:
            recursive_script = self.script_dir / "jimmy_recursive_emergence_validator.py"
            if not recursive_script.exists():
                return None
            
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, str(recursive_script)],
                capture_output=True,
                text=True,
                timeout=300
            )
            execution_time = time.time() - start_time
            
            status = "PASS" if result.returncode == 0 else "WARN"
            score = 100.0 if result.returncode == 0 else 50.0
            
            return ValidationResult(
                name="Recursive Emergence Validator",
                status=status,
                score=score,
                passed=1 if status == "PASS" else 0,
                failed=0,
                warnings=1 if status == "WARN" else 0,
                details={"stdout": result.stdout, "stderr": result.stderr},
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            return ValidationResult(
                name="Recursive Emergence Validator",
                status="FAIL",
                score=0.0,
                passed=0,
                failed=1,
                warnings=0,
                details={"error": str(e)},
                execution_time=0.0,
                timestamp=datetime.now().isoformat()
            )
    
    def _run_shell_validators(self) -> List[ValidationResult]:
        """Run shell-based validators"""
        results = []
        
        # Shell validators to run
        shell_validators = [
            ("validate_dockerfile.sh", "Dockerfile Validation"),
            ("validate_helm.sh", "Helm Validation"),
            ("validate_service_yaml.sh", "Service YAML Validation"),
        ]
        
        for script_name, display_name in shell_validators:
            script_path = self.script_dir / script_name
            if not script_path.exists():
                continue
            
            try:
                start_time = time.time()
                result = subprocess.run(
                    ["bash", str(script_path), str(self.workspace_root)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                execution_time = time.time() - start_time
                
                status = "PASS" if result.returncode == 0 else "WARN"
                score = 100.0 if result.returncode == 0 else 50.0
                
                results.append(ValidationResult(
                    name=display_name,
                    status=status,
                    score=score,
                    passed=1 if status == "PASS" else 0,
                    failed=0,
                    warnings=1 if status == "WARN" else 0,
                    details={"stdout": result.stdout, "stderr": result.stderr},
                    execution_time=execution_time,
                    timestamp=datetime.now().isoformat()
                ))
            except Exception as e:
                results.append(ValidationResult(
                    name=display_name,
                    status="FAIL",
                    score=0.0,
                    passed=0,
                    failed=1,
                    warnings=0,
                    details={"error": str(e)},
                    execution_time=0.0,
                    timestamp=datetime.now().isoformat()
                ))
        
        return results
    
    def _aggregate_results(self) -> Dict[str, Any]:
        """Aggregate all validation results"""
        total_passed = sum(r.passed for r in self.results)
        total_failed = sum(r.failed for r in self.results)
        total_warnings = sum(r.warnings for r in self.results)
        total_time = sum(r.execution_time for r in self.results)
        
        # Calculate overall score
        if len(self.results) == 0:
            overall_score = 0.0
        else:
            overall_score = sum(r.score for r in self.results) / len(self.results)
        
        # Determine overall status
        if total_failed > 0:
            overall_status = "FAIL"
        elif total_warnings > 0:
            overall_status = "WARN"
        else:
            overall_status = "PASS"
        
        report = {
            "overall_status": overall_status,
            "overall_score": overall_score,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_warnings": total_warnings,
            "total_execution_time": total_time,
            "timestamp": datetime.now().isoformat(),
            "results": [asdict(r) for r in self.results]
        }
        
        # Print summary
        print("\n" + "=" * 80)
        print(" VALIDATION SUMMARY")
        print("=" * 80)
        print(f"Overall Status: {overall_status}")
        print(f"Overall Score: {overall_score:.1f}%")
        print(f"Passed: {total_passed}")
        print(f"Failed: {total_failed}")
        print(f"Warnings: {total_warnings}")
        print(f"Total Time: {total_time:.2f}s")
        print()
        
        for result in self.results:
            status_icon = {"PASS": "", "FAIL": "", "WARN": "", "SKIP": "⏭"}[result.status]
            print(f"{status_icon} {result.name}: {result.status} ({result.score:.1f}%)")
        
        print("=" * 80)
        
        return report


def main():
    """CLI Entry Point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description=" Unified Validation Orchestrator - Single entry point for ALL validations"
    )
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    parser.add_argument("--output", help="Save report to JSON file")
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace) if args.workspace else None
    orchestrator = UnifiedValidationOrchestrator(workspace_root)
    
    report = orchestrator.run_all()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n Report saved to: {args.output}")
    
    # Exit with appropriate code
    exit_code = 0 if report["overall_status"] == "PASS" else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

