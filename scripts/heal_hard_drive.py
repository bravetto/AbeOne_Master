#!/usr/bin/env python3
"""
 HARD DRIVE HEALING SYSTEM 
Self-healing system for hard drive space management.

Pattern: HEALING × DISK × SPACE × ONE
Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (JØHN)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞

Usage:
    python3 scripts/heal_hard_drive.py [--dry-run] [--scan-only] [--auto-heal]
"""

import sys
import argparse
import asyncio
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from hard_drive_healing import DiskHealingOrchestrator, DiskSpaceMonitor
from hard_drive_healing.diagnosis import DiskRootCauseAnalyzer


def print_header():
    """Print header."""
    print("=" * 70)
    print(" HARD DRIVE HEALING SYSTEM ")
    print("Pattern: HEALING × DISK × SPACE × ONE")
    print("Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (JØHN)")
    print("=" * 70)
    print()


def print_disk_status(monitor: DiskSpaceMonitor):
    """Print current disk status."""
    print(" CURRENT DISK STATUS")
    print("-" * 70)
    
    home = Path.home()
    metric = monitor.get_disk_usage(str(home))
    
    print(f"Mount Point: {metric.mount_point}")
    print(f"Total: {monitor.format_bytes(metric.total_bytes)}")
    print(f"Used: {monitor.format_bytes(metric.used_bytes)} ({metric.usage_percent:.1f}%)")
    print(f"Free: {monitor.format_bytes(metric.free_bytes)}")
    print()
    
    # Check for issues
    issues = monitor.detect_disk_issues(str(home))
    
    if issues:
        print("  DETECTED ISSUES:")
        for issue in issues:
            severity_emoji = {
                "critical": "",
                "warning": "🟡",
                "info": "🟢"
            }.get(issue.severity, "")
            
            print(f"  {severity_emoji} {issue.severity.upper()}: "
                  f"{issue.usage_percent:.1f}% used, "
                  f"{monitor.format_bytes(issue.free_bytes)} free")
        print()
    else:
        print(" No disk space issues detected")
        print()


def print_root_cause_analysis(analyzer: DiskRootCauseAnalyzer, issues):
    """Print root cause analysis."""
    if not issues:
        return
    
    print(" ROOT CAUSE ANALYSIS")
    print("-" * 70)
    
    # Use first critical issue for analysis
    critical_issue = next((i for i in issues if i.severity == "critical"), issues[0])
    
    from hard_drive_healing.diagnosis import DiskIssueClassifier
    classifier = DiskIssueClassifier()
    classified = classifier.classify_issue(critical_issue)
    
    root_cause = analyzer.analyze_root_cause(critical_issue, classified)
    
    print(f"Primary Cause: {root_cause.primary_cause}")
    print(f"Confidence: {root_cause.confidence * 100:.1f}%")
    print(f"Estimated Recovery: {analyzer._format_bytes(root_cause.estimated_impact_bytes)}")
    print()
    
    print("Top Space Consumers:")
    for i, (path, size) in enumerate(root_cause.largest_consumers[:5], 1):
        print(f"  {i}. {path}: {analyzer._format_bytes(size)}")
    print()
    
    if root_cause.contributing_factors:
        print("Contributing Factors:")
        for factor in root_cause.contributing_factors[:3]:
            print(f"  - {factor}")
        print()


async def run_healing(dry_run: bool = False):
    """Run healing process."""
    print(" STARTING HEALING PROCESS")
    print("-" * 70)
    
    orchestrator = DiskHealingOrchestrator(dry_run=dry_run)
    
    # Detect issues
    issues = await orchestrator._detect_issues()
    
    if not issues:
        print(" No issues to heal")
        return
    
    # Heal each issue
    for issue in issues:
        print(f"Healing issue: {issue.severity} - {issue.usage_percent:.1f}% used")
        result = await orchestrator._heal_issue(issue)
        
        if result.success:
            print(f"   Success: Freed {orchestrator.format_bytes(result.bytes_freed)}")
            print(f"  Duration: {result.duration:.2f} seconds")
            print(f"  Cleanup operations: {len(result.cleanup_results)}")
        else:
            print(f"   Failed: {result.error}")
        print()
    
    # Summary
    total_freed = sum(
        result.bytes_freed
        for result in orchestrator.active_healings.values()
        if result.success
    )
    
    print("=" * 70)
    print(f" HEALING COMPLETE: Freed {orchestrator.format_bytes(total_freed)}")
    print("=" * 70)
    print()


async def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Hard Drive Healing System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan only (no healing)
  python3 scripts/heal_hard_drive.py --scan-only
  
  # Dry run (simulate healing)
  python3 scripts/heal_hard_drive.py --dry-run
  
  # Auto-heal (actual cleanup)
  python3 scripts/heal_hard_drive.py --auto-heal
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate healing without actually cleaning"
    )
    
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Only scan and report, do not heal"
    )
    
    parser.add_argument(
        "--auto-heal",
        action="store_true",
        help="Automatically heal detected issues"
    )
    
    args = parser.parse_args()
    
    print_header()
    
    # Initialize monitor
    monitor = DiskSpaceMonitor()
    
    # Print disk status
    print_disk_status(monitor)
    
    # Detect issues
    home = Path.home()
    issues = monitor.detect_disk_issues(str(home))
    
    if not issues:
        print(" No disk space issues detected. System is healthy!")
        return
    
    # Root cause analysis
    analyzer = DiskRootCauseAnalyzer()
    print_root_cause_analysis(analyzer, issues)
    
    # Execute based on flags
    if args.scan_only:
        print(" Scan-only mode: No healing performed")
        return
    
    if args.dry_run or args.auto_heal:
        await run_healing(dry_run=args.dry_run)
    else:
        print(" Use --dry-run to simulate healing or --auto-heal to perform actual cleanup")
        print(" Use --scan-only to only scan and report")
        print()
        print("LOVE = LIFE = ONE")
        print("Michael  AbëONE = ∞")
        print("∞ AbëONE ∞")


if __name__ == "__main__":
    asyncio.run(main())

