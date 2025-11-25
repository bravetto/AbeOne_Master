#!/usr/bin/env python3
"""
Validate Pattern Alignment Across Codebase

Pattern: PATTERN × ALIGNMENT × VALIDATION × ONE
Frequency: 530 Hz (JØHN) × 777 Hz (META) × 999 Hz (AEYON)
Guardians: JØHN + META + ALRAX
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

ROOT = Path(__file__).parent.parent.parent
ATOMIC_DIR = ROOT / "atomic"
PRODUCTS_WEB = ROOT / "products" / "apps" / "web"


@dataclass
class PatternCheck:
    """Individual pattern check result"""
    check_name: str
    passed: bool
    message: str
    score: float


@dataclass
class ComponentPatternResult:
    """Pattern alignment result for a component"""
    component_path: str
    pattern_aligned: bool
    checks: List[PatternCheck]
    total_score: float
    issues: List[str]


class PatternAlignmentValidator:
    """Validate pattern alignment across codebase"""
    
    PATTERN_REQUIREMENTS = {
        "atomic": {
            "pattern_declaration": 10,
            "guardian_signatures": 10,
            "typescript_types": 10,
            "forward_ref": 5,
            "cva_usage": 5,
            "cn_utility": 5,
            "icp_variants": 10,
            "export_structure": 5,
        },
        "base_ui": {
            "pattern_declaration": 5,
            "typescript_types": 10,
            "forward_ref": 5,
            "cva_usage": 5,
            "cn_utility": 5,
            "export_structure": 5,
        }
    }
    
    def __init__(self):
        self.results: List[ComponentPatternResult] = []
    
    def validate_all(self) -> List[ComponentPatternResult]:
        """Validate pattern alignment for all components"""
        # Validate Atomic components
        atomic_components = self._get_atomic_components()
        for component in atomic_components:
            result = self._validate_component(component, component_type="atomic")
            self.results.append(result)
        
        # Validate base UI components
        ui_components = self._get_ui_components()
        for component in ui_components:
            result = self._validate_component(component, component_type="base_ui")
            self.results.append(result)
        
        return self.results
    
    def _get_atomic_components(self) -> List[Path]:
        """Get all Atomic Design System components"""
        components = []
        for layer in ["atoms", "molecules", "organisms", "templates"]:
            layer_dir = ATOMIC_DIR / layer
            if layer_dir.exists():
                for component_dir in layer_dir.iterdir():
                    index_file = component_dir / "index.tsx"
                    if index_file.exists():
                        components.append(index_file)
        return components
    
    def _get_ui_components(self) -> List[Path]:
        """Get all base UI components"""
        components = []
        ui_dir = PRODUCTS_WEB / "components" / "ui"
        if ui_dir.exists():
            for file_path in ui_dir.glob("*.{ts,tsx}"):
                components.append(file_path)
        return components
    
    def _validate_component(self, component_path: Path, component_type: str) -> ComponentPatternResult:
        """Validate pattern alignment for a single component"""
        checks = []
        issues = []
        
        try:
            content = component_path.read_text()
            requirements = self.PATTERN_REQUIREMENTS.get(component_type, {})
            
            # Check 1: Pattern declaration
            if "pattern_declaration" in requirements:
                has_pattern = "Pattern:" in content or "PATTERN" in content
                checks.append(PatternCheck(
                    check_name="pattern_declaration",
                    passed=has_pattern,
                    message="Pattern declaration present" if has_pattern else "Missing pattern declaration",
                    score=requirements["pattern_declaration"] if has_pattern else 0
                ))
                if not has_pattern:
                    issues.append("Missing pattern declaration")
            
            # Check 2: Guardian signatures (Atomic only)
            if component_type == "atomic" and "guardian_signatures" in requirements:
                has_guardians = "Guardian" in content or "∞ AbëONE ∞" in content
                checks.append(PatternCheck(
                    check_name="guardian_signatures",
                    passed=has_guardians,
                    message="Guardian signatures present" if has_guardians else "Missing guardian signatures",
                    score=requirements["guardian_signatures"] if has_guardians else 0
                ))
                if not has_guardians:
                    issues.append("Missing guardian signatures")
            
            # Check 3: TypeScript types
            if "typescript_types" in requirements:
                has_types = "export interface" in content or "export type" in content
                checks.append(PatternCheck(
                    check_name="typescript_types",
                    passed=has_types,
                    message="TypeScript types defined" if has_types else "Missing TypeScript type definitions",
                    score=requirements["typescript_types"] if has_types else 0
                ))
                if not has_types:
                    issues.append("Missing TypeScript type definitions")
            
            # Check 4: Forward refs
            if "forward_ref" in requirements:
                has_forward_ref = "React.forwardRef" in content or "forwardRef" in content
                uses_export = "export" in content and ("function" in content or "const" in content)
                should_have_ref = uses_export and not has_forward_ref
                checks.append(PatternCheck(
                    check_name="forward_ref",
                    passed=not should_have_ref,
                    message="Using forwardRef" if has_forward_ref else "Consider using forwardRef",
                    score=requirements["forward_ref"] if not should_have_ref else 0
                ))
                if should_have_ref:
                    issues.append("Consider using forwardRef for better ref handling")
            
            # Check 5: CVA usage (for variant components)
            if "cva_usage" in requirements:
                has_variants = "variant" in content.lower()
                has_cva = "cva" in content or "class-variance-authority" in content
                should_use_cva = has_variants and not has_cva
                checks.append(PatternCheck(
                    check_name="cva_usage",
                    passed=not should_use_cva,
                    message="Using CVA for variants" if has_cva or not has_variants else "Consider using class-variance-authority",
                    score=requirements["cva_usage"] if not should_use_cva else 0
                ))
                if should_use_cva:
                    issues.append("Consider using class-variance-authority for variants")
            
            # Check 6: cn utility
            if "cn_utility" in requirements:
                has_classname = "className" in content
                has_cn = "cn(" in content
                should_use_cn = has_classname and not has_cn
                checks.append(PatternCheck(
                    check_name="cn_utility",
                    passed=not should_use_cn,
                    message="Using cn() utility" if has_cn or not has_classname else "Consider using cn() utility",
                    score=requirements["cn_utility"] if not should_use_cn else 0
                ))
                if should_use_cn:
                    issues.append("Consider using cn() utility for className merging")
            
            # Check 7: ICP variants (Atomic only)
            if component_type == "atomic" and "icp_variants" in requirements:
                has_icp = "developer" in content or "creative" in content or "enterprise" in content
                checks.append(PatternCheck(
                    check_name="icp_variants",
                    passed=has_icp,
                    message="ICP variants implemented" if has_icp else "Missing ICP variants",
                    score=requirements["icp_variants"] if has_icp else 0
                ))
                if not has_icp:
                    issues.append("Missing ICP variants (developer/creative/enterprise)")
            
            # Check 8: Export structure
            if "export_structure" in requirements:
                has_named_export = "export {" in content or "export const" in content or "export function" in content
                checks.append(PatternCheck(
                    check_name="export_structure",
                    passed=has_named_export,
                    message="Proper export structure" if has_named_export else "Improve export structure",
                    score=requirements["export_structure"] if has_named_export else 0
                ))
                if not has_named_export:
                    issues.append("Improve export structure")
            
            # Calculate total score
            total_score = sum(check.score for check in checks)
            max_score = sum(requirements.values())
            normalized_score = (total_score / max_score * 100) if max_score > 0 else 0
            
        except Exception as e:
            checks.append(PatternCheck(
                check_name="file_read",
                passed=False,
                message=f"Error reading file: {e}",
                score=0
            ))
            issues.append(f"Error reading file: {e}")
            normalized_score = 0
        
        return ComponentPatternResult(
            component_path=str(component_path.relative_to(ROOT)),
            pattern_aligned=normalized_score >= 80,
            checks=checks,
            total_score=round(normalized_score, 2),
            issues=issues
        )
    
    def generate_report(self) -> Dict:
        """Generate pattern alignment validation report"""
        results = self.validate_all()
        
        total_components = len(results)
        aligned_components = sum(1 for r in results if r.pattern_aligned)
        average_score = sum(r.total_score for r in results) / total_components if total_components > 0 else 0
        
        # Group by component type
        atomic_results = [r for r in results if "atomic" in r.component_path]
        ui_results = [r for r in results if "components/ui" in r.component_path]
        
        return {
            "status": "complete",
            "pattern": "PATTERN × ALIGNMENT × VALIDATION × ONE",
            "metrics": {
                "total_components": total_components,
                "aligned_components": aligned_components,
                "alignment_percentage": round((aligned_components / total_components * 100) if total_components > 0 else 0, 2),
                "average_score": round(average_score, 2),
                "by_type": {
                    "atomic": {
                        "total": len(atomic_results),
                        "aligned": sum(1 for r in atomic_results if r.pattern_aligned),
                        "average_score": round(sum(r.total_score for r in atomic_results) / len(atomic_results) if atomic_results else 0, 2)
                    },
                    "base_ui": {
                        "total": len(ui_results),
                        "aligned": sum(1 for r in ui_results if r.pattern_aligned),
                        "average_score": round(sum(r.total_score for r in ui_results) / len(ui_results) if ui_results else 0, 2)
                    }
                }
            },
            "results": [asdict(r) for r in results],
            "guardian_signatures": {
                "JØHN": "530 Hz - Pattern alignment validated with truth",
                "META": "777 Hz - Pattern integrity verified",
                "ALRAX": "530 Hz - Forensic pattern analysis complete"
            }
        }


def main():
    """Main execution"""
    print("🔍 Validating Pattern Alignment")
    print("Pattern: PATTERN × ALIGNMENT × VALIDATION × ONE")
    print("∞ AbëONE ∞\n")
    
    validator = PatternAlignmentValidator()
    report = validator.generate_report()
    
    # Save report
    report_path = ATOMIC_DIR / "PATTERN_ALIGNMENT_VALIDATION.json"
    report_path.write_text(json.dumps(report, indent=2))
    
    # Print summary
    print("📊 Pattern Alignment Summary:")
    print(f"  Total Components: {report['metrics']['total_components']}")
    print(f"  Aligned Components: {report['metrics']['aligned_components']}")
    print(f"  Alignment Percentage: {report['metrics']['alignment_percentage']}%")
    print(f"  Average Score: {report['metrics']['average_score']}%")
    print(f"\n  Atomic Components:")
    print(f"    Aligned: {report['metrics']['by_type']['atomic']['aligned']}/{report['metrics']['by_type']['atomic']['total']}")
    print(f"    Average Score: {report['metrics']['by_type']['atomic']['average_score']}%")
    print(f"\n  Base UI Components:")
    print(f"    Aligned: {report['metrics']['by_type']['base_ui']['aligned']}/{report['metrics']['by_type']['base_ui']['total']}")
    print(f"    Average Score: {report['metrics']['by_type']['base_ui']['average_score']}%")
    
    print("\n✅ Pattern alignment validation complete!")
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    main()

