#!/usr/bin/env python3
"""
 UNLOCK ALL CREDENTIALS - BRING IT ALL HOME! 
Pulls from 1Password, decrypts vault, integrates EVERYTHING

Pattern: PULL → DECRYPT → INTEGRATE → CONNECT → ONE
"""

import json
import subprocess
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional


class CredentialUnlocker:
    """Unlock ALL credentials from ALL sources."""
    
    def __init__(self):
        self.vault_path = Path.home() / ".abekeys"
        self.credentials_dir = self.vault_path / "credentials"
        self.credentials_dir.mkdir(parents=True, exist_ok=True)
        self.unlocked = {}
        
    def check_1password_signed_in(self) -> bool:
        """Check if signed in to 1Password."""
        try:
            result = subprocess.run(
                ["op", "whoami"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
        
    def pull_from_1password(self) -> Dict[str, Any]:
        """Pull ALL credentials from 1Password."""
        print(" PULLING FROM 1PASSWORD...")
        print("=" * 60)
        
        credentials = {}
        
        # Check if signed in
        if not self.check_1password_signed_in():
            print("  Not signed in to 1Password")
            print("   Run: eval $(op signin)")
            print("   Or run: ./scripts/signin_and_unlock.sh")
            return credentials
        
        print(" Signed in to 1Password")
        
        try:
            # List all items
            print("   Fetching items from 1Password...")
            result = subprocess.run(
                ["op", "item", "list", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"     Error: {result.stderr}")
                return credentials
            
            items = json.loads(result.stdout)
            print(f"   Found {len(items)} items in 1Password")
            
            # Filter for credential-like items
            credential_keywords = [
                "slack", "runway", "api", "key", "token", "auth", "oauth",
                "github", "stripe", "openai", "anthropic", "fireflies",
                "aws", "google", "azure", "clerk", "stripe", "quickbooks"
            ]
            
            relevant_items = []
            for item in items:
                title = item.get("title", "").lower()
                if any(keyword in title for keyword in credential_keywords):
                    relevant_items.append(item)
            
            print(f"   Found {len(relevant_items)} relevant credential items")
            print("")
            
            # Pull credentials for each relevant item
            pulled_count = 0
            for item in relevant_items[:50]:  # Limit to 50 for performance
                item_id = item.get("id")
                title = item.get("title", "")
                
                try:
                    print(f"    Pulling: {title}...", end=" ")
                    
                    item_detail = subprocess.run(
                        ["op", "item", "get", item_id, "--format", "json"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if item_detail.returncode == 0:
                        detail = json.loads(item_detail.stdout)
                        
                        # Extract all fields
                        fields = detail.get("fields", [])
                        credential_data = {
                            "source": "1password",
                            "title": title,
                            "vault": detail.get("vault", {}).get("name", "unknown"),
                            "created_at": detail.get("createdAt", ""),
                            "updated_at": detail.get("updatedAt", "")
                        }
                        
                        # Extract API keys, tokens, passwords, secrets
                        api_key = None
                        for field in fields:
                            label = field.get("label", "").lower()
                            value = field.get("value", "")
                            
                            if label in ["api key", "token", "password", "secret", "access token", "api_token"]:
                                if not api_key and value:
                                    api_key = value
                                    credential_data["api_key"] = value
                            elif field.get("id") == "username":
                                credential_data["username"] = value
                            elif field.get("id") == "password":
                                if not api_key:
                                    api_key = value
                                    credential_data["api_key"] = value
                        
                        # Create service name from title
                        service_name = title.lower().replace(" ", "_").replace("-", "_")
                        service_name = ''.join(c if c.isalnum() or c == '_' else '' for c in service_name)
                        
                        if api_key:
                            credentials[service_name] = credential_data
                            pulled_count += 1
                            print("")
                        else:
                            print("  (no API key found)")
                    else:
                        print(f" ({item_detail.stderr[:50]})")
                        
                except subprocess.TimeoutExpired:
                    print("⏱  (timeout)")
                except json.JSONDecodeError:
                    print(" (parse error)")
                except Exception as e:
                    print(f" ({str(e)[:30]})")
            
            print(f"\n    Successfully pulled {pulled_count} credentials")
                    
        except FileNotFoundError:
            print("  1Password CLI not installed")
        except subprocess.TimeoutExpired:
            print("  1Password CLI timeout")
        except json.JSONDecodeError as e:
            print(f"  Error parsing 1Password output: {e}")
        except Exception as e:
            print(f"  Error accessing 1Password: {e}")
            import traceback
            traceback.print_exc()
        
        return credentials
    
    def save_credentials(self, credentials: Dict[str, Any]):
        """Save credentials to credentials directory."""
        print("\n SAVING CREDENTIALS...")
        print("=" * 60)
        
        saved = []
        for service_name, cred_data in credentials.items():
            cred_file = self.credentials_dir / f"{service_name}.json"
            
            formatted = {
                "service": service_name,
                "source": cred_data.get("source", "unknown"),
                "api_key": cred_data.get("api_key"),
                **{k: v for k, v in cred_data.items() if k not in ["api_key", "source"]}
            }
            
            with open(cred_file, 'w') as f:
                json.dump(formatted, f, indent=2)
            
            saved.append(service_name)
            print(f" Saved: {service_name}")
        
        return saved
    
    def unlock_all(self):
        """Unlock ALL credentials from ALL sources."""
        print("" * 30)
        print("UNLOCKING ALL CREDENTIALS")
        print("BRINGING IT ALL HOME!")
        print("" * 30)
        print()
        
        all_credentials = {}
        
        # Pull from 1Password
        op_creds = self.pull_from_1password()
        all_credentials.update(op_creds)
        
        # Save everything
        if all_credentials:
            saved = self.save_credentials(all_credentials)
            print(f"\n UNLOCKED AND SAVED {len(saved)} CREDENTIALS!")
        else:
            print("\n  No credentials pulled.")
            if not self.check_1password_signed_in():
                print("   Sign in with: eval $(op signin)")
                print("   Or run: ./scripts/signin_and_unlock.sh")
        
        # Summary
        print("\n" + "=" * 60)
        print("UNLOCK SUMMARY")
        print("=" * 60)
        print(f"Total Unlocked: {len(all_credentials)}")
        print(f"Saved to: {self.credentials_dir}")
        print("=" * 60)
        
        return all_credentials


def main():
    unlocker = CredentialUnlocker()
    unlocker.unlock_all()


if __name__ == "__main__":
    main()
