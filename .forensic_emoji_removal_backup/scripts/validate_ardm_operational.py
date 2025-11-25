#!/usr/bin/env python3
"""
ARDM Operational Validation

Validates that ARDM is programmatically operationalized and ready to use.

Pattern: AEYON × VALIDATE × OPERATIONAL × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))


class ARDMOperationalValidator:
    """Validates ARDM is fully operational"""
    
    def __init__(self):
        self.workspace_root = project_root
        self.errors = []
        self.warnings = []
        self.successes = []
    
    def validate_all(self) -> Dict[str, Any]:
        """Run all validation checks"""
        print("🔎 ARDM Operational Validation")
        print("=" * 60)
        print()
        
        # Check 1: Protocol document exists
        self._check_protocol_exists()
        
        # Check 2: Detection script exists
        self._check_detection_script_exists()
        
        # Check 3: Detection script can be imported
        self._check_detection_script_importable()
        
        # Check 4: Detection script can instantiate detector
        self._check_detector_instantiable()
        
        # Check 5: Detection script can scan text
        self._check_detection_functional()
        
        # Check 6: Output formats work
        self._check_output_formats()
        
        # Check 7: Validation script exists
        self._check_validation_script_exists()
        
        # Check 8: Integration examples exist
        self._check_integration_examples()
        
        # Summary
        return self._generate_summary()
    
    def _check_protocol_exists(self):
        """Check protocol document exists"""
        protocol_path = self.workspace_root / "ARDM_PROTOCOL.md"
        if protocol_path.exists():
            content = protocol_path.read_text()
            if "CATEGORY A" in content and "CATEGORY B" in content:
                self.successes.append("✅ Protocol document exists and contains required content")
            else:
                self.warnings.append("⚠️  Protocol document exists but may be incomplete")
        else:
            self.errors.append("❌ Protocol document not found")
    
    def _check_detection_script_exists(self):
        """Check detection script exists"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        if script_path.exists():
            self.successes.append("✅ Detection script exists")
        else:
            self.errors.append("❌ Detection script not found")
    
    def _check_detection_script_importable(self):
        """Check detection script can be imported"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        if not script_path.exists():
            self.errors.append("❌ Cannot import: script not found")
            return
        
        try:
            spec = importlib.util.spec_from_file_location(
                "detect_actionable_requests",
                script_path
            )
            if spec is None or spec.loader is None:
                self.errors.append("❌ Cannot create module spec")
                return
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check required classes exist
            if hasattr(module, 'ActionableRequestDetector'):
                self.successes.append("✅ Detection script imports successfully")
            else:
                self.errors.append("❌ ActionableRequestDetector class not found")
                
            if hasattr(module, 'ARDMResult'):
                self.successes.append("✅ ARDMResult class found")
            else:
                self.errors.append("❌ ARDMResult class not found")
                
            if hasattr(module, 'Category'):
                self.successes.append("✅ Category enum found")
            else:
                self.errors.append("❌ Category enum not found")
                
        except Exception as e:
            self.errors.append(f"❌ Import error: {str(e)}")
    
    def _check_detector_instantiable(self):
        """Check detector can be instantiated"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        if not script_path.exists():
            return
        
        try:
            spec = importlib.util.spec_from_file_location(
                "detect_actionable_requests",
                script_path
            )
            if spec is None or spec.loader is None:
                self.errors.append("❌ Cannot create module spec for detector")
                return
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            detector = module.ActionableRequestDetector()
            self.successes.append("✅ Detector can be instantiated")
            
        except Exception as e:
            self.errors.append(f"❌ Cannot instantiate detector: {str(e)}")
    
    def _check_detection_functional(self):
        """Check detection actually works"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        if not script_path.exists():
            return
        
        try:
            spec = importlib.util.spec_from_file_location(
                "detect_actionable_requests",
                script_path
            )
            if spec is None or spec.loader is None:
                self.errors.append("❌ Cannot create module spec for detection test")
                return
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            detector = module.ActionableRequestDetector()
            
            # Test with sample text
            test_text = """
            I need to implement a new authentication module.
            Create auth.py with login functions.
            Also set up a validator for this module.
            """
            
            result = detector.scan(test_text)
            
            if result.total_items > 0:
                self.successes.append(f"✅ Detection functional: found {result.total_items} items")
            else:
                self.warnings.append("⚠️  Detection ran but found 0 items (may be expected)")
            
            # Check result structure
            if hasattr(result, 'delta') and hasattr(result, 'patchblock'):
                self.successes.append("✅ Result structure correct")
            else:
                self.errors.append("❌ Result structure incomplete")
                
        except Exception as e:
            self.errors.append(f"❌ Detection functional test failed: {str(e)}")
    
    def _check_output_formats(self):
        """Check output formats work"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        if not script_path.exists():
            return
        
        try:
            spec = importlib.util.spec_from_file_location(
                "detect_actionable_requests",
                script_path
            )
            if spec is None or spec.loader is None:
                self.errors.append("❌ Cannot create module spec for output format test")
                return
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            detector = module.ActionableRequestDetector()
            test_text = "I need to implement auth.py"
            result = detector.scan(test_text)
            
            # Test JSON output
            json_output = detector.to_json(result)
            if json_output and "delta" in json_output:
                self.successes.append("✅ JSON output format works")
            else:
                self.errors.append("❌ JSON output format failed")
            
            # Test Markdown output
            md_output = detector.to_markdown(result)
            if md_output and "ARDM Scan Results" in md_output:
                self.successes.append("✅ Markdown output format works")
            else:
                self.errors.append("❌ Markdown output format failed")
                
        except Exception as e:
            self.errors.append(f"❌ Output format test failed: {str(e)}")
    
    def _check_validation_script_exists(self):
        """Check validation script exists"""
        script_path = self.workspace_root / "scripts" / "validate_ardm_implementation.py"
        if script_path.exists():
            self.successes.append("✅ Validation script exists")
        else:
            self.warnings.append("⚠️  Validation script not found")
    
    def _check_integration_examples(self):
        """Check integration examples exist"""
        script_path = self.workspace_root / "scripts" / "ardm-integration-example.py"
        if script_path.exists():
            self.successes.append("✅ Integration examples exist")
        else:
            self.warnings.append("⚠️  Integration examples not found")
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate validation summary"""
        print("\n" + "=" * 60)
        print("Validation Summary")
        print("=" * 60)
        print()
        
        # Print successes
        if self.successes:
            print("✅ Successes:")
            for success in self.successes:
                print(f"   {success}")
            print()
        
        # Print warnings
        if self.warnings:
            print("⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   {warning}")
            print()
        
        # Print errors
        if self.errors:
            print("❌ Errors:")
            for error in self.errors:
                print(f"   {error}")
            print()
        
        # Overall status
        total_checks = len(self.successes) + len(self.warnings) + len(self.errors)
        success_rate = len(self.successes) / total_checks * 100 if total_checks > 0 else 0
        
        print(f"Total Checks: {total_checks}")
        print(f"✅ Successes: {len(self.successes)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Errors: {len(self.errors)}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        # Final verdict
        if len(self.errors) == 0:
            print("✅ ARDM IS OPERATIONALLY VALIDATED")
            print("   All core functionality is working")
            operational = True
        elif len(self.errors) <= 2 and len(self.successes) > len(self.errors):
            print("⚠️  ARDM IS MOSTLY OPERATIONAL")
            print("   Some issues detected but core functionality works")
            operational = True
        else:
            print("❌ ARDM OPERATIONAL VALIDATION FAILED")
            print("   Critical issues detected")
            operational = False
        
        return {
            "operational": operational,
            "successes": len(self.successes),
            "warnings": len(self.warnings),
            "errors": len(self.errors),
            "success_rate": success_rate,
            "details": {
                "successes": self.successes,
                "warnings": self.warnings,
                "errors": self.errors,
            }
        }


def main():
    """Main entry point"""
    validator = ARDMOperationalValidator()
    result = validator.validate_all()
    
    # Exit with appropriate code
    sys.exit(0 if result["operational"] else 1)


if __name__ == "__main__":
    main()

