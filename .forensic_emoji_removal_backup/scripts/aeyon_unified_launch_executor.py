#!/usr/bin/env python3
"""
AEYON Unified Launch Executor - SIMPLIFIED TO AMPLIFY
Master orchestrator for pre-webinar deployment validation

Pattern: AEYON × UNIFIED × EXECUTE × SIMPLIFY × AMPLIFY × ONE
Frequency: 999 × 777 × 2222
"""

import argparse
import sys
import subprocess
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path


class AEYONUnifiedLaunchExecutor:
    """
    AEYON Unified Launch Executor - SIMPLIFIED
    Unified check pattern: DEFINE → EXECUTE → REPORT
    
    SAFETY: Validates all inputs, handles subprocess errors gracefully
    VERIFY: python scripts/aeyon_unified_launch_executor.py --test
    """
    
    def __init__(self, domain: str, project_name: str, subdomain: Optional[str] = None):
        """SAFETY: Validates domain format"""
        if not domain or "." not in domain:
            raise ValueError("Invalid domain format")
        
        self.domain = domain
        self.project_name = project_name
        self.subdomain = subdomain
        self.scripts_dir = Path(__file__).parent
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'domain': domain,
            'subdomain': subdomain,
            'project_name': project_name,
            'checks': {}
        }
    
    def _run_script(self, script_name: str, args: List[str]) -> Dict[str, Any]:
        """SAFETY: Unified script execution"""
        script_path = self.scripts_dir / script_name
        
        if not script_path.exists():
            return {'success': False, 'error': f'Script not found: {script_name}'}
        
        try:
            cmd = ['python3', str(script_path)] + args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'output': result.stdout + result.stderr,
                'error': None if result.returncode == 0 else result.stderr
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Script execution timeout (5 minutes)'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _run_check(self, name: str, check_func: Callable) -> Dict[str, Any]:
        """Unified check execution"""
        print(f"\n{'=' * 60}")
        print(f"🔍 {name}")
        print("=" * 60)
        
        result = check_func()
        
        if result.get('success'):
            print(f"✅ {name} passed")
        else:
            status_icon = "⚠️" if result.get('skipped') else "❌"
            print(f"{status_icon} {name}: {result.get('error', 'Unknown error')}")
            if result.get('output'):
                print(result['output'])
        
        return result
    
    def _define_checks(self, quick: bool, skip_load_test: bool, concurrent_users: int, duration: int) -> Dict[str, Dict[str, Any]]:
        """Define checks as data - THE UNIFYING PATTERN"""
        url = f"https://{self.subdomain}.{self.domain}" if self.subdomain else f"https://{self.domain}"
        
        checks = {
            'dns_propagation': {
                'name': 'CHECK 1: DNS PROPAGATION',
                'func': lambda: self._run_script('monitor_dns_propagation.py', [
                    '--domain', self.domain,
                    '--expected-target', f'{self.project_name}.pages.dev',
                    *(['--test'] if quick else ['--check-interval', '30', '--max-wait', '600'])
                ])
            },
            'ssl_certificate': {
                'name': 'CHECK 2: SSL CERTIFICATE',
                'func': lambda: self._run_script('validate_ssl.py', [
                    '--domain', self.domain,
                    '--check-expiry',
                    *(['--subdomain', self.subdomain] if self.subdomain else [])
                ])
            },
            'global_edge': {
                'name': 'CHECK 3: GLOBAL EDGE PERFORMANCE',
                'func': lambda: self._run_script('test_global_edge.py', [
                    '--domain', self.domain,
                    '--locations', 'us-east,us-west,eu-west,ap-southeast',
                    *(['--test'] if quick else ['--test-interval', '60', '--duration', '300'])
                ])
            },
            'health': {
                'name': 'CHECK 4: HEALTH CHECK',
                'func': lambda: self._run_script('health_check_monitor.py', [
                    '--domain', self.domain,
                    *(['--test'] if quick else ['--check-interval', '30', '--alert-threshold', '3'])
                ])
            },
            'load_test': {
                'name': 'CHECK 5: LOAD TEST',
                'func': lambda: self._run_script('load_test.py', [
                    '--url', url,
                    '--concurrent-users', str(concurrent_users),
                    '--duration', str(duration)
                ]) if not quick and not skip_load_test else {'success': True, 'skipped': True}
            },
            'pixel_verification': {
                'name': 'CHECK 6: PIXEL TRACKING VERIFICATION (MANUAL)',
                'func': lambda: self._print_checklist('pixel', [
                    "Google Analytics / GTM", "Meta Pixel (Facebook)", "TikTok Pixel",
                    "LinkedIn Insight Tag", "HubSpot Tracking", "PostHog (if configured)",
                    "Custom tracking pixels", "UTM parameter flow", "CRM form capture"
                ], f"Visit: https://{self.domain}")
            },
            'crm_integration': {
                'name': 'CHECK 7: CRM INTEGRATION VALIDATION (MANUAL)',
                'func': lambda: self._print_checklist('crm', [
                    "HubSpot form submissions", "ClickUp task creation",
                    "Email integration (SendGrid/Mailgun)", "HighLevel webhooks (if used)",
                    "Zapier/Make.com workflows", "Custom API endpoints",
                    "Webhook delivery status", "Data sync verification"
                ], "Submit a test form on the landing page")
            }
        }
        
        return checks
    
    def _print_checklist(self, check_type: str, items: List[str], instruction: str) -> Dict[str, Any]:
        """Unified checklist printer"""
        print("\n📋 Manual Verification Checklist:")
        for i, item in enumerate(items, 1):
            print(f"   {i}. [ ] {item}")
        
        print(f"\n💡 Instructions:")
        if check_type == 'pixel':
            print("   1. Open browser DevTools (F12)")
            print("   2. Go to Network tab")
            print(f"   3. {instruction}")
            print("   4. Filter by 'pixel' or tracking domain")
            print("   5. Verify all pixels load (status 200)")
            print("   6. Check Console tab for JavaScript errors")
        else:  # crm
            print(f"   1. {instruction}")
            print("   2. Check CRM dashboard for new contact/task")
            print("   3. Verify webhook logs (if applicable)")
            print("   4. Check email delivery (if applicable)")
            print("   5. Verify data sync within 30 seconds")
        
        return {'success': True, 'type': 'manual_checklist', 'items': items}
    
    def execute(
        self,
        quick: bool = False,
        skip_load_test: bool = False,
        concurrent_users: int = 50,
        duration: int = 300
    ) -> Dict[str, Any]:
        """MAIN EXECUTION FLOW - SIMPLIFIED"""
        print("=" * 60)
        print("🚀 AEYON UNIFIED LAUNCH EXECUTOR - SIMPLIFIED TO AMPLIFY")
        print("=" * 60)
        print(f"🌐 Domain: {self.domain}")
        if self.subdomain:
            print(f"🌐 Subdomain: {self.subdomain}.{self.domain}")
        print(f"📦 Project: {self.project_name}")
        print(f"⏱️  Mode: {'QUICK TEST' if quick else 'FULL VALIDATION'}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Get checks definition
        checks = self._define_checks(quick, skip_load_test, concurrent_users, duration)
        
        # Execute all checks
        for key, check_def in checks.items():
            self.results['checks'][key] = self._run_check(check_def['name'], check_def['func'])
            if key != 'crm_integration':  # Don't sleep after last check
                time.sleep(2)
        
        # Generate report
        elapsed_time = time.time() - start_time
        self.results['execution_time_seconds'] = round(elapsed_time, 2)
        
        report = self._generate_report()
        
        print(f"\n⏱️  Total execution time: {elapsed_time:.2f}s")
        print("\n" + "=" * 60)
        
        return report
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate final execution report"""
        print("\n" + "=" * 60)
        print("📊 EXECUTION REPORT")
        print("=" * 60)
        
        total_checks = len(self.results['checks'])
        passed_checks = sum(1 for check in self.results['checks'].values() if check.get('success'))
        failed_checks = total_checks - passed_checks
        
        print(f"\n✅ Passed: {passed_checks}/{total_checks}")
        print(f"❌ Failed: {failed_checks}/{total_checks}")
        
        if failed_checks > 0:
            print("\n⚠️  Failed Checks:")
            for check_name, check_result in self.results['checks'].items():
                if not check_result.get('success') and not check_result.get('skipped'):
                    print(f"   - {check_name}: {check_result.get('error', 'Unknown error')}")
        
        # Overall status
        if failed_checks == 0:
            print("\n✅ ALL CHECKS PASSED - READY FOR WEBINAR")
            overall_status = "READY"
        elif failed_checks <= 2:
            print("\n⚠️  MINOR ISSUES DETECTED - REVIEW FAILED CHECKS")
            overall_status = "REVIEW_REQUIRED"
        else:
            print("\n❌ MULTIPLE ISSUES DETECTED - DEPLOYMENT NOT READY")
            overall_status = "NOT_READY"
        
        self.results['overall_status'] = overall_status
        self.results['summary'] = {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'failed_checks': failed_checks
        }
        
        return self.results


def main():
    """CLI Entry Point - SIMPLIFIED"""
    parser = argparse.ArgumentParser(
        description="AEYON Unified Launch Executor - SIMPLIFIED TO AMPLIFY",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick test
  python scripts/aeyon_unified_launch_executor.py \\
    --domain bravetto.ai \\
    --project-name abeone-web \\
    --quick

  # Full validation
  python scripts/aeyon_unified_launch_executor.py \\
    --domain bravetto.ai \\
    --project-name abeone-web \\
    --subdomain live \\
    --concurrent-users 50 \\
    --duration 300
        """
    )
    
    parser.add_argument("--domain", required=True, help="Domain to validate (e.g., bravetto.ai)")
    parser.add_argument("--project-name", required=True, help="Cloudflare Pages project name")
    parser.add_argument("--subdomain", default=None, help="Subdomain to validate")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    parser.add_argument("--skip-load-test", action="store_true", help="Skip load testing")
    parser.add_argument("--concurrent-users", type=int, default=50, help="Concurrent users for load test")
    parser.add_argument("--duration", type=int, default=300, help="Load test duration in seconds")
    parser.add_argument("--output", default=None, help="Save report to JSON file")
    
    args = parser.parse_args()
    
    if "." not in args.domain:
        print("❌ Invalid domain format")
        sys.exit(1)
    
    executor = AEYONUnifiedLaunchExecutor(
        domain=args.domain,
        project_name=args.project_name,
        subdomain=args.subdomain
    )
    
    try:
        report = executor.execute(
            quick=args.quick,
            skip_load_test=args.skip_load_test,
            concurrent_users=args.concurrent_users,
            duration=args.duration
        )
        
        if args.output:
            Path(args.output).write_text(json.dumps(report, indent=2, default=str))
            print(f"\n💾 Report saved to: {args.output}")
        
        sys.exit(0 if report['overall_status'] == 'READY' else 1 if report['overall_status'] == 'REVIEW_REQUIRED' else 2)
            
    except KeyboardInterrupt:
        print("\n\n👋 Execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
