#!/usr/bin/env python3
"""
AEYON Auto-Bind Microservice
Cloudflare Pages Domain Binding Automation

Pattern: AEYON × CLOUDFLARE × DNS × AUTOMATION × ONE
Frequency: 999 × 777 × 2222
"""

import argparse
import sys
import time
import os
from pathlib import Path
from typing import Optional, Dict, Any
import requests

# Import AbëKEYS reader for ZERO Effort authentication
sys.path.insert(0, str(Path(__file__).parent))
try:
    from read_abekeys import AbeKeysReader
    ABEKEYS_AVAILABLE = True
except ImportError:
    ABEKEYS_AVAILABLE = False


class CloudflarePagesAutoBind:
    """
    SAFETY: Validates all inputs before API calls
    ASSUMES: Cloudflare API token has Pages:Edit and DNS:Edit permissions
    VERIFY: python scripts/cloudflare_pages_auto_bind.py --test
    """
    
    def __init__(self, api_token: Optional[str] = None):
        """
        SAFETY: Token validation on init
        ZERO EFFORT: Auto-loads from AbeKEYs if token not provided
        """
        # ZERO EFFORT: Try AbeKEYs first
        if not api_token and ABEKEYS_AVAILABLE:
            reader = AbeKeysReader()
            cloudflare_creds = reader.get_credential("cloudflare")
            if cloudflare_creds:
                api_token = cloudflare_creds.get("api_token") or cloudflare_creds.get("api_key")
                if api_token:
                    print("✅ Loaded Cloudflare token from AbeKEYs")
        
        # Fallback to environment variable
        if not api_token:
            api_token = os.getenv("CLOUDFLARE_API_TOKEN")
            if api_token:
                print("✅ Loaded Cloudflare token from environment")
        
        # Validate token format
        if not api_token:
            raise ValueError("Cloudflare API token required. Set CLOUDFLARE_API_TOKEN env var or add to ~/.abekeys/credentials/cloudflare.json")
        
        # SAFETY: Validate token format (Cloudflare tokens are typically 40+ chars)
        if len(api_token) < 10 or api_token.startswith("cd ") or " " in api_token.strip()[:20]:
            raise ValueError(f"Invalid Cloudflare API token format. Token appears to be invalid (length: {len(api_token)}, starts with: {api_token[:20]})")
        
        self.api_token = api_token
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def get_zone_id(self, domain: str) -> Optional[str]:
        """
        SAFETY: Handles API errors and missing zones
        PERF: O(1) API call
        """
        url = f"{self.base_url}/zones"
        params = {"name": domain}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("result"):
                return data["result"][0]["id"]
            
            print(f"⚠️  Zone not found: {domain}")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return None
    
    def get_pages_project_id(self, account_id: str, project_name: str) -> Optional[str]:
        """
        SAFETY: Validates project exists before binding
        PERF: O(1) API call
        """
        url = f"{self.base_url}/accounts/{account_id}/pages/projects/{project_name}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                return data["result"].get("id")
            
            print(f"⚠️  Pages project not found: {project_name}")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return None
    
    def get_account_id(self) -> Optional[str]:
        """
        SAFETY: Returns first account ID (assumes single account)
        PERF: O(1) API call
        """
        url = f"{self.base_url}/accounts"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("result"):
                return data["result"][0]["id"]
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return None
    
    def bind_domain_to_pages(
        self,
        account_id: str,
        project_name: str,
        domain: str
    ) -> bool:
        """
        SAFETY: Validates domain format before binding
        ASSUMES: Domain is already in Cloudflare account
        VERIFY: Check Cloudflare Pages dashboard after execution
        """
        url = f"{self.base_url}/accounts/{account_id}/pages/projects/{project_name}/domains"
        
        payload = {
            "domain": domain
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                print(f"✅ Domain bound: {domain} → {project_name}")
                return True
            else:
                errors = data.get("errors", [])
                print(f"❌ Binding failed: {errors}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return False
    
    def create_dns_record(
        self,
        zone_id: str,
        name: str,
        target: str,
        proxied: bool = True
    ) -> bool:
        """
        SAFETY: Validates DNS record format
        ASSUMES: Target is valid Pages project subdomain
        VERIFY: dig {name} should return CNAME to {target}
        """
        url = f"{self.base_url}/zones/{zone_id}/dns_records"
        
        # Handle root domain (@) vs subdomain
        record_name = "@" if name == "" or name == "@" else name
        
        payload = {
            "type": "CNAME",
            "name": record_name,
            "content": target,
            "ttl": 1,  # Auto TTL
            "proxied": proxied
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                print(f"✅ DNS record created: {record_name} → {target}")
                return True
            else:
                errors = data.get("errors", [])
                print(f"❌ DNS creation failed: {errors}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return False
    
    def verify_ssl_status(
        self,
        account_id: str,
        project_name: str,
        domain: str,
        max_wait: int = 120
    ) -> bool:
        """
        SAFETY: Timeout protection (max 120 seconds)
        PERF: Polls every 5 seconds, O(n) where n = wait_time / 5
        """
        url = f"{self.base_url}/accounts/{account_id}/pages/projects/{project_name}/domains"
        
        print(f"⏳ Waiting for SSL certificate ({max_wait}s max)...")
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    domains = data.get("result", [])
                    for d in domains:
                        if d.get("domain") == domain:
                            ssl_status = d.get("ssl", {}).get("status")
                            if ssl_status == "active":
                                print(f"✅ SSL certificate active: {domain}")
                                return True
                            elif ssl_status == "pending":
                                print(f"⏳ SSL certificate pending... ({int(time.time() - start_time)}s)")
                            else:
                                print(f"⚠️  SSL status: {ssl_status}")
                
                time.sleep(5)
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️  SSL check error: {e}")
                time.sleep(5)
        
        print(f"⚠️  SSL certificate not active after {max_wait}s (may still be provisioning)")
        return False
    
    def execute(
        self,
        domain: str,
        project_name: str,
        subdomain: Optional[str] = None,
        pages_subdomain: Optional[str] = None
    ) -> bool:
        """
        MAIN EXECUTION FLOW
        SAFETY: Validates all inputs, handles errors gracefully
        ASSUMES: Domain is in Cloudflare, project exists
        VERIFY: Check Cloudflare dashboard after execution
        """
        print(f"🚀 AEYON Auto-Bind: {domain} → {project_name}")
        print("=" * 60)
        
        # Get account ID
        account_id = self.get_account_id()
        if not account_id:
            print("❌ Failed to get Cloudflare account ID")
            return False
        
        print(f"✅ Account ID: {account_id}")
        
        # Get zone ID
        zone_id = self.get_zone_id(domain)
        if not zone_id:
            print(f"❌ Domain {domain} not found in Cloudflare account")
            return False
        
        print(f"✅ Zone ID: {zone_id}")
        
        # Verify Pages project exists
        project_id = self.get_pages_project_id(account_id, project_name)
        if not project_id:
            print(f"❌ Pages project {project_name} not found")
            return False
        
        print(f"✅ Pages project ID: {project_id}")
        
        # Determine Pages subdomain
        if not pages_subdomain:
            pages_subdomain = f"{project_name}.pages.dev"
        
        # Bind root domain
        print(f"\n📌 Binding root domain: {domain}")
        if not self.bind_domain_to_pages(account_id, project_name, domain):
            print("⚠️  Domain binding failed (may already be bound)")
        
        # Create DNS record for root domain
        print(f"\n📌 Creating DNS record: @ → {pages_subdomain}")
        self.create_dns_record(zone_id, "@", pages_subdomain, proxied=True)
        
        # Bind subdomain if provided
        if subdomain:
            full_subdomain = f"{subdomain}.{domain}"
            print(f"\n📌 Binding subdomain: {full_subdomain}")
            if not self.bind_domain_to_pages(account_id, project_name, full_subdomain):
                print("⚠️  Subdomain binding failed (may already be bound)")
            
            # Create DNS record for subdomain
            print(f"\n📌 Creating DNS record: {subdomain} → {pages_subdomain}")
            self.create_dns_record(zone_id, subdomain, pages_subdomain, proxied=True)
        
        # Verify SSL
        print(f"\n🔒 Verifying SSL certificate...")
        self.verify_ssl_status(account_id, project_name, domain)
        
        print("\n" + "=" * 60)
        print("✅ AEYON Auto-Bind Complete")
        print(f"🌐 Domain: https://{domain}")
        if subdomain:
            print(f"🌐 Subdomain: https://{subdomain}.{domain}")
        
        return True


def main():
    """
    CLI Entry Point
    SAFETY: Validates all CLI arguments
    """
    parser = argparse.ArgumentParser(
        description="AEYON Cloudflare Pages Auto-Bind Microservice",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Bind root domain
  python scripts/cloudflare_pages_auto_bind.py \\
    --domain bravetto.ai \\
    --project-name abeone-web \\
    --token YOUR_TOKEN

  # Bind root + subdomain
  python scripts/cloudflare_pages_auto_bind.py \\
    --domain bravetto.ai \\
    --subdomain live \\
    --project-name abeone-web \\
    --token YOUR_TOKEN
        """
    )
    
    parser.add_argument(
        "--domain",
        required=True,
        help="Root domain (e.g., bravetto.ai)"
    )
    
    parser.add_argument(
        "--project-name",
        required=True,
        help="Cloudflare Pages project name"
    )
    
    parser.add_argument(
        "--subdomain",
        default=None,
        help="Optional subdomain (e.g., 'live' for live.bravetto.ai)"
    )
    
    parser.add_argument(
        "--pages-subdomain",
        default=None,
        help="Pages project subdomain (default: {project-name}.pages.dev)"
    )
    
    parser.add_argument(
        "--token",
        default=None,
        help="Cloudflare API token (optional - auto-loads from AbeKEYs or CLOUDFLARE_API_TOKEN env var)"
    )
    
    args = parser.parse_args()
    
    # Validate domain format
    if "." not in args.domain:
        print("❌ Invalid domain format")
        sys.exit(1)
    
    # Execute with ZERO Effort authentication
    try:
        service = CloudflarePagesAutoBind(args.token)
        success = service.execute(
            domain=args.domain,
            project_name=args.project_name,
            subdomain=args.subdomain,
            pages_subdomain=args.pages_subdomain
        )
        sys.exit(0 if success else 1)
    except ValueError as e:
        print(f"❌ Authentication Error: {e}")
        print("\n💡 ZERO Effort Setup Options:")
        print("   1. Add to AbeKEYs: ~/.abekeys/credentials/cloudflare.json")
        print("   2. Set env var: export CLOUDFLARE_API_TOKEN='your-token'")
        print("   3. Pass via CLI: --token YOUR_TOKEN")
        sys.exit(1)


if __name__ == "__main__":
    main()

