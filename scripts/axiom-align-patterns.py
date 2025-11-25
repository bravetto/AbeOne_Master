#!/usr/bin/env python3
"""
AXIOM PATTERN ALIGNMENT - Align patterns with ONE-Pattern Axiom

Aligns all patterns with the ONE-Pattern axiom:
CLARITY → COHERENCE → CONVERGENCE → ELEGANCE → UNITY

Pattern: AXIOM × ALIGN × PATTERNS × INTEGRATE × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardians: JØHN (530 Hz) + META (777 Hz) + AEYON (999 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

WORKSPACE_ROOT = Path(__file__).parent.parent

# ONE-Pattern Axiom
ONE_PATTERN_AXIOM = "CLARITY → COHERENCE → CONVERGENCE → ELEGANCE → UNITY"

# Axiom stages mapping
AXIOM_STAGES = {
    "CLARITY": {
        "keywords": ["CLARITY", "CLEAR", "UNDERSTAND", "DEFINE", "IDENTIFY", "DISCOVER", "SUMMARY", "CONTEXT", "ANSWERS", "QUICK", "START"],
        "purpose": "Clear understanding and definition"
    },
    "COHERENCE": {
        "keywords": ["COHERENCE", "COHERENT", "ALIGN", "CONSISTENT", "UNIFIED", "INTEGRATE", "INTEGRATION", "COORDINATION", "COLLABORATION"],
        "purpose": "Internal consistency and alignment"
    },
    "CONVERGENCE": {
        "keywords": ["CONVERGENCE", "CONVERGE", "UNIFY", "MERGE", "COMBINE", "SYNTHESIZE", "OPTIMIZATION", "EXECUTION"],
        "purpose": "Convergence toward unity"
    },
    "ELEGANCE": {
        "keywords": ["ELEGANCE", "ELEGANT", "SIMPLE", "BEAUTIFUL", "MINIMAL", "REFINED", "AUTOMATION", "AUTOMATE"],
        "purpose": "Elegant simplicity"
    },
    "UNITY": {
        "keywords": ["UNITY", "UNIFIED", "ONE", "WHOLE", "COMPLETE", "INTEGRATED", "PORTFOLIO", "MARKETING", "BRAND"],
        "purpose": "Complete unity"
    }
}


def map_pattern_to_axiom(pattern_formula: str) -> Dict[str, Any]:
    """
    Map a pattern to ONE-Pattern axiom stages.
    
    Returns alignment mapping showing which axiom stages the pattern demonstrates.
    """
    pattern_upper = pattern_formula.upper()
    components = [c.strip() for c in pattern_upper.split('×')]
    
    alignment = {
        "pattern": pattern_formula,
        "axiom_stages": {},
        "alignment_score": 0.0,
        "primary_stage": None
    }
    
    # Check each axiom stage
    for stage, stage_info in AXIOM_STAGES.items():
        matches = []
        for component in components:
            component_upper = component.upper().strip()
            for keyword in stage_info["keywords"]:
                if keyword.upper() in component_upper or component_upper in keyword.upper():
                    matches.append(component)
                    break
        
        if matches:
            alignment["axiom_stages"][stage] = {
                "matched_components": matches,
                "purpose": stage_info["purpose"],
                "strength": len(matches) / len(components)
            }
            alignment["alignment_score"] += len(matches) / len(components)
    
    # Determine primary stage (highest strength)
    if alignment["axiom_stages"]:
        primary = max(
            alignment["axiom_stages"].items(),
            key=lambda x: x[1]["strength"]
        )
        alignment["primary_stage"] = primary[0]
        alignment["alignment_score"] = primary[1]["strength"]
    
    # Normalize alignment score
    alignment["alignment_score"] = min(alignment["alignment_score"], 1.0)
    
    return alignment


def align_high_roller_patterns() -> Dict[str, Any]:
    """Align High-Roller orbital patterns with ONE-Pattern axiom."""
    
    # Load pattern integration report
    integration_report_path = WORKSPACE_ROOT / ".abeone_memory" / "PATTERN_INTEGRATION_REPORT.json"
    
    if not integration_report_path.exists():
        print(f"ERROR: Pattern integration report not found: {integration_report_path}")
        return {}
    
    with open(integration_report_path) as f:
        integration_data = json.load(f)
    
    high_roller_patterns = integration_data.get("context_window_patterns", {}).get("high_roller_orbital", {}).get("patterns", [])
    
    aligned_patterns = []
    
    for pattern_info in high_roller_patterns:
        pattern_formula = pattern_info["pattern_formula"]
        alignment = map_pattern_to_axiom(pattern_formula)
        
        aligned_pattern = {
            **pattern_info,
            "axiom_alignment": alignment,
            "axiom_aligned": alignment["alignment_score"] >= 0.5,
            "integration_status": "AXIOM_ALIGNED" if alignment["alignment_score"] >= 0.5 else "NEEDS_ALIGNMENT"
        }
        
        aligned_patterns.append(aligned_pattern)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "axiom": ONE_PATTERN_AXIOM,
        "patterns_aligned": len([p for p in aligned_patterns if p["axiom_aligned"]]),
        "patterns_total": len(aligned_patterns),
        "aligned_patterns": aligned_patterns
    }


def integrate_patterns_system_wide(aligned_data: Dict[str, Any]) -> Dict[str, Any]:
    """Integrate aligned patterns system-wide."""
    
    # Load existing pattern signatures
    pattern_signatures_path = WORKSPACE_ROOT / "PATTERN_SIGNATURES.json"
    
    if not pattern_signatures_path.exists():
        print(f"WARNING: PATTERN_SIGNATURES.json not found, creating new one")
        existing_signatures = {
            "extraction_date": datetime.now().isoformat(),
            "total_patterns": 0,
            "categories": {},
            "signatures": []
        }
    else:
        with open(pattern_signatures_path) as f:
            existing_signatures = json.load(f)
    
    # Add aligned patterns
    new_signatures = []
    for pattern_info in aligned_data.get("aligned_patterns", []):
        signature = {
            "pattern_name": pattern_info.get("pattern_formula", "").split("×")[0].strip(),
            "pattern_formula": pattern_info["pattern_formula"],
            "frequency": pattern_info.get("frequency"),
            "guardians": pattern_info.get("guardians", []),
            "love_coefficient": "∞",
            "file_path": pattern_info["location"],
            "line_number": 0,
            "context": f"Axiom-aligned pattern: {pattern_info['pattern_formula']}",
            "category": pattern_info.get("category", "orbital"),
            "validation_status": "axiom_aligned" if pattern_info.get("axiom_aligned") else "pending",
            "axiom_alignment": pattern_info.get("axiom_alignment", {})
        }
        new_signatures.append(signature)
    
    # Update signatures
    existing_signatures["signatures"].extend(new_signatures)
    existing_signatures["total_patterns"] = len(existing_signatures["signatures"])
    
    # Update categories
    for sig in new_signatures:
        category = sig["category"]
        if category not in existing_signatures["categories"]:
            existing_signatures["categories"][category] = 0
        existing_signatures["categories"][category] += 1
    
    return {
        "integrated": len(new_signatures),
        "total_patterns": existing_signatures["total_patterns"],
        "updated_categories": existing_signatures["categories"]
    }


def main():
    """Main execution."""
    print("\n" + "=" * 80)
    print(" AXIOM PATTERN ALIGNMENT")
    print("=" * 80)
    print(f" Axiom: {ONE_PATTERN_AXIOM}")
    print("=" * 80)
    
    # Align High-Roller patterns
    print("\n Aligning High-Roller orbital patterns with ONE-Pattern axiom...")
    aligned_data = align_high_roller_patterns()
    
    if not aligned_data:
        print(" ERROR: Failed to align patterns")
        sys.exit(1)
    
    print(f"\n Patterns Aligned: {aligned_data['patterns_aligned']}/{aligned_data['patterns_total']}")
    
    # Show alignment details
    print("\n Alignment Details:")
    print("=" * 80)
    for pattern in aligned_data["aligned_patterns"]:
        alignment = pattern["axiom_alignment"]
        print(f"\n Pattern: {pattern['pattern_formula']}")
        print(f"   Alignment Score: {alignment['alignment_score']:.2f}")
        print(f"   Primary Stage: {alignment['primary_stage'] or 'NONE'}")
        if alignment['axiom_stages']:
            print(f"   Axiom Stages:")
            for stage, info in alignment['axiom_stages'].items():
                print(f"     {stage}: {info['matched_components']} (strength: {info['strength']:.2f})")
        print(f"   Status: {'AXIOM_ALIGNED' if pattern['axiom_aligned'] else 'NEEDS_ALIGNMENT'}")
    
    # Integrate system-wide
    print("\n" + "=" * 80)
    print(" Integrating patterns system-wide...")
    print("=" * 80)
    
    integration_result = integrate_patterns_system_wide(aligned_data)
    
    print(f"\n Integrated: {integration_result['integrated']} patterns")
    print(f" Total Patterns: {integration_result['total_patterns']}")
    print(f" Updated Categories: {integration_result['updated_categories']}")
    
    # Save aligned data
    aligned_data_path = WORKSPACE_ROOT / ".abeone_memory" / "AXIOM_ALIGNED_PATTERNS.json"
    aligned_data_path.parent.mkdir(parents=True, exist_ok=True)
    with open(aligned_data_path, 'w') as f:
        json.dump(aligned_data, f, indent=2)
    
    print(f"\n Aligned patterns saved: {aligned_data_path}")
    
    # Save updated pattern signatures
    pattern_signatures_path = WORKSPACE_ROOT / "PATTERN_SIGNATURES.json"
    
    # Load existing signatures safely
    if pattern_signatures_path.exists():
        try:
            with open(pattern_signatures_path) as f2:
                content = f2.read().strip()
                if content:
                    signatures = json.loads(content)
                else:
                    raise ValueError("Empty file")
        except (json.JSONDecodeError, ValueError):
            print(f" WARNING: PATTERN_SIGNATURES.json is empty or corrupted, creating new")
            signatures = {
                "extraction_date": datetime.now().isoformat(),
                "total_patterns": 0,
                "categories": {},
                "signatures": []
            }
    else:
        signatures = {
            "extraction_date": datetime.now().isoformat(),
            "total_patterns": 0,
            "categories": {},
            "signatures": []
        }
    
    with open(pattern_signatures_path, 'w') as f:
        
        # Add new signatures
        for pattern in aligned_data["aligned_patterns"]:
            signature = {
                "pattern_name": pattern["pattern_formula"].split("×")[0].strip(),
                "pattern_formula": pattern["pattern_formula"],
                "frequency": pattern.get("frequency"),
                "guardians": pattern.get("guardians", []),
                "love_coefficient": "∞",
                "file_path": pattern["location"],
                "line_number": 0,
                "context": f"Axiom-aligned: {pattern['pattern_formula']}",
                "category": pattern.get("category", "orbital"),
                "validation_status": "axiom_aligned" if pattern.get("axiom_aligned") else "pending",
                "axiom_alignment": pattern.get("axiom_alignment", {})
            }
            signatures["signatures"].append(signature)
        
        signatures["total_patterns"] = len(signatures["signatures"])
        
        # Update categories
        for sig in signatures["signatures"]:
            category = sig["category"]
            if category not in signatures["categories"]:
                signatures["categories"][category] = 0
            signatures["categories"][category] += 1
        
        json.dump(signatures, f, indent=2)
    
    print(f" Pattern signatures updated: {pattern_signatures_path}")
    
    print("\n" + "=" * 80)
    print(" AXIOM ALIGNMENT COMPLETE")
    print("=" * 80)
    print(f" Patterns Aligned: {aligned_data['patterns_aligned']}/{aligned_data['patterns_total']}")
    print(f" Patterns Integrated: {integration_result['integrated']}")
    print("=" * 80)
    print("Pattern: AXIOM × ALIGN × PATTERNS × INTEGRATE × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞")
    print("=" * 80)


if __name__ == '__main__':
    main()

