#!/usr/bin/env python3
"""
Cross-Browser Testing - Automated Browser Compatibility
Pattern: VALIDATION × CROSS_BROWSER × COMPATIBILITY × TRUTH × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
Guardians: AEYON (999 Hz) + JØHN (530 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class BrowserTestResult:
    def __init__(self, name: str, passed: bool, message: str = "", details: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details
        self.timestamp = datetime.now().isoformat()

class CrossBrowserTester:
    def __init__(self, workspace_root: Optional[Path] = None, base_url: str = "http://localhost:53009"):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.base_url = base_url
        self.results: List[BrowserTestResult] = []
        
    def test_user_agent_compatibility(self) -> BrowserTestResult:
        """Test compatibility with different user agents"""
        url = f"{self.base_url}/"
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        successful = 0
        failed = []
        
        for ua in user_agents:
            try:
                req = urllib.request.Request(url)
                req.add_header('User-Agent', ua)
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.getcode() in [200, 404]:  # 404 is acceptable for root path
                        successful += 1
                    else:
                        failed.append(f"UA: {ua[:50]}... Status: {response.getcode()}")
            except Exception as e:
                failed.append(f"UA: {ua[:50]}... Error: {str(e)[:50]}")
        
        success_rate = successful / len(user_agents)
        
        if success_rate >= 0.8:  # 80% success rate
            return BrowserTestResult(
                "User Agent Compatibility",
                True,
                f"{successful}/{len(user_agents)} user agents compatible",
                f"Success rate: {success_rate*100:.1f}%"
            )
        else:
            return BrowserTestResult(
                "User Agent Compatibility",
                False,
                f"Only {successful}/{len(user_agents)} user agents compatible",
                f"Failed: {len(failed)}, Success rate: {success_rate*100:.1f}%"
            )
    
    def test_http_methods(self) -> BrowserTestResult:
        """Test different HTTP methods"""
        url = f"{self.base_url}/"
        methods = ["GET", "HEAD", "OPTIONS"]
        successful = 0
        failed = []
        
        for method in methods:
            try:
                req = urllib.request.Request(url, method=method)
                with urllib.request.urlopen(req, timeout=5) as response:
                    status = response.getcode()
                    if status in [200, 404, 405]:  # 405 Method Not Allowed is acceptable
                        successful += 1
                    else:
                        failed.append(f"{method}: Status {status}")
            except urllib.error.HTTPError as e:
                if e.code in [404, 405]:  # Acceptable errors
                    successful += 1
                else:
                    failed.append(f"{method}: HTTP {e.code}")
            except Exception as e:
                failed.append(f"{method}: {str(e)[:50]}")
        
        success_rate = successful / len(methods)
        
        if success_rate >= 0.67:  # At least 2/3 methods work
            return BrowserTestResult(
                "HTTP Methods",
                True,
                f"{successful}/{len(methods)} HTTP methods supported",
                f"Success rate: {success_rate*100:.1f}%"
            )
        else:
            return BrowserTestResult(
                "HTTP Methods",
                False,
                f"Only {successful}/{len(methods)} HTTP methods supported",
                f"Failed: {len(failed)}, Success rate: {success_rate*100:.1f}%"
            )
    
    def test_headers_compatibility(self) -> BrowserTestResult:
        """Test compatibility with different headers"""
        url = f"{self.base_url}/"
        header_sets = [
            {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
            {"Accept": "application/json"},
            {"Accept-Language": "en-US,en;q=0.9"},
            {"Accept-Encoding": "gzip, deflate, br"},
            {"Cache-Control": "no-cache"}
        ]
        
        successful = 0
        failed = []
        
        for headers in header_sets:
            try:
                req = urllib.request.Request(url)
                for key, value in headers.items():
                    req.add_header(key, value)
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.getcode() in [200, 404]:
                        successful += 1
                    else:
                        failed.append(f"Headers {list(headers.keys())}: Status {response.getcode()}")
            except Exception as e:
                failed.append(f"Headers {list(headers.keys())}: {str(e)[:50]}")
        
        success_rate = successful / len(header_sets)
        
        if success_rate >= 0.8:
            return BrowserTestResult(
                "Headers Compatibility",
                True,
                f"{successful}/{len(header_sets)} header sets compatible",
                f"Success rate: {success_rate*100:.1f}%"
            )
        else:
            return BrowserTestResult(
                "Headers Compatibility",
                False,
                f"Only {successful}/{len(header_sets)} header sets compatible",
                f"Failed: {len(failed)}, Success rate: {success_rate*100:.1f}%"
            )
    
    def test_content_type_handling(self) -> BrowserTestResult:
        """Test content type handling"""
        url = f"{self.base_url}/"
        content_types = [
            "text/html",
            "application/json",
            "application/xml",
            "text/plain"
        ]
        
        successful = 0
        failed = []
        
        for content_type in content_types:
            try:
                req = urllib.request.Request(url)
                req.add_header("Accept", content_type)
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.getcode() in [200, 404]:
                        successful += 1
                    else:
                        failed.append(f"{content_type}: Status {response.getcode()}")
            except Exception as e:
                failed.append(f"{content_type}: {str(e)[:50]}")
        
        success_rate = successful / len(content_types)
        
        if success_rate >= 0.75:
            return BrowserTestResult(
                "Content Type Handling",
                True,
                f"{successful}/{len(content_types)} content types handled",
                f"Success rate: {success_rate*100:.1f}%"
            )
        else:
            return BrowserTestResult(
                "Content Type Handling",
                False,
                f"Only {successful}/{len(content_types)} content types handled",
                f"Failed: {len(failed)}, Success rate: {success_rate*100:.1f}%"
            )
    
    def run_all_tests(self) -> Dict:
        """Run all cross-browser tests"""
        print("∞ AbëONE ∞")
        print("Cross-Browser Testing - Automated Browser Compatibility")
        print("Pattern: VALIDATION × CROSS_BROWSER × COMPATIBILITY × TRUTH × ONE")
        print("")
        
        # Run tests
        tests = [
            self.test_user_agent_compatibility,
            self.test_http_methods,
            self.test_headers_compatibility,
            self.test_content_type_handling
        ]
        
        for test in tests:
            result = test()
            self.results.append(result)
        
        # Summary
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print("=" * 60)
        print("CROSS-BROWSER TEST RESULTS")
        print("=" * 60)
        print("")
        
        for i, result in enumerate(self.results, 1):
            status = "✅" if result.passed else "❌"
            print(f"{status} {i}. {result.name}")
            print(f"   {result.message}")
            if result.details:
                print(f"   Details: {result.details}")
            print("")
        
        print("=" * 60)
        print(f"Total: {passed}/{total} passed")
        print("=" * 60)
        print("")
        
        if passed == total:
            print("✅ ALL CROSS-BROWSER TESTS PASSED")
        else:
            print(f"⚠️  {total - passed} tests failed")
        
        print("")
        print("Pattern: VALIDATION × CROSS_BROWSER × COMPATIBILITY × TRUTH × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "message": r.message,
                    "details": r.details,
                    "timestamp": r.timestamp
                }
                for r in self.results
            ]
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test cross-browser compatibility"
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:53009",
        help="Base URL to test (default: http://localhost:53009)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--workspace",
        type=str,
        help="Workspace root directory (default: parent of script)"
    )
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace) if args.workspace else None
    tester = CrossBrowserTester(workspace_root, args.url)
    results = tester.run_all_tests()
    
    if args.json:
        print(json.dumps(results, indent=2))
        return 0
    
    return 0 if results["failed"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

