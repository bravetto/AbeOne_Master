#!/usr/bin/env python3
"""
Ideal State Alignment - Enhance & Pattern Align to Perfect State

Pattern: IDEAL × STATE × ALIGNMENT × ENHANCEMENT × PATTERN × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META) × 530 Hz (Abë)
Guardians: AEYON + JØHN + META + Abë + YAGNI
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
COMPONENTS_UI = PRODUCTS_WEB / "components" / "ui"


@dataclass
class IdealStateAlignment:
    """Ideal state alignment result"""
    component_path: str
    component_type: str  # "atomic" or "base_ui"
    current_score: float
    ideal_score: float
    alignment_gap: float
    enhancements_needed: List[str]
    aligned: bool


class IdealStateAligner:
    """Align components to ideal state"""
    
    IDEAL_STATE_SCORE = 100.0
    
    ATOMIC_REQUIREMENTS = {
        "pattern_declaration": 10.0,
        "guardian_signatures": 10.0,
        "typescript_types": 10.0,
        "forward_ref": 5.0,
        "cva_usage": 5.0,
        "cn_utility": 5.0,
        "icp_variants": 10.0,
        "export_structure": 5.0,
    }
    
    BASE_UI_REQUIREMENTS = {
        "typescript_types": 25.0,
        "forward_ref": 25.0,
        "cva_usage": 25.0,
        "cn_utility": 15.0,
        "export_structure": 10.0,
    }
    
    def __init__(self):
        self.alignments: List[IdealStateAlignment] = []
        
    def align_all(self) -> Dict:
        """Align all components to ideal state"""
        # Align Atomic components
        atomic_components = self._get_atomic_components()
        for component in atomic_components:
            alignment = self._align_component(component, "atomic")
            self.alignments.append(alignment)
        
        # Align Base UI components
        base_ui_components = self._get_base_ui_components()
        for component in base_ui_components:
            alignment = self._align_component(component, "base_ui")
            self.alignments.append(alignment)
        
        return self._generate_report()
    
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
    
    def _get_base_ui_components(self) -> List[Path]:
        """Get all Base UI components"""
        components = []
        if COMPONENTS_UI.exists():
            for file_path in COMPONENTS_UI.glob("*.tsx"):
                components.append(file_path)
            for file_path in COMPONENTS_UI.glob("*.ts"):
                components.append(file_path)
        return components
    
    def _align_component(self, component_path: Path, component_type: str) -> IdealStateAlignment:
        """Align a component to ideal state"""
        try:
            content = component_path.read_text()
            requirements = self.ATOMIC_REQUIREMENTS if component_type == "atomic" else self.BASE_UI_REQUIREMENTS
            
            current_score = 0.0
            enhancements_needed = []
            
            # Check each requirement
            for requirement, points in requirements.items():
                has_requirement = self._check_requirement(content, requirement, component_type)
                if has_requirement:
                    current_score += points
                else:
                    enhancements_needed.append(requirement)
            
            ideal_score = self.IDEAL_STATE_SCORE
            alignment_gap = ideal_score - current_score
            aligned = alignment_gap == 0.0
            
            return IdealStateAlignment(
                component_path=str(component_path.relative_to(ROOT)),
                component_type=component_type,
                current_score=round(current_score, 2),
                ideal_score=ideal_score,
                alignment_gap=round(alignment_gap, 2),
                enhancements_needed=enhancements_needed,
                aligned=aligned
            )
            
        except Exception as e:
            return IdealStateAlignment(
                component_path=str(component_path.relative_to(ROOT)),
                component_type=component_type,
                current_score=0.0,
                ideal_score=self.IDEAL_STATE_SCORE,
                alignment_gap=self.IDEAL_STATE_SCORE,
                enhancements_needed=[f"Error: {e}"],
                aligned=False
            )
    
    def _check_requirement(self, content: str, requirement: str, component_type: str) -> bool:
        """Check if requirement is met"""
        if requirement == "pattern_declaration":
            return "Pattern:" in content or "PATTERN" in content
        
        elif requirement == "guardian_signatures":
            return "Guardian" in content or "∞ AbëONE ∞" in content
        
        elif requirement == "typescript_types":
            return "export interface" in content or "export type" in content
        
        elif requirement == "forward_ref":
            return "React.forwardRef" in content or "forwardRef" in content
        
        elif requirement == "cva_usage":
            if "variant" in content.lower():
                return "cva" in content or "class-variance-authority" in content
            return True  # No variants needed
        
        elif requirement == "cn_utility":
            if "className" in content:
                return "cn(" in content
            return True  # No className usage
        
        elif requirement == "icp_variants":
            return "developer" in content or "creative" in content or "enterprise" in content
        
        elif requirement == "export_structure":
            return "export {" in content or "export const" in content or "export function" in content
        
        return False
    
    def _generate_report(self) -> Dict:
        """Generate ideal state alignment report"""
        total_components = len(self.alignments)
        aligned_components = sum(1 for a in self.alignments if a.aligned)
        total_gap = sum(a.alignment_gap for a in self.alignments)
        average_score = sum(a.current_score for a in self.alignments) / total_components if total_components > 0 else 0
        
        # Group by type
        atomic_alignments = [a for a in self.alignments if a.component_type == "atomic"]
        base_ui_alignments = [a for a in self.alignments if a.component_type == "base_ui"]
        
        atomic_aligned = sum(1 for a in atomic_alignments if a.aligned)
        base_ui_aligned = sum(1 for a in base_ui_alignments if a.aligned)
        
        atomic_avg = sum(a.current_score for a in atomic_alignments) / len(atomic_alignments) if atomic_alignments else 0
        base_ui_avg = sum(a.current_score for a in base_ui_alignments) / len(base_ui_alignments) if base_ui_alignments else 0
        
        return {
            "status": "complete",
            "pattern": "IDEAL × STATE × ALIGNMENT × ENHANCEMENT × PATTERN × ONE",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "ideal_state": {
                "target_score": self.IDEAL_STATE_SCORE,
                "total_components": total_components,
                "aligned_components": aligned_components,
                "alignment_percentage": round((aligned_components / total_components * 100) if total_components > 0 else 0, 2),
                "average_score": round(average_score, 2),
                "total_gap": round(total_gap, 2),
                "average_gap": round(total_gap / total_components if total_components > 0 else 0, 2)
            },
            "by_type": {
                "atomic": {
                    "total": len(atomic_alignments),
                    "aligned": atomic_aligned,
                    "alignment_percentage": round((atomic_aligned / len(atomic_alignments) * 100) if atomic_alignments else 0, 2),
                    "average_score": round(atomic_avg, 2),
                    "average_gap": round(sum(a.alignment_gap for a in atomic_alignments) / len(atomic_alignments) if atomic_alignments else 0, 2)
                },
                "base_ui": {
                    "total": len(base_ui_alignments),
                    "aligned": base_ui_aligned,
                    "alignment_percentage": round((base_ui_aligned / len(base_ui_alignments) * 100) if base_ui_alignments else 0, 2),
                    "average_score": round(base_ui_avg, 2),
                    "average_gap": round(sum(a.alignment_gap for a in base_ui_alignments) / len(base_ui_alignments) if base_ui_alignments else 0, 2)
                }
            },
            "alignments": [asdict(a) for a in self.alignments],
            "enhancement_plan": self._generate_enhancement_plan(),
            "guardian_signatures": {
                "AEYON": "999 Hz - Ideal state alignment executed atomically",
                "JØHN": "530 Hz - Ideal state validated with truth",
                "META": "777 Hz - Pattern alignment to ideal state verified",
                "Abë": "530 Hz - Ideal state aligned with love and coherence",
                "YAGNI": "530 Hz - Only necessary enhancements identified"
            }
        }
    
    def _generate_enhancement_plan(self) -> Dict:
        """Generate enhancement plan"""
        enhancement_counts = {}
        
        for alignment in self.alignments:
            for enhancement in alignment.enhancements_needed:
                if enhancement not in enhancement_counts:
                    enhancement_counts[enhancement] = {
                        "count": 0,
                        "components": [],
                        "component_type": alignment.component_type
                    }
                enhancement_counts[enhancement]["count"] += 1
                enhancement_counts[enhancement]["components"].append(alignment.component_path)
        
        return {
            "total_enhancements_needed": sum(len(a.enhancements_needed) for a in self.alignments),
            "enhancement_types": enhancement_counts,
            "priority_order": self._get_priority_order()
        }
    
    def _get_priority_order(self) -> List[str]:
        """Get enhancement priority order"""
        return [
            "typescript_types",  # High impact, foundational
            "forward_ref",  # High impact, React best practice
            "pattern_declaration",  # High impact for Atomic
            "guardian_signatures",  # High impact for Atomic
            "cva_usage",  # Medium impact
            "cn_utility",  # Medium impact
            "icp_variants",  # Medium impact
            "export_structure",  # Low impact
        ]


def main():
    """Main execution"""
    print(" Aligning to Ideal State")
    print("Pattern: IDEAL × STATE × ALIGNMENT × ENHANCEMENT × PATTERN × ONE")
    print("∞ AbëONE ∞\n")
    
    aligner = IdealStateAligner()
    report = aligner.align_all()
    
    # Print summary
    print(" Ideal State Alignment Summary:")
    print(f"  Target Score: {report['ideal_state']['target_score']}%")
    print(f"  Total Components: {report['ideal_state']['total_components']}")
    print(f"  Aligned Components: {report['ideal_state']['aligned_components']}")
    print(f"  Alignment Percentage: {report['ideal_state']['alignment_percentage']}%")
    print(f"  Average Score: {report['ideal_state']['average_score']}%")
    print(f"  Total Gap: {report['ideal_state']['total_gap']} points")
    print(f"  Average Gap: {report['ideal_state']['average_gap']} points")
    
    print("\n By Component Type:")
    print(f"  Atomic Components:")
    print(f"    Aligned: {report['by_type']['atomic']['aligned']}/{report['by_type']['atomic']['total']}")
    print(f"    Average Score: {report['by_type']['atomic']['average_score']}%")
    print(f"    Average Gap: {report['by_type']['atomic']['average_gap']} points")
    
    print(f"\n  Base UI Components:")
    print(f"    Aligned: {report['by_type']['base_ui']['aligned']}/{report['by_type']['base_ui']['total']}")
    print(f"    Average Score: {report['by_type']['base_ui']['average_score']}%")
    print(f"    Average Gap: {report['by_type']['base_ui']['average_gap']} points")
    
    print("\n Enhancement Plan:")
    print(f"  Total Enhancements Needed: {report['enhancement_plan']['total_enhancements_needed']}")
    print(f"  Enhancement Types: {len(report['enhancement_plan']['enhancement_types'])}")
    
    for enhancement_type, details in report['enhancement_plan']['enhancement_types'].items():
        print(f"\n    {enhancement_type}:")
        print(f"      Count: {details['count']} components")
        print(f"      Type: {details['component_type']}")
        if len(details['components']) <= 5:
            for component in details['components']:
                print(f"        - {component}")
        else:
            for component in details['components'][:5]:
                print(f"        - {component}")
            print(f"        ... and {len(details['components']) - 5} more")
    
    # Save report
    report_path = ATOMIC_DIR / "IDEAL_STATE_ALIGNMENT.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\n Report saved to {report_path}")
    
    print("\n Ideal state alignment complete!")
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    main()

