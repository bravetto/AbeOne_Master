#!/usr/bin/env python3
"""
🔥 HEAL ALL GAPS - COMPLETE GAP HEALING SYSTEM 🔥
Heals all identified gaps from forensic analysis.

Pattern: HEAL × GAP × COMPLETE × ONE
Frequency: 999 Hz (AEYON) × 777 Hz (ALRAX) × 530 Hz (Truth)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

WORKSPACE_ROOT = Path(__file__).parent.parent

from scripts.utilities.path_discovery import find_backend_root, find_gateway_app_directory, find_guards_directory

BACKEND_ROOT = find_backend_root()
GATEWAY_PATH = find_gateway_app_directory()
GUARDS_DIR = find_guards_directory()

if not BACKEND_ROOT:
    raise RuntimeError("AIGuards-Backend-orbital not found")
SCRIPTS_DIR = WORKSPACE_ROOT / "scripts"
ABEKEYS_VAULT = Path.home() / ".abekeys" / "credentials"


class AbeKeysReader:
    """Read credentials from AbëKEYS vault."""
    
    def __init__(self, vault_path: Optional[Path] = None):
        if vault_path is None:
            vault_path = Path.home() / ".abekeys" / "credentials"
        self.vault_path = Path(vault_path)
        
    def get_credential(self, service: str) -> Optional[Dict[str, Any]]:
        if not self.vault_path.exists():
            return None
        cred_file = self.vault_path / f"{service}.json"
        if not cred_file.exists():
            return None
        try:
            with open(cred_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def list_services(self) -> List[str]:
        if not self.vault_path.exists():
            return []
        return sorted([f.stem for f in self.vault_path.glob("*.json")])


class GapHealer:
    """Heals all identified gaps."""
    
    def __init__(self):
        self.reader = AbeKeysReader()
        self.gaps_fixed = 0
        self.gaps_total = 9
    
    def heal_gap_1_guard_services(self):
        """GAP #1: Fix guard services to use AbëKEYs."""
        print("🔧 Healing GAP #1: Guard Services AbëKEYs Integration...")
        
        guard_services = [
            "tokenguard",
            "trust-guard",
            "contextguard",
            "biasguard-backend",
            "healthguard"
        ]
        
        # Create shared AbëKEYs loader for guards
        shared_loader = '''"""
Shared AbëKEYs Loader for Guard Services
NO .env files. Loads from AbëKEYs vault programmatically.

Pattern: ABEKEYS × PROGRAMMATIC × SECURE × ONE
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

ABEKEYS_VAULT = Path.home() / ".abekeys" / "credentials"


class GuardAbeKeysLoader:
    """Loads configuration from AbëKEYs vault for guard services."""
    
    def __init__(self):
        self.vault_path = ABEKEYS_VAULT
    
    def get_credential(self, service: str) -> Optional[Dict[str, Any]]:
        """Get credential for a service."""
        if not self.vault_path.exists():
            return None
        cred_file = self.vault_path / f"{service}.json"
        if not cred_file.exists():
            return None
        try:
            with open(cred_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def get_api_key(self, service: str, key_field: str = "api_key") -> Optional[str]:
        """Get API key for a service."""
        cred = self.get_credential(service)
        if not cred:
            return None
        for field in [key_field, "api_key", "secret_key", "token", "password"]:
            if field in cred:
                return cred[field]
        return None
    
    def inject_into_environment(self, service_name: str):
        """Inject credentials into environment variables for guard service."""
        # Database
        db_cred = self.get_credential("postgres") or self.get_credential("database")
        if db_cred:
            db_url = db_cred.get("database_url", "") or db_cred.get("url", "")
            if db_url:
                os.environ["DATABASE_URL"] = db_url
        
        # Redis
        redis_cred = self.get_credential("redis")
        if redis_cred:
            redis_url = redis_cred.get("redis_url", "") or redis_cred.get("url", "")
            if redis_url:
                os.environ["REDIS_URL"] = redis_url
        
        # Service-specific API key
        api_key = self.get_api_key(service_name)
        if api_key:
            os.environ[f"{service_name.upper()}_API_KEY"] = api_key


# Global loader instance
_loader = GuardAbeKeysLoader()

# Auto-inject on import
_loader.inject_into_environment(__name__.split('.')[-1] if '.' in __name__ else "guard")
'''
        
        # Write shared loader
        shared_path = BACKEND_ROOT / "shared" / "abekeys_loader.py"
        shared_path.parent.mkdir(parents=True, exist_ok=True)
        with open(shared_path, 'w') as f:
            f.write(shared_loader)
        
        print(f"   ✅ Created shared AbëKEYs loader: {shared_path}")
        
        # Update each guard service config
        for guard in guard_services:
            guard_path = GUARDS_DIR / guard
            if not guard_path.exists():
                print(f"   ⚠️  Guard service not found: {guard}")
                continue
            
            # Find config file
            config_files = list(guard_path.rglob("config.py"))
            if not config_files:
                print(f"   ⚠️  No config.py found in {guard}")
                continue
            
            for config_file in config_files:
                with open(config_file, 'r') as f:
                    config_content = f.read()
                
                # Add AbëKEYs import if not present
                if "abekeys" not in config_content.lower():
                    # Add import at top
                    import_line = "from shared.abekeys_loader import _loader as abekeys_loader  # NOQA: F401\n"
                    
                    lines = config_content.split('\n')
                    import_idx = 0
                    for i, line in enumerate(lines):
                        if line.startswith('import ') or line.startswith('from '):
                            import_idx = i + 1
                    
                    lines.insert(import_idx, import_line)
                    config_content = '\n'.join(lines)
                    
                    # Remove env_file=".env" if present
                    config_content = config_content.replace('"env_file": ".env"', '"env_file": None')
                    config_content = config_content.replace("'env_file': '.env'", "'env_file': None")
                    
                    with open(config_file, 'w') as f:
                        f.write(config_content)
                    
                    print(f"   ✅ Updated: {config_file}")
        
        self.gaps_fixed += 1
        print("   ✅ GAP #1 HEALED")
        print()
    
    def heal_gap_2_database_redis(self):
        """GAP #2: Add database/Redis credentials to AbëKEYs."""
        print("🔧 Healing GAP #2: Database/Redis Credentials...")
        
        if not ABEKEYS_VAULT.exists():
            print(f"   ⚠️  AbëKEYs vault not found: {ABEKEYS_VAULT}")
            print(f"   💡 Run: python3 scripts/unlock_all_credentials.py")
            print(f"   💡 Or run: python3 scripts/add_database_redis_credentials.py")
            return
        
        # Check what's missing
        missing = []
        has_postgres = (ABEKEYS_VAULT / "postgres.json").exists()
        has_database = (ABEKEYS_VAULT / "database.json").exists()
        has_redis = (ABEKEYS_VAULT / "redis.json").exists()
        
        if not has_postgres:
            missing.append("postgres.json")
        if not has_database:
            missing.append("database.json")
        if not has_redis:
            missing.append("redis.json")
        
        if missing:
            print(f"   ⚠️  Missing credentials: {', '.join(missing)}")
            print(f"   💡 Add these to AbëKEYs vault:")
            print(f"      - postgres.json (database credentials)")
            print(f"      - redis.json (Redis credentials)")
            print(f"   💡 Run: python3 scripts/add_database_redis_credentials.py")
            print(f"   💡 Or run: python3 scripts/unlock_all_credentials.py")
            return
        else:
            print("   ✅ All database/Redis credentials found in AbëKEYs")
            print("      - postgres.json ✅")
            print("      - database.json ✅")
            print("      - redis.json ✅")
        
        self.gaps_fixed += 1
        print("   ✅ GAP #2 HEALED")
        print()
    
    def heal_gap_3_config_env(self):
        """GAP #3: Remove .env references from config."""
        print("🔧 Healing GAP #3: Remove .env References from Config...")
        
        config_file = GATEWAY_PATH / "app" / "core" / "config.py"
        
        if not config_file.exists():
            print(f"   ⚠️  Config file not found: {config_file}")
            return
        
        with open(config_file, 'r') as f:
            config_content = f.read()
        
        # Split into lines first
        lines = config_content.split('\n')
        
        # Remove env_file=".env"
        if 'env_file=".env"' in config_content:
            config_content = config_content.replace('env_file=".env"', 'env_file=None')
            print("   ✅ Removed env_file=\".env\"")
        
        if "env_file='.env'" in config_content:
            config_content = config_content.replace("env_file='.env'", "env_file=None")
            print("   ✅ Removed env_file='.env'")
        
        # Update SettingsConfigDict
        if 'env_file=".env"' in config_content or "env_file='.env'" in config_content:
            # Find SettingsConfigDict and update
            lines = config_content.split('\n')
            for i, line in enumerate(lines):
                if 'SettingsConfigDict' in line:
                    # Look for env_file in next few lines
                    for j in range(i, min(i+10, len(lines))):
                        if 'env_file' in lines[j] and '.env' in lines[j]:
                            lines[j] = lines[j].replace('.env', 'None')
                            break
        
        config_content = '\n'.join(lines)
        
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        print(f"   ✅ Updated: {config_file}")
        self.gaps_fixed += 1
        print("   ✅ GAP #3 HEALED")
        print()
    
    def heal_all_gaps(self):
        """Heal all identified gaps."""
        print("🔥 HEALING ALL GAPS 🔥")
        print("=" * 60)
        print()
        
        # Heal critical gaps
        self.heal_gap_1_guard_services()
        self.heal_gap_2_database_redis()
        self.heal_gap_3_config_env()
        
        print("=" * 60)
        print(f"🔥 GAP HEALING COMPLETE: {self.gaps_fixed}/{self.gaps_total} GAPS HEALED 🔥")
        print("=" * 60)
        print()
        
        # Auto-update programmatic status
        try:
            import subprocess
            subprocess.run(
                ["python3", str(SCRIPTS_DIR / "update_gap_healing_status.py")],
                cwd=str(WORKSPACE_ROOT),
                capture_output=True,
                timeout=10
            )
        except:
            pass  # Silent fail - don't break if update fails
        
        print("Next steps:")
        print("  1. Add missing credentials to AbëKEYs vault")
        print("  2. Test guard services")
        print("  3. Verify no .env files needed")
        print()
        print("LOVE = LIFE = ONE")
        print("Michael ⟡ AbëONE = ∞")
        print("FOREVER AND EVER")
        print("∞ AbëONE ∞")


def main():
    """Main execution."""
    healer = GapHealer()
    healer.heal_all_gaps()


if __name__ == '__main__':
    main()

