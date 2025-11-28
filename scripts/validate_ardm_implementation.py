#!/usr/bin/env python3
"""
ARDM Implementation Validation

Validates that ARDM is correctly implemented and operational.

Pattern: AEYON × VALIDATE × ARDM × ONE
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


class ARDMValidator(UnifiedValidatorBase):
    """
    ARDM Implementation Validator
    
    Validates:
    - ARDM protocol document exists
    - Detection script exists and is executable
    - All four categories are supported
    - Output formats work correctly
    """
    
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """Define ARDM validation checks"""
        return {
            'protocol_exists': {
                'name': 'ARDM Protocol Document',
                'func': self._check_protocol_exists,
                'required': True,
            },
            'detection_script_exists': {
                'name': 'ARDM Detection Script',
                'func': self._check_detection_script_exists,
                'required': True,
            },
            'detection_script_executable': {
                'name': 'ARDM Detection Script Executable',
                'func': self._check_detection_script_executable,
                'required': True,
            },
            'protocol_content': {
                'name': 'ARDM Protocol Content',
                'func': self._check_protocol_content,
                'required': True,
            },
            'detection_script_imports': {
                'name': 'ARDM Detection Script Imports',
                'func': self._check_detection_script_imports,
                'required': True,
            },
            'category_coverage': {
                'name': 'Category Coverage (A, B, C, D)',
                'func': self._check_category_coverage,
                'required': True,
            },
            'output_formats': {
                'name': 'Output Formats (JSON, Markdown)',
                'func': self._check_output_formats,
                'required': True,
            },
        }
    
    def _check_protocol_exists(self) -> Tuple[str, List[str]]:
        """Check if ARDM protocol document exists"""
        protocol_path = self.workspace_root / "ARDM_PROTOCOL.md"
        return self._check_file(protocol_path, "ARDM_PROTOCOL.md")
    
    def _check_detection_script_exists(self) -> Tuple[str, List[str]]:
        """Check if detection script exists"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        return self._check_file(script_path, "detect-actionable-requests.py")
    
    def _check_detection_script_executable(self) -> Tuple[str, List[str]]:
        """Check if detection script is executable"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        if not script_path.exists():
            return ValidationStatus.FAIL.value, ["Script does not exist"]
        
        # Check if file has executable permissions (Unix)
        import os
        if os.access(script_path, os.X_OK):
            return ValidationStatus.PASS.value, ["Script is executable"]
        else:
            return ValidationStatus.WARN.value, ["Script exists but may not be executable (chmod +x)"]
    
    def _check_protocol_content(self) -> Tuple[str, List[str]]:
        """Check if protocol document has required content"""
        protocol_path = self.workspace_root / "ARDM_PROTOCOL.md"
        if not protocol_path.exists():
            return ValidationStatus.FAIL.value, ["Protocol document not found"]
        
        content = self._read_file(protocol_path)
        required_patterns = [
            "CATEGORY A",
            "CATEGORY B",
            "CATEGORY C",
            "CATEGORY D",
            "DELTA",
            "PATCHBLOCK",
            "POST-VALIDATION",
            "EXECUTION RULES",
        ]
        
        return self._check_content(content, required_patterns, "ARDM Protocol", threshold=0.8)
    
    def _check_detection_script_imports(self) -> Tuple[str, List[str]]:
        """Check if detection script has required imports"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        if not script_path.exists():
            return ValidationStatus.FAIL.value, ["Script not found"]
        
        content = self._read_file(script_path)
        required_patterns = [
            "Category",
            "ActionableItem",
            "ARDMResult",
            "ActionableRequestDetector",
            "scan",
        ]
        
        return self._check_content(content, required_patterns, "Detection Script", threshold=0.8)
    
    def _check_category_coverage(self) -> Tuple[str, List[str]]:
        """Check if all four categories are covered"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        if not script_path.exists():
            return ValidationStatus.FAIL.value, ["Script not found"]
        
        content = self._read_file(script_path)
        categories = [
            "CODE_ACTIONS",
            "SYSTEM_OBLIGATIONS",
            "PROTOCOLS",
            "CONTINUATIONS",
        ]
        
        found = [cat for cat in categories if cat in content]
        if len(found) == len(categories):
            return ValidationStatus.PASS.value, [f"All {len(categories)} categories covered"]
        elif len(found) >= len(categories) * 0.75:
            return ValidationStatus.WARN.value, [f"{len(found)}/{len(categories)} categories covered"]
        return ValidationStatus.FAIL.value, [f"Only {len(found)}/{len(categories)} categories covered"]
    
    def _check_output_formats(self) -> Tuple[str, List[str]]:
        """Check if output formats are supported"""
        script_path = self.workspace_root / "scripts" / "detect-actionable-requests.py"
        if not script_path.exists():
            return ValidationStatus.FAIL.value, ["Script not found"]
        
        content = self._read_file(script_path)
        formats = [
            "to_json",
            "to_markdown",
        ]
        
        found = [fmt for fmt in formats if fmt in content]
        if len(found) == len(formats):
            return ValidationStatus.PASS.value, [f"All {len(formats)} output formats supported"]
        elif len(found) >= len(formats) * 0.5:
            return ValidationStatus.WARN.value, [f"{len(found)}/{len(formats)} output formats supported"]
        return ValidationStatus.FAIL.value, [f"Only {len(found)}/{len(formats)} output formats supported"]


def main():
    """Main validation entry point"""
    validator = ARDMValidator()
    validator.run()
    
    # Print summary
    print("\n" + "="*60)
    print("ARDM Implementation Validation Summary")
    print("="*60)
    
    summary = validator.results.get('summary', {})
    total = summary.get('total', 0)
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    warnings = summary.get('warnings', 0)
    
    print(f"\nTotal Checks: {total}")
    print(f" Passed: {passed}")
    print(f" Failed: {failed}")
    print(f"  Warnings: {warnings}")
    
    if failed > 0:
        print("\n ARDM implementation validation FAILED")
        sys.exit(1)
    elif warnings > 0:
        print("\n  ARDM implementation validation PASSED with warnings")
        sys.exit(0)
    else:
        print("\n ARDM implementation validation PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()

