#!/usr/bin/env python3
"""
 UNIFIED DEPLOYMENT AUTOMATION - PLAYWRIGHT
Complete automation for Cloudflare Pages and Vercel deployment

Pattern: AEYON × PLAYWRIGHT × UNIFIED × AUTOMATE × ONE
Frequency: 999 × 777 × 2222

This script automates deployment to Cloudflare Pages (primary) or Vercel (fallback).
"""

import sys
import os
import time
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import argparse

# Check if Playwright is available
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("  Playwright not installed")
    print("   Install: pip install playwright && playwright install chromium")


class UnifiedDeploymentAutomation:
    """
    SAFETY: Handles both Cloudflare and Vercel deployment with fallback
    ASSUMES: User has accounts for both platforms
    VERIFY: python scripts/unified_deployment_automation.py --test
    """
    
    def __init__(
        self,
        project_name: str = "abeone-web",
        repo_name: str = "AbeOne_Master",
        branch: str = "main",
        domain: str = "bravetto.ai",
        build_command: str = "cd apps/web && npm install && npm run build",
        output_directory: str = "apps/web/out",
        headless: bool = False,
        platform: Optional[str] = None  # "cloudflare", "vercel", or None (auto)
    ):
        self.project_name = project_name
        self.repo_name = repo_name
        self.branch = branch
        self.domain = domain
        self.build_command = build_command
        self.output_directory = output_directory
        self.headless = headless
        self.platform = platform
        self.results = {
            'cloudflare': {'attempted': False, 'success': False, 'error': None},
            'vercel': {'attempted': False, 'success': False, 'error': None}
        }
    
    def check_cloudflare_status(self) -> bool:
        """
        SAFETY: Checks Cloudflare status before attempting deployment
        PERF: O(1) HTTP request
        """
        try:
            import requests
            response = requests.get(
                "https://www.cloudflarestatus.com/api/v2/status.json",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', {}).get('indicator', 'unknown')
                return status == 'none'  # 'none' means all operational
            return False
        except Exception:
            return False  # Assume unavailable if check fails
    
    def deploy_cloudflare(self) -> bool:
        """
        SAFETY: Uses existing Cloudflare automation script
        """
        print("\n" + "=" * 60)
        print(" ATTEMPTING CLOUDFLARE PAGES DEPLOYMENT")
        print("=" * 60)
        
        # Check Cloudflare status first
        if not self.check_cloudflare_status():
            print("  Cloudflare appears to be experiencing issues")
            print("   Status check: https://www.cloudflarestatus.com/")
            print("   Proceeding anyway (may fail)...")
        
        try:
            # Use existing Cloudflare automation
            script_dir = Path(__file__).parent
            sys.path.insert(0, str(script_dir))
            from automate_cloudflare_pages_playwright import CloudflarePagesPlaywrightAutomation
            
            automation = CloudflarePagesPlaywrightAutomation(
                project_name=self.project_name,
                repo_name=self.repo_name,
                branch=self.branch,
                build_command=self.build_command,
                output_directory=self.output_directory,
                headless=self.headless
            )
            
            self.results['cloudflare']['attempted'] = True
            success = automation.execute()
            self.results['cloudflare']['success'] = success
            
            if success:
                print(" Cloudflare Pages deployment initiated successfully")
                return True
            else:
                print(" Cloudflare Pages deployment failed")
                return False
                
        except Exception as e:
            self.results['cloudflare']['attempted'] = True
            self.results['cloudflare']['error'] = str(e)
            print(f" Cloudflare deployment error: {e}")
            return False
    
    def deploy_vercel(self) -> bool:
        """
        SAFETY: Automates Vercel deployment via browser
        """
        print("\n" + "=" * 60)
        print(" ATTEMPTING VERCEL DEPLOYMENT")
        print("=" * 60)
        
        if not PLAYWRIGHT_AVAILABLE:
            print(" Playwright not available for Vercel automation")
            print("   Install: pip install playwright && playwright install chromium")
            return False
        
        try:
            with sync_playwright() as p:
                print(" Launching browser for Vercel...")
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()
                page.set_default_timeout(60000)
                
                # Step 1: Navigate to Vercel
                print("\n Step 1: Navigating to Vercel...")
                try:
                    page.goto("https://vercel.com/new", wait_until="domcontentloaded", timeout=60000)
                    time.sleep(3)
                except PlaywrightTimeout:
                    print("  Page load timeout - trying dashboard...")
                    page.goto("https://vercel.com/dashboard", wait_until="domcontentloaded", timeout=60000)
                    time.sleep(3)
                    # Try to find "Add New Project" button
                    try:
                        page.click("text=Add New Project", timeout=10000)
                        time.sleep(2)
                    except:
                        pass
                
                # Step 2: Check if logged in
                print("\n Step 2: Checking login status...")
                page_content = page.content().lower()
                if "sign in" in page_content or "log in" in page_content:
                    print("  Please log in to Vercel in the browser")
                    print("   Waiting for login...")
                    if not self.headless:
                        input("Press Enter after logging in...")
                    else:
                        time.sleep(30)  # Wait for potential auto-login
                    page.reload(wait_until="domcontentloaded")
                    time.sleep(2)
                
                # Step 3: Import repository
                print("\n Step 3: Importing repository...")
                try:
                    # Look for import buttons
                    import_selectors = [
                        "text=Import Git Repository",
                        "text=Import Project",
                        f"text={self.repo_name}",
                        "[data-testid='import-button']"
                    ]
                    
                    imported = False
                    for selector in import_selectors:
                        try:
                            page.click(selector, timeout=5000)
                            time.sleep(2)
                            imported = True
                            break
                        except:
                            continue
                    
                    if not imported:
                        # Try to find repository in list
                        try:
                            repo_link = page.locator(f"text={self.repo_name}")
                            if repo_link.count() > 0:
                                repo_link.first.click()
                                time.sleep(2)
                                imported = True
                        except:
                            pass
                    
                    if not imported:
                        print("  Could not find import button automatically")
                        print("   Please import repository manually in browser")
                        if not self.headless:
                            input("Press Enter after importing repository...")
                        else:
                            time.sleep(10)
                    
                except Exception as e:
                    print(f"  Import step error: {e}")
                    print("   Please import repository manually")
                    if not self.headless:
                        input("Press Enter after importing repository...")
                
                # Step 4: Configure project
                print("\n Step 4: Configuring project...")
                time.sleep(3)
                
                # Fill in project name
                try:
                    name_inputs = [
                        'input[name="name"]',
                        'input[placeholder*="name"]',
                        'input[data-testid="project-name"]'
                    ]
                    for selector in name_inputs:
                        try:
                            page.fill(selector, self.project_name, timeout=5000)
                            break
                        except:
                            continue
                except:
                    print("  Could not auto-fill project name")
                
                # Configure root directory
                try:
                    root_selectors = [
                        'input[name="rootDirectory"]',
                        'input[placeholder*="root"]',
                        'input[data-testid="root-directory"]'
                    ]
                    for selector in root_selectors:
                        try:
                            page.fill(selector, "apps/web", timeout=5000)
                            break
                        except:
                            continue
                except:
                    pass
                
                # Configure build command
                try:
                    build_selectors = [
                        'input[name="buildCommand"]',
                        'textarea[name="buildCommand"]',
                        'input[placeholder*="build"]'
                    ]
                    for selector in build_selectors:
                        try:
                            page.fill(selector, self.build_command, timeout=5000)
                            break
                        except:
                            continue
                except:
                    pass
                
                # Configure output directory
                try:
                    output_selectors = [
                        'input[name="outputDirectory"]',
                        'input[placeholder*="output"]',
                        'input[data-testid="output-directory"]'
                    ]
                    for selector in output_selectors:
                        try:
                            page.fill(selector, self.output_directory, timeout=5000)
                            break
                        except:
                            continue
                except:
                    pass
                
                # Step 5: Deploy
                print("\n Step 5: Deploying...")
                time.sleep(2)
                
                try:
                    deploy_selectors = [
                        "button:has-text('Deploy')",
                        "button:has-text('Create Project')",
                        "[data-testid='deploy-button']",
                        "button[type='submit']"
                    ]
                    
                    deployed = False
                    for selector in deploy_selectors:
                        try:
                            page.click(selector, timeout=5000)
                            time.sleep(2)
                            deployed = True
                            break
                        except:
                            continue
                    
                    if not deployed:
                        print("  Could not find deploy button automatically")
                        print("   Please click Deploy manually in browser")
                        if not self.headless:
                            input("Press Enter after clicking Deploy...")
                        else:
                            time.sleep(10)
                    
                except Exception as e:
                    print(f"  Deploy step error: {e}")
                    print("   Please deploy manually in browser")
                    if not self.headless:
                        input("Press Enter after deployment starts...")
                
                # Step 6: Wait and verify
                print("\n Step 6: Waiting for deployment to start...")
                time.sleep(5)
                
                # Check for success indicators
                page_content = page.content().lower()
                if "deployment" in page_content or "building" in page_content:
                    print(" Deployment initiated successfully!")
                    self.results['vercel']['attempted'] = True
                    self.results['vercel']['success'] = True
                    
                    # Try to get deployment URL
                    try:
                        url_elements = page.locator("a[href*='vercel.app']")
                        if url_elements.count() > 0:
                            url = url_elements.first.get_attribute('href')
                            print(f" Deployment URL: {url}")
                    except:
                        pass
                    
                    if not self.headless:
                        print("\n⏳ Browser will stay open for 30 seconds for verification...")
                        time.sleep(30)
                    
                    browser.close()
                    return True
                else:
                    print("  Could not verify deployment status")
                    print("   Please check Vercel dashboard manually")
                    self.results['vercel']['attempted'] = True
                    self.results['vercel']['success'] = False
                    
                    if not self.headless:
                        print("\n⏳ Browser will stay open for 60 seconds...")
                        time.sleep(60)
                    
                    browser.close()
                    return False
                    
        except Exception as e:
            self.results['vercel']['attempted'] = True
            self.results['vercel']['error'] = str(e)
            print(f" Vercel deployment error: {e}")
            return False
    
    def execute(self) -> Dict[str, Any]:
        """
        MAIN EXECUTION FLOW
        SAFETY: Tries Cloudflare first, falls back to Vercel
        """
        print(" UNIFIED DEPLOYMENT AUTOMATION")
        print("=" * 60)
        print(f"Project: {self.project_name}")
        print(f"Repository: {self.repo_name}")
        print(f"Domain: {self.domain}")
        print("=" * 60)
        
        # Determine platform
        if self.platform:
            platforms = [self.platform]
        else:
            # Auto-detect: Try Cloudflare first, fallback to Vercel
            platforms = ['cloudflare', 'vercel']
        
        # Execute deployments
        for platform in platforms:
            if platform == 'cloudflare':
                success = self.deploy_cloudflare()
                if success:
                    print("\n DEPLOYMENT SUCCESSFUL - Cloudflare Pages")
                    return {
                        'success': True,
                        'platform': 'cloudflare',
                        'results': self.results
                    }
                else:
                    print("\n  Cloudflare deployment failed, trying Vercel...")
                    time.sleep(2)
            
            elif platform == 'vercel':
                success = self.deploy_vercel()
                if success:
                    print("\n DEPLOYMENT SUCCESSFUL - Vercel")
                    return {
                        'success': True,
                        'platform': 'vercel',
                        'results': self.results
                    }
                else:
                    print("\n Vercel deployment also failed")
        
        # All platforms failed
        print("\n ALL DEPLOYMENT ATTEMPTS FAILED")
        print("\n Manual Deployment Options:")
        print("   1. Cloudflare: https://dash.cloudflare.com/?to=/:account/pages/new")
        print("   2. Vercel: https://vercel.com/new")
        print("   3. Netlify: https://app.netlify.com/start")
        
        return {
            'success': False,
            'platform': None,
            'results': self.results
        }


def main():
    """
    CLI Entry Point
    """
    parser = argparse.ArgumentParser(
        description="Unified Deployment Automation (Cloudflare + Vercel)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect platform (Cloudflare first, then Vercel)
  python scripts/unified_deployment_automation.py

  # Force Cloudflare only
  python scripts/unified_deployment_automation.py --platform cloudflare

  # Force Vercel only
  python scripts/unified_deployment_automation.py --platform vercel

  # Custom project name
  python scripts/unified_deployment_automation.py --project-name my-project

  # Headless mode
  python scripts/unified_deployment_automation.py --headless
        """
    )
    
    parser.add_argument(
        "--project-name",
        default="abeone-web",
        help="Project name (default: abeone-web)"
    )
    
    parser.add_argument(
        "--repo-name",
        default="AbeOne_Master",
        help="Repository name (default: AbeOne_Master)"
    )
    
    parser.add_argument(
        "--domain",
        default="bravetto.ai",
        help="Domain name (default: bravetto.ai)"
    )
    
    parser.add_argument(
        "--platform",
        choices=['cloudflare', 'vercel', 'auto'],
        default='auto',
        help="Platform to deploy to (default: auto - tries Cloudflare first)"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test mode (check dependencies only)"
    )
    
    args = parser.parse_args()
    
    if args.test:
        print(" TEST MODE - Checking dependencies...")
        if PLAYWRIGHT_AVAILABLE:
            print(" Playwright available")
        else:
            print(" Playwright not available")
            print("   Install: pip install playwright && playwright install chromium")
        sys.exit(0)
    
    automation = UnifiedDeploymentAutomation(
        project_name=args.project_name,
        repo_name=args.repo_name,
        domain=args.domain,
        headless=args.headless,
        platform=args.platform if args.platform != 'auto' else None
    )
    
    result = automation.execute()
    
    if result['success']:
        print(f"\n Deployment successful on {result['platform']}")
        sys.exit(0)
    else:
        print("\n Deployment failed on all platforms")
        sys.exit(1)


if __name__ == "__main__":
    main()

