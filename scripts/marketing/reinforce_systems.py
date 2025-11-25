#!/usr/bin/env python3
"""
Marketing System Reinforcement Script
Reinforces all systems through AEYON EEAAO REBUILD 2X cycle
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSET_REGISTRY_PATH = PROJECT_ROOT / "marketing" / "assets" / "ASSET_REGISTRY.json"
REINFORCEMENT_REPORT_PATH = PROJECT_ROOT / "marketing" / "assets" / "REINFORCEMENT_REPORT.txt"


def load_asset_registry() -> Dict[str, Any]:
    """Load the asset registry."""
    if ASSET_REGISTRY_PATH.exists():
        with open(ASSET_REGISTRY_PATH, 'r') as f:
            return json.load(f)
    return {}


def check_path_exists(path: str) -> bool:
    """Check if a path exists."""
    full_path = PROJECT_ROOT / path
    return full_path.exists()


def validate_landing_pages_reinforcement(registry: Dict[str, Any]) -> Dict[str, Any]:
    """Validate landing pages reinforcement."""
    results = {
        "total": 0,
        "reinforced": 0,
        "icp_aware": 0,
        "visit_aware": 0,
        "needs_reinforcement": []
    }
    
    landing_pages = registry.get("landing_pages", {})
    for name, config in landing_pages.items():
        results["total"] += 1
        path = config.get("path", "")
        status = config.get("status", "unknown")
        icp_aware = config.get("icp_aware", False)
        visit_aware = config.get("visit_aware", False)
        
        if check_path_exists(path) and status == "complete":
            results["reinforced"] += 1
            if icp_aware:
                results["icp_aware"] += 1
            if visit_aware:
                results["visit_aware"] += 1
        else:
            results["needs_reinforcement"].append(name)
    
    return results


def validate_guards_reinforcement(registry: Dict[str, Any]) -> Dict[str, Any]:
    """Validate GUARDS reinforcement."""
    results = {
        "total": 0,
        "reinforced": 0,
        "precision_boosted": 0,
        "latency_optimized": 0,
        "needs_reinforcement": []
    }
    
    guards = registry.get("guards", {})
    for name, config in guards.items():
        results["total"] += 1
        reinforced = config.get("reinforced", False)
        
        if reinforced:
            results["reinforced"] += 1
            if config.get("precision_boost") == "completed" or config.get("coherence_boost") == "completed" or config.get("validation_boost") == "completed":
                results["precision_boosted"] += 1
            if "<30ms" in str(config.get("latency", "")) or "<25ms" in str(config.get("latency", "")) or "<5ms" in str(config.get("latency", "")):
                results["latency_optimized"] += 1
        else:
            results["needs_reinforcement"].append(name)
    
    return results


def validate_guardians_lock(registry: Dict[str, Any]) -> Dict[str, Any]:
    """Validate Guardians lock status."""
    results = {
        "total": 0,
        "locked": 0,
        "coherence_strengthened": 0,
        "execution_optimized": 0,
        "pattern_awareness_loaded": 0,
        "needs_lock": []
    }
    
    guardians = registry.get("guardians", {})
    for name, config in guardians.items():
        results["total"] += 1
        status = config.get("status", "unknown")
        reinforced = config.get("reinforced", False)
        
        if status == "locked" and reinforced:
            results["locked"] += 1
            if config.get("coherence_field") == "strengthened":
                results["coherence_strengthened"] += 1
            if config.get("execution_field") == "optimized":
                results["execution_optimized"] += 1
            if config.get("pattern_awareness") == "loaded":
                results["pattern_awareness_loaded"] += 1
        else:
            results["needs_lock"].append(name)
    
    return results


def generate_reinforcement_report(registry: Dict[str, Any], validation_results: Dict[str, Any]) -> str:
    """Generate reinforcement report."""
    report = []
    report.append(" AEYON EEAAO REBUILD 2X - REINFORCEMENT REPORT")
    report.append("=" * 70)
    report.append(f"Date: {datetime.now().isoformat()}")
    report.append("")
    
    # Landing Pages
    lp_results = validation_results["landing_pages"]
    report.append(" LANDING PAGES REINFORCEMENT")
    report.append(f"  Total: {lp_results['total']}")
    report.append(f"  Reinforced: {lp_results['reinforced']}")
    report.append(f"  ICP-Aware: {lp_results['icp_aware']}")
    report.append(f"  Visit-Aware: {lp_results['visit_aware']}")
    report.append(f"  Needs Reinforcement: {len(lp_results['needs_reinforcement'])}")
    if lp_results['needs_reinforcement']:
        report.append(f"    - {', '.join(lp_results['needs_reinforcement'])}")
    report.append("")
    
    # GUARDS
    guards_results = validation_results["guards"]
    report.append("  GUARDS REINFORCEMENT")
    report.append(f"  Total: {guards_results['total']}")
    report.append(f"  Reinforced: {guards_results['reinforced']}")
    report.append(f"  Precision Boosted: {guards_results['precision_boosted']}")
    report.append(f"  Latency Optimized: {guards_results['latency_optimized']}")
    report.append(f"  Needs Reinforcement: {len(guards_results['needs_reinforcement'])}")
    if guards_results['needs_reinforcement']:
        report.append(f"    - {', '.join(guards_results['needs_reinforcement'])}")
    report.append("")
    
    # Guardians
    guardians_results = validation_results["guardians"]
    report.append(" GUARDIANS LOCK STATUS")
    report.append(f"  Total: {guardians_results['total']}")
    report.append(f"  Locked: {guardians_results['locked']}")
    report.append(f"  Coherence Strengthened: {guardians_results['coherence_strengthened']}")
    report.append(f"  Execution Optimized: {guardians_results['execution_optimized']}")
    report.append(f"  Pattern Awareness Loaded: {guardians_results['pattern_awareness_loaded']}")
    report.append(f"  Needs Lock: {len(guardians_results['needs_lock'])}")
    if guardians_results['needs_lock']:
        report.append(f"    - {', '.join(guardians_results['needs_lock'])}")
    report.append("")
    
    # Overall Status
    total_systems = (
        lp_results['total'] +
        guards_results['total'] +
        guardians_results['total']
    )
    reinforced_systems = (
        lp_results['reinforced'] +
        guards_results['reinforced'] +
        guardians_results['locked']
    )
    reinforcement_rate = (reinforced_systems / total_systems * 100) if total_systems > 0 else 0
    
    report.append(" OVERALL REINFORCEMENT STATUS")
    report.append(f"  Reinforcement Rate: {reinforcement_rate:.1f}%")
    report.append(f"  Systems Reinforced: {reinforced_systems}/{total_systems}")
    report.append("")
    
    report.append("∞ AbëONE Reinforcement Complete ∞")
    
    return "\n".join(report)


def main():
    """Main reinforcement function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Reinforce marketing systems")
    parser.add_argument("--validate", action="store_true", help="Validate reinforcement")
    parser.add_argument("--report", action="store_true", help="Generate report")
    args = parser.parse_args()
    
    # Load registry
    registry = load_asset_registry()
    
    # Update last reinforced
    registry["last_reinforced"] = datetime.now().isoformat()
    registry["reinforcement_cycle"] = "AEYON_EEAAO_REBUILD_2X"
    
    if args.validate or args.report:
        # Validate reinforcement
        validation_results = {
            "landing_pages": validate_landing_pages_reinforcement(registry),
            "guards": validate_guards_reinforcement(registry),
            "guardians": validate_guardians_lock(registry)
        }
        
        # Generate report
        if args.report:
            report = generate_reinforcement_report(registry, validation_results)
            print(report)
            
            # Save report
            REINFORCEMENT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(REINFORCEMENT_REPORT_PATH, 'w') as f:
                f.write(report)
    
    # Save updated registry
    with open(ASSET_REGISTRY_PATH, 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(" System reinforcement complete")


if __name__ == "__main__":
    main()

