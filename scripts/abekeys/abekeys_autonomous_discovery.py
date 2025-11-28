#!/usr/bin/env python3
"""
AbëKEYs Autonomous API Discovery & Extraction System
Pattern Recognition + Epistemic Search + CLI Automation + Browser Automation

Pattern: ABEKEYS × AUTONOMOUS × DISCOVERY × EXTRACTION × HARVEST × ONE
Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (Abë)
Guardians: AEYON (999 Hz) + META (777 Hz) + Abë (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import os

# Add AbëKEYs to path
sys.path.insert(0, str(Path(__file__).parent))
try:
    from read_abekeys import AbeKeysReader
except ImportError:
    AbeKeysReader = None


@dataclass
class DiscoveredCredential:
    """Discovered credential information"""
    service: str
    credential_type: str  # api_key, access_token, client_id, etc.
    location: str  # file path, env var, password manager, etc.
    value: Optional[str] = None
    confidence: float = 0.0
    source: str = ""  # file, env, 1password, browser, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)


class AbekeysAutonomousDiscovery:
    """Autonomous API discovery and extraction system"""
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.vault_path = Path.home() / ".abekeys" / "credentials"
        self.vault_path.mkdir(parents=True, exist_ok=True)
        self.discovered: List[DiscoveredCredential] = []
        
        # Service patterns for discovery
        self.service_patterns = {
            "shopify": {
                "indicators": ["shopify", "myshopify.com", "shpat_", "X-Shopify-Access-Token"],
                "env_vars": ["SHOPIFY_ACCESS_TOKEN", "SHOPIFY_API_KEY", "SHOPIFY_SHOP_DOMAIN"],
                "file_patterns": ["shopify.json", "shopify.yml", ".shopify"],
                "oauth": "shopify"
            },
            "facebook": {
                "indicators": ["facebook", "fb_", "graph.facebook.com", "FACEBOOK_ACCESS_TOKEN"],
                "env_vars": ["FACEBOOK_ACCESS_TOKEN", "FB_ACCESS_TOKEN", "META_ACCESS_TOKEN"],
                "file_patterns": ["facebook.json", "fb.json", ".facebook"],
                "oauth": "facebook"
            },
            "google_ads": {
                "indicators": ["googleads", "google-ads", "google_ads", "GOOGLE_ADS"],
                "env_vars": ["GOOGLE_ADS_CLIENT_ID", "GOOGLE_ADS_CLIENT_SECRET", "GOOGLE_ADS_REFRESH_TOKEN"],
                "file_patterns": ["google_ads.json", "googleads.json"],
                "oauth": "google"
            },
            "sendgrid": {
                "indicators": ["sendgrid", "SG.", "api.sendgrid.com"],
                "env_vars": ["SENDGRID_API_KEY", "SG_API_KEY"],
                "file_patterns": ["sendgrid.json", ".sendgrid"],
                "oauth": None
            },
            "mailchimp": {
                "indicators": ["mailchimp", "us1.api.mailchimp.com"],
                "env_vars": ["MAILCHIMP_API_KEY", "MC_API_KEY"],
                "file_patterns": ["mailchimp.json", ".mailchimp"],
                "oauth": None
            },
        }
    
    def discover_from_files(self) -> List[DiscoveredCredential]:
        """Discover credentials from files using pattern recognition"""
        discovered = []
        
        # Search common locations
        search_paths = [
            self.workspace_root,
            Path.home() / ".config",
            Path.home() / ".local" / "share",
            Path("/etc"),
        ]
        
        # Search for credential files
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            # Search for .env files
            for env_file in search_path.rglob(".env*"):
                try:
                    creds = self._extract_from_env_file(env_file)
                    discovered.extend(creds)
                except Exception as e:
                    pass
            
            # Search for config files
            for config_file in search_path.rglob("*config*.json"):
                try:
                    creds = self._extract_from_json_file(config_file)
                    discovered.extend(creds)
                except Exception as e:
                    pass
            
            # Search for credential files
            for cred_file in search_path.rglob("*credential*.json"):
                try:
                    creds = self._extract_from_json_file(cred_file)
                    discovered.extend(creds)
                except Exception as e:
                    pass
        
        return discovered
    
    def _extract_from_env_file(self, env_file: Path) -> List[DiscoveredCredential]:
        """Extract credentials from .env file"""
        discovered = []
        
        try:
            with open(env_file, 'r') as f:
                content = f.read()
            
            # Match service patterns
            for service, patterns in self.service_patterns.items():
                for env_var in patterns.get("env_vars", []):
                    pattern = rf"{re.escape(env_var)}\s*=\s*['\"]?([^'\n\"]+)['\"]?"
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        cred = DiscoveredCredential(
                            service=service,
                            credential_type="api_key",
                            location=str(env_file),
                            value=match.group(1),
                            confidence=0.8,
                            source="env_file",
                            metadata={"env_var": env_var}
                        )
                        discovered.append(cred)
        except Exception:
            pass
        
        return discovered
    
    def _extract_from_json_file(self, json_file: Path) -> List[DiscoveredCredential]:
        """Extract credentials from JSON file"""
        discovered = []
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Match service patterns
            for service, patterns in self.service_patterns.items():
                # Check if file matches service indicators
                file_lower = json_file.name.lower()
                if any(indicator in file_lower for indicator in patterns["indicators"]):
                    # Extract credentials
                    cred = DiscoveredCredential(
                        service=service,
                        credential_type="config",
                        location=str(json_file),
                        value=None,  # Will extract from data
                        confidence=0.9,
                        source="json_file",
                        metadata={"data": data}
                    )
                    discovered.append(cred)
        except Exception:
            pass
        
        return discovered
    
    def discover_from_env(self) -> List[DiscoveredCredential]:
        """Discover credentials from environment variables"""
        discovered = []
        
        for service, patterns in self.service_patterns.items():
            for env_var in patterns.get("env_vars", []):
                value = os.getenv(env_var)
                if value:
                    cred = DiscoveredCredential(
                        service=service,
                        credential_type="api_key",
                        location=f"env:{env_var}",
                        value=value,
                        confidence=0.95,
                        source="environment",
                        metadata={"env_var": env_var}
                    )
                    discovered.append(cred)
        
        return discovered
    
    def discover_from_1password(self) -> List[DiscoveredCredential]:
        """Discover credentials from 1Password CLI"""
        discovered = []
        
        try:
            # Check if op CLI is available
            result = subprocess.run(
                ["op", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # Try to list items
                result = subprocess.run(
                    ["op", "item", "list", "--format", "json"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    items = json.loads(result.stdout)
                    for item in items:
                        # Match service patterns
                        for service, patterns in self.service_patterns.items():
                            if any(indicator in item.get("title", "").lower() for indicator in patterns["indicators"]):
                                cred = DiscoveredCredential(
                                    service=service,
                                    credential_type="1password",
                                    location=f"1REPLACE_MEid')}",
                                    value=None,  # Would need to fetch
                                    confidence=0.85,
                                    source="1password",
                                    metadata={"item": item}
                                )
                                discovered.append(cred)
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass
        
        return discovered
    
    def discover_from_browser_storage(self) -> List[DiscoveredCredential]:
        """Discover credentials from browser storage (cookies, localStorage)"""
        discovered = []
        
        # Browser storage locations (macOS)
        browser_paths = [
            Path.home() / "Library" / "Application Support" / "Google" / "Chrome",
            Path.home() / "Library" / "Application Support" / "Brave Browser",
            Path.home() / "Library" / "Application Support" / "Firefox",
        ]
        
        # Note: Browser storage extraction requires browser automation
        # This is a placeholder for browser automation integration
        
        return discovered
    
    def discover_from_cli_tools(self) -> List[DiscoveredCredential]:
        """Discover credentials from CLI tools (aws, gcloud, etc.)"""
        discovered = []
        
        # AWS CLI
        aws_creds = Path.home() / ".aws" / "credentials"
        if aws_creds.exists():
            cred = DiscoveredCredential(
                service="aws",
                credential_type="credentials_file",
                location=str(aws_creds),
                value=None,
                confidence=0.9,
                source="aws_cli",
                metadata={}
            )
            discovered.append(cred)
        
        # Google Cloud CLI
        gcloud_config = Path.home() / ".config" / "gcloud"
        if gcloud_config.exists():
            cred = DiscoveredCredential(
                service="google_cloud",
                credential_type="config",
                location=str(gcloud_config),
                value=None,
                confidence=0.9,
                source="gcloud_cli",
                metadata={}
            )
            discovered.append(cred)
        
        return discovered
    
    def harvest_credentials(self) -> Dict[str, List[DiscoveredCredential]]:
        """Harvest credentials from all sources"""
        print("\n" + "=" * 80)
        print("🔥 ABËKEYS AUTONOMOUS DISCOVERY & HARVESTING")
        print("=" * 80)
        
        harvested = {
            "files": [],
            "environment": [],
            "1password": [],
            "browser": [],
            "cli_tools": []
        }
        
        print("\n🔍 Discovering from files...")
        harvested["files"] = self.discover_from_files()
        print(f"   Found {len(harvested['files'])} credentials in files")
        
        print("\n🔍 Discovering from environment...")
        harvested["environment"] = self.discover_from_env()
        print(f"   Found {len(harvested['environment'])} credentials in environment")
        
        print("\n🔍 Discovering from 1Password...")
        harvested["1password"] = self.discover_from_1password()
        print(f"   Found {len(harvested['1password'])} credentials in 1Password")
        
        print("\n🔍 Discovering from CLI tools...")
        harvested["cli_tools"] = self.discover_from_cli_tools()
        print(f"   Found {len(harvested['cli_tools'])} credentials in CLI tools")
        
        # Flatten all discovered
        all_discovered = []
        for source, creds in harvested.items():
            all_discovered.extend(creds)
        
        self.discovered = all_discovered
        
        return harvested
    
    def store_discovered(self, service_filter: Optional[str] = None) -> int:
        """Store discovered credentials in AbëKEYs vault"""
        stored = 0
        
        print("\n" + "=" * 80)
        print("💾 STORING DISCOVERED CREDENTIALS")
        print("=" * 80)
        
        for cred in self.discovered:
            if service_filter and cred.service != service_filter:
                continue
            
            # Skip if already exists
            cred_file = self.vault_path / f"{cred.service}.json"
            if cred_file.exists():
                print(f"   ⚠️  {cred.service} already exists, skipping")
                continue
            
            # Create credential file
            cred_data = {
                "service": cred.service,
                "source": cred.source,
                "discovered_at": datetime.now().isoformat(),
                "location": cred.location,
                "confidence": cred.confidence,
            }
            
            # Add value if available
            if cred.value:
                cred_data["api_key"] = cred.value
            elif cred.metadata.get("data"):
                # Extract from metadata
                data = cred.metadata["data"]
                if isinstance(data, dict):
                    cred_data.update(data)
            
            # Store
            with open(cred_file, 'w') as f:
                json.dump(cred_data, f, indent=2)
            
            cred_file.chmod(0o600)  # Secure permissions
            
            print(f"   ✅ Stored {cred.service} ({cred.source})")
            stored += 1
        
        return stored
    
    def trigger_emergence(self) -> Dict[str, Any]:
        """Trigger emergence - activate autonomous discovery"""
        print("\n" + "=" * 80)
        print("🚀 TRIGGERING EMERGENCE - AUTONOMOUS DISCOVERY")
        print("=" * 80)
        
        # Harvest credentials
        harvested = self.harvest_credentials()
        
        # Store discovered
        stored = self.store_discovered()
        
        # Summary
        total_discovered = sum(len(creds) for creds in harvested.values())
        
        result = {
            "emergence_triggered": True,
            "timestamp": datetime.now().isoformat(),
            "total_discovered": total_discovered,
            "stored": stored,
            "by_source": {k: len(v) for k, v in harvested.items()},
            "services_found": list(set(c.service for c in self.discovered))
        }
        
        print("\n" + "=" * 80)
        print("✅ EMERGENCE TRIGGERED")
        print("=" * 80)
        print(f"Total Discovered: {total_discovered}")
        print(f"Stored: {stored}")
        print(f"Services Found: {', '.join(result['services_found'])}")
        print("=" * 80)
        
        return result


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AbëKEYs Autonomous Discovery & Extraction"
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        help="Workspace root directory"
    )
    parser.add_argument(
        "--service",
        type=str,
        help="Filter by service name"
    )
    parser.add_argument(
        "--trigger",
        action="store_true",
        help="Trigger emergence (full autonomous discovery)"
    )
    
    args = parser.parse_args()
    
    discovery = AbekeysAutonomousDiscovery(workspace_root=args.workspace_root)
    
    if args.trigger:
        result = discovery.trigger_emergence()
        print(f"\n🎯 Emergence Result: {json.dumps(result, indent=2)}")
    else:
        harvested = discovery.harvest_credentials()
        if args.service:
            stored = discovery.store_discovered(service_filter=args.service)
        else:
            stored = discovery.store_discovered()
        print(f"\n✅ Stored {stored} credentials")


if __name__ == "__main__":
    main()

