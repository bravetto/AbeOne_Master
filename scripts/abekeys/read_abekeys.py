#!/usr/bin/env python3
"""
AbëKEYS Vault Reader
Reads credentials from ~/.abekeys/credentials/ directory

Pattern: VALIDATE → READ → VALIDATE → RETURN
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class AbeKeysReader:
    """Read credentials from AbëKEYS vault."""
    
    def __init__(self, vault_path: Optional[Path] = None):
        """Initialize AbëKEYS reader."""
        if vault_path is None:
            vault_path = Path.home() / ".abekeys" / "credentials"
        self.vault_path = Path(vault_path)
        
    def get_credential(self, service: str) -> Optional[Dict[str, Any]]:
        """
        Get credential for a service.
        
        Args:
            service: Service name (e.g., 'slack', 'runway', 'fireflies')
            
        Returns:
            Dict with credential info or None if not found
        """
        # VALIDATE: Check vault exists
        if not self.vault_path.exists():
            return None
            
        # READ: Load credential file
        cred_file = self.vault_path / f"{service}.json"
        if not cred_file.exists():
            return None
            
        try:
            with open(cred_file, 'r') as f:
                cred_data = json.load(f)
            return cred_data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {cred_file}: {e}")
            return None
    
    def list_services(self) -> list[str]:
        """List all available credential files."""
        if not self.vault_path.exists():
            return []
            
        services = []
        for cred_file in self.vault_path.glob("*.json"):
            services.append(cred_file.stem)
        return sorted(services)
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service."""
        cred = self.get_credential(service)
        if cred:
            return cred.get("api_key") or cred.get("API_KEY") or cred.get("token")
        return None


def main():
    """CLI interface."""
    import sys
    
    reader = AbeKeysReader()
    
    if len(sys.argv) > 1:
        # Get specific service
        service = sys.argv[1]
        cred = reader.get_credential(service)
        
        if cred:
            print(f" Found credentials for {service}:")
            print(json.dumps(cred, indent=2))
            
            # Extract API key if available
            api_key = reader.get_api_key(service)
            if api_key:
                print(f"\n API Key: {api_key[:20]}...")
        else:
            print(f" No credentials found for {service}")
            print(f"   Expected file: ~/.abekeys/credentials/{service}.json")
            print(f"\n   Available services: {', '.join(reader.list_services())}")
    else:
        # List all services
        services = reader.list_services()
        if services:
            print(" Available credentials in AbëKEYS vault:")
            for service in services:
                cred = reader.get_credential(service)
                has_key = "" if reader.get_api_key(service) else ""
                print(f"  {has_key} {service}")
        else:
            print(" No credentials found in AbëKEYS vault")
            print(f"   Vault path: {reader.vault_path}")


if __name__ == "__main__":
    main()

