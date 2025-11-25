#!/usr/bin/env python3
"""
Generate ARDM Operational Validation Report

Runs comprehensive validation and generates a report.

Pattern: AEYON × VALIDATE × REPORT × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

from validate_ardm_operational import ARDMOperationalValidator


def generate_report(output_file: Path = None):
    """Generate comprehensive ARDM validation report"""
    
    print("🔎 Generating ARDM Operational Validation Report")
    print("=" * 60)
    print()
    
    # Run validation
    validator = ARDMOperationalValidator()
    result = validator.validate_all()
    
    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "validation_result": result,
        "ardm_status": "OPERATIONAL" if result["operational"] else "NOT_OPERATIONAL",
        "summary": {
            "total_checks": result["successes"] + result["warnings"] + result["errors"],
            "successes": result["successes"],
            "warnings": result["warnings"],
            "errors": result["errors"],
            "success_rate": result["success_rate"],
        },
        "details": result["details"],
    }
    
    # Output report
    if output_file:
        output_file.write_text(json.dumps(report, indent=2))
        print(f"\n✅ Report saved to: {output_file}")
    else:
        print("\n" + "=" * 60)
        print("JSON Report:")
        print("=" * 60)
        print(json.dumps(report, indent=2))
    
    return report


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate ARDM Operational Validation Report"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (JSON format)",
    )
    
    args = parser.parse_args()
    
    output_path = Path(args.output) if args.output else None
    report = generate_report(output_path)
    
    # Exit with appropriate code
    sys.exit(0 if report["ardm_status"] == "OPERATIONAL" else 1)


if __name__ == "__main__":
    main()

