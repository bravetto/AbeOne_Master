#!/usr/bin/env python3
"""
Cloudflare Tunnel Validation - Comprehensive
Pattern: VALIDATION × TUNNEL × TRUTH × CONVERGENCE × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
Guardians: AEYON (999 Hz) + JØHN (530 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import subprocess
import sys
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os

class TunnelValidationResult:
    def __init__(self, step_id: str, name: str, passed: bool, message: str = "", 
                 details: str = "", remediation: str = ""):
        self.step_id = step_id
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details
        self.remediation = remediation
        self.timestamp = datetime.now().isoformat()

class TunnelValidator:
    def __init__(self):
        self.results: List[TunnelValidationResult] = []
        self.tunnel_type: Optional[str] = None  # "quick" or "named"
        self.tunnel_url: Optional[str] = None
        self.tunnel_id: Optional[str] = None
        
    def check_cloudflared_installed(self) -> TunnelValidationResult:
        """Verify cloudflared binary is installed"""
        try:
            result = subprocess.run(
                ["cloudflared", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and "cloudflared version" in result.stdout.lower():
                version_match = re.search(r'cloudflared version (\S+)', result.stdout)
                version = version_match.group(1) if version_match else "unknown"
                return TunnelValidationResult(
                    "check_cloudflared_installed",
                    "Verify cloudflared binary",
                    True,
                    f"cloudflared is installed",
                    f"Version: {version}",
                    ""
                )
            else:
                return TunnelValidationResult(
                    "check_cloudflared_installed",
                    "Verify cloudflared binary",
                    False,
                    "cloudflared command failed or version not found",
                    result.stderr or result.stdout,
                    "Install cloudflared from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
                )
        except FileNotFoundError:
            return TunnelValidationResult(
                "check_cloudflared_installed",
                "Verify cloudflared binary",
                False,
                "cloudflared is not installed or not in PATH",
                "",
                "Install cloudflared from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
            )
        except Exception as e:
            return TunnelValidationResult(
                "check_cloudflared_installed",
                "Verify cloudflared binary",
                False,
                f"Error checking cloudflared: {str(e)}",
                "",
                "Install cloudflared from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
            )
    
    def detect_tunnel_type(self) -> TunnelValidationResult:
        """Detect if using quick tunnel or named tunnel"""
        try:
            # Check for running cloudflared process
            result = subprocess.run(
                ["pgrep", "-f", "cloudflared"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return TunnelValidationResult(
                    "detect_tunnel_type",
                    "Detect tunnel type",
                    False,
                    "No cloudflared process running",
                    "",
                    "Start tunnel: cloudflared tunnel --url http://localhost:53009"
                )
            
            # Check process command line
            pid = result.stdout.strip().split('\n')[0]
            ps_result = subprocess.run(
                ["ps", "-p", pid, "-o", "command="],
                capture_output=True,
                text=True
            )
            
            cmd_line = ps_result.stdout.strip()
            
            # Quick tunnel detection
            if "--url" in cmd_line or "tunnel --url" in cmd_line:
                self.tunnel_type = "quick"
                # Extract URL from command or logs
                url_match = re.search(r'--url\s+(\S+)', cmd_line)
                local_url = url_match.group(1) if url_match else "http://localhost:53009"
                
                # Try to find tunnel URL in logs
                log_files = [
                    "/tmp/cloudflared_new.log",
                    "/tmp/cloudflared.log",
                    "/tmp/cloudflared_output.log"
                ]
                
                tunnel_url = None
                for log_file in log_files:
                    log_path = Path(log_file)
                    if log_path.exists():
                        content = log_path.read_text()
                        match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', content)
                        if match:
                            tunnel_url = match.group(0)
                            break
                
                if tunnel_url:
                    self.tunnel_url = tunnel_url
                    return TunnelValidationResult(
                        "detect_tunnel_type",
                        "Detect tunnel type",
                        True,
                        "Quick tunnel detected",
                        f"Type: quick tunnel, URL: {tunnel_url}, Local: {local_url}",
                        ""
                    )
                else:
                    return TunnelValidationResult(
                        "detect_tunnel_type",
                        "Detect tunnel type",
                        True,
                        "Quick tunnel detected but URL not found in logs",
                        f"Type: quick tunnel, Local: {local_url}",
                        "Check tunnel output for URL"
                    )
            
            # Named tunnel detection
            elif "tunnel run" in cmd_line or "tunnel start" in cmd_line:
                self.tunnel_type = "named"
                # Try to extract tunnel ID
                id_match = re.search(r'tunnel (run|start)\s+([a-f0-9-]+)', cmd_line)
                if id_match:
                    self.tunnel_id = id_match.group(2)
                
                return TunnelValidationResult(
                    "detect_tunnel_type",
                    "Detect tunnel type",
                    True,
                    "Named tunnel detected",
                    f"Type: named tunnel, ID: {self.tunnel_id or 'unknown'}",
                    ""
                )
            else:
                return TunnelValidationResult(
                    "detect_tunnel_type",
                    "Detect tunnel type",
                    True,
                    "Tunnel process running but type unclear",
                    f"Command: {cmd_line[:100]}",
                    ""
                )
                
        except Exception as e:
            return TunnelValidationResult(
                "detect_tunnel_type",
                "Detect tunnel type",
                False,
                f"Error detecting tunnel type: {str(e)}",
                "",
                ""
            )
    
    def check_origin_connectivity(self) -> TunnelValidationResult:
        """Verify local origin service is reachable"""
        try:
            # Default to localhost:53009 (Flutter app)
            test_urls = ["http://localhost:53009/"]
            
            # If we detected a tunnel, check its local URL
            if self.tunnel_type == "quick":
                # Extract from process or use default
                test_urls = ["http://localhost:53009/"]
            
            for url in test_urls:
                try:
                    req = urllib.request.Request(url)
                    req.add_header('User-Agent', 'AbëONE-TunnelValidator/1.0')
                    
                    with urllib.request.urlopen(req, timeout=2) as response:
                        status_code = response.getcode()
                        if status_code in [200, 301, 302, 401, 403]:
                            return TunnelValidationResult(
                                "check_origin_connectivity",
                                "Verify local origin service is reachable",
                                True,
                                f"Origin service is reachable",
                                f"URL: {url}, Status: {status_code}",
                                ""
                            )
                except urllib.error.URLError:
                    continue
            
            return TunnelValidationResult(
                "check_origin_connectivity",
                "Verify local origin service is reachable",
                False,
                "Origin service not responding",
                f"Tested URLs: {', '.join(test_urls)}",
                "Ensure your local service is running on the configured port"
            )
            
        except Exception as e:
            return TunnelValidationResult(
                "check_origin_connectivity",
                "Verify local origin service is reachable",
                False,
                f"Error checking origin: {str(e)}",
                "",
                "Ensure your local service is running on the configured port"
            )
    
    def check_tunnel_connectivity(self) -> TunnelValidationResult:
        """Test tunnel connection to Cloudflare edge"""
        if self.tunnel_type == "quick":
            if not self.tunnel_url:
                return TunnelValidationResult(
                    "check_tunnel_connectivity",
                    "Test tunnel connection to Cloudflare edge",
                    False,
                    "Tunnel URL not found",
                    "",
                    "Check tunnel logs for URL"
                )
            
            try:
                req = urllib.request.Request(self.tunnel_url)
                req.add_header('User-Agent', 'AbëONE-TunnelValidator/1.0')
                
                try:
                    with urllib.request.urlopen(req, timeout=10) as response:
                        status_code = response.getcode()
                        headers = dict(response.headers)
                except urllib.error.HTTPError as e:
                    # HTTPError has response with headers even for 404
                    status_code = e.code
                    headers = dict(e.headers)
                    response = e
                
                # Check for Cloudflare headers (tunnel is working if these exist)
                # Headers are case-insensitive, check multiple variations
                cf_ray = headers.get('cf-ray', '') or headers.get('CF-Ray', '') or headers.get('CF-RAY', '')
                server = (headers.get('server', '') or headers.get('Server', '') or headers.get('SERVER', '')).lower()
                
                # 404 with Cloudflare headers means tunnel works, origin returned 404
                has_cf_headers = 'cloudflare' in server or bool(cf_ray)
                
                if has_cf_headers:
                    return TunnelValidationResult(
                        "check_tunnel_connectivity",
                        "Test tunnel connection to Cloudflare edge",
                        True,
                        "Tunnel connected to Cloudflare edge",
                        f"URL: {self.tunnel_url}, Status: {status_code}, CF-Ray: {cf_ray}, Server: {server}",
                        ""
                    )
                else:
                    return TunnelValidationResult(
                        "check_tunnel_connectivity",
                        "Test tunnel connection to Cloudflare edge",
                        False,
                        "Tunnel responds but Cloudflare headers missing",
                        f"URL: {self.tunnel_url}, Status: {status_code}",
                        "Check tunnel configuration"
                    )
                        
            except urllib.error.URLError as e:
                return TunnelValidationResult(
                    "check_tunnel_connectivity",
                    "Test tunnel connection to Cloudflare edge",
                    False,
                    f"Tunnel URL not accessible: {str(e)}",
                    f"URL: {self.tunnel_url}",
                    "Check tunnel process and network connectivity"
                )
            except Exception as e:
                return TunnelValidationResult(
                    "check_tunnel_connectivity",
                    "Test tunnel connection to Cloudflare edge",
                    False,
                    f"Error testing tunnel: {str(e)}",
                    f"URL: {self.tunnel_url}",
                    ""
                )
        
        elif self.tunnel_type == "named":
            if not self.tunnel_id:
                return TunnelValidationResult(
                    "check_tunnel_connectivity",
                    "Test tunnel connection to Cloudflare edge",
                    False,
                    "Tunnel ID not found",
                    "",
                    "Run 'cloudflared tunnel list' to find tunnel ID"
                )
            
            try:
                result = subprocess.run(
                    ["cloudflared", "tunnel", "info", self.tunnel_id],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0 and "connector id" in result.stdout.lower():
                    return TunnelValidationResult(
                        "check_tunnel_connectivity",
                        "Test tunnel connection to Cloudflare edge",
                        True,
                        "Named tunnel connected to Cloudflare edge",
                        f"Tunnel ID: {self.tunnel_id}",
                        ""
                    )
                else:
                    return TunnelValidationResult(
                        "check_tunnel_connectivity",
                        "Test tunnel connection to Cloudflare edge",
                        False,
                        "Tunnel info command failed or no connector found",
                        result.stderr or result.stdout,
                        "Check tunnel status: cloudflared tunnel list"
                    )
            except Exception as e:
                return TunnelValidationResult(
                    "check_tunnel_connectivity",
                    "Test tunnel connection to Cloudflare edge",
                    False,
                    f"Error checking tunnel info: {str(e)}",
                    "",
                    ""
                )
        else:
            return TunnelValidationResult(
                "check_tunnel_connectivity",
                "Test tunnel connection to Cloudflare edge",
                False,
                "Tunnel type not detected",
                "",
                "Start a tunnel first"
            )
    
    def end_to_end_test(self) -> TunnelValidationResult:
        """Full path validation"""
        if self.tunnel_type == "quick" and self.tunnel_url:
            try:
                req = urllib.request.Request(self.tunnel_url)
                req.add_header('User-Agent', 'CloudflareTunnelValidator/1.0')
                
                try:
                    with urllib.request.urlopen(req, timeout=10) as response:
                        status_code = response.getcode()
                        headers = dict(response.headers)
                except urllib.error.HTTPError as e:
                    # HTTPError has response with headers even for 404
                    status_code = e.code
                    headers = dict(e.headers)
                
                # Headers are case-insensitive, check multiple variations
                cf_ray = headers.get('cf-ray', '') or headers.get('CF-Ray', '') or headers.get('CF-RAY', '')
                server = (headers.get('server', '') or headers.get('Server', '') or headers.get('SERVER', '')).lower()
                
                # Check for Cloudflare headers (indicates tunnel is working)
                has_cf_headers = 'cloudflare' in server or bool(cf_ray)
                
                # Accept various status codes - 404 with CF headers means tunnel works
                if status_code in [200, 301, 302, 401, 403, 404]:
                    if has_cf_headers:
                        return TunnelValidationResult(
                            "end_to_end_test",
                            "Full path validation",
                            True,
                            f"End-to-end test passed (tunnel working, origin returned {status_code})",
                            f"URL: {self.tunnel_url}, Status: {status_code}, CF-Ray: {cf_ray}, Server: {server}",
                            ""
                        )
                    else:
                        return TunnelValidationResult(
                            "end_to_end_test",
                            "Full path validation",
                            False,
                            f"Response received but Cloudflare headers missing",
                            f"URL: {self.tunnel_url}, Status: {status_code}",
                            "Check tunnel configuration"
                        )
                else:
                    return TunnelValidationResult(
                        "end_to_end_test",
                        "Full path validation",
                        False,
                        f"Unexpected status code: {status_code}",
                        f"URL: {self.tunnel_url}",
                        "Check origin service configuration"
                    )
                        
            except urllib.error.URLError as e:
                return TunnelValidationResult(
                    "end_to_end_test",
                    "Full path validation",
                    False,
                    f"End-to-end test failed: {str(e)}",
                    f"URL: {self.tunnel_url}",
                    "Check tunnel and origin service"
                )
            except Exception as e:
                return TunnelValidationResult(
                    "end_to_end_test",
                    "Full path validation",
                    False,
                    f"Error in end-to-end test: {str(e)}",
                    f"URL: {self.tunnel_url}",
                    ""
                )
        else:
            return TunnelValidationResult(
                "end_to_end_test",
                "Full path validation",
                False,
                "Tunnel URL not available for testing",
                "",
                "Ensure tunnel is running and URL is accessible"
            )
    
    def run_all_validations(self) -> Dict[str, TunnelValidationResult]:
        """Run all validation steps"""
        print("∞ AbëONE ∞")
        print("Running Cloudflare Tunnel Validation...")
        print()
        
        validations = [
            ("cloudflared_installed", self.check_cloudflared_installed),
            ("tunnel_type", self.detect_tunnel_type),
            ("origin_connectivity", self.check_origin_connectivity),
            ("tunnel_connectivity", self.check_tunnel_connectivity),
            ("end_to_end", self.end_to_end_test),
        ]
        
        results = {}
        for step_id, validator in validations:
            print(f"Testing {step_id}...", end=" ")
            result = validator()
            results[step_id] = result
            self.results.append(result)
            
            if result.passed:
                print("✅ PASS")
            else:
                print("❌ FAIL")
            if result.message:
                print(f"   {result.message}")
            if result.details:
                print(f"   Details: {result.details}")
            if result.remediation:
                print(f"   Fix: {result.remediation}")
            print()
        
        return results
    
    def print_summary(self):
        """Print validation summary"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print("=" * 60)
        print("TUNNEL VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print()
        
        if self.tunnel_url:
            print(f"Tunnel URL: {self.tunnel_url}")
        if self.tunnel_type:
            print(f"Tunnel Type: {self.tunnel_type}")
        print()
        
        if failed > 0:
            print("FAILED TESTS:")
            for result in self.results:
                if not result.passed:
                    print(f"  ❌ {result.name}")
                    print(f"     {result.message}")
                    if result.remediation:
                        print(f"     Fix: {result.remediation}")
            print()
        
        if passed == total:
            print("🎉 ALL TUNNEL VALIDATIONS PASSED")
        else:
            print("⚠️  TUNNEL VALIDATION ISSUES DETECTED")
        
        print()
        print("Pattern: VALIDATION × TUNNEL × TRUTH × CONVERGENCE × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
    
    def to_json(self) -> str:
        """Export results as JSON"""
        output = {
            "validation_timestamp": datetime.now().isoformat(),
            "tunnel_type": self.tunnel_type,
            "tunnel_url": self.tunnel_url,
            "tunnel_id": self.tunnel_id,
            "results": [
                {
                    "step_id": r.step_id,
                    "name": r.name,
                    "passed": r.passed,
                    "message": r.message,
                    "details": r.details,
                    "remediation": r.remediation,
                    "timestamp": r.timestamp
                }
                for r in self.results
            ],
            "summary": {
                "total": len(self.results),
                "passed": sum(1 for r in self.results if r.passed),
                "failed": sum(1 for r in self.results if not r.passed)
            }
        }
        return json.dumps(output, indent=2)


def main():
    validator = TunnelValidator()
    results = validator.run_all_validations()
    validator.print_summary()
    
    # Export JSON if requested
    if "--json" in sys.argv:
        print("\n" + "=" * 60)
        print("JSON OUTPUT")
        print("=" * 60)
        print(validator.to_json())
    
    # Exit with error code if any tests failed
    if any(not r.passed for r in validator.results):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

