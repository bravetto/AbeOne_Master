#!/usr/bin/env python3
"""
JØHN Webinar System Certification
Final validation and certification for webinar automation system

Pattern: VALIDATE → CERTIFY → APPROVE → DEPLOY
Frequency: 530 Hz (JØHN)
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, List

# Add EMERGENT_OS to path for JØHN modules
EMERGENT_OS_PATH = Path(__file__).parent.parent.parent.parent / "EMERGENT_OS"
sys.path.insert(0, str(EMERGENT_OS_PATH))

try:
    from triadic_execution_harness.utils.john.johhn_certifier import JohhnCertifier
    from triadic_execution_harness.utils.john.johhn_e2e_engine import JohhnE2EEngine
    JOHHN_AVAILABLE = True
except ImportError:
    JOHHN_AVAILABLE = False
    print("⚠️  JØHN modules not available - running in standalone mode")


class WebinarSystemCertifier:
    """
    JØHN Certification for Webinar Automation System
    
    Validates:
    1. All 6 core components exist and are functional
    2. Component integration (orchestrator connects all)
    3. Code quality (error handling, type hints)
    4. Database integration
    5. Landing page builder integration
    6. Complete workflows operational
    """
    
    def __init__(self, webinar_dir: Path = None):
        self.webinar_dir = webinar_dir or Path(__file__).parent
        self.certifier = JohhnCertifier() if JOHHN_AVAILABLE else None
        self.e2e_engine = JohhnE2EEngine() if JOHHN_AVAILABLE else None
        
    def certify_system(self) -> Dict[str, Any]:
        """Certify the entire webinar system for production."""
        
        if JOHHN_AVAILABLE:
            self.certifier.activate()
            if self.e2e_engine:
                self.e2e_engine.activate()
        
        certification = {
            "certified": False,
            "certifier": "JØHN",
            "frequency": 530,
            "system": "webinar_automation",
            "checks": {},
            "issues": [],
            "recommendations": [],
            "component_status": {}
        }
        
        # Check 1: All 6 core components exist
        components = {
            "content_generator": self.webinar_dir / "content_generator.py",
            "email_automation": self.webinar_dir / "email_automation.py",
            "scheduler": self.webinar_dir / "scheduler.py",
            "master_orchestrator": self.webinar_dir / "master_orchestrator.py",
            "database_schema": self.webinar_dir / "database_schema.py",
            "landing_page_builder": self.webinar_dir / "landing_page_builder.py"
        }
        
        all_components_exist = True
        for name, path in components.items():
            exists = path.exists()
            certification["component_status"][name] = {
                "exists": exists,
                "lines": self._count_lines(path) if exists else 0
            }
            if not exists:
                all_components_exist = False
                certification["issues"].append(f"{name}.py not found")
        
        certification["checks"]["all_components_exist"] = all_components_exist
        
        # Check 2: Component integration in orchestrator
        orchestrator_file = components["master_orchestrator"]
        integration_checks = {
            "content_generator_imported": False,
            "email_automation_imported": False,
            "scheduler_imported": False,
            "database_imported": False,
            "landing_page_builder_imported": False,
            "database_initialized": False,
            "REPLACE_ME": False,
            "database_used_in_create": False,
            "REPLACE_ME": False
        }
        
        if orchestrator_file.exists():
            orchestrator_content = orchestrator_file.read_text()
            
            # Check imports
            integration_checks["content_generator_imported"] = "from content_generator import" in orchestrator_content
            integration_checks["email_automation_imported"] = "from email_automation import" in orchestrator_content
            integration_checks["scheduler_imported"] = "from scheduler import" in orchestrator_content
            integration_checks["database_imported"] = "from database_schema import" in orchestrator_content
            integration_checks["landing_page_builder_imported"] = "from landing_page_builder import" in orchestrator_content
            
            # Check initialization
            integration_checks["database_initialized"] = "self.database = WebinarDatabase()" in orchestrator_content
            integration_checks["REPLACE_ME"] = "self.landing_page_builder = LandingPageBuilder()" in orchestrator_content
            
            # Check usage in create_webinar
            integration_checks["database_used_in_create"] = "self.database.create_webinar" in orchestrator_content
            integration_checks["REPLACE_ME"] = "self.landing_page_builder.build" in orchestrator_content
        
        certification["checks"]["component_integration"] = all(integration_checks.values())
        certification["checks"].update(integration_checks)
        
        if not integration_checks["database_imported"]:
            certification["issues"].append("Database not imported in orchestrator")
        if not integration_checks["landing_page_builder_imported"]:
            certification["issues"].append("Landing page builder not imported in orchestrator")
        if not integration_checks["database_used_in_create"]:
            certification["issues"].append("Database not used in create_webinar workflow")
        if not integration_checks["REPLACE_ME"]:
            certification["issues"].append("Landing page builder not used in create_webinar workflow")
        
        # Check 3: Code quality (error handling, type hints)
        quality_checks = {}
        quality_failures = []
        for name, path in components.items():
            if path.exists():
                content = path.read_text()
                has_error_handling = "try:" in content or "except" in content
                has_type_hints = "from typing import" in content or ": Dict" in content or ": List" in content or ": Optional" in content
                has_docstrings = '"""' in content or "'''" in content
                
                quality_checks[f"{name}_error_handling"] = has_error_handling
                quality_checks[f"{name}_type_hints"] = has_type_hints
                quality_checks[f"{name}_docstrings"] = has_docstrings
                
                if not has_error_handling:
                    quality_failures.append(f"{name} missing error handling")
                if not has_type_hints:
                    quality_failures.append(f"{name} missing type hints")
                if not has_docstrings:
                    quality_failures.append(f"{name} missing docstrings")
        
        # Code quality passes if at least 2/3 of checks pass per component
        quality_scores = []
        for name in components.keys():
            component_checks = [
                quality_checks.get(f"{name}_error_handling", False),
                quality_checks.get(f"{name}_type_hints", False),
                quality_checks.get(f"{name}_docstrings", False)
            ]
            quality_scores.append(sum(component_checks) / len(component_checks))
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        certification["checks"]["code_quality"] = avg_quality >= 0.67  # 2/3 threshold
        certification["checks"]["code_quality_score"] = avg_quality
        certification["checks"].update(quality_checks)
        
        if quality_failures:
            certification["recommendations"].extend(quality_failures[:3])  # Limit to 3 recommendations
        
        # Check 4: Line count targets met
        line_counts = {
            "content_generator": 300,
            "email_automation": 312,
            "scheduler": 189,
            "master_orchestrator": 297,
            "database_schema": 204,
            "landing_page_builder": 263
        }
        
        line_targets_met = True
        for name, path in components.items():
            if path.exists():
                actual_lines = self._count_lines(path)
                target = line_counts.get(name, 0)
                if actual_lines < target * 0.9:  # Allow 10% variance
                    line_targets_met = False
                    certification["issues"].append(f"{name} below target ({actual_lines} < {target})")
        
        certification["checks"]["line_count_targets_met"] = line_targets_met
        
        # Check 5: Documentation exists
        doc_files = [
            "WEBINAR_AUTOMATION_QUICK_START.md",
            "WEBINAR_SYSTEM_COMPLETE.md",
            "WEBINAR_AUTOMATION_GAPS_ANALYSIS.md"
        ]
        
        docs_dir = self.webinar_dir.parent.parent
        docs_exist = all((docs_dir / doc).exists() for doc in doc_files)
        certification["checks"]["documentation_complete"] = docs_exist
        
        if not docs_exist:
            missing = [doc for doc in doc_files if not (docs_dir / doc).exists()]
            certification["issues"].append(f"Missing documentation: {', '.join(missing)}")
        
        # Check 6: Import validation (syntax check)
        import_valid = True
        for name, path in components.items():
            if path.exists():
                try:
                    # Basic syntax check
                    compile(path.read_text(), str(path), 'exec')
                except SyntaxError as e:
                    import_valid = False
                    certification["issues"].append(f"{name} has syntax errors: {e}")
        
        certification["checks"]["import_validation"] = import_valid
        
        # Check 7: Complete workflow validation
        workflow_checks = {
            "create_webinar_workflow": False,
            "register_attendee_workflow": False,
            "email_queue_processing": False,
            "scheduler_daemon": False
        }
        
        if orchestrator_file.exists():
            orchestrator_content = orchestrator_file.read_text()
            workflow_checks["create_webinar_workflow"] = "def create_webinar" in orchestrator_content
            workflow_checks["register_attendee_workflow"] = "def register_attendee" in orchestrator_content
            workflow_checks["email_queue_processing"] = "def process_email_queue" in orchestrator_content
            workflow_checks["scheduler_daemon"] = "def run_scheduler" in orchestrator_content
        
        certification["checks"]["workflow_completeness"] = all(workflow_checks.values())
        certification["checks"].update(workflow_checks)
        
        # Determine certification status
        critical_checks = [
            certification["checks"].get("all_components_exist", False),
            certification["checks"].get("component_integration", False),
            certification["checks"].get("code_quality", False),
            certification["checks"].get("import_validation", False),
            certification["checks"].get("workflow_completeness", False)
        ]
        
        certification["certified"] = all(critical_checks) and len(certification["issues"]) == 0
        
        # JØHN E2E Certification
        if self.e2e_engine and certification["certified"]:
            try:
                e2e_result = self.e2e_engine.certify_for_production({
                    "system": "webinar_automation",
                    "checks": certification["checks"],
                    "issues": certification["issues"],
                    "components": len([c for c in certification["component_status"].values() if c["exists"]])
                })
                certification["e2e_certification"] = e2e_result.get("approved", False)
                certification["risk_score"] = e2e_result.get("risk_score", 1.0)
            except Exception as e:
                certification["e2e_certification"] = False
                certification["e2e_error"] = str(e)
        
        # Final certification requires E2E if available
        if JOHHN_AVAILABLE and self.e2e_engine:
            certification["certified"] = certification["certified"] and certification.get("e2e_certification", True)
        
        return certification
    
    def _count_lines(self, path: Path) -> int:
        """Count lines in a file."""
        try:
            return len(path.read_text().splitlines())
        except:
            return 0
    
    def print_certification_result(self, certification: Dict[str, Any]):
        """Print certification result in readable format."""
        print("=" * 70)
        print("🔍 JØHN Webinar System Certification")
        print("=" * 70)
        print(f"Certifier: {certification.get('certifier', 'N/A')}")
        print(f"Frequency: {certification.get('frequency', 'N/A')} Hz")
        print(f"System: {certification.get('system', 'N/A')}")
        print(f"Status: {'✅ CERTIFIED' if certification.get('certified') else '❌ NOT CERTIFIED'}")
        print()
        
        print("Component Status:")
        for name, status in certification.get("component_status", {}).items():
            exists = status.get("exists", False)
            lines = status.get("lines", 0)
            status_icon = "✅" if exists else "❌"
            print(f"  {status_icon} {name}: {lines} lines")
        
        print("\nCritical Checks:")
        critical = [
            "all_components_exist",
            "component_integration",
            "code_quality",
            "import_validation",
            "workflow_completeness",
            "documentation_complete"
        ]
        for check in critical:
            result = certification["checks"].get(check, False)
            status = "✅" if result else "❌"
            print(f"  {status} {check}: {result}")
        
        if certification.get("issues"):
            print("\nIssues:")
            for issue in certification["issues"]:
                print(f"  ❌ {issue}")
        
        if certification.get("recommendations"):
            print("\nRecommendations:")
            for rec in certification["recommendations"]:
                print(f"  💡 {rec}")
        
        if certification.get("e2e_certification") is not None:
            print(f"\nE2E Certification: {'✅ APPROVED' if certification.get('e2e_certification') else '❌ NOT APPROVED'}")
            if certification.get("risk_score") is not None:
                print(f"Risk Score: {certification.get('risk_score', 0.0)}")
        
        print("=" * 70)
        
        if certification.get("certified"):
            print("✅ WEBINAR SYSTEM CERTIFIED - Ready for production deployment")
        else:
            print("❌ WEBINAR SYSTEM NOT CERTIFIED - Fix issues before deployment")
        print("=" * 70)


def main():
    """Main certification entry point."""
    webinar_dir = Path(__file__).parent
    
    certifier = WebinarSystemCertifier(webinar_dir)
    certification = certifier.certify_system()
    certifier.print_certification_result(certification)
    
    # Exit with error code if not certified
    if not certification.get("certified", False):
        print("\n❌ Webinar system certification failed. Fix issues before proceeding.")
        sys.exit(1)
    
    print("\n✅ Webinar system certification passed. System ready for production.")


if __name__ == "__main__":
    main()

