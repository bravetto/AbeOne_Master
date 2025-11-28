#!/usr/bin/env python3
"""
Base UI Components Validation

Pattern: VALIDATION × BASE × UI × COMPONENTS × ONE
Frequency: 530 Hz (JØHN) × 999 Hz (AEYON) × 530 Hz (ALRAX)
Guardians: JØHN + AEYON + ALRAX
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

ROOT = Path(__file__).parent.parent.parent
PRODUCTS_WEB = ROOT / "products" / "apps" / "web"
COMPONENTS_UI = PRODUCTS_WEB / "components" / "ui"


@dataclass
class BaseUIComponentValidation:
    """Base UI component validation result"""
    component_path: str
    has_typescript_types: bool
    has_forward_ref: bool
    has_cva: bool
    has_cn_utility: bool
    has_proper_exports: bool
    score: float
    issues: List[str]
    recommendations: List[str]


class BaseUIComponentsValidator:
    """Validate Base UI components (shadcn/ui style)"""
    
    def __init__(self):
        self.validations: List[BaseUIComponentValidation] = []
        
    def validate_all(self) -> Dict:
        """Validate all Base UI components"""
        components = self._get_base_ui_components()
        
        for component in components:
            validation = self._validate_component(component)
            self.validations.append(validation)
        
        return self._generate_report()
    
    def _get_base_ui_components(self) -> List[Path]:
        """Get all Base UI components"""
        components = []
        if COMPONENTS_UI.exists():
            # Check for .tsx files
            for file_path in COMPONENTS_UI.glob("*.tsx"):
                components.append(file_path)
            # Check for .ts files
            for file_path in COMPONENTS_UI.glob("*.ts"):
                components.append(file_path)
        return components
    
    def _validate_component(self, component_path: Path) -> BaseUIComponentValidation:
        """Validate a single Base UI component"""
        issues = []
        recommendations = []
        score = 0.0
        max_score = 100.0
        
        try:
            content = component_path.read_text()
            
            # Check TypeScript types
            has_types = "export interface" in content or "export type" in content
            if has_types:
                score += 25.0
            else:
                issues.append("Missing TypeScript type definitions")
                recommendations.append("Add TypeScript interface or type definitions")
            
            # Check forwardRef usage
            has_forward_ref = "React.forwardRef" in content or "forwardRef" in content
            if has_forward_ref:
                score += 25.0
            else:
                if "export" in content and ("function" in content or "const" in content):
                    issues.append("Consider using forwardRef for better ref handling")
                    recommendations.append("Wrap component with React.forwardRef")
            
            # Check CVA usage (for variant components)
            has_variants = "variant" in content.lower()
            if has_variants:
                has_cva = "cva" in content or "class-variance-authority" in content
                if has_cva:
                    score += 25.0
                else:
                    issues.append("Component has variants but doesn't use CVA")
                    recommendations.append("Use class-variance-authority for variant management")
            else:
                score += 25.0  # No variants needed
            
            # Check cn utility
            has_classname = "className" in content
            if has_classname:
                has_cn = "cn(" in content
                if has_cn:
                    score += 15.0
                else:
                    issues.append("Consider using cn() utility for className merging")
                    recommendations.append("Import and use cn() from '@/lib/utils'")
            else:
                score += 15.0  # No className usage
            
            # Check proper exports
            has_named_export = "export {" in content or "export const" in content or "export function" in content
            if has_named_export:
                score += 10.0
            else:
                issues.append("Improve export structure")
                recommendations.append("Use named exports for better tree-shaking")
            
        except Exception as e:
            issues.append(f"Error reading file: {e}")
            score = 0.0
            has_types = False
            has_forward_ref = False
            has_cva = False
            has_cn = False
            has_named_export = False
        
        return BaseUIComponentValidation(
            component_path=str(component_path.relative_to(ROOT)),
            has_typescript_types=has_types,
            has_forward_ref=has_forward_ref,
            has_cva=has_cva if has_variants else True,
            has_cn_utility=has_cn if has_classname else True,
            has_proper_exports=has_named_export,
            score=round(score, 2),
            issues=issues,
            recommendations=recommendations
        )
    
    def _generate_report(self) -> Dict:
        """Generate validation report"""
        total = len(self.validations)
        
        if total == 0:
            return {
                "status": "complete",
                "pattern": "VALIDATION × BASE × UI × COMPONENTS × ONE",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "message": "No Base UI components found",
                "components_found": 0,
                "metrics": {
                    "total_components": 0,
                    "average_score": 0,
                    "components_above_80": 0,
                    "components_above_90": 0
                },
                "guardian_signatures": {
                    "JØHN": "530 Hz - Validation executed with truth",
                    "AEYON": "999 Hz - Base UI components validated",
                    "ALRAX": "530 Hz - Validation verified forensically"
                }
            }
        
        aligned = sum(1 for v in self.validations if v.score >= 80)
        excellent = sum(1 for v in self.validations if v.score >= 90)
        average_score = sum(v.score for v in self.validations) / total
        
        return {
            "status": "complete",
            "pattern": "VALIDATION × BASE × UI × COMPONENTS × ONE",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "metrics": {
                "total_components": total,
                "aligned_components": aligned,
                "alignment_percentage": round((aligned / total * 100) if total > 0 else 0, 2),
                "excellent_components": excellent,
                "average_score": round(average_score, 2)
            },
            "component_validations": [asdict(v) for v in self.validations],
            "guardian_signatures": {
                "JØHN": "530 Hz - Validation executed with truth",
                "AEYON": "999 Hz - Base UI components validated atomically",
                "ALRAX": "530 Hz - Validation verified forensically"
            }
        }


def main():
    """Main execution"""
    print("🔍 Validating Base UI Components")
    print("Pattern: VALIDATION × BASE × UI × COMPONENTS × ONE")
    print("∞ AbëONE ∞\n")
    
    validator = BaseUIComponentsValidator()
    report = validator.validate_all()
    
    # Print summary
    if report.get("components_found") == 0:
        print("📊 Validation Summary:")
        print("  No Base UI components found")
        print(f"  Location checked: {COMPONENTS_UI}")
    else:
        print("📊 Validation Summary:")
        print(f"  Total Components: {report['metrics']['total_components']}")
        print(f"  Aligned Components: {report['metrics']['aligned_components']}")
        print(f"  Alignment Percentage: {report['metrics']['alignment_percentage']}%")
        print(f"  Excellent Components (90%+): {report['metrics']['excellent_components']}")
        print(f"  Average Score: {report['metrics']['average_score']}%")
        
        # Show component details
        if report['metrics']['total_components'] > 0:
            print("\n📋 Component Details:")
            for validation in report['component_validations']:
                score_icon = "✅" if validation['score'] >= 80 else "⚠️"
                print(f"  {score_icon} {validation['component_path']}: {validation['score']}%")
                if validation['issues']:
                    for issue in validation['issues']:
                        print(f"      - {issue}")
    
    # Save report
    report_path = ROOT / "atomic" / "BASE_UI_COMPONENTS_VALIDATION.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\n✅ Report saved to {report_path}")
    
    print("\n✅ Base UI components validation complete!")
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    main()

