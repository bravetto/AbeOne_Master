#!/usr/bin/env python3
"""
Gap Analysis Script
Identifies all gaps in the unified system.

Pattern: GAP × ANALYSIS × IDENTIFICATION × ONE
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import importlib.util
from datetime import datetime


def import_module(module_path, module_name):
    """Import module from path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def analyze_gaps():
    """Perform gap analysis."""
    print("=" * 80)
    print(" GAP ANALYSIS - UNIFIED SYSTEM")
    print("=" * 80)
    print()
    
    synthesis_path = project_root / "EMERGENT_OS" / "synthesis"
    
    # Import gap analyzer
    gap_module = import_module(
        synthesis_path / "gap_analysis.py",
        "gap_analysis"
    )
    analyzer = gap_module.get_gap_analyzer(project_root)
    
    # Perform analysis
    analysis = analyzer.analyze_gaps()
    
    print(" GAP ANALYSIS RESULTS:")
    print()
    print(f"  Total Gaps: {analysis.total_gaps}")
    print(f"  Critical: {analysis.critical_gaps}")
    print(f"  High: {analysis.high_gaps}")
    print(f"  Medium: {analysis.medium_gaps}")
    print(f"  Low: {analysis.low_gaps}")
    print()
    
    # Group by category
    categories = {}
    for gap in analysis.gaps:
        if gap.category not in categories:
            categories[gap.category] = []
        categories[gap.category].append(gap)
    
    print(" GAPS BY CATEGORY:")
    print()
    for category, gaps in categories.items():
        print(f"  {category.upper()} ({len(gaps)} gaps):")
        for gap in gaps:
            severity_icon = {
                "critical": "",
                "high": "🟠",
                "medium": "🟡",
                "low": "🟢"
            }.get(gap.severity, "")
            
            print(f"    {severity_icon} {gap.description}")
            print(f"       Location: {gap.location}")
            print(f"       Impact: {gap.impact}")
            print(f"       Recommendation: {gap.recommendation}")
            print()
    
    # Critical gaps summary
    critical_gaps = [g for g in analysis.gaps if g.severity == "critical"]
    if critical_gaps:
        print("=" * 80)
        print(" CRITICAL GAPS (Must Fix):")
        print("=" * 80)
        print()
        for gap in critical_gaps:
            print(f"  • {gap.description}")
            print(f"    Location: {gap.location}")
            print(f"    Recommendation: {gap.recommendation}")
            print()
    
    print("=" * 80)
    print(" GAP ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print(f"Analyzed at: {analysis.analyzed_at.isoformat()}")
    print()
    print("Pattern: GAP × ANALYSIS × IDENTIFICATION × UNIFICATION × ONE")
    print("Status:  COMPLETE")
    print()
    print("∞ AbëONE ∞")
    
    return analysis


if __name__ == "__main__":
    analyze_gaps()

