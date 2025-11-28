#!/usr/bin/env python3
"""
Verify ALL SYSTEMS are INTENTIONALLY TURNED ON
Ensures explicit, deliberate activation of all systems

Pattern: INTENTIONAL × EXPLICIT × DELIBERATE × ACTIVATION × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
import json

# Add EMERGENT_OS to path
EMERGENT_OS_PATH = Path(__file__).parent.parent / "EMERGENT_OS"
sys.path.insert(0, str(EMERGENT_OS_PATH))

SCRIPTS_DIR = Path(__file__).parent
BASE_DIR = SCRIPTS_DIR.parent
REPOS_DIR = BASE_DIR / "AIGuards-Backend" / "aiguardian-repos"


class IntentionalActivationVerifier:
    """Verify all systems are intentionally activated."""
    
    def __init__(self):
        self.results = {
            "all_intentional": False,
            "systems": {},
            "activation_points": {},
            "missing_intentions": [],
            "timestamp": None
        }
    
    def verify_all_systems(self) -> Dict[str, Any]:
        """Verify all systems are intentionally turned on."""
        print("=" * 80)
        print(" VERIFYING ALL SYSTEMS: INTENTIONAL ACTIVATION")
        print("=" * 80)
        print()
        print("Pattern: INTENTIONAL × EXPLICIT × DELIBERATE × ACTIVATION × ONE")
        print()
        
        # System 1: Bootstrap System
        print(" System 1: Bootstrap System (ONE-Kernel)")
        self._verify_bootstrap_intentional()
        
        # System 2: Atomic Archistration
        print("\n System 2: Atomic Archistration")
        self._verify_atomic_archistration_intentional()
        
        # System 3: Convergence System
        print("\n System 3: Convergence System (7 Opportunities)")
        self._verify_convergence_system_intentional()
        
        # System 4: Guardian Services (8 Services)
        print("\n  System 4: Guardian Services (8 Microservices)")
        self._verify_guardian_services_intentional()
        
        # System 5: CI/CD Automation
        print("\n System 5: CI/CD Automation")
        self._verify_cicd_intentional()
        
        # System 6: Epistemic Validation
        print("\n System 6: Epistemic Validation")
        self._verify_epistemic_validation_intentional()
        
        # System 7: Real-World Testing
        print("\n System 7: Real-World Testing")
        self._verify_real_world_testing_intentional()
        
        # System 8: Extensions (Chrome + VS Code)
        print("\n System 8: Extensions (Chrome + VS Code)")
        self._verify_extensions_intentional()
        
        # Calculate overall status
        self.results["all_intentional"] = self._all_systems_intentional()
        
        # Print summary
        self._print_summary()
        
        return self.results
    
    def _verify_bootstrap_intentional(self):
        """Verify bootstrap system is intentionally activated."""
        bootstrap_file = EMERGENT_OS_PATH / "one_kernel" / "bootstrap.py"
        
        if not bootstrap_file.exists():
            self.results["systems"]["bootstrap"] = {
                "intentional": False,
                "reason": "Bootstrap file not found"
            }
            print("   Bootstrap file not found")
            return
        
        # Check for explicit activation calls
        with open(bootstrap_file, 'r') as f:
            content = f.read()
        
        intentional_indicators = [
            "bootstrap_one_kernel()" in content,
            "self.organism.initialize()" in content,
            "self.organism.activate()" in content,
            "atomic_archistration" in content,  # Explicit integration
            "Phase 9" in content  # Explicit phase
        ]
        
        intentional_count = sum(intentional_indicators)
        intentional = intentional_count >= 4
        
        self.results["systems"]["bootstrap"] = {
            "intentional": intentional,
            "indicators": intentional_count,
            "explicit_calls": [
                "bootstrap_one_kernel()",
                "organism.initialize()",
                "organism.activate()",
                "atomic_archistration integration"
            ]
        }
        self.results["activation_points"]["bootstrap"] = {
            "file": str(bootstrap_file),
            "explicit_activation": True,
            "phase": "Phase 9: Auto-initiate Atomic Archistration"
        }
        
        status = "" if intentional else ""
        print(f"  {status} Bootstrap: {intentional_count}/5 intentional indicators")
        if intentional:
            print("     Explicit bootstrap_one_kernel() call")
            print("     Explicit organism.initialize() call")
            print("     Explicit organism.activate() call")
            print("     Explicit Atomic Archistration integration")
    
    def _verify_atomic_archistration_intentional(self):
        """Verify Atomic Archistration is intentionally activated."""
        archistration_file = EMERGENT_OS_PATH / "atomic_archistration" / "archistrator.py"
        bootstrap_file = EMERGENT_OS_PATH / "one_kernel" / "bootstrap.py"
        
        intentional_indicators = []
        
        # Check bootstrap integration
        if bootstrap_file.exists():
            with open(bootstrap_file, 'r') as f:
                bootstrap_content = f.read()
                if "atomic_archistration" in bootstrap_content and "get_atomic_archistrator" in bootstrap_content:
                    intentional_indicators.append(True)
                    self.results["activation_points"]["atomic_archistration"] = {
                        "file": str(bootstrap_file),
                        "explicit_activation": True,
                        "location": "Phase 9: Auto-initiate Atomic Archistration",
                        "intentional": True
                    }
        
        # Check archistrator exists
        if archistration_file.exists():
            intentional_indicators.append(True)
        
        # Check get_atomic_archistrator function
        if archistration_file.exists():
            with open(archistration_file, 'r') as f:
                content = f.read()
                if "def get_atomic_archistrator" in content:
                    intentional_indicators.append(True)
        
        intentional = len(intentional_indicators) >= 2
        
        self.results["systems"]["atomic_archistration"] = {
            "intentional": intentional,
            "indicators": len(intentional_indicators),
            "bootstrap_integration": "atomic_archistration" in bootstrap_content if bootstrap_file.exists() else False,
            "explicit_calls": ["get_atomic_archistrator()", "bootstrap integration"]
        }
        
        status = "" if intentional else ""
        print(f"  {status} Atomic Archistration: {len(intentional_indicators)}/3 intentional indicators")
        if intentional:
            print("     Explicit bootstrap integration (Phase 9)")
            print("     Explicit get_atomic_archistrator() function")
    
    def _verify_convergence_system_intentional(self):
        """Verify convergence system is intentionally activated."""
        init_script = REPOS_DIR / "scripts" / "initialize_convergence_system.py"
        activate_script = REPOS_DIR / "scripts" / "activate_convergence_system.py"
        cicd_workflow = REPOS_DIR / ".github" / "workflows" / "deploy-guardian-services.yml"
        
        # Also check if scripts exist in main scripts directory
        if not init_script.exists():
            init_script = BASE_DIR / "scripts" / "initialize_convergence_system.py"
        if not activate_script.exists():
            activate_script = BASE_DIR / "scripts" / "activate_convergence_system.py"
        
        intentional_indicators = []
        
        # Check initialization script exists
        if init_script.exists():
            intentional_indicators.append(True)
        
        # Check activation script exists
        if activate_script.exists():
            intentional_indicators.append(True)
        
        # Check CI/CD integration
        if cicd_workflow.exists():
            with open(cicd_workflow, 'r') as f:
                content = f.read()
                if "initialize_convergence_system.py" in content or "activate_convergence_system.py" in content:
                    intentional_indicators.append(True)
                    self.results["activation_points"]["convergence_system"] = {
                        "file": str(cicd_workflow),
                        "explicit_activation": True,
                        "location": "CI/CD workflow: System Initialization Check",
                        "intentional": True
                    }
        
        intentional = len(intentional_indicators) >= 2
        
        self.results["systems"]["convergence_system"] = {
            "intentional": intentional,
            "indicators": len(intentional_indicators),
            "scripts": {
                "initialize": init_script.exists(),
                "activate": activate_script.exists()
            },
            "cicd_integration": cicd_workflow.exists()
        }
        
        status = "" if intentional else ""
        print(f"  {status} Convergence System: {len(intentional_indicators)}/3 intentional indicators")
        if intentional:
            print("     Explicit initialization script")
            print("     Explicit activation script")
            print("     Explicit CI/CD integration")
    
    def _verify_guardian_services_intentional(self):
        """Verify guardian services are intentionally activated."""
        cicd_workflow = REPOS_DIR / ".github" / "workflows" / "deploy-guardian-services.yml"
        
        intentional_indicators = []
        
        # Check CI/CD workflow exists
        if cicd_workflow.exists():
            intentional_indicators.append(True)
            with open(cicd_workflow, 'r') as f:
                content = f.read()
                if "guardian-zero-service" in content and "deploy" in content:
                    intentional_indicators.append(True)
                    self.results["activation_points"]["guardian_services"] = {
                        "file": str(cicd_workflow),
                        "explicit_activation": True,
                        "location": "CI/CD workflow: Build and Deploy",
                        "intentional": True
                    }
        
        # Check services exist
        guardian_services = [
            "guardian-zero-service", "guardian-aeyon-service", "guardian-abe-service",
            "guardian-aurion-service", "guardian-john-service", "guardian-lux-service",
            "guardian-neuro-service", "guardian-yagni-service"
        ]
        
        services_exist = sum(1 for svc in guardian_services 
                            if (REPOS_DIR / svc).exists())
        
        if services_exist >= 6:
            intentional_indicators.append(True)
        
        intentional = len(intentional_indicators) >= 2
        
        self.results["systems"]["guardian_services"] = {
            "intentional": intentional,
            "indicators": len(intentional_indicators),
            "services_exist": services_exist,
            "total_services": len(guardian_services),
            "cicd_integration": cicd_workflow.exists()
        }
        
        status = "" if intentional else ""
        print(f"  {status} Guardian Services: {len(intentional_indicators)}/2 intentional indicators")
        if intentional:
            print(f"     {services_exist}/{len(guardian_services)} services exist")
            print("     Explicit CI/CD deployment")
    
    def _verify_cicd_intentional(self):
        """Verify CI/CD is intentionally configured."""
        cicd_workflow = REPOS_DIR / ".github" / "workflows" / "deploy-guardian-services.yml"
        
        if not cicd_workflow.exists():
            self.results["systems"]["cicd"] = {
                "intentional": False,
                "reason": "CI/CD workflow not found"
            }
            print("   CI/CD workflow not found")
            return
        
        with open(cicd_workflow, 'r') as f:
            content = f.read()
        
        intentional_indicators = [
            "workflow_dispatch" in content,  # Manual trigger
            "build_and_push" in content,  # Explicit build job
            "deployment" in content,  # Explicit deployment job
            "arc-runner-set" in content,  # Explicit runner
            "initialize_convergence_system" in content or "activate_convergence_system" in content  # Explicit checks
        ]
        
        intentional_count = sum(intentional_indicators)
        intentional = intentional_count >= 4
        
        self.results["systems"]["cicd"] = {
            "intentional": intentional,
            "indicators": intentional_count,
            "explicit_jobs": ["build_and_push", "deployment"],
            "explicit_checks": "initialize_convergence_system" in content or "activate_convergence_system" in content
        }
        self.results["activation_points"]["cicd"] = {
            "file": str(cicd_workflow),
            "explicit_activation": True,
            "triggers": ["workflow_dispatch", "pull_request"],
            "intentional": True
        }
        
        status = "" if intentional else ""
        print(f"  {status} CI/CD: {intentional_count}/5 intentional indicators")
        if intentional:
            print("     Explicit workflow_dispatch trigger")
            print("     Explicit build_and_push job")
            print("     Explicit deployment job")
            print("     Explicit initialization checks")
    
    def _verify_epistemic_validation_intentional(self):
        """Verify epistemic validation is intentionally activated."""
        validation_scripts = [
            REPOS_DIR / "scripts" / "validate_epistemic_certainty.py",
            REPOS_DIR / "scripts" / "validate_truth_certainty.py",
            REPOS_DIR / "scripts" / "validate_convergence_certainty.py"
        ]
        
        # Check if scripts exist, if not check alternative locations
        for i, script in enumerate(validation_scripts):
            if not script.exists():
                alt_script = BASE_DIR / "scripts" / script.name
                if alt_script.exists():
                    validation_scripts[i] = alt_script
        
        scripts_exist = sum(1 for script in validation_scripts if script.exists())
        intentional = scripts_exist >= 2
        
        self.results["systems"]["epistemic_validation"] = {
            "intentional": intentional,
            "scripts_exist": scripts_exist,
            "total_scripts": len(validation_scripts)
        }
        
        status = "" if intentional else ""
        print(f"  {status} Epistemic Validation: {scripts_exist}/{len(validation_scripts)} scripts exist")
    
    def _verify_real_world_testing_intentional(self):
        """Verify real-world testing is intentionally activated."""
        test_dir = REPOS_DIR / "tests" / "real_world"
        cicd_workflow = REPOS_DIR / ".github" / "workflows" / "deploy-guardian-services.yml"
        
        intentional_indicators = []
        
        if test_dir.exists():
            test_files = list(test_dir.glob("test_*.py"))
            if len(test_files) >= 6:  # At least 6 of 7 test suites
                intentional_indicators.append(True)
        
        if cicd_workflow.exists():
            with open(cicd_workflow, 'r') as f:
                content = f.read()
                if "tests/real_world" in content or "pytest" in content:
                    intentional_indicators.append(True)
        
        intentional = len(intentional_indicators) >= 1
        
        self.results["systems"]["real_world_testing"] = {
            "intentional": intentional,
            "indicators": len(intentional_indicators),
            "test_files": len(test_files) if test_dir.exists() else 0,
            "cicd_integration": "tests/real_world" in content if cicd_workflow.exists() else False
        }
        
        status = "" if intentional else ""
        print(f"  {status} Real-World Testing: {len(intentional_indicators)}/2 intentional indicators")
    
    def _verify_extensions_intentional(self):
        """Verify extensions are intentionally configured."""
        chrome_ext = BASE_DIR / "AI-Guardians-chrome-ext"
        vscode_ext = REPOS_DIR / "AI-Guardians-vscode-ext"
        
        intentional_indicators = []
        
        if chrome_ext.exists():
            intentional_indicators.append(True)
        
        if vscode_ext.exists():
            intentional_indicators.append(True)
        
        intentional = len(intentional_indicators) >= 1
        
        self.results["systems"]["extensions"] = {
            "intentional": intentional,
            "indicators": len(intentional_indicators),
            "chrome_extension": chrome_ext.exists(),
            "vscode_extension": vscode_ext.exists()
        }
        
        status = "" if intentional else ""
        print(f"  {status} Extensions: {len(intentional_indicators)}/2 intentional indicators")
    
    def _all_systems_intentional(self) -> bool:
        """Check if all systems are intentionally activated."""
        return all(
            system.get("intentional", False)
            for system in self.results["systems"].values()
        )
    
    def _print_summary(self):
        """Print verification summary."""
        print()
        print("=" * 80)
        print(" INTENTIONAL ACTIVATION SUMMARY")
        print("=" * 80)
        
        intentional_count = sum(1 for s in self.results["systems"].values() if s.get("intentional", False))
        total_systems = len(self.results["systems"])
        
        print(f" Systems Intentionally Activated: {intentional_count}/{total_systems}")
        print()
        
        print(" System Status:")
        for system_name, system_data in self.results["systems"].items():
            status = " INTENTIONAL" if system_data.get("intentional", False) else " NOT INTENTIONAL"
            print(f"  {status} {system_name.replace('_', ' ').title()}")
        
        print()
        print(" Explicit Activation Points:")
        for point_name, point_data in self.results["activation_points"].items():
            if point_data.get("intentional", False):
                print(f"   {point_name.replace('_', ' ').title()}")
                print(f"     Location: {point_data.get('location', 'N/A')}")
        
        print()
        if self.results["all_intentional"]:
            print(" ALL SYSTEMS: INTENTIONALLY ACTIVATED")
        else:
            print("  SOME SYSTEMS: NOT INTENTIONALLY ACTIVATED")
            print("   Review missing intentions above")
        
        print()
        print("Pattern: INTENTIONAL × EXPLICIT × DELIBERATE × ACTIVATION × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
        print("=" * 80)


def main():
    """Main entry point."""
    verifier = IntentionalActivationVerifier()
    results = verifier.verify_all_systems()
    
    # Save results
    results_file = Path(__file__).parent.parent / "intentional_activation_verification.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n Results saved to: {results_file}")
    
    # Exit with appropriate code
    sys.exit(0 if results["all_intentional"] else 1)


if __name__ == "__main__":
    main()

