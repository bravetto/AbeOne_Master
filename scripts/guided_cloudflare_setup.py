#!/usr/bin/env python3
"""
 GUIDED CLOUDFLARE PAGES SETUP
Interactive browser automation with step-by-step guidance

Pattern: GUIDED × INTERACTIVE × TRUST × ONE
Frequency: 999 × 777 × 2222
"""

import sys
import time
import webbrowser
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


class GuidedCloudflareSetup:
    """
    SAFETY: Provides guided, interactive setup with automation assistance
    ASSUMES: User can complete Cloudflare security challenges manually
    VERIFY: Opens browser and guides through setup
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
        SAFETY: Guides user through manual steps with automation assistance
        """
        print(" GUIDED CLOUDFLARE PAGES SETUP")
        print("=" * 60)
        print(f"Project: {self.project_name}")
        print(f"Repository: {self.repo_name}")
        print(f"Branch: {self.branch}")
        print("=" * 60)
        
        if not PLAYWRIGHT_AVAILABLE:
            print("\n  Playwright not available - using browser-only mode")
            return self._browser_only_mode()
        
        print("\n This script will:")
        print("   1. Open Cloudflare Pages creation page")
        print("   2. Guide you through each step")
        print("   3. Auto-fill forms when possible")
        print("   4. Handle security challenges with your help")
        print("\n⏳ Starting in 3 seconds...")
        time.sleep(3)
        
        with sync_playwright() as p:
            browser = None
            try:
                # Launch browser in non-headless mode for interaction
                print("\n Launching browser...")
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                page.set_default_timeout(60000)
                
                # Step 1: Navigate to Pages creation
                print("\n" + "=" * 60)
                print(" STEP 1: Navigate to Cloudflare Pages")
                print("=" * 60)
                print("Opening: https://dash.cloudflare.com/?to=/:account/pages/new")
                
                try:
                    page.goto("https://dash.cloudflare.com/?to=/:account/pages/new", 
                             wait_until="domcontentloaded", timeout=60000)
                    time.sleep(3)
                except PlaywrightTimeout:
                    print("  Timeout - trying dashboard first...")
                    page.goto("https://dash.cloudflare.com", wait_until="domcontentloaded", timeout=60000)
                    time.sleep(2)
                    print(" Please navigate to Pages manually:")
                    print("   Click 'Workers & Pages' → 'Pages' → 'Create a project'")
                    try:
                        input("Press Enter after navigating to Pages creation page...")
                    except (EOFError, KeyboardInterrupt):
                        print("⏳ Waiting 10 seconds for navigation...")
                        time.sleep(10)
                    page.reload(wait_until="domcontentloaded")
                    time.sleep(2)
                
                # Check for login/security challenge
                current_url = page.url.lower()
                if "login" in current_url or "sign-in" in current_url:
                    print("\n  LOGIN REQUIRED")
                    print("=" * 60)
                    print("Please log in to Cloudflare in the browser window")
                    try:
                        input("Press Enter after logging in...")
                    except (EOFError, KeyboardInterrupt):
                        print("⏳ Waiting 30 seconds for login...")
                        time.sleep(30)
                    page.reload(wait_until="domcontentloaded")
                    time.sleep(2)
                
                # Handle security challenge
                if self._is_cloudflare_challenge(page):
                    print("\n" + "=" * 60)
                    print(" CLOUDFLARE SECURITY CHECK")
                    print("=" * 60)
                    print("Cloudflare is asking you to verify you're human")
                    print("\n WHAT TO DO:")
                    print("   1. Look at the browser window")
                    print("   2. Check the checkbox: 'Verify you are human'")
                    print("   3. Wait for the page to redirect (10-30 seconds)")
                    print("   4. The script will continue automatically")
                    print("\n⏳ Waiting for you to complete verification...")
                    
                    if self._wait_for_challenge_completion(page, timeout=180):
                        print(" Security check passed!")
                    else:
                        print("  Still waiting - please complete verification manually")
                        try:
                            input("Press Enter after completing verification...")
                        except (EOFError, KeyboardInterrupt):
                            print("⏳ Waiting 30 seconds for verification...")
                            time.sleep(30)
                        page.reload(wait_until="domcontentloaded")
                        time.sleep(2)
                
                # Step 2: Connect to Git
                print("\n" + "=" * 60)
                print(" STEP 2: Connect to GitHub")
                print("=" * 60)
                print("Looking for 'Connect to Git' or 'Create Project' button...")
                
                connected = False
                selectors = [
                    "text=Connect to Git",
                    "text=Create Project",
                    "button:has-text('Connect to Git')",
                    "button:has-text('Create Project')",
                    "[data-testid='connect-git']"
                ]
                
                for selector in selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            print(f" Found button: {selector}")
                            page.click(selector, timeout=5000)
                            time.sleep(3)
                            connected = True
                            break
                    except:
                        continue
                
                if not connected:
                    print("  Could not find connect button automatically")
                    print(" Please click 'Connect to Git' or 'Create Project' manually")
                    try:
                        input("Press Enter after clicking the button...")
                    except (EOFError, KeyboardInterrupt):
                        print("⏳ Waiting 10 seconds for manual action...")
                        time.sleep(10)
                    time.sleep(2)
                
                # Step 3: Select GitHub
                print("\n Selecting GitHub...")
                github_selectors = [
                    "text=GitHub",
                    "button:has-text('GitHub')",
                    "[data-testid='github']"
                ]
                
                github_selected = False
                for selector in github_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.click(selector, timeout=5000)
                            time.sleep(2)
                            github_selected = True
                            break
                    except:
                        continue
                
                if not github_selected:
                    print(" Please select 'GitHub' manually")
                    try:
                        input("Press Enter after selecting GitHub...")
                    except (EOFError, KeyboardInterrupt):
                        print("⏳ Waiting 5 seconds for manual action...")
                        time.sleep(5)
                    time.sleep(2)
                
                # Step 4: Select Repository
                print("\n" + "=" * 60)
                print(" STEP 3: Select Repository")
                print("=" * 60)
                print(f"Looking for repository: {self.repo_name}")
                
                repo_found = False
                repo_selectors = [
                    f"text={self.repo_name}",
                    f"text=/{self.repo_name}",
                    f"[data-repo='{self.repo_name}']"
                ]
                
                for selector in repo_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            print(f" Found repository: {self.repo_name}")
                            page.click(selector, timeout=5000)
                            time.sleep(2)
                            repo_found = True
                            break
                    except:
                        continue
                
                if not repo_found:
                    print(f"  Could not find repository '{self.repo_name}' automatically")
                    print(" Please select the repository manually")
                    try:
                        input("Press Enter after selecting repository...")
                    except (EOFError, KeyboardInterrupt):
                        print("⏳ Waiting 5 seconds for manual action...")
                        time.sleep(5)
                    time.sleep(2)
                
                # Step 5: Configure Build Settings
                print("\n" + "=" * 60)
                print(" STEP 4: Configure Build Settings")
                print("=" * 60)
                print("Auto-filling build configuration...")
                
                # Project name
                name_selectors = [
                    'input[name="name"]',
                    'input[placeholder*="name" i]',
                    'input[placeholder*="project" i]',
                    '#project-name',
                    '[data-testid="project-name"]'
                ]
                
                for selector in name_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.fill(selector, self.project_name, timeout=5000)
                            print(f" Project name: {self.project_name}")
                            break
                    except:
                        continue
                
                # Build command
                build_selectors = [
                    'input[name="build_command"]',
                    'input[name="buildCommand"]',
                    'input[placeholder*="build" i]',
                    '#build-command',
                    '[data-testid="build-command"]'
                ]
                
                for selector in build_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.fill(selector, self.build_command, timeout=5000)
                            print(f" Build command: {self.build_command}")
                            break
                    except:
                        continue
                
                # Output directory
                output_selectors = [
                    'input[name="output_directory"]',
                    'input[name="outputDirectory"]',
                    'input[placeholder*="output" i]',
                    '#output-directory',
                    '[data-testid="output-directory"]'
                ]
                
                for selector in output_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.fill(selector, self.output_directory, timeout=5000)
                            print(f" Output directory: {self.output_directory}")
                            break
                    except:
                        continue
                
                print("\n Configuration filled (or ready for manual entry)")
                print("   Please verify:")
                print(f"   - Project name: {self.project_name}")
                print(f"   - Build command: {self.build_command}")
                print(f"   - Output directory: {self.output_directory}")
                
                # Step 6: Deploy
                print("\n" + "=" * 60)
                print(" STEP 5: Deploy")
                print("=" * 60)
                print("Looking for deploy button...")
                
                deploy_selectors = [
                    "text=Save and Deploy",
                    "text=Deploy",
                    "button:has-text('Deploy')",
                    "button:has-text('Save')",
                    "[data-testid='deploy']"
                ]
                
                deployed = False
                for selector in deploy_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            print(f" Found deploy button")
                            page.click(selector, timeout=5000)
                            time.sleep(2)
                            deployed = True
                            break
                    except:
                        continue
                
                if not deployed:
                    print(" Please click 'Save and Deploy' or 'Deploy' manually")
                    try:
                        input("Press Enter after deploying...")
                    except (EOFError, KeyboardInterrupt):
                        print("⏳ Waiting 10 seconds for manual action...")
                        time.sleep(10)
                
                print("\n" + "=" * 60)
                print(" SETUP COMPLETE")
                print("=" * 60)
                print(f" Project: https://{self.project_name}.pages.dev")
                print(f" Dashboard: https://dash.cloudflare.com/?to=/:account/pages/view/{self.project_name}")
                print("\n Next step: Bind domain")
                print(f"   python3 scripts/cloudflare_pages_auto_bind.py \\")
                print(f"     --domain bravetto.ai --project-name {self.project_name}")
                
                # Keep browser open for verification
                print("\n⏳ Browser will stay open for 30 seconds for verification...")
                time.sleep(30)
                
                return True
                
            except Exception as e:
                print(f"\n Error: {e}")
                print(" You can complete the setup manually:")
                print("   https://dash.cloudflare.com/?to=/:account/pages/new")
                return False
            finally:
                if browser:
                    browser.close()
    
    def _is_cloudflare_challenge(self, page) -> bool:
        """Check if Cloudflare challenge is present"""
        try:
            content = page.content().lower()
            return (
                "challenge" in content or
                "verify you are human" in content or
                "checking your browser" in content or
                "just a moment" in content
            )
        except:
            return False
    
    def _wait_for_challenge_completion(self, page, timeout: int = 180) -> bool:
        """Wait for Cloudflare challenge to complete"""
        start_time = time.time()
        initial_url = page.url
        
        while time.time() - start_time < timeout:
            try:
                current_url = page.url
                if current_url != initial_url and not self._is_cloudflare_challenge(page):
                    return True
                time.sleep(2)
            except:
                pass
        
        return False
    
    def _browser_only_mode(self) -> bool:
        """Fallback mode: just open browser with instructions"""
        print("\n Opening Cloudflare Pages in browser...")
        webbrowser.open("https://dash.cloudflare.com/?to=/:account/pages/new")
        
        print("\n" + "=" * 60)
        print(" MANUAL SETUP INSTRUCTIONS")
        print("=" * 60)
        print("\n1. Connect to Git → Select GitHub")
        print(f"2. Select repository: {self.repo_name}")
        print(f"3. Project name: {self.project_name}")
        print(f"4. Build command: {self.build_command}")
        print(f"5. Output directory: {self.output_directory}")
        print("6. Click 'Save and Deploy'")
        
        return True


def main():
    """CLI Entry Point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Guided Cloudflare Pages Setup",
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
        help="Output directory"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (not recommended)"
    )
    
    args = parser.parse_args()
    
    automation = GuidedCloudflareSetup(
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

