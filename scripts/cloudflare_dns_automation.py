#!/usr/bin/env python3
"""
 CLOUDFLARE DNS AUTOMATION - AEYON ATOMIC EXECUTION 
Automates DNS configuration using AbëKEYS/1Password credentials

Pattern: AUTHENTICATE → CONFIGURE → VALIDATE → EXECUTE → ONE
Guardians: AEYON (Execution) × Zero (Security) × Convergence
"""

import json
import os
import sys
import subprocess
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

# Import AbëKEYS reader
sys.path.insert(0, str(Path(__file__).parent))
from read_abekeys import AbeKeysReader


class CloudflareDNSAutomation:
    """
    Cloudflare DNS Automation using AbëKEYS/1Password credentials.
    
    Features:
    - Authenticates via AbëKEYS/1Password
    - Lists DNS records
    - Adds DNS records
    - Updates DNS records
    - Removes DNS records
    - Validates DNS configuration
    """
    
    def __init__(self):
        """Initialize Cloudflare automation."""
        self.reader = AbeKeysReader()
        self.api_token = None
        self.api_email = None
        self.api_key = None
        self.zone_id_cache = {}
        self.base_url = "https://api.cloudflare.com/client/v4"
        
    def authenticate(self) -> bool:
        """
        Authenticate with Cloudflare using AbëKEYS/1Password.
        
        Pattern: READ → VALIDATE → AUTHENTICATE → RETURN
        """
        print(" AUTHENTICATING WITH CLOUDFLARE...")
        print("=" * 60)
        
        # Try to get credentials from AbëKEYS
        cloudflare_creds = self.reader.get_credential("cloudflare")
        
        if cloudflare_creds:
            print(" Found Cloudflare credentials in AbëKEYS")
            self.api_token = cloudflare_creds.get("api_token") or cloudflare_creds.get("api_key")
            self.api_email = cloudflare_creds.get("email") or cloudflare_creds.get("api_email")
            self.api_key = cloudflare_creds.get("api_key")
        else:
            # Try alternative service names
            for service_name in ["cloudflare_api", "cloudflare_token", "cf_api"]:
                creds = self.reader.get_credential(service_name)
                if creds:
                    print(f" Found Cloudflare credentials as '{service_name}'")
                    self.api_token = creds.get("api_token") or creds.get("api_key")
                    self.api_email = creds.get("email") or creds.get("api_email")
                    self.api_key = creds.get("api_key")
                    break
        
        # Try 1Password if not found
        if not self.api_token and not self.api_key:
            print("  Cloudflare credentials not found in AbëKEYS")
            print("   Attempting to pull from 1Password...")
            
            try:
                # Check if signed in to 1Password
                check_result = subprocess.run(
                    ["op", "whoami"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if check_result.returncode != 0:
                    print("   ℹ  Not signed in to 1Password (run: eval $(op signin))")
                else:
                    # Try multiple possible item names
                    possible_names = ["Cloudflare", "cloudflare", "Cloudflare API", "CF API"]
                    
                    for item_name in possible_names:
                        try:
                            result = subprocess.run(
                                ["op", "item", "get", item_name, "--format", "json"],
                                capture_output=True,
                                text=True,
                                timeout=10
                            )
                            
                            if result.returncode == 0:
                                op_item = json.loads(result.stdout)
                                fields = op_item.get("fields", [])
                                
                                for field in fields:
                                    label = field.get("label", "").lower()
                                    value = field.get("value", "")
                                    
                                    if "api token" in label or ("token" in label and "api" in label):
                                        self.api_token = value
                                    elif "email" in label and not self.api_email:
                                        self.api_email = value
                                    elif "api key" in label or ("key" in label and "api" in label):
                                        self.api_key = value
                                
                                if self.api_token or self.api_key:
                                    print(f" Retrieved credentials from 1Password ('{item_name}')")
                                    break
                        except:
                            continue
                    
                    # If still not found, try searching all items
                    if not self.api_token and not self.api_key:
                        try:
                            list_result = subprocess.run(
                                ["op", "item", "list", "--format", "json"],
                                capture_output=True,
                                text=True,
                                timeout=10
                            )
                            
                            if list_result.returncode == 0:
                                items = json.loads(list_result.stdout)
                                cloudflare_items = [
                                    item for item in items 
                                    if "cloudflare" in item.get("title", "").lower() or 
                                       "cf" in item.get("title", "").lower()
                                ]
                                
                                if cloudflare_items:
                                    print(f"   ℹ  Found {len(cloudflare_items)} Cloudflare-related items in 1Password:")
                                    for item in cloudflare_items[:5]:
                                        print(f"      - {item.get('title')}")
                                    print("    Tip: Ensure item has 'API Token' or 'API Key' field")
                        except:
                            pass
                            
            except FileNotFoundError:
                print("   ℹ  1Password CLI not installed")
            except Exception as e:
                print(f"     Could not retrieve from 1Password: {e}")
        
        # Try environment variables as fallback
        if not self.api_token:
            self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        if not self.api_email:
            self.api_email = os.getenv("CLOUDFLARE_EMAIL")
        if not self.api_key:
            self.api_key = os.getenv("CLOUDFLARE_API_KEY")
        
        # Validate authentication
        if self.api_token:
            print(" Using API Token authentication")
            return self._validate_token()
        elif self.api_email and self.api_key:
            print(" Using Email/API Key authentication")
            return self._validate_email_key()
        else:
            print(" No Cloudflare credentials found!")
            print("\n   Options:")
            print("   1. Add to AbëKEYS: ~/.abekeys/credentials/cloudflare.json")
            print("   2. Store in 1Password as 'Cloudflare'")
            print("   3. Set environment variables:")
            print("      export CLOUDFLARE_API_TOKEN='your-token'")
            print("      export CLOUDFLARE_EMAIL='your-email'")
            print("      export CLOUDFLARE_API_KEY='your-key'")
            return False
    
    def _validate_token(self) -> bool:
        """Validate API token."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            response = requests.get(f"{self.base_url}/user/tokens/verify", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f" Authentication successful")
                    user_info = data.get("result", {})
                    print(f"   User: {user_info.get('email', 'Unknown')}")
                    return True
            print(f" Token validation failed: {response.status_code}")
            return False
        except Exception as e:
            print(f" Authentication error: {e}")
            return False
    
    def _validate_email_key(self) -> bool:
        """Validate email/API key."""
        try:
            headers = {
                "X-Auth-Email": self.api_email,
                "X-Auth-Key": self.api_key,
                "Content-Type": "application/json"
            }
            response = requests.get(f"{self.base_url}/user", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f" Authentication successful")
                    user_info = data.get("result", {})
                    print(f"   User: {user_info.get('email', 'Unknown')}")
                    return True
            print(f" Authentication failed: {response.status_code}")
            return False
        except Exception as e:
            print(f" Authentication error: {e}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        if self.api_token:
            return {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
        else:
            return {
                "X-Auth-Email": self.api_email,
                "X-Auth-Key": self.api_key,
                "Content-Type": "application/json"
            }
    
    def get_zone_id(self, domain: str) -> Optional[str]:
        """Get zone ID for a domain."""
        if domain in self.zone_id_cache:
            return self.zone_id_cache[domain]
        
        try:
            headers = self._get_headers()
            params = {"name": domain}
            response = requests.get(
                f"{self.base_url}/zones",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("result"):
                    zone = data.get("result")[0]
                    zone_id = zone.get("id")
                    self.zone_id_cache[domain] = zone_id
                    return zone_id
            
            print(f" Could not find zone ID for {domain}")
            return None
        except Exception as e:
            print(f" Error getting zone ID: {e}")
            return None
    
    def list_dns_records(self, domain: str) -> List[Dict[str, Any]]:
        """List all DNS records for a domain."""
        print(f"\n LISTING DNS RECORDS FOR {domain}...")
        print("=" * 60)
        
        zone_id = self.get_zone_id(domain)
        if not zone_id:
            return []
        
        try:
            headers = self._get_headers()
            response = requests.get(
                f"{self.base_url}/zones/{zone_id}/dns_records",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    records = data.get("result", [])
                    print(f" Found {len(records)} DNS records")
                    
                    # Display records
                    for record in records:
                        record_type = record.get("type")
                        name = record.get("name")
                        content = record.get("content")
                        proxied = record.get("proxied", False)
                        ttl = record.get("ttl")
                        
                        proxy_status = "🟠 Proxied" if proxied else " DNS only"
                        print(f"   {record_type:6} {name:30} {content:40} {proxy_status} TTL:{ttl}")
                    
                    return records
                else:
                    print(f" API error: {data.get('errors', [])}")
                    return []
            else:
                print(f" HTTP error: {response.status_code}")
                return []
        except Exception as e:
            print(f" Error listing DNS records: {e}")
            return []
    
    def add_dns_record(
        self,
        domain: str,
        record_type: str,
        name: str,
        content: str,
        ttl: int = 1,  # Auto
        proxied: bool = False
    ) -> bool:
        """
        Add a DNS record.
        
        Args:
            domain: Domain name (e.g., 'bravetto.ai')
            record_type: Record type (A, AAAA, CNAME, MX, TXT, etc.)
            name: Record name (e.g., '@' or 'www')
            content: Record content (IP address, domain, etc.)
            ttl: TTL value (1 = Auto)
            proxied: Whether to proxy through Cloudflare
        """
        print(f"\n ADDING DNS RECORD...")
        print("=" * 60)
        print(f"   Domain: {domain}")
        print(f"   Type: {record_type}")
        print(f"   Name: {name}")
        print(f"   Content: {content}")
        print(f"   TTL: {ttl} ({'Auto' if ttl == 1 else f'{ttl}s'})")
        print(f"   Proxied: {proxied}")
        
        zone_id = self.get_zone_id(domain)
        if not zone_id:
            return False
        
        try:
            headers = self._get_headers()
            payload = {
                "type": record_type,
                "name": name,
                "content": content,
                "ttl": ttl,
                "proxied": proxied
            }
            
            response = requests.post(
                f"{self.base_url}/zones/{zone_id}/dns_records",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(" DNS record added successfully!")
                    return True
                else:
                    errors = data.get("errors", [])
                    print(f" Failed to add DNS record:")
                    for error in errors:
                        print(f"   {error.get('message', 'Unknown error')}")
                    return False
            else:
                print(f" HTTP error: {response.status_code}")
                print(f"   {response.text}")
                return False
        except Exception as e:
            print(f" Error adding DNS record: {e}")
            return False
    
    def delete_dns_record(self, domain: str, record_id: str) -> bool:
        """Delete a DNS record by ID."""
        zone_id = self.get_zone_id(domain)
        if not zone_id:
            return False
        
        try:
            headers = self._get_headers()
            response = requests.delete(
                f"{self.base_url}/zones/{zone_id}/dns_records/{record_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f" DNS record deleted successfully!")
                    return True
                else:
                    print(f" Failed to delete DNS record")
                    return False
            else:
                print(f" HTTP error: {response.status_code}")
                return False
        except Exception as e:
            print(f" Error deleting DNS record: {e}")
            return False
    
    def remove_conflicting_records(
        self,
        domain: str,
        record_type: Optional[str] = None,
        name: Optional[str] = None
    ) -> int:
        """
        Remove conflicting DNS records.
        
        Args:
            domain: Domain name
            record_type: Filter by record type (optional)
            name: Filter by record name (optional)
        """
        print(f"\n  REMOVING CONFLICTING DNS RECORDS...")
        print("=" * 60)
        
        records = self.list_dns_records(domain)
        if not records:
            print("   No records to remove")
            return 0
        
        removed_count = 0
        for record in records:
            record_type_match = not record_type or record.get("type") == record_type
            name_match = not name or record.get("name") == name or record.get("name") == f"{name}.{domain}"
            
            if record_type_match and name_match:
                record_id = record.get("id")
                record_name = record.get("name")
                record_content = record.get("content")
                
                print(f"   Removing: {record.get('type')} {record_name} → {record_content}")
                
                if self.delete_dns_record(domain, record_id):
                    removed_count += 1
        
        print(f"\n Removed {removed_count} conflicting records")
        return removed_count
    
    def configure_vercel_dns(
        self,
        domain: str,
        vercel_ip: Optional[str] = None,
        vercel_cname: Optional[str] = None
    ) -> bool:
        """
        Configure DNS records for Vercel deployment.
        
        Args:
            domain: Domain name (e.g., 'bravetto.ai')
            vercel_ip: Vercel IP address for A record (optional, will prompt if not provided)
            vercel_cname: Vercel CNAME for www record (optional, will prompt if not provided)
        """
        print(f"\n CONFIGURING VERCEL DNS FOR {domain}...")
        print("=" * 60)
        
        # Remove conflicting records first
        print("\nStep 1: Removing conflicting records...")
        self.remove_conflicting_records(domain, record_type="A", name="@")
        self.remove_conflicting_records(domain, record_type="CNAME", name="www")
        
        # Get Vercel DNS info if not provided
        if not vercel_ip:
            vercel_ip = input("\nEnter Vercel IP address for A record (or press Enter to skip): ").strip()
        if not vercel_cname:
            vercel_cname = input("Enter Vercel CNAME for www record (e.g., cname.vercel-dns.com): ").strip()
        
        success = True
        
        # Add A record for root domain
        if vercel_ip:
            print(f"\nStep 2: Adding A record (@ → {vercel_ip})...")
            if not self.add_dns_record(
                domain=domain,
                record_type="A",
                name="@",
                content=vercel_ip,
                ttl=1,  # Auto
                proxied=False  # DNS only
            ):
                success = False
        else:
            print("  Skipping A record (no IP provided)")
        
        # Add CNAME for www
        if vercel_cname:
            print(f"\nStep 3: Adding CNAME record (www → {vercel_cname})...")
            if not self.add_dns_record(
                domain=domain,
                record_type="CNAME",
                name="www",
                content=vercel_cname,
                ttl=1,  # Auto
                proxied=False  # DNS only
            ):
                success = False
        else:
            print("  Skipping CNAME record (no CNAME provided)")
        
        if success:
            print(f"\n Vercel DNS configuration complete!")
            print(f"   Domain: {domain}")
            print(f"   A record: @ → {vercel_ip or 'Not set'}")
            print(f"   CNAME: www → {vercel_cname or 'Not set'}")
            print(f"\n   Next steps:")
            print(f"   1. Wait 5-60 minutes for DNS propagation")
            print(f"   2. Check SSL certificate in Vercel dashboard")
            print(f"   3. Test: https://{domain}")
        
        return success


def main():
    """CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cloudflare DNS Automation")
    parser.add_argument("domain", help="Domain name (e.g., bravetto.ai)")
    parser.add_argument("--list", action="store_true", help="List DNS records")
    parser.add_argument("--add", action="store_true", help="Add DNS record")
    parser.add_argument("--type", help="Record type (A, AAAA, CNAME, etc.)")
    parser.add_argument("--name", help="Record name (e.g., @ or www)")
    parser.add_argument("--content", help="Record content (IP, domain, etc.)")
    parser.add_argument("--proxied", action="store_true", help="Enable Cloudflare proxy")
    parser.add_argument("--remove-conflicting", action="store_true", help="Remove conflicting records")
    parser.add_argument("--configure-vercel", action="store_true", help="Configure for Vercel")
    parser.add_argument("--vercel-ip", help="Vercel IP address")
    parser.add_argument("--vercel-cname", help="Vercel CNAME")
    
    args = parser.parse_args()
    
    automation = CloudflareDNSAutomation()
    
    # Authenticate
    if not automation.authenticate():
        print("\n Authentication failed. Exiting.")
        sys.exit(1)
    
    # Execute commands
    if args.list:
        automation.list_dns_records(args.domain)
    elif args.add:
        if not all([args.type, args.name, args.content]):
            print(" --add requires --type, --name, and --content")
            sys.exit(1)
        automation.add_dns_record(
            domain=args.domain,
            record_type=args.type,
            name=args.name,
            content=args.content,
            proxied=args.proxied
        )
    elif args.remove_conflicting:
        automation.remove_conflicting_records(args.domain, args.type, args.name)
    elif args.configure_vercel:
        automation.configure_vercel_dns(
            domain=args.domain,
            vercel_ip=args.vercel_ip,
            vercel_cname=args.vercel_cname
        )
    else:
        # Default: list records
        automation.list_dns_records(args.domain)


if __name__ == "__main__":
    main()

