#!/usr/bin/env python3
"""
Validate Elegance and Frictionless Operation - SIMPLIFIED
Refactored to use UnifiedValidatorBase

Ensures all systems are elegant, simple, and operate without friction

Pattern: ELEGANCE × SIMPLICITY × FRICTIONLESS × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Add EMERGENT_OS to path
EMERGENT_OS_PATH = Path(__file__).parent.parent / "EMERGENT_OS"
sys.path.insert(0, str(EMERGENT_OS_PATH))
sys.path.insert(0, str(Path(__file__).parent))

from unified_validator_base import UnifiedValidatorBase, ValidationStatus

SCRIPTS_DIR = Path(__file__).parent
BASE_DIR = SCRIPTS_DIR.parent
REPOS_DIR = BASE_DIR / "AIGuards-Backend" / "aiguardian-repos"


class EleganceFrictionlessValidator(UnifiedValidatorBase):
    """
    Validate elegance and frictionless operation - SIMPLIFIED
    
    Pattern: EXECUTE → VALIDATE → RETURN
    SAFETY: Handles missing files gracefully
    VERIFY: python scripts/validate_elegance_frictionless.py
    """
    
    def __init__(self, workspace_root=None):
        super().__init__(workspace_root)
        self.emergent_os = self.workspace_root / "EMERGENT_OS"
        self.repos_dir = self.workspace_root / "AIGuards-Backend" / "aiguardian-repos"
    
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """Define checks as data - THE UNIFYING PATTERN"""
        return {
            'bootstrap_elegance': {
                'name': 'Bootstrap System Elegance',
                'func': self._check_bootstrap_elegance,
                'required': True
            },
            'atomic_archistration_elegance': {
                'name': 'Atomic Archistration Elegance',
                'func': self._check_atomic_archistration_elegance,
                'required': True
            },
            'guardian_services_elegance': {
                'name': 'Guardian Services Elegance',
                'func': self._check_guardian_services_elegance,
                'required': True
            },
            'cicd_elegance': {
                'name': 'CI/CD Workflow Elegance',
                'func': self._check_cicd_elegance,
                'required': False
            },
            'integration_frictionless': {
                'name': 'Integration Points Frictionless',
                'func': self._check_integration_frictionless,
                'required': True
            },
            'code_quality': {
                'name': 'Code Quality (YAGNI/KISS/DRY)',
                'func': self._check_code_quality,
                'required': True
            }
        }
    
    def _check_bootstrap_elegance(self) -> Dict[str, Any]:
        """Validate bootstrap system elegance"""
        bootstrap_file = self.emergent_os / "one_kernel" / "bootstrap.py"
        
        if not bootstrap_file.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Bootstrap file not found']}
        
        content = self._read_file(bootstrap_file)
        lines = len(content.split('\n'))
        
        # Elegance indicators
        elegance_checks = [
            lines < 300,  # Concise
            "class ONEKernel" in content,  # Clear class
            "def bootstrap" in content,  # Clear function
            "Phase" in content,  # Clear phases
            "try:" in content and "except" in content,  # Error handling
        ]
        
        # Frictionless indicators
        frictionless_checks = [
            "bootstrap_one_kernel()" in content,  # Simple API
            "singleton" in content.lower(),  # Singleton
            "atomic_archistration" in content,  # Integrated
            len(re.findall(r'if.*:', content)) < 20,  # Not over-complicated
            "return True" in content or "return False" in content,  # Clear returns
        ]
        
        elegance_score = sum(elegance_checks) / len(elegance_checks)
        frictionless_score = sum(frictionless_checks) / len(frictionless_checks)
        overall_score = (elegance_score + frictionless_score) / 2
        
        status = ValidationStatus.PASS.value if overall_score >= 0.8 else ValidationStatus.WARN.value if overall_score >= 0.6 else ValidationStatus.FAIL.value
        
        details = [
            f"Elegance: {elegance_score:.2%}",
            f"Frictionless: {frictionless_score:.2%}",
            f"Lines: {lines}"
        ]
        
        return {'status': status, 'details': details, 'elegance_score': elegance_score, 'frictionless_score': frictionless_score}
    
    def _check_atomic_archistration_elegance(self) -> Dict[str, Any]:
        """Validate Atomic Archistration elegance"""
        archistrator_file = self.emergent_os / "atomic_archistration" / "archistrator.py"
        
        if not archistrator_file.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Archistrator file not found']}
        
        content = self._read_file(archistrator_file)
        
        # Elegance indicators
        elegance_checks = [
            "class AtomicArchistrator" in content,
            "def operationalize" in content,
            "@dataclass" in content,
            "AsyncGenerator" in content or "async def" in content,
            "Pattern:" in content,
        ]
        
        # Frictionless indicators
        frictionless_checks = [
            "get_atomic_archistrator()" in content,
            "singleton" in content.lower() or "_archistrator_instance" in content,
            "verbose" in content,
            len(re.findall(r'if.*:', content)) < 30,
            "return" in content,
        ]
        
        elegance_score = sum(elegance_checks) / len(elegance_checks)
        frictionless_score = sum(frictionless_checks) / len(frictionless_checks)
        overall_score = (elegance_score + frictionless_score) / 2
        
        status = ValidationStatus.PASS.value if overall_score >= 0.8 else ValidationStatus.WARN.value if overall_score >= 0.6 else ValidationStatus.FAIL.value
        
        details = [
            f"Elegance: {elegance_score:.2%}",
            f"Frictionless: {frictionless_score:.2%}"
        ]
        
        return {'status': status, 'details': details, 'elegance_score': elegance_score, 'frictionless_score': frictionless_score}
    
    def _check_guardian_services_elegance(self) -> Dict[str, Any]:
        """Validate guardian services elegance"""
        sample_service = self.repos_dir / "guardian-zero-service" / "service.py"
        
        if not sample_service.exists():
            return {'status': ValidationStatus.WARN.value, 'details': ['Sample service not found']}
        
        content = self._read_file(sample_service)
        
        # Elegance indicators
        elegance_checks = [
            "from fastapi import FastAPI" in content,
            "@asynccontextmanager" in content,
            "lifespan=lifespan" in content,
            "CORSMiddleware" in content,
            "BaseModel" in content,
        ]
        
        # Frictionless indicators
        frictionless_checks = [
            "os.getenv" in content,
            "CONSCIOUSNESS_ENABLED" in content,
            "FULL_INTEGRATION = False" in content,
            "/health" in content,
            "port=" in content or "EXPOSE" in content,
        ]
        
        elegance_score = sum(elegance_checks) / len(elegance_checks)
        frictionless_score = sum(frictionless_checks) / len(frictionless_checks)
        overall_score = (elegance_score + frictionless_score) / 2
        
        status = ValidationStatus.PASS.value if overall_score >= 0.8 else ValidationStatus.WARN.value if overall_score >= 0.6 else ValidationStatus.FAIL.value
        
        details = [
            f"Elegance: {elegance_score:.2%}",
            f"Frictionless: {frictionless_score:.2%}"
        ]
        
        return {'status': status, 'details': details, 'elegance_score': elegance_score, 'frictionless_score': frictionless_score}
    
    def _check_cicd_elegance(self) -> Dict[str, Any]:
        """Validate CI/CD workflow elegance"""
        cicd_workflow = self.repos_dir / ".github" / "workflows" / "deploy-guardian-services.yml"
        
        if not cicd_workflow.exists():
            return {'status': ValidationStatus.INFO.value, 'details': ['CI/CD workflow not found']}
        
        content = self._read_file(cicd_workflow)
        
        # Elegance indicators
        elegance_checks = [
            "name:" in content,
            "runs-on:" in content,
            "steps:" in content,
            "- name:" in content,
            "if:" in content,
        ]
        
        # Frictionless indicators
        frictionless_checks = [
            "workflow_dispatch" in content,
            "arc-runner-set" in content,
            "continue-on-error" in content,
            "||" in content or "&&" in content,
            "echo" in content,
        ]
        
        elegance_score = sum(elegance_checks) / len(elegance_checks)
        frictionless_score = sum(frictionless_checks) / len(frictionless_checks)
        overall_score = (elegance_score + frictionless_score) / 2
        
        status = ValidationStatus.PASS.value if overall_score >= 0.8 else ValidationStatus.WARN.value if overall_score >= 0.6 else ValidationStatus.FAIL.value
        
        details = [
            f"Elegance: {elegance_score:.2%}",
            f"Frictionless: {frictionless_score:.2%}"
        ]
        
        return {'status': status, 'details': details, 'elegance_score': elegance_score, 'frictionless_score': frictionless_score}
    
    def _check_integration_frictionless(self) -> Dict[str, Any]:
        """Validate integration points are frictionless"""
        integration_points = {
            "bootstrap_atomic": {
                "file": self.emergent_os / "one_kernel" / "bootstrap.py",
                "pattern": "atomic_archistration"
            },
            "cicd_initialization": {
                "file": self.repos_dir / ".github" / "workflows" / "deploy-guardian-services.yml",
                "pattern": "initialize_convergence_system"
            },
            "guardian_swarm": {
                "file": self.emergent_os / "synthesis" / "guardian_swarm_unification.py",
                "pattern": "get_guardian_swarm"
            }
        }
        
        frictionless_count = 0
        total_points = len(integration_points)
        
        for point_name, point_data in integration_points.items():
            if point_data["file"].exists():
                content = self._read_file(point_data["file"])
                if point_data["pattern"] in content:
                    frictionless_count += 1
        
        frictionless_score = frictionless_count / total_points if total_points > 0 else 0.0
        
        status = ValidationStatus.PASS.value if frictionless_score >= 0.8 else ValidationStatus.WARN.value if frictionless_score >= 0.6 else ValidationStatus.FAIL.value
        
        details = [
            f"Score: {frictionless_score:.2%}",
            f"Integration Points: {frictionless_count}/{total_points}"
        ]
        
        return {'status': status, 'details': details, 'frictionless_score': frictionless_score}
    
    def _check_code_quality(self) -> Dict[str, Any]:
        """Validate code quality (YAGNI, KISS, DRY)"""
        code_quality_issues = []
        
        # Check guardian services
        sample_service = self.repos_dir / "guardian-zero-service" / "service.py"
        if sample_service.exists():
            content = self._read_file(sample_service)
            
            if content.count("if") > 20:
                code_quality_issues.append("Too many conditionals (YAGNI violation)")
            if content.count("print(") > 10:
                code_quality_issues.append("Too many print statements (DRY violation)")
        
        # Check bootstrap
        bootstrap_file = self.emergent_os / "one_kernel" / "bootstrap.py"
        if bootstrap_file.exists():
            content = self._read_file(bootstrap_file)
            
            if "Phase" not in content or content.count("Phase") < 8:
                code_quality_issues.append("Bootstrap lacks clear phase structure")
        
        quality_score = 1.0 - (len(code_quality_issues) * 0.1)
        quality_score = max(0.0, min(1.0, quality_score))
        
        status = ValidationStatus.PASS.value if quality_score >= 0.8 else ValidationStatus.WARN.value if quality_score >= 0.6 else ValidationStatus.FAIL.value
        
        details = [f"Quality Score: {quality_score:.2%}"]
        if code_quality_issues:
            details.extend([f"Issue: {issue}" for issue in code_quality_issues])
        else:
            details.append("No issues found")
        
        return {'status': status, 'details': details, 'quality_score': quality_score, 'issues': code_quality_issues}


def main():
    """CLI Entry Point - UNIFIED BASE CLASS"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Elegance Frictionless Validator - UNIFIED BASE CLASS")
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    
    args = parser.parse_args()
    
    validator = EleganceFrictionlessValidator(Path(args.workspace) if args.workspace else None)
    results = validator.run()
    
    if args.output:
        Path(args.output).write_text(json.dumps(results, indent=2, default=str))
        print(f"\n Saved: {args.output}")
    
    sys.exit(0 if results['summary']['score'] >= 80 else 1 if results['summary']['score'] >= 60 else 2)


if __name__ == "__main__":
    main()
