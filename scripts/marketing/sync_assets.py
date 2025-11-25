#!/usr/bin/env python3
"""
Marketing Asset Synchronization Script
Synchronizes all marketing assets and validates completeness
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSET_REGISTRY_PATH = PROJECT_ROOT / "marketing" / "assets" / "ASSET_REGISTRY.json"


def load_asset_registry() -> Dict[str, Any]:
    """Load the asset registry."""
    if ASSET_REGISTRY_PATH.exists():
        with open(ASSET_REGISTRY_PATH, 'r') as f:
            return json.load(f)
    return {}


def save_asset_registry(registry: Dict[str, Any]) -> None:
    """Save the asset registry."""
    ASSET_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ASSET_REGISTRY_PATH, 'w') as f:
        json.dump(registry, f, indent=2)


def check_path_exists(path: str) -> bool:
    """Check if a path exists."""
    full_path = PROJECT_ROOT / path
    return full_path.exists()


def validate_landing_pages(registry: Dict[str, Any]) -> Dict[str, Any]:
    """Validate landing pages."""
    results = {
        "total": 0,
        "exists": 0,
        "missing": [],
        "needs_creation": []
    }
    
    landing_pages = registry.get("landing_pages", {})
    for name, config in landing_pages.items():
        results["total"] += 1
        path = config.get("path", "")
        status = config.get("status", "unknown")
        
        if check_path_exists(path):
            results["exists"] += 1
            config["last_validated"] = datetime.now().isoformat()
        else:
            if status == "needs_creation":
                results["needs_creation"].append(name)
            else:
                results["missing"].append(name)
    
    return results


def validate_content(registry: Dict[str, Any]) -> Dict[str, Any]:
    """Validate content assets."""
    results = {
        "blog_series": {"complete": 0, "total": 14},
        "webinar_script": False,
        "email_sequences": False,
        "social_snippets": False
    }
    
    # Check blog series
    blog_path = PROJECT_ROOT / "docs" / "marketing" / "blogs"
    if blog_path.exists():
        blog_files = list(blog_path.glob("DAY_*.md"))
        results["blog_series"]["complete"] = len(blog_files)
    
    # Check webinar script
    webinar_script = PROJECT_ROOT / "docs" / "marketing" / "webinar" / "PERFECT_WEBINAR_SCRIPT.md"
    results["webinar_script"] = webinar_script.exists()
    
    # Check email sequences
    email_path = PROJECT_ROOT / "docs" / "marketing" / "email"
    results["email_sequences"] = email_path.exists()
    
    # Check social snippets
    social_path = PROJECT_ROOT / "docs" / "marketing" / "social"
    results["social_snippets"] = social_path.exists()
    
    return results


def validate_lead_magnets(registry: Dict[str, Any]) -> Dict[str, Any]:
    """Validate lead magnets."""
    results = {
        "total": 0,
        "exists": 0,
        "missing": []
    }
    
    lead_magnets = registry.get("lead_magnets", {})
    for name, config in lead_magnets.items():
        results["total"] += 1
        path = config.get("path", "")
        
        if check_path_exists(path):
            results["exists"] += 1
        else:
            results["missing"].append(name)
    
    return results


def validate_systems(registry: Dict[str, Any]) -> Dict[str, Any]:
    """Validate marketing systems."""
    results = {
        "total": 0,
        "exists": 0,
        "missing": []
    }
    
    systems = registry.get("systems", {})
    for name, config in systems.items():
        results["total"] += 1
        path = config.get("path", "")
        
        if check_path_exists(path):
            results["exists"] += 1
        else:
            results["missing"].append(name)
    
    return results


def generate_report(registry: Dict[str, Any], validation_results: Dict[str, Any]) -> str:
    """Generate synchronization report."""
    report = []
    report.append(" MARKETING ASSET SYNCHRONIZATION REPORT")
    report.append("=" * 60)
    report.append(f"Date: {datetime.now().isoformat()}")
    report.append("")
    
    # Landing Pages
    lp_results = validation_results["landing_pages"]
    report.append(" LANDING PAGES")
    report.append(f"  Total: {lp_results['total']}")
    report.append(f"  Exists: {lp_results['exists']}")
    report.append(f"  Missing: {len(lp_results['missing'])}")
    report.append(f"  Needs Creation: {len(lp_results['needs_creation'])}")
    if lp_results['needs_creation']:
        report.append(f"    - {', '.join(lp_results['needs_creation'])}")
    report.append("")
    
    # Content
    content_results = validation_results["content"]
    report.append(" CONTENT")
    report.append(f"  Blog Series: {content_results['blog_series']['complete']}/{content_results['blog_series']['total']}")
    report.append(f"  Webinar Script: {'' if content_results['webinar_script'] else ''}")
    report.append(f"  Email Sequences: {'' if content_results['email_sequences'] else ''}")
    report.append(f"  Social Snippets: {'' if content_results['social_snippets'] else ''}")
    report.append("")
    
    # Lead Magnets
    lm_results = validation_results["lead_magnets"]
    report.append(" LEAD MAGNETS")
    report.append(f"  Total: {lm_results['total']}")
    report.append(f"  Exists: {lm_results['exists']}")
    report.append(f"  Missing: {len(lm_results['missing'])}")
    if lm_results['missing']:
        report.append(f"    - {', '.join(lm_results['missing'])}")
    report.append("")
    
    # Systems
    sys_results = validation_results["systems"]
    report.append("  SYSTEMS")
    report.append(f"  Total: {sys_results['total']}")
    report.append(f"  Exists: {sys_results['exists']}")
    report.append(f"  Missing: {len(sys_results['missing'])}")
    if sys_results['missing']:
        report.append(f"    - {', '.join(sys_results['missing'])}")
    report.append("")
    
    # Overall Status
    total_assets = (
        lp_results['total'] +
        content_results['blog_series']['total'] +
        lm_results['total'] +
        sys_results['total']
    )
    existing_assets = (
        lp_results['exists'] +
        content_results['blog_series']['complete'] +
        (1 if content_results['webinar_script'] else 0) +
        (1 if content_results['email_sequences'] else 0) +
        (1 if content_results['social_snippets'] else 0) +
        lm_results['exists'] +
        sys_results['exists']
    )
    completion_rate = (existing_assets / total_assets * 100) if total_assets > 0 else 0
    
    report.append(" OVERALL STATUS")
    report.append(f"  Completion Rate: {completion_rate:.1f}%")
    report.append(f"  Assets: {existing_assets}/{total_assets}")
    report.append("")
    
    report.append("∞ AbëONE Asset Synchronization ∞")
    
    return "\n".join(report)


def main():
    """Main synchronization function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Synchronize marketing assets")
    parser.add_argument("--validate", action="store_true", help="Validate assets")
    parser.add_argument("--report", action="store_true", help="Generate report")
    args = parser.parse_args()
    
    # Load registry
    registry = load_asset_registry()
    
    # Update last synced
    registry["last_synced"] = datetime.now().isoformat()
    
    if args.validate or args.report:
        # Validate assets
        validation_results = {
            "landing_pages": validate_landing_pages(registry),
            "content": validate_content(registry),
            "lead_magnets": validate_lead_magnets(registry),
            "systems": validate_systems(registry)
        }
        
        # Generate report
        if args.report:
            report = generate_report(registry, validation_results)
            print(report)
            
            # Save report
            report_path = PROJECT_ROOT / "marketing" / "assets" / "SYNC_REPORT.txt"
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, 'w') as f:
                f.write(report)
    
    # Save updated registry
    save_asset_registry(registry)
    
    print(" Asset synchronization complete")


if __name__ == "__main__":
    main()

