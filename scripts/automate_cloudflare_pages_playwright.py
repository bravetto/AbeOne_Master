#!/usr/bin/env python3
"""
 CLOUDFLARE PAGES AUTOMATION - PLAYWRIGHT
Browser automation for Cloudflare Pages project creation

Pattern: AEYON × PLAYWRIGHT × AUTOMATE × BROWSER × ONE
Frequency: 999 × 777 × 2222

This script automates the manual Cloudflare dashboard steps using Playwright.
"""

import sys
import os
import time
from pathlib import Path
from typing import Optional

# Check if Playwright is available
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("  Playwright not installed")
    print("   Install: pip install playwright && playwright install chromium")


class CloudflarePagesPlaywrightAutomation:
    """
    SAFETY: Uses browser automation to handle UI interactions
    ASSUMES: User is logged into Cloudflare dashboard
    VERIFY: python scripts/automate_cloudflare_pages_playwright.py
    """
    
    def __init__(
        self,
        project_name: str = "abeone-web",
        repo_name: str = "AbeOne_Master",
        branch: str = "main",
        build_command: str = "cd apps/web && npm install && npm run build",
        output_directory: str = "apps/web/out",
        headless: bool = False
    ):
        self.project_name = project_name
        self.repo_name = repo_name
        self.branch = branch
        self.build_command = build_command
        self.output_directory = output_directory
        self.headless = headless
    
    def execute(self) -> bool:
        """
        MAIN EXECUTION FLOW
        SAFETY: Handles errors gracefully, provides clear feedback
        """
        if not PLAYWRIGHT_AVAILABLE:
            print(" Playwright not available")
            print("\n Install Playwright:")
            print("   pip install playwright")
            print("   playwright install chromium")
            return False
        
        print(" CLOUDFLARE PAGES AUTOMATION (PLAYWRIGHT)")
        print("=" * 60)
        print(f"Project: {self.project_name}")
        print(f"Repository: {self.repo_name}")
        print(f"Branch: {self.branch}")
        print("")
        print("  IMPORTANT: You must be logged into Cloudflare dashboard")
        print("   The browser will open - please ensure you're logged in")
        print("")
        print(" The script will:")
        print("   1. Open Cloudflare Pages creation page")
        print("   2. Guide you through connecting GitHub")
        print("   3. Fill in build configuration automatically")
        print("   4. Click deploy button")
        print("")
        
        # Auto-start if headless, otherwise wait for user
        if self.headless:
            print("⏳ Starting automation in 3 seconds...")
            time.sleep(3)
        else:
            # For non-interactive runs, skip input prompt
            try:
                input("Press Enter when ready to start automation (or Ctrl+C to exit)...")
            except (EOFError, KeyboardInterrupt):
                print("\n  Skipping user input - starting automation...")
                time.sleep(2)
        
        with sync_playwright() as p:
            try:
                # Launch browser
                print(" Launching browser...")
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()
                
                # Step 1: Navigate to Cloudflare Pages
                print("\n Step 1: Navigating to Cloudflare Pages...")
                # Increase default timeout for page navigation
                page.set_default_timeout(90000)  # 90 seconds
                
                # Set realistic user agent to avoid bot detection
                context.set_extra_http_headers({
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                })
                
                try:
                    page.goto("https://dash.cloudflare.com/?to=/:account/pages/new", wait_until="domcontentloaded", timeout=90000)
                    time.sleep(5)  # Wait for page load and any redirects
                except PlaywrightTimeout:
                    print("  Page load timeout - trying alternative approach...")
                    # Try going to main dashboard first
                    page.goto("https://dash.cloudflare.com", wait_until="domcontentloaded", timeout=90000)
                    time.sleep(3)
                    # Then navigate to Pages
                    page.goto("https://dash.cloudflare.com/?to=/:account/pages/new", wait_until="domcontentloaded", timeout=90000)
                    time.sleep(3)
                
                # Check for Cloudflare challenge page
                current_url = page.url.lower()
                page_content = page.content().lower()
                
                if "challenge" in current_url or "just a moment" in page_content or "verify you are human" in page_content:
                    print("\n  CLOUDFLARE SECURITY CHECK DETECTED")
                    print("=" * 60)
                    print(" Cloudflare is asking you to verify you're human")
                    print("   This is normal for automated browsers")
                    print()
                    print(" WHAT TO DO:")
                    print("   1. Look at the browser window")
                    print("   2. Check the checkbox: 'Verify you are human'")
                    print("   3. Wait for the page to redirect (may take 10-30 seconds)")
                    print("   4. The script will automatically continue after verification")
                    print()
                    print("⏳ Waiting for you to complete the verification...")
                    print("   (The script will wait up to 2 minutes)")
                    print("=" * 60)
                    
                    # Wait for challenge to complete - check for redirect away from challenge page
                    challenge_start_time = time.time()
                    max_wait_time = 120  # 2 minutes
                    
                    while time.time() - challenge_start_time < max_wait_time:
                        current_url = page.url.lower()
                        page_content = page.content().lower()
                        
                        # Check if we've passed the challenge
                        if ("challenge" not in current_url and 
                            "just a moment" not in page_content and 
                            "verify you are human" not in page_content and
                            "dash.cloudflare.com" in current_url):
                            print(" Security check passed! Continuing automation...")
                            time.sleep(2)
                            break
                        
                        # Check if we're on login page (challenge passed but need login)
                        if "login" in current_url or "sign-in" in current_url:
                            print(" Security check passed!")
                            print("  Login required - please log in manually")
                            if not self.headless:
                                try:
                                    input("Press Enter after logging in...")
                                except (EOFError, KeyboardInterrupt):
                                    print("Waiting 10 seconds for manual login...")
                                    time.sleep(10)
                                page.reload(wait_until="domcontentloaded")
                                time.sleep(2)
                            break
                        
                        time.sleep(2)  # Check every 2 seconds
                    else:
                        print("  Timeout waiting for security check completion")
                        print("   Please complete the verification manually")
                        if not self.headless:
                            try:
                                input("Press Enter after completing verification...")
                            except (EOFError, KeyboardInterrupt):
                                print("Waiting 10 seconds for manual verification...")
                                time.sleep(10)
                            page.reload(wait_until="domcontentloaded")
                            time.sleep(2)
                
                # Check if logged in (after challenge)
                current_url = page.url.lower()
                if "login" in current_url or "sign-in" in current_url:
                    print("  Login required")
                    print("   Please log in manually in the browser")
                    print("   After logging in, navigate to: https://dash.cloudflare.com/?to=/:account/pages/new")
                    if not self.headless:
                        try:
                            input("Press Enter after logging in and navigating to Pages...")
                        except (EOFError, KeyboardInterrupt):
                            print("Waiting 15 seconds for manual login and navigation...")
                            time.sleep(15)
                        page.reload(wait_until="domcontentloaded")
                        time.sleep(2)
                    else:
                        print(" Cannot handle login in headless mode")
                        return False
                
                # Verify we're on the right page
                current_url = page.url.lower()
                if "pages" not in current_url and "dash.cloudflare.com" in current_url:
                    print("  Not on Pages page - navigating...")
                    page.goto("https://dash.cloudflare.com/?to=/:account/pages/new", wait_until="domcontentloaded", timeout=90000)
                    time.sleep(3)
                
                # Step 2: Connect to Git
                print("\n Step 2: Connecting to GitHub...")
                print("   Looking for 'Connect to Git' or 'Create Project' button...")
                
                # Wait a bit for page to fully load
                time.sleep(3)
                
                # Take screenshot for debugging
                if not self.headless:
                    screenshot_path = Path.home() / "Desktop" / "cloudflare_pages_debug.png"
                    page.screenshot(path=str(screenshot_path))
                    print(f"    Screenshot saved to: {screenshot_path}")
                
                # Try multiple selectors for connect button
                connect_selectors = [
                    "text=Connect to Git",
                    "text=Connect to GitHub", 
                    "text=Create a project",
                    "button:has-text('Connect')",
                    '[data-testid*="connect"]',
                    'a:has-text("Connect")'
                ]
                
                connected = False
                for selector in connect_selectors:
                    try:
                        button = page.locator(selector).first
                        if button.is_visible(timeout=3000):
                            print(f"    Found button: {selector}")
                            button.click()
                            time.sleep(3)
                            connected = True
                            break
                    except PlaywrightTimeout:
                        continue
                
                if not connected:
                    print("  Could not find connect button automatically")
                    print("   The page may already be on the setup form")
                    print("   Or you may need to connect GitHub manually")
                    if not self.headless:
                        try:
                            input("   Press Enter after connecting GitHub (or if already connected)...")
                        except (EOFError, KeyboardInterrupt):
                            print("   Continuing automatically...")
                            time.sleep(3)
                    else:
                        print("   Continuing with assumption that GitHub is connected...")
                        time.sleep(3)
                
                # Try to select GitHub if we clicked connect
                if connected:
                    try:
                        github_selectors = [
                            "text=GitHub",
                            '[data-testid*="github"]',
                            'button:has-text("GitHub")'
                        ]
                        for selector in github_selectors:
                            try:
                                github_btn = page.locator(selector).first
                                if github_btn.is_visible(timeout=2000):
                                    github_btn.click()
                                    time.sleep(2)
                                    break
                            except PlaywrightTimeout:
                                continue
                    except Exception as e:
                        print(f"     Could not select GitHub automatically: {e}")
                        if not self.headless:
                            try:
                                input("   Press Enter after selecting GitHub...")
                            except (EOFError, KeyboardInterrupt):
                                print("   Continuing automatically...")
                                time.sleep(2)
                
                # Step 3: Select Repository
                print("\n Step 3: Selecting repository...")
                try:
                    # Wait for repository list
                    repo_selector = page.locator(f"text={self.repo_name}").first
                    if repo_selector.is_visible(timeout=10000):
                        repo_selector.click()
                        time.sleep(2)
                    else:
                        print(f"  Repository '{self.repo_name}' not found")
                        print("   Available repositories:")
                        repos = page.locator('[data-testid*="repo"]').or_(page.locator("text=/.*/")).all()
                        for repo in repos[:5]:  # Show first 5
                            print(f"     - {repo.text_content()}")
                        print(f"\n   Please select '{self.repo_name}' manually")
                        try:
                            input("   Press Enter after selecting repository...")
                        except (EOFError, KeyboardInterrupt):
                            print("   Continuing automatically...")
                            time.sleep(2)
                except PlaywrightTimeout:
                    print("  Timeout waiting for repository list")
                    print(f"   Please select '{self.repo_name}' manually")
                    try:
                        input("   Press Enter after selecting repository...")
                    except (EOFError, KeyboardInterrupt):
                        print("   Continuing automatically...")
                        time.sleep(2)
                
                # Step 4: Select Branch
                print("\n Step 4: Selecting branch...")
                try:
                    branch_input = page.locator('input[placeholder*="branch"]').or_(page.locator('input[name*="branch"]')).first
                    if branch_input.is_visible(timeout=5000):
                        branch_input.fill(self.branch)
                        time.sleep(1)
                    else:
                        print(f"  Branch selector not found - using default")
                except PlaywrightTimeout:
                    print("  Branch selector not found - using default")
                
                # Step 5: Begin Setup
                print("\n Step 5: Starting setup...")
                try:
                    begin_button = page.locator("text=Begin setup").or_(page.locator("text=Continue")).or_(page.locator("button:has-text('Begin')")).first
                    if begin_button.is_visible(timeout=5000):
                        begin_button.click()
                        time.sleep(3)  # Wait for build configuration page
                    else:
                        print("  Could not find 'Begin setup' button")
                        print("   Please click it manually and press Enter...")
                        try:
                            input()
                        except (EOFError, KeyboardInterrupt):
                            print("   Continuing automatically...")
                            time.sleep(2)
                except PlaywrightTimeout:
                    print("  Timeout - please proceed manually")
                    try:
                        input("   Press Enter after clicking 'Begin setup'...")
                    except (EOFError, KeyboardInterrupt):
                        print("   Continuing automatically...")
                        time.sleep(2)
                
                # Step 6: Configure Build Settings
                print("\n Step 6: Configuring build settings...")
                
                # Project name
                try:
                    project_name_input = page.locator('input[name*="name"]').or_(page.locator('input[placeholder*="project"]')).first
                    if project_name_input.is_visible(timeout=5000):
                        project_name_input.fill(self.project_name)
                        time.sleep(1)
                except PlaywrightTimeout:
                    print("  Project name input not found")
                
                # Build command
                try:
                    build_cmd_input = page.locator('input[name*="build"]').or_(page.locator('textarea[name*="build"]')).or_(page.locator('input[placeholder*="build"]')).first
                    if build_cmd_input.is_visible(timeout=5000):
                        build_cmd_input.fill(self.build_command)
                        time.sleep(1)
                    else:
                        print("  Build command input not found")
                        print(f"   Please enter manually: {self.build_command}")
                except PlaywrightTimeout:
                    print("  Build command input not found")
                    print(f"   Please enter manually: {self.build_command}")
                
                # Output directory
                try:
                    output_dir_input = page.locator('input[name*="output"]').or_(page.locator('input[name*="destination"]')).or_(page.locator('input[placeholder*="output"]')).first
                    if output_dir_input.is_visible(timeout=5000):
                        output_dir_input.fill(self.output_directory)
                        time.sleep(1)
                    else:
                        print("  Output directory input not found")
                        print(f"   Please enter manually: {self.output_directory}")
                except PlaywrightTimeout:
                    print("  Output directory input not found")
                    print(f"   Please enter manually: {self.output_directory}")
                
                # Step 7: Deploy
                print("\n Step 7: Deploying...")
                try:
                    deploy_button = page.locator("text=Save and Deploy").or_(page.locator("text=Deploy")).or_(page.locator("button:has-text('Deploy')")).first
                    if deploy_button.is_visible(timeout=5000):
                        print(" Clicking deploy button...")
                        deploy_button.click()
                        time.sleep(2)
                        
                        # Wait for deployment to start
                        print("⏳ Waiting for deployment to start...")
                        time.sleep(5)
                        
                        # Check for success indicators
                        if page.locator("text=Deployment").or_(page.locator("text=Building")).is_visible(timeout=10000):
                            print(" Deployment started!")
                        else:
                            print("  Deployment status unclear - check dashboard")
                    else:
                        print("  Could not find deploy button")
                        print("   Please click 'Save and Deploy' manually")
                        try:
                            input("   Press Enter after deploying...")
                        except (EOFError, KeyboardInterrupt):
                            print("   Continuing automatically...")
                            time.sleep(2)
                except PlaywrightTimeout:
                    print("  Timeout waiting for deploy button")
                    print("   Please deploy manually")
                    try:
                        input("   Press Enter after deploying...")
                    except (EOFError, KeyboardInterrupt):
                        print("   Continuing automatically...")
                        time.sleep(2)
                
                print("\n" + "=" * 60)
                print(" AUTOMATION COMPLETE")
                print(f" Check deployment: https://dash.cloudflare.com/?to=/:account/pages/view/{self.project_name}")
                print(f" Site URL: https://{self.project_name}.pages.dev")
                print("\n Next step: Bind domain")
                print("   python3 scripts/cloudflare_pages_auto_bind.py \\")
                print("     --domain bravetto.ai --project-name abeone-web")
                
                # Keep browser open for user to verify
                if not self.headless:
                    print("\n⏳ Browser will stay open for 30 seconds for verification...")
                    time.sleep(30)
                
                browser.close()
                return True
                
            except Exception as e:
                print(f"\n Error during automation: {e}")
                print("\n The browser will stay open so you can complete manually")
                if not self.headless:
                    try:
                        input("Press Enter to close browser...")
                    except (EOFError, KeyboardInterrupt):
                        print("Closing browser automatically in 10 seconds...")
                        time.sleep(10)
                return False


def main():
    """CLI Entry Point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automate Cloudflare Pages Setup with Playwright",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--project-name",
        default="abeone-web",
        help="Project name (default: abeone-web)"
    )
    
    parser.add_argument(
        "--repo-name",
        default="AbeOne_Master",
        help="GitHub repository name (default: AbeOne_Master)"
    )
    
    parser.add_argument(
        "--branch",
        default="main",
        help="Production branch (default: main)"
    )
    
    parser.add_argument(
        "--build-command",
        default="cd apps/web && npm install && npm run build",
        help="Build command"
    )
    
    parser.add_argument(
        "--output-directory",
        default="apps/web/out",
        help="Build output directory"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    
    args = parser.parse_args()
    
    automation = CloudflarePagesPlaywrightAutomation(
        project_name=args.project_name,
        repo_name=args.repo_name,
        branch=args.branch,
        build_command=args.build_command,
        output_directory=args.output_directory,
        headless=args.headless
    )
    
    success = automation.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
