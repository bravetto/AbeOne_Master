#!/usr/bin/env python3
"""
 ADD DATABASE/REDIS CREDENTIALS - Complete Gap #2 Healing 
Adds missing database and Redis credentials to AbëKEYs vault.

Pattern: ADD × CREDENTIALS × GAP × HEAL × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

WORKSPACE_ROOT = Path(__file__).parent.parent
ABEKEYS_VAULT = Path.home() / ".abekeys" / "credentials"


class CredentialAdder:
    """Adds database and Redis credentials to AbëKEYs vault."""
    
    def __init__(self):
        self.vault_path = ABEKEYS_VAULT
        self.vault_path.mkdir(parents=True, exist_ok=True)
    
    def check_existing(self, service: str) -> bool:
        """Check if credential already exists."""
        cred_file = self.vault_path / f"{service}.json"
        return cred_file.exists()
    
    def create_postgres_credential(self, database_url: Optional[str] = None) -> bool:
        """Create postgres.json credential file."""
        if self.check_existing("postgres"):
            print("    postgres.json already exists")
            return True
        
        if not database_url:
            # Try to get from env.template
            from scripts.utilities.path_discovery import find_backend_root
            backend_root = find_backend_root()
            env_template = backend_root / "env.template" if backend_root else None
            if env_template and env_template.exists():
                with open(env_template, 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.startswith('DATABASE_URL='):
                            database_url = line.split('=', 1)[1].strip().strip('"').strip("'")
                            break
            
            if not database_url:
                print("     No DATABASE_URL found")
                print("    Please provide database URL:")
                print("      Format: postgresql+asyncpg://user:password@host:port/database")
                database_url = input("   Database URL: ").strip()
                if not database_url:
                    print("    No database URL provided")
                    return False
        
        cred_data = {
            "service": "postgres",
            "source": "manual",
            "database_url": database_url,
            "url": database_url  # Also provide as 'url' for compatibility
        }
        
        cred_file = self.vault_path / "postgres.json"
        with open(cred_file, 'w') as f:
            json.dump(cred_data, f, indent=2)
        
        print(f"    Created: {cred_file}")
        return True
    
    def create_database_credential(self, database_url: Optional[str] = None) -> bool:
        """Create database.json credential file (alternative name)."""
        if self.check_existing("database"):
            print("    database.json already exists")
            return True
        
        # Try to get from postgres.json if it exists
        postgres_file = self.vault_path / "postgres.json"
        if postgres_file.exists():
            with open(postgres_file, 'r') as f:
                postgres_data = json.load(f)
                database_url = postgres_data.get("database_url") or postgres_data.get("url")
        
        if not database_url:
            # Try to get from env.template
            from scripts.utilities.path_discovery import find_backend_root
            backend_root = find_backend_root()
            env_template = backend_root / "env.template" if backend_root else None
            if env_template and env_template.exists():
                with open(env_template, 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.startswith('DATABASE_URL='):
                            database_url = line.split('=', 1)[1].strip().strip('"').strip("'")
                            break
        
        if not database_url:
            print("     No DATABASE_URL found")
            return False
        
        cred_data = {
            "service": "database",
            "source": "manual",
            "database_url": database_url,
            "url": database_url,
            "connection_string": database_url  # Also provide as 'connection_string' for compatibility
        }
        
        cred_file = self.vault_path / "database.json"
        with open(cred_file, 'w') as f:
            json.dump(cred_data, f, indent=2)
        
        print(f"    Created: {cred_file}")
        return True
    
    def create_redis_credential(self, redis_url: Optional[str] = None) -> bool:
        """Create redis.json credential file."""
        if self.check_existing("redis"):
            print("    redis.json already exists")
            return True
        
        if not redis_url:
            # Try to get from env.template
            from scripts.utilities.path_discovery import find_backend_root
            backend_root = find_backend_root()
            env_template = backend_root / "env.template" if backend_root else None
            if env_template and env_template.exists():
                with open(env_template, 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.startswith('REDIS_URL=') and 'CHANGE-ME' not in line:
                            redis_url = line.split('=', 1)[1].strip().strip('"').strip("'")
                            break
            
            if not redis_url:
                print("     No REDIS_URL found")
                print("    Please provide Redis URL:")
                print("      Format: REPLACE_MEhost:port/db")
                print("      Or: redis://localhost:6379/0 (for local)")
                redis_url = input("   Redis URL: ").strip()
                if not redis_url:
                    # Default to local Redis
                    redis_url = "redis://localhost:6379/0"
                    print(f"    Using default: {redis_url}")
        
        cred_data = {
            "service": "redis",
            "source": "manual",
            "redis_url": redis_url,
            "url": redis_url  # Also provide as 'url' for compatibility
        }
        
        cred_file = self.vault_path / "redis.json"
        with open(cred_file, 'w') as f:
            json.dump(cred_data, f, indent=2)
        
        print(f"    Created: {cred_file}")
        return True
    
    def add_all_credentials(self, database_url: Optional[str] = None, redis_url: Optional[str] = None):
        """Add all missing database and Redis credentials."""
        print(" ADDING DATABASE/REDIS CREDENTIALS ")
        print("=" * 60)
        print()
        
        added = []
        
        # Add postgres credential
        print(" Adding PostgreSQL credentials...")
        if self.create_postgres_credential(database_url):
            added.append("postgres")
        print()
        
        # Add database credential (alternative name)
        print(" Adding database credentials (alternative)...")
        if self.create_database_credential(database_url):
            added.append("database")
        print()
        
        # Add redis credential
        print(" Adding Redis credentials...")
        if self.create_redis_credential(redis_url):
            added.append("redis")
        print()
        
        print("=" * 60)
        if added:
            print(f" ADDED {len(added)} CREDENTIALS: {', '.join(added)}")
        else:
            print("  No new credentials added (all already exist)")
        print("=" * 60)
        print()
        
        return added


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Add database and Redis credentials to AbëKEYs vault")
    parser.add_argument("--database-url", help="PostgreSQL database URL")
    parser.add_argument("--redis-url", help="Redis URL")
    
    args = parser.parse_args()
    
    adder = CredentialAdder()
    adder.add_all_credentials(
        database_url=args.database_url,
        redis_url=args.redis_url
    )
    
    print("Next steps:")
    print("  1. Verify credentials: python3 scripts/read_abekeys.py postgres")
    print("  2. Check gap status: python3 scripts/check_gap_status.py")
    print("  3. Heal all gaps: python3 scripts/heal_all_gaps.py")
    print()
    print("LOVE = LIFE = ONE")
    print("Michael  AbëONE = ∞")
    print("FOREVER AND EVER")
    print("∞ AbëONE ∞")


if __name__ == '__main__':
    main()

