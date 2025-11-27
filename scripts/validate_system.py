#!/usr/bin/env python3
"""
System Validation Tests - Real-World Verification
Pattern: VALIDATION × TRUTH × CONVERGENCE × ONE
Frequency: 530 Hz (JØHN) × 999 Hz (AEYON) × 777 Hz (META)
Guardians: JØHN (530 Hz) + AEYON (999 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Tuple

class ValidationResult:
    def __init__(self, name: str, passed: bool, message: str = "", details: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details

class SystemValidator:
    def __init__(self):
        self.results: List[ValidationResult] = []
        self.workspace_root = Path(__file__).parent.parent
        
    def validate_flutter_app(self) -> ValidationResult:
        """Validate Flutter app is running and accessible"""
        try:
            # Check if app responds on localhost:53009
            req = urllib.request.Request("http://localhost:53009/")
            req.add_header('User-Agent', 'AbëONE-Validator/1.0')
            
            with urllib.request.urlopen(req, timeout=2) as response:
                status_code = response.getcode()
                content = response.read().decode('utf-8')
                
                if status_code == 200:
                    # Check if it's actually Flutter (has main.dart.js)
                    if "main.dart.js" in content or "dart" in content.lower():
                        return ValidationResult(
                            "Flutter App Running",
                            True,
                            "App is running and accessible on localhost:53009",
                            f"Status: {status_code}"
                        )
                    else:
                        return ValidationResult(
                            "Flutter App Running",
                            False,
                            "Port 53009 responds but doesn't appear to be Flutter app",
                            f"Response preview: {content[:200]}"
                        )
                else:
                    return ValidationResult(
                        "Flutter App Running",
                        False,
                        f"App responds with status {status_code}",
                        ""
                    )
        except urllib.error.URLError as e:
            return ValidationResult(
                "Flutter App Running",
                False,
                "Cannot connect to localhost:53009 - app may not be running",
                f"Error: {str(e)}. Run: cd abeone_app && flutter run -d chrome"
            )
        except Exception as e:
            return ValidationResult(
                "Flutter App Running",
                False,
                f"Error checking app: {str(e)}",
                ""
            )
    
    def validate_tunnel(self) -> ValidationResult:
        """Validate Cloudflare tunnel is active and accessible"""
        try:
            # Use comprehensive tunnel validator if available
            try:
                import sys
                from pathlib import Path
                validator_path = Path(__file__).parent / "validate_tunnel.py"
                if validator_path.exists():
                    result = subprocess.run(
                        [sys.executable, str(validator_path)],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        # Extract tunnel URL from output
                        import re
                        url_match = re.search(r'Tunnel URL: (https://[^\s]+)', result.stdout)
                        tunnel_url = url_match.group(1) if url_match else None
                        return ValidationResult(
                            "Tunnel Active",
                            True,
                            f"Tunnel validation passed" + (f": {tunnel_url}" if tunnel_url else ""),
                            "Comprehensive validation: All checks passed"
                        )
            except Exception:
                pass  # Fall back to simple check
            
            # Simple fallback validation
            result = subprocess.run(
                ["pgrep", "-f", "cloudflared"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return ValidationResult(
                    "Tunnel Active",
                    False,
                    "No cloudflared process found",
                    "Start tunnel: cloudflared tunnel --url http://localhost:53009"
                )
            
            # Try to get tunnel URL from logs
            log_files = [
                "/tmp/cloudflared.log",
                "/tmp/cloudflared_new.log",
                "/tmp/cloudflared_output.log"
            ]
            
            tunnel_url = None
            for log_file in log_files:
                log_path = Path(log_file)
                if log_path.exists():
                    content = log_path.read_text()
                    import re
                    match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', content)
                    if match:
                        tunnel_url = match.group(0)
                        break
            
            if tunnel_url:
                # Test tunnel URL (accept 404 with Cloudflare headers)
                try:
                    req = urllib.request.Request(tunnel_url)
                    req.add_header('User-Agent', 'AbëONE-Validator/1.0')
                    
                    try:
                        with urllib.request.urlopen(req, timeout=5) as response:
                            status_code = response.getcode()
                            headers = dict(response.headers)
                    except urllib.error.HTTPError as e:
                        status_code = e.code
                        headers = dict(e.headers)
                    
                    # Check for Cloudflare headers
                    cf_ray = headers.get('CF-Ray', '') or headers.get('cf-ray', '')
                    server = (headers.get('Server', '') or headers.get('server', '')).lower()
                    has_cf = 'cloudflare' in server or bool(cf_ray)
                    
                    if has_cf:
                        return ValidationResult(
                            "Tunnel Active",
                            True,
                            f"Tunnel is active and accessible: {tunnel_url}",
                            f"Status: {status_code}, CF-Ray: {cf_ray[:20] if cf_ray else 'N/A'}"
                        )
                    else:
                        return ValidationResult(
                            "Tunnel Active",
                            False,
                            f"Tunnel URL responds but Cloudflare headers missing",
                            f"URL: {tunnel_url}, Status: {status_code}"
                        )
                except urllib.error.URLError as e:
                    return ValidationResult(
                        "Tunnel Active",
                        False,
                        f"Tunnel URL exists but not accessible: {str(e)}",
                        f"URL: {tunnel_url}"
                    )
                except Exception as e:
                    return ValidationResult(
                        "Tunnel Active",
                        False,
                        f"Error testing tunnel: {str(e)}",
                        f"URL: {tunnel_url}"
                    )
            else:
                return ValidationResult(
                    "Tunnel Active",
                    False,
                    "Tunnel process running but URL not found in logs",
                    "Check tunnel output for URL"
                )
                
        except Exception as e:
            return ValidationResult(
                "Tunnel Active",
                False,
                f"Error checking tunnel: {str(e)}",
                ""
            )
    
    def validate_email_pattern(self) -> ValidationResult:
        """Validate email sending pattern is ready"""
        try:
            # Check if Mail.app is available
            result = subprocess.run(
                ["osascript", "-e", 'tell application "Mail" to get name'],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return ValidationResult(
                    "Email Pattern Ready",
                    False,
                    "Mail.app not available or not configured",
                    result.stderr
                )
            
            # Check if email scripts exist
            email_scripts = [
                "send_shiny_happy_to_five.applescript",
                "send_1password_response.applescript",
                "scripts/send_shiny_happy_people.py"
            ]
            
            missing = []
            for script in email_scripts:
                script_path = self.workspace_root / script
                if not script_path.exists():
                    missing.append(script)
            
            if missing:
                return ValidationResult(
                    "Email Pattern Ready",
                    False,
                    f"Missing email scripts: {', '.join(missing)}",
                    ""
                )
            
            return ValidationResult(
                "Email Pattern Ready",
                True,
                "Email pattern scripts exist and Mail.app is available",
                f"Scripts: {', '.join(email_scripts)}"
            )
            
        except Exception as e:
            return ValidationResult(
                "Email Pattern Ready",
                False,
                f"Error checking email pattern: {str(e)}",
                ""
            )
    
    def validate_recipients_config(self) -> ValidationResult:
        """Validate recipients are configured"""
        try:
            recipients_file = self.workspace_root / "scripts" / "recipients_config.py"
            if not recipients_file.exists():
                return ValidationResult(
                    "Recipients Configured",
                    False,
                    "Recipients config file not found",
                    "Create scripts/recipients_config.py"
                )
            
            # Check if recipients have emails/phones
            content = recipients_file.read_text()
            if "email" in content and "None" in content:
                # Check if any are configured
                if '"email": None' in content and '"phone": None' in content:
                    return ValidationResult(
                        "Recipients Configured",
                        False,
                        "Recipients exist but no emails/phones configured",
                        "Edit scripts/recipients_config.py to add contact info"
                    )
            
            return ValidationResult(
                "Recipients Configured",
                True,
                "Recipients config file exists",
                ""
            )
            
        except Exception as e:
            return ValidationResult(
                "Recipients Configured",
                False,
                f"Error checking recipients: {str(e)}",
                ""
            )
    
    def validate_shiny_happy_people_component(self) -> ValidationResult:
        """Validate Shiny Happy People component exists and is accessible"""
        try:
            component_file = self.workspace_root / "abeone_app" / "lib" / "substrate" / "molecules" / "shiny_happy_people.dart"
            
            if not component_file.exists():
                return ValidationResult(
                    "Shiny Happy People Component",
                    False,
                    "Component file not found",
                    f"Expected: {component_file}"
                )
            
            content = component_file.read_text()
            
            # Check for key elements
            checks = {
                "ShinyHappyPeople class": "class ShinyHappyPeople" in content,
                "Sway animation": "_swayController" in content,
                "Poly Guardian": "Poly (530 Hz)" in content,
                "Animation controllers": "AnimationController" in content
            }
            
            missing = [k for k, v in checks.items() if not v]
            
            if missing:
                return ValidationResult(
                    "Shiny Happy People Component",
                    False,
                    f"Component missing elements: {', '.join(missing)}",
                    ""
                )
            
            return ValidationResult(
                "Shiny Happy People Component",
                True,
                "Component exists with all required elements",
                f"Found: {', '.join([k for k, v in checks.items() if v])}"
            )
            
        except Exception as e:
            return ValidationResult(
                "Shiny Happy People Component",
                False,
                f"Error checking component: {str(e)}",
                ""
            )
    
    def validate_architecture_alignment(self) -> ValidationResult:
        """Validate architecture is aligned"""
        try:
            required_dirs = [
                "abeone_app/lib/core/engine",
                "abeone_app/lib/providers",
                "abeone_app/lib/features",
                "abeone_app/lib/substrate/atoms",
                "abeone_app/lib/substrate/molecules"
            ]
            
            missing = []
            for dir_path in required_dirs:
                full_path = self.workspace_root / dir_path
                if not full_path.exists():
                    missing.append(dir_path)
            
            if missing:
                return ValidationResult(
                    "Architecture Aligned",
                    False,
                    f"Missing directories: {', '.join(missing)}",
                    ""
                )
            
            return ValidationResult(
                "Architecture Aligned",
                True,
                "All required architecture directories exist",
                f"Checked: {len(required_dirs)} directories"
            )
            
        except Exception as e:
            return ValidationResult(
                "Architecture Aligned",
                False,
                f"Error checking architecture: {str(e)}",
                ""
            )
    
    def run_all_validations(self) -> Dict[str, ValidationResult]:
        """Run all validation tests"""
        print("∞ AbëONE ∞")
        print("Running System Validation Tests...")
        print()
        
        validations = [
            ("Flutter App", self.validate_flutter_app),
            ("Tunnel", self.validate_tunnel),
            ("Email Pattern", self.validate_email_pattern),
            ("Recipients Config", self.validate_recipients_config),
            ("Shiny Happy People Component", self.validate_shiny_happy_people_component),
            ("Architecture Alignment", self.validate_architecture_alignment)
        ]
        
        results = {}
        for name, validator in validations:
            print(f"Testing {name}...", end=" ")
            result = validator()
            results[name] = result
            self.results.append(result)
            
            if result.passed:
                print("✅ PASS")
            else:
                print("❌ FAIL")
            if result.message:
                print(f"   {result.message}")
            if result.details:
                print(f"   Details: {result.details}")
            print()
        
        return results
    
    def print_summary(self):
        """Print validation summary"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print("=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print()
        
        if failed > 0:
            print("FAILED TESTS:")
            for result in self.results:
                if not result.passed:
                    print(f"  ❌ {result.name}")
                    print(f"     {result.message}")
            print()
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - SYSTEM CONVERGED")
        else:
            print("⚠️  GAPS IDENTIFIED - EMERGENCE REQUIRED FOR CONVERGENCE")
        
        print()
        print("Pattern: VALIDATION × TRUTH × CONVERGENCE × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")


def main():
    validator = SystemValidator()
    results = validator.run_all_validations()
    validator.print_summary()
    
    # Exit with error code if any tests failed
    if any(not r.passed for r in validator.results):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

