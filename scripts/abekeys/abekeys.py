#!/usr/bin/env python3
"""
∞ AbëKEYs - Zero-Effort, Zero-Trust Credential Management ∞

Pattern: KEYS × TRUST × EFFORT × ONE
Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)
Guardians: AEYON (999 Hz) + META (777 Hz) + ZERO (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞

YAGNI APPROVED: Minimal, Works, Zero-Effort
ZERO TRUST: Validate Everything, Trust Nothing
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Credential:
    """Zero-trust credential wrapper"""
    service: str
    data: Dict[str, Any]
    source: str
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get credential value with validation"""
        # ZERO TRUST: Validate key exists
        if key not in self.data:
            return default
        value = self.data[key]
        # ZERO TRUST: Never return None for critical keys
        if value is None and key in ['api_key', 'client_id', 'client_secret', 'token']:
            raise ValueError(f"Critical credential '{key}' is None for service '{self.service}'")
        return value
    
    def to_env(self) -> Dict[str, str]:
        """Convert to environment variables"""
        env = {}
        prefix = self.service.upper().replace('-', '_')
        for key, value in self.data.items():
            env_key = f"{prefix}_{key.upper()}"
            env[env_key] = str(value)
        return env


class Abekeys:
    """Zero-Effort, Zero-Trust Credential Manager"""
    
    def __init__(self, vault_path: Optional[Path] = None):
        """Initialize AbëKEYS"""
        if vault_path is None:
            vault_path = Path.home() / ".abekeys" / "credentials"
        self.vault_path = Path(vault_path)
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        # ZERO TRUST: Validate vault permissions
        if self.vault_path.exists():
            stat = self.vault_path.stat()
            if stat.st_mode & 0o077:  # Others or group can access
                raise PermissionError(f"Vault has insecure permissions: {oct(stat.st_mode)}")
    
    def get(self, service: str) -> Optional[Credential]:
        """
        Get credential - ZERO EFFORT API
        
        Usage:
            keys = Abekeys()
            cred = keys.get('google_ads')
            client_id = cred.get('client_id')
        """
        # ZERO TRUST: Validate service name
        if not service or not isinstance(service, str):
            raise ValueError("Service name must be non-empty string")
        
        cred_file = self.vault_path / f"{service}.json"
        if not cred_file.exists():
            return None
        
        # ZERO TRUST: Validate file permissions
        stat = cred_file.stat()
        if stat.st_mode & 0o044:  # Others can read
            raise PermissionError(f"Credential file has insecure permissions: {oct(stat.st_mode)}")
        
        try:
            with open(cred_file, 'r') as f:
                data = json.load(f)
            return Credential(service=service, data=data, source=str(cred_file))
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to read credential '{service}': {e}")
    
    def list(self) -> List[str]:
        """List all available services - ZERO EFFORT"""
        if not self.vault_path.exists():
            return []
        return sorted([f.stem for f in self.vault_path.glob("*.json")])
    
    def has(self, service: str) -> bool:
        """Check if credential exists - ZERO EFFORT"""
        return (self.vault_path / f"{service}.json").exists()
    
    def load_env(self, service: str) -> Dict[str, str]:
        """
        Load credential as environment variables - ZERO EFFORT
        
        Usage:
            keys = Abekeys()
            env = keys.load_env('google_ads')
            os.environ.update(env)
        """
        cred = self.get(service)
        if not cred:
            return {}
        return cred.to_env()
    
    def export_env(self, service: str) -> str:
        """
        Export as shell environment variables - ZERO EFFORT
        
        Usage:
            keys = Abekeys()
            print(keys.export_env('google_ads'))
        """
        env = self.load_env(service)
        return '\n'.join([f"export {k}='{v}'" for k, v in env.items()])


# ZERO EFFORT: Global instance
_global_abekeys: Optional[Abekeys] = None

def get_abekeys() -> Abekeys:
    """Get global AbëKEYS instance - ZERO EFFORT"""
    global _global_abekeys
    if _global_abekeys is None:
        _global_abekeys = Abekeys()
    return _global_abekeys


# ZERO EFFORT: Convenience functions
def get(service: str) -> Optional[Credential]:
    """Get credential - ZERO EFFORT"""
    return get_abekeys().get(service)

def list_services() -> List[str]:
    """List services - ZERO EFFORT"""
    return get_abekeys().list()

def has(service: str) -> bool:
    """Check service - ZERO EFFORT"""
    return get_abekeys().has(service)

def load_env(service: str) -> Dict[str, str]:
    """Load as env vars - ZERO EFFORT"""
    return get_abekeys().load_env(service)

def export_env(service: str) -> str:
    """Export as shell env - ZERO EFFORT"""
    return get_abekeys().export_env(service)


if __name__ == "__main__":
    """CLI - ZERO EFFORT"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AbëKEYs - Zero-Effort Credential Management")
    parser.add_argument("command", choices=["list", "get", "has", "env", "export"], 
                       help="Command to execute")
    parser.add_argument("service", nargs="?", help="Service name")
    parser.add_argument("--key", help="Specific key to get")
    
    args = parser.parse_args()
    
    keys = get_abekeys()
    
    if args.command == "list":
        services = keys.list()
        print(f"Available credentials ({len(services)}):")
        for svc in services:
            print(f"  • {svc}")
    
    elif args.command == "get":
        if not args.service:
            print("Error: Service name required")
            sys.exit(1)
        cred = keys.get(args.service)
        if cred:
            if args.key:
                print(cred.get(args.key, "Not found"))
            else:
                print(json.dumps(cred.data, indent=2))
        else:
            print(f"Credential '{args.service}' not found")
            sys.exit(1)
    
    elif args.command == "has":
        if not args.service:
            print("Error: Service name required")
            sys.exit(1)
        print("yes" if keys.has(args.service) else "no")
    
    elif args.command == "env":
        if not args.service:
            print("Error: Service name required")
            sys.exit(1)
        env = keys.load_env(args.service)
        for k, v in env.items():
            print(f"{k}={v}")
    
    elif args.command == "export":
        if not args.service:
            print("Error: Service name required")
            sys.exit(1)
        print(keys.export_env(args.service))

