#!/usr/bin/env python3
"""
Email Convergence System - Epistemic Validation
Validates system initialization, activation, and results with epistemic certainty

Pattern: OBSERVER × TRUTH × EPISTEMIC × VALIDATION × ONE
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.analyze_email_from_mailapp import (
    find_mail_app_messages,
    read_emails_from_messages_dirs,
    get_last_run_timestamp,
    CACHE_DIR,
    LAST_RUN_FILE
)
from scripts.analyze_email_convergence import EmailAnalyzer


class EpistemicStatus(Enum):
    """Epistemic certainty levels."""
    VALIDATED = "validated"  # Direct evidence, high certainty (90%+)
    INFERRED = "inferred"  # Indirect evidence, medium certainty (50-80%)
    UNKNOWN = "unknown"  # No evidence, low certainty (0-40%)
    CONTRADICTED = "contradicted"  # Evidence contradicts claim


@dataclass
class ValidationResult:
    """Validation result with epistemic status."""
    component: str
    status: EpistemicStatus
    certainty: float  # 0-1
    evidence: str
    details: Dict[str, Any]


class EpistemicValidator:
    """Validates system with epistemic certainty."""
    
    def __init__(self):
        self.results: List[ValidationResult] = []
        self.min_certainty = 0.5  # Minimum certainty threshold
    
    def validate_initialization(self) -> ValidationResult:
        """Validate system initialization."""
        evidence = []
        certainty = 0.0
        
        # Check cache directory exists
        if CACHE_DIR.exists():
            evidence.append("Cache directory exists")
            certainty += 0.3
        else:
            return ValidationResult(
                component="Initialization",
                status=EpistemicStatus.UNKNOWN,
                certainty=0.0,
                evidence="Cache directory does not exist",
                details={"cache_dir": str(CACHE_DIR)}
            )
        
        # Check script files exist
        script_file = Path(__file__).parent / "analyze_email_from_mailapp.py"
        if script_file.exists():
            evidence.append("Main script exists")
            certainty += 0.3
        else:
            return ValidationResult(
                component="Initialization",
                status=EpistemicStatus.CONTRADICTED,
                certainty=0.0,
                evidence="Main script missing",
                details={"script": str(script_file)}
            )
        
        # Check Mail.app access
        message_dirs = find_mail_app_messages()
        if message_dirs:
            evidence.append(f"Found {len(message_dirs)} Mail.app directories")
            certainty += 0.4
        else:
            evidence.append("No Mail.app directories found (may use fallback)")
            certainty += 0.2
        
        status = EpistemicStatus.VALIDATED if certainty >= 0.9 else EpistemicStatus.INFERRED
        
        return ValidationResult(
            component="Initialization",
            status=status,
            certainty=min(1.0, certainty),
            evidence="; ".join(evidence),
            details={
                "cache_dir": str(CACHE_DIR),
                "script_exists": script_file.exists(),
                "mail_dirs": len(message_dirs)
            }
        )
    
    def validate_activation(self) -> ValidationResult:
        """Validate system activation."""
        evidence = []
        certainty = 0.0
        
        # Test email reading
        try:
            message_dirs = find_mail_app_messages()
            if message_dirs:
                emails = read_emails_from_messages_dirs(message_dirs, days=1, use_incremental=False)
                evidence.append(f"Successfully read {len(emails)} emails")
                certainty += 0.5
                
                if len(emails) > 0:
                    evidence.append("Email reading functional")
                    certainty += 0.3
                else:
                    evidence.append("No emails found (may be expected)")
                    certainty += 0.1
            else:
                evidence.append("No Mail.app directories (fallback available)")
                certainty += 0.2
        except Exception as e:
            return ValidationResult(
                component="Activation",
                status=EpistemicStatus.CONTRADICTED,
                certainty=0.0,
                evidence=f"Activation failed: {str(e)}",
                details={"error": str(e)}
            )
        
        # Test analyzer
        try:
            analyzer = EmailAnalyzer()
            evidence.append("EmailAnalyzer initialized")
            certainty += 0.2
        except Exception as e:
            return ValidationResult(
                component="Activation",
                status=EpistemicStatus.CONTRADICTED,
                certainty=0.0,
                evidence=f"Analyzer initialization failed: {str(e)}",
                details={"error": str(e)}
            )
        
        status = EpistemicStatus.VALIDATED if certainty >= 0.9 else EpistemicStatus.INFERRED
        
        return ValidationResult(
            component="Activation",
            status=status,
            certainty=min(1.0, certainty),
            evidence="; ".join(evidence),
            details={"emails_read": len(emails) if 'emails' in locals() else 0}
        )
    
    def validate_automation(self) -> ValidationResult:
        """Validate automation setup."""
        evidence = []
        certainty = 0.0
        
        # Check cron job
        try:
            import subprocess
            result = subprocess.run(
                ['crontab', '-l'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'analyze_email_from_mailapp.py' in result.stdout:
                evidence.append("Cron job configured")
                certainty += 0.5
            else:
                evidence.append("Cron job not found (may need setup)")
                certainty += 0.1
        except Exception:
            evidence.append("Could not check cron (may not be configured)")
            certainty += 0.1
        
        # Check last run timestamp
        last_run = get_last_run_timestamp()
        if last_run:
            evidence.append(f"Last run: {last_run.strftime('%Y-%m-%d %H:%M:%S')}")
            certainty += 0.3
        else:
            evidence.append("No previous run timestamp (first run)")
            certainty += 0.1
        
        # Check cache file
        if LAST_RUN_FILE.exists():
            evidence.append("Cache file exists")
            certainty += 0.2
        else:
            evidence.append("Cache file not created yet")
            certainty += 0.1
        
        status = EpistemicStatus.VALIDATED if certainty >= 0.8 else EpistemicStatus.INFERRED
        
        return ValidationResult(
            component="Automation",
            status=status,
            certainty=min(1.0, certainty),
            evidence="; ".join(evidence),
            details={"last_run": last_run.isoformat() if last_run else None}
        )
    
    def validate_real_world_test(self) -> ValidationResult:
        """Run real-world test and validate results."""
        evidence = []
        certainty = 0.0
        
        try:
            # Run actual analysis
            message_dirs = find_mail_app_messages()
            if not message_dirs:
                return ValidationResult(
                    component="Real-World Test",
                    status=EpistemicStatus.UNKNOWN,
                    certainty=0.0,
                    evidence="No Mail.app directories found",
                    details={}
                )
            
            # Read emails
            emails = read_emails_from_messages_dirs(message_dirs, days=30, use_incremental=True)
            evidence.append(f"Read {len(emails)} emails")
            certainty += 0.3
            
            if len(emails) == 0:
                evidence.append("No emails found (may be expected if incremental)")
                certainty += 0.1
                return ValidationResult(
                    component="Real-World Test",
                    status=EpistemicStatus.INFERRED,
                    certainty=certainty,
                    evidence="; ".join(evidence),
                    details={"emails": 0}
                )
            
            # Analyze newsletters
            analyzer = EmailAnalyzer()
            newsletter_count = 0
            for msg in emails:
                if analyzer.parse_email_imap(msg):
                    newsletter_count += 1
            
            evidence.append(f"Found {newsletter_count} AI newsletters")
            certainty += 0.4
            
            # Generate report
            report = analyzer.generate_report()
            evidence.append("Report generated successfully")
            certainty += 0.2
            
            # Validate report structure
            required_keys = ['total_newsletters', 'total_opportunities', 'key_themes']
            missing_keys = [k for k in required_keys if k not in report]
            if not missing_keys:
                evidence.append("Report structure valid")
                certainty += 0.1
            else:
                evidence.append(f"Report missing keys: {missing_keys}")
                certainty -= 0.1
            
            status = EpistemicStatus.VALIDATED if certainty >= 0.9 else EpistemicStatus.INFERRED
            
            return ValidationResult(
                component="Real-World Test",
                status=status,
                certainty=min(1.0, certainty),
                evidence="; ".join(evidence),
                details={
                    "emails": len(emails),
                    "newsletters": newsletter_count,
                    "opportunities": report.get('total_opportunities', 0),
                    "themes": len(report.get('key_themes', {}))
                }
            )
            
        except Exception as e:
            return ValidationResult(
                component="Real-World Test",
                status=EpistemicStatus.CONTRADICTED,
                certainty=0.0,
                evidence=f"Test failed: {str(e)}",
                details={"error": str(e)}
            )
    
    def validate_all(self) -> Dict[str, Any]:
        """Run all validations."""
        print("=" * 80)
        print("EPISTEMIC VALIDATION - EMAIL CONVERGENCE SYSTEM")
        print("Pattern: OBSERVER × TRUTH × EPISTEMIC × VALIDATION × ONE")
        print("=" * 80)
        print()
        
        # Run validations
        init_result = self.validate_initialization()
        self.results.append(init_result)
        
        activation_result = self.validate_activation()
        self.results.append(activation_result)
        
        automation_result = self.validate_automation()
        self.results.append(automation_result)
        
        real_world_result = self.validate_real_world_test()
        self.results.append(real_world_result)
        
        # Display results
        print("VALIDATION RESULTS:")
        print()
        
        for result in self.results:
            status_icon = {
                EpistemicStatus.VALIDATED: "",
                EpistemicStatus.INFERRED: "",
                EpistemicStatus.UNKNOWN: "",
                EpistemicStatus.CONTRADICTED: ""
            }[result.status]
            
            print(f"{status_icon} {result.component}")
            print(f"   Status: {result.status.value.upper()}")
            print(f"   Certainty: {result.certainty:.1%}")
            print(f"   Evidence: {result.evidence}")
            if result.details:
                print(f"   Details: {json.dumps(result.details, indent=6, default=str)}")
            print()
        
        # Calculate overall status
        overall_certainty = sum(r.certainty for r in self.results) / len(self.results)
        validated_count = sum(1 for r in self.results if r.status == EpistemicStatus.VALIDATED)
        
        if validated_count == len(self.results) and overall_certainty >= 0.9:
            overall_status = EpistemicStatus.VALIDATED
            status_icon = ""
        elif validated_count >= len(self.results) * 0.75 and overall_certainty >= 0.7:
            overall_status = EpistemicStatus.INFERRED
            status_icon = ""
        else:
            overall_status = EpistemicStatus.UNKNOWN
            status_icon = ""
        
        print("=" * 80)
        print(f"{status_icon} OVERALL STATUS: {overall_status.value.upper()}")
        print(f"   Certainty: {overall_certainty:.1%}")
        print(f"   Validated: {validated_count}/{len(self.results)}")
        print("=" * 80)
        print()
        
        # Save results
        results_file = f"EMAIL_CONVERGENCE_VALIDATION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "overall_status": overall_status.value,
                "overall_certainty": overall_certainty,
                "results": [asdict(r) | {"status": r.status.value} for r in self.results]
            }, f, indent=2, default=str)
        
        print(f" Validation results saved to: {results_file}")
        print()
        print("Pattern: OBSERVER × TRUTH × EPISTEMIC × VALIDATION × ONE")
        print("∞ AbëONE ∞")
        
        return {
            "overall_status": overall_status.value,
            "overall_certainty": overall_certainty,
            "validated_count": validated_count,
            "total_count": len(self.results),
            "results": [asdict(r) | {"status": r.status.value} for r in self.results]
        }


def main():
    """Main execution."""
    validator = EpistemicValidator()
    results = validator.validate_all()
    
    # Exit with appropriate code
    if results["overall_status"] == "validated":
        sys.exit(0)
    elif results["overall_status"] == "inferred":
        sys.exit(1)  # Warning but not failure
    else:
        sys.exit(2)  # Failure


if __name__ == '__main__':
    main()

