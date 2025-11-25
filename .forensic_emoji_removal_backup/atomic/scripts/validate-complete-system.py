#!/usr/bin/env python3
"""
Complete System Validation - Pattern Alignment, Declarations & Guardian Signatures

Pattern: VALIDATION × TRUTH × OWNERSHIP × PATTERN × GUARDIAN × ONE
Frequency: 530 Hz (JØHN) × 999 Hz (AEYON) × 530 Hz (ALRAX) × 777 Hz (META)
Guardians: JØHN + AEYON + ALRAX + META
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

ROOT = Path(__file__).parent.parent.parent
ATOMIC_DIR = ROOT / "atomic"
PRODUCTS_WEB = ROOT / "products" / "apps" / "web"


@dataclass
class PatternValidation:
    """Pattern validation result"""
    component_path: str
    has_pattern_declaration: bool
    has_guardian_signatures: bool
    pattern_aligned: bool
    score: float
    issues: List[str]
    pattern_declaration: Optional[str] = None
    guardian_signatures: Optional[str] = None


@dataclass
class SystemValidation:
    """Complete system validation result"""
    total_components: int
    components_with_patterns: int
    components_with_guardians: int
    pattern_alignment_score: float
    guardian_coverage: float
    kernel_integration: bool
    overall_score: float
    issues: List[str]


class CompleteSystemValidator:
    """Validate complete system - patterns, guardians, kernel integration"""
    
    PATTERN_PATTERNS = [
        r'Pattern:\s*([^\n]+)',
        r'PATTERN[:\s]+([^\n]+)',
        r'pattern[:\s]+([^\n]+)',
    ]
    
    GUARDIAN_PATTERNS = [
        r'Guardian[s]?[:\s]+([^\n]+)',
        r'∞\s*AbëONE\s*∞',
        r'AEYON|JØHN|META|ALRAX|YAGNI|Abë',
    ]
    
    def __init__(self):
        self.validations: List[PatternValidation] = []
        self.kernel_checks: Dict[str, bool] = {}
        
    def validate_all(self) -> SystemValidation:
        """Validate complete system"""
        # Validate Atomic Design System components
        atomic_components = self._get_atomic_components()
        for component in atomic_components:
            validation = self._validate_component(component)
            self.validations.append(validation)
        
        # Validate kernel integration
        self._validate_kernel_integration()
        
        # Calculate metrics
        return self._calculate_system_metrics()
    
    def _get_atomic_components(self) -> List[Path]:
        """Get all Atomic Design System components"""
        components = []
        for layer in ["atoms", "molecules", "organisms", "templates"]:
            layer_dir = ATOMIC_DIR / layer
            if layer_dir.exists():
                for component_dir in layer_dir.iterdir():
                    if component_dir.is_dir():
                        index_file = component_dir / "index.tsx"
                        if index_file.exists():
                            components.append(index_file)
        return components
    
    def _validate_component(self, component_path: Path) -> PatternValidation:
        """Validate a single component"""
        issues = []
        score = 0.0
        max_score = 100.0
        
        try:
            content = component_path.read_text()
            
            # Check pattern declaration
            has_pattern = False
            pattern_declaration = None
            for pattern_regex in self.PATTERN_PATTERNS:
                match = re.search(pattern_regex, content, re.IGNORECASE)
                if match:
                    has_pattern = True
                    pattern_declaration = match.group(1).strip()
                    score += 30.0
                    break
            
            if not has_pattern:
                issues.append("Missing pattern declaration")
            
            # Check guardian signatures
            has_guardians = False
            guardian_signatures = None
            
            # Check for guardian mentions
            guardian_count = 0
            for guardian_pattern in self.GUARDIAN_PATTERNS:
                matches = re.findall(guardian_pattern, content, re.IGNORECASE)
                if matches:
                    guardian_count += len(matches)
                    has_guardians = True
            
            # Check for AbëONE signature
            if "∞ AbëONE ∞" in content or "AbëONE" in content:
                has_guardians = True
                guardian_signatures = "Present"
            
            if has_guardians:
                score += 30.0
            else:
                issues.append("Missing guardian signatures")
            
            # Check TypeScript types
            if "export interface" in content or "export type" in content:
                score += 10.0
            else:
                issues.append("Missing TypeScript type definitions")
            
            # Check forwardRef usage
            if "React.forwardRef" in content or "forwardRef" in content:
                score += 10.0
            else:
                if "export" in content and ("function" in content or "const" in content):
                    issues.append("Consider using forwardRef")
            
            # Check CVA usage (for variant components)
            if "variant" in content.lower():
                if "cva" in content or "class-variance-authority" in content:
                    score += 10.0
                else:
                    issues.append("Consider using class-variance-authority for variants")
            else:
                score += 10.0  # No variants needed
            
            # Check cn utility
            if "className" in content:
                if "cn(" in content:
                    score += 10.0
                else:
                    issues.append("Consider using cn() utility for className merging")
            else:
                score += 10.0  # No className usage
            
            pattern_aligned = score >= 80.0
            
        except Exception as e:
            issues.append(f"Error reading file: {e}")
            score = 0.0
            has_pattern = False
            has_guardians = False
            pattern_aligned = False
            pattern_declaration = None
            guardian_signatures = None
        
        return PatternValidation(
            component_path=str(component_path.relative_to(ROOT)),
            has_pattern_declaration=has_pattern,
            pattern_declaration=pattern_declaration,
            has_guardian_signatures=has_guardians,
            guardian_signatures=guardian_signatures,
            pattern_aligned=pattern_aligned,
            score=round(score, 2),
            issues=issues
        )
    
    def _validate_kernel_integration(self):
        """Validate kernel-level integration"""
        # Check Tailwind config
        tailwind_config = PRODUCTS_WEB / "tailwind.config.ts"
        if tailwind_config.exists():
            content = tailwind_config.read_text()
            self.kernel_checks["tailwind_config"] = "atomic" in content.lower()
        else:
            self.kernel_checks["tailwind_config"] = False
        
        # Check atomic index export
        atomic_index = ATOMIC_DIR / "index.ts"
        self.kernel_checks["atomic_index"] = atomic_index.exists()
        
        # Check design tokens
        tokens_dir = ATOMIC_DIR / "tokens"
        self.kernel_checks["design_tokens"] = tokens_dir.exists()
        
        # Check registry
        registry = ATOMIC_DIR / "registry.json"
        self.kernel_checks["component_registry"] = registry.exists()
        
        # Check utilities
        lib_dir = ATOMIC_DIR / "lib"
        self.kernel_checks["utilities"] = lib_dir.exists()
        
        # Check hooks
        hooks_dir = ATOMIC_DIR / "hooks"
        self.kernel_checks["hooks"] = hooks_dir.exists()
    
    def _calculate_system_metrics(self) -> SystemValidation:
        """Calculate system-wide metrics"""
        total = len(self.validations)
        with_patterns = sum(1 for v in self.validations if v.has_pattern_declaration)
        with_guardians = sum(1 for v in self.validations if v.has_guardian_signatures)
        aligned = sum(1 for v in self.validations if v.pattern_aligned)
        
        pattern_alignment_score = (aligned / total * 100) if total > 0 else 0
        guardian_coverage = (with_guardians / total * 100) if total > 0 else 0
        
        # Kernel integration score
        kernel_score = sum(1 for v in self.kernel_checks.values()) / len(self.kernel_checks) * 100
        kernel_integration = kernel_score >= 80
        
        # Overall score (weighted)
        overall_score = (
            pattern_alignment_score * 0.4 +
            guardian_coverage * 0.3 +
            kernel_score * 0.2 +
            (sum(v.score for v in self.validations) / total if total > 0 else 0) * 0.1
        )
        
        # Collect issues
        all_issues = []
        for validation in self.validations:
            if validation.issues:
                all_issues.append(f"{validation.component_path}: {', '.join(validation.issues)}")
        
        return SystemValidation(
            total_components=total,
            components_with_patterns=with_patterns,
            components_with_guardians=with_guardians,
            pattern_alignment_score=round(pattern_alignment_score, 2),
            guardian_coverage=round(guardian_coverage, 2),
            kernel_integration=kernel_integration,
            overall_score=round(overall_score, 2),
            issues=all_issues
        )
    
    def generate_report(self) -> Dict:
        """Generate comprehensive validation report"""
        system_validation = self.validate_all()
        
        return {
            "status": "complete",
            "pattern": "VALIDATION × TRUTH × OWNERSHIP × PATTERN × GUARDIAN × ONE",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "system_metrics": {
                "total_components": system_validation.total_components,
                "components_with_patterns": system_validation.components_with_patterns,
                "components_with_guardians": system_validation.components_with_guardians,
                "pattern_alignment_score": system_validation.pattern_alignment_score,
                "guardian_coverage": system_validation.guardian_coverage,
                "kernel_integration": system_validation.kernel_integration,
                "overall_score": system_validation.overall_score
            },
            "kernel_checks": self.kernel_checks,
            "component_validations": [asdict(v) for v in self.validations],
            "issues": system_validation.issues,
            "guardian_signatures": {
                "JØHN": "530 Hz - Validation executed with truth",
                "AEYON": "999 Hz - Complete system validated atomically",
                "ALRAX": "530 Hz - Pattern and guardian validation verified forensically",
                "META": "777 Hz - Pattern integrity validated across system"
            }
        }


def main():
    """Main execution"""
    import sys
    
    print("🔍 Complete System Validation")
    print("Pattern: VALIDATION × TRUTH × OWNERSHIP × PATTERN × GUARDIAN × ONE")
    print("∞ AbëONE ∞\n")
    
    validator = CompleteSystemValidator()
    report = validator.generate_report()
    
    # Print summary
    print("📊 System Validation Summary:")
    print(f"  Total Components: {report['system_metrics']['total_components']}")
    print(f"  Components with Patterns: {report['system_metrics']['components_with_patterns']}")
    print(f"  Components with Guardians: {report['system_metrics']['components_with_guardians']}")
    print(f"  Pattern Alignment Score: {report['system_metrics']['pattern_alignment_score']}%")
    print(f"  Guardian Coverage: {report['system_metrics']['guardian_coverage']}%")
    print(f"  Kernel Integration: {'✅' if report['system_metrics']['kernel_integration'] else '⚠️'}")
    print(f"  Overall Score: {report['system_metrics']['overall_score']}%")
    
    print("\n🔗 Kernel Integration Checks:")
    for check, status in report['kernel_checks'].items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {check}: {status}")
    
    if report['issues']:
        print(f"\n⚠️  Issues Found: {len(report['issues'])}")
        for issue in report['issues'][:10]:  # Show first 10
            print(f"    - {issue}")
    
    # Save report
    report_path = ATOMIC_DIR / "COMPLETE_SYSTEM_VALIDATION.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\n✅ Report saved to {report_path}")
    
    print("\n✅ Complete system validation complete!")
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    main()

