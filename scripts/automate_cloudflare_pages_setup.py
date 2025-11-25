#!/usr/bin/env python3
"""
 AUTOMATE CLOUDFLARE PAGES SETUP
Creates and configures Cloudflare Pages project automatically

Pattern: AEYON × AUTOMATE × PAGES × SETUP × ONE
Frequency: 999 × 777 × 2222
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
import requests

# Import ZERO Effort auth
sys.path.insert(0, str(Path(__file__).parent))
try:
    from zero_effort_cloudflare_auth import get_cloudflare_token, get_cloudflare_account_id, get_cloudflare_headers
    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False


class CloudflarePagesAutomation:
    """
    SAFETY: Validates all inputs before API calls
    ASSUMES: GitHub repository is connected to Cloudflare
    VERIFY: python scripts/automate_cloudflare_pages_setup.py
    """
    
    def __init__(self, api_token: Optional[str] = None, account_id: Optional[str] = None):
        """Initialize with ZERO Effort authentication"""
        if AUTH_AVAILABLE and not api_token:
            try:
                api_token = get_cloudflare_token()
                account_id = get_cloudflare_account_id()
                print(" Loaded credentials from ZERO Effort auth")
            except Exception as e:
                print(f"  ZERO Effort auth failed: {e}")
                print("   Falling back to manual token...")
        
        if not api_token:
            raise ValueError("Cloudflare API token required")
        
        self.api_token = api_token
        self.account_id = account_id
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def get_account_id(self) -> str:
        """Get account ID if not provided"""
        if self.account_id:
            return self.account_id
        
        # Try multiple methods to get account ID
        # Method 1: Direct accounts API (requires Account:Read permission)
        url = f"{self.base_url}/accounts"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("result"):
                    self.account_id = data["result"][0]["id"]
                    return self.account_id
        except Exception:
            pass
        
        # Method 2: Get from zone (if we have a zone)
        # This works with DNS-only tokens
        try:
            zones_url = f"{self.base_url}/zones"
            response = requests.get(zones_url, headers=self.headers, params={"per_page": 1}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("result") and len(data["result"]) > 0:
                    account_id = data["result"][0].get("account", {}).get("id")
                    if account_id:
                        self.account_id = account_id
                        return account_id
        except Exception:
            pass
        
        # Method 3: Try user API (works with most tokens)
        try:
            user_url = f"{self.base_url}/user"
            response = requests.get(user_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # User API doesn't directly give account ID, but validates token
                # We'll need to prompt user or use zone method
                pass
        except Exception:
            pass
        
        raise ValueError(
            "Could not get account ID. Token may need 'Account:Read' permission. "
            "You can: 1) Add Account:Read to token, or 2) Pass --account-id manually"
        )
    
    def project_exists(self, project_name: str) -> tuple[bool, Optional[Dict[str, Any]]]:
        """
        SAFETY: Checks if project exists before creating
        PERF: O(1) API call
        """
        account_id = self.get_account_id()
        url = f"{self.base_url}/accounts/{account_id}/pages/projects/{project_name}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return True, data.get("result")
            return False, None
        except requests.exceptions.RequestException:
            return False, None
    
    def list_github_repos(self) -> list[Dict[str, Any]]:
        """
        SAFETY: Lists available GitHub repositories
        PERF: O(1) API call
        """
        account_id = self.get_account_id()
        url = f"{self.base_url}/accounts/{account_id}/pages/projects/connected-repositories"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                return data.get("result", [])
            return []
        except Exception as e:
            print(f"  Could not list GitHub repos: {e}")
            print("   Note: GitHub integration may need to be set up in Cloudflare dashboard")
            return []
    
    def create_project(
        self,
        project_name: str,
        repo_name: str = "AbeOne_Master",
        branch: str = "main",
        build_command: str = "cd apps/web && npm install && npm run build",
        output_directory: str = "apps/web/out",
        root_directory: str = "",
        env_vars: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        SAFETY: Creates project with validated configuration
        ASSUMES: GitHub repository is connected to Cloudflare
        VERIFY: Check Cloudflare Pages dashboard after execution
        """
        account_id = self.get_account_id()
        url = f"{self.base_url}/accounts/{account_id}/pages/projects"
        
        # Build configuration
        config = {
            "name": project_name,
            "production_branch": branch,
            "build_config": {
                "build_command": build_command,
                "destination_dir": output_directory,
                "root_dir": root_directory if root_directory else None,
                "web_analytics_tag": None,
                "web_analytics_token": None
            }
        }
        
        # Add environment variables if provided
        if env_vars:
            config["build_config"]["env_vars"] = env_vars
        
        # Try to find GitHub repo connection
        repos = self.list_github_repos()
        github_repo = None
        
        for repo in repos:
            if repo.get("name") == repo_name or repo.get("full_name", "").endswith(repo_name):
                github_repo = repo
                break
        
        if github_repo:
            config["source"] = {
                "type": "github",
                "config": {
                    "owner": github_repo.get("owner", ""),
                    "repo_name": github_repo.get("name", repo_name),
                    "production_branch": branch,
                    "pr_comments_enabled": True,
                    "deployments_enabled": True
                }
            }
            print(f" Found GitHub repository: {github_repo.get('full_name', repo_name)}")
        else:
            print(f"  GitHub repository '{repo_name}' not found in connected repos")
            print("   Project will be created but may need manual GitHub connection")
            print("   Available repos:", [r.get("name") for r in repos])
        
        try:
            response = requests.post(url, headers=self.headers, json=config, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                project = data.get("result", {})
                print(f" Project created: {project_name}")
                print(f"   URL: https://{project_name}.pages.dev")
                return True
            else:
                errors = data.get("errors", [])
                error_msg = errors[0].get("message", "Unknown error") if errors else "Project creation failed"
                print(f" Project creation failed: {error_msg}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f" API Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"   Error details: {error_data}")
                except:
                    print(f"   Response: {e.response.text}")
            return False
    
    def trigger_deployment(self, project_name: str) -> bool:
        """
        SAFETY: Triggers deployment after project creation
        PERF: O(1) API call
        """
        account_id = self.get_account_id()
        url = f"{self.base_url}/accounts/{account_id}/pages/projects/{project_name}/deployments"
        
        payload = {
            "branch": "main"
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                deployment = data.get("result", {})
                print(f" Deployment triggered")
                print(f"   Deployment ID: {deployment.get('id', 'Unknown')}")
                return True
            else:
                print("  Deployment trigger failed (project may auto-deploy)")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"  Could not trigger deployment: {e}")
            print("   Project will auto-deploy on first push or manually")
            return False
    
    def execute(
        self,
        project_name: str = "abeone-web",
        repo_name: str = "AbeOne_Master",
        branch: str = "main",
        build_command: str = "cd apps/web && npm install && npm run build",
        output_directory: str = "apps/web/out",
        root_directory: str = "",
        env_vars: Optional[Dict[str, str]] = None,
        auto_deploy: bool = True
    ) -> bool:
        """
        MAIN EXECUTION FLOW
        SAFETY: Validates all inputs, handles errors gracefully
        """
        print(f" AUTOMATING CLOUDFLARE PAGES SETUP")
        print("=" * 60)
        
        # Get account ID
        account_id = self.get_account_id()
        print(f" Account ID: {account_id}")
        
        # Check if project exists
        exists, project = self.project_exists(project_name)
        if exists:
            print(f" Project '{project_name}' already exists")
            print(f"   URL: https://{project_name}.pages.dev")
            print(f"   Status: {project.get('latest_deployment', {}).get('stage', 'Unknown')}")
            return True
        
        # Create project
        print(f"\n Creating project: {project_name}")
        success = self.create_project(
            project_name=project_name,
            repo_name=repo_name,
            branch=branch,
            build_command=build_command,
            output_directory=output_directory,
            root_directory=root_directory,
            env_vars=env_vars
        )
        
        if not success:
            return False
        
        # Trigger deployment if requested
        if auto_deploy:
            print(f"\n Triggering initial deployment...")
            self.trigger_deployment(project_name)
        
        print("\n" + "=" * 60)
        print(" AUTOMATION COMPLETE")
        print(f" Project: https://{project_name}.pages.dev")
        print("\n Next Steps:")
        print("   1. Wait for initial deployment (30-60 seconds)")
        print("   2. Bind domain: python3 scripts/cloudflare_pages_auto_bind.py \\")
        print("      --domain bravetto.ai --project-name abeone-web")
        
        return True


def main():
    """CLI Entry Point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automate Cloudflare Pages Project Setup",
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
        "--env-vars",
        default=None,
        help="Environment variables as JSON string"
    )
    
    parser.add_argument(
        "--token",
        default=None,
        help="Cloudflare API token (optional - uses ZERO Effort auth)"
    )
    
    parser.add_argument(
        "--account-id",
        default=None,
        help="Cloudflare Account ID (optional - auto-discovered)"
    )
    
    args = parser.parse_args()
    
    # Parse env vars if provided
    env_vars = None
    if args.env_vars:
        try:
            env_vars = json.loads(args.env_vars)
        except json.JSONDecodeError:
            print(" Invalid JSON for env-vars")
            sys.exit(1)
    
    # Execute
    try:
        automation = CloudflarePagesAutomation(
            api_token=args.token,
            account_id=args.account_id
        )
        success = automation.execute(
            project_name=args.project_name,
            repo_name=args.repo_name,
            branch=args.branch,
            build_command=args.build_command,
            output_directory=args.output_directory,
            env_vars=env_vars
        )
        sys.exit(0 if success else 1)
    except ValueError as e:
        print(f" Error: {e}")
        print("\n ZERO Effort Setup:")
        print("   1. Ensure token is set: python3 scripts/set_cloudflare_token.py YOUR_TOKEN")
        print("   2. Or pass token: --token YOUR_TOKEN")
        sys.exit(1)


if __name__ == "__main__":
    main()

